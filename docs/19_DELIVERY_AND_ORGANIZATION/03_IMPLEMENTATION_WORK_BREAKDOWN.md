# Implementation Work Breakdown

| Metadata | Value |
|---|---|
| ID / version | 19/03_IMPLEMENTATION_WORK_BREAKDOWN / 0.1 |
| Status | Proposed planning estimate; no stakeholder sign-off |
| Owner / reviewers | Program director / product, operations, engineering, finance, legal and QA |
| Updated | 2026-11-15 |
| Purpose and scope | Implementation Work Breakdown for a proposed English-first marketplace. |

## Work packages and exit criteria
No production implementation is authorized by this specification. Estimates are hypotheses pending P0 decisions, discovery findings and team capacity.

| Package | Owner / deliverable | Prerequisites | Exit evidence |
|---|---|---|---|
| W1 Governance and decisions | Product, legal, finance: jurisdiction, model, rules, acceptance | Named sponsor, qualified counsel | Signed DEC-01–07 decisions; prioritized requirements and traceability. |
| W2 Product, service and design | Product/design/operations: journeys, screen states, content and assets | Representative users and branch operators | Tested critical flows, accessible components, approved visual and motion handoff. |
| W3 Platform foundation | Architecture/SRE/security: environments, identity, authorization, audit, observability | W1 privacy boundary and approved architecture | Access-denial and restore drills, controlled build/release path. |
| W4 Seller and branch | Backend/frontend/operations: intake, consent, scheduling, CRM, branch work | W2 workflow and W3 identity | Capacity concurrency and no-show UAT, accessible form evidence. |
| W5 Inspection and valuation | Inspection/domain team: configurable checklist, reviewed report and recorded estimate | W4 vehicle/appointment; inspection and legal policy | Versioned evidence, correction and stale-auction tests. |
| W6 Dealer and auction | Auction team: verification, scoped auction access, bid/close and realtime display | W3 access, W5 report, approved auction rules | Linearizable bid/close test, reconnect and failure/recovery exercises. |
| W7 Contract and settlement tracking | Legal/finance/engineering: agreement evidence, obligations, reconciliation, title and handover | W1 money/title decisions, W6 seller decision | Mismatch/default tests and signed operating acceptance; no inferred custody. |
| W8 Verification and pilot | QA/security/operations: UAT, load, security, recovery, staff training | Integrated W4–W7 | Passing independent gates and explicit pilot go/no-go. |
| W9 Later phases | Product-led consumer marketplace, CMS, finance partners and advanced services | Pilot evidence, legal/provider decisions | Separate phase gate and operational capacity. |

Work should be vertically sliced by scenario rather than implementing screens, APIs or tables in isolation. Each slice includes role checks, domain transaction, error handling, event, audit, analytics, accessible states and acceptance evidence. Track estimates and dependencies per package; integration and rework contingencies are explicit in the cost model.
