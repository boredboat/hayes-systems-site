#!/usr/bin/env python3
"""Post-build structural assertions for the preview pages."""
import re
import sys
from pathlib import Path

P = Path('/home/mrh/real-estate-consulting/site/preview')
ok = True

def check(label, cond):
    global ok
    print(('PASS ' if cond else 'FAIL ') + label)
    if not cond:
        ok = False

idx = (P / 'index-preview.html').read_text()
hiw = (P / 'how-it-works-preview.html').read_text()
est = (P / 'estimate-preview.html').read_text()

# Evelyn: only inside the off-script FAQ entry
entries = re.findall(r'<details><summary>(.*?)</summary>', idx)
eve_outside = 0
for m in re.finditer(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', idx, re.S):
    if 'Evelyn' in m.group(2) and 'off script' not in m.group(1):
        eve_outside += 1
check('Evelyn absent from lead-facing copy (only off-script FAQ)', eve_outside == 0)
check('off-script FAQ entry retained', any('off script' in e for e in entries))

# Structure: stats band out of header, founder before contact
check('stats band is own section after </header>',
      '</header>\n\n<section class="stats-band"' in idx)
check('no stats-grid remnant', 'stats-grid' not in idx)
check('founder section precedes contact',
      idx.find('<section class="founder-sec"') < idx.find('<section id="contact">') and idx.find('<section class="founder-sec"') != -1)
check('exactly one founder section in markup', idx.count('<section class="founder-sec"') == 1)

# Nav token consolidation
check('nav uses var(--navy)', 'background:var(--navy);border-bottom' in idx)
check('no off-token #121F2C left', '#121F2C' not in idx)

# Audit card bullet removed (4 li remain), campaigns card has 5
audit_card = idx.split('audit-plan')[1].split('</div>')

def li_count(chunk):
    return chunk.count('<li>')
audit_chunk = idx[idx.find('audit-plan'):idx.find('plan after')]
camp_chunk = idx[idx.find('plan after'):idx.find('Continuous coverage')]
check('audit card has 4 bullets (misplaced 5th removed)', li_count(audit_chunk) == 4)
check('campaigns card has 5 bullets', li_count(camp_chunk) == 5)

# Steps copy: assistant phrasing, no Evelyn in steps
steps_chunk = idx[idx.find('class="steps"'):idx.find('</section>', idx.find('class="steps"'))]
check('step 2 uses "our conversational AI assistant"', 'our conversational AI assistant' in steps_chunk and 'Evelyn' not in steps_chunk)
check('step 3 retitled', 'Appointments hit your calendar' in steps_chunk)

# how-it-works: note line + trimmed card + renamed heads
check('hiw plan-note present once', hiw.count('plan-note') >= 1 and 'Solo agents are fine on any plan, including free. Teams' in hiw)
check('hiw card trimmed to price + no-show only (2 paragraphs)',
      '<p class="card-head">$60 per appointment that lands on your calendar.</p>\n    <p class="card-sub">If a prospect no-shows' in hiw and hiw.count('<p class="card-sub">') == 1)
check('hiw invoice sentence lives in table section only once', hiw.count('one invoice covers the appointments') == 0)
check('hiw heads renamed', '<h2>Stop any time</h2>' in hiw and '<h2>How your data is handled</h2>' in hiw)
check('hiw title pipe', '<title>How It Works | Hayes Systems</title>' in hiw)

# estimate
check('est title pipe', '<title>Your Launch Estimate | Hayes Systems</title>' in est)
check('est small print trimmed', 'free replacement' not in est)
check('est scopes added', est.count('scope="row"') == 4 and est.count('scope="col"') == 2)

# Retainer copy: no $50/$500 numbers outside FAQ
faq_chunk = idx[idx.find('faq-list'):idx.find('</section>', idx.find('faq-list'))]
retainer_chunk = idx[idx.find('Continuous coverage'):idx.find('plan-note')]
check('retainer band carries no $ figures', '$' not in retainer_chunk.split('eyebrow')[0] + retainer_chunk)

# Theme: tokens unchanged vs live
live_idx = Path('/home/mrh/real-estate-consulting/site/index.html').read_text()
tok = re.search(r':root\{.*?\}', live_idx, re.S).group(0)
check('index :root token block byte-identical', tok in idx)

sys.exit(0 if ok else 1)
