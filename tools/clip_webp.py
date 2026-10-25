#!/usr/bin/env python3
"""
Cut a flight clip into a looping animated WebP for a slide.

    tools/clip_webp.py SRC --start 5 --dur 7 --lock --out assets/opener.webp
    tools/clip_webp.py SRC --start 67 --dur 4.5 --fixed 1370,780,800 --speed 0.5 --out assets/flip.webp

Two ways to frame it:

--lock      follow the aircraft. Each frame finds the quad -- the darkest
            small blob against the sky -- near where it last was, takes its
            darkness-weighted centroid to sub-pixel, smooths it a sixth of a
            second, and crops round it. The quad sits still mid-frame and the
            sky moves, like a chase camera. --seed X,Y (source pixels) says
            where it starts; without it, the darkest blob in the first frame.
--fixed CX,CY,W
            a still window centred on CX,CY, W source pixels wide (16:9), for
            a figure that should be seen moving through the frame.

A WebP, not a video: Marp draws each slide in an SVG foreignObject and
Chromium composites a playing <video> outside it, at its natural size. An
animated image scales with the slide, loops, and gives the PNG and PDF
exports a first frame. Put it on a slide with Marp's image syntax,
![bg](assets/x.webp) or ![h:270](assets/x.webp); a style attribute is dropped
by the served deck.

Two lessons from the first opener, which jittered: keep the source frame
rate (24 fps from 30 drops every fifth frame), and lock on the centroid, not
the darkest pixel, which hops as the silhouette changes. Check the result
with tools/slide_frames.py on the served deck. Needs ffmpeg with libwebp,
numpy and OpenCV.
"""

import argparse
import json
import subprocess
import sys

import numpy as np

try:
    import cv2
except ImportError:
    sys.exit("OpenCV is required: pip install --user opencv-python")

WIN = 90            # centroid search half-size, source pixels
DARK = 25           # how much darker than its surroundings counts as quad
SMOOTH_S = 1 / 6.0  # centroid smoothing window


def probe(src):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height,r_frame_rate",
                          "-of", "json", src], capture_output=True, text=True, check=True)
    st = json.loads(out.stdout)["streams"][0]
    num, den = (int(v) for v in st["r_frame_rate"].split("/"))
    return st["width"], st["height"], num / den


def frames(src, start, dur, w, h, fmt):
    ch = 3 if fmt == "bgr24" else 1
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(start), "-t", str(dur), "-i", src,
                          "-f", "rawvideo", "-pix_fmt", fmt, "-"], stdout=subprocess.PIPE)
    n = w * h * ch
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape((h, w, ch) if ch == 3 else (h, w))
    p.wait()


def darkness(g):
    g = g.astype(np.float32)
    d = cv2.blur(g, (61, 61)) - g
    d[d < DARK] = 0
    return d


def first_fix(g):
    """The darkest small blob in a frame, searched at quarter size."""
    small = cv2.resize(g, (g.shape[1] // 4, g.shape[0] // 4), interpolation=cv2.INTER_AREA)
    d = cv2.GaussianBlur(darkness(small), (9, 9), 0)
    m = 10
    d[:m, :] = 0
    d[-m:, :] = 0
    d[:, :m] = 0
    d[:, -m:] = 0
    y, x = np.unravel_index(np.argmax(d), d.shape)
    return float(x * 4 + 2), float(y * 4 + 2)


def track(src, start, dur, w, h, fps, seed):
    cents, lost = [], 0
    pos = seed
    for g in frames(src, start, dur, w, h, "gray"):
        if pos is None:
            pos = first_fix(g)
        x0, y0 = int(max(0, pos[0] - WIN)), int(max(0, pos[1] - WIN))
        x1, y1 = int(min(w, pos[0] + WIN)), int(min(h, pos[1] + WIN))
        d = darkness(g[y0:y1, x0:x1])
        m = d.sum()
        if m > 0:
            yy, xx = np.mgrid[y0:y1, x0:x1]
            pos = ((d * xx).sum() / m, (d * yy).sum() / m)
        else:
            lost += 1
            pos = first_fix(g)
        cents.append(pos)
    c = np.array(cents)
    k = max(1, int(round(fps * SMOOTH_S)) | 1)
    ker = np.ones(k) / k
    cs = np.stack([np.convolve(np.pad(c[:, j], k // 2, mode="edge"), ker, mode="valid")
                   for j in (0, 1)], 1)
    steps = np.hypot(*np.diff(cs, axis=0).T) if len(cs) > 1 else np.zeros(1)
    print("  tracked %d frames, lost %d; quad moves %.1f px/frame mean, %.1f max (before crop)"
          % (len(cs), lost, steps.mean(), steps.max()))
    return cs


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help="source video")
    ap.add_argument("--start", type=float, required=True, help="seconds into the source")
    ap.add_argument("--dur", type=float, required=True, help="seconds of source to use")
    frame = ap.add_mutually_exclusive_group(required=True)
    frame.add_argument("--lock", action="store_true", help="follow the quad")
    frame.add_argument("--fixed", help="CX,CY,W: a still 16:9 window, source pixels")
    ap.add_argument("--crop", type=int, default=1280,
                    help="--lock window width in source pixels (default 1280: 1:1 from 4K)")
    ap.add_argument("--seed", help="X,Y: where the quad is in the first frame, source pixels")
    ap.add_argument("--speed", type=float, default=1.0,
                    help="playback speed, 0.5 for half (needs a high source frame rate)")
    ap.add_argument("--fps", type=float,
                    help="thin to this rate by keeping every Nth frame; it must divide the play "
                         "rate evenly, since an uneven drop is what made the first opener jitter")
    ap.add_argument("--width", type=int, default=1280, help="output width (default 1280)")
    ap.add_argument("--quality", type=int, default=92,
                    help="WebP quality (default 92; 70 showed blocks on a projector)")
    ap.add_argument("--out", required=True, help="the .webp to write")
    args = ap.parse_args()

    w, h, fps = probe(args.src)
    print("  source %dx%d at %.2f fps" % (w, h, fps))
    if args.fixed:
        cx, cy, cw = (float(v) for v in args.fixed.split(","))
        n = int(round(args.dur * fps)) + 2
        centres = np.tile([cx, cy], (n, 1))
    else:
        cw = args.crop
        seed = tuple(float(v) for v in args.seed.split(",")) if args.seed else None
        centres = track(args.src, args.start, args.dur, w, h, fps, seed)
    cw = int(cw)
    chh = cw * 9 // 16
    ow = args.width
    oh = ow * 9 // 16

    # play rate: the source's rate scaled by the speed, so no frame is dropped
    out_fps = fps * args.speed
    every = 1
    if args.fps:
        every = int(round(out_fps / args.fps))
        if every < 1 or abs(out_fps / every - args.fps) > 0.05 * args.fps:
            sys.exit("--fps %g does not divide the play rate %.2f evenly" % (args.fps, out_fps))
        out_fps /= every
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                            "-s", "%dx%d" % (ow, oh), "-r", "%.4f" % out_fps, "-i", "-",
                            "-c:v", "libwebp_anim", "-lossless", "0", "-quality", str(args.quality),
                            "-compression_level", "6", "-loop", "0", args.out],
                           stdin=subprocess.PIPE)
    count = 0
    for i, f in enumerate(frames(args.src, args.start, args.dur, w, h, "bgr24")):
        if i % every:
            continue
        x, y = centres[min(i, len(centres) - 1)]
        x = float(np.clip(x, cw / 2, w - cw / 2))
        y = float(np.clip(y, chh / 2, h - chh / 2))
        crop = cv2.getRectSubPix(np.ascontiguousarray(f), (cw, chh), (x, y))
        if (ow, oh) != (cw, chh):
            crop = cv2.resize(crop, (ow, oh), interpolation=cv2.INTER_AREA if ow < cw else cv2.INTER_CUBIC)
        enc.stdin.write(crop.tobytes())
        count += 1
    enc.stdin.close()
    enc.wait()
    if out_fps > 50:
        print("  note: %.0f fps is more than a browser shows; consider --speed or a lower source rate"
              % out_fps)
    print("  %d frames at %.1f fps -> %s" % (count, out_fps, args.out))
    return enc.returncode


if __name__ == "__main__":
    sys.exit(main())
