# Graphic asset specifications

**ID:** 07/06_GRAPHIC_ASSET_SPECIFICATIONS · **Version:** 0.1 · **Status:** PROPOSED, subject to prototyping and review · **Owner:** Motion design director · **Reviewers:** UX, accessibility, performance, frontend, product · **Updated:** 2026-11-15

## Asset inventory and ownership
| Asset | Format and intended dimensions | Production and accessibility requirements |
|---|---|---|
| Vehicle listing photo | Original master; responsive AVIF/WebP and JPEG fallback, 4:3 card and 16:9 detail crops, widths 480/960/1440/1920. | Document vehicle ID/revision, capture date and consent; truthful defect representation; descriptive alt where informative. |
| Inspection photo | Lossless or high-quality original stored securely; access-controlled derivative. | Preserve provenance, timestamp and report revision; no location/identity leakage in public derivative; minimum retention per policy. |
| Hero/editorial | High-quality master, responsive renditions and 16:9/4:3 crops. | Original/cleared rights, release, expiry and subject; no hidden unsupported claims. |
| Icon | Optimized SVG, 24×24 viewBox, 2-unit stroke; monochrome using semantic color. | Decorative icon hidden from assistive technology; functional icon needs text/name, high-contrast check. |
| Inspection diagram | Vector outline with numbered markers and separate findings list. | No reliance on hue or gesture, preserve accurate alignment and keyboard/text equivalent. |
| Motion/video | H.264/appropriate modern codec, poster, captions and transcript. | No autoplay audio; lazy-load; reduced-motion/static poster; license and release documented. |
| 3D model | glTF/GLB master, asset manifest, PBR textures, approved mobile fallback. | Label representative vs actual; preserve author/license, source and version; do not imply verified damage. |

## Naming and delivery
Use `asset-category_subject_view_revision_locale.ext`, e.g. `vehicle_opaqueid_front-r3_en.webp`; never put names, VIN, phone or credentials in public filenames. Store originals separately from derived renditions, preserve metadata and an audit trail, strip sensitive EXIF from delivery derivatives, checksum source and derivative, and restrict signed URLs by object and duration. Treat images containing identity, plates or location as potentially sensitive until privacy review.

## Quality gate
Check actual aspect ratios, photographic fidelity, visible alt-text context, image dimensions, responsive source selection, network budget, licenses, storage classification and accessibility. Do not expose original private inspection images or derivatives in public listing absent explicit approval and content review. Record missing assets rather than substituting reference-business imagery.
