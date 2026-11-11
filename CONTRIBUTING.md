# Contributing

Contributions should make an agent materially better at a concrete quantitative-trading or trading-systems task.

## Good contributions

- A clearly bounded workflow for market microstructure, market making, execution, quantitative research, exchange systems, low-latency engineering, risk, or production operations.
- A short, accurate activation description with specific trigger phrases or task conditions.
- Domain-specific steps, equations with stated assumptions, edge cases, and a usable deliverable checklist.
- References to primary papers, official venue documentation, maintained technical documentation, or well-established open-source projects.
- Tests, reproducible examples, and explicit statements about what the data or model cannot establish.

## Requirements

1. One skill per directory, with a `SKILL.md` directly inside it.
2. Use standard YAML frontmatter with required `name` and `description` fields. The `name` must match the directory name.
3. Keep each skill focused. It should tell an agent when to activate, what information to gather, how to work, what to validate, and what to deliver.
4. Do not claim access to proprietary Jane Street systems, internal strategies, exchange feeds, or non-public trading methods.
5. Do not copy skill text or code from other repositories unless the license permits it and all required notices are retained. Prefer independently written procedures and cite conceptual sources.
6. Do not include API keys, credentials, account identifiers, customer data, exchange entitlements, or private market data.
7. Keep external actions safe. A skill must not instruct an agent to place live orders, relax production limits, or disable controls without explicit authorization and the proper approvals.
8. Run `python3 scripts/validate_skills.py` and `python3 -m unittest discover -s tests -v` before submitting a pull request.

## Review checklist

- Does the description activate on the correct tasks and avoid unrelated tasks?
- Are assumptions, units, timestamps, and sign conventions explicit?
- Are the key financial and venue mechanics correct for the stated scope?
- Does the skill distinguish historical replay from counterfactual simulation?
- Are fill, queue, fees, latency, market impact, and risk assumptions visible where relevant?
- Are examples reproducible and free of invented benchmark results?
- Are references credible, current where needed, and correctly attributed?

## License and copyright

Contributions to the original skills and repository-authored material are made available under Apache-2.0. By submitting a contribution, you agree that it will be distributed under that license unless the contribution is explicitly marked otherwise and accepted with a compatible notice. The retained `socratic-tutor` skill is third-party material under its original MIT license and is not covered by this repository's Apache-2.0 grant. See [LICENSE](LICENSE), [NOTICE](NOTICE), and `socratic-tutor/LICENSE.md`.