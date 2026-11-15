# Implementation checkpoint

Status: **IN PROGRESS / NOT READY**. The complete requested platform has not been delivered. This checkpoint is an executable local implementation, with explicit remaining work rather than a claim of final completion.

## Current code

- Django5.2 / DRF, PostgreSQL17, initial migrations and a separate transaction branch migration; real persistence and constrained core tables.
- Scoped identities, password hashing, email verification/recovery mail sink, TOTP staff challenge, session expiry/revocation epochs, CSRF and basic authentication throttling. Local credential login is an explicit extension; a production OIDC adapter is not implemented.
- Seller vehicle intake, assigned CRM lead, capacity-locked appointments/check-in/reschedule/cancel, template-pinned report revisions and independent publication, material report correction holding affected auctions.
- Locked dealer eligibility and auction admission/close, safe integer money, deadline checks, deterministic sequence, durable command receipts for accepted/rejected commands, immutable accepted bids, seller acceptance creating one case.
- Obligations, evidence, exact independent reconciliation, contract evidence/signature records, title and handover/closure guards have implementation paths. The complete legal/financial workflow is not yet end-to-end verified.
- Consumer listings/filtering/inquiries, offer-origin code, support/claims/content/policy and account record operations exist at differing maturity. Workflow guards, projections and interfaces need further completion.
- A real outbox worker delivers in-app notifications and schedules/closes auctions. Bounded retry and dead-letter processing is implemented and tested. External delivery and reminder coverage remain unfinished.
- Original public UI, seller wizard, sign-in, vehicle detail/inquiry, branches, private workspace tables/schema-driven forms, evidence upload, booking component and dealer bidding view.20 logical panel configurations are wired; they are not20 completed bespoke applications. The private routes currently share a role-selected workspace rather than full route-specific detail screens.
- Raster evidence re-encoding and private grants work; PDF processing remains quarantined. The complete media/retention/provider pipeline is unfinished.

## Executed evidence

33 backend tests,4 browser journeys, TypeScript, Ruff, migration drift check and optimized Next build passed in this session. See evidence/verification.json and per-command logs. Browser screenshots show desktop, mobile and seller workspace. Zero npm production dependency advisories were reported by the executed audit. This is not a backend dependency audit or penetration test.

## Required continuation order

1. Complete backend contract tests for all supported paths; correct residual DTO/status/pagination mismatches. api-coverage.json lists129 operations,3 without dispatch handlers,3 provider/adapter dependencies and21 explicitly partial paths.102 other dispatch paths remain unverified as complete features.
2. Replace remaining generic lifecycle assumptions with complete guard/effect handlers, including source allocation/reversal, supplier default, support/claim exceptions and access revocation. Add tests for every84 transition and all120 scenario acceptance records.
3. Complete native anonymous request ownership recovery, dealer member management, campaign execution, provider inbox and remaining consumer/privacy actions. Dealer verification aliases, sourcing actions and scoped asynchronous exports now have implementation paths; exports and CMS independent approval have focused tests. Keep live providers disabled until configured; sandbox adapters must be isolated.
4. Finish contract document generation and exact-version legal evidence; finish consumer offer, title, logistics and finance integration tests. Do not label recorded external evidence as a real transfer or provider signature.
5. Replace generic forms/details with all48 route-specific complete screens, properly integrated upload/checklist/approval components, session step-up dialogs, notification UI, accurate metrics, empty/error/retry behavior and server pagination. Finish accessible interaction tests.
6. Complete optional graphics/media/SEO publication lifecycle and actual asset production. Existing SVGs are representative development artwork, not actual vehicle photos.
7. Harden storage encryption/key management, TOTP enrollment/protection, production IAM/admin access, provider authentication, audit immutability, retention/hold deletion, worker retries and operational restore/load/security tests.
8. Validate all applicable nonfunctional and release gates. Update the requirement registry from meaningful evidence. No scenario is marked fully Verified merely because related code exists.

## Workspace preservation

Original specs remain unchanged. README and new app/tooling files are uncommitted; no unrelated files were deleted. No remote repository push, hosting, domain, production deployment or real financial/message action occurred. Local database and credentials are git-ignored. The previous documentation-only phase is superseded by the user's implementation request; production legal decisions remain open.

Latest additions: actual dealer inspection-report viewer, scoped checklist reads, exact-version CMS review, private CSV jobs/download grants, sourcing/proposal actions, controlled dealer resubmission, worker retry/dead-letter and malformed-credential/input guards. These do not make the remaining full-scenario and UI criteria complete.

Final recorded check set:33 backend tests and4 headless browser tests pass; the latest optimized build passes. CSV jobs, CMS approval, retry/dead-letter behavior and dealer report access now have focused evidence. Three missing dispatch paths remain (anonymous intake claim challenge/completion and the generic typed obligation-transition alias); supported direct evidence/reconciliation commands already exist. OIDC, normalized provider ingestion and financing integration still require completion. Detailed domain guards and full screen-specific UX remain incomplete.
