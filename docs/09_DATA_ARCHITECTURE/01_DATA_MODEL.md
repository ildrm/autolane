# Data Model

| Metadata | Value |
|---|---|
| ID / version | 09/01_DATA_MODEL / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Data Model; jurisdiction-dependent policy decisions remain open. |

## Model conventions and ownership
**PROPOSED.** Entity identifiers are opaque UUIDs; timestamps are UTC instants; date-only values represent a local civil date with jurisdiction when required. Each mutable aggregate carries `version`, created/updated timestamps and actor; soft deletion is not a retention policy. Sensitive identity and contact information must be separated or encrypted and exposed only to authorized purposes. See [dictionary](03_DATA_DICTIONARY.md) and [retention](07_DATA_RETENTION.md).

| Aggregate / owner | Records and relationships | Invariants and access |
|---|---|---|
| Identity | User, UserProfile, Role, Permission, Organization, OrganizationMember | Unique membership per organization and user; roles scoped by organization/branch; account suspension blocks new actions. |
| Dealer | DealerAccount, DealerVerification | Organization has one current status and versioned verification evidence; checks remain private. |
| Branch | Branch, BranchSchedule, BranchEmployee, Appointment | Appointment has branch and reserved slot; allocation must not exceed capacity under concurrency. |
| Acquisition | SellerLead, consent and contact | Seller and vehicle references; access limited to customer and assigned staff. |
| Vehicle | VehicleMake, VehicleModel, VehicleTrim, VehicleSpecification, Vehicle, VehicleOwnership, VehicleDocument, VehicleMedia | Taxonomy hierarchy valid; confidential identifiers encrypted; ownership assertions are distinct from proof of title. |
| Inspection | InspectionTemplate, InspectionItem, Inspection, InspectionFinding, InspectionReport, InspectionRevision | Template and report revisions immutable once published; findings belong to versioned template and inspection; auction pins report revision. |
| Valuation | Valuation, ValuationAdjustment, MarketPriceRecord | Versioned inputs, currency, range and confidence; overrides require authorized reason. |
| Auction | Auction, AuctionParticipant, Bid, AuctionResult, AuctionDispute | At most one finalized outcome, sequence unique per auction; accepted bids and audit immutable; unique command key per principal. |
| Consumer | VehicleListing, PurchaseRequest, ProcurementRequest | Public listing state is independent of dealer-auction state and permits only reviewed public fields. |
| Finance | FinancingApplication, FinancingOffer, PaymentObligation, PaymentTransaction, Refund, Fee, LedgerEntry, ReconciliationRecord | Obligations and observed external transactions separated; posted ledger journals balance per currency; unknown != settled. |
| Legal / logistics | Contract, ContractDocument, ContractSignature, LogisticsOrder, VehicleHandover, Delivery | Contract pins template/document; delivery and title transfer are separate state. |
| Service / governance | WarrantyPolicy, WarrantyClaim, SupportTicket, Notification, NotificationTemplate, CMSArticle, SEOPage, AnalyticsEvent, AuditLog, FeatureFlag | Claims governed by approved policy; immutable access audit; consent gates analytics and messaging. |

Deletion, pseudonymization and legal hold rules require jurisdiction and legal review. No object store URI is a permanent public credential. Cross-context references identify an aggregate, never transfer its write ownership. Entity-level field detail and examples are specified for the critical loop in the data dictionary; extended entity fields require owner review before migration design.
