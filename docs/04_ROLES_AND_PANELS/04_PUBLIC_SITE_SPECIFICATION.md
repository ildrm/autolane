# Public site specification

| Metadata | Value |
|---|---|
| Document ID | 04/04_PUBLIC_SITE_SPECIFICATION |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Public site specification; English-first automotive marketplace documentation |

## Scope and pages
| Screen | Content and primary action | Data / guard / failure |
|---|---|---|
| Home | Explain seller, buyer and dealer services; start a seller request or browse published inventory. | Only approved claims and published content; loading/empty/error have accessible messages. |
| Sell | Explain steps, document preparation, potential fees and seller choice; begin request. | Fees/guarantees appear only from approved jurisdiction policy. |
| Buy and vehicle detail | Search published consumer inventory, display price, availability, inspection summary and inquiry action. | Never expose dealer-only reports; stale/unavailable listing clearly marked; no reserved-sale claim. |
| Auction explanation | Describe process, eligibility, seller review and approved terms. | Do not imply open public bidding or guaranteed price. |
| Valuation | Collect minimal vehicle parameters and show indicative range/confidence and limitations. | Missing comparables produces unavailable/manual review, not an invented price. |
| Branch finder | Show public branch details, hours and available appointment entry. | Slot confirmation requires actual reservation; branch closure hides/marks unavailable times. |
| Help, contact, legal and articles | Search approved help, contact support, read effective terms and editorial content. | Form consent and rate limits; version and effective dates; no unreviewed legal claim. |
| Partner entry | Explain eligibility and begin dealer application. | Approval is pending human review; no auction access until explicit grant. |

## UX and technical acceptance
English LTR, responsive navigation, keyboard and screen-reader labels, visible form errors, semantic headings and reduced-motion support. Public routes render meaningful, canonical content; filter combinations and unavailable listings follow SEO policy. Clearly show currency and tax inclusion when known, local time zone for appointments and contact next steps. Operational failure shows a safe retry rather than private exception details. Verify publication authorization, mobile usability, semantic metadata, privacy and stale inventory handling before launch.
