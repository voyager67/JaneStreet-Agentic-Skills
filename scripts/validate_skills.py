#!/usr/bin/env python3
"""Dependency-free structural validator for JaneStreet Agentic Skills."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
URL = re.compile(r"https?://[^\s)<>]+", re.IGNORECASE)
UPSTREAM_SHA256 = "9190b68440ad99be4d865c63b87939f23a362efac0776c5a67c93d1498bb5e37"
EXPECTED_SKILL_COUNT = 20

# Git blob object IDs from the 16 existing skill files before this restructure.
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


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = content.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing frontmatter delimiter")
    fields: dict[str, str] = {}
    for line_number, line in enumerate(content[4:end].splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid scalar frontmatter at line {line_number}")
        key, value = line.split(":", 1)
        key = key.strip()
        if key in fields:
            raise ValueError(f"duplicate frontmatter key {key!r}")
        fields[key] = scalar(value)
    return fields, content[end + 5:]


def parse_ui_metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    fields = {}
    for key in ("display_name", "short_description", "default_prompt"):
        match = re.search(rf"^  {key}:\s*(.+?)\s*$", text, re.MULTILINE)
        if not match:
            raise ValueError(f"missing interface.{key}")
        fields[key] = scalar(match.group(1))
        if not fields[key]:
            raise ValueError(f"interface.{key} is empty")
    if len(fields["short_description"]) > 64:
        raise ValueError("interface.short_description exceeds 64 characters")
    if not re.search(r"^policy:\s*$", text, re.MULTILINE):
        raise ValueError("missing policy section")
    if not re.search(r"^  allow_implicit_invocation:\s*(true|false)\s*$", text, re.MULTILINE):
        raise ValueError("policy.allow_implicit_invocation must be boolean")
    return fields


def skill_directories() -> list[Path]:
    if not SKILLS_ROOT.is_dir():
        return []
    return sorted(path for path in SKILLS_ROOT.iterdir()
                  if path.is_dir() and (path / "SKILL.md").is_file())


def check_urls(path: Path, errors: list[str]) -> None:
    content = path.read_text(encoding="utf-8")
    for raw in URL.findall(content):
        candidate = raw.rstrip(".,;:")
        try:
            parsed = urlsplit(candidate)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname or "." not in parsed.hostname:
                errors.append(f"{path.relative_to(ROOT)}: malformed URL {candidate!r}")
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: malformed URL {candidate!r}")


def main() -> int:
    errors: list[str] = []
    dirs = skill_directories()
    names = {folder.name for folder in dirs}

    for folder in dirs:
        skill_path = folder / "SKILL.md"
        try:
            fields, body = parse_frontmatter(skill_path)
        except (OSError, ValueError) as exc:
            errors.append(f"{skill_path.relative_to(ROOT)}: {exc}")
            continue

        name = fields.get("name", "")
        description = fields.get("description", "")
        if name != folder.name:
            errors.append(f"{skill_path.relative_to(ROOT)}: name must match directory {folder.name!r}")
        if not NAME.fullmatch(name) or len(name) > 64:
            errors.append(f"{skill_path.relative_to(ROOT)}: invalid name {name!r}")
        if not description or len(description) > 1024:
            errors.append(f"{skill_path.relative_to(ROOT)}: description missing or exceeds 1024 characters")
        if len(body.strip()) < 300:
            errors.append(f"{skill_path.relative_to(ROOT)}: instructions too short")
        if len(skill_path.read_text(encoding="utf-8").splitlines()) > 500:
            errors.append(f"{skill_path.relative_to(ROOT)}: exceeds 500 lines")

        metadata = folder / "agents" / "openai.yaml"
        if not metadata.is_file():
            errors.append(f"{metadata.relative_to(ROOT)}: missing OpenAI UI metadata")
        else:
            try:
                ui = parse_ui_metadata(metadata)
                if len(ui["display_name"]) > 64:
                    errors.append(f"{metadata.relative_to(ROOT)}: display_name exceeds 64 characters")
            except (OSError, ValueError) as exc:
                errors.append(f"{metadata.relative_to(ROOT)}: {exc}")
        check_urls(skill_path, errors)

    if len(dirs) != EXPECTED_SKILL_COUNT:
        errors.append(f"expected {EXPECTED_SKILL_COUNT} skills, found {len(dirs)}")

    for name, expected_sha in PRESERVED_SKILL_BLOBS.items():
        path = SKILLS_ROOT / name / "SKILL.md"
        if not path.is_file():
            errors.append(f"preserved skill missing: {name}")
        elif git_blob_sha(path) != expected_sha:
            errors.append(f"existing skill content changed: {name}")

    retained = SKILLS_ROOT / "socratic-tutor" / "SKILL.md"
    if not retained.is_file():
        errors.append("Jane Street socratic-tutor is missing")
    elif hashlib.sha256(retained.read_bytes()).hexdigest() != UPSTREAM_SHA256:
        errors.append("Jane Street socratic-tutor fingerprint mismatch")

    for doc_name in ("README.md", "SKILLS.md", "ROADMAP.md", "CONTRIBUTING.md", "COMPATIBILITY.md", "EVALUATION.md"):
        path = ROOT / doc_name
        if not path.is_file():
            errors.append(f"{doc_name} is missing")
            continue
        doc = path.read_text(encoding="utf-8")
        if doc_name in {"README.md", "SKILLS.md"}:
            for name in sorted(names):
                if name not in doc:
                    errors.append(f"{doc_name} does not reference skill {name!r}")
        check_urls(path, errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(dirs)} skills, OpenAI metadata, documentation, URLs, and preserved skill hashes.")
    for folder in dirs:
        print(f"  OK  {folder.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
