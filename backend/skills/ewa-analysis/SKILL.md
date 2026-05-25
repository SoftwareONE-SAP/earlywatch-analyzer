---
name: ewa-analysis
description: >
  SAP EarlyWatch Alert (EWA) analysis guidance for system health reports. Use
  this skill when analyzing EWA report sections, selecting domain thresholds,
  calibrating severity, writing SAP Basis remediation, or correlating findings.
---

# SAP EarlyWatch Alert Analysis

Use this skill for SAP EWA report analysis. The backend loads this entrypoint
only after a section has selected `ewa-analysis`.

Detailed guidance is split into references so the backend can load only the
material needed by the current section:

- `core-analysis`: analysis workflow, severity calibration, finding format, and
  common EWA section types.
- `thresholds-performance`: workload, CPU, memory pressure indicators at the OS
  level, and response-time thresholds.
- `thresholds-memory`: SAP extended memory, heap, roll, and buffer thresholds.
- `thresholds-database`: database latency, cache, SQL, growth, and tablespace
  thresholds.
- `thresholds-batch`: batch job, background work process, and scheduler
  thresholds.
- `thresholds-security`: users, password, RFC, kernel, and patching thresholds.
- `thresholds-operations`: spool, transport, system log, dump, ICM, enqueue,
  and maintenance thresholds.
- `remediation-memory`: memory and buffer remediation playbooks.
- `remediation-database`: database remediation playbooks.
- `remediation-batch`: batch processing remediation playbooks.
- `remediation-security`: security remediation playbooks.
- `remediation-operations`: operational cleanup, transport, dump, spool, and
  connectivity remediation playbooks.
- `correlations`: cross-domain compound risk patterns.

Do not load every reference by default. Pick the smallest set that matches the
section being analyzed.
