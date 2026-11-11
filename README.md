# JaneStreet Agentic Skills

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Skill validation](https://github.com/voyager67/JaneStreet-Agentic-Skills/actions/workflows/skill-validation.yml/badge.svg)](https://github.com/voyager67/JaneStreet-Agentic-Skills/actions/workflows/skill-validation.yml)

**A portable, evaluated skill collection for quantitative trading, systems engineering, mathematical reasoning, and technical learning.**

The repository contains 15 independently authored quantitative-trading and trading-systems skills, four additional learning/research skills, and Jane Street's original Socratic Tutor retained under its separate MIT license. All skill packages live under `skills/`.

## Repository structure

```text
JaneStreet-Agentic-Skills/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── ROADMAP.md
├── skills/
│   ├── socratic-tutor/
│   │   ├── SKILL.md                  # retained unchanged
│   │   ├── LICENSE.md                # original MIT license
│   │   ├── references/
│   │   │   ├── assessment-rubric.md
│   │   │   └── session-state.md
│   │   └── examples/
│   ├── mathematical-reasoning/
│   ├── code-understanding/
│   ├── research-paper-tutor/
│   ├── interview-simulator/
│   └── ... 15 existing quantitative-trading skills
├── evals/
│   ├── test_cases.yaml
│   └── <skill-name>/cases.yaml
├── scripts/
│   ├── validate_skills.py
│   ├── evaluate_skills.py
│   └── install_skills.py
└── .github/workflows/
    └── skill-validation.yml
```

All 16 existing skills were moved under `skills/` without changing their original `SKILL.md` content. The validator checks their Git blob hashes to prevent accidental edits.

## Skill catalogue

### Market microstructure

- **[lob-microstructure](skills/lob-microstructure/)** — order-flow imbalance, spread/depth, microprice, price impact, and adverse selection.
- **[order-book-reconstruction](skills/order-book-reconstruction/)** — exchange-message parsing, MBO/L2 state, sequencing, invariants, and recovery.
- **[queue-position-modeling](skills/queue-position-modeling/)** — queue-ahead estimation, passive fill probability, and uncertainty bounds.

### Trading and quantitative research

- **[market-making](skills/market-making/)** — inventory-aware quoting, fill/markout models, spread economics, and hedging.
- **[etf-arbitrage](skills/etf-arbitrage/)** — basket value, creation/redemption, premium/discount, cross-asset hedges, and frictions.
- **[volatility-market-making](skills/volatility-market-making/)** — options quoting, volatility surfaces, Greeks, hedging, and scenario risk.
- **[quant-research-validation](skills/quant-research-validation/)** — leakage, survivorship, multiple testing, realistic costs, and out-of-sample validation.
- **[agent-based-market-simulation](skills/agent-based-market-simulation/)** — discrete-event market simulation with interacting agents and explicit exchange rules.

### Execution and trading systems

- **[hft-market-replay](skills/hft-market-replay/)** — tick-level replay, latency, event ordering, queue-aware fills, and impact assumptions.
- **[execution-analysis](skills/execution-analysis/)** — implementation shortfall, slippage, participation, impact, and execution schedules.
- **[tick-data-engineering](skills/tick-data-engineering/)** — tick-data pipelines, timestamp semantics, sequence recovery, and provenance.
- **[exchange-gateway-engineering](skills/exchange-gateway-engineering/)** — order-entry state machines, protocols, acknowledgements, throttles, and recovery.
- **[low-latency-performance](skills/low-latency-performance/)** — tail-latency measurement and systems profiling.
- **[pre-trade-risk-controls](skills/pre-trade-risk-controls/)** — pre-trade limits, stale-data guards, throttles, and kill switches.
- **[production-trading-operations](skills/production-trading-operations/)** — production readiness, telemetry, reconciliation, incidents, and release controls.

### Mathematical and technical learning

- **[socratic-tutor](skills/socratic-tutor/)** — Jane Street's original structured Socratic tutor, retained unchanged under MIT.
- **[mathematical-reasoning](skills/mathematical-reasoning/)** — rigorous problem solving, derivations, proofs, counterexamples, and verification.
- **[code-understanding](skills/code-understanding/)** — codebase comprehension, execution tracing, root-cause debugging, and guided learning.
- **[research-paper-tutor](skills/research-paper-tutor/)** — paper walkthroughs, method/equation explanations, evidence appraisal, and reproducibility critique.
- **[interview-simulator](skills/interview-simulator/)** — adaptive technical interviews with evidence-based scoring and feedback.

## Quick start

Clone and install the full collection:

```bash
git clone https://github.com/voyager67/JaneStreet-Agentic-Skills.git
cd JaneStreet-Agentic-Skills

# Codex project skills
python3 scripts/install_skills.py --agent codex --scope project

# Claude Code project skills
python3 scripts/install_skills.py --agent claude-code --scope project
```

Install only selected skills:

```bash
python3 scripts/install_skills.py --agent codex --scope project --skills market-making,mathematical-reasoning,research-paper-tutor
```

Preview with `--dry-run`. Existing destination folders are not overwritten unless `--force` is supplied. See [COMPATIBILITY.md](COMPATIBILITY.md) for user installs and custom destinations.

## Validation and behavioral evaluation

Run structural checks and tests:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/evaluate_skills.py validate
```

The evaluation suite contains two cases per skill: a realistic trigger and a boundary/stress scenario. Cases are available centrally in `evals/test_cases.yaml` and individually in `evals/<skill-name>/cases.yaml`. These files use YAML 1.2's JSON-compatible subset so they remain readable YAML without requiring a third-party parser.

Render blinded prompts without evaluation criteria:

```bash
python3 scripts/evaluate_skills.py render
python3 scripts/evaluate_skills.py render --skill mathematical-reasoning
python3 scripts/evaluate_skills.py render --format json --output /tmp/skill-prompts.json
```

Score completed reviewer records:

```bash
python3 scripts/evaluate_skills.py score path/to/reviewer-results.jsonl
```

The repository does not call model APIs or invent benchmark results. Actual skill-enabled versus baseline model comparisons still need to be run and reviewed. See [EVALUATION.md](EVALUATION.md).

## Version roadmap

See [ROADMAP.md](ROADMAP.md) for scope and acceptance gates.

| Version | Main objective |
|---|---|
| 0.2.0 | Evaluation framework and session-state improvements |
| 0.3.0 | Adaptive assessment and spaced-repetition improvements |
| 0.4.0 | Cross-agent compatibility and automated validation |
| 0.5.0 | Mathematical reasoning and research tutor |
| 1.0.0 | Stable, tested skill collection with documented benchmarks |

## Scope, attribution, and licensing

The trading skills guide research and engineering. They are not exchange connectivity, trading software, market data, investment recommendations, or permission to place orders. No skill grants tool access or data entitlements. Live trading, production changes, and limit changes require explicit authorization and organizational controls.

This project is independent and is not affiliated with, sponsored by, or endorsed by Jane Street Group, LLC. The original `skills/socratic-tutor/SKILL.md` from [Jane Street's public agent_skills repository](https://github.com/janestreet/agent_skills) is retained unchanged under its original MIT license. The supplemental references and examples in that directory are repository-authored material under Apache-2.0. Repository-authored skills, scripts, tests, and documentation are also Apache-2.0. See [NOTICE](NOTICE) and [the original MIT license](skills/socratic-tutor/LICENSE.md).

Public references informing the quantitative scope include Jane Street's [trading overview](https://www.janestreet.com/what-we-do/overview/), the [SEC ETF investor bulletin](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-24), [HftBacktest](https://github.com/nkaz001/hftbacktest), [ML4T Agent Skills](https://github.com/ml4t/skills), [ABIDES-JPMC](https://github.com/jpmorganchase/abides-jpmc-public), [JAX-LOB](https://arxiv.org/abs/2308.13289), Nasdaq [ITCH](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf) and [OUCH](https://nasdaqtrader.com/Trader.aspx?id=OUCH), NYSE [Pillar](https://www.nyse.com/trade/pillar), Avellaneda and Stoikov's [market-making model](https://doi.org/10.1080/14697680701381228), Cont, Kukanov and Stoikov's [order-book impact study](https://doi.org/10.1093/jjfinec/nbt003), and Rigtorp's [queue-position estimation](https://rigtorp.se/2013/06/08/estimating-order-queue-position/). These links are references, not included third-party code or endorsements.

See [CHANGELOG.md](CHANGELOG.md) for changes and [CONTRIBUTING.md](CONTRIBUTING.md) for contribution requirements.
