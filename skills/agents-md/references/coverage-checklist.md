# Coverage Checklist

Use this during repo investigation (between Phase 1 and Phase 2) and again during auditing.

Not every topic applies to every project. A static site needs 3 of these; a distributed microservice system needs most. Use this as an investigation guide, not a mandatory list. For each topic: check if the repo has signals, check if the AGENTS.md system covers it, and present gaps to the user.

**Loading guidance:** Load after Phase 1 answers to guide repo investigation. Use during Phase 2 to structure gap presentation. Use during auditing for the gap analysis step.

---

## 1. Architecture & Design Patterns

**What to look for in the repo:**
- Directory structure signals (e.g., `domain/`, `ports/`, `adapters/`, `infrastructure/` → hexagonal; `contexts/` or per-domain packages → DDD; `controllers/`, `models/`, `views/` → MVC)
- Import direction (do infrastructure files import domain files, or vice versa? Violations signal architectural drift)
- Naming conventions (aggregates, entities, value objects, bounded contexts, use cases, commands, events)
- Existing architecture docs or ADRs

**What to ask the user (Phase 1 Q7):**
"Does your codebase follow a specific architecture pattern? (e.g., DDD, hexagonal, clean architecture, MVC, event-driven, CQRS, layered) — or should I infer it from the code?"

**Conditional follow-ups:**
- Names a specific pattern → "What are the key boundaries or modules? Where does business logic live vs. infrastructure/adapter code?"
- Says DDD → "What are the main bounded contexts? Any aggregates or domain events the agent should know about?"
- Says event-driven → "What's the event bus or message broker? What are the main event types?"
- Says "infer it" → scan for structural signals, then present findings in Phase 2

**What belongs in root:** One sentence naming the pattern + key top-level boundaries. E.g., "Hexagonal architecture. Domain logic in `src/domain/`, ports in `src/ports/`, adapters in `src/adapters/`."

**What belongs in sub-files:** Invariants the agent must respect (e.g., "domain layer must never import from adapters"), bounded context descriptions, module responsibilities, where to add new features of each type.

**Example root entry:**
```markdown
Domain-driven design. Bounded contexts: `orders/`, `payments/`, `catalog/`. Domain logic never imports infrastructure.
```

**Example sub-file entry (e.g., `src/orders/AGENTS.md`):**
```markdown
## Architecture

Orders bounded context. Aggregate root: `Order`. Domain events: `OrderPlaced`, `OrderCancelled`.
Business logic lives in `domain/`. Repository interfaces in `ports/`. Database adapters in `adapters/`.
Never import from `src/payments/` directly — communicate via events only.
```

---

## 2. Performance

**What to look for in the repo:**
- ORM configuration (eager vs. lazy loading defaults, N+1 detection tools like `bullet`)
- Pagination patterns (cursor-based, offset-based, max page sizes in controllers)
- Caching infrastructure (Redis, Memcached, in-memory cache, CDN)
- Batch processing patterns (bulk inserts, queue workers)
- Known performance constraints in comments or docs

**What to ask the user (Phase 1 Q8):**
"Are there specific performance conventions your team follows? (e.g., N+1 query prevention, pagination strategy, caching rules, batch size limits, lazy vs. eager loading)"

**Conditional follow-ups:**
- Mentions ORM/database → "Which ORM? Are there rules about eager vs. lazy loading, or query patterns to avoid?"
- Mentions caching → "What's the caching strategy? (TTL-based, invalidation-based, cache-aside?) Any cache boundaries the agent should respect?"
- Mentions pagination → "What pagination style? (cursor-based, offset-based?) Max page sizes?"

**What belongs in root:** Universal constraints that apply across the codebase. E.g., "All list endpoints must be paginated. No unbounded queries."

**What belongs in sub-files:** ORM-specific query patterns, cache invalidation rules scoped to a domain, batch processing conventions for a specific worker.

**Example root entry:**
```markdown
- All list endpoints paginated (cursor-based, max 100 items). Never return unbounded collections.
- Avoid N+1 queries — always use eager loading when accessing related entities in a loop.
```

**Example sub-file entry:**
```markdown
## Performance

Use `includes(:user, :items)` when fetching orders for display. Avoid calling `.user` inside loops.
Cache product catalog in Redis with 5-minute TTL. Invalidate on `ProductUpdated` events.
Bulk-insert order line items — never insert in a loop.
```

---

## 3. Security

**What to look for in the repo:**
- Auth middleware location and pattern (JWT decode, session validation, OAuth callbacks)
- Authorization checks (role guards, policy objects, permission checks — where do they live?)
- Input validation libraries and where validation happens (controller/handler level, domain level)
- Secrets management (env files, secret manager integrations, any hardcoded credentials to flag)
- CORS configuration
- Rate limiting middleware
- SQL injection protections (parameterized queries, ORM escaping)

**What to ask the user (Phase 1 Q9):**
"Are there security patterns the agent should follow? (e.g., auth/authz approach, input validation strategy, secrets management, CORS policy)"

**Conditional follow-ups:**
- Mentions auth → "What's the auth pattern? (JWT, session-based, OAuth?) Where does authorization logic live?"
- Mentions input validation → "Validation at which layer? (controller/handler level, domain level, both?) Which library?"
- Mentions secrets → "How are secrets managed? (env vars, vault, cloud secrets manager?) Any rules about what must never be hardcoded?"

**What belongs in root:** Universal rules that apply to all code. E.g., "Never hardcode secrets. All inputs validated before reaching domain layer."

**What belongs in sub-files:** Auth/authz patterns scoped to the API layer, security conventions for a specific service or bounded context.

**Example root entry:**
```markdown
- Never hardcode secrets. Use env vars (see `.env.example`).
- Validate all external input before it reaches domain logic.
- Authorization via policy objects in `app/policies/` — never inline permission checks.
```

**Example sub-file entry:**
```markdown
## Security

JWT auth: decode in `middleware/auth.ts`, attach `req.user`. All routes under `/api/` require authentication unless decorated with `@Public()`.
Rate limit: 100 req/min per API key enforced at API gateway. Don't duplicate in service code.
```

---

## 4. Error Handling

**What to look for in the repo:**
- Custom error classes or error type hierarchy
- Global error handlers or middleware
- Error propagation patterns (throw vs. return error objects, Result types, Either monads)
- Retry logic (libraries, manual retry loops, exponential backoff)
- Circuit breakers
- Error logging conventions

**What belongs in root:** Universal error handling strategy. E.g., "Use typed errors. All errors must be logged before re-throwing."

**What belongs in sub-files:** Service-specific retry policies, circuit breaker config for external dependencies, error format for API responses.

**Example root entry:**
```markdown
- Throw typed errors (extend `AppError`). Never throw raw strings.
- Log errors with context before re-throwing across service boundaries.
- External API calls: retry 3 times with exponential backoff via `src/utils/retry.ts`.
```

---

## 5. Data Access

**What to look for in the repo:**
- Repository pattern vs. direct ORM calls
- Transaction boundaries (where transactions start/end)
- Migration tools and conventions (Flyway, Liquibase, Alembic, ActiveRecord migrations)
- Read/write splitting or multiple DB connections
- Soft deletes vs. hard deletes

**What belongs in root:** Key data access rules that affect all code. E.g., "Never call ORM directly from service layer — use repository interfaces."

**What belongs in sub-files:** Transaction patterns for a specific domain, migration naming conventions, replica routing rules.

---

## 6. API Contracts

**What to look for in the repo:**
- Response envelope structure (e.g., `{ data, meta }`, `{ result, error }`)
- Versioning strategy (URL path versioning `/v1/`, header versioning)
- Pagination format in responses
- Error response format
- OpenAPI/Swagger specs

**What belongs in root:** Envelope format and versioning rule (brief). E.g., "All responses use `{ data, meta }` envelope. Errors use `{ error: { code, message } }`."

**What belongs in sub-files:** Full API design conventions for a specific service — URL patterns, specific headers, field naming rules.

---

## 7. Observability

**What to look for in the repo:**
- Logging library and structured logging format
- Trace/span instrumentation (OpenTelemetry, Datadog APM)
- Metrics conventions (what gets measured, naming patterns)
- Log levels usage (`debug`, `info`, `warn`, `error`)

**What belongs in root:** Logging library and key rules. E.g., "Structured logging via `pino`. Always include `requestId` in log context. No `console.log` in production code."

**What belongs in sub-files:** Service-specific metric naming, tracing conventions for a specific integration.

---

## 8. Deployment & Infrastructure

**What to look for in the repo:**
- CI/CD pipeline config (GitHub Actions, Jenkinsfile, etc.)
- Environment differentiation (feature flags, env-specific config)
- Container/orchestration setup (Dockerfile, docker-compose, Kubernetes manifests)
- Secrets injection patterns
- Rollback procedures or feature flag toggles

**What belongs in root:** Only if the agent needs to know deployment facts for code decisions. E.g., "Cold start time is a concern — avoid heavy module-level initialization."

**What belongs in sub-files:** Service-specific deployment notes, environment-specific config rules, CI pipeline conventions.

---

## 9. State Management (frontend)

**What to look for in the repo:**
- State management library (Redux, Zustand, Pinia, MobX, Jotai)
- Server state library (React Query, SWR, Apollo)
- Local vs. server state separation patterns
- Cache invalidation patterns

**What belongs in root:** State library names and key rules. E.g., "Zustand for local UI state. React Query for server state. Never use Redux."

**What belongs in sub-files:** Feature-specific store conventions, query key naming patterns, optimistic update patterns.

---

## 10. Concurrency

**What to look for in the repo:**
- Background job frameworks and queue libraries
- Locking patterns (optimistic locking, advisory locks, mutex usage)
- Idempotency handling (for queues, webhooks, retried requests)
- Async/await vs. callbacks vs. promise chains
- Race condition mitigations

**What belongs in root:** Universal rules. E.g., "All queue consumers must be idempotent. Use idempotency keys for external API calls."

**What belongs in sub-files:** Locking conventions scoped to a specific domain, job processing patterns for a specific worker.

---

## 11. Accessibility (frontend)

**What to look for in the repo:**
- a11y testing tools (axe, jest-axe, Playwright accessibility checks)
- ARIA patterns in components
- Focus management conventions
- Color contrast and design token compliance

**What belongs in root:** "All new components must pass axe audits. Keyboard navigation required for all interactive elements."

**What belongs in sub-files:** Component-library-specific ARIA patterns, design system accessibility conventions.

---

## Gap Presentation Format

After investigating the repo, present what was found and what wasn't. Example:

```
I found documented conventions for: commands, testing, linting.

These topics appear relevant to this repo but aren't covered:

| Topic | Signal found | Suggested action |
|---|---|---|
| Architecture | Layered structure (controllers/services/repos) — pattern not named | Document in root (1 line) + sub-file |
| Performance | Pagination used in controllers — no documented rules | Ask: are there N+1/pagination conventions to document? |
| Security | JWT middleware present — no auth conventions documented | Document auth pattern in API sub-file |
| Error handling | Custom `AppError` class found — no propagation rules | Document in root conventions |

Which of these gaps matter for your project? (add / not needed / handled elsewhere)
```
