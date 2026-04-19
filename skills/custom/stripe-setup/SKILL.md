# stripe-setup

Add Stripe billing to any Flask app. Handles subscriptions + one-time payments.

## When to use
- Jay says "add Stripe", "add payments", "integrate billing"
- Setting up subscription tiers on a new app
- Adding a one-time purchase (like the $90 installation service)

## Required env vars (set in Railway)
- `STRIPE_SECRET_KEY` — from Stripe dashboard → Developers → API Keys
- `STRIPE_PUBLISHABLE_KEY` — same location
- `STRIPE_WEBHOOK_SECRET` — from Stripe dashboard → Webhooks
- `STRIPE_PRICE_PRO` — Price ID for pro plan (price_xxx)
- `STRIPE_PRICE_BUSINESS` — Price ID for business plan

## Stripe product setup steps
1. Go to stripe.com → Products → Add Product
2. Set name, price, billing period (monthly for subscriptions, one-time for services)
3. Copy the Price ID (starts with `price_`)
4. Add to Railway env vars
5. Add webhook endpoint: `https://<APP_URL>/webhook/stripe`
   - Events: checkout.session.completed, customer.subscription.updated, customer.subscription.deleted, invoice.payment_failed

## Code template already in TOOL_LIBRARY.md (#13 Stripe Billing)
The full implementation is in AI-Agent-Widget/app.py — copy from there.

## One-time payment pattern (e.g. $90 installation)
```python
checkout = stripe.checkout.Session.create(
    customer_email=session.get('email'),
    payment_method_types=['card'],
    line_items=[{'price': STRIPE_PRICE_INSTALLATION, 'quantity': 1}],
    mode='payment',  # NOT 'subscription'
    success_url=request.host_url + 'billing/success',
    cancel_url=request.host_url + 'pricing',
    metadata={'user_id': str(session['user_id']), 'plan': 'installation'},
)
```

## Critical Rules (from REFLECTIONS.md)
1. Always use Stripe idempotency keys on money-moving calls
2. Format: `f"{action}_{user_id}_{date_string}"`
3. Always verify webhook signature before processing
4. Test with Stripe test mode first (test card: 4242 4242 4242 4242)
