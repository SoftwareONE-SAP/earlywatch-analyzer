# Azure Migration Guide

Start from this clone folder: `C:\GenAI\ewa_analyzer_azure`.

## Recommended Target

Use the minimum moving-parts Azure shape:

- one Azure Container App running the combined image from `Dockerfile.containerapp`
- one Azure Container Apps environment
- one Azure Container Registry
- one Azure Storage account plus blob container
- one Azure OpenAI or Azure AI Services resource
- optional Azure Key Vault
- Microsoft Entra ID authentication enabled on the Container App

This keeps the frontend and backend on the same origin, removes the need for a second frontend host, and lets the backend scale to zero when idle.

## Deployment Checklist

### 1. Preflight and Safety

- [ ] Confirm you are working from the correct clone and branch.
- [ ] Verify Azure CLI, Docker, Node.js 20+, Python 3.12+, and Git are available where needed.
- [ ] Identify the target Azure subscription, resource group, and region.
- [ ] Rotate any credentials that were ever stored in plaintext files.
- [ ] Confirm no real secrets will be copied into source-controlled files.
- [ ] Confirm this is an Azure-only deployment with no BTP fallback requirement.

### 2. Confirm Runtime Expectations

- [ ] Review [docs/RUNTIME_ARCHITECTURE.md](RUNTIME_ARCHITECTURE.md).
- [ ] Confirm Azure Blob Storage remains the only persistent store.
- [ ] Confirm the Azure OpenAI deployment names that will be used.
- [ ] Confirm Microsoft Entra app roles `Viewer` and `Administrator` will be assigned.

### 3. Create Azure Resources

- [ ] Create or identify a resource group.
- [ ] Create or identify an Azure Container Registry.
- [ ] Create or identify a storage account and blob container.
- [ ] Create or identify an Azure OpenAI or Azure AI Services resource.
- [ ] Create a Container Apps environment.
- [ ] Create a bootstrap Container App.
- [ ] Decide whether a Key Vault will be used for secret storage.

### 4. Configure Runtime and Authentication

- [ ] Set the backend runtime variables on the Container App.
- [ ] Set `AUTH_ENABLED=true`.
- [ ] Set `TRUST_PLATFORM_AUTH_HEADERS=true`.
- [ ] Enable Container Apps built-in Microsoft Entra authentication.
- [ ] Require login for unauthenticated requests.

### 5. Configure GitHub Deployment

- [ ] Add the required GitHub repository secrets.
- [ ] Use `.github/workflows/deploy-to-containerapp.yml` for image pushes and app updates.
- [ ] Run the workflow once to replace the bootstrap image with the real app image.

### 6. Validate the Azure Deployment

- [ ] Open the app URL and verify Entra sign-in is required.
- [ ] Confirm `/api/health` returns successfully after sign-in.
- [ ] Upload a small EWA file and confirm Blob artifacts are created.
- [ ] Run an analysis and confirm Excel export works.
- [ ] Confirm the app scales to zero when idle.

## 1. Rotate Secrets First

Rotate any credentials that were ever present in local plaintext files before deploying:

- Azure Storage account keys or connection strings
- Azure OpenAI keys
- Azure AI Foundry or Anthropic keys if still used
- ACR credentials
- Azure credentials if still used

Do not copy `mtaext.yaml`, `.env`, or other local config files into source control.

## 2. Azure Resources To Create

Create or identify these Azure resources:

- Resource group, for example `rg-ewa-analyzer-prod`
- Azure Container Registry, for example `myregistry.azurecr.io`
- Storage account and blob container, for example `earlywatch`
- Azure OpenAI or Azure AI Services resource with the required model deployments
- Container Apps environment, for example `env-ewa-analyzer-prod`
- Bootstrap Container App, for example `ewa-analyzer`
- Optional Key Vault for secrets

## 3. Create Azure Resources With CLI

Adjust names before running:

```powershell
$location = "uksouth"
$rg = "rg-ewa-analyzer-prod"
$acr = "<globally-unique-acr-name>"
$storage = "<globally-unique-storage-name>"
$container = "earlywatch"
$caEnv = "env-ewa-analyzer-prod"
$app = "ewa-analyzer"

az group create --name $rg --location $location
az acr create --resource-group $rg --name $acr --sku Basic --admin-enabled true
az storage account create --resource-group $rg --name $storage --location $location --sku Standard_LRS
az storage container create --name $container --account-name $storage --auth-mode login
az containerapp env create --name $caEnv --resource-group $rg --location $location

# Bootstrap app so runtime settings and auth can be configured before the first real deploy.
az containerapp create --name $app --resource-group $rg --environment $caEnv `
  ## Legacy Notes

  Older Azure Web Apps and SAP BTP migration snippets have been removed from the active runbook.

## 8. Validation Checklist

- Open the Container App URL and confirm sign-in is required.
- Confirm the app loads from a single origin and UI API calls stay on that origin.
- Confirm `/api/health` returns successfully.
- Upload a small EWA file and confirm blobs appear in the configured container.
- Run AI analysis and export Excel.
- Confirm the Container App revision can scale back to zero when the app is idle.

## 9. Common Failures

App loads but API calls return 401 or 403:

- Confirm `AUTH_ENABLED=true` and `TRUST_PLATFORM_AUTH_HEADERS=true` are set.
- Confirm Container Apps built-in auth is enabled and unauthenticated requests redirect to login.
- Confirm users have Entra app roles named `Viewer` or `Administrator`.

Backend fails on startup:

- Missing `AZURE_STORAGE_CONNECTION_STRING` or `AZURE_STORAGE_CONTAINER_NAME`.
- Wrong Azure OpenAI endpoint, key, or deployment name.
- Check Container App logs for the exact missing variable.

Workflow pushes image but app does not update:

- Confirm `AZURE_CONTAINER_APP_NAME` and `AZURE_CONTAINERAPPS_ENVIRONMENT` secrets are correct.
- Confirm the ACR credentials in GitHub match the registry attached to the Container App.

## Legacy Notes

Legacy SAP BTP deployment assets may still exist in the repository, but they are not part of the supported Azure deployment path.

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

## Legacy Notes

Legacy SAP BTP deployment assets may still exist in the repository, but they are not part of the supported Azure deployment path.

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
