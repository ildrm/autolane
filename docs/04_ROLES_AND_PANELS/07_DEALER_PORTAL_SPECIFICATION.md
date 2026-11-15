# Dealer portal specification

| Metadata | Value |
|---|---|
| Document ID | 04/07_DEALER_PORTAL_SPECIFICATION |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Dealer portal specification; English-first automotive marketplace documentation |

## Organization onboarding and authority
Business representative submits organization identity and relevant documents; dealer operations review evidence, record decision and grant authorized organization membership. Approved status and each bidder's explicit authority are checked on every bid and report access. Rejected or incomplete application receives a safe status and support/appeal route; suspended members cannot start new bids. Document handling uses scoped, scanned, expiring access and audit.

## Dealer workflows
| Screen | Information / action | Success and failure |
|---|---|---|
| Auction discovery | Eligible auctions with vehicle basics, report version, schedule and approved terms; search/watch. | No unauthorized inventory; empty, stale and cancelled state visible. |
| Auction detail | Authorized report, limitations, opening/closing times in local zone, server-derived current amount and applicable increments. | Refresh or reconnect when stale; client countdown is advisory. |
| Bid confirmation | Enter amount/currency, understand terms, submit with a request key; receive authoritative accepted/rejected result and bid reference. | Invalid increment, eligibility, deadline or concurrency conflict returns clear reason; timeout is unknown until status reconciled, not a reason to send a second independent bid. |
| History and outcomes | Organization sees its own bids, accepted/rejected status, auction outcome and next contractual action. | Result is not proof of sale, paid funds or title; changes and disputes are auditable. |
| Membership and account | Authorized administrator invites/removes members and reviews scope. | No self-escalation or access beyond organization grant; revoked access takes effect. |
| Transactions and support | Review permitted contracts, obligations, settlement and assigned cases. | Never expose other dealer bids or sensitive seller information beyond approved policy. |

## Acceptance
Simulate two authorized bidders, duplicate request, close race, stale state, suspended organization and cross-tenant access. Exact reserve, tie, extension, deposit, binding effect and default rules require DEC-04 and applicable legal review; optional features remain disabled until approved.
