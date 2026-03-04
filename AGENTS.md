# Skills

AI agent skills repository. Each skill lives in `skills/<name>/` with a `SKILL.md` entry point and optional `references/` directory.

## Development

- When renaming, adding, or removing a skill, update the table in `README.md` to match.
- No local build, test, or lint commands. CI runs `skill-lint` on PRs touching `skills/**` or `.skill-lint.yml`.

## Skill Structure

- Each `SKILL.md` follows this order: YAML frontmatter → intro → references routing table → core content.
- YAML frontmatter has exactly two fields: `name` (kebab-case, must match directory name) and `description` (include trigger phrases for skill loader matching).
- Progressive-disclosure pattern: lean `SKILL.md` as workflow hub, deep content in `references/`.
- References routing table uses a "When…" / "Read" column pair. Always include "do not load all references at once."
- Reference files: lowercase kebab-case `.md` in `references/`.

## Naming

- Skill directories are lowercase kebab-case noun-phrases. Avoid verb-object names.

## Conventions

- Skills are instructional markdown only — no executable code.
- Reference files are loaded on demand — routing tables tell the agent when to read each one.
- Frontmatter `description` fields are consumed by the skill loader for trigger matching. Keep them precise and include explicit trigger phrases.
