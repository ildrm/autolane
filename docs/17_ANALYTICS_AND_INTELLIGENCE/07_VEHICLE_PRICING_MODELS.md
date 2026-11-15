# Vehicle pricing models

**ID:** 17/07_VEHICLE_PRICING_MODELS · **Version:** 0.1 · **Status:** PROPOSED, subject to privacy, finance and product approval · **Owner:** Head of data · **Reviewers:** Analytics, security, legal, finance, product · **Updated:** 2026-11-15

## Purpose and staging
A valuation is a provisional, explainable range and not a bid, guaranteed sale price or binding offer. Inputs include make/model/variant, model year, mileage with unit, region, condition and published inspection revision; rights to comparable sales and regional data must be validated. Record source and timestamp, currency, model/rule version, data-quality flags and confidence category. Market and jurisdiction are not yet decided.

| Stage | Method | Benefits and limits | Safeguard |
|---|---|---|---|
| 1 | Transparent rules and analyst-reviewed comparable transactions; median/robust range after documented condition and mileage adjustments. | Easier audit with limited data; sparse comparables and analyst bias remain. | Show comparable age/count and adjustments; abstain or request manual review when insufficient. |
| 2 | Statistical regression with temporal validation and segment-specific uncertainty. | Estimates systematic relationships; assumes stable data and may fail rare vehicles. | Backtest by time/region, compare to stage 1 and audit residuals. |
| 3 | Carefully governed ML with calibrated intervals and controlled deployment. | May capture nonlinear patterns; adds drift, explainability and monitoring costs. | Shadow before serving; approval, model card, retraining and rollback required. |

## Decision and data contract
At request, validate taxonomy, age, mileage, inspection version and compatible currency/region; flag missing/outlier inputs. Select comparable window and minimum sample only after pricing analyst validates local data; no numeric threshold is currently approved. Return range, confidence, as-of time, explanation categories, provenance and “estimate, not an offer.” If low coverage, stale market data, unknown condition or model failure, abstain and route to an authorized analyst. Manual overrides require reason, actor, previous and new range, approval if policy demands, and audit; publish corrections as new revisions without overwriting historic forecasts.

## Measurement and risks
Report absolute error, interval coverage, segment coverage, data freshness and override rate as defined in the KPI dictionary. Use time-split evaluation and holdout, compare actual completed transactions while disclosing selection bias because unsold vehicles lack observed prices. Monitor protected/proxy geography and disparate error where legally and ethically permitted; do not use sensitive personal attributes without privacy approval. Ensure estimates are never used to automatically deny service or finance. No automated valuation model is claimed to exist.
