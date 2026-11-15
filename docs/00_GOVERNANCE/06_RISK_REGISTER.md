# Risk register

| Metadata | Value |
|---|---|
| Document ID | 00/06_RISK_REGISTER |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and documentation leadership |
| Reviewers | Operations, legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Risk register; English-first automotive marketplace documentation |

Scale likelihood/impact 1–5 is **proposed** and must be reassessed with observed data. Priority is product of the two, not a financial loss estimate.

| ID / risk | L × I | Owner | Preventive control | Trigger and response |
|---|---:|---|---|---|
| R-01 Unapproved funds custody | 3×5 | Finance/legal | Select licensed model and contractual obligations before launch. | Provider cannot establish authority: stop payments and escalate. |
| R-02 Bid race or unavailable close | 3×5 | Auction engineering | Authoritative ordered accepted-bid ledger and atomic close; test concurrency. | Bid/result mismatch: freeze award, preserve evidence, incident response and approved terms. |
| R-03 Incorrect vehicle report | 4×4 | Inspection lead | Evidence checklist, explicit unknowns, review, versioning. | Material issue: suspend affected sale pending review; notify according to terms. |
| R-04 Fraudulent ownership or bidder | 3×5 | Risk operations | Check authority, account eligibility, scoped access and audit. | Mismatch: hold publication/settlement, investigate with legal. |
| R-05 Personal document exposure | 3×5 | Security/privacy | Least privilege, protected files, access logging, retention schedule. | Suspected exposure: revoke access, preserve audit and follow incident policy. |
| R-06 Insufficient liquidity | 4×4 | Commercial lead | Segment participation and recruit relevant verified buyers. | No-bid rate exceeds pilot tolerance: pause expansion and investigate segment. |
| R-07 Incorrect closure | 3×5 | Finance | Require separate contract, payment, transfer and dispute checks. | Missing evidence: block ordinary closure and assign reconciliation owner. |
| R-08 Branch capacity or outage | 3×4 | Branch operations | Capacity controls, appointment notifications and staffed fallback. | Branch unavailable: close affected slots, contact customers and reschedule. |
| R-09 Unsupported legal promise | 3×5 | Legal | Review all market-specific claims, warranty and fee copy. | Unapproved template: withdraw from publication pending review. |
| R-10 Insufficient evidence of requirements | 4×4 | Product | Traceability and scenario review with named owners. | Missing API/test/permission: block affected gate and log remediation. |

Risk scores are illustrative; thresholds, time-to-response, residual risks and risk acceptance must be approved per launch market. Review weekly during discovery and after every incident.
