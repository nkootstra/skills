# Comptime and Generics

Zig's `comptime` system lets you run code during compilation to generate types, enforce constraints, and eliminate runtime overhead. It's Zig's approach to generics and metaprogramming.

## Comptime Parameters for Generic Functions

```zig
fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}
```

## Generic Data Structures

The standard pattern for generic containers uses a function that returns a type:

```zig
fn Stack(comptime T: type) type {
    return struct {
        items: []T,
        count: usize,
        allocator: std.mem.Allocator,

        const Self = @This();

        pub fn init(allocator: std.mem.Allocator, capacity: usize) !Self {
            return Self{
                .items = try allocator.alloc(T, capacity),
                .count = 0,
                .allocator = allocator,
            };
        }

        pub fn push(self: *Self, value: T) !void {
            if (self.count >= self.items.len)
                return error.StackOverflow;
            self.items[self.count] = value;
            self.count += 1;
        }

        pub fn pop(self: *Self) ?T {
            if (self.count == 0) return null;
            self.count -= 1;
            return self.items[self.count];
        }

        pub fn deinit(self: *Self) void {
            self.allocator.free(self.items);
        }
    };
}
```

## Type Introspection with @typeInfo

```zig
fn printFields(value: anytype) void {
    const T = @TypeOf(value);
    const info = @typeInfo(T);

    switch (info) {
        .@"struct" => |s| {
            inline for (s.fields) |field| {
                std.debug.print("{s}: {}\n", .{ field.name, @field(value, field.name) });
            }
        },
        else => std.debug.print("{}\n", .{value}),
    }
}
```

Use `@typeInfo` and `@TypeOf` for reflection. Use `@hasDecl` to check for method existence at compile time.

## Compile-Time Validation

Use `@compileError` to catch misuse at compile time rather than runtime:

```zig
fn safeDiv(comptime T: type, a: T, b: T) T {
    if (@typeInfo(T) != .int and @typeInfo(T) != .float) {
        @compileError("safeDiv requires numeric type, got " ++ @typeName(T));
    }
    if (b == 0) @panic("division by zero");
    return @divTrunc(a, b);
}
```

### Structural Type Requirements

Enforce that types implement required methods:

```zig
fn Serializable(comptime T: type) type {
    if (!@hasDecl(T, "serialize")) {
        @compileError(@typeName(T) ++ " must implement serialize()");
    }
    if (!@hasDecl(T, "deserialize")) {
        @compileError(@typeName(T) ++ " must implement deserialize()");
    }

    return struct {
        value: T,

        pub fn toBytes(self: @This(), buf: []u8) !usize {
            return self.value.serialize(buf);
        }

        pub fn fromBytes(data: []const u8) !@This() {
            return .{ .value = try T.deserialize(data) };
        }
    };
}
```

## Compile-Time String Processing

Comptime can process strings at compile time to build lookup tables, parse formats, etc.:

```zig
fn comptimeHash(comptime s: []const u8) u32 {
    comptime {
        var hash: u32 = 0;
        for (s) |c| {
            hash = hash *% 31 +% c;
        }
        return hash;
    }
}

// Usage — hash is computed at compile time, zero runtime cost
const key_hash = comptimeHash("my_key");
```

## Comptime Lookup Tables

Precompute lookup tables at compile time for zero-cost runtime lookups:

```zig
const LookupTable = blk: {
    var table: [256]u8 = [_]u8{0} ** 256;
    for ('a'..'z' + 1) |c| table[c] = 1; // letters
    for ('0'..'9' + 1) |c| table[c] = 2; // digits
    break :blk table;
};
// LookupTable is baked into the binary — zero runtime cost
```

See `references/performance.md` for a CRC32 lookup table example.

## Comptime State Machines

Generate state machine dispatch tables at compile time:

```zig
fn StateMachine(comptime State: type, comptime Event: type) type {
    return struct {
        state: State,

        const Self = @This();

        pub fn init(initial: State) Self {
            return .{ .state = initial };
        }

        pub fn transition(self: *Self, event: Event) void {
            self.state = dispatch(self.state, event);
        }

        fn dispatch(state: State, event: Event) State {
            // Comptime switch generates an optimized jump table
            return switch (state) {
                inline else => |s| switch (event) {
                    inline else => |e| comptime getNextState(s, e),
                },
            };
        }

        fn getNextState(comptime state: State, comptime event: Event) State {
            _ = state;
            _ = event;
            @compileError("undefined transition");
        }
    };
}
```

## Fat Pointer Interfaces (Runtime Polymorphism)

Zig doesn't have interfaces or traits. For compile-time polymorphism, use `anytype` with comptime validation. For runtime polymorphism (storing different implementations in the same collection), use fat pointers — a data pointer plus a vtable pointer:

```zig
const Writer = struct {
    ptr: *anyopaque,
    writeFn: *const fn (*anyopaque, []const u8) anyerror!usize,

    fn write(self: Writer, data: []const u8) !usize {
        return self.writeFn(self.ptr, data);
    }

    fn init(pointer: anytype) Writer {
        const Ptr = @TypeOf(pointer);
        const impl = struct {
            fn write(p: *anyopaque, data: []const u8) anyerror!usize {
                const self: Ptr = @ptrCast(@alignCast(p));
                return self.write(data);
            }
        };
        return .{
            .ptr = pointer,
            .writeFn = impl.write,
        };
    }
};

// Store different writers uniformly:
var writers: [3]Writer = .{
    Writer.init(&file_writer),
    Writer.init(&socket_writer),
    Writer.init(&buffer_writer),
};
```

This is exactly how `std.mem.Allocator` works internally.

## Multi-Writer Pattern

Fan out writes to multiple destinations simultaneously:

```zig
fn MultiWriter(comptime N: usize) type {
    return struct {
        writers: [N]std.io.AnyWriter,

        const Self = @This();

        pub fn writer(self: *Self) std.io.Writer(*Self, anyerror, writeFn) {
            return .{ .context = self };
        }

        fn writeFn(self: *Self, data: []const u8) anyerror!usize {
            for (&self.writers) |*w| {
                try w.writeAll(data);
            }
            return data.len;
        }
    };
}
```

## anytype Guidance

Don't overuse `anytype`. If a function only works with a specific interface, use a concrete type or define a clear contract. `anytype` should be used when you genuinely need duck-typing behavior, not as a lazy way to avoid specifying types.

```zig
// Good: genuinely generic — writer just needs .write()
fn serialize(writer: anytype, value: anytype) !void {
    try writer.writeAll(std.fmt.comptimePrint("{}", .{value}));
}

// Bad: only works with one type, anytype hides the contract
fn processUser(user: anytype) void { ... }
// Better: be explicit
fn processUser(user: User) void { ... }
```

## Comptime Event Emitter Pattern

A complete example of using comptime to build a type-safe event system with per-event payloads and dynamic listener management:

```zig
fn EventEmitter(comptime events: type) type {
    // events is an enum like: enum { on_connect, on_message, on_close }
    const event_count = @typeInfo(events).@"enum".fields.len;

    return struct {
        // One listener list per event kind
        listeners: [event_count]std.ArrayList(Callback),
        allocator: std.mem.Allocator,

        const Self = @This();
        const Callback = *const fn (ctx: ?*anyopaque) void;

        pub fn init(allocator: std.mem.Allocator) Self {
            var self: Self = .{
                .listeners = undefined,
                .allocator = allocator,
            };
            for (&self.listeners) |*list| {
                list.* = std.ArrayList(Callback).init(allocator);
            }
            return self;
        }

        pub fn deinit(self: *Self) void {
            for (&self.listeners) |*list| {
                list.deinit();
            }
        }

        pub fn on(self: *Self, event: events, callback: Callback) !void {
            try self.listeners[@intFromEnum(event)].append(callback);
        }

        pub fn off(self: *Self, event: events, callback: Callback) void {
            const list = &self.listeners[@intFromEnum(event)];
            for (list.items, 0..) |cb, i| {
                if (cb == callback) {
                    _ = list.swapRemove(i);
                    return;
                }
            }
        }

        pub fn emit(self: *Self, event: events, ctx: ?*anyopaque) void {
            for (self.listeners[@intFromEnum(event)].items) |cb| {
                cb(ctx);
            }
        }
    };
}

// Usage:
const MyEvents = enum { on_connect, on_message, on_close };
const Emitter = EventEmitter(MyEvents);

test "event emitter" {
    var em = Emitter.init(std.testing.allocator);
    defer em.deinit();

    var called = false;
    const cb = struct {
        fn handler(ctx: ?*anyopaque) void {
            const flag: *bool = @ptrCast(@alignCast(ctx.?));
            flag.* = true;
        }
    }.handler;

    try em.on(.on_connect, cb);
    em.emit(.on_connect, @ptrCast(&called));
    try std.testing.expect(called);
}
```

**Key patterns used:**
- Enum → integer index via `@intFromEnum` for O(1) event dispatch
- One `ArrayList` per event variant, indexed by enum ordinal
- `*const fn` for callback type — avoids allocating closures
- `?*anyopaque` for type-erased context — callers cast back with `@ptrCast(@alignCast(...))`
- init/deinit pattern with `std.testing.allocator` in tests

For typed payloads per event, use a comptime map from enum value to payload type and generate separate callback signatures per event. This is an advanced pattern — start with the `?*anyopaque` version above.

## Typed EventEmitter with Comptime Payload Map

For compile-time type-safe event payloads, use `EventEmitter(comptime EventEnum, comptime PayloadMap)`. Each event variant maps to a specific payload type via a comptime function, so callbacks are type-safe per event:

```zig
fn EventEmitter(comptime EventEnum: type, comptime payloadType: fn (EventEnum) type) type {
    const event_fields = @typeInfo(EventEnum).@"enum".fields;
    const event_count = event_fields.len;

    return struct {
        /// One type-erased listener list per event kind.
        listeners: [event_count]std.ArrayList(ErasedCallback),
        allocator: std.mem.Allocator,

        const Self = @This();
        const ErasedCallback = *const fn (ptr: *const anyopaque) void;

        pub fn init(allocator: std.mem.Allocator) Self {
            var self: Self = .{
                .listeners = undefined,
                .allocator = allocator,
            };
            for (&self.listeners) |*list| {
                list.* = std.ArrayList(ErasedCallback).init(allocator);
            }
            return self;
        }

        pub fn deinit(self: *Self) void {
            for (&self.listeners) |*list| {
                list.deinit();
            }
        }

        /// Register a typed callback for `event`.
        /// The callback receives a pointer to the event's payload type.
        pub fn on(
            self: *Self,
            comptime event: EventEnum,
            comptime callback: *const fn (*const payloadType(event)) void,
        ) !void {
            const erased: ErasedCallback = @ptrCast(callback);
            try self.listeners[@intFromEnum(event)].append(erased);
        }

        /// Remove a previously registered listener.
        pub fn off(
            self: *Self,
            comptime event: EventEnum,
            comptime callback: *const fn (*const payloadType(event)) void,
        ) void {
            const erased: ErasedCallback = @ptrCast(callback);
            const list = &self.listeners[@intFromEnum(event)];
            for (list.items, 0..) |cb, i| {
                if (cb == erased) {
                    _ = list.swapRemove(i);
                    return;
                }
            }
        }

        /// Emit an event with its typed payload. All registered listeners are called.
        pub fn emit(self: *Self, comptime event: EventEnum, payload: *const payloadType(event)) void {
            for (self.listeners[@intFromEnum(event)].items) |cb| {
                cb(@ptrCast(payload));
            }
        }
    };
}

// --- Usage example ---

const MyEvents = enum { on_connect, on_message, on_close };

// Comptime function mapping each event to its payload type
fn MyPayloads(event: MyEvents) type {
    return switch (event) {
        .on_connect => struct { address: []const u8, port: u16 },
        .on_message => struct { data: []const u8, sender_id: u32 },
        .on_close => struct { reason: []const u8 },
    };
}

const MyEmitter = EventEmitter(MyEvents, MyPayloads);

test "typed event emitter" {
    var em = MyEmitter.init(std.testing.allocator);
    defer em.deinit();

    // Track whether handler was called with correct payload
    const State = struct {
        var received_port: u16 = 0;
        var message_count: u32 = 0;

        fn onConnect(payload: *const MyPayloads(.on_connect)) void {
            received_port = payload.port;
        }
        fn onMessage(_: *const MyPayloads(.on_message)) void {
            message_count += 1;
        }
    };

    try em.on(.on_connect, State.onConnect);
    try em.on(.on_message, State.onMessage);

    // Emit with typed payload — wrong payload type would be a compile error
    em.emit(.on_connect, &.{ .address = "127.0.0.1", .port = 8080 });
    em.emit(.on_message, &.{ .data = "hello", .sender_id = 1 });
    em.emit(.on_message, &.{ .data = "world", .sender_id = 2 });

    try std.testing.expectEqual(@as(u16, 8080), State.received_port);
    try std.testing.expectEqual(@as(u32, 2), State.message_count);

    // Remove listener and verify it stops receiving
    em.off(.on_message, State.onMessage);
    em.emit(.on_message, &.{ .data = "ignored", .sender_id = 3 });
    try std.testing.expectEqual(@as(u32, 2), State.message_count);
}
```

**Key patterns used:**
- `EventEmitter(comptime EventEnum, comptime PayloadMap)` — event enum + comptime function mapping events to payload types
- Callback signature is `*const fn (*const PayloadType) void` — type-safe per event variant
- Type erasure via `@ptrCast` to store heterogeneous callbacks in a single `ArrayList`
- `@intFromEnum` for O(1) dispatch to the correct listener list
- init/deinit pair with `std.testing.allocator` in tests
- `on`/`off`/`emit` form the complete listener lifecycle

The simpler `?*anyopaque` callback approach (shown above in "Comptime Event Emitter Pattern") is preferred when you don't need per-event payload type safety.

## Common Comptime Mistakes

1. **Using `anytype` when a concrete type works** — hides the expected interface, making errors confusing.
2. **Confusing compile-time and runtime contexts** — a `comptime` variable can't be modified at runtime; trying to modify it in a runtime loop is an error.
3. **Forgetting `@setEvalBranchQuota`** — comptime evaluation has a default branch limit (1000). Complex comptime loops may need `@setEvalBranchQuota(10000)` or higher.
4. **Trying to store runtime values in comptime containers** — comptime arrays and structs are baked into the binary; use `ArrayList` or similar runtime containers for dynamic data.
5. **Generating types without init/deinit** — if a generated type contains `ArrayList` or other owned resources, it MUST have `deinit()`.
