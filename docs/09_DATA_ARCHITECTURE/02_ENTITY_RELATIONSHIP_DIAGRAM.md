# Entity Relationship Diagram

| Metadata | Value |
|---|---|
| ID / version | 09/02_ENTITY_RELATIONSHIP_DIAGRAM / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Entity Relationship Diagram; jurisdiction-dependent policy decisions remain open. |

## Conceptual relationships
```mermaid
erDiagram
 USER ||--o{ ORGANIZATION_MEMBER : joins
 ORGANIZATION ||--o{ ORGANIZATION_MEMBER : includes
 ORGANIZATION ||--o| DEALER_ACCOUNT : holds
 USER ||--o{ SELLER_LEAD : submits
 SELLER_LEAD }o--|| VEHICLE : concerns
 BRANCH ||--o{ APPOINTMENT : hosts
 SELLER_LEAD ||--o{ APPOINTMENT : schedules
 VEHICLE ||--o{ INSPECTION : receives
 INSPECTION ||--o{ INSPECTION_REVISION : versions
 VEHICLE ||--o{ VALUATION : has
 VEHICLE ||--o{ AUCTION : enters
 INSPECTION_REVISION ||--o{ AUCTION : pins
 AUCTION ||--o{ BID : records
 ORGANIZATION ||--o{ BID : places
 AUCTION ||--o| AUCTION_RESULT : closes
 AUCTION_RESULT ||--o{ CONTRACT : coordinates
 CONTRACT ||--o{ PAYMENT_OBLIGATION : defines
 PAYMENT_OBLIGATION ||--o{ RECONCILIATION_RECORD : checked
 VEHICLE ||--o{ VEHICLE_HANDOVER : transfers_custody
 VEHICLE ||--o{ VEHICLE_LISTING : publishes
```
Cardinality is conceptual: contract and obligation creation depends on the approved legal model, while a vehicle may appear in multiple auctions at different times but must not have multiple concurrently active auctions unless specifically approved. A published inspection revision is immutable and may be shared by multiple authorized auctions. Sensitive source documents have separate protected storage and are not embedded in public search records.

## Transaction and evidence relationships

```mermaid
erDiagram
 AUCTION_RESULT ||--o| SELLER_DECISION : receives
 SELLER_DECISION ||--o| TRANSACTION_CASE : acceptance_creates
 TRANSACTION_CASE ||--o{ CONTRACT : versions
 TRANSACTION_CASE ||--o{ PAYMENT_OBLIGATION : defines
 TRANSACTION_CASE ||--|| OWNERSHIP_TRANSFER : tracks
 TRANSACTION_CASE ||--o{ DELIVERY : coordinates
 PAYMENT_TRANSACTION ||--o{ PAYMENT_ALLOCATION : supplies
 PAYMENT_OBLIGATION ||--o{ PAYMENT_ALLOCATION : receives
 INSPECTION_REVISION ||--o{ INSPECTION_FINDING : freezes
 INSPECTION_FINDING }o--|| INSPECTION_ITEM : answers
 APPOINTMENT_SLOT ||--o{ APPOINTMENT : reserves
```

An accepted current decision creates at most one transaction case; rejection creates none. Allocation totals cannot exceed verified payment and must match currency. Findings are revision-owned. Contracting parties, retention and exact legal finality remain approved-policy inputs.
