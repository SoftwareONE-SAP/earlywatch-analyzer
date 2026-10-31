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

## Persistent State

The backend does not use a database. All persistent state is stored in Azure Blob Storage:

- uploaded source files
- normalized compact HTML
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
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI or Azure AI Services endpoint. |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key. |
| `AZURE_OPENAI_API_VERSION` | API version used by the SDK. |
| `CHAT_REASONING_EFFORT` | Reasoning effort for document chat. Required. |
| `ORCHESTRATOR_REASONING_EFFORT` | Reasoning effort for planner, cross-reference, and synthesis. Required. |
| `DEEP_REASONING_EFFORT` | Reasoning effort for specialist/domain-analysis workers. Required. |

Recommended for the one-container Container Apps path:

| Variable | Purpose |
| --- | --- |
| `ENVIRONMENT=production` | Enables production defaults. |
| `AUTH_ENABLED=true` | Turns on backend authorization checks. |
| `TRUST_PLATFORM_AUTH_HEADERS=true` | Trusts Container Apps auth headers instead of requiring SPA bearer tokens. |
| `ORCHESTRATOR_MODEL` | Required planner deployment; default for downstream analysis roles. |
| `SPECIALIST_MODEL` | Required parallel specialist deployment. |
| `CHAT_MODEL` | Required independent document-chat deployment. |

Direct JWT validation variables remain available for deployments where the frontend sends bearer tokens:

| Variable | Purpose |
| --- | --- |
| `ENTRA_TENANT_ID` | Expected Microsoft Entra tenant ID. |
| `ENTRA_API_CLIENT_ID` | API app registration client ID. |
| `ENTRA_API_AUDIENCE` | Optional custom audience override. |
| `ENTRA_ISSUER` | Optional issuer override. |

Optional Claude-on-Azure variables:

| Variable | Purpose |
| --- | --- |
| `ORCHESTRATOR_PROVIDER`, `SPECIALIST_PROVIDER` | Optional. `azure_openai` (default) or `foundry_claude` to run that role on Claude. |
| `CROSS_REFERENCE_PROVIDER`, `SYNTHESIS_PROVIDER` | Optional. Default: `azure_openai` if the role has its own `*_MODEL`, otherwise the orchestrator's provider. |
| `CHAT_PROVIDER` | Optional. `azure_openai` (default) or `foundry_claude`. |
| `AZURE_ANTHROPIC_ENDPOINT` | Claude endpoint, `https://<resource>.services.ai.azure.com/anthropic`. |
| `AZURE_ANTHROPIC_API_KEY` | Claude API key (`<set-in-secret-store>`; use a secret store or Key Vault reference only). |
| `ANTHROPIC_MAX_OUTPUT_TOKENS` | Optional, default 32000. Claude needs a maximum answer length, and thinking counts toward it. |

Claude is optional and nothing changes if these are unset. Put the Claude deployment name (for example `claude-sonnet-5-5`) in the existing `*_MODEL` / `CHAT_MODEL` setting. Azure OpenAI settings are still required (Decision-1 uses them). `CHAT_MAX_OUTPUT_TOKENS` may need raising when chat uses Claude with thinking on.

## Authentication Model

- The recommended Azure path is Container Apps built-in Microsoft Entra authentication plus same-origin frontend hosting.
- The backend can read authenticated user claims from `X-MS-CLIENT-PRINCIPAL*` headers when `TRUST_PLATFORM_AUTH_HEADERS=true`.
- The application requires users to be authenticated but does not enforce specific Entra app roles.
- If you choose a bearer-token SPA flow instead, keep `TRUST_PLATFORM_AUTH_HEADERS=false` and configure the `ENTRA_*` JWT settings.

## Known Deployment Risks

- The combined image requires the SAPUI5 build output to exist under `sapui5/dist/`; `Dockerfile.containerapp` handles this automatically.
- Long-running analysis requests can take minutes. Keep Container App ingress and client timeouts high enough for interactive runs.
- If `CORS_ALLOWED_ORIGINS` is unset in production, the backend now allows only same-origin requests.
- Azure Blob Storage remains the only persistent store. Losing or misconfiguring the container name will break uploads and report retrieval.
