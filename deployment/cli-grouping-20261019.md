# CLI settings and grouping deployment — 2026-10-19

Deployment target: `ewa-analyzer` in `rg-ewa-analyzer-prod`, subscription `DEV.SAP.TEST1`.
The live source checkout is `C:/GenAI/earlywatch-analyzer`. The older public
checkout at `C:/GenAI/ewa-ai-analyzer` and the CLI checkout were left unchanged.

## Portal-editable settings

These are runtime environment variables, not image build arguments. They can all
be changed without rebuilding the image. In Azure Portal select the Container App,
then **Revisions and replicas > Create new revision**. Edit the existing application
container, change **Environment variables** with source **Manual**, and create the
revision. See [Microsoft's environment-variable instructions](https://learn.microsoft.com/en-us/azure/container-apps/environment-variables).

| Variable | Deployed value |
| --- | --- |
| `ORCHESTRATOR_MODEL` | `gpt-6-luna` |
| `ORCHESTRATOR_REASONING_EFFORT` | `xhigh` |
| `SPECIALIST_MODEL` | `gpt-6.1-sol` |
| `CHAT_MODEL` | `gpt-6.1-sol` (preserved from the previous chat setting) |
| `SPECIALIST_REASONING_EFFORT` | `medium` |
| `CROSS_REFERENCE_MODEL` | `gpt-6.1-sol` |
| `CROSS_REFERENCE_REASONING_EFFORT` | `high` |
| `SYNTHESIS_MODEL` | `gpt-6.1-sol` |
| `SYNTHESIS_REASONING_EFFORT` | `high` |
| `MAX_CONCURRENCY` | `10` |
| `REQUEST_TIMEOUT_SECONDS` | `600` |
| `PLANNING_TIMEOUT_SECONDS` | `600` |
| `MAX_TASK_SECTIONS` | `12` |
| `MAX_TASK_CONTENT_CHARS` | `48000` |
| `MAX_PARENT_CONTEXT_CHARS` | `4000` |

The October 20 cleanup removes the legacy model aliases. Use `ORCHESTRATOR_MODEL`,
`SPECIALIST_MODEL`, and the independent `CHAT_MODEL` setting. The Actions workflow
migrates missing current names from the existing model selections, then removes
all obsolete `V2_*` settings in the same update as the new image. Existing Portal
selections are preserved on repeated deployments. `SPECIALIST_REASONING_EFFORT`
still takes precedence over `DEEP_REASONING_EFFORT`.
Blank cross-reference/synthesis values inherit their corresponding planner
setting independently. Blank planner timeout inherits the request timeout.
`MAX_PARENT_CONTEXT_CHARS=0` disables supplementary ancestor excerpts.
Task count/source budgets must be positive. Timeouts are seconds and must be
positive. Three model retries is the code default, matching the CLI.

The running image was checked to contain no `/app/backend/config.yaml`; Portal
runtime settings are therefore not shadowed by a bundled YAML configuration.
Credentials, authentication, storage, routing, chat settings, and resources were
preserved by updating only the image and the 14 analysis environment variables.

## Grouping behavior

The CLI's hierarchy-aware planning module groups related sources, validates unique
ownership, splits groups to respect source budgets, and assigns omitted sources
to bounded hierarchy fallback tasks. Ancestor excerpts remain separate from owned
sources. A specialist request produces separately attributed per-source results;
usage is recorded once per request. Duplicate/unexpected source identities fail
the affected group. Missing source results produce explicit partial coverage.
An oversized individual source fails without truncation or a specialist call.

The existing web workbook layout is retained, with per-source findings and added
Analysis Tasks and Source Coverage sheets. Partial coverage/downstream failures
produce Unknown report health. Zero successfully analysed sources fail without
publishing a workbook. CLI-specific analysis-trace/evidence features were not
part of this port.

## Deployment workflow and verification

- Previous image: `ewaanalyzeracr.azurecr.io/ewa-analyzer:db814fb5712e79fd48f80e3b67e554dee7f27deb`.
- Previous revision: `ewa-analyzer--0000045`.
- Initial direct image: `ewaanalyzeracr.azurecr.io/ewa-analyzer:cli-grouping-20261019-205734-89431744`.
- Initial direct digest: `sha256:20a9fb99435ed77170c92cbfdac6fde685ff3d813f920c4856339e8d3e35d865`.
- Initial direct revision: `ewa-analyzer--cli-grouping-20261019-205734`.
- Initial ACR build `ca1`: Succeeded. Built on the deployed base image by digest, retaining
  its existing frontend, operating system dependencies, and Python packages.
- 53 offline tests passed locally on Python 3.12 and inside the deployment image.
  Tests include real Responses payload construction over mocked HTTP, grouped HTML
  through graph/JSON/Excel output, hierarchy fallback, Portal grouping overrides,
  source identity/coverage failures, and budget rejection without model calls.
- Read-only inspection inside the running revision confirmed all four roles'
  model/reasoning/600-second timeout settings, concurrency 10, and grouping
  limits 12/48000/4000. API `/api/ping` returned OK; frontend `/` returned HTTP 200
  over loopback. External unauthenticated access still returned HTTP 401.
- Azure reported Healthy, with 100% of traffic on the new revision.
- No live report/model-inference run was performed. Provider acceptance of the
  selected models/efforts and behavior on a real report remain unverified.
- The initial direct deployment was rolled back to the previous image under
  revision `ewa-analyzer--pipeline-reset-20261019` at the user's request. The
  requested Portal environment settings were retained for the pipeline deployment.

The release path is the existing
[`deploy-to-containerapp.yml`](../.github/workflows/deploy-to-containerapp.yml)
workflow in `SoftwareONE-SAP/earlywatch-analyzer`. A push to `main` builds the full
`Dockerfile.containerapp`, pushes commit-SHA and `latest` image tags to ACR, and
updates the Container App. The workflow retains the Portal-managed environment
values; do not bake them into the image or overwrite them on every deployment.

For release acceptance, verify the Actions run succeeds, the live image tag equals
the pushed commit SHA, the active revision is Healthy with 100% traffic, the
runtime settings match the table above, and `/api/ping` responds OK inside the
container. The initial direct image is retained only as historical evidence;
it is not the image to use for subsequent releases.
