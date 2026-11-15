# Acceptance Gate Checklist

| Metadata | Value |
|---|---|
| ID / version | 20/08_ACCEPTANCE_GATE_CHECKLIST / 0.1 |
| Status | Proposed handoff; implementation not approved |
| Owner / reviewers | Documentation architect / product, operations, legal, finance, engineering, security and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Acceptance Gate Checklist for future review and implementation planning. |

## Independent gates — all currently pending
Each gate requires named accountable reviewer, exact document/build version, evidence location, date, pass/fail, exceptions and re-review date. These requirements are **proposed**, not evidence of completed tests or sign-off.

| Gate | Minimum pass evidence | Owner |
|---|---|---|
| Product | Approved business model, scope, journey priorities and measurable outcomes; valid requirement crosswalk. | Product lead |
| UX | Tested task flows, errors and recovery with representative sellers, dealers and staff; action/data mapping. | UX research lead |
| Visual design | Original rights-cleared brand and assets, consistent responsive components and contrast tests. | Design lead |
| Motion | Timings, triggers, interruption, reduced-motion alternative and measured performance for critical transitions. | Motion lead |
| Architecture and data | Approved ADRs, domain boundaries, field-level schemas, consistent contracts, bid/close correctness and restore evidence. | Principal architect / data lead |
| Security and privacy | Threat model, scope/authorization tests, privacy assessment, verified mitigation and incident process. | Security / privacy leads |
| QA | Requirement-to-test-to-result trace, positive/negative/authorization/retry/race coverage and defect disposition. | QA director |
| SEO and content | Crawl, canonical/indexation, content accuracy, structured data and public/private isolation checks. | SEO / content leads |
| Operations | Actual staff trained, operating hours, queue owners, escalation and branch/provider outage drills passed. | Operations lead |
| Finance and legal | Jurisdiction, parties, auctions, custody, settlement, contracts, transfer, tax, privacy and liability approved in writing. | Finance / legal leads |
| Handoff and delivery | All P0 decisions closed, manifest and references accurate, reading order, operational owner and release plan accepted. | Documentation architect / program director |

Any unresolved P0, failed financial integrity or critical security/authorization issue prevents the corresponding gate and readiness declaration. Noncritical exceptions require accountable approval, evidence of compensating control and expiry; they cannot waive applicable law. Record actual test results, not merely test plans.

## Revision 0.3 source of truth

The [current audit](../FINAL_COMPLETENESS_AUDIT.md), [policy baseline](../POLICY_BASELINE.md), [scenario acceptance mappings](../SCENARIO_TRACEABILITY.md) and [API/schema handoff](05_API_AND_SCHEMA_CONTRACTS.md) supersede earlier limited-coverage counts and validation status. Real stakeholder approval, provider evidence and runtime testing are still not claimed.
