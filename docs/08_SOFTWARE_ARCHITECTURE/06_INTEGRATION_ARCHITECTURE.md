# Integration Architecture

| Metadata | Value |
|---|---|
| ID / version | 08/06_INTEGRATION_ARCHITECTURE / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Integration Architecture; jurisdiction-dependent policy decisions remain open. |

## Provider boundary
External providers are adapters behind domain-owned ports. A provider request records operation ID, semantic payload hash, attempt, deadline, trace ID and provider correlation ID. No secret or document body is placed in logs. Webhooks verify signature, timestamp and replay token, then enter a durable inbox before acknowledgement. Authenticated provider callbacks may be delayed, duplicated or reordered and cannot override a later terminal decision without reconciliation.

| Integration | Data / trigger | Retry and fallback |
|---|---|---|
| SMS, email | Minimum destination and approved template after commit | Retry transient failures with backoff; suppress permanently invalid recipients; route important failures to CRM. |
| Identity | Minimal subject and document references after consent | Pending on timeout, manual review on mismatch; prohibit silent approval. |
| Payment / external settlement | Only after DEC-03, provider contract and lawful authority | Idempotency key and status query; timeout means unknown, not failed; reconciliation before retry or refund. |
| Electronic signature / registry | Approved version and participant identity | Verify callback and evidence; unavailable means signature/transfer pending, never presumed. |
| Maps / taxonomy | Non-sensitive location or catalog query | Cached last-good catalog with age; manual address and correction possible. |
| Carrier / lender | Explicit consent and minimum information | Provider response authoritative only within approved contract; outages enqueue manual escalation. |

Every adapter needs contract tests, sandbox credentials, documented provider rates and retention, circuit breaker, revocation and a per-provider kill switch. Negotiated SLAs and lawful data transfer are unresolved.
