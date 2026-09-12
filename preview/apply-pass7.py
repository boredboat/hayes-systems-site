#!/usr/bin/env python3
"""Pass 7: step-3 card trim (26w -> 23w, 270px column fits 5 lines)."""
import sys
from pathlib import Path

idx_path = Path('/home/mrh/real-estate-consulting/site/preview/index-preview.html')
idx = idx_path.read_text()

old = '<p>On the call, the assistant confirms the lead is genuinely looking, with a sense of timeline and budget, then books during the call.</p>'
new = '<p>On the call, the assistant confirms the lead is genuinely looking, with a sense of timeline and budget, then books.</p>'
assert idx.count(old) == 1, 'anchor not unique'
idx = idx_path.write_text(idx.replace(old, new))
print('PASS-7 DONE')
