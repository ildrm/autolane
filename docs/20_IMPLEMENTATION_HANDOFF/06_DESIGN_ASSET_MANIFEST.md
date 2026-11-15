# Design Asset Manifest

| Metadata | Value |
|---|---|
| ID / version | 20/06_DESIGN_ASSET_MANIFEST / 0.1 |
| Status | Proposed handoff; implementation not approved |
| Owner / reviewers | Documentation architect / product, operations, legal, finance, engineering, security and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Design Asset Manifest for future review and implementation planning. |

## Proposed assets and production ownership
This is a requirements manifest, **not an inventory of delivered or licensed files**. Brand, asset rights, exact names and final designs require approval.

| Asset family | Proposed source / deliverables | Owner and acceptance |
|---|---|---|
| Brand marks | Original wordmark, symbol, light/dark versions and clear-space rules | Brand lead; trademark search and legal clearance before use. |
| Design tokens | Named color, typography, spacing, elevation, focus, semantic and motion tokens | Design systems lead; validate contrast, themes and developer handoff. |
| UI library | Buttons, fields, cards, inspection states, tables, dialogs and status labels | Design + frontend; keyboard, accessible names, responsive and state coverage. |
| Photography | Original licensed vehicle exterior/interior/defect images, release and usage metadata | Photography lead; model/vehicle rights, color accuracy, responsive crops and alt text. |
| Icons / illustration | Original set in vector format with consistent stroke and semantic labels | Design lead; accessible meaning and optical sizing. |
| Motion | State transition specifications, source files, exports, durations, easing, reduced-motion alternatives | Motion lead; performance and accessibility review on target devices. |
| Optional 360/3D | Only after user-value case; optimized model/textures plus static images and textual inspection descriptions | Creative engineering; mobile, fallback, licensing and memory budget tests. |
| Legal / operational document templates | Approved locale-specific contract and report templates with version and hash | Legal and inspection leads; permissions and immutable revision policy. |

References: [creative direction](../06_VISUAL_DESIGN_SYSTEM/01_CREATIVE_DIRECTION.md), [tokens](../06_VISUAL_DESIGN_SYSTEM/03_DESIGN_TOKENS.md), [asset specifications](../07_ANIMATION_3D_AND_GRAPHICS/06_GRAPHIC_ASSET_SPECIFICATIONS.md), [motion accessibility](../07_ANIMATION_3D_AND_GRAPHICS/08_ANIMATION_ACCESSIBILITY.md). Final handoff must attach actual assets, source/export formats, rights, ownership, checksum, version, intended usage, size and review evidence.

## Revision 0.3 source of truth

The [current audit](../FINAL_COMPLETENESS_AUDIT.md), [policy baseline](../POLICY_BASELINE.md), [scenario acceptance mappings](../SCENARIO_TRACEABILITY.md) and [API/schema handoff](05_API_AND_SCHEMA_CONTRACTS.md) supersede earlier limited-coverage counts and validation status. Real stakeholder approval, provider evidence and runtime testing are still not claimed.
