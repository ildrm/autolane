# Data quality and lineage

**ID:** 17/08_DATA_QUALITY · **Version:** 0.1 · **Status:** PROPOSED, subject to privacy, finance and product approval · **Owner:** Head of data · **Reviewers:** Analytics, security, legal, finance, product · **Updated:** 2026-11-15

## Critical data and checks
| Data / owner | Rule | Detection and response |
|---|---|---|
| Lead and appointment / CRM | Stable unique IDs, valid timestamps, status transition and branch reference. | Daily source-to-warehouse counts and orphan checks; quarantine invalid rows. |
| Inspection / operations | Published report has vehicle, checklist revision, reviewer and immutable report version. | Detect missing required evidence or duplicate revision; route to inspection owner. |
| Auction / auction service | Accepted bid references one auction, authoritative sequence and decision; one final outcome per auction version. | Compare accepted bid/order and close totals to source; never fix domain state from analytics. |
| Contract and settlement / finance | Case, currency, exact amount where permitted, verification evidence and status revision. | Reconcile counts/totals by currency; isolate mismatch, prohibit reporting financial totals as final. |
| Behavioral events / analytics | Valid schema/version, allowed purpose, UUID, UTC time and approved properties. | Reject unknown fields, duplicates and invalid consent; monitor arrival and deletion requests. |
| Valuation / pricing | Inputs, inspection/source revision, timestamp, confidence and model version. | Track missingness, implausible units, stale comparables and outcome linkage. |

## Quality controls and incident response
Measure completeness, validity, uniqueness, timeliness, consistency and lineage per dataset and named owner. Proposed checks run at ingestion and daily; thresholds require data-owner approval, and unresolved critical discrepancies mark downstream dashboards incomplete. Store raw immutable authorized records only within retention and legal constraints; corrections and late data are versioned, source-of-truth never replaced by inferred values. Alert owner with case count, impact and lineage; stop affected publication or model if data error risks user harm, correct at source where possible, replay idempotently, reconcile and document resolution.

## Acceptance
Synthetic test suite includes missing/replayed/out-of-order records, consent withdrawal, schema drift, invalid date/units, duplicate bid, financial rounding, stale report revision, unavailable source and deletion request. Dashboard shows freshness and quality status; validate that analysts lack raw identity documents and unapproved exports.
