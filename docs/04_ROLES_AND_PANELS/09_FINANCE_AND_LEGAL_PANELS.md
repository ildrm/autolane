# Finance and legal panels

| Metadata | Value |
|---|---|
| Document ID | 04/09_FINANCE_AND_LEGAL_PANELS |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Finance and legal panels; English-first automotive marketplace documentation |

## Legal workspace
Authorized legal users see assigned parties, jurisdiction, approved template/version, signature requirements, document evidence, amendments, transfer tasks and disputes. Issue or amend a contract only with necessary review; a material change creates a new version and captures required acknowledgements. Missing signer, conflicting ownership, legal hold or unapproved template blocks the relevant step. Users can record title evidence without implying payment or physical handover. File download and sensitive case access are scoped and audited.

## Finance workspace
| Screen | Data and action | Controls / exceptions |
|---|---|---|
| Obligations | Payer, payee, exact amount, currency, due event, policy and related contract. | No assumed deposit, fee, tax or payout; create only under approved terms. |
| Evidence and reconciliation | External provider/bank reference, expected/observed amount and status, preparer and reviewer. | Partial or mismatch stays pending/disputed; uploaded receipt alone is not verified settlement. |
| Adjustments/refunds | Request reason, amount, evidence and proposed remedy. | Separate preparer and authorized approver; no money movement unless approved provider/model permits it. |
| Bank details | Masked destination and verified change history. | Independent verification and approval; no unrestricted edit or export. |
| Closure checklist | Contract, reconciled obligations, transfer and custody evidence, unresolved disputes. | BR-005 blocks ordinary closure on missing mandatory evidence or material financial discrepancies. |

## Acceptance
Finance can trace each obligation and adjustment to applicable policy, independent evidence and approver; duplicate provider notifications do not double count. Legal can trace signed contract versions and transfer evidence. Cross-role, self-approval, stale evidence, partial payment, changed payee and legal hold are tested. No UI implies the platform holds funds, lends, owns vehicles or guarantees payment without separate legal approval.
