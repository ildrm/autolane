# Data Retention

| Metadata | Value |
|---|---|
| ID / version | 09/07_DATA_RETENTION / 0.3 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Data Retention; jurisdiction-dependent policy decisions remain open. |

## Retention and privacy policy
**DECISION REQUIRED:** jurisdiction, tax, statutory holds, contract terms, consent and minimum retention are not known. The following is a classification and control scheme, not an approved deletion schedule.

| Class | Examples | Controls / disposition |
|---|---|---|
| Identity and contact | profiles, dealer documents | Least privilege, encrypted storage, purpose limitation; delete or pseudonymize after approved schedule unless hold applies. |
| Transaction and accounting | obligations, contracts, journal evidence | Restricted immutable history; legal and tax owner defines retention and hold; redact permitted ancillary data separately. |
| Vehicle and inspection | VIN, photos, report revisions | Restrict identifying data and unapproved images; retain versions while claims or legal obligations require. |
| Security and audit | access and privileged actions | Append-only with protected access, minimal personal content; security/legal sets duration. |
| Analytics and marketing | event IDs, attribution and consent | Minimize identifiers, enforce consent and deletion propagation; use aggregated results where possible. |

Deletion workflow: authenticate request, classify scope, check jurisdiction/holds and dependencies, approve, delete or pseudonymize in primary, object versions, caches and projections; record non-sensitive completion evidence and handle backup expiry under policy. Legal hold stops disposal. Test restore does not silently resurrect erased data; reapply tombstones before serving. Rights and response deadlines require legal sign-off.

## Policy record and deletion execution contract

A retention policy version contains class, jurisdiction, purpose, lawful basis reference, trigger event, minimum duration, maximum duration where applicable, hold precedence, primary/object/projection action, backup-expiry method, policy owner, approving counsel and effective time. Missing approved duration disables automatic destructive disposal; it does not authorize indefinite lawful retention or launch. Configuration validation rejects negative durations, contradictory min/max and an effective policy without approval. Legal hold has a case reference, scoped records, issuer, reason, issued time and reviewed release; a broad administrator toggle cannot remove it.

Privacy processing states are `received → identity_pending → assessing → approved|partially_approved|denied → executing → completed`, with `on_hold` from assessing/executing and controlled resume. A request may be completed with a reasoned partial response when preservation is required; it must never be mislabeled as all data erased. Processor records per-system task, legal basis, owner, attempt, result and evidence hash. Failed downstream deletion is retried and remains visible; completed status requires all applicable systems accounted for. Backups are isolated, age out on approved schedule and apply the erasure ledger before any restore becomes queryable. Contacting the requester uses a verified channel; exported access bundles recheck current identity and authorization.

Test held transaction plus removable marketing profile, expired verification evidence, duplicate request, user identity change during processing, failed warehouse deletion, backup restore and revoked export access. Record only the minimum completion evidence; the audit itself has an approved retention class.
