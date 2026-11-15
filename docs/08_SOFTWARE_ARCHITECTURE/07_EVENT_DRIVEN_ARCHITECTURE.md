# Event Driven Architecture

| Metadata | Value |
|---|---|
| ID / version | 08/07_EVENT_DRIVEN_ARCHITECTURE / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Event Driven Architecture; jurisdiction-dependent policy decisions remain open. |

## Publish and consume
On the same database commit as a domain transition, insert an outbox record with event ID, type, schema version, aggregate ID, aggregate sequence, occurred-at UTC, tenant scope, correlation/causation IDs and minimal payload. Relay publishes at least once and marks delivery only after broker acknowledgement. Consumers store processed event ID in an inbox transaction with their projection changes. Ordering is guaranteed only within a single aggregate where explicitly specified; cross-aggregate consumers resolve dependencies and reconcile snapshots.

| Producer | Event | Consumer and action |
|---|---|---|
| Scheduling | appointment.confirmed.v1 | Notification schedules reminder; CRM projects stage. |
| Inspection | inspection.report_published.v1 | Auction preparation pins immutable revision; audit records approver. |
| Auction | auction.bid_accepted.v1 | Gateway broadcasts permitted price/version; analytics receives minimized event. |
| Auction | auction.closed.v1 | Seller decision workflow creates notification and task. |
| Contracts | contract.signed.v1 | Transaction workflow reevaluates readiness, not settlement. |
| Settlement | settlement.reconciled.v1 | Transaction workflow reevaluates closure, not title transfer. |

Broker outage leaves committed outbox rows for retry. Malformed or repeated permanent failures enter a dead-letter queue with alert, operator owner, safe replay and no payload secrets. Event IDs are distinct from analytics events, which must not leak bidder identity. Schema changes add fields compatibly; breaking meaning requires a new version and consumer migration. Event occurrence is not proof of email delivery or external payment.
