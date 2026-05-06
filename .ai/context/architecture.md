# Architecture

**Project:** EWA Analyzer Azure Migration Minimal Clone  
**Initialized:** 2026-05-01

## Overview

This repository contains the runtime, frontend, and deployment assets for the EWA Analyzer application. The backend is a stateless FastAPI service that stores artifacts in Azure Blob Storage. The active Azure target is a single Azure Container App running a combined image that serves both the backend API and the built SAPUI5 frontend from the same origin.

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.12 |
| Language | JavaScript | Node.js ecosystem |
| Runtime | Python | 3.12 |
| Runtime | Node.js | 20+ |
| Protocol/Framework | FastAPI | 0.115.12+ |
| Protocol/Framework | SAPUI5 | current project setup |
| Storage | Azure Blob Storage | SDK-based |
| AI SDKs | OpenAI, Anthropic, Google GenAI | current project setup |
| Document/Export | openpyxl, PyMuPDF, python-docx | current project setup |

## Directory Structure

```
.
├── README.md
├── docker-compose.yml
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
└── scripts/
```

## Key Components

| File / Module | Responsibility |
|--------------|----------------|
| `backend/ewa_main.py` | Backend application entry point and same-container static frontend host in Azure. |
| `backend/workflow_orchestrator.py` | Orchestrates workflow execution. |
| `backend/ewa_pipeline/` | Structured pipeline for indexing, analysis, reporting, tracking, and orchestration. |
| `backend/core/azure_clients.py` | Azure client setup and service wiring. |
| `backend/core/runtime_config.py` | Runtime configuration loading. |
| `backend/core/entra_auth.py` | JWT validation and optional Container Apps platform-auth header parsing. |
| `backend/routers/` | API routes for health, auth, storage, export, chat, and AI operations. |
| `sapui5/webapp/` | SAPUI5 frontend application source. |
| `Dockerfile.containerapp` | Combined frontend and backend image build for Azure Container Apps. |
| `.github/workflows/deploy-to-containerapp.yml` | GitHub Actions deployment workflow for the Container App target. |
| `docs/AZURE_MIGRATION_GUIDE.md` | Azure migration runbook. |
| `docs/RUNTIME_ARCHITECTURE.md` | Runtime shape and environment variable reference. |

## Decision Log

| Date | Decision | Rationale | Alternatives Considered |
|------|----------|-----------|------------------------|
| 2026-05-01 | Initial memory system setup | Consistent session handoffs | None |
| 2026-05-02 | Use one Azure Container App for both frontend and backend | Lowest operational complexity, same-origin requests, and scale-to-zero cost profile | Split Azure Web Apps, Static Web Apps plus API |
| 2026-05-02 | Use Container Apps built-in Entra auth with trusted platform headers | Avoids adding a separate frontend token acquisition flow for the current Azure target | Pure bearer-token SPA flow |
