# EWA Analyzer

**Turn a 100-page SAP EarlyWatch Alert report into a prioritised, evidence-linked action list — in minutes, for a few cents.**

EWA Analyzer ingests SAP EarlyWatch Alert (EWA) exports, runs them through a multi-agent AI pipeline built on **LangGraph**, and produces a structured analysis: findings with severity, evidence, and Basis remediation steps, cross-domain risk correlations, an executive summary, and a downloadable Excel workbook. It runs on Azure (Container Apps + Blob Storage + Azure OpenAI) with a SAPUI5 front end.

---

## The problem it solves

SAP EarlyWatch Alert reports are the standard health check for a productive SAP system — but they are long, dense, and heavy on tables and traffic-light icons. Across a managed-services estate with dozens of systems, a human reviewing each one every week is slow, inconsistent, and easy to skim. Two engineers reading the same report often surface different findings.

EWA Analyzer makes that review **fast, consistent, and repeatable**. Every report is analysed the same way, every finding is tied back to the evidence in the source document, and every recommendation points at concrete SAP transactions. Because the pipeline tracks token cost per phase, the price of each analysis is known and auditable.

---

## How it works

The system has two halves: a **domain-specific ingestion step** that makes an EWA report cheap for a language model to read, and a **coordinator-worker agent graph** that does the analysis.

```mermaid
flowchart TD
    A[".doc EWA export"] -->|doc → html| B["Raw HTML"]
    B -->|compact semantic HTML<br/>icons → RED / YELLOW / GREEN tokens| C["Compact HTML"]
    C --> D["Document tree<br/>(analyzable sections)"]

    D --> P["planner<br/>(orchestrator model)<br/>triage + prioritise sections"]
    P -->|LangGraph Send, one per section| S1["domain_analyst"]
    P --> S2["domain_analyst"]
    P --> S3["domain_analyst …N (parallel)"]

    K["ewa-analysis skill<br/>thresholds + remediation refs"] -.selective load.-> S1
    K -.-> S2
    K -.-> S3

    S1 --> X["cross_reference<br/>correlate findings across domains"]
    S2 --> X
    S3 --> X
    X --> Y["synthesize<br/>exec summary · health · top-5 actions"]
    Y --> Z["Excel workbook + JSON"]
    Z --> BLOB["Azure Blob Storage"]
    BLOB --> UI["SAPUI5 front end<br/>view · chat · export"]
```

### 1. Ingestion — making an EWA report LLM-friendly

An EWA export is a Word document full of styling and status **icons**. Feeding that to a model raw is expensive and noisy. The ingestion step does two useful things:

- **Compact semantic HTML.** The document is converted `.doc → HTML → compact HTML`, stripping presentation while keeping structure (headings, tables, sections). This cuts token count dramatically.
- **Icon tokenization.** EWA relies on red/yellow/green status icons to signal health. An `icon_classifier` turns those images into text tokens — `[RED]`, `[YELLOW]`, `[GREEN]` — so the model can read a status it would otherwise be blind to.

The compact document is then parsed into a **tree** and split into *analyzable sections*.

### 2. Analysis — a LangGraph coordinator-worker graph

The analysis is a small team of AI agents rather than one giant prompt. LangGraph (a framework for building stateful, multi-step agent workflows as a graph) wires them together:

| Node | Model tier | Role |
|---|---|---|
| `planner` | Orchestrator (most capable) | Reads the tree, prioritises sections, and hands each analyst a focus hint and the relevant skill references. |
| `domain_analyst` ×N | Specialist (faster / cheaper) | Runs **in parallel**, one invocation per section. Produces structured findings — severity, evidence, impact, remediation. |
| `cross_reference` | Orchestrator | Correlates findings across sections to surface compound risks a single-section view would miss. |
| `synthesize` | Orchestrator | Writes the executive summary, overall system health, and top-5 priority actions. |

The parallel fan-out (LangGraph's `Send` primitive) is what keeps a large report fast: sections are analysed concurrently, not one after another. Every node writes **structured output** (Pydantic schemas), so findings are machine-parseable rather than free text.

### 3. The skills system — curated Basis knowledge, loaded on demand

The quality of each finding depends on the model knowing *what "good" looks like* for an SAP system. That expertise lives in a filesystem **skill** at `backend/skills/ewa-analysis/`, split into reference files:

- `thresholds-*` — memory, database, performance, batch, security, operations thresholds.
- `remediation-*` — matching Basis remediation playbooks.
- `correlations` — cross-domain compound-risk patterns.

Rather than dumping all of this into every prompt, the planner and analysts **selectively load only the references a section needs** (progressive disclosure). A memory section pulls the memory thresholds and playbook; a security section pulls the security ones. This keeps prompts focused and cheap while encoding real SAP Basis expertise as retrievable context.

### 4. Output and storage

The final result is written as a formatted **Excel workbook** plus JSON artifacts, all persisted to **Azure Blob Storage** — there is no database. Blob storage is the single source of truth, so container restarts and scale-to-zero events do not lose data. The SAPUI5 front end lists, views, and exports analyses, and includes a **chat** feature for asking follow-up questions grounded in the analysed report.

---

## Tech stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph (coordinator-worker graph, parallel `Send` fan-out) |
| Model inference | Azure OpenAI (default) or Anthropic-on-Azure; orchestrator / specialist / router tiers |
| Backend API | FastAPI (Python 3.12+) |
| Frontend | SAPUI5 |
| Storage | Azure Blob Storage (uploads, compact HTML, analysis JSON, Excel) |
| Structured output | Pydantic schemas via `with_structured_output` |
| Hosting | Azure Container Apps (single combined image) |
| Auth | Microsoft Entra ID (platform headers or JWT bearer) |
| Cost control | Per-phase token + cost tracking |

---

## Repository structure

| Path | Contents |
|---|---|
| `backend/ewa_pipeline/` | The analysis pipeline: agents (`orchestrator`, `runner`, `skill_loader`), indexer, report/Excel generation, cost tracking. |
| `backend/converters/` | `.doc` → HTML → compact semantic HTML, plus the icon classifier. |
| `backend/skills/ewa-analysis/` | Curated SAP Basis thresholds and remediation references. |
| `backend/routers/` | FastAPI routes: storage, AI, chat, export, auth, health. |
| `sapui5/` | SAPUI5 front end and build config. |
| `docs/` | Runtime architecture and Azure migration guide. |
| `deployment/` | Deployment instructions and environment notes. |
| `samples/` | Example EWA export and extracted HTML for local testing. |

---

## Getting started (local)

**Prerequisites:** Python 3.12+, Node.js 20+, Docker (optional), and Azure resources (Blob Storage + a model endpoint) for a full run.

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item ..\.env.example .env   # then fill in real values locally
python ewa_main.py
```

The API serves on `http://localhost:8001`.

### Frontend

```powershell
cd sapui5
npm install
npm start
```

The SAPUI5 app serves on `http://localhost:8080` and, in local mode, calls the backend on `http://localhost:8001`.

### Run the pipeline directly (CLI)

The pipeline can be run without the UI — useful for testing or batch analysis:

```powershell
cd backend
python -m ewa_pipeline analyze --doc ..\samples\<report>.doc --output output\analysis.xlsx
```

---

## Configuration

All configuration is via environment variables — see `.env.example` for the full list. The essentials:

| Variable | Purpose |
|---|---|
| `AZURE_STORAGE_CONNECTION_STRING` | Blob Storage access (prefer Key Vault / platform secrets). |
| `AZURE_STORAGE_CONTAINER_NAME` | Blob container for uploads and outputs. |
| `PROVIDER` | `openai` or `anthropic`. |
| `AZURE_OPENAI_ENDPOINT` / `AZURE_OPENAI_API_KEY` / `AZURE_OPENAI_API_VERSION` | Model endpoint and credentials. |
| `ORCHESTRATOR_MODEL` | Required planner deployment; default for cross-reference and synthesis. |
| `SPECIALIST_MODEL` | Required deployment for parallel domain analysts. |
| `CHAT_MODEL` | Required independent deployment for document chat. |
| `CHAT_REASONING_EFFORT` | Required reasoning effort for document chat. |
| `ORCHESTRATOR_REASONING_EFFORT` | Required planner reasoning effort; default for downstream roles. |
| `DEEP_REASONING_EFFORT` | Required reasoning effort for specialist/domain-analysis workers. |
| `SPECIALIST_REASONING_EFFORT` | Optional override for `DEEP_REASONING_EFFORT`. |
| `CROSS_REFERENCE_MODEL`, `SYNTHESIS_MODEL` | Independent downstream deployments; blank inherits planner. |
| `CROSS_REFERENCE_REASONING_EFFORT`, `SYNTHESIS_REASONING_EFFORT` | Independent downstream reasoning efforts; blank inherits planner. |
| `REQUEST_TIMEOUT_SECONDS` | Timeout per model request, default 180 seconds. |
| `PLANNING_TIMEOUT_SECONDS` | Optional planner-only timeout; blank inherits the request timeout. |
| `MAX_CONCURRENCY` | Maximum parallel section-analysis tasks per report, default 4. |
| `MAX_TASK_SECTIONS` | Maximum source sections per grouped task, default 12. |
| `MAX_TASK_CONTENT_CHARS` | Maximum complete source HTML characters per task, default 48000. |
| `MAX_PARENT_CONTEXT_CHARS` | Maximum supplementary parent-context characters per task, default 4000; 0 disables excerpts. |
| `DECISION_ENABLED` | Optional, off by default. `true` uses Microsoft Decision-1 to match SAP alerts to our findings in the "SAP vs Us" sheet (about 500 extra small calls per report). If a call fails, word-overlap matching is used. |
| `DECISION_MODEL` | Decision-1 model name, default `Decision-1`. |
| `DECISION_KEEP` / `DECISION_POSSIBLE` | Score at or above `DECISION_KEEP` (default 0.85) counts as a match; at or above `DECISION_POSSIBLE` (default 0.5) is shown as "please check". |
| `DECISION_WORKERS` / `DECISION_BUDGET_SECONDS` | Parallel calls (default 8) and the most time spent per report (default 300 seconds). |

**Heading check.** Decision-1 matches on topic, so it can pick a sibling finding. When it picks a finding, a plain-Python check re-ranks its own scores: if another candidate (score at or above `DECISION_POSSIBLE`) sits under a report heading, its own or a parent one, that repeats SAP's alert wording, and the first pick does not, the report uses that candidate instead. The row is marked "Medium" confidence and names the first pick as "also close, please check". It makes no extra AI calls. To compare results with and without it on saved scores, without any AI calls or output files, run this from `backend/`:

```
python -m ewa_pipeline alert-replay --result output/X_result.json --tree output/X.compact_tree.json --scores output/X_d1_scores.json --labels output/X_alert_summary.csv --keep 0.85
```

**Same-statement check.** SAP's alert text never names a SQL statement, but SAP's report has a section for the alert that lists the statement IDs (32 hex characters). After the heading check, a plain-Python step finds that section by its wording, reads the IDs, and looks at the chosen finding. If the finding names none of those IDs but another candidate (score at or above `DECISION_POSSIBLE`) does, the report uses the candidate with the highest score and names the first pick as "also close, please check". If no such candidate exists, nothing changes. It makes no extra AI calls, and `alert-replay` includes it in the "after" result.

The model clients retry failed requests up to three times by default. A YAML
configuration can set `max_model_retries`, the timeouts, and `max_concurrency`;
explicit YAML runtime values take precedence over environment values. Reasoning
levels must be supported by the selected Azure deployment.

Azure Portal environment variables remain the normal deployment controls. In the
Container App, open **Revisions and replicas > Create new revision**, edit the
application container's **Environment variables**, and create the new revision.
Use **Manual** as the source for these non-secret analysis settings. Runtime values are read at process
startup; changing a Portal value does not require rebuilding the image. The
container image does not include a `config.yaml` that could override these values.

The Actions deployment updates the existing Container App's image and model
settings in one operation. It migrates missing `ORCHESTRATOR_MODEL`,
`SPECIALIST_MODEL`, and `CHAT_MODEL` values from the old selections and removes
obsolete `V2_*` variables. Explicit current model selections are preserved on
subsequent runs. The Container App and its registry access must already be
provisioned before enabling the deployment workflow.

The planner groups related source sections into bounded specialist requests.
Python validates unique ownership, splits groups by source count/content limits,
and backfills omitted sources by hierarchy. Each response must identify every
owned source separately. Oversized individual sources fail explicitly without
truncation or model calls. Usage is charged once per grouped request. Workbooks
have four tabs: Priority Actions, Findings, SAP vs SoftwareONE (only when SAP data
exists) and Risk Heatmap (only when there is something to show). Findings keeps
every per-source finding. Sections that could not be analysed show as a line on
Priority Actions; the task and coverage details stay in the saved result JSON.
Partial section coverage is marked Unknown and zero successful sections fail.

See [the October 19 grouping deployment record](deployment/cli-grouping-20261019.md)
for the current values, verification, and source/image provenance.
| `AUTH_ENABLED` / `TRUST_PLATFORM_AUTH_HEADERS` | Entra authentication behaviour in hosted environments. |

> **Never commit real keys or connection strings.** Store secrets in Azure Container App settings, Key Vault, or a CI/CD secret store.

---

## Deployment

The recommended shape is a **single combined image** (`Dockerfile.containerapp`) on **Azure Container Apps**: FastAPI serves the built SAPUI5 assets from the same origin, backed by one Blob Storage account and one Azure OpenAI resource, with Entra ID authentication enabled on the Container App.

Notes:
- Analysis requests can take minutes — keep ingress and client timeouts high enough for interactive runs.
- With `CORS_ALLOWED_ORIGINS` unset in production, the backend allows same-origin requests only.
- Blob Storage is the only persistent store; a misconfigured container name will break uploads and retrieval.

See `docs/RUNTIME_ARCHITECTURE.md` and `docs/AZURE_MIGRATION_GUIDE.md` for the full runbook.

---

## Documentation

- **`docs/RUNTIME_ARCHITECTURE.md`** — runtime components, model tiers, and known deployment risks.
- **`docs/AZURE_MIGRATION_GUIDE.md`** — Azure provisioning and deployment runbook.
