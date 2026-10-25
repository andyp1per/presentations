---
name: module-new
description: Scaffold a new module directory from the templates. Use when adding a module to a series or creating a standalone module.
argument-hint: "<title> [--series <name> --number <n>] [--flight]"
allowed-tools: Read, Grep, Glob, Bash(python3 tools/new_module.py:*), Bash(python3 tools/module_index.py:*)
---

# Scaffold a module

## Task: $ARGUMENTS

Read `CLAUDE.md` for the module layout and status pipeline. If the module
belongs to a series, read `series/<name>/README.md` so the summary and
dependencies match the plan.

## Run

```bash
python3 tools/new_module.py --title "<title>" \
    --summary "<one line for the index>" \
    --series <NN-slug> --number <n> \
    --runtime 12:00 [--flight]
```

Omit `--series` and `--number` for a standalone module; it lands in
`modules/<slug>/`.

The script refuses to overwrite an existing module. If the intent is to
renumber or rename, move the directory and fix `module.yaml` by hand rather
than scaffolding over the top.

## Then

1. Fill in `module.yaml`: `depends_on`, and `evidence` if the logs already
   exist.
2. Update `series/<name>/README.md` if the plan changed.
3. Run `python3 tools/module_index.py --write` to refresh the tables.

Do not draft the script or slides in the same pass unless asked. Scaffolding
and writing are separate decisions.
