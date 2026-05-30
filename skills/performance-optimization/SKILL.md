# SKILL: Performance Optimization

> Make any web app fast — Core Web Vitals, caching, bundling, edge rendering.

## Core Web Vitals Targets (2025)

| Metric | Good | Needs Work | Bad |
|--------|------|------------|-----|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5-4s | > 4s |
| **INP** (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |
| **TTFB** (Time to First Byte) | < 800ms | 800-1800ms | > 1800ms |
| **FCP** (First Contentful Paint) | < 1.8s | 1.8-3s | > 3s |

## Frontend Optimization

### Image Optimization (Biggest Win)
```tsx
// Next.js — automatic optimization
import Image from "next/image"

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority          // LCP image — load immediately
  quality={85}
  placeholder="blur" // Blur-up placeholder
/>

// For external images, add to next.config.js:
// images: { domains: ["cdn.example.com"] }
```

### Code Splitting
```tsx
// Dynamic imports for heavy components
import dynamic from "next/dynamic"

const Chart = dynamic(() => import("@/components/Chart"), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Don't render on server if not needed
})

// Route-based splitting (automatic in Next.js App Router)
// Each page is automatically code-split
```

### Font Optimization
```ts
// next/font — self-hosted, zero layout shift
import { Inter } from "next/font/google"

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
})
```

### Bundle Analysis
```bash
# Analyze bundle size
npm install @next/bundle-analyzer
# next.config.js:
const withBundleAnalyzer = require("@next/bundle-analyzer")({ enabled: process.env.ANALYZE === "true" })
module.exports = withBundleAnalyzer(nextConfig)

# Run: ANALYZE=true npm run build
```

## Backend Optimization

### Database Query Optimization
```python
# BAD: N+1 query problem
projects = await Project.find_all()
for project in projects:
    project.owner = await User.find(project.user_id)  # N+1!

# GOOD: Join in one query
projects = await Project.find_all(include=[Project.owner])

# GOOD: Select only needed columns
users = await User.find_all(select=[User.id, User.name, User.email])

# Add indexes for common queries
# CREATE INDEX idx_projects_user_id ON projects(user_id);
```

### Caching Strategy
```python
# Redis caching
import redis
import json

cache = redis.Redis(host="localhost", port=6379)

async def get_projects(user_id: str):
    cache_key = f"projects:{user_id}"
    
    # Try cache first
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Fetch from DB
    projects = await Project.find_all(user_id=user_id)
    
    # Cache for 5 minutes
    cache.set(cache_key, json.dumps(projects), ex=300)
    
    return projects

# Invalidate on mutation
async def create_project(user_id: str, data: dict):
    project = await Project.create(user_id=user_id, **data)
    cache.delete(f"projects:{user_id}")  # Invalidate cache
    return project
```

### Response Compression
```python
# FastAPI
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Next.js — automatic with Vercel
```

### Connection Pooling
```python
# SQLAlchemy async with connection pooling
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # Max connections
    max_overflow=10,       # Extra connections under load
    pool_timeout=30,       # Wait time for connection
    pool_recycle=3600,     # Recycle connections after 1hr
)
```

## CDN & Edge

### Cloudflare (Free Tier)
- CDN for static assets
- Image optimization (Polish, WebP)
- DDoS protection
- Workers for edge logic
- Analytics (privacy-friendly)

### Vercel Edge
```ts
// middleware.ts — run at edge
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  // A/B testing, geo-routing, auth checks at edge
  const country = request.geo?.country
  if (country === "US") {
    return NextResponse.rewrite(new URL("/us" + request.nextUrl.pathname, request.url))
  }
}

export const config = { matcher: ["/((?!api|_next|static).*)"] }
```

## Performance Monitoring

### Lighthouse CI
```yaml
# .github/workflows/lighthouse.yml
- name: Lighthouse CI
  uses: treosh/lighthouse-ci-action@v10
  with:
    urls: |
      https://yoursite.com/
      https://yoursite.com/pricing
    budgetPath: ./lighthouse-budget.json
```

### Real User Monitoring (RUM)
```ts
// lib/analytics.ts — send Web Vitals to your analytics
import { onCLS, onFID, onLCP, onTTFB, onINP } from "web-vitals"

function sendToAnalytics(metric: Metric) {
  fetch("/api/analytics/vitals", {
    method: "POST",
    body: JSON.stringify(metric),
    keepalive: true,
  })
}

onCLS(sendToAnalytics)
onFID(sendToAnalytics)
onLCP(sendToAnalytics)
onTTFB(sendToAnalytics)
onINP(sendToAnalytics)
```

## Quick Performance Checklist
- [ ] Images optimized (WebP, lazy loading, correct sizes)
- [ ] Fonts self-hosted with `font-display: swap`
- [ ] JavaScript code-split by route
- [ ] CSS purged (Tailwind JIT does this)
- [ ] API responses cached (Redis)
- [ ] Database queries indexed
- [ ] CDN for static assets
- [ ] Gzip/Brotli compression
- [ ] Server-side rendering for content pages
- [ ] Preload critical resources
- [ ] Minimize third-party scripts
- [ ] Use `next/image` for all images
- [ ] Set proper cache headers
