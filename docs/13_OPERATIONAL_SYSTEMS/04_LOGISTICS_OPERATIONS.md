# Logistics operations

| Metadata | Value |
|---|---|
| Document ID | 13/04_LOGISTICS_OPERATIONS |
| Version / status | 0.1 / proposed; requires domain review |
| Owner | Logistics Lead |
| Reviewers | Operations, Product, Security, Legal, QA |
| Updated | 2026-11-15 |
| Scope | Logistics operations for the proposed marketplace; jurisdiction and transaction model remain open. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Service boundary and workflow

Logistics coordinates physical custody, not legal title or payment. Authorized operations record a transfer request with vehicle/case, origin and destination, time window, vehicle condition, contact and service type. A dispatcher assigns a verified carrier or driver with appropriate coverage and records insurance and contractual terms where required. The carrier sees only assigned jobs and minimum contact information.

The driver records pickup timestamp, condition checklist, photos, odometer and signed or otherwise approved proof. Custody changes from scheduled to collected only after evidence is accepted; delivery changes from in-transit to delivered only after authorized proof of delivery. Failed pickup/delivery records location, reason and custodian and returns to an owned rescheduling queue. Track timestamps in UTC and show local times at both endpoints.

## Exceptions and security

A damage report preserves pickup and delivery evidence, freezes deletion, identifies custody periods and routes to claims; it does not automatically determine liability. Unavailable driver, invalid insurance, unsafe condition or missing recipient authority prevents dispatch or handover as appropriate. Delay notifications are idempotent, avoid disclosing precise location broadly and remain queued on provider outage. Disputes hold closure until operations resolves or approves an explicit exception.

## Data and acceptance

Entities: delivery job, assignment, custody event, proof version, condition observation, carrier and claim reference. Track on-time deliveries / completed deliveries, failed attempts / attempts, damage claims / deliveries and median delay with period and denominator. A forged or unauthorized delivery proof does not change custody. A retried pickup cannot create two custody transfers. A damage claim retains both photo sets after a correction.
