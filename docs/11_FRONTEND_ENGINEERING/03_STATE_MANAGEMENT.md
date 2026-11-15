# State Management

| Metadata | Value |
|---|---|
| ID / version | 11/03_STATE_MANAGEMENT / 0.3 |
| Status | Proposed, pending design and product review |
| Owner / reviewers | Frontend architect / design, accessibility, security, QA |
| Updated | 2026-11-15 |
| Scope | State Management, initial English LTR release. |

## State ownership
| State | Authority / local behavior | Recovery |
|---|---|---|
| Auction bids, outcome, eligibility | Backend transaction store; client stores snapshot version only | On reconnect or uncertain command result, fetch authoritative snapshot and retry same idempotency key. |
| Session and scopes | Identity service; server checks every request | On expiry clear private caches, disconnect streams and reauthenticate. |
| Form draft | Component/session state for non-sensitive values | Preserve across recoverable validation failure; prompt before navigation; no secrets in localStorage or URL. |
| Listing filters | URL query when non-sensitive | Back/forward navigation and sharing reproduce public filters. |
| UI preference | Local device storage only with consent as required | Validate defaults and honor reduced motion. |
| Search results | Versioned cached projection | Revalidate on focus and before binding action; mark stale. |

Use server state cache with scoped query keys, invalidation after mutation and no cross-user reuse. Sensitive identity documents and contract bodies do not enter persistent client caches. Optimistic edits are suitable for reversible preferences only; never optimistically show a bid, payment or signed contract as committed. Test logout, organization switching, version conflicts and multi-tab session revocation.

## Cache key and reset specification

Query identity includes resource type, resource ID or normalized filter hash, current principal ID, organization/branch scope, representation version and locale/currency where applicable. Public and private queries use distinct stores. Entity tags belong to the exact returned representation; a collection tag cannot authorize mutation of an item. A command receipt is associated with the intended operation, payload hash and principal; logout removes browser-held payload while the server keeps its durable receipt.

State transitions for a binding command are `idle → validating → submitting → committed | rejected | unknown`; `unknown → reconciling → committed | rejected | unknown`. There is no `unknown → idle` transition that allocates a new key automatically. Editing amount after a definitive rejection creates a new intent; editing while unknown requires resolution first. Form dirty state is independent of server object version. A new server version shows a comparison and requires confirmation rather than silently replacing dirty fields. Multi-tab logout or organization change disconnects streams, aborts pending reads, clears all private caches and restores only non-sensitive preferences. Cross-tab messages carry revocation signal and epoch, never credentials or record bodies.
