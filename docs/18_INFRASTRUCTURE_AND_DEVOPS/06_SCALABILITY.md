# Scalability strategy

| Metadata | Value |
|---|---|
| Document ID | 18/06_SCALABILITY |
| Version / status | 0.1 / proposed, not deployed |
| Owner | Principal Architect and SRE |
| Reviewers | Architecture, Security, Finance, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Scalability strategy for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [recovery plan](07_BACKUP_AND_RECOVERY.md). |

## Scale-out order

First optimize database indexes and queries, enforce pagination, cache public read-heavy pages and serve responsive images via CDN. Scale stateless web/API services and real-time gateways horizontally while maintaining durable bid decisions in the authoritative transactional store. Partition work by auction only when correctness of each auction's ordering is preserved; increasing node count alone must not split one auction's authority. Independently scale image processing and notification workers with queue backpressure. Search and analytics use projections and cannot become authoritative for bidding or financial status.

Track database CPU, lock wait, connection pool saturation, read/write latency, queue age, gateway connection count, message fanout and object egress. Add read replicas only for appropriately stale-tolerant reads, and show freshness; never read a current bid or settlement decision from a lagging replica without consistency guarantees. Split services only after measured bottlenecks, team ownership and operational benefits justify the added failure and consistency costs. Scale down safely after peak; benchmark database vertical scaling and its limits before sharding.

## Failure and acceptance

Load shedding must reject or defer before accepting work; an accepted bid cannot disappear because a worker or gateway scales down. A reconnect retrieves authoritative state. A backlog alarm identifies owner and age, and recovery drains without duplicate side effects. Performance tests and cost estimates demonstrate each scaling step before production change.
