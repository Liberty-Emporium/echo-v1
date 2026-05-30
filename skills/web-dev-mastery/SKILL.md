---
name: web-dev-mastery
description: Web development best practices, patterns, and tools for building client SaaS applications. Maintained by OWL research, used by both OWL and Bull.
---

# Web Dev Mastery — Shared Skill for OWL & Bull

## Purpose
This skill captures proven web development patterns, tools, and workflows for building client SaaS applications. Updated regularly from OWL's research runs.

## Tech Stack Recommendations (2026)

### For Client SaaS Apps (like Sweet Spot Cakes)
| Layer | Recommended | Why |
|-------|-------------|-----|
| **Frontend** | Next.js 15 + React 19 | Server components, great DX, huge ecosystem |
| **Styling** | Tailwind CSS + shadcn/ui | Fast UI building, professional look out of the box |
| **Backend** | Next.js API Routes + tRPC | Type-safe APIs, no separate backend needed |
| **Database** | PostgreSQL via Supabase or Neon | Free tier generous, great tooling |
| **Auth** | NextAuth.js v5 (Auth.js) | Easy setup, multiple providers |
| **Payments** | Stripe | Industry standard, great docs |
| **Hosting** | Vercel or Railway | Easy deploys, auto-scales |
| **ORM** | Drizzle ORM | Type-safe, lighter than Prisma |
| **AI** | OpenRouter API | One key, access to all models |

### For Simple Client Sites
| Layer | Recommended |
|-------|-------------|
| **Site Builder** | Next.js or Astro |
| **CMS** | Sanity or Strapi |
| **Hosting** | Vercel |
| **Forms** | Formspree or Resend |

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

## Deployment Checklist

Every client project should follow this checklist:

- [ ] Environment variables documented in .env.example
- [ ] Database migrations tested
- [ ] Auth flow tested (sign up, sign in, password reset)
- [ ] Payment flow tested (if applicable)
- [ ] Mobile responsive verified
- [ ] Loading states and error boundaries in place
- [ ] SEO meta tags configured
- [ ] Analytics connected (if applicable)
- [ ] Backup strategy documented
- [ ] Custom domain + SSL configured

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

### Role-Based Access
- Three roles: `owner`, `admin`, `staff`
- Owner has full control, cannot be removed
- Admin can manage staff and settings
- Staff can only access assigned features

## Security Essentials

- All API routes validate auth session
- Rate limiting on auth endpoints
- Input validation with Zod on all forms and API inputs
- CSP headers configured
- HttpOnly cookies for session tokens
- Database backups automated (Supabase does this by default)

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

## Cost-Conscious Hardware Strategy

See `references/hardware-pricing.md` for current used/refurbished pricing.

Key principles:
- Business-grade used hardware (Dell, HP, Epson) is 50-75% cheaper than new
- Facebook Marketplace, eBay, OfferUp are primary sources
- Stripe/Square card readers are often free with merchant account
- Indoor kiosks can be DIY'd for $150-500 vs $3,500+ new
- Outdoor kiosks cost $500-1,500 in custom build materials

## Research Sources
This skill is updated from OWL's web dev research runs. Latest research logged at:
`/home/lol/Desktop/openclaw/echo-v1/research/web-dev-future-log.json`
