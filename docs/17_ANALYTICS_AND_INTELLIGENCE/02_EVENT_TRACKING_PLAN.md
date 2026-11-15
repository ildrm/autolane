# Event tracking plan

**ID:** 17/02_EVENT_TRACKING_PLAN · **Version:** 0.1 · **Status:** PROPOSED, subject to privacy, finance and product approval · **Owner:** Head of data · **Reviewers:** Analytics, security, legal, finance, product · **Updated:** 2026-11-15

## Event envelope
Event names are lower_snake_case past-tense facts. A domain event is authoritative only when emitted from the owning system after committed state; UI interactions are analytics observations, not proof of business completion. All events contain `event_id` (UUID), `event_name`, `schema_version` (integer), `occurred_at` (producer UTC ISO 8601 instant) and `received_at` (collector UTC ISO 8601 instant), `source`, `environment`, `purpose`, and privacy-safe `correlation_id`. Optional `session_id` and pseudonymous actor ID require applicable consent/legal basis; `screen_id` uses UX inventory IDs where applicable. Business entities stay in restricted event channels using opaque IDs, never customer-visible identifiers or raw VIN. A versioned consent status and policy reference must be evaluated at collection time; do not send optional events before consent where required.

## Catalog
| Event | Trigger/source and minimal allowed properties | Measurement / duplication rule |
|---|---|---|
| `sell_start_selected` | Seller selects Start selling on public page; screen, coarse channel. | Consented CTA interaction only; distinct from a flow loaded or a created lead. |
| `sell_flow_started` | Seller UI starts; screen, coarse channel. | Count consented starts by event ID; not a lead. |
| `lead_submitted` | Lead service confirms creation; opaque lead ID, policy version. | Distinct leads after server commit; exclude duplicate/rejected per KPI definition. |
| `lead_qualified` | Authorized staff/service changes qualification; lead ID, outcome category. | State history supports matured cohort; qualification may be reversed. |
| `appointment_booked` | Booking committed; booking ID, opaque branch ID, scheduled instant. | Distinct confirmed bookings; reschedule not a new lead. |
| `appointment_attended` | Authorized check-in committed; booking ID and attendance category. | Distinct attended appointments. |
| `inspection_published` | Supervisor publishes report revision; inspection ID, revision. | Count inspections by distinct ID; revisions separate. |
| `valuation_completed` | Service/analyst publishes range; opaque valuation ID, model/rule revision, confidence band. | No price in general analytics; restricted valuation store holds values. |
| `dealer_application_submitted` | Dealer registration committed; opaque application ID. | Unique applications; approval is separate. |
| `dealer_approved` | Review commits approval; organization ID in restricted channel. | Count unique approved organizations; exclude withdrawn/duplicate applications. |
| `auction_opened` / `auction_closed` | Auction service commits state; opaque auction ID, policy version, outcome category on close. | Deduplicate by event ID; canonical auction state determines outcome. |
| `bid_submitted` / `bid_decided` | UI starts / server commits bid decision; opaque auction/bid ID, accepted/rejected category, reason category. | Never infer acceptance from UI submit; general analytics excludes amount. |
| `offer_decided` | Seller decision recorded; opaque offer ID and accept/reject category. | Distinct offer; expiry and pending tracked separately. |
| `contract_status_changed` | Contract service records milestone; case ID, status category. | Status does not imply payment/title. |
| `settlement_verified` | Finance confirms payment evidence; case ID and verification category. | No money amount in general analytics; correction event adjusts reporting. |
| `transaction_closed` | Authorized closure committed; case ID, outcome category. | Distinct case; excludes cancellations and provisional closure. |
| `consumer_inquiry_submitted` / `sourcing_request_submitted` | Service accepts request; opaque request ID, page family. | Distinct requests; no message text. |
| `financing_inquiry_submitted` | Provider inquiry accepted under consent; opaque request ID, provider category. | Inquiry is not approval or funded loan. |
| `support_case_resolved` | Support commits resolution; case ID, opened/resolved UTC, resolution category. | Reopens measured separately; no free-text payload. |
| `content_viewed` | Consented page view; canonical page family, page ID, campaign source category. | No query text or full URL containing parameters. |

## Versioning, controls and tests
Schemas document required/optional properties, enums, null semantics, producer, consumer, purpose and retention; additive compatible changes require review and breaking changes increment version. Events use deterministic idempotency key from source for replay; deduplicate by `source+event_id` and retain corrections as separate causally linked facts, not silent overwrites. Reject/strip free text, full URL query, names, phone, email, VIN, identity documents, payment identifiers and precise location from general analytics. Tests cover consent denied/withdrawn, duplicate and delayed events, invalid enum/version, timestamp skew, service replay and source-to-report counts. Analytics naming here is proposed and must be reconciled with product, backend and QA catalogs before implementation.

## Mapping to operational event contracts
The following mappings are proposals for an ingestion transformation, not equivalences between optional behavior tracking and a domain event. The restricted domain envelope in [event contracts](../10_BACKEND_AND_APIS/08_EVENT_CONTRACTS.md) has `type`, aggregate sequence and causation; the analytics envelope has `event_name`, purpose and collector receipt time. A schema registry must formally approve these transformations and applicable legal basis.

| Operational event | Analytics projection | Transformation and distinction |
|---|---|---|
| `appointment.confirmed` | `appointment_booked` | One committed appointment; map appointment ID and starts_at; suppress contact details. |
| `inspection.report_published` | `inspection_published` | Map inspection ID and report revision; never publish photographs. |
| `auction.bid_accepted` | `bid_decided` with accepted category | Suppress amount and currency in general analytics. A rejection needs a separate authorized producer event; it cannot be inferred from absence of acceptance. |
| `auction.closed` | `auction_closed` | Map outcome only after privacy review; no winning identity in general analytics. |
| `seller.decision_recorded` | `offer_decided` | Map only accept/reject, keeping expiry as a distinct outcome, and retain decision version for correction. |
| `settlement.reconciled` | No automatic equivalence | `settlement_verified` means evidence verified and can precede or differ from reconciliation; finance must define separate authoritative producer and mapping. |

Domain events may be required for operations even when optional behavioral analytics is declined. That distinction does not establish a legal basis or exempt any use from privacy review. `bid_submitted` denotes a consented UI observation, not a domain command or accepted bid; projection delivery may be delayed or absent without altering business state.

## Expanded contract baseline — revision 0.3

The fixed `workflow_outcome_recorded` v1 event is defined in the [analytics JSON Schema](../contracts/workflow-analytics.schema.json). Its scenario_id is a property, not a dynamically generated event name; purpose and collection policy remain mandatory.
