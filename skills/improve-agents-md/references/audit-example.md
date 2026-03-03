# Audit Example: Backend API Service

A worked example showing how to audit a bloated AGENTS.md into a clean root file plus scoped sub-files. Read this when performing an audit to understand the expected workflow and output format.

The example uses a generic backend service. The same principles apply regardless of language or framework.

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

- Total: 62 lines
- Distinct instructions: ~33
- Style rules: 6 (indentation, async/await, exports, doc comments, casing, import order)
- Inferrable commands: 6 (install, dev, build, start, lint, format)
- Directory tree: 12 lines

## Step 2: Classify

| Instruction | Classification | Action |
|---|---|---|
| Project description (lines 1-3) | Essential | Keep |
| Directory tree (12 lines) | Anti-pattern: Deep tree | Remove, replace with sentence |
| install, dev, build, start | Inferrable commands | Remove |
| lint, format | Inferrable commands | Remove |
| test, test:unit, test:integration | Partially inferrable | Keep `test:integration` (requires Docker) |
| db:migrate, db:seed | Non-obvious commands | Keep |
| All 6 code style rules | Style/lint rules | Remove (enforce via linter config) |
| API conventions (9 lines) | Correct, scoped to controllers | Move to path-scoped rule |
| Testing conventions (5 lines) | Correct, scoped to tests | Move to path-scoped rule |
| Event handling (5 lines) | Correct, scoped to events | Move to path-scoped rule |

## Step 3: Relocate, then rewrite

### After: Root AGENTS.md (20 lines)

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
- Events must be idempotent — consumers may receive duplicates.

For API design, testing, and event patterns: see scoped rules.
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

## Step 5: Results Summary

| Metric | Before | After (root) | After (total) |
|---|---|---|---|
| Root file lines | 62 | 20 | — |
| Total lines across all files | 62 | 20 + 14 + 10 + 10 = 54 | 54 |
| Style/lint rules | 6 | 0 | 0 |
| Inferrable commands | 6 | 0 | 0 |
| Information lost | — | 0 instructions | 0 instructions |

Every correct instruction from the original is present in the output. The 6 style rules were removed (enforce via linter config). The 6 inferrable commands were removed. The directory tree was replaced with a one-line architecture summary. Scoped content was moved to rules that only load when the agent touches relevant files.
