# Performance and Hardware Thresholds

Use this reference for EWA sections about workload, dialog response, CPU,
physical memory, swap, storage latency, and general sizing.

| Metric | Healthy | Warning | Critical | Transactions | Notes |
| --- | --- | --- | --- | --- | --- |
| Dialog response time | < 1.0s | 1.0-2.0s | > 2.0s | ST03N | Users notice sustained response above 2 seconds |
| Database request time per dialog step | < 200ms | 200-400ms | > 400ms | ST03N, ST04 | High DB time often drives end-user latency |
| Roll wait time | < 200ms | 200-500ms | > 500ms | ST03N | Can indicate RFC, enqueue, or roll contention |
| Average CPU utilization | < 60% | 60-80% | > 80% | ST06, OS07 | Average hides spikes; also inspect peak |
| Peak CPU utilization | < 70% | 70-85% | > 85% | ST06 | Above 85% causes scheduling delays |
| Physical memory utilization | < 80% | 80-92% | > 92% | ST06 | Leave OS cache and DB headroom |
| Swap space utilization | < 5% | 5-20% | > 20% | ST06 | Active swap causes nonlinear performance loss |
| Swap in/out rate | < 100 pages/s | 100-1000 pages/s | > 1000 pages/s | ST06 | Sustained swap means real memory pressure |
| Disk read latency | < 5ms | 5-15ms | > 15ms | ST06 | Enterprise storage should remain low latency |
| Disk write latency | < 5ms | 5-15ms | > 15ms | ST06 | Write latency affects DB commits |

Severity guidance:

- Critical when response time or hardware pressure is causing broad current user
  impact, not merely because a single threshold is red.
- High when sustained utilization leaves little headroom and response metrics
  are degraded.
- Medium for trends that need capacity planning but are not hurting users yet.
