# JUDGE BASELINE — captured from LIVE site (main @ 0462aef + badb7e5 brief-only)
# Card: t_9cbedb2d (Judge). Written BEFORE previews existed. All values verified in-browser
# (Chromium via browser_exec, file:// URLs) on 2026-09-12 ~19:05 EDT.

## 1. Live state (git)
- site repo on branch main, HEAD = badb7e5 (preview-BRIEF.md only; +74 lines, 1 file vs 0462aef)
- 0462aef = last commit before the brief = the live site baseline for theme comparison
- working tree clean

## 2. Theme tokens (identical in index.html and how-it-works.html; estimate.html subset)
--navy #02101F | --navy-lift #071526 (not in estimate) | --navy-card #0B1C30
--ivory #EDE8DD | --soft #F4F1EA | --cream #FCFAF4 (estimate only)
--gold #D9A441 | --gold-soft rgba(217,164,65,.14)
--ink-on-light #0A1B2E | --gold-ink #7D5C15
--serif 'Cormorant Garamond',Georgia,serif | --sans Montserrat...
Nav element bg (index): rgb(18,31,44) solid  (literal, not a token — #121F2C)

## 3. Computed colors, LIVE index.html @1440
nav rgb(18,31,44) | hero/ivory bg rgb(237,232,221) ink rgb(10,27,46)
problem+pricing+contact sections bg rgb(244,241,234) (soft)
how/faq/founder sections transparent (ivory body shows through)
footer rgb(2,16,31) (navy)
hero btn gold rgb(217,164,65) / navy text rgb(2,16,31)
h1 Cormorant Garamond 600 rgb(10,27,46); body Montserrat

## 4. Fonts (file:// load OK on live pages)
Cormorant Garamond 500,600; Montserrat 300,400,500,600,700 — all status=loaded
CHECK IN PREVIEW: preview/ is one level deeper → font src must become ../fonts/...
@matt.jpg?v=3 resolves on live; only image on index.

## 5. Copy-rule baseline (LIVE)
- index.html em-dash count: 0
- how-it-works.html: 1 (title "How It Works — Hayes Systems")
- estimate.html: 1 (title "Your Launch Estimate — Hayes Systems")
- Banned words (revolutionary/game-changing/unleash/cutting-edge/disrupt): 0 in all three
- "small" self-reference: 0
- Timeline promises (in N days/weeks, results in): 0
- Evelyn: TWO live occurrences in index.html —
    L301 step-2 copy "Evelyn, our conversational AI assistant" (LEAD-FACING — violates
    brief if kept in preview; preview must say "our conversational AI assistant" only)
    L362 FAQ "What stops the AI from going off script?" (SANCTIONED — she's named only there)
- Retell AI mention in FAQ body (not hero). Hero meta description: "email, SMS, and opt-in
  AI voice outreach" — no "blunt AI" anywhere.

## 6. Sanctioned numbers (brief) + where they live on live index
2% (L66 meta/og, L92?) — conversion
$60 — L331 pricing card, L374 FAQ retainer ("$50 instead of $60" — the $50 IS sanctioned,
      appears in retainer FAQ; estimate.html computes $60 arithmetic in script)
90 day — L273 stats band ("90 days+")
April–June / ~31% January trough — L372 seasonality FAQ (worded "slows about a third",
      "jumps about a third" — the ~31% expressed as a third; no literal "31%" string on live)
$9K commission framing — NOT on live index (form label only); brief allows "$9K-ish framing"
Retainer: $500/mo start, $50/appointment — live FAQ copy.
Pre-existing stats band claims (5+, 70%, 90 days+) — not in sanctioned set; they were on the
      live page before the brief; brief rule is "no invented numbers / every claim matches
      the real workflow". 5+/70% are industry claims already shipped live — previews should
      not ADD new unsanctioned numbers; flag if new ones appear.

## 7. Readability/overflow baseline (LIVE index @375 and @1440)
- 375px: HORIZONTAL OVERFLOW (scrollWidth 1071 > 375) caused by .footer-links row not
  wrapping (links L24→R1071). Preview brief says 375 must hold — preview must fix or the
  defect carries into preview → FAIL item 4.
- Paragraphs >5 rendered lines @1440: many (FAQ entries 6–15 lines; step copy 6–11; hero
  lede 7). Brief's own DoD says "no wall-of-text over ~4 lines"; judge card says >5 = fail.
  Live is far over; previews expected to improve. Judge on preview values, not live's.

## 8. estimate.html mechanics
- Numbers filled by querystring (?w=&appts=lo-hi); cost = appts × $60 (low & high) in script.
- Tables/card layout; .btn Continue → onboard.html (relative link — preview in preview/ must
  keep working navigation or at least not break: judge notes link targets).
- Title em-dash must be fixed in preview.

## 9. Build's playwright constraint
Task names /home/mrh/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome — exists+exec.
Python playwright module NOT importable from /usr/bin/python3 nor hermes venv; no node
playwright in hermes node_modules. Build must use CDP directly (mine does) or install.

## 10. Observed live oddities (context, not preview-blocking)
- <title> of all three pages starts with "🐴 " emoji. Outside copy rules; note only.
- index nav bg is a literal (rgb(18,31,44)) not a token — preview may inherit; compare as-is.
