# Color system

**ID:** 06/05_COLOR_SYSTEM · **Version:** 0.1 · **Status:** PROPOSED; no trademark, asset or stakeholder approval · **Owner:** Design systems lead · **Reviewers:** Brand, accessibility, UX, frontend · **Updated:** 2026-11-15

## Semantic use
Use ink for primary text, muted ink for secondary text, white/paper as primary surfaces and teal for the primary action. Success, warning, danger and informational colors convey additional meaning only with an icon and explicit text. Never paint a transaction “success” solely because an auction closed: the actual state label determines presentation. Currency, reserve and confidential bid information do not receive color-based disclosure semantics.

| State | Light surface | Foreground | Required label |
|---|---|---|---|
| Neutral | `#F6F8F7` | `#10212A` | e.g., Pending review |
| Success | `#E8F5EC` | `#176638` | e.g., Confirmed |
| Warning | `#FFF4DB` | `#805000` | e.g., Action required |
| Error | `#FCE8E8` | `#A12628` | e.g., Not confirmed |
| Informational | `#E8F2FA` | `#235C91` | e.g., In progress |

Calculated WCAG relative-luminance contrast for the listed foreground/background pairs, in table order: 6.25:1, 6.27:1, 6.32:1, 6.15:1; white on teal `#075A5A` is 8.02:1. These calculations cover only the exact solid colors shown; measure actual rendered states, focus indicators, overlays and dark-theme pairings before approval. Use 4.5:1 normal text and 3:1 large text; graphical controls and focus indicators must satisfy applicable non-text contrast, and link identification must not rely on color. High-contrast settings need native system colors or equivalent visible borders. In dark theme reassign semantic values; never invert photos or status colors blindly. Disabled buttons should explain why through visible adjacent text where interaction is blocked; do not rely on low contrast to convey ineligibility.

## Verification
Audit action text, placeholder, status badge, icon, graph, hover, pressed, error and focus in both themes with automated checks plus manual testing. Review color vision deficiency and grayscale. Document actual ratio, background and component state in design handoff; if a pairing fails, change the pair, not the text's meaning.
