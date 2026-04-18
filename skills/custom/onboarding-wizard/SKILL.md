# onboarding-wizard

**Version:** 1.0.0
**Created:** 2026-04-18
**Author:** Echo

## Description

Multi-step trial signup wizard for Jay's SaaS apps. Converts visitor → trial user with store setup, onboarding flow, and first-login experience. Distilled from lessons learned across Liberty Inventory, Dropship Shipping, and Consignment Solutions.

## When To Use

- Building a new SaaS app signup flow
- Improving an existing /wizard route
- Adding step-by-step onboarding after signup

## The Proven Wizard Pattern

### Route Structure

```
GET  /          → Landing page with CTA → /wizard
GET  /wizard    → Step 1: Store name + contact info
POST /start-trial → Create account, redirect to /dashboard
GET  /login     → Returning users
POST /login     → Auth check, redirect to /dashboard
GET  /dashboard → Protected — requires login
```

### Step 1 Wizard Form (wizard.html)

```html
<form method="POST" action="/start-trial">
  <!-- Store/Business Name -->
  <div class="form-group">
    <label>Business Name</label>
    <input type="text" name="store_name" required 
           placeholder="Acme Thrift Store"
           pattern="[A-Za-z0-9 '\-]{2,60}" 
           title="2-60 characters, letters, numbers, spaces">
  </div>

  <!-- Contact Email -->
  <div class="form-group">
    <label>Your Email</label>
    <input type="email" name="contact_email" required>
  </div>

  <!-- Contact Name -->
  <div class="form-group">
    <label>Your Name</label>
    <input type="text" name="contact_name" required>
  </div>

  <!-- Password — ALWAYS with show/hide toggle (Jay's Rule) -->
  <div class="form-group" style="position:relative">
    <label>Create Password</label>
    <input type="password" name="password" id="pw" required minlength="8">
    <span onclick="togglePw()" 
          style="position:absolute;right:12px;top:38px;cursor:pointer;font-size:1.2rem"
          id="eye">👁️</span>
  </div>

  <button type="submit" class="btn-primary">Start My Free Trial →</button>
  <p style="text-align:center;color:#666;font-size:0.85rem;margin-top:8px">
    14-day free trial • No credit card required
  </p>
</form>

<script>
function togglePw() {
  const pw = document.getElementById('pw');
  const eye = document.getElementById('eye');
  if (pw.type === 'password') {
    pw.type = 'text'; eye.textContent = '🙈';
  } else {
    pw.type = 'password'; eye.textContent = '👁️';
  }
}
</script>
```

### /start-trial Route

```python
@app.route('/start-trial', methods=['POST'])
def start_trial():
    store_name = request.form.get('store_name', '').strip()
    email = request.form.get('contact_email', '').strip().lower()
    name = request.form.get('contact_name', '').strip()
    password = request.form.get('password', '')

    # Validation
    if not all([store_name, email, name, password]):
        flash('All fields required.', 'error')
        return redirect('/wizard')
    if len(password) < 8:
        flash('Password must be at least 8 characters.', 'error')
        return redirect('/wizard')

    # Duplicate email check
    existing = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
    if existing:
        flash('An account with that email already exists. <a href="/login">Log in</a>', 'error')
        return redirect('/wizard')

    # Create account
    slug = slugify(store_name)
    # Ensure slug uniqueness
    base_slug = slug
    counter = 1
    while conn.execute("SELECT id FROM users WHERE slug=?", (slug,)).fetchone():
        slug = f"{base_slug}-{counter}"
        counter += 1

    trial_ends = (datetime.now(timezone.utc) + timedelta(days=14)).isoformat()
    password_hash = hash_password(password)  # bcrypt via saas_security_core

    conn.execute("""
        INSERT INTO users (email, password_hash, name, slug, plan, trial_ends_at, created_at)
        VALUES (?, ?, ?, ?, 'trial', ?, datetime('now'))
    """, (email, password_hash, name, slug, trial_ends))
    conn.commit()

    # Log in immediately
    user_id = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()['id']
    session['user_id'] = user_id
    session['email'] = email
    session['slug'] = slug
    session['plan'] = 'trial'

    # Send welcome email (non-blocking)
    from email_service import send_welcome
    send_welcome(email, name)

    flash(f'Welcome, {name}! Your 14-day trial has started.', 'success')
    return redirect('/dashboard')
```

## Known Gotchas (from lessons-learned)

### Slug Uniqueness
Always check for slug collisions before inserting. Two stores named "ABC Store" → same slug → DB constraint error.

### Wizard Form Validation
- Client-side validation (HTML5) is UX only — always validate server-side too
- `pattern` attribute on store_name prevents special chars that break slugs
- Email uniqueness check must happen before slug creation

### First Dashboard Experience
After trial signup, show:
1. Completion percentage bar ("Your setup is 20% complete")
2. 3 action items to get started
3. Trial countdown banner ("12 days left in your trial — Upgrade")

### Trial Countdown Banner (in base.html)

```python
# In route context processor
@app.context_processor
def inject_trial_info():
    if 'user_id' not in session:
        return {}
    user = get_user(session['user_id'])
    if user and user['plan'] == 'trial':
        trial_ends = datetime.fromisoformat(user['trial_ends_at'])
        days_left = max(0, (trial_ends - datetime.now(timezone.utc)).days)
        return {'trial_days_left': days_left}
    return {}
```

```html
{% if trial_days_left is defined %}
<div style="background:{% if trial_days_left <= 3 %}#dc2626{% else %}#f59e0b{% endif %};
            color:white;text-align:center;padding:8px;font-size:0.9rem">
  ⏰ {{ trial_days_left }} days left in your trial —
  <a href="/settings/billing" style="color:white;font-weight:bold">Upgrade now</a>
</div>
{% endif %}
```
