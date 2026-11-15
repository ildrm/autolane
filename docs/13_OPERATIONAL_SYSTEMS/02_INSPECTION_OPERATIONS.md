# Inspection operations

| Metadata | Value |
|---|---|
| Document ID | 13/02_INSPECTION_OPERATIONS |
| Version / status | 0.1 / proposed; requires domain review |
| Owner | Inspection Operations Lead |
| Reviewers | Operations, Product, Security, Legal, QA |
| Updated | 2026-11-15 |
| Scope | Inspection operations for the proposed marketplace; jurisdiction and transaction model remain open. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Workflow

An authorized inspector opens an assigned, checked-in case and verifies vehicle identity and document completeness. The selected jurisdiction-specific checklist is versioned and comprises configurable sections and points, including body, paint, chassis, mechanical, electrical, interior, tyres and road test when permitted. Each applicable point records result, severity, comment, evidence and inspector; not-applicable requires reason. The checklist may model 145 points but does not claim to reproduce the reference company's proprietary list.

Inspections move **draft → submitted → supervisor review → published**, with return-to-draft for correction. Submission requires all mandatory items and evidence; only a supervisor with review permission can publish. The published report references immutable vehicle identity, checklist version, evidence versions, timestamps and author/reviewer. A subsequent correction creates a new version and reason; prior versions remain available to authorized auditors. A potentially material correction after auction publication pauses affected processing for an auction manager and legal review; the customer and dealers are informed as determined by approved policy. Do not silently replace the report relied on by bidders.

Uploads enter quarantine, are scanned and bound to the case before controlled access; failed or pending scans cannot be published as evidence. Inspectors see assigned cases, reviewers see scoped branch cases, and dealers see only the released report permitted by policy. Offline capture, if introduced, requires encrypted local storage, expiry and conflict review; it is not an MVP assumption.

## Quality and exceptions

A supervisor may reject a report with item-level feedback; unavailable equipment, unsafe road test, document mismatch or missing VIN stops affected checks and creates a task, not a fabricated pass. Record disagreements as support cases referencing report version. An inspection is not automatically a warranty, and customer-facing coverage needs approved terms.

## Acceptance and tests

Publishing an incomplete mandatory checklist fails without changing state. An inspector cannot approve their own report unless a separately approved exception policy permits it. Report correction preserves the published original, initiates the materiality review and produces an audit event. A malware-positive upload is never served to dealers.
