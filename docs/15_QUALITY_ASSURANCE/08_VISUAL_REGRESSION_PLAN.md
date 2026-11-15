# Visual regression plan

| Metadata | Value |
|---|---|
| Document ID | 15/08_VISUAL_REGRESSION_PLAN |
| Version / status | 0.1 / proposed; review required |
| Owner | Design QA Lead |
| Reviewers | Product, QA, Engineering, Operations, Security, Design |
| Updated | 2026-11-15 |
| Scope | Visual regression plan for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [release quality gates](10_RELEASE_QUALITY_GATES.md). |

## Scope and baseline

Capture deterministic screenshots for approved component variants and representative seller, dealer, branch, inspection, support and finance workflows at mobile, tablet and desktop widths. Include empty, loading, error, denied, validation, long text, large text, keyboard focus, high contrast and reduced-motion states. Seed fixed data, timezone, fonts, imagery and viewport; disable or freeze animation, random values and countdown time so genuine visual differences are detectable.

Compare perceptual diffs with region masks only for documented dynamic areas; an overbroad mask must not hide price, status, legal text or focus changes. Each baseline change requires design review with build, reason and screenshots; never blindly approve all diffs after a dependency update. Check color contrast and accessible semantics separately because screenshots alone cannot establish either. Test right-sized asset loading and small-screen layout without leaking private data.

## Acceptance

No clipped action, hidden error, overlapping price or unintelligible focus state appears in critical flows. Approved changes update baseline with reviewer identity; unreviewed differences block the affected release. A false positive creates a reproducible fixture fix, not an undocumented tolerance increase.
