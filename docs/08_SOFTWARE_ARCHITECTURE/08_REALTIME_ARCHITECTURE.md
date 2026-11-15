# Realtime Architecture

| Metadata | Value |
|---|---|
| ID / version | 08/08_REALTIME_ARCHITECTURE / 0.1 |
| Status | Proposed specification; no stakeholder approval |
| Owner / reviewers | Architecture and data leads / product, security, operations, QA |
| Updated | 2026-11-15 |
| Scope | Realtime Architecture; jurisdiction-dependent policy decisions remain open. |

## Authoritative bid and update protocol
Commands use HTTPS and idempotency; authenticated WebSocket channels carry only scoped auction snapshots and updates. On connection authenticate session, authorize every auction subscription, send latest authoritative snapshot with monotonic auction version, then updates. Client discards older versions and resyncs on gaps, reconnect, foreground resume or uncertain command outcome. A stream update is informational: only the committed command response or subsequent authoritative snapshot establishes acceptance.

Server time is authoritative. Deliver server timestamp and close time; client countdown is an estimate and announces meaningful state changes accessibly rather than every tick. Gateway fanout can duplicate or reorder; sequence numbers detect the problem. If clock health is uncertain or primary storage unavailable, reject new bids as temporarily unavailable and prevent final close until safe recovery; publish a truthful status rather than invented time. Do not accept offline bids.

**Proposed initial verification targets, not measured:** accepted bid commit p95 ≤500 ms and update observed p95 ≤1 s within one region at the agreed representative load; final SLOs require capacity testing, network boundaries and operational approval. Test reconnect, revoked access, duplicate messages, slow consumers and time boundary races. Private bidder identity and reserve remain hidden except where approved policy grants visibility.
