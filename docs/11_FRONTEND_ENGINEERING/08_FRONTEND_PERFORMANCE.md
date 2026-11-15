# Frontend Performance

| Metadata | Value |
|---|---|
| ID / version | 11/08_FRONTEND_PERFORMANCE / 0.3 |
| Status | Proposed, pending design and product review |
| Owner / reviewers | Frontend architect / design, accessibility, security, QA |
| Updated | 2026-11-15 |
| Scope | Frontend Performance, initial English LTR release. |

## Proposed budgets and measurement
Targets are **PROPOSED**, not observed service performance. On a representative mid-tier mobile device and agreed network profile: public LCP p75 ≤2.5 s, INP p75 ≤200 ms and CLS p75 ≤0.1 at the 75th percentile, segmented by page and region. Initial compressed JS and image budgets must be measured on selected stack before sign-off; use server rendering, route-level lazy loading, responsive images and restrained third-party scripts. Preload only critical fonts/images; prevent layout shifts by reserving dimensions.

Auction functionality takes priority over decorative graphics: live status and bid controls load without 3D; charts and heavy visuals defer until visible, and animations use transform/opacity where feasible. No 3D or motion asset blocks bid acknowledgement. Measure synthetic lab and consented real-user metrics with route, device class and release version, excluding personal data. Run performance regression checks and record baseline plus variance; isolate failures by network, origin latency and rendering. Targets are launch candidates requiring testing and approval, not guaranteed outcomes.

## Initial enforceable asset budgets

Proposed transfer budgets per first-load route: public HTML ≤80 KiB compressed, critical CSS ≤40 KiB, initial JavaScript ≤180 KiB, above-fold imagery ≤250 KiB and fonts ≤100 KiB; total critical transfer ≤650 KiB. Private dashboard initial JavaScript ≤250 KiB; auction route no 3D dependency and ≤200 KiB application JavaScript. These are starting budget decisions to validate against NFR targets, not claims about an existing build. Optional 3D/model assets load only after user intent and outside critical transfer; the motion asset budget is authoritative for that optional experience.

Measure home, sell form, listing results, listing detail, dealer auction and inspector checklist separately on a documented mid-tier Android device, mobile Safari and desktop baseline. Capture cold and warm navigation, first meaningful form interaction, hydration long tasks, image decode and stream burst behavior. Use at least five lab runs and record median plus worst case; field percentiles require a sufficient rolling sample and no substitution of lab scores for real-user results. A >10% bundle growth requires explicit owner review even if below ceiling; any LCP/INP/CLS release target breach blocks that route until repaired or a time-limited exception is approved. Disable optional graphics before sacrificing transaction responsiveness.
