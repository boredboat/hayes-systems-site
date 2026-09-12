#!/usr/bin/env python3
"""Targeted shot: founder band + contact head on index-preview."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 1000})
    pg.goto('file:///home/mrh/real-estate-consulting/site/preview/index-preview.html',
            wait_until='networkidle')
    pg.wait_for_timeout(600)
    pg.locator('.founder-sec').scroll_into_view_if_needed()
    pg.wait_for_timeout(400)
    pg.screenshot(path='/home/mrh/real-estate-consulting/site/preview/shots/index-founder-1440.png')
    # confirm order programmatically
    order = pg.evaluate("""
    Array.from(document.querySelectorAll('section, footer'))
      .map(s => s.id || s.className.split(' ')[0] || s.tagName)
    """)
    print('section order:', order)
    b.close()
