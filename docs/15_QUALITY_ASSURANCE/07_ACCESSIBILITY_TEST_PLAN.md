# Accessibility test plan

| Metadata | Value |
|---|---|
| Document ID | 15/07_ACCESSIBILITY_TEST_PLAN |
| Version / status | 0.1 / proposed; review required |
| Owner | Accessibility QA Lead |
| Reviewers | Product, QA, Engineering, Operations, Security, Design |
| Updated | 2026-11-15 |
| Scope | Accessibility test plan for the proposed marketplace. |
| Related | [Discovery baseline](../00_MASTER_INDEX.md); [release quality gates](10_RELEASE_QUALITY_GATES.md). |

## Standard and coverage

Target WCAG 2.2 AA for public and operational web experiences. Accessibility review covers seller onboarding/booking, dealer auction, inspection reporting, finance review, authentication, CMS publishing, responsive layouts and the content templates. Evaluate with keyboard alone, screen readers on supported desktop and mobile combinations, 200% text scaling, 400% reflow, high contrast/forced colors, zoom and reduced motion. Use automated scanning as a partial check, not evidence of full conformance.

## Concrete checks

Every control has an accessible name, visible label, clear focus and logical order; error summaries link to invalid fields and validation is announced without losing entered values. Dialogs manage focus and allow escape where safe. Time limits provide legally and operationally valid accommodations; an auction's actual end remains server-authoritative, with accessible countdown and timely non-color status. Bid updates use an appropriate live region without announcing every transient tick. Tables preserve header associations; charts have equivalent data; images have meaningful alternatives and decorative graphics are ignored. Reduced-motion removes nonessential movement without hiding status. All functions work without hover or drag alone.

## Acceptance

No critical task is blocked for a keyboard or screen-reader user; all reported WCAG failures are mapped to criterion, route, reproduction, severity and owner. Focus, contrast and error behavior are verified at required breakpoints with evidence. Conduct moderated usability sessions with people with disabilities before first release; assistive technology combinations and results must be recorded rather than presumed.
