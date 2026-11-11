# Compatibility and installation

The repository uses the portable Agent Skills directory format: each skill is a folder containing a `SKILL.md` manifest and optional supporting files. The skill content is model- and vendor-neutral; discovery paths and optional UI metadata are host-specific.

## Codex

Install all skills into the current repository:

```bash
python3 scripts/install_skills.py --agent codex --scope project
```

Install into the current user's Codex skills directory:

```bash
python3 scripts/install_skills.py --agent codex --scope user
```

Codex repository skills are discovered under `.agents/skills/`; user skills are discovered under `~/.agents/skills/`. Start a new Codex session after installation.

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

Copy the selected skill directory, including its `SKILL.md` and any companion files, into the skill-discovery directory documented by that host:

```bash
python3 scripts/install_skills.py --agent custom --destination /path/to/your/skills --skills market-making,quant-research-validation
```

Use `--dry-run` to preview the operation. The installer refuses to overwrite an existing skill directory unless `--force` is supplied. With `--force`, it replaces only the selected destination skill directories.

## ChatGPT desktop and OpenAI surfaces

Each skill includes an optional `agents/openai.yaml` file with a user-facing name, concise description, and suggested prompt. This metadata is intended for OpenAI surfaces that support the optional Agent Skills metadata. It does not add tools, credentials, market data, or exchange access.

The skill directories can also be packaged or uploaded as standalone skill bundles in environments that support Agent Skills. Follow the host's current UI and packaging instructions; do not assume a Codex or Claude filesystem path is a ChatGPT desktop import path.

## Compatibility limits

- The core `SKILL.md` format is portable; implicit activation quality depends on the host and model.
- UI metadata is optional and may be ignored by hosts that do not implement it.
- The installer copies files only. It does not install Python packages, configure APIs, connect to venues, provide data entitlements, or enable live trading.
- A host may impose additional limits on skill count, description length, tools, or file access. Validate the installed skill with that host before relying on it.
