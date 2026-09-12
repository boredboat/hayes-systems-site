# NOTES: preview pages vs live

Built from SPEC.md (t_c4a2f834) applied to byte-copies of the live pages.
Live pages untouched (md5-verified; git shows only preview/ added).
Assets resolve through symlinks: fonts/, img/, matt.jpg, and the sibling
pages linked from copy (clients, compliance, privacy, cancellation,
onboard, how-it-works).

## index-preview.html

- Nav: background consolidated from off-token #121F2C to var(--navy).
- Hero: lede cut 56 to 37 words per SPEC (vendor, service area, and
  "nothing to learn" details dropped; Retell AI stays in the FAQ).
- Stats: moved out of the header into its own navy band under the hero;
  chrome removed, gold numerals on navy, ivory captions at 72 percent,
  hairline dividers; stat 3 caption cut 30 to 13 words.
- Problem: card captions cut to SPEC copy; card shadow softened one step.
- How it works: step copy per SPEC; step 2 now says "our conversational
  AI assistant" (Evelyn removed from lead-facing copy; she remains only
  in the off-script FAQ entry, per the standing rule).
- Pricing: section sub rewritten; the audit card's misplaced close-out
  bullet deleted (the Campaigns card keeps it); campaigns bullet 4
  reworded to drop the hyphen-as-dash; retainer paragraph cut 90 to about
  55 words with the $50/$500 numbers kept in the FAQ only.
- Founder band: moved before the contact section (page now ends on the
  conversion moment), put on the soft band, copy per SPEC.
- FAQ: all 14 entries kept; every answer tightened to 5 rendered lines
  or fewer at 1440 (measured, not eyeballed); long answers split at
  sentence boundaries instead of losing facts; the unsanctioned "jumps
  about a third in a single month" figure dropped from the seasonality
  answer; sanctioned numbers ($60, $50/$500, April to June, about a
  third slower by January, 5+/70%/90 days+) all retained.
- Contact: placeholder em-dash entity removed.
- Footer: link row now wraps (live page overflows 724px at 375; preview
  is 0px); chat card glow inset reduced at mobile (was pushing scrollWidth
  to 401px).

## how-it-works-preview.html

- Title em-dash replaced with a pipe.
- "What you do" item 1 cut to its step sentence; the booking-plan detail
  (solo free, teams round-robin, GoHighLevel) moved to a note line under
  the list.
- "What you pay" card trimmed to price line plus no-show line; the cost
  table stays the single detailed source.
- h2 top margin standardized to 40px; mobile page padding 48/64 at 900px
  and below.
- "Stopping" retitled "Stop any time"; "What we ask of your data"
  retitled "How your data is handled"; stopping paragraph tightened.

## estimate-preview.html

- Title em-dash replaced with a pipe.
- Card small print trimmed to the billing sentence (band math stays in
  "Where these numbers come from", now split into two paragraphs at the
  sentence boundary for mobile).
- Table cells get explicit scope attributes (no visual change).
- Spacing/type inherit the global scale; h2 margin 40px.

## QA evidence (rerunnable)

- preview/verify.py: 23 structural assertions, all PASS.
- preview/dash-scan.py: 0 em/en dashes in rendered text (details opened)
  and 0 in serialized HTML, all three pages.
- preview/shots.py: 1440 and 375 renders plus mid-page shots in
  preview/shots/; scrollWidth minus clientWidth = 0 at both widths on
  all three pages (live index is +724 at 375).
- preview/line-measure.py: 0 paragraphs or list items over 5 rendered
  lines at 1440 on all three pages. At 375 some FAQ answers still run
  6 to 9 lines inside a 331px measure; cutting further would drop facts,
  so they were split at sentence boundaries instead.
- Live integrity: index.html, how-it-works.html, estimate.html md5
  unchanged; git -C site status shows only preview/ untracked.

## Mobile line-count note for review

The 5-line readability bar is met at 1440 everywhere. On a 375px viewport
the FAQ measure is 331px, so even SPEC-authored copy (the 37-word hero
lede) renders 7 lines. Every 375 paragraph over 5 lines is a split or
tightened version of its 1440 counterpart; none is a wall of text by
word count (all under 60 words except the footer legal line).
