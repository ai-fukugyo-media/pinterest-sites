"""Add one Pinterest pin per Rakuten product introduced on SNS to jp/product_pins.json.

    python3 scripts/add_product_pins.py ../miumo/content/sns/2026-10-26_rakuten_*.json
    python3 scripts/build_jp.py            # then rebuild jp/pins.csv

RK specs carry a "pinterest" block; RA review specs use their first caption line. The pin image is the
spec's card already published under miumo/sns/<date>/, and the pin links to our link hub (jp/links/),
never straight to the affiliate URL. A product already in the file is skipped.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINS = ROOT / "jp" / "product_pins.json"
MEDIA = "https://ai-fukugyo-media.github.io/pinterest-sites/miumo/sns"
HUB = "https://ai-fukugyo-media.github.io/pinterest-sites/jp/links/"


def pin_for(spec_path: Path) -> dict | None:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    day = re.match(r"(\d{4}-\d{2}-\d{2})_", spec_path.name).group(1)
    kind = spec["id"][:2]
    if kind == "RK" and spec.get("pinterest"):
        image = f"{spec['id']}_tiktok_01.jpg"
        title, description = spec["pinterest"]["title"], spec["pinterest"]["description"]
    elif kind == "RA":
        image = f"{spec['id']}_ig_01.jpg"
        title = spec["tiktok_caption"].splitlines()[0].replace("※PR", "").strip()
        description = "※PR " + " ".join(spec["instagram_caption"].split("\n\n")[1:3]).replace("\n", " ")
    else:
        return None
    if not (ROOT / "miumo" / "sns" / day / image).exists():
        raise SystemExit(f"{image} is not under miumo/sns/{day}/ yet (copy the SNS media first)")
    tags = spec.get("search_keywords") or [t.lstrip("#") for t in re.findall(r"#\S+", description) if t != "#PR"]
    return {"id": spec["id"], "title": title, "media": f"{MEDIA}/{day}/{image}",
            "description": description, "link": HUB, "keywords": ",".join(tags[:6])}


def main(argv: list[str]) -> int:
    data = json.loads(PINS.read_text(encoding="utf-8")) if PINS.exists() else {"pins": []}
    known = {p["id"] for p in data["pins"]}
    added = []
    for arg in argv:
        pin = pin_for(Path(arg))
        if pin and pin["id"] not in known:
            data["pins"].append(pin)
            known.add(pin["id"])
            added.append(pin["id"])
    PINS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"added {len(added)}: {', '.join(added) or '-'} -> {PINS.relative_to(ROOT)} ({len(data['pins'])} pins)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
