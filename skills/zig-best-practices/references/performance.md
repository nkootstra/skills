# Performance Optimization

Zig gives you low-level control without sacrificing safety. Think about performance structurally, not as an afterthought.

## Build Modes — The Biggest Lever

This is the single most impactful performance decision:

- **Debug** (default) — safety on, no optimizations. For development.
- **ReleaseFast** — maximum speed, safety checks off. For throughput-critical production code.
- **ReleaseSafe** — optimizations with safety retained. When you want speed but can't afford undefined behavior.
- **ReleaseSmall** — minimize binary size. For embedded or size-constrained environments.

## Arena Allocators in Hot Paths

If a function allocates repeatedly in a loop (parsing requests, processing records), an arena allocator avoids per-object free overhead and reduces allocator contention:

```zig
fn processRecords(backing: std.mem.Allocator, records: []const Record) !Results {
    var arena = std.heap.ArenaAllocator.init(backing);
    defer arena.deinit();
    const alloc = arena.allocator();

    var results = Results.init(backing);
    errdefer results.deinit();

    for (records) |record| {
        const result = try processOne(alloc, record);
        try results.append(result);

        // Reset arena — frees all temporary allocations but keeps the
        // underlying memory pages for reuse (no syscalls)
        _ = arena.reset(.retain_capacity);
    }

    return results;
}
```

## Stack Over Heap

Use fixed-size buffers when the upper bound is known. `FixedBufferAllocator` over a stack buffer avoids all heap overhead.

## SIMD with @Vector

Zig provides portable SIMD through the `@Vector` built-in type. The compiler maps it to hardware SIMD instructions automatically:

```zig
const Vec4f = @Vector(4, f32);
const a: Vec4f = .{ 1.0, 2.0, 3.0, 4.0 };
const b: Vec4f = .{ 5.0, 6.0, 7.0, 8.0 };
const sum = a + b; // hardware-accelerated vector add
```

### SIMD Sum Example

```zig
fn simdSum(data: []const u8) u64 {
    const Vec = @Vector(16, u8);
    const AccVec = @Vector(16, u64);

    var acc: AccVec = @splat(0);
    var i: usize = 0;

    while (i + 16 <= data.len) : (i += 16) {
        const chunk: Vec = data[i..][0..16].*;
        const wide: AccVec = @as(AccVec, chunk);
        acc += wide;
    }

    var total: u64 = @reduce(.Add, acc);

    // Handle remaining bytes
    while (i < data.len) : (i += 1) {
        total += data[i];
    }

    return total;
}
```

## Comptime Lookup Tables

Push computation to compile time. Lookup tables, hash values, format strings — anything that can be computed at compile time should be:

```zig
const crc32_table = blk: {
    var table: [256]u32 = undefined;
    for (0..256) |i| {
        var crc: u32 = @intCast(i);
        for (0..8) |_| {
            if (crc & 1 != 0) {
                crc = (crc >> 1) ^ 0xEDB88320;
            } else {
                crc >>= 1;
            }
        }
        table[i] = crc;
    }
    break :blk table;
};

fn crc32(data: []const u8) u32 {
    var crc: u32 = 0xFFFFFFFF;
    for (data) |byte| {
        const index = (crc ^ byte) & 0xFF;
        crc = (crc >> 8) ^ crc32_table[index];
    }
    return crc ^ 0xFFFFFFFF;
}
```

## Buffered I/O

Always wrap file readers/writers with buffering for I/O-heavy workloads. This alone can yield 10x throughput improvements for small reads/writes:

```zig
fn processLargeFile(path: []const u8) !void {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();

    var buf_reader = std.io.bufferedReader(file.reader());
    const reader = buf_reader.reader();

    const out_file = try std.fs.cwd().createFile("output.txt", .{});
    defer out_file.close();

    var buf_writer = std.io.bufferedWriter(out_file.writer());
    const writer = buf_writer.writer();

    var line_buf: [4096]u8 = undefined;
    while (try reader.readUntilDelimiterOrEof(&line_buf, '\n')) |line| {
        try writer.writeAll(line);
        try writer.writeByte('\n');
    }
    try buf_writer.flush(); // Don't forget to flush!
}
```

## Struct Layout for Cache Performance

Order struct fields by access pattern and size to minimize cache misses:

```zig
// BAD: padding wastes cache lines
const BadLayout = struct {
    flag: bool,       // 1 byte + 7 padding
    big_value: u64,   // 8 bytes
    small: u8,        // 1 byte + 7 padding
    another_big: u64, // 8 bytes
};
// Total: 32 bytes

// BETTER: group by size
const BetterLayout = struct {
    big_value: u64,
    another_big: u64,
    small: u8,
    flag: bool,
};
// Total: 24 bytes

// BEST for iteration: struct-of-arrays (SoA) instead of array-of-structs (AoS)
const ParticleSystem = struct {
    x: []f32,
    y: []f32,
    mass: []f32,
    count: usize,
};
```

## Benchmarking

Zig doesn't have a built-in benchmark framework, but you can measure with `std.time.Timer`:

```zig
fn benchmark(comptime func: anytype, args: anytype, iterations: u32) f64 {
    var timer = std.time.Timer.start() catch unreachable;

    var i: u32 = 0;
    while (i < iterations) : (i += 1) {
        _ = @call(.auto, func, args);
    }

    const elapsed_ns = timer.read();
    return @as(f64, @floatFromInt(elapsed_ns)) / @as(f64, @floatFromInt(iterations));
}

pub fn main() !void {
    const ns_per_call = benchmark(myFunction, .{arg1, arg2}, 10000);
    std.debug.print("Average: {d:.2} ns/call\n", .{ns_per_call});
}
```

For production benchmarking, use external tools like `hyperfine` on the compiled binary.

## Profiling

Zig has no built-in profiler, but builds with `-Doptimize=Debug` produce DWARF debug info compatible with `perf`, `valgrind`, and `tracy`. Measure first, then optimize the hot path.
