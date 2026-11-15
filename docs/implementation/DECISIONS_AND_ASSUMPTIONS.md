# Implementation decisions and deviations

The user authorizes implementation and local builds, superseding the historical documentation-only restriction. Source specs remain the baseline. No remote publication, domain or host is authorized or attempted.

- Adopt documented proposed Django/DRF, PostgreSQL and Next/React/TypeScript. Locked dependencies are uv.lock and apps/web/package-lock.json.
- Native isolated PostgreSQL replaces Docker for this workstation to reduce resource use; no shared database service is modified.
- Local credential registration/login/verification endpoints extend the provider-assertion-only source contract. Production OIDC validation is not implemented and the assertion endpoint returns an explicit unavailable operation.
- Operational aggregates use a shared versioned Record model alongside typed core tables. This reduces early plumbing but does not complete all normalized domain relations/constraints.
- Realtime UI currently uses labeled5-second authoritative polling; one-shot SSE snapshot endpoint exists. Persistent WebSocket delivery/replay/resynchronization remains incomplete.
- Private panels share schema-driven forms/workspace. This is a working intermediate implementation, not completed screen-specific UX.
- External-evidence-only finance; no payout/escrow or live lender/payment/signature/SMS integration. File-based verification email is development-only. PDF remains quarantined without a scanner.
- `/v1/auth/action-challenges` extends step-up purposes for legal/consumer/export, with TOTP. Full enrollment and polished step-up UI remain unfinished.
- Original representative SVG assets avoid copying reference-site photography. Actual licensed vehicle media and optional final creative assets remain a separate delivery task.

None of these decisions grants production legal approval or converts incomplete requirements into verified ones.
