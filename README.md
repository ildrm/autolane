# Autolane

An open-source English-first automotive marketplace and operations platform. GPL-2.0; see LICENSE. **Implementation is in progress, not the completed documented platform.** The source specifications remain in [docs](docs/00_MASTER_INDEX.md); current code status and explicit gaps are tracked in [implementation progress](docs/implementation/IMPLEMENTATION_PROGRESS.md).

## Local use with limited resource consumption

Prerequisites: Python3.12+, uv, Node24+ / npm, PostgreSQL17 native tools on PATH. Tested here with Python3.14.5, Node26.12.0 and PostgreSQL17.11. No domain, hosting account or paid provider is needed. Commands below do not deploy anything.

```sh
python3 scripts/local.py setup
.venv/bin/python scripts/local.py start
```

Open http://127.0.0.1:3000. The API listens only on127.0.0.1:8000; PostgreSQL uses its own data directory under `.local/postgres` and port55432. It does not modify an existing PostgreSQL service. Buffers are32MiB, connections16, parallel DB workers disabled. API concurrency is capped at12 with one worker. Node heap is capped at1GiB, Next build workers at1. Notification/deadline processing uses one5-second polling worker. The first setup installs dependencies sequentially; it can take time and needs network access. Docker is not needed.

```sh
.venv/bin/python scripts/local.py stop
```

Stop terminates only processes launched by this controller (matching PID and process birth time) and the isolated database. If starting manually, stop those terminal processes separately. No visible browser is opened by startup or tests. Browser checks are headless, one worker. There is no auto-start OS service.

## Development accounts and data

Setup explicitly creates fictional example.test identities, vehicles, a branch, checklist and open development auction. It never seeds a non-development environment. Credentials and authenticator secrets are written to the git-ignored, owner-readable `.local/development-accounts.json`; default development password is `Development-only-2026!`. Seller: `seller@example.test`; dealer: `dealer@example.test`. Staff (for example `inspector@example.test`, `reviewer@example.test`, `finance@example.test`) require TOTP from their own development secret. These accounts are local fixtures, not verified real identities. Registering a new account sends verification mail to `.local/mail` rather than a real recipient. Use the Verify email option on sign-in to complete verification.

All inventory artwork is original representative SVG illustration, clearly labeled. It is not photography of an actual inspected vehicle. Seeded operational records are fictional; newly submitted forms and bids persist in PostgreSQL.

## Verify and build

```sh
.venv/bin/python scripts/local.py test
.venv/bin/python scripts/local.py build
```

The first command runs Ruff, PostgreSQL integration/concurrency tests and TypeScript checks. The build command creates a Next.js production bundle locally; it does not publish. Stop the web process before building to avoid two processes sharing `.next`. After a successful build, the local controller uses `next start` instead of the development compiler.

With API/web running and fixtures installed:

```sh
cd apps/web
npm run test:e2e
```

Playwright uses installed Google Chrome in headless mode on macOS. Set `CHROME_PATH` to another Chromium executable on other systems. One worker is configured. Tests create additional fictional selling requests in the development database; backend tests use a separate temporary test database and do not alter that inventory. For a screenshot smoke check, run `node scripts/browser-smoke.mjs` from apps/web. Screenshots and evidence are in docs/implementation/evidence; failed traces remain git-ignored under apps/web/test-results.

## Architecture and safety boundaries

Django/DRF, PostgreSQL, Next.js/React/TypeScript. Core typed tables store identities, scopes, booking capacity, report revisions, auctions/bids/results and obligations; operational modules currently use versioned Record aggregates. Commands enforce server-side scope, state/version, idempotency and transactional audit/outbox. Generic forms consume request schemas, while dedicated seller, booking, evidence and dealer bidding interfaces cover core interactions.

Financial mode is external-evidence-only. No real payment, payout, escrow, lender approval or electronic signature provider is configured. Evidence processing supports inert re-encoded raster images; PDF remains quarantined until a scanner/CDR integration is supplied. External provider APIs, production privacy/retention and several advanced workflows remain incomplete. Production mode requires a supplied secret and TLS/security configuration; local test success is not production readiness.

See [.env.example](.env.example) for environment variables. Export them in the shell/service environment; the application does not automatically load arbitrary `.env` files. Do not commit real secrets or customer records. `.local`, dependency directories, generated builds and caches are ignored by Git.

## Contributor map

- `apps/api/marketplace`: models, migrations, command services, permissions, API routing and tests.
- `apps/web/src`: server-rendered public pages, account/operations UI, tokens and typed HTTP client.
- `scripts/local.py`: isolated native development lifecycle.
- `docs/implementation`: requirement registry, checkpoint, known gaps and actual verification evidence.
- `.github/workflows/ci.yml`: configured verification pipeline; hosted execution has not been claimed.

Use versioned domain commands rather than writing transaction data through admin. The built-in Django admin intentionally exposes only IAM/configuration plus read-only audit; it is not a bypass for bid or financial mutations. Review the security/readiness gaps before any real-user installation.
