---
name: web-dev-mastery
description: Web development best practices, patterns, and tools for building client SaaS applications. Maintained by OWL research, used by both OWL and Bull. Updated from web-dev-future research cron.
---

# Web Dev Mastery — Shared Skill for OWL & Bull

## Purpose
This skill captures proven web development patterns, tools, and workflows for building client SaaS applications. Updated regularly from OWL's research cron jobs. Both OWL and Bull load this skill when building web apps, choosing tech stacks, or doing UI/UX work.

---

## Tech Stack Recommendations (2026)

### For Client SaaS Apps (like Sweet Spot Cakes)
| Layer | Recommended | Why |
|-------|-------------|-----|
| **Frontend** | Next.js 16+ + React 19 | RSC default, 400% faster dev startup, AI-first tooling, Turbopack maturing |
| **Styling** | Tailwind CSS + shadcn/ui | Fast UI building, professional look out of the box |
| **Backend** | Next.js API Routes + tRPC | Type-safe APIs, no separate backend needed, Server Actions for simple cases |
| **Database** | PostgreSQL via Supabase or Neon | Free tier generous, great tooling, edge functions |
| **Auth** | NextAuth.js v5 (Auth.js) | Easy setup, multiple providers |
| **Payments** | Stripe | Industry standard, great docs, Stripe Terminal for in-person |
| **Hosting** | Vercel (simple) or Railway (full-stack) | Easy deploys, auto-scales. NOTE: multi-cloud strategy advised — single-cloud outage risk |
| **ORM** | Drizzle ORM | Type-safe, lighter than Prisma |
| **AI** | OpenRouter API | One key, access to all models |
| **Runtime** | **Bun** for new projects (v1.3+) | 7x faster installs, built-in image API, HTTP/2+3, production-ready. Node.js LTS for enterprise clients |
| **Edge** | Cloudflare Workers + D1 + Durable Objects | Most complete edge platform, Deno Deploy for serverless |

### Key Meta Trends (Mid-2026)
- **AI-agent-first development**: 30% of Vercel deployments now from AI agents (up 1000%)
- **Rust-based tooling** replacing Webpack (Turbopack stable)
- **Server Components** now default rendering paradigm
- **Multi-model AI gateways** (Vercel AI Gateway: 6+ providers)
- **Integrated observability** (OpenTelemetry in SvelteKit, Next.js)
- **Platform resilience awareness** — Google Cloud suspended Railway's production account (8hr outage). Always have multi-cloud fallback
- **Security-first runtimes** — Deno Sandbox for untrusted code, Claw Patrol agent firewall

### For Simple Client Sites
| Layer | Recommended |
|-------|-------------|
| **Site Builder** | Next.js or Astro |
| **CMS** | Sanity or Strapi |
| **Hosting** | Vercel |
| **Forms** | Formspree or Resend |

---

## Project Scaffolding

### Standard Client SaaS Starter
```bash
npx create-next-app@latest client-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd client-app
npm install drizzle-orm @supabase/supabase-js next-auth stripe @trpc/server @trpc/client @trpc/react-query
```

### Key Config Files
See `references/` for:
- `next.config.js` — standard Next.js config with image domains, redirects
- `tailwind.config.ts` — with shadcn/ui theme setup
- `drizzle.config.ts` — database connection config
- `.env.example` — all required environment variables

---

## Deployment Checklist

Every client project should follow this checklist:

- [ ] Environment variables documented in .env.example
- [ ] Database migrations tested
- [ ] Auth flow tested (sign up, sign in, password reset)
- [ ] Payment flow tested with Stripe test mode
- [ ] Mobile responsive verified (test on actual phones)
- [ ] Loading states and error boundaries in place
- [ ] SEO meta tags configured
- [ ] Analytics connected (if applicable)
- [ ] Backup strategy documented and automated
- [ ] Custom domain + SSL configured
- [ ] Multi-cloud failover plan documented

---

## Common SaaS Patterns

### Multi-Tenancy
- Use Supabase Row Level Security (RLS) for data isolation
- Each client gets a `tenant_id` on all tables
- Middleware injects tenant context on every request

### Subscription Billing
- Stripe Checkout for initial signup
- Stripe Customer Portal for self-service management
- Webhook handler for `invoice.paid`, `subscription.updated`, `subscription.deleted`
- Grace period of 7 days before locking access

### Stripe Terminal (In-Person Payments)
- Stripe Terminal SDK for card readers
- Reader registration via Stripe Dashboard
- Works with WisePOS E and other Stripe-certified readers
- Sweet Spot Cakes deployment uses this for counter POS

### Role-Based Access
- Three roles: `owner`, `admin`, `staff`
- Owner has full control, cannot be removed
- Admin can manage staff and settings
- Staff can only access assigned features

---

## Security Essentials

### Supply Chain Security (Critical — May 2026)
- **npm ecosystem under siege**: Mini Shai-Hulud campaign compromised 323 npm packages with 16M weekly downloads
- **Action**: Pin to known-safe versions, run `npm install --ignore-scripts`, rotate ALL credentials regularly
- Use lock files (package-lock.json) and commit them
- Audit dependencies before every deploy: `npm audit`
- Microsoft's `durabletask` PyPI and `node-ipc` were also compromised — check Python packages too

### Standard Security
- All API routes validate auth session
- Rate limiting on auth endpoints
- Input validation with Zod on all forms and API inputs
- CSP headers configured
- HttpOnly cookies for session tokens
- Database backups automated (Supabase does this by default)
- Environment variables NEVER committed to git

---

## File Structure Convention
```
src/
├── app/           # Next.js app router pages
│   ├── (auth)/    # Auth group (login, register)
│   ├── dashboard/ # Protected dashboard routes
│   └── api/       # API routes
├── components/    # React components
│   ├── ui/        # shadcn/ui components
│   └── forms/     # Form components
├── lib/           # Utility functions, configs
├── server/        # Server-side logic, tRPC routers
├── types/         # TypeScript types
└── styles/        # Global styles
```

---

## Cost-Conscious Hardware Strategy

### Key Principles
- Business-grade used hardware is **50-75% cheaper** than new
- **Facebook Marketplace, eBay, OfferUp** are primary sources
- Stripe/Square card readers are **free** with merchant account
- Indoor kiosks can be DIY'd for **$150–500** vs $3,500+ new
- Outdoor kiosks cost **$500–1,500** in custom build materials

### Current Used Pricing (2026)
| Hardware | New | Used/Refurbished |
|----------|-----|-----------------|
| POS terminal / touchscreen PC (Dell OptiPlex, HP ElitePOS) | $500–$1,500 | $100–$400 |
| 15–22" touchscreen monitor | $300–$800 | $75–$250 |
| Receipt printer (Epson TM-T88V) | $180–$250 | $50–$120 |
| Cash drawer (APG Vasario) | $120–$180 | $30–$80 |
| Card reader (Stripe/Square) | $0–$75 | Free with merchant account |
| Barcode scanner (Honeywell) | $80–$130 | $20–$50 |
| Indoor kiosk (DIY: used screen + mini PC) | $900–$3,500 | $150–$500 |
| Outdoor kiosk (custom build) | $3,500–$5,500 | $500–$1,500 |

### Starter Packages (Cost-Effective)
| Package | Includes | Used Cost | New Cost |
|---------|----------|-----------|----------|
| **Basic** (1 kitchen terminal + POS + printer + reader) | Counter setup | $200–$500 | $1,000–$2,000 |
| **Standard** | Basic + indoor kiosk | $350–$1,000 | $2,000–$4,000 |
| **Full** | Standard + outdoor kiosk | $850–$2,500 | $3,500–$6,000 |

---

## Research Sources & Changelog

This skill is updated from OWL's research. Latest research at:
- `/home/lol/Desktop/openclaw/echo-v1/research/web-dev-future-log.json`
- `/home/lol/Desktop/openclaw/echo-v1/research/web-dev-future/` (detailed notes per run)
- `/home/lol/Desktop/openclaw/echo-v1/research/CHANGELOG.md` (all research)

### Recent Research Highlights

**Run 1 — Frontend Frameworks (2026-05-30)**
- React 19.2 stable, React Foundation under Linux Foundation
- Next.js 16.2: 400% faster dev, AI-first tooling (AGENTS.md, Agent DevTools)
- Svelte 5 with runes, new Svelte CLI
- React Compiler v1.0 stable, CRA deprecated
- Vercel AI Gateway: 6+ model providers

**Run 2 — Backend Trends (2026-05-30)**
- Bun 1.3: Image API, HTTP/2+3, 7x faster installs — ready for production
- Deno 2.8: Sandbox for untrusted code, Claw Patrol firewall open-sourced
- Cloudflare Workers most complete edge platform
- 30% of Vercel deployments now agent-driven
- REST resurging for simplicity, SSE > WebSockets when possible

---

## Lessons Learned (From Past Projects)

### From Liberty Emporium Projects
- Always use environment variables for API keys — never in database
- Soft delete (active/inactive flag) preferred over hard delete for client data
- Multi-tenant apps need tenant_id on ALL tables with RLS
- Staff/PIN login is better than passwords for non-technical users
- Railway volume mounts persist data across deploys; local files do not
- Always test WiFi connectivity at premises before abandoning on-site
- Sugar Sammy (Stripe+Flask integration) — documented in `references/stripe-sugar-sammy.md`

### From USB Agent / Liberty Agent Project
- Bootstrap scripts must handle multiple OS environments (Windows/Mac/Linux)
- Puppy Linux (FossaPup64) best for bootable USB agent
- tkinter desktop widget works for customer-facing UI
- Weatherproof kiosk: IP65 enclosure + sunlight-readable screen + heater/cooler
- Card readers obtained free from payment processor with merchant account
