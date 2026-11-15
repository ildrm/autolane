# Service blueprints

| Metadata | Value |
|---|---|
| Document ID | 03/02_SERVICE_BLUEPRINTS |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Service blueprints; English-first automotive marketplace documentation |

## Foundational transaction blueprint
| Layer | Request and booking | Check-in and inspection | Auction and seller choice | Contract and transfer |
|---|---|---|---|---|
| Customer actions | Enter vehicle, contact, select branch/time and consent. | Present vehicle and authorized documents, review inspection. | Review outcome, terms and explicitly accept or decline. | Provide required signatures and evidence, arrange completion. |
| Frontstage | Web shows validation, slot, confirmation and document instructions. | Staff explain scope and limitations; seller sees case status. | Dealer sees authoritative bid status; seller sees specific offer and deadline. | Authorized staff explain next action and separate payment/transfer states. |
| Backstage | CRM verifies and assigns; scheduling reserves capacity. | Branch validates authority; inspector captures evidence; supervisor publishes version; pricing reviews. | Operations confirms eligibility and terms; server orders bids and closes; communications issue notifications. | Legal verifies agreement; finance reconciles independently; operations records handover and transfer. |
| Supporting systems | Contact verification, calendar, communications and audit. | Evidence storage, template versioning, access control and audit. | Auction ledger, eligibility, delivery retries and seller decision. | Contract records, provider/bank evidence, case management and legal hold. |
| Recovery | Failed message → queue; slot taken → alternatives. | Missing document → hold; disputed report → versioned review. | Duplicate/late bid → explicit decision; outage → published policy. | Mismatched amount, unexecuted contract or missing title evidence → assigned exception. |

## Lines of responsibility and evidence
The customer-facing service is a proposal; physical and legal workflow must be validated per jurisdiction. A notification confirms only a message status, not legal service or acceptance. Audit records actor, object, time, policy version and reason for privileged changes. Customer support has minimum case data and cannot mark funds settled; that authority belongs to scoped finance. Every backstage queue needs owner, timestamp, next action and escalation; quantitative SLAs are not established.
