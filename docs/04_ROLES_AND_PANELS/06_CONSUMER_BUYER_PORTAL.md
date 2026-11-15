# Consumer buyer portal

| Metadata | Value |
|---|---|
| Document ID | 04/06_CONSUMER_BUYER_PORTAL |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Consumer buyer portal; English-first automotive marketplace documentation |

## Scope and journey
Phase 2 proposal: browse separately approved consumer inventory, compare accurate inspection summaries and total disclosed price, ask for a purchase appointment or submit a sourcing request. A consumer listing is not automatic access to a private dealer auction and does not guarantee availability or financing.

| Screen | Action and data | Failure / privacy |
|---|---|---|
| Search results | Search/filter by vehicle attributes, region, price, year and mileage; sort with clearly stated basis. | No results offers filter reset; unavailable or stale data has visible state. |
| Vehicle detail | View public photos, authorized report summary, price/tax and known conditions, contact/inquiry. | Removed inventory is unavailable; report limitations and missing information are explicit. |
| Inquiry/appointment | Provide contact, preferred time and consent; receive reference and human follow-up. | Slot conflicts offer alternatives; avoid revealing another customer's reservation. |
| Favorites/saved search | Authenticated buyer saves permitted items and notification preferences. | Removed listing remains marked unavailable; disable alerts on opt-out. |
| Sourcing request | Record desired attributes, budget/currency, location and payment preference; advisor qualifies and sends candidate. | No match receives status and review plan; changed price requires fresh acknowledgement. |
| Buyer account | Review own inquiries, messages and case next action. | Ownership and minimum necessary access on every request; support can only view assigned case. |

## Acceptance
A buyer can distinguish advertised price from fees and optional financing, identify any unverified condition, withdraw/cancel a request under policy and see accurate availability. Tests cover cross-account access, stale listing, no match, inaccessible images, consent changes and provider failure. Reservation, financing approval and warranty are not implied without approved policy.
