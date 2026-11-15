# Data Fetching

| Metadata | Value |
|---|---|
| ID / version | 11/04_DATA_FETCHING / 0.3 |
| Status | Proposed, pending design and product review |
| Owner / reviewers | Frontend architect / design, accessibility, security, QA |
| Updated | 2026-11-15 |
| Scope | Data Fetching, initial English LTR release. |

## Fetching and mutations
Typed clients validate response shape and map stable errors to accessible UI messages. Server-render anonymous public pages with explicit cache lifetimes and revalidation; never cache personalized, dealer or staff response in shared CDN. Browser fetches send scoped session cookies and CSRF headers; include request correlation ID without sensitive data. Limit pagination to server-defined sizes and cancel superseded search requests.

Mutation lifecycle: capture user intent → validate fields locally → allocate idempotency key for the exact semantic operation → send → render pending state → on committed success show authoritative result and invalidate affected views. If a timeout occurs, preserve key and payload and reconcile via replay; a changed amount is a new intent and new key. A stale version returns conflict and requires user review, not silent overwrite. Retry only transient reads with bounded jitter; retries for money/bids must use identical key and explicit reconciliation. Avoid automatic unsafe retries on permanent 4xx errors. Show last verified time for stale public data and fail closed on inaccessible private resources.

## Request policy and visible outcomes

| Response / condition | Client action | User-facing result |
|---|---|---|
| 200/201 | Decode schema; accept new version; invalidate affected scoped queries | Show committed state and next step. |
| 202 | Track returned challenge/job/inbox resource | “Your request is being processed.” No completed domain state. |
| 401 | Clear private cache; disconnect feed; validated same-origin login return | “Sign in to continue.” Retain only safe draft fields. |
| 403/404 | Clear restricted record; avoid automatic retry | Generic access/not-found state; no existence hints. |
| 409 | Inspect stable domain code; refresh authoritative state | Slot/listing no longer available or incompatible key; preserve safe choices. |
| 412 | Refetch resource ETag, compare against edited version | “This record changed. Review the latest version.” |
| 422 | Map field paths to controls and focus error summary | Specific correctable field errors. |
| 429 | Respect Retry-After; stop automatic command retries | Visible retry time without silently queueing a bid. |
| 5xx/network timeout | Up to two retry attempts for idempotent reads, 0.5s then 1.5s jitter; binding commands reconcile same key | Unknown state retained; no inferred failure or success. |

Proposed public catalog cache ceiling is 60 seconds; publication, sold and withdrawal events actively invalidate by listing ID. Binding inquiry/offer acceptance still checks authority. Public editorial cache ceiling is 5 minutes with publication invalidation. Private responses are `private, no-store`, including errors and signed file grants. An in-flight read is aborted on scope change and any late response is discarded if its scope epoch no longer matches. These proposed cache values are reversible deployment settings, not consistency guarantees.
