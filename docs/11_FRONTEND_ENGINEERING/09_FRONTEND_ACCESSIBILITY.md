# Frontend Accessibility

| Metadata | Value |
|---|---|
| ID / version | 11/09_FRONTEND_ACCESSIBILITY / 0.3 |
| Status | Proposed, pending design and product review |
| Owner / reviewers | Frontend architect / design, accessibility, security, QA |
| Updated | 2026-11-15 |
| Scope | Frontend Accessibility, initial English LTR release. |

## Interaction requirements
Meet WCAG 2.2 AA for initial English LTR experience, validated by automated and manual tests. All controls have visible labels, programmatic names, keyboard reachability and clearly visible focus. Preserve logical heading order and a skip link; dialogs trap focus while open and return focus to trigger. Do not rely solely on color, animation or sound for bid, validation or financial status. Status badges include text and contrast tested against their surface.

Forms associate field errors and hints and focus a concise error summary after submit. Auction messages use a polite live region for meaningful accepted/rejected/closed states, avoid a per-second countdown announcement, and expose current price and deadline as text. Respect reduced-motion preferences with no loss of function; pause optional auto-updating content where applicable without preventing authoritative updates. Provide descriptive image alternatives, accessible table headers, touch targets and zoom/reflow at 320 CSS pixels. Test screen readers, keyboard only, browser zoom 200%, narrow reflow, forced colors and loss of connection. Document exceptions with owner and remediation before release.

## Verification checklist with accountable outcomes

| Interaction | Manual test | Passing result |
|---|---|---|
| Navigation and dialogs | Keyboard only from page start; open/close nested confirmation | Logical focus order, no trap outside modal, visible focus restored. |
| Forms and authentication | Screen reader, invalid input, autofill, pasted code | Label/hint/error associated, no memory puzzle, correction preserves valid fields. |
| Live auction | Screen reader during rapid updates and reconnect | Meaningful accepted/rejected/disconnected state, no per-tick speech flood. |
| Zoom and reflow | 200% text, 400% browser zoom at 1280px, 320px CSS width | No lost action or two-dimensional page scrolling except essential data presentation. |
| Contrast and color | Test tokens in each state and forced colors | Text and controls meet applicable AA criteria; status remains understandable without color. |
| Touch and motor access | Narrow touch viewport, keyboard alternative to dragging | Product target 44×44 CSS px controls where practical; required WCAG target-size rules and exceptions checked explicitly. |
| Reduced motion | Enable OS preference before and during visit | Functional static fallback; no essential information lost. |

Accessibility owner records browser, assistive technology version, screen/fixture, observed result, severity and retest evidence. Automated rules cannot establish conformance alone. Release blockers include inaccessible bid/booking submission, unannounced errors, lost focus and content unavailable at zoom. Normative baseline: [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/); product target sizes above may exceed the standard's minimum and must not be mislabeled as the exact legal rule.
