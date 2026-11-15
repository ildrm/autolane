# Information architecture

**ID:** 05/02_INFORMATION_ARCHITECTURE · **Version:** 0.1 · **Status:** PROPOSED, subject to research and stakeholder review · **Owner:** UX lead · **Reviewers:** Product, accessibility, operations, engineering, legal · **Updated:** 2026-11-15

## Design intent
Organize around user intent and transaction status, not internal department names. The public website, seller account, dealer portal and staff workspace share identity where appropriate but have distinct authorization. Route names are proposed logical paths; a path never grants access. Initial copy is English/LTR.

## Site map and intent mapping
| Surface | Primary navigation | Secondary locations | User goal |
|---|---|---|---|
| Public | Sell, Buy, Value, Branches, How it works | Help, Journal, About, Dealer sign-up, Sign in | Understand service and start a journey. |
| Seller | My vehicles, Appointments, Offers, Documents, Support | Profile, Notifications | Track own case and make an explicit offer decision. |
| Consumer | Browse, Saved, Requests, Appointments | Profile, Support | Find and enquire about publishable vehicles. |
| Dealer | Auctions, Watchlist, Bids, Purchases | Team, Documents, Support | Inspect approved auction data and bid. |
| Operations | Work queue, Branches, Inspections, Auctions, Transactions | Customers, Reports, Settings | Process assigned work and exceptions. Modules appear only if authorized. |

## Hierarchy and findability
Public URL patterns: `/sell`, `/value`, `/branches`, `/branches/{slug}`, `/buy`, `/cars/{slug}`, `/journal/{slug}`, `/dealers`; index only approved public content. Account patterns: `/account/sales/{id}`, `/dealer/auctions/{id}`, `/ops/transactions/{id}`; private surfaces are authenticated, excluded from indexing, not linked in public sitemaps. Region, currency and timezone are displayed explicitly where needed. IDs in routes are opaque and never authorization. User-visible labels avoid exposing internal codes.

## Cross-journey transitions
Seller's request leads to booking, then to a case dashboard; a return to the dashboard preserves completed steps. Dealers enter a public explanation before identity verification and approval; only approved bidders see private auctions. Winning a bid creates a pending outcome, not a completed transaction. Consumer inventory and private dealer lots have separate visibility. Support remains reachable from every status and receives a case reference without sensitive data in URLs.

## Acceptance
A navigation test asks at least 5 participants per role to locate appointment changes, inspection reports, bids and support; record first-click success and misconceptions. Public search engines can fetch only intended pages; private data returned for an unauthorized request must not reveal existence or content. Product, operations and security review category names and route inventory before release.
