# Exception handling

| Metadata | Value |
|---|---|
| Document ID | 03/07_EXCEPTION_HANDLING |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Exception handling; English-first automotive marketplace documentation |

## Case contract
Any failed or ambiguous critical step produces an exception record containing case ID, object/version, category, severity, detection time, assigned team and owner, customer-safe status, next action, due time when approved, evidence links, attempts, audit and resolution. Do not copy raw sensitive identity or payment details into general alerts. Automated retries require idempotency; retry exhaustion must create a visible queue, not a silent drop.

| Class | Containment | Recovery owner and exit condition |
|---|---|---|
| Identity/authority mismatch | Block auction publication and transfer. | Branch/legal validate evidence or reject with appropriate notice; no automatic merging. |
| Inspection incompleteness/dispute | Mark affected item unknown and pause material downstream use. | Supervisor reviews evidence; publishes a corrected version or reasoned decision. |
| Auction processing inconsistency | Stop award or further unsafe actions, preserve accepted ledger. | Incident commander and auction/legal reconcile and follow published terms; notify impacted users. |
| Seller declines/expires | Do not create an accepted decision. | CRM closes attempt or seeks new consent for policy-approved next step. |
| Payment mismatch/default | Hold settlement/ordinary close, retain actual provider evidence. | Finance/legal reconcile or apply contracted remedy with authorized approval. |
| External provider outage | Show pending, retry safely, maintain queue. | Integration owner checks provider authoritative status before declaring complete. |
| Transfer or carrier dispute | Preserve custody, title and condition evidence separately. | Operations/legal/support determine next step and approved remedy. |
| Privacy/security incident | Restrict access and preserve relevant logs. | Security/privacy follow incident and legal-notification policy. |

## Escalation and communication
Severity reflects customer harm, financial exposure, active fraud and time sensitivity. Give each case one accountable owner; handoffs record acceptance. User notices explain what is known and next step, avoiding unsupported guarantees and internal technical details. Record manual actions and approvals so later reconciliation can distinguish them from system events. Release gates require scenario testing of retries, escalation, access and case closure; exact response times are subject to approved operational capacity.
