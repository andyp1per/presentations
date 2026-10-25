---
name: shorts
description: Plan and write the vertical shorts cut from a module, with captions for YouTube Shorts, X and TikTok. Use when a module needs clips for distribution.
argument-hint: "<module directory> [how many, or which idea]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(python3 tools/new_short.py:*), Bash(python3 tools/check_posts.py:*), Bash(python3 tools/render_slides.py:*)
---

# Write a module's shorts

## Task: $ARGUMENTS

## Read first

1. `channel/distribution.md` - the platform limits, which platform gets which
   kind of clip, and the rules for writing a short.
2. The module's `script.md`. Shorts are cut from footage the module already
   has, so every short must point at a real chapter or clip.
3. `CLAUDE.md` for the house style. It applies to captions too.

## Timing matters

Draft the shorts **while the module script is being written**, not after the
edit. The whole point is that the shots a short needs get captured on the day.
A short planned after the fact is limited to whatever happened to be filmed.

If the module is already recorded, say so and work from what exists rather
than inventing a shot that was never captured.

## Choosing them

Two or three per module. Look for:

- A number that is surprising on its own. These are the best shorts.
- A single parameter with a non-obvious consequence.
- A before-and-after where the difference is visible, not just measurable.
- A mistake worth warning people about.

Do not cut a short that is just the module's introduction. It has no payoff
and it reads as an advert.

## Platform split

From `channel/distribution.md`, and worth restating because it is the thing
most often got wrong:

| Clip | YouTube | X | TikTok |
|------|---------|---|--------|
| Parameter or config tip | yes | yes | no |
| Log or data finding | yes | yes | no |
| Flying, crash, save, visible A/B | yes | yes | yes |
| Talking head | yes | maybe | no |

X is the highest value destination: the ArduPilot developer community is
already there. TikTok only earns a clip when the clip is genuinely visual, and
the whole TikTok experiment is allowed to fail.

## Scaffold and write

```bash
python3 tools/new_short.py <module> --title "..." --seconds 45 --platforms youtube,x
```

Then fill in the hook, body, payoff and end card, and write each caption
**inside the fenced blocks**. `check_posts.py` measures the fences, so notes
outside them do not count against the limit.

Rules that get broken most often:

- The hook is the first two seconds and it is not a greeting.
- Assume the sound is off. Every number and parameter name that matters must
  be on screen as text.
- The payoff comes before the end, not at it.
- X free accounts are 280 characters for the whole post, and 140 seconds of
  video.

## Cards

Vertical title and stat cards live in `<module>/shorts/cards.md`, rendered
with the 1080x1920 theme:

```bash
python3 tools/render_slides.py <module> --shorts --format png
```

Keep content out of the top 12% and bottom 20% of the frame; platform chrome
covers both. The theme's padding already allows for this.

## Check

```bash
python3 tools/check_posts.py <module>
```

Fix every error. Warnings are judgement calls, but a caption still containing
TODO at status `cut` is an error, not a warning.

## Recording what went out

After posting, set each URL under `posted:` in the short's frontmatter and
move `status` to `posted`. That is what stops a clip going out twice or being
forgotten. There is no automated posting from this repo and there should not
be; uploading is an outward-facing action and the credentials do not belong in
git.
