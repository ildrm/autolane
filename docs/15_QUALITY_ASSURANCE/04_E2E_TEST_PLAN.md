# End-to-end test plan

| Metadata | Value |
|---|---|
| Document ID | 15/04_E2E_TEST_PLAN |
| Version / status | 0.1 / proposed; review required |
| Owner | E2E Test Lead |
| Reviewers | Product, QA, Engineering, Operations, Security, Design |
| Updated | 2026-11-15 |
| Scope | End-to-end test plan for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [release quality gates](10_RELEASE_QUALITY_GATES.md). |

## Journeys

Use isolated synthetic accounts and deterministic external-provider simulations. Seed versioned branch calendars, vehicle taxonomy, dealer eligibility, inspection templates and auction policies. Preserve a correlation ID from UI through APIs, events and audit without logging personal data. Test at least: seller submits and books; branch check-in; inspector submits and supervisor publishes; analyst reviews valuation; eligible dealer bids; auction closes; seller chooses; legal coordinates contract; finance records and reconciles external payment evidence; authorized operations records transfer and closes. Verify each participant sees only permitted state.

Negative journeys include duplicate lead, no appointment capacity, document mismatch, inspector unavailability, report rejection and correction, dealer suspension, losing network after bid commit, seller rejection, buyer default, contract refusal, payment mismatch and delayed title transfer. For later phases cover a consumer item sold while viewed, finance rejection/expiry, failed logistics handover and disputed warranty eligibility. Each case includes preconditions, actor, action, expected visible state, durable data, notifications, audit and recovery owner.

## Reliability and acceptance

Run critical paths on every release candidate, with a smaller smoke subset on each merge and full cross-browser coverage on a controlled schedule. Test system time via controlled clock interfaces, not by sleeping until a real auction ends. A transient UI failure is not retried until it passes without retaining first failure evidence. One P0 mismatch, missing authorization boundary or divergent transaction state blocks release. Final sign-off requires recorded approved business policies and evidence of independent operational UAT.
