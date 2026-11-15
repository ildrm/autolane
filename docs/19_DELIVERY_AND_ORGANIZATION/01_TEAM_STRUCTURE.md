# Team Structure

| Metadata | Value |
|---|---|
| ID / version | 19/01_TEAM_STRUCTURE / 0.1 |
| Status | Proposed planning estimate; no stakeholder sign-off |
| Owner / reviewers | Program director / product, operations, engineering, finance, legal and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Team Structure for a proposed English-first marketplace. |

## Purpose and staffing model
This is a **PROPOSED planning model**, not an approved organization, measured schedule or claim that specialists have reviewed the documents. Allocate named accountable owners before implementation. FTE is full-time-equivalent capacity, not headcount; one person may perform compatible roles if segregation and sufficient time remain. See [resource and cost estimates](07_RESOURCE_AND_COST_ESTIMATES.md).

| Responsibility | Required seniority and skills | Deliverables / dependencies | Lean / balanced / enterprise FTE |
|---|---|---|---:|
| Product leadership and business analysis | Senior product owner; marketplace, prioritization, acceptance | Scope, backlog, business rules; depends on commercial and legal direction | 1 / 2 / 3 |
| Research and service design | Senior researcher; interview, operational observation, analysis | Personas, validated journeys and usability evidence; depends on branch access | 0.25 / 0.5 / 1 |
| UX, UI and design system | Senior designer; interaction, accessibility, responsive interfaces | Screen states, component/tokens and handoff; depends on validated workflows | 0.75 / 1.5 / 3 |
| Motion and graphics | Mid/senior creative; animation and optimized media | Motion timings, assets and fallbacks; depends on creative direction | 0.1 / 0.25 / 1 |
| Frontend | Senior React/web engineers; accessibility, realtime UX | Responsive public/dealer/operations interfaces; depends on contracts and designs | 1.5 / 3 / 5 |
| Backend and realtime | Senior backend engineers; domain modeling, concurrency, integration | API, auction, transactions and adapters; depends on approved rules | 2 / 4 / 7 |
| Data and database | Senior data engineer/DBA; relational integrity, valuation, retention | Schema, reporting, backups and data quality; depends on data model and privacy policy | 0.4 / 0.75 / 2 |
| Platform, SRE and DevOps | Senior platform engineer; deployment, recovery, observability | Environments, CI, runbooks and restore evidence; depends on architecture | 0.5 / 1 / 2 |
| Quality and test | Senior test architect/engineers; automation, accessibility, load | Test plan, UAT evidence, quality gates; depends on requirements and environments | 0.8 / 1.5 / 3 |
| Security and privacy | Senior security engineer; IAM, threat modeling, PII | Threat model, authorization tests and incident procedures; depends on jurisdiction | 0.25 / 0.5 / 1 |
| SEO, content and analytics | Senior practitioner; indexation, attribution and measurement | Public content policy and event definitions; depends on UX/content approvals | 0.2 / 0.5 / 1 |
| Automotive operations and scenario specialist | Senior branch/auction operator; inspection, exceptions and training | Operational rules, UAT, playbooks and staffing; depends on pilot capacity | 0.2 / 0.3 / 1 |
| Finance and legal domain review | Qualified market-specific legal/finance expertise | Contracting model, money flow, tax, transfer and retention approvals | 0.05 / 0.2 / 0.5 |

The above approximate totals are **8.0 / 16.0 / 30.5 FTE**, respectively; utilization, calendar availability and local compensation vary. Fractional specialist capacity is an average allocation, not evidence that critical review is optional. Product, QA, operations, legal and finance approval are independent from engineering and may need additional availability at release. The enterprise plan intentionally reserves specialist capacity; final staffing follows detailed estimation and hiring availability.

## Documentation phase and working cadence
For further documentation review allocate a proposed 3–5 FTE core for 4–8 weeks: product/requirements 1, architecture/data 1, design/accessibility 0.5–1, QA/security 0.5–1, operations/legal/finance 0.5–1 shared. Estimate excludes user recruiting and external legal opinions and can overlap specialist work; acceptance depends on evidence and closure of P0 decisions, not elapsed time.

Weekly: product and operations resolve scenarios; design/engineering review state behavior and authorization; QA creates tests concurrently; security/privacy review threat and data changes; finance/legal approve financial and contractual semantics; SRE reviews failure/recovery. A cross-functional review records named owner, decision and expiry. No team member may self-approve their own restricted financial adjustment.
