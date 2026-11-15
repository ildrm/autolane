# Release Strategy

| Metadata | Value |
|---|---|
| ID / version | 19/09_RELEASE_STRATEGY / 0.1 |
| Status | Proposed planning estimate; no stakeholder sign-off |
| Owner / reviewers | Program director / product, operations, engineering, finance, legal and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Release Strategy for a proposed English-first marketplace. |

## Controlled deployment and pilot
Use isolated development, test and staging with synthetic data; access to production is least-privilege and audited. Release a versioned candidate with database compatibility, configuration and rollback plan. Enable a private staff rehearsal first, then a small preapproved branch/dealer cohort, then gradually expand only after gate evidence and stable support coverage. Feature flags default off for credit, deposits, proxy bidding, 3D and other unapproved features. A feature flag is not a substitute for server authorization or legal approval.

Before each cohort: product/operations confirm scope and staff, QA supplies candidate-specific evidence, security/privacy review changes, SRE confirms monitoring and restore, finance/legal approve actual money and contract flows, and service support has a named incident owner. Observe auction correctness, accepted-bid confirmation, error and reconciliation rates, stale projections, queue age and accessibility. Baselines and thresholds must be agreed before pilot; pause at a material error, unresolved financial discrepancy, unauthorized access, missed bid integrity invariant or loss of on-call coverage.

Rollback distinguishes safe UI/config rollback from irreversible external actions. Stop accepting new bids on loss of authoritative state; preserve existing history, notify affected parties under approved policy and reconcile provider effects before restarting. Never undo settled money by simply rolling back a database. Record release decision, version, operator, evidence, incident communication and post-release review.
