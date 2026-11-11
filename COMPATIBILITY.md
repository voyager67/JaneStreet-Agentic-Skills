# Compatibility and installation

The repository uses the portable Agent Skills directory format. Each package lives under `skills/<skill-name>/` and contains a `SKILL.md` manifest plus optional references, examples, and host metadata. Skill content is model- and vendor-neutral; discovery paths are host-specific.

## Codex

Install all skills into the current repository:

```bash
python3 scripts/install_skills.py --agent codex --scope project
```

Install into the current user's Codex skills directory:

```bash
python3 scripts/install_skills.py --agent codex --scope user
```

Codex repository skills are installed under `.agents/skills/`; user skills are installed under `~/.agents/skills/`. Start a new Codex session after installation.

## Claude Code

Install all skills into the current repository:

```bash
python3 scripts/install_skills.py --agent claude-code --scope project
```

Install into the current user's Claude Code skills directory:

```bash
python3 scripts/install_skills.py --agent claude-code --scope user
```

The installer uses `.claude/skills/` for project scope and `~/.claude/skills/` for user scope. Start a new Claude Code session after installation.

## Other Agent Skills-compatible hosts

Copy the selected skill directory, including its `SKILL.md` and companion files, into the skill-discovery directory documented by that host:

```bash
python3 scripts/install_skills.py --agent custom --destination /path/to/your/skills --skills market-making,quant-research-validation
```

Use `--dry-run` to preview the operation. Existing destination skills are never overwritten unless `--force` is passed. With `--force`, only the selected destination skill directories are replaced.

## OpenAI surfaces

Each skill includes optional `agents/openai.yaml` metadata with a display name, short description, and suggested prompt. Hosts that do not support this metadata can ignore it. It does not add tools, credentials, market data, or exchange access.

## Compatibility limits

- The core `SKILL.md` format is portable; implicit activation quality depends on the host and model.
- UI metadata is optional and may be ignored by hosts that do not implement it.
- The installer copies skill directories only. It does not install packages, configure APIs, connect to venues, provide data entitlements, or enable live trading.
- A host may impose limits on skill count, description length, tools, or file access. Validate installed skills with the target host before relying on them.
