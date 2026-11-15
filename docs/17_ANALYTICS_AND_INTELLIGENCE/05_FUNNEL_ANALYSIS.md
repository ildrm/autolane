# Funnel analysis and attribution

**ID:** 17/05_FUNNEL_ANALYSIS · **Version:** 0.1 · **Status:** PROPOSED, subject to privacy, finance and product approval · **Owner:** Head of data · **Reviewers:** Analytics, security, legal, finance, product · **Updated:** 2026-11-15

## Cohorts and steps
| Funnel | Eligible first event / linked steps | Success and open-state treatment |
|---|---|---|
| Seller | Unique submitted lead → qualified → confirmed booking → attended → inspection published → auction finalized → seller accepted → transaction closed. | One lead cohort with configurable maturation window; show cancellations, rejections, no bid, pending and duplicates separately. |
| Dealer | Application submitted → approved → first eligible auction → first accepted bid → qualifying win → closed purchase. | Count organizations, not individual users; approved and invited denominators separately. |
| Consumer | Consented public listing view → inquiry submitted → appointment → transaction if available. | Views are consent-dependent; authoritative inquiry and closure are separate data sources. |
| Valuation | Consented start → completed estimate → lead submitted → booking. | A valuation is not an offer or a sale; treat low-confidence review separately. |
| Finance | Consent → provider inquiry → provider decision → funding if confirmed. | Do not infer approval or payout from an application; restricted group access. |

For each cohort publish numerator, denominator, observation window, delay to maturity, time to next step and missingness; do not multiply events for revisits, edits or reschedules. Late events recalculate prior periods with versioned as-of snapshots. Track abandonment only where interaction events are legally permitted; behavioral and operational counts have different populations, so do not silently divide one by the other.

## Attribution and privacy
Proposed default is first observed eligible source within a fixed window, plus last eligible source as a sensitivity view; specific window and channel mapping are **DECISION REQUIRED**. A visitor whose consent or source is unavailable remains unattributed. Campaign parameters are allowlisted and stripped of identifiers; do not collect full query strings. Content-assisted conversion is a descriptive observed path, not proof of causation. Deletion/withdrawal is propagated under approved policy; identity stitching requires explicit legal review.

## Analysis and tests
Display sample size, confidence intervals where valid, channel mix, missingness and consent coverage; compare segments only with enough eligible observations and privacy threshold. Validate duplicate, anonymous-to-authenticated, late, canceled and cross-device paths using synthetic data. If a funnel denominator or source changes, version the metric and avoid comparing incompatible periods.
