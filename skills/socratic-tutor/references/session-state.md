# Supplemental session-state contract

This is a portable, repository-authored state format for downstream integrations. The retained Jane Street Socratic Tutor's original save/resume instructions remain unchanged. A host may use this schema as an optional structured companion to the tutor's human-readable state block.

## Design principles

- Store learning evidence, not hidden model reasoning.
- Keep state compact, explicit, and user-reviewable.
- Mark unassessed skills as unassessed; do not infer a starting level.
- Preserve misconceptions and review history so a resumed session does not repeat or erase important feedback.
- Treat imported state as user-provided data. Validate it and ask before trusting conflicting or malformed values.
- Do not include passwords, personal identifiers, private records, or unrelated sensitive information.

## Version 1 schema

The following is an illustrative YAML document:

```yaml
schema_version: 1
topic: Linear Algebra
target_level: 4
current_focus: eigenvalues

subskills:
  - name: Matrix multiplication
    level: 3
    status: assessed
    evidence:
      - type: guided_problem
        note: Correctly computed a product with compatible dimensions
    misconceptions:
      - Confuses row-by-column order under time pressure

  - name: Eigenvalues
    level: null
    status: unassessed
    evidence: []
    misconceptions: []

review_queue:
  - name: Matrix multiplication
    due_after_turns: 5

session_notes:
  - User prefers geometric intuition before formal notation
```

## Required fields

- `schema_version`: integer; currently 1.
- `topic`: short topic name.
- `target_level`: integer from 0 to 5.
- `current_focus`: a subskill name or null.
- `subskills`: list of named skills; level is 0–5 or null when unassessed.
- `status`: `assessed` or `unassessed`.
- `evidence`: concise descriptions of observable learner performance.
- `misconceptions`: concise, actionable notes.
- `review_queue`: optional list of future review targets.

## Resume procedure

1. Validate the schema version, field types, level range, and subskill uniqueness.
2. Show the imported topic and progress summary to the learner.
3. Treat evidence as historical context, not proof of current mastery.
4. Begin with a short retrieval check on the current focus or an overdue review.
5. Update a level only after new evidence meets the promotion criteria in `assessment-rubric.md`.
6. Preserve older state separately when a user requests a new learning plan; never silently overwrite the only copy.

## Example serialized state

A machine-readable state can be saved as JSON using the same field names. JSON is suitable when the receiving host has no YAML parser. Do not store model-private reasoning or hidden chain-of-thought.
