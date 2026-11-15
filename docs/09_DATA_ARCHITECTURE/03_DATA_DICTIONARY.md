# Data Dictionary

| Metadata | Value |
|---|---|
| ID / version | 09/03_DATA_DICTIONARY / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Data Dictionary; jurisdiction-dependent policy decisions remain open. |

## Field conventions
Common fields: `id UUID required`, `created_at timestamp with timezone required`, `updated_at timestamp with timezone required` and `version integer required default 1`; actor IDs and tenant/branch scope are required where the aggregate is scoped. IDs are never authorization. Optional fields are explicitly marked `?`; no omitted field may silently imply affirmative consent or cleared funds.

| Entity | Core fields and validation | Ownership / key and index |
|---|---|---|
| User | email? normalized, phone? E.164, status enum, verified_at? | Identity; unique normalized verified identifier under approved lifecycle policy. |
| OrganizationMember | user_id, organization_id, status, role_id; both IDs required | Dealer; unique organization/user active membership. |
| SellerLead | seller_id, vehicle_id, branch_id?, stage enum, consent_version, consent_at | Acquisition; index seller/stage and branch/stage. |
| Vehicle | make_id, model_id, trim_id?, year int, mileage int ≥0, mileage_unit, vin_ciphertext?, vin_lookup_hash? | Vehicle; scoped uniqueness for confirmed VIN according to jurisdiction, never log VIN. |
| Appointment | lead_id, branch_id, starts_at, ends_at, status enum, slot_id | Scheduling; start < end; transactional slot allocation and branch/time index. |
| Inspection | vehicle_id, inspector_id, template_version_id, status, branch_id | Inspection; assigned branch controls visibility and workflow. |
| InspectionRevision | inspection_id, revision int, report_object_ref, status, published_at?, publisher_id? | Inspection; unique inspection/revision; published content immutable. |
| Valuation | vehicle_id, currency ISO code, lower_minor, upper_minor, confidence?, policy_version, input_revision, approver_id? | Valuation; lower ≤ upper, amounts integer; override auditable. |
| Auction | vehicle_id, report_revision_id, policy_version, status, opens_at, closes_at, current_bid_minor?, currency, sequence, result_id? | Auction; version and locking protect bid/close; fixed currency. |
| Bid | auction_id, organization_id, actor_id, amount_minor integer >0, currency, sequence, accepted_at, command_key, payload_hash | Auction; unique auction/sequence and principal/operation/command_key; immutable accepted bid. |
| AuctionResult | auction_id, winning_bid_id?, outcome enum, decided_at, policy_version | Auction; unique auction; outcome may be no qualifying bid. |
| PaymentObligation | transaction_id, payer_party_id, payee_party_id, amount_minor, currency, due_at?, status, basis_document_id | Finance; no paid status without authorized evidence and reconciliation policy. |
| PaymentTransaction | obligation_id, provider_ref?, observed_amount_minor, currency, evidence_ref?, status | Finance; provider ref uniquely scoped by provider; provider timeout is unknown. |
| LedgerEntry | journal_id, account_id, debit_minor, credit_minor, currency | Finance; one side positive, balanced journal by currency, immutable reversal instead of edit. |
| AuditLog | actor_id?, action, object_type, object_id, occurred_at, correlation_id, before_hash?, after_hash?, reason? | Security; append only, access controlled, no full secrets. |

Example auction: `{id: "opaque-id", status: "open", currency: "EUR", current_bid_minor: 1250000, sequence: 7}` represents EUR 12,500.00 only when the configured EUR exponent is 2; amount units and rounding rules must always travel with currency metadata. Other required entity families and ownership are listed in [model](01_DATA_MODEL.md); exhaustive jurisdiction-specific fields, nullability, retention and migration constraints remain a required design review, not invented facts.

## Extended entity register

In this register `!` denotes required; `?` denotes nullable; IDs use opaque UUID. The common identity, timestamps, version, tenant scope, audit and retention rules above apply unless an append-only entity specifies otherwise. Each reference below is owned by its context, so access to one linked record does not confer access to another. Retention and deletion duration remain **DECISION REQUIRED**; all financial, identity, evidence, contract and audit data are restricted and subject to legal hold. Null is not an affirmative status. The listed required fields are a minimum logical model, not an exhaustive database migration specification.

| Entity / owner | Required business fields; nullable fields; invariant and lookup | Lifecycle, confidentiality and example |
|---|---|---|
| UserProfile / Identity | `user_id!`, `display_name!`, `phone?`, `locale!` (default `en`) | User-scoped profile; personal data; example locale `en`. |
| Role / IAM | `name!`, `scope_type!`, `version!` | Versioned grant bundle, least privilege; example `branch_inspector`. |
| Permission / IAM | `resource!`, `action!`, `constraints!` | Unique action/resource/scope; administrative data; example `inspection:publish`. |
| Organization / Dealer | `legal_name!`, `jurisdiction!`, `status!`, `registration_number?` | Pending/active/suspended; confidential business data. |
| DealerAccount / Dealer | `organization_id!`, `status!`, `approved_at?`, `policy_version!` | One current organization account; bid rights require active membership. |
| DealerVerification / Dealer | `organization_id!`, `status!`, `reviewer_id?`, `evidence_ref?`, `decision_at?` | Separate evidence and review history; restricted identity data. |
| Branch / Branch | `name!`, `jurisdiction!`, `timezone!`, `address!`, `status!` | Public branch details are a separate approved projection; example timezone `Europe/Paris`. |
| BranchSchedule / Branch | `branch_id!`, `local_day!`, `start_local!`, `end_local!`, `capacity!` | Version schedules; holiday overrides; start before end and capacity nonnegative. |
| BranchEmployee / Branch | `branch_id!`, `user_id!`, `assignment_status!` | Active branch/user association is unique; personnel data restricted. |
| VehicleMake / Vehicle | `name!`, `slug!`, `status!` | Unique canonical slug in taxonomy version; public when approved. |
| VehicleModel / Vehicle | `make_id!`, `name!`, `slug!`, `status!` | Unique make/slug within catalog version. |
| VehicleTrim / Vehicle | `model_id!`, `name!`, `model_year?`, `status!` | Belongs to model; optional model year must be plausible. |
| VehicleSpecification / Vehicle | `vehicle_id!`, `key!`, `value!`, `unit?`, `source!` | Unique key/version per vehicle, unit from controlled vocabulary. |
| VehicleOwnership / Vehicle | `vehicle_id!`, `party_id!`, `claim_status!`, `evidence_ref?`, `verified_at?` | An assertion is not legal title confirmation; sensitive evidence. |
| VehicleDocument / Vehicle | `vehicle_id!`, `kind!`, `object_ref!`, `checksum!`, `scan_status!` | Only clean authorized file is retrievable; private, versioned evidence. |
| VehicleMedia / Vehicle | `vehicle_id!`, `object_ref!`, `usage_rights!`, `visibility!`, `alt_text?` | Publication requires consent and media review; revisions retained per policy. |
| InspectionTemplate / Inspection | `jurisdiction!`, `version!`, `status!`, `effective_at?` | Approved version pinned to inspections; immutable after publication. |
| InspectionItem / Inspection | `template_version_id!`, `code!`, `label!`, `required!`, `value_type!` | Unique code/template version; condition must be representable, not assumed proprietary checklist. |
| InspectionFinding / Inspection | `inspection_id!`, `revision_id!`, `item_id!`, `value!`, `severity?`, `comment?`, `evidence_ref?` | Unique revision/item; findings belong to an immutable published revision or editable draft revision. |
| InspectionReport / Inspection | `inspection_id!`, `current_revision_id?`, `status!` | Links approved immutable revision, access scoped by actor and auction eligibility. |
| ValuationAdjustment / Pricing | `valuation_id!`, `kind!`, `amount_minor!`, `currency!`, `reason!` | Signed integer adjustment; currency equals valuation; audit overrides. |
| MarketPriceRecord / Pricing | `vehicle_class!`, `amount_minor!`, `currency!`, `observed_at!`, `source!`, `region?` | Source rights and provenance required; restricted commercially sensitive data. |
| AuctionParticipant / Auction | `auction_id!`, `organization_id!`, `eligibility_status!`, `policy_version!` | Unique auction/organization; bidder must also have active personal grant. |
| AuctionDispute / Auction | `auction_id!`, `claimant_id!`, `status!`, `reason!`, `resolution?` | Preserve bids and event history; outcome requires authorized review. |
| VehicleListing / Consumer | `vehicle_id!`, `status!`, `asking_minor!`, `currency!`, `published_revision?` | Public only after review and explicit publication; independent of auction visibility. |
| PurchaseRequest / Consumer | `buyer_id!`, `listing_id!`, `status!`, `contact_id!`, `consent_version!` | Validate authoritative listing availability; private buyer contact. |
| ProcurementRequest / Sourcing | `buyer_id!`, `criteria!`, `budget_minor?`, `currency?`, `status!` | Buyer may withdraw; budget/currency paired when present. |
| FinancingApplication / Finance | `party_id!`, `provider_id!`, `consent_ref!`, `status!`, `provider_ref?` | Restricted financial data; provider decision is external, no assumed approval. |
| FinancingOffer / Finance | `application_id!`, `terms_ref!`, `expires_at!`, `status!` | Exact lender terms and required disclosure; sensitive and versioned. |
| Contract / Legal | `transaction_id!`, `template_version!`, `status!`, `document_hash?`, `executed_at?` | Immutable executed version; authorization and legal hold apply. |
| ContractDocument / Legal | `contract_id!`, `revision!`, `object_ref!`, `checksum!`, `scan_status!` | Unique contract/revision; encrypted and access audited. |
| ContractSignature / Legal | `contract_id!`, `signer_id!`, `document_hash!`, `provider_ref?`, `verified_at?` | Signature evidence bound to exact document version; status not inferred from provider timeout. |
| Refund / Finance | `transaction_id!`, `amount_minor!`, `currency!`, `status!`, `approver_id?`, `provider_ref?` | Model requires approved custody policy; no execution implied. |
| Fee / Finance | `basis_id!`, `amount_minor!`, `currency!`, `policy_version!`, `payer_id!` | Fees nonnegative unless explicit adjustment; legal terms and tax rules open. |
| ReconciliationRecord / Finance | `obligation_id!`, `status!`, `source_ref!`, `reviewer_id?`, `resolved_at?` | Only independent authorized reviewer can reconcile; no deletion of evidence. |
| LogisticsOrder / Logistics | `transaction_id!`, `carrier_id?`, `status!`, `pickup_window?`, `destination!` | Assigned carrier sees necessary transfer data only. |
| VehicleHandover / Logistics | `vehicle_id!`, `from_party!`, `to_party!`, `occurred_at!`, `condition_ref!` | Signed custody evidence is not legal title. |
| Delivery / Logistics | `order_id!`, `status!`, `proof_ref?`, `completed_at?` | Delivery requires verified proof; exception state for damage/delay. |
| WarrantyPolicy / Claims | `jurisdiction!`, `version!`, `coverage_ref!`, `status!`, `effective_at?` | Only approved policy may be offered; immutable version. |
| WarrantyClaim / Claims | `policy_version!`, `claimant_id!`, `vehicle_id!`, `status!`, `decision_ref?` | Review and financial remedy approval separated; sensitive claim evidence. |
| SupportTicket / Support | `requester_id!`, `category!`, `status!`, `assigned_to?`, `transaction_id?` | Access by case assignment; audit sensitive disclosures. |
| Notification / Communications | `recipient_id!`, `template_version!`, `channel!`, `delivery_status!`, `provider_ref?` | Message sent and business action accepted are separate events; consent respected. |
| NotificationTemplate / Communications | `name!`, `channel!`, `version!`, `locale!`, `body_ref!`, `status!` | Approved immutable version; avoid secrets in messages. |
| CMSArticle / Content | `slug!`, `title!`, `body_ref!`, `author_id!`, `status!`, `published_at?` | Public only after editorial approval; unique slug per content version policy. |
| SEOPage / Content | `path!`, `canonical_url!`, `robots_policy!`, `content_version!` | Validate canonical and avoid indexing private paths. |
| AnalyticsEvent / Analytics | `event_id!`, `name!`, `occurred_at!`, `schema_version!`, `purpose!`, `subject_key?` | Deduplicate ID, pseudonymize and enforce consent/retention. |
| FeatureFlag / Administration | `name!`, `environment!`, `state!`, `effective_at?`, `approver_id?` | Sensitive policy changes require authorization, audit and approved rollout. |

Common field lengths, enum authority and relational checks are specified in the field-constraints supplement; transport field details are in OpenAPI and the schema reference. Jurisdiction-specific retention and legal evidence remain decisions requiring approval; physical migrations are intentionally outside this documentation phase.

## Critical missing-record supplements

The following proposed records complete logical relationships needed by the discovery loop; they do not substitute for jurisdiction-specific policies or a physical schema. Common metadata, access and retention conventions above apply.

| Entity / owner | Logical fields and constraints | State, security and behavior |
|---|---|---|
| AppointmentSlot / Scheduling | `id!`, `branch_id!`, `starts_at!`, `ends_at!`, `capacity!` ≥0, `reserved_count!` between 0 and capacity, `calendar_version!`, `version!`; `starts_at < ends_at`. | Branch-scoped; reservation and release are atomic with Appointment updates; inspect conflicting schedule edits before capacity reductions. Local branch display derives from branch timezone and UTC instants. |
| SellerDecision / Seller transaction | `id!`, `auction_result_id!`, `offer_version!`, `seller_id!`, `decision!` (`accept` or `reject`), `recorded_at!`, `policy_version!`, `consent_evidence_ref?`, `command_key!`. | One effective decision per offer version under approved correction policy; seller ownership and valid time verified server-side. Reject stale commands and retain original decision and authorized corrections. A decision is not proof of contract, payment or title. |
| TransactionCase / Transaction coordination | `id!`, `seller_id!`, `channel!` (`dealer_auction` or `consumer`), `buyer_party_id!`, `buyer_organization_id?`, `vehicle_id!`, `auction_result_id?`, `consumer_offer_id?`, `policy_version!`, `status!`, `owner_id!`, `version!`; references to contract, obligation, transfer and handover records are optional until present. | Exactly one origin is required: dealer_auction requires auction_result_id and buyer_organization_id; consumer requires consumer_offer_id and buyer_party_id. State is a coordination projection derived from separately owned facts. Closure requires an approved policy's evidence and independent checks; a missing or unknown external outcome cannot be represented as complete. Restrict each field by actor and purpose. |
| OwnershipTransfer / Legal operations | `id!`, `transaction_id!`, `status!`, `jurisdiction!`, `version!`, `evidence_ref?`, `recorded_by?`, `verified_at?`. | Record verified external transfer milestones with evidence. Status enum, authority and proof depend on DEC-01 and DEC-05; physical custody is separate. Scope identity evidence to authorized legal staff. |
| IdempotentCommand / owning context | `principal_id!`, `operation!`, `key!`, `payload_hash!`, `state!`, `created_at!`, `result_ref?`, `expires_at!`; unique principal/operation/key. | Same key and payload returns recorded outcome, different payload conflicts. Retention and recovery must prevent a retry after expiration from causing a second financial or binding action; exact window requires policy. |
| OutboxEvent / source context | `event_id!`, `aggregate_type!`, `aggregate_id!`, `aggregate_sequence!`, `schema_version!`, `type!`, `occurred_at!`, `payload!`, `delivery_state!`. | Insert in same transaction as source change; at-least-once dispatch with idempotent consumers. Payload excludes direct identity documents and secrets; protect internal topics. |

Acceptance: two concurrent reservations cannot exceed slot capacity; replayed seller decision with the same payload returns the original result; transaction closure cannot be asserted from custody or an uploaded receipt alone. Exact field formats, state enums, indexes, retention, deletion and cross-context mappings remain review items.

## Expanded contract baseline — revision 0.3

[Field constraints](10_FIELD_CONSTRAINTS.md) define common logical field types, cross-field checks, relational integrity and lifecycle precision; OpenAPI shapes are authorized projections, not a substitute for persistence ownership.
