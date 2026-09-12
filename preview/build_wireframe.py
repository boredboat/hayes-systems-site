#!/usr/bin/env python3
"""Build site/preview/index-wireframe.html from site/index.html.
Every replacement asserts its exact match count; any mismatch fails the build."""
import sys

SRC = "/home/mrh/real-estate-consulting/site/index.html"
DST = "/home/mrh/real-estate-consulting/site/preview/index-wireframe.html"
t = open(SRC, encoding="utf-8").read()
report, fails = [], []

def rep(old, new, n=1, tag=""):
    global t
    c = t.count(old)
    if c != n:
        fails.append(f"[{tag}] expected {n} match, found {c}: {old[:70]!r}")
        return
    t = t.replace(old, new)
    report.append(f"OK  {tag}")

# stats band: close header early, open a section (order matters)
rep('  </div>\n</header>', '  </div>\n</section>', 1, "stats-close")
rep('\n  </div>\n  <div class="container stats-grid">',
    '\n  </div>\n</header>\n\n<section class="stats-band" aria-label="The follow-up gap">\n  <div class="container stats-grid">',
    1, "stats-open")

rep('<title>Hayes Systems | Lead Reactivation for Real Estate Teams</title>',
    '<title>Homepage refresh wireframe | Hayes Systems preview</title>\n<meta name="robots" content="noindex">',
    1, "title")
rep('<link rel="canonical" href="https://www.hayessystems.com/">\n', '', 1, "canonical")
rep("url('fonts/", "url('../fonts/", 7, "font-paths")
rep("url('img/hero-newengland.webp')", "url('../img/hero-newengland.webp')", 1, "hero-img")
rep("url('img/hero-newengland-mobile.webp')", "url('../img/hero-newengland-mobile.webp')", 1, "hero-img-m")
rep('background:#121F2C', 'background:var(--navy)', 1, "nav-navy")
rep('<body id="top">\n',
    '<body id="top">\n<div class="preview-flag">Preview wireframe: homepage refresh, for review only, not live</div>\n',
    1, "flag")

rep('<p class="lede">Your CRM is already full of leads you paid for. Hayes Systems pairs proven email and text outreach with the latest in voice automation provided by Retell AI, turning forgotten contacts into qualified appointments on your calendar. Our Massachusetts-based team proudly serves New England and beyond, delivering measurable results with no CRM changes and nothing to learn.</p>',
    '<p class="lede">Your CRM already holds leads you paid for and never fully worked. Hayes Systems re-engages them with personalized email, text, and opt-in AI calls, and books qualified appointments straight onto your calendar.</p>',
    1, "lede")

rep('<div class="stat"><div class="big">5+</div><p>follow-up touches are what it typically takes to convert a lead. Most agents stop at two.</p></div>',
    '<div class="stat"><div class="big">5+</div><p>touches usually needed before a lead converts. Most agents stop at two.</p></div>', 1, "stat1")
rep('<div class="stat"><div class="big">90 days+</div><p>is all it takes for a lead to go cold. The older they get, the more the window where "not ready yet" quietly becomes "ready now." Nobody\'s calling them. We are.</p></div>',
    '<div class="stat"><div class="big">90 days+</div><p>is all it takes for a lead to go cold. Nobody\'s calling them. We are.</p></div>', 1, "stat3")

rep('<div class="pain"><div class="big">$20-60</div><h3>What each lead cost you.</h3><p>Multiply that by the contacts sitting untouched in your CRM and you\'ll see the inventory you\'re ignoring while paying for new leads.</p></div>',
    '<div class="pain"><div class="big">$20-60</div><h3>What each lead cost you.</h3><p>Multiply that by every contact sitting untouched in your CRM.</p></div>', 1, "pain1")
rep('<div class="pain"><div class="big">1-2</div><h3>Follow-up attempts before most agents quit.</h3><p>Consumers need five or more touches before they engage, and the gap between those two numbers is where deals go to die.</p></div>',
    '<div class="pain"><div class="big">1-2</div><h3>Follow-up attempts before most agents quit.</h3><p>It takes five or more touches to convert. Deals die inside that gap.</p></div>', 1, "pain2")
rep('<div class="pain"><div class="big">9 Sides</div><h3>What the typical agent closed in 2025 (NAR).</h3><p>At that volume, every reactivated conversation matters more than another ad dollar, and it costs a fraction as much.</p></div>',
    '<div class="pain"><div class="big">9 Sides</div><h3>What the typical agent closed in 2025 (NAR).</h3><p>At that volume, one reactivated conversation is worth more than another ad dollar.</p></div>', 1, "pain3")

rep('<p>This isn\'t another platform to configure because we run the entire sequence and appointments are booked automatically into your calendar. Here\'s the whole process:</p>',
    '<p>We run the whole sequence, and appointments land on your calendar automatically. That\'s the entire process:</p>', 1, "how-sub")
rep('<p>Export your dormant leads, the ones quiet for three months or more. No integrations to build, nothing to change in your CRM.</p>',
    '<p>Export the leads quiet for three months or more. No integrations, no changes to your CRM.</p>', 1, "step1")
rep('<p>We start with a personalized email, follow it with a friendly text, and let leads who want a call simply say so. Evelyn, our conversational AI assistant, takes it from there, opening with your own read on the local market when you provide one.</p>',
    '<p>A personalized email, then a friendly text. Leads who want a call say so, and our conversational AI assistant takes it from there.</p>', 1, "step2")
rep('<h3>Qualified leads hit your calendar</h3><p>On the call, our assistant checks that the lead is genuinely looking and has a sense of timeline and budget, so appointments are with people who mean it. Your booking software connects with one click, and the appointment is scheduled automatically during the call.</p>',
    '<h3>Qualified leads hit your calendar</h3><p>On the call, the assistant confirms the lead is genuinely looking, with a sense of timeline and budget, then books during the call. Your booking link connects with one click.</p>', 1, "step3")
rep('<p>You pay per appointment we book. Every no-show is replaced free, and if a campaign doesn\'t produce, it doesn\'t cost you.</p>',
    '<p>Billed per booked appointment, one invoice at campaign close. No-shows are replaced free, and a campaign that books nothing costs nothing.</p>', 1, "step4")

rep('<p>We get paid when you get appointments. It starts with a free audit of your database, and every appointment lands on your calendar before a single dollar changes hands.</p>',
    '<p>A free audit of your database first. Then you pay only for appointments that land on your calendar.</p>', 1, "pricing-sub")
rep('          <li><svg class="check" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#D9A441" stroke-width="2.6"><path d="M20 6L9 17l-5-5"/></svg>Then every campaign ends with a full report of what it produced: messages delivered, conversations re-engaged, and appointments booked</li>\n', '', 1, "audit-bullet-rm")
rep('Close-out report: messages, conversations, and appointments - the full numbers',
    'Close-out report with the full numbers: messages, conversations, appointments', 1, "camp-bullet4")
rep('<p style="font-size:15px;color:rgba(10,27,46,.82);line-height:1.65">Most agencies wait until the pipeline runs dry to look at their old leads, and by then the best ones already signed with whoever called first. With a retainer we watch your list continually, deliver a quarterly report on what the program actually produced, from appointments booked to reactivation rates across your list, and launch campaigns the moment a segment shows life. Retainer clients enjoy a discounted per appointment rate and continual coverage, so reactivation simply runs in the background while you close.</p>',
    '<p style="font-size:15px;color:rgba(10,27,46,.82);line-height:1.65">Most teams wait until the pipeline runs dry to look at old leads. A retainer watches your list year-round: campaigns launch the moment a segment shows life, and a quarterly report shows what the program actually produced. Retainer clients book at a discounted per-appointment rate.</p>', 1, "retainer")

# FAQ: keep first 6 entries, replace the rest with a note row
faq_start = t.find('<details><summary>When a lead replies, how fast do you respond?')
faq_end_marker = 'retainer starts at $500 a month.</p></details>'
faq_end = t.find(faq_end_marker)
if faq_start == -1 or faq_end == -1:
    fails.append("[faq-trim] markers not found")
else:
    faq_end += len(faq_end_marker)
    note = '<div class="faq-more">Eight more entries carry over from the current FAQ with tightened answers: reply speed, inside sales teams, what you need on your side, what counts as a billable appointment, no-shows, seasonality, other services, and retainers.</div>'
    t = t[:faq_start] + note + t[faq_end:]
    report.append("OK  faq-trim")

# Founder: cut from after contact, insert before contact, normalize padding, fix img path
fs = t.find('<section class="founder-sec"')
ff = t.find('<footer>')
if fs == -1 or ff == -1 or not (fs < ff):
    fails.append("[founder-move] markers not found")
else:
    block = t[fs:ff].rstrip()
    t = t[:fs].rstrip() + '\n\n<footer>' + t[ff + len('<footer>'):]
    block = block.replace(' style="padding:56px 0 64px"', '')
    block = block.replace('src="matt.jpg?v=3"', 'src="../matt.jpg?v=3"')
    t = t.replace('<section id="contact">', block + '\n\n<section id="contact">', 1)
    report.append("OK  founder-move")

rep('#contact{background:var(--soft);border-top:1px solid rgba(217,164,65,.16)}',
    '#contact{border-top:1px solid rgba(217,164,65,.16)}', 1, "contact-bg")
rep('placeholder="e.g. 12000 &mdash; powers the value estimate in your audit"',
    'placeholder="e.g. 12000, powers the value estimate in your audit"', 1, "placeholder")

# static form: replace the submit script
ss = t.rfind('<script>')
se = t.rfind('</script>')
if ss == -1 or se == -1 or se < ss:
    fails.append("[script-noop] not found")
else:
    t = t[:ss] + '<script>\nfunction submitted(e){e.preventDefault();window.alert("Preview wireframe: the form is static in this preview.");return false}\n</script>\n' + t[se + len('</script>'):]
    report.append("OK  script-noop")

# relative links for subpages
for h in ["clients.html", "compliance.html", "privacy.html", "cancellation.html", "how-it-works.html"]:
    c = t.count(f'href="{h}"')
    if c == 0:
        fails.append(f"[rel-link] missing href={h}")
    else:
        t = t.replace(f'href="{h}"', f'href="../{h}"')
        report.append(f"OK  rel-link {h} x{c}")

css_add = """.preview-flag{background:var(--gold);color:var(--navy);font-size:11px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;text-align:center;padding:7px 12px}
.stats-band{background:var(--navy);border-top:1px solid rgba(217,164,65,.16);border-bottom:1px solid rgba(217,164,65,.16);padding:56px 0}
.stats-band .stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin:0;padding:0 24px;max-width:1120px}
.stats-band .stat{background:none;border:none;box-shadow:none;text-align:left;padding:6px 32px;border-left:1px solid rgba(217,164,65,.22);border-radius:0}
.stats-band .stat:first-child{border-left:none;padding-left:0}
.stats-band .stat .big{color:var(--gold)}
.stats-band .stat p{color:rgba(244,241,234,.72);margin:8px auto 0 0;max-width:300px}
@media(max-width:820px){.stats-band .stats-grid{grid-template-columns:1fr}.stats-band .stat{border-left:none;padding:14px 0;border-top:1px solid rgba(217,164,65,.22)}.stats-band .stat:first-child{border-top:none;padding-top:0}}
.faq-more{grid-column:1/-1;border:1px dashed rgba(10,27,46,.2);border-radius:12px;padding:16px 24px;font-size:13.5px;color:rgba(10,27,46,.62);text-align:center}
.founder-sec{background:var(--soft);border-top:1px solid rgba(217,164,65,.16);border-bottom:1px solid rgba(217,164,65,.16)}
@media(max-width:900px){section{padding:56px 0}}
.footer-links{flex-wrap:wrap;gap:12px 22px}
@media(max-width:900px){.chat-wrap::before{inset:-20px 0}}
"""
rep('</style>\n<link rel="icon"', css_add + '</style>\n<link rel="icon"', 1, "css-append")

# Evelyn may appear ONLY inside the off-script FAQ entry (which names her twice:
# "Evelyn only calls..." and "Evelyn runs on Retell AI"). Assert containment, not count.
es = t.find('<details><summary>What stops the AI from going off script?')
ee = t.find('</details>', es) + len('</details>')
ev_positions = [i for i in range(len(t)) if t.startswith("Evelyn", i)]
if es == -1 or ee == -1:
    fails.append("[evelyn] off-script entry not found")
elif not all(es <= p <= ee for p in ev_positions):
    fails.append(f"[evelyn] {len(ev_positions)} occurrence(s) outside the sanctioned FAQ entry")
else:
    report.append(f"OK  evelyn-contained ({len(ev_positions)} mentions, all inside the off-script entry)")

for bad in ['&mdash;', '#121F2C', 'Retell AI, turning']:
    if bad in t:
        fails.append(f"[leftover] {bad!r} still present")

if fails:
    print("FAILURES:")
    for f in fails:
        print(" ", f)
    sys.exit(1)

open(DST, "w", encoding="utf-8").write(t)
print(f"written {DST} ({len(t)} bytes)")
print("\n".join(report))
