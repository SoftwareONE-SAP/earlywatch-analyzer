# EWA Analyzer Azure Migration Minimal Clone

This folder contains the Azure runtime and deployment assets needed to run the EWA Analyzer application safely.

## Contents

- `backend/`: Python FastAPI service and Azure/OpenAI/storage integration.
- `sapui5/`: SAPUI5 frontend source and build config.
- `.github/workflows/`: current CI/CD workflows.
- `.env.example`: sanitized runtime config template.

## Secret Handling

Do not commit real secrets. Keep real values in GitHub Actions secrets, Azure Key Vault, or Azure Container App settings.

Before migration, rotate any credentials that were previously present in local files.

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

- Replace placeholders using secret-store values.
- The local `docker-compose.yml` is for smoke testing only; production Azure deployment should use managed secrets and explicit container/image definitions.

## Migration Instructions

Use `docs/AZURE_MIGRATION_GUIDE.md` as the start-to-finish runbook for Azure migration.

Use `docs/RUNTIME_ARCHITECTURE.md` for the runtime shape, required environment variables, and known migration risks.
