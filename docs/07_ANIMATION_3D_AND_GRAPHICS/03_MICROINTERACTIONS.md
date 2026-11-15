# Microinteractions

**ID:** 07/03_MICROINTERACTIONS · **Version:** 0.1 · **Status:** PROPOSED, subject to prototyping and review · **Owner:** Motion design director · **Reviewers:** UX, accessibility, performance, frontend, product · **Updated:** 2026-11-15

## State-driven patterns
| Action | Visual feedback | Actual event / interruption | Accessible and reduced motion |
|---|---|---|---|
| Select time slot | Radio outline changes over 120ms. | Selection is provisional until booking response; newer slot selection cancels the visual transition. | Radio announced selected; final state instant in reduced motion. |
| Save draft | Status changes “Saving” → “Saved” only on acknowledgment. | Failure preserves local values where secure and allowed; user can retry. | Polite status, no repeated announcements. |
| Submit bid | Button reads “Submitting…” while request resolves; no optimistic checkmark. | Server acceptance/rejection controls outcome; timeout becomes “Checking your bid.” | Announce result once; button state and focus preserved; no motion required. |
| Current price changes | Brief background highlight, number swaps immediately. | Newest version wins; ignore stale visual messages, refresh authoritative state if sequence gaps. | Show textual price and currency; do not continuously announce all price changes. |
| Accept/reject offer | Confirmation dialog names amount, action and consequences from approved terms. | Cancel closes; confirm sends one request, uncertain result reconciled. | Focus trapped only while modal open and restored; immediate state when motion reduced. |
| Validation error | Border plus text appears with no shake. | Correction clears only affected error; submitted values persist. | Focus linked summary; do not rely on color. |
| Photo upload | Per-file progress with status and cancel. | Upload success is not verification; failed scan displays actionable error. | Progress label and textual status; static under reduced motion. |
| Alert | Inline message or dismissible notice appears without layout surprise. | Critical alert persists; dismissed transient toast does not hide required action. | Announce only meaningful change, no time-dependent interaction required. |

## Acceptance
Every effect has a source event, final state and interruption rule; no animation may delay bidding controls or claim completion. Test keyboard, touch, slow and offline networks, rapid repeated inputs and assistive technology. Motion implementation is optional enhancement; all facts remain visible when disabled.
