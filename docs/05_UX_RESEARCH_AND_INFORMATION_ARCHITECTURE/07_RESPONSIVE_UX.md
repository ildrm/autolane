# Responsive UX

**ID:** 05/07_RESPONSIVE_UX · **Version:** 0.1 · **Status:** PROPOSED, subject to research and stakeholder review · **Owner:** UX lead · **Reviewers:** Product, accessibility, operations, engineering, legal · **Updated:** 2026-11-15

## Breakpoints and grid
Proposed viewport bands: compact 320–599 CSS px, medium 600–1023, wide 1024–1439, expanded ≥1440. Use 4/8/12-column grids respectively, side padding 16/24/32 px and max reading width 1280 px; reflow is content-driven, not device-specific. At compact widths stack cards and form sections; filters open a labeled drawer with Apply and Reset. At medium widths use two columns only when fields remain readable. At wide widths use a main area and contextual rail with explicit reading order; never put essential error feedback only in the rail.

## Functional behavior
Auction price, bid field and deadline stay visible together without covering the inspection and terms; a fixed action bar must reserve space and not obscure focused content. Operational tables retain semantic table structure and allow horizontal scrolling with visible affordance and keyboard access; narrow layouts may offer an equivalent labeled record list, not omit columns essential to decisions. Branch maps have an equivalent text list. Dialogs become full-height drawers when required; focus and escape behavior remain equivalent. Galleries use swipe as an additional affordance, with labeled previous/next buttons.

## Zoom, touch and input
At 320 CSS px and 400% browser zoom, reflow text without two-dimensional scrolling except for inherently two-dimensional content such as data tables. Meet WCAG 2.2 target-size requirements or documented exceptions; aim for 44×44 CSS px touch targets with spacing. Test portrait and landscape, large text, virtual keyboard, mouse, keyboard and touch. Do not rely on hover, drag, orientation or device motion for a required action.

## Acceptance
Test SCR-003, 005, 008, 017, 022 and 026 at 320, 375, 768, 1024 and 1440 widths with long English labels and delayed content; compare reading and focus order to the visual order, confirm every task remains possible, and ensure no clipped offer amount, currency, fee, button or error. Record findings with screenshot, viewport, browser and severity.
