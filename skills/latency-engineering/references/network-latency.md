# Network & Intranode Latency Reference

Covers: TCP/IP stack, kernel bypass, NIC interrupt affinity, multicore topology.

---

## Network Stack Latency

The path a packet takes from NIC to userspace application introduces latency at every layer:

```
NIC receive queue
  → Hardware interrupt / polling (NAPI)
  → Kernel network stack (software interrupt / softirq)
  → Protocol processing (TCP/IP)
  → Socket buffer
  → Application recvmsg() syscall
```

Each handoff can add latency. Key sources:
- **Cross-CPU interrupts**: if NIC interrupt fires on CPU A but app thread runs on CPU B, an IPI (inter-processor interrupt) is required — expensive
- **IRQ coalescing**: batches interrupts to reduce overhead but adds latency per packet
- **Socket buffer copies**: data copied from kernel to userspace on each syscall

### Tuning the Kernel Network Stack

**IRQ affinity** (pin NIC interrupts to specific CPUs):
```bash
# Set NIC IRQs to CPU 0 and 1
echo 3 > /proc/irq/<irq_number>/smp_affinity
```

**Two strategies**:
1. **Isolate interrupt CPUs**: dedicate CPUs to NIC interrupt processing, exclude from app threads — reduces jitter on app threads
2. **Colocate interrupt + app thread**: same CPU handles interrupts and processes the data — avoids cross-CPU wakeup

**Receive Side Scaling (RSS)**: distribute incoming packets across multiple NIC receive queues, each handled by a different CPU — increases parallelism.

---

## Kernel Bypass Networking

For sub-100µs latency requirements, the OS kernel becomes the bottleneck. Kernel bypass moves packet processing to userspace entirely.

### DPDK (Data Plane Development Kit)

- Polls NIC directly from userspace (no interrupts)
- Zero-copy packet access
- Requires dedicated CPU cores for polling
- Used in: network appliances, HFT, telco

### RDMA (Remote Direct Memory Access)

- Transfers data directly between application memory on two machines — no CPU involvement on the receiver
- InfiniBand or RoCE (RDMA over Converged Ethernet)
- Latency: ~1–2 µs for a round-trip (vs ~50 µs for TCP/IP)
- Used in: HPC clusters, high-frequency trading, distributed databases (e.g., FaRM)

### io_uring (Async I/O without syscall overhead)

- Linux 5.1+: submit I/O operations to a ring buffer shared between kernel and userspace
- Batches syscalls — amortizes overhead across many operations
- Works for network and disk I/O

---

## TCP/IP Protocol Latency

### TCP Nagle Algorithm

Nagle buffers small writes to reduce packet count — adds up to 200ms latency for interactive applications.

**Disable for latency-sensitive sockets**:
```c
int flag = 1;
setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(flag));
```

### TCP_QUICKACK

Disables delayed ACKs (which wait up to 200ms before sending):
```c
setsockopt(fd, IPPROTO_TCP, TCP_QUICKACK, &flag, sizeof(flag));
```

### Connection Establishment Overhead

TCP 3-way handshake: 1 round-trip = geographic latency × 2 (worst case).
- Use **connection pools** to amortize this cost
- Use **HTTP/2 or HTTP/3** for multiplexing multiple requests over one connection
- Use **TLS session resumption** to avoid full TLS handshake

---

## Multicore and NUMA Topology

### CPU Cache Hierarchy Impact on Latency

| Cache level | Latency  | Typical size |
|-------------|----------|--------------|
| L1          | ~1 ns    | 32–64 KB     |
| L2          | ~4 ns    | 256 KB–1 MB  |
| L3 (LLC)    | ~10 ns   | 8–32 MB      |
| DRAM        | ~100 ns  | GBs          |

**False sharing**: two threads on different cores write to different variables that happen to share a cache line → constant cache invalidation → 10–100× slower than expected. Fix by padding data structures to cache-line boundaries (typically 64 bytes).

### NUMA (Non-Uniform Memory Access)

On multi-socket servers, memory is attached to specific sockets. Accessing memory on a remote socket costs 2–3× more than local.

**Diagnosis**:
```bash
numastat -p <pid>          # show per-NUMA memory stats
perf stat -e numa-node     # count remote memory accesses
```

**Mitigation**:
- Pin threads to CPUs on the same NUMA node as their data
- Use `numactl --membind=0 --cpunodebind=0 ./app` to bind to NUMA node 0
- Implement thread-per-core with data partitioned per core

### Thread-Per-Core Architecture

Each CPU core gets exactly one application thread and owns a partition of the data. Eliminates:
- Context switching
- Lock contention (each thread owns its data)
- Cross-NUMA memory accesses (if data is allocated on the local socket)

Used in: Seastar framework (Scylla DB), DPDK applications, high-performance networking.
