---
name: slides
description: Draft or revise a module's Marp deck and render it. Use when writing slides.md or producing slide images for the edit.
argument-hint: "<module directory> [what to change]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(python3 tools/render_slides.py:*)
---

# Build a module deck

## Task: $ARGUMENTS

## Read first

`CLAUDE.md`, the Making the Slides section. Then the module's `script.md`:
the deck follows the script, not the other way round. Every `[SLIDE n]`
direction in the script must land on a real slide, and every slide should be
called for by the script.

## The theme

`themes/fossuav.css`, applied automatically by the render script. Available
per-slide classes:

| Class | For |
|-------|-----|
| `<!-- _class: title -->` | Opening and closing slides |
| `<!-- _class: section -->` | Act breaks |
| `<!-- _class: stat -->` | One number, full screen. The screenshot slides |

And these wrappers inside a slide:

| Wrapper | For |
|---------|-----|
| `<div class="cols">` | Two even columns, for before/after |
| `<div class="params">` | Parameter blocks. Viewers pause on these; be exact |
| `<div class="warn">` | The thing that bites them if they skip a step |
| `<div class="note">` | Aside worth pausing on |
| `<div class="ok">` | Confirmation or a good outcome |

## Rules

- Five bullets maximum, six words each.
- One idea per slide. Add a slide rather than a bullet.
- Never put a sentence on a slide that the narration also says.
- Parameter values must be complete and correct: people will copy them off a
  paused frame and fly with them.
- Keep the bottom corners clear for lower thirds and pagination.

## Diagrams, animation and clips

A picture on nearly every slide. Each module draws its own in
`assets/diagrams.py` (the scaffold provides one), which imports
`tools/svganim.py` for the palette, the `Svg` builder, `marmott_glyph()`,
`fly()` and the ten display figures. Edit and re-run; never hand-edit an SVG.

- `fly()` animates the Marmott along a path: ballistic segments slowed, rolls
  as the body flipping over, yaws as it going edge-on, `pitch` events for a
  body turn against the path, and an optional thrust arrow whose length is
  the g. It is SMIL, so it runs inside an `<img>` and freezes at frame 0 in a
  PNG or PDF; make frame 0 a sensible still.
- Check poses with `python3 tools/svganim.py filmstrip <svg> --at 0,1,2`, and
  that it moves on the served slide with `tools/slide_frames.py`. A PNG render
  cannot show either.
- Physics is checked by eye on every animation, because the audience will:
  thrust along the body, never the path; no line flown inverted; a quad that
  runs in nose-down shows it. The library's docstring lists the conventions.
- Flight footage goes in as a looping WebP from `tools/clip_webp.py`,
  `--lock` to follow the quad or `--fixed` for a still window. Not a
  `<video>`: Chromium composites it outside the slide. Keep the source frame
  rate, or thin it evenly with `--fps`.
- Size images with Marp's syntax (`![h:270](...)`, `![bg](...)`) or scoped
  `<style>`; the served deck drops `style` attributes.
- Builds are Marp fragments: `*` bullets reveal one per click.
- Every `---` slide break needs a blank line before it. Text run into it
  merges two slides without any error.

## Render

```bash
python3 tools/render_slides.py <module>                 # HTML, quickest check
python3 tools/render_slides.py <module> --format pdf
python3 tools/render_slides.py <module> --format png    # one PNG per slide for the editor
python3 tools/render_slides.py <module> --contact       # every slide on one sheet
python3 tools/render_slides.py <module> --serve         # the player, for reading and presenting
python3 tools/render_slides.py --all --serve            # every module on the home page
python3 tools/render_slides.py <module> --watch
```

Output lands in `build/` and is gitignored. Render before finishing: a deck
that has never been rendered usually has a layout that overflows.

Then read the deck back with `--contact`, which renders the PNGs and montages
them onto a single sheet. Looking at every slide at once is how you catch the
one that overflows, the one that repeats a slide three earlier, and the one
that does not look like it belongs to the same deck.

`--serve` is for reading the deck as a deck, and for recording against it. It
puts the script's narration into the presenter notes for each slide, matched up
through the `[SLIDE n]` directions, so `p` gives you the words next to the
slide. If a slide's notes come up empty, its narration has no `[SLIDE n]`
direction pointing at it, which is worth fixing in the script rather than
working around here.

Update `module.yaml` status to `slides` when the deck renders and matches the
script.
