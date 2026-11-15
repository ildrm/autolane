# Component states and feedback

**ID:** 06/08_COMPONENT_STATES · **Version:** 0.1 · **Status:** PROPOSED; no trademark, asset or stakeholder approval · **Owner:** Design systems lead · **Reviewers:** Brand, accessibility, UX, frontend · **Updated:** 2026-11-15

## State precedence
Treat disabled, pending, error and success as explicit states; do not rely only on opacity or color. For submit controls the accepted server outcome outranks optimistic animation. On a network timeout where a bid or decision may have succeeded, show “Checking…” and query authoritative history; never claim failure or enable a second independent submission until the outcome is reconciled. If permissions change, replace action with explanation and safe navigation; server authorization remains decisive.

| State | Visual/content | Interaction and accessibility |
|---|---|---|
| Default | Normal token surface, label, helper as needed. | Enabled and keyboard reachable. |
| Hover | Slight surface change on pointer devices. | Must not reveal required information exclusively. |
| Focus | 2px visible focus ring with 2px offset, sufficient contrast. | Never clipped or obscured by sticky content; focus order follows task. |
| Pressed | Clear pressed color/border and optional 120ms feedback. | Announce toggle state through appropriate semantics. |
| Disabled | Label and reason visible, e.g., “Available after verification.” | Prefer explanation adjacent; preserve reading and discoverability. |
| Loading | Reserved size and text “Loading…” or “Checking…”. | Announce status politely; prevent duplicate action; no indefinite shimmer. |
| Error | Field message plus summary, icon and semantic danger. | Focus summary on submit; link to field; preserve user data. |
| Success | Specific confirmed outcome and next step. | Announce once; do not assert settlement, sale or title beyond known fact. |
| Empty | Explain why empty and give a safe action when available. | Remains meaningful to a screen reader and keyboard user. |

For auction updates, announce own bid result and relevant outbid status; countdown ticks are visual and not live-announced repeatedly. Avoid toast-only critical information. If error resolution affects money, show the authoritative outcome, timestamp and support reference. Test each state with slow network, concurrent edits, revoked access, reduced motion, keyboard and screen reader.
