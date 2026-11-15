# Final Requirements Baseline

| Metadata | Value |
|---|---|
| ID / version | 20/02_FINAL_REQUIREMENTS_BASELINE / 0.3 |
| Status | Proposed handoff; implementation not approved |
| Owner / reviewers | Documentation architect / product, operations, legal, finance, engineering, security and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Final Requirements Baseline for future review and implementation planning. |

## Baseline status
**PROPOSED, NOT FINAL OR APPROVED.** The heading reflects the requested artifact name; no requirements baseline has been signed by stakeholders. The [governance traceability table](../00_GOVERNANCE/07_REQUIREMENTS_TRACEABILITY.md) retains the original business objectives; the rows below summarize them, while the120 FR-SCN requirements in the scenario traceability records provide the expanded behavior baseline.

| ID | Requirement and acceptance evidence | Current gap |
|---|---|---|
| BUS-001 / FR-001 | Seller reserves an available branch slot once; concurrent requests for the last slot yield at most one confirmation. | Approve capacity/cancellation policy; execute the mapped concurrency, authorization and replay cases after implementation. |
| BUS-002 / FR-002 | Inspector captures and reviews a versioned checklist; correction retains the original published snapshot and reason. | Approve inspection policy, mandatory items, permissions and complete test matrix. |
| BUS-003 / FR-003 | Eligible dealers' bids are ordered by authoritative state; competing requests receive deterministic outcomes. | Approve auction law and policy; complete outage, close race and permission verification. |
| BUS-004 / FR-004 | Seller makes an explicit decision on a particular offer; no answer or rejection is not acceptance. | Approve deadline, legal effect, identity and appeals policy. |
| BUS-005 / FR-005 | Contract, payment, ownership transfer and handover evidence remain distinct; missing required evidence blocks ordinary closure. | Select approved legal and money-flow model, evidence and role segregation. |

The [current crosswalk](../TRACEABILITY_CROSSWALK.md) preserves these five business objectives and links all120 scenario requirements and test specifications,48 screens,20 panels, operation IDs, entity families and distinct audit/analytics contracts. The structured validation confirms references resolve. Application tests are specified but cannot have executed before software exists; stakeholder policy approval remains separate.

Cross-cutting requirements: English and LTR; configurable jurisdiction, currency, timezone and taxes; scoped authentication and authorization; immutable audit for sensitive changes; accessibility target WCAG 2.2 AA; private report access; safe retry and recovery; no production money movement without authorized model and provider. The [measurable NFR baseline](../NFR_MEASURABLE_BASELINE.md) proposes 26 targets and measurement methods, none measured or approved. They must be refined, independently measured and agreed. Named owners must review the provided scope, acceptance specifications, schema/event definitions and analytics purposes before approving their release baseline; executable application tests are built during implementation.

**Change control:** propose change with rationale and evidence → product, impacted operation and legal/security review → update affected requirement, contract, design and test version → record approval, effective date and migration impact. Any later requirement ID must resolve to one canonical definition, with archived mapping for renamed IDs. Structured trace checks and48 documentation fixtures pass; runtime correctness and policy approval are distinct readiness gates.

## Revision 0.3 source of truth

The [current audit](../FINAL_COMPLETENESS_AUDIT.md), [policy baseline](../POLICY_BASELINE.md), [scenario acceptance mappings](../SCENARIO_TRACEABILITY.md) and [API/schema handoff](05_API_AND_SCHEMA_CONTRACTS.md) supersede earlier limited-coverage counts and validation status. Real stakeholder approval, provider evidence and runtime testing are still not claimed.
