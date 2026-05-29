#!/usr/bin/env python3
"""
dump.py - Download the Cascadeur Python API site as raw HTML.

Part of the api_docs toolchain (dump -> convert -> diff) for periodically
mirroring https://cascadeur.com/python-api/ and tracking changes over time.

What it does
------------
1. Reads the page list (pages.txt; one dotted name per line, e.g. csc.app.Application).
   If --refresh-list is given, it first re-derives the list from the live
   genindex/csc/index pages so newly added/removed API pages are picked up.
2. Downloads each _generate/<name>.html plus the index pages (index, csc,
   genindex, py-modindex) into the output directory.
3. Writes a manifest.json (sha256 + size per page) for fast diffing.

Network: uses urllib from the stdlib (no external deps). Run anywhere with
Python 3; it does NOT need Cascadeur (this only touches the website).

Usage
-----
    python dump.py                         # dump latest into ../../docs/api-reference/raw-html
    python dump.py --out PATH              # custom output dir
    python dump.py --refresh-list          # re-scan the site for the full page set first
    python dump.py --snapshot              # also copy the result into snapshots/<UTC-timestamp>/

See README.md in this folder for the full workflow.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

BASE = "https://cascadeur.com/python-api/"
GENERATE = BASE + "_generate/"
INDEX_PAGES = ("index", "csc", "genindex", "py-modindex")
UA = "Mozilla/5.0 (api_docs dump.py)"

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.normpath(os.path.join(HERE, "..", "..", "docs", "api-reference", "raw-html"))
PAGES_TXT = os.path.join(HERE, "pages.txt")


def _fetch(url, retries=3, pause=1.0, want_headers=False):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
                if want_headers:
                    return data, {"etag": r.headers.get("ETag", ""),
                                  "last_modified": r.headers.get("Last-Modified", "")}
                return data
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as ex:
            last = ex
            time.sleep(pause * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}: {last}")


def read_pages(path=PAGES_TXT):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]


def refresh_page_list(out_path=PAGES_TXT):
    """Re-derive the full set of _generate pages from the live index pages."""
    names = set()
    for idx in ("genindex", "csc", "index", "py-modindex"):
        try:
            html = _fetch(BASE + idx + ".html").decode("utf-8", "replace")
        except Exception as ex:  # noqa: BLE001
            print(f"  (warn: could not fetch {idx}.html: {ex})")
            continue
        for m in re.finditer(r"_generate/(csc\.[A-Za-z0-9_.]+)\.html", html):
            names.add(m.group(1))
    names = sorted(names)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(names) + "\n")
    print(f"refreshed page list: {len(names)} pages -> {out_path}")
    return names


def dump(out_dir, pages, with_index=True):
    os.makedirs(out_dir, exist_ok=True)
    manifest = {}
    ok = fail = 0
    failures = []

    def save(name, url):
        nonlocal ok, fail
        try:
            data, hdrs = _fetch(url, want_headers=True)
        except Exception as ex:  # noqa: BLE001
            fail += 1
            failures.append(f"{name}: {ex}")
            print(f"  FAIL {name}: {ex}")
            return
        path = os.path.join(out_dir, name + ".html")
        with open(path, "wb") as f:
            f.write(data)
        manifest[name + ".html"] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
            "etag": hdrs.get("etag", ""),
            "last_modified": hdrs.get("last_modified", ""),
        }
        ok += 1

    if with_index:
        for idx in INDEX_PAGES:
            save(idx, BASE + idx + ".html")
    for name in pages:
        save(name, GENERATE + name + ".html")

    manifest_meta = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "base_url": BASE,
        "page_count": len(pages),
        "files": manifest,
    }
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest_meta, f, indent=2, ensure_ascii=False)

    print(f"dump done: ok={ok} fail={fail} -> {out_dir}")
    if failures:
        print("failures:")
        for x in failures:
            print("  -", x)
    return ok, fail


def make_snapshot(src_dir):
    """Copy the raw-html dir into snapshots/<UTC timestamp>/ for diffing."""
    import shutil
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    snap_root = os.path.join(HERE, "snapshots", ts)
    os.makedirs(snap_root, exist_ok=True)
    dst = os.path.join(snap_root, "raw-html")
    shutil.copytree(src_dir, dst, dirs_exist_ok=True)
    print(f"snapshot saved: {dst}")
    return snap_root


def main(argv=None):
    ap = argparse.ArgumentParser(description="Download the Cascadeur Python API site as raw HTML.")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output dir for raw HTML (default: docs/api-reference/raw-html)")
    ap.add_argument("--refresh-list", action="store_true", help="re-derive pages.txt from the live site first")
    ap.add_argument("--no-index", action="store_true", help="do not download index pages")
    ap.add_argument("--snapshot", action="store_true", help="also copy result into snapshots/<timestamp>/")
    args = ap.parse_args(argv)

    if args.refresh_list:
        pages = refresh_page_list()
    else:
        pages = read_pages()
        if not pages:
            print("pages.txt is empty; running --refresh-list automatically")
            pages = refresh_page_list()

    ok, fail = dump(args.out, pages, with_index=not args.no_index)
    if args.snapshot:
        make_snapshot(args.out)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
