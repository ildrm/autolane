# Observability

| Metadata | Value |
|---|---|
| Document ID | 18/04_OBSERVABILITY |
| Version / status | 0.3 / proposed, not deployed |
| Owner | Observability Lead |
| Reviewers | Architecture, Security, Finance, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Observability for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [recovery plan](07_BACKUP_AND_RECOVERY.md). |

## Signals and ownership

Instrument request, auction decision, outbox, notification, payment evidence and reconciliation with a correlation ID that is not personal data. Metrics include API success/latency by route, bid decision accepted/rejected/unknown, close latency, websocket disconnect/reconciliation, database lock wait and replication lag, queue age/retries/dead letters, provider error rate, appointment conflicts, reconciliation exceptions, restore health and security-denied actions. Record business state transitions with policy version and audit identifier. Keep metric labels bounded; never attach customer ID, VIN, account number or unbounded URL as a metric label.

Logs are structured with timestamp, service, severity, trace, operation, result and redacted identifiers. Do not log tokens, identity documents, full payment data or message body. Distributed traces follow synchronous calls and outbox propagation, sampled according to privacy policy. Audit records have access controls, tamper-evident retention and separately monitored delivery. Operations dashboards show freshness and distinguish no traffic from missing telemetry.

## Alert policy and acceptance

Define service-level indicators and on-call thresholds from approved targets and baseline; alerts must have severity, owner, runbook and deduplication. Page immediately for suspected bid integrity loss, failed audit persistence or confirmed production data exposure; route backlog and cost trends to business-hours review. A synthetic end-to-end probe validates an appointment and simulated bid without creating live obligations. Test that a failed telemetry pipeline alarms rather than silently appearing healthy.

## Proposed alert thresholds and response ownership

Thresholds are initial configuration decisions to tune through staging evidence; integrity conditions have no error budget. Use multi-signal confirmation for noisy operational symptoms and preserve the original business incident even if alerts auto-resolve.

| Signal | Trigger / severity | Owner and immediate action |
|---|---|---|
| Accepted receipt missing after recovery, conflicting auction result, unbalanced posted journal | Any occurrence / SEV-1 | Auction/finance lead plus incident commander; stop affected binding writes, preserve evidence. |
| Trusted clock or synchronous durability guarantee unavailable | Any active binding write path / SEV-1 | SRE; fail closed, record affected interval, invoke integrity runbook. |
| Sustained core error rate | >2% unexpected5xx for5min with ≥100 requests / SEV-2 | API on-call; inspect release, database and dependency health. Low traffic uses failed probes. |
| Bid latency | p95 >500ms for10min at defined load / SEV-2 | Auction on-call; inspect row lock wait, eligibility locks and primary health. |
| Outbox age | Oldest critical event >60s for5min / SEV-2; >15min / SEV-1 if critical notices blocked | Worker owner; restore relay, no manual domain-state editing. |
| Malware scanner unavailable | Oldest required evidence >10min / SEV-2 | Platform/security; keep quarantine, show pending to affected teams. |
| Unauthorized access spike | >5× baseline and ≥50 denials/min for5min / security triage | Security; investigate scoped rate controls without locking out all legitimate users. |
| Restore/checksum failure or missing backup proof | Any scheduled verification fails / SEV-2 | Database/storage owner; repair protection and assess acknowledged-evidence exposure. |
| No telemetry heartbeat | Missing two1-minute heartbeats / SEV-2 | Observability owner; separately monitored alert channel, do not report healthy zero traffic. |

Each alert includes service/environment, bounded operation, first/last occurrence, trace sample pointer, affected scope count and runbook; no customer details. Track acknowledgement and mitigation time separately. Dashboard ratios display numerator, denominator, window and freshness. Logs/traces sample by approved policy; consequential audit persistence cannot be sampled away.
