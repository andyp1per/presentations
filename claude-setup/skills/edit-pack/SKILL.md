---
name: edit-pack
description: Build the overlay cards and timed edit sheet for a module, ready to import into CapCut. Use when a module is scripted and heading into the edit.
argument-hint: "<module directory>"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(python3 tools/edit_pack.py:*), Bash(python3 tools/render_slides.py:*)
---

# Build a module's edit pack

## Task: $ARGUMENTS

Read `channel/editing.md` first, then `channel/branding.md` for the palette
and the naming rules. The module's `script.md` is the input; everything the
sheet knows comes from the directions already written there.

## Generate

```bash
python3 tools/edit_pack.py <module>
python3 tools/render_slides.py <module> --format png --scale 2
python3 tools/render_slides.py <module> --overlays --format png --scale 1
```

The first run scaffolds `<module>/overlays.md`. After that it is yours to
edit and will not be overwritten without `--force`.

## Write the cards

The scaffold gives you a lower third, one chapter card per chapter, a stat
pop, a parameter callout and an end card. Then:

- **Fill in the stat pops.** Every number said aloud that matters should have
  one. These are what people screenshot, so the value must be exact.
- **Fill in the parameter callouts** from the source, not from memory, in the
  same form the code uses: `FSTRATE_ENABLE`, not `FSTRATE Enable`.
- **Cut chapter cards that do not earn their place.** A card on every chapter
  is noise. The cold open never gets one; it fights the hook.
- **Add a `warn` card** wherever the module tells someone not to skip a step.
- **Set the end card** to name the next module, not just the channel.

Card order sets the PNG numbering the edit sheet refers to, so rerun
`tools/edit_pack.py` after adding or removing one.

## Check before handing to the edit

- Every `[SLIDE n]` in the script resolves to a real slide in the sheet.
- Every footage line in the media bin is something that exists or is on the
  flight card. If the script asks for a shot nobody filmed, that is a
  reflight, and better found now than in the timeline.
- Cards are legible over the footage they will land on. Composite one over a
  bright frame and look at it; white text over a bright sky is the failure
  case, and the panel backgrounds in the theme exist for that reason.

## Timecodes

They are word-rate estimates. They give order and duration, not frame
accuracy. Once the cut is locked, take the real chapter times off the CapCut
timeline for `publish.md`, and never paste the estimates into YouTube.
