# Auction security

| Metadata | Value |
|---|---|
| Document ID | 14/06_AUCTION_SECURITY |
| Version / status | 0.1 / proposed; security and legal review required |
| Owner | Auction Security Lead |
| Reviewers | Product, Architecture, Security, Privacy, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Auction security for proposed marketplace; applicable legal obligations remain unresolved. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Bidding integrity

Only an authenticated, approved and non-suspended dealer member with explicit bid permission for that organization and auction may submit a bid. Server validates current eligibility, auction state, authoritative time, increment and any approved limit inside the same serialized decision boundary that appends an accepted bid. Reject client-supplied timestamps as authority. Idempotency key binds actor, auction and request payload; replay returns original result, while key reuse with different payload is rejected. Bid acknowledgements and outbox publication follow durable commit.

The live channel authenticates subscription and filters messages by auction eligibility; never expose private bidder identity, reserve or other dealer data unless the approved policy explicitly allows it. Reconnection retrieves current authoritative snapshot and sequence, then fills any available gap; if a gap cannot be recovered show a stale indicator and reload rather than guess. A server-side close and bid request must serialize so that the selected ordering is consistent with the approved deadline rule.

## Abuse and operations

Rate-limit without silently dropping accepted bids. Detect unusual synchronized bids, many identities, repeated cancellations and access anomalies as investigation signals, not automatic findings of fraud. Auction interventions require reason, evidence, authorization and immutable history. Pause, cancellation and post-interruption recovery require business and legal policy approval; do not extend or alter deadlines silently.

## Acceptance

Run simultaneous valid bids and close requests repeatedly; each accepted bid has a unique durable order and one consistent outcome. Replaying a bid does not create another. Unauthorized subscriptions get no confidential payload. Disconnect after commit reconciles the same outcome on reconnect. Signed administrator actions and all exceptions are auditable.
