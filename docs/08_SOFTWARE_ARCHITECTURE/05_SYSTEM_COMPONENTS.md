# System Components

| Metadata | Value |
|---|---|
| ID / version | 08/05_SYSTEM_COMPONENTS / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | System Components; jurisdiction-dependent policy decisions remain open. |

## Components and operational boundaries
| Component | Responsibility | Failure response |
|---|---|---|
| Edge | TLS termination, request size and abuse controls, routing | Fail closed on invalid identity; return traceable unavailable response during outage. |
| Web presentation | Render public pages and authenticated screens | Server render indexable pages; preserve user input and offer retries. |
| API application | Authentication, object authorization, command validation and transactional domain rules | Return stable error codes; no accepted result before commit. |
| PostgreSQL | Store authoritative business state, idempotency, audit, outbox | Block binding writes when unavailable; restore and reconcile before reopen. |
| Relay and workers | Dispatch committed events and integrate with external systems | Exponential backoff with jitter, dead-letter and operator replay; deduplicate. |
| Gateway | Authorized subscriptions and versioned auction updates | Disconnect and resync; never decide state or cache private reports across organizations. |
| Object storage | Encrypted immutable versions of private reports and signed documents | Short-lived scoped access, malware scan/quarantine, deny on missing authorization. |
| Search / analytics | Rebuildable consumer listing and aggregate views | Mark lag and reindex; never used as bid/payment authority. |

**Acceptance:** simulate each component unavailable; binding decisions remain accurate, private objects are not public, failed work becomes visible and recoverable, and projections catch up after replay.
