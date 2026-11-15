# Raci Matrix

| Metadata | Value |
|---|---|
| ID / version | 19/02_RACI_MATRIX / 0.1 |
| Status | Proposed planning estimate; no stakeholder sign-off |
| Owner / reviewers | Program director / product, operations, engineering, finance, legal and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Raci Matrix for a proposed English-first marketplace. |

## Accountability model
A = accountable final decision owner, R = produces or executes, C = consulted, I = informed. One accountable role per row; a person may fill several compatible roles, but security, financial or audit independence must not be removed. Roles: P product lead, O automotive operations, D design/accessibility, E architecture/engineering, Q QA, S security/privacy, F finance, L legal, Rl release/SRE, M marketing/SEO.

| Deliverable / decision | P | O | D | E | Q | S | F | L | Rl | M |
|---|---|---|---|---|---|---|---|---|---|---|
| Product scope, prioritization | A | C | C | R | C | C | C | C | I | C |
| Customer research and UX | C | C | A/R | C | C | C | I | C | I | C |
| Inspection and branch playbook | C | A/R | C | C | C | C | I | C | I | I |
| Auction commercial and bidding policy | R | A | C | R | C | C | C | C | I | I |
| Contract and jurisdiction approval | C | C | I | C | I | C | C | A/R | I | I |
| Funds flow, reconciliation and ledger policy | C | C | I | R | C | C | A/R | C | I | I |
| Architecture, API and data contracts | C | C | C | A/R | C | C | C | C | C | I |
| Threat model, privacy and incident controls | C | C | C | R | C | A/R | C | C | C | I |
| Test strategy and evidence | C | C | C | R | A/R | C | C | C | C | I |
| Design, visual and motion system | C | C | A/R | C | C | C | I | I | I | C |
| Search, content and SEO rules | C | C | R | R | C | C | I | C | I | A |
| Recovery and deployment runbooks | I | C | I | R | C | C | I | I | A/R | I |
| Launch recommendation and pilot | A | R | C | R | R | C | C | C | R | I |

**Enforcement:** the release lead collects each independent domain approval; product launch accountability does not permit overriding legal or security blockers. If one role is missing, mark the RACI row unstaffed; do not infer sign-off. Review role assignments and conflict-of-interest controls before every release.
