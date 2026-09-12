#!/usr/bin/env python3
"""Pass 2: FAQ tightening to <=5 rendered lines (~70 words), link fixes.
Every edit exact-match asserted. All-or-nothing per file."""
import sys
from pathlib import Path

P = Path('/home/mrh/real-estate-consulting/site/preview')
idx_path = P / 'index-preview.html'
idx = idx_path.read_text()

def apply_edits(html, edits, label):
    for i, (old, new) in enumerate(edits):
        n = html.count(old)
        if n != 1:
            print(f'FAIL [{label} edit {i}]: matched {n} times.')
            print('  old: ' + old[:110].replace('\n', '\\n'))
            sys.exit(1)
        html = html.replace(old, new)
    return html

def swap_faq(html, summary, new_block, label):
    start = f'<details><summary>{summary}</summary>'
    s = html.find(start)
    if s == -1 or html.find(start, s + 1) != -1:
        print(f'FAIL [{label}]: anchor missing or not unique'); sys.exit(1)
    e = html.find('</details>', s)
    if e == -1:
        print(f'FAIL [{label}]: no close'); sys.exit(1)
    return html[:s] + f'<details><summary>{summary}</summary>{new_block}</details>' + html[e + len('</details>'):]

edits = []

# --- FAQ 2: off-script (104w -> 68w), facts kept: consent, AI disclosure, narrow scope, licensee boundary, recordings, Retell demo
idx = swap_faq(idx, 'What stops the AI from going off script?',
    '<p>Evelyn only calls leads who explicitly asked for the call and opens every conversation by saying she is an AI assistant. Her job is narrow: confirm budget and timeline and book the appointment. Property-specific questions belong to you, the licensee, so she says so plainly and books the call with you to answer them. Every call is recorded and transcribed. Evelyn runs on <a href="https://www.retellai.com/#try-demo" target="_blank" rel="noopener">Retell AI</a>; try their live demo.</p>',
    'faq-offscript')

# --- FAQ 6: build-myself (126w -> two paragraphs, 66w + 37w)
idx = swap_faq(idx, 'Why not just build this myself?',
    '<p>You can, and some agents try. The pieces exist; the hard part is making them all work together. Automations break quietly: a CRM changes its export format, a scheduling link expires, and the workflow you set up in January is silently doing nothing by March. Someone has to notice and fix it every time, forever. That is a second job, and it is the job we actually do.</p>'
    '<p>You would also take on the compliance side yourself, as the sender of record: consent records, opt-out suppression, calling-hour rules. Build it yourself and you own the maintenance. Work with us and you never think about it.</p>',
    'faq-build-myself')

# --- FAQ 8: inside sales team (71w -> 60w)
idx = apply_edits(idx, [(
    "Good, keep them on new leads. That is the job they are measured on, and we do not touch it. We work the opposite end: the old list that never gets called because fresh inquiries always win the hour. Appointments we book arrive on your agents' calendars with the same qualification notes your inside team writes (timeline, budget, who they are), so the handoff feels identical to what they already trust.",
    "Good, keep them on new leads; that is the job they are measured on, and we do not touch it. We work the old list that never gets called because fresh inquiries always win the hour. Appointments we book arrive on your agents' calendars with the same qualification notes your inside team writes (timeline, budget), so the handoff feels identical to what they already trust."
)], 'faq-sales')

# --- FAQ 9: what do I need: already 68w after pass 1, kept

# --- FAQ 10: what counts as appointment (82w -> 62w; no-show sentence redundant with next entry)
idx = apply_edits(idx, [(
    "An appointment that lands on your calendar with a prospect from your list, whether our assistant books it during a call or they book directly from the link we send. That's the billing event. When a campaign wraps, one invoice covers the appointments it booked and is charged automatically to the card on file. If anything on it looks wrong, you have 14 days to say so and we make it right. If someone no-shows, your next booked appointment is on us.",
    "An appointment that lands on your calendar with a prospect from your list, whether our assistant books it during a call or they book directly from the link we send. That's the billing event. When a campaign wraps, one invoice covers the appointments it booked and is charged automatically to the card on file. If anything on it looks wrong, you have 14 days to say so and we make it right."
)], 'faq-whatcounts')

idx_path.write_text(idx)
print(f'index-preview.html updated ({len(idx)} bytes)')

# --- sibling page symlinks so relative links resolve from preview/
for page in ['clients.html', 'compliance.html', 'privacy.html', 'cancellation.html',
             'onboard.html', 'how-it-works.html']:
    lnk = P / page
    if not lnk.exists():
        lnk.symlink_to(Path('..') / page)
        print(f'symlinked {page}')
    else:
        print(f'{page} already present')

print('PASS-2 DONE')
