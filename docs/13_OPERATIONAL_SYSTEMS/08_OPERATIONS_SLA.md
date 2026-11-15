# Operations service levels

| Metadata | Value |
|---|---|
| Document ID | 13/08_OPERATIONS_SLA |
| Version / status | 0.1 / proposed; requires domain review |
| Owner | Operations Director |
| Reviewers | Operations, Product, Security, Legal, QA |
| Updated | 2026-11-15 |
| Scope | Operations service levels for the proposed marketplace; jurisdiction and transaction model remain open. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Proposed operating targets

Targets below are planning hypotheses, not current performance, guarantees or contractual commitments. Clock rules, coverage hours, holidays and exclusions require commercial and legal approval. Instrument UTC event times with branch timezone for business-hours reporting, and report data completeness beside each percentile.

| Service indicator | Proposed target / measurement | Owner and escalation |
|---|---|---|
| New lead response | 90% first human attempt within 1 business hour during staffed hours; denominator all eligible nonduplicate leads. | CRM lead; overdue queue every 15 minutes. |
| Appointment availability | 90% of eligible requests offered a slot within 3 branch working days; denominator requests where vehicle and branch coverage are valid. | Branch lead; review branch capacity daily. |
| Inspection completion | 90% of attended eligible inspections reach supervisor review within 2 branch hours; record excluded unsafe or incomplete cases separately. | Inspection lead; escalate blocked equipment immediately. |
| Reconciliation exception | 95% assigned to finance within 1 business hour; denominator newly detected discrepancies. | Finance lead; no automatic assertion of settled state. |
| Support first response | 90% within 1 business day, by priority and coverage window; safety and security route immediately to incident response. | Support lead; backlog age alert. |
| Delivery on time | 90% within customer-agreed window; denominator completed deliveries with a valid window, report failed deliveries separately. | Logistics lead; investigate missed windows. |

## Measurement and governance

A business-hours clock runs only inside the versioned branch/team calendar; after-hours cases start at next opening. Awaiting customer can pause resolution only under approved rules, with pause reason and duration reported. Do not pause first-response clock simply because a case was assigned. Calculate per-case durations and monthly proportions; publish sample size, missing timestamps, outliers and excluded cases. Revisions never rewrite event history.

## Acceptance and response

An overdue case appears in the owner's queue and triggers a bounded escalation; coverage gaps have an alternate owner. Reports flag missing timestamps instead of treating them as zero. Quarterly review validates whether targets are affordable and realistic; target breach triggers root-cause review, not automated compensation absent a contract.
