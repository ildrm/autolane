# Design-to-development handoff

**ID:** 06/10_DESIGN_TO_DEV_HANDOFF · **Version:** 0.1 · **Status:** PROPOSED; no trademark, asset or stakeholder approval · **Owner:** Design systems lead · **Reviewers:** Brand, accessibility, UX, frontend · **Updated:** 2026-11-15

## Deliverable contract
Each production-ready screen frame should contain screen ID and route from [inventory](../05_UX_RESEARCH_AND_INFORMATION_ARCHITECTURE/04_SCREEN_INVENTORY.md), owner, version, applicable roles, breakpoints, component variants, copy, token bindings, layout constraints, interactive prototype and linked state matrix. Document loading, empty, permission denied, stale, validation error, partial failure and confirmed-success states. Include an accessible reading/focus order and data prerequisites; describe any unresolved legal or financial policy without inventing content.

## Asset and version practice
Use Figma-compatible `category/role/state` variable names and `Component / variant / state` component naming. Link original or licensed source, crop, alt text, resolution, expiration and rights to each image; annotate imagery that is illustrative rather than inspection evidence. Provide SVG icons with semantic names and test high contrast. Document font license, subset, fallback and metrics. Designers version accepted components; engineers report deviations with screenshots and screen ID. Changes to an approved component require design, frontend and accessibility review, release notes and migration guidance.

## Acceptance and handoff gate
For each screen validate interactions with design and product, keyboard semantics with accessibility, actual source-of-truth states with backend, permission boundaries with security, and failure scenarios with QA. Capture visual snapshots at compact, medium and wide widths, 200% zoom, reduced motion and dark mode if supported. Explicitly identify missing assets, policies or copy and assign owners. Delivery of this specification is not a finished Figma file, validated design, implementation or stakeholder sign-off.
