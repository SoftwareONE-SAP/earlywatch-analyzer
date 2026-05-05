# Runtime Architecture

This is the minimum runtime context for the current Azure-only target.

## Recommended Azure Shape

- One Azure Container App running the combined image from `Dockerfile.containerapp`
- One Azure Container Apps environment
- One Azure Container Registry for image storage
- One Azure Storage account plus blob container for all persistent artifacts
- One Azure OpenAI or Azure AI Services resource for model inference
- Optional Azure Key Vault for secret storage
- Microsoft Entra ID authentication enabled on the Container App

## Application Parts

- `backend/`: FastAPI API service. In the combined deployment it also serves the built SAPUI5 assets when `sapui5/dist/` is present.
- `sapui5/`: SAPUI5 frontend source. In Azure it is built into static assets and served from the same origin as the API.

Legacy SAP BTP artifacts may still exist in the repository, but they are not part of the active Azure runtime.

## Persistent State

The backend does not use a database. All persistent state is stored in Azure Blob Storage:

- uploaded source files
- extracted markdown
- AI analysis JSON
- workbook payload JSON
- generated Excel output

Container restarts and scale-to-zero events should not lose data as long as the same blob storage account/container is configured.

## Minimum Runtime Variables

Required for the backend:

| Variable | Purpose |
| --- | --- |
| `AZURE_STORAGE_CONNECTION_STRING` | Blob Storage access. Prefer Azure secrets or Key Vault over files. |
| `AZURE_STORAGE_CONTAINER_NAME` | Blob container used for uploads and outputs. |
| `PROVIDER` | `openai` or `anthropic`. |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI or Azure AI Services endpoint. |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key. |
| `AZURE_OPENAI_API_VERSION` | API version used by the SDK. |
| `AZURE_OPENAI_SUMMARY_MODEL` | Legacy fallback — see V2 pipeline variables below. |
| `AZURE_OPENAI_PARAM_MODEL` | Legacy fallback — see V2 pipeline variables below. |
| `AZURE_OPENAI_FAST_MODEL` | Legacy fallback — see V2 pipeline variables below. |
| `AZURE_OPENAI_CHAT_MODEL` | Legacy fallback — see V2 pipeline variables below. |

Recommended for the one-container Container Apps path:

| Variable | Purpose |
| --- | --- |
| `ENVIRONMENT=production` | Enables production defaults. |
| `AUTH_ENABLED=true` | Turns on backend authorization checks. |
| `TRUST_PLATFORM_AUTH_HEADERS=true` | Trusts Container Apps auth headers instead of requiring SPA bearer tokens. |
| `V2_ORCHESTRATOR_MODEL` | Deployment used by the planner, cross-reference, and synthesis steps. Most capable model. |
| `V2_SPECIALIST_MODEL` | Deployment used by the parallel domain analyst subagents. |
| `V2_ROUTER_MODEL` | Deployment used for routing decisions and page indexing. Fastest/cheapest model.

Direct JWT validation variables remain available for deployments where the frontend sends bearer tokens:

| Variable | Purpose |
| --- | --- |
| `ENTRA_TENANT_ID` | Expected Microsoft Entra tenant ID. |
| `ENTRA_API_CLIENT_ID` | API app registration client ID. |
| `ENTRA_API_AUDIENCE` | Optional custom audience override. |
| `ENTRA_ISSUER` | Optional issuer override. |

Optional Anthropic-on-Azure variables:

| Variable | Purpose |
| --- | --- |
| `AZURE_ANTHROPIC_ENDPOINT` | Azure AI Foundry Anthropic endpoint. |
| `AZURE_ANTHROPIC_API_KEY` | Anthropic provider key. |
| `ANTHROPIC_SUMMARY_MODEL` | Legacy summary model. |
| `V2_ANTHROPIC_ROUTER_MODEL` | Router model for the V2 pipeline. |
| `V2_ANTHROPIC_SPECIALIST_MODEL` | Specialist model for the V2 pipeline. |
| `V2_ANTHROPIC_DEEP_MODEL` | Deep analysis model for the V2 pipeline. |

## Authentication Model

- The recommended Azure path is Container Apps built-in Microsoft Entra authentication plus same-origin frontend hosting.
- The backend can read authenticated user claims from `X-MS-CLIENT-PRINCIPAL*` headers when `TRUST_PLATFORM_AUTH_HEADERS=true`.
- The application expects Entra app roles named `Viewer` and `Administrator` for route authorization.
- If you choose a bearer-token SPA flow instead, keep `TRUST_PLATFORM_AUTH_HEADERS=false` and configure the `ENTRA_*` JWT settings.

## Known Deployment Risks

- The combined image requires the SAPUI5 build output to exist under `sapui5/dist/`; `Dockerfile.containerapp` handles this automatically.
- Long-running analysis requests can take minutes. Keep Container App ingress and client timeouts high enough for interactive runs.
- If `CORS_ALLOWED_ORIGINS` is unset in production, the backend now allows only same-origin requests.
- Azure Blob Storage remains the only persistent store. Losing or misconfiguring the container name will break uploads and report retrieval.
