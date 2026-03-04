---
name: python-best-practices
description: >
  Comprehensive Python expertise covering language fundamentals, idiomatic patterns, software design
  principles, and production best practices. Use when writing, reviewing, debugging, or refactoring
  Python code. Triggers: Python, .py files, pip, uv, pytest, dataclasses, asyncio, type hints, or
  any Python library.
---

# Python Best Practices

## How to use this skill

Read **SKILL.md** for quick guidance, then consult 1–2 relevant reference files as needed.
**Do NOT read all reference files at once.** For simple tasks, the quick principles below may suffice.

### Reference files — when to read each one

| Reference | Read when... |
|-----------|-------------|
| `references/pythonic-idioms.md` | Writing any Python. PEP 8, unpacking, comprehensions, walrus operator, match, regex, anti-patterns. |
| `references/data-structures.md` | Lists, tuples, dicts, sets, containers, dates/times, file I/O, pathlib, JSON/CSV/TOML/YAML, databases. |
| `references/functions-and-generators.md` | Functions, closures, decorators, generators, comprehensions, recursion, memoization, backtracking. |
| `references/classes-and-design.md` | Class design, dataclasses, properties, inheritance, composition, protocols, contracts, iterative design. |
| `references/design-patterns.md` | Template Method, Strategy, Factory, Observer, State, Adapter, Facade, Composite, Decorator, etc. |
| `references/error-handling.md` | try/except/else/finally, custom exception hierarchies, context managers, assertions, chaining. |
| `references/concurrency.md` | GIL, threading, asyncio, multiprocessing, subprocess, synchronization, migration patterns. |
| `references/testing-and-quality.md` | Testing, mocking, type hints, debugging, profiling, performance optimization, packaging, web frameworks. |

## Quick principles

1. **Explicit over implicit.** Favor clarity over cleverness. Extract hard-to-read expressions into descriptively named helpers.
2. **Follow PEP 8.** `lowercase_underscore` for functions/variables, `CapitalizedWord` for classes, `ALL_CAPS` for constants. 4-space indent, lines ≤ 79 chars. Use `black` and `ruff`.
3. **Use the right data structure.** Dicts → lookups, sets → membership, lists → ordered sequences, tuples → fixed records, deques → queues, dataclasses → structured data.
4. **Prefer composition over inheritance.** Inherit only for true is-a relationships; otherwise compose or use mix-ins.
5. **Write for the reader.** Code is read far more than written. Use descriptive names, docstrings, type hints, and small focused functions.
6. **Don't repeat yourself.** Extract shared logic, but don't over-abstract — two occurrences may be coincidence, three is a pattern.
7. **Errors should never pass silently.** Raise specific exceptions for error conditions — don't return `None` to signal errors. Returning `None` for "not found" is ambiguous (is it a missing value or an error?); raise `LookupError` or a custom exception instead. Reserve `None` returns for truly optional values, not error states. Catch specific exceptions. Keep try blocks short.
8. **Test your code.** Python defers nearly all checks to runtime. Automated tests are your compiler.
9. **Encapsulate what varies.** Isolate changing parts from stable parts — the foundation of good design.
10. **Iterate toward good design.** Well-designed code rarely emerges in one pass. Write, test, refactor, repeat. Backtracking is normal.
