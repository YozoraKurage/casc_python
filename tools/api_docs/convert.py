#!/usr/bin/env python3
"""
convert.py - Convert dumped Sphinx HTML pages into Markdown.

Part of the api_docs toolchain (dump -> convert -> diff). Reads the raw HTML
produced by dump.py and writes one .md per page, mirroring the layout used by
docs/api-reference/ (module subfolders, sub-namespace kept where needed).

It parses the Sphinx/Docutils structure:
  - <dl class="py class">   -> class page (H1, signature, description, members)
  - <dl class="py method">  -> method (full signature + field-list desc/returns)
  - <dl class="py property"> / "py attribute" -> properties / enum members
  - <div class="highlight"> -> fenced ```python code blocks
  - enum members "<Enum.NAME: N>" -> "## Members" with integer values

No external deps (stdlib only). This is a best-effort structural converter; the
raw HTML is always kept by dump.py so conversion can be re-run/improved anytime.

Usage
-----
    python convert.py                       # raw-html -> docs/api-reference (per-module folders)
    python convert.py --in DIR --out DIR
    python convert.py --only csc.app        # only pages whose name starts with this
    python convert.py --no-index            # skip writing per-folder _index.md
"""

import argparse
import html as htmllib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_IN = os.path.normpath(os.path.join(HERE, "..", "..", "docs", "api-reference", "raw-html"))
DEFAULT_OUT = os.path.normpath(os.path.join(HERE, "..", "..", "docs", "api-reference"))
OFFICIAL = "https://cascadeur.com/python-api/_generate/"

# How a dotted page name maps to a subfolder + filename.
# Module is the 2nd component (csc.<module>.<...>). Some modules keep the
# sub-namespace in the filename to avoid collisions (e.g. tools.attractor.Args).
KEEP_SUBNS = {
    ("tools", "attractor"), ("tools", "selection"), ("tools", "mirror"),
    ("layers", "layer"), ("layers", "index"),
    ("view", "camera_utils"),
    ("domain", "assets"),
}


def target_path(name):
    """csc.app.Application -> ('app', 'Application.md');
       csc.tools.attractor.Args -> ('tools', 'attractor.Args.md');
       csc.Guid -> ('csc', 'Guid.md')."""
    parts = name.split(".")
    assert parts[0] == "csc", name
    if len(parts) == 2:                       # csc.Guid
        return "csc", parts[1] + ".md"
    module = parts[1]                         # csc.<module>.<...>
    rest = parts[2:]
    if len(rest) >= 2 and (module, rest[0]) in KEEP_SUBNS:
        return module, ".".join(rest) + ".md"
    return module, rest[-1] + ".md"


# ---------------------------------------------------------------------------
# Tiny HTML helpers (regex-based; the pages are regular Sphinx output)
# ---------------------------------------------------------------------------

def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return htmllib.unescape(s)


def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def sig_text(dt_html):
    """Extract a clean signature string from a <dt class="sig ..."> block."""
    # drop the headerlink anchor
    dt_html = re.sub(r'<a class="headerlink".*?</a>', "", dt_html, flags=re.S)
    txt = strip_tags(dt_html)
    # collapse whitespace but keep the arrow
    txt = txt.replace("¶", "")
    return norm_ws(txt)


def first_dd(block):
    """Return the description text from the first <dd> directly under a dl,
    excluding nested member <dl> blocks and field-lists."""
    m = re.search(r"<dd[^>]*>(.*?)</dd>", block, re.S)
    if not m:
        return ""
    inner = m.group(1)
    # cut at the first nested py member dl or field-list
    cut = re.search(r'<dl class="py |<dl class="field-list', inner)
    if cut:
        inner = inner[:cut.start()]
    # remove code-example highlight blocks (handled separately)
    inner = re.sub(r'<div class="highlight.*?</div>\s*</div>', "", inner, flags=re.S)
    inner = re.sub(r'<div class="highlight.*?</div>', "", inner, flags=re.S)
    return norm_ws(strip_tags(inner))


def extract_code_blocks(block):
    """Return list of code example strings from highlight divs in the first dd."""
    m = re.search(r"<dd[^>]*>(.*?)</dd>", block, re.S)
    scope = m.group(1) if m else block
    # only the part before nested members
    cut = re.search(r'<dl class="py ', scope)
    if cut:
        scope = scope[:cut.start()]
    out = []
    for hm in re.finditer(r'<pre>(.*?)</pre>', scope, re.S):
        code = htmllib.unescape(re.sub(r"<[^>]+>", "", hm.group(1)))
        code = code.rstrip("\n")
        if code.strip():
            out.append(code)
    return out


def field_list(method_block):
    """Parse a method's field-list: returns (params_desc, returns, rtype).
    Each is a plain string or '' if absent."""
    m = re.search(r'<dl class="field-list[^"]*">(.*?)</dl>', method_block, re.S)
    if not m:
        return "", "", ""
    fl = m.group(1)
    fields = {}
    # pairs of <dt>label</dt><dd>value</dd>
    for dm in re.finditer(r"<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>", fl, re.S):
        label = norm_ws(strip_tags(dm.group(1))).rstrip(":").lower()
        val = norm_ws(strip_tags(dm.group(2)))
        fields[label] = val
    params = fields.get("parameters", "")
    returns = fields.get("returns", "")
    rtype = fields.get("return type", "")
    return params, returns, rtype


def enum_members(class_block):
    """Find enum members rendered as '<Enum.NAME: N>' and return [(name,val)] by value."""
    found = {}
    for em in re.finditer(r"&lt;[A-Za-z0-9_]+\.([A-Za-z0-9_]+):\s*(-?\d+)&gt;", class_block):
        found[em.group(1)] = int(em.group(2))
    for em in re.finditer(r"<[A-Za-z0-9_]+\.([A-Za-z0-9_]+):\s*(-?\d+)>", strip_tags(class_block)):
        found.setdefault(em.group(1), int(em.group(2)))
    return sorted(found.items(), key=lambda kv: kv[1])


SKIP_MEMBERS = {"__module__", "__annotations__", "__members__", "__hash__",
                "__eq__", "__ne__", "__index__", "__int__", "__str__", "__repr__",
                "__getstate__", "__setstate__", "__new__", "__doc__", "__name__",
                "name", "value"}  # pybind enum/object boilerplate


def member_blocks(class_block, kind):
    """Yield (signature_text, full_block_html) for each <dl class="py <kind>"> nested."""
    for m in re.finditer(r'<dl class="py %s">(.*?)</dl>\s*(?=<dl class="py |</dd>|$)' % kind,
                         class_block, re.S):
        block = m.group(1)
        dt = re.search(r'<dt[^>]*class="sig[^"]*"[^>]*>(.*?)</dt>', block, re.S)
        if not dt:
            continue
        sig = sig_text(dt.group(1))
        yield sig, block


def leaf_name(sig):
    """Get the member's short name from a signature like 'static null() -> ...'."""
    s = re.sub(r"^\s*(static|classmethod|property|abstractmethod)\s+", "", sig)
    m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)", s)
    return m.group(1) if m else ""


def convert_one(name, html):
    """Convert a single page's HTML to Markdown text."""
    out = []
    out.append(f"# {name}")
    out.append("")
    out.append(f"> 公式: {OFFICIAL}{name}.html")
    out.append("")

    cm = re.search(r'<dl class="py (class|function|exception)">(.*?)</dl>\s*</section>',
                   html, re.S)
    if not cm:
        # fallback: take the first py class/function dl to its matching area
        cm = re.search(r'<dl class="py (class|function|exception)">(.*)', html, re.S)
    if not cm:
        out.append("> (変換失敗: py class/function ブロックが見つからない)")
        return "\n".join(out) + "\n"

    kind = cm.group(1)
    block = cm.group(2)

    dt = re.search(r'<dt[^>]*class="sig[^"]*"[^>]*>(.*?)</dt>', block, re.S)
    signature = sig_text(dt.group(1)) if dt else name
    desc = first_dd(block)
    codes = extract_code_blocks(block)

    if desc:
        out.append(desc)
        out.append("")
    out.append("```python")
    out.append(signature)
    out.append("```")
    out.append("")
    for code in codes:
        out.append("```python")
        out.append(code)
        out.append("```")
        out.append("")

    if kind == "function":
        params, returns, rtype = field_list(block)
        if params:
            out.append(f"- **Parameters:** {params}")
        if returns:
            out.append(f"- **Returns:** {returns}")
        if rtype:
            out.append(f"- **Return type:** {rtype}")
        if params or returns or rtype:
            out.append("")
        return "\n".join(out).rstrip() + "\n"

    # enum members
    members = enum_members(block)
    if members:
        out.append("## Members")
        out.append("")
        for nm, val in members:
            out.append(f"- `{nm}` = {val}")
        out.append("")

    # properties / attributes
    props = []
    for sig, _blk in member_blocks(block, "property"):
        nm = leaf_name(sig)
        if nm and nm not in SKIP_MEMBERS:
            props.append((nm, sig))
    for sig, _blk in member_blocks(block, "attribute"):
        nm = leaf_name(sig)
        if nm and nm not in SKIP_MEMBERS and not members:
            props.append((nm, sig))
    if props:
        out.append("## Properties")
        out.append("")
        seen = set()
        for nm, sig in props:
            if nm in seen:
                continue
            seen.add(nm)
            out.append(f"- `{sig}`")
        out.append("")

    # methods (group overloads by name)
    methods = []  # list of (name, [sigs], desc, returns, rtype)
    by_name = {}
    order = []
    for sig, blk in member_blocks(block, "method"):
        nm = leaf_name(sig)
        if not nm or nm in SKIP_MEMBERS:
            continue
        # For enums, the only "methods" are pybind boilerplate constructors -> skip.
        if members and nm == "__init__":
            continue
        params, returns, rtype = field_list(blk)
        mdesc = first_dd("<dd>" + blk.split("</dt>", 1)[-1] if "</dt>" in blk else blk)
        if nm not in by_name:
            by_name[nm] = {"sigs": [], "desc": "", "returns": returns, "rtype": rtype}
            order.append(nm)
        if sig not in by_name[nm]["sigs"]:        # dedup identical overload signatures
            by_name[nm]["sigs"].append(sig)
        if mdesc and not by_name[nm]["desc"]:
            by_name[nm]["desc"] = mdesc
        if returns and not by_name[nm]["returns"]:
            by_name[nm]["returns"] = returns
        if rtype and not by_name[nm]["rtype"]:
            by_name[nm]["rtype"] = rtype

    if order:
        out.append("## Methods")
        out.append("")
        for nm in order:
            info = by_name[nm]
            for sig in info["sigs"]:
                out.append(f"- `{sig}`")
            if info["desc"]:
                out.append(f"  - {info['desc']}")
            if info["returns"]:
                out.append(f"  - Returns: {info['returns']}")
            if info["rtype"]:
                out.append(f"  - Return type: {info['rtype']}")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


MODULE_TITLES = {
    "csc": "csc", "math": "csc.math", "physics": "csc.physics", "parts": "csc.parts",
    "fbx": "csc.fbx", "external": "csc.external", "view": "csc.view", "app": "csc.app",
    "tools": "csc.tools", "rig": "csc.rig", "layers": "csc.layers", "model": "csc.model",
    "domain": "csc.domain", "update": "csc.update",
}


def write_indexes(out_dir, created):
    """created: dict module -> list of (filename, dotted_name)."""
    for module, items in sorted(created.items()):
        items.sort(key=lambda x: x[0].lower())
        lines = [f"# {MODULE_TITLES.get(module, module)}", ""]
        for fn, dotted in items:
            label = dotted[len("csc."):] if dotted.startswith("csc.") else dotted
            lines.append(f"- [{label}](./{fn})")
        lines.append("")
        with open(os.path.join(out_dir, module, "_index.md"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Convert dumped Sphinx HTML to Markdown.")
    ap.add_argument("--in", dest="in_dir", default=DEFAULT_IN, help="raw HTML dir")
    ap.add_argument("--out", dest="out_dir", default=DEFAULT_OUT, help="markdown output root")
    ap.add_argument("--only", default="", help="only convert pages whose dotted name startswith this")
    ap.add_argument("--no-index", action="store_true", help="do not (re)write per-folder _index.md")
    args = ap.parse_args(argv)

    # Only per-API pages: csc.<module>.<...>.html (>=2 dotted parts before .html).
    # Excludes index pages like csc.html / genindex.html / py-modindex.html.
    files = [f for f in os.listdir(args.in_dir)
             if f.endswith(".html") and f.startswith("csc.")
             and len(f[:-len(".html")].split(".")) >= 2]
    files.sort()
    created = {}
    n = 0
    for fn in files:
        name = fn[:-len(".html")]
        if args.only and not name.startswith(args.only):
            continue
        html = open(os.path.join(args.in_dir, fn), encoding="utf-8", errors="replace").read()
        module, out_fn = target_path(name)
        md = convert_one(name, html)
        mod_dir = os.path.join(args.out_dir, module)
        os.makedirs(mod_dir, exist_ok=True)
        with open(os.path.join(mod_dir, out_fn), "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
        created.setdefault(module, []).append((out_fn, name))
        n += 1

    if not args.no_index:
        write_indexes(args.out_dir, created)

    print(f"converted {n} pages into {args.out_dir}")
    for module, items in sorted(created.items()):
        print(f"  {module}: {len(items)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
