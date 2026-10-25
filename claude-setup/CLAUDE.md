# CLAUDE.md

Guidance for Claude Code when working in this repository.

This repo produces YouTube modules teaching ArduPilot. Each module ships three
artifacts: a video, a Marp slide deck, and a written article. The written
article is not a transcript; it is the reference version, and it is the thing
that is still useful in three years when the video is dated.

## Available Skills

| Skill | Use for |
|-------|---------|
| `/series-plan <topic>` | Planning or revising a series: the arc, the module list, what each one answers |
| `/module-new <title>` | Scaffolding a new module directory from the templates |
| `/script <module>` | Drafting or revising `script.md`, and checking its timings |
| `/slides <module>` | Drafting or revising `slides.md`, and rendering the deck |
| `/flight-card <module>` | Building the flight plan for a module that includes real flying |
| `/shorts <module>` | Writing the vertical clips and their YouTube, X and TikTok captions |
| `/edit-pack <module>` | Overlay cards and the timed edit sheet, ready to import into CapCut |
| `/publish <module>` | Producing the title, description, chapters, tags and thumbnail brief |
| `/pr-explainer <PR or branch>` | A narrated video and an interactive page for one ArduPilot PR, or a branch's related PRs, from measured evidence |

## The Audience Contract

Every module is pitched at a **capable pilot who has never opened the source**.

Assume they can build a quad, solder, set parameters in Mission Planner or
QGroundControl, and flash firmware. Do not assume git, C++, a terminal, DMA,
threads, the EKF, waf, or SITL. When a module needs one of those, teach the
part it needs and no more.

This cuts both ways. Do not talk down, do not pad with basics they already
have, and never explain what a quadcopter is. The viewer is competent and
short on time; they are missing specific knowledge, not intelligence.

Two failure modes, both fatal:

- Explaining a mechanism the viewer cannot act on. If they cannot do anything
  differently after hearing it, cut it or move it to the article.
- Giving a recipe with no mechanism. The channel's value is that the person
  explaining it wrote the code. A viewer should leave knowing *why*, not just
  which parameter to set.

## What the Channel Already Does

Measured from the channel's 15 most recent videos (July 2026). These are
facts about the existing back catalogue, not preferences, and they are here so
new modules are consistent with what works and deliberately different from
what does not.

| Observation | Number |
|-------------|--------|
| Median duration | 13:08 |
| Duration spread | 1:44 to 67:57, bimodal: short demos or long deep dives |
| Videos with chapters | 0 of 15 |
| Description length | 1 to 3 lines, usually just hashtags |
| Best performer | AI Playbooks Part #1, 656 views |
| Worst performer | Acro Fencing Part 1, 111 views |

Established conventions worth keeping:

- Series titles are `<Series> Part #<N> - <Subtitle>`, as in "ArduPilot AI
  Playbooks Part #5 - Feature Development with Claude Code!". Match this.
- Three or four lowercase hashtags at the end of the description, always
  including `#ardupilot`.
- Descriptive titles, hardware named in full, no clickbait. An exclamation
  mark occasionally, nothing louder.
- The long technical series is the format that works here. AI Playbooks ran
  13 to 51 minutes across five parts and is the channel's strongest run.

Two habits to break, both evidenced above:

- **No video has chapters.** For anything over ten minutes this is the
  cheapest available improvement, and half the back catalogue is over twenty.
  `tools/script_check.py` produces the timings; `/publish` will not sign off a
  module without them.
- **Descriptions are close to empty.** This channel is found through search by
  people with a specific problem, and a three-hashtag description gives them
  nothing to match against. Every module gets a real description with the
  parameter names, the firmware version, and links.

And one trap to avoid: "Acro Fencing Part 1" and "Cinelifter Build Video 1"
were both published without a part 2 ever following. Acro Fencing Part 1 is
the least-watched video on the channel. Numbering a video as part one is a
promise, and an unkept one costs more than it gains. See the publishing rule
in the series planning skill.

## Format

Modules aim at 10 to 15 minutes, chaptered, one idea each. If a module needs
twenty minutes it is two modules; say so rather than letting it sprawl. If it
has said everything it has to say in seven, it is a seven minute module.

That range is a deliberate change from the current back catalogue, which is
either under nine minutes or over twenty with nothing in between. It is a
target for concept modules, not a rule to enforce in either direction. A
hands-on walkthrough or a flight comparison can run to twenty-five minutes if
the content is dense the whole way, which is exactly what the AI Playbooks
series did successfully, and a parameter walkthrough can be done properly in
eight. What is not acceptable is a twelve minute module padded to twenty-five,
a dense forty minute module chopped arbitrarily at fifteen, or an eight minute
module stretched to reach twelve.

Padding upward is the easier mistake to make, because the target reads like a
floor. It is not. When a script comes in under, set the target to the honest
estimate rather than adding words: `script_check.py --retime` gives the number,
put it in `target_runtime` and in `module.yaml`, and say that is what you did.
The fast rates series runs from six and a half minutes to twelve and a half for
this reason.

The shape that works:

| Section | Rough share | Job |
|---------|-------------|-----|
| Cold open | 0:00-0:30 | Show the problem. No intro, no greeting, no channel branding |
| Framing | 0:30-1:15 | The question this answers, and what they will be able to do |
| The idea | 1:15-4:30 | Mechanism, on slides, one analogy that holds up |
| In practice | 4:30-8:30 | The actual doing: screen capture, bench, or flight |
| Result | 8:30-11:00 | Evidence that it worked, or honestly that it did not |
| Recap and next | 11:00-end | Three sentences, then name the next module |

Entertainment comes from real stakes: a real aircraft, a real failure, a real
number that surprises. It does not come from jokes written into the script,
jump cuts, or sound effects. When something goes wrong on camera, that is the
best footage available; keep it.

## Repository Layout

```
youtube-presentations/
|-- CLAUDE.md                    this file
|-- README.md                    repo overview and the series index
|-- .claude/
|   |-- settings.json            narrow permissions for the tools
|   `-- skills/*/SKILL.md        the slash commands above
|-- series/
|   `-- 01-fast-rates/
|       |-- README.md            the series plan
|       `-- 01-<slug>/           a module
|-- modules/<slug>/              standalone modules, not part of a series
|-- explainers/<slug>/           narrated explainers for a branch or group of PRs (/pr-explainer)
|-- templates/                   what /module-new copies
|-- themes/fossuav.css           the Marp theme
|-- tools/                       the helper scripts
`-- build/                       rendered decks, gitignored
```

A module directory holds:

| File | What it is |
|------|-----------|
| `module.yaml` | Metadata. Drives the index tables. Keep it accurate |
| `README.md` | The article. The written deliverable, not a transcript |
| `script.md` | The spoken script with chapter markers and shot directions |
| `slides.md` | The Marp deck |
| `publish.md` | Title, description, chapters, tags, thumbnail brief |
| `flight-card.md` | Only for modules with real flying |
| `overlays.md` | Transparent overlay cards for the edit, generated then hand-edited |
| `shorts/` | Vertical clips cut from this module, one file each, plus `cards.md` |
| `assets/` | Images and plots referenced by the deck and the article |

Channel-level decisions that apply across every module live in `channel/`:
positioning and playlists in `channel/README.md`, the visual system in
`channel/branding.md`, and the shorts and cross-posting rules in
`channel/distribution.md`. Read those before making a decision that would
apply to more than one module.

Status runs `planned` -> `scripted` -> `slides` -> `recorded` -> `edited` ->
`published`. Update `module.yaml` when a stage completes, then run
`python3 tools/module_index.py --write` so the tables match.

## Tooling and Permissions

`.claude/settings.json` authorizes **specific scripts**, not the underlying
tools. There is no blanket `python3`, `git` or `npx` grant, because a wide-open
permission means every future command runs unprompted, including a destructive
one. Each repeatable operation is a script in `tools/`, and the script path is
what gets allow-listed. Subprocess calls made inside an allow-listed script do
not prompt, which is why `render_slides.py` wraps `npx` rather than `npx` being
granted directly.

| Script | Does |
|--------|------|
| `tools/new_module.py` | Scaffolds a module from `templates/` |
| `tools/script_check.py` | Estimates runtime from word count, checks and rewrites chapter markers |
| `tools/render_slides.py` | Renders `slides.md` through marp-cli to HTML, PDF, PPTX or PNG, and montages a contact sheet |
| `tools/module_index.py` | Validates `module.yaml` files and regenerates the index tables |
| `tools/new_short.py` | Scaffolds a short inside a module |
| `tools/check_posts.py` | Checks shorts against the YouTube, X and TikTok limits |
| `tools/edit_pack.py` | Builds the overlay cards and the timed edit sheet from `script.md` |
| `tools/slide_frames.py` | Screenshots a served slide at real wall-clock times, the check that an animated slide moves |
| `tools/svganim.py` | The animated-diagram library: the Marmott glyph, a flying quad, the ten figure icons; `filmstrip` freezes an animation at set times |
| `tools/clip_webp.py` | Cuts flight footage into a looping WebP for a slide, locked on the quad or in a fixed window |
| `tools/new_explainer.py` | Scaffolds an explainer from `templates/pr-explainer/`: into the PR's directory in the analysis archive, or `explainers/<slug>` for a branch |

When you catch yourself about to run the same ad-hoc command shape twice,
offer to fold it into a `tools/` script rather than asking for a broad
permission. A genuinely one-off command should just prompt once.

## Accuracy

This channel's whole claim is that the person explaining the feature wrote it.
One confidently wrong parameter description undoes that, permanently, in the
comments.

- **Verify every parameter against the source.** Names, ranges, defaults,
  units and `@Values` come from the `AP_GROUPINFO` block, not from memory.
  ArduPilot is checked out at `/home/andy/github/ardupilot` and the wiki at
  `/home/andy/github/ardupilot_wiki`. Quote the actual behaviour the code
  implements.
- **Always find and read the pull request.** For any ArduPilot feature this
  channel covers, the PR is a primary source and is not optional. Andy puts
  material in PR descriptions and review discussion that appears nowhere
  else: the configuration that was rejected before the one that shipped, the
  reason a limit exists, flight test results, and incidents found in review.
  Read the description **and** the comment thread, and check for a superseded
  earlier PR and for follow-up fixes.

  ```bash
  gh pr view <N> --repo ArduPilot/ardupilot --json body,comments
  gh pr list --repo ArduPilot/ardupilot --search "<feature> author:andyp1per" --state all
  ```

  Two things that only surfaced from the PRs on the fast rates series: a
  climb-away incident under vibration compensation that is in no other
  source, and confirmation that a bug reported on the forum had already been
  fixed. Both would have changed what went on camera.
- **Check whether a reported problem was fixed.** A bug in a forum thread or
  a PR review is a snapshot. Before presenting one as a live gotcha, look for
  the fix commit and say which version it landed in. Presenting a fixed bug
  as current is as wrong as missing a live one.
- **Prove a ref exists before concluding anything from its absence.** An
  absent grep result means "not found", which is not the same as "not
  present". `git show missing-branch:file | grep -c foo` prints 0 exactly as
  it would if the branch existed and the string were missing, and that has
  already produced one wrong claim in this repo.

  Release branches upstream are named `ArduPilot-4.7`, not `Copter-4.7`, and
  release tags are `Copter-4.7.0`. The local ArduPilot clone's `origin` is
  Andy's fork, so upstream branches are not fetched there at all: query
  GitHub rather than the local clone.

  ```bash
  gh api "repos/ArduPilot/ardupilot/branches?per_page=100" --paginate --jq '.[].name'
  gh api "repos/ArduPilot/ardupilot/contents/<path>?ref=ArduPilot-4.7" --jq '.content' | base64 -d
  ```

  When a feature's availability matters, check the release **tag** and not
  just the branch. `BRD_IDLE_STATS` is in `Copter-4.7.0` but in none of the
  4.7 betas, which is exactly the distinction a viewer will trip over.
  `ArduCopter/ReleaseNotes.txt` on the release branch is the fastest
  confirmation.
- **Pin the firmware version.** Behaviour changes between releases. Every
  module states which version it was made against, and `module.yaml` records
  the firmware and airframe the evidence came from.
- **A number on screen needs a source.** CPU loads, loop rates, latencies and
  before/after plots come from a log, a bench measurement, or a comment in the
  source that says where it came from. Record the log in `module.yaml` under
  `evidence` so the claim can be re-checked.
- **A mechanism inferred from one log is a hypothesis.** Say so on camera, or
  go and test it, but do not present it as settled.
- **Corrections are loud.** An error found after publication goes in the
  module README's Corrections section and in a pinned comment. Do not quietly
  edit the article and move on.
- **Do not overclaim the benefit.** If a feature helps agile aerobatic
  aircraft and does nothing for a heavy camera ship, say exactly that. Telling
  viewers a feature is not for them buys more trust than any demo.

## Writing the Script

`script.md` has YAML frontmatter (`module`, `target_runtime`, `wpm`) and
chapters as `## [MM:SS] Title`.

Plain paragraphs are spoken. Direction lines start with a bracketed uppercase
tag and are not counted toward runtime:

| Tag | Use |
|-----|-----|
| `[SHOT]` | Camera setup or framing |
| `[SCREEN]` | Screen capture: Mission Planner, terminal, log viewer |
| `[SLIDE n]` | Cut to slide n of the deck |
| `[B-ROLL 8s]` | Cutaway footage. A duration books silent screen time |
| `[FLIGHT]` | Flight footage; the flight card says how it was captured |
| `[GRAPHIC]` | Motion graphic or animation to be made in the edit |
| `[NOTE]` | Note to self, never appears in the edit |

Blockquotes are on-screen text, not narration, and are not counted.

Rules for the words themselves:

- Write for the ear. Short sentences. One clause per breath. Read it aloud;
  if you run out of air, it is too long.
- Say numbers the way you would say them: "two and a half milliseconds", not
  "2.5ms". The slide carries the digits.
- No "as I mentioned", "as we discussed", "in this video we will". Say the
  thing.
- Do not narrate the slide. If the slide says it, say something else about it.
- Kill every "so", "basically", "essentially" and "just" on the second pass.

Then check the timing:

```bash
python3 tools/script_check.py series/01-fast-rates/01-the-400hz-problem
python3 tools/script_check.py <module> --retime    # set markers from estimates
python3 tools/script_check.py <module> --check     # non-zero if it is off target
```

## Making the Slides

Marp, rendered with `themes/fossuav.css`. The deck is a visual aid for
narration, not a document. Nobody should ever be reading a slide while you are
talking over it.

- Five bullets maximum, six words each. If it needs a sentence it belongs in
  the article.
- One idea per slide. Reach for a new slide before a new bullet.
- Use `<!-- _class: stat -->` when the whole point is one number. These are the
  slides people screenshot.
- Use `<!-- _class: section -->` for act breaks so the viewer knows where they
  are.
- Parameter values go in a `<div class="params">` block: viewers pause the
  video on these, so they must be complete and correct.
- Nothing smaller than the theme's base size. Assume a phone screen.
- Keep the bottom-left and bottom-right corners clear for overlays.

```bash
python3 tools/render_slides.py <module>                  # HTML
python3 tools/render_slides.py <module> --format pdf
python3 tools/render_slides.py <module> --format png     # one PNG per slide, for the edit
python3 tools/render_slides.py <module> --contact        # the whole deck on one sheet
python3 tools/render_slides.py <module> --serve          # the player and presenter view
python3 tools/render_slides.py <module> --watch
```

`--serve` is how to read a deck and how to present from one. The rendered HTML
is already a player the arrow keys drive, but presenter view and the slide
overview sync between windows through localStorage, which a browser blocks on a
`file://` URL, so both only work when the deck is served. Presenter view is `p`,
and gives the current slide, the next one, a wall clock, an elapsed timer and a
notes pane.

The notes pane is the script. `--serve` writes a copy of the deck into
`build/present/` with each slide's narration attached as a presenter note,
resolved from the `[SLIDE n]` directions, so the words come up on the second
screen against the slide they belong to. Everything before the first `[SLIDE n]`
lands on the title card, which is the cold open. `[NOTE]` lines are left out;
the other directions stay in as the stage cues. `slides.md` is never touched:
the copy is generated, the deck stays hand written.

With `--all` the home page lists every module, which is the way to move between
decks without restarting anything.

`--contact` is the last look before calling a deck done. It montages every
slide onto one image, scaled down far enough to take in at once, which is where
a slide that overflows or does not match the others becomes obvious. It needs
ImageMagick, and it re-renders the PNGs, so it replaces the `--format png` run
rather than following it.

## Writing the Article

The module `README.md` stands alone. Someone who found it from a search and
will never watch the video should still get the answer.

- Lead with the short version. A reader who stops after three sentences must
  still leave with the correct conclusion.
- Carry the detail the video had to drop: full parameter tables, ranges,
  edge cases, the version it applies to.
- Include what can go wrong and how to back out. This is the section people
  come back for.
- Link the source files. Viewers who want to go deeper should be able to.
- Do not write "in this video". The article is its own thing.

## Modules That Fly

Real flying gets a `flight-card.md`, filled in before leaving. It exists so
the footage and the log come back usable the first time, and so the flight can
actually falsify the claim rather than just illustrate it.

- Fly A and B back to back in the same conditions. A comparison across two
  days is not a comparison.
- Save a full parameter file per configuration and record the filenames in
  `module.yaml`.
- Set `LOG_BITMASK` for the fields the module reads before flying, not after.
- Abort criteria are named specific behaviours, agreed out loud before arming.
- Experimental parameters raise the odds of a departure: fly high, over clear
  ground, with a switch back to a known-good configuration.

Never write a script that depends on footage which does not exist yet as
though it does. Mark it `[FLIGHT]` and leave the claim unwritten until the log
is on the bench.

## The Edit

CapCut stays the editor. The repo produces everything around the cut and
nothing of the cut itself. Full detail in `channel/editing.md`; the parts that
change how you work:

- **The script is the edit plan.** `[SHOT]`, `[SCREEN]`, `[SLIDE n]` and
  `[B-ROLL 8s]` directions become timed rows in the edit sheet, and
  `[SLIDE 12]` resolves to the real slide 12 PNG. Write the directions
  properly and the edit plan is free.
- **Overlay cards render with real alpha** at 1920x1080, so they drop onto an
  overlay track with no keying. Cards sit on a panel, never as bare text: they
  land over footage, and white text on a bright sky is unreadable.
- **There is no intro sting.** The lower third at about 8 seconds is the
  intro. A logo animation at 00:00 spends the seconds where viewers decide
  whether to stay.
- **Hard cut by default.** A transition needs a reason: time passing, or two
  views of the same thing. A transition on every cut reads as padding.
- **Do not generate CapCut project files.** The format is reverse-engineered
  and version-pinned, and a wrong field leaves a project that will not open.
  The reasoning is written up in `channel/editing.md`; do not relitigate it
  without a reason that document does not already cover.
- **Estimated timecodes never reach YouTube.** They are word-rate estimates
  for ordering the edit. Real chapter times come off the locked timeline.

## Shorts and Cross-posting

Every module yields two or three vertical clips, cut from footage the module
already has, and each goes to YouTube Shorts, X and sometimes TikTok. The
rules are in `channel/distribution.md`; the parts that change how you work:

- **Plan the shorts while writing the module script.** A short planned after
  the edit is limited to whatever happened to get filmed. Planning them early
  is how the shot list ends up complete.
- **A short is a complete idea in under a minute**, not a trimmed module. Hook
  in two seconds, one idea, payoff before the end.
- **Assume the sound is off.** Every number and parameter name that matters is
  on screen as text.
- **The platforms are not one audience.** X is where the ArduPilot developer
  community already is and gets the technical clips. TikTok only earns a clip
  when it is visually interesting, and the TikTok experiment is allowed to
  fail without that meaning anything went wrong.
- **Do not build automated posting.** Uploading is outward-facing and the
  credentials do not belong in this repository. The repo produces the clips,
  the captions and the checks.

Platform limits are recorded in `channel/distribution.md` and enforced by
`tools/check_posts.py`. They were checked in July 2026 against secondary
sources, not platform documentation, and they move. Re-verify before relying
on a pass, and update both the doc and the tool together.

## House Style

The same rules as the ArduPilot playbooks, because the same people read both.

- ASCII punctuation only. Write `-`, `--`, `"`, `...`. No em-dashes,
  en-dashes, arrows, smart quotes or ellipsis characters, anywhere: prose,
  slides, descriptions, comments.
- No bold mini-headlines on bullets (`**Thing.** explanation`) in scripts or
  video descriptions. Plain bullets.
- Backticks only where an identifier would otherwise be ambiguous.
- Vary sentence structure. Do not template every item as a matched
  problem/solution pair.
- No hype. "important", "powerful", "game-changing" and "huge improvement" all
  get cut. State the effect and let it speak.
- In-repo `README.md` prose wraps at about 75 columns. Tables do not wrap.

## Commits

- Atomic commits, one module or one tool per commit.
- Subject prefixed with the area, matching the ArduPilot habit:
  - `fast-rates:` for a module in that series
  - `series:` for a series plan
  - `tools:` for the helper scripts
  - `templates:`, `theme:`, `skills:` for those
  - Examples: `fast-rates: draft module 3 script`, `tools: add script_check`
- Do not list Claude as author or co-author.
- Never `git clean` without explicit permission.
- Do not push without being asked.
