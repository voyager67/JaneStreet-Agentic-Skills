# Contributing

Contributions should make an agent materially better at a concrete research, learning, quantitative-trading, or software-engineering task.

## Repository layout

- `skills/<skill-name>/SKILL.md`: one portable skill package.
- `skills/<skill-name>/agents/openai.yaml`: optional OpenAI UI metadata.
- `skills/<skill-name>/references/` and `examples/`: supporting material when needed.
- `evals/<skill-name>/cases.yaml`: skill-level trigger and boundary cases.
- `evals/test_cases.yaml`: central evaluation manifest.
- `scripts/`: validation, installation, and evaluation utilities.

## Requirements

1. Use a lowercase kebab-case skill directory under `skills/`; its frontmatter `name` must match the directory.
2. Use concise, accurate frontmatter with required `name` and `description` fields. The description must clearly identify activation scope and non-goals.
3. Keep each skill focused. Explain when to activate, what information to gather, how to work, what to validate, and what to deliver.
4. Add `agents/openai.yaml` metadata with a short UI description and useful suggested prompt.
5. Add at least one `trigger` and one `boundary` case in both the skill-level file and central manifest.
6. Keep the 16 existing skill instructions unchanged unless a future change explicitly requests their revision. A test validates their current Git blob hashes.
7. Do not claim access to proprietary Jane Street systems, internal strategies, exchange feeds, or non-public methods.
8. Do not copy text or code unless the license permits it and all notices are retained. The original Jane Street Socratic Tutor remains under its MIT license; supplemental references/examples are repository-authored.
9. Do not include API keys, credentials, account identifiers, customer data, exchange entitlements, or private market data.
10. Trading skills must not authorize live orders, limit changes, or control disablement without explicit authorization and required approvals.
11. Run all checks before opening a pull request:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/evaluate_skills.py validate
```

## Review checklist

- Does the description activate on the correct tasks and avoid unrelated tasks?
- Are claims, assumptions, evidence, units, timestamps, and sign conventions explicit?
- Does the skill distinguish observed facts, simulations, hypotheses, and interpretations?
- Are failure modes, safety boundaries, and user intent respected?
- Are evaluation cases useful, blinded, and aligned with the current skill?
- Are references credible and correctly attributed?
- Are original third-party skill files and licenses preserved?

## Licensing

Repository-authored skills, documentation, scripts, tests, and supplemental examples are licensed under Apache-2.0 unless explicitly marked otherwise. The retained `skills/socratic-tutor/SKILL.md` and its original `LICENSE.md` remain Jane Street third-party material under MIT and are not relicensed. See [LICENSE](LICENSE), [NOTICE](NOTICE), and [skills/socratic-tutor/LICENSE.md](skills/socratic-tutor/LICENSE.md).
