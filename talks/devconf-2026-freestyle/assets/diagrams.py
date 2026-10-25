#!/usr/bin/env python3
"""Draw the deck's diagrams as SVG, in the fossuav palette.

    python3 modules/devconf-2026-freestyle/assets/diagrams.py

Writes next to this file. Every shape here is a schematic: the figure
pictograms follow the segment strings in ACROBATIC_RULES.md 7.3, and the
numbers printed on a diagram are the ones the slide sources in module.yaml.
Nothing is plotted from a log except fig_check.svg, whose two values are
from JOURNAL.md 2026-07-19.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools"))
from svganim import *            # noqa: F401,F403  the palette, Svg, the glyph, the figures
Svg.outdir = HERE

# --- mechanism diagrams ----------------------------------------------------

def loop_forces():
    """What a loop asks of the thrust: toward the centre, all the way round."""
    s = Svg(560, 480)
    c, r = (280, 240), 150
    s.circle(c, r, color=RULE, width=3)
    s.circle(c, 5, color=DIM, fill=DIM)
    for phi, thrust, label, lx, ly in [
            (0, 90, "bottom: ~6 g up", 0, -52),
            (0.5 * math.pi, 40, "", 0, 0),
            (math.pi, 10, "top: thrust at the ground", 0, 44),
            (1.5 * math.pi, 40, "", 0, 0)]:
        p = loop_pt(c, r, phi)
        up_deg = math.degrees(math.atan2(c[1] - p[1], c[0] - p[0]))
        s.quad(p, up_deg, thrust=thrust if phi != math.pi else 0)
        if phi == math.pi:
            s.arrow((p[0], p[1] - 10), (p[0], p[1] - 30), color=ACC, width=3)
        if label:
            s.text((p[0] + lx, p[1] + ly), label, size=22, color=FG)
    # direction of travel
    s.path(arc(c, r + 26, 0.15 * math.pi, 0.35 * math.pi), color=DIM, width=3, arrow=True)
    return s


def sizing():
    s = Svg(640, 480)
    c, r = (360, 250), 160
    s.circle(c, r, color=ACC, width=4)
    s.path([c, (c[0] + r * math.cos(math.radians(30)), c[1] + r * math.sin(math.radians(30)))],
           color=DIM, width=2)
    s.text((c[0] + 80, c[1] + 58), "r", size=24, color=DIM)
    top, bot = (c[0], c[1] + r), (c[0], c[1] - r)
    s.arrow((top[0] + 30, top[1]), (top[0] - 50, top[1]), color=ACC2, width=4)
    s.text((top[0], top[1] + 20), "v_top", size=24, color=ACC2, mono=True)
    s.arrow((bot[0] - 30, bot[1]), (bot[0] + 60, bot[1]), color=ACC2, width=4)
    s.text((bot[0], bot[1] - 36), "v_bot", size=24, color=ACC2, mono=True)
    # height
    x = c[0] + r + 60
    s.path([(x, bot[1]), (x, top[1])], color=DIM, width=2)
    s.path([(x - 8, bot[1]), (x + 8, bot[1])], color=DIM, width=2)
    s.path([(x - 8, top[1]), (x + 8, top[1])], color=DIM, width=2)
    s.text((x + 16, c[1] - 8), "2r", size=24, color=DIM, anchor="start")
    # forces at the bottom
    fx = 110
    s.quad((fx, bot[1] + 20), 90)
    s.arrow((fx, bot[1] + 30), (fx, bot[1] + 120), color=ACC, width=4)
    s.text((fx, bot[1] + 132), "thrust: n g", size=22, color=ACC, mono=True)
    s.arrow((fx, bot[1] + 10), (fx, bot[1] - 30), color=DIM, width=3)
    s.text((fx, bot[1] - 58), "weight", size=22, color=DIM, mono=True)
    return s


def float_segments():
    """The float loop broken into its segments, ACROBATIC_RULES 7.3."""
    s = Svg(900, 420)
    c, r = (450, 200), 150
    y0 = c[1] - r
    s.path([(40, y0), (c[0], y0)], color=DIM, width=6)
    s.text((190, y0 - 34), "T  run-up", size=24, color=DIM)
    s.path(arc(c, r, 0, 0.75 * math.pi), color=ACC, width=7)
    s.text(loop_pt(c, r + 60, 0.4 * math.pi), "A  pull", size=24, color=ACC)
    s.path(arc(c, r, 0.75 * math.pi, 1.25 * math.pi), color=ACC2, width=7, dash="12 12")
    s.text((c[0], c[1] + r + 30), "B  float: idle thrust, gravity turns it", size=24, color=ACC2)
    s.path(arc(c, r, 1.25 * math.pi, 2 * math.pi), color=ACC, width=7)
    s.text(loop_pt(c, r + 70, 1.6 * math.pi), "A  pull-out", size=24, color=ACC)
    s.path([(c[0], y0), (860, y0)], color=DIM, width=6, arrow=True)
    s.text((720, y0 - 34), "T  recover", size=24, color=DIM)
    for phi in (0.75 * math.pi, 1.25 * math.pi):
        p = loop_pt(c, r, phi)
        s.circle(p, 9, color=FG, fill=BG, width=3)
    s.circle(loop_pt(c, r, 0), 9, color=FG, fill=BG, width=3)
    return s


def crash_rotation():
    """Schematic of 19 July: the circle it could not fly, and the rotation it could."""
    s = Svg(900, 480)
    s.text((220, 450), "what it flew", size=26, color=WARN, weight=700)
    s.text((680, 450), "what rotation allows", size=26, color=OK, weight=700)
    c, r = (240, 170), 120
    base = c[1] - r
    s.path([(30, base), (c[0], base)], color=DIM, width=4)
    s.path(arc(c, r, 0, 2 * math.pi), color=RULE, width=3, dash="8 10")
    s.path(arc(c, r, 0, 0.5 * math.pi), color=ACC, width=5)
    q = loop_pt(c, r, 0.5 * math.pi)
    up = [(q[0], q[1] + 6 * t) for t in range(0, 21)]
    s.path(up, color=WARN, width=5)
    hook = [(up[-1][0] - 30 * (1 - math.cos(t * math.pi / 16)), up[-1][1] + 20 * math.sin(t * math.pi / 16))
            for t in range(0, 17)]
    s.path(hook, color=WARN, width=5, arrow=True)
    s.text((q[0] - 40, up[-1][1] + 50), "out of speed, zero thrust, inverted", size=20, color=WARN)
    s.text((c[0], c[1] - 8), "sized for", size=20, color=DIM)
    s.text((c[0], c[1] - 32), "a 15 m circle", size=20, color=DIM)
    x2, b2 = 560, base
    s.path([(x2, b2), (x2 + 80, b2)], color=DIM, width=4)
    q2 = (x2 + 80 + 120, b2 + 120)
    s.path(arc((x2 + 80, b2 + 120), 120, 0, 0.5 * math.pi), color=ACC, width=5)
    s.path([q2, (q2[0], q2[1] + 90)], color=OK, width=5, arrow=True)
    for (px_, py_), ang in [((q2[0] + 70, q2[1] + 10), -90), ((q2[0] + 70, q2[1] + 100), 0)]:
        s.items.append('<g opacity="0.55" transform="translate(%.1f,%.1f) rotate(%d) scale(1.1)">%s</g>'
                       % (px_, s._y(py_), ang, marmott_glyph()))
    s.rot_marker((q2[0] + 70, q2[1] + 50), r=16, color=OK, width=4)
    s.text((q2[0] - 20, b2 - 30), "270 deg at 700 dps: 0.39 s", size=20, color=OK)
    s.text((q2[0] - 20, q2[1] + 150), "upright, 3.6 m higher", size=20, color=OK)
    # animated, in step: the left flies what it flew, the right finishes on rotation
    lrun = [(30 + i * 10.5, base) for i in range(21)]
    larc = arc(c, r, 0, 0.5 * math.pi, n=30)

    def g_left(q):
        if q[1] <= base + 0.5 and q[0] < c[0] - 1:
            return 4.1
        if q[1] <= c[1] + 0.5 and q[0] > c[0]:
            phi = math.atan2(q[0] - c[0], -(q[1] - c[1]))
            return 5.85 * max(0.0, math.cos(phi)) + 0.3
        return 0.0
    hx, hy = hook[-1]
    fall = [(hx - 120 * u, hy - (hy - base) * u * u) for u in [i / 24 for i in range(25)]]
    s.path(fall, color=WARN, width=3, dash="6 8")
    ix, iy = fall[-1]
    n0 = len(s.items)
    s.path([(ix + (22 if k % 2 == 0 else 9) * math.cos(math.pi * k / 8),
             iy + 4 + (22 if k % 2 == 0 else 9) * math.sin(math.pi * k / 8)) for k in range(16)],
           color=WARN, width=3, close=True)
    s.text((ix, iy + 36), "crashed", size=20, color=WARN, weight=700)
    boom = "".join(s.items[n0:])
    del s.items[n0:]
    s.fly([(lrun, 1), (larc, 1.2), (up, 3.0), (hook, 4.0), (fall, 1.6)],
          [(lrun[0], "pitch", 0, 76, lrun[3]), (larc[0], "pitch", 0, -76, larc[-1]),
           (fall[0], "pitch", 0, -720, fall[-1])],
          dur=6.0, hold=0.22, scale=1.1, thrust=g_left, g_px=6)
    s.items.append('<g opacity="0">%s<animate attributeName="opacity" values="0;1;1" '
                   'keyTimes="0;0.78;1" dur="6s" repeatCount="indefinite" calcMode="discrete"/></g>' % boom)
    rc = (x2 + 80, b2 + 120)
    rrun = [(x2 + i * 4, b2) for i in range(21)]
    coast = [(q2[0], q2[1] + 4.5 * i) for i in range(21)]
    rarc = arc(rc, 120, 0, 0.5 * math.pi, n=30)

    def g_right(q):
        if q[1] <= b2 + 0.5 and q[0] < rc[0] - 1:
            return 4.1
        if q[1] <= rc[1] + 0.5 and q[0] > rc[0]:
            phi = math.atan2(q[0] - rc[0], -(q[1] - rc[1]))
            return 5.85 * max(0.0, math.cos(phi)) + 0.3
        return 0.0                              # the coast: rotation costs no thrust
    s.fly([(rrun, 1), (rarc, 1.2), (coast, 4.0)],
          [(rrun[0], "pitch", 0, 76, rrun[3]), (rarc[0], "pitch", 0, -76, rarc[-1]),
           (coast[0], "pitch", 0, -270, coast[-1])], dur=6.0, hold=0.35, scale=1.1,
          thrust=g_right, g_px=6)
    return s


def check_chart():
    """Short of pull against outcome, JOURNAL 2026-07-19 (last)."""
    s = Svg(900, 300)
    x0, y0, scale = 260, 30, 30
    rows = [("17 Jul, 10 m loop", 11.9, OK, "flew clean"),
            ("19 Jul, 15 m loop", 8.8, WARN, "crashed")]
    for i, (lab, v, col, out) in enumerate(rows):
        y = y0 + 170 - i * 110
        s.text((x0 - 16, y + 18), lab, size=24, color=FG, anchor="end")
        s.items.append('<rect x="%.1f" y="%.1f" width="0" height="50" rx="6" fill="%s">'
                       '<animate attributeName="width" values="0;%.1f;%.1f" keyTimes="0;0.3;1" '
                       'dur="5s" repeatCount="indefinite"/></rect>'
                       % (x0, s._y(y + 50), col, v * scale, v * scale))
        s.text((x0 + v * scale + 14, y + 18), "%.1f%%: %s" % (v, out), size=24, color=col, anchor="start")
    s.path([(x0, y0 - 10), (x0, y0 + 240)], color=DIM, width=2)
    s.text((x0 + 180, y0 - 24), "short of the pull it needed", size=20, color=DIM)
    return s


def fence():
    """Plan view of the show-box fence, as autoacro.md describes it."""
    s = Svg(900, 400)
    cy = 200
    start = (330, cy)
    ahead, behind, half = 470, 210, 90
    m = 44
    s.rect(start[0] - behind - m, cy - half - m, ahead + behind + 2 * m, 2 * (half + m),
           fill="none", stroke=WARN, width=3, rx=4)
    s.rect(start[0] - behind, cy - half, ahead + behind, 2 * half, fill=PANEL, stroke=DIM, width=2, rx=4,
           dash="8 8")
    s.path([(start[0] - 150, cy), (start[0] + ahead - 20, cy)], color=ACC, width=4, arrow=True)
    s.text((start[0] + 250, cy - 36), "display line: the heading when staged", size=20, color=ACC)
    s.circle(start, 9, color=FG, fill=FG)
    s.text((start[0] - 10, cy - 36), "start", size=20, color=FG)
    stage = (start[0] + 60, cy)
    s.circle(stage, 8, color=ACC2, fill=BG, width=3)
    s.text((stage[0] - 170, cy + 44), "staged here; the start moves back by AUTA_START_M", size=20, color=ACC2, anchor="start")
    s.text((start[0] + 120, cy - half + 14), "the box the show plans and has flown", size=20, color=DIM)
    s.text((start[0] + 120, cy - half - m + 12), "+ AUTA_FEN_MRGXY", size=20, color=WARN)
    return s


def testing():
    """The testing ladder, cheapest at the bottom."""
    s = Svg(900, 440)
    tiers = [
        ("Offline", "analysis scripts, Lua bench", "86 scripts", DIM),
        ("Native SITL", "Rise255 model, autotest", "34 tests", ACC2),
        ("RealFlight", "same autotest, virtual joystick", "17 tests", ACC2),
        ("The Marmott", "a field card per session", "the only witness", ACC),
    ]
    for i, (name, what, count, col) in enumerate(tiers):
        w = 820 - i * 90
        x = (900 - w) / 2
        y = 20 + i * 102
        s.rect(x, y, w, 86, fill=PANEL, stroke=col, width=3, rx=10)
        s.text((x + 26, y + 50), name, size=28, color=col, anchor="start", weight=700)
        s.text((x + 26, y + 18), what, size=20, color=DIM, anchor="start")
        s.text((x + w - 26, y + 36), count, size=24, color=FG, anchor="end")
    return s




# --- second review --------------------------------------------------------

def freestyle_flow(live=False):
    """A continuous line through several figures: what flow looks like.

    live: a quad flies it, body on the path with a 10 deg forward lean (the
    lines' lean against drag, the arcs' powered lag, RULES 1.2 and 1.4), and
    its pace set by height: slow over the tops, fast through the bottoms."""
    s = Svg(900, 300)
    pts = [(20, 60), (110, 60)]
    pts += arc((180, 130), 70, 0, 2 * math.pi)[1:]
    pts += [(180 + t, 60 + 22 * math.sin(2 * math.pi * 2 * t / 170)) for t in range(0, 171, 3)]
    pts += [(350 + t, 60 + 150 * math.sin(math.pi * t / 200)) for t in range(0, 201, 4)]
    pts += arc((620, 130), 70, 0, 2 * math.pi)[1:]
    pts += [(880, 60)]
    s.path(pts, color=ACC, width=5, arrow=True)
    if live:
        fine = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 6))
            fine += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(1, n + 1)]
        k, v0 = 10.0, 19.0
        speed = lambda q: math.sqrt(max(v0 ** 2 - 2 * G * (q[1] - 60) / k, 4.0))
        seg = path_seg(fine, speed, k, lambda q: 0.0)
        seg = [(x, y, t, a + 10.0, g) for x, y, t, a, g in seg]
        flight = join(seg)
        s.fly_att(flight[0], flight[1], flight[2], dur=9.0, hold=0.1, scale=2.0)
    return s


def ball():
    """Throw a ball: the physics every figure borrows."""
    s = Svg(900, 400)
    x0, y0, vx, vy, g = 250, 40, 7.0, 13.0, 9.81
    k = 18
    T = 2 * vy / g
    pts = [(x0 + vx * t * k * 0.8, y0 + (vy * t - 0.5 * g * t * t) * k) for t in [T * i / 60 for i in range(61)]]
    s.path(pts, color=ACC, width=5, arrow=True)
    apex = pts[30]
    s.circle(apex, 14, color=FG, fill=FG)
    s.circle(pts[10], 11, color=DIM, fill=DIM)
    s.circle(pts[50], 11, color=DIM, fill=DIM)
    s.text((apex[0], apex[1] + 34), "top: slow and weightless, free to turn", size=24, color=ACC2)
    s.text((pts[10][0] - 22, pts[10][1] - 8), "slows as it climbs", size=22, color=FG, anchor="end")
    s.text((pts[50][0] + 24, pts[50][1] - 8), "gravity brings it down", size=22, color=FG, anchor="start")
    s.text((pts[58][0] + 24, y0 + 6), "fast again: carry it on", size=22, color=FG, anchor="start")
    return s


def twitch(live=False):
    """Schematic: lean angle between two figures, asked for smoothly and flown by
    guided, with the quad drawn at its lean at points along the way. Travel is
    to the right; positive lean is nose down.

    live: a cursor runs along the time axis with a quad per row at its lean,
    and the quads drawn along the way fade back to ghosts."""
    s = Svg(900, 560)
    x0, x1, y0 = 160, 870, 380
    ks = 1.6           # px per degree

    def guided(t):
        u = t / 700.0
        if u < 0.08:
            return -70 * u / 0.08
        if u < 0.30:
            return -70
        v = (u - 0.30) / 0.70
        return -70 * math.cos(math.pi * v * 2.2) * math.exp(-2.6 * v)

    def line(t):
        return -22 * math.sin(math.pi * t / 700)

    s.path([(x0, y0), (x1, y0)], color=DIM, width=2)
    for lim in (70, -70):
        s.path([(x0, y0 + lim * ks), (x1, y0 + lim * ks)], color=WARN, width=2, dash="8 8")
    s.text((x0 - 12, y0 + 70 * ks - 7), "nose up 70", size=20, color=WARN, anchor="end")
    s.text((x0 - 12, y0 - 70 * ks - 7), "nose down 70", size=20, color=WARN, anchor="end")
    s.text((x0 - 12, y0 - 7), "level", size=20, color=DIM, anchor="end")
    s.text((x1, y0 + 70 * ks + 12), "lean limit", size=18, color=WARN, anchor="end")
    s.path([(x0 + t, y0 + line(t) * ks) for t in range(0, 701, 10)], color=ACC2, width=5)
    s.path([(x0 + t, y0 + guided(t) * ks) for t in range(0, 701, 5)], color=ACC, width=5)
    s.text((x0 + 16, y0 + 40 * ks), "%s: slams to the limit, swings back" % ("position control" if live else "guided"),
           size=22, color=ACC, anchor="start")
    s.text((x0 + 440, y0 - 48 * ks), "a line: one gentle lean", size=22, color=ACC2, anchor="start")
    s.text((x0, 534), "figure ends", size=20, color=DIM, anchor="start")
    s.text((x1 - 170, 534), "next figure starts", size=20, color=DIM, anchor="end")
    s.text((x0 + 300, 534), "time ->", size=20, color=DIM)

    # the quad at its lean, two rows under the plot
    rows = [(guided, 170, ACC, "position" if live else "guided"), (line, 60, ACC2, "a line")]
    for fn, ry, col, name in rows:
        s.text((20, ry - 8), name, size=22, color=col, anchor="start", weight=700)
    for t in (40, 130, 230, 330, 430, 530, 640):
        x = x0 + t
        for fn, ry, col, name in rows:
            lean = fn(t)
            s.circle((x, y0 + lean * ks), 6, color=col, fill=col)
            s.items.append('<g%s transform="translate(%.1f,%.1f) rotate(%.1f) scale(1.5)">%s</g>'
                           % (' opacity="0.3"' if live else "", x, s._y(ry), -lean, marmott_glyph()))
        s.path([(x, y0 + guided(t) * ks), (x, 205)], color=RULE, width=2, dash="3 6")
    if live:
        dur, run = 6.0, 0.85
        ts = list(range(0, 701, 10))
        kt = ";".join("%.4f" % (run * t / 700) for t in ts) + ";1"
        # the cursor down through both rows, and a dot on each curve
        s.items.append('<g><path d="M 0 %.1f L 0 %.1f" stroke="%s" stroke-width="2"/>'
                       '<animateMotion values="%s" keyTimes="%s" dur="%gs" repeatCount="indefinite" '
                       'calcMode="linear"/></g>'
                       % (s._y(y0 + 75 * ks), s._y(30), FG,
                          ";".join("%.1f,0" % (x0 + t) for t in ts + [700]), kt, dur))
        for fn, ry, col, name in rows:
            dots = ";".join("%.1f,%.1f" % (x0 + t, s._y(y0 + fn(t) * ks)) for t in ts + [700])
            s.items.append('<g><circle r="10" fill="%s" stroke="%s" stroke-width="3"/>'
                           '<animateMotion values="%s" keyTimes="%s" dur="%gs" repeatCount="indefinite" '
                           'calcMode="linear"/></g>' % (BG, col, dots, kt, dur))
            leans = ";".join("%.1f" % -fn(t) for t in ts + [700])
            path = ";".join("%.1f,%.1f" % (x0 + t, s._y(ry)) for t in ts + [700])
            s.items.append('<g><g><g transform="scale(1.9)">%s</g>'
                           '<animateTransform attributeName="transform" type="rotate" values="%s" '
                           'keyTimes="%s" dur="%gs" repeatCount="indefinite" calcMode="linear"/></g>'
                           '<animateMotion values="%s" keyTimes="%s" dur="%gs" repeatCount="indefinite" '
                           'calcMode="linear"/></g>'
                           % (marmott_glyph(), leans, kt, dur, path, kt, dur))
    return s


def loop_shapes():
    """What the g buys: a round loop against a ballistic, taller one.

    Animated: a quad flies each, with its thrust as an arrow. Schematic loads:
    the round loop is the ideal n = 3 + 3 cos(th) (RULES 1.2, m = 1, no
    drag); the ballistic loop pulls through its sides and idles across the top.
    """
    s = Svg(900, 420)
    base = 60
    c1, r1 = (230, base + 130), 130
    s.path([(40, base), (420, base)], color=DIM, width=3)
    s.circle(c1, r1, color=ACC, width=5)
    s.text((c1[0], 390), "round: pulled all the way", size=24, color=ACC)
    s.text((c1[0], 22), "more g at the bottom", size=22, color=FG)
    c2x = 660
    s.path([(480, base), (860, base)], color=DIM, width=3)
    front = [(c2x + 90 * math.sin(t * math.pi / 30), base + 120 - 120 * math.cos(t * math.pi / 30)) for t in range(0, 16)]
    back = [(c2x - 90 * math.sin(t * math.pi / 30), base + 120 - 120 * math.cos(t * math.pi / 30)) for t in range(0, 16)]
    s.path(front, color=ACC, width=5)
    s.path(back, color=ACC, width=5)
    p0, p1 = front[-1], back[-1]
    top = [(p0[0] + (p1[0] - p0[0]) * i / 30,
            p0[1] + 110 * (1 - (2 * i / 30 - 1) ** 2)) for i in range(31)]
    s.path(top, color=ACC2, width=5, dash="10 10")
    s.text((c2x, 390), "ballistic top: gravity turns it", size=24, color=ACC2)
    s.text((c2x, 22), "less g, taller, not round", size=22, color=FG)

    def round_g(q):
        if q[1] <= base + 0.5 and (q[0] < c1[0] - 5 or q[0] > c1[0] + 5):
            return 1.0
        th = math.atan2(q[0] - c1[0], -(q[1] - c1[1]))     # 0 at the bottom
        return 3 + 3 * math.cos(th)

    def ball_g(q):
        if q[1] <= base + 0.5 and abs(q[0] - c2x) > 5:
            return 1.0
        if q[1] > base + 120 + 1:                            # the dashed top
            return 0.2
        th = math.acos(max(-1.0, min(1.0, (base + 120 - q[1]) / 120)))
        return 1 + 3 * math.cos(th)

    line = lambda x0, x1: [(x0 + (x1 - x0) * i / 16, base) for i in range(17)]
    s.fly([(line(60, c1[0] - 6), 1), (arc(c1, r1, 0, 2 * math.pi, n=80), 1),
           (line(c1[0] + 6, 400), 1)],
          dur=5.0, scale=1.8, thrust=round_g, g_px=9)
    s.fly([(line(500, c2x - 6), 1), (front, 1), (top, BALLISTIC), (back[::-1], 1),
           (line(c2x + 6, 840), 1)],
          dur=5.0, scale=1.8, thrust=ball_g, g_px=9)
    return s


def crash_story():
    """19 July, annotated schematic. Numbers from JOURNAL 2026-07-19 (the crash)."""
    s = Svg(900, 460)
    c, r = (300, 200), 150
    base = c[1] - r
    s.path([(20, base), (c[0], base)], color=DIM, width=4)
    s.text((20, base - 30), "run-up: 23.9 m/s", size=20, color=DIM, anchor="start")
    s.path(arc(c, r, 0, 2 * math.pi), color=RULE, width=3, dash="8 10")
    s.text((c[0], c[1]), "the 15 m loop", size=20, color=DIM)
    s.path(arc(c, r, 0, 0.5 * math.pi), color=ACC, width=5)
    q = loop_pt(c, r, 0.5 * math.pi)
    up = [(q[0], q[1] + 7 * t) for t in range(0, 21)]
    s.path(up, color=WARN, width=5)
    hook = [(up[-1][0] - 36 * (1 - math.cos(t * math.pi / 16)), up[-1][1] + 22 * math.sin(t * math.pi / 16))
            for t in range(0, 17)]
    s.path(hook, color=WARN, width=5, arrow=True)
    x = q[0] + 26
    s.text((x, base + 10), "arc at 22.4 m/s", size=20, color=FG, anchor="start")
    s.text((x, base + 76), "pull: 5.85 g of 7.9 asked,", size=20, color=ACC, anchor="start")
    s.text((x, base + 52), "mixer saturated", size=20, color=ACC, anchor="start")
    s.text((x, q[1] + 30), "vertical at 11.2 m/s (wanted 19.9)", size=20, color=FG, anchor="start")
    s.text((x, up[-1][1] - 30), "coasts to +11 m of 15", size=20, color=WARN, anchor="start")
    s.text((up[-1][0] - 10, up[-1][1] + 44), "over the top, inverted, zero thrust", size=20, color=WARN)
    # the flight, animated: saturated pull, then a coast with nothing left
    runup = [(20 + i * 14, base) for i in range(21)]
    arcp = arc(c, r, 0, 0.5 * math.pi, n=30)

    def g_of(q):
        if q[1] <= base + 0.5 and q[0] < c[0] - 1:
            return 4.1                      # 76 deg nose-down holding height: 1/cos(76)
        if q[1] <= c[1] + 0.5 and q[0] > c[0]:
            phi = math.atan2(q[0] - c[0], -(q[1] - c[1]))
            return 5.85 * max(0.0, math.cos(phi)) + 0.3
        return 0.0
    # then out of the sky: a tumbling fall to the ground, and the impact
    hx, hy = hook[-1]
    fall = [(hx - 150 * u, hy - (hy - base) * u * u) for u in [i / 24 for i in range(25)]]
    s.path(fall, color=WARN, width=3, dash="6 8")
    ix, iy = fall[-1]
    burst = []
    for k in range(16):
        rr = 26 if k % 2 == 0 else 11
        a_ = math.pi * 2 * k / 16
        burst.append((ix + rr * math.cos(a_), iy + 4 + rr * math.sin(a_)))
    n0 = len(s.items)
    s.path(burst, color=WARN, width=3, close=True)
    s.text((ix, iy + 40), "crashed", size=24, color=WARN, weight=700)
    boom = "".join(s.items[n0:])
    del s.items[n0:]
    s.fly([(runup, 1), (arcp, 1.2), (up, 3.0), (hook, 4.0), (fall, 1.6)],
          [(runup[0], "pitch", 0, 76, runup[3]),         # pitch forward for the run-up
           (arcp[0], "pitch", 0, -76, arcp[-1]),         # bleeds off over the up arc
           (fall[0], "pitch", 0, -720, fall[-1])], dur=6.0, hold=0.22,
          scale=1.3, thrust=g_of, g_px=7)
    # the impact shows once the fall ends and holds until the loop restarts
    s.items.append('<g opacity="0">%s<animate attributeName="opacity" values="0;1;1" '
                   'keyTimes="0;0.78;1" dur="6s" repeatCount="indefinite" calcMode="discrete"/></g>' % boom)
    return s


def hidden_target():
    """The position controller's integrated target at the entry gate."""
    s = Svg(900, 380)
    for row, (y, ahead, col, lab1, lab2) in enumerate([
            (280, True, ACC, "target ahead: pushed over the gate early", "16 of 18 reps, 0.1-0.2 s"),
            (100, False, WARN, "target behind: braked short of the gate", "2 of 18 reps, 3.0-3.5 s, 55-64 m")]):
        s.path([(40, y), (860, y)], color=RULE, width=3)
        gate = 600
        s.path([(gate, y - 30), (gate, y + 30)], color=FG, width=3, dash="6 6")
        s.text((gate, y + 44), "entry gate", size=18, color=DIM)
        veh = 460
        s.quad((veh, y + 8), 60, thrust=0)
        tgt = veh + 90 if ahead else veh - 140
        s.circle((tgt, y), 12, color=col, width=3)
        s.path([(tgt - 8, y), (tgt + 8, y)], color=col, width=2)
        s.path([(tgt, y - 8), (tgt, y + 8)], color=col, width=2)
        if ahead:
            s.arrow((veh + 20, y - 30), (veh + 110, y - 30), color=col, width=4)
        else:
            s.arrow((veh - 20, y - 30), (veh - 110, y - 30), color=col, width=4)
        s.text((40, y + 40 if row == 0 else y - 64), lab1, size=22, color=col, anchor="start")
        s.text((40, y + 14 if row == 0 else y - 90), lab2, size=20, color=DIM, anchor="start")
    return s


def dead_ideas():
    """The do-not-resurrect list, as a bin."""
    s = Svg(900, 420)
    bx, by, bw, bh = 330, 30, 240, 250
    s.path([(bx, by + bh), (bx + 20, by), (bx + bw - 20, by), (bx + bw, by + bh)], color=DIM, width=5)
    s.path([(bx - 16, by + bh), (bx + bw + 16, by + bh)], color=DIM, width=6)
    for i in range(1, 5):
        x = bx + 20 + i * (bw - 40) / 5
        s.path([(x, by + 20), (x - 4 + i * 2, by + bh - 20)], color=RULE, width=3)
    for (x, y, rr) in [(390, 300, 26), (450, 318, 30), (510, 296, 24), (430, 350, 22), (490, 346, 20)]:
        s.circle((x, y), rr, color=FG, fill=PANEL, width=3)
    for x, y, t in [(160, 370, '"Slow over the top is safe"'), (745, 370, '"Air mode holds attitude"'),
                    (160, 210, "Euler pitch near vertical"), (745, 210, "Trusting a .parm file"),
                    (160, 60, "Rate FF off live speed"), (745, 60, "Shrink figures, shrink box")]:
        s.rect(x - 150, y - 16, 300, 44, fill=PANEL, rx=6)
        s.text((x, y), t, size=21, color=FG)
    return s


def rules_pipeline(live=False):
    """Journal -> rules track -> promoted, and the side exit.

    live: a finding travels the track to CLAUDE.md, then another is
    contradicted on the way and goes to Do not resurrect."""
    s = Svg(900, 360)
    boxes = [
        (30, "JOURNAL.md", "what happened, dated", "17,600 lines", DIM),
        (330, "ACROBATIC_RULES", "the maths, the track", "ONCE -> PROVEN xN", ACC2),
        (630, "CLAUDE.md", "promoted rules", "3 incidents or 2 airframes", ACC),
    ]
    for x, name, what, note, col in boxes:
        s.rect(x, 170, 240, 130, fill=PANEL, stroke=col, width=3, rx=10)
        s.text((x + 120, 262), name, size=24, color=col, weight=700, mono=True)
        s.text((x + 120, 230), what, size=20, color=FG)
        s.text((x + 120, 196), note, size=18, color=DIM)
    s.arrow((272, 235), (326, 235), color=FG, width=3)
    s.arrow((572, 235), (626, 235), color=FG, width=3)
    s.rect(310, 20, 280, 90, fill=PANEL, stroke=WARN, width=3, rx=10)
    s.text((450, 72), "Do not resurrect", size=24, color=WARN, weight=700)
    s.text((450, 42), "contradicted: moved, dated", size=18, color=DIM)
    s.arrow((450, 168), (450, 114), color=WARN, width=3)
    if live:
        # under the boxes, so the text stays readable: one finding promoted,
        # then one contradicted and sent to the bin
        dur = 8.0
        for col, pts, kt, shown in [
                (OK, [(150, 140), (450, 140), (450, 140), (750, 140), (750, 140), (750, 140)],
                 "0;0.12;0.2;0.32;0.44;1", "0;0.44"),
                (WARN, [(150, 140), (150, 140), (450, 140), (450, 140), (450, 122), (450, 122), (450, 122)],
                 "0;0.5;0.62;0.7;0.76;0.94;1", "0.5;0.94")]:
            vals = ";".join("%.1f,%.1f" % (x, s._y(y)) for x, y in pts)
            on, off = shown.split(";")
            vis = "1;0" if on == "0" else "0;1;0"
            vkt = "0;%s" % off if on == "0" else "0;%s;%s" % (on, off)
            s.items.append('<g><circle r="13" fill="%s" stroke="%s" stroke-width="3"/>'
                           '<animateMotion values="%s" keyTimes="%s" dur="%gs" repeatCount="indefinite" '
                           'calcMode="linear"/>'
                           '<animate attributeName="opacity" values="%s" keyTimes="%s" dur="%gs" '
                           'repeatCount="indefinite" calcMode="discrete"/></g>'
                           % (col, FG, vals, kt, dur, vis, vkt, dur))
    return s


QUAD_GLYPH = marmott_glyph()


def fence3d():
    """The show box fence in perspective, animated through the applet's sequence.

    Loiter at the staging point with no fence; switch to middle and the fence
    is drawn but not live; switch high and it goes live, the vehicle backs
    AUTA_START_M to the start and flies; the mode is handed back and the fence
    is off again (autoacro.md, the show-box fence). A still shows the start.
    """
    DUR = 10.0
    s = Svg(900, 520)
    fx0, fx1, fy0, fy1 = 90, 690, 170, 390       # front face of the band
    dx, dy, k = 130, 70, 0.86                    # depth offset, shrink of the back face
    cxm = (fx0 + fx1) / 2

    def back(x, y):
        return (cxm + (x - cxm) * k + dx, fy0 + (y - fy0) * k + dy)

    ground = 40
    m = 40
    g = [(fx0 - m, ground), (fx1 + m, ground), back(fx1 + m, ground), back(fx0 - m, ground)]
    g[2] = (g[2][0], ground + dy + 30)
    g[3] = (g[3][0], ground + dy + 30)
    front = [(fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1)]
    rear = [back(x, y) for x, y in front]

    def fence(color, dash, values, times):
        n0 = len(s.items)
        s.path(g, color=color, width=2, dash="8 8", close=True)
        s.path(rear, color=color, width=2, close=True, dash=dash)
        for a_, b_ in zip(front, rear):
            s.path([a_, b_], color=color, width=2, dash=dash)
        s.path(front, color=color, width=4, close=True, dash=dash)
        s.text((fx0 + 14, fy1 - 30), "FENCE_ALT_MAX", size=20, color=color, anchor="start", mono=True)
        s.text((fx0 + 14, fy0 + 12), "FENCE_ALT_MIN", size=20, color=color, anchor="start", mono=True)
        s.text((fx0 - m, 12), "dashed: the box plus AUTA_FEN_MRGXY on every side", size=20,
               color=color, anchor="start")
        body = "".join(s.items[n0:])
        del s.items[n0:]
        s.items.append('<g opacity="0">%s<animate attributeName="opacity" values="%s" keyTimes="%s" '
                       'dur="%gs" repeatCount="indefinite" calcMode="discrete"/></g>'
                       % (body, values, times, DUR))

    # The cycle opens on the fence going live, so a still shows it. Phases:
    # live, back and fly 0-0.58 | handed back 0.58-0.75 | loiter 0.75-0.87 |
    # staged 0.87-1, then live again.
    fence(DIM, "6 8", "0;1;0;1", "0;0.58;0.75;0.87")
    fence(WARN, None, "1;0", "0;0.58")

    ly = ground + (dy + 30) / 2
    s.path([(fx0 + 40, ly), (fx1 + 20, ly)], color=ACC, width=4, arrow=True)
    st = (fx0 + 170, ly)
    s.circle(st, 8, color=FG, fill=FG)
    s.text((st[0], ly - 30), "start", size=20, color=FG)
    s.text((fx1 - 20, ly - 30), "display line", size=20, color=ACC, anchor="end")

    # what is happening, one caption per phase
    for text, vals in [("Switch high: fence live, back 15 m, fly", "1;0;0;0"),
                       ("Mode handed back: fence off, still staged", "0;1;0;0"),
                       ("Loiter at the staging point", "0;0;1;0"),
                       ("Switch to middle: fence drawn, not live", "0;0;0;1")]:
        n0 = len(s.items)
        s.text((fx0 - m, 490), text, size=26, color=FG, anchor="start", weight=700)
        body = s.items.pop()
        s.items.append('<g opacity="0">%s<animate attributeName="opacity" values="%s" '
                       'keyTimes="0;0.58;0.75;0.87" dur="%gs" repeatCount="indefinite" '
                       'calcMode="discrete"/></g>' % (body, vals, DUR))

    h = fy0 + 100
    stage = (st[0] + 60, h)
    start = (st[0], h)
    # the show: out along the line, a loop, an immelmann, back inverted, a split-S
    r = 45
    show = [start, (st[0] + 120, h)]
    show += arc((st[0] + 120, h + r), r, 0, 2 * math.pi)[1:]
    show += [(fx1 - 80, h)]
    show += arc((fx1 - 80, h + r), r, 0, math.pi)[1:]
    i_top = len(show) - 1                     # the immelmann's top: half roll upright
    show += [(st[0] + 60, h + 2 * r)]
    i_ss = len(show) - 1                      # the split-S's entry: half roll inverted
    show += arc((st[0] + 60, h + r), r, math.pi, 2 * math.pi)[1:]   # ends at the stage point
    sd = lambda pts: "M " + " L ".join("%.1f %.1f" % (x, s._y(y)) for x, y in pts)

    # a level quad for the hover and the move back, a flying one for the show
    hover = sd([stage, start]) + " " + sd([stage, (stage[0] + 1, stage[1])])
    L = 60.0
    kp = "0;%.4f;%.4f;1;1" % (L / (L + 1), L / (L + 1))
    s.items.append('<g><g transform="scale(1.5)">%s</g>'
                   '<animateMotion path="%s" keyPoints="%s" keyTimes="0;0.08;0.5799;0.58;1" '
                   'calcMode="linear" dur="%gs" repeatCount="indefinite"/>'
                   '<animate attributeName="opacity" values="1;0;1" keyTimes="0;0.08;0.58" '
                   'dur="%gs" repeatCount="indefinite" calcMode="discrete"/></g>'
                   % (QUAD_GLYPH, hover, kp, DUR, DUR))
    # rolls: the show's glyph flies at a constant speed from 0.08 to 0.58, so a
    # point's time is 0.08 + 0.5 x its fraction of the path. A quad cannot fly
    # a line inverted, so the leg back along the top is flown upright.
    cum = [0.0]
    for p0, p1 in zip(show, show[1:]):
        cum.append(cum[-1] + math.hypot(p1[0] - p0[0], p1[1] - p0[1]))
    at = lambda i: 0.08 + 0.5 * cum[i] / cum[-1]
    ta, tb = at(i_top), at(i_ss)
    roll = ('<animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 -1;1 -1;1 1;1 1" '
            'keyTimes="0;%.4f;%.4f;%.4f;%.4f;1" dur="%gs" repeatCount="indefinite" calcMode="linear"/>'
            % (ta, ta + 0.025, tb - 0.025, tb, DUR))
    s.items.append('<g opacity="0"><g transform="scale(1.5)"><g>%s%s</g></g>'
                   '<animateMotion path="%s" rotate="auto" keyPoints="0;0;1;1" keyTimes="0;0.08;0.58;1" '
                   'calcMode="linear" dur="%gs" repeatCount="indefinite"/>'
                   '<animate attributeName="opacity" values="0;1;0" keyTimes="0;0.08;0.58" '
                   'dur="%gs" repeatCount="indefinite" calcMode="discrete"/></g>'
                   % (QUAD_GLYPH, roll, sd(show), DUR, DUR))
    return s


def wind_drift():
    """Schematic: a mirrored second show doubles the wind drift (JOURNAL 2026-09-26)."""
    s = Svg(900, 400)
    x0, L, d = 190, 470, 80
    y1, y2 = 250, 120
    s.arrow((640, 360), (800, 360), color=ACC2, width=5)
    s.text((720, 376), "wind", size=30, color=ACC2)
    s.path([(x0, 60), (x0, 330)], color=DIM, width=2, dash="6 8")
    s.text((x0, 346), "start", size=28, color=FG)
    s.path([(x0, y1), (x0 + L, y1)], color=DIM, width=3, dash="10 10")
    s.path([(x0, y1 - 16), (x0 + L + d, y1 - 16)], color=ACC, width=6, arrow=True)
    s.text((20, y1 - 12), "show 1", size=30, color=FG, anchor="start", weight=700)
    s.text((x0 + L + d + 10, y1 - 26), "+d", size=30, color=ACC, anchor="start")
    e = x0 + L + d
    s.path([(e, y2), (e - L, y2)], color=DIM, width=3, dash="10 10")
    s.path([(e, y2 - 16), (e - L + d, y2 - 16)], color=ACC, width=6, arrow=True)
    s.text((20, y2 - 12), "show 2", size=30, color=FG, anchor="start", weight=700)
    s.path([(x0, y2 - 50), (e - L + d, y2 - 50)], color=WARN, width=4)
    s.path([(x0, y2 - 60), (x0, y2 - 40)], color=WARN, width=4)
    s.path([(e - L + d, y2 - 60), (e - L + d, y2 - 40)], color=WARN, width=4)
    s.text((e - L + d + 14, y2 - 60), "2d from home", size=30, color=WARN, anchor="start")
    s.text((x0 + L / 2 + 40, y1 + 40), "dashed: the plan, orange: flown", size=26, color=DIM)
    # the flight: show 1 out and blown on, a pause, show 2 back and blown on again
    p1a, p1b = (x0, y1 - 16), (x0 + L + d, y1 - 16)
    p2a, p2b = (e, y2 - 16), (e - L + d, y2 - 16)
    path = "M %.1f %.1f L %.1f %.1f M %.1f %.1f L %.1f %.1f" % (
        p1a[0], s._y(p1a[1]), p1b[0], s._y(p1b[1]), p2a[0], s._y(p2a[1]), p2b[0], s._y(p2b[1]))
    s.items.append('<g><g transform="translate(0,-22) scale(1.4)">%s</g>'
                   '<animateMotion path="%s" keyPoints="0;0.4999;0.5001;1;1" '
                   'keyTimes="0;0.4;0.45;0.85;1" calcMode="linear" dur="6s" repeatCount="indefinite"/></g>'
                   % (marmott_glyph(), path))
    return s


def thrust_sweep():
    """Thrust points where the body points: settled, or still rotating."""
    s = Svg(980, 420)

    def quad_at(c, ang, alpha=1.0, k=2.6):
        s.items.append('<g opacity="%.2f" transform="translate(%.1f,%.1f) rotate(%.1f) scale(%.1f)">%s</g>'
                       % (alpha, c[0], s._y(c[1]), ang, k, marmott_glyph()))

    def up(ang, n):
        a = math.radians(ang)
        return (math.sin(a) * n, math.cos(a) * n)

    # left: settled, then thrust. A faint copy of the end state, for a still
    c = (210, 160)
    quad_at(c, 0, 0.2)
    s.items.append('<g opacity="0.25">')
    s.arrow((c[0], c[1] + 30), (c[0], c[1] + 150), color=ACC, width=6)
    s.items.append('</g>')
    # live, on the right panel's 4 s clock: turns 70 -> 0 with no thrust, then pushes
    s.items.append('<g transform="translate(%.1f,%.1f)"><g transform="scale(2.6)">%s</g>'
                   '<animateTransform attributeName="transform" type="rotate" values="70;0;0;70" '
                   'keyTimes="0;0.55;0.95;1" dur="4s" repeatCount="indefinite" additive="sum"/></g>'
                   % (c[0], s._y(c[1]), marmott_glyph()))
    n0 = len(s.items)
    s.arrow((c[0], c[1] + 30), (c[0], c[1] + 150), color=ACC, width=6)
    push = "".join(s.items[n0:])
    del s.items[n0:]
    s.items.append('<g transform="translate(%.1f,%.1f)"><g>'
                   '<g transform="translate(%.1f,%.1f)">%s</g>'
                   '<animateTransform attributeName="transform" type="scale" values="0.01;0.01;1;1;0.01" '
                   'keyTimes="0;0.55;0.65;0.95;1" dur="4s" repeatCount="indefinite"/></g></g>'
                   % (c[0], s._y(c[1] + 30), -c[0], -s._y(c[1] + 30), push))
    s.text((c[0], 395), "settled, then thrust", size=28, color=OK, weight=700)
    s.text((c[0], 70), "the push goes where", size=24, color=FG)
    s.text((c[0], 40), "you meant it", size=24, color=FG)

    # right: thrust while the body is still turning
    s.path([(430, 30), (430, 390)], color=RULE, width=2)
    base = 190
    for x, ang, al in [(520, 0, 0.2), (620, 35, 0.2), (720, 70, 0.2)]:
        quad_at((x, base), ang, al)
        dx, dy = up(ang, 100)
        ox, oy = up(ang, 30)
        s.items.append('<g opacity="0.35">')
        s.path([(x + ox, base + oy), (x + dx, base + dy)], color=ACC, width=5, arrow=True)
        s.items.append('</g>')
    # the live one: moves 520 -> 720 while turning 0 -> 70, 4 s loop, hold at the end
    live = ('<g transform="scale(2.6)">%s</g>'
            '<path d="M 0 -30 L 0 -96" stroke="%s" stroke-width="5" stroke-linecap="round"/>'
            '<path d="M -9 -92 L 0 -108 L 9 -92 Z" fill="%s"/>' % (marmott_glyph(), ACC, ACC))
    s.items.append('<g><g>%s<animateTransform attributeName="transform" type="rotate" '
                   'values="0;70;70;0" keyTimes="0;0.55;0.95;1" dur="4s" repeatCount="indefinite"/></g>'
                   '<animateMotion path="M 520 %.1f L 720 %.1f" keyPoints="0;1;1;0" keyTimes="0;0.55;0.95;1" '
                   'calcMode="linear" dur="4s" repeatCount="indefinite"/></g>'
                   % (live, s._y(base), s._y(base)))
    s.path([(620 + 110 * math.sin(t), 20 + 100 * math.cos(t) * 0.8) for t in
            [(-0.9 + 1.8 * i / 20) for i in range(21)]], color=ACC2, width=3, arrow=True)
    s.text((620, 45), "still rotating", size=24, color=ACC2)
    # wanted against got, beside it
    wx, wy = 860, 160
    s.path([(wx, wy), (wx, wy + 130)], color=OK, width=4, dash="8 6", arrow=True)
    s.text((wx - 12, wy + 150), "wanted", size=24, color=OK, anchor="end")
    gx, gy = up(35, 130)
    n0 = len(s.items)
    s.arrow((wx, wy), (wx + gx, wy + gy), color=WARN, width=6)
    got = "".join(s.items[n0:])
    del s.items[n0:]
    # the net push builds while the body turns, and holds
    s.items.append('<g transform="translate(%.1f,%.1f)"><g>'
                   '<g transform="translate(%.1f,%.1f)">%s</g>'
                   '<animateTransform attributeName="transform" type="scale" values="0.05;1;1;0.05" '
                   'keyTimes="0;0.55;0.95;1" dur="4s" repeatCount="indefinite"/></g></g>'
                   % (wx, s._y(wy), -wx, -s._y(wy), got))
    s.text((wx + gx - 20, wy + gy + 20), "got", size=24, color=WARN, anchor="start")
    s.text((wx + 20, wy - 30), "the net push", size=22, color=FG)
    s.text((660, 395), "thrust while still rotating", size=28, color=WARN, weight=700)
    return s


def ab_null(live=False):
    """The 2 Sep A/B (JOURNAL): the handed sideways speed halved, the drift did not move.
    Before n=4 (mean), after n=2 (1.24/1.29 m/s, 12.0/12.9 m).

    live: the before bars grow, then the after bars, then the verdicts. The
    cycle opens on the finished chart, so a still or a PDF shows it whole."""
    s = Svg(560, 380)
    dur, clear = 8.0, 0.2

    def appear(n0, at, grow=None):
        """Wrap the items drawn since n0 to show from `at`; or to grow up from y 80."""
        body = "".join(s.items[n0:])
        del s.items[n0:]
        at = clear + 0.05 + at * (1 - clear)
        if grow:
            s.items.append('<g transform="translate(%.1f,%.1f)"><g transform="translate(%.1f,%.1f)">%s</g>'
                           '<animateTransform attributeName="transform" type="scale" '
                           'values="1 1;1 1;1 0.001;1 0.001;1 1;1 1" keyTimes="0;%.3f;%.3f;%.3f;%.3f;1" '
                           'dur="%gs" repeatCount="indefinite" additive="sum"/></g>'
                           % (grow[0], s._y(80), -grow[0], -s._y(80), body,
                              clear, clear + 0.001, at, at + 0.08, dur))
        else:
            s.items.append('<g>%s<animate attributeName="opacity" values="1;0;1" '
                           'keyTimes="0;%.3f;%.3f" dur="%gs" repeatCount="indefinite" calcMode="discrete"/></g>'
                           % (body, clear, at, dur))

    groups = [("sideways speed", "handed over", 2.85, 1.265, "m/s", 3.2, ("2.85", "1.24/1.29")),
              ("drift", "off the line", 11.6, 12.45, "m", 14.0, ("11.6", "12.0/12.9"))]
    x = 60
    for name, sub, before, after, unit, top, labels in groups:
        k = 220 / top
        for j, (v, col, lab) in enumerate([(before, DIM, "before"), (after, ACC2, "after")]):
            bx = x + j * 90
            at = 0.05 if j == 0 else 0.3
            n0 = len(s.items)
            s.rect(bx, 80, 70, v * k, fill=col, rx=4)
            if live:
                appear(n0, at, grow=(bx,))
            n0 = len(s.items)
            s.text((bx + 35, 80 + v * k + 12), labels[j], size=20, color=FG)
            if live:
                appear(n0, at + 0.1)
            s.text((bx + 35, 56), lab, size=18, color=DIM)
        s.text((x + 80, 26), name, size=22, color=FG, weight=700)
        s.text((x + 80, 4), sub + " (" + unit + ")", size=18, color=DIM)
        x += 270
    n0 = len(s.items)
    s.text((140, 350), "cut by 56%", size=26, color=ACC2, weight=700)
    if live:
        appear(n0, 0.5)
    n0 = len(s.items)
    s.text((410, 350), "no change", size=26, color=WARN, weight=700)
    if live:
        appear(n0, 0.6)
    return s


def closing_strip():
    """Every figure in show order, on one line."""
    names = [f for f, _ in FIGURES]
    order = ["fig_floatloop.svg", "fig_immelmann.svg", "fig_flick.svg", "fig_pivot.svg",
             "fig_floatimmel.svg", "fig_splits.svg", "fig_loopspin.svg", "fig_immelmann.svg",
             "fig_drill.svg", "fig_rewind.svg"]
    return order


# --- v2: the restructured deck ---------------------------------------------
#
# Attitude follows ACROBATIC_RULES. On a line a quad cannot be level and fast
# (1.4: thrust is its only forward force), so a run-in leans into the line and
# a recover leans back against it; the run-up lean is the Marmott's flown 76
# deg (JOURNAL 2026-07-19, as on the crash slide). In a pulled arc the body
# rides the path (1.2: perpendicular thrust does no work, so a figure entered
# on its number is unpowered and the climb is paid for by the run-up's speed).
# Loops are the perfect loop of 1.1 at m = 1, d = 0: n = 3 + 3 cos th.

G = 9.81
RUNUP_LEAN = 76.0


def accel_line(x0, y, v0, v1, k, lean=RUNUP_LEAN, n=30):
    """A level line flown from v0 to v1 m/s, rightward, height held: a
    triangle of acceleration that peaks at `lean` and is level at both ends,
    so it starts or stops at a hover and hands over level. Thrust is
    sqrt(a^2 + g^2). x0 in px, k px per m. Samples (x, y, t, att, g)."""
    sgn = 1 if v1 >= v0 else -1
    a0 = G * math.tan(math.radians(lean))
    T = 2 * abs(v1 - v0) / a0
    acc = lambda t: sgn * a0 * (1 - abs(2 * t / T - 1))
    vel = lambda t: v0 + sgn * a0 * t * t / T if t <= T / 2 else v1 - sgn * a0 * (T - t) ** 2 / T
    out, x, N = [], 0.0, n * 20
    for i in range(N + 1):
        t = T * i / N
        if i:
            x += (vel(t) + vel(t - T / N)) / 2 * T / N
        if i % 20 == 0:
            a = acc(t)
            out.append((x0 + x * k, y, t, math.degrees(math.atan2(a, G)), math.hypot(a, G) / G))
    return out


def line_len(v0, v1, lean=RUNUP_LEAN):
    """Metres an accel_line takes."""
    return accel_line(0, 0, v0, v1, 1.0, lean)[-1][0]


def loop_arc(c, r, R, phi0, phi1, v_bot, n=48, g_fn=None):
    """A perfect-loop arc, body on the path: v^2 = v_bot^2 - 2 g R (1 - cos phi),
    thrust v^2/(g R) + cos phi unless g_fn(phi) says otherwise. r px, R m.
    Samples (x, y, t, att, g)."""
    out, t = [], 0.0
    v = lambda ph: math.sqrt(max(v_bot ** 2 - 2 * G * R * (1 - math.cos(ph)), 0.25))
    for i in range(n + 1):
        ph = phi0 + (phi1 - phi0) * i / n
        if i:
            ph0 = phi0 + (phi1 - phi0) * (i - 1) / n
            t += R * abs(ph - ph0) / ((v(ph) + v(ph0)) / 2)
        q = loop_pt(c, r, ph)
        g = g_fn(ph) if g_fn else v(ph) ** 2 / (G * R) + math.cos(ph)
        out.append((q[0], q[1], t, -math.degrees(ph), g))
    return out


def path_seg(pts, speed, k, g_fn):
    """Any path, body on it: time from speed(q) m/s, attitude from the tangent."""
    out, t = [], 0.0
    for i, q in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        if i:
            d = math.hypot(q[0] - pts[i - 1][0], q[1] - pts[i - 1][1]) / k
            t += d / ((speed(q) + speed(pts[i - 1])) / 2)
        out.append((q[0], q[1], t, -math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])), g_fn(q)))
    return out


def join(*segs):
    """Chain segments end to end: times offset, the repeated joint dropped,
    attitude unwrapped so the glyph never spins the long way round."""
    pts, ts, att, gs = [], [], [], []
    for seg in segs:
        t0 = ts[-1] if ts else 0.0
        turn = 0.0
        if att:
            turn = 360.0 * round((att[-1] - seg[0][3]) / 360.0)
        prev = None
        for k, (x, y, t, a, g) in enumerate(seg):
            a += turn
            if prev is not None and abs(a - prev) > 180:
                turn += 360.0 * round((prev - a) / 360.0)
                a = seg[k][3] + turn
            prev = a
            if pts and k == 0:
                continue
            pts.append((x, y))
            ts.append(t0 + t)
            att.append(a)
            gs.append(g)
    return pts, ts, att, gs


def fly_flight(s, flight, **kw):
    pts, ts, att, gs = flight
    s.fly_att(pts, ts, att, thrust=gs if kw.pop("thrust", True) else None, **kw)


def real_dur(flight, hold=0.18):
    """A cycle long enough that the flight runs in real time."""
    return round((flight[1][-1] - flight[1][0]) / (1 - hold), 1)


def gauge(s, x, y0, full, scale, vals, kts, dur, col, ticks, name):
    """A bar that rises and falls with vals at kts; ticks are (value, label)."""
    s.rect(x - 24, y0, 48, full, fill="none", stroke=RULE, width=2, rx=4)
    s.items.append('<g transform="translate(%.1f,%.1f)"><rect x="-22" y="%.1f" width="44" height="%.1f" '
                   'rx="3" fill="%s"><animateTransform attributeName="transform" type="scale" values="%s" '
                   'keyTimes="%s" dur="%gs" repeatCount="indefinite" calcMode="linear"/></rect></g>'
                   % (x, s._y(y0), -full, full, col,
                      ";".join("1 %.4f" % max(v * scale / full, 0.001) for v in vals),
                      ";".join("%.4f" % k for k in kts), dur))
    for v, lab in ticks:
        y = y0 + v * scale
        s.path([(x - 30, y), (x + 30, y)], color=FG, width=2)
        s.text((x + 36, y - 7), lab, size=20, color=FG, anchor="start")
    s.text((x, y0 - 30), name, size=22, color=col, weight=700)


def toss():
    """The thrown-ball slide, flown the way the code throws a quad (RULES
    1.5): lean in to build speed, level, toss upright on thrust, coast with the
    thrust off and flip over the top where rotation is free, catch upright,
    carry the speed on. Real time; horizontal speed held, drag ignored over
    the hop."""
    s = Svg(900, 420)
    k, vx, n_b, t_b = 50.0, 4.0, 3.0, 0.4
    y0 = 50
    run = accel_line(70, y0, 0.0, vx, k, lean=30)
    seg_b, seg_c, seg_k = [], [], []
    vy_b = (n_b - 1) * G * t_b
    x1 = run[-1][0]
    for i in range(9):                                   # the toss: upright, thrust up
        t = t_b * i / 8
        seg_b.append((x1 + vx * t * k, y0 + 0.5 * (n_b - 1) * G * t * t * k, t,
                      run[-1][3] * max(0.0, 1 - i / 3), n_b))
    xb2, yb2 = seg_b[-1][0], seg_b[-1][1]
    tc = 2 * vy_b / G
    for i in range(41):                                  # the coast: thrust off, flip at the top
        t = tc * i / 40
        u = (t / tc - 0.2) / 0.6
        flip = -360.0 * min(max(u, 0.0), 1.0)
        seg_c.append((xb2 + vx * t * k, yb2 + (vy_b * t - 0.5 * G * t * t) * k, t, flip, 0.0))
    xc, yc = seg_c[-1][0], seg_c[-1][1]
    for i in range(9):                                   # the catch: upright, arrest the sink
        t = t_b * i / 8
        seg_k.append((xc + vx * t * k, yc - (vy_b * t - 0.5 * (n_b - 1) * G * t * t) * k, t, 0.0, n_b))
    # carry it on: the same speed held, leaning into its own drag
    lean = 10.0
    out = [(seg_k[-1][0] + vx * t * k, y0, t, lean * min(1.0, t / 0.15), 1 / math.cos(math.radians(lean)))
           for t in [0.6 * i / 12 for i in range(13)]]
    flight = join(run, seg_b, seg_c, seg_k, out)
    pts = flight[0]
    s.path(pts, color=ACC, width=5, arrow=True)
    nb, nc = len(run), len(run) + len(seg_b) - 1
    s.path(pts[nb - 1:nc], color=FG, width=7)
    s.path(pts[nc + 40:nc + 48], color=FG, width=7)
    apex = seg_c[20]
    s.text((apex[0], apex[1] + 30), "top: slow and weightless, free to turn", size=24, color=ACC2)
    up, down = seg_c[9], seg_c[31]
    s.text((up[0] - 26, up[1] - 8), "kinetic -> potential", size=22, color=FG, anchor="end")
    s.text((down[0] + 26, down[1] - 8), "potential -> kinetic", size=22, color=FG, anchor="start")
    s.text(((run[0][0] + run[-1][0]) / 2, y0 - 34), "build speed", size=22, color=DIM)
    s.text((seg_b[4][0] - 14, seg_b[4][1] + 26), "toss: props up", size=22, color=FG, anchor="end")
    s.text((seg_k[4][0] + 14, seg_k[4][1] + 26), "catch", size=22, color=FG, anchor="start")
    s.text(((out[0][0] + out[-1][0]) / 2, y0 - 34), "carry it on", size=22, color=DIM)
    fly_flight(s, flight, dur=real_dur(flight), scale=2.2, g_px=7)
    return s


def loop_budget():
    """The 6 g slide's loop at its own pace: lean in from a hover to the
    entry speed, a 15 m perfect loop, lean back to a hover. Speed and thrust
    as gauges; every number is the sizing law's, not a log's."""
    s = Svg(800, 440)
    R = 7.5
    c, r = (300, 240), 150
    k = r / R
    base = c[1] - r
    vb = math.sqrt(5 * G * R)
    run = accel_line(c[0] - line_len(0, vb) * k, base, 0.0, vb, k)
    loop = loop_arc(c, r, R, 0, 2 * math.pi, vb, n=96)
    out = accel_line(c[0], base, vb, 0.0, k)
    flight = join(run, loop, out)
    s.path([run[0][:2], (c[0], base)], color=DIM, width=3)
    s.path(arc(c, r, 0, 2 * math.pi), color=ACC, width=5)
    s.path([(c[0], base), out[-1][:2]], color=DIM, width=3, arrow=True)
    s.text((c[0], c[1] + r + 18), "top: 8.6 m/s, gravity alone turns it", size=22, color=ACC2)
    s.text((c[0], base - 34), "bottom: 19 m/s, 6 g", size=22, color=FG)
    dx = c[0] + r + 22
    s.path([(dx, base + 8), (dx, base + 2 * r)], color=DIM, width=2)
    s.path([(dx - 7, base + 2 * r), (dx + 7, base + 2 * r)], color=DIM, width=2)
    s.text((dx + 10, c[1] - 8), "15 m", size=20, color=DIM, anchor="start")
    hold = 0.18
    dur = real_dur(flight, hold)
    fly_flight(s, flight, dur=dur, hold=hold, scale=2.0, g_px=4)
    pts, ts, att, gs = flight
    T = ts[-1]
    kts = [(1 - hold) * t / T for t in ts] + [1.0]
    # speed at each flown point: differentiate the flown positions, so the
    # gauge cannot disagree with the quad
    v = [0.0]
    for i in range(1, len(pts)):
        d = math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]) / k
        v.append(d / max(ts[i] - ts[i - 1], 1e-6))
    v = [v[1]] + [(v[i] + v[i + 1]) / 2 for i in range(1, len(v) - 1)] + [v[-1]]
    v[0], v[-1] = 0.0, 0.0
    gauge(s, 610, 70, 290, 14, v + [0.0], kts, dur, ACC2,
          [(vb, "19"), (math.sqrt(G * R), "8.6")], "speed, m/s")
    gauge(s, 725, 70, 290, 45, gs + [gs[-1]], kts, dur, ACC,
          [(6, "6 g"), (1, "1 g"), (0, "0")], "thrust, g")
    return s


def no_wing():
    """Thrust on, the body aims the path; thrust off, the body turns for free.

    Left: lean in along the line for speed, then the loop with the thrust at
    the centre, then lean back. The arrow is a fixed length: the direction is
    the point here, the 6 g slide has the size. Right: a ballistic arc, back-
    flipping over the top with the path unchanged."""
    s = Svg(900, 420)
    R, c, r = 7.5, (240, 215), 115
    k = r / R
    base = c[1] - r
    vb = math.sqrt(5 * G * R)
    run = accel_line(c[0] - line_len(0, vb) * k, base, 0.0, vb, k)
    out = accel_line(c[0], base, vb, 0.0, k)
    flight = join(run, loop_arc(c, r, R, 0, 2 * math.pi, vb, n=80), out)
    s.path([run[0][:2], (c[0], base)], color=DIM, width=3)
    s.path(arc(c, r, 0, 2 * math.pi), color=ACC, width=5)
    s.path([(c[0], base), out[-1][:2]], color=DIM, width=3, arrow=True)
    flight = (flight[0], flight[1], flight[2], [5.0] * len(flight[3]))
    fly_flight(s, flight, dur=real_dur(flight, 0.1), hold=0.1, scale=1.7, g_px=7)
    s.text((c[0], c[1] + r + 22), "top: thrust at the ground", size=22, color=FG)
    s.text((c[0], base - 34), "line: thrust leans in for speed", size=20, color=FG)
    s.text((c[0], 18), "thrust on: the body aims the path", size=24, color=ACC, weight=700)
    s.path([(450, 40), (450, 400)], color=RULE, width=2)
    x0, x1, y0, h = 510, 860, 80, 230
    pts = [(x0 + (x1 - x0) * i / 60, y0 + h * (1 - (2 * i / 60 - 1) ** 2)) for i in range(61)]
    s.path(pts, color=ACC2, width=5, dash="10 10", arrow=True)
    segs = [([p0, p1], abs(p1[0] - p0[0]) / math.hypot(p1[0] - p0[0], p1[1] - p0[1]))
            for p0, p1 in zip(pts, pts[1:])]
    s.fly(segs, [(pts[18], "pitch", 0, -360, pts[42])], dur=4.2, hold=0.2, scale=1.7)
    s.text(((x0 + x1) / 2, y0 + h + 34), "same arc, whatever the attitude", size=22, color=FG)
    s.text(((x0 + x1) / 2, 18), "thrust off: the body turns for free", size=24, color=ACC2, weight=700)
    return s


def loop_shapes_v2():
    """Slide 11 with the attitude flown and the ballistic loop made physical.

    Both lean in from a hover to the same entry speed (the 15 m perfect
    loop's, sqrt(5 g R)) and lean back after. Round: the perfect loop, n = 3 +
    3 cos th. Ballistic: a gentler pull (radius 1.2 R, so less g at the
    bottom) that runs a little past vertical, to 110 deg, then the true
    parabola from that state -- position and velocity carried across, so no
    kink -- and a mirrored pull-out from the parabola's end. Energy conserved,
    drag ignored, idle thrust drawn but not flown. It comes out taller, slower
    over the top, and exits ahead of where it entered. Real time, side by side."""
    s = Svg(900, 440)
    R, k = 7.5, 15.0
    base = 60
    vb = math.sqrt(5 * G * R)
    L = line_len(0, vb) * k
    c1 = (225, base + R * k)
    s.path([(c1[0] - L, base), (c1[0] + L, base)], color=DIM, width=3)
    s.circle(c1, R * k, color=ACC, width=5)
    s.text((c1[0], 410), "round: pulled all the way", size=24, color=ACC)
    s.text((c1[0], 22), "more g at the bottom", size=22, color=FG)
    round_f = join(accel_line(c1[0] - L, base, 0.0, vb, k),
                   loop_arc(c1, R * k, R, 0, 2 * math.pi, vb, n=80),
                   accel_line(c1[0], base, vb, 0.0, k))

    rp, a_cut = 1.2 * R, math.radians(110)
    x0 = 615
    c2 = (x0, base + rp * k)
    front = loop_arc(c2, rp * k, rp, 0, a_cut, vb, n=40)
    v_cut = math.sqrt(vb ** 2 - 2 * G * rp * (1 - math.cos(a_cut)))
    vx, vy = v_cut * math.cos(a_cut), v_cut * math.sin(a_cut)
    px, py = front[-1][0], front[-1][1]
    tf = 2 * vy / G
    top = []
    for i_ in range(41):
        t = tf * i_ / 40
        top.append((px + vx * t * k, py + (vy * t - 0.5 * G * t * t) * k, t,
                    -math.degrees(math.atan2(vy - G * t, vx)), 0.2))
    ex, ey = top[-1][0], top[-1][1]
    a_out = 2 * math.pi - a_cut
    c3 = (ex - rp * k * math.sin(a_out), ey + rp * k * math.cos(a_out))
    out = loop_arc(c3, rp * k, rp, a_out, 2 * math.pi, vb, n=40)
    s.path([(x0 - L, base), (x0, base)], color=DIM, width=3)
    s.path([q[:2] for q in front], color=ACC, width=5)
    s.path([q[:2] for q in top], color=ACC2, width=5, dash="10 10")
    s.path([q[:2] for q in out], color=ACC, width=5)
    s.path([(c3[0], base), (c3[0] + L, base)], color=DIM, width=3)
    s.text((c2[0] + 40, 410), "ballistic top: gravity turns it", size=24, color=ACC2)
    s.text((c2[0] + 40, 22), "less g, taller, slower on top", size=22, color=FG)
    ball_f = join(accel_line(x0 - L, base, 0.0, vb, k), front, top, out,
                  accel_line(c3[0], base, vb, 0.0, k))
    Tmax = max(round_f[1][-1], ball_f[1][-1])
    run = 0.85
    dur = round(Tmax / run, 1)
    for f in (round_f, ball_f):
        fly_flight(s, f, dur=dur, hold=1 - run * f[1][-1] / Tmax, scale=1.8, g_px=6)
    return s


def guided_loop():
    """Where the position controller's picture holds on a loop. Below the
    equator the thrust that turns the path still holds the quad up; above it,
    it points at the ground, and the position controller assumes thrust holds
    you up. All of the figure is flown in Guided either way."""
    s = Svg(560, 480)
    c, r = (280, 240), 150
    s.path(arc(c, r, -0.5 * math.pi, 0.5 * math.pi), color=OK, width=7)
    s.path(arc(c, r, 0.5 * math.pi, 1.5 * math.pi), color=WARN, width=7)
    s.text((c[0], c[1] - r - 44), "thrust holds it up: position control's world", size=22, color=OK)
    s.text((c[0], c[1] + r + 22), "thrust at the ground", size=22, color=WARN)
    flight = join(loop_arc(c, r, 7.5, 0, 2 * math.pi, math.sqrt(5 * G * 7.5), n=80))
    flight = (flight[0], flight[1], flight[2], [5.0] * len(flight[3]))
    fly_flight(s, flight, dur=real_dur(flight, 0.04), hold=0.04, scale=1.8, g_px=8)
    return s


def split_segments():
    """The split, flown: which Guided command flies each segment of a float
    loop (ACROBATIC_RULES 7.3). All of it is Guided mode; the script picks the
    command. Position targets lean in from a hover and level at the gate; rate
    and thrust pull with the body on the path, idle over the top, and pull
    out; position targets lean back to a hover. Thrust: the run-in's, the perfect
    loop's 3 + 3 cos th through the pulls, idle across the float."""
    s = Svg(900, 450)
    R, c, r = 7.5, (450, 220), 150
    k = r / R
    y0 = c[1] - r
    vb = math.sqrt(5 * G * R)
    L = line_len(0, vb) * k
    run = accel_line(c[0] - L, y0, 0.0, vb, k)
    pull = loop_arc(c, r, R, 0, 0.75 * math.pi, vb)
    top = loop_arc(c, r, R, 0.75 * math.pi, 1.25 * math.pi, vb, n=24, g_fn=lambda ph: 0.2)
    outp = loop_arc(c, r, R, 1.25 * math.pi, 2 * math.pi, vb)
    rec = accel_line(c[0], y0, vb, 0.0, k)
    segs = [run, pull, top, outp, rec]
    flight = join(*segs)
    hold = 0.18
    dur = real_dur(flight, hold)
    T = flight[1][-1]
    ends, i = [], 0
    for seg in segs:
        i += len(seg) - (1 if ends else 0)
        ends.append((1 - hold) * flight[1][i - 1] / T)

    def lit(n0, a, b):
        """Show what was drawn since n0 only while its segment is flying."""
        body = "".join(s.items[n0:])
        del s.items[n0:]
        s.items.append('<g opacity="0">%s<animate attributeName="opacity" values="0;0.35;0" '
                       'keyTimes="0;%.4f;%.4f" dur="%gs" repeatCount="indefinite" calcMode="discrete"/></g>'
                       % (body, a, b, dur))

    starts = [0.0] + ends[:-1]
    for seg, a, b, col in zip(segs, starts, ends, [FG, ACC, ACC2, ACC, FG]):
        n0 = len(s.items)
        s.path([q[:2] for q in seg], color=col, width=22)
        lit(n0, a, b)
    s.path([run[0][:2], (c[0], y0)], color=DIM, width=6)
    s.path(arc(c, r, 0, 0.75 * math.pi), color=ACC, width=7)
    s.path(arc(c, r, 0.75 * math.pi, 1.25 * math.pi), color=ACC2, width=7, dash="12 12")
    s.path(arc(c, r, 1.25 * math.pi, 2 * math.pi), color=ACC, width=7)
    s.path([(c[0], y0), rec[-1][:2]], color=DIM, width=6, arrow=True)
    s.text((c[0] - 16, y0 - 34), "T  position: entry speed", size=22, color=FG, anchor="end")
    s.text((c[0] + 16, y0 - 34), "T  position: recover", size=22, color=FG, anchor="start")
    s.text((c[0] + r + 24, c[1] - 8), "A  rate + thrust: pull", size=22, color=ACC, anchor="start")
    s.text((c[0] - r - 24, c[1] - 8), "A  rate + thrust: pull-out", size=22, color=ACC, anchor="end")
    s.text((c[0], c[1] + r + 26), "B  rate + idle: gravity turns it", size=22, color=ACC2)
    for phi in (0, 0.75 * math.pi, 1.25 * math.pi):
        s.circle(loop_pt(c, r, phi), 9, color=FG, fill=BG, width=3)
    for text, col, vals in [("POSITION", FG, "1;0;1"), ("RATE + THRUST", ACC, "0;1;0")]:
        n0 = len(s.items)
        s.text((24, 404), text, size=30, color=col, anchor="start", weight=800)
        body = "".join(s.items[n0:])
        del s.items[n0:]
        s.items.append('<g>%s<animate attributeName="opacity" values="%s" keyTimes="0;%.4f;%.4f" '
                       'dur="%gs" repeatCount="indefinite" calcMode="discrete"/></g>'
                       % (body, vals, ends[0], ends[3], dur))
    s.text((24, 376), "the Guided command in use", size=20, color=DIM, anchor="start")
    fly_flight(s, flight, dur=dur, hold=hold, scale=1.6, g_px=6)
    return s


def boost():
    """Angle boost against tilt, from AC_AttitudeControl_Multi::get_throttle_boosted:
    out = in x clamp(10 cos tilt, 0, 1) / clamp(cos target tilt, 0.1, 1), the
    tilt and its target taken as equal. The quad's arrow is capped at x5 so it
    stays on the slide; the plot is not."""
    s = Svg(900, 400)
    px0, px1, py0, k = 400, 860, 60, 28.0
    X = lambda deg: px0 + (px1 - px0) * deg / 180
    Y = lambda f: py0 + f * k

    def factor(deg):
        ct = math.cos(math.radians(deg))
        return max(0.0, min(1.0, 10 * ct)) / max(0.1, min(1.0, ct))

    s.path([(px0, py0), (px1, py0)], color=DIM, width=2)
    s.path([(px0, py0), (px0, Y(10.6))], color=DIM, width=2)
    for d in (0, 90, 180):
        s.path([(X(d), py0 - 6), (X(d), py0)], color=DIM, width=2)
        s.text((X(d), py0 - 28), str(d), size=20, color=FG)
    s.text((X(135), py0 - 28), "tilt, deg", size=20, color=DIM)
    for f, lab in ((1, "x1"), (10, "x10")):
        s.text((px0 - 10, Y(f) - 7), lab, size=20, color=FG, anchor="end")
    s.path([(X(90), py0), (X(90), Y(10.6))], color=RULE, width=2, dash="4 8")
    s.path([(px0, Y(1)), (px1, Y(1))], color=OK, width=4, dash="10 8")
    curve = [(X(d / 4), Y(factor(d / 4))) for d in range(0, 721)]
    s.path(curve, color=WARN, width=4)
    s.circle((X(60), Y(2)), 6, color=WARN, fill=WARN)
    s.text((X(60) - 12, Y(2) + 6), "x2 at 60", size=20, color=WARN, anchor="end")
    s.text((X(84.3) - 12, Y(10) - 8), "x10 at 84", size=20, color=WARN, anchor="end")
    s.text((X(135), Y(1) + 10), "inverted: zero", size=20, color=WARN)
    lx = X(96)
    s.path([(lx, 290), (lx + 36, 290)], color=WARN, width=4)
    s.text((lx + 46, 282), "on: holds a hover", size=20, color=FG, anchor="start")
    s.path([(lx, 252), (lx + 36, 252)], color=OK, width=4, dash="10 8")
    s.text((lx + 46, 244), "off: asked is given", size=20, color=FG, anchor="start")

    # one slow back-flip, lingering where the boost runs away
    angs, ts, t = [], [], 0.0
    for a in range(0, 361):
        tilt = a if a <= 180 else 360 - a
        angs.append(a)
        ts.append(t)
        t += 3.0 if 50 <= tilt <= 100 else 1.0
    dur, run = 9.0, 0.9
    kt = ";".join("%.4f" % (run * x / ts[-1]) for x in ts) + ";1"
    tilts = [a if a <= 180 else 360 - a for a in angs] + [0]
    fs = [factor(d) for d in tilts]
    cx, cy = 190, 210
    s.circle((cx, cy), 120, color=RULE, width=2, dash="4 8")
    s.text((cx, 26), "asked: dashed, given: solid", size=20, color=DIM)
    unit = 22
    given = ";".join("M 0 -10 L 0 %.1f" % (-10 - unit * min(f, 5.0)) for f in fs)
    head = ";".join("0 %.1f" % (-10 - unit * min(f, 5.0)) for f in fs)
    s.items.append(
        '<g transform="translate(%.1f,%.1f)"><g>'
        '<path stroke="%s" stroke-width="6" stroke-linecap="round" d="M 0 -10 L 0 -32">'
        '<animate attributeName="d" values="%s" keyTimes="%s" dur="%gs" repeatCount="indefinite"/></path>'
        '<g><path d="M -9 6 L 0 -10 L 9 6 Z" fill="%s"/>'
        '<animateTransform attributeName="transform" type="translate" values="%s" keyTimes="%s" '
        'dur="%gs" repeatCount="indefinite"/></g>'
        '<path d="M 0 -10 L 0 %.1f" stroke="%s" stroke-width="4" stroke-dasharray="6 6"/>'
        '<g transform="scale(3.2)">%s</g>'
        '<animateTransform attributeName="transform" type="rotate" values="%s" keyTimes="%s" '
        'dur="%gs" repeatCount="indefinite"/></g></g>'
        % (cx, s._y(cy), WARN, given, kt, dur, WARN, head, kt, dur, -10 - unit, OK,
           marmott_glyph(), ";".join("%d" % a for a in angs + [360]), kt, dur))
    dots = ";".join("%.1f,%.1f" % (X(d), s._y(Y(f))) for d, f in zip(tilts, fs))
    s.items.append('<g><circle r="9" fill="%s" stroke="%s" stroke-width="3"/>'
                   '<animateMotion values="%s" keyTimes="%s" dur="%gs" repeatCount="indefinite"/></g>'
                   % (FG, WARN, dots, kt, dur))
    return s


def pilot_replay():
    """Schematic: the same stick inputs on another day fly another figure.
    Same sticks, so the same attitudes at the same times; the replay drifts
    downwind and sinks, more the further it goes."""
    s = Svg(660, 400)
    R, c, r = 7.5, (300, 210), 100
    k = r / R
    base = c[1] - r
    vb = math.sqrt(5 * G * R)
    L = line_len(0, vb) * k
    rec = join(accel_line(c[0] - L, base, 0.0, vb, k), loop_arc(c, r, R, 0, 2 * math.pi, vb, n=60),
               accel_line(c[0], base, vb, 0.0, k))
    cum = [0.0]
    for a, b in zip(rec[0], rec[0][1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    rep_pts = [(x + 80 * (u / cum[-1]), y - 70 * (u / cum[-1]) ** 2) for (x, y), u in zip(rec[0], cum)]
    rep = (rep_pts, rec[1], rec[2], rec[3])
    s.path(rec[0], color=DIM, width=4, arrow=True)
    s.path(rep_pts, color=WARN, width=4, arrow=True)
    s.arrow((520, 360), (630, 360), color=ACC2, width=4)
    s.text((575, 374), "wind", size=22, color=ACC2)
    s.text((40, 52), "the day it was flown", size=22, color=FG, anchor="start")
    s.text((40, 24), "the same sticks, another day", size=22, color=WARN, anchor="start")
    s.path([(10, 58), (32, 58)], color=DIM, width=4)
    s.path([(10, 30), (32, 30)], color=WARN, width=4)
    dur = real_dur(rec)
    fly_flight(s, rec, dur=dur, scale=1.8, thrust=False)
    fly_flight(s, rep, dur=dur, scale=1.8, thrust=False)
    return s



def rules_pipeline_bin():
    """Journal -> rules track -> promoted, and the bin: a finding is promoted
    to CLAUDE.md, then another is contradicted and thrown in the bin."""
    s = Svg(900, 380)
    boxes = [
        (30, "JOURNAL.md", "what happened, dated", "17,600 lines", DIM),
        (330, "ACROBATIC_RULES", "the maths, the track", "ONCE -> PROVEN xN", ACC2),
        (630, "CLAUDE.md", "promoted rules", "3 incidents or 2 airframes", ACC),
    ]
    by0 = 220
    for x, name, what, note, col in boxes:
        s.rect(x, by0, 240, 130, fill=PANEL, stroke=col, width=3, rx=10)
        s.text((x + 120, by0 + 92), name, size=24, color=col, weight=700, mono=True)
        s.text((x + 120, by0 + 60), what, size=20, color=FG)
        s.text((x + 120, by0 + 26), note, size=18, color=DIM)
    s.arrow((272, by0 + 65), (326, by0 + 65), color=FG, width=3)
    s.arrow((572, by0 + 65), (626, by0 + 65), color=FG, width=3)
    # the bin, under the rules track
    bx, bb, bw, bh = 385, 14, 130, 120
    s.path([(bx, bb + bh), (bx + 16, bb), (bx + bw - 16, bb), (bx + bw, bb + bh)], color=DIM, width=5)
    s.path([(bx - 12, bb + bh), (bx + bw + 12, bb + bh)], color=DIM, width=6)
    for i in range(1, 4):
        x = bx + 16 + i * (bw - 32) / 4
        s.path([(x, bb + 14), (x - 3 + i * 1.5, bb + bh - 14)], color=RULE, width=3)
    for (x, y, rr) in [(425, bb + bh + 4, 16), (458, bb + bh + 10, 19), (488, bb + bh + 2, 14)]:
        s.circle((x, y), rr, color=FG, fill=PANEL, width=3)
    s.text((bx + bw + 34, 92), "Do not resurrect", size=24, color=WARN, weight=700, anchor="start")
    s.text((bx + bw + 34, 62), "56 dead ideas, each one dated", size=20, color=DIM, anchor="start")
    s.text((bx + bw + 34, 36), "and the measurement that killed it", size=20, color=DIM, anchor="start")
    dur = 8.0
    lane = by0 - 26
    # promoted: along under the boxes to CLAUDE.md
    s.items.append('<g><circle r="13" fill="%s" stroke="%s" stroke-width="3"/>'
                   '<animateMotion values="%s" keyTimes="0;0.12;0.2;0.32;0.44;1" dur="%gs" '
                   'repeatCount="indefinite" calcMode="linear"/>'
                   '<animate attributeName="opacity" values="1;0" keyTimes="0;0.44" dur="%gs" '
                   'repeatCount="indefinite" calcMode="discrete"/></g>'
                   % (OK, FG, ";".join("%.1f,%.1f" % (x, s._y(y)) for x, y in
                                       [(150, lane), (450, lane), (450, lane), (750, lane), (750, lane),
                                        (750, lane)]), dur, dur))
    # contradicted: to the rules track, then lobbed into the bin
    # a lob off the rules track that lands on top of the pile
    p0, p1, p2 = (450, lane), (580, lane + 60), (470, bb + bh + 30)
    throw = [((1 - u) ** 2 * p0[0] + 2 * u * (1 - u) * p1[0] + u * u * p2[0],
              (1 - u) ** 2 * p0[1] + 2 * u * (1 - u) * p1[1] + u * u * p2[1]) for u in
             [i / 16 for i in range(17)]]
    land = throw[-1]
    pts = [(150, lane), (150, lane), (450, lane), (450, lane)] + throw[1:] + [land, land]
    kt = [0, 0.5, 0.62, 0.68] + [0.68 + 0.14 * i / 16 for i in range(1, 17)] + [0.84, 1]
    s.items.append('<g opacity="0"><circle r="14" fill="%s" stroke="%s" stroke-width="3"/>'
                   '<animateMotion values="%s" keyTimes="%s" dur="%gs" repeatCount="indefinite" '
                   'calcMode="linear"/>'
                   '<animate attributeName="opacity" values="0;1;0" keyTimes="0;0.5;0.97" dur="%gs" '
                   'repeatCount="indefinite" calcMode="discrete"/></g>'
                   % (PANEL, WARN, ";".join("%.1f,%.1f" % (x, s._y(y)) for x, y in pts),
                      ";".join("%.4f" % k for k in kt), dur, dur))
    return s


def boost_factor(tilt_deg):
    """get_throttle_boosted's multiplier, the tilt and its target taken as equal."""
    ct = math.cos(math.radians(tilt_deg))
    return max(0.0, min(1.0, 10 * ct)) / max(0.1, min(1.0, ct))


def boost_flight(boost, R=7.5, cap=10.6, gain=3.0, dt=0.001):
    """A point mass flown by the arc schedule of ACROBATIC_RULES 1.2: the
    perfect loop's ask n = v^2/(R g) + cos(path), the body servoed onto the
    path at rate v/R + 3 (path - body). With boost on, the thrust given is the
    ask through get_throttle_boosted, capped at the Marmott's full throttle
    (10.6 g, the powerloop log of 2026-07-10). Returns (t, x, y, body, asked,
    given) per sample, metres and degrees, until the body has gone round."""
    vb = math.sqrt(5 * G * R)
    x = y = 0.0
    vx, vy = vb, 0.0
    tb, prev, turns, t = 0.0, 0.0, 0.0, 0.0
    out = []
    while t < 8.0:
        v = math.hypot(vx, vy)
        tp = math.atan2(vy, vx)
        if tp - prev < -math.pi:
            turns += 2 * math.pi
        elif tp - prev > math.pi:
            turns -= 2 * math.pi
        prev = tp
        path = tp + turns
        asked = max(v * v / (R * G) + math.cos(path), 0.0)
        tilt = abs(((math.degrees(tb) + 180) % 360) - 180)
        given = min(asked * boost_factor(tilt), cap) if boost else asked
        out.append((t, x, y, math.degrees(tb), asked, given))
        vx += -G * given * math.sin(tb) * dt
        vy += (G * given * math.cos(tb) - G) * dt
        x += vx * dt
        y += vy * dt
        tb += (v / R + gain * (path - tb)) * dt
        t += dt
        if tb >= 2 * math.pi and path >= 2 * math.pi - 0.05:
            break
    return out[::20] + [out[-1]]


def boost_loops():
    """Angle boost on against off, the same loop asked of both. Right: boost
    off, the perfect loop, given is asked. Left: boost on, SIMULATED by
    boost_flight -- the same ask and servo, the thrust through the boost: full
    throttle up the front, nothing at all past 90 deg of tilt, so it sails up
    and back ballistic and full throttle on the back side flings it out. The
    dashed circle is the loop it was asked to fly. Both panels share a scale.
    The flown Marmott (powerloop, 2026-07-10) did the same thing for real:
    10.6 g up the front, 0 g for 1.04 s inverted, +32 m.

    HALF SPEED. At the loop's own pace the fade from 84 to 90 deg of tilt
    takes 65 ms and the arrow reads as a glitch; the slide says half speed."""
    s = Svg(900, 440)
    k, base = 11.5, 48
    flights = []
    for x0, on in ((318, True), (680, False)):
        f = boost_flight(on)
        c = (x0, base + 7.5 * k)
        s.path(arc(c, 7.5 * k, 0, 2 * math.pi), color=RULE if on else ACC, width=3 if on else 5,
               dash="8 8" if on else None)
        pts = [(x0 + q[1] * k, base + q[2] * k) for q in f]
        if on:
            s.path(pts, color=WARN, width=4, arrow=True)
        flights.append((f, pts, on))
    Tmax = max(f[-1][0] for f, _, _ in flights)
    run = 0.88
    dur = round(2 * Tmax / run, 1)
    for f, pts, on in flights:
        ts = [q[0] for q in f]
        att = [-q[3] for q in f]
        hold = 1 - run * ts[-1] / Tmax
        s.fly_att(pts, ts, att, thrust=[q[5] for q in f], dur=dur, hold=hold, scale=1.8, g_px=5.5,
                  tcolor=WARN if on else OK, twidth=5)
        s.fly_att(pts, ts, att, thrust=[q[4] for q in f], dur=dur, hold=hold, scale=1.8, g_px=5.5,
                  tcolor=FG, dash="3 4", glyph=False, twidth=1.4)
    s.path([(470, 40), (470, 400)], color=RULE, width=2)
    s.text((240, 414), "angle boost on (simulated)", size=26, color=WARN, weight=700)
    s.text((680, 414), "angle boost off", size=26, color=OK, weight=700)
    s.text((240, 14), "dashed: the loop it was asked to fly", size=20, color=DIM)
    s.text((680, 14), "given is what was asked", size=20, color=DIM)
    return s


def main():
    for name, fn in FIGURES:
        fn().save(name)
    loop_forces().save("loop_forces.svg")
    sizing().save("sizing.svg")
    float_segments().save("float_segments.svg")
    crash_rotation().save("crash_rotation.svg")
    check_chart().save("fig_check.svg")
    fence().save("fence.svg")
    testing().save("testing.svg")
    freestyle_flow().save("freestyle_flow.svg")
    ball().save("ball.svg")
    twitch().save("twitch.svg")
    loop_shapes().save("loop_shapes.svg")
    crash_story().save("crash_story.svg")
    hidden_target().save("hidden_target.svg")
    dead_ideas().save("dead_ideas.svg")
    rules_pipeline().save("rules_pipeline.svg")
    fence3d().save("fence3d.svg")
    wind_drift().save("wind_drift.svg")
    thrust_sweep().save("thrust_sweep.svg")
    ab_null().save("ab_null.svg")
    # v2: new names, so v1's pictures stay as they were reviewed
    toss().save("ball_flight.svg")
    freestyle_flow(live=True).save("freestyle_flow_live.svg")
    twitch(live=True).save("twitch_live.svg")
    rules_pipeline(live=True).save("rules_pipeline_live.svg")
    rules_pipeline_bin().save("rules_pipeline_bin.svg")
    boost_loops().save("boost_loops.svg")
    ab_null(live=True).save("ab_null_live.svg")
    loop_budget().save("loop_budget.svg")
    loop_shapes_v2().save("loop_shapes_v2.svg")
    no_wing().save("no_wing.svg")
    guided_loop().save("guided_loop.svg")
    split_segments().save("split_segments.svg")
    boost().save("boost.svg")
    pilot_replay().save("pilot_replay.svg")


if __name__ == "__main__":
    main()
