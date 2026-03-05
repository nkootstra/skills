# Standard Library Recipes

Common patterns using Zig's standard library for data structures, I/O, strings, networking, and concurrency.

## Data Structures

### ArrayList (Dynamic Array)

```zig
var list = std.ArrayList(u32).init(allocator);
defer list.deinit();

try list.append(1);
try list.append(2);
try list.appendSlice(&[_]u32{ 3, 4, 5 });

for (list.items) |item| {
    std.debug.print("{}\n", .{item});
}
```

### HashMap

```zig
var map = std.AutoHashMap([]const u8, u32).init(allocator);
defer map.deinit();

try map.put("hello", 42);

if (map.get("hello")) |value| {
    std.debug.print("found: {}\n", .{value});
}
```

For string keys, use `std.StringHashMap(V)` which handles hashing and comparison correctly for byte slices.

### Linked Lists

The standard library provides `std.SinglyLinkedList` and `std.DoublyLinkedList`. These are intrusive — the node type is embedded in your data:

```zig
const Node = struct {
    data: u32,
    list_node: std.SinglyLinkedList(Node).Node = .{},
};
```

---

## File I/O

### Reading a File

```zig
const file = try std.fs.cwd().openFile("data.txt", .{});
defer file.close();

// Read the entire file (with a max size limit)
const contents = try file.readToEndAlloc(allocator, 1024 * 1024);
defer allocator.free(contents);
```

### Writing a File

```zig
const file = try std.fs.cwd().createFile("output.txt", .{});
defer file.close();

try file.writeAll("Hello, Zig!\n");

// Buffered writing for performance
var buf_writer = std.io.bufferedWriter(file.writer());
try buf_writer.writer().print("Value: {}\n", .{42});
try buf_writer.flush();
```

### Reading Line by Line

```zig
const file = try std.fs.cwd().openFile("data.txt", .{});
defer file.close();

var buf_reader = std.io.bufferedReader(file.reader());
var reader = buf_reader.reader();

var line_buf: [4096]u8 = undefined;
while (try reader.readUntilDelimiterOrEof(&line_buf, '\n')) |line| {
    std.debug.print("{s}\n", .{line});
}
```

### Directory Iteration

```zig
var dir = try std.fs.cwd().openDir("src", .{ .iterate = true });
defer dir.close();

var iter = dir.iterate();
while (try iter.next()) |entry| {
    std.debug.print("{s} ({s})\n", .{ entry.name, @tagName(entry.kind) });
}
```

---

## String Handling

Strings in Zig are just byte slices (`[]const u8`). There is no special string type.

### Formatting

```zig
// Print to stdout
std.debug.print("Hello, {s}! You are {} years old.\n", .{ name, age });

// Format to a buffer
var buf: [256]u8 = undefined;
const formatted = try std.fmt.bufPrint(&buf, "{s}_{}", .{ prefix, id });

// Allocate a formatted string
const s = try std.fmt.allocPrint(allocator, "user_{}", .{id});
defer allocator.free(s);
```

### Splitting and Tokenizing

```zig
// Split by delimiter (preserves empty tokens)
var iter = std.mem.splitScalar(u8, "a,b,c,d", ',');
while (iter.next()) |token| {
    // process token
}

// Tokenize (collapses consecutive delimiters)
var tok = std.mem.tokenizeScalar(u8, "hello   world", ' ');
while (tok.next()) |token| {
    // "hello", then "world" (no empty tokens)
}
```

### Comparison and Search

```zig
const equal = std.mem.eql(u8, "hello", "hello");
const has_it = std.mem.indexOf(u8, haystack, needle) != null;
const starts = std.mem.startsWith(u8, path, "/home/");
```

---

## Networking

### HTTP GET Request

```zig
var client = std.http.Client{ .allocator = allocator };
defer client.deinit();

var response = std.ArrayList(u8).init(allocator);
defer response.deinit();

const result = try client.fetch(.{
    .uri = try std.Uri.parse("https://example.com/api"),
    .response_storage = .{ .dynamic = &response },
});

if (result.status == .ok) {
    std.debug.print("Response: {s}\n", .{response.items});
}
```

### TCP Server

```zig
const address = try std.net.Address.parseIp("127.0.0.1", 8080);
var server = try address.listen(.{});
defer server.deinit();

while (true) {
    const conn = try server.accept();
    defer conn.stream.close();
    // handle connection...
}
```

---

## Concurrency

### Basic Thread Spawning

```zig
fn worker(id: usize) void {
    std.debug.print("Worker {} started\n", .{id});
}

pub fn main() !void {
    var threads: [4]std.Thread = undefined;
    for (&threads, 0..) |*t, i| {
        t.* = try std.Thread.spawn(.{}, worker, .{i});
    }
    for (&threads) |t| {
        t.join();
    }
}
```

Always join or detach threads to avoid resource leaks.

### Mutex-Protected Shared State

```zig
const SharedCounter = struct {
    value: u64 = 0,
    mutex: std.Thread.Mutex = .{},

    fn increment(self: *SharedCounter) void {
        self.mutex.lock();
        defer self.mutex.unlock();
        self.value += 1;
    }
};
```

### Thread Pool

```zig
var pool: std.Thread.Pool = undefined;
try pool.init(.{
    .allocator = allocator,
    .n_jobs = 8,
});
defer pool.deinit();

pool.spawn(myTask, .{arg1, arg2});
```

### Prefer message passing over shared mutable state when the design allows it.

### Async I/O

For high-concurrency network services, Zig provides non-blocking I/O primitives. Use `std.io.poll` for event-driven architectures.
