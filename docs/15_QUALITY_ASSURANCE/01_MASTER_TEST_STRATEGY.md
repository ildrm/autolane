# Master test strategy

| Metadata | Value |
|---|---|
| Document ID | 15/01_MASTER_TEST_STRATEGY |
| Version / status | 0.1 / proposed; review required |
| Owner | QA Director |
| Reviewers | Product, QA, Engineering, Operations, Security, Design |
| Updated | 2026-11-15 |
| Scope | Master test strategy for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [release quality gates](10_RELEASE_QUALITY_GATES.md). |

## Scope and levels

Verify the seller-to-dealer transaction loop first, then retail, sourcing, credit and logistics according to release scope. Business rules and interfaces remain proposed until responsible owners approve them. Run unit tests for deterministic validation and state transitions; integration tests against real transactional storage and queues; API contract and authorization tests; end-to-end journeys against representative services and providers' sandboxes; manual exploratory, accessibility, security and UAT reviews. Synthetic data only in lower environments, with controlled test accounts for each organization and branch.

Prioritize auction ordering, eligibility, settlement reconciliation, access boundaries, report correction and transaction recovery. A test fixture must include one seller, two dealers in separate organizations, a branch, an inspector, reviewer, auction manager, finance maker/checker and an unauthorized actor. Each run records build, policy versions, data reset, provider simulation, environment, results and logs without sensitive data. Flaky tests are quarantined with owner and deadline; removing a failing test does not satisfy a gate.

## Coverage and gates

Map each release requirement to positive and negative expected outcomes, actor, test case, environment and evidence. Measure critical scenario coverage as passed critical scenarios / applicable approved critical scenarios; keep blocked and not-run distinct from passed. Verify both branch-level permissions and cross-organization isolation. No production launch while P0 legal/commercial decisions remain open; no known critical security issue, unresolved bid integrity error or unverified financial reconciliation. QA sign-off does not substitute for legal, finance or operations approval.

Test data must cover stale versions, duplicate requests, daylight-saving changes, multi-currency rejection, failed notifications, provider callbacks and interrupted jobs. Run disaster recovery and restore with synthetic transactions before launch. Record defects with reproducible input, expected/actual behavior, severity, owner and retest evidence.
