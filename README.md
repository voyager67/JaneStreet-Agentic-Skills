# JaneStreet Agentic Skills

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Skill validation](https://github.com/voyager67/JaneStreet-Agentic-Skills/actions/workflows/validate.yml/badge.svg)](https://github.com/voyager67/JaneStreet-Agentic-Skills/actions/workflows/validate.yml)

**A portable, evaluated toolkit for quantitative trading research and trading-systems engineering.**

Fifteen independently authored skills cover the lifecycle from market-data integrity and microstructure research to execution, risk controls, and production operations. The repository also retains Jane Street's public Socratic Tutor as a separately licensed reference skill.

Each skill is a directory containing a `SKILL.md` file. The skills use the common Agent Skills format and do not require a particular model, vendor, API key, market-data provider, or trading platform.

## Skill catalogue

### Market microstructure

- **[lob-microstructure](lob-microstructure/)** — analyze order-flow imbalance, spread/depth, microprice, price impact, and adverse selection.
- **[order-book-reconstruction](order-book-reconstruction/)** — parse exchange messages and rebuild a validated MBO/L2 book with sequencing, invariants, and recovery.
- **[queue-position-modeling](queue-position-modeling/)** — estimate queue-ahead, passive fill probability, and sensitivity to queue assumptions.

### Trading and research

- **[market-making](market-making/)** — develop inventory-aware quoting policies, fill/markout models, spread economics, and hedge logic.
- **[etf-arbitrage](etf-arbitrage/)** — analyze ETF basket value, creation/redemption, premium/discount, cross-asset hedges, and primary/secondary-market frictions.
- **[volatility-market-making](volatility-market-making/)** — research options quoting, volatility surfaces, Greeks, hedging, and scenario risk.
- **[quant-research-validation](quant-research-validation/)** — test signals while controlling look-ahead, leakage, survivorship, multiple testing, and trading costs.
- **[agent-based-market-simulation](agent-based-market-simulation/)** — design discrete-event market simulations with interacting agents and explicit exchange rules.

### Execution and trading systems

- **[hft-market-replay](hft-market-replay/)** — run tick-by-tick backtests with latency, event ordering, queue-aware fills, and explicit impact assumptions.
- **[execution-analysis](execution-analysis/)** — analyze implementation shortfall, slippage, participation, market impact, and execution schedules.
- **[tick-data-engineering](tick-data-engineering/)** — build reliable tick-data pipelines with timestamp semantics, sequence recovery, and reproducible provenance.
- **[exchange-gateway-engineering](exchange-gateway-engineering/)** — design order-entry state machines, protocol handling, acknowledgements, throttles, and reconnect recovery.
- **[low-latency-performance](low-latency-performance/)** — measure and improve tail latency in event loops, feed handlers, and gateways.
- **[pre-trade-risk-controls](pre-trade-risk-controls/)** — specify and test pre-trade limits, stale-data guards, throttles, and kill switches.
- **[production-trading-operations](production-trading-operations/)** — review production readiness, telemetry, reconciliation, incident response, and release controls.

### Retained reference skill

- **[socratic-tutor](socratic-tutor/)** — Jane Street's Socratic tutoring skill, retained unchanged under its original MIT license.

## Quick start

Clone the repository and install the skills for your agent:

```bash
git clone https://github.com/voyager67/JaneStreet-Agentic-Skills.git
cd JaneStreet-Agentic-Skills

# Codex, current project
python3 scripts/install_skills.py --agent codex --scope project

# Or Claude Code, current project
python3 scripts/install_skills.py --agent claude-code --scope project
```

Install only selected skills:

```bash
python3 scripts/install_skills.py --agent codex --scope project --skills market-making,quant-research-validation
```

Preview an installation with `--dry-run`. Existing target directories are never overwritten unless `--force` is explicitly passed. See [COMPATIBILITY.md](COMPATIBILITY.md) for user-level installs, custom destinations, OpenAI metadata, and host limitations.

## Quality and evaluation

The repository includes two distinct quality layers:

**Structural validation** checks skill manifests, directory/name agreement, description limits, OpenAI UI metadata, catalogue coverage, and the retained third-party file fingerprint.

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

**Behavioral evaluation** provides trigger and boundary prompts for every skill, an evaluator-only rubric, and a model-agnostic JSONL scoring tool. It does not call a model API or fabricate test results.

```bash
python3 scripts/evaluate_skills.py validate
python3 scripts/evaluate_skills.py render --skill hft-market-replay
python3 scripts/evaluate_skills.py score path/to/reviewer-results.jsonl
```

For a fair comparison, test the same prompts with and without the skill, keep the model/host/tool settings fixed, and retain raw responses and reviewer scores. Read [EVALUATION.md](EVALUATION.md) before interpreting a score. The starter cases are regression tests, not an industry benchmark or evidence of trading profitability.

## Development

The repository uses Python's standard library; no package installation is required for validation, tests, evaluation-data checks, or skill installation.

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/evaluate_skills.py validate
```

GitHub Actions runs the same checks across the supported Python matrix on pushes and pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md) for authoring requirements and review criteria.

## Scope and limitations

These skills guide research, implementation, testing, and review. They are not exchange connectivity, trading software, market data, investment recommendations, or permission to place orders. A skill does not grant tool access or data entitlements. Live trading, production changes, limit changes, and other consequential actions require explicit user authorization and the relevant organizational controls.

The workflows are platform-agnostic. They tell an agent what to inspect and how to reason, while leaving the choice of Python, C++, Rust, OCaml, FPGA tooling, data vendor, simulator, and venue protocol to the actual project.

## Independence, attribution, and licensing

This project is independent and is not affiliated with, sponsored by, or endorsed by Jane Street Group, LLC. The repository name identifies the retained reference skill and the intended quantitative-trading audience; it does not claim to represent Jane Street or reproduce its proprietary methods, systems, or trading strategies.

The original `socratic-tutor/SKILL.md` from [Jane Street's public agent_skills repository](https://github.com/janestreet/agent_skills) is retained unchanged under its original MIT license and copyright notice. No other Jane Street skill or repository material is included. Repository-authored trading skills, documentation, scripts, and tests are licensed under Apache-2.0. Copyright and third-party attribution details are in [NOTICE](NOTICE); the retained skill has its own [MIT license](socratic-tutor/LICENSE.md).

Public references that informed domain scope and technical checks include:

- **Jane Street** — [public trading overview](https://www.janestreet.com/what-we-do/overview/) and [ETF liquidity offering](https://www.janestreet.com/what-we-do/client-offering/?tab=etfs). Public context only; no proprietary strategies are reproduced.
- **ETF market structure** — [SEC Investor Bulletin](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-24) and [ICI creation/redemption guide](https://www.ici.org/viewpoints/view_12_etfbasics_creation).
- **Historical replay and queue models** — [HftBacktest](https://github.com/nkaz001/hftbacktest), its [order-fill documentation](https://hftbacktest.readthedocs.io/en/latest/order_fill.html), and [latency models](https://hftbacktest.readthedocs.io/en/latest/latency_models.html).
- **Quantitative research validation** — [ML4T Agent Skills](https://github.com/ml4t/skills), [The Probability of Backtest Overfitting](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253), and López de Prado's [Advances in Financial Machine Learning](https://doi.org/10.1002/9781119482086).
- **Agent-based simulation** — [ABIDES-JPMC](https://github.com/jpmorganchase/abides-jpmc-public) and [JAX-LOB](https://arxiv.org/abs/2308.13289). ABIDES-JPMC is archived; check source status and license before reusing its code.
- **Exchange protocols** — [Nasdaq TotalView-ITCH](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf), [Nasdaq OUCH](https://nasdaqtrader.com/Trader.aspx?id=OUCH), and [NYSE Pillar](https://www.nyse.com/trade/pillar).
- **Market-making and microstructure research** — Avellaneda & Stoikov, [High-frequency trading in a limit order book](https://doi.org/10.1080/14697680701381228); Cont, Kukanov & Stoikov, [The Price Impact of Order Book Events](https://doi.org/10.1093/jjfinec/nbt003); and Rigtorp, [Estimating Order Queue Position](https://rigtorp.se/2013/06/08/estimating-order-queue-position/).
- **Low-latency engineering** — Linux kernel [CPU isolation](https://docs.kernel.org/admin-guide/cpu-isolation.html), [network timestamping](https://docs.kernel.org/networking/timestamping.html), and [perf sched](https://github.com/torvalds/linux/blob/master/tools/perf/Documentation/perf-sched.txt) documentation.
- **Agent Skills format** — [format specification](https://agentskills.io/specification) and [OpenAI skill-building guidance](https://learn.chatgpt.com/docs/build-skills).

See [CHANGELOG.md](CHANGELOG.md) for repository changes.
