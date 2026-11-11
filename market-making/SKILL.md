---
name: market-making
description: Design, analyze, or improve two-sided quoting and liquidity-provision strategies, including reservation prices, inventory skew, spread selection, adverse-selection filters, hedging, and quote lifecycle. Use for electronic market making and dealer-style quoting, not generic directional trading.
---
# Market-Making Research and Quoting

Work as a market-making researcher. Treat quoting as a joint problem in expected spread capture, fill probability, adverse selection, inventory risk, hedge cost, and operational constraints. A theoretical quote is a starting hypothesis, not a production policy.

## Workflow

1. **Specify the venue and product.** Record tick/lot size, price-time or pro-rata priority, maker/taker fees and rebates, auction behavior, trading hours, position limits, hedge instrument, and whether the strategy is passive, aggressive, or mixed.
2. **Build the economics per fill.** Decompose expected P&L into spread capture, fees/rebates, post-fill markout, hedge slippage, funding/borrow/carry, and inventory valuation. Keep realized P&L and forecast components separate.
3. **Establish a fair-value estimate.** State the reference price and inputs. Compare mid, microprice, cross-venue fair value, and model value where relevant. Quantify stale-input and basis risk.
4. **Model inventory explicitly.** Define signed inventory, target inventory, hard limits, risk horizon, volatility estimate, and penalty for carrying risk. A classical Avellaneda–Stoikov reservation-price approximation is `r = S - q * gamma * sigma^2 * tau`, with long inventory `q > 0`; it expresses a price skew, not a universal quote formula. The model's assumptions (diffusion price, arrival-intensity form, utility, horizon) must be tested before applying it.
5. **Set quote distances.** Explain what determines each side's distance from fair value: spread target, volatility, fill intensity, inventory, queue priority, adverse-selection forecast, and fees. Do not quote from a single closed-form equation without examining its assumptions.
6. **Estimate fill and toxicity jointly.** Segment fill probability and post-fill markout by quote distance, queue position, market state, side, and time horizon. A higher fill rate can be bad if it concentrates in informed flow.
7. **Define quote lifecycle.** Specify new/replace/cancel decisions, minimum resting time if any, rate limits, stale-data behavior, cancel-on-disconnect, and what happens when acknowledgements lag.
8. **Evaluate inventory and hedging.** Report inventory distribution, time at risk limits, tail exposure, hedge frequency, hedge cost, and P&L by inventory bucket. Include correlated instruments and basis risk where applicable.
9. **Run controlled experiments.** Compare against a simple baseline, isolate one policy change at a time, and test across volatility/liquidity regimes and out-of-sample periods.

## Required diagnostics

- Bid and ask fill rates, fill-to-cancel ratio, queue-adjusted fill rate.
- Effective spread, realized spread, signed markouts at multiple horizons.
- Gross spread capture versus net economics after fees, rebates, hedge costs, and inventory P&L.
- Inventory mean, dispersion, tails, limit breaches, and time-to-flat.
- Quote age, cancel/replace rate, reject rate, acknowledgement delay, and stale-quote exposure.

## Guardrails

- Do not equate maker rebates with positive expected value.
- Avoid adverse-selection labels that leak post-fill prices into pre-trade features.
- Do not infer queue position from L2 data as though exact FIFO rank were observed.
- Calibrate volatility and fill intensity on the same relevant instrument/session regime; disclose extrapolation.
- Never send live orders or change production limits as part of research without explicit authorization and the firm's approval process.

## Deliverable

Produce a quote-policy specification, assumptions table, unit-economics decomposition, fill/markout study, inventory analysis, regime robustness, operational failure behavior, and a clear go/no-go recommendation with evidence gaps.

## Further reading

- Avellaneda & Stoikov, *High-frequency trading in a limit order book* (2008): https://doi.org/10.1080/14697680701381228
- Jane Street, trading overview (context on liquidity provision and quantitative research): https://www.janestreet.com/what-we-do/overview/
- Garriott, van Kervel & Zoican, *Queuing and inventories in limit order markets* (2025): https://doi.org/10.1016/j.finmar.2025.100982
