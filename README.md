# EWA Analyzer

EWA Analyzer is a web application for processing SAP EarlyWatch exports, generating AI-assisted analysis, and delivering structured outputs including workbook exports.

## What this project includes

- Backend API built with FastAPI for upload, processing, analysis, chat, and export flows.
- SAPUI5 frontend for file management, analysis views, and user interaction.
- Azure Blob Storage integration for source documents and generated artifacts.
- LLM integration (Azure OpenAI by default, optional Anthropic-on-Azure settings).
- Containerized deployment assets for local smoke tests and Azure hosting.

## Repository structure

- backend/: FastAPI app, orchestration pipeline, routers, converters, and services.
- sapui5/: SAPUI5 frontend app and build configuration.
- docs/: runtime architecture and deployment guidance.
- deployment/: deployment instructions and environment notes.
- scripts/: helper scripts for local and deployment workflows.

## Core runtime flow

1. Upload a ZIP that contains EWA HTML export content.
2. Backend extracts and converts content to markdown.
3. AI pipeline processes markdown and generates analysis outputs.
4. Results are stored in Blob Storage and exposed through API endpoints.
5. Frontend consumes APIs for listing, viewing, and exporting analysis assets.

## Prerequisites

- Python 3.12+
- Node.js 20+
- Docker (optional, for image-based checks)
- Azure resources for production runtime (Blob Storage and model endpoints)

## Local development setup

### 1) Backend

From project root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a local env file from the template and set real values in your local environment:

```powershell
Copy-Item ..\.env.example .env
```

Start the API:

```powershell
python ewa_main.py
```

The backend serves on http://localhost:8001 by default.

### 2) Frontend

From project root:

```powershell
cd sapui5
npm install
npm start
```

The SAPUI5 app serves on http://localhost:8080.

In local mode, the frontend is configured to call http://localhost:8001.

## Environment configuration

Use .env.example as the reference for supported variables, including:

- Azure Blob Storage connection values
- Azure OpenAI model and endpoint settings
- Optional Anthropic-on-Azure model settings
- Environment, auth toggle, and CORS controls

Never commit real keys or connection strings. Store secrets in your platform secret manager.

## Build checks

From project root:

```powershell
docker build ./backend
docker build ./sapui5
```

SAPUI5 production build:

```powershell
cd sapui5
npm run build
```

## Deployment

- Container-oriented deployment assets are included for Azure hosting.
- Configure secrets through Azure Container App settings, Key Vault, or CI/CD secret stores.
- Keep frontend and backend routing aligned for same-origin API calls in hosted environments.

## Additional documentation

- docs/RUNTIME_ARCHITECTURE.md: runtime components, processing flow, and system behavior.
- docs/AZURE_MIGRATION_GUIDE.md: Azure environment provisioning and deployment runbook.
