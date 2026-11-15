# Operational model

| Metadata | Value |
|---|---|
| Document ID | 01/06_OPERATIONAL_MODEL |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and documentation leadership |
| Reviewers | Operations, legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Operational model; English-first automotive marketplace documentation |

## Service ownership and handoffs
| Stage / owner | Input → output | Hold and recovery |
|---|---|---|
| Acquisition / CRM | Seller request, contact and consent → qualified case with owner. | Suspected duplicate goes to review; unverified phone receives safe retry. |
| Scheduling / branch | Eligible request and capacity → confirmed slot and customer notice. | Slot conflict offers alternatives; closure or no-show reschedules under policy. |
| Inspection / supervisor | Verified vehicle and authority → reviewed, versioned report with evidence and limitations. | Missing identity or critical finding blocks publication; corrections retain prior reports. |
| Valuation / analyst | Report and comparables → indicative range, confidence and rationale. | Insufficient data causes abstention or review, never fabricated precision. |
| Auction / dealer operations | Eligible vehicle and report → ordered accepted bids and close outcome. | Bid outage or lost eligibility invokes published policy; preserve history. |
| Seller decision / CRM | Offer version and applicable terms → explicit decision or recorded expiry. | Rejected/expired is not accepted; relist requires policy and consent. |
| Contracts / legal | Parties, terms and evidence → signed agreement/version and obligations. | Identity mismatch or unsigned changes pause downstream work. |
| Settlement / finance | Obligation and independent evidence → matched or disputed record. | Amount/payee mismatch creates exception; no automatic claim of cleared funds. |
| Transfer and closure / operations | Contract, reconciliation and legal requirements → recorded transfer, physical handover and closed case. | Separate ownership/custody; missing evidence blocks ordinary close. |

## Staffing and service control
Each queue has a named owner, arrival time, priority, next action, due time and escalation; target SLAs require measured volume, branch hours and approved commitments. A shift lead reassigns absences and pauses intake when qualified capacity is exhausted. Each handoff preserves case ID and minimum necessary evidence. Support cannot silently override auction, finance or identity states. All privileged transitions require authorization, reason and audit.

## Acceptance
Run a table-top case including inspection dispute, unsuccessful auction, payment discrepancy and branch closure. Confirm a single accountable owner for each open case, communication on next action, and no closure without approved evidence. See [business operations detail](../01_BUSINESS_MODEL_AND_OPERATIONS.md).
