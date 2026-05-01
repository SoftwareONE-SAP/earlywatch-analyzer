# Runtime Architecture

This is the minimum architecture context needed for migration.

## Application Parts

- `backend/`: FastAPI API service. It is stateless and stores persistent artifacts in Azure Blob Storage.
- `sapui5/`: SAPUI5 frontend. It calls backend `/api/*` endpoints.
- `approuter/`: SAP BTP approuter. Required for BTP deployment, not required for a pure Azure Web Apps migration unless you intentionally keep the BTP route/auth layer.
- `ui-deployer/`: SAP HTML5 repository deployer. Required for BTP MTA deployment, not required for pure Azure Web Apps.
- `mta.yaml` and `xs-security.json`: BTP deployment/auth descriptors. Keep them in the clone so rollback or hybrid deployment remains possible.

## Persistent State

The backend does not use a database. All persistent state is stored in Azure Blob Storage:

- uploaded source files
- extracted markdown
- AI analysis JSON
- workbook payload JSON
- generated Excel output

Container restarts should not lose data as long as the same blob storage account/container is configured.

## Minimum Runtime Variables

Required for the backend:

| Variable | Purpose |
| --- | --- |
| `AZURE_STORAGE_CONNECTION_STRING` | Blob Storage access. Prefer Key Vault/App Settings over files. |
| `AZURE_STORAGE_CONTAINER_NAME` | Blob container used for uploads and outputs. |
| `PROVIDER` | `openai` or `anthropic`. |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI/AI Services endpoint. |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI key. |
| `AZURE_OPENAI_API_VERSION` | API version used by the SDK. |
| `AZURE_OPENAI_SUMMARY_MODEL` | Main summary/analysis model deployment. |
| `AZURE_OPENAI_PARAM_MODEL` | Parameter extraction model deployment. |
| `AZURE_OPENAI_FAST_MODEL` | Fast/chat model deployment. |
| `AZURE_OPENAI_CHAT_MODEL` | Chat model deployment. |

Optional Anthropic-on-Azure variables:

| Variable | Purpose |
| --- | --- |
| `AZURE_ANTHROPIC_ENDPOINT` | Azure AI Foundry Anthropic endpoint. |
| `AZURE_ANTHROPIC_API_KEY` | Anthropic provider key. |
| `ANTHROPIC_SUMMARY_MODEL` | Legacy summary model. |
| `V2_ANTHROPIC_ROUTER_MODEL` | Router model for the V2 pipeline. |
| `V2_ANTHROPIC_SPECIALIST_MODEL` | Specialist model for the V2 pipeline. |
| `V2_ANTHROPIC_DEEP_MODEL` | Deep analysis model for the V2 pipeline. |

## Known Migration Risks

- `sapui5/webapp/model/config.js` currently hardcodes the Azure backend URL as `https://sap-ewa-analyzer-backend.azurewebsites.net`.
- `sapui5/webapp/chat.html` has the same hardcoded Azure backend URL.
- If your Azure backend Web App has a different name, update both files before building the frontend image.
- CORS must allow the frontend Web App origin when frontend and backend run as separate Azure Web Apps.
- Long-running analysis requests can take minutes. Keep backend HTTP timeout settings high enough for Web Apps and any reverse proxy.
