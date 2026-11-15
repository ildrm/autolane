# Unresolved Decisions

| Metadata | Value |
|---|---|
| ID / version | 20/09_UNRESOLVED_DECISIONS / 0.3 |
| Status | Proposed handoff; implementation not approved |
| Owner / reviewers | Documentation architect / product, operations, legal, finance, engineering, security and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Unresolved Decisions for future review and implementation planning. |

## Decision register and escalation
Canonical initial decisions are defined in [master index](../00_MASTER_INDEX.md); the entries below identify review needs without silently changing IDs or status. All remain **DECISION REQUIRED** unless an accountable owner records an approved decision and evidence.

| ID / priority | Decision and accountable role | Needed before |
|---|---|---|
| DEC-01 / P0 | Launch jurisdiction, regulated activities and contracting entities; executive sponsor + legal. | Legal notices, tax, identity, contracts, transfer, infrastructure location and launch. |
| DEC-02 / P0 | Intermediary vs owned-inventory and legal title/risk allocation; product + legal. | Contract parties, obligations, warranties and accounting. |
| DEC-03 / P0 | Direct settlement vs provider, escrow or platform custody; finance + legal. | Payment/settlement integration, ledger, fee recognition and refunds. |
| DEC-04 / P0 | Auction binding effect, eligibility, reserve, increments, authoritative time/ties, cancellation, seller response and default; commercial operations + legal. | Final auction implementation contract, tests, terms and pilot. |
| DEC-05 / P0 | Contract validity, authorized signature and ownership-transfer evidence; legal + operations. | Templates, signing and closure policy. |
| DEC-06 / P0 | Inspection responsibility, correction, warranty and dispute remedies; inspection lead + legal. | Checklist approval, marketing claims and claim workflow. |
| DEC-07 / P0 | Consent, privacy, records, retention, lawful access and incident obligations; privacy + security. | Collection, sharing, production data and release. |
| DEC-08 / P1 | Launch region, branch capacity, staffing and volume; operations + product. | Capacity plan, pilot size, unit economics and vendor sizing. |
| DEC-09 / P1 | Technology choices and service boundaries; principal architect. | Approved ADRs, hiring and detailed deployment plan. |
| DEC-10 / P1 | Proxy bids, anti-sniping, credit, deposits and automated valuation; product + operations. | Optional functionality; keep disabled until independently approved. |

Documentation review now includes semantic OpenAPI validation,168 schema definitions, guarded transitions, logical field constraints and scenario/screen/panel/API references. Remaining approval or future evidence concerns selected external provider protocols, market-specific retention and legal terms, named stakeholder review, representative workload/NFR validation, actual participant research and rights-cleared production assets. These are explicit dependencies, not a claim of newly approved policy. Decisions record alternatives, rationale, impacted parties, effective date, approver, evidence, dependencies and review date. Escalate blocked P0s to executive sponsor; elapsed time never implies approval.

## Revision 0.3 source of truth

The [current audit](../FINAL_COMPLETENESS_AUDIT.md), [policy baseline](../POLICY_BASELINE.md), [scenario acceptance mappings](../SCENARIO_TRACEABILITY.md) and [API/schema handoff](05_API_AND_SCHEMA_CONTRACTS.md) supersede earlier limited-coverage counts and validation status. Real stakeholder approval, provider evidence and runtime testing are still not claimed.
