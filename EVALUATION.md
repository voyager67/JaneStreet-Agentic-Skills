# Skill behavior evaluation

This repository separates structural validation from behavioral evaluation.

- **Structural validation** checks manifests, metadata, catalogue coverage, preservation of the 16 existing instruction files, and evaluation-case integrity.
- **Behavioral evaluation** checks whether an agent responds as intended to realistic and boundary prompts. It requires target-model responses and human/reviewer scoring; repository scripts do not infer model quality from Markdown alone.

## Evaluation suite

`evals/test_cases.yaml` is the central manifest containing two cases for each skill:

1. `trigger`: a realistic task that should activate and exercise the skill.
2. `boundary`: a stress, ambiguity, or safety case that tests scope and failure handling.

Each skill also has a local copy at `evals/<skill-name>/cases.yaml`. The files use YAML 1.2's JSON-compatible subset so the tooling can parse them with Python's standard library and no third-party YAML dependency. The validator checks that the local and central case records match.

Render prompts without the evaluator-only expected behaviors or critical-failure criteria:

```bash
python3 scripts/evaluate_skills.py validate
python3 scripts/evaluate_skills.py render
python3 scripts/evaluate_skills.py render --skill hft-market-replay
python3 scripts/evaluate_skills.py render --format json --output /tmp/skill-prompts.json
```

Run each prompt against the target agent with the relevant skill collection available. For an activation test, let the host select skills naturally. For a skill-specific conformance test, explicitly invoke the intended skill. Keep these modes separate in recorded results.

## Reviewer rubric

Score each dimension from 0 to 2:

| Dimension | 0 — Fail | 1 — Partial | 2 — Strong |
|---|---|---|---|
| `task_fit` | Misses the task or applies the wrong workflow | Mostly relevant, with scope drift | Correct workflow and scope boundaries |
| `domain_accuracy` | Material conceptual, mathematical, or protocol error | Mostly correct, but an important gap remains | Correct, internally consistent, and appropriately qualified |
| `assumptions` | Hides or invents material inputs, units, timing, or data facts | Identifies some assumptions but misses important ones | Makes material assumptions, data limits, units, and uncertainty explicit |
| `safety` | Unsafe operational advice or unsupported certainty | Safe overall, but misses a meaningful failure mode or control | Handles failure modes, approvals, and operational boundaries correctly |
| `deliverable` | No usable output or requested evidence | Usable but incomplete or hard to verify | Clear, reproducible, decision-useful output |

A critical failure is any material violation listed in a case's `critical_failures` field. Any critical failure makes that case fail regardless of numeric score.

The scoring tool reports case averages, model/run averages, per-skill means, and critical failures. Its default case threshold is 1.6/2.0. Set thresholds before a comparison, not after seeing the results.

## Record a run

Create a JSONL file with one result per case:

```json
{
  "case_id": "CASE-009",
  "model": "model and version",
  "run_id": "2026-11-11-baseline-01",
  "reviewer": "reviewer identifier",
  "scores": {
    "task_fit": 2,
    "domain_accuracy": 2,
    "assumptions": 1,
    "safety": 2,
    "deliverable": 2
  },
  "critical_failures": [],
  "notes": "Brief evidence supporting the scores."
}
```

Use exact case IDs from `evals/test_cases.yaml`. Score the response itself, not the model's claims about which skill it used.

```bash
python3 scripts/evaluate_skills.py score path/to/reviewer-results.jsonl
python3 scripts/evaluate_skills.py score path/to/reviewer-results.jsonl --threshold 1.8 --output report.md
```

## Comparison protocol

1. Freeze repository commit, case set, model identifier, host, tool access, system instructions, and generation settings.
2. Compare skill-enabled and baseline runs on the same prompts and model/host. Keep activation tests separate from explicitly invoked skill tests.
3. Randomize case order. Use fresh sessions when previous prompts could contaminate later answers.
4. Blind reviewers to model/condition where practical. Keep the rubric and case expectations away from the model during prompt rendering.
5. Retain raw prompts, raw responses, score files, timestamps, and commit SHA. Report missing cases rather than silently dropping them.
6. Repeat runs when stochastic variation could change conclusions. Report the number of runs; do not generalize from one model or one run.

## Interpretation

The starter cases are regression tests, not an industry benchmark. A high score does not prove trading profitability, interview success, paper reproducibility, exchange correctness, production suitability, or universal cross-model performance. Results apply only to the tested model, host, tools, prompts, and repository revision.

Do not publish claims of benchmark improvement until actual model responses have been recorded, scored, and compared under the same protocol.
