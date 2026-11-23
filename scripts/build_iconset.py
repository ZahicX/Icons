#!/usr/bin/env python3
"""Generate iconset.json and the icon table in README.md from icons/."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "icons"
BASE_URL = "https://cdn.jsdelivr.net/gh/ZahicX/Icons@main/icons"
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def natural_key(name: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


entries = []
for p in sorted(ICONS.iterdir(), key=lambda p: natural_key(p.name)):
    if not p.is_file() or p.suffix.lower() not in EXTS:
        continue
    entries.append({"name": p.stem, "url": f"{BASE_URL}/{p.name}"})

data = {"name": "Icons", "icons": entries}
(ROOT / "iconset.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"iconset.json: {len(entries)} icons")

readme = ROOT / "README.md"
start, end = "<!-- icons:start -->", "<!-- icons:end -->"
if readme.exists() and start in readme.read_text(encoding="utf-8"):
    text = readme.read_text(encoding="utf-8")
    rows = "\n".join(
        f"| ![{e['name']}]({e['url'].split('/gh/ZahicX/Icons@main/')[-1]}) "
        f"| `{e['name']}` | {e['url']} |"
        for e in entries
    )
    block = (
        f"{start}\n"
        "| 预览 | 名称 | 直链 |\n| --- | --- | --- |\n"
        f"{rows}\n{end}"
    )
    text = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: block, text, flags=re.S)
    readme.write_text(text, encoding="utf-8")
    print("README.md: icon table updated")