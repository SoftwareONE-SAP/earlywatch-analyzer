# Deployment Instructions

## Step 1: Preflight and Safety

Complete these checks before creating any Azure resources or changing application configuration.

### Goal

Make sure the deployment starts from a known-good workspace, with the right tools installed and no secret leakage risk.

### Checklist

- [ ] Confirm you are working in the correct repository and branch.
- [ ] Verify the workspace is the Azure migration clone, not the BTP-only clone.
- [ ] Install or confirm availability of Azure CLI, Docker Desktop, Node.js 20+, Python 3.12+, and Git.
- [ ] Identify the target Azure subscription, resource group name, and region before creating anything.
- [ ] Rotate any credentials that may have existed in local plaintext files, including storage, OpenAI, Foundry, ACR, and BTP secrets.
- [ ] Confirm no real secrets will be copied into source-controlled files such as `.env`, `mtaext.yaml`, or backend config files.
- [ ] Decide whether this deployment is Azure-only or must keep BTP fallback artifacts intact.

### Inputs Needed

- Azure subscription ID or name.
- Target resource group name.
- Azure region.
- A list of secret values that will come from secure storage rather than files.

### Exit Criteria

- The workspace and branch are confirmed.
- Required tools are available.
- Secrets have been rotated or reviewed.
- The Azure deployment target has been identified.
- No deployment commands should run until this step is complete.

### Notes

- Use [docs/AZURE_MIGRATION_GUIDE.md](../docs/AZURE_MIGRATION_GUIDE.md) as the full migration runbook.
- Use [docs/RUNTIME_ARCHITECTURE.md](../docs/RUNTIME_ARCHITECTURE.md) to confirm the required backend environment variables.
- If any secret was ever stored in a local file, assume it is compromised and rotate it before deployment.

## Step 2: Confirm Runtime Expectations

Validate the application runtime contract before creating Azure resources. This prevents configuring the wrong services, wrong model names, or the wrong storage path.

### Goal

Confirm that the backend is being deployed as a stateless container app with Azure Blob Storage for persistence, and that the model provider and auth strategy are understood before infrastructure is created.

### Checklist

- [ ] Read the backend runtime variable table in [docs/RUNTIME_ARCHITECTURE.md](../docs/RUNTIME_ARCHITECTURE.md).
- [ ] Confirm the backend uses Azure Blob Storage as the only persistent store.
- [ ] Confirm the following artifacts will be stored in Blob Storage:
	- uploaded source files
	- extracted markdown
	- AI analysis JSON
	- workbook payload JSON
	- generated Excel output
- [ ] Confirm which model provider will be used for this deployment: `openai` or `anthropic`.
- [ ] Confirm the Azure OpenAI or Azure AI Foundry resource endpoint that will be used.
- [ ] Confirm the exact deployment names for the models the backend will call.
- [ ] Decide whether the first smoke test will run with `AUTH_ENABLED=false`.
- [ ] Confirm whether this deployment is Azure-only or whether BTP fallback artifacts must remain usable.
- [ ] Confirm the frontend and backend will be deployed as separate Linux Web Apps for Containers.
- [ ] Confirm the frontend will call the backend over HTTPS and not through a local proxy.

### Required Backend Variables

These values must be available from App Service settings, Key Vault references, or deployment secrets before the backend can start successfully:

- `AZURE_STORAGE_CONNECTION_STRING`
- `AZURE_STORAGE_CONTAINER_NAME`
- `PROVIDER`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_SUMMARY_MODEL`
- `AZURE_OPENAI_PARAM_MODEL`
- `AZURE_OPENAI_FAST_MODEL`
- `AZURE_OPENAI_CHAT_MODEL`

### Values To Decide Now

- Storage account name.
- Blob container name.
- Azure region.
- OpenAI or Foundry endpoint.
- Model deployment names for summary, parameter, fast, and chat workloads.
- Whether auth is disabled for the first validation run.

### Exit Criteria

- The deployment target architecture is clear.
- The backend storage and model dependencies are known.
- The app settings that must be configured in Azure are listed.
- There is no ambiguity about whether auth will be active during the first smoke test.
- You can move on to resource creation without guessing at runtime details.

### Validation Questions

Before proceeding to Step 3, you should be able to answer all of these:

- Which blob container will hold the application artifacts?
- Which model provider will the backend use?
- What are the exact Azure deployment names for the models?
- Will the first smoke test run with auth enabled or disabled?
- Is a BTP fallback still required, or is this Azure-only?

### Notes

- Do not create Azure resources until these runtime choices are settled.
- If the backend settings are still unknown, stop here and resolve them first.
- Keep [docs/AZURE_MIGRATION_GUIDE.md](../docs/AZURE_MIGRATION_GUIDE.md) open while filling in the values for this step.

## Step 3: Create Azure Resources

Create the Azure infrastructure that will host the backend, frontend, storage, and AI services.

### Goal

Provision the minimum Azure services required for the application to run as two Linux Web Apps for Containers with Blob-backed storage and model access.

### Checklist

- [ ] Create or identify the Azure resource group for the deployment.
- [ ] Create or identify the Azure Container Registry that will store both images.
- [ ] Create or identify the Azure Storage account that will hold runtime artifacts.
- [ ] Create the blob container used by the backend for uploaded files and generated outputs.
- [ ] Create or identify the Azure OpenAI or Azure AI Services resource that provides model inference.
- [ ] Create the Linux App Service Plan for the two Web Apps.
- [ ] Create the backend Web App for Containers.
- [ ] Create the frontend Web App for Containers.
- [ ] Decide whether to create a Key Vault for secrets instead of storing values directly in App Service settings.
- [ ] Confirm the chosen names are globally unique where Azure requires it.
- [ ] Confirm the selected region is available for all required services.

### Resource Inventory

You should end this step with the following Azure resources identified or created:

- Resource group.
- Azure Container Registry.
- Storage account.
- Blob container.
- Azure OpenAI / AI Services resource.
- Linux App Service Plan.
- Backend Web App.
- Frontend Web App.
- Optional Key Vault.

### Recommended Naming Pattern

Use a consistent naming scheme so the deployment is easy to operate and troubleshoot.

- Resource group: `rg-ewa-analyzer-prod`
- Container Registry: a globally unique registry name
- Storage account: a globally unique storage account name
- Container: `earlywatch`
- App Service Plan: `asp-ewa-analyzer-prod`
- Backend Web App: `sap-ewa-analyzer-backend`
- Frontend Web App: `sap-ewa-analyzer-ui`

### Important Constraints

- The backend and frontend must both run on Linux App Service for Containers.
- The backend should not rely on local disk for persistent data.
- The storage container must be available before you configure backend settings.
- The ACR must be reachable by both Web Apps or by the deployment mechanism you choose.
- The Azure OpenAI or Foundry resource must have the required model deployments created before backend validation.

### Exit Criteria

- The Azure resource group exists.
- The registry, storage account, and blob container exist.
- The backend and frontend Web Apps exist.
- The App Service Plan exists and is Linux-based.
- The AI service endpoint exists and is accessible.
- You can proceed to app settings without needing to create new infrastructure later.

### Validation Questions

Before moving to Step 4, confirm these answers:

- What is the exact resource group name?
- What is the exact storage account name?
- What is the exact blob container name?
- What is the exact backend Web App name?
- What is the exact frontend Web App name?
- Which AI service endpoint will the backend use?
- Will secrets be stored in Key Vault or directly in Web App settings?

### Notes

- If Azure resource creation fails because of RBAC or quota, resolve that before moving on.
- If the storage container cannot be created with `--auth-mode login`, use the Azure Portal or an account key as described in the migration guide.
- Keep [docs/AZURE_MIGRATION_GUIDE.md](../docs/AZURE_MIGRATION_GUIDE.md) open to compare the resource list against the runbook.

---

## Step 3a: Azure Resource Creation Script

Replace every `<PLACEHOLDER>` before running. Run the scripts in order. Each block is independent and safe to re-run if it was already partially completed.

### Variables — fill these in first

```powershell
# ── Identity ──────────────────────────────────────────────────────────────────
$location        = "<AZURE_REGION>"                    # e.g. uksouth, westeurope, eastus
$subscriptionId  = "<SUBSCRIPTION_ID>"                 # from: az account show --query id -o tsv

# ── Resource group ────────────────────────────────────────────────────────────
$rg              = "<RESOURCE_GROUP_NAME>"             # e.g. rg-ewa-analyzer-prod

# ── Container Registry ────────────────────────────────────────────────────────
# Globally unique, 5-50 chars, lowercase letters and numbers only, no hyphens.
$acr             = "<ACR_NAME>"                        # e.g. ewaanalyzeracr

# ── Storage ───────────────────────────────────────────────────────────────────
# Globally unique, 3-24 chars, lowercase letters and numbers only.
$storage         = "<STORAGE_ACCOUNT_NAME>"            # e.g. ewastorageprod
$container       = "earlywatch"                        # blob container name — keep this value

# ── App Service ───────────────────────────────────────────────────────────────
$plan            = "asp-ewa-analyzer-prod"
$backendApp      = "sap-ewa-analyzer-backend"          # must be globally unique on azurewebsites.net
$frontendApp     = "sap-ewa-analyzer-ui"               # must be globally unique on azurewebsites.net

# ── AI / Model ────────────────────────────────────────────────────────────────
$openAiEndpoint  = "<AZURE_OPENAI_ENDPOINT>"           # e.g. https://my-resource.openai.azure.com/
$openAiKey       = "<AZURE_OPENAI_API_KEY>"
$openAiVersion   = "2025-03-01-preview"

# Legacy pipeline models
$summaryModel    = "<SUMMARY_DEPLOYMENT_NAME>"         # exact deployment name in your AI resource
$paramModel      = "<PARAM_DEPLOYMENT_NAME>"
$fastModel       = "<FAST_DEPLOYMENT_NAME>"
$chatModel       = "<CHAT_DEPLOYMENT_NAME>"

# V2 agentic pipeline models (OpenAI)
$v2RouterModel      = "<V2_ROUTER_DEPLOYMENT_NAME>"    # e.g. gpt-5.4-nano
$v2SpecialistModel  = "<V2_SPECIALIST_DEPLOYMENT_NAME>" # e.g. gpt-5.4-mini
$v2DeepModel        = "<V2_DEEP_DEPLOYMENT_NAME>"      # e.g. gpt-5.4

# Anthropic (optional — only needed if PROVIDER=anthropic or dual-provider)
$anthropicEndpoint          = "<AZURE_ANTHROPIC_ENDPOINT>"   # e.g. https://my-resource.services.ai.azure.com/anthropic
$anthropicKey               = "<AZURE_ANTHROPIC_API_KEY>"
$anthropicSummaryModel      = "<ANTHROPIC_SUMMARY_MODEL>"     # e.g. claude-haiku-4-5
$anthropicParamModel        = "<ANTHROPIC_PARAM_MODEL>"
$v2AnthropicRouterModel     = "<V2_ANTHROPIC_ROUTER_MODEL>"   # e.g. claude-haiku-4.5
$v2AnthropicSpecialistModel = "<V2_ANTHROPIC_SPECIALIST_MODEL>"
$v2AnthropicDeepModel       = "<V2_ANTHROPIC_DEEP_MODEL>"     # e.g. claude-sonnet-4.6
$anthropicThinkingBudget    = 8000
```

### Script 1: Create the resource group, ACR, storage, and blob container

```powershell
az account set --subscription $subscriptionId

# Resource group
az group create `
  --name $rg `
  --location $location

# Container Registry (admin enabled so Web Apps can pull with username/password)
az acr create `
  --resource-group $rg `
  --name $acr `
  --sku Basic `
  --admin-enabled true `
  --location $location

# Storage account
az storage account create `
  --resource-group $rg `
  --name $storage `
  --location $location `
  --sku Standard_LRS `
  --kind StorageV2

# Blob container
# If this fails with RBAC errors, create the container in the Azure Portal instead.
az storage container create `
  --name $container `
  --account-name $storage `
  --auth-mode login
```

### Script 2: Create the App Service Plan and Web Apps

```powershell
# Linux App Service Plan
az appservice plan create `
  --resource-group $rg `
  --name $plan `
  --is-linux `
  --sku B1 `
  --location $location

# Backend Web App — starts with nginx placeholder image, replaced later
az webapp create `
  --resource-group $rg `
  --plan $plan `
  --name $backendApp `
  --deployment-container-image-name nginx

# Frontend Web App — starts with nginx placeholder image, replaced later
az webapp create `
  --resource-group $rg `
  --plan $plan `
  --name $frontendApp `
  --deployment-container-image-name nginx
```

### Script 3: Configure backend App Settings

```powershell
$storageConnection = az storage account show-connection-string `
  --resource-group $rg `
  --name $storage `
  --query connectionString `
  --output tsv

az webapp config appsettings set `
  --resource-group $rg `
  --name $backendApp `
  --settings `
    ENVIRONMENT=production `
    AUTH_ENABLED=false `
    AZURE_STORAGE_CONNECTION_STRING="$storageConnection" `
    AZURE_STORAGE_CONTAINER_NAME="$container" `
    PROVIDER=openai `
    AZURE_OPENAI_ENDPOINT="$openAiEndpoint" `
    AZURE_OPENAI_API_KEY="$openAiKey" `
    AZURE_OPENAI_API_VERSION="$openAiVersion" `
    AZURE_OPENAI_SUMMARY_MODEL="$summaryModel" `
    AZURE_OPENAI_PARAM_MODEL="$paramModel" `
    AZURE_OPENAI_FAST_MODEL="$fastModel" `
    AZURE_OPENAI_CHAT_MODEL="$chatModel" `
    SUMMARY_REASONING_EFFORT=none `
    PARAM_REASONING_EFFORT=none `
    V2_ROUTER_MODEL="$v2RouterModel" `
    V2_SPECIALIST_MODEL="$v2SpecialistModel" `
    V2_DEEP_MODEL="$v2DeepModel" `
    AZURE_ANTHROPIC_ENDPOINT="$anthropicEndpoint" `
    AZURE_ANTHROPIC_API_KEY="$anthropicKey" `
    ANTHROPIC_SUMMARY_MODEL="$anthropicSummaryModel" `
    ANTHROPIC_PARAM_MODEL="$anthropicParamModel" `
    V2_ANTHROPIC_ROUTER_MODEL="$v2AnthropicRouterModel" `
    V2_ANTHROPIC_SPECIALIST_MODEL="$v2AnthropicSpecialistModel" `
    V2_ANTHROPIC_DEEP_MODEL="$v2AnthropicDeepModel" `
    ANTHROPIC_THINKING_BUDGET_TOKENS="$anthropicThinkingBudget"
```

> **Remember:** Set `AUTH_ENABLED=true` after the first smoke test passes.

### Script 4: Configure CORS

```powershell
az webapp cors add `
  --resource-group $rg `
  --name $backendApp `
  --allowed-origins "https://$frontendApp.azurewebsites.net"
```

---

## Step 3b: GitHub Actions Setup for Push-to-ACR

The workflow `.github/workflows/deploy-to-azure-webapps.yml` builds both containers, pushes them to ACR, and redeploys both Web Apps on every push to the `azure-migration` branch.

### Script 5: Create a service principal for GitHub Actions

```powershell
az ad sp create-for-rbac `
  --name "sp-ewa-analyzer-deploy" `
  --role contributor `
  --scopes "/subscriptions/$subscriptionId/resourceGroups/$rg" `
  --sdk-auth
```

Copy the full JSON output — you need it as the `AZURE_CREDENTIALS` secret.

### Script 6: Get ACR credentials

```powershell
$acrLoginServer = az acr show `
  --resource-group $rg `
  --name $acr `
  --query loginServer `
  --output tsv

$acrUsername = az acr credential show `
  --resource-group $rg `
  --name $acr `
  --query username `
  --output tsv

$acrPassword = az acr credential show `
  --resource-group $rg `
  --name $acr `
  --query passwords[0].value `
  --output tsv

Write-Host "ACR_LOGIN_SERVER  : $acrLoginServer"
Write-Host "REGISTRY_USERNAME : $acrUsername"
Write-Host "REGISTRY_PASSWORD : $acrPassword"
```

### GitHub Secrets to Add

Go to **GitHub → repository → Settings → Secrets and variables → Actions** and create these secrets:

| Secret name | Value |
|---|---|
| `ACR_LOGIN_SERVER` | Output of `$acrLoginServer` above |
| `REGISTRY_USERNAME` | Output of `$acrUsername` above |
| `REGISTRY_PASSWORD` | Output of `$acrPassword` above |
| `AZURE_CREDENTIALS` | Full JSON from Script 5 |
| `AZURE_RESOURCE_GROUP` | Your `$rg` value |
| `AZURE_BACKEND_WEBAPP_NAME` | Your `$backendApp` value |
| `AZURE_FRONTEND_WEBAPP_NAME` | Your `$frontendApp` value |

### Fix the hardcoded registry in push-to-acr.yml

The file `.github/workflows/push-to-acr.yml` currently has a hardcoded registry URL. Replace the `REGISTRY` env value with your actual ACR login server:

```yaml
env:
  REGISTRY: <ACR_LOGIN_SERVER>    # e.g. ewaanalyzeracr.azurecr.io
```

### Triggering the workflow

The `deploy-to-azure-webapps.yml` workflow runs automatically on push to `azure-migration`. You can also trigger it manually from GitHub → Actions → **Deploy Containers to Azure Web Apps** → **Run workflow**.

Once triggered it will:
1. Build the backend image from `./backend`.
2. Build the frontend image from `./sapui5`.
3. Push both to ACR tagged with the commit SHA and `latest`.
4. Point both Web Apps at the new image tag.
5. Restart both Web Apps.
