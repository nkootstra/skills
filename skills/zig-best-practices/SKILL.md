---
name: zig-best-practices
description: "Comprehensive Zig expertise covering allocators, comptime, error handling, build system, C interop, and performance. Use when writing, reviewing, debugging, or refactoring Zig code. Triggers: Zig, .zig files, build.zig, build.zig.zon, zig test, zig build, allocators, comptime, or any Zig-specific concept."
---

# Zig Best Practices

Helps you write, review, and improve idiomatic, safe, and performant Zig code. Adapt depth to the user's level — skip basics for advanced comptime questions, explain fundamentals for allocator newcomers.

## How to use this skill

Read **SKILL.md** for quick guidance, then consult 1-2 relevant reference files as needed.
**Do NOT load all references at once.**

### Reference files — when to read each one

| Reference | Read when... |
|-----------|-------------|
| `references/memory-management.md` | Allocators, alloc/free, defer/errdefer, arena patterns, init/deinit, FixedBufferAllocator, allocation failure testing, custom allocator wrappers. |
| `references/error-handling.md` | Error unions, try/catch, errdefer chains, specific error sets, error return traces, optional handling patterns. |
| `references/comptime-and-generics.md` | Comptime parameters, `@typeInfo`, generic structs, compile-time validation, lookup tables, state machines, `anytype`, fat pointer interfaces, type-level metaprogramming. |
| `references/types-and-pointers.md` | Pointer types (`*T`, `[*]T`, `[]T`, sentinels), type casting (`@ptrCast`, `@alignCast`, `@bitCast`, `@intCast`), packed structs, zero-sized types, integer overflow, type coercion, anonymous structs/tuples, custom formatting, volatile/hardware access. |
| `references/testing-and-build.md` | Inline tests, table-driven tests, `std.testing.allocator`, coverage, `build.zig`, `build.zig.zon`, dependencies, cross-compilation, custom build steps, docs generation, project structure. |
| `references/stdlib-recipes.md` | Data structures (ArrayList, HashMap, LinkedList), file I/O, string handling, networking (HTTP, TCP), concurrency (threads, mutex, thread pool). |
| `references/performance.md` | SIMD/`@Vector`, cache-friendly layout, benchmarking, buffered I/O, arena in hot paths, build modes, comptime lookup tables, stack vs heap. |
| `references/c-interop.md` | `@cImport`, `extern struct`, C pointers, string conversion, exporting Zig to C, sentinel termination for C APIs. |
| `references/code-review-checklist.md` | Reviewing Zig code, code review, PR review, common mistakes to check for, formatting/style rules. |

## Quick principles

1. **Default to `const`.** Only use `var` when you genuinely need mutation.
2. **Pair every allocation with deallocation via `defer`.** Use `errdefer` for cleanup that should only run on error paths.
3. **Pass allocators as explicit parameters.** Functions that allocate accept an `Allocator` — no globals, no hidden heap.
4. **Errors are values.** Use specific error sets, propagate with `try`, handle with `catch`. Never silently discard errors without good reason.
5. **Use optionals (`?T`) for absence, not `undefined`.** Reserve `undefined` for buffers you'll fill immediately.
6. **Prefer slices (`[]T`) over many-item pointers (`[*]T`).** Convert raw pointers to slices as early as possible.
7. **Push work to `comptime` when it makes sense.** But don't overuse `anytype` — if a concrete type works, use it.
8. **Write inline tests with `std.testing.allocator`.** It catches memory leaks automatically.
9. **Run `zig fmt` unconditionally.** No exceptions, no debates.
10. **Profile before optimizing.** Choose the right build mode first — it's the single biggest performance lever.
