# Definition Of Done

| Metadata | Value |
|---|---|
| ID / version | 19/10_DEFINITION_OF_DONE / 0.1 |
| Status | Proposed planning estimate; no stakeholder sign-off |
| Owner / reviewers | Program director / product, operations, engineering, finance, legal and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Definition Of Done for a proposed English-first marketplace. |

## Delivery and document completion
A backlog item is done only when its product intent, owner, priority and acceptance criteria are approved; role and object scope, data reads/writes, business rules and failure states are specified; related UX/copy/accessibility states and contract changes are reviewed; applicable event/audit and analytics definitions exist; positive, negative, authorization, duplicate/retry and concurrency tests pass; monitoring and operational recovery are documented; privacy, security and legal concerns are resolved or have an approved time-bound disposition. New behavior cannot be declared complete merely because a screen renders.

A release candidate additionally needs versioned architecture/data decisions; end-to-end UAT; relevant accessibility, security, performance, privacy, recovery and integration evidence; current runbooks, training and on-call roster; migration/rollback plan; all applicable financial/legal approvals; and a named go/no-go outcome. Critical failures or unresolved P0 decisions block release and implementation-ready declaration.

A documentation artifact is done when its ID, version, owner, status, evidence classification, scope, links, acceptance tests, explicit assumptions and unresolved questions are present, its references resolve, and designated reviewers have reviewed it. An automatically generated file with sections or filenames alone is not sufficient. Draft status remains until review is recorded; the machine-readable manifest must reflect reality and not silently upgrade status.

## Expanded contract baseline — revision 0.3

Documentation done, implementation tested, and live business authorized are independent states defined in [policy baseline](../POLICY_BASELINE.md). A document-only task does not require production code or fabricated application test results.
