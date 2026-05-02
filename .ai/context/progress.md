# Progress

**Last Updated:** 2026-05-02 (Handover 0002)

## Active Task

Repository cleanup is complete, and the Azure deployment path has been shifted to a single Azure Container App architecture with same-origin frontend hosting, GitHub Actions deployment, and Microsoft Entra authentication support.

## Completed (Recent)

| Date | Item |
|------|------|
| 2026-05-01 | Initialized local git repository and created the first commit |
| 2026-05-01 | Removed dead legacy backend modules, prompts, and schemas |
| 2026-05-01 | Trimmed unused V2 and Anthropic runtime config variables |
| 2026-05-01 | Verified the working tree is clean after the initial commit |
| 2026-05-01 | Created the first structured handover file |
| 2026-05-02 | Added same-container SAPUI5 static serving to `backend/ewa_main.py` |
| 2026-05-02 | Added Container Apps auth-header trust support via `TRUST_PLATFORM_AUTH_HEADERS` |
| 2026-05-02 | Switched deployed frontend API calls to same-origin instead of a separate Azure backend hostname |
| 2026-05-02 | Added `Dockerfile.containerapp` and `.github/workflows/deploy-to-containerapp.yml` |
| 2026-05-02 | Rewrote Azure deployment docs for the single-Container-App target |

## Blocked

- Docker is not available in the current local environment, so the combined image has not been build-validated here.

## Next Steps

1. Add the required GitHub Actions secrets and bootstrap the Azure Container App in the target subscription.
2. Run the first real Container Apps deployment and verify Microsoft Entra sign-in, Blob storage access, and analysis/export flows.
3. If stricter secret handling is required, move sensitive runtime values from plain Container App environment variables to Container App secrets or Key Vault references.
