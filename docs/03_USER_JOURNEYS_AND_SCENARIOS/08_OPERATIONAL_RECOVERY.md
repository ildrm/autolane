# Operational recovery

| Metadata | Value |
|---|---|
| Document ID | 03/08_OPERATIONAL_RECOVERY |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Operational recovery; English-first automotive marketplace documentation |

## Recovery protocol
1. **Detect and contain:** identify affected cases and time range; stop unsafe new actions and protect authoritative records. Separate unavailable status from failed payment or lost bid.
2. **Assign authority:** incident commander coordinates technical restoration; auction, branch, legal, finance and privacy owners decide respective business actions under preapproved terms. No engineer silently changes bid or payment history.
3. **Preserve evidence:** record timeline, provider references, committed state, message delivery and actor actions in a restricted case. Avoid exposing personal records in incident channels.
4. **Restore and reconcile:** bring service back, process idempotent pending work, compare committed bid sequence and close result, compare obligations against provider/bank evidence, and investigate mismatches before award or ordinary transaction closure.
5. **Communicate:** give affected customers a factual current status and contact route; record delivery attempts. Legal determines mandated notice and auction remedy.
6. **Close and learn:** affected-case owners attest reconciliation, remaining exceptions have owners and deadlines, then write incident review and corrective actions. Never assert recovery based only on service availability.

## Scenario-specific playbooks
| Event | Required actions | Exit condition |
|---|---|---|
| Auction outage at close | Capture authoritative time/ledger, hold award, restore and reconcile; apply published pause/cancel/restart terms only. | Auction/legal approve result or cancelled outcome, impacted bidders informed. |
| Branch closure | Stop availability, identify confirmed bookings, offer alternatives and preserve no-show distinction. | Every affected appointment confirmed rescheduled or explicitly cancelled. |
| Provider timeout | Query provider using original correlation key before retrying; avoid duplicate payment or message. | Confirm authoritative status or escalate unresolved item. |
| Data restoration | Restore to isolated environment, validate integrity and access controls, compare recovery point with known commits and replay safely. | SRE and domain owners approve consistency; unresolved gaps are cases. |
| Compromised privileged account | Revoke sessions/grants, preserve evidence and review affected changes. | Security completes containment and relevant owners verify disputed state. |

Recovery time, data loss objectives, escalation times and customer remedy are proposed only after capacity and legal review; no undocumented manual fallback may transfer money or alter a winner.
