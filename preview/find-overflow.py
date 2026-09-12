#!/usr/bin/env python3
"""Find which elements overflow the viewport horizontally at 375 (preview index)."""
import sys
from playwright.sync_api import sync_playwright

page = sys.argv[1] if len(sys.argv) > 1 else 'index'
SITE = f'file:///home/mrh/real-estate-consulting/site/preview/{page}-preview.html'

JS = """
(() => {
  const vw = document.documentElement.clientWidth;
  const bad = [];
  document.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > vw + 1 || r.left < -1) {
      bad.push({
        tag: el.tagName.toLowerCase(),
        cls: (el.className && el.className.baseVal !== undefined) ? el.className.baseVal : String(el.className || ''),
        id: el.id || '',
        left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width)
      });
    }
  });
  return {vw, count: bad.length, bad: bad.slice(0, 20)};
})()
"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 375, 'height': 812})
    pg.goto(SITE, wait_until='networkidle')
    pg.wait_for_timeout(500)
    res = pg.evaluate(JS)
    print('viewport:', res['vw'], 'overflowers:', res['count'])
    for x in res['bad']:
        print(x)
    b.close()
