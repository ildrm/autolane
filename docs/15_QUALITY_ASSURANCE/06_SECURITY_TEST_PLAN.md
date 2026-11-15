# Security test plan

| Metadata | Value |
|---|---|
| Document ID | 15/06_SECURITY_TEST_PLAN |
| Version / status | 0.1 / proposed; review required |
| Owner | Security QA Lead |
| Reviewers | Product, QA, Engineering, Operations, Security, Design |
| Updated | 2026-11-15 |
| Scope | Security test plan for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [release quality gates](10_RELEASE_QUALITY_GATES.md). |

## Coverage

Test unauthenticated, customer, dealer from two separate organizations, staff from two branches, inspector, supervisor, finance maker/checker and platform admin. For each role exercise direct API calls, real-time subscriptions, file links and state mutations; do not assume hidden UI means denied access. Use the [security testing specification](../14_SECURITY_AND_COMPLIANCE/09_SECURITY_TESTING.md) as control source and record build, test identity, endpoint, payload, expected/actual result and evidence.

Include credential stuffing and recovery enumeration, session fixation and revocation, expired step-up, cross-site request attempts, injection and output encoding, forged callbacks, bid replay, request floods, upload bypass, insecure direct object access, unauthorized exports, staff termination, secrets exposure and backup access. Test privilege changes and immediate access revocation according to the approved propagation objective. Simulate compromise only in authorized environments; protect evidence and avoid live customer data.

## Defect handling and acceptance

Risk-rate findings with impact, exploitability, affected asset and exposure; assign owner and remediation deadline. Critical unresolved security findings block launch. A time-limited exception for a noncritical risk requires compensating control, named risk owner and explicit approval, never a blanket waiver for unresolved legal obligations. Independently retest fixes and inspect for variant paths. Ensure audit records do not themselves expose document contents, passwords or financial credentials.
