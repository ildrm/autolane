# Revenue model

| Metadata | Value |
|---|---|
| Document ID | 01/05_REVENUE_MODEL |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and documentation leadership |
| Reviewers | Operations, legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Revenue model; English-first automotive marketplace documentation |

## Candidate mechanisms
| Mechanism | Candidate payer / trigger | Controls and unresolved policy |
|---|---|---|
| Transaction service fee | Seller or buyer when a defined qualifying transaction closes. | Define payer, percentage/fixed basis, caps, tax, discounts, cancellation and refunds; disclose before commitment. |
| Dealer subscription | Dealer organization per term or active seat. | State access, renewal/cancellation and no guaranteed inventory; verify willingness to pay. |
| Inspection or documentation service | Contracting customer per explicitly agreed service. | Describe covered work, limits, no-show rules and remedy. |
| Financing or logistics partner remuneration | Partner under a separately reviewed arrangement. | Verify broker permissions, conflicts, referral disclosure, consent and provider responsibilities. |
| Premium placement or aggregated insight | Dealer/business under separate order. | Label placement, prevent auction manipulation, apply privacy and competition safeguards. |

All mechanisms and rates are proposals; no fee may be billed solely because it appears in this catalog. **DECISION REQUIRED:** price, payer, basis, charge event, taxes, refunds, revenue recognition and local permissions.

## Quote and calculation rules
Generate a quote snapshot with policy/version, jurisdiction, vehicle, payer, line items, currency, tax treatment, effective window and explicit total; use exact decimal or minor-unit arithmetic per currency, an approved rounding policy and preserved calculation inputs. Material revisions require a new quote and customer acknowledgement where required. Auction price is transaction consideration, not platform revenue. A payment or invoice is not necessarily recognized revenue; finance selects recognition rules.

## Measurement and testing
Net earned fee = approved earned gross fees − applicable discounts, refunds and adjustments, excluding tax collected for authorities where appropriate. Contribution = earned net revenue − attributable variable service and acquisition costs. Use [synthetic scenario](../01_BUSINESS_MODEL_AND_OPERATIONS.md) only as arithmetic illustration, never forecast. Tests: fixed/percentage quote and tax rounding, fee version changes, failed sale and refund, currency mismatch, duplicate event, dispute and audit. Finance and legal approve before use.
