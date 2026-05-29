#!/usr/bin/env python3
"""
check.py - Fast change detector for the Cascadeur API site.

The Cascadeur app does NOT notify you when the docs change -- the API docs are
just a website. But the site is a single Sphinx build, so we can detect changes
with only ONE or TWO HTTP requests (not one per page):

  1. HEAD index.html         -> the whole site is rebuilt together, so its
                                ETag/Last-Modified changes whenever ANY page does.
  2. GET  objects.inv (16KB) -> the Sphinx inventory listing every symbol; diff it
                                to see exactly which pages were ADDED / REMOVED.

This replaces the old (terrible) approach of HEAD-ing all ~209 pages one by one,
which took minutes. This version finishes in ~1 second.

Exit codes: 0 = no change, 10 = change detected, 2 = no baseline.

Usage
-----
    python check.py                 # ~1s: is the site newer than our last dump?
    python check.py --run-dump      # if changed, run dump --snapshot -> convert -> diff
    python check.py --inventory     # also fetch objects.inv and list added/removed pages
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import zlib

BASE = "https://cascadeur.com/python-api/"
UA = "Mozilla/5.0 (api_docs check.py)"

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "docs", "api-reference", "raw-html"))
DEFAULT_MANIFEST = os.path.join(RAW_DIR, "manifest.json")
INV_CACHE = os.path.join(RAW_DIR, "objects.inv")


def head(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="HEAD")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return {"etag": r.headers.get("ETag", ""),
                "last_modified": r.headers.get("Last-Modified", ""),
                "status": r.status}


def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def load_manifest(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def baseline_index_headers(manifest):
    """ETag/Last-Modified of index.html recorded at the last dump."""
    files = manifest.get("files", {})
    info = files.get("index.html", {})
    return info.get("etag", ""), info.get("last_modified", "")


def parse_objects_inv(data):
    """Parse a Sphinx objects.inv (v2) into a set of fully-qualified names.

    Format: 4 header lines (line 4 says 'zlib'), then zlib-compressed body of
    'name domain:role priority uri dispname' lines.
    """
    nl = data.find(b"\n")
    # skip 4 header lines
    pos = 0
    for _ in range(4):
        pos = data.find(b"\n", pos) + 1
    body = zlib.decompress(data[pos:])
    names = set()
    for line in body.decode("utf-8", "replace").splitlines():
        m = re.match(r"(\S+)\s+(\S+)\s+", line)
        if m and m.group(1).startswith("csc"):
            names.add(m.group(1))
    return names


def inventory_diff():
    """Compare live objects.inv against the cached copy. Returns (added, removed) name sets."""
    try:
        live = get(BASE + "objects.inv")
    except Exception as ex:  # noqa: BLE001
        print(f"  (warn: could not fetch objects.inv: {ex})")
        return None, None
    live_names = parse_objects_inv(live)
    if os.path.exists(INV_CACHE):
        old_names = parse_objects_inv(open(INV_CACHE, "rb").read())
    else:
        old_names = set()
    added = sorted(live_names - old_names)
    removed = sorted(old_names - live_names)
    return added, removed


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fast change detector for the Cascadeur API site (1-2 requests).")
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST, help="manifest.json from the last dump")
    ap.add_argument("--inventory", action="store_true",
                    help="also GET objects.inv and list added/removed symbol pages")
    ap.add_argument("--run-dump", action="store_true",
                    help="if changed, run dump.py --snapshot && convert.py && diff.py")
    args = ap.parse_args(argv)

    manifest = load_manifest(args.manifest)
    if not manifest:
        print(f"No manifest at {args.manifest}. Run a full dump first:  python dump.py --snapshot")
        return 2

    t0 = time.time()
    base_etag, base_lm = baseline_index_headers(manifest)
    try:
        cur = head(BASE + "index.html")
    except Exception as ex:  # noqa: BLE001
        print(f"could not reach the site: {ex}")
        return 2

    if base_etag and cur["etag"]:
        site_changed = base_etag != cur["etag"]
    elif base_lm and cur["last_modified"]:
        site_changed = base_lm != cur["last_modified"]
    else:
        site_changed = True  # no baseline headers -> can't be sure

    dt = (time.time() - t0) * 1000
    print(f"site check in {dt:.0f}ms  (1 request)")
    print(f"  baseline index: etag={base_etag or '-'}  lm={base_lm or '-'}")
    print(f"  live     index: etag={cur['etag'] or '-'}  lm={cur['last_modified'] or '-'}")

    added = removed = None
    if args.inventory or site_changed:
        added, removed = inventory_diff()
        if added is not None:
            print(f"  inventory: +{len(added)} pages, -{len(removed)} pages")
            for x in added[:50]:
                print(f"    + {x}")
            for x in removed[:50]:
                print(f"    - {x}")

    if not site_changed:
        print("No change since last dump (site rebuild timestamp unchanged).")
        return 0

    print("\nSite has been rebuilt since the last dump -> a full dump is recommended.")
    if args.run_dump:
        print("Running full update (dump --refresh-list --snapshot -> convert -> diff)...")
        import subprocess
        py = sys.executable
        subprocess.run([py, os.path.join(HERE, "dump.py"), "--refresh-list", "--snapshot"], check=False)
        subprocess.run([py, os.path.join(HERE, "convert.py")], check=False)
        subprocess.run([py, os.path.join(HERE, "diff.py"),
                        "--json", os.path.join(HERE, "last-diff.json")], check=False)
        # refresh the cached inventory so next check compares against this build
        try:
            open(INV_CACHE, "wb").write(get(BASE + "objects.inv"))
        except Exception:  # noqa: BLE001
            pass
        print("Update complete. See CHANGELOG.md (latest entry).")
        return 0

    print("Run a full update with:  python check.py --run-dump")
    return 10


if __name__ == "__main__":
    sys.exit(main())
