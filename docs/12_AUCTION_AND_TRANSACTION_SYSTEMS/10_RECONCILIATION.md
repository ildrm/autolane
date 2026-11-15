# Reconciliation

| Metadata | Value |
|---|---|
| ID / version | 12/10_RECONCILIATION / 0.1 |
| Status | Proposed; legal, finance and auction policies unapproved |
| Owner / reviewers | Auction and finance architecture / legal, operations, security, QA |
| Updated | 2026-11-15 |
| Scope | Reconciliation; no authority to transfer funds or ownership is implied. |

## Match, review and resolve
Reconciliation compares authoritative obligations and recorded evidence with provider/bank statements or other independently approved external confirmation. Ingest statement using authenticated source, statement ID, date, currency and checksum; isolate duplicate lines. Match candidate by provider reference, parties, currency, exact minor-unit amount and approved timing window. No fuzzy or tolerance match becomes final without explicitly approved policy. Associate evidence and retain matching rationale without copying account credentials into logs.

| Outcome | Status and next action |
|---|---|
| Unique exact match | Pending approval; independent finance reviewer checks source and posts reconciliation. |
| No statement / provider timeout | Unknown/pending; poll under provider contract and assign owner, never infer failure or resend payment blindly. |
| Partial, excess, wrong currency or duplicate | Discrepancy/held; operator investigates and records approved resolution or adjustment. |
| Refunded or chargeback after match | Reopen linked case, record provider evidence, reverse through approved journal and notify permitted parties. |
| Suspected fraud or conflicting documents | Restrict further actions and escalate to security/legal with preserved evidence. |

State transitions require version checks, idempotency and audit; a preparer cannot approve their own adjustment. Daily completeness checks compare source line counts and totals per currency against ingestion and resolved/unresolved cases, and alerts identify aging items. Closure cannot rely on a stale dashboard or message receipt. All settlement rules and time windows are pending finance/legal decisions and provider agreements.
