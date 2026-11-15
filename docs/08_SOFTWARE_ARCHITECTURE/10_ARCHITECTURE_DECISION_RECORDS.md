# Architecture Decision Records

| Metadata | Value |
|---|---|
| ID / version | 08/10_ARCHITECTURE_DECISION_RECORDS / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Architecture Decision Records; jurisdiction-dependent policy decisions remain open. |

## ADR register
All decisions below are **PROPOSED**, dated 2026-11-15, owner principal architect, subject to technical and domain approval.

| ADR | Context and decision | Consequence / revisit trigger |
|---|---|---|
| ADR-01 | Start modular monolith with clear ownership and one transactional store. | Low initial operations cost; split only for measured scaling/team isolation needs. |
| ADR-02 | Serialize each auction's bid and close on one authoritative database transaction. | Hot auction throughput bounded by per-auction serialization; load test and consider partition/shard only if targets fail. |
| ADR-03 | Use transactional outbox and idempotent inbox for asynchronous projections. | At-least-once delivery; operate lag, dead-letter and replay controls. |
| ADR-04 | Separate binding HTTP commands from WebSocket updates. | Reconnection uses snapshot/version; added gateway operations. |
| ADR-05 | Store ISO currency and integer minor units with explicit policy version; reject currency mismatch. | Currencies with nonstandard minor units require catalog; rounding only under approved financial policy. |
| ADR-06 | Start settlement as recording externally confirmed obligations and evidence; no implied custody. | True money movement remains blocked on DEC-03 and provider contracts. |
| ADR-07 | Public pages may be server rendered; authenticated and private pages never cache publicly. | CDN configuration and privacy tests required. |
| ADR-08 | Start with human-reviewed rule-based valuation, record confidence and overrides. | No claims of model precision; add model only after data, monitoring and validation. |

Decision records need explicit reviewer, status transition, alternatives, risk owner and implementation impact before becoming approved. Business decisions DEC-01–DEC-07 take precedence over conflicting provisional technical assumptions.
