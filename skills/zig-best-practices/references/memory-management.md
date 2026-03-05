# Memory Management

Zig makes every heap allocation explicit through an `Allocator` parameter. There's no `new` keyword, no garbage collector. This gives you complete control over when and where memory is used.

## Choosing the Right Allocator

- **`std.heap.page_allocator`** — Simplest, but slow (asks the OS for whole pages). Good for one-off large allocations.
- **`std.heap.ArenaAllocator`** — Batch allocations, free everything at once. Ideal for request-scoped or phase-scoped work.
- **`std.heap.GeneralPurposeAllocator`** — Balanced safety and performance. Detects double-free and use-after-free in debug mode.
- **`std.heap.FixedBufferAllocator`** — Allocates from a pre-existing buffer, no heap involved. Perfect for embedded or kernel code.
- **`std.testing.allocator`** — Use this in tests; it detects memory leaks.

## Pass Allocators as Parameters

Functions that allocate should accept an `Allocator` parameter rather than using a global. This makes code testable, composable, and clear about where memory comes from.

```zig
fn processData(allocator: std.mem.Allocator, data: []const u8) ![]u8 {
    const result = try allocator.alloc(u8, data.len * 2);
    errdefer allocator.free(result);
    // process...
    return result;
}
```

Use `create`/`destroy` for single items, `alloc`/`free` for slices.

## defer and errdefer

**Always pair allocations with deallocations using `defer`:**

```zig
const buf = try allocator.alloc(u8, 1024);
defer allocator.free(buf);
// use buf...
```

**Use `errdefer` for cleanup on error paths.** When a function allocates and might return an error later, `errdefer` ensures the allocation is freed on failure but kept on success.

```zig
fn init(allocator: Allocator) !Self {
    const data = try allocator.alloc(u8, 1024);
    errdefer allocator.free(data);

    const index = try buildIndex(data);
    errdefer index.deinit();

    return Self{ .data = data, .index = index };
}
```

## Arena Allocator for Scoped Work

When you need to allocate many things during a phase of work and then discard them all at once:

```zig
pub fn processRequest(raw_data: []const u8) !Response {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit(); // frees everything at once

    const allocator = arena.allocator();

    const parsed = try parseRequest(allocator, raw_data);
    const validated = try validate(allocator, parsed);
    const response = try buildResponse(allocator, validated);

    return response;
}
```

Use `arena.reset(.retain_capacity)` in loops to reuse memory without syscalls. See `references/performance.md` for hot-path arena patterns.

## FixedBufferAllocator for Stack-Based Allocation

When you know the maximum memory needed upfront and want to avoid heap allocation entirely:

```zig
var buf: [4096]u8 = undefined;
var fba = std.heap.FixedBufferAllocator.init(&buf);
const allocator = fba.allocator();

const data = try allocator.alloc(u8, 100); // comes from the stack buffer
```

## The init/deinit Pattern

Zig structs that own resources follow a consistent init/deinit pattern:

```zig
const MyResource = struct {
    data: []u8,
    allocator: std.mem.Allocator,

    pub fn init(allocator: std.mem.Allocator, size: usize) !MyResource {
        const data = try allocator.alloc(u8, size);
        return MyResource{
            .data = data,
            .allocator = allocator,
        };
    }

    pub fn deinit(self: *MyResource) void {
        self.allocator.free(self.data);
        self.* = undefined; // Poison the struct to catch use-after-free
    }
};
```

Setting `self.* = undefined` after deinit is a defensive practice — if someone accidentally uses the struct after freeing it, they'll get obviously wrong behavior rather than subtle bugs.

## Testing Allocator for Leak Detection

In tests, always use `std.testing.allocator`. It will fail the test if you leak memory:

```zig
test "list operations don't leak" {
    var list = std.ArrayList(u8).init(std.testing.allocator);
    defer list.deinit();

    try list.append(42);
    try list.append(43);

    try std.testing.expectEqual(@as(usize, 2), list.items.len);
    // If deinit() is missing, the test fails with a leak report
}
```

## Allocation Failure Testing

### std.testing.FailingAllocator

Test that your code handles `OutOfMemory` correctly by using an allocator that fails after N allocations:

```zig
test "handles allocation failure gracefully" {
    var failing = std.testing.FailingAllocator.init(std.testing.allocator, .{
        .fail_index = 3,
    });
    const alloc = failing.allocator();

    const result = myFunction(alloc);
    try std.testing.expectError(error.OutOfMemory, result);
}
```

### Exhaustive Allocation Failure Testing

Test every allocation point by iterating the fail index:

```zig
test "no leaks on any allocation failure" {
    var fail_index: usize = 0;
    while (true) : (fail_index += 1) {
        var failing = std.testing.FailingAllocator.init(std.testing.allocator, .{
            .fail_index = fail_index,
        });
        const alloc = failing.allocator();

        if (myFunction(alloc)) |result| {
            result.deinit();
            break; // all allocations succeeded — we're done
        } else |err| {
            try std.testing.expectEqual(error.OutOfMemory, err);
        }
    }
}
```

## Custom Allocator Wrappers

You can wrap any allocator to add logging, tracking, or arena semantics:

```zig
const TrackingAllocator = struct {
    backing: std.mem.Allocator,
    total_allocated: usize = 0,
    total_freed: usize = 0,
    active_allocations: usize = 0,

    pub fn allocator(self: *TrackingAllocator) std.mem.Allocator {
        return .{
            .ptr = self,
            .vtable = &.{
                .alloc = alloc,
                .resize = resize,
                .free = free,
            },
        };
    }

    fn alloc(ctx: *anyopaque, len: usize, ptr_align: u8, ret_addr: usize) ?[*]u8 {
        const self: *TrackingAllocator = @ptrCast(@alignCast(ctx));
        const result = self.backing.rawAlloc(len, ptr_align, ret_addr);
        if (result != null) {
            self.total_allocated += len;
            self.active_allocations += 1;
        }
        return result;
    }

    fn resize(ctx: *anyopaque, buf: []u8, buf_align: u8, new_len: usize, ret_addr: usize) bool {
        const self: *TrackingAllocator = @ptrCast(@alignCast(ctx));
        return self.backing.rawResize(buf, buf_align, new_len, ret_addr);
    }

    fn free(ctx: *anyopaque, buf: []u8, buf_align: u8, ret_addr: usize) void {
        const self: *TrackingAllocator = @ptrCast(@alignCast(ctx));
        self.total_freed += buf.len;
        self.active_allocations -= 1;
        self.backing.rawFree(buf, buf_align, ret_addr);
    }

    pub fn report(self: *const TrackingAllocator) void {
        std.debug.print(
            "Allocated: {} bytes, Freed: {} bytes, Active: {}\n",
            .{ self.total_allocated, self.total_freed, self.active_allocations },
        );
    }
};
```

## Common Pitfalls

### Dangling Pointers from Slices

Slices don't own their data. If the backing memory is freed, the slice becomes dangling:

```zig
// WRONG: returning a slice into freed memory
fn getTemp(allocator: Allocator) ![]u8 {
    var list = std.ArrayList(u8).init(allocator);
    defer list.deinit(); // frees the backing array!
    try list.appendSlice("hello");
    return list.items; // dangling pointer!
}

// RIGHT: transfer ownership
fn getTemp(allocator: Allocator) ![]u8 {
    var list = std.ArrayList(u8).init(allocator);
    errdefer list.deinit();
    try list.appendSlice("hello");
    return list.toOwnedSlice(); // caller owns the memory
}
```

### Forgetting defer Ordering

`defer` executes in reverse order. Be mindful when the order of cleanup matters:

```zig
const a = try acquireA();
defer releaseA(a);         // runs second
const b = try acquireB(a);
defer releaseB(b);         // runs first
```

### Ignoring Allocator Failures

Every allocation can fail with `OutOfMemory`. Always handle or propagate allocation errors with `try`.

## Anti-Patterns Quick Reference

These are the most common memory mistakes in Zig code reviews:

```zig
// 1. ANTI-PATTERN: global mutable allocator
var global_alloc = std.heap.page_allocator;
pub fn getData() ![]u8 { return try global_alloc.alloc(u8, 100); }
// FIX: fn getData(allocator: std.mem.Allocator) ![]u8 { ... }

// 2. ANTI-PATTERN: missing defer for file.close()
var file = try std.fs.cwd().openFile(path, .{});
const data = try file.readToEndAlloc(allocator, max_size);
// file is never closed!
// FIX: add `defer file.close();` immediately after openFile

// 3. ANTI-PATTERN: missing errdefer after allocation
const buf = try allocator.alloc(u8, 1024);
const result = try riskyOperation(buf); // if this fails, buf leaks
// FIX: add `errdefer allocator.free(buf);` after alloc

// 4. ANTI-PATTERN: no deinit for HashMap/ArrayList
var cache = std.StringHashMap([]u8).init(allocator);
// ... used but never deinited
// FIX: defer cache.deinit();

// 5. ANTI-PATTERN: using anyerror instead of specific error set
fn process(data: []const u8) anyerror!Result { ... }
// FIX: const ProcessError = error{ InvalidFormat, TooLarge };
// fn process(data: []const u8) ProcessError!Result { ... }

// 6. ANTI-PATTERN: var where const suffices
var result = try compute(); // never mutated
// FIX: const result = try compute();
```
