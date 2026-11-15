# Module Dependency Order

| Metadata | Value |
|---|---|
| ID / version | 20/04_MODULE_DEPENDENCY_ORDER / 0.1 |
| Status | Proposed handoff; implementation not approved |
| Owner / reviewers | Documentation architect / product, operations, legal, finance, engineering, security and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Module Dependency Order for future review and implementation planning. |

## Proposed implementation sequence after approval
| Order | Module / vertical slice | Prerequisite and acceptance |
|---:|---|---|
| 1 | Environments, identity, organization, role/object authorization, audit and notifications | Approved legal/privacy scope and threat model; revoked users denied and sensitive actions auditable. |
| 2 | Vehicle taxonomy, seller lead, consent, CRM and branch schedule | Approved data, consent, capacity and messaging policies; duplicate lead review and slot locking tested. |
| 3 | Inspection templates/revisions and human-reviewed valuation | Vehicle and appointment, approved checklist and evidence rights; published revision immutable and corrections traced. |
| 4 | Dealer onboarding, eligibility and verified report access | Organization and permissions; reviewer separation and suspension behavior tested. |
| 5 | Auction scheduling, authoritative bids/close, realtime dealer UI | Pinned inspection and approved DEC-04 rules; concurrency, time, idempotency, replay and outbox tests pass. |
| 6 | Seller offer presentation and explicit decision | Finalized qualifying outcome, identity and approved deadline; refusal/expiry never silently accepted. |
| 7 | Contract and settlement evidence, finance reconciliation, transfer and handover | Approved DEC-01–05 money/title model and provider contracts; independent evidence checks and discrepancy recovery tested. |
| 8 | Support, branch operations, observability, recovery and full UAT | Implement alongside all above, not a final add-on; confirm queues, training and actual support coverage. |
| 9 | Consumer marketplace, sourcing, CMS and SEO | Approved publication, consent, availability and separate inventory model; public/private leakage tests. |
| 10 | Financing, logistics, warranty and advanced data products | Separate licensed partners, legal policies, operational capacity and governed models. |

Cross-cutting security, accessibility, design, QA and analytics apply to every slice. Context boundaries do not imply microservice deployments. This sequence is not authorization to start work while P0 decisions or scope remain unapproved.

## Revision 0.3 source of truth

The [current audit](../FINAL_COMPLETENESS_AUDIT.md), [policy baseline](../POLICY_BASELINE.md), [scenario acceptance mappings](../SCENARIO_TRACEABILITY.md) and [API/schema handoff](05_API_AND_SCHEMA_CONTRACTS.md) supersede earlier limited-coverage counts and validation status. Real stakeholder approval, provider evidence and runtime testing are still not claimed.
