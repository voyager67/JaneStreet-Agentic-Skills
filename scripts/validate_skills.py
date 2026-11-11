#!/usr/bin/env python3
"""Validate skill packages, preservation of existing skills, and evaluation cases."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
EVALS_ROOT = ROOT / "evals"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
UPSTREAM_SHA256 = "9190b68440ad99be4d865c63b87939f23a362efac0776c5a67c93d1498bb5e37"
EXPECTED_SKILLS = {
    "agent-based-market-simulation",
    "code-understanding",
    "etf-arbitrage",
    "exchange-gateway-engineering",
    "execution-analysis",
    "hft-market-replay",
    "interview-simulator",
    "lob-microstructure",
    "low-latency-performance",
    "market-making",
    "mathematical-reasoning",
    "order-book-reconstruction",
    "pre-trade-risk-controls",
    "production-trading-operations",
    "quant-research-validation",
    "queue-position-modeling",
    "research-paper-tutor",
    "socratic-tutor",
    "tick-data-engineering",
    "volatility-market-making",
}
PRESERVED_SKILL_BLOBS = {
    "agent-based-market-simulation": "7bbc34a461b804890227f34271fe4258a7cc0de2",
    "etf-arbitrage": "c3997858a5348585381ddda0b1f79db9381efd5c",
    "exchange-gateway-engineering": "9bec552a16b063afe8d31c9f7f8c039fc08755de",
    "execution-analysis": "b678bcf562b10303f25ea98872a61795d64f70a9",
    "hft-market-replay": "65f5b6faf2998537dd4e7b7f6024a4afaebb59cb",
    "lob-microstructure": "ce74b88b7e596acff3c96903d61fea0866e6fcf9",
    "low-latency-performance": "47e98a0be22bedb3f3003a33b933fd8aac379cf4",
    "market-making": "9663407cc53be668b4fa5d65ef3bc0b33df0be63",
    "order-book-reconstruction": "f91ac3b6b42da7ca49c973ca753ba20a3d066e58",
    "pre-trade-risk-controls": "46898f92acb1a28708d8841aae0e5fcd392a99e2",
    "production-trading-operations": "5add336374371018c908e53d2d7fc7dfd3b5267c",
    "quant-research-validation": "b7ea4bbfe228bd47c8fe1a6c7b19c246013a7313",
    "queue-position-modeling": "e64aeedbbfe6456814dd606b294d25c293eae91e",
    "socratic-tutor": "93bb7befeb73c41b4354175f9ef765547d4f3506",
    "tick-data-engineering": "aa81ac5c70d92ebfb43a9f35c5015dfeef74e9b2",
    "volatility-market-making": "021d41d2332633728f8b6616788a71f4baa2a138",
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = content.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing frontmatter delimiter")
    fields = {}
    for line in content[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields, content[end + 5:]


def load_cases(path: Path) -> list[dict]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)} must contain JSON-compatible YAML: {exc}") from exc
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a list of case objects")
    return value


def main() -> int:
    errors = []
    folders = sorted(path for path in SKILLS_ROOT.iterdir()
                     if path.is_dir() and (path / "SKILL.md").is_file())
    actual = {folder.name for folder in folders}

    if actual != EXPECTED_SKILLS:
        errors.append(
            f"skill catalogue mismatch; missing={sorted(EXPECTED_SKILLS-actual)}, "
            f"unexpected={sorted(actual-EXPECTED_SKILLS)}"
        )

    for folder in folders:
        path = folder / "SKILL.md"
        try:
            fields, body = parse_frontmatter(path)
        except (OSError, ValueError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        name = fields.get("name", "")
        description = fields.get("description", "")
        if name != folder.name or not NAME.fullmatch(name):
            errors.append(f"{path.relative_to(ROOT)}: invalid or mismatched skill name")
        if not description or len(description) > 1024:
            errors.append(f"{path.relative_to(ROOT)}: missing or overly long description")
        if len(body.strip()) < 200:
            errors.append(f"{path.relative_to(ROOT)}: skill instructions are unexpectedly short")

    for name, expected in PRESERVED_SKILL_BLOBS.items():
        path = SKILLS_ROOT / name / "SKILL.md"
        if not path.is_file() or git_blob_sha(path) != expected:
            errors.append(f"existing skill content changed or missing: {name}")

    tutor = SKILLS_ROOT / "socratic-tutor" / "SKILL.md"
    if not tutor.is_file() or hashlib.sha256(tutor.read_bytes()).hexdigest() != UPSTREAM_SHA256:
        errors.append("retained Jane Street Socratic Tutor fingerprint mismatch")

    try:
        central = load_cases(EVALS_ROOT / "test_cases.yaml")
    except ValueError as exc:
        errors.append(str(exc))
        central = []

    required_fields = {"id", "skill", "kind", "prompt", "expected_behaviors", "critical_failures"}
    seen = set()
    coverage = {name: set() for name in EXPECTED_SKILLS}
    for index, case in enumerate(central, 1):
        missing = required_fields - case.keys()
        if missing:
            errors.append(f"evaluation case {index}: missing fields {sorted(missing)}")
            continue
        case_id = case["id"]
        skill = case["skill"]
        if case_id in seen:
            errors.append(f"duplicate evaluation case id: {case_id}")
        seen.add(case_id)
        if skill not in EXPECTED_SKILLS:
            errors.append(f"evaluation case {case_id}: unknown skill {skill}")
            continue
        if case["kind"] not in {"trigger", "boundary"}:
            errors.append(f"evaluation case {case_id}: invalid kind {case['kind']}")
        coverage[skill].add(case["kind"])
        if not isinstance(case["prompt"], str) or len(case["prompt"].strip()) < 20:
            errors.append(f"evaluation case {case_id}: prompt is missing or too short")
        for key in ("expected_behaviors", "critical_failures"):
            if not isinstance(case[key], list) or not case[key]:
                errors.append(f"evaluation case {case_id}: {key} must be a non-empty list")

    for skill in sorted(EXPECTED_SKILLS):
        if coverage[skill] != {"trigger", "boundary"}:
            errors.append(f"{skill}: expected trigger and boundary evaluation cases")
        local_path = EVALS_ROOT / skill / "cases.yaml"
        try:
            local = load_cases(local_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        expected_local = [case for case in central if case.get("skill") == skill]
        if local != expected_local:
            errors.append(f"{local_path.relative_to(ROOT)} differs from central test_cases.yaml")

    if len(central) != len(EXPECTED_SKILLS) * 2:
        errors.append(f"expected {len(EXPECTED_SKILLS)*2} evaluation cases, found {len(central)}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(folders)} skills, preserved 16 existing skill files, and {len(central)} evaluation cases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
