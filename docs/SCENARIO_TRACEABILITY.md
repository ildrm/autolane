# Complete scenario traceability and acceptance specification

**ID:** SCENARIO-TRACEABILITY · **Version:** 0.3 · **Status:** proposed, not runtime-tested · **Owner:** Requirements and QA · **Updated:** 2026-11-15

All120 scenarios in the original catalog have a unique FR-SCN requirement and TST-SCN acceptance ID. The [structured source](contracts/scenario-traceability.json) contains the same records, including six ordered test steps. A supporting API is a contract dependency; it does not grant the scenario actor every staff operation listed. Governed manual procedures, disabled credit and provider onboarding are explicit delivery modes below. Analytics uses fixed `workflow_outcome_recorded` v1 with scenario_id/outcome and approved purpose; no raw contact, VIN, evidence or bid amount. Audit is a restricted business record, separate from optional analytics.

For every scenario: prepare named preconditions with synthetic records and pinned policy; act as the scoped principal; verify its specific success, audit and asynchronous effects; replay same key and test changed payload conflict; repeat with wrong scope/stale ETag and no disclosure/mutation; inject the named failure and verify row-specific recovery. Manual workflows apply equivalent access, evidence and duplicate-action controls through a recorded procedure. No application test is claimed passed by these specifications.

## SCN-01 — Last appointment slot

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-001 / TST-SCN-001 |
| Priority / actor | P0 / seller/branch, ROLE-002 or ROLE-006 |
| Screen / entity | SCR-005 / Appointment |
| Preconditions, trigger and input | One eligible capacity unit remains; two authorized parties concurrently request the same branch and slot. |
| Success | Atomically reserve once; requested → confirmed for one case. |
| Failure and recovery | Other request conflicts; preserve draft and offer other slots; no overbooking. |
| Supporting operation IDs | createAppointment, readAppointment, transitionAppointment |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Capacity override and cancellation windows require policy approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-02 — Correct published inspection

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-002 / TST-SCN-002 |
| Priority / actor | P0 / inspection supervisor, ROLE-008 |
| Screen / entity | SCR-022 / Inspection |
| Preconditions, trigger and input | A published report has a documented material error; supervisor submits corrected findings and evidence. |
| Success | Publish a new report version and retain original; published v1 → published v2. |
| Failure and recovery | Incomplete evidence returns for review; material dispute places affected sale on hold. |
| Supporting operation IDs | readInspection, createInspectionRevision, transitionInspection, publishInspection |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Who must be notified and whether an auction pauses require DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-03 — Simultaneous valid bids

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-003 / TST-SCN-003 |
| Priority / actor | P0 / authorized dealer bidder, ROLE-004 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Auction open and two authorized bidders submit competing otherwise valid bids. |
| Success | Order evaluations atomically; each receives its actual decision and one current leader. |
| Failure and recovery | A bid no longer meeting current increment is rejected; committed records remain ordered. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Increment, tie and time authority require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-04 — Seller decision on offer

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-004 / TST-SCN-004 |
| Priority / actor | P0 / verified seller, ROLE-002 |
| Screen / entity | SCR-008 / SellerDecision |
| Preconditions, trigger and input | A current offer version and disclosed response terms are presented; seller chooses accept or reject. |
| Success | Record explicit decision with offer version and actor; presented → accepted or rejected. |
| Failure and recovery | Stale, expired or unauthorized action is refused; silence is not acceptance. |
| Supporting operation IDs | readResultRecord, recordSellerDecision |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Effect and expiry of acceptance require DEC-04/DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-05 — Reconcile before closure

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-005 / TST-SCN-005 |
| Priority / actor | P0 / finance approver, ROLE-014 |
| Screen / entity | SCR-026 / Transaction |
| Preconditions, trigger and input | A transaction has an executed contract and evidence submitted for obligations and transfer. |
| Success | Independently verify policy-required evidence; reconcile and close only if all guards pass. |
| Failure and recovery | Mismatch, missing evidence or unresolved material discrepancy blocks ordinary closure and creates assigned case. |
| Supporting operation IDs | readTransaction, closeTransaction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Evidence and permitted exceptional close require DEC-03/DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-06 — Conflicting seller authority

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-006 / TST-SCN-006 |
| Priority / actor | P0 / branch coordinator, ROLE-006 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | Submitted ownership documents disagree with declared seller or vehicle. |
| Success | Create review hold; reviewer validates authority before publication. |
| Failure and recovery | If evidence cannot establish authority, reject or withdraw according to approved terms; no auction is created. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Acceptable ownership evidence and appeal require DEC-01/DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-07 — Branch closure or no-show

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-007 / TST-SCN-007 |
| Priority / actor | P1 / branch coordinator, ROLE-006 |
| Screen / entity | SCR-005 / Appointment |
| Preconditions, trigger and input | A confirmed appointment is missed or the branch is marked closed. |
| Success | Record distinct no-show or branch-closure reason; identify affected appointments and offer rescheduling. |
| Failure and recovery | Failed notice is queued for staff follow-up; no-show is not assigned to a customer because a branch closed. |
| Supporting operation IDs | createAppointment, readAppointment, transitionAppointment |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Cancellation and rebooking deadlines require policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-08 — Uninspectable safety item

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-008 / TST-SCN-008 |
| Priority / actor | P0 / assigned inspector, ROLE-007 |
| Screen / entity | SCR-022 / Inspection |
| Preconditions, trigger and input | A required checklist item cannot be examined due to vehicle condition or access. |
| Success | Record unknown with reason and evidence; submit to supervisor. |
| Failure and recovery | Do not replace unknown with pass; if policy prohibits publication keep report in review. |
| Supporting operation IDs | readInspection, createInspectionRevision, transitionInspection, publishInspection |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Minimum report completeness requires DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-09 — Dealer suspended during open auction

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-009 / TST-SCN-009 |
| Priority / actor | P0 / dealer operations, explicit suspension grant pending role-matrix approval |
| Screen / entity | SCR-015 / DealerVerification |
| Preconditions, trigger and input | An active bidder becomes suspended while an auction is open. |
| Success | Recheck eligibility and prevent further bids while retaining accepted history. |
| Failure and recovery | Previously accepted bids are handled only under published terms and recorded decision; no silent erasure. |
| Supporting operation IDs | readDealerVerification, transitionDealerVerification |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Treatment of existing bids requires DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-10 — Bid at authoritative deadline

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-010 / TST-SCN-010 |
| Priority / actor | P0 / authorized dealer bidder, ROLE-004 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | A bid and close contend near the scheduled end time. |
| Success | Apply approved authoritative time and ordering once; acknowledge the recorded acceptance or rejection. |
| Failure and recovery | Late bid is rejected without mutation; client timer alone never decides. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Cutoff, tie and extension policy require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-11 — Reconnect after ambiguous bid

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-011 / TST-SCN-011 |
| Priority / actor | P0 / authorized dealer bidder, ROLE-004 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Connection fails after bid submission but before response reaches dealer. |
| Success | Query recorded submission by original request key; display authoritative decision. |
| Failure and recovery | If still pending, show unknown and retry status safely; do not submit a fresh independent bid. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Status retention and outage terms require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-12 — Auction has no qualifying bid

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-012 / TST-SCN-012 |
| Priority / actor | P1 / auction operator, ROLE-010 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | An auction closes with no accepted qualifying bid. |
| Success | Record no-qualifying-result and notify assigned seller support. |
| Failure and recovery | No offer or winner is invented; follow-up or relist requires consent and approved policy. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Qualification, reserve and relist require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-13 — Seller rejects presented offer

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-013 / TST-SCN-013 |
| Priority / actor | P1 / verified seller, ROLE-002 |
| Screen / entity | SCR-008 / SellerDecision |
| Preconditions, trigger and input | Seller reviews the current offer and chooses rejection. |
| Success | Record rejected decision and notify authorized CRM owner; no sale is marked complete. |
| Failure and recovery | If offer became stale reject submission and require refresh; optional reason is not mandatory without policy. |
| Supporting operation IDs | readResultRecord, recordSellerDecision |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Further negotiation and relisting require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-14 — Winning dealer defaults

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-014 / TST-SCN-014 |
| Priority / actor | P0 / auction operator, ROLE-010; restriction requires separate authorized grant |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | A winning dealer fails an obligation established by approved terms. |
| Success | Open default case, preserve terms and evidence, assign legal owner. |
| Failure and recovery | Restrict account only as authorized; do not silently select next bidder or impose automatic penalty. |
| Supporting operation IDs | createSupportTicket, readSupportTicket, transitionSupportTicket |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | ROLE-012 opens a default matter from the support case, preserves accepted terms and notices, records an independently approved disposition; no auto-penalty or next-bidder award. |
| Policy dependency | Notice, cure, remedies and deposits require DEC-04/DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-15 — Payment mismatch

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-015 / TST-SCN-015 |
| Priority / actor | P0 / finance preparer, ROLE-013 |
| Screen / entity | SCR-043 / PaymentObligation |
| Preconditions, trigger and input | Payment evidence has a payee, amount, currency or reference inconsistent with an obligation. |
| Success | Flag discrepancy and assign independent investigation; transaction remains pending. |
| Failure and recovery | Do not claim settlement from uploaded receipt; query authoritative provider or bank through approved channel. |
| Supporting operation IDs | readPaymentObligation, submitPaymentEvidence, prepareReconciliation, approveReconciliation, transitionPaymentObligation |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Evidence, tolerances and custody require DEC-03. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-16 — Ownership transfer delayed

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-016 / TST-SCN-016 |
| Priority / actor | P0 / legal operator, ROLE-012 |
| Screen / entity | SCR-042 / OwnershipTransfer |
| Preconditions, trigger and input | Payment, title and custody milestones are at different completion states. |
| Success | Record each status separately, assign transfer follow-up and inform affected authorized parties. |
| Failure and recovery | Keep unresolved title pending; do not infer legal ownership or require premature custody transfer. |
| Supporting operation IDs | readOwnershipTransfer, verifyOwnershipTransfer |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Market-specific transfer sequence and deadline require DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-17 — Seller disputes inspection

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-017 / TST-SCN-017 |
| Priority / actor | P0 / support and supervisor, ROLE-011/ROLE-008 |
| Screen / entity | SCR-022 / Inspection |
| Preconditions, trigger and input | Seller challenges a published finding with a case reference and explanation. |
| Success | Preserve original version; review evidence and issue correction or reasoned decision. |
| Failure and recovery | If material issue threatens auction fairness, apply approved hold policy; retain dispute and appeal evidence. |
| Supporting operation IDs | readInspection, createInspectionRevision, transitionInspection, publishInspection |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Coverage, response times and remedy require DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-18 — External service outage

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-018 / TST-SCN-018 |
| Priority / actor | P0 / integration owner with support, scoped service identity |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | Identity, message or payment provider times out after an attempted request. |
| Success | Mark operation pending, correlate original request and query authoritative provider on recovery. |
| Failure and recovery | Use safe retries; create assigned exception at exhaustion and never claim unconfirmed success. |
| Supporting operation IDs | createSupportTicket, readSupportTicket, transitionSupportTicket |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Provider-specific retry windows and legal notices require agreement. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-19 — Cross-tenant record access attempt

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-019 / TST-SCN-019 |
| Priority / actor | P0 / dealer bidder or staff, ROLE-004 or scoped staff |
| Screen / entity | SCR-028 / Authorization |
| Preconditions, trigger and input | An authenticated user requests another organization's private case or document. |
| Success | Server denies request and logs access decision without disclosing record contents. |
| Failure and recovery | Do not leak information in search, real-time streams, download URL or error text. |
| Supporting operation IDs | readPolicyRecord, createPolicyVersion |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Privacy log retention and notification require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-20 — Privacy deletion request with hold

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-020 / TST-SCN-020 |
| Priority / actor | P0 / privacy officer, explicitly granted privacy role |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | A verified subject requests erasure for a record under a legal or retention hold. |
| Success | Record request, evaluate scope and hold, restrict processing when applicable and communicate reason. |
| Failure and recovery | Never delete required held evidence blindly; escalate unresolved basis for counsel review. |
| Supporting operation IDs | createPrivacyRequest, readPrivacyRequest |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Typed request and authorized status contracts exist. Processor/external fulfillment remains an assigned review workflow and must not be marked complete before evidence. |
| Policy dependency | Deletion deadlines, legal basis and appeal require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-21 — Vehicle becomes unavailable during viewing

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-021 / TST-SCN-021 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-030 / VehicleListing |
| Preconditions, trigger and input | Buyer views a published listing while inventory changes to unavailable. |
| Success | Refresh or invalidate availability and retain any existing inquiry for follow-up. |
| Failure and recovery | Prevent new claim that vehicle is available; never reveal dealer-only auction data. |
| Supporting operation IDs | listConsumerListings, readVehicleListing, transitionVehicleListing |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Availability freshness commitment requires product policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-22 — Damage during transport

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-022 / TST-SCN-022 |
| Priority / actor | P0 / assigned logistics operator, explicitly granted logistics role |
| Screen / entity | SCR-034 / Delivery |
| Preconditions, trigger and input | A vehicle's delivery condition differs from recorded pickup condition. |
| Success | Preserve time-stamped before/after evidence, record exception and assign claim owner. |
| Failure and recovery | Do not infer title change or promise compensation; secure third-party evidence. |
| Supporting operation IDs | createDelivery, readDelivery, transitionDelivery, recordDeliveryHandover |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Carrier liability, insurance and remedy require DEC-05/DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-23 — First-time seller begins intake

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-023 / TST-SCN-023 |
| Priority / actor | P1 / visitor then seller, ROLE-001/ROLE-002 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | A visitor starts a new request and enters vehicle, contact and required consent. |
| Success | Validate entries, create request and associate verified account when required; draft → submitted. |
| Failure and recovery | Preserve safe draft on invalid data; no marketing permission is inferred. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Verification and consent basis require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-24 — Returning seller starts another request

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-024 / TST-SCN-024 |
| Priority / actor | P1 / authenticated seller, ROLE-002 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | A verified seller starts a new vehicle case from their account. |
| Success | Reuse authorized contact details by confirmation and create a distinct vehicle request. |
| Failure and recovery | Possible duplicate enters review rather than automatic merge or disclosure of another account. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Duplicate resolution and data minimization require policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-25 — Vehicle meets eligibility criteria

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-025 / TST-SCN-025 |
| Priority / actor | P1 / CRM reviewer, ROLE-011 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | Submitted vehicle information meets the active approved eligibility policy. |
| Success | Record applicable policy version and mark request eligible for branch booking. |
| Failure and recovery | Unknown or conflicting attributes route to manual review, not automatic approval. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Vehicle eligibility rules and market coverage require approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-26 — Unsupported vehicle category

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-026 / TST-SCN-026 |
| Priority / actor | P1 / seller and CRM reviewer, ROLE-002/ROLE-011 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | Submitted make, category or location is outside approved intake coverage. |
| Success | Show respectful unavailable message and optionally record consented follow-up. |
| Failure and recovery | Do not create a booking or promise future support; correct a mistaken taxonomy through review. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Supported vehicle categories and follow-up require product policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-27 — Incomplete vehicle details

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-027 / TST-SCN-027 |
| Priority / actor | P1 / seller, ROLE-002 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | A draft lacks a required make, year, mileage or location field. |
| Success | Display each required field and retain valid entered values for completion. |
| Failure and recovery | Do not create an eligible application from incomplete values; retry save if service unavailable. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Required fields and retention period require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-28 — Duplicate seller request review

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-028 / TST-SCN-028 |
| Priority / actor | P0 / CRM reviewer, ROLE-011 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | A new request has matching vehicle identifier and contact to an existing case. |
| Success | Flag potential duplicate for scoped review and associate records only after verified decision. |
| Failure and recovery | Do not disclose another person's request or merge solely from approximate matches. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | ROLE-011 reviews assigned lead evidence, requests additional identity proof, links a reviewed duplicate case reference without deleting or merging original records; ambiguous match remains on hold. |
| Policy dependency | Matching thresholds and merge authority require policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-29 — Invalid phone entry

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-029 / TST-SCN-029 |
| Priority / actor | P1 / seller, ROLE-002 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | Seller enters a phone number invalid for chosen country/format. |
| Success | Show specific accessible field error and retain other form values. |
| Failure and recovery | Do not send verification or expose whether phone belongs to an account. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Allowed countries and verification provider require DEC-01/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-30 — Verification failure and retry

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-030 / TST-SCN-030 |
| Priority / actor | P0 / seller, ROLE-002 |
| Screen / entity | SCR-038 / Authentication |
| Preconditions, trigger and input | Correctly formatted phone receives a challenge that is entered incorrectly or expires. |
| Success | Explain failure, provide a bounded resend or approved support path and preserve draft. |
| Failure and recovery | Throttle repeated attempts without revealing codes; no verified status until provider confirmation. |
| Supporting operation IDs | createSession, completeAuthChallenge, requestAccountRecovery, createStepUpChallenge, completeStepUp |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Retry limits and recovery evidence require security approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-31 — Book available appointment

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-031 / TST-SCN-031 |
| Priority / actor | P1 / seller, ROLE-002 |
| Screen / entity | SCR-005 / Appointment |
| Preconditions, trigger and input | Eligible request, permitted branch and available slot are displayed in branch local time. |
| Success | Confirm one reservation with reference, timezone and document instructions. |
| Failure and recovery | If slot is taken concurrently, preserve request and offer alternatives; no duplicate notification. |
| Supporting operation IDs | createAppointment, readAppointment, transitionAppointment |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Scheduling horizons and cancellation terms require operations approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-32 — Reschedule confirmed appointment

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-032 / TST-SCN-032 |
| Priority / actor | P1 / seller or branch coordinator, ROLE-002/ROLE-006 |
| Screen / entity | SCR-005 / Appointment |
| Preconditions, trigger and input | A confirmed appointment and new eligible slot exist; actor requests change. |
| Success | Reserve new capacity and release old reservation consistently, then show updated confirmation. |
| Failure and recovery | If replacement slot fails, retain original confirmed reservation and display conflict. |
| Supporting operation IDs | createAppointment, readAppointment, transitionAppointment |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Cutoff and capacity-change policy require approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-33 — Cancel confirmed appointment

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-033 / TST-SCN-033 |
| Priority / actor | P1 / seller or branch coordinator, ROLE-002/ROLE-006 |
| Screen / entity | SCR-005 / Appointment |
| Preconditions, trigger and input | A current appointment is cancellable under applicable terms. |
| Success | Record cancellation and reason if supplied; release capacity once and notify appropriate parties. |
| Failure and recovery | If cancellation is too late or service unavailable show accurate state and route to assistance. |
| Supporting operation IDs | createAppointment, readAppointment, transitionAppointment |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Late cancellation consequences require policy and legal review. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-34 — Seller arrives late

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-034 / TST-SCN-034 |
| Priority / actor | P1 / branch coordinator, ROLE-006 |
| Screen / entity | SCR-005 / Appointment |
| Preconditions, trigger and input | A confirmed customer arrives after scheduled time and branch checks queue. |
| Success | Record arrival time and present approved reallocation or reschedule option. |
| Failure and recovery | If no capacity exists do not promise same-day inspection; create a follow-up task. |
| Supporting operation IDs | createAppointment, readAppointment, transitionAppointment |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Grace period and queue priority require operations approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-35 — Seller arrives at wrong branch

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-035 / TST-SCN-035 |
| Priority / actor | P1 / branch coordinator, ROLE-006 |
| Screen / entity | SCR-005 / Appointment |
| Preconditions, trigger and input | Customer presents a valid booking at a branch different from the booked location. |
| Success | Verify identity and booking; offer transfer if authorized capacity exists or directions/reschedule. |
| Failure and recovery | Do not cancel the original appointment without approved action; protect other branch records. |
| Supporting operation IDs | createAppointment, readAppointment, transitionAppointment |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Cross-branch transfer authority and capacity rules require policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-36 — Incorrect seller documents

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-036 / TST-SCN-036 |
| Priority / actor | P0 / branch coordinator, ROLE-006 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | Customer arrives with documents that are incomplete, expired or inconsistent. |
| Success | Record document issue and missing requirement; provide secure route to resubmit. |
| Failure and recovery | Do not publish vehicle or represent identity verified; escalate suspected fraud to authorized team. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Required document list and fraud response require DEC-01/DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-37 — Inspection completed and explained

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-037 / TST-SCN-037 |
| Priority / actor | P1 / inspector and supervisor, ROLE-007/ROLE-008 |
| Screen / entity | SCR-022 / Inspection |
| Preconditions, trigger and input | Vehicle and seller authority validated, all required checklist items assessed or marked unknown. |
| Success | Review and publish versioned findings and limitations; inform seller that report is available. |
| Failure and recovery | Incomplete review returns to assigned inspector; no premature completed report. |
| Supporting operation IDs | readInspection, createInspectionRevision, transitionInspection, publishInspection |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Checklist and publication criteria require DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-38 — Cancel request before contract

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-038 / TST-SCN-038 |
| Priority / actor | P0 / verified seller, ROLE-002 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | Seller requests withdrawal after request submission and before contract execution. |
| Success | Record request and apply permitted cancellation terms; inform assigned CRM owner. |
| Failure and recovery | If auction is active or contract effects are unclear, hold for legal review rather than silently cancel. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Withdrawal rights, auction effects and fees require DEC-04/DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-39 — Dispute contract terms

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-039 / TST-SCN-039 |
| Priority / actor | P0 / seller with legal operator, ROLE-002/ROLE-012 |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | Seller identifies incorrect party, price or condition in an issued agreement. |
| Success | Open legal case, pause signature or downstream action and review the applicable version. |
| Failure and recovery | Do not overwrite a signed document; issue a reviewed amendment and collect required acknowledgements if approved. |
| Supporting operation IDs | createSupportTicket, readSupportTicket, transitionSupportTicket |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | ROLE-012 reviews the challenged document hash and instructions, records a legal hold and uses the contract void/amend path only after authority is established; finance remains separate. |
| Policy dependency | Amendment rights and signatures require DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-40 — Change destination payment details

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-040 / TST-SCN-040 |
| Priority / actor | P0 / seller and finance reviewer, ROLE-002/ROLE-013 |
| Screen / entity | SCR-043 / PaymentObligation |
| Preconditions, trigger and input | Authorized party requests a change to previously verified bank destination. |
| Success | Place change and affected payment initiation on hold; independently verify and obtain independent approval. |
| Failure and recovery | Failed identity or conflicting evidence leaves original instruction unchanged and escalates possible fraud. |
| Supporting operation IDs | readPaymentObligation, submitPaymentEvidence, prepareReconciliation, approveReconciliation, transitionPaymentObligation |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | ROLE-013 records a proposed counterparty-detail change; ROLE-014 independently verifies through a known channel and retains prior evidence. External counterparty executes any real payment under approved process. |
| Policy dependency | Verification method and approver authority require DEC-03/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-41 — Settlement remains delayed

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-041 / TST-SCN-041 |
| Priority / actor | P1 / seller and finance staff, ROLE-002/ROLE-013 |
| Screen / entity | SCR-043 / PaymentObligation |
| Preconditions, trigger and input | An obligation passes its agreed expected date without verified completion. |
| Success | Show truthful pending status, assign follow-up and query approved authoritative source. |
| Failure and recovery | Do not claim funds arrived or provide unapproved compensation; escalate overdue case. |
| Supporting operation IDs | readPaymentObligation, submitPaymentEvidence, prepareReconciliation, approveReconciliation, transitionPaymentObligation |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Settlement deadlines, notices and remedy require DEC-03/DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-42 — Seller changes a vehicle attribute after submission

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-042 / TST-SCN-042 |
| Priority / actor | P1 / seller and CRM reviewer, ROLE-002/ROLE-011 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | Seller corrects mileage or condition before report publication. |
| Success | Version the proposed change, record actor and ask reviewer whether a new inspection is needed. |
| Failure and recovery | Changes after auction publication are held for review; no silent alteration of buyer evidence. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Materiality and restart criteria require DEC-04/DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-43 — Seller withdraws marketing consent

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-043 / TST-SCN-043 |
| Priority / actor | P1 / seller, ROLE-002 |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | Authenticated seller withdraws optional promotional permission. |
| Success | Record updated preference/version and stop future eligible marketing messages. |
| Failure and recovery | Do not terminate necessary service communication solely from marketing opt-out; failed propagation enters retry queue. |
| Supporting operation IDs | changePreference, readPreferences |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Typed request and authorized status contracts exist. Processor/external fulfillment remains an assigned review workflow and must not be marked complete before evidence. |
| Policy dependency | Lawful bases and propagation deadlines require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-44 — Seller loses access during offer period

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-044 / TST-SCN-044 |
| Priority / actor | P0 / seller with support, ROLE-002/ROLE-011 |
| Screen / entity | SCR-038 / Authentication |
| Preconditions, trigger and input | A verified seller cannot sign in while an offer is awaiting response. |
| Success | Use approved identity recovery; restore scoped access and display current offer state. |
| Failure and recovery | Do not extend deadline or accept a decision solely on an unverified support request. |
| Supporting operation IDs | createSession, completeAuthChallenge, requestAccountRecovery, createStepUpChallenge, completeStepUp |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Recovery proof and offer extension require DEC-04/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-45 — Seller raises incorrect fee quote

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-045 / TST-SCN-045 |
| Priority / actor | P1 / seller and finance reviewer, ROLE-002/ROLE-013 |
| Screen / entity | SCR-043 / PaymentObligation |
| Preconditions, trigger and input | Seller identifies a mismatch in the displayed fee or tax line before commitment. |
| Success | Hold quote, review policy version and issue corrected version with required acknowledgement. |
| Failure and recovery | Do not silently replace an accepted quote or invent a charge; escalate disputed fee. |
| Supporting operation IDs | readPaymentObligation, submitPaymentEvidence, prepareReconciliation, approveReconciliation, transitionPaymentObligation |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Fee calculation, tax and refund rights require DEC-01/DEC-03. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-46 — Seller reports suspected account compromise

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-046 / TST-SCN-046 |
| Priority / actor | P0 / seller with security, ROLE-002 and security role |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | Seller reports unauthorized access or unexpected transaction action. |
| Success | Suspend risky sessions, preserve audit, verify identity and route to security investigation. |
| Failure and recovery | Do not disclose sensitive details to the unverified reporter or alter accepted auction history silently. |
| Supporting operation IDs | createSupportTicket, readSupportTicket, transitionSupportTicket |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Response, data retention and notices require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-47 — Create auction draft

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-047 / TST-SCN-047 |
| Priority / actor | P0 / auction operator, ROLE-010 |
| Screen / entity | SCR-025 / AuctionPreparation |
| Preconditions, trigger and input | A reviewed inspection and eligible vehicle are available; operator creates draft with approved terms. |
| Success | Record draft, vehicle/report versions and intended eligibility without publishing. |
| Failure and recovery | Missing report, seller authority or approved terms blocks scheduling and returns actionable reason. |
| Supporting operation IDs | createAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Auction creation authority and mandatory terms require DEC-04/DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-48 — Schedule auction

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-048 / TST-SCN-048 |
| Priority / actor | P1 / auction operator, ROLE-010 |
| Screen / entity | SCR-025 / AuctionPreparation |
| Preconditions, trigger and input | A valid draft has a permitted proposed start and end in the applicable time zone. |
| Success | Validate future start, end after start and allowed policy; record scheduled state and UTC instants. |
| Failure and recovery | Conflicting or invalid schedule fails without opening auction; show local-zone conversion. |
| Supporting operation IDs | createAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Duration and scheduling authority require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-49 — Publish scheduled auction

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-049 / TST-SCN-049 |
| Priority / actor | P0 / auction operator, ROLE-010 |
| Screen / entity | SCR-025 / AuctionPreparation |
| Preconditions, trigger and input | Eligible auction draft has reviewed terms, authorized vehicle and required report version. |
| Success | Publish to eligible dealers and record terms/version; scheduled listing becomes discoverable. |
| Failure and recovery | Unapproved report or legal hold blocks publication; no private report is made public. |
| Supporting operation IDs | createAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Required approvals and visibility require DEC-04/DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-50 — Approved dealer joins auction

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-050 / TST-SCN-050 |
| Priority / actor | P1 / authorized dealer bidder, ROLE-004 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Dealer organization active, member authorized and auction within eligible visibility. |
| Success | Show eligible auction and current authorized report/terms; record viewing or join as configured. |
| Failure and recovery | Revoked member or wrong organization receives denial without private auction details. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Eligibility and report disclosure require DEC-04/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-51 — Unauthorized dealer denied

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-051 / TST-SCN-051 |
| Priority / actor | P0 / unapproved dealer, ROLE-004 without active grant |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Dealer attempts access or bid before account approval or after suspension. |
| Success | Deny protected data and bid action; provide safe onboarding or support route. |
| Failure and recovery | Do not reveal competitor prices, identities or hidden eligibility criteria. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Approval, appeal and restricted disclosures require policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-52 — Bid below required increment

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-052 / TST-SCN-052 |
| Priority / actor | P0 / authorized dealer bidder, ROLE-004 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Open auction has approved current leading amount and increment; a smaller increment is submitted. |
| Success | Reject with the valid minimum if the approved policy allows disclosure; retain no accepted mutation. |
| Failure and recovery | Refresh authoritative current amount because another bid may have changed the minimum. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Increment schedule and disclosure require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-53 — Bid accepted successfully

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-053 / TST-SCN-053 |
| Priority / actor | P0 / authorized dealer bidder, ROLE-004 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Open auction, active bid authority, valid currency and amount satisfying policy. |
| Success | Atomically append accepted bid, return bid reference and authoritative status, publish permitted update. |
| Failure and recovery | If commit fails return error or unknown and query status; never show success before durable record. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Bid binding effect and visible fields require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-54 — Duplicate bid submission

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-054 / TST-SCN-054 |
| Priority / actor | P0 / authorized dealer bidder, ROLE-004 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Same bidder repeats a request with identical idempotency key and payload. |
| Success | Return original accepted or rejected decision and reference without another bid. |
| Failure and recovery | Same key with different payload returns conflict; no silent replacement. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Idempotency retention and payload handling require technical policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-55 — Countdown mismatch

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-055 / TST-SCN-055 |
| Priority / actor | P0 / authorized dealer bidder, ROLE-004 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Browser clock or network delay causes display timer to differ from server time. |
| Success | Refresh server-derived deadline and clearly indicate stale connection when detected. |
| Failure and recovery | If deadline passed on authority, reject bid and retain audit despite client showing time remaining. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Clock tolerance and public wording require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-56 — Close with valid bids

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-056 / TST-SCN-056 |
| Priority / actor | P0 / auction engine and operator, scoped system role |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Auction reaches approved close condition with accepted qualifying bids. |
| Success | Freeze ordered accepted ledger and produce one provisional outcome referencing governing terms. |
| Failure and recovery | If close cannot commit, leave outcome pending and incident queue; no fabricated winner. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Reserve, qualification and finality require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-57 — Reserve not reached

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-057 / TST-SCN-057 |
| Priority / actor | P0 / auction engine, scoped system role |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | An approved reserve applies and highest accepted bid is below it at close. |
| Success | Record unsuccessful or review-required outcome exactly as published policy specifies. |
| Failure and recovery | Do not disclose private reserve if prohibited or claim a winner; seller and operations see authorized status. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Reserve configuration and result semantics require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-58 — Select highest qualifying bid

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-058 / TST-SCN-058 |
| Priority / actor | P0 / auction engine and operator, scoped system role |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Auction closed with qualifying accepted bids and approved ranking rules. |
| Success | Select one outcome using authoritative accepted sequence and record rule version. |
| Failure and recovery | If disqualification or tie handling is unresolved, hold outcome rather than improvise. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Ties, reserve and winner selection require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-59 — Dealer has insufficient approved credit

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-059 / TST-SCN-059 |
| Priority / actor | P1 / dealer bidder and finance partner, ROLE-004 plus scoped partner |
| Screen / entity | SCR-033 / FinancingApplication |
| Preconditions, trigger and input | An approved financing/credit policy applies and available authorized limit is insufficient. |
| Success | Display eligible next step or reject per approved policy without exposing unrelated credit data. |
| Failure and recovery | Never assume lender approval or auto-create a loan; outdated credit status is pending review. |
| Supporting operation IDs | readFinancingApplication, createFinancingApplication, transitionFinancingApplication, ingestProviderEvent |
| Delivery mode | disabled_pending_policy |
| Boundary and procedure | Credit-backed bids are disabled by default. Reject an attempted credit path without changing auction state; activate only after approved credit policy, lender contracts and a separately reviewed exposure-reservation design. |
| Policy dependency | Credit limit, underwriting and enforcement require DEC-10 and lender agreement. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-60 — Cancel scheduled or open auction

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-060 / TST-SCN-060 |
| Priority / actor | P0 / auction operator, ROLE-010 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | A permitted cancellation reason occurs and actor has required authorization. |
| Success | Apply published cancellation procedure, capture approvals and preserve existing bids and report version. |
| Failure and recovery | Unauthorized request is denied; do not erase bids or imply participants accepted new terms. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Cancellation grounds, timing and notifications require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-61 — Relist an unsuccessful vehicle

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-061 / TST-SCN-061 |
| Priority / actor | P1 / auction operator, ROLE-010 |
| Screen / entity | SCR-025 / AuctionPreparation |
| Preconditions, trigger and input | Prior auction ended unsuccessfully and relisting is permitted with required seller consent. |
| Success | Create a new auction referencing old outcome but new schedule, terms and report version. |
| Failure and recovery | Do not reuse stale evidence or carry old bids as new bids; review material report changes. |
| Supporting operation IDs | createAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Relist consent, fees and inspection freshness require DEC-04/DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-62 — Detect suspicious bid pattern

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-062 / TST-SCN-062 |
| Priority / actor | P0 / fraud analyst, explicitly granted risk role |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | Monitoring identifies repeated coordinated or anomalous activity under approved indicators. |
| Success | Open restricted review case, preserve evidence and apply only authorized temporary restrictions. |
| Failure and recovery | Avoid publicly accusing users; prior bids remain until a reasoned policy-based decision. |
| Supporting operation IDs | createSupportTicket, readSupportTicket, transitionSupportTicket |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | ROLE-019 opens a restricted risk review, preserves bid sequence and explanation, and uses the suspension transition only with authorized evidence. A signal alone is not a finding of fraud. |
| Policy dependency | Detection thresholds, investigations and appeals require DEC-04/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-63 — Dealer disputes auction result

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-063 / TST-SCN-063 |
| Priority / actor | P0 / dealer bidder with auction/legal review, ROLE-004/ROLE-010/ROLE-012 |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | Dealer submits an outcome complaint with auction and bid references within policy. |
| Success | Preserve ledger and incident evidence; assign independent reviewer and communicate case state. |
| Failure and recovery | Do not silently rerank or reveal another dealer's confidential details; appeal per approved terms. |
| Supporting operation IDs | createSupportTicket, readSupportTicket, transitionSupportTicket |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Dispute period, evidence and remedy require DEC-04/DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-64 — Interruption during finalization

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-064 / TST-SCN-064 |
| Priority / actor | P0 / incident commander and auction operator, scoped roles |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | System interruption occurs while a close operation is in progress. |
| Success | Determine authoritative committed close and bid log; hold award until reconciliation. |
| Failure and recovery | If commit status is ambiguous keep result pending; apply approved cancellation or recovery terms. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Outage and finalization recovery require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-65 — Dealer submits wrong currency

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-065 / TST-SCN-065 |
| Priority / actor | P1 / authorized dealer bidder, ROLE-004 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | Open auction is configured in one ISO currency and bid specifies a different currency. |
| Success | Reject bid with clear currency mismatch and preserve submitted audit evidence. |
| Failure and recovery | Do not convert amounts silently or accept exchange-rate assumption. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Currency policy and exchange handling require DEC-01/DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-66 — Inspection changes during live auction

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-066 / TST-SCN-066 |
| Priority / actor | P0 / auction operator and supervisor, ROLE-010/ROLE-008 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | A material report correction is approved while bids already exist. |
| Success | Preserve each report version and route auction to policy-controlled hold or update decision. |
| Failure and recovery | Do not silently substitute report behind accepted bids; notify permitted users as policy requires. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Materiality, cancellation and bidder consent require DEC-04/DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-67 — Auction notification delivery fails

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-067 / TST-SCN-067 |
| Priority / actor | P1 / communications service with support, scoped service role |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | An authorized dealer or seller notification is queued but provider cannot deliver it. |
| Success | Record failed delivery and retry using same notification identity; show operations queue after exhaustion. |
| Failure and recovery | No message is represented as delivered or legal acceptance; alternative channel requires consent. |
| Supporting operation IDs | createSupportTicket, readSupportTicket, transitionSupportTicket |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | Notification worker retries same intent within configured budget; ROLE-011 owns exhausted delivery in the operations queue and verifies current contact preference before an approved alternate channel. |
| Policy dependency | Channel, retry, legal notice requirements require DEC-04/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-68 — Bidder authority revoked between view and submit

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-068 / TST-SCN-068 |
| Priority / actor | P0 / authorized dealer administrator and bidder, ROLE-005/ROLE-004 |
| Screen / entity | SCR-017 / Auction |
| Preconditions, trigger and input | A dealer member viewed an auction before their bid permission was revoked. |
| Success | Recheck permission at the authoritative bid submission and reject subsequent action. |
| Failure and recovery | Do not rely on cached session grants; keep earlier valid records for policy review. |
| Supporting operation IDs | getAuctionSnapshot, submitBid, readBidCommand, closeAuction, transitionAuction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Revocation propagation and existing bids require DEC-04. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-69 — Search public vehicles

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-069 / TST-SCN-069 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-030 / VehicleListing |
| Preconditions, trigger and input | Published consumer inventory exists and user submits a text or basic attribute query. |
| Success | Return authorized published matching vehicles with price/currency and availability state. |
| Failure and recovery | Empty or backend error is clearly distinguished; no dealer-only auction records appear. |
| Supporting operation IDs | listConsumerListings, readVehicleListing, transitionVehicleListing |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Publication and availability policy require product approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-70 — Apply complex vehicle filters

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-070 / TST-SCN-070 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-030 / VehicleListing |
| Preconditions, trigger and input | Buyer selects multiple compatible model, region, price and year filters. |
| Success | Return intersection of published results, applied filters and understandable counts. |
| Failure and recovery | Invalid range gets field error; no contradictory or private inventory leaks. |
| Supporting operation IDs | listConsumerListings, readVehicleListing, transitionVehicleListing |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Search freshness, permitted filters and accessibility require approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-71 — Search returns no matches

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-071 / TST-SCN-071 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-030 / VehicleListing |
| Preconditions, trigger and input | A valid set of filters has zero published results. |
| Success | Show no-results state and allow removal of individual filters or saved-search opt-in. |
| Failure and recovery | Do not label provider outage as zero results; do not fabricate inventory. |
| Supporting operation IDs | listConsumerListings, readVehicleListing, transitionVehicleListing |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Saved-search marketing consent requires DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-72 — View published vehicle detail

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-072 / TST-SCN-072 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-030 / VehicleListing |
| Preconditions, trigger and input | Buyer opens a currently published consumer vehicle. |
| Success | Show accurate vehicle attributes, authorized inspection summary, price, currency, availability and known limitations. |
| Failure and recovery | Unavailable or stale details show status and contact path; omit private seller information. |
| Supporting operation IDs | listConsumerListings, readVehicleListing, transitionVehicleListing |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Required claims, guarantees and tax display require DEC-01/DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-73 — Save vehicle

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-073 / TST-SCN-073 |
| Priority / actor | P1 / authenticated consumer buyer, ROLE-003 |
| Screen / entity | SCR-030 / VehicleListing |
| Preconditions, trigger and input | A visible vehicle listing is accessible and buyer selects save. |
| Success | Add vehicle once to buyer's saved list and show confirmation. |
| Failure and recovery | Repeated save is idempotent; removed listing displays unavailable rather than leaking private data. |
| Supporting operation IDs | setSavedVehicle, listSavedVehicles |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Typed request and authorized status contracts exist. Processor/external fulfillment remains an assigned review workflow and must not be marked complete before evidence. |
| Policy dependency | Retention and notification preference require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-74 — Request a vehicle purchase

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-074 / TST-SCN-074 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-031 / PurchaseRequest |
| Preconditions, trigger and input | Vehicle is published and buyer submits verified or policy-required contact details. |
| Success | Create inquiry with listing version, contact consent and advisor assignment. |
| Failure and recovery | If listing becomes unavailable preserve inquiry and communicate status; no implied reservation. |
| Supporting operation IDs | createPurchaseRequest, readPurchaseRequest, transitionPurchaseRequest |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Reservation and purchase commitment require legal policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-75 — Submit purchase application

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-075 / TST-SCN-075 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-031 / PurchaseRequest |
| Preconditions, trigger and input | Buyer elects to proceed with disclosed application and supplies required information. |
| Success | Validate required fields and create application pending authorized review. |
| Failure and recovery | Missing or invalid data retains draft with field errors; avoid collecting unrelated financial evidence. |
| Supporting operation IDs | createPurchaseRequest, readPurchaseRequest, transitionPurchaseRequest |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Required identity and application legal effect require DEC-01/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-76 — Financing approved by provider

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-076 / TST-SCN-076 |
| Priority / actor | P0 / consumer buyer and lender, ROLE-003 plus scoped provider |
| Screen / entity | SCR-033 / FinancingApplication |
| Preconditions, trigger and input | Buyer consented and external lender returns an authenticated approval with terms and expiry. |
| Success | Record provider decision and display its actual conditions, without asserting disbursement. |
| Failure and recovery | If approval is incomplete or unverifiable remain pending and query provider; no self-approval by UI. |
| Supporting operation IDs | readFinancingApplication, createFinancingApplication, transitionFinancingApplication, ingestProviderEvent |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Lender agreement, disclosures and expiry require DEC-10. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-77 — Financing rejected by provider

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-077 / TST-SCN-077 |
| Priority / actor | P0 / consumer buyer and lender, ROLE-003 plus scoped provider |
| Screen / entity | SCR-033 / FinancingApplication |
| Preconditions, trigger and input | Provider returns verified declined decision for a consented application. |
| Success | Record declined state and display authorized provider-supplied reason or next steps. |
| Failure and recovery | Do not infer protected-attribute reason; restrict credit evidence and support an alternative path. |
| Supporting operation IDs | readFinancingApplication, createFinancingApplication, transitionFinancingApplication, ingestProviderEvent |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Adverse-decision notices and appeal require DEC-01/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-78 — Financing offer expires

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-078 / TST-SCN-078 |
| Priority / actor | P0 / consumer buyer and lender, ROLE-003 plus scoped provider |
| Screen / entity | SCR-033 / FinancingApplication |
| Preconditions, trigger and input | Previously approved financing exceeds provider's actual validity period. |
| Success | Display expired status and disable use of the expired approval; offer authorized renewal route. |
| Failure and recovery | Do not imply an extension or issue a new credit decision without provider confirmation. |
| Supporting operation IDs | readFinancingApplication, createFinancingApplication, transitionFinancingApplication, ingestProviderEvent |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Expiry, consent and reapplication rules require lender agreement. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-79 — Review proposed purchase contract

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-079 / TST-SCN-079 |
| Priority / actor | P0 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-026 / Contract |
| Preconditions, trigger and input | An authorized buyer receives a reviewed contract version for the transaction. |
| Success | Show parties, price, conditions and version, and allow approval or objection as terms permit. |
| Failure and recovery | Missing or modified documents trigger review; a click does not guarantee legally sufficient signature. |
| Supporting operation IDs | readContract, transitionContract, recordSignatureEvidence |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Signature, disclosure and cancellation require DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-80 — Request vehicle delivery

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-080 / TST-SCN-080 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-034 / Delivery |
| Preconditions, trigger and input | Delivery is offered for a completed eligible transaction with disclosed terms. |
| Success | Capture destination and preferred window, request approved carrier quote or scheduling. |
| Failure and recovery | No vehicle is promised delivered until carrier confirms; invalid address gets correction. |
| Supporting operation IDs | createDelivery, readDelivery, transitionDelivery, recordDeliveryHandover |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Fees, insurance and custody transfer require DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-81 — Confirm vehicle delivery

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-081 / TST-SCN-081 |
| Priority / actor | P1 / buyer and assigned carrier, ROLE-003 and scoped partner |
| Screen / entity | SCR-034 / Delivery |
| Preconditions, trigger and input | A delivery is scheduled and carrier presents vehicle and condition evidence. |
| Success | Record authorized proof of handover and condition, with timestamp and participant. |
| Failure and recovery | If recipient disputes condition, preserve evidence and open case instead of unconditional clean acceptance. |
| Supporting operation IDs | createDelivery, readDelivery, transitionDelivery, recordDeliveryHandover |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Legal title, delivery evidence and dispute rights require DEC-05/DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-82 — Make inspection warranty claim

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-082 / TST-SCN-082 |
| Priority / actor | P0 / buyer and support, ROLE-003/ROLE-011 |
| Screen / entity | SCR-035 / WarrantyClaim |
| Preconditions, trigger and input | An approved warranty exists and buyer reports a potentially covered issue with evidence. |
| Success | Open claim, check applicable policy/version and assign independent review. |
| Failure and recovery | If no approved coverage exists explain support options without promising remedy; missing evidence triggers request. |
| Supporting operation IDs | createWarrantyClaim, readWarrantyClaim, transitionWarrantyClaim |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Coverage, exclusions, claim window and remedy require DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-83 — Buyer cancels sourcing request

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-083 / TST-SCN-083 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-031 / PurchaseRequest |
| Preconditions, trigger and input | A pending custom sourcing request has no completed binding purchase. |
| Success | Record cancellation, stop new candidate proposals where possible and notify assigned advisor. |
| Failure and recovery | Retain required contractual evidence and handle any fees only under approved terms. |
| Supporting operation IDs | actOnProcurement, readProcurement |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Typed request and authorized status contracts exist. Processor/external fulfillment remains an assigned review workflow and must not be marked complete before evidence. |
| Policy dependency | Cancellation rights, retention and partner notifications require DEC-05/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-84 — Saved vehicle is sold

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-084 / TST-SCN-084 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-030 / VehicleListing |
| Preconditions, trigger and input | A saved published vehicle becomes unavailable. |
| Success | Mark saved item unavailable and notify only under authorized preference. |
| Failure and recovery | Do not silently remove important history or send marketing contrary to opt-out. |
| Supporting operation IDs | listSavedVehicles, readVehicleListing |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Typed request and authorized status contracts exist. Processor/external fulfillment remains an assigned review workflow and must not be marked complete before evidence. |
| Policy dependency | Notification purpose and retention require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-85 — Buyer reports inaccurate vehicle listing

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-085 / TST-SCN-085 |
| Priority / actor | P1 / consumer buyer and inventory reviewer, ROLE-003 plus scoped inventory role |
| Screen / entity | SCR-030 / VehicleListing |
| Preconditions, trigger and input | Buyer flags inconsistent mileage, price or photo in a published listing. |
| Success | Open review, preserve listing version and correct or unpublish if necessary. |
| Failure and recovery | Do not rewrite historic inquiry terms or ignore material safety issue. |
| Supporting operation IDs | listConsumerListings, readVehicleListing, transitionVehicleListing |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Correction, claims and disclosure require DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-86 — Buyer changes purchase contact details

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-086 / TST-SCN-086 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-031 / PurchaseRequest |
| Preconditions, trigger and input | Authenticated buyer edits contact information on an open inquiry. |
| Success | Verify updated address or number if needed and record the change with effective time. |
| Failure and recovery | Never use unverified details for security-critical notifications; retain prior record as required. |
| Supporting operation IDs | createPrivacyRequest, readPrivacyRequest |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Typed request and authorized status contracts exist. Processor/external fulfillment remains an assigned review workflow and must not be marked complete before evidence. |
| Policy dependency | Verification and retention require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-87 — Buyer receives financing estimate not approval

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-087 / TST-SCN-087 |
| Priority / actor | P1 / consumer buyer, ROLE-003 |
| Screen / entity | SCR-033 / FinancingApplication |
| Preconditions, trigger and input | Buyer enters optional budget and terms into a financing calculator. |
| Success | Show clearly labeled indicative amount, assumptions, currency and lender-decision caveat. |
| Failure and recovery | Invalid term or rate is rejected; do not imply a guaranteed loan or personalized approved offer. |
| Supporting operation IDs | readFinancingApplication, createFinancingApplication, transitionFinancingApplication, ingestProviderEvent |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Rate source, disclosures and eligibility require DEC-01/DEC-10. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-88 — Consumer inquiry assigned to unavailable advisor

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-088 / TST-SCN-088 |
| Priority / actor | P1 / CRM coordinator, ROLE-011 |
| Screen / entity | SCR-031 / PurchaseRequest |
| Preconditions, trigger and input | An advisor assigned to an open inquiry becomes unavailable. |
| Success | Reassign to an authorized available advisor and preserve history and customer continuity. |
| Failure and recovery | No unrestricted reassignment across data scopes; unresolved capacity appears in queue. |
| Supporting operation IDs | createPurchaseRequest, readPurchaseRequest, transitionPurchaseRequest |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Assignment and response-time targets require operations approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-89 — Prevent branch overbooking

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-089 / TST-SCN-089 |
| Priority / actor | P0 / branch coordinator, ROLE-006 |
| Screen / entity | SCR-005 / Appointment |
| Preconditions, trigger and input | Two agents or customer and agent attempt capacity beyond the same slot limit. |
| Success | Authorize at most configured number of reservations and give remaining actor a conflict. |
| Failure and recovery | No conflicting confirmation is issued; reconciliation detects external/manual bookings. |
| Supporting operation IDs | createAppointment, readAppointment, transitionAppointment |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Capacity override and external booking policy require operations approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-90 — Assigned inspector unavailable

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-090 / TST-SCN-090 |
| Priority / actor | P1 / branch coordinator and supervisor, ROLE-006/ROLE-008 |
| Screen / entity | SCR-005 / Appointment |
| Preconditions, trigger and input | An inspector is absent for a scheduled inspection. |
| Success | Reassign to another authorized qualified inspector or reschedule and notify customer. |
| Failure and recovery | Do not let unqualified staff publish findings or silently mark inspection complete. |
| Supporting operation IDs | createAppointment, readAppointment, transitionAppointment |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Qualification and staffing fallback require DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-91 — Supervisor rejects inspection

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-091 / TST-SCN-091 |
| Priority / actor | P0 / inspection supervisor, ROLE-008 |
| Screen / entity | SCR-022 / Inspection |
| Preconditions, trigger and input | A submitted report lacks evidence, has inconsistency or fails checklist review. |
| Success | Return report to draft with precise reason and assign correction to inspector. |
| Failure and recovery | Do not publish rejected version or erase previous published report. |
| Supporting operation IDs | readInspection, createInspectionRevision, transitionInspection, publishInspection |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Review criteria and correction timelines require DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-92 — Inspection document upload fails

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-092 / TST-SCN-092 |
| Priority / actor | P1 / assigned inspector, ROLE-007 |
| Screen / entity | SCR-022 / File |
| Preconditions, trigger and input | Inspector uploads permitted evidence but network or storage fails. |
| Success | Keep finding pending, retain safe local draft if approved and offer retry. |
| Failure and recovery | Do not mark evidence uploaded without server confirmation; reject unsafe file and surface reason. |
| Supporting operation IDs | createUploadGrant, readFileStatus, createDownloadGrant |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | File handling, offline storage and retention require security approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-93 — Analyst overrides valuation

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-093 / TST-SCN-093 |
| Priority / actor | P0 / pricing analyst and reviewer, ROLE-009 plus independent reviewer |
| Screen / entity | SCR-024 / Valuation |
| Preconditions, trigger and input | Comparable-based range is insufficient or analyst identifies documented exceptional condition. |
| Success | Record original and proposed value, rationale, evidence, actor and reviewer if required. |
| Failure and recovery | Insufficient authority leaves valuation pending; never overwrite history or present override as guaranteed offer. |
| Supporting operation IDs | createValuation, readValuation, transitionValuation |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Override thresholds and approval requirement require pricing policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-94 — Inventory state conflicts with transaction

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-094 / TST-SCN-094 |
| Priority / actor | P1 / inventory operator, scoped inventory role |
| Screen / entity | SCR-030 / VehicleListing |
| Preconditions, trigger and input | An already sold or withdrawn vehicle is still shown as publicly available. |
| Success | Unpublish or mark unavailable based on authoritative transaction evidence; open reconciliation task. |
| Failure and recovery | Do not silently change the historical listing or expose private auction state. |
| Supporting operation IDs | listConsumerListings, readVehicleListing, transitionVehicleListing |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Inventory ownership and publication permissions require policy. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-95 — Revise issued contract

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-095 / TST-SCN-095 |
| Priority / actor | P0 / legal operator, ROLE-012 |
| Screen / entity | SCR-026 / Contract |
| Preconditions, trigger and input | An issued agreement requires a material change after participant feedback. |
| Success | Create reviewed version and request applicable party acknowledgements, retaining previous version. |
| Failure and recovery | Do not overwrite signed version or assume old signatures bind new text. |
| Supporting operation IDs | readContract, transitionContract, recordSignatureEvidence |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Amendment workflow and legal effect require DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-96 — Payment provider unavailable

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-096 / TST-SCN-096 |
| Priority / actor | P0 / finance preparer and integration owner, ROLE-013 and service role |
| Screen / entity | SCR-043 / Integration |
| Preconditions, trigger and input | An approved provider request or status lookup fails or times out. |
| Success | Mark pending and query original correlation reference after recovery before retrying. |
| Failure and recovery | No duplicate payment, refund or claim of settlement is allowed; create finance exception if unresolved. |
| Supporting operation IDs | ingestProviderEvent, readPaymentObligation |
| Delivery mode | provider_activation_dependency |
| Boundary and procedure | Adapter retains intent and correlation, marks unknown, queries contracted provider status before retry. Internal normalized inbox is specified; external provider protocol is selected and tested during onboarding. |
| Policy dependency | Provider SLA, retry and manual fallback require DEC-03. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-97 — Partial settlement received

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-097 / TST-SCN-097 |
| Priority / actor | P0 / finance preparer, ROLE-013 |
| Screen / entity | SCR-043 / PaymentObligation |
| Preconditions, trigger and input | Authoritative evidence confirms less than the obligation in the same currency. |
| Success | Record unique verified partial amount and remaining balance; retain transaction pending. |
| Failure and recovery | Duplicate notification cannot count twice; mismatch or overpayment creates separate review. |
| Supporting operation IDs | readPaymentObligation, submitPaymentEvidence, prepareReconciliation, approveReconciliation, transitionPaymentObligation |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Partial payments, refund and rounding require DEC-03. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-98 — Escalate financial discrepancy

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-098 / TST-SCN-098 |
| Priority / actor | P0 / finance approver, ROLE-014 |
| Screen / entity | SCR-043 / PaymentObligation |
| Preconditions, trigger and input | A prepared reconciliation has unresolved amount, payee or document discrepancy. |
| Success | Reject reconciliation, assign investigation and record reason with evidence. |
| Failure and recovery | Do not approve own sensitive preparation or close ordinary transaction with material mismatch. |
| Supporting operation IDs | readPaymentObligation, submitPaymentEvidence, prepareReconciliation, approveReconciliation, transitionPaymentObligation |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Approver separation and dispute escalation require DEC-03. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-99 — Delivery attempt fails

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-099 / TST-SCN-099 |
| Priority / actor | P1 / assigned carrier and logistics operator, scoped partner/logistics role |
| Screen / entity | SCR-034 / Delivery |
| Preconditions, trigger and input | Carrier cannot deliver because recipient unavailable or location inaccessible. |
| Success | Record failed attempt, vehicle custody and condition; contact recipient for approved rescheduling. |
| Failure and recovery | Do not mark delivered or abandon vehicle; escalate security or storage concern. |
| Supporting operation IDs | createDelivery, readDelivery, transitionDelivery, recordDeliveryHandover |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Retry, custody, fees and liability require DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-100 — Escalate customer complaint

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-100 / TST-SCN-100 |
| Priority / actor | P1 / support agent, ROLE-011 |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | Customer reports unresolved issue exceeding an approved escalation threshold or involving material harm. |
| Success | Create or elevate case, preserve communications and assign accountable specialist. |
| Failure and recovery | Do not promise remedy beyond authority or expose another party's confidential data. |
| Supporting operation IDs | createSupportTicket, readSupportTicket, transitionSupportTicket |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Severity levels, SLA and appeals require operations/legal approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-101 — Investigate duplicate customer identity

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-101 / TST-SCN-101 |
| Priority / actor | P1 / CRM reviewer, ROLE-011 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | Two customer records share identifiers or disputed contact information. |
| Success | Review evidence under limited access and link or merge only with authorized audit. |
| Failure and recovery | If identity uncertain keep records separate; never reveal one person's data to another. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | Privacy/IAM specialist reviews identity evidence in a restricted case, links records with provenance and access review. Destructive identity merge is disabled until a separately approved reversible merge specification exists. |
| Policy dependency | Merge authority, matching threshold and retention require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-102 — Suspend dealer account

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-102 / TST-SCN-102 |
| Priority / actor | P0 / dealer risk reviewer, scoped risk role |
| Screen / entity | SCR-015 / DealerVerification |
| Preconditions, trigger and input | Documented eligibility breach or verified fraud concern meets approved suspension criteria. |
| Success | Record reason, effective time and reviewer; block new access and bids according to policy. |
| Failure and recovery | Previously accepted bids are preserved and reviewed under approved terms; provide appeal when required. |
| Supporting operation IDs | readDealerVerification, transitionDealerVerification |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Suspension, ongoing bids and notices require DEC-04/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-103 — Administrator attempts unauthorized change

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-103 / TST-SCN-103 |
| Priority / actor | P0 / platform administrator, ROLE-016 |
| Screen / entity | SCR-028 / Authorization |
| Preconditions, trigger and input | Admin without approved domain permission requests financial adjustment or role escalation. |
| Success | Deny action, record attempted privileged operation and require approved access workflow. |
| Failure and recovery | Admin status does not bypass finance/legal separation; sensitive details stay masked. |
| Supporting operation IDs | readPolicyRecord, createPolicyVersion |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Emergency access and dual control require security approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-104 — Audit investigation

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-104 / TST-SCN-104 |
| Priority / actor | P0 / security or compliance investigator, explicitly granted role |
| Screen / entity | SCR-040 / AuditAndRecovery |
| Preconditions, trigger and input | Authorized incident review requires actor, policy and record history for a case. |
| Success | Retrieve scoped immutable event trail and document evidence access and investigation purpose. |
| Failure and recovery | If log gap or tampering suspected preserve evidence and escalate; avoid unnecessary exports. |
| Supporting operation IDs | Governed operational procedure; no public mutation endpoint |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | Security auditor uses restricted audit tooling under a purpose-bound grant, records query scope and evidence checksum, and obtains independent approval for export. Metrics API is not an audit-log API. |
| Policy dependency | Audit retention and investigator authority require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-105 — Disaster recovery restoration

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-105 / TST-SCN-105 |
| Priority / actor | P0 / SRE incident commander with domain owners, scoped recovery roles |
| Screen / entity | SCR-040 / AuditAndRecovery |
| Preconditions, trigger and input | A declared disaster makes the primary service unavailable and approved backups exist. |
| Success | Restore isolated environment, verify integrity, reconcile critical auction and finance records before reopening. |
| Failure and recovery | If recovery point lacks confirmed data, keep affected transactions on hold and open cases. |
| Supporting operation IDs | Governed operational procedure; no public mutation endpoint |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | SRE follows RB-01 and isolated restore procedure; verifies critical receipt, object and finance manifests; domain owners authorize reopening with measured recovery evidence. |
| Policy dependency | RPO/RTO and business resumption authority require SRE and domain approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-106 — Customer document fails malware scan

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-106 / TST-SCN-106 |
| Priority / actor | P0 / assigned staff, scoped upload role |
| Screen / entity | SCR-022 / File |
| Preconditions, trigger and input | A customer or staff member submits an attachment for a case. |
| Success | Quarantine unsafe or unscannable file, deny download and notify uploader to resubmit safely. |
| Failure and recovery | Do not expose raw malware or mark evidence accepted; keep case in required-evidence state. |
| Supporting operation IDs | createUploadGrant, readFileStatus, createDownloadGrant |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | File types, retention and malware response require security approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-107 — Vehicle identifier conflict

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-107 / TST-SCN-107 |
| Priority / actor | P0 / branch coordinator, ROLE-006 |
| Screen / entity | SCR-007 / SellerLead |
| Preconditions, trigger and input | Vehicle identifier supplied at intake differs from physical or registration evidence. |
| Success | Put case on hold, preserve both values and assign verification review. |
| Failure and recovery | Do not automatically rewrite an approved report or publish an uncertain vehicle. |
| Supporting operation IDs | readSellerLead, createSellerLead, transitionSellerLead |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Acceptable identifiers and correction authority require DEC-05/DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-108 — Checklist template changes mid-inspection

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-108 / TST-SCN-108 |
| Priority / actor | P0 / inspector and supervisor, ROLE-007/ROLE-008 |
| Screen / entity | SCR-022 / Inspection |
| Preconditions, trigger and input | An inspection started under a template that is superseded before completion. |
| Success | Keep the started report tied to its immutable template version; supervisor applies approved migration decision. |
| Failure and recovery | Do not silently introduce missing checks or change past scoring; create explicit review if new standard is mandatory. |
| Supporting operation IDs | readInspection, createInspectionRevision, transitionInspection, publishInspection |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Template effective dates and migration require DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-109 — Required inspection photograph missing

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-109 / TST-SCN-109 |
| Priority / actor | P0 / assigned inspector, ROLE-007 |
| Screen / entity | SCR-022 / Inspection |
| Preconditions, trigger and input | A checklist requires a photo and the inspector attempts submission without it. |
| Success | Show missing-evidence error or permitted unknown-reason route and retain entered findings. |
| Failure and recovery | Do not publish report if mandatory proof is absent; upload failure creates recovery task. |
| Supporting operation IDs | readInspection, createInspectionRevision, transitionInspection, publishInspection |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Mandatory images and exceptions require DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-110 — Valuation has stale comparable data

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-110 / TST-SCN-110 |
| Priority / actor | P1 / pricing analyst, ROLE-009 |
| Screen / entity | SCR-024 / Valuation |
| Preconditions, trigger and input | Available market comparables exceed approved freshness threshold or sample is insufficient. |
| Success | Display data age and abstain or route to analyst review; record method version. |
| Failure and recovery | Do not create a precise estimate from insufficient evidence; no automatic auction reserve. |
| Supporting operation IDs | createValuation, readValuation, transitionValuation |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Freshness, sample threshold and disclosure require pricing approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-111 — Notification sent to wrong channel

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-111 / TST-SCN-111 |
| Priority / actor | P1 / support and privacy reviewer, ROLE-011 and privacy role |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | A notification attempt is routed to a stale, invalid or unauthorized contact channel. |
| Success | Stop subsequent sends, record delivery status and verify preferred contact through approved process. |
| Failure and recovery | Escalate possible disclosure and do not repeat sensitive content through another unverified address. |
| Supporting operation IDs | createSupportTicket, readSupportTicket, transitionSupportTicket |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | ROLE-023/011 halts affected sends, verifies recipient/channel and preference, assesses exposure, records response and independently approves any resend; do not repeat the wrong message automatically. |
| Policy dependency | Incident reporting and contact verification require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-112 — Contract signer authority revoked

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-112 / TST-SCN-112 |
| Priority / actor | P0 / legal operator, ROLE-012 |
| Screen / entity | SCR-026 / Contract |
| Preconditions, trigger and input | An organization member loses authority while an agreement is awaiting signature. |
| Success | Pause signature request and verify authorized replacement; retain version and prior audit. |
| Failure and recovery | Do not accept a later signature solely because an old link exists. |
| Supporting operation IDs | readContract, transitionContract, recordSignatureEvidence |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Signature validity and delegation require DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-113 — Payment evidence arrives twice

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-113 / TST-SCN-113 |
| Priority / actor | P0 / finance preparer, ROLE-013 |
| Screen / entity | SCR-043 / PaymentObligation |
| Preconditions, trigger and input | Provider repeats a notification with the same authenticated transaction reference. |
| Success | Associate evidence once to its obligation and acknowledge duplicate safely. |
| Failure and recovery | A changed amount under the same reference enters discrepancy review; no double counting. |
| Supporting operation IDs | readPaymentObligation, submitPaymentEvidence, prepareReconciliation, approveReconciliation, transitionPaymentObligation |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Provider identity and idempotency retention require DEC-03. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-114 — Refund or adjustment requested

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-114 / TST-SCN-114 |
| Priority / actor | P0 / finance preparer and approver, ROLE-013/ROLE-014 |
| Screen / entity | SCR-043 / PaymentObligation |
| Preconditions, trigger and input | An eligible contract and approved remedy give rise to a documented refund request. |
| Success | Record request, independent approval and provider status as separate facts. |
| Failure and recovery | Insufficient authority or missing supporting evidence blocks action; no funds are moved by a mere record. |
| Supporting operation IDs | readPaymentObligation, submitPaymentEvidence, prepareReconciliation, approveReconciliation, transitionPaymentObligation |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | Finance preparer records remedy request and evidence, independent finance approver confirms allowable amount/basis, approved external counterparty executes if applicable; match external result before closure. |
| Policy dependency | Refund eligibility, provider authorization and tax effects require DEC-03/DEC-05. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-115 — Close case with open support dispute

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-115 / TST-SCN-115 |
| Priority / actor | P0 / operations closer and support, scoped operations role |
| Screen / entity | SCR-026 / Transaction |
| Preconditions, trigger and input | All ordinary closure evidence exists but a material support dispute remains open. |
| Success | Keep normal closure blocked and assign dispute owner; show customer-safe pending status. |
| Failure and recovery | Any exception must be expressly permitted and separately approved with reason. |
| Supporting operation IDs | readTransaction, closeTransaction |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Definition of material dispute and exception authority require DEC-05/DEC-06. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-116 — Third-party identity check returns uncertain

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-116 / TST-SCN-116 |
| Priority / actor | P0 / identity-review specialist, explicitly granted role |
| Screen / entity | SCR-015 / DealerVerification |
| Preconditions, trigger and input | A provider returns inconclusive rather than pass or fail on a consented check. |
| Success | Record pending review and request appropriate additional evidence through secure channel. |
| Failure and recovery | Do not convert uncertainty to verified or deny permanently without approved review/appeal. |
| Supporting operation IDs | readDealerVerification, transitionDealerVerification |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Identity provider, alternatives and retention require DEC-01/DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-117 — Sensitive export requested

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-117 / TST-SCN-117 |
| Priority / actor | P0 / authorized analyst and reviewer, ROLE-017 plus designated approver |
| Screen / entity | SCR-040 / AuditAndRecovery |
| Preconditions, trigger and input | A business user requests identifiable data export for a documented purpose. |
| Success | Verify purpose, scope and approval, minimize fields, log access and deliver via protected channel. |
| Failure and recovery | Deny overbroad or expired request; no public link or unrestricted bulk download. |
| Supporting operation IDs | requestExport, readExportJob, downloadExport |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Typed request and authorized status contracts exist. Processor/external fulfillment remains an assigned review workflow and must not be marked complete before evidence. |
| Policy dependency | Permitted fields, retention and approval require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-118 — Reconcile missed event after outage

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-118 / TST-SCN-118 |
| Priority / actor | P0 / domain operator and SRE, scoped operations roles |
| Screen / entity | SCR-040 / AuditAndRecovery |
| Preconditions, trigger and input | An event delivery is missing or duplicated after an outage while authoritative record exists. |
| Success | Compare authoritative state with projections and replay using original event identity. |
| Failure and recovery | Avoid duplicate bid, notification, payment or transfer effect; unmatched discrepancies stay assigned. |
| Supporting operation IDs | Governed operational procedure; no public mutation endpoint |
| Delivery mode | governed_manual_workflow |
| Boundary and procedure | Worker owner compares source/outbox/inbox sequences, obtains scoped replay authority and replays original event IDs; consumers deduplicate and no provider financial action is repeated automatically. |
| Policy dependency | Replay authorization and event retention require architecture approval. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-119 — Expired privileged session attempts change

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-119 / TST-SCN-119 |
| Priority / actor | P0 / administrator, ROLE-016 |
| Screen / entity | SCR-038 / Authentication |
| Preconditions, trigger and input | A previously approved elevated access window has expired before a policy change request. |
| Success | Deny change and require new time-limited, reviewed elevation and step-up. |
| Failure and recovery | No hidden extension or cached privilege permits the action; record denial. |
| Supporting operation IDs | createSession, completeAuthChallenge, requestAccountRecovery, createStepUpChallenge, completeStepUp |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Supporting staff operations do not confer permissions on the customer; use only the action authorized by the state catalog. |
| Policy dependency | Elevation duration and approval require security governance. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

## SCN-120 — Customer requests correction of personal data

| Contract item | Specification |
|---|---|
| Requirement / test | FR-SCN-120 / TST-SCN-120 |
| Priority / actor | P0 / verified data subject and privacy officer, ROLE-002/ROLE-003 plus privacy role |
| Screen / entity | SCR-027 / SupportTicket |
| Preconditions, trigger and input | A subject identifies inaccurate personal information held in an open or closed case. |
| Success | Verify identity, review correction and update permitted current records while retaining legally required historical evidence. |
| Failure and recovery | Conflicting or fraudulent request remains under review; do not overwrite immutable transaction evidence. |
| Supporting operation IDs | createPrivacyRequest, readPrivacyRequest |
| Delivery mode | proposed_contract_mapping |
| Boundary and procedure | Typed request and authorized status contracts exist. Processor/external fulfillment remains an assigned review workflow and must not be marked complete before evidence. |
| Policy dependency | Correction rights, retention and response deadlines require DEC-07. |
| Audit | workflow.audit.v1: actor, scope, object/version, key, result, policy, reason, UTC; restricted; no raw documents |
| Analytics | workflow_outcome_recorded v1, scenario_id and outcome; purpose-gated after authoritative outcome |

