# Environment strategy

| Metadata | Value |
|---|---|
| Document ID | 18/02_ENVIRONMENT_STRATEGY |
| Version / status | 0.1 / proposed, not deployed |
| Owner | Platform Lead |
| Reviewers | Architecture, Security, Finance, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Environment strategy for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [recovery plan](07_BACKUP_AND_RECOVERY.md). |

## Isolation and purpose

| Environment | Purpose and data | Access / promotion |
|---|---|---|
| Local and ephemeral | Developer experiments and pull-request verification using synthetic fixtures. | Per developer/service identity; short lifetime, no production secrets. |
| Integration | Exercise service interfaces, provider simulators and asynchronous processing with resettable synthetic data. | Engineering and QA; mutable test data and documented configuration. |
| Staging | Production-like topology, representative load, release candidates, restore and security tests; synthetic data only by default. | Restricted named staff, audited and no live payment action. |
| Production | Approved customer services, private data and live integrations. | Least privilege, MFA, reviewed changes and audited emergency access. |

Configuration varies by environment through reviewed, versioned policies and secret references. Build one immutable artifact and promote the same digest after tests; do not rebuild a different production image. Explicitly distinguish sandbox and live provider credentials and fail startup when an environment pairing is invalid. Clocks, currencies, legal policies and mock providers must be testable without affecting real customers.

## Acceptance

A nonproduction principal cannot read production identity documents or secrets. A staging payment points to a sandbox and cannot cause a live transfer. Environment drift and expiring credentials alert owners. The selected region, retention and access policy are documented before customer data is introduced.
