# Hiding Latency Reference

Covers: asynchronous processing, prefetching, optimistic updates, speculative execution, predictive resource allocation.

Use these techniques when you cannot reduce latency further (physical limits, third-party systems, etc.) and need to make it *invisible* to users.

---

## Asynchronous Processing

**Core idea**: Don't wait for slow operations — initiate them and continue doing other work.

### Async vs. Sync vs. Concurrent vs. Parallel

- **Synchronous**: each task completes before the next begins; simple but wastes idle time
- **Concurrent**: multiple tasks interleaved on shared compute (illusion of parallelism)
- **Parallel**: multiple tasks executing simultaneously on different cores
- **Asynchronous**: tasks initiated without blocking; react to completion events

Async doesn't imply parallel — it's about *structuring code* to avoid blocking. You can have single-threaded async (event loop) or multi-threaded async.

### Event Loop

An event loop drives async execution:
1. Poll for I/O readiness (e.g., `epoll`, `io_uring`, `kqueue`)
2. Dispatch callbacks/continuations for ready events
3. Never block in a callback

**Key constraint**: never block the event loop thread. Blocking operations (sync DB calls, CPU-intensive work) must be offloaded to thread pools.

### I/O Multiplexing

OS interfaces for async I/O:
- `epoll` (Linux) / `kqueue` (BSD/macOS): file descriptor readiness notifications
- `io_uring` (Linux 5.1+): full async I/O, including disk — lowest overhead
- `IOCP` (Windows): completion-port model

### Deferring Work

Move non-critical work out of the request path:
- **Message queues** (Kafka, RabbitMQ, SQS): decouple producers from slow consumers
- **Background jobs**: email sending, analytics, thumbnail generation
- **Write coalescing**: batch small writes and flush periodically

**Tradeoff**: deferred work introduces eventual consistency and makes error handling harder.

### Async Error Handling

- Errors surface at completion, not initiation — use callbacks, futures, or structured error channels
- Timeout every async operation; async systems can silently accumulate stuck tasks
- Use circuit breakers for downstream dependencies

### Observability in Async Systems

- Distributed tracing (OpenTelemetry) is essential — request spans cross async boundaries
- Correlate logs with trace IDs to reconstruct causality
- Monitor queue depths as a leading indicator of latency degradation

---

## Predictive Techniques

**Core formula**:
1. Identify operations with latency you cannot reduce
2. Build predictors for *when* results will be needed
3. Initiate operations ahead of time

When prediction is correct → near-zero perceived latency. When wrong → wasted resources, possible cache pollution.

### Prefetching

Fetch data before it's requested.

**Prefetching strategies**:
| Strategy           | How                                      | Best for                         |
|--------------------|------------------------------------------|----------------------------------|
| Pattern-based      | Detect sequential/strided access patterns | Sequential reads, pagination     |
| Semantic           | Use app logic to predict next action      | User navigation flows, wizards   |
| ML-based           | Learn non-obvious access correlations    | Complex user behavior patterns   |

**Prefetching at hardware/OS level**: CPUs have hardware prefetchers for sequential memory access; Linux uses readahead for file I/O — understanding these helps avoid interfering with them.

**Tuning prefetch aggressiveness**:
- Too conservative: miss opportunities, no benefit
- Too aggressive: waste bandwidth, pollute CPU caches, trigger side effects (e.g., read receipts)

**Practical example**: prefetch user-specific data during authentication, before the user lands on the dashboard.

### Optimistic Updates

Apply writes immediately on the client side; sync in the background.

**When it works**: low write-write conflict rate, UX can tolerate occasional rollbacks.

**When it fails**: high contention on shared data; rollback UX is unacceptable.

**Implementation requirements**:
- Conflict detection (version vectors, CRDTs, timestamps)
- Rollback / merge strategy
- UI must reflect pending state and handle conflict gracefully

**Examples**: Google Docs collaborative editing, mobile apps with offline-first sync.

### Speculative Execution

Perform likely-needed operations before they're confirmed necessary.

- If result is used → zero additional latency
- If result is discarded → wasted resources

**Speculative branching**: begin processing the most likely next request before previous response is fully acknowledged.

**Risks**: side effects from speculative execution that shouldn't have happened (e.g., charging a user, sending an email). Only speculate on side-effect-free operations.

### Predictive Resource Allocation

Pre-provision resources (VMs, DB connections, containers) before they're needed.

**Techniques**:
- **Overprovisioning**: maintain spare capacity; eliminates provisioning latency at cost of idle spend
- **Prewarming**: spin up instances during low-traffic windows before predicted traffic spikes
- **Predictive autoscaling**: use time-series forecasting (traffic patterns, cron jobs) to scale ahead of demand rather than reactively

**Failure mode**: misprediction → over- or under-provisioned → cost waste or latency spike.
