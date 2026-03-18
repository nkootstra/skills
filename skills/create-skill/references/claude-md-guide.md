# Agent Context File Guide

Agent context files give AI coding agents project-level instructions: conventions, commands, directory maps, and constraints. Different tools use different filenames:

| File | Used by |
|------|---------|
| `CLAUDE.md` | Claude Code — injected as a system reminder on every turn |
| `AGENTS.md` | OpenCode, Codex, and other agents that follow the AGENTS.md convention |
| `.cursorrules` | Cursor IDE |
| `CLAUDE.md` (project-level) | Claude.ai projects (similar role, configured differently) |

The writing principles in this guide apply to all of them. Where behavior differs between formats, notes are called out explicitly.

## When to Use an Agent Context File vs a Skill

**Use an agent context file for:**
- Project-wide conventions (import style, naming patterns, directory structure)
- Testing setup and commands
- Tech stack and architecture overview
- API conventions that apply across the codebase
- Anything that should apply to *every* task in this project

**Use a skill for:**
- Reusable multi-step workflows (standup posts, deploy procedures, code scaffolding)
- Processes that need scripts, templates, or reference data
- Workflows that should be shareable across projects or teams
- Complex tasks that benefit from progressive disclosure and bundled resources

**The diagnostic question:** Is the user's problem "Claude doesn't follow my project conventions" or "Claude doesn't know how to do this multi-step workflow"? The first is an agent context file problem. The second is a skill.

If someone says "Claude keeps ignoring my testing conventions" — that's almost certainly a context file issue, not something that needs a skill. If someone says "I want Claude to automate our sprint setup process" — that's a skill.

## The Core Problem

Agents inject context files as system reminders with a caveat like "may or may not be relevant." The longer the file gets, the more the agent treats individual sections as optional — especially sections that don't seem relevant to the current task.

## Solution: `<important if="condition">` Blocks

Wrap conditionally-relevant sections in `<important if="condition">` XML tags. This gives the agent an explicit relevance signal that cuts through the "may or may not be relevant" framing.

```markdown
<important if="you are writing or modifying database queries or models">
- Use the repository layer in `src/repositories/` — never query from route handlers directly
- Wrap mutations in transactions using the context manager in `src/db/session.py`
</important>
```

> **Note:** The `<important if>` pattern is supported in Claude Code's CLAUDE.md. For AGENTS.md and `.cursorrules`, the pattern may not have native support — use clear section headers and concise, unambiguous language instead, and keep the file lean to compensate.

## Principles

### 1. Foundational context stays bare, domain guidance gets wrapped

Context relevant to virtually every task — project identity, directory map, tech stack — stays as plain markdown at the top. Domain-specific guidance that only matters for certain tasks gets wrapped.

**Rule of thumb:** if it's relevant to 90%+ of tasks, leave it bare. If it's relevant to a specific kind of work, wrap it.

### 2. Conditions must be specific and targeted

Bad — overly broad:
```markdown
<important if="you are writing or modifying any code">
- Use the repository pattern
- Write tests
- Handle errors
</important>
```

Good — each rule has its own narrow trigger:
```markdown
<important if="you are writing or modifying database queries or models">
- Use the repository layer in `src/repositories/` — never query from route handlers
- Wrap mutations in transactions — see `src/db/session.py`
</important>

<important if="you are writing or modifying tests">
- Use `db_session` fixture — it rolls back automatically after each test
- Mock external HTTP calls with `respx`, not `unittest.mock`
</important>
```

### 3. Less is more

Frontier models can reliably follow a limited number of instructions. Your context file should be as lean as possible:

- **Cut anything a linter or formatter can enforce.** If ESLint catches it, don't put it in the file. Suggest pre-commit hooks instead.
- **Cut anything the agent can discover from existing code.** If your codebase consistently uses a pattern, the agent will follow it after reading a few files.
- **Cut code snippets.** They go stale and bloat the file. Use file path references instead (e.g., "see `src/utils/example.ts` for the pattern").
- **Cut vague instructions.** "Follow best practices" or "leverage the X agent" aren't concrete enough to affect behavior.

### 4. Keep all commands

Don't drop commands during a rewrite. The commands table is foundational reference — the agent needs to know what's available even if some commands are used less frequently.

### 5. Don't shard into separate files unnecessarily

The whole point of `<important if>` blocks is that everything is inline but conditionally weighted — the agent sees it all but only attends to what matches. Don't split into separate files unless the content is genuinely very long or complex.

### 6. AGENTS.md-specific: use clear section headers

Since `AGENTS.md` doesn't have native support for `<important if>`, compensate with:
- Short, unambiguous section headers (e.g., `## Database`, `## Testing`, `## Deployment`)
- Bullet points over prose — easier to scan
- Keep the entire file under ~100 lines where possible
- Put the most commonly-violated rules first within each section

## Output Structure

When rewriting a `CLAUDE.md` (supports `<important if>`):

```markdown
# CLAUDE.md

[one-line project identity]

## Project map
[directory listing with brief descriptions]

<important if="you need to run commands to build, test, lint, or generate code">
[commands table — ALL commands from the original]
</important>

<important if="<specific trigger for domain area 1>">
[domain guidance]
</important>

<important if="<specific trigger for domain area 2>">
[domain guidance]
</important>
```

When rewriting an `AGENTS.md` or `.cursorrules` (no `<important if>` support):

```markdown
# AGENTS.md

[one-line project identity]

## Project map
[directory listing with brief descriptions]

## Commands
[commands table — ALL commands from the original]

## [Domain area 1]
[concise bullet-point rules]

## [Domain area 2]
[concise bullet-point rules]
```

## How to Apply

When rewriting an existing context file:

1. **Extract project identity** — a single sentence describing what this is. Leave it bare at the top.
2. **Extract the directory map** — keep bare (no wrapper). This is foundational context.
3. **Extract tech stack** — if present, keep bare near the top. Condense to one or two lines.
4. **Extract commands** — keep ALL commands. Wrap in a single `<important if>` block (CLAUDE.md) or a plain `## Commands` section (AGENTS.md).
5. **Break apart rules** — split rule lists into individual `<important if>` blocks with specific conditions (CLAUDE.md), or into clearly-named sections (AGENTS.md). Group related rules, but never group unrelated rules under one broad condition.
6. **Wrap domain sections** — testing, API patterns, state management, i18n, etc. each get their own block.
7. **Delete linter territory** — remove style guidelines and formatting rules enforceable by tooling.
8. **Delete code snippets** — replace with file path references.
9. **Delete vague instructions** — remove anything not concrete and actionable.

## Example

**Before (CLAUDE.md):**
```markdown
# CLAUDE.md

This is a Python FastAPI service with a PostgreSQL database.

## Coding Standards
- Use type hints on all functions
- Use snake_case for variables and functions, PascalCase for classes
- Always use double quotes for strings
- Write docstrings for all public functions
- Keep functions under 40 lines
- Use f-strings instead of .format()

## Database
- Use SQLAlchemy ORM, never raw SQL
- All queries go through the repository layer in `src/repositories/`
- Wrap mutations in transactions — see `src/db/session.py` for the pattern
- Never call `session.commit()` in a route handler directly

## Testing
- Use pytest with the fixtures in `tests/conftest.py`
- Database tests use `db_session` fixture which rolls back after each test
- Mock external HTTP calls with `respx` — see `tests/helpers.py`
- Test file names must match: `test_<module>.py`
```

**After (CLAUDE.md):**
```markdown
# CLAUDE.md

Python FastAPI service with PostgreSQL.

## Project map
- `src/routes/` — API route handlers
- `src/repositories/` — database query layer
- `src/services/` — business logic
- `src/db/` — SQLAlchemy session and base model
- `tests/` — pytest suite with shared fixtures in `conftest.py`

<important if="you need to run commands">

| Command | What it does |
|---|---|
| `make dev` | Start the service with hot reload |
| `make test` | Run the full test suite |
| `make lint` | Run ruff and mypy |
| `make migrate` | Apply pending Alembic migrations |
</important>

<important if="you are writing or modifying database queries or models">
- Use SQLAlchemy ORM, never raw SQL
- All queries go through the repository layer in `src/repositories/`
- Wrap mutations in transactions — see `src/db/session.py` for the session pattern
- Never call `session.commit()` in a route handler — the session context manager handles it
</important>

<important if="you are writing or modifying tests">
- Use pytest with fixtures from `tests/conftest.py`
- Use `db_session` fixture for database tests — it rolls back after each test automatically
- Mock external HTTP calls with `respx` — see `tests/helpers.py` for examples
- Test files must be named `test_<module>.py`
</important>
```

**What was removed:** type hints, snake_case/PascalCase, double quotes, docstrings, f-strings, function length limit — all linter/formatter territory or patterns Claude infers from reading existing code. **What was kept:** the non-obvious conventions Claude can't infer: the repository pattern, the session commit rule, and the specific test fixture names and mock library.

**Same content as AGENTS.md:**
```markdown
# AGENTS.md

Python FastAPI service with PostgreSQL.

## Project map
- `src/routes/` — API route handlers
- `src/repositories/` — database query layer
- `src/services/` — business logic
- `src/db/` — SQLAlchemy session and base model
- `tests/` — pytest suite with shared fixtures in `conftest.py`

## Commands
| Command | What it does |
|---|---|
| `make dev` | Start the service with hot reload |
| `make test` | Run the full test suite |
| `make lint` | Run ruff and mypy |
| `make migrate` | Apply pending Alembic migrations |

## Database
- Use SQLAlchemy ORM, never raw SQL
- All queries go through `src/repositories/` — never from route handlers
- Wrap mutations in transactions — see `src/db/session.py`
- Never call `session.commit()` in a route handler

## Testing
- Use pytest with fixtures from `tests/conftest.py`
- Use `db_session` fixture — rolls back after each test automatically
- Mock external HTTP with `respx` — see `tests/helpers.py`
- Test files must be named `test_<module>.py`
```
