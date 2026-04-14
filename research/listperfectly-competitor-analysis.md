# List Perfectly — Competitor Analysis & Build Plan
> Researched: 2026-04-14

---

## What List Perfectly Does (The Target)

**URL:** https://listperfectly.com  
**Tagline:** "The #1 Way to Crosslist and Grow Your Business"  
**Core Value:** AI-powered crosslisting for resellers — create one listing, publish everywhere

### Key Features
- AI Listing Assistant — creates titles, descriptions, keywords from photos
- Crosslisting to 10+ marketplaces (eBay, Poshmark, Etsy, Mercari, Depop, etc.)
- Bulk actions — import, crosslist, delist, relist, mark sold
- Auto Sales Detection & Delist — syncs sold status across platforms
- Inventory Management & Analytics dashboard
- Background Remover (via PhotoRoom)
- Pricing Tool (Google Lens + ChatGPT + Barcode Lookup)
- Community ("Listing Party" live events)
- 24/7 human support

### Pricing (estimated from competitor research)
- Simple: ~$29/mo
- Business: ~$49/mo  
- Teams: ~$99/mo

---

## Competitors Mapped

| Product | Users | Price | Key Differentiator |
|---------|-------|-------|-------------------|
| **List Perfectly** | Large | $29-99/mo | AI + community + most platforms |
| **Crosslist.io** | 50,000+ | $29-45/mo | 11+ marketplaces, password-free |
| **PrimeLister** | 10,000+ | ~$9-29/mo | Poshmark automation specialist |
| **Vendoo** | Growing | ~$12-49/mo | Analytics heavy |
| **ListCross** | Growing | Unknown | AI-first, claims 156% more sales |

---

## Our Version — "List Liberty" (Working Title)

### Our Advantage Over List Perfectly
1. **Cheaper** — they charge $29-99/mo; we target $19.95/mo starter
2. **AI-first** — OpenRouter AI for every listing, not just premium tiers
3. **Built for thrift/resellers** — we understand Liberty Inventory users
4. **Same stack** — Flask + SQLite + Railway, fast to build and deploy
5. **Multi-tenant from day 1** — use Liberty Inventory's SaaS blueprint

### MVP Feature Set (Phase 1)

#### Core
- [ ] User registration + 14-day free trial
- [ ] "Create Listing" form — title, description, price, condition, photos
- [ ] AI title/description generator from product details or photo description
- [ ] Listing catalog (manage all listings in one place)
- [ ] Export listing to clipboard-ready format per platform

#### Phase 2 (post-launch)
- [ ] Direct posting to eBay via API
- [ ] Direct posting to Poshmark (browser automation)
- [ ] Direct posting to Mercari
- [ ] Auto delist when sold
- [ ] Inventory sync dashboard
- [ ] Background remover (via remove.bg API or rembg Python lib)

#### Phase 3 (scale)
- [ ] Etsy, Depop, Facebook Marketplace
- [ ] Bulk import from CSV
- [ ] Sales analytics dashboard
- [ ] Mobile app (React Native or PWA)

### Pricing Strategy
| Plan | Price | Listings/mo | AI Credits | Platforms |
|------|-------|-------------|------------|-----------|
| Starter | $19.95/mo | 100 | 100 AI generates | 2 |
| Pro | $39.95/mo | Unlimited | Unlimited | All |
| Teams | $79.95/mo | Unlimited | Unlimited | All + team seats |

14-day free trial, no credit card required.

---

## Technical Architecture

### Stack (same as all our apps)
- **Backend:** Flask + SQLite (WAL mode)
- **AI:** OpenRouter (ai_helper.py with rate limit fix)
- **Auth:** Multi-tenant SaaS blueprint from Liberty Inventory
- **Deploy:** Railway + /data volume
- **Payments:** Stripe

### Database Schema (MVP)
```sql
-- Users (multi-tenant)
users (id, email, password_hash, plan, trial_ends_at, created_at)
tenants (id, slug, name, owner_id, stripe_customer_id)

-- Listings
listings (id, tenant_id, title, description, price, condition, 
          category, brand, size, photos_json, status, created_at)

-- Platform Posts
platform_posts (id, listing_id, platform, external_id, 
                posted_at, status, url)

-- AI Usage
ai_usage (id, tenant_id, action, tokens_used, model, created_at)
```

### Key Routes
```
GET  /                    → Landing page
GET  /signup              → Trial signup  
GET  /dashboard           → Listing catalog
GET  /listings/new        → Create listing form
POST /listings/create     → Save + AI generate
POST /listings/<id>/ai    → Regenerate AI content
POST /listings/<id>/post  → Post to platform
GET  /listings/<id>/edit  → Edit listing
GET  /analytics           → Sales dashboard
GET  /settings            → Account + billing
```

---

## Go-To-Market

### Target Customer
- Thrift store resellers (direct overlap with Liberty Inventory users)
- eBay/Poshmark side-hustlers (10M+ in US)
- Small resale businesses (1-10 employees)

### Acquisition Strategy
1. **Liberty Inventory upsell** — existing customers get first access
2. **Reddit** — r/Flipping, r/Poshmark, r/Mercari (2.5M+ combined members)
3. **TikTok/YouTube** — "How I crosslist 100 items in 1 hour" content
4. **SEO** — "list perfectly alternative", "cheap crosslisting app"

### Revenue Projection
| Month | Customers | MRR |
|-------|-----------|-----|
| 1 | 10 | $200 |
| 3 | 50 | $1,000 |
| 6 | 200 | $4,000 |
| 12 | 500 | $10,000 |

---

## Build Timeline

- **Week 1:** Core auth + listing CRUD + AI generation
- **Week 2:** Platform export templates + polish
- **Week 3:** eBay API integration + beta launch
- **Week 4:** Poshmark + Mercari + Stripe billing

**Total to MVP:** ~4 weeks of focused building

---

*Researched by Echo · 2026-04-14*
