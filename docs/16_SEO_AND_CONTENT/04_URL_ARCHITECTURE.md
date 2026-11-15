# URL architecture

**ID:** 16/04_URL_ARCHITECTURE · **Version:** 0.1 · **Status:** PROPOSED, subject to content, legal and engineering approval · **Owner:** Head of SEO · **Reviewers:** Content, product, privacy, engineering · **Updated:** 2026-11-15

## Route families
| Pattern | Resource / canonical approach | Indexation |
|---|---|---|
| `/sell`, `/value`, `/buy`, `/dealers`, `/branches` | Evergreen intent landing pages with self canonical. | Index when approved. |
| `/buy/{make}`, `/buy/{make}/{model}`, `/buy/city/{city}` | Approved curated category; stable slugs mapped to taxonomy ID. | Index only when eligibility gates pass. |
| `/cars/{stable-slug}` | Unique public consumer vehicle; stable opaque ID in mapping prevents collisions. | Index when available and consented; lifecycle in indexation rules. |
| `/branches/{slug}` | Open branch location and hours. | Index if verified and active. |
| `/journal/{slug}` | Original article, canonical to itself. | Index only after editorial review. |
| `/account/...`, `/dealer/application`, `/dealer/auctions/...`, `/ops/...` | Authenticated account, application status, auction or operations; no sensitive data in path/query. | Private; noindex is supplemental to authorization. |
| `/dealer/apply` | Public application entry, with applicant state protected after creation. | Not intended as an indexed landing page; `/dealers` is the canonical public explanation. |
| `/buy?sort=...&...` | User filters/sort and pagination. | Do not index arbitrary facets; canonical only where genuinely duplicate. |

Use lowercase readable ASCII slugs, hyphens, stable object mapping and approved redirects; no contact, vehicle identifier, document or token in URLs. URL parameter ordering is deterministic. Different substantive pagination pages should self-canonical; do not canonicalize all pages to the first page. Filter combinations are noindex or not made crawlable according to policy, while ensuring search-engine access to noindex where needed. Redirect renamed resources to the closest equivalent using a single permanent redirect; no cycles/chains or mass redirects to unrelated pages. Review Google's [ecommerce URL guidance](https://developers.google.com/search/docs/specialty/ecommerce/designing-a-url-structure-for-ecommerce-sites).

## Acceptance
Crawl staging representative routes with JS off and on; canonical tags, status, sitemap, breadcrumbs and internal links must agree. Maintain a redirect ledger with old/new, reason, owner and removal decision. Test slug collisions, Unicode input, deprecated branch, pagination and arbitrary filter parameters.
