# Testing and Build System

## Writing Tests

### Inline Tests

Zig tests live right next to the code they test — no separate test files needed:

```zig
fn add(a: u32, b: u32) u32 {
    return a + b;
}

test "add returns sum of two positive integers" {
    try std.testing.expectEqual(@as(u32, 5), add(2, 3));
}
```

Use `zig test` to run tests. For build-system-integrated testing, `zig build test` runs the test step defined in `build.zig`.

### Use std.testing.allocator

Always use `std.testing.allocator` in tests — it detects memory leaks and will fail the test if any allocations aren't freed.

### Table-Driven Tests

```zig
test "parseNumber handles various inputs" {
    const cases = .{
        .{ "42", 42 },
        .{ "0", 0 },
        .{ "-1", null },
        .{ "abc", null },
    };

    inline for (cases) |case| {
        const input = case[0];
        const expected = case[1];
        const result = parseNumber(input);
        if (expected) |exp| {
            try std.testing.expectEqual(exp, result orelse unreachable);
        } else {
            try std.testing.expect(result == null);
        }
    }
}
```

### Testing Error Conditions

```zig
test "divide returns error on zero divisor" {
    const result = divide(10, 0);
    try std.testing.expectError(error.DivisionByZero, result);
}
```

### Descriptive Test Names

Names like `"test add"` tell you nothing when they fail. Use names that describe the behavior: `"add returns sum of two positive integers"`.

### Doctests

Code examples in doc comments are compiled and run as tests:

```zig
/// Calculates the distance between two points.
///
/// ```zig
/// const d = distance(.{ .x = 0, .y = 0 }, .{ .x = 3, .y = 4 });
/// try std.testing.expectEqual(@as(f64, 5.0), d);
/// ```
fn distance(a: Point, b: Point) f64 { ... }
```

### Allocation Failure Testing

See `references/memory-management.md` for `std.testing.FailingAllocator` and exhaustive allocation failure testing patterns.

## Coverage Testing

### Using kcov

Zig programs in Debug mode emit DWARF debug info compatible with kcov:

```bash
zig build test
kcov --include-pattern=src/ coverage/ ./zig-out/bin/test
open coverage/index.html
```

### Built-in Source-Level Coverage

Zig 0.14+ supports `-fcode-coverage` for LLVM source-based coverage:

```bash
zig build test -fcode-coverage
# Produces profraw files for llvm-profdata / llvm-cov
```

### Build System Integration for Coverage

```zig
const coverage_step = b.step("coverage", "Run tests with code coverage");
const coverage_run = b.addSystemCommand(&.{
    "kcov", "--include-pattern=src/", "coverage/",
});
coverage_run.addArtifactArg(tests);
coverage_step.dependOn(&coverage_run.step);
```

---

## Build System

Zig's build system uses Zig itself — your `build.zig` is a Zig program.

### Scaffolding

Use `zig init` to scaffold a project. It generates `build.zig`, `build.zig.zon`, and a source structure.

### Build Modes

- **Debug** (default) — safety checks on, no optimizations. For development.
- **ReleaseSafe** — optimizations + safety checks. Good for production where correctness matters most.
- **ReleaseFast** — maximum speed, safety checks off. For performance-critical production code you trust.
- **ReleaseSmall** — minimize binary size. For embedded or size-constrained environments.

### Basic build.zig

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(exe);

    // Run step
    const run_cmd = b.addRunArtifact(exe);
    const run_step = b.step("run", "Run the application");
    run_step.dependOn(&run_cmd.step);

    // Test step
    const tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&b.addRunArtifact(tests).step);
}
```

### Use `zig build --watch` during development for automatic rebuilds.

### Multi-Module Projects

```zig
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Shared module
    const lib_mod = b.addModule("mylib", .{
        .root_source_file = b.path("src/root.zig"),
    });

    // Library artifact
    const lib = b.addStaticLibrary(.{
        .name = "mylib",
        .root_source_file = b.path("src/root.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(lib);

    // Executable
    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    exe.root_module.addImport("mylib", lib_mod);
    b.installArtifact(exe);

    // Tests
    const tests = b.addTest(.{
        .root_source_file = b.path("src/root.zig"),
        .target = target,
        .optimize = optimize,
    });
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&b.addRunArtifact(tests).step);
}
```

### Custom Build Steps

The build system is a DAG — steps can depend on other steps:

```zig
// Code generation
const gen_step = b.addSystemCommand(&.{
    "python3", "scripts/generate_bindings.py",
});
gen_step.addFileArg(b.path("api_spec.json"));
const generated = gen_step.addOutputFileArg("bindings.zig");

// Use generated file as a module
exe.root_module.addAnonymousImport("bindings", .{
    .root_source_file = generated,
});
```

### Documentation Generation

```zig
const docs_step = b.step("docs", "Generate documentation");
const docs = b.addStaticLibrary(.{
    .name = "mylib",
    .root_source_file = b.path("src/root.zig"),
    .target = target,
    .optimize = optimize,
});
const install_docs = b.addInstallDirectory(.{
    .source = docs.getEmitDocs(),
    .install_dir = .prefix,
    .install_subdir = "docs",
});
docs_step.dependOn(&install_docs.step);
```

Zig produces HTML documentation from `///` doc comments on public declarations.

### Cross-Compilation

Cross-compilation works with the same `build.zig` — no platform-specific configuration:

```bash
zig build -Dtarget=aarch64-linux-gnu    # Linux ARM64
zig build -Dtarget=x86_64-windows-msvc  # Windows x86_64
zig build -Dtarget=x86_64-macos         # macOS
```

---

## Dependencies and Package Management

### build.zig.zon

```zon
.{
    .name = "my-library",
    .version = "1.2.0",
    .minimum_zig_version = "0.13.0",
    .dependencies = .{
        .zap = .{
            .url = "https://github.com/zigzap/zap/archive/refs/tags/v0.2.0.tar.gz",
            .hash = "1220abc123...",
        },
        .local_dep = .{
            .path = "../shared-lib",
        },
    },
    .paths = .{
        "build.zig",
        "build.zig.zon",
        "src",
    },
}
```

The `.paths` field controls what files are included when your package is consumed as a dependency.

### Fetching Dependencies

```bash
zig fetch https://github.com/user/repo/archive/v1.0.tar.gz
zig fetch --save https://github.com/user/repo/archive/v1.0.tar.gz  # auto-add to build.zig.zon
```

### Using Dependencies in build.zig

```zig
const zap = b.dependency("zap", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("zap", zap.module("zap"));
exe.linkLibrary(zap.artifact("zap")); // if linking C libraries
```

### Hash Verification

Zig uses content-addressable hashing for reproducible builds. The hash ensures you always get the exact same source. Update the hash when upgrading a dependency version — `zig fetch` gives you the correct hash.

---

## Project Structure

### Standard Layout

```
my-project/
├── build.zig            # Build configuration
├── build.zig.zon        # Dependencies and package metadata
├── src/
│   ├── main.zig         # Executable entry point
│   ├── root.zig         # Library root (public API)
│   ├── core/
│   │   ├── engine.zig
│   │   └── types.zig
│   └── utils/
│       ├── logging.zig
│       └── config.zig
├── tests/
│   └── integration_test.zig
└── examples/
    └── basic_usage.zig
```

### Library Project Checklist

When setting up a reusable library that other Zig projects can depend on, **all** of these are required:

1. **`build.zig`** — with library artifact, test step, and docs step
2. **`build.zig.zon`** — with `.name`, `.version`, `.minimum_zig_version`, `.paths`, and dependencies
3. **`src/root.zig`** — library entry point, re-exports public API
4. **Specific error sets** — `const ParseError = error{ InvalidField, UnexpectedEof };` not `anyerror`
5. **`///` doc comments** on every `pub` function and type
6. **Inline tests** using `std.testing.allocator` in every module
7. **Streaming/allocator-based design** — accept `Allocator` parameter, never use global allocators

### Complete Library build.zig.zon Example

```zon
.{
    .name = "csv-parser",
    .version = "0.1.0",
    .minimum_zig_version = "0.13.0",
    .dependencies = .{},
    .paths = .{
        "build.zig",
        "build.zig.zon",
        "src",
    },
}
```

### Complete Library build.zig Example

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Library module (for consumers to import)
    _ = b.addModule("csv", .{
        .root_source_file = b.path("src/root.zig"),
    });

    // Library artifact
    const lib = b.addStaticLibrary(.{
        .name = "csv",
        .root_source_file = b.path("src/root.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(lib);

    // Tests
    const tests = b.addTest(.{
        .root_source_file = b.path("src/root.zig"),
        .target = target,
        .optimize = optimize,
    });
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&b.addRunArtifact(tests).step);

    // Documentation
    const docs_step = b.step("docs", "Generate documentation");
    const docs = b.addStaticLibrary(.{
        .name = "csv",
        .root_source_file = b.path("src/root.zig"),
        .target = target,
        .optimize = optimize,
    });
    const install_docs = b.addInstallDirectory(.{
        .source = docs.getEmitDocs(),
        .install_dir = .prefix,
        .install_subdir = "docs",
    });
    docs_step.dependOn(&install_docs.step);
}
```

### Library root.zig Pattern

```zig
//! CSV parsing library with streaming support.
//! Handles quoted fields, custom delimiters, and RFC 4180 compliance.

pub const Parser = @import("parser.zig").Parser;
pub const ParseError = @import("parser.zig").ParseError;
pub const Config = @import("config.zig").Config;

test {
    // Pull in tests from all submodules
    _ = @import("parser.zig");
    _ = @import("config.zig");
}
```

### Module Organization

Each `.zig` file is a module. Expose a clean public surface through a root file:

```zig
// src/root.zig — library public API
pub const Engine = @import("core/engine.zig").Engine;
pub const Config = @import("utils/config.zig").Config;
pub const LogLevel = @import("utils/logging.zig").LogLevel;
pub const Error = Engine.Error;
```

### Separation of Concerns

Split modules by responsibility, not by language feature:

```zig
// src/parser.zig — only parsing
pub fn parse(input: []const u8) !Ast { ... }

// src/validator.zig — only validation
pub fn validate(ast: Ast) !ValidatedAst { ... }

// src/formatter.zig — only formatting
pub fn format(allocator: Allocator, ast: ValidatedAst) ![]u8 { ... }
```

### Dependency Inversion

Accept interfaces (via `anytype` or function pointers) rather than concrete implementations:

```zig
const Logger = struct {
    logFn: *const fn ([]const u8) void,

    pub fn log(self: Logger, msg: []const u8) void {
        self.logFn(msg);
    }
};

fn processWithLogging(logger: Logger, data: []const u8) !void {
    logger.log("starting processing");
    // ...
}
```

### Naming Conventions

- `camelCase` for functions and local variables
- `PascalCase` for types (structs, enums, unions) and comptime-known values
- `UPPER_SNAKE_CASE` for compile-time constants (`const MAX_SIZE: usize = 4096`)
- File names use `snake_case.zig`

### Keep Files Focused

A file growing past 500-800 lines often means two responsibilities are tangled. Split along natural boundaries.

### Write Doc Comments on Public API

```zig
/// Parses a CSV row into a slice of fields.
/// Returns `error.MalformedInput` if the row has unmatched quotes.
pub fn parseRow(allocator: Allocator, line: []const u8) ![][]const u8 { ... }
```
