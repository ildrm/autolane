# Backup and disaster recovery

| Metadata | Value |
|---|---|
| Document ID | 18/07_BACKUP_AND_RECOVERY |
| Version / status | 0.3 / proposed, not deployed |
| Owner | Disaster Recovery Lead |
| Reviewers | Architecture, Security, Finance, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Backup and disaster recovery for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [recovery plan](07_BACKUP_AND_RECOVERY.md). |

## Proposed recovery objectives

These are **planning targets**, not validated service levels: authoritative transaction database RPO ≤5 minutes and RTO ≤2 hours; object evidence RPO ≤24 hours and RTO ≤8 hours; search and analytics projections may rebuild after the transactional platform is stable. Auction policy must specify treatment of bids acknowledged after the latest recoverable point: an RPO alone does not authorize losing accepted bids. The final architecture must demonstrate durable acknowledged writes, recover acknowledged bids from independent evidence, or suspend service when durability cannot be assured; legal and operations must approve incident handling.

Take encrypted, access-controlled backups and transaction logs in a separate fault domain, protect deletion with a distinct role and retention/immutability controls, and monitor completion and restore feasibility. Retention, geographic location and legal holds depend on jurisdiction. Include application configuration, policy versions, object metadata and encryption keys in recovery planning without storing keys with backups. Test point-in-time restore and actual object retrieval, not only backup job success.

## Restore runbook and evidence

Incident commander identifies recovery point, restricts writes, preserves affected source evidence and authorizes restore into isolated infrastructure. Verify integrity, compare committed bid/financial/outbox records and external provider statements, rebuild projections, resolve missing or duplicate notifications, verify permissions, then authorize controlled reopening. Never replay a payment or issue a new auction result solely because an event was replayed. Record actual RPO/RTO, discrepancies, approvals and follow-up actions. Exercise at least before launch and whenever material topology changes; set recurring cadence in approved operations policy.

## Acknowledgement durability takes precedence

The ordinary 5-minute backup RPO is not an accepted-bid or approved-financial-write loss allowance. Those acknowledgements require synchronously durable replicated commit across the selected failure boundary, or a separately demonstrated recoverable write receipt before success is returned. If the design cannot meet this during degradation, stop acceptance rather than acknowledge and later erase. Restore verifies every acknowledged binding receipt; any discrepancy blocks reopening and enters incident/legal review. Cloud topology and measured failure-domain guarantees remain a delivery validation task.

## Evidence-object durability and restore manifest

Critical report revisions, accepted terms, executed documents, title and payment proof must be durably stored and checksum-verified before a business action acknowledges dependence on them. The ordinary24-hour object-backup objective applies only to recoverable/noncritical material; it cannot permit losing the sole evidence of an accepted or approved transaction. Replication/fault-boundary selection and acknowledgement policy must demonstrate this distinction before activation. If the only critical evidence copy is unavailable or unverified, publication/approval fails closed.

A restore manifest captures backup ID, source time/LSN, encryption-key reference, object versions/checksums, schema version, receipt/outbox range, privacy erasure-ledger version and unresolved holds. Restore into an isolated account/network without provider egress. Check critical row counts, unique auction results, accepted receipts, journal totals, source allocations, object checksums and scope enforcement; apply erasure/hold policies before any user access. Replaying events does not resend customer messages or execute provider actions until individually reconciled. Record measured RPO/RTO and actual missing data; a successful database startup is not a successful recovery exercise.
