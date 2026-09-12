#!/usr/bin/env python3
"""Final checks: fonts load, sibling links resolve, small-business wording."""
from pathlib import Path
from playwright.sync_api import sync_playwright

P = Path('/home/mrh/real-estate-consulting/site/preview')

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 1000})
    for name in ['index', 'how-it-works', 'estimate']:
        pg.goto(f'file://{P}/{name}-preview.html?w=800&appts=12-30', wait_until='networkidle')
        pg.wait_for_timeout(500)
        fonts = pg.evaluate("""
        Array.from(document.fonts).filter(f => f.status === 'loaded')
          .map(f => f.family + ' ' + f.weight).sort()
        """)
        h1 = pg.evaluate("""
        getComputedStyle(document.querySelector('h1')).fontFamily
        """)
        # collect link hrefs and test resolution
        bad_links = pg.evaluate("""
        Array.from(document.querySelectorAll('a[href]'))
          .map(a => a.getAttribute('href'))
          .filter(h => !h.startsWith('http') && !h.startsWith('#') && !h.startsWith('mailto'))
          .filter(h => {
            try { return !fetch(h, {method:'HEAD'}) } catch(e) { return false }
          })
        """)
        # simpler: check each relative target exists on disk
        import re
        html = (P / f'{name}-preview.html').read_text()
        rels = sorted(set(re.findall(r'href="([^"#][^":]*?)"', html)))
        missing = [r for r in rels
                   if not r.startswith(('http', 'mailto:'))
                   and '?' not in r
                   and not (P / r).exists()
                   and not (P.parent / r).exists()]
        print(f'{name}: loaded fonts = {fonts}')
        print(f'  h1 family: {h1.split(",")[0]}')
        print(f'  relative links: {rels}')
        print(f'  missing targets: {missing}')
    b.close()

# wording: never call the business small
for f in ['index-preview.html', 'how-it-works-preview.html', 'estimate-preview.html']:
    t = (P / f).read_text().lower()
    hits = [w for w in ['small team', 'small business', 'we\'re small', 'small agency', 'boutique'] if w in t]
    print(f'{f}: small-business wording hits = {hits}')
