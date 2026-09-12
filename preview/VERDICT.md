# VERDICT — t_9cbedb2d (Judge) — 2026-09-12 ~19:45 EDT

Independent verification of build t_5982d6b9 against site/preview-BRIEF.md.
All checks run fresh by the judge (git, grep, md5, in-browser DOM via CDP).
Rerunnable judge script: preview/judge-claims-audit.py.

## 1. LIVE UNTOUCHED — PASS
- `git -C site status --porcelain` → `?? preview/` only (untracked).
- HEAD = badb7e5; `git diff 0462aef..HEAD` = preview-BRIEF.md +74 lines, nothing else.
- md5 live files vs `git show 0462aef:` — index 2b8dcf2f…, how-it-works 25745a8f…,
  estimate 94b07873… all byte-identical.

## 2. COPY RULES — PASS
- Em/en dashes: 0 in all three files (raw + entity grep); 0 in rendered DOM
  (innerText scanned for U+2014/U+2013 in-browser). Titles now use "|".
- Banned words (revolutionary/game-changing/unleash/cutting-edge/disrupt): 0.
- "blunt": 0. Small-business self-reference: 0. Timeline promises: 0.
- Evelyn: exactly 1 occurrence, inside the sanctioned off-script FAQ
  <details> (L368). Step-2 lead-facing copy now "our conversational AI
  assistant" (verified in rendered text).
- Claims audit: every number in all three previews traced to (a) the
  sanctioned set ($60/$50/$500, 90 days+, April-June "about a third") or
  (b) copy already shipping verbatim on live index ($20-60, 1-2, 5+, 70%,
  9 Sides NAR, 10 to 30, $12-16, 14 days, 250/500/1,000/2,500 form bands).
  No new numbers invented. Estimate math verified live in browser:
  ?w=250&appts=2-4 → $120/$240 = 2x60 / 4x60. The unsanctioned
  "jumps about a third in a single month" was dropped (disclosed in NOTES).
- Advisory A: how-it-works-preview L60 uses a spaced hyphen as a dash
  ("your entire export - the full list, not a sample"). Not an em-dash,
  no rule broken; reads as a dash substitute. index had the same pattern
  reworded away; this one survived.

## 3. THEME PRESERVED — PASS
- :root token block: all 11 tokens byte-identical to live (--navy #02101F,
  --gold #D9A441, --ivory #EDE8DD, --soft, --navy-lift, --navy-card,
  --gold-soft, --ink-on-light, --gold-ink, --serif, --sans).
- Computed colors sampled hero/nav/footer/buttons/h1/body: all equal to
  live EXCEPT nav bg: live literal rgb(18,31,44) → preview var(--navy)
  rgb(2,16,31). Disclosed in NOTES as token consolidation; the live value
  was the off-token element. Defensible, but it is the one visible color
  delta vs live — Matt should glance at the nav strip.
- Fonts ACTUALLY load in preview/ (document.fonts: Cormorant Garamond
  500/600, Montserrat 400/500/600/700 all status=loaded; h1 computed
  family = Cormorant Garamond). No fallback.
- how-it-works/estimate have no nav/footer on live either — parity holds.

## 4. RENDERS — PASS
- Overflow at 1440: 0px (all three). At 375: 0px (all three).
  Live index baseline was +724px at 375 — fixed in preview.
- Screenshots: 28 files in preview/shots/ (above-fold + mid at 1440+375
  for all three pages, plus founder band, wireframe, and live baselines).
  All preview shots (19:33+) postdate final HTML edits (19:29-19:33).
- Programmatic defect sweep at 1440 + 375: 0 broken images, 0 off-page
  elements, 0 clipped text blocks, 0 unintended sibling asymmetry
  (hero-grid is an intentional 2-col; cta-grid columns equal 508px with
  align-items:start).
- Verification gap disclosed: judge vision tool (zai vision) returned
  provider 400 "Unknown Model" — screenshots could not be eyeballed.
  Compensated with DOM geometry, clipping, symmetry, computed-color, and
  font-load probes. A 30-second human glance at shots/ before merge is
  recommended.

## 5. READABILITY — PASS (with advisory)
- 1440: 0 paragraphs/list items over 5 rendered lines on all three pages
  (measured via Range client-rects: max 5 / 4 / 3). Live baseline was
  6-15 line walls.
- Measure at 1440: everything ≤70ch except one 77ch paragraph and the
  footer-legal line (101ch, single line). Brief says ~70ch for body;
  footer legal is conventionally exempt. Advisory B.
- 375: 20 paragraphs render 6-12 lines, but every one ≤71 words (worst is
  the footer-legal line; content paragraphs ≤53 words) — no wall of text
  by word count. NOTES discloses this honestly: a 331px measure wraps even
  the 32-word lede to 7 lines. The 5-line bar is met at 1440; 375 exceeds
  by line count only, bounded by word count. Advisory C — acceptable.

## 6. NOTES.md — PASS
- Exists in preview/, section-by-section for all three pages, one line per
  change with why. Honest disclosures (375 caveat, dropped unsanctioned
  figure, nav consolidation, footer overflow fix). QA evidence section
  with rerunnable scripts; verify.py rerun by judge → all PASS.
- Nit: NOTES says hero lede "56 to 37 words"; measured 32 words (within
  the ≤37 SPEC target, so tighter than claimed — direction is fine).

## NOTES FOR MATT (non-blocking)
1. Advisory A: hyphen-as-dash in how-it-works L60.
2. Advisory B: footer-legal 101ch / one 77ch paragraph vs ~70ch bar.
3. Advisory C: 375 line counts (word-bounded, disclosed).
4. Nav strip is one token-step darker navy than live (disclosed consolidation).
5. Secondary pages (compliance/privacy/etc.) got NO preview copies —
   preview links resolve to the live pages via symlinks. The brief's
   deliverables list only the three main pages, so this matches scope,
   but the "secondary pages get typography touches" line was not executed.
6. Title emoji (🐴) retained from live on all pages — pre-existing.

## OVERALL: PASS
All six audit items pass on independent evidence. No copy-rule violations,
no theme drift beyond the one disclosed nav consolidation, live site
byte-untouched, renders clean at both widths, readability targets met at
1440. Advisories above are polish-level, none blocking.
