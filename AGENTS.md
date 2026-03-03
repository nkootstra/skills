# Skills

AI agent skills repository. Each skill lives in `skills/<name>/` with a `SKILL.md` entry point and optional `references/` directory.

## Development

When renaming, adding, or removing a skill, update the table in `README.md` to match. The table lists each skill's directory name and the `description` field from its YAML frontmatter.

## Conventions

- Each skill follows the progressive-disclosure pattern: lean `SKILL.md` (workflow hub + routing table) with deep content in `references/`.
- Skill names are noun-phrases: `code-complexity-audit`, `compact-markdown`, `python-best-practices`. Avoid verb-object names.
- Reference files are loaded on demand — `SKILL.md` routing tables tell the agent when to read each one.
- YAML frontmatter `description` fields are consumed by the skill loader for trigger matching. Keep them precise.
