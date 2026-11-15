# Admin Api

| Metadata | Value |
|---|---|
| ID / version | 10/07_ADMIN_API / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Backend and architecture leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Admin Api; commercial and jurisdiction-dependent policy decisions remain open. |

## Privileged control plane
| Operation | Scope and evidence | Result |
|---|---|---|
| `POST /v1/admin/policies/{id}/versions` | Policy admin, MFA step-up, reason and proposed version | Draft immutable policy version, 202 pending review; existing auctions remain pinned. |
| `POST /v1/admin/policies/{id}/approvals` | Different qualified approver, explicit decision and version | Approve/reject with audit; activation only at future effective time after validations. |
| `POST /v1/admin/memberships/{id}/suspend` | Scoped security/admin role, reason | Disable future commands and subscriptions; existing bids remain immutable; alert operations. |
| `GET /v1/admin/audit-events` | Authorized auditor, reason, object/time filter | Paginated minimally necessary audit; export separately approved and logged. |

All writes require current session, CSRF where applicable, step-up, version precondition and idempotency. No super-admin silently edits accepted bids, ledger journals, inspection revisions or signed contracts. Access is tenant/branch scoped, exceptional overrides require independent approval and expiry. Test privilege escalation, self-approval, duplicate submissions, stale versions and audit unavailability; fail closed for privileged changes if durable audit cannot be written.
