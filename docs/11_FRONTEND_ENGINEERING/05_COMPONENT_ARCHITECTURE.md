# Component Architecture

| Metadata | Value |
|---|---|
| ID / version | 11/05_COMPONENT_ARCHITECTURE / 0.3 |
| Status | Proposed, pending design and product review |
| Owner / reviewers | Frontend architect / design, accessibility, security, QA |
| Updated | 2026-11-15 |
| Scope | Component Architecture, initial English LTR release. |

## Ownership and contracts
Organize shared primitives (buttons, inputs, dialogs, status, typography), domain composites (vehicle card, inspection summary, auction bid panel) and route screens separately. Components receive typed data and callbacks; they do not directly call privileged endpoints or infer user authorization. Design tokens provide consistent light/dark, focus, color and motion behavior; visible labels and text convey all status alongside color.

| Composite | Inputs and behavior | Required states |
|---|---|---|
| Vehicle card | Published vehicle, price/currency and availability | Loading, available, unavailable, image fallback; entire interactive target is keyboard accessible. |
| Bid panel | Snapshot, permissible increment, connection state, action callback | Ready, pending, accepted, rejected, unknown, closed and denied; never assert acceptance until committed. |
| Inspection report | Authorized immutable revision and findings | Loading, restricted, incomplete, published and revised; link findings to evidence only when permitted. |
| Financial status | Obligation, verified evidence and reconciliation state | Pending, discrepancy, reconciled; do not label money paid based on uploaded evidence. |

Test components at narrow and wide viewport, keyboard, screen reader labels, reduced motion, error handling and visual contrast. Version component APIs with design review; changes affecting semantics require accessibility review.

## Component acceptance matrix

| Component | Controlled values and emitted intent | Important contract fixture |
|---|---|---|
| MoneyInput | Original text, currency metadata and parsed safe integer; emits draft and valid minor units | Unsupported currency, zero where prohibited, separator ambiguity and safe-integer overflow. |
| AppointmentPicker | Branch timezone, available server slot IDs and selected slot | Last slot conflict refresh preserves branch/date, DST duplicate local labels include offset. |
| EvidenceUploader | Upload grant, bytes progress, file ID and scan state | 100% upload still scanning; rejected scan never yields an attachment action. |
| StateBadge | Canonical state plus plain English label and icon | Text alone communicates state under grayscale/forced colors. |
| ApprovalDiff | Immutable before/after revision, evidence and authorized action | Same person as author sees denial, not enabled approval. |
| AsyncExport | Filter snapshot, purpose, job status and download expiry | Revoked scope hides downloadable link even if job completed earlier. |
| DataTable | Stable row ID, sort/filter/page, selected IDs and capabilities | Selection reconciles when row disappears; action reports individual failures. |
| CaseTimeline | Ordered authoritative event projection and freshness | Duplicate event ignored; unknown actor displayed safely, no fabricated milestone. |

Composites receive formatted presentation objects; raw contract documents and access tokens are never serialized into story fixtures. Each semantic change increments its component contract version and updates associated accessibility, empty/error and visual fixtures. Standard UI wording comes from the English content dictionary; domain states must not be guessed from translated display strings.
