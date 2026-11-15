# Bidding Rules

| Metadata | Value |
|---|---|
| ID / version | 12/02_BIDDING_RULES / 0.1 |
| Status | Proposed; legal, finance and auction policies unapproved |
| Owner / reviewers | Auction and finance architecture / legal, operations, security, QA |
| Updated | 2026-11-15 |
| Scope | Bidding Rules; no authority to transfer funds or ownership is implied. |

## Binding rules and approval status
**DECISION REQUIRED:** the current increment, reserve treatment, withdrawal rights, seller response deadline, tie and remedy rules are not approved. The following is a proposed computational baseline, disabled for production until a policy version is signed by product, commercial operations and legal.

| Rule | Proposed behavior / guard | Acceptance check |
|---|---|---|
| Eligibility | Active verified dealer, active membership and explicit bid grant for this auction; recheck at acceptance, not only at page load. | Suspension races with bid under defined lock/version ordering; no later bid accepted after effective suspension. |
| Amount | Positive integer minor units in auction currency; minimum starting amount and stepped increment from pinned policy. | Wrong currency and non-incremented amount return definitive rejection without mutation. |
| Timing | Accept only while status open and authoritative timestamp after lock is strictly earlier than `closes_at`. | Bid at exactly close is rejected; clock uncertainty fails closed. |
| Ordering | Each accepted bid gets a sequence under the same auction lock; no reliance on device time. | Equal simultaneous requests cannot both occupy one sequence; ranking follows approved price/tie policy. |
| Idempotency | Same actor/key and same payload replays stored result; different payload conflicts. | Lost acknowledgement and retry create one bid only. |
| Confidentiality | Broadcast price and sequence; disclose bidder identity and reserve only to permitted actors. | Other dealers cannot read hidden identity or reserve from API or stream. |
| Result | After close, highest qualifying accepted bid is a proposed default, subject to reserve and tie policy; seller acceptance is separate. | No bid or unmet approved reserve yields no qualifying offer; no contract generated automatically. |

Proxy bids, automatic limits, anti-sniping extensions, deposits, private auctions, credit and post-auction negotiation are optional and disabled until independently approved. Buyer default, seller withdrawal, cancellation and relisting require contractual remedies, operator workflow and notice; do not invent a forfeiture or fee.
