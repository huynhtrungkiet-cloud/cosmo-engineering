#!/usr/bin/env python3
"""Fill the Cosmo Engineering (CE) title block on the CE DXF template and optionally add geometry.

Usage
-----
  # 1) Discover the attribute tags in the template (run once after exporting CE-TEMPLATE.dxf)
  python fill_titleblock.py --list --template CE-TEMPLATE.dxf

  # 2) Produce a drawing from the template with the title block filled
  python fill_titleblock.py --template CE-TEMPLATE.dxf --out drawings/8.010-FFM-00_001_R00.dxf \
      --set "Title=DRIVE SHAFT" --set "Part Number=8.010-FFM-00_001" --set "Project=FFM" \
      --set "Material where not indicated=SCM440 (JIS G4105)" --set "Scale=1:2" --set "Status=WorkInProgress" \
      [--map titleblock-map.json] [--geometry geometry.py]

Fields are matched to attributes by (a) exact tag, (b) a mapping file {field: tag}, (c) the attribute's
prompt text (case-insensitive) – so the human-readable names from ce-standards.md §2.1 usually work as-is.
`--geometry` is an optional Python file defining `draw(msp, doc)` that adds the part geometry (ezdxf API).
Requires: pip install ezdxf
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import ezdxf
except ImportError:  # pragma: no cover
    sys.exit("ezdxf is required: pip install ezdxf")


def iter_attrib_blocks(doc):
    """Yield (space_name, insert) for every block reference with attributes, in model and paper spaces."""
    for layout in doc.layouts:
        for insert in layout.query("INSERT"):
            if insert.attribs:
                yield layout.name, insert


def list_tags(doc) -> list[dict]:
    rows = []
    for space, insert in iter_attrib_blocks(doc):
        for att in insert.attribs:
            prompt = ""
            block = doc.blocks.get(insert.dxf.name)
            if block is not None:
                for attdef in block.query("ATTDEF"):
                    if attdef.dxf.tag == att.dxf.tag:
                        prompt = attdef.dxf.prompt
                        break
            rows.append({"layout": space, "block": insert.dxf.name, "tag": att.dxf.tag, "prompt": prompt, "value": att.dxf.text})
    return rows


def resolve_tag(field: str, rows: list[dict], mapping: dict[str, str]) -> str | None:
    if field in mapping:
        return mapping[field]
    f = field.strip().lower()
    for r in rows:
        if r["tag"].lower() == f:
            return r["tag"]
    for r in rows:
        if r["prompt"].strip().lower() == f:
            return r["tag"]
    for r in rows:  # loose: prompt starts with field (e.g. "Designed by" -> "Designed by 01")
        if r["prompt"].strip().lower().startswith(f):
            return r["tag"]
    return None


def fill(doc, values: dict[str, str], mapping: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    rows = list_tags(doc)
    done, missing = {}, []
    for field, value in values.items():
        tag = resolve_tag(field, rows, mapping)
        if tag is None:
            missing.append(field)
            continue
        for _, insert in iter_attrib_blocks(doc):
            if insert.has_attrib(tag):
                insert.get_attrib(tag).dxf.text = value
                done[field] = tag
    return done, missing


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--template", required=True, type=Path)
    ap.add_argument("--list", action="store_true", help="print attribute tags/prompts and exit")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--set", action="append", default=[], metavar="FIELD=VALUE")
    ap.add_argument("--map", type=Path, help="JSON {field: tag} overrides")
    ap.add_argument("--geometry", type=Path, help="python file with draw(msp, doc)")
    a = ap.parse_args(argv)

    doc = ezdxf.readfile(str(a.template))
    if a.list:
        for r in list_tags(doc):
            print(f"{r['layout']:>12} | {r['block']:<22} | tag={r['tag']:<28} prompt={r['prompt']!r:<34} value={r['value']!r}")
        return 0
    if not a.out:
        ap.error("--out is required unless --list")

    values = {}
    for item in a.set:
        if "=" not in item:
            ap.error(f"--set expects FIELD=VALUE, got {item!r}")
        k, v = item.split("=", 1)
        values[k.strip()] = v
    mapping = json.loads(a.map.read_text(encoding="utf-8")) if a.map else {}

    done, missing = fill(doc, values, mapping)
    if a.geometry:
        ns: dict = {}
        exec(compile(a.geometry.read_text(encoding="utf-8"), str(a.geometry), "exec"), ns)  # user-supplied script
        ns["draw"](doc.modelspace(), doc)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(str(a.out))
    for k, t in done.items():
        print(f"filled {k!r} -> tag {t}")
    for k in missing:
        print(f"WARNING: no attribute found for field {k!r} (use --list and --map)", file=sys.stderr)
    print(f"saved {a.out}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
