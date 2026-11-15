# Reference business analysis

| Metadata | Value |
|---|---|
| Document ID | 01/01_REFERENCE_BUSINESS_ANALYSIS |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and documentation leadership |
| Reviewers | Operations, legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Reference business analysis; English-first automotive marketplace documentation |

## Findings and evidence limits
The [research evidence register](../00_RESEARCH_EVIDENCE.md) contains 14 observations with sources and answers to all 30 mandatory business questions. **VERIFIED as public company statements**, the reference describes seller intake, appointment confirmation, inspection, online bidding, seller review, contract and transfer; dealer-facing marketing describes business registration and identity verification. Its consumer marketplace and sourcing pages address a different audience. Marketing claims and seller terms can have different scope; private implementation, actual financial flows, current counts and technical architecture remain unverified.

| Question | Evidence-based finding | Implication for new product |
|---|---|---|
| Who supplies and purchases? | Seller and approved dealer flows are described, with separate retail pages. | Model supplier, bidder and consumer explicitly; do not assume the same listing is exposed to all. |
| Physical service role | Public process describes branches, document review and inspection. | Schedule staffed capacity, report versions and handoffs. |
| Price and winner | Public copy mentions an initial price and highest bidder; detailed auction rule is not disclosed. | Specify and approve independent terms; do not copy an inferred proprietary algorithm. |
| Seller choice | Public seller flow describes offer communication and agreement. | Separate bid outcome from acceptance and contract. |
| Payment and credit | Seller terms and marketing make statements with differing scope. | Obtain legal/provider agreements before claims of settlement custody or financing. |

## Gaps and next actions
No authenticated dealer UI or wizard internals were inspected; no attempt to bypass access was made. Seek a permitted demonstration and current terms where useful. Do not assert their staff panels, code, database or fee rates. Translate and independently review transaction-critical Persian sources. Refresh dated claims before any strategic or legal decision. Acceptance: product team can cite each reference claim, list uncertainty, and avoid presenting proposed features as observed facts.
