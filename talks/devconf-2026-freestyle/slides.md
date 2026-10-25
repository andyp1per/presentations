---
marp: true
theme: fossuav
paginate: true
math: mathjax
footer: "Learning to Fly Freestyle - ArduPilot DevCon 2026"
---

<!-- _class: title -->
<!-- _paginate: false -->

<style>
/* DevCon 2026 logo, bottom right of every slide; page number beside it */
section {
  background-image: url(assets/devcon2026_logo.png);
  background-repeat: no-repeat;
  background-position: right 22px bottom 12px;
  background-size: auto 54px;
}
section::after {
  right: 150px;
}
</style>

# Learning to Fly Freestyle

## An automatic aerobatic display on a quad

Dr Andy Piper

---

<!-- _paginate: false -->
<!-- _footer: "" -->

![bg](assets/opening_float_loop.webp)

---

## Andy Piper and FOSS UAV

<style scoped>
.me { display: grid; grid-template-columns: 210px 1fr 1.2fr; gap: 18px 34px; align-items: start; }
.me > div:nth-child(1) { grid-column: 1; grid-row: 1; }
.me > div:nth-child(2) { grid-column: 2; grid-row: 1; }
.me > div:nth-child(3) { grid-column: 3; grid-row: 1 / span 2; }
.me > .photos { grid-column: 1 / span 2; grid-row: 2; }
.me h3 { margin-top: 0; }
.me .brand { display: flex; align-items: center; gap: 14px; margin-bottom: 6px; }
.me .brand img { height: 44px; border-radius: 0; }
.photos { display: flex; gap: 18px; align-items: center; }
.photos img { height: 160px; }
.me .sfd { text-align: center; margin-top: 14px; }
.me .sfd img { height: 60px; border-radius: 0; }
</style>

<div class="me">
<div>

![w:210](assets/andy_piper.jpg)

</div>
<div>

### Dr Andy Piper

- PhD, Cambridge
- BEA, Oracle, then startups
- ArduPilot since 2015
- CRSF, DShot, harmonic notch, fast rates

</div>
<div>

<div class="brand"><img src="assets/fossuav_wings.svg"><span class="big">fossuav.com</span></div>

- SmallFastDrone: ArduCopter, small and fast
- 40+ features, 14 merged upstream
- ArduPilot AI Playbooks
- Development, tuning, log analysis

<div class="sfd"><img src="assets/sfd_logo_white.png"></div>

</div>
<div class="photos"><img src="assets/andy_quad_1.jpg"><img src="assets/andy_quad_2.jpg"></div>
</div>

---

## Freestyle

![w:820](assets/freestyle_flow_live.svg)

<div class="cols">
<div>

- Loops, flips, rolls, snaps
- One into the next, no pauses
- Float: hang time over the top

</div>
<div>

- Judged on flow, consistency, creativity
- A pilot does it by feel

</div>
</div>

<span class="dim">Judging criteria: MultiGP freestyle. Can a script fly by feel?</span>

---

## Last year, this year

<div class="cols">
<div>

### 2025

- Flip on a switch
- One figure
- One Lua applet

![h:270](assets/flip_on_a_switch.webp)

<span class="dim">Half speed, ground camera.</span>

</div>
<div>

### 2026

- Ten figures, ten lines
- Two minutes on a line
- Hands the aircraft back

</div>
</div>

---

## The show

<style scoped>
.show { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 48px; }
.show div { display: flex; align-items: center; gap: 20px; }
.show img { height: 78px; width: 120px; object-fit: contain; }
.hard ul { list-style: none; margin: 0; padding: 0; position: absolute; left: 650px; top: 386px; }
.hard li { width: 520px; height: 166px; border: 4px solid var(--warn); border-radius: 14px; box-sizing: border-box; position: relative; }
.hard li span { position: absolute; right: 18px; top: 44px; width: 180px; text-align: right; line-height: 1.25; color: var(--warn); font-weight: 800; }
</style>

<div class="show">
<div><img src="assets/fig_floatloop.svg">1. Float loop</div>
<div><img src="assets/fig_splits.svg">6. Split-S</div>
<div><img src="assets/fig_immelmann.svg">2. Immelmann</div>
<div><img src="assets/fig_loopspin.svg">7. Loop-spin</div>
<div><img src="assets/fig_flick.svg">3. Juicy flick</div>
<div><img src="assets/fig_immelmann.svg">8. Immelmann</div>
<div><img src="assets/fig_pivot.svg">4. Pivot loop</div>
<div><img src="assets/fig_drill.svg">9. Drill</div>
<div><img src="assets/fig_floatimmel.svg">5. Float immelmann</div>
<div><img src="assets/fig_rewind.svg">10. Rewind</div>
</div>

<div class="hard">

* <span>Hard for a human pilot</span>

</div>

<span class="dim">Side view. Grey arrows: direction of travel. Dashed: ballistic. Cyan ring round the path: a roll; flat ring: a yaw.</span>

---

## Three questions

1. How should the aircraft move?
2. How do we fly that motion?
3. What went wrong, and how do we fix it?

<span class="dim">RealFlight flies it live in the middle. The Marmott flies it this afternoon.</span>

---

<!-- _class: section -->

# How should the aircraft move?

## Entry speed, the float over the top, and attitude

---

## Fly it like a thrown ball

![w:760](assets/ball_flight.svg)

<div class="cols">
<div>

- Thrust builds speed: kinetic energy
- The climb trades it for height

</div>
<div>

- Rotate at the top, where it's free
- Carry the speed into the next

</div>
</div>

---

## Entry speed: a perfect loop needs 6 g

$$
\underbrace{\frac{v_{top}^2}{r} = g}_{\text{top: gravity turns it}}
\qquad
\underbrace{v_{bot}^2 = v_{top}^2 + 4 g r = 5 g r}_{\text{falling } 2r}
\qquad
\underbrace{n = 1 + \frac{v_{bot}^2}{g r} = 6}_{\text{bottom: weight + turn}}
$$

<style scoped>
.bud { display: grid; grid-template-columns: 1.6fr 1fr; gap: 24px; align-items: center; }
</style>

<div class="bud">
<div>

![w:590](assets/loop_budget.svg)

</div>
<div>

- Thrust turns it: $v^2/r$
- Bigger: gentler, so faster
- Same 6 g, any size or mass
- Faster: more g, to the limit

</div>
</div>

<span class="dim">A perfect loop: a true circle, no drag, the slowest top. 15 m, at its own pace.</span>

---

## The float: round costs g, ballistic costs shape

![w:840](assets/loop_shapes_v2.svg)

<div class="cols">
<div>

- Round: keeps its speed over the top

</div>
<div>

- Ballistic: spends it on height

</div>
</div>

---

## Attitude: a quad has no wing

![w:900](assets/no_wing.svg)

<div class="cols">
<div>

- Only thrust and gravity turn the path

</div>
<div>

- Thrust points where the body points

</div>
</div>

---

<!-- _class: section -->

# How do we fly that motion?

## Replay a pilot, position control all the way, or split it

---

## Why not replay a pilot?

<div class="cols">
<div>

![w:540](assets/pilot_replay.svg)

- Stick inputs fit one battery, wind, airframe

</div>
<div>

![h:250](assets/steve.jpg)

- The pilot's moves are the reference
- Sim and aircraft checked against them
- Shapes, rates and timing to match

</div>
</div>

<span class="dim">Schematic. The pilot's profile is a feed-forward inside the loop, never an open-loop replay.</span>

---

## Why not position control all the way round?

<style scoped>
.reveal ul { list-style: none; margin: 0.6em 0 0; padding: 0; }
.reveal li { border-left: 5px solid var(--ok); background: var(--panel); border-radius: 8px; padding: 0.5em 1em; font-size: 0.92em; }
.reveal li strong { color: var(--ok); }
.reveal li span { display: block; margin-top: 0.2em; }
</style>

<div class="cols">
<div>

![w:440](assets/guided_loop.svg)

</div>
<div>

- All of it flies in Guided
- Position targets: run-ins, lines, recoveries
- The position controller knows the limits
- It assumes thrust holds you up

* ...or can it?

</div>
</div>

<div class="reveal">

* <strong>It can. The PR goes up now, live.</strong><span>Thrust past 90 deg, vertical arc waypoints. `PSC_TVEC_EN`, off by default.</span>

</div>

---

## Rate and thrust, with angle boost off

![w:720](assets/boost_loops.svg)

<div class="cols">
<div>

- The script sends body rate and thrust
- Every thrust a g-load, measured in flight

</div>
<div>

- Boost on, the first loop climbed 32 m
- Angle boost off: the g asked is given

</div>
</div>

<span class="dim">Half speed; the left is simulated. Dashed arrow: asked. Solid: given.</span>

---

## The split

All of it is Guided: the script picks the command each segment trusts.

![w:700](assets/split_segments.svg)

<div class="ok">

A mode change is the kill switch.

</div>

---

## Testing

<style scoped>
.ladder ul { list-style: none; padding: 0; margin: 18px 0 0; display: flex; flex-direction: column; align-items: center; gap: 14px; }
.ladder li { display: grid; grid-template-columns: 1fr auto; gap: 2px 24px; align-items: center; border: 3px solid var(--dim); border-radius: 10px; padding: 10px 26px; background: var(--panel); box-sizing: border-box; }
.ladder li:nth-child(1) { width: 100%; }
.ladder li:nth-child(2) { width: 88%; border-color: var(--accent-2); }
.ladder li:nth-child(3) { width: 76%; border-color: var(--accent-2); }
.ladder li:nth-child(4) { width: 64%; border-color: var(--accent); }
.ladder .n { font-weight: 800; }
.ladder .c { grid-row: 1 / span 2; grid-column: 2; text-align: right; }
.ladder .w { color: var(--dim); font-size: 0.8em; }
</style>

<div class="ladder">

* <span class="n">Static: Lua benches and log analysis</span><span class="c">105 scripts</span><span class="w">the maths and every flight, checked offline</span>
* <span class="n">Native SITL</span><span class="c">32 tests</span><span class="w">the Rise255 model, the autotest suite</span>
* <span class="n">RealFlight</span><span class="c">17 tests</span><span class="w">the same autotest, a virtual joystick</span>
* <span class="n">The Marmott</span><span class="c">the only witness</span><span class="w">a field card per session</span>

</div>

<span class="dim">Cheapest first; each rung catches what the one above cannot.</span>

---

## Testing in RealFlight

<div class="cols">
<div>

### What it's for

- 45 displays in an afternoon
- Spread: +-7.4 m to +-1.5 m
- Does the show hold together

</div>
<div>

### Watch for its limits

- Drag: 0.40-0.45 g vs 0.30
- Idle: 0.83 g vs ~0.2
- Lua at 97 Hz vs 24.5
- The shape of an arc

</div>
</div>

<div class="warn">

For a month both sims flew renamed parameters: dropped silently from a defaults file.

</div>

<span class="dim">Each pair: RealFlight, then the Marmott.</span>

---

<!-- _class: section -->

# Live: RealFlight

## `RealFlightShowFenceStartOffset`

---

<!-- _class: section -->

# What went wrong, and how do we fix it?

## When physical reality intervenes

---

## Problem 1: 19 July, the drag we didn't size for

![w:680](assets/crash_story.svg)

<div class="warn">

`AUTA_LP_DRAG` is not a drag estimate. It is the safety factor.

</div>

<span class="dim">Schematic, numbers from the log. Sized on 0.30 g of drag; it met 0.65.</span>

---

## Rule 1: always finish the figure

<div class="cols">
<div>

![w:560](assets/crash_rotation.svg)

</div>
<div>

![w:420](assets/fig_check.svg)

- Refuse only at the start, on height
- Once started, give up the circle
- Rotation is free: finish on it

</div>
</div>

<span class="dim">A check before the figure can't see inside it: the loop that flew was further short than the one that crashed.</span>

---

## Problem 2: the twitch between figures

<style scoped>
.tw { display: grid; grid-template-columns: 1.7fr 1fr; gap: 28px; align-items: center; }
</style>

<div class="tw">
<div>

![w:700](assets/twitch_live.svg)

</div>
<div>

- The next figure wants a new speed
- Position control goes as hard as `WP_ACC` allows
- The quad slams to its lean limit, then swings back

<div class="ok">

Rule 2: turn the position controller down between figures.

</div>

</div>
</div>

<span class="dim">Schematic. Fix: each line lowers `WP_ACC` and `PSC_JERK_NE` for its span.</span>

---

## Problem 3: handing over still rotating

Thrust is how a quad climbs, brakes and accelerates, and it points where the body points.

![w:600](assets/thrust_sweep.svg)

<div class="ok">

Rule 3: don't correct at the wrong moment. Brake the rotation, then thrust.

</div>

<span class="dim">Twelve instances. Immelmann: 764 dps, 142 deg past upright. Loop-spin: 182 dps, 36 deg past level.</span>

---

## Problem 4: the wind

<div class="cols">
<div>

![w:520](assets/wind_drift.svg)

</div>
<div>

- Figures fly the air, lines the ground
- A mirrored repeat doubles the drift
- Placement centres the box, can't shrink it
- The fence knows nothing of wind

</div>
</div>

<div class="params">

`EK3_DRAG_MCOEF` = 0.22: EKF3 estimates wind only by drag fusion; fitted off the Marmott's own logs

</div>

<div class="ok">

Rule 4: don't chase the wind on the lines. Paying it back grew the box 60-110 m (RealFlight).

</div>

<span class="dim">26 Sep: 76 m from its mirror in 1-2 m/s along. 28 Sep: 34 m off the line in 3-4 m/s across.</span>

---

## Building it with Claude Code

![w:820](assets/rules_pipeline_bin.svg)

<div class="cols">
<div>

- Every session reads all of it first
- Rules promoted only once proven

</div>
<div>

- 56 dead ideas, killed by measurement
- Offline, SITL, RealFlight, then fly

</div>
</div>

---

## Problem 5: a convincing wrong answer

<style scoped>
.claim { font-size: 30px; font-weight: 700; margin: 4px 0 18px; }
.claim span { color: var(--dim); font-weight: 500; }
.stamp { display: inline-block; border: 3px solid var(--ok); color: var(--ok); border-radius: 6px; padding: 0 8px; font-size: 20px; font-weight: 800; letter-spacing: 2px; transform: rotate(-8deg); margin-left: 6px; }
.ab ul { list-style: none; padding-left: 0; margin: 0; }
.wrong ul { list-style: none; margin: 0; padding: 0; position: absolute; top: 126px; left: 700px; }
.wrong li { color: var(--warn); border: 6px solid var(--warn); border-radius: 12px; padding: 0 18px; font-size: 56px; font-weight: 900; letter-spacing: 4px; transform: rotate(-9deg); background: rgba(16, 20, 26, 0.25); }
</style>

<div class="claim"><span>Claude:</span> the sideways speed handed over causes the drift</div>

<div class="cols">
<div>

* **Correlation:** more sideways speed, more drift, r = +0.86 <span class="stamp">TRUE</span>
* **Control:** two identical immelmanns, 11.6 m against 6.1 m, 4 runs of 4 <span class="stamp">TRUE</span>
* **Mechanism:** a line of code commands them differently <span class="stamp">TRUE</span>

</div>
<div class="ab">

* ![w:440](assets/ab_null_live.svg)

</div>
</div>

<div class="wrong">

* WRONG

</div>

<span class="dim">RealFlight, 2 Sep. Every fact was true; the conclusion was not.</span>

<div class="ok">

Rule 5: measure every time it explains. Two runs, four mechanisms dead in one day.

</div>

---

## The rules

<style scoped>
table { font-size: 1.15em; }
</style>

| Problem | Rule |
|---|---|
| 1. The drag we didn't size for | Always finish the figure |
| 2. The twitch between figures | Turn position control down between figures |
| 3. Handing over still rotating | Brake the rotation, then thrust |
| 4. The wind | Don't chase it on the lines |
| 5. A convincing wrong answer | Measure every time it explains |

---

## What the branch needed

<div class="params">

set_target_rate_and_throttle(..., use_angle_boost)
set_target_angle_and_rate_and_throttle(..., use_angle_boost)
set_target_rate_and_climbrate(...)
AC_Fence polygon build bindings

</div>

Master has the first two, always with angle boost, which cuts the thrust to zero inverted.

<div class="ok">

The ask: rate and angle commands with angle boost off, so a script can fly inverted.

</div>

---

## Why it's safe to stand near

<style scoped>
.pics { display: flex; gap: 40px; align-items: center; }
</style>

<div class="pics">

![w:380](assets/fence3d.svg)

![w:400](assets/crsf_menu.jpg)

</div>

<div class="cols">
<div>

- Fenced, report only, while it flies
- Every figure height-gated first
- A mode change hands it back

</div>
<div>

- A local pilot on one switch
- Moves, sizes, floor: all from the radio

</div>
</div>

<div class="warn">

Wind is the limit. The Marmott has only left the line in 3 m/s or more across. Line down the wind; over 2 m/s across, no show.

</div>

<!-- Go/no-go: lay the line down the wind on the day. Over 2 m/s across, no show. FENCE_ACTION 0, report only, agreed with the site; the pilot's mode change is what acts. -->

---

## What you learned

<style scoped>
.learn { display: grid; grid-template-columns: repeat(3, 1fr); gap: 34px; }
.learn h3 { margin-top: 0; font-size: 1.0em; }
.strip { display: flex; gap: 6px; margin-top: 28px; }
.strip img { height: 64px; width: 98px; object-fit: contain; }
</style>

<div class="learn">
<div>

### How should it move?

- Entry speed sizes the figure
- Gravity turns the top
- Thrust goes where the body points

</div>
<div>

### How do we fly it?

- Position control on the lines
- Rate and thrust in the figures
- Angle boost off to go inverted

</div>
<div>

### What went wrong?

- Always finish the figure
- Brake the rotation, then thrust
- Measure every time it explains

</div>
</div>

<div class="strip">
<img src="assets/fig_floatloop.svg"><img src="assets/fig_immelmann.svg"><img src="assets/fig_flick.svg"><img src="assets/fig_pivot.svg"><img src="assets/fig_floatimmel.svg"><img src="assets/fig_splits.svg"><img src="assets/fig_loopspin.svg"><img src="assets/fig_immelmann.svg"><img src="assets/fig_drill.svg"><img src="assets/fig_rewind.svg">
</div>

---

<!-- _class: title -->

# This afternoon

## Area X.O, Saturday pm

---

<!-- _class: title -->
<!-- _paginate: false -->

# Questions

---

<!-- _class: section -->

# Backup

## For questions: the full maths, the handovers, the tooling

---

## A loop is an energy budget

<div class="cols">
<div>

![w:520](assets/sizing.svg)

</div>
<div>

### Assumptions

- A point mass on a circle
- Thrust along the body, body on the path
- Drag: a constant $d$ g along the path
- At the top, gravity alone turns it

</div>
</div>

---

## The sizing law: size = $2r$

$$
\begin{aligned}
\text{top:}\quad & v_{top}^2 = m^2\, g\, r \\[4pt]
\text{climb } 2r\text{:}\quad & v_{bot}^2 = v_{top}^2 + 4\, g\, r + 2\pi d\, g\, r \\[4pt]
\text{bottom:}\quad & n_{bot} = 1 + \frac{v_{bot}^2}{g\, r} = m^2 + 5 + 2\pi d \\[4pt]
\text{rate:}\quad & \omega_{bot} = \frac{v_{bot}}{r}
\end{aligned}
$$

- $m$ is the top-speed multiplier; $m = 1$ means gravity alone turns the top
- $d$ = `AUTA_LP_DRAG` = 0.2 gives $n_{bot}$ = 7.3 g
- Checked: $v_{top}$ 5.81 m/s predicted, 5.85 flown

<span class="dim">Not modelled: idle thrust at the top (0.17-0.22 g) pinches it; real drag grows with speed.</span>

---

## Drag was the finding

$$
v_{bot}^2 = g\,r\,(5 + 2\pi d) \qquad d = 0.3:\ \ 2\pi d = 1.9
$$

- Drag is over a quarter of the entry energy
- Leave it out: the loop reaches the top slow
- Slow at the top, it falls through itself
- That is the 19 July crash

<div class="warn">

`AUTA_LP_DRAG` is not a drag estimate. It is the safety factor.

</div>

<span class="dim">10 Jul: first loop, no drag term. 11 Jul: a budget, measured level. 19 Jul: read 0.65 g, sized on 0.30. Same speed and airframe reads 0.47 to 0.65 g.</span>

---

## A bigger figure costs sky, not g

| Immelmann size | 8 m | 12 m |
|---|---|---|
| Bottom pull | same | same |
| Arc climb | 6.3-7.3 m | 10.0-10.5 m |
| Pitch rate | 235 dps | 192 dps |
| Its leg of the box | +19 to +27 m | +51 m |

<span class="dim">Marmott, 2026-09-21. Floor 8 m: smaller cannot be sized. Ceiling ~15 m: the run-up cannot build the speed.</span>

---

## Angle boost: right for hover, wrong for figures

$$
T_{out} = T_{in} \cdot \frac{\mathrm{clamp}(10\cos\theta,\ 0,\ 1)}{\max(\cos\theta_{target},\ 0.1)}
$$

<div class="cols">
<div>

### What it's for

- Tilting loses vertical thrust
- Divide by $\cos\theta$ to hold height
- Fades from ~84 deg, zero past 90

</div>
<div>

### Why it's off here

- In a figure, thrust is the control
- The g asked must be the g given
- It removes thrust inverted, where loops pull

</div>
</div>

<span class="dim">`AC_AttitudeControl_Multi::get_throttle_boosted`. Off: every thrust is a g-load, $g_0 + k \cdot$ throttle, measured in flight.</span>

---

## Zero throttle is not zero thrust

- The mixer lifts the average for authority
- 0.44-0.52 g at zero, while rotating
- So "ballistic" still carries thrust
- An upright cut arrests at ~0.5 g, not 1

<div class="params">

`MOT_SPIN_MIN` at the bottom of the thrust curve
Above it, every "zero thrust" segment carries thrust

</div>

<span class="dim">Marmott. Idle alone is 0.17-0.22 g; RealFlight's is 0.83 g.</span>

---

## Where segments hand over

| Handover | What went wrong | Fix |
|---|---|---|
| Line to line | `WP_ACC` pegged: the twitch | Lines deliver the next entry speed |
| Arc to apex | Half-roll handed over at 764 dps | Brake to an attitude, then hand over |
| Fall to hover | Recover aimed low: 3.6 m under the start | Aim at the height the figure meant |

Clean when speed and load are continuous across it.

---

## What the pilot did give us

<div class="cols">
<div>

- Reference moves: log271, and Steve on the Marmott
- Sim and aircraft checked against the same log
- Shapes, rates and timing to match

</div>
<div>

![h:300](assets/steve.jpg)

</div>
</div>

<div class="ok">

Caught: our knife edge, tuned in RealFlight, was a wingover. It fell 4 m where the pilot's falls 12.6, because his bank is a schedule (86, 68, 20 deg), not a hold.

</div>

<span class="dim">The pilot's profile is a feed-forward inside the loop, never an open-loop replay.</span>

---

## Four rungs of testing

![w:820](assets/testing.svg)

---

## Test a move from the transmitter

<div class="cols">
<div>

![w:560](assets/crsf_menu.jpg)

</div>
<div>

- Pick any of 19 moves
- Resize it between runs: 8-30 m
- Set the height floor
- Flip Scripting1 to fly it
- No laptop in the field

</div>
</div>

---

## Living inside the scripting engine

- 500 KB of heap for every script
- Split moves by show, not family
- Compile on the idle path, not load
- Lua's 100-local limit: 101 fails silently
- 24.5 Hz on the aircraft: 29 deg per tick at 700 dps

<span class="dim">Load order was worth more than bytes: one moved require took the peak 500k to 475-485k.</span>

---

## Rules it earned

- A figure is never energy-limited; only its radius is
- A move is handed the speed it wants
- A handover gate is guilty until measured
- The display is bimodal: one run proves nothing
- Do not tune the loop against RealFlight

---

## Do not resurrect: 56 dead ideas

![w:820](assets/dead_ideas.svg)

<span class="dim">Each was flown, believed, and killed by measurement. Several were re-invented twice.</span>
