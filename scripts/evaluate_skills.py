#!/usr/bin/env python3
"""Validate, render, and score the repository's model-agnostic skill evaluations."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "evals" / "cases.jsonl"
DIMENSIONS = ("task_fit", "domain_accuracy", "assumptions", "safety", "deliverable")
DEFAULT_THRESHOLD = 1.6


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: each JSONL record must be an object")
        records.append(value)
    return records


def skill_names() -> set[str]:
    return {
        path.name for path in ROOT.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }


def validate_cases(cases: list[dict]) -> list[str]:
    errors: list[str] = []
    required = {"id", "skill", "kind", "prompt", "expected_behaviors", "critical_failures"}
    known_skills = skill_names()
    seen: set[str] = set()
    coverage: dict[str, set[str]] = defaultdict(set)

    for index, case in enumerate(cases, 1):
        prefix = f"case {index}"
        missing = required - case.keys()
        extra = case.keys() - required
        if missing:
            errors.append(f"{prefix}: missing fields: {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"{prefix}: unexpected fields: {', '.join(sorted(extra))}")
        case_id = case.get("id")
        skill = case.get("skill")
        kind = case.get("kind")
        prompt = case.get("prompt")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{prefix}: id must be a non-empty string")
        elif case_id in seen:
            errors.append(f"{prefix}: duplicate id {case_id!r}")
        else:
            seen.add(case_id)
        if skill not in known_skills:
            errors.append(f"{prefix}: unknown skill {skill!r}")
        if kind not in {"trigger", "boundary"}:
            errors.append(f"{prefix}: kind must be 'trigger' or 'boundary'")
        elif skill in known_skills:
            coverage[skill].add(kind)
        if not isinstance(prompt, str) or len(prompt.strip()) < 20:
            errors.append(f"{prefix}: prompt must contain at least 20 characters")
        for key in ("expected_behaviors", "critical_failures"):
            values = case.get(key)
            if not isinstance(values, list) or not values or any(
                not isinstance(item, str) or not item.strip() for item in values
            ):
                errors.append(f"{prefix}: {key} must be a non-empty list of strings")

    for skill in sorted(known_skills):
        kinds = coverage.get(skill, set())
        for required_kind in ("trigger", "boundary"):
            if required_kind not in kinds:
                errors.append(f"{skill}: missing {required_kind} evaluation case")
    if not cases:
        errors.append("evaluation case set is empty")
    return errors


def render_cases(cases: list[dict], selected_skill: str | None, output_format: str) -> str:
    selected = [case for case in cases if selected_skill is None or case["skill"] == selected_skill]
    if selected_skill is not None and not selected:
        raise ValueError(f"no cases found for skill {selected_skill!r}")
    if output_format == "json":
        # Evaluator-only expectations and failure criteria are intentionally omitted.
        return json.dumps(
            [{"id": case["id"], "prompt": case["prompt"]} for case in selected],
            indent=2,
            ensure_ascii=False,
        ) + "\n"

    blocks = ["# Skill evaluation prompts", ""]
    for case in selected:
        blocks.extend([f"## {case['id']}", "", case["prompt"], ""])
    return "\n".join(blocks).rstrip() + "\n"


def validate_results(results: list[dict], cases: list[dict]) -> list[str]:
    errors: list[str] = []
    case_ids = {case["id"] for case in cases}
    seen: set[tuple[str, str, str]] = set()
    required = {"case_id", "model", "run_id", "reviewer", "scores", "critical_failures"}
    for index, result in enumerate(results, 1):
        prefix = f"result {index}"
        missing = required - result.keys()
        if missing:
            errors.append(f"{prefix}: missing fields: {', '.join(sorted(missing))}")
            continue
        case_id = result["case_id"]
        if case_id not in case_ids:
            errors.append(f"{prefix}: unknown case_id {case_id!r}")
        for field in ("model", "run_id", "reviewer"):
            if not isinstance(result[field], str) or not result[field].strip():
                errors.append(f"{prefix}: {field} must be a non-empty string")
        key = (str(case_id), str(result["model"]), str(result["run_id"]))
        if key in seen:
            errors.append(f"{prefix}: duplicate case/model/run result {key}")
        seen.add(key)
        scores = result["scores"]
        if not isinstance(scores, dict) or set(scores) != set(DIMENSIONS):
            errors.append(f"{prefix}: scores must contain exactly {', '.join(DIMENSIONS)}")
        else:
            for dimension, value in scores.items():
                if isinstance(value, bool) or not isinstance(value, int) or value not in (0, 1, 2):
                    errors.append(f"{prefix}: {dimension} must be integer 0, 1, or 2")
        failures = result["critical_failures"]
        if not isinstance(failures, list) or any(not isinstance(v, str) for v in failures):
            errors.append(f"{prefix}: critical_failures must be a list of strings")
    if not results:
        errors.append("review result file is empty")
    return errors


def summarize_results(results: list[dict], cases: list[dict], threshold: float) -> dict:
    case_by_id = {case["id"]: case for case in cases}
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for result in results:
        groups[(result["model"], result["run_id"])].append(result)

    summary = []
    for (model, run_id), rows in sorted(groups.items()):
        case_scores = [
            mean(row["scores"][dimension] for dimension in DIMENSIONS)
            for row in rows
        ]
        passed = [
            score >= threshold and not row["critical_failures"]
            for score, row in zip(case_scores, rows)
        ]
        per_skill: dict[str, list[float]] = defaultdict(list)
        for row, score in zip(rows, case_scores):
            per_skill[case_by_id[row["case_id"]]["skill"]].append(score)
        summary.append({
            "model": model,
            "run_id": run_id,
            "cases_scored": len(rows),
            "mean_score": round(mean(case_scores), 3),
            "case_passes": sum(passed),
            "case_pass_rate": round(sum(passed) / len(passed), 3),
            "critical_failure_count": sum(len(row["critical_failures"]) for row in rows),
            "skills": {
                skill: round(mean(scores), 3)
                for skill, scores in sorted(per_skill.items())
            },
        })
    return {"threshold": threshold, "runs": summary}


def format_report(summary: dict) -> str:
    lines = [
        "# Skill evaluation report",
        "",
        f"Case pass threshold: **{summary['threshold']:.2f}/2.00**",
        "",
        "| Model | Run | Cases | Mean / 2 | Case pass rate | Critical failures |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for run in summary["runs"]:
        lines.append(
            f"| {run['model']} | {run['run_id']} | {run['cases_scored']} | "
            f"{run['mean_score']:.3f} | {run['case_passes']}/{run['cases_scored']} "
            f"({run['case_pass_rate']:.1%}) | {run['critical_failure_count']} |"
        )
        lines.extend(["", f"### Per-skill means — {run['model']} / {run['run_id']}", "",
                      "| Skill | Mean / 2 |", "|---|---:|"])
        for skill, score in run["skills"].items():
            lines.append(f"| {skill} | {score:.3f} |")
    return "\n".join(lines) + "\n"


def write_output(content: str, output: str | None) -> None:
    if output:
        Path(output).expanduser().write_text(content, encoding="utf-8")
        print(f"Wrote {output}")
    else:
        sys.stdout.write(content)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="validate case coverage and schema")
    render_parser = subparsers.add_parser("render", help="render prompts without evaluator-only criteria")
    render_parser.add_argument("--skill", help="render one skill's cases")
    render_parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    render_parser.add_argument("--output", help="write rendered prompts to this path")
    score_parser = subparsers.add_parser("score", help="summarize reviewer-scored JSONL results")
    score_parser.add_argument("input", help="review result JSONL path")
    score_parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    score_parser.add_argument("--output", help="write a Markdown report to this path")
    args = parser.parse_args(argv)

    try:
        cases = load_jsonl(CASES_PATH)
        errors = validate_cases(cases)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1

        if args.command == "validate":
            print(f"Validated {len(cases)} cases across {len(skill_names())} skills.")
            return 0
        if args.command == "render":
            if args.skill and args.skill not in skill_names():
                raise ValueError(f"unknown skill {args.skill!r}")
            rendered = render_cases(cases, args.skill, args.format)
            write_output(rendered, args.output)
            return 0
        if args.command == "score":
            if not 0.0 <= args.threshold <= 2.0:
                raise ValueError("threshold must be between 0 and 2")
            results = load_jsonl(Path(args.input).expanduser())
            errors = validate_results(results, cases)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}", file=sys.stderr)
                return 1
            summary = summarize_results(results, cases, args.threshold)
            write_output(format_report(summary), args.output)
            return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
