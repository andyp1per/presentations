# Presentations

Talks on ArduPilot by Andy Piper of [FOSS UAV](https://fossuav.com): the
slides, the speaker notes, and the tools that built them.

| Talk | Event | Slides |
|------|-------|--------|
| [Learning to Fly Freestyle](talks/devconf-2026-freestyle/) | ArduPilot Developer Conference 2026, Ottawa, 24 October 2026 | [PDF](talks/devconf-2026-freestyle/slides.pdf), [HTML](talks/devconf-2026-freestyle/slides.html), [notes](talks/devconf-2026-freestyle/script.md) |

## Layout

| Path | What it is |
|------|-----------|
| `talks/<slug>/` | One talk: `slides.md`, the speaker notes in `script.md`, `assets/`, and the rendered `slides.pdf` and `slides.html` |
| `themes/` | The Marp theme |
| `tools/` | The scripts that render, serve and check a deck |
| `claude-setup/` | The Claude Code instructions and skills the decks were written with |
| [TOOLING.md](TOOLING.md) | Notes on all of the above |

## Building a deck

From the root of this repository:

```bash
python3 tools/render_slides.py talks/devconf-2026-freestyle --serve       # present it; p for the notes
python3 tools/render_slides.py talks/devconf-2026-freestyle --format pdf
```

This needs Python 3 with PyYAML, Node.js for npx, and a Chromium.
Output goes to `build/`, which git ignores.
