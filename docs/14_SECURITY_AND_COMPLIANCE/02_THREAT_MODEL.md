# Threat model

| Metadata | Value |
|---|---|
| Document ID | 14/02_THREAT_MODEL |
| Version / status | 0.3 / proposed; security and legal review required |
| Owner | Threat Modeling Lead |
| Reviewers | Product, Architecture, Security, Privacy, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Threat model for proposed marketplace; applicable legal obligations remain unresolved. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Assets, actors and abuse cases

Protect identity documents, customer contact information, unpublished inspection media, dealer eligibility, accepted bids and their order, contracts, financial evidence, privileged configuration and audit records. Threat actors include unauthenticated attackers, compromised customers or dealers, malicious insiders, compromised providers and accidental operators. Entry points include public forms, dealer bid API, uploads, support workflows, webhooks, administrative actions and event consumers.

| Threat | Impact | Control and verification |
|---|---|---|
| Cross-tenant access by changing an identifier | Confidential reports or bids disclosed | Object and organization scope enforced server-side on every request; test alternate IDs across roles and endpoints. |
| Bid replay, forged timestamp or race | Invalid winner or duplicate commitment | Server-authoritative ordering and deadline; unique request key, transactional validation and append-only accepted records; run concurrency and replay tests. |
| Insider manipulates published inspection | Misleading auction information | Independent review, versioned publication, reasoned correction and immutable history; test separation and dispute audit. |
| Malicious upload or stored script | Malware, session theft or exposure | Quarantine and scan, content verification, safe rendering, restrictive headers and non-executable storage; test evasions and blocked retrieval. |
| Spoofed provider callback | False payment or delivery status | Verify provider signature, timestamp and replay ID; reconcile authoritative provider evidence; test bad signatures and duplicate delivery. |
| Privilege escalation or fraudulent refund | Money loss or unapproved changes | Step-up, least privilege, independent approval, immutable audit; test initiator cannot approve own action. |
| Stolen session and bot credential stuffing | Account takeover and fraud | MFA, rate limits, device/session review and revocation; monitor failed and anomalous attempts without disclosing account existence. |
| DDoS or provider outage near auction close | Inconsistent outcome or unavailable bidding | Protect capacity, fail closed on uncertain authority, reconcile and use documented incident protocol; simulate partition and recovery. |
| Broad analytics export | Sensitive data leakage | Purpose-limited fields, row-level access, query/export review and retention; test authorization and deletion propagation. |

## Review and acceptance

Reassess when money flow, jurisdiction, a new provider or deployment boundary changes. Rank risk by likelihood and impact after control owners agree; no numerical likelihood is invented here. Each P0 threat requires a named owner, mitigating control and executable negative test before launch. Record residual risk and explicit approval; unknown legal or provider obligations block related activation.

## Threat-to-control-to-test register

| Threat ID / boundary | Abuse sequence | Prevent/detect/recover / acceptance |
|---|---|---|
| THR-01 Browser→API | Change organization or object ID while retaining a valid session | Server object scope and projection allowlist; test every panel read/write with other tenant ID, including replay and exports. |
| THR-02 Admission→DB | Submit before cutoff but hold lock until after close | Post-lock trusted clock and shared close lock; reject late effective acceptance and retain receipt. |
| THR-03 IAM→auction | Suspend member concurrently with bid | Common eligibility lock order; exactly one ordering, no newly accepted bid after effective suspension. |
| THR-04 Anonymous intake→account | Claim victim lead by guessed UUID or matching email | Draft-bound challenge plus verified authenticated contact; generic invalid result, no record merge or existence disclosure. |
| THR-05 Provider→adapter | Reuse event ID with changed amount/evidence | Signature verification, unique provider/event and payload hash; quarantine conflict, no settlement change. |
| THR-06 Upload→publication | Mislabeled file, active content or stale scan grant | Byte/type/size validation, quarantine, safe rendering and access recheck; malicious object cannot publish or download. |
| THR-07 Author→approval | Same user approves via a second role or generic transition endpoint | Compare immutable actor IDs, not role names; aliases share invariant handler; denial across both APIs. |
| THR-08 Worker→consumer | Duplicate/reorder accepted, reversal and closure facts | Inbox idempotency, monotonic versions and authoritative recheck; disputed obligation cannot be hidden by old event. |
| THR-09 Analytics→export | Combine small cohorts or inject spreadsheet formulas | Purpose/row/field scope, cohort thresholds and escaped export cells; request/job/download all reauthorize. |
| THR-10 Admin→policy | Activate unapproved custody or extend a live auction | Independent version approval and legal activation gate; existing auction policy immutable. |

Security owner assigns severity from actual exposure and attacker capability; all listed integrity and cross-tenant failures block the relevant release. Threats are design-review hypotheses, not discovered vulnerabilities in deployed software. Review after provider onboarding, new data fields, changes in trust boundaries or significant incident.
