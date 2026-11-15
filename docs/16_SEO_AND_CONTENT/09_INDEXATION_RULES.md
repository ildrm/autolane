# Indexation and listing lifecycle

**ID:** 16/09_INDEXATION_RULES · **Version:** 0.1 · **Status:** PROPOSED, subject to content, legal and engineering approval · **Owner:** Head of SEO · **Reviewers:** Content, product, privacy, engineering · **Updated:** 2026-11-15

## Decision matrix
| Resource state | HTTP / index signal | Sitemap and user experience |
|---|---|---|
| Approved, public and available listing | 200, self canonical, indexable. | Include canonical; show verified availability, price and report summary. |
| Temporarily unavailable with useful content | 200 with explicit unavailable status; retain indexability only if useful and lawfully publishable. | Exclude from sitemap if no longer an intended canonical; show alternatives without misrepresenting availability. |
| Sold with durable useful permitted content | 200 with sold state and remove active offer; index policy determined by privacy/retention and editorial usefulness. | Remove from active listing sitemap; do not represent as available. |
| Withdrawn consent or sensitive disclosure | Revoke access immediately; remove data and images; appropriate 404/410 or legally reviewed response. | Remove sitemap/internal links, initiate search removal process where necessary; noindex or robots alone cannot protect data. |
| Permanently retired with exact equivalent | 301/308 to genuine equivalent if policy allows. | Remove old URL from sitemap; update internal links. |
| Permanently retired without equivalent | 404 or 410, with helpful navigation and no private content. | Remove sitemap; do not redirect all records to homepage. |
| Uncurated facets/internal search | Crawlable noindex where appropriate or link architecture that avoids generating combinations; noindex must be retrievable. | Omit sitemap; maintain accessible filters for users. |
| Private account / auction / operations | Authentication and authorization mandatory; return no private content to anonymous users. | Never public sitemap; noindex is supplemental, not security. |

## Governance and tests
Business owner determines retention and legal basis for sold data; content owner determines usefulness and SEO owner controls index policy. Preserve audit history and avoid showing a sold price without rights or policy approval. Test status code, HTML robots, canonical, sitemap, structured data, asset availability and re-crawl of representative transitions; no mixed “available” markup on sold page. Search engines choose their own indexing and removal timing.
