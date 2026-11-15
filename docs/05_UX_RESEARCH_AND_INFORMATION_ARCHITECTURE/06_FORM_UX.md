# Form UX and validation

**ID:** 05/06_FORM_UX · **Version:** 0.1 · **Status:** PROPOSED, subject to research and stakeholder review · **Owner:** UX lead · **Reviewers:** Product, accessibility, operations, engineering, legal · **Updated:** 2026-11-15

## Principles
Use one question per meaningful decision, visible persistent labels and plain English. Required fields are marked in text; optional fields are labeled optional. Divide seller onboarding into vehicle, contact and appointment; show progress as “Step 1 of 3” and explain that a request is not a sale. Provide Back without data loss. Use semantic input types and autocomplete where suitable; do not enforce unsupported assumptions about phone format, address or vehicle identifiers before jurisdiction is selected.

## Field contract
| Field | Validation and behavior | Error copy |
|---|---|---|
| Make/model/variant | Make and model required; reset dependent selection only after confirmation if already populated; variant may be unknown. | “Select a make and model.” |
| Year | Four-digit year within configured taxonomy range; do not infer current model year. | “Enter a valid model year.” |
| Mileage | Nonnegative integer and explicit km/mi, honor configured market maximum; show chosen unit. | “Enter a valid mileage and select a unit.” |
| Contact | Require configured contact channel; normalize server-side; verify if policy requires; allow accessible paste and password managers. | “Enter a valid contact detail.” |
| Consent | Required service terms and optional marketing are separate unticked choices; link to versioned text. | “Review and accept the required terms to continue.” |
| Branch/slot | Confirm branch, timezone and an available server-issued slot; reserve atomically on submit. | “That time is no longer available. Choose another time.” |
| Bid | Exact decimal amount and ISO currency; show current minimum and policy-defined increments; server makes final decision. | “The minimum bid has changed. Review the current amount.” |
| Photos/documents | Explicit allowed types and size from policy; scan server-side; accessible list and remove control. | “This file could not be uploaded. Try another file.” |

Validate format on blur and all required fields on submit; use a linked summary with focus plus field-level error. Do not clear input on errors. Timeouts leave state “checking” where a duplicate action could have financial consequences. Autosave excludes sensitive information unless approved; show Saved only after acknowledgment, distinguish unsaved and error, support resume after authentication and expire drafts under policy. OTP errors do not reveal account existence; allow resend with rate limits and a support alternative. CAPTCHA, if necessary, must have an accessible alternative.

## Privacy and acceptance
Explain why contact, location, documents and consent are needed before collection; link to privacy notice and do not reuse marketing consent as a condition of service unless approved by legal. Validate all rules on server and preserve accessible error links, keyboard completion and mobile input. Test empty, malformed, min/max, expired session, duplicate submission, stale slot, network outage and refresh/back cases. Research whether a shorter field sequence improves completion without increasing corrections.
