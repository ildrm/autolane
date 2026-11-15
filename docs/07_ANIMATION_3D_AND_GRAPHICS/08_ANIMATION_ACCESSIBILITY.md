# Animation accessibility

**ID:** 07/08_ANIMATION_ACCESSIBILITY · **Version:** 0.1 · **Status:** PROPOSED, subject to prototyping and review · **Owner:** Motion design director · **Reviewers:** UX, accessibility, performance, frontend, product · **Updated:** 2026-11-15

## User controls and presentation
Honor OS `prefers-reduced-motion` and any explicit in-product preference; the more restrictive setting wins. In reduced motion remove parallax, autoplay video, continuous shimmer, scene rotation and spatial transitions; show the same content and statuses immediately. User-initiated gallery navigation remains possible with no automatic movement. Respect system high contrast, zoom, font size and input settings. Do not use motion, hue, sound or a single visual position as the only carrier of information.

## Trigger, timing and notification
Interactions must work without animation and allow immediate interruption. Do not trap focus in an animating panel; dialogs establish focus and modality immediately and return focus on close. Provide pause, stop or hide controls where applicable for moving or auto-updating content and ensure text remains readable. Avoid flashing more than three times in any one second. Changes to user's own bid and outbid status use concise polite live announcements, but countdown ticks and every market price change are not announced continuously. Time limits and extension options require legal/business decisions and must satisfy applicable accessibility requirements.

## Test matrix and acceptance
Test with reduced-motion enabled before loading and toggled during animation; with keyboard, screen reader, magnification, high contrast, low-power mode and 400% zoom. Verify moving content is pausable where required, motion does not obscure focus, no auto-scroll or unexpected shift occurs, and 3D/media have equivalent still/text alternatives. Include users with vestibular sensitivity in research with consent and a stop option. Document each failed criterion, issue owner and retest; no critical motion accessibility issue passes release.
