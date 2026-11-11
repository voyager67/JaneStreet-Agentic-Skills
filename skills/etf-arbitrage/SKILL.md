---
name: etf-arbitrage
description: Analyze ETF primary/secondary-market pricing, basket valuation, creation/redemption economics, premium/discount dynamics, and cross-asset hedging. Use for ETF market making, authorized-participant workflows, basket arbitrage, and ETF liquidity research; not for treating end-of-day NAV as an executable intraday fair value.
---
# ETF Primary/Secondary-Market Arbitrage

Act as an ETF market-structure and quantitative trading researcher. An ETF is a traded claim on a portfolio with a primary-market create/redeem mechanism. Do not reduce the problem to comparing the ETF last price with stale published NAV.

## Workflow

1. **Identify the fund and market structure.** Record domicile, listing venue, currency, trading hours, share class, creation-unit size, settlement cycle, authorized-participant access, in-kind/cash/mixed creation, redemption rules, and the authoritative creation/redemption basket source.
2. **Reconstruct the intraday basket value.** Price each basket component with synchronized, tradeable reference prices. Apply FX conversion, accrued income, cash components, corporate actions, derivative exposure, fund liabilities/fees where relevant, and basket-specific cash adjustments. Keep official NAV, indicative value, and your own real-time basket estimate separate.
3. **Check basket tradability.** For each constituent, measure quote age, spread, depth, market state, trading calendar, borrow availability, price limits, and local-market closure. A quoted basket value is not executable if significant components are stale, halted, closed, or expensive to hedge.
4. **Calculate the deviation consistently.** Define premium/discount against the contemporaneous basket estimate using a clear numerator, denominator, currency, and timestamp. Compare ETF bid/ask—not only last trade—to executable basket-side prices. Account for creation/redemption unit sizing and residual inventory.
5. **Build both sides of the economics.** For ETF rich to basket: assess ETF sale/shorting, basket purchase, borrow/locate, financing, creation costs, and delivery/settlement. For ETF cheap to basket: assess ETF purchase, basket shorting/borrow, redemption terms, financing, and settlement. Treat these as possible structures, not guaranteed arbitrage trades.
6. **Include frictions and constraints.** Model commissions, exchange fees, stamp/transaction taxes, bid/ask, market impact, borrow/recall, financing, FX, creation/redemption fees, taxes, settlement mismatch, minimum size, and capital usage. Include uncertainty in every leg.
7. **Handle asynchronous global markets.** For international, fixed-income, commodity, or crypto-underlying ETFs, identify which underlying markets are closed or thin. Estimate fair-value uncertainty from proxy instruments and avoid calling stale underlying prices a reliable NAV anchor.
8. **Evaluate inventory and unwind risk.** Track ETF shares, basket constituents, cash, FX, borrow, futures/derivatives hedges, and unsettled creations/redemptions. Stress component gaps, FX jumps, halted constituents, failed creations, settlement fails, and borrow recalls.
9. **Test the mechanism empirically.** Study premium/discount persistence, spread/depth, basket liquidity, AP activity if observable, market hours, volatility, and stress periods. Use event-time alignment and avoid using the final NAV as if it were known intraday.
10. **Report actionable thresholds as estimates.** Calculate a break-even band and uncertainty interval after all expected costs. State which inputs are tradeable, indicative, stale, model-based, or unavailable.

## Guardrails

- Do not use end-of-day NAV as an intraday executable price.
- Do not assume every market participant can create or redeem directly; AP eligibility and fund terms matter.
- Do not assume the published portfolio composition file equals the exact executable creation basket in every fund and circumstance.
- Do not infer that a premium/discount is risk-free profit; it may compensate for stale underlying marks, liquidity, borrow, financing, taxes, settlement, or inventory risk.
- Do not ignore closed local markets, FX hours, holidays, underlying-market halts, or settlement mismatch.
- Do not initiate live ETF, basket, FX, borrow, or derivatives transactions without explicit authorization and the required controls.

## Deliverable

Return the fund/venue facts, basket-source and timestamp audit, component tradability table, premium/discount definition, executable two-sided cost model, creation/redemption constraints, residual inventory risks, stress analysis, break-even band, and unresolved data gaps.

## Further reading

- Jane Street public ETF and cross-asset liquidity offering: https://www.janestreet.com/what-we-do/client-offering/?tab=etfs
- SEC Investor Bulletin on ETF primary/secondary markets and creation/redemption: https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-24
- Investment Company Institute, ETF creation/redemption process: https://www.ici.org/viewpoints/view_12_etfbasics_creation
- State Street, how ETFs are created and redeemed: https://www.ssga.com/us/en/intermediary/resources/education/how-etfs-are-created-and-redeemed
