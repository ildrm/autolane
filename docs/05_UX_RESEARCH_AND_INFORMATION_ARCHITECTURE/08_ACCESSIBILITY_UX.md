# Accessibility UX

**ID:** 05/08_ACCESSIBILITY_UX · **Version:** 0.1 · **Status:** PROPOSED, subject to research and stakeholder review · **Owner:** UX lead · **Reviewers:** Product, accessibility, operations, engineering, legal · **Updated:** 2026-11-15

## Standard and responsibility
Target [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/) on all public and authenticated flows; W3C's [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) guide widget behavior. This is a proposed acceptance requirement, not a claim of conformance. Accessibility specialist owns test evidence; product and engineering own remediation.

## Interaction requirements
Use native controls and landmarks first; one meaningful H1 per page, logical headings and a skip link. Associate labels, instructions, errors and required state programmatically. Maintain visible focus, logical order, no keyboard trap, and predictable return focus after dialogs. Never depend on color alone for status or errors. For normal text aim at least 4.5:1 and large text 3:1; non-text components and focus indicators require applicable contrast. Meet target-size, focus-not-obscured, consistent help and accessible authentication criteria of WCAG 2.2. Respect reduced motion; support text resize, 400% zoom and responsive reflow. Video needs captions and meaningful image/diagram alternatives.

## Critical context
A live auction must announce the user's accepted or rejected bid and meaningful outbid status politely without announcing every countdown tick. The authoritative close is text and timestamp, never animation alone. A modal offer decision has an accessible heading, explicit action text, cancel and focus return; no auto-acceptance. Inspection diagrams require a textual list of findings. Charts include an equivalent data table; maps include a location list. Form errors appear in a focused summary and adjacent to fields without erasing input.

## Test plan and acceptance
Automated checks supplement manual tests; run keyboard-only and screen-reader task tests on desktop and mobile, contrast and zoom checks, reduced-motion and high-contrast modes, speech-control labels, and an assessment involving disabled users. Test sign-in, seller booking, bid, offer decision, inspection correction and support. Log criterion, route, role, steps, actual/expected behavior, impact and retest evidence. No unresolved critical accessibility blocker may pass the UX gate; conformant experience is assessed against complete user journeys, not individual pages alone.
