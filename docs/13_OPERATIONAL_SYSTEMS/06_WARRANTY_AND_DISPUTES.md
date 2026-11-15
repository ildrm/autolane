# Warranty and dispute operations

| Metadata | Value |
|---|---|
| Document ID | 13/06_WARRANTY_AND_DISPUTES |
| Version / status | 0.1 / proposed; requires domain review |
| Owner | Claims and Legal Operations Leads |
| Reviewers | Operations, Product, Security, Legal, QA |
| Updated | 2026-11-15 |
| Scope | Warranty and dispute operations for the proposed marketplace; jurisdiction and transaction model remain open. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Policy and eligibility

No warranty is promised by this specification. Any offer needs a separately approved, jurisdiction-specific policy defining coverage, exclusions, claim window, evidence, liability, remedy and appeal. Store the policy version presented and accepted for the relevant transaction. If no approved policy applies, classify a report as a service complaint and do not display guaranteed compensation.

Claim intake links transaction, vehicle, inspection report version, claimant, issue date and evidence; record received time and eligible policy version. An authorized claims reviewer checks coverage and evidence, identifies conflicts of interest and records findings. Status progresses received → evidence requested or under review → decision pending → approved, denied or withdrawn → remedy pending → closed. Decisions require reason and evidence; denial includes applicable appeal route. A different authorized reviewer handles an appeal when possible. Compensation or refund execution requires finance approval under the selected settlement model.

## Exceptions and data access

Missing evidence prompts a dated request and retains the original claim date. A corrected inspection, disputed ownership, duplicate complaint or suspected fraud is routed to the relevant domain; evidence is retained under a legal hold if required. Adverse decisions are not made solely by a model. Communications avoid exposing another party's documents. Policy changes do not rewrite earlier accepted coverage; a legal hold overrides ordinary deletion until lifted.

## Acceptance and metrics

Claims filed against an earlier policy are evaluated against that version, subject to legal review. An ineligible or expired claim cannot be denied without a reason and appeal information. An approver without financial authority cannot execute compensation. Track claim frequency per completed transaction and resolution percentile by cohort, policy and disposition; no target is implied.
