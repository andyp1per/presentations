#!/usr/bin/env python3
"""
Animated SVG diagrams for the decks: the Marmott glyph, a flying-quad
animation, and the ten display figures as icons.

    tools/svganim.py figures <dir>                 write the ten figure icons
    tools/svganim.py filmstrip <svg> [--at 0,1,2]  freeze an animation at times, to a PNG

A deck's own diagrams live in its assets/diagrams.py, which imports this:

    import os, sys
    HERE = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools"))   # from modules/<slug>/assets
    from svganim import *            # noqa: F401,F403
    Svg.outdir = HERE

Everything is SMIL inside the SVG, so it animates inside an <img> on a Marp
slide and freezes at its first frame in a PNG or PDF export. A still cannot
show that anything moves: check the served deck with tools/slide_frames.py,
and an animation's poses with the filmstrip here.

Coordinates are maths-style, x right and y UP; Svg flips them on output.
The colours are the fossuav theme's (themes/fossuav.css, channel/branding.md).

Conventions the drawings follow, each one caught by eye at least once:
- every quad is marmott_glyph(), battery on top, props on hubs over the motors
- thrust points along the body, never along the path
- a quad at speed on a line leans into it: thrust is its only forward force,
  so it cannot be level and fast (fly_att, not fly, for anything with lines)
- a quad cannot hold a line inverted: roll it upright for the leg
- a roll shows from the side as the body flipping over (height scale);
  a yaw as the body going edge-on and back (width scale)
- direction of travel is an arrowhead on the path; a roll is a ring round it
"""

import math
import os
import subprocess
import sys

BG = "#10141a"
PANEL = "#182029"
FG = "#e9eef4"
DIM = "#94a2b1"
ACC = "#ff8c1a"
ACC2 = "#2ec8d8"
WARN = "#ff5252"
OK = "#4ade80"
RULE = "#2a3440"
FONT = "Inter, Segoe UI, DejaVu Sans, sans-serif"
MONO = "JetBrains Mono, DejaVu Sans Mono, monospace"


class Svg:
    """A tiny SVG builder in maths coordinates: x right, y UP."""

    def __init__(self, w, h, bg=None):
        self.w, self.h = w, h
        self.items = []
        self.bg = bg

    def _y(self, y):
        return self.h - y

    def path(self, pts, color=ACC, width=4, dash=None, arrow=False, close=False):
        d = "M " + " L ".join("%.1f %.1f" % (x, self._y(y)) for x, y in pts)
        if close:
            d += " Z"
        extra = ' stroke-dasharray="%s"' % dash if dash else ""
        self.items.append(
            '<path d="%s" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round"%s/>' % (d, color, width, extra))
        if arrow and len(pts) >= 2:
            self.arrowhead(pts[-2], pts[-1], color, size=width * 3.2)

    def arrowhead(self, p0, p1, color, size=12):
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        tip = p1
        left = (tip[0] - size * math.cos(ang - 0.45), tip[1] - size * math.sin(ang - 0.45))
        right = (tip[0] - size * math.cos(ang + 0.45), tip[1] - size * math.sin(ang + 0.45))
        pts = [left, tip, right]
        d = "M " + " L ".join("%.1f %.1f" % (x, self._y(y)) for x, y in pts) + " Z"
        self.items.append('<path d="%s" fill="%s" stroke="%s" stroke-width="1" '
                          'stroke-linejoin="round"/>' % (d, color, color))

    def arrow(self, p0, p1, color=FG, width=3):
        self.path([p0, p1], color=color, width=width, arrow=True)

    def circle(self, c, r, color=DIM, width=2, fill="none", dash=None):
        extra = ' stroke-dasharray="%s"' % dash if dash else ""
        self.items.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" '
                          'stroke-width="%s"%s/>' % (c[0], self._y(c[1]), r, fill, color, width, extra))

    def rect(self, x, y, w, h, fill=PANEL, stroke=None, width=2, rx=8, dash=None):
        s = ' stroke="%s" stroke-width="%s"' % (stroke, width) if stroke else ""
        if dash:
            s += ' stroke-dasharray="%s"' % dash
        self.items.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" '
                          'fill="%s"%s/>' % (x, self._y(y + h), w, h, rx, fill, s))

    def text(self, p, s, size=20, color=FG, anchor="middle", weight=500, mono=False):
        fam = MONO if mono else FONT
        self.items.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="%s" '
                          'font-weight="%s" fill="%s" text-anchor="%s">%s</text>'
                          % (p[0], self._y(p[1]), fam, size, weight, color, anchor, s))

    def rot_marker(self, c, r=11, color=ACC2, ccw=True, width=3):
        """A rotation glyph: 300 deg of arc with a head."""
        a0, a1 = (math.radians(30), math.radians(330)) if ccw else (math.radians(150), math.radians(-150))
        n = 24
        pts = [(c[0] + r * math.cos(a0 + (a1 - a0) * i / n),
                c[1] + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
        self.path(pts, color=color, width=width, arrow=True)

    def roll_ring(self, c, rx=5, ry=14, color=ACC2, width=3, flip=False):
        """A roll: a narrow ring wrapped round a horizontal path, with a head."""
        n = 30
        a0, a1 = (math.radians(110), math.radians(110 + 300))
        if flip:
            a0, a1 = a1, a0
        pts = [(c[0] + rx * math.cos(a0 + (a1 - a0) * i / n),
                c[1] + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
        self.path(pts, color=color, width=width, arrow=True)

    def yaw_marker(self, c, rx=16, ry=6, color=ACC2, width=3):
        """Yaw seen from the side: a flat ellipse with a head."""
        n = 30
        a0, a1 = math.radians(200), math.radians(200 + 320)
        pts = [(c[0] + rx * math.cos(a0 + (a1 - a0) * i / n),
                c[1] + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
        self.path(pts, color=color, width=width, arrow=True)

    def quad(self, c, ang_deg, thrust=0.0, color=FG, tcolor=ACC):
        """Side view of a quad: a bar with two props, thrust along +body-z.

        ang_deg is the body-up direction measured from +x, so 90 is upright.
        """
        a = math.radians(ang_deg)
        ux, uy = math.cos(a), math.sin(a)          # body up
        px, py = uy, -ux                           # along the arms
        L = 16
        p0 = (c[0] - px * L, c[1] - py * L)
        p1 = (c[0] + px * L, c[1] + py * L)
        self.path([p0, p1], color=color, width=5)
        for q in (p0, p1):
            a0 = (q[0] + ux * 5 - px * 9, q[1] + uy * 5 - py * 9)
            a1 = (q[0] + ux * 5 + px * 9, q[1] + uy * 5 + py * 9)
            self.path([a0, a1], color=DIM, width=3)
        if thrust > 0:
            self.arrow((c[0] + ux * 8, c[1] + uy * 8),
                       (c[0] + ux * (8 + thrust), c[1] + uy * (8 + thrust)), color=tcolor, width=3)

    def fly(self, segs, events=(), dur=4.0, hold=0.18, color=FG, scale=1.0, thrust=None, g_px=9):
        """Animate a small quad along the figure, SMIL only, so it runs in an <img>.

        segs:   [(points, weight)] or [(points, weight, "jump")], maths coords,
                flown in order. weight is time per unit length: 1 powered, >1
                slower (the ballistic parts). A "jump" segment starts a new
                subpath, so the quad is moved there without flying the gap.
        events: [(point, kind)] or [(point, kind, dwell)], dwell in the same
                units as length x weight, holding the quad still at that point
                while the event plays. Kinds, as a side view shows them:
                  "roll_half", "roll_full"  the body flips over (height scale)
                  "yaw_cusp"   a yaw 180 where the path reverses: the body
                               foreshortens to edge-on and back (width scale)
                  "yaw"        a yaw 180 with the travel unchanged, so the quad
                               flies on backwards: edge-on and back, no flip
                  "yaw360"     edge-on twice
                  "reverse"    the path retraces with the nose held (the rewind)
        thrust: optional per-point thrust in g, one value per flown point
                (after joining the segments), drawn as an orange arrow out of
                the props, g_px pixels per g.
        A still render shows the quad at the start of the figure.
        """
        pts, lens, tws, starts, gs = [], [], [], set(), []
        L = T = 0.0
        for seg in segs:
            seg_pts, w = seg[0], seg[1]
            jump = len(seg) > 2 and seg[2] == "jump"
            for k, q in enumerate(seg_pts):
                if pts and not (jump and k == 0):
                    d = math.hypot(q[0] - pts[-1][0], q[1] - pts[-1][1])
                    if d < 1e-6:
                        continue
                    L += d
                    T += d * w
                if jump and k == 0:
                    starts.add(len(pts))
                gs.append(thrust(q) if thrust else 0.0)
                pts.append(q)
                lens.append(L)
                tws.append(T)

        def nearest(q):
            return min(range(len(pts)), key=lambda j: (pts[j][0] - q[0]) ** 2 + (pts[j][1] - q[1]) ** 2)

        # dwells push every later time back
        dwell_at = {}
        for ev in events:
            if len(ev) > 2 and ev[2]:
                dwell_at[nearest(ev[0])] = ev[2]
        shift, tws2, dw_start = 0.0, [], {}
        for i in range(len(pts)):
            tws2.append(tws[i] + shift)
            if i in dwell_at:
                dw_start[i] = tws2[-1]
                shift += dwell_at[i]
        L, T = lens[-1], tws2[-1]
        run = 1.0 - hold
        tn = lambda t: run * t / T

        kp, kt = [], []
        for i in range(len(pts)):
            if i in starts:
                continue
            kp.append(lens[i] / L)
            kt.append(tn(tws2[i]))
            if i in dwell_at:
                kp.append(lens[i] / L)
                kt.append(tn(tws2[i] + dwell_at[i]))
        kp += [1.0, 1.0]
        kt += [run, 1.0]
        d = ""
        for i, (x, y) in enumerate(pts):
            d += ("M" if i == 0 or i in starts else " L") + " %.1f %.1f" % (x, self._y(y))

        frames = [(0.0, (1, 1))]
        sy = 1
        rframes, rot = [(0.0, 0.0)], 0.0
        for ev in events:
            i = nearest(ev[0])
            kind = ev[1]
            t0 = tn(dw_start.get(i, tws2[i]))
            t1 = tn(dw_start[i] + dwell_at[i]) if i in dwell_at else t0
            tc = (t0 + t1) / 2
            if kind == "roll_half":
                frames += [(tc - 0.045, (1, sy)), (tc + 0.045, (1, -sy))]
                sy = -sy
            elif kind == "roll_full":
                frames += [(tc - 0.06, (1, sy)), (tc, (1, -sy)), (tc + 0.06, (1, sy))]
            elif kind == "yaw_cusp":
                frames += [(tc - 0.05, (1, sy)), (tc - 0.001, (0, sy)),
                           (tc + 0.001, (0, -sy)), (tc + 0.05, (1, -sy))]
                sy = -sy
            elif kind == "yaw":
                a, b = (t0, t1) if t1 > t0 else (tc - 0.06, tc + 0.06)
                frames += [(a, (1, sy)), ((a + b) / 2, (0, sy)), (b, (1, sy))]
            elif kind == "yaw360":
                a, b = (t0, t1) if t1 > t0 else (tc - 0.08, tc + 0.08)
                q = (b - a) / 4
                frames += [(a, (1, sy)), (a + q, (0, sy)), (a + 2 * q, (1, sy)),
                           (a + 3 * q, (0, sy)), (b, (1, sy))]
            elif kind == "reverse":
                frames += [(tc - 0.001, (1, sy)), (tc + 0.001, (1, -sy))]
                sy = -sy
            elif kind == "pitch":
                # (start point, "pitch", 0, degrees, end point): the body turns
                # that far against the path between the two points, SVG sense
                tb = tn(tws2[nearest(ev[4])])
                rframes += [(t0, rot), (tb, rot + ev[3])]
                rot += ev[3]
        frames += [(run, (1, sy)), (1.0, (1, sy))]
        rframes += [(run, rot), (1.0, rot)]
        frames.sort(key=lambda f: f[0])
        vals = ";".join("%g %d" % f[1] for f in frames)
        kts = ";".join("%.4f" % min(max(f[0], 0.0), 1.0) for f in frames)

        glyph = marmott_glyph()
        if thrust:
            # thrust arrow up the body axis, its length the g at each point
            tk, tv = [], []
            for i in range(0, len(pts), 2):
                t = tn(tws2[i])
                if tk and t <= tk[-1]:
                    continue
                tk.append(t)
                tv.append(gs[i])
                if i in dwell_at:
                    tk.append(tn(tws2[i] + dwell_at[i]))
                    tv.append(gs[i])
            tk += [run, 1.0]
            tv += [gs[-1], gs[-1]]
            dvals = ";".join("M 0 -5 L 0 %.1f" % (-5 - max(g, 0.0) * g_px) for g in tv)
            hvals = ";".join("0 %.1f" % (-5 - max(g, 0.0) * g_px) for g in tv)
            glyph = ('<path stroke="%s" stroke-width="3" stroke-linecap="round" d="M 0 -5 L 0 -5">'
                     '<animate attributeName="d" values="%s" keyTimes="%s" dur="%.1fs" '
                     'repeatCount="indefinite" calcMode="linear"/></path>'
                     '<g><path d="M -5 4 L 0 -4 L 5 4 Z" fill="%s"/>'
                     '<animateTransform attributeName="transform" type="translate" values="%s" '
                     'keyTimes="%s" dur="%.1fs" repeatCount="indefinite" calcMode="linear"/></g>'
                     % (ACC, dvals, ";".join("%.4f" % k for k in tk), dur, ACC, hvals,
                        ";".join("%.4f" % k for k in tk), dur)) + glyph
        if len(rframes) > 3:
            glyph = ('<g>%s<animateTransform attributeName="transform" type="rotate" values="%s" '
                     'keyTimes="%s" dur="%.1fs" repeatCount="indefinite" calcMode="linear"/></g>'
                     % (glyph, ";".join("%.1f" % f[1] for f in rframes),
                        ";".join("%.4f" % min(max(f[0], 0.0), 1.0) for f in rframes), dur))
        self.items.append(
            '<g><g transform="scale(%g)"><g>%s<animateTransform attributeName="transform" type="scale" '
            'values="%s" keyTimes="%s" dur="%.1fs" repeatCount="indefinite" calcMode="linear"/></g></g>'
            '<animateMotion path="%s" rotate="auto" keyPoints="%s" keyTimes="%s" calcMode="linear" '
            'dur="%.1fs" repeatCount="indefinite"/></g>'
            % (scale, glyph, vals, kts, dur, d, ";".join("%.4f" % k for k in kp),
               ";".join("%.4f" % k for k in kt), dur))

    def fly_att(self, pts, times, att, thrust=None, dur=4.0, hold=0.18, scale=1.0, g_px=9,
                tcolor=ACC, dash=None, glyph=True, twidth=3):
        """Fly the quad with its attitude given, SMIL only.

        fly() turns the body with the path (rotate="auto"). That is right in a
        pulled arc, where the body rides the path, and wrong on a line, where a
        quad at speed leans into it. Here the attitude is data.

        pts:    flown points, maths coords
        times:  time at each point, any units, increasing; the flight takes
                (1 - hold) of the cycle and holds its last pose for the rest
        att:    body angle at each point in degrees, SVG sense: 0 is level with
                the props up, positive is clockwise, so a quad flying right
                leans nose-down with a positive angle. Unwrap it: a jump of
                360 between neighbours spins the glyph the long way round.
        thrust: optional g at each point, drawn up the body axis, g_px per g,
                in tcolor, twidth wide, dashed if dash is given. glyph=False draws only the
                arrow, to lay a second one (asked against given) over a quad
                flown with the same points and times.
        A still render shows the first pose.
        """
        T0, T = times[0], times[-1] - times[0]
        run = 1.0 - hold
        kt = ["%.4f" % (run * (t - T0) / T) for t in times] + ["1"]
        kts = ";".join(kt)
        motion = ";".join("%.1f,%.1f" % (x, self._y(y)) for x, y in pts + [pts[-1]])
        rot = ";".join("%.1f" % a for a in list(att) + [att[-1]])
        arrow = ""
        if thrust:
            gs = list(thrust) + [thrust[-1]]
            hs = max(twidth / 3.0, 0.6)
            arrow = ('<path stroke="%s" stroke-width="%g" stroke-linecap="round"%s d="M 0 -5 L 0 -5">'
                     '<animate attributeName="d" values="%s" keyTimes="%s" dur="%gs" '
                     'repeatCount="indefinite" calcMode="linear"/></path>'
                     '<g><path d="M %g %g L 0 %g L %g %g Z" fill="%s"/>'
                     '<animateTransform attributeName="transform" type="translate" values="%s" '
                     'keyTimes="%s" dur="%gs" repeatCount="indefinite" calcMode="linear"/></g>'
                     % (tcolor, twidth, ' stroke-dasharray="%s"' % dash if dash else "",
                        ";".join("M 0 -5 L 0 %.1f" % (-5 - max(g, 0.0) * g_px) for g in gs),
                        kts, dur, -5 * hs, 4 * hs, -4 * hs, 5 * hs, 4 * hs, tcolor,
                        ";".join("0 %.1f" % (-5 - max(g, 0.0) * g_px) for g in gs),
                        kts, dur))
        self.items.append(
            '<g><g transform="scale(%g)"><g>%s%s<animateTransform attributeName="transform" '
            'type="rotate" values="%s" keyTimes="%s" dur="%gs" repeatCount="indefinite" '
            'calcMode="linear"/></g></g><animateMotion values="%s" keyTimes="%s" dur="%gs" '
            'repeatCount="indefinite" calcMode="linear"/></g>'
            % (scale, arrow, marmott_glyph() if glyph else "", rot, kts, dur, motion, kts, dur))

    outdir = "."

    def save(self, name):
        """Write to Svg.outdir, which a deck's diagrams.py sets to its assets/."""
        body = "\n".join(self.items)
        bg = '<rect width="100%%" height="100%%" fill="%s"/>' % self.bg if self.bg else ""
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">\n'
               '%s\n%s\n</svg>\n' % (self.w, self.h, self.w, self.h, bg, body))
        with open(os.path.join(self.outdir, name), "w") as f:
            f.write(svg)


def marmott_glyph():
    """Side view of the Marmott, proportions measured off its side photo.

    Units: 1 = 1/40 of prop tip to prop tip. Plate top at y 0, up is -y. The
    battery rides on top, strapped between the motors (its size is estimated
    for a 6S pack at this scale, not measured). Each prop is a blade tapered
    from a hub over its motor, drawn in front of the battery so the two read
    as two. The whole is shifted so the centre of mass rides the path.
    """
    def blade(hx):
        top, bot = [], []
        for i in range(21):
            dx = -7.9 + 15.8 * i / 20
            half = 0.75 * (1 - (dx / 7.9) ** 2) + 0.12
            top.append("%.2f %.2f" % (hx + dx, -3.2 - half))
            bot.append("%.2f %.2f" % (hx + dx, -3.2 + half))
        return ('<path d="M %s L %s Z" fill="#c9d3de"/>' % (" L ".join(top), " L ".join(reversed(bot))) +
                '<circle cx="%.1f" cy="-3.2" r="0.9" fill="%s"/>' % (hx, FG))
    return "".join([
        '<g transform="translate(0,1.2)">',
        '<rect x="-5.2" y="-4.9" width="10.4" height="4.7" rx="0.7" fill="#55606d" stroke="%s" stroke-width="0.6"/>' % FG,  # battery on top
        '<rect x="-12.8" y="-2.4" width="4" height="2.4" rx="0.6" fill="%s"/>' % FG,   # motors
        '<rect x="8.8" y="-2.4" width="4" height="2.4" rx="0.6" fill="%s"/>' % FG,
        blade(-10.8), blade(10.8),                                      # two props, one per motor
        '<rect x="-13.8" y="0" width="27.2" height="0.9" rx="0.4" fill="%s"/>' % FG,    # frame plate
        '</g>',
    ])


def loop_pt(c, r, phi, mirror=False):
    """Point on a loop flown left to right: phi 0 is the bottom, pi the top."""
    sx = -1 if mirror else 1
    return (c[0] + sx * r * math.sin(phi), c[1] - r * math.cos(phi))


def arc(c, r, phi0, phi1, n=40, mirror=False):
    return [loop_pt(c, r, phi0 + (phi1 - phi0) * i / n, mirror) for i in range(n + 1)]


# --- the ten figures -------------------------------------------------------

PW, PH = 200, 130
BALLISTIC = 2.2       # a ballistic segment's time per unit length, against 1 powered


def pic_floatloop():
    s = Svg(PW, PH)
    c, r = (100, 62), 46
    entry = [(10, 16), loop_pt(c, r, 0)]
    front = arc(c, r, 0, 0.75 * math.pi)
    top = arc(c, r, 0.75 * math.pi, 1.25 * math.pi)
    back = arc(c, r, 1.25 * math.pi, 2 * math.pi)
    exit_ = [loop_pt(c, r, 2 * math.pi), (190, 16)]
    s.path(entry, color=DIM, width=3)
    s.arrowhead((20, 16), (46, 16), DIM, size=10)
    s.path(front, color=ACC)
    s.path(top, color=ACC2, dash="6 7")
    s.path(back, color=ACC)
    s.path(exit_, color=DIM, width=3, arrow=True)
    s.fly([(entry, 1), (front, 1), (top, BALLISTIC), (back, 1), (exit_, 1)])
    return s


def pic_immelmann(float_top=False):
    s = Svg(PW, PH)
    c, r = (120, 62), 46
    entry = [(20, 16), loop_pt(c, r, 0)]
    s.path(entry, color=DIM, width=3)
    s.arrowhead((30, 16), (56, 16), DIM, size=10)
    if float_top:
        up, hang = arc(c, r, 0, 0.8 * math.pi), arc(c, r, 0.8 * math.pi, math.pi)
        s.path(up, color=ACC)
        s.path(hang, color=ACC2, dash="6 7")
        segs = [(entry, 1), (up, 1), (hang, BALLISTIC)]
    else:
        up = arc(c, r, 0, math.pi)
        s.path(up, color=ACC)
        segs = [(entry, 1), (up, 1)]
    top = loop_pt(c, r, math.pi)
    exit_ = [top, (24, top[1])]
    s.path(exit_, color=DIM, width=3, arrow=True)
    ring = (top[0] - 22, top[1])
    s.roll_ring(ring)
    s.fly(segs + [(exit_, 1)], [(ring, "roll_half")])
    return s


def pic_splits():
    s = Svg(PW, PH)
    c, r = (110, 62), 46
    top = loop_pt(c, r, math.pi, mirror=True)
    entry = [(14, top[1]), top]
    s.path(entry, color=DIM, width=3)
    s.arrowhead((24, top[1]), (50, top[1]), DIM, size=10)
    ring = (top[0] - 26, top[1])
    s.roll_ring(ring)
    down = arc(c, r, math.pi, 2 * math.pi, mirror=True)
    s.path(down, color=ACC)
    bot = loop_pt(c, r, 2 * math.pi, mirror=True)
    exit_ = [bot, (14, bot[1])]
    s.path(exit_, color=DIM, width=3, arrow=True)
    s.fly([(entry, 1), (down, 1), (exit_, 1)], [(ring, "roll_half")])
    return s


def pic_flick():
    s = Svg(PW, PH)
    entry = [(10, 50), (60, 50)]
    s.path(entry, color=DIM, width=3)
    s.arrowhead((16, 50), (40, 50), DIM, size=10)
    hop = [(60 + t, 50 + 40 * math.sin(math.pi * t / 80)) for t in range(0, 81, 3)]
    s.path(hop, color=ACC2, dash="6 7")
    s.roll_ring((88, 88), ry=15)
    s.roll_ring((112, 88), ry=15, flip=True)
    exit_ = [(140, 50), (190, 34)]
    s.path(exit_, color=DIM, width=3, arrow=True)
    s.fly([(entry, 1), (hop, BALLISTIC), (exit_, 1)], [((88, 86), "roll_full"), ((112, 86), "roll_full")])
    return s


def pic_pivot():
    """A 180 deg yaw pivot at the end of the run-in, still sliding forward, so
    the float loop climbs the far side tail-first (up the back leg), floats over
    the top, comes down the near side and pulls out flying back the other way."""
    s = Svg(PW, PH)
    y, px, r = 30, 132, 32
    entry = [(10, y), (px, y)]
    s.path(entry, color=DIM, width=3)
    s.arrowhead((20, y), (46, y), DIM, size=10)
    c = (px, y + r)
    up = arc(c, r, 0, 0.75 * math.pi)                  # the back leg, tail first
    top = arc(c, r, 0.75 * math.pi, 1.25 * math.pi)
    down = arc(c, r, 1.25 * math.pi, 1.5 * math.pi)
    r2 = r + 12                                        # the pull-out, onto the line home
    hc = (px - r - r2, y + r)
    hook = [(hc[0] + r2 * math.cos(a), hc[1] + r2 * math.sin(a))
            for a in [-math.pi / 2 * i / 12 for i in range(13)]]
    s.path(up, color=ACC)
    s.path(top, color=ACC2, dash="6 7")
    s.path(down + hook[1:], color=ACC)
    s.yaw_marker((px, y), rx=12, ry=5)
    exit_ = [hook[-1], (12, hook[-1][1])]
    s.path(exit_, color=DIM, width=3, arrow=True)
    s.fly([(entry, 1), (up, 1), (top, BALLISTIC), (down, 1), (hook, 1), (exit_, 1)],
          [((px, y), "yaw", 30)])
    return s


def pic_loopspin():
    s = Svg(PW, PH)
    c, r = (90, 58), 42
    entry = [(10, 16), loop_pt(c, r, 0)]
    s.path(entry, color=DIM, width=3)
    s.arrowhead((16, 16), (42, 16), DIM, size=10)
    up = arc(c, r, 0, math.pi)
    s.path(up, color=ACC)
    top = loop_pt(c, r, math.pi)
    fall = [(top[0] - 8 * math.sin(t * math.pi / 40), top[1] - 3.5 * t) for t in range(0, 21)]
    s.path(fall, color=ACC2, dash="6 7")
    s.yaw_marker((top[0], top[1]), rx=16, ry=6)
    end = fall[-1]
    pull = [(end[0] + 26 * (1 - math.cos(t * math.pi / 24)), end[1] - 26 * math.sin(t * math.pi / 24))
            for t in range(0, 13)]
    s.path(pull, color=ACC)
    exit_ = [pull[-1], (190, pull[-1][1])]
    s.path(exit_, color=DIM, width=3, arrow=True)
    s.fly([(entry, 1), (up, 1), (fall, BALLISTIC), (pull, 1), (exit_, 1)],
          [(up[-2], "yaw360", 110)])
    return s


def pic_drill():
    s = Svg(PW, PH)
    s.path([(10, 62), (190, 62)], color=ACC, width=4, arrow=True)
    s.arrowhead((12, 62), (34, 62), ACC, size=10)
    s.roll_ring((80, 62), rx=6, ry=18)
    s.roll_ring((120, 62), rx=6, ry=18)
    line = [(10 + t, 62) for t in range(0, 181, 4)]
    s.fly([(line, 1)], [((80, 62), "roll_full"), ((120, 62), "roll_full")])
    return s


def pic_rewind():
    s = Svg(PW, PH)
    entry = [(10, 20), (60, 20)]
    s.path(entry, color=DIM, width=3)
    s.arrowhead((14, 20), (38, 20), DIM, size=10)
    c, r = (60, 20 + 80), 80
    ang = lambda t: t * 0.55 * math.pi / 20 * 0.9
    up = [(c[0] + r * math.sin(ang(t)), c[1] - r * math.cos(ang(t))) for t in range(0, 21)]
    s.path(up, color=ACC, arrow=True)
    # the retrace, drawn inside the arc and heading back down, nose still up
    inner = [(c[0] + (r - 16) * math.sin(ang(t)), c[1] - (r - 16) * math.cos(ang(t))) for t in range(20, -1, -1)]
    s.path(inner, color=ACC2, dash="6 7", arrow=True)
    exit_ = [(60, 36), (12, 36)]
    s.path(exit_, color=DIM, width=3, arrow=True)
    s.fly([(entry, 1), (up[:12], 1), (up[11:], BALLISTIC), (inner, BALLISTIC, "jump"), (exit_, 1)],
          [(up[-2], "reverse", 40)])
    return s


FIGURES = [
    ("fig_floatloop.svg", pic_floatloop),
    ("fig_immelmann.svg", pic_immelmann),
    ("fig_flick.svg", pic_flick),
    ("fig_pivot.svg", pic_pivot),
    ("fig_floatimmel.svg", lambda: pic_immelmann(float_top=True)),
    ("fig_splits.svg", pic_splits),
    ("fig_loopspin.svg", pic_loopspin),
    ("fig_drill.svg", pic_drill),
    ("fig_rewind.svg", pic_rewind),
]


# --- command line -----------------------------------------------------------

def _figures(outdir):
    Svg.outdir = outdir
    os.makedirs(outdir, exist_ok=True)
    for name, fn in FIGURES:
        fn().save(name)
        print("  %s" % os.path.join(outdir, name))


def _filmstrip(svg_path, times, out):
    """Freeze an SVG's animation at each time and screenshot the row: the
    quickest way to check poses, since a still render shows only frame 0."""
    import re
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from render_slides import find_browser
    browser, _ = find_browser()
    if not browser:
        sys.exit("no browser found; set CHROME_PATH")
    svg = open(svg_path).read()
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
    w, h = (int(m.group(1)), int(m.group(2))) if m else (900, 400)
    tw = 440
    th = int(tw * h / w)
    svg = re.sub(r'width="\d+" height="\d+"', 'width="%d" height="%d"' % (tw, th), svg, count=1)
    cells = "".join('<div style="display:inline-block;border:1px solid #333;margin:2px">'
                    '<div style="color:#ccc;font:12px sans-serif">%.2fs</div>%s</div>'
                    % (t, svg.replace("<svg ", '<svg data-t="%s" ' % t, 1)) for t in times)
    cols = 4
    page = os.path.abspath(out) + ".html"
    with open(page, "w") as f:
        f.write('<html><body style="background:%s;margin:4px;width:%dpx">%s<script>'
                'document.querySelectorAll("svg[data-t]").forEach(s=>{s.pauseAnimations();'
                's.setCurrentTime(parseFloat(s.dataset.t));});</script></body></html>'
                % (BG, cols * (tw + 8), cells))
    rows = (len(times) + cols - 1) // cols
    subprocess.run([browser, "--headless", "--no-sandbox", "--virtual-time-budget=2000",
                    "--screenshot=%s" % os.path.abspath(out),
                    "--window-size=%d,%d" % (cols * (tw + 8) + 16, rows * (th + 26) + 16),
                    "file://" + page], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(page)
    print("  %s" % out)


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("figures", help="write the ten figure icons")
    f.add_argument("dir")
    m = sub.add_parser("filmstrip", help="freeze an animated SVG at times, to a PNG")
    m.add_argument("svg")
    m.add_argument("--at", default="0,0.5,1,1.5,2,2.5,3,3.5",
                   help="seconds, comma-separated (default 0..3.5 by 0.5)")
    m.add_argument("--out", help="PNG to write (default <svg>-filmstrip.png)")
    args = ap.parse_args()
    if args.cmd == "figures":
        _figures(args.dir)
    else:
        times = [float(t) for t in args.at.split(",")]
        _filmstrip(args.svg, times, args.out or os.path.splitext(args.svg)[0] + "-filmstrip.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
