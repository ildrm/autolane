# Indexing Strategy

| Metadata | Value |
|---|---|
| ID / version | 09/05_INDEXING_STRATEGY / 0.3 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Indexing Strategy; jurisdiction-dependent policy decisions remain open. |

## Query-driven indexes
| Query | Candidate index | Guardrail |
|---|---|---|
| Auction listing by status and close | `(status, closes_at, id)` | Partial open-state index only if query predicates are stable. |
| Bid history | unique `(auction_id, sequence)` and `(auction_id, accepted_at)` | Sequence is definitive ordering; timestamp alone is not tie breaker. |
| Idempotent bid replay | unique `(principal_id, operation_id, command_key)` | Scope and expiry documented; retain bid outcomes beyond ordinary request cache. |
| Branch schedules | `(branch_id, starts_at, status)` | Capacity enforced by locked slot or exclusion rule, not index alone. |
| Work queue | `(assignee_id, status, updated_at)` | Add scope and age; verify real plans and cardinality. |
| Provider lookup | unique `(provider_id, provider_ref)` where reference exists | Avoid exposing provider reference to unauthorized users. |
| Vehicle identity | keyed/hash lookup for normalized VIN plus controlled decryption | Protect low-entropy identifiers from dictionary attacks. |

Measure query plans, p95 latency, insert overhead, bloat and storage under representative scale; remove unused redundant indexes. Search index is derived and cannot enforce authoritative eligibility or price. Index creation and migrations must be reviewed for blocking and rollback; avoid indexing unbounded personal text.

## Additional correctness and operational access paths

| Relation | Constraint / access path | Purpose |
|---|---|---|
| InspectionRevision | Unique `(inspection_id, revision_number)` | Immutable revision identity and deterministic history. |
| InspectionFinding | Unique `(revision_id, item_id)` | No duplicate response to an item in one report revision. |
| SellerDecision | Unique effective `(auction_result_id, offer_version)` | Replays and simultaneous seller decisions cannot create two outcomes. |
| TransactionCase | Unique non-null auction result OR consumer offer origin | Each accepted commercial origin yields one case. |
| VehicleChannelReservation | Unique active `vehicle_id` | Prevent simultaneous auction and consumer sale commitments. |
| PaymentAllocation | Unique `(source_payment_id, obligation_id, allocation_reference)` plus locked source total | Prevent duplicate allocation and over-allocation under concurrent reconciliation. |
| InboxReceipt | Unique `(provider_id, provider_event_id)` | Same ID/different hash quarantined; ordinary duplicate safely acknowledged. |
| OutboxEvent | `(delivery_state, next_attempt_at, event_id)` | Bounded worker batches without scanning full history. |
| PolicyVersion | Unique `(policy_id, version)` | Independently approved immutable policy references. |
| PrivacyRequest | `(status, due_at, assigned_to)` within privacy scope | Due-date work queue without indexing identity content. |
| ConsumerOffer | `(buyer_id, status, expires_at, id)` | Own offers, expiry processing and stable pagination. |

Candidate indexes remain logical specifications, not automatically executable DDL. Query evidence must show representative cardinality, tenant skew, hot-auction write contention and p95/p99 planning outcomes. A partial index's predicate must exactly match lifecycle semantics; adding a new active state requires reviewing uniqueness and queries together.
