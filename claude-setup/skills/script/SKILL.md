---
name: script
description: Draft or revise a module's spoken script and check its chapter timings. Use when writing script.md or when a script runs long or short.
argument-hint: "<module directory> [what to change]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(python3 tools/script_check.py:*)
---

# Write a module script

## Task: $ARGUMENTS

## Read first

1. `CLAUDE.md` - the Audience Contract, Format, and Writing the Script
   sections. The rules there are not negotiable.
2. The module's `module.yaml` and `README.md`.
3. The series `README.md`, so this module picks up where the last one left
   off and sets up the next.
4. The ArduPilot source for every parameter and mechanism mentioned. Verify,
   do not recall. A wrong parameter description in a teaching video is the
   worst failure this repo has.

## Format

YAML frontmatter, then `## [MM:SS] Title` chapters. Plain paragraphs are
spoken; bracketed uppercase tags are directions and are not counted. See
`CLAUDE.md` for the tag list.

## Drafting order

Write the cold open last. It is the most important thirty seconds and it is
much easier once the rest exists and you know what the payoff actually is.

Work in this order: the demonstration, then the mechanism that explains it,
then the recap, then the framing, then the cold open.

## Check the timing

```bash
python3 tools/script_check.py <module>
python3 tools/script_check.py <module> --retime
```

The estimate is words divided by the frontmatter `wpm`, plus any silent time
booked with a duration tag such as `[B-ROLL 8s]`. Target is 10 to 15 minutes.

If it runs long, cut content, do not speed up the delivery. The usual
candidates, in order: mechanism the viewer cannot act on, a second example
that makes the same point, and history.

## Before finishing

- Read the whole thing aloud. Anything you stumble on gets rewritten.
- Confirm every `[FLIGHT]` and `[SCREEN]` direction refers to footage that
  exists or is on the flight card. Never write a claim as settled when the
  log to support it has not been captured.
- Update `module.yaml` status to `scripted`.
