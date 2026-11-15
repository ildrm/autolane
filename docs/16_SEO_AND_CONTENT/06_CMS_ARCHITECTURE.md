# CMS architecture

**ID:** 16/06_CMS_ARCHITECTURE · **Version:** 0.1 · **Status:** PROPOSED, subject to content, legal and engineering approval · **Owner:** Head of SEO · **Reviewers:** Content, product, privacy, engineering · **Updated:** 2026-11-15

## Content model and lifecycle
Content types: page, article, vehicle taxonomy entry, branch, campaign landing page, policy notice, media asset and reusable block. Each stores stable ID, URL/slug, title, summary, body, author, source references, accessibility description, owner, review/expiry, published revision, indexability and audit history. Branch records include verified address, hours, timezone, accessibility and operational status. A public listing is sourced from an approved consumer inventory projection, not a CMS copy of private auctions.

Draft → review → approved → scheduled → published → stale/retired. Editors create and revise; topic experts and legal approve required categories; a separate publisher grants publication. Changes to canonical, robots, redirect or structured-data fields require SEO review; legal claims cannot be published without approval. Store prior revisions, actor, approval and timestamps; preview is authenticated and noindex. Publication is atomic by revision, cache invalidation is confirmed, and rollback restores a known approved revision without deleting audit evidence.

## Security and failure
Role- and object-scoped permissions; MFA for privileged publishers; sanitized rich text, allowed embeds and CSP; media provenance and rights expiration; no arbitrary script or privileged API key in content. On API/CMS outage serve a last approved public revision if still valid, label stale operational facts or withdraw them when accuracy cannot be guaranteed; never expose a draft. No private customer data in CMS analytics or content. Publication failure yields clear pending status and retry with idempotent revision key.

## Acceptance
Verify approval separation, draft leakage, malicious embed, access revocation, redirects/canonical and structured data, cache invalidation, broken asset and rollback. Report content owner and review date; maintain export format and vendor-exit plan. CMS choice remains **DECISION REQUIRED**.
