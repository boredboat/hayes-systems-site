import re, collections

base = '/home/mrh/real-estate-consulting/site/preview/'
for f in ['index-preview.html', 'how-it-works-preview.html', 'estimate-preview.html']:
    html = open(base + f).read()
    body = re.sub(r'<(style|script)[^>]*>.*?</\1>', '', html, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'\s+', ' ', text)
    toks = re.findall(
        r"\$?\d[\d.,]*%?[kK+]?(?:\s?(?:days?|weeks?|months?|hours?|appointments?|leads?|per\s?\w+|/\s?\w+|mo))?",
        text)
    c = collections.Counter(t.strip() for t in toks)
    print("==", f)
    for k, v in sorted(c.items(), key=lambda x: -x[1]):
        print(f"  {v}x {k!r}")
    print()

    # show each numeric token in sentence context for manual claims review
    print("  -- context --")
    for m in re.finditer(r"[^.?!]*\b\d[\d.,]*\S*[^.?!]*[.?!]?", text):
        s = m.group(0).strip()
        if len(s) > 240:
            s = s[:240] + "..."
        print("   *", s)
    print()
