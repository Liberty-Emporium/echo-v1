# SKILL: Database Design

> PostgreSQL patterns for SaaS, multi-tenant, e-commerce.

## Principles
1. UUIDs for public IDs (never auto-increment)
2. Timestamps on every table (created_at, updated_at, deleted_at)
3. Indexes on FKs and query columns
4. NOT NULL with defaults
5. Constraints at DB level

## Multi-Tenant
```sql
-- Shared schema with tenant_id
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_projects_tenant ON projects(tenant_id);
```

## Users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT,
    name TEXT,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ  -- soft delete
);
CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
```

## Workspaces + Members
```sql
CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    plan TEXT DEFAULT 'free'
);

CREATE TABLE workspace_members (
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role TEXT DEFAULT 'member',
    PRIMARY KEY (workspace_id, user_id)
);
```

## E-Commerce
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id),
    name TEXT NOT NULL,
    price_cents INTEGER NOT NULL,  -- Always cents!
    active BOOLEAN DEFAULT true
);

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL,
    status TEXT DEFAULT 'pending',
    total_cents INTEGER NOT NULL,
    stripe_payment_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Audit Log
```sql
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    workspace_id UUID, user_id UUID,
    action TEXT NOT NULL, resource_type TEXT, resource_id TEXT,
    ip_address INET, created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_audit_workspace ON audit_logs(workspace_id, created_at DESC);
```

## Prisma Equivalent
```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  role      String   @default("user")
  workspaceId String?
  workspace Workspace? @relation(fields: [workspaceId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  deletedAt DateTime?
  @@index([email])
}
```

## Migrations
```bash
npx prisma migrate dev --name description  # Local
npx prisma migrate deploy                  # Production
```
