# Panel implementation contracts

**ID:** PANEL-CONTRACTS · **Version:** 0.3 · **Status:** proposed · **Owner:** Product design and domain operations · **Reviewers:** Security, API, QA, accessibility · **Updated:** 2026-11-15

## Shared contract for all 20 panels

These are logical authorization boundaries, not 20 independent deployments. Each panel below supplies its navigation, fields, actions, data, metrics and ownership. Together with this common behavior they specify the 30 requested panel dimensions without redefining common controls. Client filtering never replaces object authorization.

**Layout and widgets:** desktop uses 240px collapsible navigation, page heading and scope/date context, maximum three summary metrics, action bar, primary table/content and an optional case-detail drawer. Tablet collapses navigation; mobile uses an agenda/list and a full-screen detail route rather than a compressed desktop table. Tables offer stable server sorting and 25-row default pages (max 100), persistent labeled filters, result count and freshness. Search queries are bounded to 200 characters, debounced 250ms for suggestions, cancel stale requests, and never enter general analytics. Critical actions remain accessible without hover or drag.

**State and copy contract:** initial load reserves layout and announces “Loading”; no sensitive stale content from a previous account persists. Empty copy is specified per panel. A failed read shows “We could not load this information. Try again.” with retry and safe reference. Denied access shows “You do not have access to this record.” without leaking existence. A successful command displays the authoritative new state and next action; unknown timeout displays “We are checking the result. Do not submit a new request.” and reconciles the original key. 412 shows “This record changed. Review the latest version.”; 422 links an error summary to labeled fields and preserves safe input. Notifications are supplementary; critical messages remain inline.

**Creation/edit/approval:** mandatory fields marked, optional fields explicit; submit validates on server. Mutations carry idempotency; editable resource uses ETag/If-Match. Approval view shows before/after, actor, policy and evidence; maker/checker and step-up enforced on server. Destructive confirmation names object and consequence, with default focus on Cancel. Bulk operations return per-item accepted/rejected results and audit each item; no hidden all-or-nothing success. Critical bid, offer, signature, payment, title and claim decisions are single-object operations.

**Documents, reports and exports:** quarantine uploads, show scan state, allow only clean scoped evidence through short-lived access; version/checksum accompanies published documents. Export is a separately authorized asynchronous job with purpose, filter snapshot, row count, expiry and audit; CSV formula prefixes are escaped, personal fields minimized, downloading rechecks permission. No export is enabled merely because a table is visible.

**Accessibility, components and performance:** use the existing button, field, table, dialog, badge, gallery, chart and navigation specifications. Keyboard, focus return, screen-reader errors, 200% text and 400% reflow are mandatory. Motion never gates input or signals acceptance before server commit. Public pages follow SEO canonicals; private pages require authentication plus noindex and exclusion from public caches/sitemaps. Follow NFR-BASELINE, reduced-motion settings and per-component tokens; do not claim measured compliance before a build exists.

**Common acceptance:** for each listed action test authorized success, wrong owner/organization/branch denial, invalid input, empty/loading/error/denied/success states, duplicate, timeout/reconnect and stale version. Check no secret in logs or analytics, durable audit for every consequential command, correct metric denominator and keyboard completion. API bindings are operationIds in the OpenAPI/index; future CMS/campaign integrations explicitly marked below are not falsely presented as implemented endpoints.

## PNL-01 — Public website

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Explain the service and invite an informed next step. Roles: ROLE-001. |
| Application choice | Public frontend; SSR content and progressive enhancement. |
| Route and screens | `/`; SCR-001,002,010,011,012,013,036,037. |
| Navigation hierarchy | Services > Sell / Buy / Value / Branches; Learn > Journal / Help; Company > About / Trust / Contact / Legal. |
| Dashboard hierarchy | Approved service claim, branch coverage and relevant fees; no private figures. |
| Create/edit/detail actions | Start selling; find branch; browse consumer inventory. |
| Fields and validation | Public content, branch hours, market eligibility; no required login to read. |
| Tables/search/bulk/exports | Search published content; filter branch by city/service; no bulk action or private export. |
| Approval and security | Content publisher reviews legal/financial claims; unpublished content cannot render. |
| API operation dependencies | listVehicleTaxonomy,listBranches,listBranchSlots,listConsumerListings. |
| Owned/read entities | CMSArticle,SEOPage,Branch,VehicleListing. |
| Empty state | “No service in this area. View other branches.” |
| Analytics and acceptance | Consented service CTA to qualified lead, grouped by landing page; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-02 — Seller dashboard

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Submit and track a vehicle sale while preserving seller choice. Roles: ROLE-002. |
| Application choice | Customer frontend; narrow-screen stepper, saved server draft. |
| Route and screens | `/account/sales/{id}`; SCR-003,004,005,006,007,008,009. |
| Navigation hierarchy | My sales > Vehicle / Appointment / Inspection / Offer / Contract / Progress; Help; Profile. |
| Dashboard hierarchy | Next required action, appointment local time, report version, conditional offer and separate transaction milestones. |
| Create/edit/detail actions | Submit vehicle; book or reschedule; accept/reject current offer. |
| Fields and validation | Make/model/trim; year 1886 through current year+1; mileage ≥0 with unit; verified contact; separate service acknowledgement and optional marketing choice. |
| Tables/search/bulk/exports | Filter own cases by status/date; no multi-case bid acceptance or bulk legal action. |
| Approval and security | Offer confirmation repeats exact amount/currency, fees, conditions and expiry; explicit decision is version-bound. |
| API operation dependencies | createSellerLead,readSellerLead,createAppointment,transitionAppointment,readResultRecord,recordSellerDecision,readTransaction. |
| Owned/read entities | SellerLead,Vehicle,Appointment,InspectionReport,AuctionResult,SellerDecision,TransactionCase. |
| Empty state | “You have no active sales. Start a vehicle submission.” |
| Analytics and acceptance | Eligible seller cohort conversion and rejection/expiry separately; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-03 — Consumer buyer

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Discover consumer inventory and coordinate an inquiry. Roles: ROLE-003. |
| Application choice | Customer frontend; responsive cards and accessible filter drawer. |
| Route and screens | `/account/requests`; SCR-029,030,031,032. |
| Navigation hierarchy | Browse > Saved vehicles / Searches; Requests > Inquiries / Sourcing; Purchases; Help. |
| Dashboard hierarchy | Availability, reviewed price breakdown, next advisor action; no dealer-only lot. |
| Create/edit/detail actions | Filter; open gallery; inquire; cancel own request. |
| Fields and validation | Listing ID and verified contact; sourcing criteria, budget/currency pair, region and payment preference. |
| Tables/search/bulk/exports | Filters make/model/year/mileage/price/city; favorites only own account; export off. |
| Approval and security | Recheck authoritative availability before request; no unapproved reservation or financing guarantee. |
| API operation dependencies | listConsumerListings,createPurchaseRequest,readPurchaseRequest,transitionPurchaseRequest. |
| Owned/read entities | VehicleListing,PurchaseRequest,ProcurementRequest. |
| Empty state | “No vehicles match. Clear a filter or request sourcing.” |
| Analytics and acceptance | Distinct inquiry conversion, availability losses and advisor response time; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-04 — Dealer portal

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Bid for an approved organization using current inspection evidence. Roles: ROLE-004,ROLE-005. |
| Application choice | Separate dealer frontend; mobile bidding with persistent status and no animated authority. |
| Route and screens | `/dealer/auctions`; SCR-014,015,016,017,018,019. |
| Navigation hierarchy | Application; Auctions > Eligible / Watchlist / Bid history; Purchases > Contracts / Obligations / Delivery; Organization. |
| Dashboard hierarchy | Organization context, eligibility, current price/currency, report revision, server cutoff and next commitment. |
| Create/edit/detail actions | Submit application; place bid; reconcile unknown result; view own purchases. |
| Fields and validation | Organization registration and representative evidence; bid positive exact integer minor units in auction currency; no client timestamp authority. |
| Tables/search/bulk/exports | Filter eligible lots by vehicle/region/end; history scoped to organization; no bulk bids. |
| Approval and security | Explicit review before bid; eligibility checked on each request and feed; display accepted only after durable acknowledgement. |
| API operation dependencies | submitDealerApplication,createDealerVerification,readDealerVerification,listEligibleAuctions,getAuctionSnapshot,submitBid,readBidCommand,readTransaction. |
| Owned/read entities | DealerVerification,OrganizationMember,Auction,Bid,AuctionResult. |
| Empty state | “No eligible auctions currently. Check your filters or account status.” |
| Analytics and acceptance | Qualified participation, accepted bid rate and completed purchases by cohort; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-05 — Auction operations

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Prepare and supervise fair auctions. Roles: ROLE-010. |
| Application choice | Shared operations module; high-density table on desktop, read/critical actions on mobile. |
| Route and screens | `/ops/auctions`; SCR-025. |
| Navigation hierarchy | Queue > Draft / Scheduled / Live / Held / Closed; Results; Incidents; Policies. |
| Dashboard hierarchy | Eligible report, pinned policy, live status, participant count and unresolved integrity alarms. |
| Create/edit/detail actions | Create; schedule; inspect; hold; close or cancel under policy. |
| Fields and validation | Vehicle/report revision, approved policy, UTC start/end, fixed currency and reason for intervention. |
| Tables/search/bulk/exports | Filter status/branch/time; audit export by separate grant; no mass close/cancel. |
| Approval and security | Intervention shows affected bidders and consequence; independent approval where policy requires; no bid edits. |
| API operation dependencies | createAuction,getAuctionSnapshot,listEligibleAuctions,transitionAuction,closeAuction. |
| Owned/read entities | Auction,AuctionParticipant,Bid,AuctionResult,AuctionDispute. |
| Empty state | “No auctions in this queue. Prepare an eligible vehicle.” |
| Analytics and acceptance | Close latency and no-qualifying-result rate; accepted history completeness; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-06 — Inspection management

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Produce attributable versioned vehicle condition evidence. Roles: ROLE-007,ROLE-008. |
| Application choice | Shared operations module optimized for tablet capture; offline write deferred. |
| Route and screens | `/ops/inspections`; SCR-022,023. |
| Navigation hierarchy | Assigned visits; Drafts; Review queue; Published reports; Corrections; Templates. |
| Dashboard hierarchy | Vehicle identity, checklist completion, unknown points, evidence scan state and reviewer. |
| Create/edit/detail actions | Capture findings; submit; return; publish; correct. |
| Fields and validation | Point result pass/defect/unknown/N/A; unknown/N/A require reason; severity on defect; evidence IDs must be clean and case-scoped. |
| Tables/search/bulk/exports | Filter branch/inspector/status; compare revisions side-by-side; no bulk publication. |
| Approval and security | Independent supervisor, mandatory points resolved per template; correction opens new revision and material hold. |
| API operation dependencies | createInspection,readInspection,createInspectionRevision,transitionInspection,publishInspection,createUploadGrant,readFileStatus. |
| Owned/read entities | Inspection,InspectionItem,InspectionFinding,InspectionRevision,VehicleDocument. |
| Empty state | “No assigned inspections. Ask your branch coordinator.” |
| Analytics and acceptance | Completion time, reviewer returns, unknown points and correction rate; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-07 — Branch operations

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Reserve real inspection capacity and handle arrivals. Roles: ROLE-006. |
| Application choice | Shared operations module; desktop calendar plus accessible agenda/mobile list. |
| Route and screens | `/ops/branches/{id}/schedule`; SCR-021. |
| Navigation hierarchy | Calendar; Check-in; Queue; Staff capacity; Holidays; Exceptions. |
| Dashboard hierarchy | Local calendar, booked/available slots, waiting and overdue cases. |
| Create/edit/detail actions | Book; reschedule; check in; mark no-show; reassign qualified staff. |
| Fields and validation | Branch/slot/lead; reason for override; holidays and staffing skills; timezone shown before confirmation. |
| Tables/search/bulk/exports | Date/branch/status/staff filters; CSV only aggregate capacity unless export grant; no silent mass rescheduling. |
| Approval and security | Last-slot conflict is recoverable; no-show requires open branch and elapsed grace; override cannot exceed safety capacity. |
| API operation dependencies | listBranchSlots,createAppointment,readAppointment,transitionAppointment. |
| Owned/read entities | Branch,BranchSchedule,AppointmentSlot,Appointment,BranchEmployee. |
| Empty state | “No appointments for this date. Select another day.” |
| Analytics and acceptance | Utilization, attendance, wait percentile and capacity conflicts; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-08 — CRM and call center

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Maintain accountable contact and follow-up without changing legal facts. Roles: ROLE-011. |
| Application choice | Shared operations module with accessible keyboard work queue. |
| Route and screens | `/ops/leads`; SCR-020. |
| Navigation hierarchy | Assigned leads; Follow-ups; Customer timeline; Duplicate review; Communications. |
| Dashboard hierarchy | Next task, due time, verified channel, service consent and current case status. |
| Create/edit/detail actions | Qualify; request evidence; assign; log contact; resolve potential duplicate. |
| Fields and validation | Disposition and next follow-up; no government ID in free-text notes; merge requires verified identity. |
| Tables/search/bulk/exports | Filter owner/stage/branch/overdue; bulk assignment only per-record scoped and audited; no unrestricted exports. |
| Approval and security | Consent checked at send time; approximate identity match never auto-merges. |
| API operation dependencies | listSellerLead,readSellerLead,transitionSellerLead,readSupportTicket. |
| Owned/read entities | SellerLead,UserProfile,SupportTicket,Notification. |
| Empty state | “Your assigned queue is empty. Review upcoming follow-ups.” |
| Analytics and acceptance | First-contact time, qualified rate and mature-cohort bookings; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-09 — Inventory management

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Maintain authoritative vehicle identity and controlled publication. Roles: ROLE-021. |
| Application choice | Shared operations module; public preview isolated from staff evidence. |
| Route and screens | `/ops/inventory`; SCR-041. |
| Navigation hierarchy | Vehicles; Publication queue; Consumer listings; Channel conflicts; Media. |
| Dashboard hierarchy | Vehicle/report revision, ownership verification, channel availability and media rights. |
| Create/edit/detail actions | Create draft listing; review; publish; suspend; withdraw; mark sold. |
| Fields and validation | Taxonomy and condition fields; exact price/currency; approved media rights; publication-specific redaction. |
| Tables/search/bulk/exports | Branch/make/status/channel filters; bulk unpublish with per-item reason/authorization only. |
| Approval and security | No live consumer sale and dealer auction collision; sold status needs verified disposition. |
| API operation dependencies | createVehicleListing,readVehicleListing,transitionVehicleListing. |
| Owned/read entities | Vehicle,VehicleListing,VehicleMedia,VehicleOwnership. |
| Empty state | “No vehicles awaiting publication. Review drafts.” |
| Analytics and acceptance | Freshness, publication errors and conflicting inventory rate; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-10 — Pricing and valuation

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Produce explainable price ranges or abstain. Roles: ROLE-009. |
| Application choice | Shared operations module with paired table/chart and text alternatives. |
| Route and screens | `/ops/valuations`; SCR-024. |
| Navigation hierarchy | Requests; Comparable review; Overrides; Accuracy; Source quality. |
| Dashboard hierarchy | Comparable coverage/freshness, condition adjustments, confidence and prior overrides. |
| Create/edit/detail actions | Request estimate; approve; reject/abstain; revise with reason. |
| Fields and validation | Comparable source rights, region/time, currency; low <= high; override reason and reviewer distinct from preparer. |
| Tables/search/bulk/exports | Filter vehicle class/region/confidence; restricted comparable export by grant. |
| Approval and security | No range when evidence insufficient; new valuation does not rewrite active auction reserve. |
| API operation dependencies | createValuation,readValuation,transitionValuation. |
| Owned/read entities | Valuation,ValuationAdjustment,MarketPriceRecord. |
| Empty state | “Not enough comparable data. Send for manual review.” |
| Analytics and acceptance | Coverage, absolute percentage error on eligible completed sales, calibration and override frequency; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-11 — Contracts and legal

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Coordinate exact contracts and independent ownership evidence. Roles: ROLE-012. |
| Application choice | Restricted shared module; document comparison desktop and readable mobile status. |
| Route and screens | `/ops/legal`; SCR-026,042. |
| Navigation hierarchy | Matter queue; Templates; Contracts; Signatures; Title transfer; Legal holds. |
| Dashboard hierarchy | Party authority, document version/hash, required signatures and title milestone. |
| Create/edit/detail actions | Review; issue; record verified signature; amend; verify transfer. |
| Fields and validation | Jurisdiction/template, party IDs, signers; exact document hash; external authority reference. |
| Tables/search/bulk/exports | Filter matter/status/expiry; restricted export; no bulk signatures/title approval. |
| Approval and security | Amendment never overwrites signed version; title not inferred from payment or custody. |
| API operation dependencies | createContract,readContract,transitionContract,recordSignatureEvidence,readOwnershipTransfer,verifyOwnershipTransfer. |
| Owned/read entities | Contract,ContractDocument,ContractSignature,OwnershipTransfer. |
| Empty state | “No matters assigned. Select a permitted queue.” |
| Analytics and acceptance | Contract cycle time and transfer delay by jurisdiction; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-12 — Finance operations

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Represent and verify obligations without inventing money movement. Roles: ROLE-013,ROLE-014. |
| Application choice | Restricted shared module; explicit totals and safe print/export. |
| Route and screens | `/ops/finance`; SCR-026,043. |
| Navigation hierarchy | Obligations; Evidence; Reconciliation; Discrepancies; Adjustments; Statements. |
| Dashboard hierarchy | Expected/matched/remaining amount and currency, independent review and discrepancies. |
| Create/edit/detail actions | Create obligation; attach evidence; prepare match; independently reconcile. |
| Fields and validation | Payer/payee, contract basis, exact amount, currency, external source/reference; zero automatic tolerance. |
| Tables/search/bulk/exports | Filter due/status/currency; CSV only scoped and audited; no bulk financial approval. |
| Approval and security | Step-up and maker/checker; duplicate source allocation, partial payment and reversal block close. |
| API operation dependencies | createPaymentObligation,readPaymentObligation,submitPaymentEvidence,prepareReconciliation,readReconciliationRecord,approveReconciliation. |
| Owned/read entities | PaymentObligation,PaymentTransaction,ReconciliationRecord,LedgerEntry. |
| Empty state | “No reconciliation items. Review outstanding obligations.” |
| Analytics and acceptance | Reconciliation delay, unresolved discrepancies and contribution under approved accounting; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-13 — Credit operations

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Coordinate approved third-party financing. Roles: ROLE-024. |
| Application choice | Restricted shared module; phase 3 disabled until provider/legal activation. |
| Route and screens | `/ops/financing`; SCR-033,044. |
| Navigation hierarchy | Applications; Awaiting provider; Offers; Expiry; Disbursement; Exceptions. |
| Dashboard hierarchy | Consent, provider status, terms/expiry and funding evidence. |
| Create/edit/detail actions | Assist application; request missing evidence; record provider result; route outage. |
| Fields and validation | Provider/application IDs, purpose-specific consent, disclosed terms and evidence; no raw credit data in analytics. |
| Tables/search/bulk/exports | Filter provider/status/expiry; restricted exports only to designated reviewer. |
| Approval and security | Lender approval cannot be overridden; no platform lending or guaranteed acceptance. |
| API operation dependencies | createFinancingApplication,readFinancingApplication,transitionFinancingApplication,ingestProviderEvent. |
| Owned/read entities | FinancingApplication,FinancingOffer. |
| Empty state | “No active applications. Financing may be unavailable in this market.” |
| Analytics and acceptance | Approval/rejection/expiry by cohort and funded status separately; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-14 — Logistics management

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Track physical custody and condition at each attempt. Roles: ROLE-020,ROLE-018. |
| Application choice | Shared module plus restricted responsive driver surface; native deferred. |
| Route and screens | `/ops/logistics`; SCR-034. |
| Navigation hierarchy | Dispatch queue; Carrier assignments; Pickup; In transit; Delivery; Damage. |
| Dashboard hierarchy | Current custodian, agreed window, carrier and unresolved exceptions. |
| Create/edit/detail actions | Assign; collect; dispatch; deliver; report damage; reschedule. |
| Fields and validation | Condition, proof IDs, authorized recipient, occurred_at; carrier qualification checked. |
| Tables/search/bulk/exports | Filter date/carrier/status/region; driver sees assigned job only; no wide location exports. |
| Approval and security | Delivery needs proof; title separate; reschedule after collection must preserve actual custodian. |
| API operation dependencies | createDelivery,readDelivery,transitionDelivery,recordDeliveryHandover. |
| Owned/read entities | Delivery,LogisticsOrder,VehicleHandover. |
| Empty state | “No assigned deliveries. Contact dispatch for changes.” |
| Analytics and acceptance | On-time delivery, failure attempts, damage claims and custody gaps; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-15 — Customer support

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Resolve complaints with minimum necessary disclosure. Roles: ROLE-011. |
| Application choice | Shared operations module with keyboard triage and restrained notification behavior. |
| Route and screens | `/ops/support`; SCR-027. |
| Navigation hierarchy | Inbox; Assigned; Waiting; Escalated; Resolved; Knowledge. |
| Dashboard hierarchy | Priority, customer-safe case summary, response due and action owner. |
| Create/edit/detail actions | Acknowledge; investigate; request evidence; escalate; resolve; reopen. |
| Fields and validation | Verified requester, case reference, safe subject/comment; public/internal note explicitly selected. |
| Tables/search/bulk/exports | Filter assignee/priority/age; bulk assignment allowed with per-record authorization; no bulk resolution. |
| Approval and security | Agent cannot settle money or alter bids; private documents need additional grants. |
| API operation dependencies | createSupportTicket,readSupportTicket,transitionSupportTicket. |
| Owned/read entities | SupportTicket,Notification,TransactionCase. |
| Empty state | “No cases in this view. Clear filters.” |
| Analytics and acceptance | Response/resolution percentiles, backlog age, reopens and satisfaction; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-16 — Warranty and disputes

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Apply an actual approved policy and retain appeal history. Roles: ROLE-022. |
| Application choice | Restricted shared module; review evidence with controlled media access. |
| Route and screens | `/ops/claims`; SCR-035. |
| Navigation hierarchy | Received; Evidence; Review; Decisions; Appeals; Remedies. |
| Dashboard hierarchy | Claim date, applicable policy/report versions, evidence and decision owner. |
| Create/edit/detail actions | Request evidence; approve/deny; appeal; track authorized remedy. |
| Fields and validation | Policy version, claimant, transaction and evidence; independent appeal reviewer. |
| Tables/search/bulk/exports | Filter policy/status/age; privileged legal export only; no bulk denials. |
| Approval and security | No warranty inferred from marketing; claim approval cannot execute financial payment. |
| API operation dependencies | createWarrantyClaim,readWarrantyClaim,transitionWarrantyClaim. |
| Owned/read entities | WarrantyClaim,WarrantyPolicy,InspectionRevision. |
| Empty state | “No claims assigned. Review upcoming evidence deadlines.” |
| Analytics and acceptance | Claims per eligible transaction, resolution and appeal outcomes; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-17 — Content and SEO

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Publish accurate useful pages with controlled indexation. Roles: ROLE-015. |
| Application choice | Headless CMS interface; phase 2; CMS selection is explicit dependency. |
| Route and screens | `/ops/content`; SCR-039. |
| Navigation hierarchy | Drafts; Review; Scheduled; Published; Redirects; Taxonomy. |
| Dashboard hierarchy | Editorial state, preview, source dates, canonical/robots and claim approval. |
| Create/edit/detail actions | Draft; submit review; schedule; publish; retire; manage redirects. |
| Fields and validation | Title, slug, body, author, sources, review date, canonical/index policy, rights-cleared media. |
| Tables/search/bulk/exports | Filter author/status/topic/staleness; preview requires token; export content only. |
| Approval and security | Content commands use createContent/readContent/reviseContent/actOnContent; selected CMS adapter must preserve exact revision, approval and publication semantics. |
| API operation dependencies | getMetrics. |
| Owned/read entities | CMSArticle,SEOPage,VehicleMedia. |
| Empty state | “No drafts. Create a researched article in the selected CMS.” |
| Analytics and acceptance | Index eligibility, qualified organic leads and stale content; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-18 — Marketing and growth

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Run approved acquisition campaigns without bypassing preferences. Roles: ROLE-025. |
| Application choice | Shared restricted module; campaign provider adapter required before activation. |
| Route and screens | `/ops/growth`; SCR-045. |
| Navigation hierarchy | Campaigns; Consent-safe audiences; Experiments; Attribution; Suppression. |
| Dashboard hierarchy | Audience eligibility, experiment status, spend source and aggregate conversion. |
| Create/edit/detail actions | Propose experiment; review audience; schedule approved campaign; stop. |
| Fields and validation | Purpose, channel, approved template, audience rule/version and start/end; exclude sensitive traits. |
| Tables/search/bulk/exports | Aggregate filters only; audience export disabled by default. |
| Approval and security | Campaign commands use createCampaign/readCampaign/actOnCampaign; sending adapter must enforce latest suppression at dispatch; experiments cannot change legal/auction terms per user. |
| API operation dependencies | getMetrics. |
| Owned/read entities | NotificationTemplate,AnalyticsEvent,ConsentRecord. |
| Empty state | “No approved campaigns. Prepare an audience and consent review.” |
| Analytics and acceptance | Incremental qualified conversion with guardrails, not clicks alone; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-19 — Analytics and BI

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Provide governed denominators and visible data freshness. Roles: ROLE-017. |
| Application choice | BI surface with row-level security; accessible data table for every chart. |
| Route and screens | `/ops/reports`; SCR-040. |
| Navigation hierarchy | Executive; Acquisition; Branch; Auction; Transactions; Finance; Data quality. |
| Dashboard hierarchy | Period/cohort, definition version, sample size, excluded records and freshness. |
| Create/edit/detail actions | Choose metric/date/scope; compare cohorts; authorized export. |
| Fields and validation | Metric allowlist, bounded UTC period, branch/organization scope; null for undefined denominator. |
| Tables/search/bulk/exports | Filter permitted dimensions; no unbounded raw personal query; audited exports. |
| Approval and security | No stale/missing data displayed as zero; privacy thresholds and finance definitions enforced. |
| API operation dependencies | getMetrics. |
| Owned/read entities | AnalyticsEvent,ReconciliationRecord,AggregateMetric. |
| Empty state | “No data for this cohort yet. Change period or inspect freshness.” |
| Analytics and acceptance | Metric coverage, reconciliation difference and freshness SLA; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## PNL-20 — Super administration

| Dimension | Specific specification |
|---|---|
| Purpose / actors | Control privileged configuration without domain bypass. Roles: ROLE-016,ROLE-026. |
| Application choice | Restricted shared module; dedicated elevated session, no public caching. |
| Route and screens | `/ops/admin/access`; SCR-028,046. |
| Navigation hierarchy | Access; Organizations; Policies; Feature flags; Audit; Alerts; Exports. |
| Dashboard hierarchy | Pending requests, expiring grants, policy diffs and audit health. |
| Create/edit/detail actions | Request grant/change; review independently; schedule activation; revoke. |
| Fields and validation | Exact subject/scope/action/effective interval, reason and policy version; required step-up. |
| Tables/search/bulk/exports | Filter requester/scope/status; bulk revocation only reviewed and item-audited; no mass privilege grants. |
| Approval and security | Separate requester/approver; no super-admin right to edit bid ledger or approve own financial adjustment. |
| API operation dependencies | readPolicyRecord,createPolicyVersion. |
| Owned/read entities | Role,Permission,OrganizationMember,FeatureFlag,AuditLog. |
| Empty state | “No pending access requests. Review expiring grants.” |
| Analytics and acceptance | Privilege review completion, expired grants and audit delivery health; common acceptance cases above apply to each action. |

**Notifications and recovery:** notify only affected authorized participants after committed state; failed delivery remains a separate queue. Unresolved cases retain owner, reason and next action. This panel cannot bypass another domain's authority. Sensitive reads, exports and mutations retain audit actor, purpose, record, scope, time, policy and result. Review with the responsible domain owner before live activation.

## Optional surfaces

Partner/carrier access uses PNL-14 scoped assignments; a standalone partner portal is justified only by contracted independent workflow. Affiliate functionality is phase 4 and requires attribution fraud, payout and disclosure rules before activation. Franchise access requires branch tenancy, contracting authority and financial isolation review. Fraud monitoring starts as restricted investigation cases under ROLE-019 and security; automated adverse decisions are disabled. Quality control starts with PNL-06 sampling and revision review. None inherits super-administrator access or introduces an unapproved financial promise.

## Intake and consumer purchase completion

PNL-02 claims an anonymous seller draft using `requestIntakeClaim` and `claimIntake`, then explicitly submits; a UUID or email match never proves ownership. PNL-03 uses `readConsumerOffer` and `acceptConsumerOffer` for seller-authorized terms, displays expiry and the exact total/currency, and requires fresh confirmation. A stale or unavailable listing returns a reviewable conflict; acceptance displays the returned transaction ID and the next legal step. PNL-04 starts a new organization using `submitDealerApplication`; the verification review endpoint is not a way for an applicant to grant membership in an existing organization. Content panel PNL-17 uses typed `createContent`, `readContent`, `reviseContent`, `actOnContent`; growth PNL-18 uses `createCampaign`, `readCampaign`, `actOnCampaign`; administration PNL-20 separates `createPolicyVersion` from independent `approvePolicy`.
