# Integration Contracts

| Metadata | Value |
|---|---|
| ID / version | 10/09_INTEGRATION_CONTRACTS / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Backend and architecture leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Integration Contracts; commercial and jurisdiction-dependent policy decisions remain open. |

## Adapter contract and responsibilities
Every integration must document provider, lawful basis, data classification, consent, supported countries, SLA, cost, retention, credentials and human owner before activation. Request has internal operation ID, provider idempotency key, version, deadline and correlation; response maps provider status into a domain state without losing raw status metadata. Callback validation requires signature, timestamp/replay protection and durable deduplication before acknowledged success.

| Adapter | Required capability | Timeout/failure |
|---|---|---|
| SMS / email / push | Template, locale English, destination, send ID and delivery outcome | Backoff for transient errors; invalid address permanently failed and assigned to CRM. |
| Identity verification | Subject, consent, minimum evidence, check ID and provider verdict | Timeout pending; conflict or rejection to authorized reviewer; no automatic pass. |
| Payment provider | Only after DEC-03; amount minor/currency, parties, reference and provider status | Timeout unknown; status query and reconciliation precede retry; never infer transfer. |
| E-signature | Approved document hash/version, signers and signed evidence | Verify callback and hash; pending if provider unavailable. |
| Registry/tax | Approved jurisdiction request and legal purpose | Preserve request reference; failure queues manual review, no title assertion. |
| Maps/taxonomy | Query and cached version | Use stale labeled data or manual input on outage. |
| Lender/carrier | Scoped consent, application/transfer reference and result | Provider decision or proof recorded; no guaranteed approval or delivery. |

Contract tests cover schema, credentials rotation, duplicate and reordered callbacks, invalid signatures, timeouts, sandbox behavior and data minimization. Rate limits and pricing are supplier-specific unresolved commercial inputs.
