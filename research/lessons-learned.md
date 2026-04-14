# Echo's Key Lessons — 5-Hour Self-Education Session
**Date:** 2026-04-14 | The day I got smarter.

---

## 🔥 The Top 10 Things I Learned Today

### 1. Service Layer is Non-Negotiable
Our current apps mix business logic in routes. This is the #1 thing that makes codebases unmaintainable past Month 2. Every new feature I build goes in a service layer. Every bug fix I touch, I extract to services.

### 2. SQLite WAL Mode is Not Optional in Production
Default SQLite is tuned for embedded devices. Without WAL mode, readers block writers and the API locks under load. I must add this to ALL our apps immediately:
```python
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA synchronous=NORMAL")
conn.execute("PRAGMA foreign_keys=ON")
```

### 3. Security is a Layered System, Not a Feature
OWASP Top 10 in Flask comes down to 5 things:
- SQLAlchemy ORM (no raw SQL with user input)
- Flask-Limiter (rate limit login endpoints)
- CSRF protection (Flask-WTF)
- Session security flags (secure, httponly, samesite)
- Never hardcode secrets — always os.environ

### 4. Core Web Vitals Directly Affect SEO Rankings
Google ranks us based on LCP, INP, and CLS scores. Our landing pages need:
- WebP images
- Preloaded LCP element
- No lazy loading on above-the-fold images
- Inline critical CSS
- Deferred JS

### 5. Stripe Idempotency Keys Prevent Double-Charges
Every Stripe call that creates money movement needs an idempotency key.
Format: `f"action_{user_id}_{resource_id}"` — prevents duplicate charges on retry.

### 6. Pricing Psychology Makes a Big Difference
- Price anchoring: show highest tier first
- Decoy pricing: 3 tiers where middle one looks bad makes top tier look great
- Loss aversion in copy: "Don't lose your progress" beats "Save your progress"
- 14-day trial is the sweet spot

### 7. Every API Should Be Versioned From Day One
`/api/v1/` prefix costs nothing to add. Removing it later costs everything.

### 8. CI/CD Pays for Itself Immediately
GitHub Actions is free for public repos, very cheap for private.
One workflow file per repo: run tests → if pass → deploy.
Broken code never reaches production again.

### 9. SQLite Is Fine Until It Isn't
Under 500 write TPS, under 100GB, read-heavy apps: SQLite wins.
Over those thresholds or needing multi-region: PostgreSQL.
Our apps are well within SQLite territory for now.
When we migrate to Fly.io → add Litestream for backup.

### 10. Freemium Converts at 2-5%, Trials Convert at 15-25%
Our 14-day trial model is correct. Free plans are hard to sustain.
The key is the email sequence during trial — days 1, 3, 7, 12, 14.
We don't have this automated yet. This is lost revenue.

---

## 🛠️ Action Items for Our Apps (Priority Order)

### Immediate (Next Session)
- [ ] Add SQLite WAL PRAGMA to all 6 apps at DB connection init
- [ ] Add Flask-Limiter to all login routes (5/min limit)
- [ ] Set session cookie flags in all apps (secure, httponly, samesite)
- [ ] Add `/api/v1/` prefix to all API routes (or plan for it)

### Short Term (Next 2 Weeks)
- [ ] Write test files for auth + overseer in each app
- [ ] Add GitHub Actions test workflow to each repo
- [ ] Build trial email sequences (7-email drip during trial)
- [ ] Implement onboarding email: day 1, 3, 7, 12, 14

### Medium Term (Next Month)
- [ ] Extract service layer for billing logic in each app
- [ ] Add background email sending (threading) to avoid route delays
- [ ] Add SEO meta tags + sitemap.xml to all landing pages
- [ ] Optimize images on all landing pages (WebP, preload LCP)

### Long Term (Post Court Case)
- [ ] Migrate to Fly.io + add Litestream backup
- [ ] Add Stripe ACH for B2B clients (massive fee savings)
- [ ] Add PostgreSQL Row Level Security
- [ ] Full CI/CD pipeline with auto-deploy

---

## 📚 Resources Worth Revisiting

- roadmap.sh — best visual roadmaps for any tech role
- realpython.com/github-actions-python — CI/CD tutorial
- flask.palletsprojects.com/patterns — official Flask patterns
- testdriven.io — Flask testing deep dives
- launchstack.space — Flask SaaS structure (excellent)
- corewebvitals.io/ultimate-checklist — performance checklist
- docs.stripe.com/billing/subscriptions/webhooks — webhook events

---

## 🧠 Permanent Rules I'm Adding to My Practice

1. **Every new Flask app starts with application factory pattern**
2. **Every login route gets rate limiting on day 1**
3. **Every SQLite connection sets WAL pragma**
4. **Every Stripe call gets an idempotency key**
5. **Every API gets /api/v1/ prefix**
6. **Every feature gets at least one test**
7. **Every deploy has a rollback plan**
8. **Every tenant query includes tenant_id filter**
9. **Every secret lives in environment variables**
10. **Every landing page has proper meta tags and CTA**
