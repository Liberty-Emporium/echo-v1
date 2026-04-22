# Multi-Tenant SaaS — Industry Study 2026
_Researched 2026-04-22. Sources: ZeonEdge, SaaS Pegasus, LaunchStack, Hunchbite, TrialMoments_

---

## What the Best SaaS Companies Do (vs What We Do)

### Isolation Model Comparison

| Company tier | Model | Why |
|-------------|-------|-----|
| Shopify, Stripe | Pool + RLS | Millions of tenants, PostgreSQL row-level security |
| Linear, Notion | Pool | Thousands of tenants, shared schema, tenant_id everywhere |
| HubSpot, Salesforce | Silo (DB-per-tenant) | Enterprise, compliance, data residency laws |
| **Our apps (Contractor, Dropship, Consignment, Inventory)** | **Silo (file-based)** | **Small scale, simple, works** |
| **Our apps (AI Widget, Pet Vet, FloodClaim)** | **Pool** | **Per-user accounts** |

**Verdict: Our model is correct for our scale.** The silo model is the right choice for <500 tenants on Railway. Shopify uses it for enterprise clients. We'd only need to change if we hit 500+ tenants on the same Railway dyno.

---

## What World-Class Multi-Tenant Apps Have That Ours Don't

### 1. Feature Gating (MISSING from most of our apps)
The industry standard is a `PLAN_LIMITS` dict + `@feature_gate` decorator:
```python
PLAN_LIMITS = {
    'trial':   {'products': 50,  'ai_calls': 10,  'exports': False},
    'starter': {'products': 500, 'ai_calls': 100, 'exports': True},
    'pro':     {'products': 9999,'ai_calls': 500, 'exports': True},
}
```
**We have:** Trial gate (block after expiry). **We lack:** Plan-based feature limits.

### 2. Stripe Webhooks (partially wired)
Production Stripe requires handling 6 events (not just checkout success):
- `customer.subscription.created` → provision
- `customer.subscription.updated` → plan change
- `customer.subscription.deleted` → downgrade/cancel
- `invoice.payment_succeeded` → confirm active
- `invoice.payment_failed` → mark past_due, notify
- `customer.subscription.trial_will_end` → send conversion email at day 11

**We have:** Checkout session creation. **We lack:** Full webhook handler on most apps.

### 3. Trial UX Conversion Patterns (MISSING)
Industry data (TrialMoments 2026):
- 14-day trial = sweet spot for B2B
- Trial countdown banner → 23% of conversions happen here
- First urgency email = Day 11 (3 days before end)
- Post-expiry: show read-only, don't delete → "resume in one click"
- 14-day trials convert at ~40% vs 30-day trials at ~30%

**We have:** Hard block on expiry. **We lack:** Countdown banner, urgency emails, grace period UX.

### 4. Onboarding Wizard (MISSING)
- Users who complete onboarding are 3-5x more likely to convert
- Get to "aha moment" in <5 minutes
- Progress checklist visible in UI
- Goal-based personalization at signup ("What's your main goal?")

**We have:** Direct redirect to dashboard after signup. **We lack:** Any guided onboarding.

### 5. Noisy Neighbor Prevention (PARTIALLY done)
We have per-tenant rate limiting (120 calls/60s). Industry adds:
- Per-tenant DB row quotas (`COUNT(*) WHERE store_slug=?` before inserts)
- Per-tenant storage quotas (directory size check before uploads)
- Per-tenant AI call quotas (track monthly usage against plan limit)

### 6. Tenant Health Dashboard (DONE ✅)
Our Overseer panel is solid. Matches industry standard.

### 7. Data Export / GDPR Right-to-Deletion (PARTIALLY done)
We have export. Missing: tenant self-service export + deletion request flow.

---

## The 5 Biggest Improvements to Make (prioritized)

### Priority 1: Feature Gating in all multi-tenant apps
Add `PLAN_LIMITS` + `@feature_gate` decorator to Contractor Pro, Dropship, Consignment, Inventory.
**Impact:** Monetization — free trial users can't use unlimited AI calls.

### Priority 2: Trial Countdown Banner
Add a persistent banner to `base.html` showing days remaining.
Shows at day 7, increases urgency at day 11, urgent at day 13.
**Impact:** 23% of conversions happen from this banner.

### Priority 3: Full Stripe Webhook Handler
Complete the webhook handler for all 6 events on every app that uses Stripe.
**Impact:** Prevents billing state going out of sync — currently if Stripe says "cancelled" we don't know.

### Priority 4: Onboarding Wizard
3-step wizard: Company info → First product/action → Invite teammate.
**Impact:** 3-5x higher trial conversion for users who complete it.

### Priority 5: Post-Expiry Grace Period
Instead of hard block: show read-only dashboard with "Resume for $X/mo" overlay.
**Impact:** 12% of conversions happen post-expiry with this in place.

---

## How Our Stack Compares to SaaS Boilerplates (LaunchStack, SaaS Pegasus)

| Feature | SaaS Pegasus | LaunchStack | Our Stack |
|---------|-------------|-------------|-----------|
| Auth | Django auth | Flask + JWT | Flask + bcrypt sessions ✅ |
| Tenancy | DB per org | JWT claims | File-based silo ✅ |
| Billing | dj-stripe | Stripe webhooks | Partial (checkout only) ⚠️ |
| Trial | Built-in | Built-in | Manual trial_ends date ⚠️ |
| Feature gates | Entitlements | Custom | Missing on most apps ❌ |
| Onboarding | Wizard | None | None ❌ |
| Overseer | Django admin | None | Custom Overseer ✅ |
| Tests | pytest | pytest | Playwright (we built this) ✅ |

**Bottom line: Our core architecture is solid. We're missing monetization infrastructure (gates, billing webhooks) and conversion UX (onboarding, trial urgency).**

---

## The Industry Secret Nobody Talks About

The best multi-tenant SaaS isn't about the database model — it's about **the tenant experience**:

1. **Sign up in 30 seconds** (email only, no CC)
2. **First value in 5 minutes** (guided wizard)
3. **See the clock** (countdown banner always visible)
4. **Feel the loss** (day 11: "You'll lose all your data in 3 days")
5. **One click to stay** (upgrade = card number → done)
6. **Never lose their data** (grace period, read-only view)

Companies with all 6 convert at 35-45%. Without them: 5-12%.

---
_Sources: ZeonEdge multi-tenant architecture 2026, SaaS Pegasus Django guide,
LaunchStack Flask guide 2026, Hunchbite Stripe billing guide, TrialMoments 2026 benchmarks_
