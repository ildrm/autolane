# Layout and spacing

**ID:** 06/06_LAYOUT_AND_SPACING · **Version:** 0.1 · **Status:** PROPOSED; no trademark, asset or stakeholder approval · **Owner:** Design systems lead · **Reviewers:** Brand, accessibility, UX, frontend · **Updated:** 2026-11-15

## Grid and composition
Use a 4px base scale and the token values in [design tokens](03_DESIGN_TOKENS.md). Compact pages use 4 columns, 16px margin and 12px gutters; medium 8 columns, 24px margin and 16px gutters; wide 12 columns, 32px margin and 24px gutters, max content 1280px centered. Main reading content caps around 72 characters; a side rail may hold contextual help and status, not unique critical details.

## Page families
Public landing: hero, primary action, factual process steps, trust evidence and supporting content; show real service constraints. Seller and dealer tasks: progress/context, one primary work area, clear action group, help; keep auction amount, bid control and current state together. Operations: heading and scope, filters, table or queue, detail panel; support density while retaining 40px controls and readable 14px minimum body. Two-column forms collapse to one column without changing reading order. Separate destructive controls from positive actions and preserve space around focus rings.

## Adaptation and acceptance
At 320px reflow without clipped text; long currency amounts wrap or expand containers without changing value. At 200% text resize there must be no overlapping fixed-height control. Test with a missing image, 10-line error, 3-digit years, long branch name and maximum permitted monetary amount. Sticky regions require dedicated layout space and must not obscure content or keyboard focus. Images reserve aspect ratio; animations do not shift surrounding layout.
