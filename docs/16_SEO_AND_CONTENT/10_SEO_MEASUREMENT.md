# SEO measurement

**ID:** 16/10_SEO_MEASUREMENT · **Version:** 0.1 · **Status:** PROPOSED, subject to content, legal and engineering approval · **Owner:** Head of SEO · **Reviewers:** Content, product, privacy, engineering · **Updated:** 2026-11-15

## Measurement model
Use search-engine aggregate performance and crawl diagnostics, consent-permitted web analytics and authoritative transactional reporting. Do not join search queries to identifiable users; unavailable consent means report fewer observed conversions, not infer missing identities. Segment public landing family, device, geographic market where allowed and brand/nonbrand taxonomy; treat search console query groups as incomplete and potentially thresholded.

| Metric | Definition and cohort | Use and caveat |
|---|---|---|
| Organic clicks / impressions | Search platform counts by canonical landing page and reporting day. | Inspect search demand and page discoverability; engine definitions and sampling differ. |
| Organic CTR | Clicks ÷ impressions within identical query/page/device period; suppress zero denominator. | Investigate titles/intent, not a guaranteed causal effect. |
| Qualified lead conversion | Qualified seller leads with first eligible observed organic session ÷ observed organic landing sessions for cohort and attribution window. | Consent and identity coverage limit attribution; use authoritative lead qualification. |
| Booking completion | Confirmed bookings ÷ observed seller request starts in same attributed cohort. | Distinguish start cohort from booking-date counts and booking cancellations. |
| Dealer application completion | Submitted unique applications ÷ eligible organic dealer-landing sessions. | Approval is a separate downstream outcome. |
| Index coverage | Count of intended canonical URLs observed indexed ÷ intended indexable canonical inventory. | Search reports can lag or sample; do not treat as exact census. |
| Web Vitals | p75 LCP, INP and CLS per page family and device, consented real-user sample. | Compare targets in [technical SEO](02_TECHNICAL_SEO.md); no current value is asserted. |

Weekly check index/canonical anomalies, coverage drops, broken links, non-200 sitemap entries and performance regressions; monthly review landing quality, attribution coverage and qualified funnel outcomes. Define attribution window and consent posture with analytics/legal before launch; version metric changes. Flag small cohorts and missing data; do not infer causation without a controlled experiment.
