#!/usr/bin/env python3
"""Compare FAQ entries between wireframe and preview; list long paragraphs."""
import re
from pathlib import Path

P = Path('/home/mrh/real-estate-consulting/site/preview')
wf = (P / 'index-wireframe.html').read_text()
pv = (P / 'index-preview.html').read_text()

def entries(t):
    return re.findall(r'<details><summary><span[^>]*>.*?</span>(.*?)</summary>', t) or \
           re.findall(r'<details><summary>(.*?)</summary>', t)

def bodies(t):
    return {s: b for s, b in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', t, re.S)}

wd, pd = bodies(wf), bodies(pv)
print('wireframe entries:', len(wd), '| preview entries:', len(pd))
for s, b in pd.items():
    if s in wd and wd[s].strip() != b.strip():
        print('\n=== DIFFERS:', s[:70])
        print('--- wireframe:'); print(wd[s][:500])
        print('--- preview:'); print(b[:500])
    elif s not in wd:
        print('\n=== NOT IN WIREFRAME (preview-only):', s[:70])

# long paragraph audit (word count as proxy; >38 words ~ >4 lines at 76ch)
print('\n=== paragraphs over 38 words (index-preview) ===')
plain = lambda t: re.sub(r'<[^>]+>', '', t)
for m in re.finditer(r'<p(?: [^>]*)?>(.*?)</p>', pv, re.S):
    w = len(plain(m.group(1)).split())
    if w > 38:
        print(f'[{w}w]', plain(m.group(1))[:110])
print('\n=== paragraphs over 38 words (how-it-works-preview) ===')
hiw = (P / 'how-it-works-preview.html').read_text()
for m in re.finditer(r'<p(?: [^>]*)?>(.*?)</p>', hiw, re.S):
    w = len(plain(m.group(1)).split())
    if w > 38:
        print(f'[{w}w]', plain(m.group(1))[:110])
print('\n=== li over 38 words (both) ===')
for name, t in [('index', pv), ('hiw', hiw)]:
    for m in re.finditer(r'<li>(.*?)</li>', t, re.S):
        w = len(plain(m.group(1)).split())
        if w > 38:
            print(f'[{name} {w}w]', plain(m.group(1))[:110])
