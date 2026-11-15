# Api Catalog

| Metadata | Value |
|---|---|
| ID / version | 10/02_API_CATALOG / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Backend and architecture leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Api Catalog; commercial and jurisdiction-dependent policy decisions remain open. |

## Conventions
All paths are under `/v1`; JSON request/response uses UTF-8 and RFC 3339 UTC timestamps. Opaque UUIDs identify resources; amount is integer `amount_minor` plus uppercase ISO `currency`. Session-based browser requests require CSRF defense; JWT/access-token deployments require audience, issuer, expiry and revocation checks. Every authenticated operation evaluates action, actor, organization/branch and object scope server-side. Mutation requires `Idempotency-Key` (bounded ASCII, 1–128 characters) and `If-Match` version for editable resources unless listed otherwise. Same actor/key/payload replays prior response; same key with different payload returns `409 IDEMPOTENCY_CONFLICT`. Validation returns `422`; authentication `401`, scope denial `403` (or approved non-disclosing `404`), failed `If-Match` precondition `412`, other domain conflicts `409`, rate limit `429`, dependency unavailable `503`; error envelope is in [error standards](10_ERROR_HANDLING_STANDARDS.md). Do not log personal payloads or bearer tokens.

| ID | Method / path | Actor; input → success | Key restrictions / behavior |
|---|---|---|---|
| API-01 | POST `/auth/sessions` | User credentials or provider assertion → session | Rate-limit per account and network; generic failure; MFA per risk policy. |
| API-02 | POST `/seller-leads` | Seller; vehicle, contact, consent → 201 lead | Verify consent version and input; deduplicate for review, not silent merge. |
| API-03 | GET `/branches` | Visitor; area/page → public branch list | Excludes staff and nonpublic capacity. |
| API-04 | POST `/appointments` | Seller or authorized staff; lead, slot → 201 booking | Lock capacity; full slot returns `409 SLOT_UNAVAILABLE`. |
| API-05 | POST `/inspections/{id}/revisions` | Assigned inspector; findings and evidence refs → 201 draft | Validate template version, branch and evidence scan status. |
| API-06 | POST `/inspections/{id}/publish` | Inspection supervisor; revision/version → 200 report | Immutable revision; correction requires new revision. |
| API-07 | POST `/valuations` | Pricing analyst; vehicle/report revision → 201 estimate | Preserve input/policy version and approval; no guarantee. |
| API-08 | POST `/auctions` | Auction manager; vehicle, report revision, pinned rule policy, time → 201 draft | Reject absent approved policy or inaccessible evidence. |
| API-09 | GET `/auctions/{id}` | Eligible dealer or authorized staff → authoritative snapshot | Scope and visible field filtering; reserve only if approved. |
| API-10 | POST `/auctions/{id}/bids` | Active bidder; amount/currency → committed result | Serialize with close; actor+idempotency key required; see [auction API](04_AUCTION_API.md). |
| API-11 | POST `/auctions/{id}/close` | Scheduler service or approved manager → result | Same lock as bid; server time and policy checks; one immutable outcome. |
| API-12 | POST `/auction-results/{id}/seller-decision` | Authorized seller; accept/reject → decision | Current offer, identity, approved deadline and explicit consent required. |
| API-13 | POST `/dealer-verifications/{id}/decision` | Reviewer; approve/reject and reason → status | Separation of duties and organization scope; audit. |
| API-14 | GET `/listings` | Visitor; validated filter/sort/cursor → public cards | Only consumer-published listings; search is eventual. |
| API-15 | POST `/purchase-requests` | Buyer; listing, contact/consent → inquiry | Recheck availability in authoritative store; notify assigned advisor. |
| API-16 | POST `/contracts/{id}/signatures` | Authorized party/provider; verified signature evidence → status | Provider callbacks authenticated, scoped and deduplicated; no inferred settlement. |
| API-17 | POST `/obligations/{id}/evidence` | Finance operator; evidence ref, claimed amount/currency → 202 review | Does not move funds or mark reconciled. |
| API-18 | POST `/reconciliations/{id}/approve` | Independent finance approver; matching evidence/version → status | Four-eyes check; discrepancy blocks closure. |
| API-19 | POST `/deliveries/{id}/handover` | Assigned operator; condition/evidence → status | Physical custody distinct from ownership transfer. |
| API-20 | POST `/support-tickets` | Authorized party; case, description → 201 | Limit evidence access and redact sensitive input from logs. |
| API-21 | POST `/admin/policies/{id}/versions` | Privileged administrator; policy content, reason → pending approval | Version immutable, second approval for critical rules, old transactions pinned. |
| API-22 | GET `/analytics/metrics` | Authorized analyst; allowed aggregate and period → results | Scope, privacy threshold, no row-level personal data without justification. |

List endpoints use page size 1–100 (default 25), opaque signed cursor containing sort position and filter hash, stable sort including ID; invalid cursor returns `400`. Set route-specific rate limits after capacity and abuse testing; provisional bidder limit 30 commands/minute per actor plus network throttling, with clear `Retry-After`, is not a commercial rule. Audit all privileged, sensitive reads and binding actions; minimally track domain outcome as specified in [events](08_EVENT_CONTRACTS.md). The original API-01–22 inventory is retained for compatibility. The expanded [operation index](12_OPERATION_INDEX.md) contains 114 formally described operations. OpenAPI 3.1 validation and documentation fixtures are recorded in [validation evidence](../review/contract-validation.json); business behavior, providers and live policies require separate verification.
