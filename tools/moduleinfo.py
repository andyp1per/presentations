#!/usr/bin/env python3
"""
Shared helpers for reading the module tree.

A module is any directory containing a module.yaml. Series modules live under
series/<series>/<module>/, standalone modules under modules/<module>/.
"""

import os
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

# The production pipeline, in order. A module's status is one of these.
STATUSES = [
    "planned",    # in the series plan, nothing written yet
    "scripted",   # script.md drafted
    "slides",     # slides.md drafted, deck renders
    "recorded",   # footage and screen capture in the can
    "edited",     # cut, graded, thumbnail done
    "published",  # live on YouTube, video_id set
]

STATUS_MARK = {
    "planned": "-",
    "scripted": "S",
    "slides": "SD",
    "recorded": "R",
    "edited": "E",
    "published": "P",
}

REQUIRED_KEYS = ["id", "title", "status", "summary"]


def repo_root(start=None):
    """Walk up from start looking for the repository marker."""
    path = os.path.abspath(start or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(path, "series")) and \
           os.path.isdir(os.path.join(path, "templates")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return os.path.abspath(start or os.getcwd())
        path = parent


def load_module(path):
    """Load one module.yaml and annotate it with its location."""
    meta_path = os.path.join(path, "module.yaml")
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = yaml.safe_load(f) or {}
    meta["_dir"] = path
    root = repo_root(path)
    meta["_relpath"] = os.path.relpath(path, root)
    return meta


def discover(root=None, series=None):
    """Return every module, sorted by series then number."""
    root = root or repo_root()
    found = []
    for base in ("series", "modules"):
        base_dir = os.path.join(root, base)
        if not os.path.isdir(base_dir):
            continue
        for dirpath, dirnames, filenames in os.walk(base_dir):
            if "module.yaml" in filenames:
                found.append(load_module(dirpath))
                dirnames[:] = []   # modules do not nest
    if series:
        found = [m for m in found if m.get("series") == series]
    found.sort(key=lambda m: (str(m.get("series") or "zz"),
                              int(m.get("number") or 0),
                              str(m.get("id") or "")))
    return found


def validate(meta):
    """Return a list of problems with a module's metadata."""
    problems = []
    for key in REQUIRED_KEYS:
        if not meta.get(key):
            problems.append("missing %s" % key)
    status = meta.get("status")
    if status and status not in STATUSES:
        problems.append("unknown status %r (expected one of %s)"
                        % (status, ", ".join(STATUSES)))
    if status == "published" and not meta.get("video_id"):
        problems.append("status is published but video_id is empty")
    for path in ("script.md", "slides.md", "README.md"):
        if status not in (None, "planned") and \
           not os.path.exists(os.path.join(meta["_dir"], path)):
            problems.append("status is %s but %s is missing" % (status, path))
    if meta.get("flight") and status not in (None, "planned") and \
       not os.path.exists(os.path.join(meta["_dir"], "flight-card.md")):
        problems.append("flight module has no flight-card.md")
    return problems


def series_list(root=None):
    """Return series directories that have a README.md, in order."""
    root = root or repo_root()
    base = os.path.join(root, "series")
    if not os.path.isdir(base):
        return []
    out = []
    for name in sorted(os.listdir(base)):
        path = os.path.join(base, name)
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "README.md")):
            out.append(name)
    return out
