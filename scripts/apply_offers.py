"""Apply offers.json URLs to every CTA marked with data-offer.

Each CTA links to the offer's affiliate_url when set (with rel="sponsored"),
otherwise to its official_url so the page never ships a dead "#" link.

    python3 scripts/apply_offers.py          # rewrite pages
    python3 scripts/apply_offers.py --check  # exit 1 if a CTA is dead or an offer lacks an affiliate URL
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTA = re.compile(r'<a class="cta" data-offer="([a-z0-9-]+)"[^>]*>')


def render(offer_id: str, offer: dict) -> str:
    affiliate = (offer.get("affiliate_url") or "").strip()
    if affiliate:
        if not affiliate.startswith("https://"):
            raise SystemExit(f"{offer_id}: affiliate_url must be https")
        return (f'<a class="cta" data-offer="{offer_id}" href="{affiliate}" '
                'rel="sponsored nofollow noopener" target="_blank">')
    return f'<a class="cta" data-offer="{offer_id}" href="{offer["official_url"]}" rel="noopener" target="_blank">'


def main(check: bool) -> int:
    offers = {k: v for k, v in json.loads((ROOT / "offers.json").read_text()).items() if not k.startswith("_")}
    problems = []
    for page in sorted(ROOT.glob("**/index.html")):
        text = page.read_text(encoding="utf-8")
        if 'class="cta" href="#"' in text:
            problems.append(f"{page.relative_to(ROOT)}: dead CTA (href=\"#\")")

        def replace(match):
            offer_id = match.group(1)
            if offer_id not in offers:
                raise SystemExit(f"{page}: unknown offer {offer_id}")
            return render(offer_id, offers[offer_id])

        updated = CTA.sub(replace, text)
        if updated != text:
            if check:
                problems.append(f"{page.relative_to(ROOT)}: not in sync with offers.json")
            else:
                page.write_text(updated, encoding="utf-8")
                print(f"updated {page.relative_to(ROOT)}")
    missing = [k for k, v in offers.items() if not (v.get("affiliate_url") or "").strip()]
    for offer_id in missing:
        print(f"WAITING: {offer_id} has no affiliate_url yet (linking to official site, no commission)")
    for problem in problems:
        print(f"ERROR: {problem}")
    return 1 if problems or (check and missing) else 0


if __name__ == "__main__":
    raise SystemExit(main("--check" in sys.argv[1:]))
