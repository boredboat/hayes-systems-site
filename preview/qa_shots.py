#!/usr/bin/env python3
"""QA renders for the homepage wireframe: 1440 + 375 into site/preview/shots/,
plus a hard overflow assertion at both widths."""
import pathlib, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8931"
PAGE = f"{BASE}/preview/index-wireframe.html"
OUT = pathlib.Path("/home/mrh/real-estate-consulting/site/preview/shots")
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    failures = []
    for w, h, tag in [(1440, 900, "1440"), (375, 720, "375"), (390, 844, "390")]:
        pg = browser.new_page(viewport={"width": w, "height": h})
        pg.goto(PAGE, wait_until="networkidle")
        pg.wait_for_timeout(400)
        # hard overflow assertions
        metrics = pg.evaluate(
            "() => ({sw: document.scrollingElement.scrollWidth,"
            " iw: window.innerWidth,"
            " offenders: [...document.querySelectorAll('*')]"
            "   .filter(e => e.getBoundingClientRect().right > window.innerWidth + 1)"
            "   .slice(0, 5).map(e => e.tagName + '.' + (e.className.baseVal || e.className || ''))})"
        )
        if metrics["sw"] > metrics["iw"] + 1:
            failures.append(f"[{tag}] page overflow scrollWidth={metrics['sw']} innerWidth={metrics['iw']} offenders={metrics['offenders']}")
        # shots: full page, above the fold, one mid-page scroll
        pg.screenshot(path=str(OUT / f"index-wireframe-{tag}-full.png"), full_page=True)
        pg.screenshot(path=str(OUT / f"index-wireframe-{tag}-fold.png"))
        pg.evaluate(f"() => window.scrollTo(0, document.body.scrollHeight * 0.45)")
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT / f"index-wireframe-{tag}-mid.png"))
        print(f"{tag}: scrollWidth={metrics['sw']} innerWidth={metrics['iw']} shots done")
        pg.close()
    browser.close()
    if failures:
        print("OVERFLOW FAILURES:")
        print("\n".join(failures))
        sys.exit(1)
    print("no horizontal overflow at 375 / 390 / 1440")
