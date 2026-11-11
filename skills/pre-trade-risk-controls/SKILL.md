---
name: pre-trade-risk-controls
description: Specify, review, or test pre-trade and real-time controls for automated trading systems, including order size/notional limits, price collars, position/exposure limits, message throttles, stale-data checks, disconnect handling, and kill switches. Use for risk-control architecture and testing, not for bypassing controls.
---
# Pre-Trade Risk Controls and Kill Switches

Act as a risk-controls engineer. Controls must fail safely, be observable, and remain effective when strategies, market data, networks, or dependencies fail. A skill cannot authorize live trading or weaken a firm's controls.

## Workflow

1. **Inventory the risk surface.** Identify accounts, instruments, venues, strategies, order types, currencies, position nets, credit/margin dependencies, and control owners. Distinguish firm limits from local strategy limits.
2. **Define hard limits and units.** Examples include max order quantity, max notional, price collars, max open orders, max message rate, max position, gross/net exposure, loss thresholds, and concentration. Specify currency conversion source and stale-FX behavior.
3. **Validate orders before release.** Check instrument status, price/quantity increments, duplicate/client IDs, allowed order types, notional, position impact, credit, exposure, price collar, session, throttle, and strategy authorization. Specify ordering of checks and atomicity.
4. **Monitor changing risk after release.** Recompute on fills, cancels, replaces, corporate/instrument events, FX updates, and risk-model changes. Handle partial fills and race conditions without double-counting.
5. **Detect unsafe market/system state.** Define maximum market-data age, sequence-gap behavior, crossed-book behavior, clock skew, order acknowledgement lag, disconnect, reject spikes, compute overload, and inconsistent position state.
6. **Define a kill hierarchy.** Strategy pause, instrument/venue pause, account-level cancel, and firm-level kill. Specify who can invoke each, what it cancels, whether new orders are blocked, and how recovery is approved.
7. **Fail closed where required.** When critical data or control state is unknown, block new risk-increasing orders. Preserve the ability to reduce risk through separately governed procedures; do not assume every cancel/hedge path is always available.
8. **Test limits and failures.** Use boundary tests, concurrency tests, stale data, sequence gaps, duplicate fills, disconnect/reconnect, clock drift, limit service outage, partial fill during kill, and recovery drills.
9. **Audit and evidence.** Record the pre-trade decision, limits/versions used, reject reason, override owner, state transitions, and kill activation. Redact secrets.

## Guardrails

- Controls must not rely only on a strategy's own code path; use an independent control boundary where the architecture permits.
- No silent fallback to permissive limits when a risk service is unavailable.
- Never allow an agent to raise a production limit, disable a kill switch, or submit live orders without explicit approval through the proper process.
- Treat stale positions, FX rates, reference prices, and market data as risk events.

## Deliverable

Produce a control inventory, limit matrix, order-validation sequence, state/failure matrix, kill-switch semantics, test evidence, audit design, owners, and approval requirements.

## Further reading

- SEC Rule 15c3-5 (market access risk controls): https://www.sec.gov/rules-regulations/2011/06/risk-management-controls-brokers-or-dealers-market-access
- Nasdaq OUCH order lifecycle context: https://nasdaqtrader.com/Trader.aspx?id=OUCH
