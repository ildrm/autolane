# Scope and prioritization

| Metadata | Value |
|---|---|
| Document ID | 02/08_SCOPE_AND_PRIORITIZATION |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and documentation leadership |
| Reviewers | Operations, legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Scope and prioritization; English-first automotive marketplace documentation |

## Decision framework
Prioritize by safety/legal necessity, contribution to an end-to-end outcome, user value, operational dependency and evidence. Record cost, risk, confidence, accountable owner and decision date; do not use a numerical score as a substitute for human review.

| Priority | Capabilities | Reason / boundary |
|---|---|---|
| P0 for a managed-loop pilot | Seller intake and consent; booking; identity/authority review; inspection; dealer approval; authoritative bids; explicit seller decision; contract coordination; settlement/transfer evidence; support; authorization; audit. | A missing step makes the core transaction incomplete or unsafe. Detailed launch behavior still depends on DEC-01–DEC-07. |
| P1 after core workflow | Consumer listings, search, sourcing, CRM and editorial content. | Require separate inventory publication, accurate availability and support workflows. |
| P2 subject to market and partner approval | Credit, financing, warranty, logistics automation, advanced analytics. | Provider, disclosure, contractual and operational dependency. |
| Experiment | 3D and personalization; AI-assisted valuation. | Do not launch without measured benefit, accessibility and model governance. |

## Scope control and acceptance
Excluded without approval: money custody, inventory ownership, lending, automatic default penalties, mandatory deposits, automated binding decisions and promises of warranty. Optional auction behavior must be independently accepted, documented and tested. A proposed change names affected users, transaction states, legal and financial terms, security, interfaces, data, analytics, tests, capacity and rollback. Product may propose a change; legal, finance and operations approve relevant consequences. Pilot launch requires release criteria and P0 decisions, not just feature completion.
