# Error Handling

Zig treats errors as first-class data flowing through your program, not as exceptional control flow that jumps across stack frames. This makes error paths visible and forces you to handle them.

## Error Unions

Use error unions (`!T`) as return types. The `!` before a type means "this can fail":

```zig
fn readConfig(path: []const u8) !Config {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();
    // ...
}
```

## Propagating with try

`try` is syntactic sugar for `catch |err| return err`. Use it when your function can't meaningfully handle the error:

```zig
const file = try std.fs.cwd().openFile(path, .{});
```

Prefer `try` over manual error inspection when propagating — it preserves error return traces.

## Handling with catch

Use `catch` when you can provide a fallback:

```zig
const value = parseNumber(input) catch |err| switch (err) {
    error.InvalidCharacter => return default_value,
    else => return err,
};
```

Pattern: `try` + `orelse` for "get or default":

```zig
const config = loadConfig(path) catch Config.defaults();
```

## Specific Error Sets

Define specific error sets rather than using `anyerror`. Specific error sets give callers useful information about what can go wrong:

```zig
const ParseError = error{
    InvalidCharacter,
    Overflow,
    UnexpectedEndOfInput,
};

fn parse(input: []const u8) ParseError!u64 { ... }
```

## The errdefer Chain

When initializing multiple resources where each step can fail, chain `errdefer` to ensure partial initialization is cleaned up:

```zig
fn initSystem(allocator: Allocator) !System {
    const db = try Database.open(allocator, "data.db");
    errdefer db.close();

    const cache = try Cache.init(allocator, 1024);
    errdefer cache.deinit();

    const logger = try Logger.init(allocator, "system.log");
    errdefer logger.deinit();

    return System{
        .db = db,
        .cache = cache,
        .logger = logger,
    };
}
```

If `Logger.init` fails, `cache.deinit()` and `db.close()` run automatically. If everything succeeds, none of the errdefers fire.

## Handling Optional Values

```zig
// Optional unwrap with fallback
const maybe_value: ?u32 = lookup(key);
const value = maybe_value orelse return error.NotFound;

// If-unwrap for optional processing
if (maybe_value) |v| {
    processValue(v);
} else {
    logMissing(key);
}
```

## Error Return Traces

Zig provides error return traces (better than stack traces for error diagnosis) automatically in Debug and ReleaseSafe builds. They show the chain of functions an error passed through, not just where it originated. This means you should prefer `try` over manual error inspection when propagating — it preserves the trace.
