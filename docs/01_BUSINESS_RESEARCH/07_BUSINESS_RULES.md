# Business rules baseline

| Metadata | Value |
|---|---|
| Document ID | 01/07_BUSINESS_RULES |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and documentation leadership |
| Reviewers | Operations, legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Business rules baseline; English-first automotive marketplace documentation |

## Proposed rules; all market-dependent terms remain subject to legal approval
| ID | Rule and verification |
|---|---|
| BR-001 | A time slot may not exceed its effective capacity. Concurrent claims for the last place cannot both confirm; released capacity becomes available under policy. |
| BR-002 | Published inspection evidence is versioned. A correction creates a new reviewed version, retains prior evidence and records actor, time and reason; material findings can place the transaction on hold. |
| BR-003 | Only an eligible, authorized bidder may submit a bid; authoritative server evaluation and ordered acceptance determine ranking. Duplicate requests must not create a second accepted bid. Final increment, timing, eligibility, tie and reserve rules require DEC-04. |
| BR-004 | The seller's decision references a specific offer and is explicit; absence of a decision is not represented as acceptance. Legal effect and expiry need approved terms. |
| BR-005 | A normal transaction close requires evidence prescribed by the approved policy for contract, settlement and transfer, plus resolution of material financial discrepancies. A bid or seller acceptance alone is insufficient. |
| BR-006 | Consumer publication and private dealer auction visibility are separately authorized; no private auction report becomes public by default. |
| BR-007 | No fee, penalty, deposit, guarantee or credit entitlement is implied until its policy and legal disclosure are approved. |
| BR-008 | Contract, payment evidence, physical custody and ownership transfer have independent statuses; one must not silently set another. |
| BR-009 | Privileged changes require actor, object, time and reason; sensitive financial and access changes follow approved segregation-of-duties policy. |
| BR-010 | Monetary amounts specify ISO currency, exact representation and approved rounding; time instants use UTC and displays use selected applicable local time zone. |
| BR-011 | No sensitive record is accessible solely by possession of an identifier; subject/organization and purpose scope must be evaluated. |
| BR-012 | A changed effective policy is versioned and never silently rewrites past accepted terms. |

## Exceptions and policy ownership
Inspectors cannot mark unknown checks as passed; supervisors review disputes. Auction operations apply published outage/cancellation rules, not ad hoc silent bid edits. Finance records reconciliation exceptions, not invented finality. Legal owns effects of acceptance and contract. Each rule must map to a test and event in the completed traceability register. BR-001–BR-005 originate in the governance traceability baseline; remaining rules are defined here. These are proposed guardrails, not completed legal terms.
