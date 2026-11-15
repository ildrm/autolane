# Continuous integration and delivery

| Metadata | Value |
|---|---|
| Document ID | 18/03_CICD_STRATEGY |
| Version / status | 0.3 / proposed, not deployed |
| Owner | Delivery Engineering Lead |
| Reviewers | Architecture, Security, Finance, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Continuous integration and delivery for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [recovery plan](07_BACKUP_AND_RECOVERY.md). |

## Pipeline and release controls

Each change receives peer review and runs dependency/secret scanning, static analysis, unit and API checks, authorization tests, schema compatibility checks and a reproducible build. A release candidate deploys to staging for contract, integration, critical E2E, accessibility, security and workload tests. Record artifact digest, dependencies, policy and schema version, test results and approvers; use signed artifacts where available. Deploy the identical artifact to production after required product, operations, security, QA, legal and finance gates pass.

Use backward-compatible expand/contract database changes, with old and new versions coexisting during rollout; destructive cleanup follows verified migration and retention review. This document specifies a process only and does not authorize creating migrations. Use progressive deployment and reversible feature flags with default-off financial and optional auction features; a flag cannot weaken permission checks. Monitor error rate, accepted bid consistency, queue age and database load; rollback the application when safe, pause new auctions if correctness is uncertain and follow the incident runbook for data-level reconciliation.

## Acceptance

A failed security or auction-integrity gate cannot be overridden by a routine deployment permission. A production deploy points to the tested digest; rollback has been exercised in staging. Failed migration or smoke checks halt promotion. Emergency changes receive recorded retrospective review and cannot bypass unresolved legal decisions.

## Candidate gates and safe release progression

Documentation/contract changes validate OpenAPI, JSON Schema, operation uniqueness, all local links and traceability IDs. Future application changes add type/static checks, unit/integration tests, authorization tests, dependency/secret scanning and migration compatibility. A candidate records immutable commit/build ID, dependency inventory, contract version and test evidence; secrets come from environment-scoped vault references. Untrusted pull-request builds receive no production credentials or customer data.

Promote the identical signed artifact from isolated integration to staging to controlled pilot. Before production, inspect contract/backfill compatibility, backup restore evidence, required DEC approvals, feature flags, operational staffing and rollback trigger. Start with a small approved traffic cohort, compare correctness/error/latency to baseline, and stop on any bid/financial integrity failure. Rollback application only when the database/contract remains backward-compatible; otherwise disable feature and perform a reviewed forward repair. No rollback may erase committed bids or financial facts. Feature flags cannot bypass authorization, legal activation or schema validation. This phase documents the process and includes no pipeline or deployment scripts.
