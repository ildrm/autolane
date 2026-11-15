# Seller Acceptance Workflow

| Metadata | Value |
|---|---|
| ID / version | 12/04_SELLER_ACCEPTANCE_WORKFLOW / 0.1 |
| Status | Proposed; legal, finance and auction policies unapproved |
| Owner / reviewers | Auction and finance architecture / legal, operations, security, QA |
| Updated | 2026-11-15 |
| Scope | Seller Acceptance Workflow; no authority to transfer funds or ownership is implied. |

## Offer decision
| State | Transition / actor | Guard and result |
|---|---|---|
| Pending presentation | → Presented by authorized operations | Qualifying finalized outcome, seller identity and permitted offer details confirmed; record immutable offer version, amount/currency and notification attempt. |
| Presented | → Accepted by authenticated seller | Explicit acceptance of current offer and approved terms before policy deadline; record actor, timestamp, offer version and policy version in one transaction. |
| Presented | → Rejected by authenticated seller | Explicit rejection with optional reason; preserve outcome and route to no-sale or authorized relist review. |
| Presented | → Expired by scheduler | Only if approved deadline exists and authoritative clock confirms expiry; notify and route to operator. |
| Any unresolved | → Held by authorized operator | Identity, report or dispute exception; record reason, scope and review task; do not fabricate seller decision. |

A seller retry with same idempotency key and payload returns original decision; conflicting versions or a competing decision return conflict and current authorized state. No response does not mean consent. Notification delivery is not presentation acceptance. Once accepted, contract workflow starts as a separate action; sale, payment and ownership remain unconfirmed. Deadline, right to withdraw and remedies await DEC-04 and legal approval. Test simultaneous accept/reject, stale offer, expired session, unreachable seller and notification failure.

## Creation and race boundary

Acceptance and expiry lock the same current offer record and compare trusted time with its explicit expiry. The exact offer version and seller identity must match. First accepted decision atomically records SellerDecision, creates one TransactionCase plus pending OwnershipTransfer, and writes receipt/audit/outbox; unique result linkage prevents duplicates. Rejection or expiry creates no sale case. Contract issuance and obligations require their own reviewed commands. Scope revalidation precedes replay; a new key cannot reverse an already effective decision. An authorized legal correction is a new evidence-backed case, not an overwrite.
