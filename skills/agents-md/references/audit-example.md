# Audit Example: Backend API Service

Worked example: audit a bloated AGENTS.md into a clean root file plus scoped sub-files. Generic backend service; same principles apply regardless of language or framework.

## Before: Original AGENTS.md (62 lines)

```markdown
# Order Service API

REST API for order management. Layered architecture with controllers,
services, and repositories. Uses a relational DB with an ORM, a cache
layer, and a message queue for async events.

## Directory Structure

src/
  controllers/     # Route handlers
  services/        # Business logic
  repositories/    # Data access
  middleware/       # Auth, validation, error handling
  events/          # Message queue producers and consumers
  utils/           # Shared helpers
  types/           # Type definitions
tests/
  unit/
  integration/

## Development

<install>             # Install dependencies
<dev>                 # Start dev server with hot reload
<build>               # Compile / bundle
<start>               # Start production server
<lint>                # Run linter
<format>              # Run formatter
<test>                # Run all tests
<test:unit>           # Unit tests only
<test:integration>    # Integration tests (requires Docker)
<db:migrate>          # Run database migrations
<db:seed>             # Seed test data

## Code Style

- Use consistent indentation
- Prefer async/await over callback chains
- Use named exports, not default exports
- Always add doc comments to public functions
- PascalCase for types, camelCase for variables
- Imports ordered: stdlib, external, internal, types

## API Conventions

- All endpoints under /api/v1/
- Use kebab-case for URL paths
- Return { data, meta } wrapper for list endpoints
- Return { data } wrapper for single item endpoints
- Errors return { error: { code, message, details } }
- Validate all request bodies with a schema library
- Include X-Request-Id header in all responses
- Rate limit: 100 req/min per API key
- Pagination: cursor-based, max 100 items per page

## Testing

- Unit tests: mock repositories, test service logic
- Integration tests: use containerized DB and cache
- Name test files next to source files
- Factories in tests/factories/ for test data
- Coverage threshold: 80% lines, 90% branches for services/

## Event Handling

- All events published with a JSON schema
- Event names: domain.entity.action (e.g. order.payment.completed)
- Consumer retry: 3 attempts with exponential backoff
- Dead letter queue for failed messages
- Events must be idempotent — consumers may receive duplicates
```

## Step 1: Measure

- 62 lines, ~33 distinct instructions
- 6 style rules, 6 inferrable commands, 12-line directory tree

## Step 2: Classify

| Instruction | Classification | Action |
|---|---|---|
| Project description (lines 1-3) | Essential | Keep |
| Directory tree (12 lines) | Anti-pattern: Deep tree | Remove, replace w/ sentence |
| install, dev, build, start | Inferrable | Remove |
| lint, format | Inferrable | Remove |
| test, test:unit, test:integration | Partially inferrable | Keep `test:integration` (requires Docker) |
| db:migrate, db:seed | Non-obvious | Keep |
| 6 code style rules | Style/lint | Remove (enforce via linter) |
| API conventions (9 lines) | Correct, scoped to controllers | Move to path-scoped rule |
| Testing conventions (5 lines) | Correct, scoped to tests | Move to path-scoped rule |
| Event handling (5 lines) | Correct, scoped to events | Move to path-scoped rule |

## Step 3: Gap Analysis

Load `references/coverage-checklist.md` and check each relevant topic against what the repo has and what the AGENTS.md covers.

| Topic | Signal in repo | AGENTS.md covers it? | Suggested action |
|---|---|---|---|
| Architecture | Layered: controllers → services → repositories. Named in description but no boundaries documented. | One sentence (too thin) | Add to root (1 line) + create `src/AGENTS.md` with boundaries |
| Performance | Pagination present in API conventions. No N+1, caching, or batch rules. | Partially (pagination max) | Add N+1 prevention rule; ask if caching conventions exist |
| Security | Rate limiting mentioned. No auth pattern, input validation approach, or secrets rules. | Partially (rate limit) | Ask about auth pattern and validation layer; document or flag |
| Error handling | No custom error classes found. No error propagation rules anywhere. | Not covered | Ask: is there an error handling strategy? Add if so. |
| Data access | ORM present. No migration or transaction boundary conventions documented. | Not covered | Low priority for this example — ask user |
| Observability | No logging library or structured logging conventions visible. | Not covered | Ask user if relevant |

Present to user:

```
I found documented conventions for: API design, testing, event handling.

These topics appear relevant to this repo but aren't covered:

| Topic | Signal found | Suggested action |
|---|---|---|
| Architecture | Layered structure clear — no boundary rules documented | Document in root + src/AGENTS.md |
| Performance | Pagination rules exist — no N+1 prevention or caching docs | Add N+1 rule; ask about caching |
| Security | Rate limiting mentioned — no auth or validation docs | Ask about auth pattern |
| Error handling | No error strategy found | Ask if one exists |

Which of these gaps matter for your project? (add / not needed / handled elsewhere)
```

User responds: architecture + N+1 prevention are important; security and error handling are handled elsewhere and don't need to be in AGENTS.md.

## Step 4: Relocate, then rewrite

### After: Root AGENTS.md (22 lines)

```markdown
# Order Service API

REST API for order management. Layered architecture:
controllers → services → repositories.
Relational DB (ORM), cache layer, message queue for async events.

## Development

<test:integration>    # Integration tests — requires Docker running
<db:migrate>          # Run database migrations
<db:seed>             # Seed test data

Run linter and typechecker before finishing.

## Conventions

- Named exports only, no default exports.
- Validate all request bodies with a schema library.
- Avoid N+1 queries — always use eager loading when fetching related entities in a loop.
- Events must be idempotent — consumers may receive duplicates.

For API design, testing, event patterns, and architecture details: see scoped rules.
```

### New: sub-file for architecture and data access

```markdown
# src/AGENTS.md

Layered architecture. Strict dependency direction: controllers call services; services call repositories. Never call repositories directly from controllers. Never put business logic in controllers.

## Adding new features

- New endpoint → add controller method, service method, repository method in that order.
- Business rules go in services. Data queries go in repositories.
- Repository interfaces in `src/repositories/interfaces/`. Implementations in `src/repositories/`.

## Performance

- Never fetch related entities inside a loop. Use eager loading or batch queries.
- All list endpoints paginated — cursor-based, max 100 items. Use `src/utils/paginate.ts`.
- Cache reads for catalog and user data (Redis, 5-min TTL). Don't cache order state.
```

### New: scoped rule for API conventions

```markdown
---
paths:
  - "src/controllers/**"
  - "src/middleware/**"
---

# API Conventions

- All endpoints under /api/v1/
- Use kebab-case for URL paths
- Return { data, meta } wrapper for list endpoints
- Return { data } wrapper for single item endpoints
- Errors return { error: { code, message, details } }
- Validate all request bodies with a schema library
- Include X-Request-Id header in all responses
- Rate limit: 100 req/min per API key
- Pagination: cursor-based, max 100 items per page
```

### New: scoped rule for testing

```markdown
---
paths:
  - "tests/**"
---

# Testing Conventions

- Unit tests: mock repositories, test service logic
- Integration tests: use containerized DB and cache
- Name test files next to source files
- Factories in tests/factories/ for test data
- Coverage threshold: 80% lines, 90% branches for services/
```

### New: scoped rule for events

```markdown
---
paths:
  - "src/events/**"
---

# Event Handling

- All events published with a JSON schema
- Event names: domain.entity.action (e.g. order.payment.completed)
- Consumer retry: 3 attempts with exponential backoff
- Dead letter queue for failed messages
- Events must be idempotent — consumers may receive duplicates
```

## Step 5: Results

| Metric | Before | After (root) | After (total) |
|---|---|---|---|
| Root lines | 62 | 22 | — |
| Total lines | 62 | — | 80 |
| Style/lint rules | 6 | 0 | 0 |
| Inferrable commands | 6 | 0 | 0 |
| Architecture documented | No | Yes (root + sub) | — |
| Performance rules | No | Yes (root + sub) | — |
| Information lost | — | 0 | 0 |
