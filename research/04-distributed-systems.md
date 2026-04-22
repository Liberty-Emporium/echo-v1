# Distributed Systems for Web Apps
_Research compiled: 2026-04-22_

---

## 1. Load Balancing & Horizontal Scaling

### Vertical vs Horizontal Scaling
- **Vertical (scale up)**: bigger server — CPU, RAM. Hard limit. Single point of failure.
- **Horizontal (scale out)**: more servers. No hard limit. Requires stateless apps or distributed state.

### Load Balancing Algorithms
| Algorithm | How | Best For |
|---|---|---|
| Round Robin | Request 1→S1, 2→S2, 3→S3, cycle | Equal capacity servers, stateless |
| Weighted Round Robin | S1 gets 2x requests of S2 | Heterogeneous server capacity |
| Least Connections | Route to server with fewest active connections | Long-lived connections (WebSocket) |
| IP Hash | Hash client IP → same server | Sticky sessions without cookies |
| Random | Random server selection | Simple, works well in practice |
| Resource-based | Route based on CPU/memory | Cloud-native, needs health metrics |

### Layer 4 vs Layer 7 Load Balancing
- **L4 (Transport)**: routes based on IP/TCP — fast, no HTTP awareness. AWS NLB, HAProxy L4.
- **L7 (Application)**: routes based on HTTP headers, URL, cookies — can do path-based routing, SSL termination. AWS ALB, Nginx, Traefik.

### Session Stickiness
Problem: stateful apps where session data is on one server.
Solutions:
1. **Sticky sessions (session affinity)** — LB routes same client to same server via cookie. Simple but breaks when server dies.
2. **Centralized session store** — Redis/Memcached. Any server handles any request. Best approach.
3. **JWT** — session state in signed token, no server-side storage needed.

### Health Checks
Load balancers probe backends:
- **Passive**: detect failures via connection errors/timeouts on real traffic
- **Active**: LB sends periodic health-check requests (e.g., `GET /health`)
- Unhealthy backends removed from rotation, re-added when healthy

---

## 2. Event-Driven Systems & Message Queues

### Why Message Queues?
- **Decoupling** — producer doesn't know about consumers
- **Buffering** — handle traffic spikes without dropping requests
- **Async processing** — return response immediately, process in background
- **Retry logic** — dead letter queues for failed messages

### Key Concepts
```
Producer → [Queue/Topic] → Consumer
```

**Point-to-Point (Queue model):**
- Message consumed by exactly one consumer
- Good for: task distribution, work queues
- Example: AWS SQS, RabbitMQ queues

**Publish-Subscribe (Topic model):**
- Message delivered to ALL subscribers
- Good for: event broadcasting, fan-out
- Example: AWS SNS, Kafka topics

### Message Queue Systems Comparison
| System | Model | Throughput | Ordering | Persistence | Use Case |
|---|---|---|---|---|---|
| Redis Streams | Queue/Stream | High | Yes | Configurable | Simple queues, real-time |
| RabbitMQ | Queue/Topic | Medium | Per-queue | Yes | Task queues, routing |
| Apache Kafka | Log/Stream | Very High | Per-partition | Yes (disk) | Event sourcing, analytics |
| AWS SQS | Queue | High | Best-effort | Yes | Cloud-native tasks |
| AWS SNS | Topic | High | No | No | Notifications, fan-out |

### Kafka Architecture
```
Topic: "orders"
├── Partition 0: [msg1, msg3, msg5...]  ← Consumer Group A, Consumer 1
├── Partition 1: [msg2, msg4, msg6...]  ← Consumer Group A, Consumer 2
└── Partition 2: [msg7, msg8...]        ← Consumer Group A, Consumer 3
```
- Messages in a partition are **strictly ordered**
- Consumer groups read from partitions independently
- Messages are retained on disk for configurable period (replay capability)
- High throughput via sequential disk I/O

### At-Most-Once vs At-Least-Once vs Exactly-Once
- **At-most-once**: message may be lost, never duplicated. Fire and forget.
- **At-least-once**: message may be duplicated, never lost. Acknowledge after processing.
- **Exactly-once**: most expensive, requires distributed transactions or idempotency. Kafka supports with transactions.

**Idempotency** — make consumers handle duplicate messages gracefully:
```python
# Idempotent consumer — safe to process same message twice
def process_order(order_id):
    if db.exists(f"processed:{order_id}"):
        return  # already done
    db.process_order(order_id)
    db.set(f"processed:{order_id}", 1)
```

---

## 3. Consistency Models

### CAP Theorem
In a distributed system, you can only guarantee 2 of 3:
- **Consistency** — all nodes see the same data at the same time
- **Availability** — every request gets a response (not necessarily latest data)
- **Partition Tolerance** — system works despite network partition between nodes

Network partitions are **unavoidable** in distributed systems. So real choice is **CP vs AP**:
- **CP** (Consistent + Partition-tolerant): may refuse requests during partition. HBase, Zookeeper, etcd
- **AP** (Available + Partition-tolerant): may serve stale data during partition. DynamoDB, Cassandra, CouchDB

### Strong Consistency
- Read always returns the most recently written value
- All nodes agree on current state before responding
- Requires coordination (consensus protocols: Paxos, Raft)
- **Raft**: used by etcd, CockroachDB. Leader receives writes, replicates to majority before acknowledging.

### Eventual Consistency
- Given no new updates, all replicas will *eventually* converge to same value
- May read stale data temporarily
- Much higher availability and performance
- Used by: DynamoDB, Cassandra, DNS

### Read-Your-Writes Consistency
A weaker guarantee: you always see your own writes, but others may see stale data.
Common in social media — you see your post immediately, others may not.

### CRDT (Conflict-free Replicated Data Types)
Data structures designed for eventual consistency:
- Operations are commutative and associative — can be applied in any order
- G-Counter (grow-only), LWW-Register (last-write-wins), OR-Set
- Used by: Riak, Redis CRDT module, collaborative editors

---

## 4. Failure Handling & Retries

### Failure Modes
- **Crash failure**: process dies cleanly
- **Omission failure**: message lost in network
- **Timing failure**: response too slow
- **Byzantine failure**: incorrect/malicious responses

### Retry Patterns

**Exponential Backoff with Jitter:**
```python
import random, time

def retry_with_backoff(fn, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            wait = (2 ** attempt) + random.uniform(0, 1)  # jitter prevents thundering herd
            time.sleep(wait)
```

**Why jitter?** — Without it, all clients retry at same time after a failure → thundering herd → overwhelms recovering server.

### Circuit Breaker Pattern
Prevents cascading failures when a downstream service is down:

```
CLOSED (normal) → too many failures → OPEN (fail fast, no requests sent)
    ↑                                        ↓ timeout
    └────── success threshold met ── HALF-OPEN (test one request)
```

```python
class CircuitBreaker:
    def __init__(self, threshold=5, timeout=60):
        self.failures = 0
        self.state = 'CLOSED'
        self.last_failure = None
        self.threshold = threshold
        self.timeout = timeout

    def call(self, fn):
        if self.state == 'OPEN':
            if time.time() - self.last_failure > self.timeout:
                self.state = 'HALF-OPEN'
            else:
                raise Exception('Circuit open — fast fail')
        try:
            result = fn()
            if self.state == 'HALF-OPEN':
                self.state = 'CLOSED'
                self.failures = 0
            return result
        except Exception:
            self.failures += 1
            self.last_failure = time.time()
            if self.failures >= self.threshold:
                self.state = 'OPEN'
            raise
```

### Bulkhead Pattern
Isolate failures to prevent system-wide cascade:
- Separate thread pools / connection pools per service
- If service A's thread pool fills up, service B still works
- Named after ship bulkheads that contain flooding to one compartment

### Timeout Everywhere
Never call an external service without a timeout:
```python
import httpx
response = httpx.get(url, timeout=5.0)  # fail after 5s
```
Without timeouts, one slow service can exhaust your thread pool.

### Saga Pattern (Distributed Transactions)
No ACID transactions across microservices. Use Sagas:
- **Choreography**: each service publishes events, others react
- **Orchestration**: central coordinator tells each service what to do
- Each step has a **compensating transaction** to undo if something fails

---

## Key Takeaways
1. **Stateless services** — store sessions in Redis, not in memory. Enables horizontal scaling.
2. **Health endpoints** — every service needs `/health` for LB probing
3. **Async by default** — move expensive work to queues (email, image processing, reports)
4. **Idempotent consumers** — handle duplicate queue messages gracefully
5. **Exponential backoff + jitter** — all retry logic
6. **Circuit breakers** — prevent cascading failures
7. **Timeouts everywhere** — never trust external calls to be fast
8. **Design for failure** — every service will fail; system should degrade gracefully

---
_Sources: Designing Data-Intensive Applications (Kleppmann), AWS Architecture Blog, Martin Fowler's patterns catalog_
