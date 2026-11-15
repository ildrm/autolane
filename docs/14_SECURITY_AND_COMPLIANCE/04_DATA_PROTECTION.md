# Data protection

| Metadata | Value |
|---|---|
| Document ID | 14/04_DATA_PROTECTION |
| Version / status | 0.1 / proposed; security and legal review required |
| Owner | Privacy and Security Leads |
| Reviewers | Product, Architecture, Security, Privacy, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Data protection for proposed marketplace; applicable legal obligations remain unresolved. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Classification and lifecycle

Classify data as public, internal, confidential or restricted. Customer contact and bid histories are confidential; identity documents, bank evidence and access secrets are restricted. A data inventory must record owner, purpose, lawful basis, categories, sharing, retention, residency and deletion exception. Retention periods, legal holds and cross-border transfers are **DECISION REQUIRED** per jurisdiction; avoid inventing a universal legal period.

Use TLS for transport and managed encryption at rest, separate keys and least-privilege access to production, backups and object storage. Encrypt backups and test restore using a distinct role. Store secrets in a managed secret service with rotation; never put them in source control, logs or analytics. Mask identifiers in support views and remove personal data from lower environments unless a specifically approved exception applies. Minimize datasets sent to analytics and providers; document recipient and purpose.

Deletion requests trigger identity verification, inventory lookup, lawful hold checks, erasure or restriction in primary stores and downstream systems, and documented backup-expiration handling. A legal hold prevents deletion only for the necessary scope. A correction creates an audit-safe version when a record's integrity requires history. Failed propagation remains open for retry and privacy review; completion cannot be claimed on a mere request.

## Acceptance

Access logs identify actor, purpose and time without storing document contents. A development engineer without a production support grant cannot retrieve identity files. Deletion reconciles every registered downstream recipient, reports retained records and the reason, and is tested on representative backup and restore paths.
