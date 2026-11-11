#!/usr/bin/env python3
"""Dependency-free structural validator for JaneStreet Agentic Skills."""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
UPSTREAM = "9190b68440ad99be4d865c63b87939f23a362efac0776c5a67c93d1498bb5e37"


def parse(path: Path):
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


def main() -> int:
    errors, names = [], set()
    dirs = sorted(
        p for p in ROOT.iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    )
    for folder in dirs:
        path = folder / "SKILL.md"
        try:
            fields, body = parse(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue

        name = fields.get("name", "")
        description = fields.get("description", "")
        if name != folder.name:
            errors.append(f"{path}: name must match folder")
        if not NAME.fullmatch(name):
            errors.append(f"{path}: invalid name {name!r}")
        if len(name) > 64:
            errors.append(f"{path}: name exceeds 64 characters")
        if not description or len(description) > 1024:
            errors.append(f"{path}: description missing or too long")
        if name in names:
            errors.append(f"{path}: duplicate skill name")
        names.add(name)
        if len(body.strip()) < 300:
            errors.append(f"{path}: instructions too short")
        if len(path.read_text(encoding="utf-8").splitlines()) > 500:
            errors.append(f"{path}: exceeds 500 lines")

    retained = ROOT / "socratic-tutor" / "SKILL.md"
    if not retained.is_file():
        errors.append("Jane Street socratic-tutor is missing")
    elif hashlib.sha256(retained.read_bytes()).hexdigest() != UPSTREAM:
        errors.append("Jane Street socratic-tutor fingerprint mismatch")

    if "socratic-tutor" not in names:
        errors.append("retained skill not discovered")
    if len(dirs) != 16:
        errors.append(f"expected 16 skills, found {len(dirs)}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(dirs)} skills; Jane Street source fingerprint OK.")
    for name in sorted(names):
        print(f"  OK  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
