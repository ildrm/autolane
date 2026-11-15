# Failure Recovery Architecture

| Metadata | Value |
|---|---|
| ID / version | 08/09_FAILURE_RECOVERY_ARCHITECTURE / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Failure Recovery Architecture; jurisdiction-dependent policy decisions remain open. |

## Failure catalogue
| Failure | Immediate behavior | Recovery / owner |
|---|---|---|
| Primary database unavailable | Reject binding commands as temporarily unavailable; no optimistic success. | SRE restores authoritative primary and verifies consistency; auction operations decides extension or cancellation under approved rules. |
| Clock health uncertain | Freeze bid acceptance and automatic closing, alert. | SRE validates clock and audit; auction operations applies approved incident policy. |
| Gateway or broker outage | Commits remain authoritative; UI shows connection issue and snapshot refresh. | Relay retries committed outbox; clients resubscribe and fetch snapshot; monitor lag. |
| Provider timeout | Mark unknown/pending; do not send a second financial operation without status inquiry. | Integration owner reconciles using provider reference and idempotency key. |
| Corrupt upload / scanner outage | Quarantine evidence and prohibit publication or download. | Rescan or request replacement; notify assigned operator. |
| Replica/search lag | Binding reads route to primary; show search freshness where needed. | Rebuild projection and verify offsets. |
| Restore | Stop writers and external side effects; restore chosen point, replay durable events cautiously. | Incident lead reconciles accepted bids, notifications and provider transactions before reopening; record any data loss. |

Backups, restore objectives and realistic throughput must be approved and rehearsed. Every recovery action has audit ID, responsible operator, affected scope and customer communication; financial reversals require authorized human approval. No automatic retry can override terminal policy.
