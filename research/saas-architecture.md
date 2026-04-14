# SaaS Architecture & Business — Research Notes
**Researched:** 2026-04-14 | Echo's Self-Education Session

---

## Multi-Tenant Architecture: The 3 Patterns

### Pattern 1: Database Per Tenant (Most Isolated)
- Each tenant = separate database file
- ✅ Complete isolation, easy backup per tenant
- ❌ High operational overhead, doesn't scale to 100s of tenants
- **Use when:** Enterprise, strict compliance, HIPAA, SOC2

### Pattern 2: Schema Per Tenant (Middle Ground)
- Single database, separate schemas per tenant
- ✅ Good isolation, easier than db-per-tenant
- ❌ Migration complexity
- **Use when:** PostgreSQL, medium scale

### Pattern 3: Shared DB + tenant_id Column (What We Use ✅)
- Single DB, all tenants in same tables with `tenant_id` field
- ✅ Lowest overhead, cost-effective, easy analytics
- ❌ Risk of data leakage if queries miss tenant filter
- **Use when:** Most SaaS startups — THIS IS OUR PATTERN

### Our Pattern Implementation
```python
# Every model needs tenant_id
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, unique=True)  # our tenant identifier

# Every query MUST filter by slug/client_id
def get_data(slug):
    client = Client.query.filter_by(slug=slug).first()
    if not client:
        abort(404)
    return Data.query.filter_by(client_id=client.id).all()
```

**The #1 multi-tenant security bug:** Forgetting `tenant_id` filter on a query.
Always enforce: **every data query must include the tenant filter.**

---

## The Row-Level Security Upgrade (Future)
PostgreSQL has native RLS (Row Level Security):
```sql
CREATE POLICY tenant_isolation ON users
    FOR ALL TO app_role
    USING (tenant_id = current_setting('app.current_tenant_id')::int);

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
```
Database enforces isolation even if app code has a bug. Bulletproof.
**Plan: Add this when we migrate to PostgreSQL on Fly.io**

---

## SaaS Pricing Strategies — What We Need to Know

### Key Business Metrics
| Metric | Formula | Target |
|--------|---------|--------|
| CLV (Customer Lifetime Value) | (Monthly Revenue × Gross Margin) / Churn Rate | Maximize |
| CAC (Customer Acquisition Cost) | Total Marketing Spend / New Customers | CLV:CAC > 3:1 |
| MRR | New MRR + Expansion - Churned | Grow 10%+/mo |
| Churn Rate | Cancelled / Total × 100 | < 5%/month |

### The 5 Pricing Models

**1. Flat Rate** — One price, all features
- Example: Basecamp $99/mo unlimited users
- Good for: Simple products with one clear value

**2. Tiered** — Multiple plans (Basic / Pro / Enterprise)
- Most common for SaaS
- Self-selection: customers pick their plan
- Our current model (mostly)

**3. Usage-Based** — Pay for what you use
- AWS model
- Good for: APIs, compute, data processing
- Revenue predictability is harder

**4. Per-Seat** — Price × number of users
- Slack model
- Natural expansion revenue as team grows
- Risk: people share logins

**5. Freemium** — Free tier + paid upgrades
- Dropbox, Notion model
- 2-5% conversion rate (industry standard)
- Good for viral/word-of-mouth products

### Pricing Psychology (Use These in Our Landing Pages)
- **Price Anchoring**: Show the highest tier first — makes others seem reasonable
- **Decoy Effect**: Add a "trap" tier that makes your target tier look like a deal
- **Loss Aversion**: "Don't lose your data" > "Backup your data" — fear > gain
- **Most Popular Badge**: Guide customers to your preferred tier
- **Annual Discount**: Offer 2 months free for annual = better cash flow + lower churn

### Trial Best Practices
- **14-day trial** is the sweet spot (enough to see value, creates urgency)
- **No credit card** required = lower barrier to signup (higher conversion)
- **Onboarding email sequence** during trial = higher activation
- **Usage emails**: "You've used X — upgrade to unlock Y"
- Day 1: Welcome + quick start
- Day 3: Feature highlight
- Day 7: "Halfway through your trial"
- Day 12: "2 days left — here's what you'll lose"
- Day 14: Final CTA

---

## Stripe Integration — Production-Grade Patterns

### The Critical Architecture Decisions

**1. Create Stripe Customer at Signup (Not at Payment)**
```python
# When user signs up:
customer = stripe.Customer.create(
    email=user.email,
    metadata={'user_id': user.id}  # CRITICAL: link back to your DB
)
user.stripe_customer_id = customer.id
db.commit()
```

**2. Idempotency Keys — Prevent Duplicate Charges**
```python
stripe.Subscription.create(
    customer=customer_id,
    items=[{'price': price_id}],
    idempotency_key=f"sub_{user_id}_{plan_id}"  # Same key = same result
)
```

**3. Webhook Architecture — Most Important Part**
```python
@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    sig = request.headers.get('Stripe-Signature')
    try:
        event = stripe.Webhook.construct_event(
            request.data, sig, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        abort(400)  # ALWAYS verify signature

    # Handle events
    if event.type == 'customer.subscription.updated':
        handle_subscription_update(event.data.object)
    elif event.type == 'invoice.payment_failed':
        handle_payment_failure(event.data.object)
    elif event.type == 'customer.subscription.deleted':
        handle_cancellation(event.data.object)

    return '', 200  # ALWAYS return 200 fast — process async if needed
```

### Critical Webhook Events to Handle
| Event | Action |
|-------|--------|
| `customer.subscription.created` | Activate account |
| `customer.subscription.updated` | Sync plan changes |
| `customer.subscription.deleted` | Deactivate, keep data 30 days |
| `invoice.payment_succeeded` | Extend access |
| `invoice.payment_failed` | Send dunning email, grace period |
| `customer.subscription.trial_will_end` | 3-day warning email |

### Payment Method Comparison
| Method | Fee | Processing | Best For |
|--------|-----|-----------|---------|
| Credit Card | 2.9% + $0.30 | Instant | All customers |
| ACH (US) | 0.8%, max $5 | 5-7 days | B2B, large amounts |
| SEPA (EU) | 0.8%, max €5 | 3-5 days | EU B2B |

**Key insight**: For a $10,000 annual B2B contract, ACH costs $5 vs $290 for card. Push enterprise clients to ACH.

---

## GitHub Actions CI/CD — Our Future Setup

### The Workflow File Structure
```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main]  # or master

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v

  deploy:
    needs: test  # Only deploy if tests pass
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway up --service ${{ secrets.RAILWAY_SERVICE_ID }}
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### Benefits of CI/CD for Our Apps
- Tests run automatically on every push
- Broken code never reaches production
- Deployment is one git push
- Clear deployment history
- Automatic security scans (add `bandit` for Python security)

### What to Add to Our Apps (Priority Order)
1. `tests/test_auth.py` — Login, signup, session tests
2. `tests/test_overseer.py` — Admin panel access control
3. `tests/test_billing.py` — Stripe webhook simulation
4. `.github/workflows/test.yml` — Run tests on PR
5. `.github/workflows/deploy.yml` — Auto-deploy on main push

---

## The Service Layer — How to Refactor Our Apps

Current state: All logic in routes
Target state: Routes handle HTTP only, services handle business logic

### Migration Strategy (Low Risk)
Don't rewrite — extract incrementally:

1. Create `services/` directory
2. Start with NEW features — always use service layer
3. When touching existing route for bug fix — extract to service at same time
4. Priority: billing service first (highest risk if broken)

### Service Layer Template
```python
# services/auth_service.py
from dataclasses import dataclass

@dataclass
class AuthResult:
    success: bool
    user: dict = None
    error: str = None
    status_code: int = 200

def register_user(email, password):
    if not email or not password:
        return AuthResult(False, error="Missing fields", status_code=400)

    if User.query.filter_by(email=email).first():
        return AuthResult(False, error="Email already exists", status_code=409)

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return AuthResult(True, user={'id': user.id, 'email': user.email})
```
