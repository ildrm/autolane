# Vehicle And Inspection Api

| Metadata | Value |
|---|---|
| ID / version | 10/05_VEHICLE_AND_INSPECTION_API / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Backend and architecture leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Vehicle And Inspection Api; commercial and jurisdiction-dependent policy decisions remain open. |

## Vehicle and report contract
| Operation | Input and actor | Validation / result |
|---|---|---|
| `GET /v1/vehicle-taxonomy` | Public make/model/trim query | Return only active taxonomy; version and stable cursor, no VIN. |
| `POST /v1/seller-leads` | Seller, vehicle attributes, contact, consent version | 201 lead; year, mileage and taxonomy valid; no automatic merge of suspected duplicates. |
| `POST /v1/inspections/{id}/revisions` | Assigned inspector, template version, findings and scanned evidence references | 201 draft; item IDs belong to template, severity allowed, no unscanned file. |
| `POST /v1/inspections/{id}/publish` | Supervisor with version and reason | 200 published immutable revision if mandatory items and evidence complete; 412 on failed `If-Match` precondition. |
| `GET /v1/inspections/{id}/reports/{revision}` | Seller, eligible dealer or scoped staff | Return role-permitted view; deny cross-branch/organization and unapproved internal notes. |

Vehicle identity and documents are private; VIN may be collected only where policy permits. Upload through short-lived object-scoped credentials, scan before publication and verify MIME, size and content signature. Corrections create new revision, preserve the prior published state, flag affected auctions and require a reviewed decision on pause/notification. Auction references the exact revision bidders saw. Tests: missing required finding, stale publish, prohibited document, malware, report correction while auction open, unauthorized cross-tenant access.
