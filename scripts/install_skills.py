#!/usr/bin/env python3
"""Install selected Agent Skills into Codex, Claude Code, or a custom directory."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
TARGETS = {
    "codex": {
        "project": Path(".agents/skills"),
        "user": Path.home() / ".agents" / "skills",
    },
    "claude-code": {
        "project": Path(".claude/skills"),
        "user": Path.home() / ".claude" / "skills",
    },
}


def available_skills() -> dict[str, Path]:
    return {
        path.name: path for path in sorted(SKILLS_ROOT.iterdir())
        if path.is_dir() and (path / "SKILL.md").is_file()
    }


def install(names: list[str], destination: Path, *, dry_run: bool = False, force: bool = False) -> list[Path]:
    skills = available_skills()
    unknown = sorted(set(names) - set(skills))
    if unknown:
        raise ValueError(f"unknown skill(s): {', '.join(unknown)}")
    if len(names) != len(set(names)):
        raise ValueError("duplicate skill names were selected")
    destination = destination.expanduser()
    targets = [destination / name for name in names]
    conflicts = [target for target in targets if target.exists() or target.is_symlink()]
    if conflicts and not force:
        formatted = ", ".join(str(path) for path in conflicts)
        raise FileExistsError(f"target skill already exists: {formatted}. Use --force to replace selected skill directories.")

    for name, target in zip(names, targets):
        source = skills[name]
        if dry_run:
            print(f"Would install {name}: {source} -> {target}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink():
            target.unlink()
        elif target.exists() and force:
            shutil.rmtree(target)
        shutil.copytree(source, target)
        print(f"Installed {name}: {target}")
    return targets


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=("codex", "claude-code", "custom"), required=True)
    parser.add_argument("--scope", choices=("project", "user"), default="project")
    parser.add_argument("--destination", help="required with --agent custom")
    parser.add_argument("--skills", help="comma-separated skill names; defaults to all skills")
    parser.add_argument("--dry-run", action="store_true", help="preview without copying files")
    parser.add_argument("--force", action="store_true", help="replace only selected destination skill directories")
    args = parser.parse_args(argv)

    try:
        if args.agent == "custom":
            if not args.destination:
                raise ValueError("--destination is required with --agent custom")
            destination = Path(args.destination)
        else:
            if args.destination:
                raise ValueError("--destination is only valid with --agent custom")
            relative = TARGETS[args.agent][args.scope]
            destination = ROOT / relative if args.scope == "project" else relative

        names = ([value.strip() for value in args.skills.split(",") if value.strip()]
                 if args.skills else sorted(available_skills()))
        if not names:
            raise ValueError("no skills selected")
        install(names, destination, dry_run=args.dry_run, force=args.force)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
