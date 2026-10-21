# Interrupted analysis recovery

## Incident evidence

Read-only Azure inspection on 21 October 2026 identified the affected source as
`F1P_06_Sep_26.html` in the `earlywatch` container. Its metadata was still
`processing=true`, `last_status=processing`, last modified at
`2026-10-20T12:07:58Z`. No matching output artifacts existed.

Log Analytics showed that revision `ewa-analyzer--0000048` accepted the job at
12:07:58Z, discovered 433 sections, and reached planning at 12:08:09Z. At
12:08:34Z it logged `Shutting down` and `Waiting for background tasks to complete`
during replacement by revision `0000049`. The current replica contained no
pipeline temporary directory and had not resumed the job. This is an interrupted
in-process worker with abandoned persistent status, rather than evidence of an
AI request running for hours.

## Behavior of the fix

- Both asynchronous analysis endpoints atomically claim source metadata using
  its ETag. Concurrent starts enqueue only one run, and storage failures prevent
  untracked work from starting.
- Each run stores an ID, start time, heartbeat time, and Container App revision.
  The worker renews its heartbeat every 30 seconds while the workflow runs.
- File-list polling recovers runs whose heartbeat is at least five minutes old:
  it clears ownership and reports Failed with an interruption/retry message.
  Legacy runs without heartbeats use the source blob's last-modified time.
- A retry can reclaim an abandoned run even before the next file-list poll.
  There is no automatic retry or automatic model spend.
- Terminal status and cleared ownership are written together. Cancellation
  attempts to persist failure immediately; a hard kill is recovered by expiry.
- Conditional metadata updates protect new claims and heartbeats from stale
  polling/cleanup. A worker that loses ownership is cancelled and must verify
  ownership before beginning artifact publication.
- Source contents and customer/report metadata are preserved. Healthy long runs
  remain Processing while their worker renews its heartbeat.

## Verification and release acceptance

The synthetic regression suite covers legacy recovery, active long jobs,
heartbeat expiry, concurrent claims, polling/heartbeat races, stale owners,
terminal states, failure/cancellation, both enqueue endpoints, actual file-list
response fields, and prevention of publication by an already retired run.
It performs no Azure writes or model calls.

Local verification on Python 3.12: all 77 backend tests (including 21 recovery
tests) and all 8 deployment migration tests passed; `git diff --check` passed.
The cached test environment required reinstallation of its existing AnyIO
version to restore a missing asyncio backend file. No dependency requirement
changed. Direct review found no blocking issues. The user authorized committing,
pushing, and deploying this fix on 21 October. Offline checks do not establish
deployment success or successful real-report inference.

Release through the existing GitHub Actions workflow after authorization. Verify:

1. The workflow and new revision are healthy and the image SHA matches the commit.
2. Refreshing the file list changes the affected document from Processing to
   Failed, with a message asking to run analysis again.
3. A user-requested retry changes it to Processing with a new run ID and advancing
   heartbeat. A second start while that run is live does not enqueue another run.
4. A successful real analysis saves the workbook and clears Processing. This
   requires real model inference and is not established by offline tests.

The worker still runs inside the web container. This fix detects interruption
and enables explicit retry; it does not make work survive container replacement
or resume partial results. Cancelling an asyncio task cannot terminate an
already-running synchronous model/storage call in its thread. The ownership
check prevents a retired pipeline from starting artifact publication, but is not
a transaction across the three separately uploaded artifact blobs.
