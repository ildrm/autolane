# Creative production pipeline and technology choices

**ID:** 07/09_CREATIVE_PRODUCTION_PIPELINE · **Version:** 0.1 · **Status:** PROPOSED, subject to prototyping and review · **Owner:** Motion design director · **Reviewers:** UX, accessibility, performance, frontend, product · **Updated:** 2026-11-15

## Technology evaluation
| Option | Best use / operational profile | Accessibility, SEO and licensing considerations |
|---|---|---|
| CSS transitions | Small state feedback; minimal runtime and maintainable tokenized timing. | Respect reduced motion; native content remains indexable; validate animation does not move focus. |
| Web Animations API | Interruptible timelines tied to UI events; moderate engineering effort. | Provide final state without API and handle cancellation; content must exist in DOM. |
| React motion library | Complex component orchestration when already justified; adds bundle and maintenance. | Review bundle, reduced motion, framework coupling, current license and dependency health. |
| GSAP | Complex authored timelines and scrubbed editorial sequences; added dependency and workflow. | Confirm current license for intended use and hosting, motion controls, graceful content fallback. |
| Rive | Stateful authored vector interactions; specialized authoring and runtime. | Supply text/DOM alternative, test mobile runtime and review current runtime/editor licenses. |
| Lottie | Lightweight authored illustrations when bounded; may be expensive for complex exports. | Static alternative, no meaningful text trapped only in animation; check file/runtime license. |
| Three.js / React Three Fiber | Optional on-demand interactive 3D; higher GPU, bundle, asset and engineering cost. | Static gallery/text equivalent, no indexing dependence, confirm licenses and WebGL compatibility. |
| WebGL / WebGPU or Canvas | Specialized visualization; highest device, accessibility and operational burden. | Retain semantic DOM/table alternative; feature-detect, test context loss and browser support, review current licenses. |

**PROPOSED:** CSS for simple feedback, Web Animations API for interruption-sensitive sequences, and static/2D alternatives by default. Introduce other runtimes only after a measured use case, licensing and device review. SEO-visible text remains server-renderable semantic content, not embedded in a canvas or video. Do not assume browser or licensing support remains static; verify authoritative vendor documentation at implementation time.

## Stage gates
1. Brief: identify user task, source of truth, accessibility and performance objective; product approves business purpose.
2. Storyboard: show start, intermediate, final, interruption and reduced-motion states; design and operations review claims.
3. Prototype: test real content, 320px, keyboard, slow device and one assistive technology path; avoid real customer data.
4. Produce: retain source files, font/model/photography rights, release and version; export optimized vector, video or 3D assets with documented fallbacks.
5. Handoff: provide trigger, exact timings/easing, asset dimensions, semantics, events, failure and performance budget to engineers; see [animation inventory](02_ANIMATION_INVENTORY.md).
6. QA: compare design, actual device behavior, accessibility, rights and network budget; issue owners repair and retest. Product and accessibility sign off before release.
7. Operate: maintain source and compiled artifacts, expiration/license register, owners and rollback; remove effects causing measurable degradation.

## 3D asset contract
Record coordinate system, origin, units, polygon count, PBR texture sizes and compression, variant mapping, approved camera constraints, model provenance, copyright and fallback poster. Establish independent condition evidence; representative graphics must not alter or replace an inspection report. No asset is considered production-ready until reviewed and licensed.
