# Implementation context and source-of-truth rules

**ID:** 20/10_IMPLEMENTATION_CONTEXT · **Version:** 0.3 · **Status:** proposed documentation handoff; live activation not approved · **Owner:** Documentation architect · **Updated:** 2026-11-15

## Product and operating baseline

Design an original English-first, LTR automotive marketplace. Foundational flow: verified seller intake, booking, inspection, reviewed valuation, eligible dealer auction, explicit seller acceptance, contract coordination, independent external settlement verification, title and physical handover, then policy-guarded closure. Consumer inventory/sourcing and authorized buyer offers form a separate commercial origin. Financing, logistics, claims, editorial, growth and analytics have explicit interfaces and activation dependencies. Start with a modular monolith, authoritative transactional PostgreSQL, private evidence store, outbox/inbox, workers and stateless realtime fan-out. Selected library/provider versions are pinned by the future delivery team after review.

The proposed financial mode is `external_evidence_only`. No receipt, ledger, provider timeout, auction win, contract signature or physical handover implies all other milestones. A pending lender offer is not credit approval. No reference-company private implementation is claimed known. No application, migration, deployment or live account change is part of this delivery.

## Required implementation reading and precedence

1. [Master index](../00_MASTER_INDEX.md), [policy baseline](../POLICY_BASELINE.md) and [prompt coverage](../review/PROMPT_COVERAGE.md) establish scope, reversible defaults and DEC-01–07 activation decisions.
2. [Scenario traceability](../SCENARIO_TRACEABILITY.md), [state catalog](../03_USER_JOURNEYS_AND_SCENARIOS/05_STATE_MACHINE_CATALOG.md), [panel contracts](../04_ROLES_AND_PANELS/12_PANEL_CONTRACTS.md) and [screen bindings](../05_UX_RESEARCH_AND_INFORMATION_ARCHITECTURE/10_SCREEN_CONTRACT_BINDINGS.md) define behavior, roles, fields, outcomes and recovery.
3. [OpenAPI](../10_BACKEND_AND_APIS/11_OPENAPI_SPECIFICATION.yaml), [operation index](../10_BACKEND_AND_APIS/12_OPERATION_INDEX.md), [schema fields](../10_BACKEND_AND_APIS/13_SCHEMA_FIELD_REFERENCE.md), [event contracts](../10_BACKEND_AND_APIS/08_EVENT_CONTRACTS.md) and [data constraints](../09_DATA_ARCHITECTURE/10_FIELD_CONSTRAINTS.md) define interfaces and persistence invariants. JSON-formatted YAML is intentional and valid OpenAPI3.1.
4. [Concurrency](../12_AUCTION_AND_TRANSACTION_SYSTEMS/03_AUCTION_CONCURRENCY.md), [financial ledger](../12_AUCTION_AND_TRANSACTION_SYSTEMS/09_FINANCIAL_LEDGER.md), [identity](../14_SECURITY_AND_COMPLIANCE/03_IDENTITY_AND_ACCESS.md) and [recovery](../18_INFRASTRUCTURE_AND_DEVOPS/07_BACKUP_AND_RECOVERY.md) define hard integrity boundaries.
5. Design/UX/motion sections05–07 and frontend section11 define original tokens, component states,48 screens, responsive/accessibility behavior, exact error handling and budgets. They are design specifications, not finished asset files or evidence of user testing.
6. QA/SEO/analytics/infrastructure sections15–18 and delivery section19 define candidate verification, observability, operations, staffing, costs and staged release. [Actual documentation checks](../review/validation-summary.json) are separate from future software tests.

Approved business decisions override reversible proposals only through versioned change review. For machine shapes, OpenAPI and structured event schemas are authoritative; for lifecycle and relational invariants, the state catalog and field/concurrency rules apply in addition. Generated indexes are navigational views, never independent rules. A conflict must be resolved and recorded before implementing the affected command; do not pick whichever document is easiest. Existing auctions/contracts retain their pinned policy versions.

## Consequential invariants and controlled boundaries

- Serialize bid admission, eligibility changes and close with the documented lock order and post-lock trusted time. No accepted acknowledgement before required durable commit; no offline bids.
- Enforce object, organization, branch, purpose and current-grant checks on every command, read, replay, subscription and download. Independent approval compares actor identity, not role labels.
- Preserve immutable reports/signatures/financial facts. Material report correction sets affected auction hold atomically before acknowledgement; analytics and notifications are not safety barriers.
- Exactly one accepted commercial origin creates a transaction. Exclusive vehicle reservation prevents conflicting dealer/consumer commitments; closure rechecks current domain evidence.
- Normalized provider events enter through authenticated internal adapters after provider-specific verification. Selected vendor credentials, signatures and sandbox protocols are onboarding inputs, not invented facts.
- IAM grant administration, protected audit retrieval, recovery/replay and reviewed external remedies use named governed procedures. Credit-backed bidding, destructive identity merge and platform disbursement remain disabled until their explicit approvals and specialized design exist.

Future implementation work can be scoped and estimated against this proposed baseline. Activation of a consequential service still requires the relevant business/legal decisions, provider onboarding and actual runtime tests. The [readiness assessment](01_IMPLEMENTATION_READINESS.md) and [final audit](../FINAL_COMPLETENESS_AUDIT.md) state the limits; there is no fabricated stakeholder sign-off.
