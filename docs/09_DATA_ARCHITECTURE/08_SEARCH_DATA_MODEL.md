# Search Data Model

| Metadata | Value |
|---|---|
| ID / version | 09/08_SEARCH_DATA_MODEL / 0.3 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Search Data Model; jurisdiction-dependent policy decisions remain open. |

## Consumer search projection
Only consumer-approved listings enter a public search index. Document fields: listing ID and revision, public vehicle make/model/trim, year, mileage and unit, region, asking amount in minor units and ISO currency, approved thumbnails, public inspection summary, availability and last source update. Exclude VIN, seller contact, identity files, internal notes, bidder identity, private inspection detail and reserve. Dealer-only auction discovery is a separately authorized projection and index or security boundary, never merely a public filter.

Events update projection idempotently by aggregate ID and version; ignore older versions, delete on unpublish and run periodic reconciliation. Search may lag; before inquiry or reservation recheck authoritative status. Filters include brand, year, mileage, price, region, body and transmission; numeric sorting is within a selected currency or explicitly converted by dated policy, never mix amounts across currencies. Use deterministic sort with ID tie breaker and cursor pagination. Rebuild from source snapshots and replay outbox; measure lag, missing documents and unauthorized fields. Empty, stale and unavailable states must be shown accurately.

## Document shape, ranking and reconciliation

Index one current approved public listing revision: `listing_id`, `public_slug`, `revision`, `availability`, `make_id`, `model_id`, `year`, `mileage_value`, `mileage_unit`, `asking_minor`, `currency`, coarse `region_id`, `body_type`, `transmission`, approved image rendition and `published_at`. Do not index VIN, ownership files, phone, precise private address, reserve, bids or unpublished report findings. Facet values come from the active taxonomy; missing values appear as unknown, not zero.

Default ordering is available first, newest published revision then stable listing ID. Explicit sorts support asking price, mileage or year plus ID tie-breaker within permitted units/currency. Cursor binds normalized filter, sort and index version; changed filter invalidates cursor. Query text ≤200 characters, page size 25 with maximum100; do not execute caller-supplied query DSL. Zero results show removable filter chips and saved/sourcing alternatives, never invented inventory.

Replay applies only newer revisions; a tombstone wins over older publication events. A daily proposed reconciliation samples missing/stale documents and checks complete counts by publication state; an emergency delist also uses direct cache invalidation and a read-time publication gate. Expose index timestamp and lag; if freshness exceeds the agreed threshold, degrade to authoritative filtered reads or show unavailable search, never serve restricted data from an old index.
