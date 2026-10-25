---
name: publish
description: Produce the YouTube title, description, chapters, tags and thumbnail brief for a module. Use when a module is edited and ready to upload.
argument-hint: "<module directory>"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(python3 tools/script_check.py:*), Bash(python3 tools/module_index.py:*)
---

# Prepare a module for upload

Channel: https://www.youtube.com/@andypiper5285

## Task: $ARGUMENTS

Read the module's `script.md`, `README.md` and `module.yaml`, plus
`CLAUDE.md` for the house style. The description and title follow the same
rules as everything else here: no hype, ASCII punctuation, no bold
mini-headlines, no text that reads as machine-written.

## Title

Offer three candidates, do not pick one. Each should:

- Front-load the payoff, not the setup.
- Stay under 60 characters so it does not truncate on mobile.
- Promise exactly what the video delivers. A title the video does not honour
  costs more in retention than it gains in clicks.
- Avoid manufactured shock. The audience is technical and reacts badly to it.

## Description

First two lines are all most viewers see. Repeat the promise and say who it
is for. Then the detail: what is covered, firmware version, hardware used.
Then links, including the module's article in this repo and the relevant
ArduPilot documentation.

State the firmware version explicitly. Behaviour changes between releases and
the video will be found by people running something else.

## Chapters

Required. No video on this channel has ever shipped with them, and half the
back catalogue runs over twenty minutes, so this is the single cheapest
improvement available. Do not mark a module ready to upload without them.

Take the timings from the locked edit, not from `script_check.py` estimates.
If the edit is not locked yet, say so and leave the block marked as
provisional. YouTube needs the first chapter at 00:00, at least three
chapters, and each one 10 seconds or longer.

## Thumbnail brief

One image, one idea, readable at 120 pixels wide. Three words of text at
most. Say what the image is, not what mood it should have.

## Pinned comment

Use it for the caveat that did not fit, a known correction, or the question
worth arguing about in the comments. A pinned comment that just says "thanks
for watching" is a wasted slot.

## After upload

Set `video_id`, `published` and `status: published` in `module.yaml`, add the
video link to the module `README.md`, then:

```bash
python3 tools/module_index.py --write
```
