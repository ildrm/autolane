# Domain Boundaries

| Metadata | Value |
|---|---|
| ID / version | 08/04_DOMAIN_BOUNDARIES / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Domain Boundaries; jurisdiction-dependent policy decisions remain open. |

## Ownership and contracts
Each domain owns its records and invariant checks. Other domains request a command or consume a minimal versioned event; no consumer mutates another domain's table. Writes listed as strong occur in one aggregate transaction; downstream projections are eventual. Authorization evaluates actor, organization, assignment, action and object before data disclosure.

| Context | Owns / interface | Dependencies and consistency |
|---|---|---|
| Identity and access | users, sessions, roles; authenticate, authorize | Strong permission lookup and revocation; external identity optional. |
| Organization and dealer | organization, verification, memberships; approve/suspend | Strong active bidder and organization eligibility check during bid; preserve history. |
| Vehicle catalog | taxonomy, vehicle identity, media references | Version taxonomy; identifier uniqueness scoped to permitted jurisdiction. |
| Seller acquisition / CRM | leads, consent, contacts, communications | CRM projects lead events; contact visibility scoped to assignment. |
| Scheduling / branch | calendars, capacity, appointment and check-in | Strong slot allocation; branch closure creates reschedule work. |
| Inspection | templates, findings, reports and immutable revisions | Publish approved report; auction pins revision; correction triggers review. |
| Valuation | comparables, estimate and override | Derived estimate nonbinding; authorized override and rationale retained. |
| Auction | auction, participants, bids, outcome | Serialize bid and close; pin policy, report and winner evidence. |
| Consumer inventory / procurement | listing, purchase and sourcing requests | Separate publication from dealer auction; search is projection. |
| Financing | application, offer, provider response | External decision; no implicit approval, restricted financial data. |
| Contracts | template/version, document and signature evidence | Legal policy, provider validation and authorization required. |
| Obligations / settlement | obligation, evidence, ledger and reconciliation case | Exact money; external settlement never assumed; segregation of duties. |
| Logistics | order, handover, delivery evidence | Physical custody distinct from title; partner assignment scoped. |
| Warranty / support | policy, claim, ticket, decision | Policy must be approved; remedy approval separated from investigator. |
| CMS / notifications / analytics / admin | editorial content; deliveries; aggregate events; policy changes | Notifications retry asynchronously, analytics minimizes identifiers; admin changes audited and versioned. |

A message outage cannot roll back the originating business transaction. Outbox backlog alerts and replay preserve delivery; missing contract, consent or permission denies consequential transitions. Every context requires named operational owner and monitoring before implementation approval.
