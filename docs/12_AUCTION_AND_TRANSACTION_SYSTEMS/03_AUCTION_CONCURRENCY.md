# Auction Concurrency

| Metadata | Value |
|---|---|
| ID / version | 12/03_AUCTION_CONCURRENCY / 0.1 |
| Status | Proposed; legal, finance and auction policies unapproved |
| Owner / reviewers | Auction and finance architecture / legal, operations, security, QA |
| Updated | 2026-11-15 |
| Scope | Auction Concurrency; no authority to transfer funds or ownership is implied. |

## Consistency and linearization
All accepted bids and the close transition for an auction serialize on the same authoritative primary database row. The sequence and result are determined inside the transaction, not by gateway arrival, application wall clocks or broker order. The proposed decision point is the **authoritative database clock read after the auction row lock is acquired**: accept only when state is open, current policy/eligibility checks pass, and that reading is strictly before `closes_at`. A transaction may commit after the deadline if it validly obtained the lock and passed the pre-deadline check; the close transaction waits behind it and includes that committed bid. This semantic is provisional and requires DEC-04 approval. A bid that acquired the lock after close or after the deadline is rejected. Do not use transaction-start timestamps for this check.

Bid transaction: (1) authenticate principal and resolve idempotency key; (2) lock or otherwise transactionally protect dealer eligibility and auction state in a fixed documented lock order; (3) use authoritative post-lock time, verify status, eligibility, pinned policy, currency, increment and exact integer amount; (4) append accepted bid with unique auction sequence, update current price/version, persist idempotency result, audit and outbox; (5) commit, then acknowledge. A rejection that must replay is stored as an idempotency result in its own consistent transaction. Same key with different request hash returns conflict. **Eligibility race:** suspension and bid acceptance must contend on the same eligibility row or another proven serializable/versioned guard; “checked at login” is insufficient. Establish uniform lock ordering for suspension, bid and close to avoid deadlocks; retry a deadlock with the same key only after checking outcome.

Close transaction locks auction, reads trustworthy DB clock, checks deadline and state, determines highest qualifying committed bid under pinned rules, inserts unique result, transitions to closed and persists audit/outbox atomically. No external call is made while holding locks. Unique constraints enforce `(auction_id, sequence)`, one result per auction and principal/operation/key identity. DB primary outage or unhealthy clock means no acceptance or finalization; failover recovery reconciles acknowledgements and external effects before reopening.

**Verification:** run concurrent bidders with equal/different amounts around the boundary, concurrent suspension and close, process crash after commit before response, deadlock and primary failover. Assert one consistent ordered history, one result, no accepted bid missing from result and identical outcome on duplicate-key replay. Throughput targets must be load-tested with representative hot auctions; connection pools and fairness need operational review.

## Fixed lock order and replay access

Acquire idempotency namespace, organization eligibility, membership/grant, then auction row in that order. Multi-record operations sort IDs within each class. Close only needs the auction row and does not subsequently request organization locks; suspension uses organization/membership locks and does not acquire auction locks. No code path may invert the order. Sample a non-transaction-start clock after acquiring all required locks; fail closed on untrusted clock/failover. Recheck current actor/object access before replaying a stored result; do not leak a previous private response after membership revocation. Binding receipt tombstones prevent a timed-out retry from creating another accepted bid after cache expiry. PostgreSQL distinction: [clock_timestamp versus transaction timestamps](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT), accessed 2026-11-15.

## Material inspection corrections and exclusive sale channel

A material correction to a report relied on by a live auction takes the affected auction lock, marks the safety hold and creates the new inspection revision in the same local database transaction before acknowledging the correction. Bids recheck that hold under the auction lock. Sending only an asynchronous correction event would permit bids against known-invalid evidence and is insufficient. Multi-auction affected rows lock in sorted ID order; correction never acquires organization/member locks after auction locks. Admission reads the pinned revision/hold state on the auction, avoiding reverse lock order with inspection. Events notify reviewers and clients after commit.

The active vehicle-channel reservation is acquired before an auction can schedule or a consumer offer can be accepted. Channel changes and consumer acceptance serialize on that reservation; a published consumer listing alone need not reserve a vehicle, but it must not advertise active availability while an exclusive dealer auction is committed. If conflict occurs, reject and retain the existing channel until an approved withdrawal/cancellation process completes.
