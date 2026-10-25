# Tooling

How the decks in this repository are made. They come out of a private
repository that produces my YouTube modules on ArduPilot. The DevCon 2026
talk was built there with Claude Code, as a standalone module.

The short version: the deck is Markdown rendered by Marp, the diagrams are
animated SVG drawn by a Python script, flight footage goes in as looping
WebP, and a few small scripts render, serve and check the result. Claude
Code works from a `CLAUDE.md` and a set of skills, which are in
[claude-setup/](claude-setup/) exactly as they stand today.

## The pieces

| Piece | Does |
|-------|------|
| [Marp](https://marp.app/), `@marp-team/marp-cli` 4.5.0 through npx | Markdown to HTML, PDF and PNG |
| `themes/fossuav.css` | The theme: dark, 1280x720, sized for a phone screen and YouTube compression |
| `tools/render_slides.py` | Wraps marp-cli: HTML, PDF, PNG, a contact sheet, and `--serve` |
| `tools/script_check.py` | Reads `script.md`: runtime from the word count, and the notes for each slide |
| `tools/svganim.py` | The animation library: the Marmott glyph, a flying quad, the ten figure icons |
| `talks/<slug>/assets/diagrams.py` | One deck's diagrams, drawn with that library |
| `tools/slide_frames.py` | Screenshots a served slide in real time, to check that it moves |
| `tools/clip_webp.py` | Cuts flight footage into a looping WebP, locked on the quad |
| `tools/moduleinfo.py` | A helper the others import |

The tools are copied unchanged from the private repository, so their
examples use its paths (`modules/...`, `series/...`). Run them from the
root of this repository: they look for the theme relative to the current
directory.

## Slides and speaker notes

The deck is `slides.md`. The speaker notes are a separate `script.md`,
where plain paragraphs are spoken and bracketed lines are directions.
`[SLIDE n]` says which slide the next words belong to, `[CLICK]` is a
build step, and `[NOTE]` is a reminder to myself.

`render_slides.py --serve` copies the deck into `build/present/` with each
slide's words attached as presenter notes, so `p` in the served deck gives
the script, the next slide and a timer on a second screen. It has to be
served rather than opened as a file: presenter view syncs its windows
through localStorage, which a browser restricts on a `file://` URL. The
copy is generated; `slides.md` stays hand written.

`script_check.py` estimates the runtime at 150 words a minute and adds any
booked silent time. The DevCon script came to 20:16, with the RealFlight
demo booked at its measured 215 seconds.

## Diagrams that move

Every diagram in the DevCon deck is drawn by its `assets/diagrams.py`, on
top of `tools/svganim.py`. An SVG is never edited by hand: change the
script and re-run it.

The animation is SMIL inside the SVG. That runs inside a plain `<img>` on
a slide, with no JavaScript, and freezes on its first frame in a PDF or
PNG. So each animation is built to open on the frame worth seeing, which
is what the PDF shows.

Every quad is the same glyph, the Marmott in side view. `fly()` moves it
along a path with ballistic segments slowed down, shows a roll as the body
flipping over and a yaw as the body going edge-on, and can draw a thrust
arrow whose length is the g. `fly_att()` takes the attitude as data, for
anything with lines in it.

The physics of every animation was checked by eye, because a room of
ArduPilot developers will check it too. Each of these was wrong at least
once before it was caught:

- Thrust points along the body, never along the path.
- A quad cannot hold a line inverted; it rolls upright for the leg.
- A quad at speed on a line leans into it, since thrust is its only
  forward force. It cannot be level and fast.
- The battery goes on top.

A PNG export cannot show whether anything moves, so there are two checks
for that. `svganim.py filmstrip <svg> --at 0,1,2` freezes one animation at
chosen times. `slide_frames.py` drives Chromium over the DevTools protocol
against the served deck, and takes screenshots in real time.

## Footage

Flight clips go in as animated WebP, not `<video>`. Marp draws each slide
inside an SVG `foreignObject`, and Chromium composites a playing video
outside it at its natural size. A WebP scales with the slide, loops, and
gives the PDF a first frame.

`clip_webp.py --lock` follows the quad: each frame it finds the darkest
small blob against the sky near where it last was, takes its centroid,
smooths it, and crops round it, so the quad sits still and the sky moves.
The first version jittered, for two reasons: dropping from 30 to 24 fps
loses every fifth frame, and locking on the darkest pixel hops as the
silhouette changes. The opener is `--start 5 --dur 7 --lock`; the flip on
a switch is `--start 67 --dur 4.5 --fixed 1370,780,800 --speed 0.5 --fps
30 --width 800 --quality 80`. The source footage is not published.

## Rendering the same way twice

`render_slides.py` pins the browser instead of letting marp-cli pick one.
Under WSL, marp found Windows Chrome, which renders with Windows fonts:
the deck came out in Segoe UI rather than Inter, every line was a
different width, and a slide overflowed on one machine and not the other.
It takes a Chromium or Chrome from the PATH, then Playwright's cached
Chromium, and `CHROME_PATH` overrides both. The committed renders use the
fallback font, DejaVu Sans, because Inter is not installed where they were
made.

## Traps

- Every slide break needs a blank line before `---`. Text run straight
  into it merges two slides without any error. This happened three times.
- The served deck drops `style` attributes. Size images with Marp's syntax
  (`![h:270](...)`) or a scoped `<style>` on the slide.
- A slide ending in `</div>` swallows an HTML comment placed straight
  after it as literal HTML, so the comment never becomes a presenter note.
  `render_slides.py` leaves a blank line before the notes for this reason.
- `--serve` serves a copy made when it starts, so restart it after an
  edit.
- Run a render with stdin from `/dev/null` when it is not in a terminal.
  One hung without it.

## Working with Claude Code

[claude-setup/](claude-setup/) holds the `CLAUDE.md`, the skills and the
permission list as they stand on 2026-10-25. What made the difference on
this deck:

- The accuracy rules come first. `CLAUDE.md` asks for every parameter to
  be checked against its `AP_GROUPINFO` block, for the pull request and
  its review thread to be read, for a reported bug to be checked for a fix
  before it is presented as live, and for every number on screen to have a
  source. The DevCon deck recorded a source for each number as it went
  onto a slide; that list became "Where the numbers come from" in the
  talk's README.
- Permissions are narrow. `settings.json` allows specific scripts, not
  `python3`, `git` or `npx` in general. A command that comes up twice
  becomes a script in `tools/`, and the script's path is what gets
  allowed. That is why `render_slides.py` wraps npx rather than npx being
  allowed directly.
- The deck has a working README that every session reads first. It
  carries the decisions that shaped the deck, with the reason for each, so
  they are not argued again. Three examples: the thrust gauge reads zero
  at the top of the loop, not 1 g; the boost-on quad must not be drawn
  flying the circle, because with boost on it cannot; and all of the
  flying is Guided, so the talk never sets "Guided" against "the script".
  That README is not published here; this file and the talk's README
  carry its public parts.
- Review stays a human job. The physical conventions above were all
  caught by eye, and one figure icon was wrong three times.
- The first version had 47 slides. Its first run-through went long and
  got lost between the maths, the problems and the goal. The second
  version was restructured around three ideas, each seen three times, with
  the first kept beside it to compare. The published deck is the second.

The flight code was built with Claude Code as well, in a separate project.
Slide 27 is how that worked. Every flight goes into a dated journal, now
17,600 lines. A finding goes onto a rules track and is promoted into
`CLAUDE.md` only once it is proven: three incidents, or two airframes.
Anything contradicted goes in a bin of dead ideas, 56 of them, each dated
with the measurement that killed it. Every session reads all of it before
it touches the code. Slide 28 is the time it went wrong anyway.

## Requirements

- Python 3 and PyYAML
- Node.js, for npx; marp-cli is fetched on first use
- Chromium: on the PATH, from Playwright's cache, or named in
  `CHROME_PATH`
- ImageMagick, for `--contact` and `--strip`
- websocket-client, for `slide_frames.py`
- ffmpeg with libwebp, numpy and OpenCV, for `clip_webp.py`
