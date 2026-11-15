# Administration specification

| Metadata | Value |
|---|---|
| Document ID | 04/10_ADMINISTRATION_SPECIFICATION |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Administration specification; English-first automotive marketplace documentation |

## Administrative domains
| Domain | Allowed configured action | Approval and guard |
|---|---|---|
| Users and organizations | Invite, suspend, revoke and assign scoped roles and dealer membership. | Verify identity and organization; sensitive grants require step-up, reason, effective period and independent approval. |
| Branches and capacity | Maintain hours, closures, staff assignments and capacity. | Change preview identifies affected appointments; closure creates reschedule work rather than silently cancelling. |
| Vehicle taxonomy and inspection templates | Version makes/models and jurisdiction-specific checklist, findings and evidence requirements. | Draft/review/publish workflow; historical inspections retain their template version. |
| Terms and commercial policy | Version fees, auction parameters, language and jurisdiction. | Legal/product/finance approval before effective date; changes never silently apply to existing accepted terms. |
| Communications | Edit reviewed templates and provider settings; inspect delivery failures. | Marketing consent and opt-outs enforced; no secret exposure or unsupported legal claims. |
| Audit and exports | Search authorized activity and produce approved exports. | Scope and purpose, sensitive fields masked, export approval and access trail; no bulk extraction by default. |
| Feature flags and operational configuration | Enable approved capabilities for cohort/market and monitor behavior. | Record actor, reason, effective time and rollback; unsafe auction/custody features remain disabled until policy approval. |

## Security and acceptance
Default deny; administrators do not bypass finance, legal or seller decisions merely by role. Emergency access requires time limit, reason, audit and retrospective review. Test privilege escalation, revoked session, configuration version conflict, dual approval, historical policy immutability, and inability to expose private documents. Admin actions should return actionable validation and safe errors without secrets.
