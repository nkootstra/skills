# Compute Latency Reference

Covers: algorithmic complexity, memory management, wait-free synchronization, concurrency models, OS overhead.

---

## Eliminating Work

**Principle**: The fastest code is no code. Profile first, then eliminate.

### Algorithmic Complexity

Big O notation gives the *growth rate*, not the absolute cost. In latency-sensitive paths:
- **O(1)** and **O(log n)**: generally safe
- **O(n)**: acceptable for small, bounded n
- **O(n²)** and worse: red flag; will surface as tail latency spikes as load grows

Common hidden O(n²) patterns:
- Nested loops over request data
- N+1 database queries (loading parent then children in a loop)
- Repeated string concatenation in a loop (some languages)

### Serialization / Deserialization

Serialization is frequently a top bottleneck in profiler output:
- Prefer binary formats (Protobuf, MessagePack, FlatBuffers) over text (JSON, XML) for hot paths
- Avoid unnecessary re-serialization when passing data between internal components
- Consider zero-copy deserialization (FlatBuffers, Cap'n Proto) for large messages

### Memory Management

- **Heap allocation** is expensive: involves system calls and can trigger GC
- **Garbage collection pauses** (JVM, Go, Python) are a primary source of latency spikes — tune GC settings and avoid allocation in hot paths
- **Stack allocation** and **memory pools / arenas** eliminate GC pressure
- **NUMA awareness**: allocate memory on the same NUMA node as the CPU thread accessing it
- For Rust/C++ systems: use custom allocators (mimalloc, jemalloc) for better multi-core scaling

### OS Overhead

- **Virtual memory / TLB misses**: large working sets cause TLB thrashing; use huge pages to reduce TLB pressure
- **Context switching**: each switch costs ~1–10 µs; minimize thread count relative to CPU cores
- **System call overhead**: every syscall crosses kernel/user boundary; batch operations when possible
- **Interrupt processing**: NIC interrupts can steal CPU time from application threads; use CPU affinity to isolate

### Precomputing (Materialized Views)

When a computation is expensive but results are read many times:
- Precompute and store the result (materialized view)
- Invalidate or refresh on write
- Trade write latency for read latency

---

## Wait-Free Synchronization

Use when: shared data must be accessed across threads AND mutex overhead is too high for tail latency requirements.

### Mutex vs. Spinlock vs. Wait-Free

| Mechanism  | Behavior on contention             | When to use                             |
|------------|------------------------------------|-----------------------------------------|
| Mutex      | Blocks thread (OS sleep)           | General purpose; large critical sections |
| Spinlock   | Burns CPU in a loop                | Very short critical sections; no sleeping allowed |
| Wait-free  | All threads always make progress   | Latency-critical paths with shared state |

**Mutexes block the thread**: the OS puts it to sleep and wakes it when the lock is free — expensive (~µs) and causes tail latency spikes under contention.

### Atomics and Memory Barriers

- **Atomic operations** (compare-and-swap, fetch-and-add) are hardware-level instructions that don't require OS involvement
- **Memory barriers / fences** control visibility ordering across CPU cores
- Ordering levels (weakest to strongest): `Relaxed → Acquire/Release → SeqCst`
- Use the weakest ordering that preserves correctness to minimize overhead

### Common Wait-Free Patterns

- **Lock-free ring buffers / SPSC queues**: single-producer single-consumer, zero contention
- **RCU (Read-Copy-Update)**: readers never block, writer creates new version and swaps atomically
- **Epoch-based reclamation**: safe memory reclamation for lock-free structures

**Practical rule**: isolate wait-free components (e.g., request queue, metrics) to keep complexity bounded.

---

## Concurrency Models

### Threads vs. Event-Driven (Async)

| Model        | Latency under load         | Complexity | Good for                          |
|--------------|----------------------------|------------|-----------------------------------|
| Thread-per-request | High (context switching) | Low      | CPU-bound, simple request handling |
| Thread pool  | Medium                     | Medium     | Mixed workloads                   |
| Event loop (async) | Low (no blocking)    | High       | I/O-bound, many concurrent connections |
| Thread-per-core + partitioning | Very low | High | Latency-critical systems         |

### Concurrency vs. Parallelism

- **Concurrency**: multiple tasks making progress (possibly interleaved on one core) — reduces blocking
- **Parallelism**: multiple tasks executing simultaneously on different cores — reduces wall-clock time

Both can reduce latency; they're complementary.

### Data Parallelism vs. Task Parallelism

- **Data parallelism**: same operation on different partitions of data (e.g., parallel map/reduce)
- **Task parallelism**: different independent tasks run concurrently (e.g., parallel DB queries for a single request)

### Transaction Isolation and Latency

Higher isolation levels increase coordination overhead:
| Level             | Anomalies prevented        | Latency impact |
|-------------------|---------------------------|----------------|
| Read uncommitted  | None                      | Lowest         |
| Read committed    | Dirty reads               | Low            |
| Repeatable read   | + Non-repeatable reads    | Medium         |
| Serializable      | All anomalies             | Highest        |

Choose the weakest isolation that is correct for your use case.

### Database Concurrency Control

- **MVCC (Multi-Version Concurrency Control)**: readers don't block writers; low read latency
- **2PL (Two-Phase Locking)**: strict but high lock contention under write-heavy load
- **Optimistic Concurrency Control**: low latency under low contention; retry cost under high contention
