# Panel architecture

| Metadata | Value |
|---|---|
| Document ID | 04/03_PANEL_ARCHITECTURE |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Panel architecture; English-first automotive marketplace documentation |

## Logical surfaces
| Surface | Users and core responsibilities | Isolation and dependencies |
|---|---|---|
| Public website | Visitor learns, starts seller flow, sees published vehicles, branches and help. | Public data only; CMS review and published-state checks. |
| Seller portal | Seller manages own request, appointment, inspection status, offer and completion. | Subject ownership and verified contact; private files protected. |
| Consumer portal | Buyer manages inquiry, sourcing and favorites. | Buyer ownership; consumer publication distinct from dealer auctions. |
| Dealer portal | Approved dealer organization and explicit bidders review eligible reports, bid and track outcomes. | Organization membership, eligible auction scope, bid authority and suspension enforcement. |
| Operations workspace | Branch, inspection, valuation, auction, CRM and support queues. | Branch/assignment scoped modules; explicit domain actions and audit. |
| Legal and finance workspace | Restricted contract, transfer, obligation, evidence and reconciliation. | Matter assignment, financial preparation/approval separation and secure documents. |
| Administration and analytics | Identity, policy, taxonomies, alerts and appropriately scoped analytics. | Privileged elevation; dual control for critical changes and limited data exports. |

These are logical boundaries, not a mandate for separate deployables. [Discovery inventory](../02_PRODUCT_AND_PANEL_INVENTORY.md) lists 20 panel concepts. Do not infer that an administrator can override domain authorization. Every panel shows loading, empty, stale, no access, error and retry states, plus appropriate case owner and next action. The public and dealer experiences may share underlying services only if authorization is enforced server-side.

## Acceptance and dependency
Screen action matrix and [role matrix](02_ROLE_PERMISSION_MATRIX.md) must agree on allowed actions. Search and real-time channels filter by current authorization; revoke access promptly. All private routes require authentication and screen metadata must not reveal restricted data. Prior to launch, complete detailed screen/API contracts, audit, usability and accessibility tests.

## Expanded contract baseline — revision 0.3

[Twenty detailed panel contracts](12_PANEL_CONTRACTS.md) define navigation, fields, authorization, components, states, API/data dependencies, exports and acceptance.
