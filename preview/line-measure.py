#!/usr/bin/env python3
"""Measure rendered line counts of every p/li in the preview pages (1440 and 375)."""
from playwright.sync_api import sync_playwright

PAGES = ['index', 'how-it-works', 'estimate']

JS = """
(() => {
  const out = [];
  document.querySelectorAll('p, li, .card-sub, .card-head, summary').forEach(el => {
    const text = el.innerText.trim();
    if (!text) return;
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = Array.from(range.getClientRects());
    // count distinct line tops
    const tops = new Set(rects.map(r => Math.round(r.top)));
    const lines = tops.size;
    if (lines > 5) out.push({lines, tag: el.tagName, text: text.slice(0, 90)});
  });
  return out;
})()
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 1000})
    for name in PAGES:
        pg.goto(f'file:///home/mrh/real-estate-consulting/site/preview/{name}-preview.html?w=800&appts=12-30',
                wait_until='networkidle')
        pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        pg.wait_for_timeout(300)
        for w in (1440, 375):
            pg.set_viewport_size({'width': w, 'height': 1000})
            pg.wait_for_timeout(250)
            hits = pg.evaluate(JS)
            print(f'--- {name} @{w}: {len(hits)} elements over 5 rendered lines')
            for h in hits:
                print(f"  [{h['lines']}L {h['tag']}] {h['text']}")
    b.close()
