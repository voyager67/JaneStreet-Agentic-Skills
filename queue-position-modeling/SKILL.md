---
name: queue-position-modeling
description: Estimate passive-order queue position and fill probability from MBO or aggregated L2 data; compare conservative and probabilistic queue models and calibrate them against observed executions. Use for maker-fill simulation, quote placement, and queue-value research.
---
# Queue Position and Passive Fill Modeling

Treat queue position as a latent state unless the feed and venue protocol expose sufficient order-level information. The objective is a calibrated fill distribution, not a single overconfident point estimate.

## Workflow

1. **Establish matching priority.** Confirm FIFO/price-time, pro-rata, size-time, or hybrid rules, plus special priority classes, hidden/reserve liquidity, self-trade prevention, and order modification priority.
2. **Classify available data.** MBO with stable order IDs may support direct queue reconstruction. MBP/L2 reports aggregate size and requires an inference model. State exactly which facts are observable.
3. **Initialize queue ahead.** Align the order's venue acknowledgement time with book events. Estimate displayed quantity ahead at the price when the order becomes live, accounting for exchange-to-feed and order-entry timing. Do not initialize from the local decision timestamp alone.
4. **Process events.** Trades at the price consume queue ahead according to aggressor and matching rules. Additions behind do not move the order backward under FIFO. Cancellations/reductions in L2 are ambiguous: model the fraction ahead versus behind rather than assuming every decrement advances the order.
5. **Compare model families.** At minimum, test:
   - **Risk-averse bound:** cancellations do not improve the simulated queue; only executions advance it.
   - **Probabilistic model:** allocate ambiguous depth reductions ahead/behind using a monotone function of estimated ahead and behind volume. Test several shapes rather than picking one because it produces more fills.
   - **MBO reconstruction:** exact order-level transitions only when the data and venue priority semantics justify it.
6. **Add timing uncertainty.** Simulate feed latency, order-entry latency, acknowledgement latency, and cancel latency. Include the possibility that the market moves before the order is acknowledged or cancelled.
7. **Calibrate on held-out fills.** Compare predicted fill probability, time-to-fill, partial-fill size, and queue-ahead evolution with actual order outcomes. Segment by depth, order size, spread, volatility, and time of day.
8. **Report bounds and uncertainty.** Run conservative/base/aggressive assumptions and show the strategy's P&L and fill rate range. A backtest that only works under optimistic queue assumptions is not robust.

## Diagnostics

- Fill probability calibration curve and Brier/log loss where appropriate.
- Time-to-first-fill and time-to-complete-fill distributions.
- Predicted versus realized partial-fill ratios.
- Fill rates by estimated queue-ahead bucket and order size/depth ratio.
- Sensitivity to unknown cancels, feed batching, and latency distributions.

## Guardrails

- Never treat L2 queue position as ground truth.
- Do not use fills to calibrate and evaluate on the same sample without a temporal holdout.
- A cancel is not automatically a cancellation ahead of your order.
- A full fill is not evidence the model is correct on unfilled orders; account for censoring.
- Do not claim realistic maker backtesting if queue position and latency are absent.

## Deliverable

State the matching rule, observability level, initialization timing, queue model equations/parameters, calibration split, fit diagnostics, scenario bounds, and the degree to which the result is identified by the data.

## Further reading

- Rigtorp, *Estimating Order Queue Position*: https://rigtorp.se/2013/06/08/estimating-order-queue-position/
- HftBacktest queue models: https://hftbacktest.readthedocs.io/en/latest/order_fill.html
- Moallemi & Yuan, *A model for queue position valuation in a limit order book*: https://business.columbia.edu/faculty/research/model-queue-position-valuation-limit-order-book
