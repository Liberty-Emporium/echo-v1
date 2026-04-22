# Advanced Backend Architecture
_Research compiled: 2026-04-22_

---

## 1. Monolith vs Microservices vs Serverless

### Monolith
All functionality in one deployable unit.

**Pros:**
- Simple to develop, test, deploy early on
- No network latency between components
- ACID transactions trivially
- Easy debugging (one process, one log)

**Cons:**
- Scales as a unit (can't scale hot path independently)
- Long build/test cycles as it grows
- One bug can crash everything
- Tech stack locked in
- Deployment coordination across teams

**Modular Monolith**: Well-structured monolith with clear module boundaries. Best of both worlds for small/medium teams. Start here.

### Microservices
Independently deployable services, each owning its data.

**Pros:**
- Independent scaling (scale checkout service 10x, not entire app)
- Independent deployment — faster releases per service
- Team autonomy — different teams own different services
- Tech diversity — use best tool for each job

**Cons:**
- Distributed systems complexity (all the CAP/failure problems)
- Network latency between services
- No ACID transactions (need Sagas)
- Service discovery, API versioning, distributed tracing
- Operationally expensive — many things to monitor/deploy

**When to split:**
- Different scaling requirements
- Different deployment cadences
- Organizational boundaries (Conway's Law)
- Truly distinct bounded contexts

**Rule of thumb**: Start with monolith. Extract service when: the pain of coupling exceeds the pain of distribution.

### Serverless (FaaS)
Functions triggered by events, no server management.

**Pros:**
- Zero infrastructure management
- Auto-scaling to zero (no idle cost)
- Pay per invocation
- Fast deployment

**Cons:**
- **Cold starts** — container init latency (50ms-2s depending on runtime)
- **Stateless** — no local state between invocations
- **15-minute max execution** (AWS Lambda) — not for long jobs
- **Vendor lock-in** — function APIs differ across providers
- **Debugging** — distributed traces required, hard to reproduce locally
- **Cost at scale** — often more expensive than containers at high volume

**Best for**: event-driven tasks, webhooks, scheduled jobs, infrequent/spiky workloads

---

## 2. API Gateway Patterns

### What an API Gateway Does
Single entry point for all client requests:
- **Routing** — route `/api/orders` to orders service, `/api/users` to users service
- **Auth** — validate JWT/API key once at gateway, pass identity to services
- **Rate limiting** — throttle per client/IP/API key
- **SSL termination** — TLS at gateway, plain HTTP to internal services
- **Request transformation** — translate REST to gRPC, aggregate responses
- **Caching** — cache responses at gateway
- **Observability** — centralized logging, metrics, tracing

### Gateway vs Service Mesh
- **API Gateway**: north-south traffic (external → internal). L7, per-request logic.
- **Service Mesh** (Istio, Linkerd): east-west traffic (service → service). mTLS, circuit breaking, retries at infrastructure level. Sidecar proxy pattern.

### BFF (Backend for Frontend)
Create separate API gateways tailored to each client type:
- Mobile BFF — returns compact responses, fewer fields
- Web BFF — richer responses, different auth flow
- Partner BFF — rate-limited, monetized API

Avoids the "one size fits all" API problem.

---

## 3. Rate Limiting & Backpressure

### Rate Limiting Algorithms

**Fixed Window Counter:**
```
100 requests per minute window
Window: 00:00-00:59, 01:00-01:59...
Problem: burst at window boundary (50 at 00:59, 50 at 01:00 = 100 in 2 seconds)
```

**Sliding Window Log:**
- Store timestamp of each request, count requests in last N seconds
- Accurate but memory-intensive (store all timestamps)

**Sliding Window Counter:**
- Approximate sliding window using two fixed windows + weighted average
- Memory efficient, close to accurate

**Token Bucket (most common):**
```
Bucket holds N tokens. Refilled at rate R tokens/second.
Each request consumes 1 token. Reject if empty.
Allows bursting up to bucket capacity, then enforced average rate.
```

**Leaky Bucket:**
```
Requests enter a queue (bucket). Processed at fixed rate (drip).
Excess requests dropped if bucket full.
Enforces strict average rate, no bursting.
```

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 47
X-RateLimit-Reset: 1714000000
Retry-After: 30  (on 429 response)
```

### Backpressure
Mechanism for consumers to signal producers to slow down:

```
Producer → [Queue] → Consumer
If queue grows too fast:
- Block producer (synchronous backpressure)
- Drop messages (load shedding)
- Return error to upstream (propagate backpressure)
```

**In HTTP context:**
- Client overwhelms server → server returns `429 Too Many Requests` with `Retry-After`
- Client implements exponential backoff
- Server uses queue with max depth — if full, reject early (`503 Service Unavailable`)

**In streaming (Node.js):**
```js
readable.pipe(writable);  // pipe handles backpressure automatically
// If writable is slow, pipe pauses readable
// Manual:
if (!writable.write(chunk)) {
  readable.pause();
  writable.once('drain', () => readable.resume());
}
```

---

## 4. Observability: Logs, Metrics, Tracing

### The Three Pillars

**Logs** — what happened
```
2026-04-22T18:43:21Z ERROR order.service - Payment failed: stripe_pi=pi_123, amount=4500, err="card_declined"
```
- Structured logging (JSON) — machine parseable
- Log levels: DEBUG < INFO < WARN < ERROR < FATAL
- Correlation ID — attach to every log line to trace a request
- Tools: Datadog, Splunk, ELK Stack (Elasticsearch + Logstash + Kibana), Loki+Grafana

**Metrics** — what's happening now (aggregated numbers)
```
http_requests_total{method="POST", endpoint="/orders", status="200"} 12453
http_request_duration_seconds{p50=0.12, p95=0.45, p99=1.2}
```
- Counters, Gauges, Histograms, Summaries
- Tools: Prometheus + Grafana, Datadog, CloudWatch
- Alert on: error rate > 1%, p99 latency > 2s, queue depth > 1000

**Traces** — how it happened (end-to-end request path)
```
Request: GET /orders/123
├── API Gateway (12ms)
├── Orders Service (45ms)
│   ├── Auth validation (3ms)
│   ├── DB query (38ms)
│   └── Cache lookup (4ms)
└── Response (total: 57ms)
```
- Distributed tracing across services
- Tools: Jaeger, Zipkin, Datadog APM, AWS X-Ray
- Propagate trace context via headers: `X-Trace-Id`, `traceparent` (W3C standard)

### SLI / SLO / SLA
- **SLI** (Service Level Indicator): measurement — "p99 latency", "error rate"
- **SLO** (Service Level Objective): target — "p99 < 500ms, 99.9% of requests"
- **SLA** (Service Level Agreement): contract with consequences — "99.9% uptime or refund"

### Error Budget
```
SLO: 99.9% uptime = 0.1% allowed downtime
Monthly budget: 43.8 minutes of downtime
If budget used up → freeze feature releases, focus on reliability
```

### Health Endpoints
```python
@app.route('/health')
def health():
    return {'status': 'ok', 'db': check_db(), 'cache': check_redis()}

@app.route('/ready')
def ready():
    # Kubernetes readiness — only return 200 when ready to serve traffic
    return {'status': 'ready'}
```

---

## Key Takeaways
1. **Start with modular monolith** — extract microservices only when you feel the pain
2. **API Gateway handles cross-cutting concerns** — auth, rate limiting, logging — not each service
3. **Token bucket rate limiting** — most flexible, handles bursts
4. **Structured JSON logging + correlation IDs** — mandatory for distributed systems
5. **Metrics + alerts** — know when things break before users tell you
6. **Distributed tracing** — essential once you have more than 2 services
7. **Define SLOs** — you can't improve what you don't measure

---
_Sources: Google SRE Book, Sam Newman's Building Microservices, AWS Architecture Docs, Honeycomb observability blog_
