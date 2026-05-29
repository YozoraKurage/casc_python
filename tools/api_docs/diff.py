#!/usr/bin/env python3
"""
diff.py - Compare two API dumps and report what changed.

Part of the api_docs toolchain (dump -> convert -> diff). This is the piece that
drives the "periodically dump, then have the AI tidy the docs" workflow: it tells
you (and the AI) exactly which API pages/members were added, removed, or changed
since the last snapshot, so doc updates can be targeted instead of re-reading
everything.

It works at two levels:
  1. Page level: which pages were ADDED / REMOVED / CHANGED (sha256 from manifest,
     or hashing files directly if no manifest).
  2. Member level (for changed pages): which class signatures / methods /
     properties / enum members were added or removed, by extracting member names
     from the raw HTML.

Output:
  - prints a human summary
  - appends a dated section to CHANGELOG.md (unless --no-changelog)
  - with --json writes a machine-readable diff for the AI to consume

No external deps (stdlib only).

Usage
-----
    # compare current dump against the newest snapshot under snapshots/
    python diff.py

    # compare two explicit dirs (each containing the .html files)
    python diff.py --old snapshots/2026.../raw-html --new ../../docs/api-reference/raw-html

    python diff.py --json report.json      # also emit JSON
    python diff.py --no-changelog          # don't touch CHANGELOG.md
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_NEW = os.path.normpath(os.path.join(HERE, "..", "..", "docs", "api-reference", "raw-html"))
SNAP_DIR = os.path.join(HERE, "snapshots")
CHANGELOG = os.path.join(HERE, "CHANGELOG.md")


def latest_snapshot():
    if not os.path.isdir(SNAP_DIR):
        return None
    snaps = [d for d in os.listdir(SNAP_DIR) if os.path.isdir(os.path.join(SNAP_DIR, d))]
    if not snaps:
        return None
    snaps.sort()
    return os.path.join(SNAP_DIR, snaps[-1], "raw-html")


def sha_map(dir_path):
    """Return {filename: sha256} for csc.*.html in dir, preferring manifest.json."""
    manifest = os.path.join(dir_path, "manifest.json")
    if os.path.exists(manifest):
        try:
            data = json.load(open(manifest, encoding="utf-8"))
            files = data.get("files", {})
            return {k: v["sha256"] for k, v in files.items() if k.startswith("csc.")}
        except Exception:  # noqa: BLE001
            pass
    out = {}
    for fn in os.listdir(dir_path):
        if fn.startswith("csc.") and fn.endswith(".html"):
            data = open(os.path.join(dir_path, fn), "rb").read()
            out[fn] = hashlib.sha256(data).hexdigest()
    return out


# --- member-level extraction -------------------------------------------------

# pybind/object boilerplate to ignore when diffing members (keep the changelog
# focused on real API changes, not enum/object dunders).
SKIP_MEMBERS = {"__init__", "__module__", "__annotations__", "__members__",
                "__hash__", "__eq__", "__ne__", "__index__", "__int__",
                "__str__", "__repr__", "__getstate__", "__setstate__",
                "__new__", "__doc__", "__name__", "name", "value"}


def members_of(dir_path, filename):
    """Extract a set of member identifiers from a page's HTML for fine diffing.
    Returns dict with keys: methods, properties, enum (name=val)."""
    path = os.path.join(dir_path, filename)
    if not os.path.exists(path):
        return {"methods": set(), "properties": set(), "enum": set()}
    html = open(path, encoding="utf-8", errors="replace").read()

    def names(kind):
        res = set()
        for m in re.finditer(r'<dl class="py %s">(.*?)</dl>' % kind, html, re.S):
            dt = re.search(r'<dt[^>]*id="([^"]+)"', m.group(1))
            if dt:
                leaf = dt.group(1).split(".")[-1]
                if leaf not in SKIP_MEMBERS:
                    res.add(leaf)
        return res

    enum = set()
    for em in re.finditer(r"&lt;[A-Za-z0-9_]+\.([A-Za-z0-9_]+):\s*(-?\d+)&gt;", html):
        enum.add(f"{em.group(1)}={em.group(2)}")
    return {"methods": names("method"), "properties": names("property") | names("attribute"),
            "enum": enum}


def member_diff(old_dir, new_dir, filename):
    o = members_of(old_dir, filename)
    n = members_of(new_dir, filename)
    out = {}
    for key in ("methods", "properties", "enum"):
        added = sorted(n[key] - o[key])
        removed = sorted(o[key] - n[key])
        if added or removed:
            out[key] = {"added": added, "removed": removed}
    return out


# --- main diff ---------------------------------------------------------------

def page_name(filename):
    return filename[:-len(".html")] if filename.endswith(".html") else filename


def run_diff(old_dir, new_dir):
    old = sha_map(old_dir)
    new = sha_map(new_dir)
    old_set, new_set = set(old), set(new)

    added = sorted(new_set - old_set)
    removed = sorted(old_set - new_set)
    changed = sorted(f for f in (new_set & old_set) if old[f] != new[f])

    changed_detail = {}
    for f in changed:
        changed_detail[f] = member_diff(old_dir, new_dir, f)

    return {
        "added": [page_name(f) for f in added],
        "removed": [page_name(f) for f in removed],
        "changed": [page_name(f) for f in changed],
        "changed_members": {page_name(f): d for f, d in changed_detail.items()},
    }


def format_report(report, old_dir, new_dir):
    lines = []
    a, r, c = report["added"], report["removed"], report["changed"]
    lines.append(f"old: {old_dir}")
    lines.append(f"new: {new_dir}")
    lines.append(f"added={len(a)} removed={len(r)} changed={len(c)}")
    lines.append("")
    if a:
        lines.append("ADDED pages:")
        lines += [f"  + {x}" for x in a]
        lines.append("")
    if r:
        lines.append("REMOVED pages:")
        lines += [f"  - {x}" for x in r]
        lines.append("")
    if c:
        lines.append("CHANGED pages:")
        for x in c:
            lines.append(f"  ~ {x}")
            d = report["changed_members"].get(x, {})
            for key in ("methods", "properties", "enum"):
                if key in d:
                    for m in d[key]["added"]:
                        lines.append(f"      + {key[:-1] if key!='enum' else 'enum'}: {m}")
                    for m in d[key]["removed"]:
                        lines.append(f"      - {key[:-1] if key!='enum' else 'enum'}: {m}")
        lines.append("")
    if not (a or r or c):
        lines.append("No changes.")
    return "\n".join(lines)


def append_changelog(report, old_dir, new_dir):
    a, r, c = report["added"], report["removed"], report["changed"]
    ts = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    block = [f"## {ts}", "",
             f"- compared `{os.path.relpath(old_dir, HERE)}` -> `{os.path.relpath(new_dir, HERE)}`",
             f"- added: {len(a)} / removed: {len(r)} / changed: {len(c)}", ""]
    if a:
        block.append("### Added pages")
        block += [f"- `{x}`" for x in a] + [""]
    if r:
        block.append("### Removed pages")
        block += [f"- `{x}`" for x in r] + [""]
    if c:
        block.append("### Changed pages")
        for x in c:
            d = report["changed_members"].get(x, {})
            bits = []
            for key in ("methods", "properties", "enum"):
                if key in d:
                    if d[key]["added"]:
                        bits.append("+" + ",".join(d[key]["added"]))
                    if d[key]["removed"]:
                        bits.append("-" + ",".join(d[key]["removed"]))
            suffix = f" ({'; '.join(bits)})" if bits else ""
            block.append(f"- `{x}`{suffix}")
        block.append("")
    block.append("> TODO(AI): 上記の差分を docs/ に反映する（手書き版 api/ と公式クローン api-reference/ の整合、cookbook/guides の更新）。")
    block.append("")

    existing = ""
    if os.path.exists(CHANGELOG):
        existing = open(CHANGELOG, encoding="utf-8").read()
    else:
        existing = "# Cascadeur Python API ドキュメント 変更履歴\n\nダンプ間の差分を新しい順に記録する（diff.py が追記）。\n\n"
    # insert new block right after the title/intro (before the first "## ")
    idx = existing.find("\n## ")
    if idx == -1:
        new_text = existing.rstrip() + "\n\n" + "\n".join(block)
    else:
        head = existing[:idx + 1]
        tail = existing[idx + 1:]
        new_text = head + "\n".join(block) + "\n" + tail
    with open(CHANGELOG, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_text)
    print(f"CHANGELOG updated: {CHANGELOG}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Diff two Cascadeur API dumps.")
    ap.add_argument("--old", default=None, help="old raw-html dir (default: newest snapshot)")
    ap.add_argument("--new", default=DEFAULT_NEW, help="new raw-html dir (default: current dump)")
    ap.add_argument("--json", default=None, help="also write machine-readable JSON report here")
    ap.add_argument("--no-changelog", action="store_true", help="do not append to CHANGELOG.md")
    args = ap.parse_args(argv)

    old_dir = args.old or latest_snapshot()
    if not old_dir or not os.path.isdir(old_dir):
        print("No old snapshot to compare against.")
        print("Create a baseline first:  python dump.py --snapshot")
        return 2
    if not os.path.isdir(args.new):
        print(f"new dir not found: {args.new}")
        return 2

    report = run_diff(old_dir, args.new)
    print(format_report(report, old_dir, args.new))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"JSON report: {args.json}")

    has_changes = bool(report["added"] or report["removed"] or report["changed"])
    if has_changes and not args.no_changelog:
        append_changelog(report, old_dir, args.new)

    return 0


if __name__ == "__main__":
    sys.exit(main())
