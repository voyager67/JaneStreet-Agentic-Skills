# Contributing

Contributions should improve a specific skill or add a focused skill that solves a distinct task.

## Skill format

- Put each skill in `skills/<skill-name>/`.
- Include a `SKILL.md` with YAML frontmatter containing `name` and `description`.
- Use a lowercase kebab-case directory and make the frontmatter name match it.
- Keep instructions specific, actionable, and scoped to the task.
- Add supporting `references/` or `examples/` only when they materially help the skill.
- Add one trigger case and one boundary case under `evals/<skill-name>/cases.yaml`, and update `evals/test_cases.yaml`.

## Quality

- Do not invent sources, benchmarks, capabilities, or results.
- State important assumptions, limitations, and safety boundaries.
- Do not include credentials, private data, or proprietary material.
- Do not imply access to Jane Street's private systems or methods.
- Preserve the original Jane Street Socratic Tutor file and its MIT license.

## Check changes

Run:

```bash
python scripts/validate_skills.py
```

## Licensing

By contributing, you agree that your repository-authored contributions are distributed under Apache-2.0. The retained Jane Street Socratic Tutor remains third-party material under its original MIT license.
