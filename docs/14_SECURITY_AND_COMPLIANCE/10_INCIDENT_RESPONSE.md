# Security incident response

| Metadata | Value |
|---|---|
| Document ID | 14/10_INCIDENT_RESPONSE |
| Version / status | 0.1 / proposed; security and legal review required |
| Owner | Incident Response Lead |
| Reviewers | Product, Architecture, Security, Privacy, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Security incident response for proposed marketplace; applicable legal obligations remain unresolved. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Detect, contain and recover

Signals include suspicious account takeover, unauthorized access, bid tampering, anomalous export, compromised provider credential and loss of audit integrity. An on-call responder records incident ID, start time, source, scope and initial severity; an incident commander assigns security, application, operations, legal/privacy and communications roles. Preserve relevant logs, state, hashes and access history under controlled evidence handling. Limit access to the incident record.

Containment may revoke sessions and credentials, suspend an account, block an integration or pause new auction actions. If auction integrity or authoritative time is uncertain, stop acceptance under the approved incident policy; preserve accepted bids and do not silently change a close time, invent an outcome or delete history. Restore from known-good state and reconcile auction and financial events against durable evidence before resuming. Operations contacts affected customers through approved channels; legal/privacy decide whether external notification is required and by what deadline.

## Escalation and closure

A severity matrix and on-call roster must be populated before launch; do not invent regulated reporting deadlines without jurisdiction. Log containment actions and their authorization, customer effects, decisions, communications and next update. Closure requires a verified fix, evidence of restored integrity, named owner for residual risks and retrospective actions with dates. Simulate loss of a webhook secret, data exposure and final-minute auction outage before production.

## Acceptance

A compromised dealer session is revoked without altering legitimate accepted bids. During a database/clock integrity incident, an uncertain bid does not receive a false accepted acknowledgement. Restore and replay do not duplicate obligations or notifications. Privacy/legal decision and evidence preservation are documented even if notification is deemed unnecessary.
