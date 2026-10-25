# Claude Code setup

The `CLAUDE.md`, skills and permissions the talks in this repository were
written with, copied on 2026-10-25 from the private repository they live
in. They are here to read, not to run: they sit outside `.claude/`, so
Claude Code does not load them when you open this repository.

They describe that repository, not this one. It makes YouTube modules on
ArduPilot as well as talks, so these files mention a series layout,
channel documents, templates, and tools for edit packs, shorts,
scaffolding and PR explainers, none of which are published here. The
tools a deck needs are in [../tools](../tools), and
[../TOOLING.md](../TOOLING.md) explains them.

| File | What it is |
|------|-----------|
| [CLAUDE.md](CLAUDE.md) | Project instructions: the audience, the format, the accuracy rules, tooling and permissions, house style |
| [settings.json](settings.json) | The permission allow-list: specific scripts rather than the tools under them |
| [skills/](skills/) | The slash commands, one `SKILL.md` each. `/slides` and `/script` are the two that apply to a talk |

To try them in a repository of your own, `CLAUDE.md` goes at its root and
each skill directory under `.claude/skills/`.
