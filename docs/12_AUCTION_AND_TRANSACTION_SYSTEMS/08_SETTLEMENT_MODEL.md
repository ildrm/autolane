# Settlement Model

| Metadata | Value |
|---|---|
| ID / version | 12/08_SETTLEMENT_MODEL / 0.1 |
| Status | Proposed; legal, finance and auction policies unapproved |
| Owner / reviewers | Auction and finance architecture / legal, operations, security, QA |
| Updated | 2026-11-15 |
| Scope | Settlement Model; no authority to transfer funds or ownership is implied. |

## Models and provisional scope
**DECISION REQUIRED:** select model, legal entities, fee payer, duties and licensed providers for each jurisdiction. Do not imply that a marketplace holds funds.

| Model | Funds path | Design implication |
|---|---|---|
| Direct external settlement | Buyer pays seller using an external channel; platform records evidence. | Proposed phase-1 planning scenario; evidence and independent reconciliation required, no execution capability. |
| Provider-mediated | Approved regulated provider collects/disburses under its contract. | Verify authorization, callbacks, idempotency, settlement statements, refunds and liability allocation. |
| Escrow | Authorized escrow arrangement holds and releases money under agreed conditions. | Separate regulated custody and release rules; no functionality enabled until legal/provider approval. |
| Platform custody/inventory | Platform collects, pays out or acquires vehicle. | Material licensing, accounting, safeguarding, title and risk requirements; separate decision and architecture. |

Obligation captures payer, payee, amount in integer minor units, ISO currency, due date, basis and policy version. Evidence records who asserted payment, provider reference, attachment, timestamp and review; evidence alone does not set reconciled. Finance matches external statements to obligations with tolerance only if approved; mismatch, unknown timeout, partial or overpayment creates a hold and assigned case. Fees, taxes, refund, chargeback and exchange-rate rules remain open. Test duplicated provider callbacks, wrong currency, stale evidence, overpayment and a crash before acknowledgement. Every correction preserves an auditable trail.
