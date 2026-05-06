# Learnings

Technical gotchas, API quirks, and patterns specific to this codebase. Updated during sessions via `/handover`.

**Pruning rule:** Remove entries that are no longer relevant or have been resolved. Archive entries older than ~30 sessions.

---

## API / SDK Quirks

<!-- Things about the external APIs or SDKs used in this project that are non-obvious. -->

- `az containerapp auth update` supports `--enabled true`, `--unauthenticated-client-action RedirectToLoginPage`, and `--proxy-convention Standard` for the built-in auth path.
- `az containerapp update --set-env-vars` accepts `secretref:` values when Container App secrets are configured separately.

---

## Patterns That Work

<!-- Approaches, patterns, or idioms that have proven effective in this codebase. -->

- The lowest-friction Azure target for this repo is one Container App that serves both the FastAPI backend and built SAPUI5 frontend from the same origin.
- Container Apps built-in Microsoft Entra auth plus `TRUST_PLATFORM_AUTH_HEADERS=true` avoids adding a separate SPA token-acquisition flow.
- For npm security-update failures in this repo, patch the smallest controlling manifest first, regenerate only that package lockfile with `npm install --package-lock-only`, and verify with `npm audit --json` before widening scope.

---

## Patterns That Failed

<!-- Things tried that didn't work and why, so you don't repeat the same mistakes. -->

- Treating the repo as blocked on a missing `config.yaml` was incorrect. `backend/ewa_pipeline/config.py` already falls back to environment-based configuration when no file exists.

---

## Environment & Tooling Notes

<!-- Non-obvious setup steps, environment variables, local dev gotchas. -->

- In production, leaving `CORS_ALLOWED_ORIGINS` unset now means same-origin only. Development localhost defaults are used only when `ENVIRONMENT` is local or dev.
- The local workspace used in this session does not have Docker on PATH, so image build validation must happen elsewhere unless Docker is installed.

---

## Debugging Notes

<!-- Known debugging techniques or tools that work well for this project. -->

- `npm audit --json` can stay red after a root dependency override if a nested vendor package resolves its own vulnerable copy; inspect `package-lock.json` for the remaining path before assuming the first override worked.
