# Auction Engine Spec

| Metadata | Value |
|---|---|
| ID / version | 12/01_AUCTION_ENGINE_SPEC / 0.1 |
| Status | Proposed; legal, finance and auction policies unapproved |
| Owner / reviewers | Auction and finance architecture / legal, operations, security, QA |
| Updated | 2026-11-15 |
| Scope | Auction Engine Spec; no authority to transfer funds or ownership is implied. |

## Scope and operating assumptions
**PROPOSED:** A controlled auction allows eligible dealer organizations to bid on an inspected vehicle; it records an auction outcome for seller consideration. It does not itself prove a binding sale, payment, or title transfer. Each auction pins immutable inspection revision, approved policy version, currency, start/end instants and vehicle reference. DEC-04 requires commercial/legal approval of bid binding effect, eligible participants, reserve and all closing rules before launch.

| State | Allowed transition and guard | Side effects / failure |
|---|---|---|
| Draft | → Scheduled by authorized operator with approved policy, available vehicle, complete inspection revision, eligible dealer pool and valid time interval | Record review, audit and outbox; invalid data remains draft. |
| Scheduled | → Open after authoritative clock reaches start and prerequisites still hold | Publish snapshot; failure holds and alerts operator. |
| Open | → Closed by close worker after deadline under same auction lock as bid | Compute qualifying result from committed bids and approved rules; one result, audit and outbox. |
| Draft/Scheduled/Open | → Cancelled only through authorized policy-specific incident procedure | Record reason, approvals and participant notices; accepted bids remain preserved. |
| Closed | terminal for auction; seller decision is a separate workflow | Reopening requires a new auction with explicit link and approved relist policy. |

A report correction during an open auction creates a separate version and raises an operational hold; whether to pause, extend or cancel is policy-dependent. No accepted bid is editable or silently removed. Real-time feed is a projection; use [concurrency](03_AUCTION_CONCURRENCY.md) for the binding transaction. Acceptance tests include same-auction bid/close races, revocation, stale report, duplicate keys, deadline clock faults and gateway outage. Owner: auction product and architecture; operations, legal, security and QA must approve policy.
