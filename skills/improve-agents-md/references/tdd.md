# Test-Driven Development

TDD principles for writing better testing guidance in agent context files, and for applying TDD when the agent works on code.

## For AGENTS.md Authors

Testing instructions in agent context files fall into three categories:

**Keep in root file** — universal testing conventions that apply to every task:
- Which test runner and command to use (if non-obvious)
- What to run before finishing (`npm run test:int` requires Docker, not just `npm test`)
- Critical invariants ("never remove or weaken existing tests")

**Move to scoped rule** — conventions specific to a test directory or file pattern:
- Unit vs integration test boundaries
- Factory/fixture patterns and locations
- Coverage thresholds per module
- Test naming conventions

**Remove** — things a linter or the framework already enforces:
- "Use `describe`/`it` blocks" (framework default)
- "Name test files `*.test.ts`" (configurable in test runner)
- "Import `expect` from..." (auto-import or framework global)

Example of a good testing section in a root AGENTS.md:

```markdown
## Testing

npm run test:int     # Integration tests — requires Docker
npm run test:unit    # Fast unit tests, no external deps

Run test:unit before finishing. Run test:int if you changed API routes or DB queries.
Tests must verify behavior through public interfaces, not implementation details.
Never remove or weaken existing tests without explicit approval.
```

## TDD Workflow: Red-Green-Refactor

### Vertical Slices, Not Horizontal

Write one test, make it pass, repeat. Each cycle responds to what you learned from the previous one.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

Writing all tests first ("horizontal slicing") produces tests that verify imagined behavior rather than actual behavior. Tests written in bulk tend to test the shape of data structures and function signatures rather than user-facing outcomes.

### The Loop

1. **RED** — Write one test for one behavior. It must fail.
2. **GREEN** — Write the minimum code to make it pass.
3. **REFACTOR** — Clean up while all tests stay green. Never refactor while RED.

Start with a tracer bullet: one test that proves the path works end-to-end through the public interface.

### Checklist Per Cycle

- Test describes behavior, not implementation
- Test uses public interface only
- Test would survive an internal refactor
- Code is minimal for this test
- No speculative features added

## Good vs Bad Tests

**Good tests** are integration-style: they exercise real code paths through public APIs and describe *what* the system does, not *how*.

```typescript
// GOOD: Tests observable behavior through the interface
test("created user is retrievable by id", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**Bad tests** are coupled to implementation. The warning sign: the test breaks when you refactor, but behavior hasn't changed.

```typescript
// BAD: Tests implementation detail (which service gets called)
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});

// BAD: Bypasses the interface to verify via database
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});
```

Red flags in tests:
- Mocking internal collaborators
- Testing private methods
- Asserting on call counts or call order
- Test name describes HOW rather than WHAT
- Verifying through external means instead of the interface

## Mocking Boundaries

Mock at **system boundaries** only:
- External APIs (payment, email, third-party services)
- Databases (prefer a test DB when possible)
- Time, randomness, file system

Do not mock your own modules or internal collaborators. If you control the code, use the real implementation.

**Design for mockability at boundaries** using dependency injection:

```typescript
// Testable: dependency passed in
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to test: dependency created internally
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

Prefer SDK-style interfaces over generic fetchers — each function is independently mockable with a specific return shape.

## Interface Design for Testability

Three principles that make code naturally testable:

1. **Accept dependencies, don't create them.** Pass external services in as parameters.
2. **Return results, don't produce side effects.** A function that returns a value is easier to test than one that mutates state.
3. **Small surface area.** Fewer public methods = fewer tests needed. Aim for deep modules: small interface hiding complex implementation.

## Refactor Phase

After all tests pass, look for:

- **Duplication** — extract shared logic into helpers
- **Long methods** — break into private helpers (keep tests on the public interface)
- **Shallow modules** — combine or deepen (small interface, rich implementation)
- **Feature envy** — move logic to where the data lives
- **Primitive obsession** — introduce value objects
- **What new code reveals** about problems in existing code

Never refactor while RED. Get to GREEN first, then clean up.
