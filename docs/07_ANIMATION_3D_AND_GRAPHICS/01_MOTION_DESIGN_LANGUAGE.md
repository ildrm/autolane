# Motion design language

**ID:** 07/01_MOTION_DESIGN_LANGUAGE · **Version:** 0.1 · **Status:** PROPOSED, subject to prototyping and review · **Owner:** Motion design director · **Reviewers:** UX, accessibility, performance, frontend, product · **Updated:** 2026-11-15

## Purpose and principles
For the recommended Quiet Precision concept, motion confirms relationships and system feedback, never masks uncertainty or creates a false sense of auction outcome. Use short opacity/transform effects that maintain context. Core content and actions work without JavaScript animation or 3D. Internal workspaces use only state-feedback motion; marketing may use opt-in narrative motion.

## Tokens and execution
`quick=120ms`, `standard=180ms`, `emphasis=240ms`, `narrative≤600ms`, delay default 0ms, standard easing `cubic-bezier(.2,0,0,1)`; all durations measured from event to settled state. Animate opacity and transform where supported; do not animate layout geometry of an active form or live price. Duration scales only for non-essential animation; time-sensitive business state is set by server response, never animation completion. New state supersedes and cancels an in-flight animation, retaining newest content; no queued old price transitions.

## Accessibility and control
Honor `prefers-reduced-motion`: disable translation, scale, parallax, autoplay and continuous shimmer; substitute an immediate visible state change or brief nonmoving opacity ≤120ms if user permits. Provide Pause/Stop for any nonessential movement meeting applicable WCAG requirements. No flashing content over three flashes per second and no essential outcome conveyed solely by movement or sound. Use labels and announcements per [accessibility UX](../05_UX_RESEARCH_AND_INFORMATION_ARCHITECTURE/08_ACCESSIBILITY_UX.md); countdown ticks are not announced each second. Do not change focus because of an animation, and user input interrupts animation immediately.

## Acceptance
At 320px and desktop, low-power device and reduced-motion mode, every workflow remains complete with the same outcome. Inspect repeated actions, tab background/foreground, disconnected network, browser zoom and screen-reader announcements. Performance budgets and per-interaction parameters are in the adjacent inventory and performance document. Motion is a proposal awaiting design, engineering and accessibility review.
