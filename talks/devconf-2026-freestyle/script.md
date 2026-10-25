---
module: devconf-2026-freestyle
target_runtime: "20:16"
wpm: 150
---

# Learning to Fly Freestyle - script

[NOTE] The speaker notes for the DevCon 2026 talk. render_slides.py --serve attaches each slide's lines to it as presenter notes by the [SLIDE n] directions, so the numbers here must match slides.md. [CLICK] is a build step on the current slide and stays in the notes as a cue; [NOTE] lines are reminders and are left out. The room is ArduPilot developers: they know the controllers and the bindings, and what they lack is what a quad does past ninety degrees.

## [00:00] Opening

Can a script fly freestyle? Not a flip on a switch. A whole display, figure
into figure, with no pauses, that hands the aircraft back at the end.

[SLIDE 2]

[NOTE] Confirm the clip is the applet flying, not a pilot, before saying so.

That's the Marmott, a five inch quad, flying a float loop with nobody on the
sticks. Watch the top. It hangs there, slow and weightless, and turns over
before it falls back into the pull. That pause is what this talk is about.

[SLIDE 3]

I'm Andy Piper. I've been writing ArduPilot code since 2015: CRSF, DShot,
the harmonic notch, and the fast rate attitude loop. My background is
distributed systems; drones started as the hobby.

FOSS UAV is my company. We do ArduPilot development, tuning and log
analysis. We also maintain SmallFastDrone, a build of ArduCopter for small,
fast quads, with forty-odd features ahead of the stable release and
fourteen of them now merged upstream. Everything you'll see today runs on
an SFD branch. If any of it is useful to you, it's all at fossuav dot com.

## [01:06] What freestyle is

[SLIDE 4]

Freestyle pilots don't fly figures one at a time. They link them. A loop
flows into a roll and the roll into a dive, and nothing stops in between.
MultiGP judges it on flow, consistency and creativity, and pilots love a
float: hang time over the top. All of it is done by feel. The question for
a script is what that feel is made of.

[SLIDE 5]

Last year I showed you a flip on a switch. One figure, one applet, flown on
demand. This year it's ten figures with a line between each, two minutes of
display, and the aircraft handed back at the end. Ten is not one, ten times.
Every handover between two figures is a problem of its own.

[SLIDE 6]

Here's the show, side on, travelling right. Dashed means ballistic: the
quad isn't pushing. Some are the classics. Some came from watching pilots,
like the juicy flick and the pivot loop.

[CLICK]

And two of them are hard for a human. The drill rolls along a line, and
every roll has to be paid for with a pulse of thrust at the right moment.
The rewind climbs, stops, and retraces its own path backwards with the nose
up. A pilot can't see the timing either of those needs. A script can
measure it.

[SLIDE 7]

Three questions, in order. How should the aircraft move? How do we fly that
motion? And what went wrong, and how do we fix it? RealFlight flies the
show live in the middle, and the Marmott flies it for real this afternoon.

## [02:48] How should the aircraft move?

[SLIDE 8]

The physics first. Three ideas carry every figure in the show: entry speed,
the float over the top, and attitude.

[SLIDE 9]

Throw a ball and you've flown most of this show. Thrust builds speed, which
is kinetic energy, and the climb trades it for height. At the top there's
almost nothing left and almost nothing holding it, so the body is free to
turn. That's where the flips go. Then gravity hands the speed back, and you
carry it into the next figure.

Watch the quad. It tosses with the props up and coasts with the thrust off.
It has no reason to point along its path. Neither does a ball.

[SLIDE 10]

This is the only maths in the talk, and the assumptions are on the slide. A
perfect loop: a true circle, no drag, the top crossed as slowly as gravity
allows. At the top, gravity alone turns it. Falling two radii adds four g r
to the speed squared. At the bottom you need one g to hold the weight and
five more to turn the path. Six g.

Mass and size cancel, so that's six g on any airframe at any size. A bigger
loop is a gentler arc flown faster, not a harder pull. Enter faster and the
bottom pull goes up, until the airframe runs out of thrust. And yes, the
gauge reads zero at the top. Up there the quad is weightless.

[SLIDE 11]

Round costs g. Ballistic costs shape. The left loop pulls all the way round
and keeps its speed over the top. The right one pulls a gentler arc, goes a
little past vertical, and lets go. From there it's a parabola. Same entry
speed, but it spends that speed on height: about five g at the bottom
instead of six, three metres taller, and less than half the speed over the
top. The price is that it isn't round, and it doesn't come back to where it
started. That's the float loop, and it's the one pilots love.

[SLIDE 12]

The third idea catches out anyone who came from planes. A quad has no wing.
Nothing turns the path except thrust and gravity, and thrust points where
the body points. On the line the quad leans in to make speed. In the loop
the thrust has to point at the centre, and over the top the centre is the
ground. On the right, with the thrust off, the body can turn however it
likes and the path doesn't care. Attitude is how you aim the only force you
have.

## [05:38] How do we fly that motion?

[SLIDE 13]

Second question. There are three ways to fly it: replay a pilot, let
position control fly the lot, or split it.

[SLIDE 14]

The obvious answer is to record a good pilot and play the sticks back. It
fails the first time the battery is lower or the wind has moved. Stick
inputs are open loop, and they fit one battery, one wind and one airframe.

What the pilot does give us is the reference. Steve flew the reference
moves on the Marmott, and the sims and the aircraft are both checked
against those: the shapes, the rates and the timing. The pilot's profile
goes in as feed-forward inside a closed loop. It is never replayed.

[SLIDE 15]

Everything here flies in Guided. The real question is which Guided command.
Position targets are the obvious one. They fly run-ins, lines and
recoveries beautifully, and the position controller knows the vehicle's
limits. But it assumes the thrust is holding you up. Below the equator of a
loop, that's true. Above it, the thrust that turns the path is pointing at
the ground, and the controller's model of the world has stopped applying.

[CLICK]

Or has it?

[CLICK]

[NOTE] The PR goes up live from arc-fixes-master. Squash its two fixup commits and push it to the fork before the talk, so opening it is one click. Put its number on the slide afterwards.

It can. There's a PR for exactly that, and it goes up now. Inverted
S-curves through arc waypoints, with the thrust allowed past ninety
degrees. It's behind PSC_TVEC_EN, and off by default.

[SCREEN] Browser: open the PR from arc-fixes-master.

[SLIDE 16]

If not position targets, then rate and thrust. The script asks for a body
rate and a thrust every tick, and every thrust is a g-load, read off a map
the aircraft measures in flight.

There's a trap on that path too. Guided's angle control applies angle
boost. It divides the thrust by the cosine of the tilt, so a hover holds
its height in a lean. From eighty-four degrees it fades the thrust out, and
past ninety it's zero. On the left is what that does to a loop, simulated,
at half speed. Full throttle up the front, nothing at all over the top, and
the quad is flung out of its own figure.

That isn't hypothetical. The Marmott's first loop did exactly this, and
climbed thirty-two metres. Turn the boost off and the g you ask for is the g
you get.

[SLIDE 17]

That's the split. All of it is Guided, and the script picks the command
each segment can trust. Position targets fly the run-up, lean the quad in
for speed, and level it at the gate. Rate and thrust fly the pull. Over the
top the thrust drops to idle and gravity turns it. Rate and thrust pull it
out, and position targets take it back. And because it's all
Guided, a mode change takes the aircraft away from the script.

## [08:36] Testing, and the demo

[SLIDE 18]

Before any of this goes near a field, it climbs a ladder.

[CLICK]

Offline first: Lua benches and log analysis. A hundred and five scripts,
and every flight goes through them.

[CLICK]

Then native SITL, on the Rise255 model, with thirty-two autotests.

[CLICK]

Then RealFlight: the same autotests through a virtual joystick, seventeen
of them.

[CLICK]

And then the Marmott, the only witness that counts. Each rung is cheaper
than the one below it, and catches what the one above can't.

[SLIDE 19]

RealFlight is the rehearsal room. Forty-five displays in an afternoon, and
the spread came down from seven metres to a metre and a half. It tells you
whether the show holds together.

It isn't the aircraft. Its drag is higher, its idle thrust is four times
the Marmott's, and it runs the Lua four times as fast. Watch the demo for
the show, not for the shape of an arc. And one warning from experience: for
a month, both simulators flew renamed parameters that a defaults file had
dropped without a word.

[SLIDE 20]

[SCREEN 215s] RealFlight on the laptop: the autotest RealFlightShowFenceStartOffset, one show.

[NOTE] Have the timed fallback recording ready in case RealFlight will not start.

A box appears on the map: that's the fence, drawn on the heading.

It backs away fifteen metres, so the box centres on us.

The short drop and the hard climb is the thrust calibration: thrust
against throttle, measured in the air.

A loop that hangs at the top is the float loop. A fast roll one way and
back is the juicy flick. A half turn of yaw, then a float loop, is the
pivot loop. A spin on top of a loop is the loop-spin.

And when it stops and hovers, it has handed the aircraft back to Loiter.

## [13:59] What went wrong, and how do we fix it?

[SLIDE 21]

Third question. In RealFlight the plan holds. On the Marmott, the airframe
and the air don't fly the plan. Here are five problems, and the rule each one taught us.

[SLIDE 22]

Problem one. The nineteenth of July, a fifteen metre loop. It was sized on
nought point three g of drag and met nought point six five. It pulled five
point eight five g of the seven point nine it asked for, with the mixer
saturated, and went vertical at eleven metres a second when it wanted
twenty. It coasted over the top inverted with nothing left, and came down.
The drag parameter, AUTA_LP_DRAG, is not a drag estimate. It's the safety
factor.

[SLIDE 23]

Rule one: always finish the figure. There's no safe way out of a loop part
way up. Refuse only at the start, on height. Once it's started, give up the
circle if you have to, but finish on rotation, because rotation is free:
two hundred and seventy degrees at seven hundred a second is under half a
second. And a check before the figure can't see inside it. The loop that
flew clean was further short of its pull than the one that crashed.

[SLIDE 24]

Problem two was the twitch between figures. The next figure wants a new
speed, and position control goes for it as hard as WP_ACC allows. In
RealFlight the lean sat pinned at its seventy degree limit in every gap.
Leashing the command upstream changed nothing, because the position
controller reshapes whatever you hand it.

Rule two: turn the position controller down between figures. Each line
ramps the speed against the clock, lowers WP_ACC and the jerk limit for its
own span, and puts them back when it hands over.

[SLIDE 25]

Problem three is the one we found twelve times: handing over while the body
is still rotating. Thrust points where the body points, so thrust while
you're still turning sweeps the push round with you. The immelmann's half
roll was handed over at seven hundred and sixty-four degrees a second, and
swung a hundred and forty-two degrees past upright. The loop-spin's
pull-out handed over still pitching, and the recover added throttle into
the swing.

Rule three: don't correct at the wrong moment. Brake the rotation, then
thrust.

[SLIDE 26]

Problem four is the wind. Figures fly the air, and lines fly the ground. The
wind moves every figure, and a mirrored second show doubles the drift
instead of cancelling it. On the twenty-sixth of September, show two ended
seventy-six metres from its mirror, in one or two metres a second along the
line. The obvious fix is to pay the wind back on the lines. In RealFlight
that grew the box by sixty to a hundred and ten metres.

Rule four: don't chase the wind on the lines.

[SLIDE 27]

A word on how this was built, because it was built with Claude Code. What
made that work wasn't the model. It was the record. Every flight goes into
a dated journal, over seventeen thousand lines of it. A finding goes onto a
rules track and is promoted only once it's proven: three incidents, or two
airframes. Anything contradicted goes in the bin, dated, with the
measurement that killed it. Fifty-six dead ideas so far, and every session
reads all of it before it touches the code.

[SLIDE 28]

Problem five is one Claude got wrong, convincingly. The claim: the sideways
speed handed over at the start of a figure causes its drift off the line.

[CLICK]

The correlation was real. More sideways speed, more drift, r of plus nought
point eight six.

[CLICK]

The control was real. Two identical immelmanns drifted eleven point six
metres against six point one, four runs out of four.

[CLICK]

And the mechanism was in the code: one line commanded them differently.
Every fact was true.

[CLICK]

We cut the sideways speed by more than half.

[CLICK]

The drift didn't move. Rule five: measure every time it explains. Two runs
killed four mechanisms in one day.

[SLIDE 29]

Three of these rules are about timing: when to commit, when to correct, and
when to push. One is about where the air is going. And one is about us.

## [18:33] Close

[SLIDE 30]

Which brings me to the ask. Master already has set_target_rate_and_throttle
and the angle version of it. But Guided always applies angle boost to them,
and angle boost cuts the thrust to zero inverted. No script on master can
fly a powered loop. The branch threads a use_angle_boost flag through to
Lua. That's the ask: those commands, with the boost off. The climb rate and
fence polygon bindings are on the branch too, if they're useful to anyone
else.

[SLIDE 31]

[NOTE] Settled 2026-10-23: FENCE_ACTION 0, agreed with the site. Report only still means Guided refuses targets outside the fence. The field card's along-line rule still stands: over ~1 m/s along, one show.

It flies near people this afternoon, so here's why that's reasonable. The
fence is live only while the show flies, drawn on the heading and sized
from the plan. It reports a breach rather than acting on it, and that's
agreed with the site. What acts is the local pilot on one switch: a mode
change hands it back. Every figure checks its height before it starts, and
the moves, their sizes and the height floor are all set from the
transmitter. Wind is the limit. The Marmott has only left the line in three
metres a second or more across it. So the line goes down the wind, and
over two across, there's no show.

[SLIDE 32]

If you keep one thing from each part: speed and gravity fly the figure, not
thrust. Fly the lines on position and the figures on rate and thrust, with
the boost off. And when the aircraft surprises you, measure before you
explain.

[SLIDE 33]

This afternoon the Marmott flies the whole show for real, at Area X.O.
Come and watch the float.

[SLIDE 34]

Thank you. Questions?
