# 3D automotive experiences and alternatives

**ID:** 07/05_3D_AUTOMOTIVE_EXPERIENCES · **Version:** 0.1 · **Status:** PROPOSED, subject to prototyping and review · **Owner:** Motion design director · **Reviewers:** UX, accessibility, performance, frontend, product · **Updated:** 2026-11-15

## Product-value decision
3D is a phase-4 experiment, not an MVP dependency or evidence of a vehicle's true condition. Approve only when a usability study demonstrates improved understanding over an accurate photographic gallery without reducing speed, access or conversion. Inspection, auction and transaction workflows must work entirely with a gallery and textual inspection list.

| Experience | Use case and value | Preferred implementation / alternative | Risks and gate |
|---|---|---|---|
| 360° turntable | Browse vehicle exterior consistently. | Progressive 24–36-frame image sequence on explicit interaction; static photo gallery fallback. | Images must represent actual vehicle, accurate lighting and version; show capture date. |
| Interactive 3D viewer | Optional representative model for explanatory discovery. | On-demand glTF/GLB; fallback still image and labeled text; clearly distinguish representative from actual vehicle. | 3D model must not imply verified condition or a real defect location. |
| Inspection body diagram | Navigate documented defects. | 2D numbered SVG or equivalent list linking to report findings/photos. | Color is supplementary; text list and keyboard access mandatory. |
| Part highlights/exploded view | Teach what a finding means. | Editorial illustration with labeled parts and text; not diagnostic proof. | Accuracy reviewed by inspector; avoid claiming unobserved damage. |
| Gallery storytelling | Explain service or showcase verified imagery. | Optimized photo/video with captions, poster and no autoplay sound. | Mobile data use, licensing, privacy and performance. |
| Animated auction visuals | Explain how bidding works on educational pages. | Simple visual sequence with text transcript; no animation required for live auction. | Avoid conflating examples with actual contract or time. |

## Interaction and budgets
Viewer starts from a static poster; explicit “Open 360° view” loads only on consent and capability. Arrow keys and labeled rotate buttons change views; pointer drag is optional. Hotspots are focusable buttons with accessible name and list equivalent, and remain anchored to documented evidence, not decorative estimates. Offer a close control, no automatic camera movement and stable focus. **PROPOSED budgets:** poster ≤150 KB at mobile rendition; initial interactive payload ≤1.5 MB compressed on mobile, ≤3 MB desktop; textures max 2048px desktop/1024px mobile, cap device-pixel ratio at 1.5; graceful fallback on memory pressure/context loss and respect save-data. Verify measured device/network performance; lower limits if needed.

## Production and acceptance
Capture consistent exposure, focal length, fixed pivot and sequence; mask identifiers only according to policy. Preserve original evidence and transformations. Review image rights, defect fidelity, accessibility, reduced motion and low-power devices. Release only if a user can discover, inspect and make every critical decision without viewer, while viewer does not introduce inaccurate or missing damage claims.
