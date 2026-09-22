#!/usr/bin/env python3
"""Apply preview/SPEC.md to the three *-preview.html pages.

Every edit is an exact-string replacement asserted to match exactly once,
or a block slice between verified anchors. Any failed assert aborts the
whole run with NOTHING written (all-or-nothing per file, and files are
written only after every edit for that file has been located).
"""
import re
import sys
from pathlib import Path

SITE = Path('/home/mrh/real-estate-consulting/site')
PREVIEW = SITE / 'preview'
EM = '\u2014'  # em dash
EN = '\u2013'  # en dash


def apply_edits(html, edits, label):
    """edits: list of (old, new). Asserts each old appears exactly once."""
    for i, (old, new) in enumerate(edits):
        n = html.count(old)
        if n != 1:
            print(f'FAIL [{label} edit {i}]: matched {n} times (need 1).')
            print('  old snippet: ' + old[:120].replace('\n', '\\n'))
            sys.exit(1)
        html = html.replace(old, new)
    return html


def replace_block(html, start_anchor, end_anchor, replacement, label, keep_end=True):
    """Slice from start_anchor to end_anchor (inclusive) and replace."""
    s = html.find(start_anchor)
    if s == -1:
        print(f'FAIL [{label}]: start anchor not found')
        sys.exit(1)
    if html.find(start_anchor, s + 1) != -1:
        print(f'FAIL [{label}]: start anchor not unique')
        sys.exit(1)
    e = html.find(end_anchor, s)
    if e == -1:
        print(f'FAIL [{label}]: end anchor not found')
        sys.exit(1)
    e_end = e + len(end_anchor)
    return html[:s] + replacement + (html[e_end:] if keep_end else html[e:])


# ============================================================ index-preview
idx_path = PREVIEW / 'index-preview.html'
idx = idx_path.read_text()

STATS_SECTION = '''</header>

<section class="stats-band" aria-label="Follow-up facts">
  <div class="container stats-row">
    <div class="stat-item"><div class="big">5+</div><p>follow-up touches are what it typically takes to convert a lead. Most agents stop at two.</p></div>
    <div class="stat-item"><div class="big">70%</div><p>of real estate leads are lost to poor follow-up, not to better competition.</p></div>
    <div class="stat-item"><div class="big">90 days+</div><p>is all it takes for a lead to go cold. Nobody's calling them. We are.</p></div>
  </div>
</section>'''

FOUNDER_NEW = '''<section class="founder-sec">
  <div class="container founder">
    <div class="founder-photo">
      <img src="matt.jpg?v=3" alt="Matt, founder of Hayes Systems" onload="this.style.display='block';document.getElementById('founder-mono').style.display='none'">
      <div id="founder-mono" class="founder-mono">M</div>
    </div>
    <div>
      <span class="eyebrow">The person behind it</span>
      <h2>Hi, I'm Matt.</h2>
      <p>I founded Hayes Systems on one principle: honesty. That's why my name and face are on it. No hollow promises, no costs hidden behind confusion. If you have questions, email me directly at <a href="mailto:Matt@hayessystems.com">Matt@hayessystems.com</a>.</p>
    </div>
  </div>
</section>'''

edits_idx = [
    # H1 nav: consolidate background to token navy
    ('nav{position:sticky;top:0;background:#121F2C;border-bottom:1px solid rgba(217,164,65,.16);z-index:50}',
     'nav{position:sticky;top:0;background:var(--navy);border-bottom:1px solid rgba(217,164,65,.16);z-index:50}'),
    # H3 stats: CSS block replaced (cards -> navy band)
    ('''/* Stats */
.stats-grid{display:grid;grid-template-columns:repeat(3,minmax(240px,320px));justify-content:center;gap:20px;margin:64px auto 8px;max-width:1120px;padding:0 24px}
@media(max-width:820px){.stats-grid{grid-template-columns:1fr}}
.stat{background:#FCFAF4;border:1px solid rgba(10,27,46,.09);box-shadow:0 10px 30px rgba(10,27,46,.06);border-radius:var(--radius);padding:28px 26px;text-align:center}
.stat .big{font-family:var(--serif);font-size:42px;color:var(--gold-ink);font-weight:600;line-height:1}
.stat p{font-size:15px;color:rgba(10,27,46,.75);margin:10px auto 0;max-width:270px;font-weight:400}''',
     '''/* Stats */
.stats-band{background:var(--navy);padding:56px 0}
.stats-row{display:grid;grid-template-columns:repeat(3,1fr);gap:0 44px}
.stat-item .big{font-family:var(--serif);font-size:42px;color:var(--gold);font-weight:600;line-height:1}
.stat-item p{font-size:15px;color:rgba(244,241,234,.72);margin:10px 0 0;max-width:300px;font-weight:400}
.stat-item + .stat-item{border-left:1px solid rgba(217,164,65,.16);padding-left:44px}
@media(max-width:820px){.stats-row{grid-template-columns:1fr;gap:26px}.stat-item + .stat-item{border-left:none;padding-left:0;border-top:1px solid rgba(217,164,65,.16);padding-top:26px}}'''),
    # Global mobile section rhythm + footer link wrap (375 overflow fix)
    ('section{padding:72px 0}\n',
     'section{padding:72px 0}\n@media(max-width:900px){section{padding:56px 0}}\n'),
    ('.footer-links{display:flex;gap:22px}',
     '.footer-links{display:flex;gap:14px 22px;flex-wrap:wrap}'),
    # H4 problem: soften card shadow one step
    ('.pain{border:1px solid rgba(217,164,65,.4);border-radius:var(--radius);padding:28px;background:#FCFAF4;box-shadow:0 10px 30px rgba(10,27,46,.06);text-align:center}',
     '.pain{border:1px solid rgba(217,164,65,.4);border-radius:var(--radius);padding:28px;background:#FCFAF4;box-shadow:0 6px 18px rgba(10,27,46,.05);text-align:center}'),
    # H7 founder: section now a soft band on the 72px scale
    ('/* Founder band */\n.founder{',
     '/* Founder band */\n.founder-sec{background:var(--soft);border-top:1px solid rgba(217,164,65,.16);border-bottom:1px solid rgba(217,164,65,.16)}\n.founder{'),
    # H9 contact: drops the soft background (founder took it)
    ('#contact{background:var(--soft);border-top:1px solid rgba(217,164,65,.16)}',
     '#contact{background:var(--ivory)}'),
    # H2 hero lede: 56 words -> 37
    ('<p class="lede">Your CRM is already full of leads you paid for. Hayes Systems pairs proven email and text outreach with the latest in voice automation provided by Retell AI, turning forgotten contacts into qualified appointments on your calendar. Our Massachusetts-based team proudly serves New England and beyond, delivering measurable results with no CRM changes and nothing to learn.</p>',
     '<p class="lede">Your CRM already holds leads you paid for and never fully worked. Hayes Systems re-engages them with personalized email, text, and opt-in AI calls, and books qualified appointments straight onto your calendar.</p>'),
    # H4 problem cards: tightened captions
    ('<p>Multiply that by the contacts sitting untouched in your CRM and you\'ll see the inventory you\'re ignoring while paying for new leads.</p>',
     '<p>Multiply that by every contact sitting untouched in your CRM.</p>'),
    ('<p>Consumers need five or more touches before they engage, and the gap between those two numbers is where deals go to die.</p>',
     '<p>It takes five or more touches to convert. Deals die inside that gap.</p>'),
    ('<p>At that volume, every reactivated conversation matters more than another ad dollar, and it costs a fraction as much.</p>',
     '<p>At that volume, one reactivated conversation is worth more than another ad dollar.</p>'),
    # H5 how: section sub
    ('<p>This isn\'t another platform to configure because we run the entire sequence and appointments are booked automatically into your calendar. Here\'s the whole process:</p>',
     '<p>We run the whole sequence, and appointments land on your calendar automatically. That\'s the entire process.</p>'),
    # H5 step copy (1-4)
    ('<p>Export your dormant leads, the ones quiet for three months or more. No integrations to build, nothing to change in your CRM.</p>',
     '<p>Export the leads quiet for three months or more. No integrations, no changes to your CRM.</p>'),
    ('<p>We start with a personalized email, follow it with a friendly text, and let leads who want a call simply say so. Evelyn, our conversational AI assistant, takes it from there, opening with your own read on the local market when you provide one.</p>',
     '<p>A personalized email, then a friendly text. Leads who want a call say so, and our conversational AI assistant takes it from there.</p>'),
    ('<h3>Qualified leads hit your calendar</h3><p>On the call, our assistant checks that the lead is genuinely looking and has a sense of timeline and budget, so appointments are with people who mean it. Your booking software connects with one click, and the appointment is scheduled automatically during the call.</p>',
     '<h3>Appointments hit your calendar</h3><p>On the call, the assistant confirms the lead is genuinely looking, with a sense of timeline and budget, then books during the call. Your booking link connects with one click.</p>'),
    ('<p>You pay per appointment we book. Every no-show is replaced free, and if a campaign doesn\'t produce, it doesn\'t cost you.</p>',
     '<p>Billed per booked appointment, one invoice at campaign close. No-shows are replaced free, and a campaign that books nothing costs nothing.</p>'),
    # H6 pricing: section sub
    ('<p>We get paid when you get appointments. It starts with a free audit of your database, and every appointment lands on your calendar before a single dollar changes hands.</p>',
     '<p>A free audit of your database first. Then you pay only for appointments that land on your calendar.</p>'),
    # H6 audit card: delete the misplaced close-out bullet (line, incl. newline)
    ('          <li><svg class="check" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#D9A441" stroke-width="2.6"><path d="M20 6L9 17l-5-5"/></svg>Then every campaign ends with a full report of what it produced: messages delivered, conversations re-engaged, and appointments booked</li>\n',
     ''),
    # H6 campaigns bullet 4: hyphen-as-dash phrasing replaced
    ('Close-out report: messages, conversations, and appointments - the full numbers',
     'Close-out report with the full numbers: messages, conversations, appointments'),
    # H6 retainer band paragraph: 90 -> ~55 words
    ('<p style="font-size:15px;color:rgba(10,27,46,.82);line-height:1.65">Most agencies wait until the pipeline runs dry to look at their old leads, and by then the best ones already signed with whoever called first. With a retainer we watch your list continually, deliver a quarterly report on what the program actually produced, from appointments booked to reactivation rates across your list, and launch campaigns the moment a segment shows life. Retainer clients enjoy a discounted per appointment rate and continual coverage, so reactivation simply runs in the background while you close.</p>',
     '<p style="font-size:15px;color:rgba(10,27,46,.82);line-height:1.65">Most teams wait until the pipeline runs dry to look at old leads. A retainer watches your list year-round: campaigns launch the moment a segment shows life, and a quarterly report shows what the program actually produced. Retainer clients book at a discounted per-appointment rate.</p>'),
    # H9 contact form: placeholder em-dash entity removed
    ('placeholder="e.g. 12000 &mdash; powers the value estimate in your audit"',
     'placeholder="e.g. 12000, powers the value estimate in your audit"'),
]

# FAQ tightened answers (block swaps anchored on summaries)
def faq_block(summary, body):
    return f'<details><summary>{summary}</summary><p>{body}</p></details>'

FAQ_EDITS = [
    ('What stops the AI from going off script?',
     'Evelyn only calls leads who explicitly asked for the call, and she opens every conversation by saying she is an AI assistant. Her job is narrow: confirm budget and timeline and get the appointment booked. If a lead asks something she cannot know, like whether a specific house is still for sale, she says so plainly and books the call with you to answer it, because specific property questions belong to the licensee. Every call is recorded and transcribed so you can hear exactly what was said. Evelyn runs on <a href="https://www.retellai.com/#try-demo" target="_blank" rel="noopener">Retell AI</a>, and you can hear the platform for yourself with their live demo.'),
    ('Why not just build this myself?',
     'You can, and some agents try. The pieces exist; the hard part is making them all work together. Automations break quietly: a CRM changes its export format, a scheduling link expires, a messaging platform tightens its rules, and the workflow you set up in January is silently doing nothing by March. Someone has to notice, diagnose, and fix it every time, forever. That is a second job, and it is the job we actually do: our sequences are monitored, and when something drifts we fix it before you hear about it. You would also take on the compliance side yourself, as the sender of record: consent records, opt-out suppression, calling-hour rules. Work with us and you never think about it; appointments just land on your calendar.'),
    ('When a lead replies, how fast do you respond?',
     'Fast enough that momentum never dies. Industry research puts a big premium on responding within the first hour, and our median reply goes out in about a minute: when a lead says yes, the next question (picking a time) is already on its way. Old leads who finally raise a hand get the same urgency a brand new inquiry would.'),
    ('What do I need on my side?',
     "Just a calendar our assistant can book appointments into. If you use Cal.com, Calendly, or GoHighLevel, we email you a link, you press authorize, and you're done. Solo? Any plan works, including free. Running a team? Your booking service needs round-robin scheduling, which on Cal.com and Calendly comes with their team plans (about $12-16 per user a month); GoHighLevel includes it in the standard subscription. Use something else? A free Cal.com calendar works alongside whatever you have."),
]

# 1) exact-string edits
idx = apply_edits(idx, edits_idx, 'index')
# 2) FAQ block swaps
for summary, body in FAQ_EDITS:
    start = f'<details><summary>{summary}</summary>'
    idx = replace_block(idx, start, '</details>', faq_block(summary, body), f'FAQ:{summary[:30]}')
# 3) move stats strip out of the header element
idx = replace_block(idx, '  <div class="container stats-grid">', '</header>', STATS_SECTION, 'stats-move')
# 4) move founder section from after contact to before it
idx = replace_block(idx, '<section class="founder-sec"', '</section>', '', 'founder-remove')
anchor = '<section id="contact">'
if idx.count(anchor) != 1:
    print('FAIL contact anchor not unique'); sys.exit(1)
idx = idx.replace(anchor, FOUNDER_NEW + '\n' + anchor)

idx_path.write_text(idx)
print(f'index-preview.html written ({len(idx)} bytes)')

# ==================================================== how-it-works-preview
hiw_path = PREVIEW / 'how-it-works-preview.html'
hiw = hiw_path.read_text()

edits_hiw = [
    # title em-dash
    (f'<title>How It Works {EM} Hayes Systems</title>',
     '<title>How It Works | Hayes Systems</title>'),
    # h2 rhythm matches homepage section-head gap
    ('h2{font-family:var(--serif);font-weight:600;font-size:24px;margin:34px 0 10px}',
     'h2{font-family:var(--serif);font-weight:600;font-size:24px;margin:40px 0 10px}'),
    # mobile page rhythm
    ('.back{display:inline-block;margin-top:26px;font-size:13px;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:var(--gold-ink);font-weight:600}',
     '.back{display:inline-block;margin-top:26px;font-size:13px;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;color:var(--gold-ink);font-weight:600}\n@media(max-width:900px){.wrap{padding:48px 20px 64px}}'),
    # "What you do" item 1: 62 words -> step sentence only, plan detail to a note line
    ('<li><strong>Fill in one form.</strong> Business details and your booking platform (Cal.com, Calendly, or GoHighLevel). Takes about five minutes in your browser, and a completed copy of everything you signed arrives in your email afterward. Solo agents are fine on any plan, including free; teams need their booking service\'s team plan for shared round-robin booking (GoHighLevel includes it in the standard subscription).</li>',
     '<li><strong>Fill in one form.</strong> Business details and your booking platform (Cal.com, Calendly, or GoHighLevel). Takes about five minutes in your browser, and a completed copy of everything you signed arrives in your email afterward.</li>'),
    ('  </ol>\n\n  <h2>What we do</h2>',
     '  </ol>\n  <p class="plan-note">Solo agents are fine on any plan, including free. Teams need their booking service\'s team plan for shared round-robin booking; GoHighLevel includes it in the standard subscription.</p>\n\n  <h2>What we do</h2>'),
    # note-line style
    ('table{width:100%;border-collapse:collapse;margin:18px 0}',
     '.plan-note{font-size:13px;color:rgba(10,27,46,.62);margin:-4px 0 18px}\ntable{width:100%;border-collapse:collapse;margin:18px 0}'),
    # "What you pay" card: four paragraphs -> two (price line + no-show line)
    ('''<p class="card-sub">That's the entire price. Nothing upfront, nothing monthly, nothing per message.</p>
    <p class="card-sub">When the campaign wraps, one invoice covers the appointments it booked. It's charged automatically to the card on file, and a receipt lands in your email the same day.</p>
    <p class="card-sub">If a prospect no-shows, that appointment isn't billed and your next one is free.</p>''',
     '''<p class="card-sub">If a prospect no-shows, that appointment isn't billed and your next one is free.</p>'''),
    # label -> benefit heads
    ('<h2>Stopping</h2>', '<h2>Stop any time</h2>'),
    ('<h2>What we ask of your data</h2>', '<h2>How your data is handled</h2>'),
]

hiw = apply_edits(hiw, edits_hiw, 'how-it-works')
hiw_path.write_text(hiw)
print(f'how-it-works-preview.html written ({len(hiw)} bytes)')

# ======================================================== estimate-preview
est_path = PREVIEW / 'estimate-preview.html'
est = est_path.read_text()

edits_est = [
    (f'<title>Your Launch Estimate {EM} Hayes Systems</title>',
     '<title>Your Launch Estimate | Hayes Systems</title>'),
    ('h2{font-family:var(--serif);font-weight:600;font-size:24px;margin:34px 0 10px}',
     'h2{font-family:var(--serif);font-weight:600;font-size:24px;margin:40px 0 10px}'),
    ('.nodata{border:1px solid rgba(10,27,46,.18);border-radius:16px;padding:22px 26px;background:var(--soft);margin:22px 0}',
     '.nodata{border:1px solid rgba(10,27,46,.18);border-radius:16px;padding:22px 26px;background:var(--soft);margin:22px 0}\n@media(max-width:900px){.wrap{padding:48px 20px 64px}}'),
    # card small print: billing sentence only (band math stays one section lower)
    ('<p class="small">You are billed only for appointments that land on your calendar, on one invoice when the campaign ends. A prospect who no-shows costs you nothing and earns you a free replacement.</p>',
     '<p class="small">You are billed only for appointments that land on your calendar, on one invoice when the campaign ends.</p>'),
    # table a11y: explicit scopes, no visual change
    ('<tr><th>What</th><th>Estimate</th></tr>',
     '<tr><th scope="col">What</th><th scope="col">Estimate</th></tr>'),
    ('<tr><td>Projected appointments booked</td><td><b id="appts">-</b></td></tr>',
     '<tr><td scope="row">Projected appointments booked</td><td><b id="appts">-</b></td></tr>'),
    ('<tr><td>Cost if the campaign hits the low end</td><td><b id="cost-lo">-</b></td></tr>',
     '<tr><td scope="row">Cost if the campaign hits the low end</td><td><b id="cost-lo">-</b></td></tr>'),
    ('<tr><td>Cost if it hits the high end</td><td><b id="cost-hi">-</b></td></tr>',
     '<tr><td scope="row">Cost if it hits the high end</td><td><b id="cost-hi">-</b></td></tr>'),
]

est = apply_edits(est, edits_est, 'estimate')
est_path.write_text(est)
print(f'estimate-preview.html written ({len(est)} bytes)')

# ------------------------------------------------------------ copy checks
bad = False
for name in ['index-preview.html', 'how-it-works-preview.html', 'estimate-preview.html']:
    t = (PREVIEW / name).read_text()
    em = t.count(EM) + t.count('&mdash;')
    en = t.count(EN)
    print(f'{name}: em-dash={em} en-dash={en}')
    if em or en:
        bad = True
if bad:
    print('FAIL: dash rule violated'); sys.exit(1)
print('ALL EDITS APPLIED CLEAN')
