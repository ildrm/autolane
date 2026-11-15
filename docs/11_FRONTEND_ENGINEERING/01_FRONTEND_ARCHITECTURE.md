# Frontend Architecture

| Metadata | Value |
|---|---|
| ID / version | 11/01_FRONTEND_ARCHITECTURE / 0.3 |
| Status | Proposed, pending design and product review |
| Owner / reviewers | Frontend architect / design, accessibility, security, QA |
| Updated | 2026-11-15 |
| Scope | Frontend Architecture, initial English LTR release. |

## Application boundaries
**PROPOSED:** React/TypeScript responsive web with server-rendered public routes and authenticated customer, dealer and staff experiences. Public catalog and articles render indexable content on the server; authenticated pages are private and excluded from shared caching. The backend, not the browser, owns authorization and business rules. Each interface consumes typed API contracts and shared accessible primitives; feature modules organize route, screen, API adapter and tests without copying sensitive data into global stores.

On the dealer auction page, obtain an authoritative snapshot, subscribe to scoped updates and submit bids through HTTPS with an idempotency key. Any disconnect or unknown bid result triggers state reconciliation; never infer acceptance from animation or countdown. For privileged operations, surface server-supplied effective permissions as usability hints while server enforces each action. Error boundaries isolate pages; forms retain non-sensitive input on recoverable failure, and personal data does not enter telemetry. SSR must not expose authorization tokens in HTML. Load design assets progressively and ensure a complete non-animated experience.

**Acceptance:** public content renders without JavaScript where feasible; a denied API yields appropriate access state, not a blank screen; staff sign-out invalidates cached private views; bid response reflects committed server state and no offline command is accepted.

## Rendering, module dependency and delivery contract

| Layer | Allowed dependencies | Output and boundary |
|---|---|---|
| Public route renderer | Published catalog/content read adapters and design primitives | HTML headings, canonical metadata, essential body and image dimensions before hydration; no session-derived object in shared cache. |
| Authenticated route loader | Current session, scoped domain reads and effective capabilities | Gate shell and fetch only visible records; 401 recovery and 404 privacy handling precede sensitive rendering. |
| Feature controller | One domain adapter, transient form state and shared feedback | Maps DTO to view model, owns command receipt, refresh and error state. No cross-feature mutable singleton. |
| API adapter | Versioned OpenAPI DTO and error contract | Credentials, CSRF, idempotency, conditional version, cancellation and response decoding in one place. Never embed privileged service credentials. |
| Presentation primitive | Tokens and explicit props/callbacks | No network, raw HTML, business authorization or persistent private state. |
| Stream adapter | Authenticated connection, schema and snapshot controller | Per-auction ordered version processing; disconnect clears subscriptions, not evidence of accepted commands. |

A delivery build pins package versions, provides a dependency inventory and separates environment configuration from public bundles. CSP-approved sources and asset rights are reviewed before external scripts load. Route error boundaries preserve the navigation shell and safe input; root failures display a plain recovery link and reference ID. A release is acceptable when every panel can render loading, empty, denied, stale and failed reads from contract fixtures without contacting a live provider. Production code remains a later phase.
