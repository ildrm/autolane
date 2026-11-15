# Application Routing

| Metadata | Value |
|---|---|
| ID / version | 11/02_APPLICATION_ROUTING / 0.3 |
| Status | Proposed, pending design and product review |
| Owner / reviewers | Frontend architect / design, accessibility, security, QA |
| Updated | 2026-11-15 |
| Scope | Application Routing, initial English LTR release. |

## Proposed route map
| Surface | Route | Access / rendering |
|---|---|---|
| Public | `/`, `/sell`, `/buy`, `/value`, `/branches`, `/help`, `/journal/{slug}` | Public, server-rendered canonical pages; stable English slugs. |
| Consumer | `/buy`, `/cars/{slug}` | Published listing only, server-rendered; private identifiers excluded. |
| Seller | `/account/sales/{leadId}`, `/account/appointments` | Authenticated owner; `noindex`, no shared caching. |
| Dealer application | `/dealer/application` | Authenticated applicant with access to own application, including pending, rejected and appeal status; noindex/private. |
| Dealer auctions | `/dealer/auctions`, `/dealer/auctions/{id}`, `/dealer/purchases/{id}` | Approved dealer and object scope; explicit bidder permission for bids; noindex/private. |
| Operations | `/ops/branches`, `/ops/inspections/{id}`, `/ops/auctions/{id}`, `/ops/transactions/{id}`, `/ops/support/{id}` | Staff role, branch and assignment; noindex/private. |
| Admin | `/ops/admin/access`, `/ops/admin/policies`, `/ops/admin/audit` | Elevated and scoped; step-up before sensitive writes. |

A direct deep link first verifies current access; return safe generic not-found where policy prevents existence disclosure. On sign-in resume only validated same-origin target. Expired session saves no sensitive form data to URL and prompts recovery. Listing delisting returns appropriate public status and canonical policy; do not expose active dealer auction pages publicly. The `/journal/{slug}` route matches the proposed UX screen inventory and SEO route family. These are proposed routes, not an instruction to create redirects. Final paths and copy require UX/product/SEO approval.

## Remaining operational and account routes

| Route | Panel / screen | Access and next action |
|---|---|---|
| `/account/requests/{id}` | Consumer PNL-03 | Own inquiry, offer and linked transaction; refresh exact terms before acceptance. |
| `/account/privacy/{id}` | Customer rights | Own request status and identity verification; no staff investigation notes. |
| `/ops/inventory/{id}` | Inventory PNL-09 / SCR-041 | ROLE-021 publication scope; internal listing read differs from public listing DTO. |
| `/ops/legal/transfers/{id}` | Legal PNL-11 / SCR-042 | ROLE-012 assigned matter; evidence access separately audited. |
| `/ops/finance/reconciliations/{id}` | Finance PNL-12 / SCR-043 | ROLE-013/014 scoped review; prepare and approve mutually separated. |
| `/ops/financing/{id}` | Financing PNL-13 / SCR-044 | ROLE-024 assigned application; restricted lender evidence. |
| `/ops/content/{id}` | CMS PNL-17 | Author and independent publisher grants; exact revision approval. |
| `/ops/growth/campaigns/{id}` | Growth PNL-18 / SCR-045 | ROLE-025; purpose, consent and suppression checked at dispatch. |
| `/ops/admin/policies/{id}` | Administration PNL-20 / SCR-046 | ROLE-016 author, ROLE-026 independent approver; step-up and effective-time check. |

All parameterized routes reject malformed IDs before fetching. Canonical public slug changes use a persisted redirect map, one hop, no wildcard redirects to unrelated pages. Private route changes update deep-link templates and notification builders together. URL query allowlists accept pagination/sort/filter only; do not place access tokens, contact details, document references or transaction evidence in URLs. Back/forward restores permitted filters; opening a different organization clears earlier route caches before rendering. Refreshing an inaccessible deep link must not briefly show cached private content.
