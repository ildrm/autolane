# Dashboard design system

**ID:** 06/09_DASHBOARD_DESIGN_SYSTEM · **Version:** 0.1 · **Status:** PROPOSED; no trademark, asset or stakeholder approval · **Owner:** Design systems lead · **Reviewers:** Brand, accessibility, UX, frontend · **Updated:** 2026-11-15

## Information density
Operations workspaces use shared navigation, scope selector and a work queue. A page includes H1, selected branch/organization, status summary, filters and primary task; timestamps show local timezone and are based on server facts. Use 14/20 body, 40px compact controls and 16px baseline spacing; retain 44px targets where necessary on touch. Do not compress critical payment or ownership evidence to a colored dot.

## Queue, case and audit patterns
Queues default to assigned work ordered by policy; columns include case reference, vehicle summary, status, owner, due time and permitted action. Filtering exposes active filters and reset; pagination and selection are server-scoped. A case detail uses clearly separated inspection, auction, seller decision, contract, settlement, title and handover sections with source and last-updated time. Every risky action has exact effect, reason, access and confirmation. Actions that require approval show requester, approver, pending status and audit trail. Inspectors cannot silently overwrite a published report; finances cannot be marked settled on a pending provider response.

## Data visualization and failures
Charts show metric definition, denominator, period, currency where relevant, last refresh and table alternative. “No data,” zero and unavailable are distinct. A failed dashboard query preserves previous values only with a visible stale timestamp; never imply they are current. Disable workflows whose preconditions cannot be established and present escalation. Access revocation hides sensitive data on refresh and rejects requests server-side.

## Acceptance
Run keyboard and screen-reader tests on filters, sort, row details and approvals; verify concurrent edits yield a conflict with recovery, branch scope cannot leak in exports and mobile views preserve essential data. Test high-volume queues, long labels, zero/unavailable and 200% text zoom.
