# Dealer Credit Policy

| Metadata | Value |
|---|---|
| ID / version | 12/05_DEALER_CREDIT_POLICY / 0.1 |
| Status | Proposed; legal, finance and auction policies unapproved |
| Owner / reviewers | Auction and finance architecture / legal, operations, security, QA |
| Updated | 2026-11-15 |
| Scope | Dealer Credit Policy; no authority to transfer funds or ownership is implied. |

## Default and alternatives
**DECISION REQUIRED:** no dealer credit facility is approved. By default a dealer's ability to bid is based only on approved eligibility and policy; no credit limit, loan, deposit or collateral is implied. Phase 1 must not create, price, extend or display a credit facility as available without a separate product decision, licensed-provider agreement and legal review.

If approved later, record lender/provider, applicant organization and consent, product terms, currency, limit, available amount, expiry, outstanding utilization, underwriting decision reference and policy version. Restrict access to authorized finance/risk staff and the relevant dealer; never expose another dealer's credit state. The lender decides credit eligibility and communicates disclosures; the platform records responses but must not promise approval. Any atomic reservation against an approved limit must release on cancellation/expiry under an approved policy and reconcile to provider records.

Provider timeout results in pending/unknown, not approval. Handle declined or expired facility by informing the dealer and offering permitted alternatives; never automatically cancel a valid bid unless the published rules permit. Risk review must cover concentration, default, repayment, consent, fraud, adverse decision review and audit. Acceptance requires legal approval, complete provider contract, independent reconciliation, access tests and documented customer disclosures.
