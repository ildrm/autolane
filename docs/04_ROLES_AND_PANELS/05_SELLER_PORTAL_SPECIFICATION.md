# Seller portal specification

| Metadata | Value |
|---|---|
| Document ID | 04/05_SELLER_PORTAL_SPECIFICATION |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Seller portal specification; English-first automotive marketplace documentation |

## Screens and behavior
| Screen / trigger | Inputs and successful outcome | Validation / failure and access |
|---|---|---|
| Request vehicle | Brand, model, variant, year, mileage/unit, location and condition; save draft or submit. | Required fields, valid ranges and taxonomy version; unsupported vehicle routes to human review. Seller sees own case only. |
| Contact and consent | Verify contact where required; record purpose, consent text/version and timestamp. | Failure permits limited retry and support; no marketing consent bundled into required service consent. |
| Appointment | Select branch/time and review document instructions; reserve and receive reference. | Atomic capacity guard, local time zone; competing booking offers alternatives; cancel/reschedule subject to policy. |
| Case status | See milestones, current owner/team, next action and contact. | Show pending, held, completed or failed truthfully; updates do not imply legal result. |
| Inspection report | Read authorized report version, findings, unknowns and limitations; raise dispute. | No access to private notes; unavailable evidence shows safe status; dispute routes to supervisor. |
| Offer decision | Read offered amount, ISO currency, terms/version and deadline; explicitly accept or decline. | Confirm identity and current version, refuse stale/expired offer; consent and legal effect follow approved terms. |
| Contract and transaction | View authorized documents, outstanding obligations, payment/transfer and handover statuses. | Payment evidence and title are independent; missing evidence remains pending; protected downloads and audited access. |
| Support | Submit a case with appropriate attachment and track response. | File-type/size scanning and scoped access; no promise of automatic remedy. |

## Acceptance
A seller can complete the journey with keyboard and assistive technology, distinguish indicative valuation from actual offer, and tell who to contact on hold. Negative tests deny other sellers, refuse stale offers and prevent a bid win from falsely showing a completed sale. Any consent, retention, signature, fee or deadline wording requires local policy approval.
