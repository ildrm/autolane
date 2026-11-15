# Secure file handling

| Metadata | Value |
|---|---|
| Document ID | 14/05_SECURE_FILE_HANDLING |
| Version / status | 0.3 / proposed; security and legal review required |
| Owner | Application Security Lead |
| Reviewers | Product, Architecture, Security, Privacy, Operations, QA |
| Updated | 2026-11-15 |
| Scope | Secure file handling for proposed marketplace; applicable legal obligations remain unresolved. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [business and operations](../01_BUSINESS_MODEL_AND_OPERATIONS.md). |

## Upload and retrieval lifecycle

The client requests a scoped, short-lived upload authorization tied to an allowed case, file class, maximum size and permitted media types. The object lands in a non-public quarantine location. Server-side processing checks actual content signature, size, archive expansion limits, malware scan result and image decoding; strip unnecessary metadata including GPS unless required and approved. Assign a server-generated opaque key; never trust a filename as a path. Pending, failed and rejected files are not published or retrievable by customers.

After successful scanning, a privileged service records checksum, case, owner, classification, scanner version and status and moves or copies the object to controlled storage. Authorized access is checked against current case, role and organization before a short-lived download link or proxy response; use safe content disposition, non-executable origin and content security policy. Published report references immutable evidence versions. A rescan finding revokes access and creates a security case; corrections never erase an audit trail.

## Failure and acceptance

An expired upload authorization or mismatched case cannot attach a file. Renamed executable, oversized archive, SVG script or failed scan remains inaccessible. Duplicate upload retries yield one attachment when supplied the same idempotency key. Verify that another dealer cannot access an unexpired link after revocation where the chosen delivery architecture requires immediate revocation; if direct signed URLs prevent this, use a proxy for highly restricted classes and document the maximum residual access window.

## File lifecycle and retrieval contract

`createUploadGrant` binds one principal, purpose, expected type/size, owning record and short expiry. Uploaded bytes enter quarantine; file states progress `awaiting_upload → scanning → clean|rejected`, with `expired` for unused grants and `deleted` only after retention/hold evaluation. A claimed extension or MIME header is insufficient: verify actual format, bounded decompression/image dimensions and scanner result. Scanner outage remains pending and never defaults clean. Replaced bytes produce a new file/version and checksum; a clean verdict cannot be reused for changed content.

Only clean files can attach to a report, contract, payment or title command; both attachment and download recheck ownership, purpose and current grants. Highly restricted evidence uses an authenticated proxy that reauthorizes access; ordinary permitted short-lived download grants are nontransferable where platform capability allows and may remain usable until their bounded expiry, which must be disclosed in security review. Default disposition is attachment with safe filename and no active same-origin execution. Public media is a distinct rights-reviewed derivative with identifying metadata/redactions, not a public flag on the raw evidence object.

Negative fixtures include executable renamed as image, oversized dimensions, decompression bomb, malware, stale grant after role revocation, cross-case file ID, changed bytes after scan, missing checksum and denied preview. Cleanup must not remove a held or published evidence version; orphan quarantine deletion uses approved retention policy and an auditable inventory.
