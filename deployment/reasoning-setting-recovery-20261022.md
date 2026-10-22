# Retry failed before analysis: invalid reasoning setting

The 22 October retry of `F1P_06_Sep_26.html` failed on revision
`ewa-analyzer--0000050` at 08:49:20Z. Live Blob metadata and Log Analytics both
reported a Pydantic configuration validation error: `reasoning.deep` received
`x-high`; the accepted value is `xhigh`.

Read-only inspection confirmed `SPECIALIST_REASONING_EFFORT=x-high` on the
Container App. The other analysis roles had valid values. Configuration loading
failed before analysis began. This differs from the 20 October interruption:
the heartbeat/status fix correctly persisted the new failure and cleared the
processing flag, but did not validate the live pipeline configuration.

The Actions deployment migration now corrects the exact `x-high` spelling
(ignoring outer whitespace/case) to `xhigh` for the known reasoning settings.
It changes the image and correction together. Other values, model selections,
unrelated settings, and secret references are preserved; no secret values are
read. Backend validation remains strict.

Regression checks cover the original spelling across all supported reasoning
setting names, preserved valid/unrelated settings, preserved secret references,
one scoped Azure update, and idempotence. The new checks reproduced the defect
before the deployment migration was changed.

Release acceptance requires the Actions run to succeed, the live setting to be
`xhigh`, and the running image's `load_config()` to accept the actual environment.
This verifies the reported configuration failure. Successful model inference and
workbook generation require a real report run and must be reported separately.
