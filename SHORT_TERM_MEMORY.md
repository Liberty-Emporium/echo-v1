# SHORT_TERM_MEMORY.md — Echo's Working Memory

> Updated at start/end of every work session.

---

## Last Updated: 2026-04-14 04:30 UTC

---

## What We Worked On (Last 24 Hours)

### ✅ Session: 2026-04-14 (Jay's new session)

#### Repo Rename
- ai-api-tracker → jays-keep-your-secrets ✅
- GitHub URL: https://github.com/Liberty-Emporium/jays-keep-your-secrets
- Railway URL unchanged: ai-api-tracker-production.up.railway.app
- All MEMORY/SHORT_TERM_MEMORY updated ✅

#### 5-Hour Self-Education Research Session ✅
- 8 research files created in research/ directory on echo-v1
- Topics: SE roadmaps, Flask architecture, webmaster, security, SaaS pricing, APIs, CI/CD, clean code
- Key files: research/lessons-learned.md (top 10 lessons + action items)

#### SQLite WAL Mode Applied to All 5 Apps ✅
- Contractor Pro AI — WAL pragma added, pushed, 200 ✅
- Pet Vet AI — WAL pragma added, pushed, 200 ✅
- Jay's Keep Your Secrets — WAL pragma added (fixed recursive bug), pushed, 200 ✅
- Liberty Inventory — WAL pragma added, pushed, 302 (redirect = OK) ✅
- Dropship Shipping — WAL pragma added, pushed, 200 ✅

---

## 📋 Top Action Items From Research

### Next Session Priority
1. Add Flask-Limiter to all login routes (5/min) — quick security win
2. Set session cookie flags (secure, httponly, samesite) in all apps
3. Build trial email sequences — days 1, 3, 7, 12, 14

### Medium Term
4. Extract service layer for billing logic
5. Add GitHub Actions test workflows
6. SEO meta tags on all landing pages
7. WebP images + LCP preload on landing pages

### Long Term (Post Court Case)
8. Fly.io migration + Litestream backup
9. Stripe ACH for B2B
10. Full CI/CD pipelines

---

## Railway App URLs
| App | URL | Branch | Overseer |
|-----|-----|--------|---------|
| jay-portfolio | https://jay-portfolio-production.up.railway.app | master | /admin |
| dropship | https://dropship-shipping-production.up.railway.app | main | /overseer |
| liberty-inventory | https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app | main | /overseer |
| contractor-pro | https://contractor-pro-ai-production.up.railway.app | main | /overseer |
| pet-vet | https://pet-vet-ai-production.up.railway.app | main | /overseer |
| jays-keep-your-secrets | https://ai-api-tracker-production.up.railway.app | master | /overseer |
| consignment | https://web-production-43ce4.up.railway.app | ? | /admin/login |

---

## 🧠 Active Lessons (Updated)

1. **sed destroys $ signs** — always use Python for HTML string replacement
2. **Jinja2 eats {# CSS** — wrap with {% raw %}...{% endraw %}
3. **Railway branch varies** — master: jay-portfolio, jays-keep-your-secrets | main: most others
4. **SQLite WAL mode** — set PRAGMA journal_mode=WAL on every connection
5. **Service layer** — business logic NEVER in route handlers
6. **get_db() text replacement bug** — regex replacements can corrupt the function itself if pattern appears inside the function body
7. **Stripe idempotency keys** — always add for money-movement calls
8. **14-day trial + email sequence** — days 1,3,7,12,14 = highest conversion

---
*Auto-updated by Echo · 2026-04-14 04:30 UTC*
