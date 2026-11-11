# Repository guidance

This repository contains 15 independently authored quantitative-trading and trading-systems skills, plus the separately licensed Jane Street `socratic-tutor` reference skill.

## Non-negotiable constraints

- Preserve `socratic-tutor/SKILL.md` byte-for-byte. It is retained third-party material under its original MIT license; the repository validator checks its SHA-256 fingerprint.
- Do not imply affiliation with Jane Street or access to its private systems, strategies, data, or internal research.
- Skills guide research and engineering. They do not provide market data, exchange connectivity, investment advice, or authorization to trade.
- Never instruct an agent to place live orders, relax production risk limits, disable controls, or resume risk-increasing trading without explicit authorization and the required human approvals.
- Distinguish observed facts, estimates, assumptions, simulated outcomes, and hypotheses. Never invent benchmark results.
- Preserve venue, instrument, timestamp, unit, sign-convention, data-provenance, and model assumptions in quantitative examples.

## Skill authoring

- Keep one skill per directory with a `SKILL.md` whose `name` matches the directory.
- Keep descriptions concise and explicit about both activation scope and non-goals.
- Use imperative, testable workflows with required inputs, checks, failure modes, and a defined deliverable.
- Prefer standard-library scripts and optional references over unnecessary runtime dependencies.
- Add two evaluation cases for each new skill: one realistic trigger and one boundary or stress case.
- Add matching `agents/openai.yaml` UI metadata and keep it synchronized with the skill.
- Update `README.md`, `SKILLS.md`, and `evals/cases.jsonl` when the catalogue changes.

## Verification

Run these commands from the repository root:

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/evaluate_skills.py validate
```

For a behavior review, render prompts without the evaluator rubric, run them against the target agent/model, and record blinded reviewer scores as described in [EVALUATION.md](EVALUATION.md).

Keep changes focused. Do not claim tests or model evaluations passed unless they were actually run.
