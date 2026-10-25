#!/usr/bin/env python3
"""
Render a module's slides.md with marp-cli.

    tools/render_slides.py series/01-fast-rates/01-the-400hz-problem
    tools/render_slides.py <module> --format pdf
    tools/render_slides.py <module> --format png --scale 2
    tools/render_slides.py <module> --contact
    tools/render_slides.py <module> --serve
    tools/render_slides.py <module> <module>/v1 --serve   two decks on one home page
    tools/render_slides.py <module> --watch
    tools/render_slides.py --all --format pdf

Output goes to build/<module path>/ which is gitignored. marp-cli is fetched
through npx, so nothing needs installing; set MARP_CLI_SPEC to pin a different
version and MARP_NPX to point at a different npx. --contact additionally needs
montage, from ImageMagick.

The browser is pinned rather than discovered, because which browser renders
decides which fonts the deck gets. Set CHROME_PATH to choose one yourself.
"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moduleinfo import repo_root, discover, load_module   # noqa: E402
from script_check import narration_by_slide, split_frontmatter   # noqa: E402

MARP_SPEC = os.environ.get("MARP_CLI_SPEC", "@marp-team/marp-cli@4.5.0")
NPX = os.environ.get("MARP_NPX", "npx")

FORMAT_FLAGS = {
    "html": ["--html"],
    "pdf": ["--pdf"],
    "pptx": ["--pptx"],
    "png": ["--images", "png"],
    "notes": ["--pdf", "--pdf-notes"],
}

FORMAT_EXT = {"html": "html", "pdf": "pdf", "pptx": "pptx",
              "png": "png", "notes": "pdf"}

# Contact sheet tiles, sized by the longest edge. The box is measured off the
# frames rather than fixed, because montage uses it as the cell size: a square
# box around a 16:9 slide leaves half of every cell empty and strands the
# label a long way under its slide.
CONTACT_EDGE = 640
CONTACT_ACROSS = 4

FRAME_GLOB = "%s.[0-9][0-9][0-9].png"

# Browsers to pin, in order of preference. Left to itself marp-cli discovers
# one, and under WSL it finds Windows Chrome, which renders with Windows fonts:
# the deck comes out in Segoe UI rather than Inter and every line is a
# different width, so the same deck overflows on one machine and not another.
# CHROME_PATH in the environment overrides all of this.
CHROME_CANDIDATES = ("chromium", "chromium-browser", "google-chrome",
                     "google-chrome-stable")
PLAYWRIGHT_CHROMIUM = "~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome"


def find_browser():
    """Pick one browser deliberately, so a deck renders the same way twice.

    Returns (path, where it came from), or (None, None) to leave marp to its
    own discovery. The playwright cache is last because it is a cache: it is
    what is on this machine rather than something the repo installed, and
    apt-installing chromium would take precedence from then on.
    """
    pinned = os.environ.get("CHROME_PATH")
    if pinned:
        return pinned, "CHROME_PATH"
    for exe in CHROME_CANDIDATES:
        found = shutil.which(exe)
        if found:
            return found, exe
    cached = glob.glob(os.path.expanduser(PLAYWRIGHT_CHROMIUM))
    if cached:
        def build(path):
            n = re.search(r"chromium-(\d+)", path)
            return int(n.group(1)) if n else 0
        return max(cached, key=build), "playwright cache"
    return None, None


def deck_name(module_dir, shorts=False, overlays=False):
    name = os.path.basename(module_dir)
    if shorts:
        name += "-shorts"
    elif overlays:
        name += "-overlays"
    return name


def clear_frames(out_dir, name):
    """Drop numbered PNGs from an earlier render.

    marp writes one PNG per slide but never removes the ones a shorter deck
    has stopped producing. That matters twice over: edit_pack.py resolves
    [SLIDE n] to these by number, and the contact sheet montages all of them,
    so a leftover frame reads as a real slide in both.
    """
    for f in glob.glob(os.path.join(out_dir, FRAME_GLOB % name)):
        os.remove(f)


def render(root, module_dir, fmt, scale, watch, server, shorts=False,
           overlays=False):
    if shorts and overlays:
        sys.exit("--shorts and --overlays are mutually exclusive")
    if overlays:
        slides = os.path.join(module_dir, "overlays.md")
        theme = os.path.join(root, "themes", "fossuav-overlay.css")
        missing = "no overlays.md (run tools/edit_pack.py first)"
    elif shorts:
        slides = os.path.join(module_dir, "shorts", "cards.md")
        theme = os.path.join(root, "themes", "fossuav-vertical.css")
        missing = "no shorts/cards.md"
    else:
        slides = os.path.join(module_dir, "slides.md")
        theme = os.path.join(root, "themes", "fossuav.css")
        missing = "no slides.md"

    if not os.path.exists(slides):
        print("  skipped %s: %s"
              % (os.path.relpath(module_dir, root), missing))
        return None

    rel = os.path.relpath(module_dir, root)
    out_dir = os.path.join(root, "build", rel)
    os.makedirs(out_dir, exist_ok=True)

    name = deck_name(module_dir, shorts, overlays)
    if fmt == "png":
        clear_frames(out_dir, name)
        out = os.path.join(out_dir, "%s.png" % name)
    elif fmt == "notes":
        out = os.path.join(out_dir, "%s-notes.pdf" % name)
    else:
        out = os.path.join(out_dir, "%s.%s" % (name, FORMAT_EXT[fmt]))

    cmd = [NPX, "--yes", MARP_SPEC, slides,
           "--theme", theme,
           "--allow-local-files",
           "--output", out]
    cmd += FORMAT_FLAGS[fmt]
    if scale and fmt in ("png", "pdf", "notes"):
        cmd += ["--image-scale", str(scale)]
    if watch:
        cmd += ["--watch"]
    if server:
        cmd += ["--preview"]

    print("  %s -> %s" % (os.path.relpath(slides, root),
                          os.path.relpath(out, root)))
    result = subprocess.run(cmd, cwd=root)
    return result.returncode


PRESENT_DIR = os.path.join("build", "present")


def deck_slug(module_dir, meta):
    """Flat, sortable name for a module on the home page.

    marp's index lists file names, so this is what you read when choosing a
    deck: the series without its ordering prefix, then the module directory.
    """
    series = str(meta.get("series") or "")
    series = re.sub(r"^\d+-", "", series)
    base = os.path.basename(module_dir)
    parent = os.path.dirname(module_dir)
    if not meta and os.path.exists(os.path.join(parent, "module.yaml")):
        # a deck kept inside a module, such as an earlier version of it, is
        # named after the module so "v1" does not stand alone on the home page
        base = "%s-%s" % (os.path.basename(parent), base)
    return "%s-%s" % (series, base) if series else base


def build_present(root, module_dir, out_dir, meta):
    """Copy the deck into the serve root with the script's narration as notes.

    Generated into build/, never back into the module: slides.md stays hand
    written. Marp turns any HTML comment that is not a directive into a
    presenter note, which is what the notes pane reads, so the script ends up
    on the second screen while the deck is on the first.

    Returns the file name written, or None if there is no deck to copy.
    """
    slides = os.path.join(module_dir, "slides.md")
    if not os.path.exists(slides):
        return None

    with open(slides, "r", encoding="utf-8") as f:
        text = f.read()
    meta_block, body, _ = split_frontmatter(text)

    script = os.path.join(module_dir, "script.md")
    notes = narration_by_slide(script) if os.path.exists(script) else {}

    chunks = body.split("\n---\n")
    for i, chunk in enumerate(chunks, start=1):
        lines = notes.get(i)
        if not lines:
            continue
        # The blank line before the comment is load bearing. A slide ending in
        # </div> has an HTML block still open, and markdown keeps consuming
        # lines into it until a blank one, so a comment placed straight after
        # the div is swallowed as literal HTML and never becomes a note.
        # A stray --> would close the comment early.
        safe = [ln.replace("-->", "--&gt;") for ln in lines]
        chunks[i - 1] = "%s\n\n<!--\n%s\n-->\n" % (chunk.rstrip(),
                                                   "\n\n".join(safe))

    deck = "\n---\n".join(chunks)

    stem = deck_slug(module_dir, meta)
    assets = os.path.join(module_dir, "assets")
    if os.path.isdir(assets):
        link = os.path.join(out_dir, "%s-assets" % stem)
        if os.path.islink(link):
            os.remove(link)
        if not os.path.exists(link):
            os.symlink(os.path.relpath(assets, out_dir), link)
        # The deck moved, so its relative asset paths have to move with it.
        deck = re.sub(r"(?<=[(\"'])assets/", "%s-assets/" % stem, deck)

    head = "---\n%s---\n\n" % _dump_frontmatter(meta_block) if meta_block else ""
    name = "%s.md" % stem
    with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
        f.write(head + deck)
    return name


def _dump_frontmatter(meta_block):
    return "".join("%s: %s\n" % (k, _yaml_scalar(v))
                   for k, v in meta_block.items())


def _yaml_scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str) and (":" in value or value != value.strip()):
        return '"%s"' % value.replace('"', '\\"')
    return value


def present_root(root, targets):
    """Build the flat directory that --serve serves.

    One markdown file per module, so marp's index page is a list of every
    module rather than a directory tree to click down through. Rebuilt each
    time, so a renamed or deleted module stops appearing on the home page.
    """
    out = os.path.join(root, PRESENT_DIR)
    os.makedirs(out, exist_ok=True)
    for stale in glob.glob(os.path.join(out, "*")):
        if os.path.islink(stale) or stale.endswith(".md"):
            os.remove(stale)

    built = []
    for module_dir in targets:
        try:
            meta = load_module(module_dir)
        except Exception:
            meta = {}
        name = build_present(root, module_dir, out, meta)
        if name:
            built.append(name)
        else:
            print("  skipped %s: no slides.md"
                  % os.path.relpath(module_dir, root))

    for name in sorted(built):
        print("  %s" % name)
    return out, built


def serve(root, serve_dir, count=1, port=None):
    """Serve the decks through marp's own server, which is the real player.

    The built HTML is already a deck the arrow keys drive, but presenter view
    and the slide overview sync between windows through localStorage, and a
    browser restricts that on a file:// URL. Served over http they both work,
    which is the difference between a page of slides and something you can
    present from. Reloads on save, so this is also the way to write a deck.
    """
    cmd = [NPX, "--yes", MARP_SPEC, "--server",
           os.path.relpath(serve_dir, root),
           "--theme", os.path.join(root, "themes", "fossuav.css"),
           "--allow-local-files"]
    env = dict(os.environ)
    if port:
        env["PORT"] = str(port)

    if count > 1:
        print("  the home page lists all %d modules; pick one" % count)
    else:
        print("  the home page has the one deck on it")
    print("  arrows, PageUp/PageDown or Space to move; f for fullscreen")
    print("  p for presenter view: the script, the next slide and a timer")
    print("  Ctrl-C to stop")
    # marp holds the terminal from here, and these lines are the instructions
    # for using it, so they are no use arriving when the server is shut down.
    sys.stdout.flush()
    return subprocess.run(cmd, cwd=root, env=env).returncode


def tile_box(frame, edge=CONTACT_EDGE):
    """Scale a frame's own aspect down to fit a box `edge` on the long side."""
    out = subprocess.run(["identify", "-format", "%w %h", frame],
                         capture_output=True, text=True)
    try:
        w, h = (int(v) for v in out.stdout.split()[:2])
    except ValueError:
        return "%dx%d" % (edge, edge)
    if w >= h:
        return "%dx%d" % (edge, round(edge * h / w))
    return "%dx%d" % (round(edge * w / h), edge)


def contact_sheet(root, module_dir, name, across=CONTACT_ACROSS):
    """Montage the rendered PNGs into one sheet for an at-a-glance pass.

    branding.md sets a consistency test for thumbnails: put them side by side
    and remake the one that does not belong. This is that test for a deck, and
    it also catches a slide that overflows. Tiles are scaled well down, since
    a sheet you have to pan around does not get looked at.
    """
    for tool in ("montage", "identify"):
        if shutil.which(tool) is None:
            print("  no %s on PATH; the contact sheet needs ImageMagick" % tool)
            return 1

    rel = os.path.relpath(module_dir, root)
    out_dir = os.path.join(root, "build", rel)
    frames = sorted(glob.glob(os.path.join(out_dir, FRAME_GLOB % name)))
    if not frames:
        print("  no PNG frames to montage; render with --format png first")
        return 1

    sheet = os.path.join(out_dir, "%s-contact.png" % name)
    cmd = ["montage", "-background", "#0b0e13", "-fill", "#94a2b1",
           "-pointsize", "22"]
    for f in frames:
        n = re.search(r"\.(\d+)\.png$", f)
        cmd += ["-label", n.group(1).lstrip("0") if n else "", f]
    cmd += ["-tile", "%dx" % across,
            "-geometry", "%s+8+8" % tile_box(frames[0]), sheet]
    rc = subprocess.run(cmd, cwd=root).returncode
    if rc == 0:
        print("  contact sheet: %s  (%d slides, %d across)"
              % (os.path.relpath(sheet, root), len(frames), across))
    return rc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("module", nargs="*", help="module directories")
    ap.add_argument("--all", action="store_true", help="render every module")
    ap.add_argument("--format", default=None, choices=sorted(FORMAT_FLAGS),
                    help="output format (default html; 'notes' is a PDF with "
                         "presenter notes)")
    ap.add_argument("--scale", type=int, default=2,
                    help="image scale for png/pdf (default 2, so 2560x1440)")
    ap.add_argument("--watch", action="store_true", help="rebuild on change")
    ap.add_argument("--preview", action="store_true", help="open marp preview")
    ap.add_argument("--shorts", action="store_true",
                    help="render shorts/cards.md vertically at 1080x1920 "
                         "instead of the 16:9 deck")
    ap.add_argument("--overlays", action="store_true",
                    help="render overlays.md as transparent 1920x1080 cards "
                         "for the edit; use --scale 1")
    ap.add_argument("--contact", action="store_true",
                    help="also build a contact sheet of every slide, for an "
                         "at-a-glance consistency pass. Implies --format png")
    ap.add_argument("--serve", action="store_true",
                    help="serve the deck as a player: arrow keys, fullscreen, "
                         "and p for presenter view with notes and a timer")
    ap.add_argument("--port", type=int,
                    help="port for --serve (default marp's own, 8080)")
    args = ap.parse_args()

    if args.serve:
        for flag in ("contact", "watch", "preview"):
            if getattr(args, flag):
                ap.error("--serve runs its own live-reloading player, so it "
                         "cannot be combined with --%s" % flag)
        for flag in ("shorts", "overlays"):
            if getattr(args, flag):
                ap.error("--serve presents the 16:9 deck, so it cannot be "
                         "combined with --%s" % flag)
        if args.format:
            ap.error("--serve does not write a file, so --format has no effect")

    fmt = args.format or "html"
    if args.contact:
        if args.format and args.format != "png":
            ap.error("--contact montages the slide PNGs, so it cannot be "
                     "combined with --format %s" % args.format)
        fmt = "png"
        if args.watch or args.preview:
            ap.error("--contact needs a render that finishes, so it cannot be "
                     "combined with --watch or --preview")

    if not args.module and not args.all:
        ap.error("give a module directory or --all")

    browser, where = find_browser()
    if browser:
        os.environ["CHROME_PATH"] = browser
        print("  browser: %s (%s)" % (browser, where))
    else:
        print("  no local browser found, so marp will choose one; this render "
              "may not match another machine's")

    root = repo_root()
    if args.all:
        targets = [m["_dir"] for m in discover(root)]
    else:
        targets = []
        for module in args.module:
            target = os.path.abspath(module)
            if not os.path.isdir(target):
                sys.exit("not a directory: %s" % module)
            targets.append(target)

    if args.serve:
        serve_dir, built = present_root(root, targets)
        if not built:
            sys.exit("nothing to serve: no slides.md in any target")
        return serve(root, serve_dir, len(built), args.port) or 0

    rc = 0
    for module_dir in targets:
        one = render(root, module_dir, fmt, args.scale,
                     args.watch, args.preview, args.shorts, args.overlays)
        if one is None:      # nothing to render here, so nothing to montage
            continue
        rc |= one
        if args.contact and one == 0:
            rc |= contact_sheet(root, module_dir,
                                deck_name(module_dir, args.shorts,
                                          args.overlays))
    return rc


if __name__ == "__main__":
    sys.exit(main())
