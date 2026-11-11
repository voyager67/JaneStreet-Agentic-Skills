# JaneStreet Agentic Skills

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

A small collection of practical skills for quantitative trading, electronic market making, and the engineering systems around them.

Each skill is a directory containing a `SKILL.md` file. The skills are designed for agents that support the common Agent Skills format; they do not require a particular model, vendor, API key, or trading platform.

## Skills

### Market microstructure

- **[lob-microstructure](lob-microstructure/)** — analyze order-flow imbalance, spread/depth, microprice, price impact, and adverse selection.
- **[order-book-reconstruction](order-book-reconstruction/)** — parse exchange messages and rebuild a validated MBO/L2 book with sequencing and recovery.
- **[queue-position-modeling](queue-position-modeling/)** — estimate queue-ahead, passive fill probability, and the sensitivity of results to queue assumptions.

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

- **[socratic-tutor](socratic-tutor/)** — Jane Street's Socratic tutoring skill, retained unchanged as the sole third-party skill in this collection.

## How to use

With an agent that supports the common `SKILL.md` format, copy the selected skill directory into the skills directory recognized by that agent. Keep the directory name and `SKILL.md` together. Then ask the agent to use the skill for a task in its description.

With a chatbot that accepts prompts but does not load skill directories, paste the Markdown body of the selected `SKILL.md` (everything below the YAML frontmatter) into the conversation or a custom instruction field.

The format describes the skill; it does not prescribe where an agent stores or discovers skills. Installation paths and explicit invocation syntax depend on the agent. Use one narrow skill at a time unless a task genuinely spans multiple workflows.

## Scope and limitations

These skills guide research, implementation, testing, and review. They are not exchange connectivity, trading software, market data, investment recommendations, or permission to place orders. A skill does not grant tool access. Live trading, production changes, limit changes, and other consequential actions require the user's explicit authorization and the relevant organizational controls.

The workflows are deliberately platform-agnostic. They tell an agent what to inspect and how to reason, while leaving the choice of Python, C++, Rust, OCaml, FPGA tooling, data vendor, simulator, and venue protocol to the actual project.

## Development

The repository keeps one skill per directory and uses only the required Agent Skills frontmatter fields (`name` and `description`). Skills are intended to be loaded progressively: short discovery metadata first, detailed workflow only when invoked. Run the checks with:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
```

Contributions should add a specific trading or systems workflow, identify its trigger conditions, state required inputs, provide a repeatable process, and include domain-specific failure modes and further reading. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Acknowledgements and references

This project is independent and is not affiliated with, sponsored by, or endorsed by Jane Street Group, LLC. The repository name describes the retained reference skill and intended quantitative-trading audience; it does not claim to represent Jane Street or reproduce its proprietary methods, systems, or trading strategies.

The following public work informed the scope and technical checks in the original skills. We credit these projects and sources for the ideas and reference material; the new skill instructions in this repository are independently written and do not copy their skill files or implementation code.

- **Jane Street — [public trading overview](https://www.janestreet.com/what-we-do/overview/) and [ETF liquidity offering](https://www.janestreet.com/what-we-do/client-offering/?tab=etfs)**: public context for the collection’s quantitative market-making and ETF focus; this project does not reproduce proprietary strategies.
- **Jane Street — [agent_skills](https://github.com/janestreet/agent_skills)**: the original `socratic-tutor/SKILL.md` is included unchanged under its original MIT license and copyright notice. No other Jane Street skill or repository material is included.
- **[SEC Investor Bulletin on ETFs](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-24)** and **[ICI ETF creation/redemption guide](https://www.ici.org/viewpoints/view_12_etfbasics_creation)**: primary/secondary market mechanics, authorized participants, and basket arbitrage.
- **[HftBacktest](https://github.com/nkaz001/hftbacktest)** and its [queue models](https://hftbacktest.readthedocs.io/en/latest/order_fill.html) and [latency models](https://hft.readthedocs.io/en/latest/latency_models.html): historical tick replay, order/feed latency, and queue-aware passive fill simulation.
- **[ML4T Agent Skills](https://github.com/ml4t/skills)**: research discipline around point-in-time data, leakage, transaction costs, time-series validation, and backtest overfitting. The repository is Apache-2.0; no ML4T skill text or code is copied here.
- **[ABIDES-JPMC](https://github.com/jpmorganchase/abides-jpmc-public)** and **[JAX-LOB](https://arxiv.org/abs/2308.13289)**: interacting-agent market simulation and GPU-accelerated limit-order-book simulation. ABIDES-JPMC is archived; check source status and license before reusing its code.
- **[Nasdaq TotalView-ITCH](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf)**, **[Nasdaq OUCH](https://nasdaqtrader.com/Trader.aspx?id=OUCH)**, and **[NYSE Pillar](https://www.nyse.com/trade/pillar)**: venue protocol semantics, market-data reconstruction, order entry, and exchange-specific state handling.
- **Avellaneda & Stoikov, *High-frequency trading in a limit order book* (2008)**: a theoretical inventory-aware quoting framework; use its assumptions as a model to test, not as a universal production recipe. [DOI](https://doi.org/10.1080/14697680701381228).
- **Cont, Kukanov & Stoikov, *The Price Impact of Order Book Events* (2014)**: empirical order-flow imbalance and short-horizon price impact. [DOI](https://doi.org/10.1093/jjfinec/nbt003).
- **Rigtorp, *Estimating Order Queue Position***: queue-ahead inference for aggregated depth feeds. [Article](https://rigtorp.se/2013/06/08/estimating-order-queue-position/).
- **Linux kernel documentation**: [CPU isolation](https://docs.kernel.org/admin-guide/cpu-isolation.html), [network timestamping](https://docs.kernel.org/networking/timestamping.html), and [`perf sched`](https://github.com/torvalds/linux/blob/master/tools/perf/Documentation/perf-sched.txt) for measurement and performance diagnosis.
- **Agent Skills specification**: [format and validation](https://agentskills.io/specification). Skills use the common directory-plus-`SKILL.md` structure.

## License

The original quantitative-trading skills and repository-authored material are licensed under the Apache License, Version 2.0 ([LICENSE](LICENSE)). Copyright and attribution details are recorded in [NOTICE](NOTICE). The retained `socratic-tutor` directory remains under Jane Street's original MIT license and includes its own `LICENSE.md`; it is not relicensed under Apache-2.0. External works listed above remain governed by their respective licenses and terms. Links and acknowledgements do not grant rights to third-party code, data, trademarks, or exchange specifications.