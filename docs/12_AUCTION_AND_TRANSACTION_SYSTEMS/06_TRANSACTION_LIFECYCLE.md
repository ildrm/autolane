# Transaction Lifecycle

| Metadata | Value |
|---|---|
| ID / version | 12/06_TRANSACTION_LIFECYCLE / 0.1 |
| Status | Proposed; legal, finance and auction policies unapproved |
| Owner / reviewers | Auction and finance architecture / legal, operations, security, QA |
| Updated | 2026-11-15 |
| Scope | Transaction Lifecycle; no authority to transfer funds or ownership is implied. |

## Transaction state and evidence
**PROPOSED:** represent independent status dimensions rather than conflating financial, contractual and title facts. Aggregate overall state is derived from recorded evidence and approved jurisdiction policy; each status change is versioned and audited.

| Dimension | Proposed states and entry guard |
|---|---|
| Auction result | pending → qualifying / no qualifying / cancelled; final result from authoritative auction. |
| Seller choice | not presented → presented → accepted / rejected / expired; explicit identity and current offer required. |
| Contract | draft → review → awaiting signatures → executed / cancelled; approved template and verified signatures. |
| Obligation | proposed → due → evidence pending → reconciled / disputed / cancelled; exact money, separate finance approver. |
| Transfer | pending → documents verified → submitted → confirmed / failed; external proof required. |
| Physical handover | scheduled → custody transferred → delivered / exception; signed/verified evidence required. |
| Case | in progress → held / completed / closed unsuccessful; reason and actor on every transition. |

Under a **provisional** closure rule, completion requires seller acceptance, required executed contract, reconciliation of applicable obligations, verified legal transfer and approved handover evidence; policy may select non-applicable dimensions only through explicit jurisdiction review. A negative or disputed state blocks completion and creates an assigned operational case. Reversal after closure is an auditable exception, not deletion of facts. No assumed cash flow, warranty or lending. Tests cover rejected offers, signatures pending, mismatched evidence, buyer default, transfer delay and duplicate event replay.
