# Event Contracts

| Metadata | Value |
|---|---|
| ID / version | 10/08_EVENT_CONTRACTS / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Backend and architecture leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Event Contracts; commercial and jurisdiction-dependent policy decisions remain open. |

## Domain event envelope
All messages are versioned, minimally scoped, at-least-once and contain `{event_id, type, schema_version, occurred_at, aggregate_type, aggregate_id, aggregate_sequence, tenant_id, correlation_id, causation_id, payload}`. `event_id` is unique, timestamps UTC, IDs opaque; aggregate sequence is monotonic per aggregate, not a global order. Payload excludes identity documents and payment instruments. A transaction writes business state and outbox together; consumer writes inbox and projection together. Consumers must deduplicate and handle version gaps and replay.

| Type v1 | Required payload | Consumer and constraints |
|---|---|---|
| `appointment.confirmed` | appointment_id, branch_id, starts_at, version | Reminder service; destination fetched through scoped API, not payload. |
| `inspection.report_published` | inspection_id, revision_id, vehicle_id | Auction operations checks eligible report; no private report content. |
| `auction.bid_accepted` | auction_id, bid_id, amount_minor, currency, sequence | Gateway applies visibility policy before broadcast; analytics receives pseudonymized form. |
| `auction.closed` | auction_id, result_id, outcome, sequence | Seller decision task and allowed notification; winner identity restricted. |
| `seller.decision_recorded` | result_id, decision, decision_version | Contract coordination only on accepted outcome; reject/expiry not a sale. |
| `contract.signed` | contract_id, signed_version | Transaction state evaluator, not automatic payment. |
| `settlement.reconciled` | obligation_id, reconciliation_id, currency | Transaction evaluator, never proof of title transfer. |
| `vehicle.handover_recorded` | transaction_id, handover_id | Logistics and transaction evaluator; custody does not prove ownership. |

Delivery status is an event distinct from domain state. Schema changes add optional fields compatibly; changed semantics use a new type version. On permanent error quarantine with alert and audited replay, never drop silently. Test duplicates, out-of-order messages, consumer failure after processing and unauthorized subscription.

## Expanded contract baseline — revision 0.3

The [state machine catalog](../03_USER_JOURNEYS_AND_SCENARIOS/05_STATE_MACHINE_CATALOG.md) additionally defines `lifecycle.transition_recorded` v1 with aggregate type/ID, transition ID, prior/new state and aggregate version, using this document’s envelope. Emit in the same transaction as domain state and audit; named events keep their distinct semantics. Analytics projection is separately purpose-gated.

## Machine-readable schema and consumer obligations

[Domain event v1 JSON Schema](../contracts/domain-event.schema.json) defines the exact envelope and 13 payload variants, including lifecycle, consumer acceptance, verified title, content publication and privacy completion. `tenant_id` is nullable only for a genuinely cross-market aggregate; null never means public access. `causation_id` may be null for an originating scheduled action; correlation remains required. Enforce UUID and UTC formats as well as structural validation. Sequence belongs to the aggregate, not the transport partition. An event schema is not permission to subscribe.

An internal event may contain a restricted evidence ID; the gateway must construct a separate authorized DTO and cannot broadcast raw payload. Privacy completion conveys only the request and disposition to restricted workflow consumers, never the requester's identity or exported data. Consumer acceptance emits `consumer.offer_accepted` atomically with the transaction origin and reservation. Title verification emits `ownership.transfer_verified` only after independent evidence verification. Content publication emits the approved revision for cache/search invalidation; it carries no draft body.

Consumer contract: deduplicate event ID; verify allowed type/version and aggregate scope; apply a contiguous aggregate revision or fetch authoritative state; persist inbox receipt with projection changes; acknowledge only after commit. Same ID/different content hash is an integrity incident. Poison messages are quarantined with schema/error code, restricted pointer and operator owner, not silently dropped. A reviewed replay preserves original event ID and occurrence time, adds replay metadata outside the immutable event and never repeats a binding business command.

Contract examples and negative fixtures validate payload shape only; they cannot prove a producer writes its outbox atomically. Implementation tests must kill the worker before/after acknowledgement, reorder related events, revoke subscription permission and deliver a reversal after earlier reconciliation. Named operation aliases and generic transition commands invoke the same domain handler, authorization, version check and idempotent origin invariant; duplicate API surfaces must never bypass maker/checker or create a second event for the same transition.
