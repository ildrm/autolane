# Realtime Ui

| Metadata | Value |
|---|---|
| ID / version | 11/07_REALTIME_UI / 0.3 |
| Status | Proposed, pending design and product review |
| Owner / reviewers | Frontend architect / design, accessibility, security, QA |
| Updated | 2026-11-15 |
| Scope | Realtime Ui, initial English LTR release. |

## Dealer auction interaction
1. Fetch `GET /v1/auctions/{id}` with active organization and render snapshot sequence and server time.
2. Authenticate a scoped stream and subscribe to the auction. Apply only updates newer than the current sequence; on gap, reconnect or organization change discard unverified deltas and refresh snapshot.
3. Display current bid and local countdown from server time; countdown is illustrative, never authoritative. Announce state changes and bid outcomes, not each second.
4. Validate currency and minimum input locally as a hint; submit with idempotency key. Disable duplicate submit while request pending, but permit safe recovery using the same key after timeout.
5. On accepted response show amount and sequence; on definitive rejection provide specific recovery. On unknown response show “Confirming your bid” until replay/snapshot resolves it. On disconnect show “Connection lost; reconnecting” and disable new bidding until state is trustworthy.
6. At close show recorded result only after server snapshot; seller acceptance, contract and settlement remain separate.

Never reveal other bidders' identity or reserve absent approved policy. Support keyboard and screen readers; reduced motion removes pulses and transitions but preserves status. Test delayed, dropped, reordered, duplicate, unauthorized and revoked subscriptions.

## Snapshot and stream reconciliation detail

A snapshot includes aggregate version and `server_time`; stream subscription acknowledges its starting sequence. If subscription starts after snapshot retrieval, the gateway replays the bounded gap or requires a new snapshot before applying updates. Never assume “fetch then subscribe” is race-free. Apply contiguous newer events; duplicates at or below applied sequence are ignored. A jump beyond the next expected sequence marks the view stale and performs one deduplicated snapshot request; buffer at most 100 events for at most 5 seconds, then discard and resubscribe. A slow client is disconnected with a resync reason rather than accumulating unbounded memory.

Reconnect backoff is 1, 2, 4, 8, 16 then 30 seconds with jitter; successful snapshot resets it. A 401/403 stops reconnect until reauthentication/authorization succeeds. Browser visibility resume refreshes scope and snapshot before enabling bidding. Polling fallback is read-only at 5-second intervals while visible, subject to server rate controls; poll responses never prove the client's pending bid without its own command receipt. Keyboard focus stays on the user's control when the leader or countdown updates. Live-region output is coalesced so other bidders' rapid activity does not make the form unusable.
