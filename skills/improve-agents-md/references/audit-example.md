# Audit Example: Node.js API Service

A worked example showing how to audit a bloated AGENTS.md into a clean root file plus scoped sub-files. Read this when performing an audit to understand the expected workflow and output format.

## Before: Original AGENTS.md (68 lines)

```markdown
# Order Service API

REST API for order management. Built with Node.js, Express, TypeScript.
Uses PostgreSQL with Prisma ORM. Redis for caching. RabbitMQ for events.

## Directory Structure

src/
  controllers/     # Route handlers
  services/        # Business logic
  repositories/    # Data access
  middleware/       # Auth, validation, error handling
  events/          # RabbitMQ producers and consumers
  utils/           # Shared helpers
  types/           # TypeScript interfaces
tests/
  unit/
  integration/
prisma/
  schema.prisma
  migrations/

## Development

npm install
npm run dev          # Start dev server with hot reload
npm run build        # Compile TypeScript
npm run start        # Start production server
npm run lint         # ESLint
npm run format       # Prettier
npm run test         # Run all tests
npm run test:unit    # Unit tests only
npm run test:int     # Integration tests (requires Docker)
npm run db:migrate   # Run Prisma migrations
npm run db:seed      # Seed test data
npm run db:studio    # Open Prisma Studio

## Code Style

- Use 2-space indentation
- Prefer async/await over .then() chains
- Use named exports, not default exports
- Always add JSDoc comments to public functions
- Use PascalCase for types and interfaces
- Use camelCase for variables and functions
- Imports ordered: node builtins, external, internal, types

## API Conventions

- All endpoints under /api/v1/
- Use kebab-case for URL paths
- Return { data, meta } wrapper for list endpoints
- Return { data } wrapper for single item endpoints
- Errors return { error: { code, message, details } }
- Always validate request body with zod schemas
- Include X-Request-Id header in all responses
- Rate limit: 100 req/min per API key
- Pagination: cursor-based, max 100 items per page

## Testing

- Unit tests: mock repositories, test service logic
- Integration tests: use testcontainers for Postgres and Redis
- Name test files: *.test.ts next to source files
- Factories in tests/factories/ for test data
- Coverage threshold: 80% lines, 90% branches for services/

## Event Handling

- All events published to RabbitMQ with JSON schema
- Event names: domain.entity.action (e.g. order.payment.completed)
- Consumer retry: 3 attempts with exponential backoff
- Dead letter queue for failed messages
- Events must be idempotent — consumers may receive duplicates
```

## Step 1: Measure

- Total: 68 lines
- Distinct instructions: ~35
- Style rules: 7 (indentation, async/await, exports, JSDoc, casing x2, import order)
- Inferrable commands: 6 (install, dev, build, start, lint, format)
- Directory tree: 14 lines

## Step 2: Classify

| Instruction | Classification | Action |
|---|---|---|
| Project description (line 1-2) | Essential | Keep |
| Stack (line 3) | Essential | Keep |
| Directory tree (14 lines) | Anti-pattern: Deep tree | Remove, replace with sentence |
| `npm install`, `dev`, `build`, `start` | Inferrable commands | Remove |
| `npm run lint`, `format` | Inferrable commands | Remove |
| `npm run test`, `test:unit`, `test:int` | Partially inferrable | Keep `test:int` (requires Docker) |
| `db:migrate`, `db:seed`, `db:studio` | Non-obvious commands | Keep |
| All 7 code style rules | Style/lint rules | Remove (use ESLint + Prettier) |
| API conventions (10 lines) | Correct, scoped to `src/controllers/` | Move to path-scoped rule |
| Testing conventions (5 lines) | Correct, scoped to `tests/` | Move to path-scoped rule |
| Event handling (5 lines) | Correct, scoped to `src/events/` | Move to path-scoped rule |

## Step 3: Relocate, then rewrite

### After: Root AGENTS.md (22 lines)

```markdown
# Order Service API

REST API for order management. Node.js + Express + TypeScript.
PostgreSQL (Prisma ORM), Redis (caching), RabbitMQ (events).
Layered architecture: controllers → services → repositories.

## Development

npm run test:int     # Integration tests — requires Docker running
npm run db:migrate   # Run Prisma migrations
npm run db:seed      # Seed test data
npm run db:studio    # Open Prisma Studio

Typecheck with `npx tsc --noEmit`, lint with `npm run lint` before finishing.

## Conventions

- Named exports only, no default exports.
- Request validation: zod schemas for all endpoints.
- Events must be idempotent — consumers may receive duplicates.

For API design, testing, and event patterns: see `.claude/rules/`.
```

### New: `.claude/rules/api-conventions.md`

```markdown
---
paths:
  - "src/controllers/**/*.ts"
  - "src/middleware/**/*.ts"
---

# API Conventions

- All endpoints under /api/v1/
- Use kebab-case for URL paths
- Return { data, meta } wrapper for list endpoints
- Return { data } wrapper for single item endpoints
- Errors return { error: { code, message, details } }
- Always validate request body with zod schemas
- Include X-Request-Id header in all responses
- Rate limit: 100 req/min per API key
- Pagination: cursor-based, max 100 items per page
```

### New: `.claude/rules/testing.md`

```markdown
---
paths:
  - "tests/**/*.ts"
  - "src/**/*.test.ts"
---

# Testing Conventions

- Unit tests: mock repositories, test service logic
- Integration tests: use testcontainers for Postgres and Redis
- Name test files: *.test.ts next to source files
- Factories in tests/factories/ for test data
- Coverage threshold: 80% lines, 90% branches for services/
```

### New: `.claude/rules/events.md`

```markdown
---
paths:
  - "src/events/**/*.ts"
---

# Event Handling

- All events published to RabbitMQ with JSON schema
- Event names: domain.entity.action (e.g. order.payment.completed)
- Consumer retry: 3 attempts with exponential backoff
- Dead letter queue for failed messages
- Events must be idempotent — consumers may receive duplicates
```

## Step 5: Results Summary

| Metric | Before | After (root) | After (total) |
|---|---|---|---|
| Root file lines | 68 | 22 | — |
| Total lines across all files | 68 | 22 + 14 + 10 + 10 = 56 | 56 |
| Style/lint rules | 7 | 0 | 0 |
| Inferrable commands | 6 | 0 | 0 |
| Information lost | — | 0 instructions | 0 instructions |

Every correct instruction from the original is present in the output. The 7 style rules were removed (enforce via ESLint/Prettier config). The 6 inferrable commands were removed. The directory tree was replaced with a one-line architecture summary. Scoped content was moved to path-scoped rules that only load when the agent touches relevant files.
