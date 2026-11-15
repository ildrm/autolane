# Error Handling Standards

| Metadata | Value |
|---|---|
| ID / version | 10/10_ERROR_HANDLING_STANDARDS / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Backend and architecture leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Error Handling Standards; commercial and jurisdiction-dependent policy decisions remain open. |

## Stable errors and recovery
Error JSON: `{error: {code, message, field_errors?, retryable, correlation_id}}`. `code` is stable uppercase machine-readable; `message` is natural English without sensitive internal data; `field_errors` maps permitted field names to actionable messages. Correlation ID links a redacted server log and audit where applicable; never include tokens, VIN, document content, account numbers or stack traces in clients.

| HTTP | Example code | Client handling |
|---|---|---|
| 400 | `INVALID_CURSOR` | Correct query; do not retry unchanged. |
| 401 / 403 | `UNAUTHENTICATED` / `FORBIDDEN` | Reauthenticate or show access denied without exposing existence. |
| 409 | `SLOT_UNAVAILABLE`, `BID_TOO_LOW`, `IDEMPOTENCY_CONFLICT` | Refresh authoritative state; a changed request needs a new idempotency key. |
| 412 | `PRECONDITION_FAILED` | The `If-Match` value is stale; retrieve the authorized current representation, review changes and use a new key for a changed command. |
| 422 | `INVALID_AMOUNT`, `CURRENCY_MISMATCH` | Highlight field, retain non-sensitive inputs. |
| 429 | `RATE_LIMITED` | Honor `Retry-After`; do not spam. |
| 503 | `AUTHORITY_UNAVAILABLE` | Offer retry with same idempotency key where outcome is uncertain, and show degraded service. |

An HTTP timeout after a command is not proof of failure: query or retry with the same key. Reject same key with changed payload. Validation, authorization and rate limits run server-side. Operational alerts distinguish business rejections from dependency failures; test every published error, including rollback after internal failure and absence of private information.
