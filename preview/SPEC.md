# SPEC: Hayes Systems visual refresh

Preview only. Nothing in this folder touches the live site. Files:
site/preview/SPEC.md (this plan), site/preview/index-wireframe.html (homepage
wireframe with real tightened copy), site/preview/shots/ (QA renders).

Token source of truth: the :root block at the top of site/index.html,
identical in all three pages. The wireframe reuses it verbatim, no edits.

## Tokens and their single job

| Token | Hex | Role |
|---|---|---|
| --navy | #02101F | Structural dark: nav, footer, new stats band |
| --navy-lift | #071526 | Unused on these pages, stays defined |
| --navy-card | #0B1C30 | Founder photo fallback |
| --ivory | #EDE8DD | Page background |
| --soft | #F4F1EA | Alternating section bands |
| #FCFAF4 | literal | Cards on any band (kept as literal, as today) |
| --gold | #D9A441 | Primary CTA, step numerals, stat numerals, hairlines at .16 alpha |
| --gold-ink | #7D5C15 | Eyebrows, links, inline emphasis on light |
| --ink-on-light | #0A1B2E | Headings and body |

No new colors anywhere. One consolidation: the nav background is currently
#121F2C, an off-token near-duplicate of navy that belongs to no family. It
becomes var(--navy). Role statement after this change: navy marks structure
(nav, stats band, footer), soft and ivory alternate for pacing, cream lifts
content, gold acts.

## Global system (all three pages)

Spacing scale, stated once and enforced:
- Sections: 72px top and bottom. New mobile rule: 56px at 900px and below.
  The current pages have no mobile section padding and render a full 72 at
  375, which is why mobile feels airless in the wrong places.
- Inner bands inside a section: 56px.
- Card padding: 28px. Grid gaps: 20px. Section head to content: 36px.
- The two current outliers normalize to this scale: the founder band's
  bespoke inline padding (56px 0 64px) and the stats strip's asymmetric
  margins (64px auto 8px).

Type scale: unchanged. 12.5px eyebrow, 15px body, 18px lede, 22px serif h3,
h2 clamp(30px, 4vw, 44px), h1 clamp(36px, 5vw, 58px), 42px stat numeral,
56px price numeral. No new sizes are introduced. Tightening is wording and
line count, not font shuffling.

Measure: line-length caps stay (~70ch max): lede 560px, section head 640px,
step and pain copy 270px centered.

Band rhythm: ivory and soft alternate down every page; navy appears only as
structure. Current homepage already alternates; the refresh keeps the beat
unbroken through the reordered bottom half (see H7).

## Page 1: index.html

### H1 Nav
Tightens: background consolidates to var(--navy).
Reflows: none.
Rewords: none. "Already a client?" stays gold, CTA stays.

### H2 Hero
Tightens: lede drops from 56 words / 4 sentences to 37 words / 2 sentences.
The dropped detail (Retell AI vendor mention, New England service area,
"nothing to learn") is either already in the trust row or belongs lower;
vendor credit stays in the FAQ where it already lives.
Primary headline (kept): "The cheapest leads you'll ever work are the ones
you already paid for."
Alternative: "The pipeline you paid for is still in your CRM."
Lede new text: "Your CRM already holds leads you paid for and never fully
worked. Hayes Systems re-engages them with personalized email, text, and
opt-in AI calls, and books qualified appointments straight onto your
calendar."
Chat demo card: unchanged, real sample conversation, no fake polish.

### H3 Stats strip
Tightens: captions cut to one or two lines (stat 3 drops from 30 words to
13). Card chrome (cream, border, shadow) is removed: numerals carry it.
Reflows: the strip moves out of the header element and becomes its own
navy band directly under the hero. This is the one structural change to
the top half, and it does three jobs: gives the hero image a clean bottom
edge, creates the strong pacing beat the brief asks for, and puts the
three follow-up facts in the highest-value slot on the page.
Numerals gold on navy, captions ivory at 72 percent, left-aligned with
hairline dividers, three equal columns, stack on mobile.
Fallback if the band reads heavy in review: keep the band ivory with gold
numerals and the same tightened captions. Copy decision stands either way.
Rewords: none beyond caption trims. Numbers 5+, 70%, 90 days+ unchanged.

### H4 Problem
Tightens: card captions from 20 to 25 words down to 10 to 15. Shadow
softens one step (0 6px 18px at .05) so bordered cards stop doubling up
depth.
Reflows: none. Three equal cards.
Primary head (kept): "You already bought this pipeline."
Alternative: "The follow-up stopped. The opportunity didn't."
Card copy, new:
- $20-60, "What each lead cost you": "Multiply that by every contact
  sitting untouched in your CRM."
- 1-2, "Follow-up attempts before most agents quit": "It takes five or
  more touches to convert. Deals die inside that gap."
- 9 sides, "What the typical agent closed in 2025 (NAR)": "At that volume,
  one reactivated conversation is worth more than another ad dollar."

### H5 How it works
Tightens: step paragraphs to two sentences max; step 2 drops from 47 words
to 24; step 3 from 44 to 26.
Reflows: none. Four equal steps, numbered chips unchanged.
Copy-rule fix: step 2 currently names Evelyn in lead-facing copy. The
wireframe says "our conversational AI assistant". The name survives only
in the existing FAQ entry about going off script, per the standing rule.
Primary head (kept): "Four steps. No new software to learn."
Alternative: "You send a list. We do the rest."
Section sub, new: "We run the whole sequence, and appointments land on
your calendar automatically. That's the entire process."
Steps, new:
1. Send us your CSV: "Export the leads quiet for three months or more. No
   integrations, no changes to your CRM."
2. We run the sequence: "A personalized email, then a friendly text. Leads
   who want a call say so, and our conversational AI assistant takes it
   from there."
3. Appointments hit your calendar: "On the call, the assistant confirms
   the lead is genuinely looking, with a sense of timeline and budget,
   then books during the call. Your booking link connects with one click."
4. Pay for results: "Billed per booked appointment, one invoice at
   campaign close. No-shows are replaced free, and a campaign that books
   nothing costs nothing."

### H6 Pricing
Tightens: the audit card loses its misplaced long bullet (the close-out
report bullet belongs to the Campaigns card, which already has it; the
duplication is deleted, not reworded). Retainer paragraph drops from 90
words to 55 and splits the quarterly-report idea into its own sentence.
Reflows: none. Two cards, retainer band, benchmark note.
Primary head (kept): "Structured so there's nothing to lose."
Alternative: "Free to start. Paid per appointment."
Section sub, new: "A free audit of your database first. Then you pay only
for appointments that land on your calendar."
Campaigns bullet 4, new: "Close-out report with the full numbers:
messages, conversations, appointments" (replaces the hyphen-as-dash
phrasing).
Retainer band, new copy: "Most teams wait until the pipeline runs dry to
look at old leads. A retainer watches your list year-round: campaigns
launch the moment a segment shows life, and a quarterly report shows what
the program actually produced. Retainer clients book at a discounted
per-appointment rate." No new numbers; the $50 / $500 detail stays in the
FAQ where it lives today.
Benchmark note: kept verbatim (500-lead, 10 to 30 conversations).

### H7 Founder band
Reflows: moves from after the contact form to before it. Rationale: the
contact form should be the last thing before the footer so the page ends
on the conversion moment; the founder story is credibility and belongs
upstream of the ask. This also repairs the band rhythm: FAQ on ivory,
founder on soft, contact on ivory, footer navy. Contact drops its soft
background accordingly.
Tightens: padding normalizes to the 72px section scale.
Rewords: "I founded Hayes Systems on one principle: honesty. That's why my
name and face are on it. No hollow promises, no costs hidden behind
confusion. If you have questions, email me directly."
Primary head (kept): "Hi, I'm Matt."
Alternative: "Why my name is on the door."

### H8 FAQ
Tightens: the wireframe shows the first six entries with tightened answers
plus a dashed placeholder row naming the rest, so rhythm is reviewable
without duplicating all fourteen. The refresh keeps all 14 entries (the
brief said 18; the live page has 14), answers tightened to the same
standard.
Evelyn stays, exactly once, in the off-script entry. Every number quoted
is from the sanctioned set.
Primary head (kept): "Questions agents always ask."
Alternative: "Asked before every first campaign."

### H9 Contact
Tightens: the commission field placeholder loses its embedded &mdash;
entity, an actual copy-rule violation on the live page. New placeholder:
"e.g. 12000, powers the value estimate in your audit".
Reflows: none. Form is static in the wireframe (submit shows a preview
notice instead of posting).
Primary head (kept): "Find out what your CRM is worth."
Alternative: "Two minutes. A straight answer."

## Page 2: how-it-works.html

Tightens:
- Title tag em-dash removed: "How It Works | Hayes Systems".
- "What you do" item 1 is 62 words with a booking-platform parenthetical
  doing half the work. Split: the step keeps its sentence; the plan
  details (solo free, teams need round-robin, GoHighLevel includes it)
  move to a small note line under the list.
- The "What you pay" card and cost table currently repeat each other.
  Card trims from four paragraphs to two (price line, no-show line); the
  table stays the single detailed source.
- h2 rhythm: top margin standardizes to 40px, matching the homepage
  section-head gap.

Reflows: none. The page's plain single-column structure is right for a
utility page; restructure would fight it.

Rewords (primary kept / alternative):
- H1 kept: "How it works, from your side of the table." Alt: "What you
  do, what we do, what it costs."
- "What you do" kept. Alt: "Your part takes one sitting."
- "What we do" kept. Alt: "Everything else is ours."
- "What you pay" kept. Alt: "One number, and it only moves when you win."
- "Stopping" becomes "Stop any time" (label to benefit). Alt: "One email
  ends it."
- "What we ask of your data" becomes "How your data is handled" (clearer,
  still plain). Alt: "Your list, used for one thing."
- "Already a client?" kept.

## Page 3: estimate.html

Tightens:
- Title tag em-dash removed: "Your Launch Estimate | Hayes Systems".
- The estimate card and "Where these numbers come from" both explain the
  band concept; the section keeps it, the card's small print trims to the
  billing sentence only.
- Table cells get explicit scope attributes; no visual change.
- Section spacing and type inherit the global scale; this page is already
  close, so touches are minimal by design. It is a noindex utility page
  reached from a private link; it should feel like the same hand drew it,
  nothing more.

Rewords (primary kept / alternative):
- H1 kept: "Your launch estimate." Alt: "What launching would cost you."
- "Where these numbers come from" kept. Alt: "The math behind the band."
- "What happens next" kept. Alt: "One form, then launch."

## Copy-rule audit of the current pages (findings)

1. index.html hero step 2 names Evelyn in lead-facing copy. Fixed in the
   wireframe and mandated by this spec for the page refresh.
2. index.html audit form placeholder contains an &mdash; entity. Fixed.
3. how-it-works.html and estimate.html title tags contain em-dashes.
   Fixed in spec for both pages.
4. FAQ count is 14 entries live, not 18 as the brief assumed. No action;
   noted so nobody hunts for four missing questions.
5. The live footer links row is a no-wrap flex with ten links and
   overflows horizontally at 375 (measured scrollWidth 1099). The
   wireframe fixes it with flex-wrap and a row gap; the page refresh
   should carry that fix.
6. No other em or en dashes in body copy across the three pages (grep
   verified during this pass; see QA).

## QA

Wireframe build: scripted transformation of site/index.html with 37
asserted replacements (exact-match counts), so tokens, SVG lockups, and
structure carry over exactly. Rerun: python3 site/preview/build_wireframe.py.

Checks run and passed:
- Em-dash grep: 0 occurrences of U+2014 and 0 of &mdash; in
  index-wireframe.html and SPEC.md.
- Copy rules: Evelyn appears only inside the existing off-script FAQ
  entry (build asserts containment); every number traces to the
  sanctioned set or to copy already on the live page.
- Overflow, measured in Chromium (scrollWidth vs innerWidth, plus
  element-level offender scan): 1440 clean, 375 clean, 390 clean.
  Two inherited live-site defects were fixed in the wireframe to get
  there: the no-wrap footer links row (1099px at 375) and the chat-card
  decorative glow pseudo-element (inset -50px, pushed scrollWidth to
  401). Both belong in the real page refresh.
- Renders: site/preview/shots/index-wireframe-{1440,375,390}-{full,fold,mid}.png.
- Vision review of the renders confirmed: gold preview banner, navy nav,
  tightened hero lede and chat card intact, navy stats band with gold
  numerals under the hero, founder band before the contact section,
  dashed FAQ placeholder row present, no clipped or overlapping text at
  either width.

The form is static in the wireframe (submit shows a preview notice); the
build script no-ops the fetch so no request leaves the page.
