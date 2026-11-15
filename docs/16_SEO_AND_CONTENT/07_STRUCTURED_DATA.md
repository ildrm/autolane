# Structured data

**ID:** 16/07_STRUCTURED_DATA · **Version:** 0.1 · **Status:** PROPOSED, subject to content, legal and engineering approval · **Owner:** Head of SEO · **Reviewers:** Content, product, privacy, engineering · **Updated:** 2026-11-15

## Policy
Add JSON-LD only for content that is visible, accurate and current for that page. Consult current [Google structured-data guidance](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) and relevant feature-specific rules during implementation. Schema.org vocabulary support does not guarantee a Google rich result, and markup must not contain unapproved guarantees or inaccessible/private data.

| Page | Candidate type | Required visible facts and condition |
|---|---|---|
| Article | `Article` | Headline, author where known, published/modified dates, sourceable content and permitted image. |
| Branch | `LocalBusiness` or appropriate subtype | Actual business name, verified address, hours and contact; no fictitious locations. |
| Breadcrumbs | `BreadcrumbList` | Matches visible hierarchy and canonical links. |
| Consumer listing | `Vehicle`/`Car`, optionally `Offer` where accurate | Vehicle identity, condition, price/currency and availability visible and current; validate search-engine feature eligibility separately. |
| Organization | `Organization` | Verified organization identity, site and contact information. |
| Guides or FAQ | Applicable semantic type if accurate | Do not assume a rich result; current eligibility and quality rules may change. |

On sale, removal or price change, synchronize visible content and markup in the same published revision; remove unsupported `Offer` rather than claiming inventory exists. Do not mark dealer-only auctions as public offers, fabricate reviews, ratings, prices or financing approvals. Test representative templates with structured data validation and raw HTML, check visible parity and regressions after release. Treat warnings as investigated; eligibility and search display remain outside platform control.
