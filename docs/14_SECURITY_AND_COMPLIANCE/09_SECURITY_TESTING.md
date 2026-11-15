# Security testing

| Metadata | Value |
|---|---|
| Document ID | 14/09_SECURITY_TESTING |
| Version / status | 0.1 / proposed; security and legal review required |
| Owner | Security QA Lead |
| Reviewers | Product, Architecture, Security, Privacy, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Security testing for proposed marketplace; applicable legal obligations remain unresolved. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Verification plan

Before merge, scan dependencies and secrets, lint for dangerous patterns, inspect authorization decisions and execute unit/API tests for every protected action. Before release, run authenticated dynamic scans in a representative environment with synthetic data; review CSP, cookie flags, session expiry, cross-site request protection, upload isolation and service identity permissions. Independent penetration testing covers customer, dealer, staff, API, real-time, provider webhook and storage boundaries. Do not test third-party systems without authorization.

| Test | Expected result |
|---|---|
| Object-level ID substitution across seller/dealer organizations | No record, existence signal or attachment is disclosed; attempt is logged appropriately. |
| Concurrent/replayed bids or forged timestamp | One authoritative result per idempotency key; no accepted bid outside server-approved rules. |
| Privilege escalation and maker/checker bypass | Denied on server, including direct API calls and expired step-up session. |
| Malicious file or invalid webhook | File remains quarantined; false callback cannot change financial state. |
| Session theft simulation and staff termination | Sessions revoked according to measured target; privileged controls prevent further access. |
| Backup restore and deletion | Only authorized role restores; data classification and lawful deletion/hold rules survive restore. |

## Gate

A release cannot proceed with unresolved critical vulnerabilities or unexplained failed authorization tests. High-severity exceptions require documented risk owner, compensating controls, expiry and explicit release authority; no exception bypasses a legal or P0 business decision. Track evidence, affected build, environment, retest and remediation owner. Perform incident tabletop and recovery exercise before first live auction.
