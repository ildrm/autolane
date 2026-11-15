# Policy baseline and decision boundaries

**ID:** POLICY-BASELINE · **Version:** 0.3 · **Status:** proposed engineering baseline, legal activation blocked · **Owner:** Product and architecture · **Reviewers:** Legal, finance, security, operations · **Updated:** 2026-11-15

## Three independent readiness states

Documentation completeness means requirements, contracts and expected results are specified and internally checked. Implementation verification means a built system passes tests. Business authorization means named owners have approved jurisdiction, terms and responsibilities. No software exists in this repository, so application test results, live Core Web Vitals and penetration-test results cannot be prerequisites to finishing documentation. They are future release gates. Unselected providers and legal rules are decision dependencies, not a reason to omit reversible engineering designs.

## Proposed working decisions

| Key | Default and validation | Change rule / activation |
|---|---|---|
| platform.language | `en`; LTR; UTF-8; all product copy English. | Localization can add language later; no inferred jurisdiction. |
| auction.authority | Primary transactional database, per-auction serialized bid and close; time sampled after locks. | Any change needs architecture/auction review and boundary tests. |
| auction.tie | First valid committed sequence wins; subsequent equal amount fails increment. | Proposed commercial rule requiring DEC-04 before live auction. |
| auction.increment_minor | Positive integer in configured currency; required, no implicit value. | Pin immutable policy version before scheduling. |
| auction.start_minor | Positive integer required; first bid >= start; later bids >= leader + increment. | Validate overflow before arithmetic; keep within declared amount maximum. |
| auction.reserve_minor | Null means no reserve; otherwise >= start; disclosure required by pinned policy. | Reserve miss yields no_qualifying_bid, never a silently selected buyer. |
| auction.extension_enabled | false; proxy/automatic bidding false; deposits false. | Explicitly designed and approved variant before activation. |
| auction.pause | Safety hold rejects bids; original cutoff unchanged. Resume only before cutoff; close held auction as pending_review. | Incident/dispute resolution requires separate reviewed case; do not retroactively change auction ledger. |
| seller.offer_expires_at | Required explicit UTC instant, later than offer creation. | Legal/commercial duration remains DEC-04. Expiration and acceptance share lock and authoritative time. |
| finance.mode | `external_evidence_only` as design baseline; no custody, escrow, credit or automatic transfers. | DEC-02/03 required for any live money-flow promise. |
| finance.reconciliation_tolerance_minor | 0; currency and parties must match; any exception is independently approved and recorded. | No silent write-off or floating-point calculation. |
| auth.staff_mfa | required; privileged step-up expires after 5 minutes; idle session 30 minutes, absolute 12 hours (proposed). | Security may tighten; weakened values require review and tests. |
| idempotency.receipt | Retain key/hash/result reference for 30 days minimum, binding bid/financial receipt for underlying transaction evidence lifecycle. | Expired full response retains tombstone and stable outcome reference; never re-execute a binding action after key expiry. Legal retention remains DEC-07. |
| provider.retry | Backoff 1, 5, 30, 120, 600 seconds with jitter; then owned exception. | Retry only provider-approved idempotent request; unknown money result requires query/reconciliation. |
| provider.callback | Authenticate source, timestamp and replay key; persist inbox before 202; processing is asynchronous. | Raw provider payload stays in adapter boundary; provider-specific signature must be specified before integration. |
| retention.production | No universal duration; required class-specific approved schedule and hold policy before collection. | Synthetic documentation fixtures do not authorize production collection. |

## Non-negotiable invariants

An accepted bid, seller decision, executed contract, payment evidence, independently reconciled obligation, legal title and physical custody are distinct records. Client timeout is not a failed business operation. A legal hold, restrictive scope or current account suspension overrides a cached permission. Audit cannot be repaired by silently rewriting history. Important updates use immutable revisions, causation and independent review where specified.

Sources for engineering semantics: [OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.0.html), [HTTP conditional requests](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match), [PostgreSQL clock semantics](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT), accessed 2026-11-15. These sources do not establish commercial or legal policy.
