# Contract Workflow

| Metadata | Value |
|---|---|
| ID / version | 12/07_CONTRACT_WORKFLOW / 0.1 |
| Status | Proposed; legal, finance and auction policies unapproved |
| Owner / reviewers | Auction and finance architecture / legal, operations, security, QA |
| Updated | 2026-11-15 |
| Scope | Contract Workflow; no authority to transfer funds or ownership is implied. |

## Template to executed evidence
1. Legal publishes a jurisdiction- and model-specific approved template version with effective dates and authorized clauses. Transactions retain the exact version and generated document hash.
2. Authorized transaction staff verify seller/buyer identity, vehicle, offer, parties, amounts, obligations and title evidence; unresolved mismatches block generation.
3. Generate a draft with explicit variable values; legal or designated reviewer approves changes. Corrections or amendments produce new versions with provenance; no silent replacement.
4. Request signatures via lawful approved provider or collect external evidence. Verify signer identity, document hash, timestamp and provider signature; duplicate callbacks are idempotent. Provider timeout remains pending.
5. Mark executed only when all required parties' verified signatures and approvals are present. Preserve the signed file in encrypted private storage with immutable metadata. Notify parties without including sensitive document contents.
6. Record ownership-transfer workflow and evidence separately. Contract execution alone is not settlement or title transfer.

Actor roles: operator prepares, legal reviewer approves template or exception, authorized participant signs, provider attests within its mandate. Require independent approval for critical amendments and record reason. Decline, expired request, identity mismatch, inaccessible provider and dispute enter a held queue with owner and deadline. Jurisdiction, signature validity, contract text and retention are DEC-01/05/07 decisions. QA tests document substitution, revoked links, out-of-order callbacks, unsigned contract and post-signature amendment.

## Consumer-origin transaction and shared closure

A consumer inquiry is nonbinding. `createConsumerOffer` requires the exact seller-authorized price, currency, terms version, expiry and evidence; the assigned buyer reads it through `readConsumerOffer`. `acceptConsumerOffer` atomically checks the listing's authoritative availability and channel reservation, buyer identity, current offer and post-lock time, and records consent plus one transaction and pending title-transfer record. Competing acceptance yields one accepted reservation and a conflict for the other; an issued offer is not itself a reservation. `withdrawConsumerOffer` works only before acceptance; the same lock order prevents accept/withdraw races. Accepted offers use the existing contract, obligation, title and physical-delivery workflows.

`TransactionCase.channel` selects one origin: dealer auction requires an accepted SellerDecision and AuctionResult; consumer requires an accepted ConsumerOffer. No generic staff state change may fabricate either origin. Buyer and seller party references are required; a buyer organization is required only for the dealer channel. Closure requires current verified contract, reconciled required obligations, verified title evidence and the required handover under pinned policy. A later payment reversal or title dispute places a linked exception on the case without erasing the prior closure audit. The legally binding point is determined by approved market terms, not by the word “accepted” in a UI status.

**Acceptance fixtures:** two buyers accepting the same available listing; offer expires while waiting for lock; listing enters auction before acceptance; stale terms; withdrawn seller authority; lost acceptance response; unauthorized advisor; accepted offer attempting withdrawal. Each has either one canonical transaction or zero, and never duplicated obligations.
