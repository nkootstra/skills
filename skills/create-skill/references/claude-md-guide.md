# CLAUDE.md Guide

> **Environment:** CLAUDE.md files are used in Claude Code. On Claude.ai, project-level instructions serve a similar role but are configured differently. The `<important if>` pattern described here applies to Claude Code's CLAUDE.md files.

Sometimes the right answer isn't a skill — it's a better CLAUDE.md. This guide helps you identify when that's the case and how to write an effective CLAUDE.md.

## When to Use CLAUDE.md vs a Skill

**Use CLAUDE.md for:**
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

**The diagnostic question:** Is the user's problem "Claude doesn't follow my project conventions" or "Claude doesn't know how to do this multi-step workflow"? The first is a CLAUDE.md problem. The second is a skill.

If someone says "Claude keeps ignoring my testing conventions" — that's almost certainly a CLAUDE.md issue, not something that needs a skill. If someone says "I want Claude to automate our sprint setup process" — that's a skill.

## The Core Problem

Claude Code injects a system reminder with every CLAUDE.md that says the contents "may or may not be relevant." The longer the file gets, the more Claude treats individual sections as optional — especially sections that don't seem relevant to the current task.

## Solution: `<important if="condition">` Blocks

Wrap conditionally-relevant sections in `<important if="condition">` XML tags. This gives Claude an explicit relevance signal that cuts through the "may or may not be relevant" framing.

```markdown
<important if="you are writing or modifying database queries or models">
- Use the repository layer in `src/repositories/` — never query from route handlers directly
- Wrap mutations in transactions using the context manager in `src/db/session.py`
</important>
```

The explicit condition tells Claude exactly when these instructions matter, rather than leaving it to decide relevance on its own.

## Principles

### 1. Foundational context stays bare, domain guidance gets wrapped

Not everything should be in an `<important if>` block. Context that's relevant to virtually every task — project identity, directory map, tech stack — stays as plain markdown at the top. Domain-specific guidance that only matters for certain tasks gets wrapped.

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

Frontier models can reliably follow a limited number of instructions. Claude Code's system prompt and tools already use many of those. Your CLAUDE.md should be as lean as possible:

- **Cut anything a linter or formatter can enforce.** If ESLint catches it, don't put it in CLAUDE.md. Suggest pre-commit hooks instead.
- **Cut anything the agent can discover from existing code.** LLMs are in-context learners — if your codebase consistently uses a pattern, the agent will follow it after reading a few files.
- **Cut code snippets.** They go stale and bloat the file. Use file path references instead (e.g., "see `src/utils/example.ts` for the pattern").
- **Cut vague instructions.** "Follow best practices" or "leverage the X agent" aren't concrete enough to affect behavior.

### 4. Keep all commands

Don't drop commands during a rewrite. The commands table is foundational reference — the agent needs to know what's available even if some commands are used less frequently.

### 5. Don't shard into separate files unnecessarily

The whole point of `<important if>` blocks is that everything is inline but conditionally weighted — the agent sees it all but only attends to what matches. Don't split into separate files unless the content is genuinely very long or complex.

## Output Structure

When rewriting a CLAUDE.md, produce this structure:

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

## How to Apply

When rewriting an existing CLAUDE.md:

1. **Extract project identity** — a single sentence describing what this is. Leave it bare at the top.
2. **Extract the directory map** — keep bare (no wrapper). This is foundational context.
3. **Extract tech stack** — if present, keep bare near the top. Condense to one or two lines.
4. **Extract commands** — keep ALL commands. Wrap in a single `<important if>` block.
5. **Break apart rules** — split rule lists into individual `<important if>` blocks with specific conditions. Group related rules, but never group unrelated rules under one broad condition.
6. **Wrap domain sections** — testing, API patterns, state management, i18n, etc. each get their own block.
7. **Delete linter territory** — remove style guidelines and formatting rules enforceable by tooling.
8. **Delete code snippets** — replace with file path references.
9. **Delete vague instructions** — remove anything not concrete and actionable.

## Example

**Before:**
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

**After:**
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

**What was removed:** type hints, snake_case/PascalCase, double quotes, docstrings, f-strings, function length limit — all linter/formatter territory (ruff enforces most of these) or patterns Claude will follow from reading the existing code. **What was kept:** the non-obvious conventions Claude can't infer: the repository pattern, the session commit rule, and the specific test fixture names and mock library.`
