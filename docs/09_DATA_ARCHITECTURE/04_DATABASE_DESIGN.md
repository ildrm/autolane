# Database Design

| Metadata | Value |
|---|---|
| ID / version | 09/04_DATABASE_DESIGN / 0.3 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Database Design; jurisdiction-dependent policy decisions remain open. |

## Logical storage design
PostgreSQL is proposed as the authoritative store; each domain has a schema/module-owned tables and constrained foreign keys where transaction boundaries permit. Use UUID primary keys; enum-like states are validated by explicit state-transition logic and database checks. Store all money as signed 64-bit minor-unit integers plus ISO currency and an approved exponent/rounding policy reference. Avoid binary floating point. Timestamps use UTC, with branch timezone stored separately for slot display.

Within one transaction take locks in the common order: idempotency receipt, organization eligibility, member/grant, then auction; validate eligibility, price, policy version and database-authoritative post-lock time; append bid, increment sequence, store idempotency outcome and insert audit/outbox, then commit. The close worker locks the same row and determines a result only after the deadline. Constraints enforce unique aggregate sequence, one result per auction, provider-scoped references and command idempotency. Published inspection report revisions and posted ledger entries are append-only; corrections are new revisions or reversing journals.

Use read replicas only for nonbinding, lag-tolerant reads. Encrypt private files in object storage and store metadata and integrity hash in the database. Test restore and replay, constraint behavior, lock contention, transactional rollback and failover before production. Partition audit and analytics by time only after retention and operational needs are established; avoid partition choices that weaken global uniqueness. Availability and recovery targets need validation against actual deployment.

## Transaction boundaries and isolation choices

| Command family | Rows locked / unique invariant | Commit and recovery |
|---|---|---|
| Book/reschedule | Slot rows in sorted ID order, appointment; unique active reservation | Capacity decrement/increment, appointment, receipt, audit/outbox together. Recheck branch calendar after lock. |
| Bid | Receipt → organization → member/grant → auction | Accepted bid and sequence written once; rejection receipt has no leader mutation. No network calls while locked. |
| Auction close | Auction and unique auction-result origin | Same serial cutoff as bids; repeat close returns same result. Close never acquires member locks after auction lock. |
| Publish report | Inspection and current draft revision | Reviewer separation, exact revision checksum, publication and correction/safety-hold intents atomic. |
| Accept offer | Receipt → vehicle channel/listing reservation → offer/result | One effective accepted origin and transaction; concurrent channel publication uses same reservation guard. |
| Reconcile obligation | Obligation, source allocations and reconciliation revision in sorted IDs | Sum and currency checked; no source amount allocated twice; independent approver and no inferred bank movement. |
| Close transaction | Case and current domain milestone versions | Verify facts under consistent snapshot/locking or detect concurrent version change; do not close on eventual BI projection. |

Proposed default is ordinary transaction isolation plus explicit row locks and uniqueness checks for these invariants. A cross-row predicate that cannot be represented by a locked parent or unique constraint requires serializable isolation with bounded same-intent retries, not an unprotected “check then insert.” A deadlock/serialization victim retries at most twice with its original key and payload; otherwise return an unknown/retryable outcome after checking receipt. Never hold DB locks while calling a payment, registry, scanning or messaging provider. The outbox records the intent; authenticated completion is a later transaction.

The implementation must protect domain ownership at both application and DB role boundaries. Migration planning uses expand/backfill/verify/contract, preserves old readers for a compatibility window and verifies restore/rollback before dropping fields. No migration script is included in this phase. [PostgreSQL locking documentation](https://www.postgresql.org/docs/current/explicit-locking.html) describes the underlying lock mechanisms; this project's lock order and invariants are design decisions.
