# BRIEF: Hayes Systems Website Visual Overhaul — PREVIEW ONLY

## THE ONE HARD RULE
**Nothing goes live.** Work happens on branch `overhaul-preview` in the
site repo (or working-tree copies named `*-preview.html` if branching is
easier said than done). The live `main` branch and the deployed site must
remain untouched. Matt reviews the preview; only HE decides what merges.

## What this is
A visual overhaul of the public marketing site (site/ in this repo):
index.html (homepage), how-it-works.html, estimate.html. Secondary pages
(compliance, privacy, cancellation, clients, onboard, unsubscribe) get only
typography/spacing consistency touches, no restructure.

## Goals (Matt's words)
- Improve **readability** — the pages are dense; density is fine, clutter
  and inconsistent rhythm are not
- Improve **layout** — clearer hierarchy, better section flow, stronger
  visual pacing between sections
- Improve **wording** — "more in line with marketing standards but not
  overly markety." Confident and plain beats hype. The existing voice is
  right; tighten the execution.
- **Keep the overall theme the same** — navy/gold on warm ivory, the serif/
  sans pairing, the pit-wall-adjacent typography character. This is a
  refresh, not a redesign.

## Hard copy rules (from the site's standing conventions)
- Zero em-dashes in any public copy
- No timeline promises ("results in two weeks"), no invented numbers
- Every claim must match the real workflow exactly
- Never call the business small; no "blunt AI" in hero copy
- Person name (Evelyn) does NOT appear in lead-facing copy — "our
  conversational AI assistant" only (she's named only on the FAQ entry
  about going off-script, which already exists and stays)
- Numbers only from the sanctioned set: 2% conversion, $60/appointment,
  $9K-ish commission baseline framing, 90-day bar, April–June peak / ~31%
  January trough (already in the FAQ)
- Tone: friendly-professional, a person helping a peer. Facts only, no
  reassurance filler.

## Current state reference (read these first)
- site/index.html — homepage: hero, stats band, problem section, how-it-
  works 4 steps, pricing cards, founder band, retainer section, FAQ (18
  entries), contact form, footer-legal
- site/how-it-works.html — process page
- site/estimate.html — post-audit estimate page
- The brand tokens live in the CSS custom properties at the top of each
  file (--navy, --gold, --ivory, etc.) — keep them.

## Deliverables
1. index-preview.html, how-it-works-preview.html, estimate-preview.html
   (in site/ or a site/preview/ subfolder) — the overhauled pages
2. Screenshots: each page at 1440 and 375, above-the-fold + one mid-page
   scroll, into site/preview/shots/
3. A NOTES.md (in the same preview folder): section-by-section what changed
   and why, one line each — so Matt can review changes against intent
   without diffing HTML

## Definition of done (per page)
- [ ] Readability pass: line-lengths sane (~70ch max for body), section
      rhythm consistent, no wall-of-text paragraphs over ~4 lines
- [ ] Layout pass: visual hierarchy obvious in 2 seconds (scan test),
      consistent vertical spacing scale, CTA placement follows the page's
      persuasion arc
- [ ] Wording pass: every heading earns its line (benefit or fact, not
      label); no sentence that a competitor couldn't also say stays
      unearned; marketing-standard clarity without hype words
      (revolutionary/game-changing/unleash/cutting-edge banned)
- [ ] Theme preserved: same palette, same font pairing, same overall
      character — side-by-side should read as "sharper," not "different"
- [ ] Zero copy-rule violations (em-dash grep, claims audit)
- [ ] Mobile 375 holds (no overflow), desktop 1440 clean
- [ ] Live site untouched: `git -C site status` clean, main branch HEAD
      unchanged
