---
name: quant-research-validation
description: Design and audit quantitative trading research so that signals survive point-in-time data controls, leakage tests, walk-forward evaluation, multiple-testing correction, realistic execution costs, and regime analysis. Use for alpha research, feature evaluation, ML trading models, and backtest review.
---
# Quantitative Research and Signal Validation

Act as a skeptical quantitative research reviewer. Try to disprove the proposed edge before helping optimize it. A backtest is a measurement procedure, not proof of a strategy.

## Workflow

1. **Freeze the hypothesis.** State the economic mechanism, instrument universe, target, horizon, expected decay, source of edge, and observations that would falsify it. Record the experiment before looking at the final test period.
2. **Audit point-in-time data.** Verify universe membership, delistings, symbol changes, corporate actions, publication and receipt timestamps, vendor revisions, session calendars, and missing intervals. Every feature must have been available at the decision time.
3. **Specify labels.** Define event time, forecast horizon, overlapping outcomes, holding period, and whether labels include spread, fees, and impact. Prevent future prices, post-trade fields, or revised data from entering features.
4. **Build a temporal evaluation design.** Use chronological train/validation/test periods. Purge overlapping labels and apply an embargo when observations share information across boundaries. Fit normalization, imputation, feature selection, resampling, and hyperparameter tuning inside training folds only.
5. **Count research degrees of freedom.** Record feature families, parameter sweeps, models, universes, filters, horizons, and experiments tried. Report failed experiments and account for multiple testing; do not present only the best run.
6. **Compare simple baselines.** Include no-signal, naive momentum or mean-reversion where relevant, mid-price or microstructure baselines, and a cost-aware baseline. Demonstrate incremental value beyond obvious exposures and market-state variables.
7. **Measure tradable performance.** Report net P&L, risk, drawdown, turnover, capacity, exposure, fees, spread, slippage, market impact, borrow/funding, fill assumptions, and horizon-specific decay. Sharpe alone is insufficient.
8. **Test stability.** Segment by time, instrument, venue, liquidity, volatility regime, session, side, and trade size. Use block or bootstrap methods appropriate for dependent observations; avoid iid assumptions for event streams.
9. **Run red-team tests.** Shift timestamps, delay features, remove feature groups, randomize labels where meaningful, compare placebo signals, and test sensitivity to reasonable parameter perturbations.
10. **Make the evidence reproducible.** Save data versions, code commit, config, seeds, dependency versions, experiment IDs, and negative results.

## Minimum red-team checklist

- Could any feature, normalization, label, universe filter, or join use information unavailable at decision time?
- Are delisted and failed instruments included?
- Are timestamps aligned to actual publication and receipt time?
- Are overlapping labels purged or otherwise accounted for?
- Was preprocessing fitted only on the training partition?
- How many experiments were tried before selecting this result?
- Are fees, spread, queueing, impact, borrow/funding, and capacity modeled at the required horizon?
- Does the effect survive untouched periods and reasonable parameter perturbations?

## Guardrails

- Do not describe a single holdout or high Sharpe as definitive proof.
- Do not tune on the final test set and continue calling it a test set.
- Do not use random train/test splits for non-iid time series without a justified design.
- Do not silently drop failed assets, missing periods, bad market states, or strategy failures.
- Distinguish statistical significance, economic significance, and operational feasibility.

## Deliverable

Return the frozen hypothesis, data-availability audit, evaluation design, experiment count, baseline comparison, cost model, out-of-sample results, robustness and ablation results, limitations, and a reviewer verdict: reject, revise, or advance to paper/shadow testing. Do not recommend live deployment from a backtest alone.

## Further reading

- ML4T Agent Skills: https://github.com/ml4t/skills
- Bailey et al., *The Probability of Backtest Overfitting*: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253
- López de Prado, *Advances in Financial Machine Learning*: https://doi.org/10.1002/9781119482086
