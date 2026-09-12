#!/usr/bin/env python3
"""Authoritative rendered-text scan: load each preview page, walk the DOM,
and report any em/en dashes or &mdash; in the RENDERED text (innerText),
plus the strings around any hit."""
from playwright.sync_api import sync_playwright

PAGES = ['index', 'how-it-works', 'estimate']
EM, EN = '\u2014', '\u2013'

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 1000})
    total = 0
    for name in PAGES:
        pg.goto(f'file:///home/mrh/real-estate-consulting/site/preview/{name}-preview.html?w=800&appts=12-30',
                wait_until='networkidle')
        pg.wait_for_timeout(400)
        # collect text nodes
        hits = pg.evaluate("""
        (() => {
          const out = [];
          const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          let n;
          while ((n = walker.nextNode())) {
            const t = n.textContent;
            if (t.includes('\\u2014') || t.includes('\\u2013') || t.includes('\\u2014'.toLowerCase())) {
              out.push(t.trim().slice(0, 160));
            }
          }
          return out;
        })()
        """)
        # also open all details so hidden FAQ text is scanned
        pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        pg.wait_for_timeout(200)
        hits2 = pg.evaluate("""
        (() => {
          const out = [];
          const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          let n;
          while ((n = walker.nextNode())) {
            const t = n.textContent;
            if (t.includes('\\u2014') || t.includes('\\u2013')) out.push(t.trim().slice(0, 160));
          }
          return out;
        })()
        """)
        all_hits = sorted(set(hits) | set(hits2))
        total += len(all_hits)
        print(f'{name}: rendered dash hits = {len(all_hits)}')
        for h in all_hits:
            print('   HIT:', h)
        # also scan title attribute / placeholder / meta description
        src = pg.content()
        for needle, label in [(EM, 'em-dash'), (EN, 'en-dash'), ('&mdash;', 'mdash-entity')]:
            c = src.count(needle)
            if c:
                print(f'   {label} in serialized HTML: {c}')
                total += c
    b.close()
    print('TOTAL RENDERED DASH OCCURRENCES:', total)
