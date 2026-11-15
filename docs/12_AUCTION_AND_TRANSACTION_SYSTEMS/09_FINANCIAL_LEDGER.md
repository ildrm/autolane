# Financial Ledger

| Metadata | Value |
|---|---|
| ID / version | 12/09_FINANCIAL_LEDGER / 0.3 |
| Status | Proposed; legal, finance and auction policies unapproved |
| Owner / reviewers | Auction and finance architecture / legal, operations, security, QA |
| Updated | 2026-11-15 |
| Scope | Financial Ledger; no authority to transfer funds or ownership is implied. |

## Proposed accounting representation
A journal records the business event, source reference, actor, approval, timestamp and entries in a single transaction. Each entry has account ID, debit or credit integer minor units and ISO currency. Every **posted journal balances per currency**; multiple currencies require separately balanced currency positions and an approved FX rate/source and rounding account. Money is never represented using binary float. A transaction's obligation or ledger entry is a record of an economic assertion, not proof of custody, settled cash or legal transfer.

Draft journals may be validated and approved by separate staff; posted entries are immutable. Correct errors by a linked reversing journal and replacement, never overwrite or delete. Unique source event and idempotency keys prevent duplicate posting. Accounts, recognition policy, chart of accounts, tax, fees, refunds, payout and FX policy are **DECISION REQUIRED** with qualified finance/legal review; illustrative accounts cannot be treated as the approved chart. No journal should imply a platform-controlled bank account without evidence and approved business model.

Example conceptual balanced journal: debit `external_settlement_clearing` 1,000,000 minor units; credit `seller_payable` 1,000,000 in the same currency, only if finance establishes those accounts and obligations apply. It is illustrative and not a mandate to book externally settled payments. Test unbalanced posting, wrong currency, duplicate event, reversal linkage, unauthorized approval and reconciliation failure.

## Posting boundary and control examples

The default `external_evidence_only` mode tracks obligations, verified source evidence, allocations and exceptions. It does **not** automatically post seller payable or bank accounts for externally settled funds. The illustrative clearing journal above is disabled unless an approved accounting model establishes that the platform has those rights and obligations. A future fee-revenue journal similarly requires approved recognition, payer, tax and chart-of-accounts policies; merely uploading a receipt is never revenue recognition.

A proposed journal record has `id`, `source_event_id`, `policy_version`, `status` (draft, reviewed, posted, reversed), `prepared_by`, independent `approved_by`, `effective_at`, `posted_at`, `reversal_of` when applicable and at least two lines. Each line carries account, one currency and exactly one positive debit/credit safe integer. Validate balanced sums with overflow-safe arithmetic. Posted journal currency totals are invariant; a reversal contains inverse lines for the original amounts and references its source. A replacement is a separate journal. A third-party payment reversal creates a disputed obligation and new evidence even if the original transaction was closed.

| Fixture | Required result |
|---|---|
| Debit 10000 / credit 9999 in EUR | Reject unbalanced journal; no posted lines. |
| EUR debit / USD credit equal numeric amount | Reject; numerical equality does not balance currencies. |
| Maker submits own approval | Deny without mutation; record authorization denial. |
| Same source event, new retry key | Return existing source-linked posting or conflict, never duplicate. |
| Source payment 10000 allocated 7000 then 4000 concurrently | At most valid total10000; second conflicting allocation rejected. |
| Refund demanded in external-evidence-only mode | Route approved counterparty process; platform does not execute funds transfer. |
