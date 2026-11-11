---
name: production-trading-operations
description: "Review production readiness and operational resilience of automated trading systems: market-data health, order-flow monitoring, reconciliation, alerting, release gates, canaries, incident response, and rollback. Use before paper/live deployment or when diagnosing trading-system incidents."
---
# Production Trading Operations

Treat production readiness as a system property spanning data, strategy, execution, risk, infrastructure, and people. A profitable backtest is not a readiness review.

## Workflow

1. **Map the end-to-end system.** Identify market-data capture, normalization, strategy, risk gateway, order gateway, venue sessions, position/P&L reconciliation, monitoring, and ownership. Document critical dependencies and failure domains.
2. **Define service indicators.** Monitor feed age, sequence gaps, packet drops, book validity, strategy decision lag, order-send/ack latency, reject/cancel rates, open-order count, position mismatches, risk-limit utilization, P&L, and CPU/memory/network saturation.
3. **Set actionable alerts.** Each alert needs threshold rationale, severity, owner, runbook, safe action, and deduplication. Use percentiles and rates, not a single average. Distinguish warning from automatic risk-reducing action.
4. **Reconcile continuously.** Compare internal orders/positions/cash with venue/broker reports. Define how to handle unknown orders, missing fills, duplicate execution reports, breaks, and end-of-day reconciliation.
5. **Stage releases.** Require reviewed code, reproducible build, data/protocol compatibility, risk-limit sign-off, replay regression, load/soak testing, security review, monitoring coverage, and tested rollback. Use paper/shadow/canary stages with explicit exposure caps.
6. **Design safe startup and shutdown.** Define order reconciliation before enabling strategies, session establishment, data freshness checks, risk-service health, staged enablement, cancel-on-shutdown policy, and position/working-order handoff.
7. **Prepare incident playbooks.** Cover stale/corrupt feed, sequence gap, wrong instrument mapping, order rejects, acknowledgement stall, position mismatch, latency spike, risk service loss, exchange halt, and runaway strategy. Include roles, decision authority, communication, evidence preservation, and recovery criteria.
8. **Run drills.** Simulate a feed gap, disconnect, delayed ack, kill switch, and rollback. Verify alert delivery and ensure the operator can identify actual venue order state.
9. **Close the loop.** Every incident gets a timeline, impact assessment, root cause, contributing factors, control gaps, action owners, due dates, and verification.

## Guardrails

- Do not auto-resume risk-increasing trading solely because a process restarted.
- Do not assume local order state is authoritative after a disconnect; reconcile with the venue.
- Do not page on noisy metrics without an action; do not leave critical faults unpaged.
- Preserve raw event and audit data for investigation while protecting secrets and personal information.
- Agents may draft runbooks and inspect telemetry, but must not independently activate live trading, relax limits, or suppress critical alarms.

## Deliverable

Return a readiness matrix, service indicators/thresholds, dependency map, release gates, rollback plan, reconcilation design, incident runbooks, drill evidence, and named human owners.

## Further reading

- Jane Street, technology and trading overview: https://www.janestreet.com/what-we-do/overview/
- Linux CPU isolation guidance: https://docs.kernel.org/admin-guide/cpu-isolation.html
- Linux network timestamping: https://docs.kernel.org/networking/timestamping.html
