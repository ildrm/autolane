# Documentation standards

| Metadata | Value |
|---|---|
| Document ID | 00/02_DOCUMENTATION_STANDARDS |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and documentation leadership |
| Reviewers | Operations, legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Documentation standards; English-first automotive marketplace documentation |

## Classification and ownership
Label all reference-specific assertions VERIFIED with accessible source and date, INFERRED with reasoning, UNVERIFIED where evidence is absent, PROPOSED for a new-platform design, and DECISION REQUIRED for material unresolved choices. A source's claim is not independent verification. Every document records ID, version, date, owner, reviewers, status, purpose and relevant linked authority; mark proposals as unapproved. Keep legal translations subject to qualified review.

## Stable identifiers and change process
Use BUS-### for objectives, FR-### for functional requirements, BR-### for rules, ROLE-### for actors, SCR-### for screens, SCN-### for scenarios, API-### for operations, ENT-### for entities, EVT-### for events and TST-### for tests. Assign each identifier once in its authoritative register; do not invent a cross-reference without registering it. Aliases in discovery artifacts are local and require mapping before baseline. Change requests state old/new behavior, owner, reason, evidence, affected interfaces, data, tests, analytics, security, and rollback; approved changes increment version and retain history. A breaking contract needs a migration and consumer notice.

## Specification quality
Each significant requirement names actor, trigger, preconditions, data read/written, success and failure behavior, permission scope, rules, asynchronous work and observability, acceptance test and metric. A state transition names source, trigger, guard, actor, target and immutable audit evidence. Financial examples specify currency, rounding, payer, payee, timing and limits, and are labeled synthetic. Document no sensitive actual customer information.

## Review and verification
Owners verify references resolve, ID definitions are unique, absence of contradictory rules, authorization on every privileged action, explicit failure recovery, and test expected results. QA checks tests against behavior rather than implementation detail. Legal reviews binding language and retention; security reviews data and permissions. Link checks prove existence, not correctness. Statuses: draft, review, approved, superseded; never mark approved without a named reviewer and recorded approval.
