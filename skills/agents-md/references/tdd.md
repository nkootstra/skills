# Test-Driven Development

TDD principles for testing guidance in agent context files and for applying TDD during code tasks.

## For AGENTS.md Authors

**Keep in root file** — universal testing conventions:
- Test runner and command (if non-obvious)
- What to run before finishing (e.g. integration tests needing Docker)
- Critical invariants ("never remove or weaken existing tests")

**Move to scoped rule** — conventions specific to a test directory or file pattern:
- Unit vs integration test boundaries
- Factory/fixture patterns and locations
- Coverage thresholds per module
- Test naming conventions

**Remove** — things a linter or framework already enforces:
- Test block structure, file naming patterns, import conventions

Example root AGENTS.md testing section:

```markdown
## Testing

<test:integration>    # Integration tests — requires Docker
<test:unit>           # Fast unit tests, no external deps

Run unit tests before finishing. Run integration tests if you changed API routes or DB queries.
Tests must verify behavior through public interfaces, not implementation details.
Never remove or weaken existing tests without explicit approval.
```

## TDD Workflow: Red-Green-Refactor

### Vertical Slices, Not Horizontal

One test, make it pass, repeat. Each cycle responds to what you learned from the previous one.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

Writing all tests first produces tests that verify imagined behavior rather than actual behavior.

### The Loop

1. **RED** — Write one test for one behavior. It must fail.
2. **GREEN** — Write minimum code to pass.
3. **REFACTOR** — Clean up while all tests stay green. Never refactor while RED.

Start w/ a tracer bullet: one test proving the path works end-to-end through the public interface.

### Checklist Per Cycle

- Test describes behavior, not implementation
- Test uses public interface only
- Test would survive an internal refactor
- Code is minimal for this test
- No speculative features added

## Good vs Bad Tests

**Good tests** exercise real code paths through public APIs and describe *what* the system does, not *how*.

```
// GOOD: Tests observable behavior through the interface
test "created user is retrievable by id":
  user = createUser(name: "Alice")
  retrieved = getUser(user.id)
  assert retrieved.name == "Alice"
```

**Bad tests** are coupled to implementation — they break when you refactor, but behavior hasn't changed.

```
// BAD: Tests implementation detail (which service gets called)
test "checkout calls paymentService.process":
  mockPayment = mock(paymentService)
  checkout(cart, payment)
  assert mockPayment.process was called with cart.total

// BAD: Bypasses the interface to verify via database
test "createUser saves to database":
  createUser(name: "Alice")
  row = db.query("SELECT * FROM users WHERE name = ?", ["Alice"])
  assert row exists
```

**Red flags:** mocking internal collaborators, testing private methods, asserting on call counts/order, test name describes HOW not WHAT, verifying through external means instead of the interface.

## Test-First Bug Fixing

When a bug is reported, don't start by trying to fix it. Start by proving it.

### The Workflow

1. **Reproduce** — Write a test that fails because of the reported bug. The test describes the *expected* behavior. If you can't write a failing test, you don't understand the bug yet.
2. **Fix** — Use subagents to attempt fixes in parallel. Each candidate fix is validated against the failing test. A fix is only accepted when the new test passes *and* all existing tests remain green.
3. **Verify** — Review the passing fix. Confirm it addresses root cause, not symptoms.

```
BUG REPORTED
  → Write failing test (RED)
  → Spawn subagents with candidate fixes
  → Each subagent runs full test suite
  → Accept first fix where all tests pass (GREEN)
  → Refactor if needed
```

### Why Test First

- **Proves the bug exists** — no guessing, no "works on my machine"
- **Defines "done"** — the fix is complete when the test passes
- **Prevents regressions** — the test stays in the suite permanently
- **Enables parallel fix attempts** — subagents can independently try different approaches, each validated by the same objective criterion

### Example AGENTS.md Section

When the user selects test-first bug workflow, include this in the generated AGENTS.md:

```markdown
## Bug Fixes

When fixing a bug, write a failing test that reproduces it before attempting a fix.
Use subagents to try candidate fixes in parallel — accept the first that passes
all tests (new + existing). Never skip the reproducing test.
```

## Mocking Boundaries

Mock at **system boundaries** only: external APIs, databases (prefer test DB when possible), time, randomness, file system. Do not mock your own modules or internal collaborators.

**Design for mockability** via dependency injection:

```
// Testable: dependency passed in
function processPayment(order, paymentClient):
  return paymentClient.charge(order.total)

// Hard to test: dependency created internally
function processPayment(order):
  client = new PaymentClient(env.API_KEY)
  return client.charge(order.total)
```

Prefer SDK-style interfaces over generic fetchers — each function is independently mockable w/ a specific return shape.

## Interface Design for Testability

1. **Accept dependencies, don't create them.** Pass external services as parameters.
2. **Return results, don't produce side effects.** Returning values is easier to test than mutating state.
3. **Small surface area.** Fewer public methods = fewer tests. Aim for deep modules: small interface hiding complex implementation.

## Refactor Phase

After all tests pass, look for:
- **Duplication** — extract shared logic into helpers
- **Long methods** — break into private helpers (keep tests on public interface)
- **Shallow modules** — combine or deepen (small interface, rich implementation)
- **Feature envy** — move logic to where the data lives
- **Primitive obsession** — introduce value objects
- **What new code reveals** about problems in existing code

Never refactor while RED. Get to GREEN first.
