# User acceptance testing plan

| Metadata | Value |
|---|---|
| Document ID | 15/09_UAT_PLAN |
| Version / status | 0.1 / proposed; review required |
| Owner | UAT Lead |
| Reviewers | Product, QA, Engineering, Operations, Security, Design |
| Updated | 2026-11-15 |
| Scope | User acceptance testing plan for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [release quality gates](10_RELEASE_QUALITY_GATES.md). |

## Participants and setup

Recruit representative seller, dealer, front-desk, inspector, auction manager, finance, legal and support participants, including accessibility needs. Each receives a role-scoped synthetic account, approved policy set and realistic but fictional vehicles, appointments, reports and transactions. Explain task goals without instructing participants which controls to click. Document their consent, test environment, build, scenario and observations; this plan does not assert that user research has already happened.

## Acceptance sessions

1. A seller submits a vehicle, corrects a validation error, books a slot, sees report and makes an informed offer decision.
2. Branch and inspection teams handle check-in, missing documents, report review and a correction after publication.
3. An approved dealer finds an eligible auction, bids, recovers from lost acknowledgment and understands the outcome and remaining seller decision.
4. Finance and legal coordinate a contract, identify partial settlement and demonstrate that title and payment are not falsely marked complete.
5. Support and logistics handle a complaint and an undelivered vehicle without losing custody or exposing another participant's data.

Capture completion, errors, confidence, time on task and qualitative feedback; avoid invented benchmark values. Classify defects by impact and route to owners. A task failure affecting auction, access, money, contract or transfer is a blocker until fixed and retested.

## Exit

Product, branch operations, inspection, dealer operations, finance, legal, accessibility and support each sign their respective scenarios against approved criteria. An unresolved policy blocks the affected test and launch; lack of participants or simulated provider behavior is reported as a limitation, not a pass.
