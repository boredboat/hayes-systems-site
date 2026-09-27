# Hero rework previews (9/26) — UNMERGED, for Matt's pick

All three replace the fabricated SMS chat prop with a "What we run for you"
service panel (5 ticks: pull leads read-only, email outreach, calls for
leads who want them, interest confirmed pre-booking, calendar booking)
and add a "Works with your CRM" text row under the calendar logo row
(Follow Up Boss, kvCORE/BoldTrail, LionDesk, HubSpot, Pipedrive, or a
CSV export — mirrors ops/crm_connect_copy.py CONNECTABLE exactly).

- vA: NEW headline "We turn the leads you already paid for into
  appointments on your calendar." + service-process lede
- vB: NEW headline "Your next appointments are already in your CRM.
  We go get them." + short punchy lede ("You keep closing. Your list
  keeps working.")
- vC: KEEPS the shipped headline ("The cheapest leads..."), service
  lede only

Mobile overflow checks pass on all three; desktop geometry verified.

## RESOLVED 9/26 (Matt's pick)
Tagline "The cheapest leads..." and photo STAY (declined vA/vB headlines).
Shipped (commit 8ff7d03): vC-shaped lede + service panel with CALL-CENTRIC
sequence — email first, interested leads get the call, appointment booked ON
that call (call is the only booking path; the earlier "convos for those who
want one" framing was wrong and did not ship). CRM row shipped as specced.
These previews are historical; live index.html is the record.
