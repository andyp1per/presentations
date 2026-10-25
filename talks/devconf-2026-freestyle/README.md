# Learning to Fly Freestyle

An automatic aerobatic display on a quad, and what the aircraft would and
would not do. Given at the ArduPilot Developer Conference 2026 in Ottawa
on Saturday 24 October 2026. The Marmott flew the display for real at
Area X.O that afternoon.

The short version: a Lua script in Guided mode flies ten freestyle figures
linked by lines on a 5 inch quad, then hands the aircraft back. Entry
speed sizes every figure, gravity turns the top of a loop, and thrust only
goes where the body points. The lines fly on position targets and the
figures on body rate and thrust, with angle boost off, so the thrust asked
for inverted is the thrust given. Five things went wrong on the real
aircraft, and each one became a rule.

## View it

| File | What it is |
|------|-----------|
| [Play the slides](https://andyp1per.github.io/presentations/talks/devconf-2026-freestyle/slides.html) | The deck as presented, animations running, in the browser: arrows or Space to move, `f` for full screen. The same file is [slides.html](slides.html) here |
| [slides.pdf](slides.pdf) | Every slide: 34 in the talk, 14 backup. Builds are pre-revealed and animations show their first frame |
| [slides.md](slides.md) | The Marp source |
| [script.md](script.md) | The speaker notes, slide by slide |
| [assets/](assets/) | Photos, clips, and the diagrams with `diagrams.py`, the script that draws them |

Nearly every diagram moves, so the HTML is the better read. To present it
with the speaker notes beside each slide, serve it from a clone of this
repository (see "Rebuilding it" below) and press `p`.

## The talk

Three questions, each answered for the same three ideas: entry speed, the
float over the top, and attitude.

| Slides | Part |
|--------|------|
| 1-7 | What freestyle is, last year's flip on a switch, the ten figures in the show, the three questions |
| 8-12 | How should the aircraft move? The thrown ball, the 6 g perfect loop, the ballistic float, and why a quad has no wing |
| 13-17 | How do we fly that motion? Why not replay a pilot, why not position control all the way round, rate and thrust with angle boost off, and the split between them |
| 18-20 | Testing: the four rungs, what RealFlight is and is not good for, then RealFlight flying the show live |
| 21-29 | What went wrong: the drag, the twitch between figures, handing over still rotating, the wind, and a convincing wrong answer. A rule from each |
| 30-34 | The ask upstream, why it is safe to stand near, what you learned, the afternoon flight, questions |
| 35-48 | Backup for questions: the loop maths, drag, figure sizes, angle boost, idle thrust, handovers, the pilot's reference moves, testing, the transmitter menu, the scripting engine, and 56 dead ideas |

The live demo at slide 20 is not in the deck. It is the RealFlight
autotest `RealFlightShowFenceStartOffset` flying one show (`AUTA_SHOWS`
1) through a virtual joystick on the laptop. A full run takes about three
and a half minutes.

## Links

- [ArduPilot PR #34871, Inverted arc and spline waypoints](https://github.com/ArduPilot/ardupilot/pull/34871),
  opened live at slide 15. It lets an arc waypoint fly in a tilted or
  vertical plane, and lets the thrust vector tilt past 90 degrees on Auto
  waypoint legs behind `PSC_TVEC_EN`, which is off by default. It stacks on
  [#34713](https://github.com/ArduPilot/ardupilot/pull/34713), which
  fixes arcs flown straight.
- The ask at slide 30. Master already has the scripting bindings
  `set_target_rate_and_throttle` and
  `set_target_angle_and_rate_and_throttle`, but Guided always applies
  angle boost to them (`ModeGuided::angle_control_run`), and angle boost
  cuts the thrust to zero past 90 degrees. No script on master can fly a
  powered loop. The ask is those commands with a `use_angle_boost` flag.
- [fossuav.com](https://fossuav.com): FOSS UAV and SmallFastDrone.

## What it ran on

- ArduCopter 4.7, SmallFastDrone build, with the AutoAcro applet
- The Marmott: a 5 inch 6S quad on a MambaH743v4
- Native SITL and RealFlight for the autotests and the live demo

The flight code is not in this repository.

## Where the numbers come from

Every number on a slide was recorded with its source as it went onto the
slide. The code references can be checked by anyone; the flight journal
and the project's rules file are not public.

From the ArduPilot source:

- Angle boost and its fade from about 84 degrees (slides 16, 40):
  `get_throttle_boosted` in
  `libraries/AC_AttitudeControl/AC_AttitudeControl_Multi.cpp`.
- Guided always applying it (slide 30): `ModeGuided::angle_control_run`
  on master, checked on 2026-10-06 and again on 2026-10-23 at
  3868711713. Master's `bindings.desc`, checked on 2026-10-06, had no rate
  and climb rate command and no fence polygon binding.
- ArduPilot since 2015 (slide 3): the first upstream commit, 33af275220,
  on 2015-03-22.

From flights, by date in the journal:

- The first Marmott loop, boost on (slide 16): 10.6 g up the front, 0 g
  for 1.04 s inverted, in at 10.4 m and peaking at 42.3 m. 2026-07-10.
- The crash (slides 22, 38): a 15 m loop sized on 0.30 g of drag that met
  0.65. 2026-07-19.
- The twitch (slide 24): lean pegged at 62-70 degrees under `WP_ACC`,
  2026-07-20. Lines lowering `WP_ACC` and `PSC_JERK_NE` for their span,
  2026-09-28.
- Handing over still rotating (slide 25): twelve instances. The immelmann
  half-roll at 764 dps, 142 degrees past upright (SITL, 2026-07-18), and
  the loop-spin pull-out at 182 dps, 36 degrees past level (RealFlight,
  2026-09-21).
- RealFlight (slide 19): 45 displays in an afternoon, the spread down from
  +-7.4 m to +-1.5 m, 2026-09-02. Both sims flying renamed parameters,
  found 2026-07-14.
- The convincing wrong answer (slide 28): r = +0.86, then refuted by the
  lateral A/B in RealFlight, 2026-09-02.
- The wind (slide 31): the Marmott left the line in 3 of 6 displays at
  3-4 m/s across (2026-09-28, 10-02, 10-05) and in none of 3 under 2 m/s
  (2026-10-02).
- Immelmann at 8 m against 12 m (slide 39): the Marmott, 2026-09-21.
- The scripting heap (slide 46): 2026-09-19.
- Thrust at zero throttle, 0.44-0.52 g while rotating (slide 41): rules
  1.8 and 1.9 of the project's rules file.

Simulated, and labelled as such on the slide:

- Slide 11's ballistic loop is flown physics, not a drawn shape: the same
  entry speed as the 15 m perfect loop, a gentler pull at 1.2 R powered
  to 110 degrees, then a true parabola and a mirrored pull-out. It comes
  out at 5.2 g against 6, 18 m tall against 15, and 3.9 m/s over the top
  against 8.6. `loop_shapes_v2` in `assets/diagrams.py`.
- Slide 16's left panel, boost on, is a point-mass simulation with the
  thrust passed through `get_throttle_boosted` and capped at the
  Marmott's 10.6 g. `boost_flight` in `assets/diagrams.py`. The flight it
  stands for is the 2026-07-10 loop above.

The testing counts at slide 18 (105 analysis scripts, 32 SITL and 17
RealFlight autotests) were counted on 2026-10-06 and were unchanged on
2026-10-23.

## Rebuilding it

From the root of this repository, since the tools find the theme from the
current directory:

```bash
python3 tools/render_slides.py talks/devconf-2026-freestyle --serve       # present it; p for the notes
python3 tools/render_slides.py talks/devconf-2026-freestyle               # HTML
python3 tools/render_slides.py talks/devconf-2026-freestyle --format pdf
python3 tools/script_check.py talks/devconf-2026-freestyle                # 20:16 at 150 wpm
python3 talks/devconf-2026-freestyle/assets/diagrams.py                   # redraw the diagrams
```

Renders land in `build/`; `slides.pdf` and `slides.html` here are copies
of them. `diagrams.py` reproduces every committed SVG byte for byte. It
also draws twelve diagrams from the first version of the deck, which this
one does not use and which are not committed. How it all fits together is
in [TOOLING.md](../../TOOLING.md).
