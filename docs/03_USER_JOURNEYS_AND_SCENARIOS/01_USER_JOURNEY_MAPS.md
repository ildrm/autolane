# User journey maps

| Metadata | Value |
|---|---|
| Document ID | 03/01_USER_JOURNEY_MAPS |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | User journey maps; English-first automotive marketplace documentation |

## Seller: request to decision and closure
| Stage | User action and visible feedback | Backstage owner and data | Failure and recovery |
|---|---|---|---|
| Discover and start | Review how service works, fees when approved and documents; enter vehicle and contact. | CRM creates request, records policy/consent version and verification state. | Invalid entry receives field-level correction; unconfirmed contact can be retried. |
| Book | Pick branch and local time; see confirmation and reference. | Branch capacity is reserved atomically. | Full slot offers alternatives; branch closure triggers notice and reschedule. |
| Inspection | Check in, review expected scope and wait for findings. | Inspector records versioned evidence; supervisor reviews. | Missing authority or incomplete inspection pauses progress; dispute opens review. |
| Offer | Review offer amount, currency, conditions and response deadline, and accept or decline. | Auction result and explicit decision reference the offer version. | No bid, rejected offer or expiry ends attempt or starts separately approved follow-up. |
| Completion | See contract, payment/transfer and handover statuses and next contact. | Legal, finance and operations record independent evidence. | Mismatch or dispute remains open; seller sees neutral pending status and support contact. |

## Dealer and staff journeys
Dealer: register organization → submit authority evidence → await review → access eligible vehicle and versioned report → submit bid → see authoritative outcome → if selected, follow contract and obligations. Ineligible, late, duplicate and ambiguous submissions must be explained without inventing a winning result. Branch staff: open capacity → manage arrivals → record exceptions → hand off to inspector. Finance: inspect obligation and external evidence → match or flag discrepancy → independent review → coordinate closure. Support: verify identity → understand case → assign owner → communicate next steps → escalate without altering privileged financial states.

## Accessibility and measurement
Each action has keyboard access, visible focus, descriptive error and accessible status announcement; avoid exposing private results to other users. Track stage transitions with consented minimal identifiers and measure cohort conversion, no-show, report correction and discrepancy rates. Validate through moderated tasks and complete scenario tests; legal and finance must approve actual obligations.
