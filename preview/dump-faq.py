#!/usr/bin/env python3
"""Dump current FAQ bodies from index-preview.html."""
import re
from pathlib import Path

idx = Path('/home/mrh/real-estate-consulting/site/preview/index-preview.html').read_text()
for s, b in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', idx, re.S):
    print('=====', s)
    print(b)
    print()
