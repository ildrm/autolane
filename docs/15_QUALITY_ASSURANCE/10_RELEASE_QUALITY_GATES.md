# Release quality gates

| Metadata | Value |
|---|---|
| Document ID | 15/10_RELEASE_QUALITY_GATES |
| Version / status | 0.1 / proposed; review required |
| Owner | Release Manager |
| Reviewers | Product, QA, Engineering, Operations, Security, Design |
| Updated | 2026-11-15 |
| Scope | Release quality gates for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [release quality gates](10_RELEASE_QUALITY_GATES.md). |

## Independent gates

| Gate | Required evidence | Accountable reviewer |
|---|---|---|
| Product and operations | Approved scope, process, exceptions and operational readiness; UAT evidence. | Product and operations leads |
| UX, accessibility and visual | Tested flows and states, WCAG 2.2 AA issue disposition, design review, responsive evidence. | Design and accessibility leads |
| Motion and performance | Reduced-motion alternatives and agreed budgets; real-device measurement for key flows. | Creative and performance leads |
| Architecture and data | Approved decisions, consistency analysis, schema/contracts review, recovery and restore exercise. | Architecture and data leads |
| Security and privacy | Threat model, authorization and penetration retest, incident exercise, privacy/legal assessment. | Security and privacy leads |
| QA | Critical requirements traced to passing tests, defects and blocked tests dispositioned, release candidate identified. | QA lead |
| SEO and content | Indexation/canonical and visible structured data checks, editorial and claims approval. | SEO and content leads |
| Finance and legal | Approved jurisdiction, parties, auction binding rules, funds flow, contracts, tax, title and claims responsibilities. | Legal and finance leads |
| Service operations | Staff coverage, monitored queues, escalation roster, customer support and rollback plans tested. | Operations and SRE leads |

## Enforcement

Record gate owner, exact build and document version, evidence link, result, exception and date. Gates are not interchangeable: engineering approval cannot resolve unapproved legal terms. No launch or implementation-ready declaration while any applicable P0 decision is open. A noncritical exception needs explicit owner, compensating controls and expiry; critical integrity/security failures are not waived by this document. Verify feature flags default off for deferred features and have a tested rollback or safe stop.
