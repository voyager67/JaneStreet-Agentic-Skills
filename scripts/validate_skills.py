#!/usr/bin/env python3
"""Dependency-free structural validator for JaneStreet Agentic Skills."""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_SHA256 = "9190b68440ad99be4d865c63b87939f23a362efac0776c5a67c93d1498bb5e37"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing frontmatter delimiter")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields, text[end + 5:]


def main() -> int:
    errors: list[str] = []
    skill_files = sorted(
        p / "SKILL.md" for p in ROOT.iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    )
    names: set[str] = set()
    for path in skill_files:
        try:
            fields, body = parse_frontmatter(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        name = fields.get("name", "")
        desc = fields.get("description", "")
        if name != path.parent.name:
            errors.append(f"{path.parent.name}: frontmatter name does not match directory")
        if not NAME_RE.fullmatch(name):
            errors.append(f"{path.parent.name}: invalid skill name")
        if not desc:
            errors.append(f"{path.parent.name}: description is missing")
        if name in names:
            errors.append(f"{path.parent.name}: duplicate skill name")
        names.add(name)
        if len(body.strip()) < 300:
            errors.append(f"{path.parent.name}: instructions are too short")
        if len(path.read_text(encoding="utf-8").splitlines()) > 500:
            errors.append(f"{path.parent.name}: exceeds 500 lines")

    retained = ROOT / "socratic-tutor" / "SKILL.md"
    if not retained.is_file():
        errors.append("Jane Street socratic-tutor/SKILL.md is missing")
    elif hashlib.sha256(retained.read_bytes()).hexdigest() != UPSTREAM_SHA256:
        errors.append("Jane Street socratic-tutor fingerprint mismatch")
    if len(skill_files) < 16:
        errors.append(f"expected 16 skills, found {len(skill_files)}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validated {len(skill_files)} skills; Jane Street source fingerprint OK.")
    for name in sorted(names):
        print(f"  OK  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
