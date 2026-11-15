# Assumptions and decisions

| Metadata | Value |
|---|---|
| Document ID | 00/05_ASSUMPTIONS_AND_DECISIONS |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and documentation leadership |
| Reviewers | Operations, legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Assumptions and decisions; English-first automotive marketplace documentation |

## Decision authority and state
[Master discovery](../00_MASTER_INDEX.md) owns DEC-01–DEC-10. All are open; role names are proposed owners, not recorded approvals. DEC-01 jurisdiction, DEC-02 commercial model, DEC-03 custody and money flow, DEC-04 auction terms, DEC-05 contracts and transfer, DEC-06 inspection/warranty, and DEC-07 privacy are P0 launch blockers. DEC-08 capacity, DEC-09 technology and DEC-10 optional auction features are P1 planning decisions. Record alternatives, chosen option, rationale, owner, evidence, effective date, consequence and approval signature before changing status.

| Assumption | Provisional planning basis | Invalidation / response |
|---|---|---|
| A-01 Operations | A branch can inspect vehicles with a trained reviewer. | Measure inspections per shift and abandon modeled capacity if queues or quality fail. |
| A-02 Funding | Non-custodial external settlement can be coordinated. | Counsel or providers may reject it; redesign funds flows and compliance before launch. |
| A-03 Liquidity | Enough approved dealers will bid in target vehicle segments. | Measure qualified bidders and no-bid outcomes in a consented pilot; reconsider inventory mix or launch area. |
| A-04 Seller choice | A presented winning bid is reviewed by seller before contractual coordination. | Any binding effect depends on terms and law; legal approval controls copy and workflow. |
| A-05 Technology | Mobile-responsive web supports initial field tasks. | Observe branch connectivity and device needs; add offline/native support only with validated requirements. |
| A-06 Inspection | Checklist and evidence can be configured per jurisdiction and versioned. | Safety or regulation may require additional certified inspection or a different process. |
| A-07 Pricing | Human-reviewed comparable-based ranges are viable at launch. | Backtest and track abstention and overrides; no ML accuracy is promised. |

## Control
Decision owners must evaluate user harm, alternatives, financial exposure, data use, irreversible effects and rollback; downstream requirements inherit the exact decision version. No assumed outcome is a legal conclusion. Any P0 remaining open means implementation-readiness is blocked; recording a provisional default is not approval.
