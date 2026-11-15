# Requirements, contracts and evidence crosswalk

**ID:** TRACE-01 · **Version:** 0.3 · **Status:** proposed mappings reviewed for internal consistency · **Owner:** Requirements lead · **Reviewers:** Product, API, data, security, analytics, QA · **Updated:** 2026-11-15

## Complete scenario index and identifier authority

[Scenario traceability](SCENARIO_TRACEABILITY.md) and its [structured records](contracts/scenario-traceability.json) now map all120 scenario IDs to a requirement, actor/precondition, screen, supporting operation IDs, entity family, outcome, failure/recovery behavior, audit/analytics and a six-part acceptance specification. `FR-SCN-001`–`FR-SCN-120` and `TST-SCN-001`–`TST-SCN-120` extend the original five business-level requirements and tests; they are not claims that runtime tests have executed. The original `API-01`–`API-22` aliases remain in the API catalog; the operation index assigns every current operation `API-X-{operationId}`.

| Business objective / original requirement | Current contract and data | Explicit correctness tests / remaining approval |
|---|---|---|
| BUS-001 / FR-001 / SCN-01 | createAppointment, listBranchSlots, readAppointment, transitionAppointment; locked AppointmentSlot and Appointment | TST-SCN-001 plus SM-02 transition cases: last-slot race, wrong owner/branch, stale ETag, same-key replay and atomic reschedule. Branch cancellation/notice policy approval remains separate. |
| BUS-002 / FR-002 / SCN-02 | readInspectionTemplate, createInspectionRevision, readInspectionRevision, publishInspection and transitionInspection; immutable Revision/Finding | TST-SCN-002 and SM-03: complete approved checklist, unknown/N/A reason, maker/checker, exact version, material correction safety hold before acknowledgement. Inspection liability/commitments require DEC-06. |
| BUS-003 / FR-003 / SCN-03 | submitBid, getAuctionSnapshot, readBidCommand, closeAuction; BidCommand receipt, Bid, AuctionResult | TST-SCN-003 and SM-06/07: post-lock clock, serial bid/close, active eligibility, replay after access revocation, resync and durable acknowledged result. Commercial auction terms DEC-04 remain open. |
| BUS-004 / FR-004 / SCN-04 | readResultRecord, recordSellerDecision; current offer, SellerDecision, unique TransactionCase and pending OwnershipTransfer | TST-SCN-004: absent/expired/stale/foreign offer rejected; accepted replay returns same transaction; no inferred signature, settlement or custody. Legal binding point requires market terms. |
| BUS-005 / FR-005 / SCN-05 | Contract/signature, obligation/evidence, prepare/approve reconciliation, title verification, handover, closeTransaction | TST-SCN-005 and SM-11/12/13: missing evidence, wrong currency, partial/duplicate allocation, self-approval, reversal and exception block closure. DEC-03/05 govern funds/title. |

## Supporting specifications

- [Panel contracts](04_ROLES_AND_PANELS/12_PANEL_CONTRACTS.md) and [panel index](contracts/panel-index.json):20 surfaces with role, route, data/action, state and approval behavior.
- [State catalog](03_USER_JOURNEYS_AND_SCENARIOS/05_STATE_MACHINE_CATALOG.md):15 families and84 guarded transitions, with structured test IDs and immutable-history semantics.
- [Operation index](10_BACKEND_AND_APIS/12_OPERATION_INDEX.md) and [OpenAPI](10_BACKEND_AND_APIS/11_OPENAPI_SPECIFICATION.yaml): request/response schemas, errors, security and version requirements.
- [Field constraints](09_DATA_ARCHITECTURE/10_FIELD_CONSTRAINTS.md), dictionary and ERD: persistence ownership and cross-record invariants; transport DTO is not the database schema.
- [Domain events](10_BACKEND_AND_APIS/08_EVENT_CONTRACTS.md), [domain schema](contracts/domain-event.schema.json) and [analytics schema](contracts/workflow-analytics.schema.json): operational facts and purpose-limited measurements remain distinct.
- [NFR baseline](NFR_MEASURABLE_BASELINE.md):26 measurable proposed targets, environments and owners; these are not measured production commitments.

## Test interpretation and remaining boundaries

Every scenario specification requires success, invalid input, wrong scope, stale version, retry/duplicate and the named failure/recovery case. Some outcomes involve a governed human procedure, provider onboarding or an intentionally disabled later-phase feature. The delivery-mode table in the scenario traceability document identifies them explicitly. A supporting read API is not a substitute for an unauthorized mutation or external provider contract. Native identity merge, credit exposure reservation, actual platform payouts and arbitrary public event replay are not silently enabled.

Documentation validation confirms references and schema fixtures only. Domain approval, realistic prototype evaluation, provider sandbox behavior and actual security/concurrency/recovery tests are separate evidence. Current results and scope are in the [final audit](FINAL_COMPLETENESS_AUDIT.md). No independent human sign-off is claimed.
