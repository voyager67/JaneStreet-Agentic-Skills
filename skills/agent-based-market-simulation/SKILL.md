---
name: agent-based-market-simulation
description: Design and evaluate agent-based or GPU-accelerated limit-order-book simulations with interacting traders, exchange agents, message latency, and explicit market rules. Use for market-design experiments, impact scenarios, RL execution research, and synthetic order-flow studies; distinguish this from historical replay.
---
# Agent-Based Market Simulation

Use a discrete-event simulation when the question depends on interactions among participants or on a counterfactual market path. Do not present synthetic simulation as a replay of what historically happened.

## Workflow

1. **State the counterfactual question.** Examples: how a new quoting policy changes spread/depth, how latency asymmetry affects fills, or how a large parent order changes market impact. Identify the measurable outcome and falsifiable comparison.
2. **Select the simulation class.** Historical event replay answers what a strategy could have done against a recorded market path under stated assumptions. Agent-based simulation allows the market path to respond to agents. GPU-parallel LOB simulation is useful for broad parameter sweeps but must preserve the market mechanics relevant to the question.
3. **Specify exchange mechanics.** Define price-time/pro-rata priority, tick/lot, matching, cancellations, hidden liquidity, auctions, trading halts, and message processing. Model only mechanics supported by evidence; label simplifications.
4. **Define agent populations.** Separate market makers, liquidity takers, execution agents, noise traders, informed traders, arbitrageurs, and background liquidity. Give each agent an observable information set, decision clock, latency, constraints, and inventory/risk policy.
5. **Calibrate and validate.** Match unconditional and conditional statistics: spread, depth, event arrival rates, order-size distribution, cancellation rate, volatility, autocorrelation, impact, and intraday patterns. Compare distributions, not only means.
6. **Make runs reproducible.** Fix seeds, configs, code revision, agent parameter distributions, and execution environment. Use multiple seeds and confidence intervals; a lucky seed is not a result.
7. **Design controlled interventions.** Change one policy or parameter at a time. Include baseline/no-agent comparisons, ablations, stress regimes, and parameter sensitivity. Prevent train/test contamination when the simulator trains agents.
8. **Check emergent behavior.** Look for unrealistic spread collapse, infinite liquidity, unstable price drift, impossible inventory, non-conservation of shares/cash, or agents exploiting implementation artifacts.
9. **Report external validity.** State which empirical observations the model reproduces, which it does not, and why conclusions may not transfer to a real venue.

## Guardrails

- Do not call synthetic order flow historical ground truth.
- Do not calibrate and validate on the same summaries without an independent period or statistic set.
- Do not hide exchange simplifications or latency assumptions.
- Do not compare simulation throughput with realism; performance and validity are separate dimensions.
- For reinforcement learning, report reward design, exploration, policy selection, and out-of-distribution stress—not reward alone.

## Deliverable

Provide the counterfactual question, simulator choice, exchange rules, agent definitions, calibration/validation table, controlled experiments, seed sensitivity, emergent-behavior checks, and external-validity limits.

## Further reading

- ABIDES-JPMC (agent-based interactive discrete-event simulator; archived): https://github.com/jpmorganchase/abides-jpmc-public
- JAX-LOB, GPU-accelerated LOB simulation: https://arxiv.org/abs/2308.13289
- HftBacktest (historical market replay, a different simulation class): https://github.com/nkaz001/hftbacktest
