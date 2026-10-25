#!/usr/bin/env python3
"""
Screenshot a served slide at real wall-clock times, to see what moves.

    tools/slide_frames.py modules/devconf-2026-freestyle --slide 6
    tools/slide_frames.py <module> --slide 6 --at 1,2,3,4 --strip
    tools/slide_frames.py <module> --slide 5 --url http://localhost:8080/

A PNG render cannot show animation: marp's image export and a headless
--screenshot both freeze the page before an animated SVG or WebP has moved,
so a still that shows every glyph at its start proves nothing either way.
This drives the browser through the DevTools protocol instead and waits in
real time between shots, against the served deck, which is the one that gets
presented. The served deck also differs from a render in what it allows: it
runs marp without --html, so this is the check that a slide survives that.

By default it starts its own server on a spare port through
render_slides.py --serve and stops it afterwards; --url points it at one
that is already running. Frames go to build/<module>/frames/, and --strip
stacks them into one image. Needs the websocket-client package
(pip install --user websocket-client, or apt install python3-websocket);
--strip also needs ImageMagick.
"""

import argparse
import base64
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moduleinfo import repo_root   # noqa: E402
from render_slides import deck_name, find_browser   # noqa: E402

try:
    import websocket
except ImportError:
    sys.exit("websocket-client is required: pip install --user websocket-client "
             "(or apt install python3-websocket)")

WIDTH, HEIGHT = 1920, 1080
SERVER_WAIT_S = 120      # the first serve fetches marp-cli through npx


def spare_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for(url, timeout):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
            return True
        except Exception:
            time.sleep(0.5)
    return False


class DevTools:
    """Just enough of the DevTools protocol to navigate and screenshot."""

    def __init__(self, browser):
        self.port = spare_port()
        self.profile = tempfile.mkdtemp(prefix="slide-frames-")
        # --remote-allow-origins: Chromium rejects a DevTools websocket from
        # any origin not named here, with a 403 that says so.
        self.proc = subprocess.Popen(
            [browser, "--headless=new", "--no-sandbox",
             "--remote-debugging-port=%d" % self.port,
             "--remote-allow-origins=http://127.0.0.1:%d" % self.port,
             "--window-size=%d,%d" % (WIDTH, HEIGHT),
             "--user-data-dir=%s" % self.profile, "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        page = None
        for _ in range(100):
            try:
                tabs = json.load(urllib.request.urlopen(
                    "http://127.0.0.1:%d/json" % self.port, timeout=2))
                page = next(t for t in tabs if t["type"] == "page")
                break
            except Exception:
                time.sleep(0.1)
        if page is None:
            self.close()
            sys.exit("the browser did not open a DevTools port")
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=30)
        self.n = 0

    def call(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                if "error" in msg:
                    raise RuntimeError("%s: %s" % (method, msg["error"]))
                return msg.get("result", {})

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)


def start_server(root, module_dir, port):
    """render_slides.py --serve in its own process group, so it can be stopped whole."""
    cmd = [sys.executable, os.path.join(root, "tools", "render_slides.py"),
           module_dir, "--serve", "--port", str(port)]
    return subprocess.Popen(cmd, cwd=root, stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=True)


def stop_server(proc):
    try:
        os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(timeout=10)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("module", help="module directory")
    ap.add_argument("--slide", type=int, required=True, help="slide number, from 1")
    ap.add_argument("--at", default="1,2,3",
                    help="seconds after the slide loads to take each shot "
                         "(default 1,2,3)")
    ap.add_argument("--url", help="use a deck server that is already running, "
                                  "e.g. http://localhost:8080/")
    ap.add_argument("--strip", action="store_true",
                    help="also stack the frames into one image")
    args = ap.parse_args()

    try:
        times = sorted(float(t) for t in args.at.split(","))
    except ValueError:
        ap.error("--at takes comma-separated seconds, e.g. 1,2.5,4")

    root = repo_root()
    module_dir = os.path.abspath(args.module)
    if not os.path.isfile(os.path.join(module_dir, "slides.md")):
        sys.exit("no slides.md in %s" % args.module)
    browser, where = find_browser()
    if not browser:
        sys.exit("no browser found; set CHROME_PATH")
    print("  browser: %s (%s)" % (browser, where))

    server = None
    base = args.url
    if not base:
        port = spare_port()
        base = "http://localhost:%d/" % port
        server = start_server(root, module_dir, port)
        if not wait_for(base, SERVER_WAIT_S):
            stop_server(server)
            sys.exit("the deck server did not come up on %s" % base)
    url = "%s%s.md#%d" % (base if base.endswith("/") else base + "/",
                          deck_name(module_dir), args.slide)

    rel = os.path.relpath(module_dir, root)
    out_dir = os.path.join(root, "build", rel, "frames")
    os.makedirs(out_dir, exist_ok=True)
    frames = []
    dt = None
    try:
        dt = DevTools(browser)
        dt.call("Page.enable")
        dt.call("Emulation.setDeviceMetricsOverride", width=WIDTH, height=HEIGHT,
                deviceScaleFactor=1, mobile=False)
        dt.call("Page.navigate", url=url)
        t0 = time.time()
        for t in times:
            while time.time() - t0 < t:
                time.sleep(0.01)
            shot = dt.call("Page.captureScreenshot", format="png")
            name = os.path.join(out_dir, "slide%02d_t%05.2f.png" % (args.slide, t))
            with open(name, "wb") as f:
                f.write(base64.b64decode(shot["data"]))
            frames.append(name)
            print("  %.2fs  %s" % (t, os.path.relpath(name, root)))
    finally:
        if dt:
            dt.close()
        if server:
            stop_server(server)

    if args.strip and frames:
        if shutil.which("convert") is None:
            print("  no convert on PATH; --strip needs ImageMagick")
            return 1
        strip = os.path.join(out_dir, "slide%02d-strip.png" % args.slide)
        subprocess.run(["convert"] + frames + ["-resize", "50%", "-append", strip], check=True)
        print("  strip: %s" % os.path.relpath(strip, root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
