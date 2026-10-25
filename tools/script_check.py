#!/usr/bin/env python3
"""
Estimate a script's runtime and check its chapter markers.

    tools/script_check.py series/01-fast-rates/01-the-400hz-problem
    tools/script_check.py <module> --check
    tools/script_check.py <module> --retime

Reads script.md. Chapters are '## [MM:SS] Title' headings. Plain paragraph and
list text is spoken and counted against the words-per-minute rate in the
frontmatter. Direction lines such as '[SHOT] ...' are not spoken; a direction
may declare silent screen time as '[B-ROLL 8s] ...' and that time is added to
the chapter. Blockquotes are on-screen text, not narration, and are not counted.

--retime rewrites the chapter markers in place from the estimates, which is the
normal way to get timings once the words are settled.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moduleinfo import repo_root   # noqa: E402

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

CHAPTER_RE = re.compile(r"^##\s+\[(\d{1,2}):(\d{2})\]\s*(.*)$")
DIRECTION_RE = re.compile(r"^\[([A-Z][A-Z0-9 _/-]*?)(?:\s+([\d.]+)s)?\]")
SLIDE_RE = re.compile(r"^\[SLIDE\s+(\d+)\]")
DEFAULT_WPM = 150
DEFAULT_TOLERANCE = 0.15


def mmss(seconds):
    seconds = max(0, int(round(seconds)))
    return "%02d:%02d" % (seconds // 60, seconds % 60)


def parse_mmss(text):
    m = re.match(r"^\s*(\d{1,3}):(\d{2})\s*$", str(text))
    if not m:
        return None
    return int(m.group(1)) * 60 + int(m.group(2))


def split_frontmatter(text):
    if not text.startswith("---"):
        return {}, text, 0
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text, 0
    block = text[3:end]
    rest = text[end + 4:].lstrip("\n")
    offset = text[:end + 4].count("\n") + 1
    return (yaml.safe_load(block) or {}), rest, offset


def count_words(line):
    line = re.sub(r"`[^`]*`", " ", line)
    line = re.sub(r"[*_~]", "", line)
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", line)
    return len([w for w in line.split() if re.search(r"[A-Za-z0-9]", w)])


def parse_script(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    meta, body, _ = split_frontmatter(text)

    chapters = []
    current = None
    in_fence = False

    for raw in body.splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        m = CHAPTER_RE.match(line)
        if m:
            current = {
                "marker": int(m.group(1)) * 60 + int(m.group(2)),
                "title": m.group(3).strip(),
                "words": 0,
                "silent": 0.0,
                "raw": line,
            }
            chapters.append(current)
            continue

        if current is None or not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith(">"):
            continue
        if stripped.startswith("<!--") or stripped.startswith("|"):
            continue

        d = DIRECTION_RE.match(stripped)
        if d:
            if d.group(2):
                current["silent"] += float(d.group(2))
            continue

        current["words"] += count_words(stripped)

    return meta, chapters, body


def narration_by_slide(path):
    """Group the spoken lines and stage cues by the slide they are said over.

    Keyed by slide number, in script order. Anything before the first
    [SLIDE n] belongs to slide 1: that is the cold open, delivered while the
    title card is up. [NOTE] lines are left out, being notes to self that were
    never meant to be read aloud, and so are [SLIDE n] lines themselves, which
    say nothing the deck is not already showing.
    """
    with open(path, "r", encoding="utf-8") as f:
        meta, body, _ = split_frontmatter(f.read())

    slides = {}
    current = 1
    in_fence = False

    for raw in body.splitlines():
        stripped = raw.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        if stripped.startswith(("#", ">", "<!--", "|")):
            continue

        s = SLIDE_RE.match(stripped)
        if s:
            current = int(s.group(1))
            continue

        d = DIRECTION_RE.match(stripped)
        if d and d.group(1).strip() == "NOTE":
            continue

        slides.setdefault(current, []).append(stripped)

    return slides


def estimate(chapters, wpm):
    for ch in chapters:
        ch["spoken"] = ch["words"] / float(wpm) * 60.0
        ch["est"] = ch["spoken"] + ch["silent"]
    return chapters


def retime(path, chapters):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    clock = 0.0
    for ch in chapters:
        new = "## [%s] %s" % (mmss(clock), ch["title"])
        text = text.replace(ch["raw"], new, 1)
        clock += ch["est"]
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return clock


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("module", help="module directory or path to a script.md")
    ap.add_argument("--wpm", type=int, help="override words per minute")
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero on timing or ordering problems")
    ap.add_argument("--retime", action="store_true",
                    help="rewrite chapter markers from the estimates")
    ap.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE,
                    help="allowed fraction over/under target runtime (default 0.15)")
    args = ap.parse_args()

    path = args.module
    if os.path.isdir(path):
        path = os.path.join(path, "script.md")
    if not os.path.exists(path):
        sys.exit("no script found: %s" % path)

    meta, chapters, _ = parse_script(path)
    if not chapters:
        sys.exit("no '## [MM:SS] Title' chapter headings found in %s" % path)

    wpm = args.wpm or int(meta.get("wpm") or DEFAULT_WPM)
    target = parse_mmss(meta.get("target_runtime") or "")
    estimate(chapters, wpm)

    root = repo_root()
    try:
        shown = os.path.relpath(path, root)
    except ValueError:
        shown = path
    print("%s   %d words per minute" % (shown, wpm))
    print()
    print("  #  MARKER  EST     DELTA   WORDS  SILENT  TITLE")

    problems = []
    clock = 0.0
    prev_marker = -1
    for i, ch in enumerate(chapters, 1):
        delta = ch["marker"] - clock
        flag = " "
        if abs(delta) > 20:
            flag = "!"
            problems.append("chapter %d (%s) marker is %+ds off the estimate"
                            % (i, ch["title"], round(delta)))
        if ch["marker"] <= prev_marker and i > 1:
            flag = "!"
            problems.append("chapter %d (%s) marker does not advance"
                            % (i, ch["title"]))
        prev_marker = ch["marker"]
        print("%s%3d  %s   %s  %+6ds  %5d  %5.0fs  %s"
              % (flag, i, mmss(ch["marker"]), mmss(ch["est"]), round(delta),
                 ch["words"], ch["silent"], ch["title"]))
        clock += ch["est"]

    words = sum(c["words"] for c in chapters)
    silent = sum(c["silent"] for c in chapters)
    print()
    print("  total %s from %d spoken words plus %.0fs of silent screen time"
          % (mmss(clock), words, silent))

    if target:
        drift = (clock - target) / float(target)
        print("  target %s, estimate is %+.0f%%" % (mmss(target), drift * 100))
        if abs(drift) > args.tolerance:
            verb = "long" if drift > 0 else "short"
            need = abs(clock - target) / 60.0 * wpm
            problems.append("script runs %s by %s (about %d words)"
                            % (verb, mmss(abs(clock - target)), round(need)))

    if args.retime:
        total = retime(path, chapters)
        print("\nrewrote %d chapter markers, ending at %s"
              % (len(chapters), mmss(total)))
        return 0

    if problems:
        print()
        for p in problems:
            print("  problem: %s" % p)
        if not args.check:
            print("\n  run with --retime to set the markers from the estimates")
        return 1 if args.check else 0

    print("\n  timings look consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
