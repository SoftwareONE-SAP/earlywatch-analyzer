# EWA Analyzer Azure Migration Minimal Clone

This folder contains the minimum runtime and deployment assets needed to validate and migrate the EWA Analyzer application safely.

## Contents

- `backend/`: Python FastAPI service and Azure/OpenAI/storage integration.
- `sapui5/`: SAPUI5 frontend source and build config.
- `approuter/`: SAP approuter route/auth config.
- `ui-deployer/`: HTML5 repo deployer module for MTA builds.
- `mta.yaml`: BTP MTA module/resource definition.
- `xs-security.json`: XSUAA scopes and role templates.
- `.github/workflows/`: current CI/CD workflows.
- `.env.example` and `mtaext.example.yaml`: sanitized config templates.

## Secret Handling

Do not commit real secrets. Keep real values in GitHub Actions secrets, Azure Key Vault, Azure App Service/Container App settings, or BTP/Cloud Foundry deployment secrets.

Before migration, rotate any credentials that were previously present in local files such as `mtaext.yaml`.

## Local Checks

From this folder:

```powershell
docker build ./backend
docker build ./sapui5
```

For SAPUI5-only validation:

```powershell
cd sapui5
npm install
npm run build
```

## Deployment Notes

- Copy `mtaext.example.yaml` to `mtaext.yaml` only in a secure local/CI environment.
- Replace placeholders using secret-store values.
- `mtaext.yaml` is ignored by git.
- The local `docker-compose.yml` is for smoke testing only; production Azure deployment should use managed secrets and explicit container/image definitions.

## Migration Instructions

Use `docs/AZURE_MIGRATION_GUIDE.md` as the start-to-finish runbook for Azure migration.

Use `docs/RUNTIME_ARCHITECTURE.md` for the runtime shape, required environment variables, and known migration risks.
