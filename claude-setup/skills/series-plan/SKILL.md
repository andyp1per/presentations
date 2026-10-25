---
name: series-plan
description: Plan or revise a module series - the arc, the module list, and what each module answers. Use when starting a new series or restructuring an existing one.
argument-hint: "<series topic or existing series name>"
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Plan a series

Read `CLAUDE.md` first, in particular the Audience Contract and Format
sections. If revising an existing series, read its `series/<name>/README.md`
and every `module.yaml` in it.

## Task: $ARGUMENTS

## Ground it before planning it

Do not plan from memory. For an ArduPilot feature:

- Find the implementation in `/home/andy/github/ardupilot` and read it.
- Find the parameters and read the `AP_GROUPINFO` documentation blocks.
- **Find and read the pull request. This is not optional.** Andy puts
  material in PR descriptions and review discussion that is in no other
  source: rejected configurations, why a limit exists, flight test results,
  and incidents found during review. Read the comment thread as well as the
  description, and look for a superseded earlier PR and for follow-up fixes.

  ```bash
  gh pr list --repo ArduPilot/ardupilot --search "<feature> author:andyp1per" --state all
  gh pr view <N> --repo ArduPilot/ardupilot --json body,comments
  ```
- Check `/home/andy/github/ardupilot_wiki` for an existing page. If one
  exists, the series should go beyond it, not restate it.
- Check for an ArduPilot Discourse post. The replies are where real users
  report the problems that make the best gotcha material.
- Check `git log --author="Andy Piper"` for the commits that built the
  feature. The development story is often the best material in the series.

Before any gotcha reaches a plan, check whether it has since been fixed and
in which version. A fixed bug presented as current is as damaging as a live
one that got missed.

## What a series plan contains

1. **The promise.** One sentence: what a viewer who watches all of it can do
   that they could not before.
2. **Who it is for, and who it is not for.** Naming the second is what makes
   the first credible.
3. **The arc.** Each module answers one question, and each question is
   created by the previous module's answer. If module 4 could be watched
   first, the arc is wrong.
4. **The module table.** Number, title, the question it answers, whether it
   needs flight, and what it depends on.
5. **Evidence needed.** Which logs, bench measurements and flights the series
   depends on, and which of those do not exist yet. This is the real schedule.
6. **What is deliberately out of scope.**

## Rules

- Six to eight modules. A longer series loses people; a shorter one is
  usually a single module with padding.
- Module 1 must stand alone as a video. It is the one most people see, and
  most of them will never watch module 2.
- Front-load the payoff. Do not spend three modules on theory before anything
  flies.
- Flight modules cost the most and slip the most. Put no more than half the
  series on flight footage, and make sure the series still works if one
  flight has to move.
- Name the honest verdict module. Every series about a feature needs a point
  where you say who should not use it.

## The publishing rule

Two series on this channel were opened and abandoned: "Acro Fencing Part 1"
and "Cinelifter Build Video 1". Acro Fencing Part 1 is the least-watched video
on the channel. Numbering something part one is a promise to the people who
watch it.

So: **do not publish module 1 until modules 1 to 3 are recorded and the
remaining scripts are drafted.** A series with a finished opener and nothing
behind it is the failure mode this repo exists to prevent. If the evidence for
later modules cannot be captured, that is a reason to cut the series down to
the modules that can ship, not to publish an opener and hope.

Every plan must state which modules are gated on evidence that does not exist
yet, in the Evidence needed table. That table is the schedule.

## Deliverable

Write `series/<NN-slug>/README.md` containing the plan, with the module table
between `<!-- BEGIN MODULE INDEX -->` and `<!-- END MODULE INDEX -->` markers
so `tools/module_index.py --write` can maintain it.

Then offer to scaffold the modules with `/module-new`. Do not scaffold them
without being asked; an unwritten plan is cheap to change and eight empty
directories are not.
