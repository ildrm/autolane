# Auction Api

| Metadata | Value |
|---|---|
| ID / version | 10/04_AUCTION_API / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Backend and architecture leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Auction Api; commercial and jurisdiction-dependent policy decisions remain open. |

## API-09 — Snapshot
`GET /v1/auctions/{id}` returns `id`, `status`, `currency`, `current_bid_minor` (nullable), `sequence`, `server_time`, `closes_at`, `report_revision_id` and policy-permitted bidder information. Active dealer organization and auction eligibility are checked at request time; responses are `Cache-Control: private, no-store`. A snapshot is authoritative at its sequence, but may already be stale by the time the next command arrives.

## API-10 — Place bid
`POST /v1/auctions/{id}/bids` with `Idempotency-Key` and body `{amount_minor: integer, currency: ISO-4217}`. Actor must have active authenticated session, active dealer organization and explicit bidder grant; auction, vehicle and pinned inspection must meet the approved eligibility policy. On the authoritative primary the service locks the auction, checks DB time `< closes_at`, validates status, currency, approved increment and eligibility, and appends bid + aggregate sequence + idempotency outcome + audit + outbox in one commit. Return `201` with `{bid_id, auction_id, amount_minor, currency, sequence, accepted_at, status:"accepted"}` only after commit.

A same-key same-payload retry returns the original status/body, including rejection if stored; same key different payload returns `409 IDEMPOTENCY_CONFLICT`. `409 AUCTION_CLOSED`, `BID_TOO_LOW`, `ELIGIBILITY_CHANGED`, `IDEMPOTENCY_CONFLICT`; `422 INVALID_AMOUNT` or `CURRENCY_MISMATCH`; `403 FORBIDDEN`; `429 RATE_LIMITED`; `503 AUTHORITY_UNAVAILABLE`. `BID_TOO_LOW` may include only policy-permitted latest snapshot. Network timeout is an **unknown outcome**; retry the same key and inspect snapshot, never assume rejection. The clock/close, increment, tie and cancellation policies remain DEC-04 and must be formally approved before release.

## API-11 / API-12 — Close and seller decision
A scheduler or privileged manager requests close, locks the same auction row, rechecks authority and records exactly one result plus outbox. Close before deadline fails absent an approved cancellation operation. Seller sees offer terms and report context then explicitly accepts or rejects using identity, version and policy deadline; decision is separate from contract, settlement and title. Tests exercise bid-close races, duplicate requests, replay after failover, revoked bidder, hidden reserve and notification failure.
