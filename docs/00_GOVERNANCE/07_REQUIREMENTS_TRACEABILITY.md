# Requirements traceability

| Metadata | Value |
|---|---|
| Document ID | 00/07_REQUIREMENTS_TRACEABILITY |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and documentation leadership |
| Reviewers | Operations, legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Requirements traceability; English-first automotive marketplace documentation |

## Method and limitations
The chain is business outcome → actor → journey/scenario → functional requirement → rule → screen → API → entity → authorization → test → analytics → acceptance. The table below establishes a **proposed initial product-side crosswalk**, not an assertion that downstream API, entity, security, event and test definitions are complete. API and schema owners must assign canonical IDs and append links before implementation; the gap is a release blocker.

| Objective | Actor and journey | Proposed requirement | Rule and scenario | Screen / data / access | Acceptance and evidence |
|---|---|---|---|---|---|
| BUS-001 Seller conversion | Seller → book | FR-001 Reserve an available slot and confirm once. | BR-001 no overbooking; SCN-01 | Seller booking; appointment and branch capacity; owner/branch scope. | TST-01 two requests for last slot yield at most one confirmation; analytics distinguish attempted and confirmed. |
| BUS-002 Trustworthy evidence | Inspector → report | FR-002 Capture and review a versioned checklist with explicit unknowns. | BR-002 no silent alteration; SCN-02 | Inspector report; vehicle and report version; assigned staff, separate reviewer. | TST-02 correction retains original published snapshot and reason. |
| BUS-003 Fair auction | Authorized dealer → bid | FR-003 Validate and order bids against authoritative state. | BR-003 server acceptance controls outcome; SCN-03 | Dealer auction; eligibility, auction and bid; org-authorized bidder. | TST-03 simultaneous bids result in a single ordered leader and deterministic acknowledgements. |
| BUS-004 Seller choice | Seller → decide | FR-004 Record explicit decision on a specific offer. | BR-004 no automatic acceptance; SCN-04 | Seller offer; outcome, decision; seller owner. | TST-04 missing/rejected/expired offer never becomes accepted. |
| BUS-005 Accurate closure | Finance/legal → reconcile | FR-005 Keep payment, contract, transfer and handover evidence separate. | BR-005 completion needs approved evidence; SCN-05 | Finance and legal cases; obligations and supporting evidence; scoped finance/legal. | TST-05 missing required evidence blocks ordinary closure. |

BUS/FR/BR/SCN/TST entries are defined in this table for this initial baseline; detailed catalogs must preserve or explicitly map them. Links to named API operations, entities, events, test suites, and analytics taxonomies are **outstanding**, not invented. Owner: requirements engineer, API architect and QA lead. A complete trace requires each requirement's successful, failed, unauthorized and duplicate/retry outcomes and evidence of review; architecture and QA gates remain open until the omissions are resolved.

## Expanded contract baseline — revision 0.3

[All 120 scenario requirements and test specifications](../SCENARIO_TRACEABILITY.md) now supplement the five core requirement chains. Machine-readable records identify automated, manual and remaining integration boundaries.
