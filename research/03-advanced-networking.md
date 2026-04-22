# Advanced Networking
_Research compiled: 2026-04-22_

---

## 1. HTTP/1.1 vs HTTP/2 vs HTTP/3

### HTTP/1.1 (1997)
- **Text-based** protocol
- **One request per TCP connection** at a time (HOL blocking)
- Workaround: browsers open 6-8 parallel TCP connections per domain
- **Keep-Alive** — reuse TCP connection for multiple requests (persistent connections)
- Problems:
  - Head-of-line blocking — request 2 waits for request 1 to complete
  - Large headers (cookies, user-agent) sent uncompressed on every request
  - No server push

### HTTP/2 (2015)
- **Binary framing** layer — not text
- **Multiplexing** — multiple requests/responses over a SINGLE TCP connection simultaneously
- **Header compression** (HPACK) — headers compressed, indexed, sent as diffs
- **Server Push** — server can send resources before client asks (largely deprecated in practice)
- **Stream prioritization** — hint to server about resource priority
- **Still over TCP** — TCP-level HOL blocking still exists (one lost packet stalls all streams)

```
HTTP/1.1:  [REQ1]→[RES1]  [REQ2]→[RES2]   (sequential or multiple connections)
HTTP/2:    [REQ1][REQ2][REQ3] → (multiplexed over 1 TCP conn) → [RES1][RES2][RES3]
```

### HTTP/3 (2022)
- Built on **QUIC** (Quick UDP Internet Connections) instead of TCP
- QUIC runs over **UDP** — eliminates TCP HOL blocking
- **Stream-level multiplexing** — a lost packet only stalls its own stream, not all streams
- **0-RTT connection establishment** — can resume sessions with no round trips (TLS 1.3 + QUIC)
- **Connection migration** — connections survive IP address changes (great for mobile)
- Built-in encryption (TLS 1.3 mandatory)
- Already deployed by Google, Cloudflare, Facebook

### Practical Implications
| Feature | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| Protocol | Text | Binary | Binary |
| Transport | TCP | TCP | UDP (QUIC) |
| Multiplexing | No | Yes (conn level) | Yes (stream level) |
| Header compression | No | HPACK | QPACK |
| HOL blocking | Both levels | TCP level | None |
| TLS | Optional | Usually | Mandatory |

**When to use what:**
- HTTP/2: virtually all modern web servers — always enable
- HTTP/3: enable on Cloudflare/CDN — client fallback handled automatically
- HTTP/1.1: legacy clients, simple internal services

---

## 2. TLS Handshake & Secure Communication

### TLS 1.2 Handshake (2 round trips)
```
Client → Server: ClientHello (TLS version, cipher suites, random)
Server → Client: ServerHello (chosen cipher, random) + Certificate + ServerHelloDone
Client → Server: ClientKeyExchange (premaster secret, encrypted with server pub key)
                 ChangeCipherSpec + Finished
Server → Client: ChangeCipherSpec + Finished
--- Connection encrypted ---
```
**Cost: 2 RTTs before first byte of data**

### TLS 1.3 Handshake (1 round trip, 0-RTT possible)
```
Client → Server: ClientHello + KeyShare (client's DH public key)
Server → Client: ServerHello + KeyShare + Certificate + Finished
--- Connection encrypted (1 RTT) ---
Client → Server: Finished + HTTP request (data on first client flight)
```

**0-RTT (Session Resumption):** Client sends data in very first message using session ticket from prior connection. Risk: replay attacks on non-idempotent requests.

### Certificate Chain of Trust
```
Root CA (self-signed, in OS/browser trust store)
    └── Intermediate CA (signed by Root)
            └── Your Certificate (signed by Intermediate)
```
Browsers verify the chain up to a trusted root. OCSP / CRL for revocation checking.

### Perfect Forward Secrecy (PFS)
- Uses **ephemeral Diffie-Hellman** key exchange
- Session keys are generated fresh for each connection
- Compromise of server's private key does NOT decrypt past sessions
- TLS 1.3 mandates PFS — ECDHE only

### HSTS (HTTP Strict Transport Security)
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```
- Tells browsers to ONLY connect via HTTPS for max-age seconds
- Preload list: browser comes with HSTS baked in for your domain
- Prevents SSL stripping attacks

---

## 3. Caching Layers

### Cache Hierarchy
```
Browser Cache (L1)
    ↓ miss
Service Worker Cache (if present)
    ↓ miss  
CDN Edge Cache (L2)
    ↓ miss
Origin Server
```

### HTTP Cache Headers
```
Cache-Control: max-age=3600          # cache for 1 hour
Cache-Control: no-cache              # must revalidate with server before using
Cache-Control: no-store              # never cache (sensitive data)
Cache-Control: immutable             # never revalidate (content-hash URLs)
Cache-Control: stale-while-revalidate=60  # serve stale while fetching fresh
ETag: "abc123"                        # content fingerprint for validation
Last-Modified: Wed, 01 Jan 2025...   # time-based validation
Vary: Accept-Encoding, Accept-Language  # cache key includes these headers
```

### Cache Validation
When `max-age` expires:
- **ETag**: `If-None-Match: "abc123"` → server returns 304 Not Modified (no body) or new content
- **Last-Modified**: `If-Modified-Since: ...` → same idea

### Cache Busting
For assets that change:
- Content-hash filenames: `app.a3b4c5d6.js` with `Cache-Control: immutable, max-age=31536000`
- HTML is short-cached or no-cache (it references the hashed assets)

### CDN Caching
CDNs cache at edge nodes globally:
- **Cache-Control: s-maxage** — CDN-specific TTL (overrides max-age for CDNs)
- **Surrogate-Key / Cache-Tag** — tag cached objects for bulk invalidation
- **Stale-While-Revalidate** — CDN serves old content while asynchronously refreshing
- **Purge API** — programmatically invalidate specific URLs or tags

### Service Worker Cache (Offline-first)
```js
// Cache-first strategy
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      return cached || fetch(event.request).then(response => {
        caches.open('v1').then(cache => cache.put(event.request, response.clone()));
        return response;
      });
    })
  );
});
```
Strategies: Cache-first, Network-first, Stale-while-revalidate, Cache-only, Network-only

---

## 4. How CDNs Work (Cloudflare Focus)

### CDN Architecture
```
User (New York)
    ↓ DNS resolves to nearest edge
Cloudflare Edge (NYC PoP) — 300+ PoPs globally
    ↓ cache miss
Origin Server (wherever)
```

### Anycast Routing
CDNs use **anycast** — same IP address announced from multiple locations. BGP routing sends traffic to the nearest PoP automatically.

### What Cloudflare Does
1. **TLS termination at edge** — TLS handshake with user at nearest PoP, separate connection to origin
2. **HTTP/2 & HTTP/3** at edge even if origin only speaks HTTP/1.1
3. **Caching** — static assets cached at edge by Cache-Control headers
4. **DDoS mitigation** — absorbs attacks at edge (anycast spreads load)
5. **WAF** — Web Application Firewall filters malicious requests
6. **Minification & compression** — Gzip/Brotli, auto-minify JS/CSS/HTML
7. **Image optimization** — Polish (lossy/lossless), Mirage (lazy load)
8. **Workers** — run JS at the edge (V8 isolates, not containers)

### Cache-Control for CDNs
```
# Cache at CDN for 1 year, browser for 1 hour
Cache-Control: public, max-age=3600, s-maxage=31536000

# Cloudflare-specific: cache for 1 hour regardless of Cache-Control
CF-Cache-Status: HIT | MISS | EXPIRED | BYPASS
```

### Origin Pull vs Origin Push
- **Pull CDN** (most CDNs): CDN fetches from origin on first miss, caches result
- **Push CDN** (rare): you push content to CDN nodes explicitly

---

## Key Takeaways
1. **Enable HTTP/2 minimum** on all servers — free multiplexing wins
2. **Use CDN for static assets** — cache at edge, content-hash URLs, `immutable`
3. **TLS 1.3** — mandatory for new deployments, 1 RTT vs 2 RTT
4. **Cache-Control strategy**: HTML=no-cache, assets=immutable+content-hash
5. **Vary header** — set correctly or CDN will serve wrong cached variant
6. **HSTS preload** for any production domain handling sensitive data
7. **HTTP/3 via CDN** — let Cloudflare/Fastly handle it, origin can still be HTTP/2

---
_Sources: MDN HTTP caching guide, Cloudflare blog, HTTP/2 RFC 7540, HTTP/3 RFC 9114, QUIC RFC 9000_
