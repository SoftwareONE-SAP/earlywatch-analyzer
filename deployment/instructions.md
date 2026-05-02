# Deployment Instructions

This file is the short operational checklist. Use [docs/AZURE_MIGRATION_GUIDE.md](../docs/AZURE_MIGRATION_GUIDE.md) for the full runbook and command examples.

## Step 1: Preflight and Safety

### Goal

Start from a clean workspace with rotated secrets and a clear Azure target.

### Checklist

- [ ] Confirm you are working in the correct repository and branch.
- [ ] Verify Azure CLI, Docker, Node.js 20+, Python 3.12+, and Git are available where needed.
- [ ] Identify the target Azure subscription, resource group, and region.
- [ ] Rotate any credentials that may have existed in plaintext files.
- [ ] Confirm no real secrets will be copied into source-controlled files.
- [ ] Decide whether BTP fallback must remain available.

### Exit Criteria

- Workspace and branch are confirmed.
- Required tools are available.
- Secrets have been rotated or reviewed.
- Azure deployment target is identified.

## Step 2: Confirm Runtime Expectations

### Goal

Confirm the one-container Azure runtime before creating infrastructure.

### Checklist

- [ ] Read [docs/RUNTIME_ARCHITECTURE.md](../docs/RUNTIME_ARCHITECTURE.md).
- [ ] Confirm Azure Blob Storage is the only persistent store.
- [ ] Confirm frontend and backend will run in one Azure Container App.
- [ ] Confirm same-origin hosting is intended, with no separate frontend host.
- [ ] Confirm the Azure OpenAI endpoint and exact deployment names.
- [ ] Confirm Microsoft Entra app roles `Viewer` and `Administrator` will be assigned.
- [ ] Confirm runtime will use `AUTH_ENABLED=true` and `TRUST_PLATFORM_AUTH_HEADERS=true`.

### Exit Criteria

- Storage, model, and auth requirements are known.
- The deployment target is clearly a single Container App, not split Web Apps.

## Step 3: Create Azure Resources

### Goal

Provision the minimum Azure services for the one-container deployment.

### Required Resources

- Resource group
- Azure Container Registry
- Storage account
- Blob container
- Azure OpenAI or Azure AI Services resource
- Container Apps environment
- Bootstrap Container App
- Optional Key Vault

### Notes

- The backend should not rely on local disk for persistent data.
- The storage container must exist before runtime settings are configured.
- The Container App should be created with `min-replicas 0` so it can scale to zero.

## Step 4: Configure Runtime and Authentication

### Goal

Configure the Container App so the combined backend and frontend can run securely.

### Checklist

- [ ] Set backend runtime variables on the Container App.
- [ ] Set `ENVIRONMENT=production`.
- [ ] Set `AUTH_ENABLED=true`.
- [ ] Set `TRUST_PLATFORM_AUTH_HEADERS=true`.
- [ ] Enable Container Apps built-in Microsoft Entra authentication.
- [ ] Require login for unauthenticated requests.
- [ ] Confirm users or groups have Entra roles `Viewer` or `Administrator`.

### Notes

- Same-origin hosting means no frontend URL rewrite is needed.
- Same-origin hosting also means explicit CORS configuration is usually unnecessary.

## Step 5: Configure GitHub Deployment

### Goal

Use GitHub Actions to build the combined image and update the Container App on each deployment.

### Checklist

- [ ] Add the required GitHub Actions secrets.
- [ ] Confirm `.github/workflows/deploy-to-containerapp.yml` matches the target Azure names.
- [ ] Run the workflow once to replace the bootstrap image with the real combined image.
- [ ] Confirm ACR contains both the `latest` tag and the commit-SHA tag.

### Required GitHub Secrets

- `ACR_LOGIN_SERVER`
- `REGISTRY_USERNAME`
- `REGISTRY_PASSWORD`
- `AZURE_CREDENTIALS`
- `AZURE_RESOURCE_GROUP`
- `AZURE_CONTAINER_APP_NAME`
- `AZURE_CONTAINERAPPS_ENVIRONMENT`

## Step 6: Validate the Deployment

### Goal

Verify the app works end-to-end in Azure.

### Checklist

- [ ] Open the Container App URL and confirm sign-in is required.
- [ ] Confirm `/api/health` responds after authentication.
- [ ] Confirm the UI and API run from the same origin.
- [ ] Upload a small EWA file and confirm blobs appear in the configured container.
- [ ] Run an analysis and confirm Excel export works.
- [ ] Confirm the Container App can scale back to zero when idle.

## Step 7: Optional BTP Fallback

### Goal

Retain BTP deployment assets without mixing them into the Azure runtime.

### Checklist

- [ ] Keep `mta.yaml`, `xs-security.json`, `approuter/`, and `ui-deployer/` in the repo.
- [ ] Keep `mtaext.example.yaml` as the template only.
- [ ] Create `mtaext.yaml` only in a secure local or CI environment.
- [ ] Do not commit `mtaext.yaml`.

## References

- [docs/AZURE_MIGRATION_GUIDE.md](../docs/AZURE_MIGRATION_GUIDE.md)
- [docs/RUNTIME_ARCHITECTURE.md](../docs/RUNTIME_ARCHITECTURE.md)
- [backend/.env.example](../backend/.env.example)
