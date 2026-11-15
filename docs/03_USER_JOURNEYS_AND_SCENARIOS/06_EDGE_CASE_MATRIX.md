# Edge case matrix

| Metadata | Value |
|---|---|
| Document ID | 03/06_EDGE_CASE_MATRIX |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Edge case matrix; English-first automotive marketplace documentation |

| Trigger | Immediate safe behavior | Owner / resolution | Required check |
|---|---|---|---|
| Last appointment claimed simultaneously | Commit one reservation only; show alternatives to loser. | Branch lead reconciles any external appointment. | SCN-01 and TST-01. |
| Phone verification fails repeatedly | Preserve draft, throttle attempts and offer approved assistance. | Support verifies without revealing whether another account exists. | No account takeover or leaked code. |
| Vehicle authority conflict or lien | Pause publication and transaction. | Branch/legal review evidence and consent. | No sale action while unresolved. |
| Inspector cannot examine a component | Record unknown and reason; never set pass by default. | Supervisor determines completeness. | Report displays limitation. |
| Report changes after bids | Preserve report versions and stop misleading continuation when required. | Supervisor and auction/legal apply approved policy. | Bidders can identify report version; history retained. |
| Duplicate bid after lost response | Return original authoritative request result. | Auction support investigates only if result unavailable. | No duplicate accepted bid. |
| Concurrent close and bid | Evaluate against one server-defined ordering. | Auction operations reconcile ledger. | Exactly one outcome; deadline policy applied consistently. |
| Suspended bidder has accepted earlier bid | Prevent new bids; retain prior history. | Legal applies published disqualification terms. | No silent removal or ad hoc winner swap. |
| Seller does not respond | Show pending until approved deadline; then record expiry if policy says so. | CRM follows up within consent. | No implied acceptance. |
| Buyer defaults | Preserve agreed obligations and evidence; open case. | Legal/dealer success act under contract. | No unapproved penalty, refund or substitution. |
| Partial payment or duplicated bank notice | Match each authoritative evidence to obligation once; retain remaining balance. | Finance reconciles exception. | Duplicate cannot produce false fully settled state. |
| Requested bank account change | Hold change and payment initiation pending independent verification. | Finance reviewers follow approved two-person process. | Evidence and approvals logged; avoid exposing account. |
| Vehicle handed over before title updated | Show separate custody and title states. | Operations coordinates legally required follow-up. | No inferred ownership transfer. |
| Notification provider down | Mark delivery pending/failed and retry with controlled backoff. | Support uses authorized fallback where required. | Message status never constitutes legal acceptance. |
| Branch or network unavailable | Do not promise invalid slot or fabricated auction outcome. | Incident owner and branch lead communicate and recover. | Restore from authoritative record and reconcile. |
| Privacy deletion requested on held evidence | Restrict processing and evaluate retention/hold rather than blindly delete. | Privacy/legal record response and review date. | Correct scope, hold and audit. |

Specific deadlines, remedies and exceptions are open until policy and jurisdiction are approved; test each matrix entry with authorized and unauthorized actors.
