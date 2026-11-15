# Motion and media performance budget

**ID:** 07/07_MOTION_PERFORMANCE_BUDGET · **Version:** 0.1 · **Status:** PROPOSED, subject to prototyping and review · **Owner:** Motion design director · **Reviewers:** UX, accessibility, performance, frontend, product · **Updated:** 2026-11-15

## Proposed targets and measurement
The values below are release hypotheses, not measured results. Web performance field targets: p75 mobile/desktop LCP ≤2.5s, INP ≤200ms, CLS ≤0.1, per [Web Vitals](https://web.dev/articles/vitals). For marketing and transaction pages, record route, device class, browser, network, percentile, sample window and consent. Lab tests use an agreed mid-tier mobile profile, CPU throttling, network throttling, cold and warm caches and 30 seconds of repeat interactions; retain trace and baseline.

| Item | Proposed budget | Gate and fallback |
|---|---|---|
| Per transition | 120–240ms; avoid layout-triggering animated properties. | If >50ms motion-attributable task or frequent dropped frames, simplify or disable. |
| Active animation | ≥55 fps target during 30 seconds on agreed lab device. | Disable nonessential effect on sustained degradation; preserve state updates. |
| Auction UI | Bid input must remain interactive while updates arrive; no animation backlog. | Coalesce visuals; authoritative bid and status processing cannot be delayed. |
| Above-fold visual | Mobile image target ≤150 KB per hero rendition and reserved aspect ratio. | Use lower-resolution crop, no autoplay video, retain usable text. |
| Optional viewer | ≤1.5 MB initial compressed mobile / ≤3 MB desktop, loaded only on request. | Static poster and gallery on data saver, unsupported device, context loss or excess budget. |
| Background work | Offscreen animation/video paused; no hidden continuous canvas loop. | Disable via visibility and intersection signals; resume only if user intent remains. |

Use transform/opacity where suitable, verify compositing rather than assuming it is free; limit simultaneous animated layers, decode images asynchronously where appropriate and avoid perpetual updates on low battery. Reduced-motion preference disables movement, but performance fallback also applies to users without that preference. Track asset bytes, decoded pixels, frame time, long tasks and layout shifts on representative mobile/desktop. If any proposal conflicts with actual accessibility or reliability needs, remove the effect; review budgets after field baseline.
