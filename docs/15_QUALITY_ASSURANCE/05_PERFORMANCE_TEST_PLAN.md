# Performance test plan

| Metadata | Value |
|---|---|
| Document ID | 15/05_PERFORMANCE_TEST_PLAN |
| Version / status | 0.1 / proposed; review required |
| Owner | Performance Lead |
| Reviewers | Product, QA, Engineering, Operations, Security, Design |
| Updated | 2026-11-15 |
| Scope | Performance test plan for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [release quality gates](10_RELEASE_QUALITY_GATES.md). |

## Workload and measurement

Size tests from explicit assumptions until traffic baselines exist. Model routine browse/search, lead submissions, branch booking bursts, image-heavy pages, concurrent auction connections and the concentrated bid/close period separately; include background jobs, provider latency and reporting load. Record concurrent clients, requests per second, bid mix, object sizes, database volume, network latency and region for every run. Run baseline, step load, spike, endurance and recovery tests; avoid equating simulated clients with confirmed business demand.

Measure bid request decision latency separately from broadcast delivery, p50/p95/p99, rejection reasons and accepted-bid correctness. Record server and queue saturation, database locks, connection counts, memory, dropped/replayed events and time to reconcile after reconnect. Measure public Core Web Vitals at the 75th percentile on real users by device and page group where lawful: LCP ≤2.5 s, INP ≤200 ms and CLS ≤0.1 are proposed release goals aligned with prompt. Lab runs use a specified throttled mobile device/network and cannot replace real-user data.

## Reliability under peak

Execute a high-contention auction with failure injection and assert accepted bids serialize correctly at every load; latency improvements cannot trade away correctness. Simulate provider outage and slow storage to confirm bounded queues, protective timeouts and readable status. Identify bottlenecks, cost and saturation knee; repeat the agreed workload after remediation. Numeric server latency/availability SLOs remain provisional until architecture, volume and operating budget are approved.

## Gate

Publish reproducible workload files or test configuration, build, environment, results and data integrity check. No release when the agreed latency budget is missed on a representative environment or when a single accepted bid is lost or duplicated.
