# Notification workflows

| Metadata | Value |
|---|---|
| Document ID | 13/07_NOTIFICATION_WORKFLOWS |
| Version / status | 0.1 / proposed; requires domain review |
| Owner | Communications Platform Lead |
| Reviewers | Operations, Product, Security, Legal, QA |
| Updated | 2026-11-15 |
| Scope | Notification workflows for the proposed marketplace; jurisdiction and transaction model remain open. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Event-to-message contract

A domain transition creates a durable notification intent with stable event ID, recipient, case reference, template version, channel, purpose, language, locale, time window and idempotency key. Resolve the recipient's verified address and preferences at send time; distinguish service messages from marketing, with legal basis and suppression rules approved for each jurisdiction. Never put secrets, full identity documents or payment details in the message. Links require authorization when opened and do not themselves grant durable access.

| Trigger | Recipient | Message intent | Recovery |
|---|---|---|---|
| Appointment confirmed or changed | Seller | Local date, time, branch and case link | Retry provider errors; create agent follow-up if urgent and undelivered. |
| Report available | Seller or eligible dealer | Report is ready; link to authorized view | Do not attach private report to an uncontrolled channel. |
| Auction bid/outcome | Eligible dealer or seller as relevant | Status and link; no claim that a bid equals a completed sale | Coalesce noncritical updates; authoritative state is fetched after reconnect. |
| Contract, settlement or dispute action needed | Appropriate participant | Next action and support route | Retry only safe intent; escalate repeated failures. |
| Consent change | Affected user | Confirmation where required | Audit and apply preference immediately. |

## Delivery and acceptance

States are queued, sending, accepted by provider, delivered when confirmed, failed, suppressed and dead-lettered. Provider acceptance is not delivery. Retries use bounded exponential backoff and stable provider idempotency keys where supported; reconcile ambiguous provider responses before resending. Provider callbacks are authenticated, deduplicated and ordered by event time. Alert on queue age and repeated failure without logging message contents.

One domain event retried multiple times yields one logical intent per recipient and purpose. An unsubscribed user receives no optional campaign; a service notification is governed by its separate policy. Provider outage leaves the business state intact and routes time-sensitive delivery to an owner.
