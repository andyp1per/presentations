# Presentations

Talks on ArduPilot by Andy Piper of [FOSS UAV](https://fossuav.com). Each
talk has its slides, its speaker notes, and a README that stands on its
own, with links and the source of every number on the slides. The decks
play in the browser with their animations running.

## Talks

Newest first.

### Learning to Fly Freestyle

ArduPilot Developer Conference 2026, Ottawa, 24 October 2026.

An automatic aerobatic display on a quad: a Lua script in Guided mode
flies ten freestyle figures linked by lines, then hands the aircraft back.
How the aircraft should move, how to fly that motion, and the five things
that went wrong on the real one. ArduPilot PR
[#34871](https://github.com/ArduPilot/ardupilot/pull/34871) was opened
live during the talk.

[Play the slides](https://andyp1per.github.io/presentations/talks/devconf-2026-freestyle/slides.html)
| [PDF](talks/devconf-2026-freestyle/slides.pdf)
| [Speaker notes](talks/devconf-2026-freestyle/script.md)
| [About the talk](talks/devconf-2026-freestyle/)

## Layout

| Path | What it is |
|------|-----------|
| `talks/<slug>/` | One talk: `slides.md`, the speaker notes in `script.md`, `assets/`, a `README.md`, and the rendered `slides.pdf` and `slides.html` |
| `themes/` | The Marp theme |
| `tools/` | The scripts that render, serve and check a deck |
| `claude-setup/` | The Claude Code instructions and skills the decks were written with |
| [TOOLING.md](TOOLING.md) | Notes on all of the above |

The repository is also served by GitHub Pages, which is what makes the
"Play the slides" links work. `.nojekyll` keeps Pages from running Jekyll,
which would render `slides.md` over the real `slides.html`. The site's
root page forwards here, so this README is the only list of talks.

## Building a deck

From the root of this repository:

```bash
python3 tools/render_slides.py talks/<slug> --serve       # present it; p for the notes
python3 tools/render_slides.py talks/<slug>               # HTML, into build/
python3 tools/render_slides.py talks/<slug> --format pdf  # PDF, into build/
```

This needs Python 3 with PyYAML, Node.js for npx, and a Chromium.
`build/` is ignored by git.

## Adding a talk

1. Make `talks/<slug>/` and copy in `slides.md`, `script.md`, and only
   the assets `slides.md` uses, along with any script that draws them.
2. Render the HTML and the PDF, and copy them from `build/talks/<slug>/`
   to `talks/<slug>/slides.html` and `slides.pdf`.
3. Write `talks/<slug>/README.md` for a reader who was not in the room.
4. Add the talk under Talks above, newest first, with its Pages link:
   `https://andyp1per.github.io/presentations/talks/<slug>/slides.html`.
