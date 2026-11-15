# Animation inventory

**ID:** 07/02_ANIMATION_INVENTORY · **Version:** 0.1 · **Status:** PROPOSED, subject to prototyping and review · **Owner:** Motion design director · **Reviewers:** UX, accessibility, performance, frontend, product · **Updated:** 2026-11-15

## Timing and fallback rules
All animations have zero delay except documented narrative sequencing; easing is `cubic-bezier(.2,0,0,1)`. New input cancels previous motion and leaves the latest server-confirmed state. Reduced motion uses the final state immediately, except a nonmoving opacity fade up to 120ms if allowed. Mobile uses the same or shorter duration, reduced distances and no autonomous parallax. These are proposals to prototype, not measured results.

| ID / interaction | Trigger; from → to | Duration; interrupt / accessible result |
|---|---|---|
| MOT-01 Page transition | Successful navigation; old opacity 1→0, new 0→1. | 180ms; abort on next navigation; focus new heading, no loading delay. |
| MOT-02 Navigation drawer | Menu activation; panel translate X −12px→0 and opacity 0→1. | 180ms; close reverses from current frame, restore focus. |
| MOT-03 Modal | Dialog opens; backdrop 0→1 opacity, panel translate Y 8px→0. | 180ms; Escape cancels where safe; focus managed immediately. |
| MOT-04 Card interaction | Pointer hover or focus; border/elevation 0→1. | 120ms; never move hit target; focus remains visible. |
| MOT-05 Filters | Server-confirmed results arrive; new region opacity .8→1. | 120ms; cancel previous, show result count text; no layout jumps. |
| MOT-06 Multi-step form | Next accepted; content opacity 0→1, X 8px→0. | 180ms; preserve input, focus step heading; back reverses meaningfully. |
| MOT-07 Validation | Error appears; border/text opacity 0→1 without shaking. | 120ms; focus error summary, no motion required for meaning. |
| MOT-08 Form completion | Confirmed server result; check icon scale .96→1 + opacity 0→1. | 180ms; success text first, no completion before response. |
| MOT-09 Gallery | Explicit next/previous; image opacity .85→1. | 180ms; skip intermediate frames on repeated click; buttons remain operable. |
| MOT-10 Comparison | Add/remove vehicle; opacity 0→1 without moving data columns until layout settled. | 180ms; announce changed comparison count. |
| MOT-11 Price update | New authoritative price; highlight background alpha 0→.12→0. | 240ms; text changes immediately; coalesce updates; not a bid acknowledgement. |
| MOT-12 Auction countdown | User sees server-adjusted timer; seconds update as text. | 0ms; no pulsing/flashing, no per-second live announcement. |
| MOT-13 Bid result | Server accepts/rejects; feedback outline opacity 0→1. | 180ms; message announced once; timeout shows checking, not failure/success. |
| MOT-14 Auction close | Confirmed close; status swaps instantly, optional static divider fade. | 180ms; status includes outcome; never select winner locally. |
| MOT-15 Transaction milestone | Confirmed event; status icon opacity 0→1. | 180ms; show precise stage, not generic “completed.” |
| MOT-16 Dashboard refresh | Authorized newer data; timestamp updates, subtle refresh glyph rotation 0→90°. | 120ms; no endless loop; stale data labeled. |
| MOT-17 Chart | On initial user-requested view; line opacity 0→1. | 240ms; equivalent table available immediately, stop on interaction. |
| MOT-18 Notification | Insert message opacity 0→1, translate Y 4px→0. | 180ms; persistent critical messages and explicit dismiss. |
| MOT-19 Loading | Reserved skeleton optional opacity .7→1→.7. | 1200ms cycle, pause and offer static fallback; no infinite animation under reduced motion. |
| MOT-20 Scroll storytelling | User scrolls within a marketing section; small opacity change, no scroll hijack. | Max 600ms; stop outside viewport; content exists without animation. |

## Measurement and signoff
On a representative mid-tier device, sample frame times during 30 seconds of auction updates and gallery interaction; target ≥55 fps during active nonessential animations and no long task >50ms attributable to motion. These are proposed lab targets; security/auction correctness is unaffected by dropped frames. Test CPU throttling, background tab, rapid clicking, focus retention, motion preference and text-only fallback. Any failed measurement disables or simplifies that effect before launch.
