# Page transitions

**ID:** 07/04_PAGE_TRANSITIONS · **Version:** 0.1 · **Status:** PROPOSED, subject to prototyping and review · **Owner:** Motion design director · **Reviewers:** UX, accessibility, performance, frontend, product · **Updated:** 2026-11-15

## Transition policy
Marketing pages may fade between routes using 180ms at the standard curve; data-heavy dashboards navigate immediately with an optional 120ms content fade. Keep the header and identity context stable. Page content must be available independently of animation and focus must move to the new page heading after the content is rendered. Do not delay server requests, reserve operations or screen-reader announcements for transition completion.

## Transition cases
| Situation | Behavior | Failure / interruption |
|---|---|---|
| Public route change | Fade only the content container, keep layout dimensions. | If data fails show current error boundary and Retry; no blank overlay. |
| Multi-step form | Translate ≤8px and fade next panel, preserve all values. | Dirty form navigation requests confirmation; network save state is explicit. |
| Dealer auction detail | Immediate content and current status; optional fade for noncritical media. | Reconnect and fetch authoritative auction before enabling bid. |
| Staff case detail | Preserve list filters and scroll for Back, bring heading into focus. | Unauthorized or stale case shows safe denial/error, not previous case data. |
| Browser back / rapid click | Cancel prior animation and navigate directly to most recent target. | Never queue obsolete pages or restore an expired authorized response. |

Reduced motion removes translation, scroll-tied effects and route transitions; use immediate content without loss of focus. Native browser back/forward, deep links and disabled animation must work. Test at 320px, 200% zoom, reduced motion, keyboard and slow network, including a route failing while an animation is running. Acceptance: no content is inaccessible during transition; no stale status becomes authoritative; layout shift does not exceed the performance budget.
