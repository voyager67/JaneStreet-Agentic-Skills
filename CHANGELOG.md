# Changelog

All notable changes to this repository are recorded here.

## Unreleased — repository restructure and learning-skill expansion

- Move all 16 existing skill directories under `skills/` without changing any of their `SKILL.md` contents or existing companion-file contents.
- Add mathematical reasoning, code understanding, research-paper tutoring, and technical interview simulation skills.
- Add supplemental assessment-rubric, session-state, and example material beside the retained Socratic Tutor without modifying its original skill instructions.
- Organize behavioral cases under `evals/<skill-name>/cases.yaml` and add the central `evals/test_cases.yaml` manifest.
- Add version roadmap milestones from 0.2.0 to 1.0.0.
- Keep the existing evaluator, installer, structural validation, compatibility guidance, and CI, updated for the new directory layout.
- Rename the CI workflow to `.github/workflows/skill-validation.yml`.
