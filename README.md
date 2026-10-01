# pinterest-sites

Static landing pages linked from Pinterest pins (served via GitHub Pages).

## Affiliate links

CTA buttons are driven by `offers.json`. To start earning on a page:

1. Get the tracking URL from the approved affiliate dashboard.
2. Paste it into that offer's `affiliate_url` in `offers.json`.
3. Run `python3 scripts/apply_offers.py` and commit.

Until an `affiliate_url` is set, the CTA links to the official site (no commission).
`python3 scripts/apply_offers.py --check` exits non-zero while any CTA is dead or any offer is still waiting for its affiliate URL.
