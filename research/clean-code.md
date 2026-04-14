# Clean Code Principles — Research Notes
**Researched:** 2026-04-14 | Echo's Self-Education Session

---

## The Core Principles Every Engineer Must Know

### SOLID (Object-Oriented Design)
| Letter | Principle | Meaning |
|--------|-----------|---------|
| **S** | Single Responsibility | One class/function = one job |
| **O** | Open/Closed | Open for extension, closed for modification |
| **L** | Liskov Substitution | Subclasses should work wherever parent works |
| **I** | Interface Segregation | Don't force classes to implement unused methods |
| **D** | Dependency Inversion | Depend on abstractions, not concretions |

### DRY — Don't Repeat Yourself
Every piece of knowledge should have a single authoritative representation.
```python
# WRONG - same validation duplicated in 3 routes
@app.route('/login')
def login():
    if not request.form.get('email'):
        return error("Email required")
    ...

# RIGHT - one validator used everywhere
def require_fields(*fields):
    for field in fields:
        if not request.form.get(field):
            return error(f"{field} required")
    return None

@app.route('/login')
def login():
    err = require_fields('email', 'password')
    if err: return err
```

### KISS — Keep It Simple, Stupid
The simplest solution that works is almost always the right one.
- Don't use a microservices architecture when a monolith works fine
- Don't add caching until you can measure slowness
- Don't over-engineer schemas before you have real data

### YAGNI — You Aren't Gonna Need It
Don't build features you might need "someday."
- Build for now, refactor when the need is real
- Over-engineering wastes time and creates technical debt
- Exception: security and data isolation (build those right from day 1)

---

## Naming Conventions (Critical for Readable Code)

### Functions — Verbs
```python
# Good
def get_user(user_id): ...
def create_invoice(client_id, amount): ...
def send_welcome_email(email): ...
def validate_stripe_webhook(payload, sig): ...

# Bad
def user(id): ...
def invoice(): ...
def email(): ...
```

### Variables — Nouns, descriptive
```python
# Good
client_slug = request.form.get('slug')
active_subscriptions = Subscription.query.filter_by(active=True).all()
stripe_customer_id = client.stripe_customer_id

# Bad
s = request.form.get('slug')
x = Subscription.query.filter_by(active=True).all()
id = client.stripe_customer_id
```

### Constants — ALL_CAPS
```python
MAX_LOGIN_ATTEMPTS = 5
DEFAULT_TRIAL_DAYS = 14
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
DATA_DIR = os.environ.get('DATA_DIR', '/data')
```

### Booleans — is_, has_, can_, should_
```python
is_admin = user.role == 'admin'
has_active_subscription = user.subscription_status == 'active'
can_access_feature = is_admin or has_active_subscription
should_send_email = not user.email_unsubscribed
```

---

## Function Design Rules

### Rule 1: Functions Should Do ONE Thing
```python
# Bad: does 3 things
def process_signup(data):
    user = User(email=data['email'])
    db.session.add(user)
    db.session.commit()
    send_welcome_email(data['email'])
    stripe_customer = stripe.Customer.create(email=data['email'])
    user.stripe_id = stripe_customer.id
    db.session.commit()
    return user

# Good: orchestrates single-responsibility functions
def process_signup(data):
    user = create_user(data['email'], data['password'])
    send_welcome_email(user.email)
    link_stripe_customer(user)
    return user
```

### Rule 2: Max 3-4 Parameters
```python
# Bad
def create_client(name, email, slug, plan, trial_days, stripe_id, ref_code, admin_email):
    ...

# Good - use a dataclass or dict
@dataclass
class ClientRegistration:
    name: str
    email: str
    slug: str
    plan: str = 'trial'

def create_client(reg: ClientRegistration):
    ...
```

### Rule 3: Return Early (Avoid Deep Nesting)
```python
# Bad — nested if hell
def process_payment(user_id, amount):
    user = User.query.get(user_id)
    if user:
        if user.subscription:
            if user.subscription.active:
                if amount > 0:
                    # actual logic here
                    return True

# Good — return early
def process_payment(user_id, amount):
    user = User.query.get(user_id)
    if not user: return False
    if not user.subscription: return False
    if not user.subscription.active: return False
    if amount <= 0: return False

    # actual logic here — clean, no nesting
    return True
```

---

## Code Comments — When and How

### Good Comments Explain WHY
```python
# Jinja2 treats {# as comment start — wrap CSS in raw to prevent parse error
{% raw %}
#sidebar { display: none; }
{% endraw %}

# Railway wipes /static/ on deploy — using base64 to survive restarts
img_data = f"data:image/png;base64,{encoded}"

# Use idempotency key to prevent duplicate Stripe customers on retry
stripe.Customer.create(email=email, idempotency_key=f"cust_{user_id}")
```

### Bad Comments Explain WHAT (Code Already Shows That)
```python
# This is wrong
i = i + 1  # increment i by 1

# This is fine (no comment needed)
retry_count += 1
```

---

## Error Handling Patterns

### Always Be Specific
```python
# Bad
try:
    do_something()
except Exception as e:
    print(f"Error: {e}")
    return None

# Good
try:
    result = stripe.Customer.create(email=email)
except stripe.error.CardError as e:
    # Card declined — tell user
    return {'error': e.user_message, 'code': 'card_declined'}, 402
except stripe.error.RateLimitError:
    # Stripe rate limit — retry
    time.sleep(1)
    return retry_create_customer(email)
except stripe.error.StripeError as e:
    # Unexpected Stripe error — log and fail gracefully
    app.logger.error(f"Stripe error creating customer: {e}")
    return {'error': 'Payment system temporarily unavailable'}, 503
```

### Structured Error Responses (API)
```python
# Consistent error format across all routes
def error_response(message, status_code=400, code=None):
    return jsonify({
        'success': False,
        'error': message,
        'code': code or 'error'
    }), status_code

def success_response(data, message=None):
    return jsonify({
        'success': True,
        'data': data,
        'message': message
    })
```

---

## Python-Specific Best Practices

### Use Context Managers for Resources
```python
# Good - auto-closes connection
with sqlite3.connect('/data/app.db') as conn:
    conn.execute("PRAGMA journal_mode=WAL")
    result = conn.execute("SELECT * FROM users WHERE id=?", (user_id,))
```

### List Comprehensions > Loops (When Readable)
```python
# Good
active_users = [u for u in users if u.active]
emails = [u.email for u in clients if u.subscription_status == 'active']

# Bad (when too complex — use a loop instead)
result = [transform(x) for x in data if condition1(x) and condition2(x) and condition3(x)]
```

### f-strings for Formatting
```python
# Good
msg = f"Welcome to {app_name}, {user.name}! Your trial ends on {trial_end.strftime('%B %d')}."

# Bad
msg = "Welcome to " + app_name + ", " + user.name + "!"
```

### Type Hints (Add to New Code)
```python
def get_client(slug: str) -> Optional[Client]:
    return Client.query.filter_by(slug=slug).first()

def create_invoice(client_id: int, amount: float, description: str) -> Invoice:
    ...
```

---

## What I'm Changing in My Code Going Forward

1. **Extract service layer** for all new features
2. **Return early** — eliminate nested ifs
3. **Better variable names** — no single-letter variables outside loops
4. **Add type hints** to new functions
5. **Specific exception handling** — no bare `except Exception`
6. **Consistent error responses** — use helper functions
7. **One function = one job** — split any function over 30 lines
