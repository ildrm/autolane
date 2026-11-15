# Critical test case catalog

| Metadata | Value |
|---|---|
| Document ID | 15/02_TEST_CASE_CATALOG |
| Version / status | 0.1 / proposed; review required |
| Owner | Test Architect |
| Reviewers | Product, QA, Engineering, Operations, Security, Design |
| Updated | 2026-11-15 |
| Scope | Critical test case catalog for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [release quality gates](10_RELEASE_QUALITY_GATES.md). |

## Release-critical tests

Test IDs below are local to this catalog; they do not claim complete requirements traceability. All outcomes assume the corresponding business rule has been approved. User interface, server state, durable audit and expected notification intent must be checked where applicable.

| ID / priority | Preconditions and action | Expected result |
|---|---|---|
| QA-001 / P0 | Two sellers request the last available slot concurrently. | One confirms; other receives a conflict and alternatives; capacity never becomes negative. |
| QA-002 / P0 | Inspector submits report missing a mandatory point. | Submit rejected with item-level feedback; published version unchanged. |
| QA-003 / P0 | Inspector attempts own report approval. | Denied under proposed maker/checker policy; denied action recorded. |
| QA-004 / P0 | Dealer A reads report restricted to B or submits as B. | Server denies; no confidential payload or bid is recorded. |
| QA-005 / P0 | Two eligible dealers submit valid competing bids concurrently. | Accepted bids have a durable authoritative order; current price and response agree with approved increment rule. |
| QA-006 / P0 | Same bid key sent twice after lost acknowledgment. | Same result returned; one logical accepted bid. Different payload under key is rejected. |
| QA-007 / P0 | Valid bid races auction closing at configured deadline. | Exactly one serialized outcome according to approved server-time rule; replay produces same result. |
| QA-008 / P0 | Seller rejects presented offer. | No contract, payment or title success implied; case follows approved recovery path. |
| QA-009 / P0 | Provider sends duplicated or forged settlement callback. | Forged callback rejected; valid duplicate not double-counted; status awaits required reconciliation. |
| QA-010 / P0 | Buyer pays partial amount or evidence conflicts. | Case stays open, discrepancy assigned to finance; no final settlement or title claim. |
| QA-011 / P0 | Report correction proposed after auction publication. | Prior version retained; configured pause/review process prevents silent substitution. |
| QA-012 / P0 | Staff maker attempts to approve own financial adjustment. | Denied and audited; separate authorized reviewer required. |
| QA-013 / P1 | Dealer loses connection following a bid. | UI marks uncertainty, reconnects and fetches authoritative outcome; no duplicate bid on retry. |
| QA-014 / P1 | Marketing consent withdrawn before queued campaign sends. | Optional message suppressed; essential service notices evaluated separately. |
| QA-015 / P1 | Vehicle damaged in transit. | Evidence retained, custody visible and claim assigned; no automatic liability judgment. |
| QA-016 / P1 | Restricted document uploaded containing executable content. | Quarantined/rejected and not served, with security alert when appropriate. |
| QA-017 / P1 | Database recovered after interruption during auction. | Durable accepted bids and event sequence reconcile; no duplicate financial or notification effects. |
| QA-018 / P1 | Keyboard-only seller completes booking and corrects an error. | Every control and message is accessible, focus is visible and no task requires a pointer. |

## Completion rule

For each test specify exact payloads, environment, policy, setup and teardown in the executable test system. Extend this seed catalog to cover all approved requirements and scenario transitions; the 18 cases here do not claim complete coverage. Blocked decisions remain blocked tests, not assumed passes.

## Expanded contract baseline — revision 0.3

[120 structured acceptance specifications](../contracts/scenario-traceability.json) and [84 transition test specifications](../contracts/state-machines.json) extend QA-001–018. Each includes precondition, role/guard, expected effect, negative outcome and replay checks. These are documentation tests to implement later, not application tests already executed.
