"""Build the Japanese Rakuten collection pages, Pinterest pin images and the bulk-upload CSV.

    python3 scripts/build_jp.py            # writes jp/<slug>/index.html, jp/index.html, jp/pins/*.jpg, jp/pins.csv
    python3 scripts/build_jp.py --check    # exit 1 if a product link is not a Rakuten affiliate URL

Data: jp/collections.json (prices/ratings are snapshots with their fetch date).
pin_hooks[0] is the overview pin; pin_hooks[k] features products[pin_products[k-1]].
The CSV follows Pinterest's bulk-create format; Publish date is UTC.
Pins link to our own collection page, never straight to the affiliate URL.
"""
from __future__ import annotations

import csv
import html
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JP = ROOT / "jp"
SITE = "https://ai-fukugyo-media.github.io/pinterest-sites/jp"
FONTS = ("/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf", "C:/Windows/Fonts/meiryo.ttc",
         "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc")
ACCENT = (232, 69, 44)
JST = timezone(timedelta(hours=9))

CSS = """:root{--bg:#faf8f3;--card:#fff;--ink:#1e1e22;--muted:#5f5f69;--line:#e6e1d6;--accent:#bf0000}
@media (prefers-color-scheme:dark){:root{--bg:#16161a;--card:#202026;--ink:#ececf0;--muted:#a0a0ab;--line:#33333b;--accent:#ff6b6b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,"Hiragino Sans","Yu Gothic",sans-serif;line-height:1.8}
main{max-width:760px;margin:0 auto;padding:24px 16px 64px}h1{font-size:1.55rem;line-height:1.4;margin:.4em 0}
.pr{font-size:.85rem;color:var(--muted);border:1px solid var(--line);border-radius:8px;padding:8px 12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:16px 0}
.card h2{font-size:1.1rem;margin:0 0 4px;line-height:1.5}.meta{color:var(--muted);font-size:.9rem;margin:0}
.btn{display:inline-block;margin-top:10px;background:var(--accent);color:#fff;text-decoration:none;font-weight:700;padding:10px 18px;border-radius:999px}
.small{font-size:.8rem;color:var(--muted)}a{color:var(--accent)}ul{padding-left:1.2em}"""


def _font(size):
    from PIL import ImageFont
    for path in FONTS:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise SystemExit("Japanese font not found")


def yen(p: dict) -> str:
    return f"{p['price']:,}円{p.get('price_suffix', '')}"


def page(c: dict) -> str:
    cards = []
    for i, p in enumerate(c["products"], 1):
        cards.append(f"""<section class="card"><h2>{i}. {html.escape(p['label'])}</h2>
<p class="meta">{yen(p)}・{html.escape(p['shipping'])}｜評価 {p['rating']}（{p['reviews']:,}件）｜{html.escape(p['shop'])}</p>
<p>{html.escape(p['note'])}</p>
<p class="small">価格・評価は {p['fetched']} 取得時点。最新の価格・送料・在庫は商品ページで確認してください。</p>
<a class="btn" href="{html.escape(p['url'])}" rel="sponsored nofollow noopener" target="_blank">楽天市場で見る（PR）</a></section>""")
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(c['title'])}</title><meta name="description" content="{html.escape(c['lead'])}">
<style>{CSS}</style></head><body><main>
<p class="pr">※このページはプロモーション（楽天アフィリエイト）を含みます。リンク先で購入されると、運営者に紹介料が入ることがあります。</p>
<h1>{html.escape(c['title'])}</h1><p>{html.escape(c['lead'])}</p>
{''.join(cards)}
<p class="small">選び方: 楽天市場のランキングから自動で集めた候補のうち、レビュー評価と件数が多いものを選んでいます。
価格・送料・ポイント・クーポンは変わることがあります。<a href="../">ほかのまとめを見る</a></p>
</main></body></html>
"""


def index(collections: list[dict]) -> str:
    items = "".join(f'<section class="card"><h2><a href="{c["slug"]}/">{html.escape(c["title"])}</a></h2>'
                    f'<p class="meta">{html.escape(c["lead"])}</p></section>' for c in collections)
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>楽天でお得に暮らす</title><meta name="description" content="楽天市場の人気商品から、まとめ買いしやすい日用品・食品を集めたまとめです。">
<style>{CSS}</style></head><body><main>
<p class="pr">※このサイトはプロモーション（楽天アフィリエイト）を含みます。</p>
<h1>楽天でお得に暮らす</h1><p>重い・かさばる日用品を、レビューの多い人気商品から選んでまとめています。</p>
{items}</main></body></html>
"""


def pin(c: dict, k: int):
    from PIL import Image, ImageDraw
    w, h = 1000, 1500
    img = Image.new("RGB", (w, h), ACCENT)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, w - 40, h - 40], radius=36, fill=(250, 248, 243))
    d.text((w - 170, 90), "※PR", font=_font(40), fill=ACCENT)
    y = 210
    for line in c["pin_hooks"][k].split("\n"):
        d.text((100, y), line, font=_font(92), fill=(30, 30, 34), stroke_width=2, stroke_fill=(30, 30, 34))
        y += 128
    d.rectangle([100, y + 20, 260, y + 32], fill=ACCENT)
    y += 90
    picks = c["products"] if k == 0 else [c["products"][c["pin_products"][k - 1]]]
    for p in picks:
        d.text((100, y), "✓ " + p["short"], font=_font(48), fill=(30, 30, 34))
        y += 64
        if k:
            for line in (f"{yen(p)}（{p['shipping']}・{p['fetched'][5:].replace('-', '/')}時点）",
                         f"評価 {p['rating']}・{p['reviews']:,}件"):
                d.text((140, y), line, font=_font(42), fill=(95, 95, 105))
                y += 62
    d.text((100, h - 230), "価格・送料は商品ページで確認", font=_font(36), fill=(95, 95, 105))
    d.text((100, h - 170), "楽天でお得に暮らす", font=_font(40), fill=(95, 95, 105))
    return img


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    data = json.loads((JP / "collections.json").read_text(encoding="utf-8"))
    bad = [p["label"] for c in data["collections"] for p in c["products"]
           if not p["url"].startswith("https://hb.afl.rakuten.co.jp/")]
    if "--check" in args:
        for label in bad:
            print(f"NOT AFFILIATE: {label}")
        return 1 if bad else 0
    (JP / "pins").mkdir(exist_ok=True)
    (JP / "index.html").write_text(index(data["collections"]), encoding="utf-8")
    rows = []
    # Pins already in pins.csv keep their publish date (they may already be scheduled
    # on Pinterest); new pins continue one a day after the last scheduled one.
    existing = {}
    if (JP / "pins.csv").exists():
        with (JP / "pins.csv").open(encoding="utf-8") as handle:
            existing = {r["Media URL"]: r["Publish date"] for r in csv.DictReader(handle)}
    start = datetime.now(JST).replace(hour=20, minute=0, second=0, microsecond=0) + timedelta(days=1)
    if existing:
        last = max(datetime.strptime(v, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc) for v in existing.values())
        start = max(start, last.astimezone(JST) + timedelta(days=1))
    n = 0
    for c in data["collections"]:
        (JP / c["slug"]).mkdir(exist_ok=True)
        (JP / c["slug"] / "index.html").write_text(page(c), encoding="utf-8")
        for k in range(len(c["pin_hooks"])):
            name = f"{c['slug']}-{k + 1:02d}.jpg"
            pin(c, k).save(JP / "pins" / name, "JPEG", quality=90, optimize=True)
            hook = c["pin_hooks"][k].replace("\n", "")
            media = f"{SITE}/pins/{name}"
            if media in existing:
                published = existing[media]
            else:
                published = (start + timedelta(days=n)).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
                n += 1  # one new pin a day, 20:00 JST
            rows.append({
                "Title": f"{hook}｜{c['title'].split('｜')[-1]}"[:100],
                "Media URL": media,
                "Pinterest board": data["board"],
                "Thumbnail": "",
                "Description": (f"※PR {c['lead']} 価格・送料は商品ページで確認してください。")[:500],
                "Link": f"{SITE}/{c['slug']}/",
                "Publish date": published,
                "Keywords": c["keywords"],
            })
    with (JP / "pins.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(data['collections'])} pages, {len(rows)} pins -> jp/")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
