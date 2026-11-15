# Field constraints and persistence contract

**ID:** DATA-CONSTRAINTS · **Version:** 0.3 · **Status:** proposed · **Owner:** Database architect · **Reviewers:** Domain owners, security, privacy, finance · **Updated:** 2026-11-15

## Type and null semantics

The dictionary's `!` is required and `?` nullable. A missing value is unknown; it never means verified, consented, zero, paid or approved. Every aggregate has UUID id, positive bigint version, UTC created_at/updated_at and owner context. Version starts at 1, increments once per successful state mutation. Append-only Bid, signature, journal and audit records do not use mutable version semantics. API projection fields may be omitted for scope/redaction; persistence-required fields cannot silently become optional.

| Field class | Logical database type and bounds | Validation / index / security |
|---|---|---|
| Entity reference `*_id` | UUID, nullable only where dictionary says optional | FK or explicit owning-context existence check; never authorize by UUID possession; index hot lookup FKs. |
| `*_at`, start/end, expiry | timestamptz, UTC API RFC3339 Z; maximum millisecond presentation precision | Compare instants, not formatted local text; start < end; expiry monotonic policy check. |
| Local date/time and timezone | date / time without zone plus IANA zone text ≤64 | Generate slots as unambiguous instants; DST gap invalid, overlap requires explicit offset/slot. |
| Monetary amount | bigint exact minor units, API absolute value ≤9,007,199,254,740,991; currency text exactly 3 uppercase letters | Configured ISO currency/exponent; amount >0 for bids/obligations; matched/refund counters ≥0; signed adjustments only; no floating point or cross-currency addition. |
| Counts / sequence / capacity | bigint ≥0; accepted auction sequence ≥1; maximum browser-safe integer for API | Unique auction/sequence; reserved ≤ capacity; enforce inside transaction. |
| Names, labels, controlled codes | text, trimmed 1–200 Unicode characters unless explicit schema smaller | Slug normalized `[a-z0-9]+(-[a-z0-9]+)*`, ≤120; unique per namespace; never silently merge identity based on normalized name. |
| Narrative reason/comment | text ≤2,000; support description ≤5,000 | Output encoded; no raw identity/payment secrets; purpose-limited and access scoped. |
| Email / phone | normalized text ≤254 / E.164-formatted ≤16 characters after verified country parsing | Input raw phone accepts bounded formatting then validates; verification timestamp and change history; reverify changed identifier. |
| Checksum | 64 lowercase hex SHA-256 | Hash exact immutable document bytes; cannot replace signature identity or provider verification. |
| Evidence/media pointer | UUID referring to protected File record | Clean scan, matching case and permissible kind; no permanent public object URI; immutable revision link. |
| Status | finite enum from state catalog | Reject unlisted transition; DB constraint or catalog FK; no client-selected arbitrary state. |
| Policy/template version | UUID plus immutable schema version | Current approval required for new cases; historic cases pin original version; never destructive cascade. |
| Idempotency key | printable ASCII 1–128 with principal+operation namespace | Unique tuple and canonical payload hash; replay current authorization; receipt/tombstone lifecycle from policy baseline. |

## Relational invariants

OrganizationMember is unique per organization/user with versioned grants and status. AppointmentSlot reservation and Appointment change commit atomically; old and new slot IDs lock in sorted order. InspectionFinding belongs to one draft revision and template point, unique on revision/point; **not** just inspection/point. An immutable published revision pins findings and clean evidence. Auction locks one vehicle channel claim to prevent concurrent live auction or consumer sale; historical auctions remain many-to-one. AuctionResult is unique per auction, winner references an accepted bid of that same auction, same currency and valid committed sequence. SellerDecision is unique per offer version/current decision and records actor, terms, time and consent evidence; acceptance/expiry serialize on offer.

TransactionCase references exact accepted result/decision, signed contract version, obligations, title record and custody record; no single boolean can replace these states. PaymentTransaction external key is unique on provider/source plus external reference; one payment may allocate to multiple obligations only through explicit allocation rows. Sum of allocations cannot exceed independently verified amount; lock payment and obligations consistently. Reconciliation stores prepared_by and approved_by, which must differ; reason required for discrepancy. Journal consists of header and at least two lines, balanced per currency; reversal links original journal and cannot update posted lines.

An upload record stores case_id, kind, byte size, actual MIME, checksum, scan result/version, quarantine key and authorized storage key; only clean state is downloadable. Legal hold links record scope, authority, reason, created_by, reviewed_at and released_by; erasure cannot ignore it. Outbox event ID and consumer inbox event ID uniqueness support at-least-once delivery; publishing order uses aggregate sequence, not wall-clock sorting.

## Deletion, indexing and acceptance

Do not cascade-delete financial, signed, published, bid, custody or audit evidence. Ordinary soft-delete is not a legal retention policy. Approved retention schedules govern restricted data with legal holds and processor propagation. Index (organization_id,status), (branch_id,status,due_at), (auction_id,sequence), (source_id,external_reference) and queue (status,next_attempt_at) where their measured query uses justify them; confirm plans with representative data before physical deployment.

Acceptance fixtures must reject a cross-auction winner, duplicate allocation, same-person reconciliation, published-finding overwrite, timestamp without timezone in the API, invalid currency and overflowing money sum. A correction preserves original evidence and produces a new version or compensating fact. These are logical requirements and documentation fixtures; no migration is generated.
