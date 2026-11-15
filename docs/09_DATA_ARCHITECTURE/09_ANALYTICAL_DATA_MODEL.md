# Analytical Data Model

| Metadata | Value |
|---|---|
| ID / version | 09/09_ANALYTICAL_DATA_MODEL / 0.3 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Analytical Data Model; jurisdiction-dependent policy decisions remain open. |

## Analytical model
Proposed warehouse marts are derived, not authoritative. Grain: `fact_auction` one row per finalized auction; `fact_bid` one accepted bid with pseudonymous organization key and auction version; `fact_appointment` one appointment lifecycle; `fact_transaction` one commercial transaction; `fact_notification` one delivery attempt. Conformed dimensions include date, branch, vehicle taxonomy, market and policy version. Keep contract and payment evidence outside broad BI access.

Ingest committed events with stable event ID, event/schema version, occurred time, received time, aggregate sequence and consent/purpose eligibility; deduplicate by event ID. Reconcile record counts and monetary totals against source by day and currency, track late data and corrections. Calculate auction participation as distinct qualified organizations per finalized auction, including zeros; conversion cohorts need explicit start time and maturity. No currency summation across codes without a dated and documented exchange-rate source.

Role-scoped aggregate access and privacy-preserving thresholds guard small populations; prevent re-identification through joins. Data quality gates cover freshness, nulls, duplicated IDs, invalid sequences, consent and currency. Failed checks quarantine the affected report and identify owner. Historical corrections use versioned facts, not quiet rewrites. Legal approval establishes retention and deletion propagation.

## Metric grain and correction rules

| Mart | Primary grain / key | Allowed measures and reconciliation |
|---|---|---|
| Acquisition | One submitted lead, cohort by submission day | Eligible and booked counts; distinguish duplicate/withdrawn outcomes. |
| Inspection | One published report revision | Inspection duration and rework; count first publication separately from correction. |
| Auction | One auction and separate one-row-per-accepted-bid fact | Organization count, qualifying winner and close latency; exclude client click attempts. |
| Conversion | One accepted origin/transaction | Seller-accepted auction and buyer-accepted consumer offer reported separately. |
| Finance | One approved allocation/reversal fact | Currency-separated obligation coverage and exception age; not revenue unless accounting policy permits. |
| Service | One ticket/claim lifecycle plus event history | First response, resolution, reopen rate; disclosed clock pauses. |

Late events update a versioned partition and mark affected reports revised; a changed metric definition increments metric version and requires backfill or clear break in series. Store valid-time and recorded-time where corrections matter. Dimensions with changing branch, policy or organization classification preserve historical attribution rather than retroactively applying the newest label. Analyst exports follow the same purpose and small-cohort controls as dashboards. A pseudonymous organization key remains potentially personal or confidential; it is not assumed anonymous.
