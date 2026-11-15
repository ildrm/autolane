# CRM operations

| Metadata | Value |
|---|---|
| Document ID | 13/03_CRM_OPERATIONS |
| Version / status | 0.1 / proposed; requires domain review |
| Owner | CRM Operations Lead |
| Reviewers | Operations, Product, Security, Legal, QA |
| Updated | 2026-11-15 |
| Scope | CRM operations for the proposed marketplace; jurisdiction and transaction model remain open. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Case and contact workflow

A lead is created from a seller, buyer, dealer or staff-assisted request with source, purpose, consent evidence where applicable, contact method and deduplication candidates. Similar phone, email or vehicle identifier is a review signal, not proof of identity: do not merge records automatically. An agent reviews the candidate pair; an approved merge preserves source IDs, consent histories, case associations and audit trail and supports correction.

Lead stages are new, qualified, follow-up, booked, closed-won and closed-lost; these are CRM summaries, not authoritative auction or financial state. Assignment uses branch/service coverage and workload; manually reassign with reason. An interaction records agent, channel, time, disposition and minimum necessary notes. Tasks carry owner, due time, status and escalation; overdue work is visible to the team lead. Failed contact generates a follow-up according to configurable contact limits; do not infer opt-in from service contact.

## Access, communications and measurement

Staff see only team/case scope. Sensitive documents live in controlled storage rather than unstructured notes; exports are separately authorized and audited. Transactional notifications and marketing consent are separate. Honor channel suppression and legally required communications according to approved local policy. CRM can request appointment or case status but cannot fabricate payment, inspection or auction outcomes.

Measure qualified leads / new leads and bookings / qualified leads for the same mature cohort, with source, date, duplicate exclusion and consent-safe attribution documented. Track overdue follow-ups / open tasks and time to first human contact. A CRM integration outage queues changes for retry and displays freshness rather than showing stale data as current.

## Acceptance and tests

A duplicate match produces a review task without overwriting either record. A revoked marketing consent prevents campaign dispatch without suppressing a legally required transaction notice. An unassigned agent cannot access sensitive case notes. Replayed lead-creation requests do not create a second lead.
