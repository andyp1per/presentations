---
name: flight-card
description: Build or review the flight plan for a module that includes real flying. Use before going out to shoot flight footage or capture logs.
argument-hint: "<module directory>"
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Build a flight card

## Task: $ARGUMENTS

A flight card exists so two things come back from the field usable the first
time: footage the edit can cut, and a log that can actually settle the
question. Read `CLAUDE.md`, the Modules That Fly and Accuracy sections, then
the module's `script.md` to see exactly which shots and which measurements the
edit is relying on.

## Start from the claim

Write down the claim the module makes, then the measurement that would show
the claim is wrong. If no outcome of the flight could contradict the module,
the flight is illustration, not evidence, and the script must not present it
as proof.

## Make the comparison valid

- A and B back to back, same session, same conditions. Two different days is
  not a comparison.
- Same battery state where thrust matters. Note the wind limit above which the
  comparison stops meaning anything.
- One variable at a time. If two parameters changed, the flight proves
  nothing about either.
- Save a full parameter file per configuration before flying, and record the
  filenames in `module.yaml` under `evidence`.

## Logging

Work out which log messages the module's claims need, and set `LOG_BITMASK`
for them before flying. Check the actual message names in the ArduPilot
source rather than assuming. Getting home with the wrong bitmask means flying
it again.

## Shot list

Go through the script and list every `[FLIGHT]` and `[B-ROLL]` direction as a
checkbox. Add the establishing shot, a close-up for the cutaway, and a piece
to camera on site. Missing one means another trip.

## Safety

- Props off for bench work.
- Failsafes verified on the ground for this exact configuration.
- Abort criteria written as specific named behaviours, agreed out loud before
  arming. "If it looks bad" is not an abort criterion.
- Experimental parameters raise the odds of a departure: high, over clear
  ground, with a switch back to a known-good configuration.

Never talk the user out of a safety step to make the shot work, and never
write a script that requires a manoeuvre the flight card says is unsafe.

## Deliverable

Fill in `flight-card.md` from the template. Leave the After the Flight section
empty; it gets filled in on the day.
