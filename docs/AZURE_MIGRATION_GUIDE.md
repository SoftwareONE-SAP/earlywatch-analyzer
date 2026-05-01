# Azure Migration Guide

Start from this clone folder: `C:\GenAI\ewa_analyzer_azure_min`.

## Deployment Checklist

Use this as the working checklist for an Azure migration. Complete the items in order and do not skip the validation gates between phases.

### 1. Preflight and Safety

- [ ] Confirm you are working from the correct clone and branch.
- [ ] Verify you have access to Azure CLI, Docker, Node.js 20+, Python 3.12+, and Git.
- [ ] Identify the target Azure subscription, resource group, and region.
- [ ] Rotate any credentials that were ever stored in local plaintext files.
- [ ] Confirm no real secrets will be copied into `mtaext.yaml`, `.env`, or source-controlled config files.
- [ ] Decide whether this deployment is Azure-only or needs BTP fallback preserved.

### 2. Confirm Runtime Expectations

- [ ] Review the backend runtime variables in [docs/RUNTIME_ARCHITECTURE.md](RUNTIME_ARCHITECTURE.md).
- [ ] Confirm blob storage will be the only persistent store for uploads, analysis JSON, workbook payloads, and generated Excel output.
- [ ] Decide whether initial smoke testing will run with `AUTH_ENABLED=false`.
- [ ] Confirm the Azure OpenAI or Azure AI Foundry model deployment names that will be used.

### 3. Create Azure Resources

- [ ] Create or identify a resource group.
- [ ] Create or identify an Azure Container Registry.
- [ ] Create or identify a storage account.
- [ ] Create the blob container used for runtime artifacts.
- [ ] Create or identify the Azure OpenAI / Azure AI Services resource.
- [ ] Create the Linux App Service Plan.
- [ ] Create the backend Web App for Containers.
- [ ] Create the frontend Web App for Containers.
- [ ] Decide whether a Key Vault will be used for secrets.

### 4. Configure Backend Settings

- [ ] Set `AZURE_STORAGE_CONNECTION_STRING` in Web App settings, not in files.
- [ ] Set `AZURE_STORAGE_CONTAINER_NAME` to the intended blob container.
- [ ] Set `PROVIDER` to `openai` or `anthropic`.
- [ ] Set `AZURE_OPENAI_ENDPOINT` to the Azure endpoint.
- [ ] Set `AZURE_OPENAI_API_KEY` from a secure secret store.
- [ ] Set `AZURE_OPENAI_API_VERSION` to the supported version.
- [ ] Set the model deployment names for summary, parameter, fast, and chat requests.
- [ ] Set reasoning-effort flags if the deployment expects them.
- [ ] Keep `AUTH_ENABLED=false` only for the initial smoke test unless Entra auth is already configured.

### 5. Align Frontend With Backend URL

- [ ] Confirm the backend Web App hostname.
- [ ] Update `sapui5/webapp/model/config.js` if the backend hostname differs from the default.
- [ ] Update `sapui5/webapp/chat.html` if the backend hostname differs from the default.
- [ ] Search for any remaining hardcoded backend URL references before building the frontend image.

### 6. Configure Cross-Origin Access

- [ ] Add the frontend Web App origin to backend CORS.
- [ ] Add any custom domain origin if one will be used.
- [ ] Recheck that the origin matches the deployed frontend hostname exactly.

### 7. Build and Smoke Test Locally

- [ ] Build the backend container locally.
- [ ] Build the frontend container locally.
- [ ] Run the backend container with the target Azure settings if you need an end-to-end smoke test.
- [ ] Verify the backend health endpoint responds successfully.
- [ ] Verify the frontend build completes without errors.

### 8. Publish Images to ACR

- [ ] Log in to Azure Container Registry.
- [ ] Tag the backend image for the registry.
- [ ] Tag the frontend image for the registry.
- [ ] Push both images to ACR.
- [ ] Confirm both repositories exist in the registry after push.

### 9. Point Web Apps to Container Images

- [ ] Configure the backend Web App to use the pushed backend image.
- [ ] Configure the frontend Web App to use the pushed frontend image.
- [ ] Provide the ACR credentials or managed identity path you have chosen.
- [ ] Restart both Web Apps after image configuration.

### 10. Validate the Azure Deployment

- [ ] Open the backend health endpoint in Azure.
- [ ] Confirm backend logs are clean enough to show the app started successfully.
- [ ] Open the frontend index page in Azure.
- [ ] Confirm browser requests go to the intended backend hostname.
- [ ] Upload a small EWA file and confirm Azure Blob artifacts are created.
- [ ] Run an analysis and confirm Excel export works.
- [ ] Confirm the app can list or create blobs in the configured container.

### 11. Production Hardening

- [ ] Re-enable auth if it was disabled for smoke testing.
- [ ] Confirm no secrets are committed anywhere in the repo.
- [ ] Confirm model deployment names match the Azure deployment names exactly.
- [ ] Verify timeouts are sufficient for long-running analysis requests.
- [ ] Confirm backup and restore expectations for the storage account are documented.

### 12. Optional BTP Fallback

- [ ] Keep `mta.yaml`, `xs-security.json`, `approuter/`, and `ui-deployer/` in place if a rollback path is required.
- [ ] Copy `mtaext.example.yaml` to `mtaext.yaml` only in a secure local or CI environment.
- [ ] Fill BTP values from a secret store, not from ad hoc plaintext files.
- [ ] Avoid committing `mtaext.yaml`.
- [ ] Run the BTP deployment script only if BTP fallback is part of the migration plan.

This guide migrates the app to Azure using two Linux Web Apps for Containers:

- backend Web App: runs `backend/Dockerfile`
- frontend Web App: runs `sapui5/Dockerfile`
- Azure Container Registry: stores both images
- Azure Blob Storage: stores all app data/artifacts
- Azure OpenAI or Azure AI Foundry: model provider

## 1. Rotate Secrets First

Rotate any credentials that were ever present in local plaintext files before deploying:

- Azure Storage account keys/connection strings
- Azure OpenAI keys
- Azure AI Foundry/Anthropic keys
- ACR credentials
- Cloud Foundry/BTP credentials if still used

Do not copy `mtaext.yaml`, `.env`, or `backend/config.yaml` into source control.

## 2. Prerequisites

Install locally if you will validate/build from your machine:

- Docker Desktop
- Azure CLI
- Node.js 20+
- Python 3.12+
- Git

Optional for BTP fallback/hybrid deployment:

- Cloud Foundry CLI v8
- CF MultiApps plugin
- MTA Build Tool (`mbt`)

## 3. Azure Resources To Create

Create or identify these Azure resources:

- Resource group, for example `rg-ewa-analyzer-prod`
- Azure Container Registry, for example `myregistry.azurecr.io`
- Storage account and blob container, for example `earlywatch`
- Azure OpenAI/AI Services resource with the required model deployments
- App Service Plan for Linux containers
- Backend Web App for Containers, for example `sap-ewa-analyzer-backend`
- Frontend Web App for Containers, for example `sap-ewa-analyzer-ui`
- Optional Key Vault for secret storage

## 4. Create Azure Resources With CLI

Adjust names before running:

```powershell
$location = "uksouth"
$rg = "rg-ewa-analyzer-prod"
$acr = "<globally-unique-acr-name>"
$storage = "<globally-unique-storage-name>"
$container = "earlywatch"
$plan = "asp-ewa-analyzer-prod"
$backendApp = "sap-ewa-analyzer-backend"
$frontendApp = "sap-ewa-analyzer-ui"

az group create --name $rg --location $location
az acr create --resource-group $rg --name $acr --sku Basic --admin-enabled true
az storage account create --resource-group $rg --name $storage --location $location --sku Standard_LRS
az storage container create --name $container --account-name $storage --auth-mode login
az appservice plan create --resource-group $rg --name $plan --is-linux --sku B1
az webapp create --resource-group $rg --plan $plan --name $backendApp --deployment-container-image-name nginx
az webapp create --resource-group $rg --plan $plan --name $frontendApp --deployment-container-image-name nginx
```

If `az storage container create --auth-mode login` fails because of RBAC, create the container in the Azure Portal or use an account key.

## 5. Configure Backend App Settings

Set backend runtime values as Azure Web App settings, not files.

```powershell
$storageConnection = az storage account show-connection-string --resource-group $rg --name $storage --query connectionString -o tsv

az webapp config appsettings set --resource-group $rg --name $backendApp --settings `
  ENVIRONMENT=production `
  AUTH_ENABLED=false `
  AZURE_STORAGE_CONNECTION_STRING="$storageConnection" `
  AZURE_STORAGE_CONTAINER_NAME="$container" `
  PROVIDER=openai `
  AZURE_OPENAI_ENDPOINT="<your-azure-openai-endpoint>" `
  AZURE_OPENAI_API_KEY="<your-azure-openai-key>" `
  AZURE_OPENAI_API_VERSION="2025-03-01-preview" `
  AZURE_OPENAI_SUMMARY_MODEL="<deployment-name>" `
  AZURE_OPENAI_PARAM_MODEL="<deployment-name>" `
  AZURE_OPENAI_FAST_MODEL="<deployment-name>" `
  AZURE_OPENAI_CHAT_MODEL="<deployment-name>" `
  SUMMARY_REASONING_EFFORT=none `
  PARAM_REASONING_EFFORT=none
```

Set `AUTH_ENABLED=false` for the first migration smoke test unless you have already configured Entra ID auth. Re-enable auth after the basic backend/frontend path works.

## 6. Configure Frontend Backend URL

Before building the frontend image, update these files if your backend Web App URL is not `https://sap-ewa-analyzer-backend.azurewebsites.net`:

- `sapui5/webapp/model/config.js`
- `sapui5/webapp/chat.html`

Search for `sap-ewa-analyzer-backend.azurewebsites.net` and replace it with your backend hostname.

## 7. Configure CORS

Allow the frontend origin on the backend Web App:

```powershell
az webapp cors add --resource-group $rg --name $backendApp --allowed-origins "https://$frontendApp.azurewebsites.net"
```

If you use a custom domain, add that origin too.

## 8. Local Build Smoke Tests

From `C:\GenAI\ewa_analyzer_azure_min`:

```powershell
docker build -t ewa-backend:local ./backend
docker build -t ewa-sapui5:local ./sapui5
```

Optional backend run:

```powershell
docker run --rm -p 8001:8001 `
  -e AZURE_STORAGE_CONNECTION_STRING="<connection-string>" `
  -e AZURE_STORAGE_CONTAINER_NAME="earlywatch" `
  -e PROVIDER="openai" `
  -e AZURE_OPENAI_ENDPOINT="<endpoint>" `
  -e AZURE_OPENAI_API_KEY="<key>" `
  -e AZURE_OPENAI_API_VERSION="2025-03-01-preview" `
  -e AZURE_OPENAI_SUMMARY_MODEL="<deployment>" `
  ewa-backend:local
```

Check backend health:

```powershell
Invoke-WebRequest http://localhost:8001/api/health
```

## 9. Push Images To ACR Manually

```powershell
$acrLoginServer = az acr show --resource-group $rg --name $acr --query loginServer -o tsv
az acr login --name $acr

docker tag ewa-backend:local "$acrLoginServer/ewa-backend:latest"
docker tag ewa-sapui5:local "$acrLoginServer/ewa-sapui5:latest"

docker push "$acrLoginServer/ewa-backend:latest"
docker push "$acrLoginServer/ewa-sapui5:latest"
```

## 10. Point Web Apps At Images

```powershell
$acrUsername = az acr credential show --resource-group $rg --name $acr --query username -o tsv
$acrPassword = az acr credential show --resource-group $rg --name $acr --query passwords[0].value -o tsv

az webapp config container set `
  --resource-group $rg `
  --name $backendApp `
  --container-image-name "$acrLoginServer/ewa-backend:latest" `
  --container-registry-url "https://$acrLoginServer" `
  --container-registry-user "$acrUsername" `
  --container-registry-password "$acrPassword"

az webapp config container set `
  --resource-group $rg `
  --name $frontendApp `
  --container-image-name "$acrLoginServer/ewa-sapui5:latest" `
  --container-registry-url "https://$acrLoginServer" `
  --container-registry-user "$acrUsername" `
  --container-registry-password "$acrPassword"

az webapp restart --resource-group $rg --name $backendApp
az webapp restart --resource-group $rg --name $frontendApp
```

## 11. GitHub Actions Deployment

The clone includes `.github/workflows/deploy-to-azure-webapps.yml`.

Create these GitHub repository secrets:

| Secret | Purpose |
| --- | --- |
| `ACR_LOGIN_SERVER` | Example: `myregistry.azurecr.io`. |
| `REGISTRY_USERNAME` | ACR username or service principal username. |
| `REGISTRY_PASSWORD` | ACR password or service principal password. |
| `AZURE_CREDENTIALS` | JSON credentials for `azure/login`. |
| `AZURE_RESOURCE_GROUP` | Resource group containing Web Apps. |
| `AZURE_BACKEND_WEBAPP_NAME` | Backend Web App name. |
| `AZURE_FRONTEND_WEBAPP_NAME` | Frontend Web App name. |

Create `AZURE_CREDENTIALS` with a service principal:

```powershell
az ad sp create-for-rbac `
  --name "sp-ewa-analyzer-deploy" `
  --role contributor `
  --scopes "/subscriptions/<subscription-id>/resourceGroups/<resource-group>" `
  --sdk-auth
```

Store the JSON output as the `AZURE_CREDENTIALS` secret.

Push to the `azure-migration` branch or run the workflow manually.

## 12. Verification Checklist

Backend:

- Open `https://<backend-app>.azurewebsites.net/api/health`.
- Check backend logs in Azure Portal or with `az webapp log tail`.
- Confirm the backend can list/create blobs in the configured container.

Frontend:

- Open `https://<frontend-app>.azurewebsites.net/index.html`.
- Confirm browser network calls go to the intended backend URL.
- Upload a small EWA file and confirm Azure Blob artifacts are created.
- Run AI analysis and export Excel.

Operational:

- Confirm no secrets are committed.
- Confirm ACR has both image repositories.
- Confirm Web Apps restart cleanly.
- Confirm model deployment names match Azure OpenAI deployment names, not generic model names.

## 13. BTP Fallback

The clone still includes BTP deployment assets:

- `mta.yaml`
- `xs-security.json`
- `approuter/`
- `ui-deployer/`
- `.github/workflows/deploy-to-btp.yml`
- `scripts/deploy-local-btp.ps1`
- `mtaext.example.yaml`

To deploy to BTP manually, copy `mtaext.example.yaml` to `mtaext.yaml` in a secure local environment, fill values from your secret store, then run:

```powershell
.\scripts\deploy-local-btp.ps1
```

Do not commit `mtaext.yaml`.

## 14. Common Failures

Frontend loads but API calls fail:

- Update hardcoded backend URL in `sapui5/webapp/model/config.js` and `sapui5/webapp/chat.html`.
- Rebuild and redeploy the frontend image.
- Check CORS on the backend Web App.

Backend fails on startup:

- Missing `AZURE_STORAGE_CONNECTION_STRING` or `AZURE_STORAGE_CONTAINER_NAME`.
- Wrong Azure OpenAI endpoint/key/deployment name.
- Check container logs for the exact missing variable.

AI calls fail:

- Confirm deployment names match Azure OpenAI deployment names.
- Confirm API version is supported by the resource.
- Confirm quota/capacity exists for the selected model.

Uploads succeed but files do not appear:

- Confirm blob container name.
- Confirm storage connection string belongs to the intended account.
- Confirm Web App setting changes were followed by restart.
