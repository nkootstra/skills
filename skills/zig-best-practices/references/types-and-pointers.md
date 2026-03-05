# Types and Pointers

Zig has a precise type system with multiple pointer types, explicit casting, and no implicit lossy conversions.

## Pointer Types

Choose the right pointer type:

| Need | Use |
|------|-----|
| Reference to one value | `*T` |
| C function return (unknown length) | `[*]T`, convert to slice ASAP |
| Known-length buffer | `[]T` (slice) |
| Null-terminated C string | `[*:0]const u8` or `[:0]const u8` |
| Optional reference | `?*T` |

**Always prefer slices over many-item pointers.** Slices carry their length and are bounds-checked in safe builds.

### Single-Item Pointer (*T)

Points to exactly one item. Most common pointer type.

```zig
var x: u32 = 42;
const ptr: *u32 = &x;
ptr.* = 100;
```

### Many-Item Pointer ([*]T)

Points to an unknown number of items. Like a C pointer — supports arithmetic but no bounds checking.

```zig
const data: [*]const u8 = buffer.ptr;
const byte = data[5]; // no bounds check
```

### Slice ([]T)

Pointer + length. The workhorse type.

```zig
const slice: []const u8 = buffer[0..n];
```

### Pointer Arithmetic

Many-item pointers support arithmetic for low-level buffer manipulation:

```zig
var ptr: [*]u8 = buffer.ptr;
ptr += 4; // advance past a 4-byte header
const value = ptr[0..8]; // slice from new position
```

## Type Casting Builtins

### @ptrCast — Change Pointer Type

The pointed-to memory must be valid for the target type:

```zig
const bytes: *[4]u8 = buffer[0..4];
const int_ptr: *const u32 = @ptrCast(bytes);
```

### @alignCast — Assert Alignment

Safety assertion — panics in debug builds if the address isn't properly aligned:

```zig
// Common pattern: @alignCast with @ptrCast for raw byte interpretation
fn readU32FromBytes(bytes: [*]const u8) u32 {
    const aligned: *const u32 = @ptrCast(@alignCast(bytes));
    return aligned.*;
}
```

For unaligned reads, use `std.mem.readInt` instead:

```zig
const value = std.mem.readInt(u32, bytes[0..4], .little);
```

### @bitCast — Reinterpret Bits

Reinterprets bits of one type as another of the same size. No conversion — just a different view:

```zig
const f: f32 = 3.14;
const bits: u32 = @bitCast(f);

// Packed struct to/from integer
const header_bits: u32 = @bitCast(my_packed_header);
const header: MyPackedHeader = @bitCast(raw_u32);
```

Both types must be the same size — compile error otherwise.

### @intCast — Narrow Integer Types

Triggers safety-checked UB if the value doesn't fit:

```zig
const big: u64 = 42;
const small: u8 = @intCast(big); // OK: 42 fits

const too_big: u64 = 300;
const bad: u8 = @intCast(too_big); // PANIC in safe builds
```

Safer alternative — `std.math.cast` returns an optional:

```zig
const maybe: ?u8 = std.math.cast(u8, big_value);
```

### Pointer-Integer Conversion

`@intFromPtr` and `@ptrFromInt` are for memory-mapped I/O and DMA — inherently unsafe, use sparingly:

```zig
const addr: usize = @intFromPtr(ptr);
const register: *volatile u32 = @ptrFromInt(0x4000_0000);
```

## Type Coercion

Zig only coerces implicitly when it's guaranteed safe:

```zig
// Integer widening (u8 → u16) ✓
const x: u8 = 42;
const y: u16 = x;

// Adding const ✓
var buf: [4]u8 = .{ 1, 2, 3, 4 };
const slice: []const u8 = &buf;

// Array to slice ✓
const arr: [3]u32 = .{ 1, 2, 3 };
const s: []const u32 = &arr;

// T to ?T ✓
const val: u32 = 5;
const opt: ?u32 = val;

// Narrowing — COMPILE ERROR, explicit cast required
// const small: u8 = big_u16;
```

### Peer Type Resolution

In `if`/`else`, `switch`, and array literals, Zig finds a common type:

```zig
const x: u8 = 5;
const y: u16 = 300;
const result = if (condition) x else y; // result is u16
```

## Integer Overflow

By default, integer overflow panics in safe builds.

**Wrapping operators (`+%`, `-%`, `*%`)** — intentional wrapping for hash functions, checksums:

```zig
var x: u8 = 255;
x +%= 1; // x is now 0

fn simpleHash(data: []const u8) u32 {
    var hash: u32 = 0;
    for (data) |byte| {
        hash = hash *% 31 +% byte;
    }
    return hash;
}
```

**Saturating operators (`|+`, `|-`, `|*`)** — clamp to min/max:

```zig
var x: u8 = 250;
x |+= 10; // x is now 255 (saturates at max)
```

**`@addWithOverflow`** — explicit overflow detection:

```zig
const result = @addWithOverflow(@as(u8, 250), @as(u8, 10));
const sum = result[0];        // 4 (wrapped value)
const overflowed = result[1]; // 1 (overflow occurred)
```

## Packed Structs

Packed structs give you exact control over memory layout at the bit level. Use them for hardware registers, binary protocols, and file format headers.

```zig
const TCPHeader = packed struct {
    src_port: u16,
    dst_port: u16,
    seq_number: u32,
    ack_number: u32,
    data_offset: u4,
    reserved: u3,
    flags: packed struct {
        ns: u1, cwr: u1, ece: u1, urg: u1,
        ack: u1, psh: u1, rst: u1, syn: u1, fin: u1,
    },
    window_size: u16,
    checksum: u16,
    urgent_pointer: u16,
};

comptime {
    std.debug.assert(@sizeOf(TCPHeader) == 20);
}
```

**Key rules:**
- No padding — fields are packed tightly at the bit level.
- Backed by integer — you can `@bitCast` between a packed struct and its integer type.
- Cannot take address of non-byte-aligned fields.
- Native endianness — use `std.mem.nativeToBig`/`bigToNative` for network protocols.
- **Don't use packed structs for general-purpose data.** Regular structs let the compiler optimize layout.

## Zero-Sized Types

`void` is the canonical zero-sized type. Use it for type-level tricks:

```zig
// A set is just a map with void values
const StringSet = std.StringHashMap(void);
var set = StringSet.init(allocator);
try set.put("key", {});
const exists = set.contains("key");
```

`anyopaque` is for type erasure (fat pointers, C interop) — unknown size, can't dereference.

In generic containers, ZST parameters are optimized away entirely by the compiler.

## Anonymous Structs and Tuples

### Anonymous Struct Literals

```zig
fn process(config: struct { width: u32, height: u32, color: bool }) void {
    // ...
}
process(.{ .width = 800, .height = 600, .color = true });
```

### Tuples

Anonymous structs with no field names behave as tuples:

```zig
const tuple = .{ @as(u32, 42), "hello", true };
const number = tuple[0]; // 42

// Commonly used with inline for
inline for (tuple) |item| {
    std.debug.print("{}\n", .{item});
}
```

## Sentinel-Terminated Types

### Arrays vs Slices

```zig
// Sentinel-terminated array: fixed size + sentinel
const arr: [5:0]u8 = .{ 'h', 'e', 'l', 'l', 'o' };
// arr.len == 5, but arr[5] == 0

// Sentinel-terminated slice
const slice: [:0]const u8 = "hello"; // string literals are [:0]const u8
```

### Conversions

```zig
// Sentinel slice → regular slice (free — drops sentinel guarantee)
const regular: []const u8 = sentinel_slice;

// Regular slice → sentinel slice (must verify or allocate)
const with_sentinel = try allocator.allocSentinel(u8, data.len, 0);
@memcpy(with_sentinel, data);

// Many-item sentinel pointer → sentinel slice
const c_str: [*:0]const u8 = external_c_func();
const zig_str: [:0]const u8 = std.mem.span(c_str);
```

## Custom Formatting

Implement a `format` method on your types for clean debug output:

```zig
const Vec3 = struct {
    x: f32, y: f32, z: f32,

    pub fn format(
        self: Vec3,
        comptime fmt: []const u8,
        options: std.fmt.FormatOptions,
        writer: anytype,
    ) !void {
        _ = fmt; _ = options;
        try writer.print("Vec3({d:.2}, {d:.2}, {d:.2})", .{ self.x, self.y, self.z });
    }
};
```

### Format Specifiers

The `fmt` parameter tells you what format the caller requested:

```zig
pub fn format(self: Color, comptime fmt: []const u8, options: std.fmt.FormatOptions, writer: anytype) !void {
    _ = options;
    if (comptime std.mem.eql(u8, fmt, "hex")) {
        try writer.print("#{x:0>2}{x:0>2}{x:0>2}", .{ self.r, self.g, self.b });
    } else {
        try writer.print("rgb({}, {}, {})", .{ self.r, self.g, self.b });
    }
}
// std.debug.print("{}\n", .{color});    → rgb(255, 128, 0)
// std.debug.print("{hex}\n", .{color}); → #ff8000
```

## Volatile and Hardware Access

Use `volatile` for memory-mapped I/O where reads/writes have physical side effects:

```zig
const register: *volatile u32 = @ptrFromInt(0x4000_0000);
register.* = 0x01; // must actually write — compiler cannot optimize away
```

**`volatile` is NOT for thread synchronization.** Use `std.atomic.Value` for atomics and `std.Thread.Mutex` for locks. This is a common misconception from C/C++.

```zig
// WRONG: volatile for thread communication
var volatile_flag: *volatile bool = &shared_flag;

// RIGHT: use atomics
var flag = std.atomic.Value(bool).init(false);
flag.store(true, .release);
const val = flag.load(.acquire);
```

For volatile pointer arrays (hardware register banks):

```zig
const gpio_registers: *volatile [16]u32 = @ptrFromInt(0x4002_0000);
gpio_registers[0] = 0x01;
const status = gpio_registers[4];
```
