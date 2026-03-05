# Code Review Checklist

When reviewing Zig code, check for these common issues. Use this as a systematic pass — work through the list top to bottom.

## Memory

1. **Memory leaks** — every `alloc` should have a matching `free` (ideally via `defer`).
2. **Missing `errdefer`** — if a function allocates then can fail later, is the allocation freed on error?
3. **Missing `errdefer` in multi-resource init** — if init acquires A then B, does failure of B clean up A?
4. **Allocator passed through globals** — pass allocators explicitly as parameters.
5. **Heap in hot loops** — could an arena or stack buffer replace per-iteration allocations?

## Error Handling

6. **Ignoring error returns** — `_ = mayFail()` discards errors silently; make sure this is intentional.
7. **Using `anyerror`** instead of specific error sets — narrow errors help callers.

## Types and Safety

8. **Using `var` where `const` would work** — default to immutability.
9. **Using `undefined` instead of optionals** — `undefined` is for performance tricks, optionals are for "maybe no value."
10. **Using volatile for thread sync** — volatile is for hardware MMIO, not thread safety; use atomics or mutexes.
11. **Unchecked integer overflow** — are wrapping operators (`+%`) used intentionally, or should overflow be a bug?
12. **Raw pointer casts without alignment** — is `@alignCast` used with `@ptrCast`? Could `std.mem.readInt` be safer?
13. **Packed struct used unnecessarily** — is bit-level layout actually needed, or would a regular struct perform better?

## Control Flow and Design

14. **Missing exhaustive switch cases** — Zig enforces this, but watch for `else` branches hiding missing cases.
15. **Not using `defer` for cleanup** — pair acquisition with cleanup immediately.
16. **Overly complex comptime** — if compile-time code is hard to follow, it will be hard to maintain.

## Project Quality

17. **Monolithic files** — files over 500 lines that mix unrelated concerns should be split.
18. **Missing doc comments on `pub` functions** — public API should be documented.
19. **Global mutable state** — prefer passing state explicitly through function parameters.
20. **Unbuffered I/O** — is file/network I/O wrapped with buffered readers/writers?

## Formatting and Style

- **Use `zig fmt`** to format all code. No exceptions.
- 4-space indentation (spaces, not tabs).
- LF line endings, no byte order marks.
- Braces on the same line as the statement.
- `camelCase` for functions/variables, `PascalCase` for types, `UPPER_SNAKE_CASE` for constants, `snake_case.zig` for files.
