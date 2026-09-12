#!/usr/bin/env python3
"""Pass 5: last 1440-full-measure >5-line FAQ fixes (split or trim, facts kept)."""
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
    # compliant: 6L -> ~4.6L
    ("Opt-outs, calling hours, and recordkeeping are our responsibility, handled before anything sends.",
     "Opt-outs, calling hours, and recordkeeping are handled before anything sends."),
    # off-script: split into two paragraphs (51w + 15w)
    ("<p>Evelyn only calls leads who explicitly asked for the call and opens every conversation by saying she is an AI assistant. Her job is narrow: confirm budget and timeline and book the appointment. Property-specific questions belong to you, the licensee, so she says so plainly and books the call with you to answer them. Every call is recorded and transcribed. Evelyn runs on <a href=\"https://www.retellai.com/#try-demo\" target=\"_blank\" rel=\"noopener\">Retell AI</a>; try their live demo.</p>",
     "<p>Evelyn only calls leads who explicitly asked for the call and opens every conversation by saying she is an AI assistant. Her job is narrow: confirm budget and timeline and book the appointment. Property-specific questions belong to you, the licensee, so she says so plainly and books the call with you to answer them.</p><p>Every call is recorded and transcribed. Evelyn runs on <a href=\"https://www.retellai.com/#try-demo\" target=\"_blank\" rel=\"noopener\">Retell AI</a>; try their live demo.</p>"),
    # build-myself p1: 6L -> 52w
    ("You can, and some agents try. The pieces exist; the hard part is making them work together. Automations break quietly: a CRM changes its export format, a scheduling link expires, and the workflow you built in January is silently dead by March. Someone has to notice and fix it, forever. That is a second job, and it is the job we actually do.",
     "You can. The pieces exist; the hard part is making them work together. Automations break quietly: a CRM changes its export format, a scheduling link expires, and the workflow you built in January is silently dead by March. Someone has to notice and fix it, forever. That is the job we actually do."),
    # what-i-need: split (21w + 43w)
    ("<p>Just a calendar our assistant can book into. Cal.com, Calendly, or GoHighLevel: we email a link, you press authorize, done. Solo agents are fine on any plan, including free. Teams need round-robin scheduling: Cal.com and Calendly include it in team plans (about $12-16 per user a month), GoHighLevel in the standard subscription. A free Cal.com calendar also works alongside anything else.</p>",
     "<p>Just a calendar our assistant can book into. Cal.com, Calendly, or GoHighLevel: we email a link, you press authorize, done.</p><p>Solo agents are fine on any plan, including free. Teams need round-robin scheduling: Cal.com and Calendly include it in team plans (about $12-16 per user a month), GoHighLevel in the standard subscription. A free Cal.com calendar also works alongside anything else.</p>"),
    # what-counts: 6L -> 51w
    ("An appointment that lands on your calendar with a prospect from your list, booked during a call or directly from the link we send. That's the billing event. One invoice at campaign close covers the appointments booked, charged to the card on file; if anything looks wrong, you have 14 days to say so and we make it right.",
     "An appointment on your calendar with a prospect from your list, booked during a call or from the link we send. One invoice at close covers the appointments booked, charged to the card on file. If anything looks wrong, you have 14 days to say so and we make it right."),
], 'index')

idx_path.write_text(idx)
print(f'index-preview.html updated ({len(idx)} bytes)')
print('PASS-5 DONE')
