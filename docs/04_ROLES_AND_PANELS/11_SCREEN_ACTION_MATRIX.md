# Screen action matrix

| Metadata | Value |
|---|---|
| Document ID | 04/11_SCREEN_ACTION_MATRIX |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Screen action matrix; English-first automotive marketplace documentation |

## Proposed action matrix
| Surface / screen | Principal actor → action | Reads / writes | Guard and expected failure |
|---|---|---|---|
| Public home / sell | Visitor → start request | Published content; request draft. | Unavailable service shows contact path; no private data. |
| Seller vehicle form | Seller → save/submit | Taxonomy, vehicle details, contact/consent → request/version. | Invalid or unsupported fields retain draft with accessible errors. |
| Seller booking | Seller or branch → reserve/reschedule | Eligible capacity → appointment and notice request. | Last slot conflict yields alternatives; branch/user scope (FR-001, BR-001). |
| Inspection form | Inspector → submit; supervisor → publish | Assigned checklist/evidence → report version. | Missing mandatory item or reviewer authority fails; old version retained (FR-002, BR-002). |
| Pricing review | Analyst → propose valuation; authorized reviewer → approve override | Report and comparables → range/confidence/reason. | Insufficient data shows abstention; no guaranteed offer. |
| Dealer auction | Authorized bidder → submit/reconcile bid | Auction/terms/eligibility → accepted or rejected bid. | Expired, duplicate, invalid or unauthorized request returns authoritative result (FR-003, BR-003). |
| Seller offer | Seller → accept/reject specific offer | Offer/terms → decision evidence. | Reject stale, unauthorized or expired action; no silent acceptance (FR-004, BR-004). |
| Legal contract | Legal operator → issue/amend/record signature | Approved template/party evidence → contract version. | Unreviewed template, mismatched identity or absent signer holds. |
| Finance reconciliation | Preparer → match; independent approver → approve | Obligation/external evidence → reconciled or discrepancy. | Mismatch and self-approval blocked; no implied transfer (FR-005, BR-005). |
| Transfer / handover | Authorized operator → record evidence | Contract and required proofs → distinct title/custody statuses. | Missing proof stays pending; no payment inference. |
| Support case | Assigned agent → acknowledge/escalate | Customer-safe case data → comment/ownership. | Unassigned/unauthorized access denied; finance override unavailable. |
| Administration | Privileged actor → request policy/role change | Versioned configuration → reviewed grant/change. | Step-up and independent approval when required; no historical rewrite. |
| Consumer listing | Visitor → filter/inquire | Public vehicle data → inquiry with consent. | No dealer-private report; stale/unavailable listing clearly marked. |

## Completion criteria
Each action requires screen-level loading, empty, invalid, conflict, no-permission and recovery states; a backend operation, entity, domain event, analytics event and concrete test must be linked before implementation. This matrix is a core baseline and does not claim every phase 2–4 screen is individually specified. Cross-tenant, retry and keyboard tests apply to all relevant actions.

## Expanded contract baseline — revision 0.3

[Panel contracts](12_PANEL_CONTRACTS.md), [scenario traceability](../SCENARIO_TRACEABILITY.md) and [operation index](../10_BACKEND_AND_APIS/12_OPERATION_INDEX.md) provide the expanded cross-domain action baseline.
