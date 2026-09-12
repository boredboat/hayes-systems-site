#!/usr/bin/env python3
"""Print full wireframe FAQ bodies for the entries that differ."""
import re
from pathlib import Path

P = Path('/home/mrh/real-estate-consulting/site/preview')
wf = (P / 'index-wireframe.html').read_text()
wd = {s: b for s, b in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', wf, re.S)}
for s in ['What stops the AI from going off script?', 'Why not just build this myself?']:
    print('=====', s)
    print(wd[s])
    print()
