# Tenant Lifecycle — Flask Code

## Stage 1: Signup

```python
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        company = request.form.get('company', '').strip()
        email   = request.form.get('email', '').strip().lower()
        pw      = request.form.get('password', '')

        # Generate slug from company name
        import re, secrets, datetime
        slug = re.sub(r'[^a-z0-9]', '-', company.lower())[:30].strip('-')
        slug = slug or secrets.token_hex(6)

        # Check slug not taken
        if os.path.exists(os.path.join(CUSTOMERS_DIR, slug)):
            slug = f"{slug}-{secrets.token_hex(3)}"

        # Set trial end date (14 days)
        trial_end = (datetime.datetime.utcnow() + datetime.timedelta(days=14)).isoformat()

        # Create tenant config
        cfg = {
            'company':     company,
            'email':       email,
            'plan':        'trial',
            'trial_ends':  trial_end,
            'created_at':  datetime.datetime.utcnow().isoformat(),
        }
        save_tenant_config(cfg, slug)

        # Create admin user
        users = {email: {'password': hash_pw(pw), 'role': 'admin', 'created_at': cfg['created_at']}}
        save_json(tenant_file('users.json', slug), users)

        # Log in immediately
        session.update({'logged_in': True, 'username': email, 'role': 'admin', 'store_slug': slug})
        flash(f'Welcome! Your 14-day trial starts now.', 'success')
        return redirect(url_for('onboarding'))  # → Step 2

    return render_template('signup.html')
```

## Stage 2: Onboarding Wizard

```python
@app.route('/onboarding')
@login_required
def onboarding():
    slug = get_slug()
    cfg  = get_tenant_config(slug)
    # Track onboarding step (0-4)
    step = cfg.get('onboarding_step', 0)
    return render_template('onboarding.html', step=step, cfg=cfg)

@app.route('/onboarding/complete', methods=['POST'])
@login_required
def onboarding_complete():
    slug = get_slug()
    cfg  = get_tenant_config(slug)
    cfg['onboarding_step']     = 4
    cfg['onboarding_done']     = True
    cfg['onboarding_done_at']  = datetime.datetime.utcnow().isoformat()
    save_tenant_config(cfg, slug)
    flash('Setup complete! You\'re all set.', 'success')
    return redirect(url_for('dashboard'))
```

### Onboarding Template Pattern
```html
<!-- 5-step wizard, get user to "aha moment" in <5 min -->
<div class="wizard">
  <div class="wizard-steps">
    <div class="step {% if step >= 1 %}done{% endif %}">1. Company info</div>
    <div class="step {% if step >= 2 %}done{% endif %}">2. Add first product</div>
    <div class="step {% if step >= 3 %}done{% endif %}">3. Invite a teammate</div>
    <div class="step {% if step >= 4 %}done{% endif %}">4. You're ready!</div>
  </div>
</div>
```

## Stage 3: Trial Enforcement

```python
def trial_gate(f):
    """Decorator: redirect expired trial to upgrade page."""
    @wraps(f)
    def decorated(*args, **kwargs):
        slug = session.get('impersonating_slug') or session.get('store_slug')
        if slug and session.get('role') != 'overseer':
            status = get_trial_status(slug)
            if status == 'expired':
                flash('Your trial has expired. Upgrade to continue.', 'warning')
                return redirect(url_for('upgrade'))
        return f(*args, **kwargs)
    return decorated

# Apply to all dashboard routes:
@app.route('/dashboard')
@login_required
@trial_gate
def dashboard():
    ...
```

## Stage 4: Upgrade / Stripe Checkout

```python
@app.route('/upgrade')
@login_required
def upgrade():
    slug  = get_slug()
    cfg   = get_tenant_config(slug)
    days  = get_trial_days_left(slug)
    return render_template('upgrade.html', cfg=cfg, days_left=days)

@app.route('/upgrade/checkout', methods=['POST'])
@login_required
@csrf_required
def start_checkout():
    import stripe as _stripe
    _stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')
    if not _stripe.api_key:
        flash('Payment system not configured yet. Contact support.', 'error')
        return redirect(url_for('upgrade'))

    slug = get_slug()
    cfg  = get_tenant_config(slug)
    plan = request.form.get('plan', 'starter')

    PRICE_IDS = {
        'starter': os.environ.get('STRIPE_PRICE_STARTER', ''),
        'pro':     os.environ.get('STRIPE_PRICE_PRO', ''),
    }
    price_id = PRICE_IDS.get(plan)
    if not price_id:
        flash('Invalid plan selected.', 'error')
        return redirect(url_for('upgrade'))

    checkout = _stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='subscription',
        customer_email=cfg.get('email'),
        metadata={'store_slug': slug, 'plan': plan},
        line_items=[{'price': price_id, 'quantity': 1}],
        success_url=url_for('upgrade_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('upgrade', _external=True),
    )
    return redirect(checkout.url)
```

## Stage 5: Stripe Webhook Handler

```python
@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    payload    = request.data
    sig_header = request.headers.get('Stripe-Signature', '')
    wh_secret  = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

    try:
        import stripe as _stripe
        event = _stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except Exception:
        return '', 400

    slug = None
    if event['data']['object'].get('metadata'):
        slug = event['data']['object']['metadata'].get('store_slug')

    if event['type'] == 'customer.subscription.created' and slug:
        cfg = get_tenant_config(slug)
        cfg['plan']                    = event['data']['object']['metadata'].get('plan', 'starter')
        cfg['plan_status']             = 'active'
        cfg['stripe_subscription_id']  = event['data']['object']['id']
        cfg['stripe_customer_id']      = event['data']['object']['customer']
        save_tenant_config(cfg, slug)

    elif event['type'] == 'customer.subscription.deleted' and slug:
        cfg = get_tenant_config(slug)
        cfg['plan']        = 'trial'
        cfg['plan_status'] = 'cancelled'
        save_tenant_config(cfg, slug)

    elif event['type'] == 'invoice.payment_failed' and slug:
        cfg = get_tenant_config(slug)
        cfg['plan_status'] = 'past_due'
        save_tenant_config(cfg, slug)

    elif event['type'] == 'customer.subscription.trial_will_end' and slug:
        # Send conversion email here (Day 11 = 3 days before end)
        pass

    return '', 200
```

## Stage 6: Post-Expiry Grace Period

```python
@app.route('/expired')
@login_required
def trial_expired():
    """Grace period page — show read-only view + upgrade CTA."""
    slug = get_slug()
    cfg  = get_tenant_config(slug)
    # Show summary of their data (don't delete anything yet)
    return render_template('trial_expired.html', cfg=cfg)
```

Template pattern — empathetic, not punishing:
```html
<div style="text-align:center;padding:3rem">
  <h1>Your trial has ended</h1>
  <p>Your data is safe. Upgrade anytime to pick up right where you left off.</p>
  <a href="/upgrade" class="btn btn-primary btn-lg">Continue with Pro →</a>
  <p style="margin-top:1rem;font-size:.85rem">
    Need more time? <a href="/extend-trial">Request a 7-day extension</a>
  </p>
</div>
```
