#!/usr/bin/env python3
"""Screenshot the preview pages at 1440 and 375 into site/preview/shots/.

Usage: uv run --with playwright python shots.py [page ...]
Pages default to the three preview pages. Also captures the live pages
for side-by-side comparison (prefixed live-).
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SITE = Path('/home/mrh/real-estate-consulting/site')
SHOTS = SITE / 'preview' / 'shots'
SHOTS.mkdir(parents=True, exist_ok=True)

PAGES = {
    'index': 'preview/index-preview.html',
    'how-it-works': 'preview/how-it-works-preview.html',
    'estimate': 'preview/estimate-preview.html',
}
LIVE = {
    'live-index': 'index.html',
    'live-how-it-works': 'how-it-works.html',
    'live-estimate': 'estimate.html',
}

widths = [(1440, 1000), (375, 812)]
scroll_second = True  # also take a mid-page shot at 1440

def shoot(pg, name, relpath):
    url = (SITE / relpath).as_uri() + '?w=800&appts=12-30'
    pg.goto(url, wait_until='networkidle')
    pg.wait_for_timeout(600)
    for w, h in widths:
        pg.set_viewport_size({'width': w, 'height': h})
        pg.wait_for_timeout(350)
        # overflow check at this width
        overflow = pg.evaluate(
            'document.documentElement.scrollWidth - document.documentElement.clientWidth')
        pg.screenshot(path=str(SHOTS / f'{name}-{w}.png'), full_page=False)
        if scroll_second and w == 1440:
            pg.evaluate('window.scrollTo(0, document.body.scrollHeight*0.45)')
            pg.wait_for_timeout(400)
            pg.screenshot(path=str(SHOTS / f'{name}-{w}-mid.png'), full_page=False)
            pg.evaluate('window.scrollTo(0, 0)')
            pg.wait_for_timeout(200)
        print(f'{name} @{w}: overflow={overflow}px')

def main():
    names = sys.argv[1:] or list(PAGES)
    targets = {}
    for n in names:
        if n in PAGES:
            targets[n] = PAGES[n]
        elif n in LIVE:
            targets[n] = LIVE[n]
        else:
            print(f'unknown page: {n}')
            sys.exit(1)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1440, 'height': 1000})
        for name, rel in targets.items():
            shoot(pg, name, rel)
        b.close()
    print('done')

if __name__ == '__main__':
    main()
