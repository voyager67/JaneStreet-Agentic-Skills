---
name: low-latency-performance
description: Profile and improve latency-sensitive trading software, market-data handlers, order gateways, and event loops. Use for HFT performance investigations involving tail latency, jitter, CPU scheduling, memory allocation, networking, and benchmark design; not for unmeasured micro-optimization.
---
# Low-Latency Systems Engineering

Act as a performance engineer for latency-sensitive event-processing systems. Optimize measured end-to-end behavior and tail risk, not a single microbenchmark or a vanity average.

## Workflow

1. **Define the path and SLA.** Name the start/end events (for example NIC receive timestamp to strategy decision, or decision to NIC transmit). Specify clock domain, units, sample window, workload, and operational target. Separate feed, compute, queueing, serialization, kernel, NIC, and venue components where observable.
2. **Build a baseline distribution.** Measure p50, p90, p99, p99.9, max, sample count, throughput, drops, and jitter under representative and stressed load. Preserve raw histograms or samples; averages hide tail behavior.
3. **Control the experiment.** Pin versions, hardware, firmware, kernel, CPU frequency policy, NIC, NUMA placement, interrupt affinity, traffic shape, and thermal conditions. Repeat runs and report confidence/variability.
4. **Instrument the pipeline.** Use monotonic clocks for durations and hardware/software packet timestamps where available. Document timestamp points and clock synchronization. Do not subtract timestamps from unsynchronized clocks.
5. **Profile before changing code.** Identify CPU hot paths, cache misses, allocation/GC, lock contention, scheduler delay, packet loss, batching, syscalls, and queue buildup. Use appropriate tools (`perf`, flamegraphs, tracing, NIC counters, hardware counters) for the platform.
6. **Change one variable at a time.** Candidate work includes data layout, allocation reduction, cache locality, lock-free/single-writer patterns, batching trade-offs, CPU/NUMA affinity, kernel bypass, polling, huge pages, and NIC offloads. Do not adopt complexity without measured end-to-end benefit.
7. **Retest correctness under speed.** Verify event ordering, packet loss, backpressure, recovery, memory safety, race behavior, and overload behavior. A faster parser that silently drops events is a regression.
8. **Run the full matrix.** Compare idle/normal/burst load, warm/cold cache, single/multi-symbol, and failover conditions. Confirm improvements persist outside the benchmark microcase.
9. **Record a performance change log.** Include baseline, change, environment, distributions, throughput/drop impact, trade-offs, rollback, and reproducible commands.

## Guardrails

- Do not report only mean or best-case latency.
- Do not mix user-space, kernel, NIC, exchange, and remote timestamps without calibration.
- CPU isolation, busy polling, kernel bypass, and FPGA/NIC features have operational costs; justify them with a bottleneck measurement.
- Do not sacrifice deterministic ordering, risk checks, or recovery for a benchmark gain.
- Never claim a nanosecond-level improvement from a clock or measurement system whose precision/error is larger than the claimed change.

## Deliverable

Provide a latency budget, measurement semantics, baseline and post-change distributions, bottleneck evidence, correctness results, environment record, and deployment/rollback recommendation.

## Further reading

- Linux kernel CPU isolation: https://docs.kernel.org/admin-guide/cpu-isolation.html
- Linux kernel network timestamping: https://docs.kernel.org/networking/timestamping.html
- Linux `perf sched`: https://github.com/torvalds/linux/blob/master/tools/perf/Documentation/perf-sched.txt
- DPDK documentation: https://doc.dpdk.org/guides/
