# Role permission matrix

| Metadata | Value |
|---|---|
| Document ID | 04/02_ROLE_PERMISSION_MATRIX |
| Version / status | 0.1 / proposed; awaiting review |
| Owner | Product and operations leadership |
| Reviewers | Legal, finance, design, architecture, security and QA as applicable |
| Last updated | 2026-11-15 |
| Scope | Role permission matrix; English-first automotive marketplace documentation |

## Permission matrix
Legend: O = own record; A = assigned case/branch; G = explicitly granted organization; R = independent reviewer/approver; — = denied. Each allowed action still requires an active user, current policy and relevant case status.

| Action | Seller | Dealer bidder | Branch | Inspector / supervisor | Auction ops | Support | Legal | Finance prep / approver | Admin |
|---|---|---|---|---|---|---|---|---|---|
| View seller case/contact | O | — | A | A minimum | A minimum | A minimum | A | A minimum | Restricted metadata |
| Reserve / change appointment | O | — | A | — | — | A by grant | — | — | Policy only |
| Record / publish report | — | — | — | A / R | — | — | — | — | No domain bypass |
| View eligible inspection report | O where policy permits | G | A | A | A | A limited | A | A limited | No general read |
| Create or cancel auction | — | — | — | — | A with approval | — | Review | — | Policy only |
| Submit bid | — | G with bidder grant | — | — | — | — | — | — | — |
| Accept/reject offer | O | — | — | — | — | Assisted action only if authorized and evidenced | — | — | — |
| View/edit contract | O applicable copy | G applicable copy | — | — | — | A limited | A | A read only | No general read |
| Record / approve reconciliation | — | — | — | — | — | — | A read | A / R separate actor | No bypass |
| Change bank details | — | — | — | — | — | — | Review | Prepare / independent approval | No bypass |
| Publish public content | — | — | — | — | — | — | Review claims | — | Content publisher grant only |
| Grant privileged access or change policy | — | — | — | — | — | — | Review | Review | Time-limited, step-up, dual approval where required |

## Enforcement and test
Default deny. Evaluate tenant/organization, case assignment, branch, data sensitivity, actor status, delegated action and current policy on every read and write, including downloads and real-time subscriptions. Record sensitive access and privileged changes without logging secrets. Refuse self-approval for designated transactions; revocation takes effect on subsequent requests and streams. Negative tests cover ID guessing, cross-tenant access, role escalation, expired grant, direct API call and unauthorized export. Exact separation-of-duties and emergency access policies require security, legal and finance approval.

## Additional scoped permission bundles

| Role | Read and command scope | Denied capability and approval constraint |
|---|---|---|
| ROLE-019 | Assigned dealer verification, risk case and eligibility decisions | Own-application approval, bid edits and financial execution denied. |
| ROLE-020 | Assigned regional logistics, carriers and delivery transitions | Cannot verify legal title or approve monetary remedy. |
| ROLE-021 | Assigned inventory, publication revisions and seller-authorized consumer offers | Cannot publish raw private evidence or create conflicting active sale channels. |
| ROLE-022 | Assigned claim evidence and reasoned remedy/appeal decision | Own-investigation independent appeal and payment execution denied. |
| ROLE-023 | Verified privacy rights requests, scoped holds and processor tasks | Cannot waive legal preservation or export unrelated records. |
| ROLE-024 | Assigned consented lender applications and safe status | Cannot invent lender decision, override terms or grant credit-backed bidding. |
| ROLE-025 | Purpose-approved campaigns, suppressions and aggregate results | Cannot override opt-out, export sensitive audiences or publish unreviewed terms. |
| ROLE-026 | Independently review exact critical policy version and approval evidence | Cannot approve own version, bypass domain policy or enable unapproved custody. |

All role IDs resolve in the user-role catalog. API action-specific guards and the state catalog narrow these bundles further. Equal role labels held by different users do not alone prove independence; compare immutable maker/reviewer actor IDs and conflicts of interest. Shared service principals are excluded from human UI sessions.
