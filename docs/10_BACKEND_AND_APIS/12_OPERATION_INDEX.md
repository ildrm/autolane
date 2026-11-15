# Current API operation index

**ID:** API-INDEX · **Version:** 0.3 · **Status:** proposed contract · **Owner:** API architect · **Updated:** 2026-11-15

Generated from [OpenAPI](11_OPENAPI_SPECIFICATION.yaml). All129 operations use stable `API-X-{operationId}` IDs; original API-01–22 remain historical aliases. Provider ingestion is an authenticated internal normalized boundary. Manual operational procedures are explicitly scoped in scenario traceability.

| ID | Method / path | Contract summary |
|---|---|---|
| API-X-getAuctionSnapshot | GET `/auctions/{auctionId}` | Get an authorized authoritative auction snapshot |
| API-X-submitBid | POST `/auctions/{auctionId}/bids` | Atomically submit an idempotent dealer bid |
| API-X-createSession | POST `/auth/sessions` | Authenticate with an approved identity provider |
| API-X-createSellerLead | POST `/seller-leads` | Create a seller lead |
| API-X-listSellerLead | GET `/seller-leads` | List permitted SellerLead |
| API-X-listBranches | GET `/branches` | List public branches |
| API-X-createAppointment | POST `/appointments` | Reserve a branch slot |
| API-X-listAppointment | GET `/appointments` | List permitted Appointment |
| API-X-createInspectionRevision | POST `/inspections/{id}/revisions` | Create inspection revision |
| API-X-publishInspection | POST `/inspections/{id}/publish` | Publish reviewed report |
| API-X-createValuation | POST `/valuations` | Create valuation for review |
| API-X-listValuation | GET `/valuations` | List permitted Valuation |
| API-X-createAuction | POST `/auctions` | Create draft auction |
| API-X-listEligibleAuctions | GET `/auctions` | listEligibleAuctions |
| API-X-closeAuction | POST `/auctions/{id}/close` | Finalize auction |
| API-X-recordSellerDecision | POST `/auction-results/{id}/seller-decision` | Record seller offer decision |
| API-X-decideDealerVerification | POST `/dealer-verifications/{id}/decision` | Approve or reject dealer verification |
| API-X-listConsumerListings | GET `/listings` | Search consumer-published listings |
| API-X-createVehicleListing | POST `/listings` | Create VehicleListing |
| API-X-createPurchaseRequest | POST `/purchase-requests` | Submit a buyer inquiry |
| API-X-listPurchaseRequest | GET `/purchase-requests` | List permitted PurchaseRequest |
| API-X-recordSignatureEvidence | POST `/contracts/{id}/signatures` | Record signature evidence |
| API-X-submitPaymentEvidence | POST `/obligations/{id}/evidence` | Submit external payment evidence |
| API-X-approveReconciliation | POST `/reconciliations/{id}/approve` | Approve a financial reconciliation |
| API-X-recordDeliveryHandover | POST `/deliveries/{id}/handover` | Record physical handover |
| API-X-createSupportTicket | POST `/support-tickets` | Create support request |
| API-X-listSupportTicket | GET `/support-tickets` | List permitted SupportTicket |
| API-X-createPolicyVersion | POST `/admin/policies/{id}/versions` | Create pending policy version |
| API-X-getMetrics | GET `/analytics/metrics` | Get permitted aggregate metrics |
| API-X-readSellerLead | GET `/seller-leads/{id}` | Read SellerLead |
| API-X-transitionSellerLead | POST `/seller-leads/{id}/transitions` | Apply a guarded SellerLead transition |
| API-X-readAppointment | GET `/appointments/{id}` | Read Appointment |
| API-X-transitionAppointment | POST `/appointments/{id}/transitions` | Apply a guarded Appointment transition |
| API-X-readInspection | GET `/inspections/{id}` | Read Inspection |
| API-X-listInspection | GET `/inspections` | List permitted Inspection |
| API-X-createInspection | POST `/inspections` | Create Inspection |
| API-X-transitionInspection | POST `/inspections/{id}/transitions` | Apply a guarded Inspection transition |
| API-X-readVehicleListing | GET `/listings/{id}` | Read VehicleListing |
| API-X-transitionVehicleListing | POST `/listings/{id}/transitions` | Apply a guarded VehicleListing transition |
| API-X-readValuation | GET `/valuations/{id}` | Read Valuation |
| API-X-transitionValuation | POST `/valuations/{id}/transitions` | Apply a guarded Valuation transition |
| API-X-transitionAuction | POST `/auctions/{auctionId}/transitions` | Apply a guarded Auction transition |
| API-X-readBidCommand | GET `/bid-commands/{id}` | Read BidCommand |
| API-X-listBidCommand | GET `/bid-commands` | List permitted BidCommand |
| API-X-readDealerVerification | GET `/dealer-verifications/{id}` | Read DealerVerification |
| API-X-listDealerVerification | GET `/dealer-verifications` | List permitted DealerVerification |
| API-X-createDealerVerification | POST `/dealer-verifications` | Create DealerVerification |
| API-X-transitionDealerVerification | POST `/dealer-verifications/{id}/transitions` | Apply a guarded DealerVerification transition |
| API-X-readPurchaseRequest | GET `/purchase-requests/{id}` | Read PurchaseRequest |
| API-X-transitionPurchaseRequest | POST `/purchase-requests/{id}/transitions` | Apply a guarded PurchaseRequest transition |
| API-X-readFinancingApplication | GET `/financing-applications/{id}` | Read FinancingApplication |
| API-X-listFinancingApplication | GET `/financing-applications` | List permitted FinancingApplication |
| API-X-createFinancingApplication | POST `/financing-applications` | Create FinancingApplication |
| API-X-transitionFinancingApplication | POST `/financing-applications/{id}/transitions` | Apply a guarded FinancingApplication transition |
| API-X-readContract | GET `/contracts/{id}` | Read Contract |
| API-X-listContract | GET `/contracts` | List permitted Contract |
| API-X-createContract | POST `/contracts` | Create Contract |
| API-X-transitionContract | POST `/contracts/{id}/transitions` | Apply a guarded Contract transition |
| API-X-readPaymentObligation | GET `/obligations/{id}` | Read PaymentObligation |
| API-X-listPaymentObligation | GET `/obligations` | List permitted PaymentObligation |
| API-X-createPaymentObligation | POST `/obligations` | Create PaymentObligation |
| API-X-transitionPaymentObligation | POST `/obligations/{id}/transitions` | Apply a guarded PaymentObligation transition |
| API-X-readDelivery | GET `/deliveries/{id}` | Read Delivery |
| API-X-listDelivery | GET `/deliveries` | List permitted Delivery |
| API-X-createDelivery | POST `/deliveries` | Create Delivery |
| API-X-transitionDelivery | POST `/deliveries/{id}/transitions` | Apply a guarded Delivery transition |
| API-X-readWarrantyClaim | GET `/claims/{id}` | Read WarrantyClaim |
| API-X-listWarrantyClaim | GET `/claims` | List permitted WarrantyClaim |
| API-X-createWarrantyClaim | POST `/claims` | Create WarrantyClaim |
| API-X-transitionWarrantyClaim | POST `/claims/{id}/transitions` | Apply a guarded WarrantyClaim transition |
| API-X-readSupportTicket | GET `/support-tickets/{id}` | Read SupportTicket |
| API-X-transitionSupportTicket | POST `/support-tickets/{id}/transitions` | Apply a guarded SupportTicket transition |
| API-X-readResultRecord | GET `/auction-results/{id}` | Read versioned ResultRecord |
| API-X-readReconciliationRecord | GET `/reconciliations/{id}` | Read versioned ReconciliationRecord |
| API-X-readPolicyRecord | GET `/admin/policies/{id}` | Read versioned PolicyRecord |
| API-X-readTransaction | GET `/transactions/{id}` | Read transaction milestones |
| API-X-closeTransaction | POST `/transactions/{id}/closure` | Close verified transaction |
| API-X-readOwnershipTransfer | GET `/ownership-transfers/{id}` | Read ownership transfer |
| API-X-verifyOwnershipTransfer | POST `/ownership-transfers/{id}/verification` | Verify title evidence |
| API-X-completeAuthChallenge | POST `/auth/challenges/complete` | Complete single-use MFA challenge |
| API-X-readCurrentSession | GET `/auth/session` | Read current session |
| API-X-revokeCurrentSession | DELETE `/auth/session` | Revoke current session and live subscriptions |
| API-X-createStepUpChallenge | POST `/auth/step-up` | Create purpose-bound step-up challenge |
| API-X-requestAccountRecovery | POST `/auth/recovery` | Request account recovery |
| API-X-ingestProviderEvent | POST `/integration-events` | Receive authenticated normalized adapter event |
| API-X-completeStepUp | POST `/auth/step-up/complete` | completeStepUp |
| API-X-listVehicleTaxonomy | GET `/vehicle-taxonomy` | listVehicleTaxonomy |
| API-X-listBranchSlots | GET `/branches/{id}/slots` | listBranchSlots |
| API-X-createUploadGrant | POST `/files/upload-grants` | createUploadGrant |
| API-X-readFileStatus | GET `/files/{id}` | readFileStatus |
| API-X-createDownloadGrant | POST `/files/{id}/download-grants` | createDownloadGrant |
| API-X-prepareReconciliation | POST `/reconciliations` | Prepare a financial match |
| API-X-readPreferences | GET `/me/preferences` | readPreferences |
| API-X-changePreference | POST `/me/preferences` | changePreference |
| API-X-listSavedVehicles | GET `/me/saved-vehicles` | listSavedVehicles |
| API-X-setSavedVehicle | POST `/me/saved-vehicles` | setSavedVehicle |
| API-X-createProcurement | POST `/procurement-requests` | createProcurement |
| API-X-readProcurement | GET `/procurement-requests/{id}` | readProcurement |
| API-X-actOnProcurement | POST `/procurement-requests/{id}/actions` | actOnProcurement |
| API-X-createPrivacyRequest | POST `/privacy-requests` | createPrivacyRequest |
| API-X-readPrivacyRequest | GET `/privacy-requests/{id}` | readPrivacyRequest |
| API-X-requestExport | POST `/exports` | requestExport |
| API-X-readExportJob | GET `/exports/{id}` | readExportJob |
| API-X-downloadExport | POST `/exports/{id}/download-grants` | downloadExport |
| API-X-readInventoryListing | GET `/inventory/listings/{id}` | Read VehicleListing |
| API-X-createContent | POST `/content-items` | createContent |
| API-X-readContent | GET `/content-items/{id}` | readContent |
| API-X-reviseContent | POST `/content-items/{id}/revisions` | reviseContent |
| API-X-actOnContent | POST `/content-items/{id}/actions` | actOnContent |
| API-X-createCampaign | POST `/campaigns` | createCampaign |
| API-X-readCampaign | GET `/campaigns/{id}` | readCampaign |
| API-X-actOnCampaign | POST `/campaigns/{id}/actions` | actOnCampaign |
| API-X-approvePolicy | POST `/admin/policies/{id}/approvals` | approvePolicy |
| API-X-submitDealerApplication | POST `/dealer-applications` | Create pending dealer organization and verification |
| API-X-requestIntakeClaim | POST `/intake/claim-challenges` | Request ownership proof for an anonymous intake |
| API-X-claimIntake | POST `/intake/claims` | Claim an intake after contact proof |
| API-X-completeRecovery | POST `/auth/recovery/complete` | Complete account recovery |
| API-X-createConsumerOffer | POST `/consumer-offers` | Issue a seller-authorized consumer offer |
| API-X-readConsumerOffer | GET `/consumer-offers/{id}` | Read own consumer offer |
| API-X-acceptConsumerOffer | POST `/consumer-offers/{id}/acceptance` | Accept current consumer offer |
| API-X-withdrawConsumerOffer | POST `/consumer-offers/{id}/withdrawal` | Withdraw an unaccepted consumer offer |
| API-X-readPublishedContent | GET `/published-content/{slug}` | Read approved public editorial or help content |
| API-X-readListingBySlug | GET `/public-listings/{slug}` | Resolve an approved public vehicle URL |
| API-X-estimatePublicVehicle | POST `/valuation-estimates` | Request an indicative public valuation range |
| API-X-readInspectionTemplate | GET `/inspection-templates/{id}` | Read assigned or approved inspection template |
| API-X-readInspectionRevision | GET `/inspection-revisions/{id}` | Read an immutable or working inspection revision |
| API-X-createSavedSearch | POST `/me/saved-searches` | Save own public listing filters |
| API-X-listSavedSearches | GET `/me/saved-searches` | List own saved searches |
| API-X-deleteSavedSearch | DELETE `/me/saved-searches/{id}` | Remove own saved search |
