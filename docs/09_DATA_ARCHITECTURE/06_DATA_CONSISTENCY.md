# Data Consistency

| Metadata | Value |
|---|---|
| ID / version | 09/06_DATA_CONSISTENCY / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Data Consistency; jurisdiction-dependent policy decisions remain open. |

## Consistency matrix
| Data / change | Guarantee | Mechanism and failure |
|---|---|---|
| Bid acceptance and auction close | Strong, serialized per auction | Same authoritative transaction and row lock; unique sequence and immutable outcome; fail closed on untrusted clock. |
| Appointment capacity | Strong per slot | Lock slot/capacity record and atomically reserve; conflict returns availability refresh. |
| Idempotency outcome | Strong with corresponding command | Same commit; same key and payload returns same result; different payload conflicts. |
| Contract, settlement and title | Separate authoritative states | Reconciliation and guarded workflow, no distributed atomicity or inference across external systems. |
| Search, dashboards and notifications | Eventual | Outbox plus idempotent inbox, lag alert, version and rebuild; binding action fetches authority. |
| External callback | At-least-once and possibly reordered | Signed callback, durable inbox, version/state guards and status reconciliation. |

Use optimistic version checks for ordinary edits and row locks for auction contention; never hold database locks during network calls. Reversal is an explicit compensating action with reason and audit, not deletion of evidence. A failed notification cannot undo a committed bid. Disaster recovery must reconcile external systems and client acknowledgements before trading resumes.
