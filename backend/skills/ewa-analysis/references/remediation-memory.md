# Memory and Buffer Remediation

## Extended Memory Exhaustion

Symptoms: EM utilization above 95%, heap escalation, PRIV mode, storage parameter
errors, or user context swapping.

Actions:

- Use `AL05` and `SM04` to identify high-memory users and sessions.
- Use `SM50` to check PRIV mode work processes.
- Increase `em/initial_size_MB` in `RZ10` after validating host memory headroom.
- Review `em/max_size_MB`, `ztta/roll_area`, and `abap/heap_area_*` for related
  limits.
- Coordinate restart if profile parameters require it.

Effort: Medium. Priority: Immediate if users are failing, Short-term if trending.

## Buffer Quality Degradation

Symptoms: buffer hit ratio below 95%, increasing swaps, or low free directory/data
areas in `ST02`.

Actions:

- Use `ST02` to identify the affected buffer.
- Increase only the affected buffer parameter, for example `abap/buffersize`,
  `zcsa/table_buffer_area`, `rtbb/buffer_length`, or `rsdb/ntab/buffersize`.
- Validate memory headroom before increasing buffers.
- Recheck swaps after restart and normal workload.

Effort: Low to Medium. Priority: Short-term unless response time is affected.
