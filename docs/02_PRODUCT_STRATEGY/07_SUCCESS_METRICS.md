# Success metrics

| Metadata | Value |
|---|---|
| Document ID | 02/07_SUCCESS_METRICS |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and documentation leadership |
| Reviewers | Operations, legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Success metrics; English-first automotive marketplace documentation |

Metrics are **PROPOSED**, not observed values or approved targets. Calculate in selected reporting time zone, record cohort age, source system, owner and policy version. Count each case once at its authoritative event/state.

| Metric | Numerator / denominator | Segment and caution | Owner |
|---|---|---|---|
| Eligible lead to close | Distinct eligible seller cases closed / distinct eligible seller cases in mature cohort | Branch, source, vehicle class; recent cohorts are incomplete. | Product |
| Auction offer coverage | Finalized auctions with ≥1 accepted qualifying bid / finalized auctions | Include zero-bid cases; compare by segment and duration policy. | Auction ops |
| Bidder participation | Distinct eligible dealer organizations with accepted bid per finalized auction | Report median/distribution and concentration, not only average. | Dealer success |
| Seller decision completion | Explicit accepted or rejected offer versions / offers presented | Distinguish expiry and pending; account for response window. | CRM |
| Booking utilization | Confirmed attended appointments / available eligible capacity | Account for closures and staff availability; do not overbook. | Branch lead |
| Inspection correction | Published reports with material corrected version / published reports | Lag and severity matter; audit sample rather than reward low reporting. | Inspection lead |
| Reconciled closure | Closed cases meeting approved evidence and no unresolved monetary discrepancy / all closed cases | Target of 100% is proposed control, not measured value. | Finance |
| Customer task completion | Participants completing defined task without moderator intervention / tested participants | Report task, sample, accessibility mix and confidence. | UX research |
| Contribution | Earned net revenue − attributable service and acquisition costs | Define accounting basis, refunds and cohort lag; exclude gross vehicle value. | Finance |

Set thresholds, minimum sample sizes, alerting, consent and review cadence before live use. Protect privacy; do not use raw customer identifiers in general dashboards. Verify deduplication, timezone boundaries, test-data exclusion and correction propagation.
