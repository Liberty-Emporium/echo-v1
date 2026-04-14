# Feature Library — Echo & Jay's Building Blocks
> Every reusable feature we've built. Use these names when talking to each other.
> "Add the **AI Chat Widget** and **Image Analyzer** to this app" = I know exactly what to build.

---

## 🤖 AI Features

### 1. AI Content Generator
**What it is:** Button that sends item details to AI and gets back a title, description, and tags written by AI.
**You've seen it in:** List It Everywhere (✨ AI Generate button)
**The call:** User clicks → AI writes → fields auto-fill
**Trigger phrase:** *"Add AI Generate"* or *"AI content writer"*

---

### 2. Image Analyzer
**What it is:** User uploads or snaps a photo → AI vision reads the image → auto-fills the entire form (title, brand, condition, price, description, tags, category).
**You've seen it in:** List It Everywhere (📷 Photo AI button)
**The call:** File picker or camera → base64 → vision model → form population
**Trigger phrase:** *"Add Image AI"* or *"Photo to listing"*

---

### 3. AI Chat Widget
**What it is:** Floating chat bubble (bottom-right corner) on every page. User opens it and talks to an AI assistant in real time. Maintains conversation history. Has quick-ask buttons.
**You've seen it in:** List It Everywhere (Liz — Reselling Coach)
**The call:** `/api/chat` endpoint + JS chat UI + persona system prompt
**Trigger phrase:** *"Add AI chat"* or *"Add a chat assistant"*

---

### 4. AI Listing Exporter
**What it is:** Takes one listing and formats it correctly for 10+ different platforms (eBay, Poshmark, Mercari, etc.) with one click. Copy-paste ready.
**You've seen it in:** List It Everywhere (Export buttons)
**The call:** Template per platform → formatted text → copy to clipboard
**Trigger phrase:** *"Add platform exporter"* or *"crosslist formatter"*

---

### 5. AI Health Score / Audit
**What it is:** AI reads your app's code or a deployed URL and gives a score (0-100) with a fix list.
**You've seen it in:** Custom skill `app-auditor`, `seo-analyzer`
**Trigger phrase:** *"Audit this app"* or *"Give it a score"*

---

## 🔐 Auth & User Management

### 6. Single-Tenant Auth
**What it is:** One user = one account. Login, signup, logout, session cookies, password hashing. No organizations.
**You've seen it in:** Pet Vet AI, Contractor Pro AI, Keep Your Secrets
**Trigger phrase:** *"Add basic auth"* or *"single user login"*

---

### 7. Multi-Tenant Auth
**What it is:** Each signup creates an isolated **Tenant** (organization). Users belong to a tenant. Tenants can't see each other's data.
**You've seen it in:** Liberty Inventory, List It Everywhere, Dropship Shipping
**The tables:** `tenants`, `users` (with `tenant_id`)
**Trigger phrase:** *"Make it multi-tenant"* or *"SaaS auth"*

---

### 8. Role-Based Access Control (RBAC)
**What it is:** Users have roles — `owner`, `admin`, `member`, `overseer`. Each role sees different pages and can do different things.
**You've seen it in:** Liberty Inventory (overseer/client), List It Everywhere (overseer/owner)
**Trigger phrase:** *"Add roles"* or *"different permission levels"*

---

### 9. Trial System
**What it is:** New signups get X days free (usually 14). After trial ends, they hit a paywall and must upgrade. Trial expiry is checked on every protected page.
**You've seen it in:** Liberty Inventory, List It Everywhere, Consignment Solutions
**The field:** `trial_ends_at` on tenant
**Trigger phrase:** *"Add a free trial"* or *"14-day trial"*

---

### 10. Rate Limiter
**What it is:** Counts requests per IP address per time window. Blocks too many login attempts, form submissions, AI calls. Stored in SQLite — no Redis needed.
**You've seen it in:** Every app (login, signup, AI routes)
**Trigger phrase:** *"Add rate limiting"* or *"prevent abuse"*

---

## 🏢 SaaS Infrastructure

### 11. Overseer Panel
**What it is:** Hidden admin dashboard only accessible to the `overseer` role. Shows ALL tenants, their plan, usage stats, MRR. Can suspend/activate accounts, change plans, impersonate any user.
**You've seen it in:** Liberty Inventory, List It Everywhere
**URL:** `/overseer`
**Trigger phrase:** *"Add overseer panel"* or *"admin dashboard for all customers"*

---

### 12. Client Impersonation
**What it is:** Overseer clicks "View As" on any tenant and gets logged in as that user — sees exactly what they see. Used for support and debugging.
**You've seen it in:** Liberty Inventory, List It Everywhere
**Trigger phrase:** *"Add impersonation"* or *"log in as customer"*

---

### 13. Stripe Billing
**What it is:** Connects to Stripe for subscription payments. Handles signup → trial → paid → cancel → webhook events. Updates tenant plan automatically.
**You've seen it in:** Liberty Inventory (Stripe integrated)
**Trigger phrase:** *"Add Stripe"* or *"add payments"*

---

### 14. Plan Enforcement
**What it is:** Each plan has limits (listings, AI credits, seats). Every action checks if the user is within their plan limits before proceeding. Upgrade wall shows if they're over.
**You've seen it in:** List It Everywhere (`PLANS` dict, limit checks)
**Trigger phrase:** *"Add plan limits"* or *"enforce subscription tiers"*

---

## 🗄️ Database Patterns

### 15. WAL Mode SQLite
**What it is:** SQLite configured for production — WAL journal mode, NORMAL sync, foreign keys on, busy timeout. Handles concurrent reads without locking.
**You've seen it in:** Every app (applied in the big security upgrade session)
**The 4 lines:** `PRAGMA journal_mode=WAL`, `synchronous=NORMAL`, `foreign_keys=ON`, `busy_timeout=5000`
**Trigger phrase:** *"Production SQLite"* or *"WAL mode"*

---

### 16. Persistent Volume (Railway)
**What it is:** A Railway volume mounted at `/data` so the SQLite database survives deploys. Without this, every deploy wipes your data.
**You've seen it in:** Every Railway app
**Trigger phrase:** *"Add persistent storage"* or *"don't wipe my data"*

---

### 17. Custom Fields / Form Builder
**What it is:** Users can add their own fields to a form (text, dropdown, number, checkbox). Fields are defined in a `custom_fields` DB table. Values saved as JSON on each record.
**You've seen it in:** List It Everywhere (Settings → Fields)
**Trigger phrase:** *"Add custom fields"* or *"let users build their own form"*

---

## 📊 Analytics & Monitoring

### 18. Health Endpoint
**What it is:** `/health` route that returns `{"status":"ok","db":"ok"}` when everything is working. Railway uses it to check if the app is alive. Returns 503 if DB is down.
**You've seen it in:** Every app
**Trigger phrase:** *"Add health check"* or standard practice — always included

---

### 19. Metrics Tracker
**What it is:** A `metrics` SQLite table + `track(metric, value)` helper. Logs events like signups, AI calls, revenue, errors. Used to power dashboards.
**You've seen it in:** All 5 apps (added in the 5-hour session)
**Trigger phrase:** *"Add metrics"* or *"track events"*

---

### 20. Structured Logging
**What it is:** Flask's `app.logger` configured with timestamps. Logs key events (signups, AI calls, errors, slow requests). Each log line has a timestamp + level + message.
**You've seen it in:** Every app
**Trigger phrase:** *"Add logging"* — always included automatically

---

## 🎨 UI Components

### 21. Dark Theme Base Template
**What it is:** The `base.html` every app inherits. Dark background (#0f0f0f), green accent (#00c851), sticky nav, toast notifications, responsive grid. All CSS is inline — no external dependencies.
**You've seen it in:** Every app
**Trigger phrase:** *"Use the dark theme"* or *"Echo style"*

---

### 22. Toast Notifications
**What it is:** Small popup in the corner that shows success/error messages for 3.5 seconds then disappears. No page reload needed.
**You've seen it in:** Every app (`showToast('message', 'success')`)
**Trigger phrase:** *"Add toast messages"* — always included in base template

---

### 23. Stats Dashboard
**What it is:** Row of stat boxes showing key numbers (total users, revenue, listings, etc.) at the top of a dashboard page.
**You've seen it in:** List It Everywhere dashboard, Overseer panel
**Trigger phrase:** *"Add stat boxes"* or *"metrics cards at the top"*

---

### 24. Landing Page with Pricing
**What it is:** Public marketing page with hero section, how-it-works steps, 3-tier pricing cards, and CTA. No external CSS frameworks.
**You've seen it in:** List It Everywhere (`/`)
**Trigger phrase:** *"Add a landing page"* or *"marketing homepage"*

---

## 🚀 Deployment Patterns

### 25. Railway Deploy Config
**What it is:** `railway.json` + `Procfile` + `requirements.txt` that tells Railway how to build and run the app. Healthcheck path, restart policy, gunicorn workers.
**You've seen it in:** Every app
**Trigger phrase:** *"Set up for Railway"* — always included

---

### 26. SEO Package
**What it is:** `<title>`, `<meta description>`, Open Graph tags, Twitter Card, canonical link, `/sitemap.xml`, `/robots.txt` all set up correctly. Each page has unique meta.
**You've seen it in:** Every app (added in the big session)
**Trigger phrase:** *"Add SEO"* — always included

---

### 27. Email Onboarding Sequence
**What it is:** Series of 6 automated emails (welcome → quick start → spotlight → check-in → upgrade reminder → last chance). Queued in SQLite, sent via SMTP in background thread. Auto-triggered on signup.
**You've seen it in:** Liberty Inventory
**Trigger phrase:** *"Add email drip"* or *"onboarding emails"*

---

## 🔒 Security Features

### 28. Security Headers
**What it is:** HTTP response headers that protect against XSS, clickjacking, MIME sniffing. Added to every response via `@app.after_request`.
**The headers:** X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Content-Security-Policy
**You've seen it in:** All 6 apps (added in security upgrade session)
**Trigger phrase:** *"Add security headers"*

---

### 29. bcrypt Password Hashing
**What it is:** Passwords stored as bcrypt hashes instead of plain SHA-256. Industry standard. Slow by design to resist brute force.
**You've seen it in:** All 6 apps (upgraded from SHA-256 in security session)
**Trigger phrase:** *"Use bcrypt"* or *"secure passwords"*

---

### 30. Global Error Handlers
**What it is:** Custom 404 and 500 pages. API routes return JSON errors, HTML routes return styled error pages.
**You've seen it in:** Every app
**Trigger phrase:** *"Add error pages"* — always included

---

## 📋 How to Use This List

When you want a feature, just say its name:

> *"Build a new app for X. Give it **Multi-Tenant Auth**, a **Trial System**, **Stripe Billing**, the **AI Chat Widget**, **Image Analyzer**, **Overseer Panel**, and the **SEO Package**."*

And I'll know exactly what to build for each one — no explanation needed.

---

*Built by Echo · 2026-04-14 · Version 1.0*
*Update this file whenever we build something new.*
