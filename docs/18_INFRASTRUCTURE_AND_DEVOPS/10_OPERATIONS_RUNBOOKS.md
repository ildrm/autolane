# Operations runbooks

| Metadata | Value |
|---|---|
| Document ID | 18/10_OPERATIONS_RUNBOOKS |
| Version / status | 0.3 / proposed, not deployed |
| Owner | Operations and SRE Leads |
| Reviewers | Architecture, Security, Finance, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Operations runbooks for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [recovery plan](07_BACKUP_AND_RECOVERY.md). |

## Auction integrity or time uncertainty

1. Confirm impact and appoint incident commander; record auction IDs and UTC time without exposing dealer data.
2. Suspend new affected auction actions using an authorized mechanism; preserve last committed bid, close time, audit, outbox and database health.
3. Compare server clock, transaction records and gateway sequence. An unknown outcome remains unknown; do not infer acceptance from a client animation.
4. Restore consistent service and reconcile acknowledged requests against durable records. Ask auction operations and legal to decide cancellation, extension or resumption under approved policy. Notify affected participants with the approved decision.
5. Document decisions, test a controlled auction and remove the hold only with named approval.

## Provider outage or reconciliation mismatch

Pause retries if provider duplicate semantics are uncertain. Reconcile each idempotency key and external reference with provider status and statement; do not issue a fresh financial operation on an ambiguous response. Create owned exceptions for unmatched/partial items; resume only after finance verifies. Message customers accurately without claiming a transfer has settled.

## Queue backlog and document scan failure

Check worker health, queue age and dead letters; reduce nonessential work, restore capacity and replay only after checking idempotency. Failed document scans stay quarantined; do not bypass scanning to clear backlog. Escalate time-sensitive customer work to authorized staff.

## Restore and verification

Use the recovery plan's isolated restore and integrity checks; compare accepted bids, obligations, evidence and notification intents before reopening. All runbook actions record actor, time, reason and outcome. Validate runbooks with on-call exercises before launch and after major topology changes.

## Operational execution checklist and exit criteria

| Runbook | Diagnose / contain | Recover / verify / exit owner |
|---|---|---|
| RB-01 Database unavailable | Confirm primary and quorum/durability health; disable binding command admission, leave safe public content | Restore selected authority; compare accepted receipts and all audit/outbox sequences; auction+finance sign off affected records before SRE reenables admission. |
| RB-02 Outbox backlog | Check oldest age, worker errors, provider status and poison-event schema | Repair consumer, replay same event IDs in bounded batches, compare source/projected versions; domain owner confirms no lost/duplicated effects. |
| RB-03 Provider callback ambiguity | Quarantine conflicting ID/hash, disable risky new retries, retain raw signed evidence in restricted storage | Query contracted source through verified channel; finance/legal adjudicates, adapter replays same correlation only. |
| RB-04 Compromised dealer session | Revoke session/member or organization as appropriate under serialized eligibility lock; disconnect subscriptions | Preserve accepted history and time boundary; risk owner reviews disputed bids, no silent deletion; restore only newly authorized scope. |
| RB-05 Public sensitive-content exposure | Emergency unpublish and CDN/search invalidation; deny origin read; preserve restricted evidence | Verify origin, cache variants and export copies; security/privacy determine notices; independent check before republish. |
| RB-06 Incorrect report after auction starts | Preserve published version, pause affected auction, record exact issue and recipients | Independent corrected report and approved auction resolution; notify authorized participants; no resumption after cutoff by silently changing close time. |
| RB-07 Failed title or settlement proof | Mark exception, prevent closure/handover where policy requires, identify current custodian | Independent verified evidence and exception disposition; legal and finance each confirm their milestone. |
| RB-08 Branch unexpectedly closed | Stop new slot allocation, enumerate future reservations, assign customer-contact tasks | Offer accessible alternative slots; move atomically after consent; operations verifies every affected booking has an owner/outcome. |

All runbooks begin with incident ID, authority to act, scope, UTC start, evidence preservation and communication owner. Read-only diagnostic collection precedes changes where practical; destructive corrections require the relevant domain approval. Exit checklist records source-of-truth consistency, reopened queues, customer follow-up, monitoring recovery and unresolved holds. Tabletop exercises use synthetic records, inject one failure at a time, time recovery and assign follow-up due dates. These are specifications for future exercises, not claims that drills have run.
