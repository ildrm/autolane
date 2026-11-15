# Executed verification

Actual captured results are in [evidence/verification.json](evidence/verification.json) and linked logs. The reported checks concern the current local code, not the earlier documentation-schema fixtures.

- Ruff: passed.
- Django migration drift: no changes detected; migrations applied successfully to the isolated PostgreSQL17 database.
-33 PostgreSQL-backed tests passed: concurrency, deadline, exact-once receipt/replay, revocation, scoped reads, slot capacity, stale versions, report review/correction, MFA/CSRF, finance maker/checker/matching, closure guards and private image upload.
-4 headless browser journeys passed: responsive marketplace/listing, seller login/intake/submission with database persistence, unauthenticated private denial, dealer report viewing and persisted bidding.
- TypeScript: passed.
- Next optimized build: passed, one build worker, Node heap cap1GiB and reduced scheduling priority. Build ID captured.
- `npm audit --omit=dev --audit-level=high`: zero reported advisories. Not a comprehensive security assessment.
- Headless screenshots: home-desktop.png, home-mobile.png and seller-mobile.png. Mobile390px overflow check passed. No visible user browser window was opened.

Not executed: full120-scenario E2E, all84-transition tests, every129-operation response contract, provider sandbox/live tests, penetration testing, complete rendered WCAG/user study, load/failover/backup restore exercises, production deployment. CI configuration exists but hosted CI execution is unverified.

The final database and browser log files are transcriptions of their observed successful tool output; verification.json identifies that recording method. The older captured lint/type/migration logs remain applicable to unchanged interfaces, with Ruff rerun successfully after the final backend/tooling changes.
