# Screen fields, actions and contract bindings

**ID:** SCREEN-BINDINGS · **Version:** 0.3 · **Status:** proposed implementation specification · **Owner:** UX/API leads · **Updated:** 2026-11-15

Read with the screen inventory, wireframe specifications and panel contracts: those define hierarchy, responsive layout, loading/empty/error/denied/success states, confirmation, copy and accessibility. The schema field reference defines exact types, required fields and bounds. Every screen below is covered by those shared rules; its data/action specifics are explicit here. This is not a claim of rendered mockups or user testing.

| Screen / route | Fields, purpose and important behavior | Supporting operation IDs / controlled procedure |
|---|---|---|
| SCR-001 `/` | Approved value proposition, coverage and trust claims | readPublishedContent, listBranches |
| SCR-002 `/sell` | Three sale steps, conditions, inspection scope and fees disclosure | readPublishedContent |
| SCR-003 `/sell/start` | Make/model/year, mileage/unit and condition | listVehicleTaxonomy, createSellerLead |
| SCR-004 `/sell/contact` | Contact, service notice, separate marketing choice and ownership proof | requestIntakeClaim, claimIntake, transitionSellerLead |
| SCR-005 `/sell/appointment` | Branch, server slot, local date/time, offset and cancellation notice | listBranches, listBranchSlots, createAppointment |
| SCR-006 `/sell/confirmation` | Persisted reference, branch, time, status and next step | readAppointment |
| SCR-007 `/account/sales/{id}` | Lead status, appointment, inspection and current offer | readSellerLead, readAppointment, readInspection, readResultRecord |
| SCR-008 `/account/sales/{id}/offer` | Amount/currency, terms version, expiry, decision and receipt | readResultRecord, recordSellerDecision |
| SCR-009 `/account/appointments/{id}` | Current slot/version, new slot and reason | readAppointment, listBranchSlots, transitionAppointment |
| SCR-010 `/value` | Public vehicle attributes, market, currency, dated range or abstention | listVehicleTaxonomy, estimatePublicVehicle |
| SCR-011 `/branches` | Region, accessible branch list and map equivalent | listBranches |
| SCR-012 `/branches/{slug}` | Approved address, timezone, accessibility and service status | listBranches, listBranchSlots |
| SCR-013 `/dealers` | Dealer eligibility, verification expectations and application CTA | readPublishedContent |
| SCR-014 `/dealer/apply` | Legal name, jurisdiction, registration, representative proof and notice | createUploadGrant, submitDealerApplication |
| SCR-015 `/dealer/application` | Verification state, requested evidence and appeal/contact route | readDealerVerification, transitionDealerVerification |
| SCR-016 `/dealer/auctions` | Eligible lot, vehicle facts, price, deadline and report version | listEligibleAuctions |
| SCR-017 `/dealer/auctions/{id}` | Vehicle/gallery, pinned report, current/minimum amount, sequence and server time | getAuctionSnapshot, readInspectionRevision, submitBid, readBidCommand |
| SCR-018 `/dealer/bids` | Own command receipt, accepted/rejected status, amount and sequence | listBidCommand, readBidCommand |
| SCR-019 `/dealer/purchases/{id}` | Transaction milestones, own documents and current obligations | readTransaction, readContract, readPaymentObligation |
| SCR-020 `/ops/queue` | Assigned queue, branch, due time, state and owner | listSellerLead, listAppointment, listInspection, listSupportTicket |
| SCR-021 `/ops/branches/{id}/schedule` | Branch calendar, capacity, booking and check-in; calendar editing is governed branch administration until dedicated adapter is approved | listBranchSlots, listAppointment, transitionAppointment |
| SCR-022 `/ops/inspections/{id}` | Pinned template/points, findings, severity, reason and evidence | readInspectionTemplate, readInspection, readInspectionRevision, createUploadGrant, createInspectionRevision, transitionInspection |
| SCR-023 `/ops/inspections/{id}/review` | Exact revision, completeness, author/reviewer, differences and decision | readInspectionRevision, publishInspection, transitionInspection |
| SCR-024 `/ops/valuations/{id}` | Inspection input, licensed comparables, range/currency, confidence and rationale | readValuation, createValuation, transitionValuation |
| SCR-025 `/ops/auctions/{id}` | Lot policy/report/time, live state, commands and exception history | getAuctionSnapshot, createAuction, transitionAuction, closeAuction |
| SCR-026 `/ops/transactions/{id}` | Separate origin, contract, obligations, title and custody milestone cards | readTransaction, readContract, readPaymentObligation, readOwnershipTransfer, readDelivery, closeTransaction |
| SCR-027 `/ops/support/{id}` | Category, assigned case, response due, evidence and resolution | readSupportTicket, transitionSupportTicket |
| SCR-028 `/ops/admin/access` | Actor, proposed role/scope/expiry, independent approver and audit; governed IAM console procedure | IAM joiner/mover/leaver procedure in identity/access; no arbitrary native grant endpoint |
| SCR-029 `/buy` | Taxonomy/price/year/mileage/region filters, result count and availability | listConsumerListings, listVehicleTaxonomy |
| SCR-030 `/cars/{slug}` | Approved gallery, vehicle specification, condition, price and availability | readListingBySlug, createPurchaseRequest, setSavedVehicle |
| SCR-031 `/account/requests/new` | Sourcing criteria, budget/currency, contact choice and consent | createProcurement, readProcurement, actOnProcurement |
| SCR-032 `/account/saved` | Saved vehicles/search filters, frequency and suppression state | listSavedVehicles, setSavedVehicle, createSavedSearch, listSavedSearches, deleteSavedSearch |
| SCR-033 `/account/finance/{id}` | Consent, lender/terms, status, expiry and external next action | readFinancingApplication, transitionFinancingApplication |
| SCR-034 `/ops/logistics/{id}` | Assigned carrier, pickup/delivery window, custody and signed proof | readDelivery, transitionDelivery, recordDeliveryHandover |
| SCR-035 `/ops/claims/{id}` | Policy, evidence, coverage decision, appeal and separate remedy approval | readWarrantyClaim, transitionWarrantyClaim |
| SCR-036 `/journal/{slug}` | Approved title, author, reviewed date, article blocks and relevant next task | readPublishedContent |
| SCR-037 `/help` | Approved help content, accessible contact and support request | readPublishedContent, createSupportTicket |
| SCR-038 `/sign-in` | Identifier/password, non-authorized MFA challenge, recovery and step-up when requested | createSession, completeAuthChallenge, readCurrentSession, revokeCurrentSession, requestAccountRecovery, completeRecovery |
| SCR-039 `/ops/content/{id}` | Typed content blocks, sources, claim review, exact revision and publish time | createContent, readContent, reviseContent, actOnContent |
| SCR-040 `/ops/reports` | Metric definition/version, cohort, period, freshness, purpose and export status | getMetrics, requestExport, readExportJob, downloadExport |
| SCR-041 `/ops/inventory` | Channel, price/currency, approved media and public projection preview | readInventoryListing, createVehicleListing, transitionVehicleListing, createConsumerOffer |
| SCR-042 `/ops/legal/transfers/{id}` | Exact parties/vehicle, jurisdiction, external transfer proof and independent verification | readOwnershipTransfer, verifyOwnershipTransfer |
| SCR-043 `/ops/finance/reconciliations/{id}` | Obligation, source allocation, residual difference, preparer and approver | readPaymentObligation, readReconciliationRecord, prepareReconciliation, approveReconciliation |
| SCR-044 `/ops/financing/{id}` | Applicant sharing basis, provider correlation, exact offer/expiry and funding evidence | readFinancingApplication, transitionFinancingApplication |
| SCR-045 `/ops/growth` | Purpose, audience, template, suppression, schedule and aggregate result | createCampaign, readCampaign, actOnCampaign, getMetrics |
| SCR-046 `/ops/admin/policies/{id}` | Typed policy diff, business impact, independent review and effective time | readPolicyRecord, createPolicyVersion, approvePolicy |
| SCR-047 `/account/requests/{id}` | Own request, current authorized offer, expiry, consent and transaction receipt | readPurchaseRequest, readConsumerOffer, acceptConsumerOffer, readTransaction |
| SCR-048 `/account/privacy/{id}` | Verified rights request, identity state, due date, hold explanation and result | createPrivacyRequest, readPrivacyRequest |

A screen test prepares a permitted record and checks content order, primary action, exact outcome, stale/unauthorized/empty variants, keyboard/focus,320px reflow and reduced motion. Shared components carry isolated fixtures; screen-specific integration tests verify correct field projection and action scope. API aliases cannot bypass the state-machine guard.
