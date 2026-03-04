# Data Latency Reference

Covers: colocation, replication, partitioning, caching.

---

## Colocation

**Pattern**: Bring compute and data physically closer together.

**Internode (distributed systems)**
- Geographic latency is often the dominant factor — cannot be optimized away without moving data
- NYC → London: 60–150 ms. London → Sydney: ~250 ms
- **Last-mile** adds 10–50 ms even after geographic colocation (Wi-Fi, ISP infrastructure)
- Use CDNs and edge deployments (e.g., Cloudflare Workers) to push content near users
- Edge types: *near edge* (nearby datacenter), *far edge* (user-controlled infra/IoT)

**Intranode (multicore systems)**
- LLC access: ~10 ns. DRAM: ~100 ns. Disk: ~10–100 µs
- **NUMA**: on multi-socket machines, remote memory access is 2–3× slower than local
- Strategy: thread-per-core + partition data per CPU core to maximize LLC hits
- Colocate interrupt processing with application threads (or isolate to dedicated CPUs) to reduce NIC→userspace latency

---

## Replication

**Pattern**: Maintain multiple consistent copies; serve reads from nearest copy.

**Why it helps latency**: Readers access local replica instead of distant primary.

**Consistency tradeoffs**:
| Model                 | Latency       | Guarantee                              |
|-----------------------|---------------|----------------------------------------|
| Strong (linearizable) | High          | Clients see single consistent view     |
| Eventual consistency  | Low           | Clients may see stale data             |

**Approaches**:
- **Single-leader**: writes go to leader, reads from replicas; simple but leader is bottleneck
- **Multi-leader**: multiple write points; higher availability, harder conflict resolution
- **Leaderless (e.g., Dynamo-style)**: writes/reads to quorum; flexible latency tuning

**Replication protocols**: Raft (understandable), Paxos (proven), Viewstamped Replication

**When NOT to replicate**: large datasets where storage cost is prohibitive; strong consistency needs make latency worse than not replicating

---

## Partitioning (Sharding)

**Pattern**: Divide data into independent subsets to reduce synchronization overhead.

**Why it helps**: Concurrent accesses to different partitions don't block each other.

**Strategies**:
- **Horizontal (sharding)**: rows/documents split by partition key
  - *Key hash*: uniform distribution, good for random access, bad for range queries
  - *Key range*: good for range scans, risk of hot partitions
- **Vertical**: split by columns; used in OLAP/columnar stores for compression + read efficiency
- **Hybrid**: combine both for mixed OLTP/OLAP workloads

**Partition key selection**:
- Prefer **high cardinality** keys to distribute load evenly
- Low cardinality → skewed partitions → hot spots → high tail latency
- Skewed workloads may require sub-partitioning or dedicated resources for hot partitions

**Downsides**: cross-partition transactions become complex or impossible; joins require scatter-gather; repartitioning is operationally expensive

---

## Caching

**Pattern**: Keep a temporary copy of hot data closer to the access point.

**When to choose caching over replication/partitioning**:
- Cannot change the underlying system
- Use case is simple key–value lookups
- Storage/compute constraints prevent full replication

**Core metric**: **cache hit ratio**. A low hit ratio can make things *worse* than no cache (overhead of misses adds up).

**Cache miss strategy**:
| Strategy         | Who fetches on miss | Latency on miss      | Notes                             |
|------------------|---------------------|----------------------|-----------------------------------|
| Cache-aside      | Application         | App → DB latency     | Simple; no transaction support    |
| Read-through     | Cache               | Cache → DB latency   | Hides miss from app; more complex |
| Write-through    | Cache (sync)        | DB commit latency    | Consistent; slow writes           |
| Write-behind     | Cache (async)       | Near-zero write lat  | Risk of data loss on cache crash  |

**Cache replacement policies**:
- **LRU** (Least Recently Used): default; good for temporal locality
- **LFU** (Least Frequently Used): good for frequency-based access patterns
- **SIEVE**: recent research showing simpler + competitive with LRU
- **TTL (time-based)**: evict after fixed age; simple; stale data risk

**Negative caching**: cache the fact that a lookup returned nothing, to avoid repeated expensive misses.

**Tail latency caveat**: cache-aside has bimodal latency — fast hits, slow misses. Geographic distance to backing store still determines miss latency.

**Consistency hazards**: concurrent cache misses can cause thundering herd; cache + DB are not transactional unless explicitly designed so.
