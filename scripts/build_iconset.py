#!/usr/bin/env python3
"""Generate iconset.json (jsDelivr), iconset-raw.json (raw GitHub) and the README icon table."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "icons"
CDN_BASE = "https://cdn.jsdelivr.net/gh/ZahicX/Icons@main/icons"
RAW_BASE = "https://raw.githubusercontent.com/ZahicX/Icons/main/icons"
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def natural_key(name: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


files = sorted(
    (p for p in ICONS.iterdir() if p.is_file() and p.suffix.lower() in EXTS),
    key=lambda p: natural_key(p.name),
)


def build(base: str):
    return {
        "name": "Icons",
        "icons": [{"name": p.stem, "url": f"{base}/{p.name}"} for p in files],
    }


for filename, base in (("iconset.json", CDN_BASE), ("iconset-raw.json", RAW_BASE)):
    (ROOT / filename).write_text(
        json.dumps(build(base), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
print(f"iconsets written: {len(files)} icons")

readme = ROOT / "README.md"
start, end = "<!-- icons:start -->", "<!-- icons:end -->"
if readme.exists() and start in readme.read_text(encoding="utf-8"):
    text = readme.read_text(encoding="utf-8")
    rows = "\n".join(
        f"| ![{p.stem}](icons/{p.name}) | `{p.stem}` | {CDN_BASE}/{p.name} | {RAW_BASE}/{p.name} |"
        for p in files
    )
    block = (
        f"{start}\n"
        "| 预览 | 名称 | jsDelivr | raw |\n| --- | --- | --- | --- |\n"
        f"{rows}\n{end}"
    )
    text = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, text, flags=re.S)
    readme.write_text(text, encoding="utf-8")
    print("README.md: icon table updated")