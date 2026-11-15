# Authentication Api

| Metadata | Value |
|---|---|
| ID / version | 10/03_AUTHENTICATION_API / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Backend and architecture leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Authentication Api; commercial and jurisdiction-dependent policy decisions remain open. |

## Session, verification and recovery
| Operation | Input / authorization | Outcome and failure |
|---|---|---|
| `POST /v1/auth/sessions` | Verified credentials or approved identity-provider assertion; anonymous subject | Return secure, HttpOnly, SameSite session cookie and CSRF token for browser clients. Invalid credentials share generic 401 and throttling; never enumerate accounts. |
| `GET /v1/auth/session` | Active session | Return actor, available scoped organizations and expiry, not hidden permissions or sensitive identity evidence. |
| `POST /v1/auth/step-up` | Active session plus approved second factor | Grant short-lived elevation bound to actor, session and purpose; fail closed on expiry. |
| `DELETE /v1/auth/session` | Current session with CSRF defense | Revoke session and associated WebSocket subscriptions; return 204. |
| `POST /v1/auth/recovery` | Identifier and recovery method | Always return generic acceptance; time-limited single-use token, rate limiting and audit; no user existence disclosure. |

Dealer bidder permission requires active organization, active membership and explicit bidding grant; account authentication alone is insufficient. Staff elevation requires strong MFA and approval policy. Authorization rechecks for each mutation and subscription; revoked membership immediately prevents future actions and disconnects streams. Store passwords only with approved adaptive hashing if platform-managed; avoid recording secrets in logs. Token/session duration, identity provider, recovery and MFA policy require security and jurisdiction review. Tests cover CSRF, session fixation, revocation, expired elevation and cross-organization access.

## Authoritative MFA and elevation contract

OpenAPI distinguishes 200 authorized AuthSession from 202 AuthChallenge. A pending challenge is not an authenticated session. Complete login MFA at `/auth/challenges/complete`; purpose-bound elevation uses `/auth/step-up` then `/auth/step-up/complete`, bound to the original session. Challenge is single-use, five-minute TTL and at most five failures. Provider assertion must be issuer/audience/nonce checked. Recovery gives uniform acceptance and does not disclose account existence. See [policy defaults](../POLICY_BASELINE.md). The browser obtains a fresh CSRF token only within an authorized session; secure HttpOnly session cookies never enter analytics or URLs.
