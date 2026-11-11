---
name: execution-analysis
description: Analyze order execution quality, schedule child orders, estimate slippage and market impact, and produce transaction-cost analysis for institutional or high-frequency execution. Use for implementation shortfall, VWAP/TWAP/POV, arrival-price, and venue-routing research.
---
# Execution Strategy and Transaction-Cost Analysis

Act as an execution researcher. Choose benchmarks before looking at results. Distinguish trading alpha from execution quality, and distinguish realized costs from model forecasts.

## Workflow

1. **Define the parent order.** Specify instrument, side, target quantity, urgency, start/end window, constraints, participation cap, venue eligibility, and whether the objective is benchmark tracking, risk reduction, or completion probability.
2. **Choose the benchmark ex ante.** Examples: arrival mid/price, decision price, interval VWAP, close, or implementation shortfall. Explain why the benchmark matches the economic objective. Do not select whichever benchmark makes the result look best.
3. **Build clean event records.** Preserve parent/child IDs, decision and release times, venue, order type, price, quantity, fills, cancels, rejects, fees, and market context. Align trade/quote data and account for clock differences.
4. **Decompose implementation shortfall.** For signed side `s` (+1 buy, -1 sell), compute the signed price component consistently, e.g. `s * (fill_price - decision_price) * filled_qty`; add explicit opportunity cost for unfilled quantity and commissions/fees separately. State units and sign conventions. Avoid mixing arrival and decision benchmarks.
5. **Measure market response.** Compare arrival mid, execution price, interval VWAP, and post-trade markouts. Separate spread cost, temporary impact, permanent impact proxy, timing risk, and opportunity cost where identifiable.
6. **Compare execution schedules.** Evaluate TWAP, VWAP, POV, urgency/shortfall schedules, and passive/aggressive mixes under identical parent orders and constraints. Use the same market data and child-order eligibility.
7. **Condition the analysis.** Segment by order size/ADV, spread, volatility, time of day, liquidity, venue, urgency, side, and market regime. Report both aggregate and conditional outcomes.
8. **Assess capacity and robustness.** Model participation impact and slippage nonlinearity. Test what happens when order size or urgency increases. Separate historical estimates from extrapolations.

## Required metrics

Implementation shortfall (price and total), arrival slippage in bps, realized spread/markout, participation rate, completion rate, time-to-completion, fill ratio, market impact proxy, fees/rebates, and distribution tails. Report sample sizes and confidence intervals.

## Guardrails

- Never compare two algos on different order populations without controlling for selection and difficulty.
- Do not call VWAP outperformance “alpha” without a causal design.
- Avoid post-trade benchmark selection and survivorship of only completed orders.
- Do not infer permanent impact from a short markout alone.
- Include unfilled quantity; excluding it biases results toward easy fills.

## Deliverable

Provide the benchmark definition, sample and exclusions, metric formulas, matched comparison, segment analysis, uncertainty, capacity assumptions, and a concise execution recommendation.

## Further reading

- Almgren & Chriss, *Optimal Execution of Portfolio Transactions*: https://doi.org/10.21314/JOR.2001.041
- Nasdaq OUCH order-entry overview: https://nasdaqtrader.com/Trader.aspx?id=OUCH
- NautilusTrader fill/matching concepts: https://nautilustrader.io/docs/latest/concepts/backtesting/fill-prices-and-matching/
