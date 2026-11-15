# Incident management

| Metadata | Value |
|---|---|
| Document ID | 18/08_INCIDENT_MANAGEMENT |
| Version / status | 0.1 / proposed, not deployed |
| Owner | SRE Incident Commander |
| Reviewers | Architecture, Security, Finance, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Incident management for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [recovery plan](07_BACKUP_AND_RECOVERY.md). |

## Severity and response

Define on-call coverage before launch and maintain contact methods outside the affected system. Suggested classification: SEV1 for suspected loss of auction integrity, financial data exposure or complete service outage; SEV2 for substantial degraded service or provider outage with a workaround; SEV3 for localized noncritical degradation. Classification and response times require operational approval. Open an incident record, assign commander, communications lead and technical owners, establish a timeline and preserve evidence.

Contain impact using scoped feature flags, rate limits, credential revocation or suspension of new auction actions. Do not silently alter an auction deadline or claim a payment completed; record uncertainty and communicate user impact in plain English after approved review. Escalate suspected exposure to privacy/legal, and financial discrepancy to finance. Maintain regular internal updates and a customer update cadence that reflects the severity and available facts.

## Recovery and learning

Verify root service health and business-state consistency, reconcile provider and audit records, replay only idempotent intents, restore user access and receive domain-owner approval before resuming sensitive actions. A post-incident review records impact, timeline, contributing factors, detection gap, remediation owner and due date without blame. Run tabletop exercises for provider outage, compromised staff account and close-time database partition.

## Acceptance

The on-call responder can reach a named alternate and locate relevant runbooks; incidents have an owner and timeline. An uncertain auction is held for human review; an apparent provider recovery cannot automatically finalize unreconciled transactions.
