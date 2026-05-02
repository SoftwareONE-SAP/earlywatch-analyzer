# EWA Analyzer Azure Migration Minimal Clone

This project contains the backend, frontend, and deployment assets for the EWA Analyzer application. It supports SAPUI5-based analysis workflows, Azure Blob-backed persistence, AI-assisted report generation, and an Azure Container Apps deployment path.

## Tech Stack

- **Language:** Python 3.12, JavaScript
- **Runtime:** Python 3.12, Node.js 20+
- **Framework / Protocol:** FastAPI, SAPUI5, Azure Blob Storage, Azure OpenAI / Anthropic integrations
- **Key Dependencies:** fastapi>=0.115.12, uvicorn>=0.34.2, openai>=1.82.0, azure-storage-blob>=12.25.1, openpyxl>=3.1.3
- **Build:** `docker build ./backend`, `docker build ./sapui5`, `cd sapui5; npm install; npm run build`
- **Entry Point:** `backend/ewa_main.py`, `backend/ewa_pipeline/__main__.py`, `sapui5/webapp/index.html`

## Project Structure

```
.
├── README.md
├── docker-compose.yml
├── mta.yaml
├── mtaext.example.yaml
├── xs-security.json
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/
├── backend/
│   ├── Dockerfile
│   ├── README.md
│   ├── ewa_main.py
│   ├── workflow_orchestrator.py
│   ├── agent/
│   ├── converters/
│   ├── core/
│   ├── ewa_pipeline/
│   ├── models/
│   ├── pageindex/
│   ├── prompts/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── skills/
│   └── utils/
├── docs/
│   ├── AZURE_MIGRATION_GUIDE.md
│   └── RUNTIME_ARCHITECTURE.md
├── sapui5/
│   ├── Dockerfile
│   ├── README.md
│   ├── package.json
│   └── webapp/
├── approuter/
│   ├── package.json
│   └── xs-app.json
├── ui-deployer/
│   └── package.json
└── scripts/
	└── deploy-local-btp.ps1
```

## AI Memory System

This project uses a structured session memory system. Context files live in `.ai/`.

**At the start of every session**, read:
1. `.ai/context/progress.md` — what is currently being worked on and what to do next
2. The latest `.ai/handover/NNNN-*.md` — detailed log from the previous session
3. `.ai/context/learnings.md` — known gotchas and patterns for this codebase
4. `.ai/context/architecture.md` — architectural decisions and project structure

**At the end of every session**, run `/handover` to update all context files and create a new handover log.

**When starting fresh**, the `/resume` command reads all context and produces a session brief.

## Key Conventions

- Backend runtime state is stored in Azure Blob Storage, not a database.
- `sapui5/webapp/model/config.js` and `sapui5/webapp/chat.html` contain the backend URL and must stay aligned.
- Keep real secrets out of source files; use Azure Web App settings, Key Vault, GitHub Actions secrets, or BTP deployment secrets.
- Keep Azure deployment artifacts aligned with the Container Apps path; legacy SAP BTP files are not part of the supported deployment path.
- Treat `backend/ewa_pipeline/` as the newer structured analysis pipeline and `backend/` root modules as the app entry/service layer.