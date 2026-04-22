---
name: multi-tenant-saas
description: >-
  Design, build, audit, and improve multi-tenant SaaS applications on the
  Liberty-Emporium Flask stack. Use when creating a new multi-tenant app,
  adding tenant isolation to an existing app, building signup/onboarding flows,
  implementing trial/plan/subscription logic, wiring Stripe billing, adding
  feature gating, building an Overseer admin panel, or diagnosing tenant data
  leaks. Triggers on phrases like "multi-tenant", "SaaS app", "tenant isolation",
  "subscription", "trial", "plan limits", "feature gating", "Stripe billing",
  "onboarding flow", "Overseer", or any work on Contractor Pro, Dropship,
  Consignment, or Inventory apps.
---

# Multi-Tenant SaaS Skill

Echo's reference for building world-class multi-tenant SaaS on Flask + SQLite/Railway.

## The 3 Isolation Models (choose one per app)

| Model | Pattern | Our Apps | Scale |
|-------|---------|----------|-------|
| **Silo** | One DB file per tenant | Contractor Pro, Dropship, Consignment, Inventory | <500 tenants |
| **Pool** | Shared DB + `store_slug` column every table | AI Widget, Pet Vet, FloodClaim | Thousands |
| **Bridge** | Shared DB + per-tenant SQLite files | (future upgrade path) | Hundreds |

**Current Liberty-Emporium standard:** Silo model (file-based `/data/customers/<slug>/`) for the
multi-tenant apps. Pool model for single-user-per-account apps (AI Widget, Pet Vet).

See `references/isolation-patterns.md` for full code patterns for both models.

## Tenant Lifecycle (the 6 stages every app must handle)

```
1. SIGNUP      → create slug, hash password, write config.json, set trial_ends
2. ONBOARDING  → welcome wizard, get-to-value in <5 mins, setup checklist
3. TRIAL       → full access, countdown banner, urgency at day 11-14
4. CONVERSION  → Stripe checkout or manual upgrade, plan set to "paid"
5. ACTIVE      → feature gates enforce plan limits, billing manages itself
6. CHURN       → cancel/expire → grace period → data export → deletion
```

See `references/tenant-lifecycle.md` for Flask code for each stage.

## The Non-Negotiable Security Rules

**Every multi-tenant route MUST filter by tenant slug. No exceptions.**

```python
# ❌ WRONG — leaks all tenants' data
items = db.execute('SELECT * FROM items').fetchall()

# ✅ CORRECT — scoped to current tenant
slug  = get_slug()   # always from session, never from URL params
items = db.execute('SELECT * FROM items WHERE store_slug=?', (slug,)).fetchall()
```

The `get_slug()` function must:
1. Prefer `session['impersonating_slug']` (Overseer impersonation)
2. Fall back to `session['store_slug']` (logged-in tenant)
3. Validate the slug exists before using it
4. Never accept slug from GET/POST params without verification

See `references/isolation-patterns.md` → "get_slug() canonical implementation".

## Plan & Feature Gating

```python
PLAN_LIMITS = {
    'trial': {'products': 50,  'users': 1,  'ai_calls': 10,  'exports': False},
    'starter':{'products': 500, 'users': 3,  'ai_calls': 100, 'exports': True},
    'pro':   {'products': 9999,'users': 10, 'ai_calls': 500, 'exports': True},
}

def plan_allows(feature, slug=None):
    """Check if current tenant's plan allows a feature/limit."""
    slug = slug or get_slug()
    plan = get_tenant_config(slug).get('plan', 'trial')
    limits = PLAN_LIMITS.get(plan, PLAN_LIMITS['trial'])
    if isinstance(limits.get(feature), bool):
        return limits[feature]
    return limits.get(feature, 0)

def feature_gate(feature):
    """Decorator: block route if plan doesn't allow feature."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not plan_allows(feature):
                if request.is_json:
                    return jsonify({'error': f'Upgrade required for {feature}'}), 403
                flash(f'This feature requires a higher plan. Upgrade to unlock it.', 'warning')
                return redirect(url_for('upgrade'))
            return f(*args, **kwargs)
        return decorated
    return decorator
```

## Trial System (14-day standard)

```python
import datetime as _dt

def get_trial_status(slug):
    cfg = get_tenant_config(slug)
    if cfg.get('plan') == 'paid':  return 'paid'
    trial_end = cfg.get('trial_ends')
    if not trial_end:              return 'expired'
    days_left = (_dt.datetime.fromisoformat(trial_end) - _dt.datetime.utcnow()).days
    if days_left > 0:              return 'active'
    return 'expired'

def get_trial_days_left(slug):
    cfg = get_tenant_config(slug)
    trial_end = cfg.get('trial_ends', '')
    if not trial_end: return 0
    return max(0, (_dt.datetime.fromisoformat(trial_end) - _dt.datetime.utcnow()).days)
```

In `base.html` — always show trial countdown:
```html
{% if trial_days_left is defined and trial_days_left <= 7 and plan != 'paid' %}
<div style="background:#f59e0b;color:#000;padding:8px;text-align:center;font-size:.85rem;font-weight:600">
  ⚡ {{ trial_days_left }} day{{ 's' if trial_days_left != 1 else '' }} left in your trial —
  <a href="/upgrade" style="color:#000;font-weight:800;text-decoration:underline">Upgrade now →</a>
</div>
{% endif %}
```

## Stripe Billing (production pattern)

The 6 webhooks you MUST handle:
```python
HANDLED_EVENTS = {
    'customer.subscription.created':   _handle_sub_created,
    'customer.subscription.updated':   _handle_sub_updated,
    'customer.subscription.deleted':   _handle_sub_deleted,
    'invoice.payment_succeeded':       _handle_payment_ok,
    'invoice.payment_failed':          _handle_payment_fail,
    'customer.subscription.trial_will_end': _handle_trial_ending,
}
```

See `references/stripe-billing.md` for complete webhook handler + checkout flow.

## Overseer Panel (admin across all tenants)

Every multi-tenant app must have `/overseer` with:
- Tenant health table (plan, trial days, last active, MRR)
- Impersonation (`session['impersonating_slug']`)
- Manual plan upgrade/extension
- Tenant data export/delete

See `references/overseer-patterns.md` for the full Overseer implementation.

## Onboarding Best Practices (2026 research)

- **14-day trial** = sweet spot for B2B SaaS (7-day creates urgency but may not be enough time)
- **No credit card at signup** = 2-3x more trial starts
- **Get-to-value in <5 minutes** = users who hit "aha moment" are 3-5x more likely to convert
- **Trial countdown banner** appears at day 11 (3 days before end)
- **One-click upgrade** from any screen — no external redirects
- **Data preserved** on upgrade (never lose their work)
- **Post-expiry grace** = show read-only view, prompt to upgrade, don't delete immediately

## What's Wrong in Our Apps Today

| App | Issue | Fix |
|-----|-------|-----|
| Consignment | Hardcoded secret key fallback | Replace with generated+persisted key |
| AI Widget | Missing SESSION_COOKIE_HTTPONLY + CSRF | Add session config block |
| Consignment | SHA-256 admin seed passwords | Seed with bcrypt |
| All apps | No trial countdown banner in UI | Add to base.html |
| All apps | No post-expiry grace period UX | Show read-only with upgrade prompt |
| Consignment+Inventory | HTTP 404 — Railway down | Check Railway dashboard, redeploy |

## Scripts

- `scripts/audit_tenant_isolation.py` — scan app.py for tenant data leaks
- `scripts/provision_tenant.py` — CLI tool to create a new tenant from command line
