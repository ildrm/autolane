# Security architecture

| Metadata | Value |
|---|---|
| Document ID | 14/01_SECURITY_ARCHITECTURE |
| Version / status | 0.1 / proposed; security and legal review required |
| Owner | Security Architect |
| Reviewers | Product, Architecture, Security, Privacy, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Security architecture for proposed marketplace; applicable legal obligations remain unresolved. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Trust boundaries and controls

Public browsers, authenticated customers, dealer organizations, privileged staff, external providers and platform workloads are separate trust zones. A reverse proxy enforces TLS, request size and abuse controls; applications independently authenticate and authorize every object-level action. Background workers authenticate as narrowly scoped service identities; no access token from an end user is blindly forwarded to a provider. Identity, payment evidence, inspection media, bids and contracts are classified separately and encrypted in transit and at rest using managed keys with audited access.

Authoritative business state resides in transactional storage, not caches or broadcasts. Every privileged configuration, access grant, report publication, auction intervention and financial adjustment records actor, scope, reason, time and outcome to protected audit storage. Logs exclude secrets, raw identity documents, full payment credentials and message content. Network restrictions are defense in depth, not authorization. Search and analytics receive only fields necessary for purpose.

**PROPOSED controls:** phishing-resistant MFA for privileged staff, step-up for sensitive actions, short-lived sessions, rate limiting by account/device/network and deny-by-default resource authorization. Session revocation and credential rotation are required. External identity, payment and messaging providers need due diligence, scoped credentials, webhook verification, timeout and incident contacts. No card data is stored by the marketplace unless a separately approved compliance assessment changes scope.

## Acceptance

Security review maps each trust crossing to identity and authorization; a compromised dealer session cannot access another organization's bid details or documents. Audit delivery failure alerts and prevents high-risk changes if durable audit cannot be recorded. Restore exercises verify encrypted backup readability and access boundaries. Relevant controls and negative tests are detailed in the remaining security documents.
