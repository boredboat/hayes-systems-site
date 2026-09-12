#!/usr/bin/env python3
"""Pass 4: final FAQ/paragraph trims. Facts preserved, sanctioned numbers only."""
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

# ------------------------------------------------ index
idx_path = P / 'index-preview.html'
idx = idx_path.read_text()

idx = apply_edits(idx, [
    # compliance FAQ 59w -> 48w
    ("Nothing we do is cold. A call only happens after that person replies YES in writing. About twenty states require paid registration to call their residents, so we don't call there; email and text continue normally. Opt-outs, calling hours, and the recordkeeping behind them are our responsibility, handled before anything sends.",
     "Nothing we do is cold. A call only happens after that person replies YES in writing. About twenty states require paid registration to call their residents, so we don't call there; email and text continue normally. Opt-outs, calling hours, and recordkeeping are our responsibility, handled before anything sends."),
    # annoy-goodwill FAQ 54w -> 46w
    ("Every message is personalized and reads as a friendly check-in from your team, not an impersonal marketing blast. The moment a lead replies, automated messages stop and a real conversation starts: interested responses go straight to you, and anyone who asks us to stop is simply stopped, suppressed everywhere, permanently, with no further contact.",
     "Every message is personalized and reads as a friendly check-in from your team, not a marketing blast. When a lead replies, automated messages stop and a real conversation starts: interested responses go straight to you, and anyone who asks us to stop is stopped everywhere, permanently."),
    # old-leads FAQ 57w -> 51w (keeps the fresher-leads fact)
    ("Older is our specialty: three months quiet is the minimum age we work (fresher leads belong to your own follow-up), and the sweet spot runs from there to a couple of years. We've seen databases with contacts three and four years old produce appointments. The audit will tell you honestly what yours is worth before anyone commits.",
     "Older is our specialty: three months quiet is the minimum age we work (fresher leads belong to your own follow-up), and the sweet spot runs to a couple of years. Databases with three- and four-year-old contacts have produced appointments. The audit tells you honestly what yours is worth before anyone commits."),
    # crm-access FAQ 53w -> 39w
    ("No. Export your full list as a CSV and send it over as-is. We handle everything on our side: duplicates, dead numbers, and junk entries are removed automatically, and only the promising old leads get worked. Appointments land right on your calendar, with nothing to integrate and nothing to cancel if you stop.",
     "No. Export your full list as a CSV and send it over as-is. We handle the rest: duplicates, dead numbers, and junk entries are removed, and only the promising old leads get worked. Appointments land right on your calendar."),
    # reply speed FAQ: pass-1 version -> tighter
    ("Fast enough that momentum never dies. Industry research puts a big premium on responding within the first hour, and our median reply goes out in about a minute: when a lead says yes, the next question (picking a time) is already on its way. Old leads who finally raise a hand get the same urgency a brand new inquiry would.",
     "Fast enough that momentum never dies: our median reply goes out in about a minute, so when a lead says yes, the next question (picking a time) is already on its way. Industry research puts a big premium on responding inside the first hour. Old leads get the same urgency as new inquiries."),
    # inside sales FAQ 65w -> 51w
    ("Good, keep them on new leads; that is the job they are measured on, and we do not touch it. We work the old list that never gets called because fresh inquiries always win the hour. Appointments we book arrive on your agents' calendars with the same qualification notes your inside team writes (timeline, budget), so the handoff feels identical to what they already trust.",
     "Good, keep them on new leads; that's the job they are measured on, and we don't touch it. We work the old list that never gets called. Appointments we book arrive on your agents' calendars with the same qualification notes your inside team writes (timeline, budget), so the handoff feels familiar."),
    # what-i-need FAQ 77w -> 61w
    ("Just a calendar our assistant can book appointments into. If you use Cal.com, Calendly, or GoHighLevel, we email you a link, you press authorize, and you're done. Solo? Any plan works, including free. Running a team? Your booking service needs round-robin scheduling, which on Cal.com and Calendly comes with their team plans (about $12-16 per user a month); GoHighLevel includes it in the standard subscription. Use something else? A free Cal.com calendar works alongside whatever you have.",
     "Just a calendar our assistant can book into. Cal.com, Calendly, or GoHighLevel: we email a link, you press authorize, done. Solo agents are fine on any plan, including free. Teams need round-robin scheduling: Cal.com and Calendly include it in team plans (about $12-16 per user a month), GoHighLevel in the standard subscription. A free Cal.com calendar also works alongside anything else."),
    # what-counts FAQ -> 59w
    ("An appointment that lands on your calendar with a prospect from your list, whether our assistant books it during a call or they book directly from the link we send. That's the billing event. When a campaign wraps, one invoice covers the appointments it booked and is charged automatically to the card on file. If anything on it looks wrong, you have 14 days to say so and we make it right.",
     "An appointment that lands on your calendar with a prospect from your list, booked during a call or directly from the link we send. That's the billing event. One invoice at campaign close covers the appointments booked, charged to the card on file; if anything looks wrong, you have 14 days to say so and we make it right."),
    # no-show FAQ 40w -> 29w
    ("When a prospect no-shows, your next booked appointment is on us. On Calendly the detection is automatic: your calendar tells us the moment a no-show is marked. On Cal.com and GoHighLevel, flag it and the credit lands the same way.",
     "When a prospect no-shows, your next booked appointment is on us. On Calendly the detection is automatic; on Cal.com and GoHighLevel, flag it and the credit lands the same way."),
    # seasonality FAQ 56w -> 42w (drops the unsanctioned jump-a-third figure)
    ("Homes sell year-round, but the market peaks April through June and slows about a third by January. A fall or winter campaign still books appointments, and it means your pipeline is built before the March ramp, when buyer activity jumps about a third in a single month. The audit prices your list as it is today.",
     "Homes sell year-round, but the market peaks April through June and slows about a third by January. A fall or winter campaign still books appointments and builds your pipeline before the March ramp. The audit prices your list as it is today."),
    # retainer FAQ 61w -> 42w
    ("Yes. A monthly retainer covers the standing service: list monitoring and hygiene, suppression management, a quarterly report of what the program produced (appointments booked and reactivation rate), and campaigns that launch as each segment shows life. Retainer clients enjoy a discounted per appointment rate with continual coverage: bookings run $50 instead of $60 and the retainer starts at $500 a month.",
     "Yes. A monthly retainer covers list monitoring and hygiene, suppression management, a quarterly report of what the program produced, and campaigns that launch as each segment shows life. Bookings run $50 instead of $60, and the retainer starts at $500 a month."),
    # build-myself p1 68w -> 63w
    ("You can, and some agents try. The pieces exist; the hard part is making them all work together. Automations break quietly: a CRM changes its export format, a scheduling link expires, and the workflow you set up in January is silently doing nothing by March. Someone has to notice and fix it every time, forever. That is a second job, and it is the job we actually do.",
     "You can, and some agents try. The pieces exist; the hard part is making them work together. Automations break quietly: a CRM changes its export format, a scheduling link expires, and the workflow you built in January is silently dead by March. Someone has to notice and fix it, forever. That is a second job, and it is the job we actually do."),
], 'index')

idx_path.write_text(idx)
print(f'index-preview.html updated ({len(idx)} bytes)')

# ------------------------------------------------ how-it-works
hiw_path = P / 'how-it-works-preview.html'
hiw = hiw_path.read_text()

hiw = apply_edits(hiw, [
    ("Any time, any way you like. Work stops within a business day. Appointments already on your calendar stay there and stay booked; the only thing owed is appointments already booked at that moment. Opt-outs we've recorded for your leads stay honored permanently. The full policy lives on our <a href=\"cancellation.html\">cancellation page</a>.",
     "Any time, any way you like. Work stops within a business day. Appointments already on your calendar stay booked; the only thing owed is appointments already booked at that moment. Recorded opt-outs stay honored permanently. The full policy is on our <a href=\"cancellation.html\">cancellation page</a>."),
], 'how-it-works')

hiw_path.write_text(hiw)
print(f'how-it-works-preview.html updated ({len(hiw)} bytes)')
print('PASS-4 DONE')
