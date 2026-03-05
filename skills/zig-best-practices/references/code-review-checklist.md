# Code Review Checklist

When reviewing Zig code, work through **three mandatory passes** in order. Do not skip any pass — issues in pass 2 (hardware/concurrency) are frequently missed when reviewers jump straight to style.

## Pass 1 — Memory Safety

1. **Memory leaks** — every `alloc` should have a matching `free` (ideally via `defer`).
2. **Missing `errdefer`** — if a function allocates then can fail later, is the allocation freed on error?
3. **Missing `errdefer` in multi-resource init** — if init acquires A then B, does failure of B clean up A?
4. **Allocator passed through globals** — pass allocators explicitly as parameters.
5. **Heap in hot loops** — could an arena or stack buffer replace per-iteration allocations?
6. **Missing `deinit`** — structs that own resources (HashMap, ArrayList, etc.) must have and call `deinit()`.
7. **Dangling pointers** — slices into freed memory, returning `list.items` after `list.deinit()`.
8. **Reading `undefined` memory** — buffers declared as `undefined` must be written before read.

### Anti-patterns to flag

```zig
// ANTI-PATTERN: global mutable allocator
var global_alloc = std.heap.page_allocator;
// FIX: pass allocator as parameter to every function

// ANTI-PATTERN: missing errdefer
const buf = try allocator.alloc(u8, 1024);
// ... more fallible operations without errdefer ...
// FIX: add errdefer allocator.free(buf); immediately after alloc

// ANTI-PATTERN: no deinit for owned container
var cache = std.StringHashMap([]u8).init(allocator);
// cache is never deinited
// FIX: defer cache.deinit(); or deinit in parent struct's deinit
```

## Pass 2 — Concurrency, Hardware, and Low-Level Safety

9. **Missing volatile on MMIO** — hardware register pointers MUST be `*volatile T`. Without volatile, the compiler may optimize away reads (breaking busy-wait loops) or writes (breaking register sequencing).
10. **Volatile for thread sync** — volatile is for hardware MMIO only. Thread-shared state must use `std.atomic.Value` or `std.Thread.Mutex`.
11. **Struct layout for hardware** — structs overlaying hardware registers or binary protocols need `extern struct` or `packed struct` for guaranteed field ordering.
12. **Raw pointer casts without alignment** — is `@alignCast` used with `@ptrCast`? For byte-to-wider-type casts, prefer `std.mem.readInt` which handles unaligned access safely.
13. **Unchecked integer overflow** — are wrapping operators (`+%`) or saturating operators (`|+`) used intentionally, or should overflow be a bug?
14. **Packed struct field addresses** — you cannot take the address of a non-byte-aligned packed struct field. Use `@bitCast` to convert the whole struct.

### Anti-patterns to flag

```zig
// ANTI-PATTERN: non-volatile hardware read in a loop
const status: *u32 = @ptrFromInt(0x4000_0010);
while (status.* & 0x01 == 0) {} // may be optimized to infinite loop
// FIX: const status: *volatile u32 = @ptrFromInt(0x4000_0010);

// ANTI-PATTERN: volatile used for thread signaling
var flag: bool = false; // or *volatile bool
fn setFlag() void { flag = true; }
// FIX: var flag = std.atomic.Value(bool).init(false);
// fn setFlag() void { flag.store(true, .release); }

// ANTI-PATTERN: @ptrCast without @alignCast
const val: *u32 = @ptrCast(byte_ptr);
// FIX: use std.mem.readInt(u32, bytes[0..4], .little) for unaligned
// OR: const val: *u32 = @ptrCast(@alignCast(byte_ptr)); when alignment is guaranteed

// ANTI-PATTERN: regular struct for hardware register block
const Regs = struct { ctrl: u32, status: u32 }; // field order not guaranteed
// FIX: const Regs = extern struct { ctrl: u32, status: u32 };
```

## Pass 3 — API Design and Completeness

15. **Using `anyerror`** instead of specific error sets — narrow errors help callers.
16. **Using `var` where `const` would work** — default to immutability.
17. **Using `undefined` instead of optionals** — `undefined` is for performance tricks, optionals are for "maybe no value."
18. **Unbuffered I/O** — is file/network I/O wrapped with buffered readers/writers?
19. **Missing doc comments on `pub` functions** — public API should be documented.
20. **Global mutable state** — prefer passing state explicitly through function parameters.
21. **Unsafe optional unwrap** — `cache.?.get(key)` crashes if cache is null. Check for null first or restructure.
22. **Missing exhaustive switch cases** — watch for `else` branches hiding missing cases.
23. **Overly complex comptime** — if compile-time code is hard to follow, it will be hard to maintain.
24. **Monolithic files** — files over 500 lines that mix unrelated concerns should be split.

## Formatting and Style

- **Use `zig fmt`** to format all code. No exceptions.
- 4-space indentation (spaces, not tabs).
- LF line endings, no byte order marks.
- Braces on the same line as the statement.
- `camelCase` for functions/variables, `PascalCase` for types, `UPPER_SNAKE_CASE` for constants, `snake_case.zig` for files.
