# Identity and access management

| Metadata | Value |
|---|---|
| Document ID | 14/03_IDENTITY_AND_ACCESS |
| Version / status | 0.3 / proposed; security and legal review required |
| Owner | Identity Lead |
| Reviewers | Product, Architecture, Security, Privacy, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Identity and access management for proposed marketplace; applicable legal obligations remain unresolved. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Identity lifecycle

Consumers authenticate via an approved identity method; dealers belong to verified organizations and receive separately granted roles. Staff identities are provisioned from an authoritative workforce system, reviewed periodically and revoked on departure. Privileged users require MFA; sensitive actions require recent step-up authentication. Recovery must not downgrade identity verification silently. Users receive generic authentication failures and rate-limited recovery to reduce enumeration.

## Authorization model

Use deny by default and evaluate subject, action, organization, branch, case assignment, resource state, policy version and current account status on the server. A seller may view only their own cases; dealer bidders act only for an approved organization and eligible auction; inspector access is assigned/branch scoped; supervisors publish reports; finance reconciles and independently approves adjustments; platform administrators manage configuration but cannot automatically execute financial or legal actions. A suspension or terminated membership takes effect for new actions and active sessions are revoked. Access to restricted files is re-evaluated before issuing short-lived links.

High-impact grants, auction interventions and policy changes require reason, audit and independent approval where feasible. Emergency access is time-limited, logged, justified and reviewed; it is not a standing bypass. Separation-of-duties exceptions need named approval, expiration and compensating review. Authorization decisions must not rely solely on hidden frontend controls.

## Acceptance

A dealer in organization A cannot read or bid for organization B; a suspended dealer cannot submit even with an old token. An inspector cannot publish their own report under the proposed separation policy. A privileged operation fails when step-up has expired. Membership revocation invalidates access within the documented operational propagation window, which must be measured and approved before production.

## Identity lifecycle and authorization evaluation order

Evaluate: authenticate credential/session → check revocation and environment/audience → identify principal and current scope → evaluate action grant → object ownership/assignment → data-field projection → source-state/business guards → fresh purpose-bound step-up where needed. Repeat current access checks before returning an old idempotent receipt or file/export grant. Effective UI capabilities are hints only. ROLE-016 administration never substitutes for finance/legal authority; dual roles on one person do not satisfy independent approval.

Login returns either a non-authorized MFA challenge or a complete session, never both. Step-up is a separate challenge tied to purpose, actor, session and expiry; successful login does not automatically approve a later financial or title action. Recovery uses single-use expiring tokens, session revocation and a new login; loss of the second factor requires independent identity recovery, not automatic removal. Anonymous seller/buyer intake uses draft-session scope and separate ownership proof. A new dealer application creates a pending organization; registration-number similarity is a review signal and cannot join an existing organization.

Joiner/mover/leaver process: domain owner requests least-privilege scope, an independent authorized approver verifies employment/organization authority, IAM applies a time-bounded grant and audit, and revocation disconnects streams and blocks subsequent reads/downloads. Organization admins can request only permitted dealer membership changes; staff/global grants require security administration and domain approval. Emergency access is limited to a named incident, expires automatically and cannot edit bids or bypass monetary approval. Until an approved IAM adapter or explicitly specified native grant API exists, this administrative process is performed in the audited identity-provider console, with case evidence; it is not an unspecified hidden endpoint.

Authentication controls follow the [OWASP authentication guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html); exact session/challenge durations and product recovery behavior are proposed project policy in the policy baseline. Test generic login/recovery messages, expired/replayed challenges, revoked sessions, unsafe redirect targets, CSRF and multi-tab scope switching.
