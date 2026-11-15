# API test plan

| Metadata | Value |
|---|---|
| Document ID | 15/03_API_TEST_PLAN |
| Version / status | 0.1 / proposed; review required |
| Owner | API Test Lead |
| Reviewers | Product, QA, Engineering, Operations, Security, Design |
| Updated | 2026-11-15 |
| Scope | API test plan for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [release quality gates](10_RELEASE_QUALITY_GATES.md). |

## Contract and behavior

For every cataloged API operation verify schema, content type, field constraints, response and error contracts, authentication, authorization, tenant/branch scope, pagination, stale version, rate limit, audit and sensitive-data minimization. Use consumer-driven checks to detect unannounced changes and require explicit versioning for incompatible changes. Schemas describe exact fields and limits; where a policy or contract is not defined mark the corresponding case blocked rather than infer implementation.

Exercise missing/expired token, invalid role, valid user with wrong object, suspended organization and duplicate idempotency key; check both HTTP result and absence of unauthorized data or mutation. For mutating requests send the same key and body twice and then a different body with the same key. Simulate timeout after commit and query authoritative result. Verify date/time in UTC, ISO currency code and exact monetary units; reject currency mismatch, invalid precision and unsupported code under configured policy.

For callbacks test invalid signature, stale timestamp, replay, out-of-order delivery and matching against the expected provider reference, currency and amount. Verify a callback cannot directly imply finalized settlement without the required reconciliation. Upload tests cover size, malicious type and tenant access. OpenAPI validation alone does not prove auction correctness: run concurrent transactions against a production-like database.

## Acceptance

Each public operation has at least one success, validation failure, authentication failure and object-authorization test; mutating operations additionally test idempotency, conflict and audit. Contract violations or unintended sensitive fields block release. Provider test failures and unsupported sandbox behavior are explicitly recorded.
