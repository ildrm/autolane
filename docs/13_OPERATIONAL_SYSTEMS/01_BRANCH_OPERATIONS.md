# Branch operations

| Metadata | Value |
|---|---|
| Document ID | 13/01_BRANCH_OPERATIONS |
| Version / status | 0.1 / proposed; requires domain review |
| Owner | Branch Operations Lead |
| Reviewers | Operations, Product, Security, Legal, QA |
| Updated | 2026-11-15 |
| Scope | Branch operations for the proposed marketplace; jurisdiction and transaction model remain open. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Workflow and controls

| Step | Actor and information | Guard, result and exception |
|---|---|---|
| Schedule | Seller or agent supplies vehicle, preferred branch and time; system reads branch-local schedule, staff skill and slot capacity. | Confirm atomically against a versioned slot; a stale or filled slot returns alternatives. Record UTC instant and branch timezone. Do not expose staff personal calendars. |
| Reschedule or cancel | Seller for own booking; agent for assigned case; branch supervisor may override with reason. | Release old capacity and reserve new capacity atomically; apply notice policy only after approval. Notify once per final version. |
| Check in | Front desk verifies booking and documents against policy; records arrival and vehicle identity. | Mismatch, missing documents, late arrival or wrong branch places case in review; no auction authorization follows an unverified identity. |
| Walk-in | Front desk creates case with consent and records available capacity. | No slot means queue or alternate booking, not silent overbooking. Supervisor override needs reason and audit. |
| Queue and assignment | Supervisor assigns skill-qualified available inspector. | Absence triggers reassignment; completion and cancellation release capacity. No-show is recorded after the configured grace period, not inferred solely from a missed reminder. |

Branch managers can view only authorized branches and aggregate capacity; customer details are case-scoped. Record actor, old/new slot, reason, UTC time and case identifier in the audit trail. Reminder failures create a retry and follow-up task; never cancel a booking solely because a message failed.

## Data and measures

Branch, local working calendar, holiday, appointment, staff capability, slot capacity, check-in, queue item and audit record are owned by scheduling/branch operations. Track booked capacity / offered capacity, attendance / confirmed appointments, inspection wait median and 90th percentile by branch and period. Exclude canceled slots from offered capacity only under a documented historical rule.

## Acceptance and tests

Two simultaneous attempts for the last slot result in exactly one confirmation; the other receives alternatives. Rescheduling across daylight-saving changes displays the intended local time and records an unambiguous instant. A user outside branch scope cannot view the queue. A no-show can be corrected with recorded reason and original history remains visible.
