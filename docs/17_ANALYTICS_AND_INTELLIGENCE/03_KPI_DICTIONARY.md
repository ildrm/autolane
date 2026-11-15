# KPI dictionary

**ID:** 17/03_KPI_DICTIONARY · **Version:** 0.1 · **Status:** PROPOSED, subject to privacy, finance and product approval · **Owner:** Head of data · **Reviewers:** Analytics, security, legal, finance, product · **Updated:** 2026-11-15

## Common conventions
Unless stated otherwise, count distinct stable entity IDs; use creation-date cohorts and a configurable matured observation window, calculate as-of date in UTC and report business-local period/timezone. Cancellations, fraud removals, duplicates, missing values and late arrivals are explicit categories, never silently imputed. Rates with zero denominator display “not enough data,” not 0%. Report absolute N, denominator, window, filters and freshness with each percentage. All metrics are **PROPOSED**, not observed results. Sources are authoritative domain records except consent-dependent attribution and satisfaction surveys; metrics must not require joining behavioral identifiers without legal approval.

## Business metrics
| KPI / owner | Numerator / denominator and cohort | Exclusions or caution |
|---|---|---|
| Lead acquisition cost / growth | Attributed acquisition spend ÷ distinct attributable new leads created in period. | State spend coverage, attribution method, currency/FX and unmatched costs; no zero-denominator value. |
| Qualified lead rate / sales | Leads marked qualified within window ÷ unique submitted leads in the creation cohort. | Separate unreviewed from rejected; report reversals. |
| Booking conversion / branch | Leads with ≥1 confirmed booking within window ÷ eligible leads in same creation cohort. | Exclude ineligible leads per versioned rule; no double count on reschedule. |
| Attendance / branch | Distinct scheduled appointments attended ÷ appointments scheduled to occur in period. | Segment canceled before cutoff and no-show; timezone and cutoff policy required. |
| Inspection completion / inspection | Inspections completed and published ÷ inspections started in matured cohort. | Distinguish rejected, returned and still in progress. |
| Auction participation / commercial | Approved organizations placing ≥1 accepted bid ÷ eligible organizations invited to that auction. | Per-auction rate, report invitation definition; no multiplication from team members. |
| Average bids per auction / auction | Accepted bid count ÷ finalized auctions in cohort. | Include no-bid auctions, exclude rejected/replayed submissions. |
| Auction success rate / auction | Auctions with a qualifying outcome ÷ finalized auctions. | Reserve and qualifying outcome require DEC-04 approval; seller acceptance is separate. |
| Seller acceptance / product | Offers explicitly accepted ÷ offers presented and whose response window has matured. | Show rejects, expired and unresolved; acceptance does not mean sale. |
| Dealer conversion / commercial | Approved dealer organizations placing a first accepted bid within window ÷ newly approved dealer organizations. | Report suspended and not-yet-matured separately. |
| Transaction completion / operations | Transactions closed with approved evidence ÷ transactions initiated in matured cohort. | Exclude cancellations only if separately disclosed; closure requires distinct milestones. |
| Revenue per transaction / finance | Earned net service revenue for transactions in cohort ÷ closed transactions. | Exclude vehicle gross value, show refunds, taxes, currency and revenue recognition policy. |
| Contribution margin / finance | (Net recognized revenue − attributable variable servicing and acquisition costs) ÷ net recognized revenue. | Cost allocation and revenue model pending; report absolute amount and FX separately. |
| Cash conversion cycle / finance | Days inventory outstanding + days sales outstanding − days payable outstanding, each computed from approved accounting balances and corresponding cost/revenue flows. | Only meaningful if relevant inventory/receivables/payables exist; alternatively report obligation-to-settlement duration; do not invent platform cash flows. |
| Customer satisfaction / support | Sum of valid survey scores ÷ number of valid responses; show scale and response rate. | Voluntary response bias; no imputation for nonrespondents. |
| Warranty claim rate / claims | Distinct eligible transactions with a claim submitted within policy window ÷ eligible transactions whose coverage window has matured. | Only when an approved warranty exists; separate accepted claims and duplicates. |
| Support resolution / support | Median and p90 elapsed time from case opened to first resolved, by cohort and business hours/calendar basis. | Reopens, pauses and unresolved cases reported separately to avoid survivor bias. |
| Repeat buyer rate / commercial | Buyers with ≥2 completed eligible transactions in period ÷ buyers with ≥1 completed eligible transaction in period. | Distinct organization, not users; right-censor recent buyers and show time horizon. |

## Operational metrics
| KPI / owner | Definition | Boundaries |
|---|---|---|
| Branch utilization / branch | Completed occupied slot-minutes ÷ staffed bookable slot-minutes in period. | Separate cancellations, maintenance and capacity overrides. |
| Inspector productivity / inspection | Completed published inspections ÷ inspector staffed hours. | Case mix, corrections and quality must accompany throughput. |
| Appointment capacity / branch | Sum configured bookable slots in period minus closures. | Report held, booked and available separately; no assumption slots are equal length. |
| Inspection turnaround / inspection | Median/p90 time from check-in to first published report. | Unpublished shown as open age; report clock/timezone. |
| Auction completion latency / auction | p95 server close commit minus policy deadline for due auctions. | Exclude documented extensions only per approved policy; measure correct deadline. |
| Payment reconciliation delay / finance | Median/p90 verified reconciliation time minus payment evidence received time. | Open discrepancies aged separately; no assumption platform has custody. |
| Contract processing time / legal | Median/p90 completed contract time minus contract prepared time. | Report returned/rejected and open age; approved template version. |
| Delivery performance / logistics | Deliveries evidenced by agreed deadline ÷ matured scheduled deliveries. | Distinguish cancellations, customer reschedule and no proof. |
| Dispute frequency / support | Distinct transactions with dispute opened ÷ eligible closed or initiated transaction cohort, explicitly choose one. | Report lifecycle and dispute type; no double count cases. |
| Fraud investigation volume / risk | Count distinct cases opened during period, plus unresolved age and decision outcome. | Not equivalent to confirmed fraud; restricted access. |

## Valuation metrics
| KPI / owner | Definition and exclusions |
|---|---|
| Valuation error / pricing | MAE = mean absolute difference between predicted point estimate and observed valid transaction price; median absolute percentage error excludes zero or missing true price; report currency, segment, horizon, sample and selection bias. |
| Prediction coverage / data science | Eligible scored cases with usable prediction ÷ all eligible requested cases; report abstentions and missing inputs. |
| Confidence calibration / data science | Actual proportion of outcomes falling in a stated prediction interval, by interval level and segment; compare to intended coverage with sample size. |
| Data freshness / data | p95 age since source observation to use; report late/missing records by source. |
| Drift / data science | Compare input and outcome distributions against named training baseline using documented tests and thresholds, plus missingness; drift is a warning, not proof of harm. |
| Override frequency / pricing | Estimates overridden by authorized reviewer ÷ estimates presented for review; include rationale and segment, measure before/after outcomes separately. |

## Governance
Every metric must also carry version, owner, source tables/events, time grain, calculation code review reference, legal basis, sensitivity, dimensions, lateness policy and change history in the eventual metric catalog. Financial definitions and eligibility policies require finance, legal and operational approval. Reconcile sample calculations and record original values alongside corrections.
