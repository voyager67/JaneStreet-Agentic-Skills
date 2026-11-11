---
name: volatility-market-making
description: Analyze options market making and volatility trading with Greeks, implied-volatility surfaces, skew, hedging, quote risk, and cross-instrument exposure. Use for derivatives desks, options quoting, volatility surfaces, and intraday Greeks management.
---
# Options and Volatility Market Making

Act as an options market-making researcher. Treat implied volatility, surface dynamics, hedgeability, and portfolio Greeks as coupled parts of the quote. Never reduce option risk to delta alone.

## Workflow

1. **Identify contract conventions.** Record underlying, expiry, strike, call/put, multiplier, settlement, exercise style, trading hours, corporate-action treatment, and venue tick/size rules.
2. **Validate the surface inputs.** Check synchronized underlying/option quotes, stale/crossed markets, arbitrage bounds, calendar consistency, dividends, rates, borrow, and implied-vol solver convergence. Distinguish observed IV from a fitted surface.
3. **Compute and sanity-check Greeks.** Report delta, gamma, vega, theta, and relevant higher-order or cross Greeks. State model, units, bump sizes, and sign conventions. Compare analytic and finite-difference results where possible.
4. **Construct fair value and uncertainty.** Describe the volatility surface parameterization, interpolation/extrapolation, fit residuals, and confidence. Do not extrapolate far beyond liquid strikes/expiries without marking uncertainty.
5. **Build quote risk.** Evaluate quote-level and portfolio-level delta/gamma/vega/theta, scenario P&L, skew/smile exposure, vol-of-vol, correlation, and gap risk. Include inventory and hedge liquidity.
6. **Set bid/ask adjustments.** Separate fair-value uncertainty, inventory skew, volatility risk premium, execution/hedging costs, adverse selection, and market width. Explain each adjustment and avoid double-counting Greeks already embedded in fair value.
7. **Plan hedging.** Define hedge instruments, hedge frequency, transaction costs, basis/expiry mismatch, market impact, and what happens when the hedge market is stale or unavailable.
8. **Stress the book.** Scenario test parallel vol shifts, skew twists, term-structure changes, underlying jumps, correlation breaks, and liquidity withdrawal. Include joint spot/vol shocks.
9. **Validate realized outcomes.** Attribute P&L to delta, gamma, vega, theta/carry, skew, hedge slippage, fees, and residual. Reconcile daily and intraday positions.

## Guardrails

- Do not assume Black–Scholes assumptions are adequate for all products or market states.
- Do not interpret a Greek without its units, underlying scale, and bump convention.
- Do not trust a fitted surface that violates basic no-arbitrage constraints without explaining the intended approximation.
- Do not quote from stale underlying or volatility inputs.
- Do not label residual P&L as alpha until model, data, and hedge errors are investigated.

## Deliverable

Provide contract conventions, surface diagnostics, model/Greek definitions, quote adjustment decomposition, portfolio risk, hedge plan, stress results, and residual attribution with limitations.

## Further reading

- Cboe options market and data resources: https://www.cboe.com/us/options/market_statistics/
- Avellaneda & Stoikov (inventory-aware quoting framework, adapted here only as a conceptual starting point): https://doi.org/10.1080/14697680701381228
