# Operations panels

| Metadata | Value |
|---|---|
| Document ID | 04/08_OPERATIONS_PANELS |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Operations panels; English-first automotive marketplace documentation |

## Shared operational workspace
| Panel | Primary actions and data | Guard, failure and audit |
|---|---|---|
| Branch | Calendar, staff and capacity; appointment check-in, cancellation and queue. | Branch scope; atomic booking; approved override requires reason. Closure triggers rescheduling queue. |
| Inspection | Assigned checklist, vehicle identity, photos, unknown findings and report history. | Inspector submits; supervisor reviews and publishes; corrections create versions and material issues hold downstream workflow. |
| Valuation | Comparable records, condition, range, confidence, data freshness and analyst explanation. | Insufficient data abstains; override records old/new value, reason and reviewer when required. |
| Auction operations | Prepare eligible auction, review terms/report, monitor state, investigate incidents and close result. | No direct modification of accepted bids; pause/cancel and eligibility changes follow approved policy and independent authorization. |
| CRM | Assigned leads, consent, contact attempts, appointment and seller follow-up. | Only authorized purpose, marketing opt-out respected, duplicate flagged for review rather than auto-merged. |
| Support | Cases, evidence requests, ownership, next action and escalation. | Minimize sensitive data; support cannot mark payment reconciled or override title. |
| Inventory | Vehicle records, public eligibility and consumer publication. | Separate private auction and consumer visibility; publication requires approved report and content. |

## Shared screen states and control
Every work queue shows priority, age, assignee, filters and next action, plus empty, loading, stale, access denied and recoverable error states. Actions show effects and required reasons before confirmation; asynchronous outcomes remain pending until authoritative completion. Reassignment and privileged overrides are auditable. Keyboard and touch interactions must work for branch devices. Operational UAT covers absence, competing appointments, evidence dispute, auction outage and handoff; metrics and SLA thresholds require approved capacity.
