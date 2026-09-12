#!/usr/bin/env python3
"""Pass 6: sentence-boundary paragraph splits (no rewording) to clear the
last >5-line items at 1440."""
import sys
from pathlib import Path

P = Path('/home/mrh/real-estate-consulting/site/preview')

def apply_edits(html, edits, label):
    for i, (old, new) in enumerate(edits):
        n = html.count(old)
        if n != 1:
            print(f'FAIL [{label} edit {i}]: matched {n} times.')
            print('  old: ' + old[:110].replace('\n', '\\n'))
            sys.exit(1)
        html = html.replace(old, new)
    return html

idx_path = P / 'index-preview.html'
idx = idx_path.read_text()

idx = apply_edits(idx, [
    # step 3: two sentences -> two paragraphs (verbatim)
    ('<h3>Appointments hit your calendar</h3><p>On the call, the assistant confirms the lead is genuinely looking, with a sense of timeline and budget, then books during the call. Your booking link connects with one click.</p>',
     '<h3>Appointments hit your calendar</h3><p>On the call, the assistant confirms the lead is genuinely looking, with a sense of timeline and budget, then books during the call.</p><p>Your booking link connects with one click.</p>'),
    # step 4: two sentences -> two paragraphs (verbatim)
    ('<h3>Pay for results</h3><p>Billed per booked appointment, one invoice at campaign close. No-shows are replaced free, and a campaign that books nothing costs nothing.</p>',
     '<h3>Pay for results</h3><p>Billed per booked appointment, one invoice at campaign close.</p><p>No-shows are replaced free, and a campaign that books nothing costs nothing.</p>'),
    # FAQ compliant: split after the YES sentence (verbatim sentences)
    ('<p>Nothing we do is cold. A call only happens after that person replies YES in writing. About twenty states',
     '<p>Nothing we do is cold. A call only happens after that person replies YES in writing.</p><p>About twenty states'),
    # FAQ off-script p1: split before "Her job is narrow" (verbatim sentences)
    ('AI assistant. Her job is narrow: confirm budget and timeline and book the appointment. Property-specific questions',
     'AI assistant.</p><p>Her job is narrow: confirm budget and timeline and book the appointment. Property-specific questions'),
], 'index')

idx_path.write_text(idx)
print(f'index-preview.html updated ({len(idx)} bytes)')
print('PASS-6 DONE')
