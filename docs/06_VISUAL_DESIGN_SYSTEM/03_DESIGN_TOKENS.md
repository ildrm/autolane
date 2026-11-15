# Design tokens

**ID:** 06/03_DESIGN_TOKENS · **Version:** 0.1 · **Status:** PROPOSED; no trademark, asset or stakeholder approval · **Owner:** Design systems lead · **Reviewers:** Brand, accessibility, UX, frontend · **Updated:** 2026-11-15

## Scope and naming
Values below are proposed design tokens in CSS pixels; they are documentation values, not source code. Figma variables use `category/role/state` (e.g., `color/text/primary`, `space/4`, `motion/duration/standard`). Components consume semantic aliases rather than hard-coded primitive colors. Light is default; dark is opt-in after contrast and image treatment review. Themes must not change transaction semantics.

| Category | Primitive values / semantic mapping |
|---|---|
| Ink | `ink/950 #10212A`, `ink/700 #314953`, `ink/500 #657A82` |
| Neutral | `white #FFFFFF`, `paper #F6F8F7`, `border #CBD5D5` |
| Accent | `teal/800 #075A5A`, `teal/700 #086B69`, `teal/100 #D8F2EF` |
| Status | `success #176638`, `warning #805000`, `danger #A12628`, `info #235C91`; use text/icon labels as well. |
| Semantic light | `text/primary=ink/950`, `text/secondary=ink/700`, `surface/base=white`, `surface/subtle=paper`, `action/primary=teal/800`, `focus=#005FCC`. |
| Semantic dark | `surface/base=#10212A`, `surface/subtle=#1B313B`, `text/primary=#F6F8F7`, `text/secondary=#D3DEDE`, `action/primary=#79D6C8`, `focus=#A9D5FF`; verify each state against its actual background. |
| Space | `1=4`, `2=8`, `3=12`, `4=16`, `5=24`, `6=32`, `7=48`, `8=64`, `9=96`; use 4px grid. |
| Shape and borders | Radius `small=4`, `control=8`, `card=12`, `pill=999`; border `default=1`, `focus=2` plus 2px offset. |
| Typography | Sans family selected after license/coverage review; `12/16`, `14/20`, `16/24`, `20/28`, `24/32`, `32/40`, `48/56`, `64/72`; weights 400, 500, 600, 700. |
| Elevation | Level 0 none; 1 card `0 2 8 rgba(16,33,42,.08)`; 2 popover `0 8 24 rgba(16,33,42,.16)`; 3 modal `0 16 48 rgba(16,33,42,.24)`. Elevation is not the sole grouping cue. |
| Layout | Breakpoints 600, 1024, 1440; content max 1280; compact/medium/wide page margins 16/24/32. |
| Motion | duration instant 0ms, quick 120ms, standard 180ms, emphasis 240ms; easing `cubic-bezier(.2,0,0,1)`; reduced motion 0ms for translation/scale. |
| Controls | Input height 48, compact staff control 40 where touch target and spacing still satisfy WCAG; focus indicator and error icon remain visible. |

## Verification
Check exact foreground/background pairings and gradients, normal text ≥4.5:1, large text ≥3:1 and applicable non-text ≥3:1; correct any failing pair before release. Do not infer compliance from palette names. Confirm dark-mode focus and disabled descriptions, high-contrast OS mode, typography fallback and asset rendering. Token change requires design and accessibility review, visual regression and versioned migration notes.

## Structured values and measured pair checks

[Design-token values](../contracts/design-tokens.json) encode the palette, spacing, breakpoints and motion durations as a documentation artifact. [Contrast results](../review/contrast-validation.json) calculate12 selected foreground/background pairs using relative luminance. All must meet their declared text/non-text threshold; this checks solid token pairs only, not rendered components, gradients, hover/disabled states or overall accessibility conformance.
