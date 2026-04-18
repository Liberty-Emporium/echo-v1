# stripe-billing

**Version:** 1.0.0
**Created:** 2026-04-18
**Author:** Echo

## Description

Complete Stripe subscription billing integration for Jay's Flask SaaS apps. Covers Stripe Checkout, webhook handling, subscription lifecycle, plan enforcement, and idempotency. The revenue unlock for all 7 apps.

## When To Use

- Adding Stripe payments to any of Jay's apps
- Debugging billing issues (failed webhooks, missed events)
- Upgrading/downgrading subscription plans
- Handling trial-to-paid conversion
- Enforcing plan limits in app logic

## Critical Rules

1. **ALWAYS use idempotency keys** — `f"{action}_{user_id}_{timestamp_day}"` prevents double-charges
2. **NEVER trust client-side data** for payment confirmation — only trust webhook events
3. **Webhook endpoint MUST use `request.data` (raw bytes)** — not `request.json` or `request.form`
4. **Always verify webhook signature** with `stripe.Webhook.construct_event()`
5. **Return 200 immediately** from webhook handler — do heavy work in background thread
6. **Store `stripe_customer_id` and `stripe_subscription_id`** on user row — never re-fetch from Stripe what you already have

## Environment Variables Required

```bash
STRIPE_SECRET_KEY=sk_live_...         # or sk_test_... for testing
STRIPE_WEBHOOK_SECRET=whsec_...       # from Stripe Dashboard → Webhooks
STRIPE_PRICE_STARTER=price_...        # Price ID for each plan tier
STRIPE_PRICE_PRO=price_...
STRIPE_PRICE_ENTERPRISE=price_...
```

## Database Schema (add to users table)

```sql
ALTER TABLE users ADD COLUMN stripe_customer_id TEXT;
ALTER TABLE users ADD COLUMN stripe_subscription_id TEXT;
ALTER TABLE users ADD COLUMN plan TEXT DEFAULT 'trial';
ALTER TABLE users ADD COLUMN plan_status TEXT DEFAULT 'active';
ALTER TABLE users ADD COLUMN trial_ends_at TEXT;
ALTER TABLE users ADD COLUMN subscription_ends_at TEXT;
```

## Core Implementation

### 1. billing_service.py — Drop into any app's services/

```python
import stripe
import os
import threading
from datetime import datetime, timezone

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

PRICE_IDS = {
    'starter': os.environ.get('STRIPE_PRICE_STARTER'),
    'pro': os.environ.get('STRIPE_PRICE_PRO'),
    'enterprise': os.environ.get('STRIPE_PRICE_ENTERPRISE'),
}

def create_checkout_session(user_id, user_email, plan, success_url, cancel_url):
    """Create Stripe Checkout session for new subscription."""
    idempotency_key = f"checkout_{user_id}_{datetime.now(timezone.utc).strftime('%Y%m%d')}"
    session = stripe.checkout.Session.create(
        customer_email=user_email,
        payment_method_types=['card'],
        line_items=[{'price': PRICE_IDS[plan], 'quantity': 1}],
        mode='subscription',
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={'user_id': str(user_id), 'plan': plan},
        idempotency_key=idempotency_key,
    )
    return session.url

def create_customer_portal(stripe_customer_id, return_url):
    """Redirect user to Stripe's self-serve billing portal."""
    session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url=return_url,
    )
    return session.url

def cancel_subscription(stripe_subscription_id):
    """Cancel at period end (not immediately)."""
    stripe.Subscription.modify(
        stripe_subscription_id,
        cancel_at_period_end=True,
    )

def get_subscription_status(stripe_subscription_id):
    """Get live status from Stripe."""
    sub = stripe.Subscription.retrieve(stripe_subscription_id)
    return {
        'status': sub.status,  # active, past_due, canceled, trialing
        'current_period_end': sub.current_period_end,
        'cancel_at_period_end': sub.cancel_at_period_end,
    }
```

### 2. billing_routes.py — Blueprint to register in app

```python
from flask import Blueprint, request, jsonify, redirect, session, current_app
import stripe, os, threading

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/billing/checkout/<plan>')
def checkout(plan):
    if plan not in ('starter', 'pro', 'enterprise'):
        return 'Invalid plan', 400
    user_id = session.get('user_id')
    user_email = session.get('email')
    url = create_checkout_session(
        user_id, user_email, plan,
        success_url=request.host_url + 'billing/success',
        cancel_url=request.host_url + 'settings/billing',
    )
    return redirect(url)

@billing_bp.route('/billing/portal')
def portal():
    stripe_customer_id = get_user_stripe_id(session['user_id'])  # impl per app
    url = create_customer_portal(stripe_customer_id, request.host_url + 'settings/billing')
    return redirect(url)

@billing_bp.route('/billing/success')
def success():
    # Don't update DB here — wait for webhook
    flash('Payment successful! Your plan will activate shortly.', 'success')
    return redirect('/dashboard')

@billing_bp.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data  # RAW bytes — critical
    sig = request.headers.get('Stripe-Signature')
    secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    try:
        event = stripe.Webhook.construct_event(payload, sig, secret)
    except ValueError:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400

    # Handle async to return 200 fast
    threading.Thread(target=handle_webhook_event, args=(event,)).start()
    return '', 200

def handle_webhook_event(event):
    """Process webhook in background thread."""
    etype = event['type']
    data = event['data']['object']

    if etype == 'checkout.session.completed':
        user_id = data['metadata']['user_id']
        plan = data['metadata']['plan']
        customer_id = data['customer']
        sub_id = data['subscription']
        update_user_plan(user_id, plan, 'active', customer_id, sub_id)

    elif etype == 'customer.subscription.updated':
        sub_id = data['id']
        status = data['status']
        update_subscription_status(sub_id, status)

    elif etype == 'customer.subscription.deleted':
        sub_id = data['id']
        downgrade_to_free(sub_id)

    elif etype == 'invoice.payment_failed':
        customer_id = data['customer']
        send_payment_failed_email(customer_id)  # impl in email service
```

### 3. Plan Enforcement Decorator

```python
from functools import wraps
from flask import session, redirect, flash

PLAN_HIERARCHY = {'trial': 0, 'starter': 1, 'pro': 2, 'enterprise': 3}

def require_plan(min_plan):
    """Decorator: require at least this plan level."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_plan = session.get('plan', 'trial')
            if PLAN_HIERARCHY.get(user_plan, 0) < PLAN_HIERARCHY.get(min_plan, 1):
                flash(f'This feature requires the {min_plan.title()} plan.', 'warning')
                return redirect('/settings/billing')
            return f(*args, **kwargs)
        return decorated
    return decorator

# Usage:
# @app.route('/advanced-feature')
# @require_plan('pro')
# def advanced_feature():
#     ...
```

## Webhook Events to Handle

| Event | Action |
|-------|--------|
| `checkout.session.completed` | Activate plan, store customer/sub IDs |
| `customer.subscription.updated` | Update plan status (upgrades, downgrades) |
| `customer.subscription.deleted` | Downgrade to free/expired |
| `invoice.payment_succeeded` | Log payment, extend subscription |
| `invoice.payment_failed` | Send payment failed email, flag account |
| `customer.subscription.trial_will_end` | Send trial ending warning email |

## Testing

```bash
# Install Stripe CLI
stripe listen --forward-to localhost:5000/webhook/stripe

# Trigger test events
stripe trigger checkout.session.completed
stripe trigger invoice.payment_failed
stripe trigger customer.subscription.deleted
```

## Registration Pattern (in app.py)

```python
from billing_routes import billing_bp
app.register_blueprint(billing_bp)
```

## Per-App Checklist

- [ ] Add env vars to Railway: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, STRIPE_PRICE_*
- [ ] Run DB migration to add stripe columns to users table
- [ ] Copy billing_service.py and billing_routes.py to app
- [ ] Implement `get_user_stripe_id()`, `update_user_plan()`, `update_subscription_status()`, `downgrade_to_free()` using app's DB pattern
- [ ] Register webhook URL in Stripe Dashboard
- [ ] Register billing_bp in app.py
- [ ] Add billing page link to settings nav
- [ ] Test full checkout flow with Stripe test card: 4242 4242 4242 4242

## Stripe Test Cards

| Card | Behavior |
|------|----------|
| 4242 4242 4242 4242 | Always succeeds |
| 4000 0000 0000 0002 | Always declines |
| 4000 0025 0000 3155 | Requires 3D Secure |
| 4000 0000 0000 9995 | Insufficient funds |
