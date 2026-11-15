# Dashboard catalog

**ID:** 17/04_DASHBOARD_CATALOG · **Version:** 0.1 · **Status:** PROPOSED, subject to privacy, finance and product approval · **Owner:** Head of data · **Reviewers:** Analytics, security, legal, finance, product · **Updated:** 2026-11-15

## Views and access
| Dashboard / owner | Metrics and grain | Scope, freshness, decisions |
|---|---|---|
| Executive / product | Qualified leads, completed transactions, revenue, contribution, open risks; weekly/monthly. | Approved aggregate only; show cohort maturity and finance reconciliation status. |
| Acquisition / growth | Organic visits, acquisition cost, lead qualification and booking cohorts by channel. | Consent-aware aggregates; daily target and attribution coverage; no individual query-to-customer join. |
| Branch / operations | Capacity, attendance, inspection turnaround and open exceptions by branch/day. | Branch-scoped managers; show unavailable data and staffing denominator. |
| Auction / commercial | Eligible buyers, participation, accepted bids, qualifying outcomes, seller decisions and close latency by lot cohort. | Restricted commercial access; no private bidder data in broad reports. |
| Dealer success | Approval, first bid, repeat purchase and account restrictions. | Organization-scoped access, suppression for small cohorts. |
| Finance / finance | Earned revenue, pending obligations, reconciliation discrepancies and aged items. | Restricted finance role; sourced from approved ledger; no payout assumption. |
| Support and claims | Volume, first resolution distribution, reopen rate and claim outcomes. | Need-to-know and anonymized groups; no customer narrative in broad dashboards. |
| Data and model | Freshness, missingness, valuation error, coverage, drift and overrides. | Restricted to authorized data/pricing staff; mark sample and model version. |
| SEO | Indexable URLs, aggregate search clicks, CTR, issue counts and field CWV p75. | Public-page aggregates; segment mobile/desktop; show source delays. |

## Presentation and controls
Each tile links to metric definition/version, source, timezone, last updated, filters, numerator/denominator, data-quality state and owner. Zero, no data, withheld, loading and stale are distinct. Provide accessible text/table equivalent to charts; avoid color-only status. Default reporting latency is a proposed next-day target in the architecture, overridden by domain owners where required; do not market analytics as authoritative real-time auction state. Exports respect scope, auditing, retention and minimum group size.

## Acceptance
Compare an independently sampled month of counts and financial totals to source systems; test filter/date boundaries, revoked role, backfill, late-arriving events and missing source. Dashboards fail closed for unauthorized detail and visibly flag stale or incomplete datasets.
