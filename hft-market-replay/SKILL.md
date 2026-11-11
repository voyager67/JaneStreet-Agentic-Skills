---
name: hft-market-replay
description: Build or audit tick-by-tick historical market replay and HFT backtests with explicit feed/order latency, exchange event ordering, queue-aware fills, fees, and market-impact assumptions. Use for high-frequency or passive-order strategy evaluation; not for daily-bar backtests.
---
# HFT Historical Replay and Backtesting

Treat a replay as a model of what the strategy could have observed and what the venue could have executed. Historical book data is not an execution oracle: simulated orders do not automatically alter the historical market.

## Workflow

1. **Define replay fidelity.** Record feed granularity (trades, L1, L2, MBO), venue/session coverage, timestamp semantics, packet sequence availability, and whether the replay is deterministic.
2. **Separate clocks.** Preserve exchange event time, packet receive time, strategy decision time, order-send time, exchange-arrival/ack time, fill time, and local response time wherever available. Document synchronization error and timestamp precision.
3. **Model latency paths.** Represent feed latency, strategy compute delay, outbound order-entry latency, exchange processing/ack delay, and cancel latency separately. Use empirical distributions or conservative envelopes, not a single constant unless justified.
4. **Specify event ordering.** Define what happens when a feed event, strategy timer, order arrival, acknowledgement, trade, and cancel cross. Test same-timestamp ties and out-of-order observations.
5. **Choose fill models.** Use MBO reconstruction where valid. For L2, disclose queue uncertainty and compare conservative/probabilistic models. State whether fills consume displayed liquidity, whether multiple simulated orders can consume the same historical liquidity, and how partial fills work.
6. **Model fees and economics.** Include maker/taker fees, rebates, funding/borrow/carry, tick/lot rounding, hedge costs, and contract multiplier. Report gross and net separately.
7. **Handle market impact honestly.** Historical replay generally assumes the strategy is small enough not to change the historical path unless an impact/agent model is added. State this assumption and test capacity limits separately.
8. **Avoid future information.** Strategy decisions at time `t` may only use messages received by `t`; a feed event's exchange timestamp does not mean the strategy had already received it. Use actual availability times in feature construction.
9. **Run scenarios.** Baseline, conservative latency, stressed latency, conservative queue, alternate fill model, higher fees, and reduced liquidity. Keep parameter selection outside the final evaluation window.
10. **Produce an audit trail.** Save config, data identifiers/hashes, code revision, random seeds, and per-order decision/fill/cancel traces.

## Deliverable

- Net P&L decomposition and returns, not only Sharpe.
- Fill ratio, maker/taker mix, partial fills, rejected/cancelled orders.
- Queue and latency assumptions, with sensitivity.
- Turnover, fees/rebates, slippage, impact assumption, and capacity caveats.
- Inventory/exposure distribution and maximum drawdown/tail loss.
- Reproducibility metadata and known simulator limitations.

## Guardrails

- Do not describe bar-based fill assumptions as HFT-grade execution simulation.
- Do not count a fill before exchange arrival or use unreceived market data.
- Do not let the same historical displayed quantity fill multiple simulated orders unless the model explicitly controls consumption.
- Backtest success is not evidence of live profitability; do not connect the research run to live trading.

## Further reading

- HftBacktest: https://github.com/nkaz001/hftbacktest
- HftBacktest latency models: https://hft.readthedocs.io/en/latest/latency_models.html
- NautilusTrader backtesting concepts: https://nautilustrader.io/docs/latest/concepts/backtesting/
- ABIDES-JPMC: https://github.com/jpmorganchase/abides-jpmc-public
