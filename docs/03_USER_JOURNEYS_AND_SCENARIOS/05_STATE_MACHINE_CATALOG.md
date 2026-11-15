# State machine catalog

**ID:** 03/05_STATE_MACHINE_CATALOG · **Version:** 0.3 · **Status:** PROPOSED · **Owner:** Domain architecture · **Reviewers:** Operations, QA, security, legal · **Updated:** 2026-11-15

## Normative transition rules

This catalog defines application states; business approvals remain DEC-01–07. All unlisted transitions are prohibited. A row listing multiple sources applies identically to each listed source. `SYSTEM-*` means a narrowly scoped service principal, never an anonymous client. Human roles resolve in the role catalog. The same actor must not prepare and approve the same inspection, verification, reconciliation, remedy payment or privileged configuration. Scope is case ownership for customers, active organization plus auction eligibility for dealers, and assigned branch/case for staff. Authentication alone grants nothing.

Every successful transition atomically increments aggregate version, writes an append-only audit record and a transactional outbox event. Event convention: `lifecycle.transition_recorded` v1 with aggregate type/ID, transition ID, prior/new state and version; no private document contents. A named domain event in a row is emitted in addition, with the same causation ID. Idempotency scope is principal + operation + key; replays recheck current authorization before returning a redacted original result. A key/payload conflict is 409; failed If-Match is 412; invalid business transition is 409; unauthorized is 403/opaque 404. Reject without mutating aggregate. A retryable transport error keeps outcome unknown and reuses the key; a changed intent uses a new key. No external call occurs inside a state transaction.

Every row defines acceptance test `SM-TST-<transition-id>`: prepare each permitted source and authorized actor; satisfy named guard, invoke twice with same key and assert one destination, version increment, audit and event; negate each guard and assert no state write; test unrelated organization, stale ETag and concurrent command. Specific external-effect recovery follows the row, with bounded retries and an assigned exception after exhaustion. Terminal states have no outgoing transition; completed but revisitable states permit only explicitly listed correction/reopen/reversal actions and preserve the earlier fact. Inspection correction creates a new draft revision, never changes the published object's state in place. BidCommand is separate from immutable accepted Bid.

## SM-01 — SellerLead

Owner: Acquisition. Initial state: `draft`. Terminal states: closed, cancelled, rejected. Completed but explicitly revisitable: none.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-01-01 | draft → submit → submitted | ROLE-002 | Verified contact, supported taxonomy, service notice acknowledged | Freeze intake revision; enqueue qualification |
| SM-01-02 | submitted,review → qualify → eligible | ROLE-011 | Authority and eligibility evidence checked under pinned policy | Record reviewer and eligibility reasons |
| SM-01-03 | submitted,eligible → request-review → review | ROLE-011 | Duplicate or authority conflict documented | Prevent booking/publication until resolved |
| SM-01-04 | eligible → start-case → in_progress | ROLE-006 | Confirmed appointment and verified seller scope | Link appointment and inspection work to the SellerLead; create no TransactionCase before offer acceptance |
| SM-01-05 | submitted,review → reject → rejected | ROLE-011 | Reason and support route supplied | Notify owner without exposing duplicate identities |
| SM-01-06 | draft,submitted,review,eligible → cancel → cancelled | ROLE-002 | Own case and no live binding obligation | Release future booking through idempotent scheduling command |
| SM-01-07 | in_progress → close → closed | ROLE-006 | Verified transaction outcome or explicit unsuccessful selling outcome with no unresolved obligation | Record outcome, never infer financial success |

## SM-02 — Appointment

Owner: Scheduling. Initial state: `confirmed`. Terminal states: completed, cancelled, no_show. Completed but explicitly revisitable: none.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-02-01 | confirmed → reschedule → confirmed | ROLE-002 | Own case, new slot valid, capacity and notice policy checked | Lock old/new slots in sorted ID order and move reservation atomically |
| SM-02-02 | confirmed → cancel → cancelled | ROLE-002 | Own case and cancellation policy allows action | Release reservation exactly once; create notification intent |
| SM-02-03 | confirmed → check-in → checked_in | ROLE-006 | Assigned branch verifies booking, vehicle and arrival | Record check-in instant and queue position |
| SM-02-04 | confirmed → mark-no-show → no_show | ROLE-006 | Grace interval elapsed in branch calendar, branch was open | Record no-show reason; capacity/history retained |
| SM-02-05 | checked_in → complete → completed | ROLE-006 | Inspection handoff recorded | Complete visit without asserting sale or report approval |

## SM-03 — Inspection

Owner: Inspection. Initial state: `draft`. Terminal states: cancelled. Completed but explicitly revisitable: published.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-03-01 | draft,returned → submit → submitted | ROLE-007 | All required points explicitly answered; unknown and N/A have reasons; clean evidence | Freeze submitted revision and assign independent reviewer |
| SM-03-02 | submitted → return → returned | ROLE-008 | Reviewer differs from author and provides point-level reasons | Create correction task; no published content changes |
| SM-03-03 | submitted → publish → published | ROLE-008 | Mandatory coverage passes template; reviewer independent; clean immutable evidence | Publish revision and emit inspection.report_published |
| SM-03-04 | published → correct → draft | ROLE-008 | Reason, materiality and new revision recorded; existing report retained | Create successor revision; material change sets linked auction safety hold |
| SM-03-05 | draft,returned → cancel → cancelled | ROLE-008 | No active auction relies on draft; reason recorded | Retain audit and prevent publication |

## SM-04 — VehicleListing

Owner: Consumer inventory. Initial state: `draft`. Terminal states: sold, withdrawn. Completed but explicitly revisitable: none.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-04-01 | draft → submit → review | ROLE-021 | Seller authority, rights-cleared media, condition and price fields complete | Freeze publication candidate separate from dealer report |
| SM-04-02 | review → publish → available | ROLE-021 | Publication grant; no active dealer-auction channel conflict | Publish only approved projection and invalidate search |
| SM-04-03 | available → suspend → unavailable | ROLE-021 | Ownership, condition or availability question documented | Remove from active search; preserve buyer inquiries |
| SM-04-04 | unavailable → restore → available | ROLE-021 | Blocking issue resolved and authority still valid | Refresh public revision and searchable availability |
| SM-04-05 | available,unavailable → mark-sold → sold | ROLE-021 | Completed transaction or independently verified external disposition | Display sold status; remove inquiry CTA |
| SM-04-06 | draft,review,available,unavailable → withdraw → withdrawn | ROLE-021 | Authorized owner request or legal reason | Unpublish with lifecycle SEO policy; retain audit |

## SM-05 — Valuation

Owner: Pricing. Initial state: `pending_review`. Terminal states: rejected. Completed but explicitly revisitable: approved.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-05-01 | pending_review → approve → approved | ROLE-009 | Approved source rights, currency-consistent range, sufficient data and independent override reviewer | Pin input/report/rule versions and explanation |
| SM-05-02 | pending_review → reject → rejected | ROLE-009 | Insufficient comparables or invalid inputs with reason | Publish abstention, never fabricate zero price |
| SM-05-03 | approved → revise → pending_review | ROLE-009 | New report/comparables or override reason; retain earlier valuation | Create successor valuation revision; active auctions unchanged |

## SM-06 — Auction

Owner: Auction. Initial state: `draft`. Terminal states: closed, cancelled. Completed but explicitly revisitable: none.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-06-01 | draft → schedule → scheduled | ROLE-010 | Published report, seller authority, approved pinned rules, valid time interval, exclusive vehicle channel | Freeze schedule/rules/report snapshot and audience |
| SM-06-02 | scheduled → open → open | SYSTEM-AUCTION | Trusted DB time reaches starts_at; report, vehicle and policy still valid | Emit auction.opened after commit |
| SM-06-03 | open → pause → paused | ROLE-010 | Material safety issue or incident; recorded reason and case | Reject new bids, preserve deadline and bid history |
| SM-06-04 | paused → resume → open | ROLE-010 | Safety issue resolved, prepublished policy allows resume and original deadline not passed | Record review, never reset or extend deadline silently |
| SM-06-05 | open,paused → close → closed | SYSTEM-AUCTION | DB time reaches deadline; same auction lock; paused/uncertain case yields pending_review result | Insert unique result and auction.closed atomically |
| SM-06-06 | draft,scheduled,open,paused → cancel → cancelled | ROLE-010 | Authorized reason and approvals per pinned policy | Preserve all bids, cancel without automatic financial penalty |

## SM-07 — BidCommand

Owner: Auction. Initial state: `received`. Terminal states: accepted, rejected. Completed but explicitly revisitable: none.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-07-01 | received → accept → accepted | SYSTEM-AUCTION | Active organization/member/grant, open auction, post-lock DB time before cutoff, correct currency/increment | Append immutable Bid, sequence, receipt, audit and outbox atomically |
| SM-07-02 | received → reject → rejected | SYSTEM-AUCTION | One eligibility, state, deadline or amount guard fails | Persist replayable decision code without changing leader |

## SM-08 — DealerVerification

Owner: Dealer. Initial state: `submitted`. Terminal states: rejected. Completed but explicitly revisitable: none.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-08-01 | submitted → request-evidence → needs_evidence | ROLE-019 | Missing verification item specified | Notify applicant, preserve received evidence |
| SM-08-02 | needs_evidence → resubmit → submitted | ROLE-005 | Authorized organization representative; clean evidence | Version submission and reset review assignment |
| SM-08-03 | submitted → approve → approved | ROLE-019 | Independent reviewer verifies business and representative authority | Activate dealer account; do not grant every member bid authority |
| SM-08-04 | submitted → reject → rejected | ROLE-019 | Evidence-based reason and appeal instructions | Disable auction access, retain decision |
| SM-08-05 | approved → suspend → suspended | ROLE-019 | Risk/contract reason and case; step-up required | Lock same eligibility record used by bidding; revoke active feed subscriptions |
| SM-08-06 | suspended → reinstate → approved | ROLE-019 | Independent risk review clears restriction | Restore eligible access prospectively; retain old decisions |

## SM-09 — PurchaseRequest

Owner: Consumer. Initial state: `submitted`. Terminal states: closed, cancelled. Completed but explicitly revisitable: none.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-09-01 | submitted → assign → assigned | ROLE-011 | Available scoped advisor and authoritative listing check | Set owner and next contact due time |
| SM-09-02 | assigned → qualify → qualified | ROLE-011 | Buyer needs and availability confirmed | Record requirements and next action; no reservation implied |
| SM-09-03 | qualified → coordinate → coordinating | ROLE-011 | Buyer selects vehicle and appropriate contract path | Link transaction case; separate consumer/dealer paths |
| SM-09-04 | submitted,assigned,qualified,coordinating → cancel → cancelled | ROLE-003 | Own request and obligations handled by legal case if necessary | Stop further optional sourcing; retain lawful evidence |
| SM-09-05 | coordinating → close → closed | ROLE-011 | Transaction outcome or explicit unsuccessful disposition recorded | Record closure category; notify buyer |

## SM-10 — FinancingApplication

Owner: Financing. Initial state: `draft`. Terminal states: rejected, expired, withdrawn, funded. Completed but explicitly revisitable: none.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-10-01 | draft → submit → submitted | ROLE-003 | Approved lender, explicit sharing basis and required application fields | Create provider intent, not credit approval |
| SM-10-02 | submitted → approve → approved | SYSTEM-PROVIDER | Authenticated correlated lender decision and current terms | Record exact offer, expiry and disclosures |
| SM-10-03 | submitted → reject → rejected | SYSTEM-PROVIDER | Authenticated correlated lender rejection | Record decision and safe explanation; offer noncredit route |
| SM-10-04 | approved → expire → expired | SYSTEM-FINANCE | Offer expiry passed and no accepted funding contract | Prevent use of stale terms; new application required |
| SM-10-05 | approved → fund → funded | SYSTEM-PROVIDER | Independently matched disbursement evidence and legal conditions | Record external funding, not platform-created money |
| SM-10-06 | draft,submitted,approved → withdraw → withdrawn | ROLE-003 | Applicant request; contracted obligations escalated if already binding | Stop future optional sharing; retain required evidence |

## SM-11 — Contract

Owner: Legal. Initial state: `draft`. Terminal states: voided, superseded. Completed but explicitly revisitable: signed.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-11-01 | draft → review → reviewed | ROLE-012 | Approved jurisdiction template, parties, amounts, fees and title process | Pin reviewed document checksum |
| SM-11-02 | reviewed → issue → issued | ROLE-012 | Required signers and authority verified; exact reviewed version unchanged | Issue signing invitations with expiring authorized access |
| SM-11-03 | issued,partially_signed → record-signature → partially_signed | ROLE-012 | One verified signer on exact document hash; other required signers outstanding | Append signature evidence; never overwrite document |
| SM-11-04 | issued,partially_signed → complete-signatures → signed | ROLE-012 | All required valid signatures refer to same document hash | Emit contract.signed; does not imply settlement |
| SM-11-05 | draft,reviewed,issued,partially_signed → void → voided | ROLE-012 | Approved legal basis and notice obligations recorded | Revoke unsigned invitations; preserve all signatures |
| SM-11-06 | signed → amend → superseded | ROLE-012 | Authorized amendment process and newly executed successor | Retain old agreement linked to replacement |

## SM-12 — PaymentObligation

Owner: Finance. Initial state: `outstanding`. Terminal states: voided. Completed but explicitly revisitable: reconciled.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-12-01 | outstanding,partially_satisfied,disputed → submit-evidence → evidence_pending | ROLE-013 | Clean evidence references known payer/payee, source, amount and currency | Record claimed payment; no transfer or settled flag |
| SM-12-02 | evidence_pending → record-partial → partially_satisfied | ROLE-014 | Independent matching confirms part of exact obligation | Record matched allocation and remaining balance |
| SM-12-03 | evidence_pending → dispute → disputed | ROLE-014 | Mismatch, duplicate allocation or uncertain finality | Assign exception and prohibit closure |
| SM-12-04 | evidence_pending,partially_satisfied → reconcile → reconciled | ROLE-014 | Independent reviewer, exact approved total, authentic source, no unresolved reversal | Record reconciliation and settlement.reconciled |
| SM-12-05 | reconciled → record-reversal → disputed | ROLE-014 | New authenticated reversal evidence | Append compensating fact, reopen financial exception; never erase history |
| SM-12-06 | outstanding → void → voided | ROLE-014 | Underlying obligation legally cancelled; no unhandled payment | Preserve reason and source approval |

## SM-13 — Delivery

Owner: Logistics. Initial state: `scheduled`. Terminal states: delivered, cancelled. Completed but explicitly revisitable: none.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-13-01 | scheduled → assign → assigned | ROLE-020 | Qualified carrier, coverage, window and pickup authority | Share minimal job information with assigned carrier |
| SM-13-02 | assigned → collect → collected | ROLE-018 | Pickup authority, condition, signed proof and custody verified | Append custody event and immutable condition evidence |
| SM-13-03 | collected → dispatch → in_transit | ROLE-020 | Carrier acceptance and destination details validated | Record dispatch and estimated window |
| SM-13-04 | in_transit → deliver → delivered | ROLE-018 | Authorized recipient proof, condition and time recorded | Record physical handover only |
| SM-13-05 | assigned,collected,in_transit → report-exception → exception | ROLE-020 | Delay, damage or failed attempt has evidence and current custodian | Assign claims/dispatch owner; preserve custody |
| SM-13-06 | exception → reschedule → assigned | ROLE-020 | New agreed window and verified custody/insurance | Create new attempt; retain failed attempt |
| SM-13-07 | scheduled,assigned → cancel → cancelled | ROLE-020 | Vehicle not collected and authorized cancellation | Notify participants; no implied fee refund |

## SM-14 — WarrantyClaim

Owner: Claims. Initial state: `received`. Terminal states: closed. Completed but explicitly revisitable: none.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-14-01 | received → request-evidence → needs_evidence | ROLE-022 | Applicable policy/version and missing evidence identified | Record next action and notice; original claim time retained |
| SM-14-02 | received,needs_evidence → review → under_review | ROLE-022 | Required evidence available; independent reviewer assigned | Preserve report, policy and transaction snapshots |
| SM-14-03 | under_review → approve → approved | ROLE-022 | Coverage, liability and proposed remedy supported by approved policy | Create remedy proposal; finance separately authorizes money |
| SM-14-04 | under_review → deny → denied | ROLE-022 | Reason and applicable appeal path supplied | Record reasoned decision without deleting evidence |
| SM-14-05 | approved → complete-remedy → closed | ROLE-022 | Authorized remedy completion independently confirmed | Close with remedy evidence and notification |
| SM-14-06 | denied → appeal → under_review | ROLE-022 | Appeal admissible under policy; independent new reviewer | Create linked review cycle; prior decision remains |
| SM-14-07 | denied → close → closed | ROLE-022 | Applicable appeal handling completed | Record closure and evidence retention policy |

## SM-15 — SupportTicket

Owner: Support. Initial state: `open`. Terminal states: none. Completed but explicitly revisitable: closed.

| ID | Source → action → destination | Authorized actor | Guard | Atomic effect / asynchronous work |
|---|---|---|---|---|
| SM-15-01 | open → assign → assigned | ROLE-011 | Available authorized team member | Set owner and response target |
| SM-15-02 | assigned → investigate → investigating | ROLE-011 | Verified customer and minimum necessary case access | Record evidence request and investigation log |
| SM-15-03 | investigating → wait-customer → awaiting_customer | ROLE-011 | Specific information request and follow-up date | Pause only approved resolution clock; not initial response |
| SM-15-04 | awaiting_customer → resume → investigating | ROLE-011 | Customer evidence received or staff follow-up | Resume clock and preserve waiting interval |
| SM-15-05 | assigned,investigating,awaiting_customer → resolve → resolved | ROLE-011 | Reasoned resolution recorded; domain actions confirmed independently | Notify with appeal/reopen path |
| SM-15-06 | resolved → close → closed | ROLE-011 | Approved confirmation/closure policy satisfied | Record closure, no financial powers inferred |
| SM-15-07 | resolved,closed → reopen → assigned | ROLE-011 | New evidence or permitted customer request | Reopen with owner, preserve prior resolution |

## Policy-specific behavior

No legal time period, warranty or financial penalty is invented here. Required unresolved policy keys prevent live activation but do not prevent synthetic validation of these guards. Optional proxy bidding, extensions, deposits, credit and automatic adverse decisions default off. Paused auctions cannot accept bids and never resume after the original deadline; closure remains a recorded outcome subject to review, not a silent award. See [policy baseline](../POLICY_BASELINE.md) and [machine-readable catalog](../contracts/state-machines.json).

## Terminal-state and revision semantics

A terminal state has no permitted outgoing transition on that lifecycle instance. A completed state may remain correctable through an explicit reviewed action: published inspections, approved valuations, signed contracts, reconciled obligations and closed tickets have the correction, successor, reversal or reopen behavior in their rows. The structured catalog distinguishes `terminal_states` from `completed_but_revisitable_states`. Historical published revisions, signed documents and posted financial facts remain immutable even when an aggregate points to a successor. States without an entry transition are not exposed as selectable statuses. A caller never sets arbitrary status directly.

Seller intake and inspection use the SellerLead as their coordination reference. A dealer TransactionCase is created only by accepted current seller offer; a consumer TransactionCase is created only by the mutually accepted, versioned consumer offer described in the transaction workflow. An appointment does not imply a transaction, a buyer, or a financial obligation.
