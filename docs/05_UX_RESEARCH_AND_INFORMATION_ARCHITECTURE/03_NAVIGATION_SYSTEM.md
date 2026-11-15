# Navigation system

**ID:** 05/03_NAVIGATION_SYSTEM · **Version:** 0.1 · **Status:** PROPOSED, subject to research and stakeholder review · **Owner:** UX lead · **Reviewers:** Product, accessibility, operations, engineering, legal · **Updated:** 2026-11-15

## Global structure
Public header has logo/home, Sell, Buy, Value, Branches and How it works; secondary Help, dealer entry and Sign in. At 1024px and above show full nav; below use labeled Menu opening a modal drawer with the same order, Close and Escape. Do not conceal essential Sell action behind hover. Current destination has text and visual indicator with `aria-current`; menu buttons expose expanded state and linked panel. Header remains in flow where sticky positioning obscures content at 200% zoom.

Seller and dealer accounts have a labeled identity switcher only when one person has multiple authorized contexts. Switching reloads scoped data and clears context-sensitive UI. Staff desktop uses collapsible left rail plus top search and profile; mobile drawer holds the same authorized destinations. Display organization and branch scope near the page title; never offer an action solely because its link is hidden.

## Interaction contract
Tab and Shift+Tab traverse visible controls; Enter/Space activates buttons; Escape closes an open drawer and returns focus to its opener. Focus moves to the new page heading after client-side navigation; back returns to previous list/filter/scroll context where possible. Breadcrumbs describe hierarchy, not browser history; only ancestors are links. Opening an auction in another tab does not alter the first tab's authoritative state. Dirty forms trigger a native or accessible in-product confirmation before intentional navigation; confirm with server whether saved before claiming a draft exists.

## States and edge cases
When an account loses permissions while open, remove privileged actions on the next server response, preserve non-sensitive unsaved text only when policy allows, show “Your access has changed. Contact your administrator.” A failed navigation retains the current screen with retry; an expired session opens sign-in and returns only to a validated internal destination. No navigation tab changes an auction or transaction state by itself.

## Acceptance
Keyboard-only operation must open and close all navigation patterns, maintain visible focus, avoid focus traps outside modal drawers and restore focus after dismissal. Test at 320px, 768px, 1024px and 1440px widths and at 200% text zoom. A role with no module permission cannot access its target by typing a URL.
