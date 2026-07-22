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

Load `core-analysis` plus the smallest relevant threshold/remediation pair:

- `performance`, `memory`, `database`, `hana`, `batch`, `security`, or
  `operations` for the corresponding technical domain;
- `continuity` for system availability, ABAP updates, number ranges, and
  database-agnostic backup/recovery; use `hana` for HANA backup/recovery;
- `integration` for RFC, message server, ICM, and NetWeaver Gateway/OData;
- `lifecycle` for maintenance phases, versions, patches, and important notes;
- `data-management` for growth, large objects, archiving, reorganization, and
  DVM;
- `data-quality` for missing EWA collectors, grey ratings, SDCCN, BW/RCA, or
  CCDB gaps.

Pair names map to `thresholds-<pair>` and `remediation-<pair>`. Use
`correlations` only when a section itself spans multiple domains. The
`thresholds` and `remediation-patterns` references are compatibility indexes,
not analysis content. Do not load every reference by default.
