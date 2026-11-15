# Screen inventory

**ID:** 05/04_SCREEN_INVENTORY · **Version:** 0.1 · **Status:** PROPOSED, subject to research and stakeholder review · **Owner:** UX lead · **Reviewers:** Product, accessibility, operations, engineering, legal · **Updated:** 2026-11-15

## Contract and conventions
Screen IDs below are stable within this document; routes are proposed and refer to screens, not backend authorization. Layouts, common state behavior, validation and acceptance are defined in [wireframe specifications](05_WIREFRAME_SPECIFICATIONS.md) and [form UX](06_FORM_UX.md). Public screens need canonical/index policy; account and staff screens are private and noindex. A screen loads authorized data only; unknown resources and denied access return safe generic copy. No seller or dealer screen exposes another party's private records.

| ID | Route / surface | Purpose; primary action; key dependency | Access / phase |
|---|---|---|---|
| SCR-001 | `/` public | Explain service; Start selling; approved content and branch coverage. | Public / 1 |
| SCR-002 | `/sell` public | Explain sale and inspection; Start selling; approved claims. | Public / 1 |
| SCR-003 | `/sell/start` seller | Vehicle details and condition; Continue; taxonomy. | Public or verified draft / 1 |
| SCR-004 | `/sell/contact` seller | Contact and consent; Continue; policy text. | Lead owner / 1 |
| SCR-005 | `/sell/appointment` seller | Branch and available slot; Book; live capacity. | Lead owner / 1 |
| SCR-006 | `/sell/confirmation` seller | Confirm appointment; View case; persisted booking. | Lead owner / 1 |
| SCR-007 | `/account/sales/{id}` seller | Status, tasks and support; view current offer; case projection. | Owner / 1 |
| SCR-008 | `/account/sales/{id}/offer` seller | Explain conditional offer; accept or reject; authorized current offer and expiry. | Owner / 1 |
| SCR-009 | `/account/appointments/{id}` seller | View and change booking; reschedule/cancel; availability. | Owner / 1 |
| SCR-010 | `/value` public | Enter attributes; estimate range; approved valuation policy. | Public / 1 |
| SCR-011 | `/branches` public | Find location; select branch; published branch details. | Public / 1 |
| SCR-012 | `/branches/{slug}` public | Hours, services and accessibility; book branch; branch status. | Public / 1 |
| SCR-013 | `/dealers` public | Explain participation; Apply; approved eligibility copy. | Public / 1 |
| SCR-014 | `/dealer/apply` dealer | Capture organization/representative; Submit; policy and verification process. | Applicant / 1 |
| SCR-015 | `/dealer/application` dealer | Display pending, approved, rejected/review and appeal contact; status. | Applicant / 1 |
| SCR-016 | `/dealer/auctions` dealer | List eligible active lots; open lot; authorized auction feed. | Approved dealer / 1 |
| SCR-017 | `/dealer/auctions/{id}` dealer | Inspection, current amount, deadline and bid control; place bid; authoritative state. | Approved authorized bidder / 1 |
| SCR-018 | `/dealer/bids` dealer | Show own bid decisions and outcomes; open auction; bid history. | Organization scoped / 1 |
| SCR-019 | `/dealer/purchases/{id}` dealer | Transaction next steps; view documents; transaction status. | Organization scoped / 1 |
| SCR-020 | `/ops/queue` staff | Assigned work and overdue exceptions; open case; role/branch scope. | Staff / 1 |
| SCR-021 | `/ops/branches/{id}/schedule` staff | Capacity, check-in and reschedule; select booking; branch calendar. | Branch scoped / 1 |
| SCR-022 | `/ops/inspections/{id}` staff | Record checklist, photos and exceptions; submit for review; template revision. | Assigned inspector / 1 |
| SCR-023 | `/ops/inspections/{id}/review` staff | Compare evidence and submit decision; publish/return; review permissions. | Supervisor / 1 |
| SCR-024 | `/ops/valuations/{id}` staff | Review comparables and range; approve/override with reason; inspection version. | Analyst/approver / 1 |
| SCR-025 | `/ops/auctions/{id}` staff | Prepare, monitor and investigate auction; authorize permitted action; lot and policy. | Auction staff / 1 |
| SCR-026 | `/ops/transactions/{id}` staff | Track contract, payment, ownership and handover separately; record evidence; transaction. | Assigned staff, finance/legal scope / 1 |
| SCR-027 | `/ops/support/{id}` staff | Classify issue, assign and respond; escalate; ticket and consent. | Support / 1 |
| SCR-028 | `/ops/admin/access` staff | Review grants and scope; request/approve change; identity/audit. | Security admin / 1 |
| SCR-029 | `/buy` consumer | Filter and browse consumer inventory; open listing; public listing index. | Public / 2 |
| SCR-030 | `/cars/{slug}` consumer | Gallery, specs, inspection summary and availability; enquire; published listing. | Public / 2 |
| SCR-031 | `/account/requests/new` consumer | Describe sourcing needs; Submit; taxonomy, consent. | Buyer / 2 |
| SCR-032 | `/account/saved` consumer | Recover favorites and saved searches; view listing; scoped account. | Buyer / 2 |
| SCR-033 | `/account/finance/{id}` buyer | Review lender terms and application status; continue with provider; explicit consent. | Applicant / 3 |
| SCR-034 | `/ops/logistics/{id}` staff | Track custody and delivery; record evidence; assigned transport. | Logistics / 3 |
| SCR-035 | `/ops/claims/{id}` staff | Review dispute evidence and policy; record decision; claims scope. | Claims / 3 |
| SCR-036 | `/journal/{slug}` public | Educational content and related journeys; read or start relevant task; published CMS. | Public / 2 |
| SCR-037 | `/help` public | Search support and contact options; choose help article; approved content. | Public / 1 |
| SCR-038 | `/sign-in` shared | Verify identity; continue securely; identity provider. | Public / 1 |
| SCR-039 | `/ops/content/{id}` editor | Draft and review publication; submit for approval; CMS state. | Editor / 2 |
| SCR-040 | `/ops/reports` analyst | Review approved aggregate metrics; select filters; governed data. | Analytics scope / 1–3 |

## Coverage and limits
Each screen uses the common states and responsive rules in the referenced documents. Composite operations screens contain multiple task-specific panels; detailed fields and final endpoints depend on policy and backend specifications. Screen list is a proposed baseline, not evidence of final design assets or user validation. Acceptance: every new route maps to one screen, an access rule, primary task and test; private routes reject unauthorized requests and are excluded from public search.

## Additional operational screens

The [panel contracts](../04_ROLES_AND_PANELS/12_PANEL_CONTRACTS.md) define full common layout, responsive behavior, components, empty/loading/error/denied/success states, validation, confirmations, audit and acceptance. The following screens inherit those explicit rules and supply domain-specific data/action bindings. These are specifications, not rendered assets.

| Screen | Route / panel | Hierarchy and primary action | Read / command / validation | Access and expected result |
|---|---|---|---|---|
| SCR-041 | `/ops/inventory` / PNL-09 | Vehicle queue → channel/availability → public preview → publish or suspend. | readInventoryListing / transitionVehicleListing; reviewed rights, price and exclusive active sale channel. | ROLE-021 branch scope; denied transitions retain prior public version and safe error. |
| SCR-042 | `/ops/legal/transfers/{id}` / PNL-11 | Case → external authority evidence → independent verification → next action. | readOwnershipTransfer / verifyOwnershipTransfer; evidence must match parties, vehicle and jurisdiction. | ROLE-012 assigned matter; title pending until verified; no inference from handover. |
| SCR-043 | `/ops/finance/reconciliations/{id}` / PNL-12 | Obligation → authoritative evidence → match/difference → approve. | readReconciliationRecord / approveReconciliation; current ETag, exact currency/parties, maker/checker, recent step-up. | ROLE-014 independent approver; mismatch holds and assigns owner; empty means no evidence, never zero balance. |
| SCR-044 | `/ops/financing/{id}` / PNL-13 | Applicant consent → lender request/decision → terms/expiry → funding. | readFinancingApplication / transitionFinancingApplication; authenticated provider decision via internal adapter only. | ROLE-024 case scope; no promise of credit; expired offer cannot be accepted. |
| SCR-045 | `/ops/growth` / PNL-18 | Approved audience → purpose/channel → campaign review → aggregate results. | createCampaign / readCampaign / actOnCampaign / getMetrics with selected provider adapter; current suppression and reviewed template required. | ROLE-025; activation blocked until provider contract exists; no sensitive audience export. |
| SCR-046 | `/ops/admin/policies/{id}` / PNL-20 | Version diff → affected flows → review evidence → approval request. | readPolicyRecord / createPolicyVersion / approvePolicy; reason, schema validation and current ETag. | ROLE-016 proposes, ROLE-026 independently approves via reviewed governance workflow; no self-activation. |

Each success test verifies the primary command, permitted field projection and accessible feedback; failure tests include scope denial, invalid data, stale ETag, retries and no duplicated effects. Private routes are authenticated, noindex, excluded from sitemap and never CDN-shared. Operations metrics use approved purpose and no raw identity data.

## Account completion screens

| ID | Route / surface | Purpose; primary action; key dependency | Access / phase |
|---|---|---|---|
| SCR-047 | `/account/requests/{id}` consumer | Current inquiry and seller-authorized offer, exact terms and expiry; accept offer and follow transaction; authoritative listing reservation. | Own buyer request / 2 |
| SCR-048 | `/account/privacy/{id}` customer | Rights request status, verification and explanation; supply required proof or read outcome; privacy workflow and legal holds. | Verified requester / 1 |

The [screen/API binding matrix](10_SCREEN_CONTRACT_BINDINGS.md) resolves every screen to fields, actions and contract endpoints or an explicit governed manual boundary. Final rendered assets and actual participant validation remain later design-delivery evidence.
