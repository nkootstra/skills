# C Interoperability

Zig interoperates with C seamlessly — it can compile C code, link against C libraries, and call C functions.

## Importing C Headers

Use `@cImport` to import C headers:

```zig
const c = @cImport({
    @cInclude("stdio.h");
});
```

## Calling C from Zig

```zig
const c = @cImport({
    @cInclude("stdlib.h");
    @cInclude("string.h");
});

pub fn main() void {
    const ptr = c.malloc(100) orelse @panic("malloc failed");
    defer c.free(ptr);
    _ = c.memset(ptr, 0, 100);
}
```

## Exporting Zig Functions to C

```zig
export fn add(a: c_int, b: c_int) c_int {
    return a + b;
}
```

## extern struct

Use `extern struct` when you need struct layout to match C exactly. Regular Zig structs may have different field ordering:

```zig
const CStruct = extern struct {
    x: c_int,
    y: c_int,
    name: [*c]const u8,
};
```

## C Pointers

Be cautious with `[*c]T` (C pointers). They allow null and pointer arithmetic, losing Zig's safety guarantees. Convert to Zig pointer types as early as possible:

```zig
const c_str: [*c]const u8 = c_function();
const zig_str: [:0]const u8 = std.mem.span(c_str);
```

### C Pointer Coercion Rules

C pointers have special coercion rules:

```zig
const c_ptr: [*c]u8 = c_function();
const optional: ?[*]u8 = c_ptr;     // C ptr to optional
const maybe_single: ?*u8 = c_ptr;   // C ptr to optional single
const null_ptr: [*c]u8 = 0;         // integer 0 to C pointer (null)
```

## String Conversion

```zig
// C string → Zig slice
const c_str: [*:0]const u8 = ...; // null-terminated C string
const zig_str: [:0]const u8 = std.mem.span(c_str);

// Zig slice → C string (must be sentinel-terminated)
const zig_str: [:0]const u8 = "hello";
const c_str: [*c]const u8 = zig_str.ptr;
```

## Sentinel Termination for C APIs

When passing strings to C functions, make sure they're null-terminated (`[:0]const u8`), not just regular slices:

```zig
// This works — string literal is null-terminated
c.puts("hello");

// This may crash — runtime slice may not be null-terminated
const slice: []const u8 = buffer[0..n];
c.puts(slice.ptr); // DANGER: not necessarily null-terminated

// Fix: allocate with sentinel
const c_str = try allocator.allocSentinel(u8, n, 0);
@memcpy(c_str, data);
```

Use sentinel-terminated slices (`[:0]const u8`) when interfacing with C APIs. For pure Zig code, prefer regular slices (`[]const u8`).
