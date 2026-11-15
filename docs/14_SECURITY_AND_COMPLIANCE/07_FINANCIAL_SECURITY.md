# Financial security

| Metadata | Value |
|---|---|
| Document ID | 14/07_FINANCIAL_SECURITY |
| Version / status | 0.1 / proposed; security and legal review required |
| Owner | Finance Security Lead |
| Reviewers | Product, Architecture, Security, Privacy, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Financial security for proposed marketplace; applicable legal obligations remain unresolved. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Financial control boundary

The provisional MVP records external obligations and settlement evidence; it does not imply custody, escrow, lending, disbursement or a payment license. Which model and provider are allowed remains DEC-03 in the discovery register. If direct or provider-mediated settlement is approved, define payer, payee, legal entity, currency, fees, evidence, status authority, refund rights and reconciliation before enabling a transaction type. Do not log full bank credentials or payment-card data; use provider-hosted or tokenized flows as approved.

## Authorization and reconciliation

Obligation creation is bound to the signed transaction and policy version. Separate preparation, independent approval and execution for refunds, adjustments and changes to destination accounts; use step-up, reason and immutable audit. Limit access by case and financial role. Provider callbacks require authentication, replay protection and validation against a known obligation and amount; a webhook alone is not proof of final settlement when provider semantics or bank confirmation require reconciliation. Reconciliation compares expected obligations with authoritative statement entries; unmatched, duplicate, partial or reversed entries are exceptions owned by finance. Preserve compensating entries rather than overwrite history.

## Acceptance

No user can both prepare and approve their own material refund under the proposed policy. A forged callback or a valid callback for a different currency leaves settlement unconfirmed. Duplicate provider messages create one logical record. A discrepancy prevents automatic closure; access to settlement evidence is denied to an unrelated dealer. Rules for settlement finality, fund recovery and legal retention remain jurisdiction-specific decisions.
