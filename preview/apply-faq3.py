#!/usr/bin/env python3
"""Pass 3: the two FAQ block swaps that pass 2 dropped on the floor."""
import sys
from pathlib import Path

P = Path('/home/mrh/real-estate-consulting/site/preview')
idx_path = P / 'index-preview.html'
idx = idx_path.read_text()

def swap_faq(html, summary, new_block, label):
    start = f'<details><summary>{summary}</summary>'
    s = html.find(start)
    if s == -1 or html.find(start, s + 1) != -1:
        print(f'FAIL [{label}]: anchor missing or not unique'); sys.exit(1)
    e = html.find('</details>', s)
    if e == -1:
        print(f'FAIL [{label}]: no close'); sys.exit(1)
    return html[:s] + f'<details><summary>{summary}</summary>{new_block}</details>' + html[e + len('</details>'):]

idx = swap_faq(idx, 'What stops the AI from going off script?',
    '<p>Evelyn only calls leads who explicitly asked for the call and opens every conversation by saying she is an AI assistant. Her job is narrow: confirm budget and timeline and book the appointment. Property-specific questions belong to you, the licensee, so she says so plainly and books the call with you to answer them. Every call is recorded and transcribed. Evelyn runs on <a href="https://www.retellai.com/#try-demo" target="_blank" rel="noopener">Retell AI</a>; try their live demo.</p>',
    'faq-offscript')

idx = swap_faq(idx, 'Why not just build this myself?',
    '<p>You can, and some agents try. The pieces exist; the hard part is making them all work together. Automations break quietly: a CRM changes its export format, a scheduling link expires, and the workflow you set up in January is silently doing nothing by March. Someone has to notice and fix it every time, forever. That is a second job, and it is the job we actually do.</p>'
    '<p>You would also take on the compliance side yourself, as the sender of record: consent records, opt-out suppression, calling-hour rules. Build it yourself and you own the maintenance. Work with us and you never think about it.</p>',
    'faq-build-myself')

idx_path.write_text(idx)
print(f'index-preview.html updated ({len(idx)} bytes)')
print('PASS-3 DONE')
