# Financial Api

| Metadata | Value |
|---|---|
| ID / version | 10/06_FINANCIAL_API / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Backend and architecture leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Financial Api; commercial and jurisdiction-dependent policy decisions remain open. |

## Financial boundaries
All financial functionality is **PROPOSED** and gated by DEC-01, DEC-02 and DEC-03. Phase-1 planning records external settlement evidence; it does not authorize funds custody, escrow, lending, payout or guarantees.

| Operation | Actor and input | Outcome / guard |
|---|---|---|
| `GET /v1/obligations/{id}` | Seller, buyer or finance with object permission | Return party-scoped amount, currency, due date and evidence status; never another party's bank details. |
| `POST /v1/obligations/{id}/evidence` | Finance operator; evidence reference, payer/payee, amount/currency and provider reference | 202 pending review; no `settled` assertion from upload alone; scan and validate reference. |
| `POST /v1/reconciliations/{id}/approve` | Independent finance approver, version, matched evidence, reason | 200 reconciled only if amount/currency, parties, provider state and approvals match policy; discrepancy remains held. |
| `POST /v1/refund-requests` | Authorized finance operator; transaction, amount/currency, reason | Proposed future flow; record request only, no refund execution without approved money flow and second approval. |

Use integer minor units and ISO currency, exact calculations and approved currency exponent; no float or cross-currency arithmetic. Require idempotency and audit on every write; provider references unique per provider. Provider timeout remains unknown; query/reconcile before any retry. Logs omit account numbers and document content. Validate duplicate evidence, mismatch, overpayment, partial payment, wrong currency, stale version and operator self-approval.
