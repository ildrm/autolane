# User roles

| Metadata | Value |
|---|---|
| Document ID | 04/01_USER_ROLES |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | User roles; English-first automotive marketplace documentation |

## Role catalog
All grants are **PROPOSED** and require object, organization, branch, purpose and effective-time scope. A role is not proof of a user's authority; identities and assignments must be verified.

| Role ID / actor | Authorized intent | Explicit boundaries |
|---|---|---|
| ROLE-001 Visitor | View public information and initiate allowed requests. | No unpublished inventory, private reports or personal cases. |
| ROLE-002 Seller | Manage own request, appointment and offer decisions. | Cannot act on another seller's case or make dealer bids without a separate grant. |
| ROLE-003 Consumer buyer | Manage own inquiries, favorites and sourcing request. | No access to dealer-only auctions or another buyer's data. |
| ROLE-004 Dealer bidder | View eligible auctions/reports and submit bids for approved organization. | Must have active organization and explicit bid authority; no unscoped user or organization access. |
| ROLE-005 Dealer administrator | Manage permitted organization members and view its activity. | Cannot grant self powers outside approved organization policy. |
| ROLE-006 Branch coordinator | Manage assigned branch schedules, check-ins and queue. | No finance approval, unrestricted export or other-branch data. |
| ROLE-007 Inspector | Record findings and evidence for assigned inspections. | Cannot erase published versions or self-approve where independent review required. |
| ROLE-008 Inspection supervisor | Review, publish and correct reports with reason. | Publication/revision auditable; material disputes follow policy. |
| ROLE-009 Pricing analyst | Review comparables and prepare valuations/overrides. | No unsupported guarantees; overrides require reason and approval if configured. |
| ROLE-010 Auction operator | Schedule and monitor approved auctions, investigate exceptions. | No silent bid editing; cancellation/override requires approved authority and reason. |
| ROLE-011 CRM/support agent | Access assigned case, communicate and escalate. | No payment settlement, legal decision or broad document export. |
| ROLE-012 Legal operator | Review applicable documents, signatures and transfer evidence. | Access limited to assigned matters; cannot independently execute finance adjustment. |
| ROLE-013 Finance preparer | Record obligation, payment evidence and reconciliation proposal. | Cannot approve own sensitive change where separation applies. |
| ROLE-014 Finance approver | Independently approve reconciliation/adjustment within grant. | Must not be same actor as preparer for designated high-risk actions. |
| ROLE-015 Content editor/publisher | Draft, review and publish approved public content. | Unapproved legal/financial claims cannot publish; grants separated where required. |
| ROLE-016 Platform/security administrator | Manage controlled identity, configuration and audit. | Time-bound elevation, step-up and dual review for critical changes; no blanket bypass of domain financial controls. |
| ROLE-017 Analyst | View authorized aggregate/row-scoped metrics. | Sensitive attributes, exports and reidentification restricted. |
| ROLE-018 External provider/carrier | Access assigned integration or delivery task only. | Minimum required data, expiring scoped credentials and no unrestricted internal portal. |

Access decisions evaluate actor, role, resource ownership/organization, branch, case assignment, action, active status and policy version. Emergency access is separately authorized, time-bound, logged and reviewed. Verify with cross-tenant, revoked-user and privilege-escalation tests.

## Additional domain roles

These close missing role definitions used by later panels; none grants financial execution implicitly. They are proposed named permission bundles, not hired staff.

| Role ID | Responsibility and scope | Restriction and review |
|---|---|---|
| ROLE-019 Dealer verification/risk reviewer | Review assigned organization evidence, approve or reject, suspend or reinstate with evidence. | Cannot review own organization/application; step-up for suspension/reinstatement; eligibility changes serialize with new bids; never erase earlier bids. |
| ROLE-020 Logistics dispatcher | Assign verified carriers and manage transfer attempts in assigned region/cases. | Cannot verify title or execute refunds; driver sees only assigned task. |
| ROLE-021 Inventory publisher | Curate vehicle records, approve public projection, suspend and retire listings in branch scope. | No simultaneous consumer sale and live dealer auction without approved channel coordination; no publication of raw identity evidence. |
| ROLE-022 Claims reviewer | Decide policy eligibility, evidence and proposed remedy for assigned claims. | Independent review/appeal; finance separately approves monetary remedy. |
| ROLE-023 Privacy officer | Verify and coordinate rights requests, retention holds and processor responses. | Cannot access unrelated files without purpose; cannot remove legal hold unilaterally. |
| ROLE-024 Credit operations | Coordinate consented lender applications and record authenticated provider decisions. | Cannot overrule lender approval or create platform credit; provider and product activation required. |
| ROLE-025 Growth operator | Manage consented audience/campaign configuration and aggregate conversions. | Cannot bypass suppression, export restricted identities or publish legal claims. |
| ROLE-026 Independent policy approver | Review assigned critical policy changes after step-up, version comparison and domain review. | Cannot approve own submitted version or authorize a regulated service absent legal clearance. |

Named service actors in the state catalog are restricted to their domain transition and environment; authenticated callback ingestion is not general administration. Human-to-service token impersonation is forbidden.
