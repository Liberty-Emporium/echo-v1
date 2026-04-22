# Echo Research Library
_Compiled: 2026-04-22 — Study session with Jay_

Deep technical knowledge base covering advanced web development topics.
Each file is a dense reference — not surface-level, but real engineering depth.

---

## Topics

| # | File | Topic | Key Takeaway |
|---|------|--------|--------------|
| 01 | [Browser Internals](01-browser-internals.md) | DOM, CSSOM, CRP, Event Loop | Animate with transform/opacity; avoid FSL; yield long tasks |
| 02 | [JavaScript Engine](02-javascript-engine.md) | V8, GC, Closures, async/await | Consistent object shapes; parallel Promise.all; handle rejections |
| 03 | [Advanced Networking](03-advanced-networking.md) | HTTP/1-3, TLS, Caching, CDN | HTTP/2 always; cache-hash assets immutable; TLS 1.3; HSTS |
| 04 | [Distributed Systems](04-distributed-systems.md) | Load balancing, Queues, CAP, Failure | Stateless services; idempotent consumers; circuit breakers; timeouts |
| 05 | [Backend Architecture](05-backend-architecture.md) | Monolith/Micro/Serverless, API GW, Observability | Start monolith; structured logs; SLOs; token bucket rate limiting |
| 06 | [Security Engineering](06-security-engineering.md) | XSS, CSRF, SSRF, JWT, CSP | Never trust input; SameSite cookies; parameterized queries; CSP |
| 07 | [Performance Engineering](07-performance-engineering.md) | Core Web Vitals, Profiling, Long Tasks | Measure first; LCP preload; set image dimensions; break long tasks |
| 08 | [WebAssembly](08-webassembly.md) | WASM internals, JS interop, edge | Use for CPU-heavy work; minimize bridge crossings; Rust+wasm-bindgen |
| 09 | [Compilers & Build Systems](09-compilers-build-systems.md) | Bundlers, Tree shaking, AST, Transpilers | Vite for apps; ES modules for tree shaking; learn AST |
| 10 | [AI-Augmented Development](10-ai-augmented-development.md) | Code eval, Self-debugging, Tool use, Planning | Eval > generate; automated test pipelines; plan then small steps |

---

## Skills to Build from This Research (Jay's Ideas)
These topics were flagged for skill development:
- [ ] Performance audit skill (Lighthouse CI integration)
- [ ] Security audit skill (bandit + semgrep + OWASP checks)
- [ ] Self-debugging loop skill (run → read error → targeted fix → verify)
- [ ] Distributed tracing skill (add trace IDs to our apps)
- [ ] CSP header generator skill

---

_Total: ~72,000 bytes of dense technical reference_
_Next session: Review + build skills from this material_
