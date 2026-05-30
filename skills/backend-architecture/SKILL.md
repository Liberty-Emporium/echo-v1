---
name: backend-architecture
description: Backend architecture patterns for client SaaS projects. Covers monolith vs microservices, API design, database patterns, caching, queues, and deployment strategies. Updated from OWL research.
---

# Backend Architecture — Shared Skill for OWL & Bull

## Purpose
Architecture patterns and decision frameworks for building client backend systems. Both agents reference this when designing new client apps or scaling existing ones.

## Architecture Decision Framework

### Start Simple: Modular Monolith
For almost every client project, start with a **modular monolith**:
- Single deployable unit (Next.js app)
- Clear module boundaries (orders, auth, inventory, etc.)
- Can be split into microservices later if needed
- No network latency between components
- ACID transactions trivially
- One process, one log — easy debugging

### When to Scale Up
- **Serverless/Edge** → when you need global low-latency (use Cloudflare Workers)
- **Microservices** → when independent scaling is truly needed AND team is large enough
- **Separate API layer** → when multiple frontends (web + mobile + kiosk) share the same API

## API Design

### REST API Best Practices
```
# Nouns, plural, hierarchical
GET    /clients              # List (with pagination)
GET    /clients/123          # Get one
POST   /clients              # Create
PUT    /clients/123          # Full replace
PATCH  /clients/123          # Partial update
DELETE /clients/123          # Soft delete (set active=false)

# Relationships
GET /clients/acme/invoices           # ACME's invoices
GET /clients/acme/invoices/456       # Specific invoice

# Actions (when CRUD doesn't fit)
POST /orders/456/approve
POST /users/123/reset-password
```

### Response Format
```json
// List
{ "data": [...], "total": 150, "page": 1, "perPage": 20 }

// Single item
{ "data": { "id": 123, "name": "Sweet Spot", ... } }

// Error
{ "error": "invalid_input", "message": "Email is required", "details: [...] }
```

### API Versioning
- URL versioning: `/api/v1/clients` (simple, common)
- Header versioning: `Accept: application/vnd.myapp.v2+json` (cleaner URLs)
- For client apps: URL versioning is fine

### When to Use What
| Pattern | Use When |
|---------|----------|
| **REST** | CRUD operations, simple data, mobile/web clients |
| **tRPC** | Full-stack TypeScript, internal APIs |
| **GraphQL** | Complex data relationships, multiple frontends |
| **SSE** | Real-time updates from server (simpler than WebSockets) |
| **WebSockets** | True bidirectional (chat, live collaboration) |

## Database Patterns

### Multi-Tenant Data Isolation
```sql
-- Every table gets tenant_id
CREATE TABLE orders (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  -- ... columns
);

-- Supabase RLS (Row Level Security)
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

### Soft Delete Pattern
```sql
-- Don't actually delete. Set active=false.
ALTER TABLE clients ADD COLUMN active BOOLEAN DEFAULT true;
ALTER TABLE clients ADD COLUMN deleted_at TIMESTAMPTZ;

-- "Delete" = UPDATE clients SET active=false, deleted_at=NOW() WHERE id=$1
-- Query active: SELECT * FROM clients WHERE active=true
```

### Key Conventions
- UUIDs for primary keys (not auto-increment — safer for distributed systems)
- `created_at` and `updated_at` on every table
- `tenant_id` on every table in multi-tenant apps
- Use migrations (Drizzle: `drizzle-kit generate` + `drizzle-kit migrate`)
- Index foreign keys and frequently queried columns

## Caching Strategy

### What to Cache
- User sessions (Supabase handles this)
- Frequently read, rarely changed data (product catalogs, settings)
- API responses with `Cache-Control` headers

### What NOT to Cache
- Real-time data (order status, inventory counts)
- User-specific data (unless per-user cache keys)
- Anything involving money/payments

### Cache Invalidation
- Time-based: `Cache-Control: max-age=3600` (1 hour)
- Event-based: clear cache on write (when order updated, clear order cache)
- Supabase real-time subscriptions can replace some caching needs

## Background Jobs & Queues

### When You Need Queues
- Sending emails (don't block the request)
- Generating reports
- Processing uploads
- Stripe webhook processing

### Options
- **Vercel Workflows** — built-in, simple, good for Next.js on Vercel
- **BullMQ + Redis** — self-hosted, more control
- **Supabase Edge Functions** — serverless, good for simple jobs
- **In-app queue** — for simple cases, a `jobs` table with a worker process

## File Storage

### For Client Apps
- **Supabase Storage** — built-in, S3-compatible, RLS policies
- **Cloudflare R2** — S3-compatible, no egress fees
- **Railway volumes** — for local file storage on Railway deploys

### Never Store Files In
- The database (use file paths/URLs)
- Git repos
- Local filesystem on serverless (ephemeral)

## Error Handling

### API Error Response Format
```json
{
  "error": "validation_failed",
  "message": "Order could not be created",
  "details": [
    { "field": "customer_name", "message": "Required" },
    { "field": "pickup_date", "message": "Must be in the future" }
  ]
}
```

### HTTP Status Codes
| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (validation) |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (no permission) |
| 404 | Not found |
| 409 | Conflict (duplicate, state conflict) |
| 422 | Unprocessable (business logic error) |
| 429 | Rate limited |
| 500 | Server error (log this, alert) |

## Monitoring & Observability

### Minimum Viable Monitoring
- Error tracking: Sentry (free tier: 5K errors/month)
- Uptime: Better Uptime or Hetrixtools (free)
- Logs: Railway/Vercel built-in logs
- Alerts: Telegram notification on critical errors

### Key Metrics to Track
- API response time (p50, p95, p99)
- Error rate (target: <0.1%)
- Active users (daily/weekly)
- Database connection pool usage
- Queue depth (if using queues)
