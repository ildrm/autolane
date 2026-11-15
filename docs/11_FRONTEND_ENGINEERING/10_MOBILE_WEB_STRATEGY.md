# Mobile Web Strategy

| Metadata | Value |
|---|---|
| ID / version | 11/10_MOBILE_WEB_STRATEGY / 0.3 |
| Status | Proposed, pending design and product review |
| Owner / reviewers | Frontend architect / design, accessibility, security, QA |
| Updated | 2026-11-15 |
| Scope | Mobile Web Strategy, initial English LTR release. |

## Device strategy
Start with responsive browser experiences rather than assuming native distribution; prioritize seller intake, dealer bidding and inspector field work. Layout flows from single-column narrow views to wider dashboard tables; important bid status and action remain visible without obscuring content. Offer numeric keypad for amounts while preserving currency and validation; touch targets and clear focus must meet the accessibility standard. Users can rotate, zoom, use keyboard and switch to a low-bandwidth mode without losing access.

Inspectors may record an **unsubmitted** local draft only if security, consent, retention and device policy approve; uploaded evidence must be scanned and server-confirmed. Do not cache identity documents unencrypted or accept offline bids, payment claims or signatures as authoritative. On background resume, expired auth, network change or reconnect, refresh auction snapshot and verify the current dealer scope. Evaluate PWA push and platform restrictions through device testing, then compare React Native, Flutter and native applications against measured need for camera, offline, notifications and operational support. No native application is assumed for MVP.

## Field conditions and offline decision

Foundational release is online-only for all binding actions and sensitive inspector evidence. Optional offline inspection drafts remain disabled until a separate managed-device security design is approved. If enabled later, a draft requires device encryption, user-bound storage, expiry, logout wipe and explicit conflict resolution against server revision; it must never auto-publish on reconnect. Camera capture previews image, orientation and legibility, strips unnecessary location metadata and provides file-picker fallback. Upload grants expire independently from draft intent; resumed upload revalidates scope and scan status.

Test a low-memory phone, throttled/interrupted connection, background suspension, orientation change, camera permission denial, 200% text and virtual keyboard covering the CTA. Sticky actions respect safe areas and never obscure error messages or focused fields. A provider redirect preserves a server-held correlation reference, validates same-origin return targets and restores pending state after reauthentication. Push notification content contains no sensitive price, identity or financial details visible on a lock screen; delivery never constitutes proof a deadline was seen. Native investment requires measured browser limitations and an owner-approved operating-cost comparison.
