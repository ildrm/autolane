# Form Implementation Spec

| Metadata | Value |
|---|---|
| ID / version | 11/06_FORM_IMPLEMENTATION_SPEC / 0.3 |
| Status | Proposed, pending design and product review |
| Owner / reviewers | Frontend architect / design, accessibility, security, QA |
| Updated | 2026-11-15 |
| Scope | Form Implementation Spec, initial English LTR release. |

## Input and validation
Seller form collects vehicle taxonomy, year, mileage, location and minimal contact/consent; dependent make/model/trim controls clear invalid child choices explicitly. Appointment selection uses server-provided branch-local times and reserves atomically. Dealer verification collects only approved identity fields and uploads. Monetary forms parse locale-aware display into integer minor units according to currency exponent, reject ambiguous/negative or overflow amounts and preserve original text until confirmed. Never use binary float as authority.

Validate on blur and submit; server error remains authoritative. Associate visible label, hint and error using accessible relationships; on failed submit focus an error summary and preserve valid entries. For multi-step flows announce step and save allowed non-sensitive draft; expiring sessions preserve only appropriate data. Consent checkboxes default unchecked, identify version and link terms. Documents upload through scoped short-lived authorization, show scanning/pending/rejected states, and do not expose private URLs. On `409`, refresh affected values and ask user to review; on timeout for bid or finance use the same idempotency key to reconcile rather than resubmit as a new action. Test keyboard, mobile input, screen reader errors, duplicate submission and timezone boundary.

## Submission and focus details

Every field specification resolves to a request-schema property, required/optional/null semantics, label, hint, bounded length/range and safe validation copy. Server-derived IDs, preparer/reviewer, scope, status and approved timestamps are not editable hidden fields. Conditional forms show and require only fields relevant to the chosen transition; changing an action clears values that no longer apply. A consent checkbox references the exact notice/terms version and is distinct from optional marketing permission.

The first invalid submission announces “There are N fields to review.” and focuses the linked error summary, then allows direct navigation to each field. Validation never clears a valid file attachment or unrelated text. A destructive confirmation describes object, consequence and alternatives, with Cancel initially focused. A price, contract or title confirmation shows exact currency, amount, party and evidence version; fresh step-up is requested only after the intended command is reviewable. Closing that challenge preserves the unsubmitted intent. Browser autofill and password managers must remain usable; pasting credentials and verification codes is permitted.

Date-only inputs remain dates; appointments send server slot IDs, not client-converted local timestamps. The displayed timezone is explicit. Evidence upload errors distinguish file too large, unsupported type, scan pending, rejected and expired grant; a retry gets a new upload grant while retaining the document's logical purpose. The upload is not itself publication or approval.
