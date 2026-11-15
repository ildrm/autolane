# Component library

**ID:** 06/07_COMPONENT_LIBRARY · **Version:** 0.1 · **Status:** PROPOSED; no trademark, asset or stakeholder approval · **Owner:** Design systems lead · **Reviewers:** Brand, accessibility, UX, frontend · **Updated:** 2026-11-15

## Component behavior catalog
All components use semantic tokens, a visible focus indicator, accessible name, disabled explanation when necessary, loading/error handling and keyboard use. Defaults below inherit [component states](08_COMPONENT_STATES.md) and [accessibility UX](../05_UX_RESEARCH_AND_INFORMATION_ARCHITECTURE/08_ACCESSIBILITY_UX.md). A role or UI state never replaces server authorization.

| Component | Variants and essential behavior | Keyboard, semantics and responsive notes |
|---|---|---|
| Button / icon button | Primary, secondary, quiet, destructive; loading prevents duplicate submission with explanatory status. | Native button; Enter/Space; icon-only needs name; min target 44px aim. |
| Input / search / amount | Text, numeric, password, search and currency with persistent label, helper and errors. | Native inputs; input mode is hint, not validation; no floating-only labels; show unit/code. |
| Combobox / vehicle selector | Make/model/variant hierarchy, unknown option where allowed. | APG combobox with labeled list, arrows/Enter/Escape; dependent value changes confirmed. |
| Select / dropdown | Native select for simple options; menu for action lists. | Select semantics vs menu semantics are distinct; focus returns after dismissal. |
| Date / time slot | Local calendar, timezone and server-issued available slots. | Typed date alternative; date picker keyboard navigable, unavailable slots explained. |
| Checkbox / radio | Independent consent vs one-of-many decisions; required and optional explicit. | Native controls, labels and fieldset/legend; no prechecked marketing consent. |
| Slider / price range | Numeric fields accompany sliders; preserve min ≤ max. | Arrow/Home/End control; announce units and values. |
| Vehicle card / comparison | Photo, accurate vehicle attributes, price and availability; comparison has labeled column headings. | Single clear link, no nested interactive targets; stack on narrow screens. |
| Auction card | Vehicle, amount/currency, server-derived status and deadline. | Link and watch control separately labeled; no animation-only outcome. |
| Status badge / inspection score | Explicit status and optional severity with text and icon. | No color-only signal; score methodology and report version visible. |
| Gallery | Main photo, thumbnails, previous/next, fullscreen optional. | Buttons accessible; swipe optional; alt describes actual image; reduced motion. |
| Stepper | Current, completed and upcoming labels; progress is informative. | Ordered list and current step; do not imply later step enabled. |
| Price / financing calculator | Exact amount, code, basis and approved disclosure; estimates labeled. | Inputs labeled; updates summarized politely; no implied financing approval. |
| Notice / toast | Inline success/warning/error, transient informational toast. | Persistent important errors; polite live region; no action only in disappearing toast. |
| Table / pagination | Row headings, sortable columns, filters and total basis. | Semantic table, sort state, labeled pages; scroll container keyboard accessible. |
| Tabs / accordion | Tabbed related views or disclosure for optional details. | APG patterns, visible focus; tab content state persists when sensible. |
| Dialog / drawer | Confirmation or task; danger separately worded. | Name, initial focus, focus containment, Escape where safe and return focus. |
| Skeleton / empty state | Reserved layout and explicit status; next useful action for empty. | Announce loading; do not create flashing animation; pause shimmer in reduced motion. |
| Chart / map | Accessible chart and underlying table; map plus address list. | Labels, units, keyboard and textual alternative; map never only route. |
| Breadcrumb / navbar / sidebar | Hierarchical navigation and role-scoped links. | Current page marked; keyboard traversal and mobile menu equivalent. |
| Command palette | Optional privileged tool for navigation and non-destructive actions only. | Explicit trigger and search label, focus handling; actions still authorize server-side. |

## Acceptance
Review variants, disabled/loading/error/success, keyboard and screen-reader behavior, long text, zoom, mobile and high contrast before release. A production component is complete only with approved design, behavior documentation, implementation and tests; none is implied by this document.
