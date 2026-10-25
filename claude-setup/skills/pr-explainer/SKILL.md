---
name: pr-explainer
description: Make a narrated explainer video and an interactive page for one ArduPilot pull request, or for a branch or group of related PRs, drawn from measured evidence. Use when asked for an explainer, an animation or a video of a PR or a branch's changes, as opposed to a full module.
argument-hint: "<PR number | branch and topic> [what to focus on]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(python3 tools/new_explainer.py:*), Bash(gh pr view:*), Bash(gh pr list:*)
---

# PR explainer

## Task: $ARGUMENTS

Two outputs: a narrated video (Manim scenes timed to a local
text-to-speech voice) and an interactive web page on the same evidence.
Two sizes have been made:

| Kind | Length | Lives in | Worked example |
|------|--------|----------|----------------|
| One PR | about 2 min | `../ardupilot-pr-analysis/<N>/video/` | #32768, baro drift at arm |
| A branch or group of PRs | 4 to 6 min | `explainers/<slug>/` here | `explainers/sfd-4.7.2-height/`, `explainers/sfd-4.7.2-flow/` |

Read the example's `scenes.py` and `script.md` before writing new ones.
For a branch, also read "A branch or a group of PRs" below first.

This is not a module. No slides, no article, no `module.yaml`.

## Read first

- This repo's `CLAUDE.md`: Audience Contract, Accuracy, Writing the Script
  and House Style all apply. The animation conventions in
  `tools/svganim.py`'s docstring and `channel/branding.md` (palette, type,
  no logo sting, open on the problem) apply to Manim the same as to SVG.
- The ArduPilot playbook, `/home/andy/github/ardupilot/CLAUDE.md`:
  "Writing for Reviewers" (open with what the user does and what goes
  wrong; second person for the failure; effects a pilot can see, not
  internal identifiers) and "Diagnosing from Logs and Data" (a mechanism
  from one log is a hypothesis; interrogate the measurement). The
  explainer is a PR description told aloud, and the same rules hold.
  Read any subsystem playbook the PR touches (`libraries/*/CLAUDE.md`).
- `../ardupilot-pr-analysis/CLAUDE.md`: the evidence cascade (real flight
  over Replay over SITL over inspection) and the rule that the archive is
  public and never holds real-flight logs.

## 1. Gather the evidence

```bash
gh pr view <N> --repo ArduPilot/ardupilot --json title,body,comments,headRefOid
```

Then the archive's `../ardupilot-pr-analysis/<N>/README.md` and any
`analysis.md`, which hold the numbers, the rejected alternatives and the
plots. Real-flight context is in `../analysis/` (`topics/`, `logs/`,
`notes/`); grep it for the subsystem. Find a named log with
`AP_LOG_ROOTS=/mnt/d/logs:/mnt/d/support python3 ../ardupilot-pr-analysis/find_log.py <name>`
(Andy's own flight campaigns are under `/mnt/d/logs`, customers' logs
under `/mnt/d/support`; pass `--acc-id`/`--bootcnt` when there are several
candidates, and confirm a candidate against the numbers its note quotes:
log numbers collide across vehicles and campaigns).

Prefer one real log for the "it happens" scene and the archive's SITL
BINs for the "this is what the change does" scene. Label a SITL stress
case as one on screen ("9.5 m injected, a stress case").

## 2. Check the claims against the code

Check each PR's state first (`gh pr view <N> --json state,closedAt`) and
again before rendering the final cut: #33497 was closed while the flow
explainer was being made, and its scene had to come out.

Read the code at the PR head and record the commit. Every sentence the
video says about behaviour gets checked there, not taken from the PR
body: a description written for reviewers rounds things off. On #32768
this found two: the reset does not run with home locked although the
body says "every arm", and the vertical-speed refusal is 1 m/s
(`LAND_DETECTOR_VEL_Z_MAX`) where the body's table shows the 1.5 m/s the
test used. Say the exact thing, and tell the user about the loose one so
they can fix the PR body too.

## 3. Scaffold

```bash
python3 tools/new_explainer.py <N> --name pr<N>-<slug>
```

Writes `../ardupilot-pr-analysis/<N>/video/` from
`templates/pr-explainer/`: `script.md`, `scenes.py` (the channel kit:
palette, Inter and JetBrains Mono, `quad()` as the Marmott glyph,
`Narrated` base class), `make_data.sh`, `make_page.py`,
`build_video.py`, `publish.md`, `README.md`, `.gitignore`.

The video needs a venv with manim and kokoro, by default `~/venv-video`:

```bash
python3 -m venv ~/venv-video && ~/venv-video/bin/pip install manim kokoro soundfile
```

Kokoro downloads its model and a spaCy model on first use.

## 4. Data

Every curve on screen comes from a log, through `make_data.sh` and the
log-analyze skill's `log_extract.py`. Never draw an illustrative curve
where a measured one exists. A video with an invented curve makes a claim
the PR never measured.

Real-flight CSVs and the built `explainer.html`, which inlines them, go
in `.gitignore`. `make_data.sh` takes the real log's path as an argument
and does not name the support directory it came from.

A customer's log on a public video shows their flight. Say which support
logs a video uses when handing it over, so the user can decide before
upload.

Re-derive every number on screen from your own extraction, including the
ones a subagent or a note reports. On the SmallFastDrone explainers that
caught: a quad described as holding 15 m that was climbing through it
(checked against GPS), a "clean before and after" where the after log had
also changed a noise parameter, a speed ratio fitted on a near-stationary
hover (too weak to quote), and a gyro slope that moved from 0.54 to 0.53
once the IMU was interpolated at its full logged rate instead of
decimated. Interrogate the measurement before narrating it.

## 5. Script

`script.md`, one `## sN` paragraph per scene, five to seven scenes, about
two minutes. The shape that worked:

| Scene | Job |
|-------|-----|
| s1 | What the pilot does and what goes wrong. No title card |
| s2 | A real log showing it happen, named |
| s3 | What the vehicle does with it today, in pilot-visible effects |
| s4 | What the change does, on the measured before/after |
| s5-s6 | The non-obvious part: a second problem the fix created, the guards |
| s7 | What it does not fix, then the PR number |

Numbers as words; the screen carries the digits. Every number said aloud
appears on screen. Show the script to the user before rendering: it is
the cheapest thing to change.

## 6. Scenes

One class per paragraph, `S1` for `s1`. Use `self.p(...)` and
`self.w(...)` so time is booked against the narration, and end with
`self.finish()`, which pads to the audio length. The audio sets the pace;
retime animations to it, never the other way.

- `Text` only. `MathTex`, `Tex` and `Axes(include_numbers=True)` need
  LaTeX; `chart()` draws axes with hand-made labels, and
  `series()`, `line()`, `key()`, `tag()`, `heading()` and `card()` cover the
  rest of what the two explainers so far needed.
- Move a chart with `VGroup(ax, labels).shift(...)`. Shifting `ax` alone
  leaves the tick labels where they were, which both SmallFastDrone
  explainers shipped a draft with; the contact sheet shows it as labels
  floating off their axis.
- Colour carries meaning across the whole video: `WARN` for how it
  behaves today, `ACC2` for with the change, `ACC` for the measured
  number that matters. Keep each to one meaning.
- Put a live readout (`always_redraw`) in a region the curve never
  reaches, and check where the curve goes before choosing one.
- Physics by eye, as for the decks: a falling quad moves down while its
  speed readout runs; thrust along the body; nothing hovers inverted.
- ASCII on screen as elsewhere: `C` not the degree sign, `to` not an
  arrow.

## 7. Render and look

```bash
python3 build_video.py --draft      # 480p, then read build/contact.png
python3 build_video.py --skip-audio # 1080p60 mp4, loudness normalised
python3 build_video.py --skip-audio S3  # re-render one scene at 1080p
python3 build_video.py --join-only  # then rejoin without rendering the rest
```

Look at the contact sheet every time: three frames per scene, one row
each. On #32768 the first sheet showed four collisions (a readout on the
curve, a label over an axis, text crossing a slope, two labels stacked)
that no amount of reading `scenes.py` would have found. Fix, re-run
`--draft` for the changed scenes (`build_video.py --draft --skip-audio S2 S4`),
then render. The final mp4 is normalised to -14 LUFS; Kokoro's raw output
is about 12 dB quieter than YouTube expects.

## 8. Interactive page

Built with the Artifact tool, and published private. Run its quickstart
and design pass first. Write the page source to `explainer.src.html` with
a `__DATA__` token where the data goes. `python3 make_page.py`
inlines `data/*.csv` as `DATA.<stem>.cols/rows` and writes
`explainer.html`, which is what gets published.

What made #32768's page useful rather than decorative: a slider replaying
the real log, a comparison of today against the change for each state
that matters, and a checker where the viewer sets up a case and the page
says what the code does and why. Every outcome it shows comes from the
code read in step 2.

## A branch or a group of PRs

Ask the user for the scope first: a branch like SmallFastDrone carries
fifty-odd PRs, and a video about all of them says nothing about any. Pick
one through-line a pilot can hold (the height being handed between
sensors; flow needing its rotation and its height) and the 20-30 PRs on
it.

- Sources: the branch's `README.md` feature list, `Tools/SFD/prs.txt`
  (order and "must stay after" notes) and `Tools/SFD/REFRESH_HISTORY.md` /
  `REFRESH_NOTES.md`, which record how the PRs interacted when stacked.
  Fetch the branch rather than checking it out, and read it with
  `git show <sha>:<path>`.
- Research in parallel, one agent per cluster of PRs, each returning per
  PR: the pilot symptom, what changed, its parameters checked in the
  branch source, the best number with its tier, and its interactions with
  the rest of the web; plus up to three real logs, verified by
  extraction. Then one more agent for real logs alone, once the scenes
  are known. Their reports are leads, not evidence: see step 4.
- Interactions are the content. Keep only those a pilot would see (a fix
  that exposed the next bug, a change that needs another first), not code
  conflicts from stacking.
- Shape: a cold open on the worst real log, one scene naming the inputs or
  the relay, then one scene per phase or input, each with a real-log
  chart, and a closing list of the settings to check. About 10 scenes,
  900 to 1000 words.
- Scaffold with `python3 tools/new_explainer.py --dest explainers/<slug>
  --name <slug> --title "<what it covers>"`. Commit here, not in the
  archive, with the `explainers:` prefix.
- The page gets a rail of phases (chart, symptom, fix, parameters, PR
  links, before/after toggle where a log pair exists) and the list of
  interactions, filterable by PR.

## 9. Publish and commit

Fill in `publish.md` (title, description with the PR link, three or four
hashtags including `#ardupilot`, visibility). The user uploads it. Do not
build or run automated posting.

Commit, staging exact paths, never the mp4, `audio/`, `media/`,
`build/`, real-flight CSVs or `explainer.html`. A branch explainer is
committed here as `explainers: <what it covers>`; a PR explainer in the
archive:

```bash
git -C ../ardupilot-pr-analysis add <N>/video/<paths>
git -C ../ardupilot-pr-analysis commit -m "pr<N>: add explainer video and interactive page sources"
```

Use the `pr<N>:` prefix, not `<N>:`. The archive's history has both, but
the ArduPilot playbook's commit hook rejects a bare number when the commit
is made from an ArduPilot session. Add the `video/` line to the PR README's file map
in the same commit. Do not push without being asked.
