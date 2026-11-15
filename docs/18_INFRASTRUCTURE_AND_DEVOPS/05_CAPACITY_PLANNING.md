# Capacity planning

| Metadata | Value |
|---|---|
| Document ID | 18/05_CAPACITY_PLANNING |
| Version / status | 0.1 / proposed, not deployed |
| Owner | SRE Lead |
| Reviewers | Architecture, Security, Finance, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Capacity planning for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [recovery plan](07_BACKUP_AND_RECOVERY.md). |

## Illustrative sizing model

All numbers below are **PROPOSED assumptions for sizing**, not observed traffic or promises. Start with 100,000 monthly visits, 2,000 qualified seller leads, 1,000 appointments and 500 completed inspections; assume 100 concurrent dealer connections at normal peak and 500 at a campaign peak. Assume 50 simultaneous auctions, 10 active bidders per auction and one attempted bid every 20 seconds at peak across active bidders: 50 × 10 / 20 = 25 bid requests/second, before retries. Apply a 2× burst allowance for 50 requests/second in a test, not as an automatic production capacity claim. Validate correlation between auction endings; simultaneous close can dominate write contention even when averages look low.

Assume 30 photos per inspection, 1 MB delivered average per image, 500 inspections/month: 15 GB new originals/month before originals, variants, retention, backups or metadata. With 3 retained variants of equal average size the illustrative gross is 45 GB/month; use actual measured sizes and storage lifecycle in estimates. Peak media egress depends on views and cache hit ratio; a cache miss storm needs a separate simulation.

## Procedure and bottlenecks

Record starting dataset, auction count, page mix, concurrency, geography, synthetic network, object size, read/write ratio, queue fanout and background analytics. Measure p50/p95/p99 response, accepted bid correctness, DB lock wait and connection pool, gateway connections, CPU/memory, cache hit, queue age and egress. Test baseline, 2× burst, outage/recovery and 24-hour endurance. Add headroom based on measured saturation and run cost sensitivity; do not approve a maximum fleet size without testing and budget.

## Acceptance

No accepted bid may be lost or duplicated at any tested rate. Report achieved limits, resource utilization, bottleneck, reproducible setup, cost assumptions and next review date; the assumed volumes do not establish SLOs or profitability.
