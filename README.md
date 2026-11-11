# JaneStreet Agentic Skills

A focused collection of reusable agent skills for quantitative trading, market microstructure, systems engineering, mathematics, software development, research, and technical learning.

## Skills

### Quantitative trading and market structure

| Skill | Purpose |
|---|---|
| [LOB Microstructure](skills/lob-microstructure/) | Order-flow imbalance, spread and depth, microprice, impact, and adverse selection |
| [Order Book Reconstruction](skills/order-book-reconstruction/) | Exchange-message parsing, MBO/L2 state, sequencing, and recovery |
| [Queue Position Modeling](skills/queue-position-modeling/) | Queue-ahead estimation and passive fill probability |
| [Market Making](skills/market-making/) | Inventory-aware quoting, fills, markouts, and hedging |
| [ETF Arbitrage](skills/etf-arbitrage/) | Basket valuation, creation/redemption, premiums, discounts, and costs |
| [Volatility Market Making](skills/volatility-market-making/) | Options quoting, volatility surfaces, Greeks, and hedging |
| [Quant Research Validation](skills/quant-research-validation/) | Leakage, multiple testing, costs, and out-of-sample research |
| [Agent-Based Market Simulation](skills/agent-based-market-simulation/) | Discrete-event market simulations and interacting agents |

### Execution and trading systems

| Skill | Purpose |
|---|---|
| [HFT Market Replay](skills/hft-market-replay/) | Tick-level replay, latency, event ordering, and fill assumptions |
| [Execution Analysis](skills/execution-analysis/) | Implementation shortfall, slippage, impact, and execution schedules |
| [Tick Data Engineering](skills/tick-data-engineering/) | Market-data pipelines, timestamps, sequencing, and provenance |
| [Exchange Gateway Engineering](skills/exchange-gateway-engineering/) | Order-entry protocols, state machines, acknowledgements, and recovery |
| [Low-Latency Performance](skills/low-latency-performance/) | Latency measurement, profiling, and tail performance |
| [Pre-Trade Risk Controls](skills/pre-trade-risk-controls/) | Order limits, stale-data checks, throttles, and kill switches |
| [Production Trading Operations](skills/production-trading-operations/) | Monitoring, reconciliation, release readiness, and incident response |

### Mathematics, software, and learning

| Skill | Purpose |
|---|---|
| [Socratic Tutor](skills/socratic-tutor/) | Structured question-led learning and mastery tracking |
| [Mathematical Reasoning](skills/mathematical-reasoning/) | Problem solving, derivations, proofs, and verification |
| [Code Understanding](skills/code-understanding/) | Codebase comprehension, execution tracing, and debugging |
| [Research Paper Tutor](skills/research-paper-tutor/) | Paper walkthroughs, methods, evidence, and limitations |
| [Interview Simulator](skills/interview-simulator/) | Technical interview practice and scored feedback |

## Mastery levels

The Socratic Tutor uses a six-level scale to track demonstrated understanding:

| Level | Description |
|---:|---|
| 0 | Unaware |
| 1 | Heard of the concept |
| 2 | Can follow an explanation |
| 3 | Can complete a task with help |
| 4 | Can work independently |
| 5 | Can handle edge cases and teach the concept |

Levels are evidence-based. A level should reflect demonstrated performance, not lesson completion or confidence alone. The [assessment rubric](skills/socratic-tutor/references/assessment-rubric.md) describes the evidence standard.

## Repository structure

```text
.
├── README.md
├── LICENSE
├── NOTICE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── skills/
│   ├── socratic-tutor/
│   │   ├── SKILL.md
│   │   ├── LICENSE.md
│   │   ├── references/
│   │   │   ├── assessment-rubric.md
│   │   │   └── session-state.md
│   │   └── examples/
│   ├── mathematical-reasoning/
│   ├── code-understanding/
│   ├── research-paper-tutor/
│   ├── interview-simulator/
│   └── ... quantitative trading and systems skills
├── evals/
│   ├── test_cases.yaml
│   └── <skill-name>/
│       └── cases.yaml
├── scripts/
│   └── validate_skills.py
└── .github/
    └── workflows/
        └── skill-validation.yml
```

## Use a skill

Open the relevant skill directory and use its `SKILL.md` with an agent that supports the Agent Skills format. Include any companion `references/` or `examples/` files provided by that skill. Follow the skill host's instructions for installing or importing skills.

## Evaluation and validation

The `evals/` directory contains example activation and boundary cases for each skill. The central file lists all cases; each skill directory contains its own cases.

Run the repository validator with Python 3.10 or later:

```bash
python scripts/validate_skills.py
```

## Licensing

Repository-authored skills and documentation are licensed under Apache-2.0. The original `skills/socratic-tutor/SKILL.md` is retained unchanged under Jane Street's MIT license, included at [skills/socratic-tutor/LICENSE.md](skills/socratic-tutor/LICENSE.md). See [NOTICE](NOTICE) for attribution and license separation.

This is an independent project and is not affiliated with or endorsed by Jane Street Group, LLC.
