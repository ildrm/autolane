# Typography

**ID:** 06/04_TYPOGRAPHY · **Version:** 0.1 · **Status:** PROPOSED; no trademark, asset or stakeholder approval · **Owner:** Design systems lead · **Reviewers:** Brand, accessibility, UX, frontend · **Updated:** 2026-11-15

## Type roles
Select a commercially cleared, English-capable sans with open apertures, distinct 0/O and 1/l, tabular numerals and 400–700 weights; family remains **DECISION REQUIRED** after font-license and performance review. System fallback: `system-ui, sans-serif`. Avoid synthetic bold/italic. Body is 16/24 px at 400; label 14/20 at 600; page title 32/40 at 700; public display 48/56, scaling down to 32/40 at compact widths; hero display max 64/72 on wide layouts. Use relative sizing so browser text settings are honored.

## Content and layout
Use tabular numerals for bid amount, balances, time and tables; currency code remains visible. Align monetary values consistently and show negative signs and precision defined by currency policy. Body line length target 45–75 characters; avoid justified text and all-caps paragraphs. Labels stay above controls and never disappear in favor of placeholders. No text should truncate legal conditions, amount or error; long names may wrap and compact tables can expose full accessible details. Do not express meaning through weight alone.

## Loading and acceptance
Preload only the critical subset where justified; use local fallback with measured metric-compatible sizing to reduce layout shift. Font files must be licensed for web distribution, versioned, subset appropriately and have a self-hosting or vendor privacy review. Test 200% text resize and 400% zoom, dyslexic-friendly distinction, numerals in auction and RTL not required for v1 but future localization must not depend on fixed widths. Detect overflow and clipping across minimum/maximum content lengths.
