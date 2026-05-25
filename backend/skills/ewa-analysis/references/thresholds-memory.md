# SAP Memory and Buffer Thresholds

Use this reference for EWA sections about SAP memory, extended memory, heap,
roll, page area, user context swapping, and SAP buffers.

| Metric | Healthy | Warning | Critical | Transactions | Parameter |
| --- | --- | --- | --- | --- | --- |
| Extended memory utilization | < 80% | 80-95% | > 95% | ST02 | em/initial_size_MB |
| Extended memory free | > 20% | 5-20% | < 5% | ST02 | em/initial_size_MB |
| EM attached per user | Below limit | Close to limit | At limit | AL05, SM04 | em/max_size_MB |
| Heap memory usage | Minimal | Moderate | Heavy or PRIV mode | ST02, SM50 | abap/heap_area_* |
| Roll area utilization | < 70% | 70-90% | > 90% | ST02 | ztta/roll_area |
| Buffer quality | > 98% | 95-98% | < 95% | ST02 | buffer-specific |
| Program buffer hit ratio | > 98% | 95-98% | < 95% | ST02 | abap/buffersize |
| Table buffer hit ratio | > 98% | 95-98% | < 95% | ST02 | zcsa/table_buffer_area |
| Buffer swaps | 0 | Occasional | Frequent/increasing | ST02 | buffer-specific |

Severity guidance:

- Extended memory above 95% plus heap or PRIV mode is usually High and can be
  Critical if users are failing or work processes are exhausted.
- Buffer quality around 96% is usually Medium unless there is matching response
  time evidence.
- Missing memory data is Medium because capacity risk cannot be validated.
