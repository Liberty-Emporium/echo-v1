# Flask & Python — Production Best Practices
**Researched:** 2026-04-14 | Echo's Self-Education Session

---

## The #1 Problem With Our Current Flask Apps

Right now, all our apps have business logic IN the route handlers. This is the most common Flask mistake that kills SaaS projects at scale.

**Wrong (what we currently do):**
```python
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    # validation here
    # database query here
    # business logic here
    # email sending here
    # token generation here
    return jsonify(...)
```

**Right (service layer pattern):**
```python
@app.route('/register', methods=['POST'])
def register():
    result, error = auth_service.register_user(
        email=request.form.get('email'),
        password=request.form.get('password')
    )
    if error:
        return error_response(error.message, error.status_code)
    return success_response(result.user_data)
```

---

## Production Flask Architecture (The Folder Structure That Scales)

```
backend/
├── app/
│   ├── __init__.py          # Application factory (create_app)
│   ├── extensions.py        # db, migrate, mail, cors — instantiated without app
│   ├── config/
│   │   ├── base.py          # Shared settings (SECRET_KEY, STRIPE, etc.)
│   │   ├── development.py   # DEBUG=True, SQLite
│   │   └── production.py    # DEBUG=False, DATABASE_URL from env
│   ├── models/
│   │   ├── user.py
│   │   ├── subscription.py
│   │   └── mixins.py        # Timestamps, soft delete — shared model logic
│   ├── routes/
│   │   ├── auth.py          # Login, register, logout
│   │   ├── payments.py      # Checkout, billing
│   │   ├── webhooks.py      # Stripe webhooks
│   │   └── admin.py         # Admin only
│   ├── services/            # ← THE MOST IMPORTANT LAYER
│   │   ├── auth_service.py  # Token gen, password hashing
│   │   ├── stripe_service.py# ALL Stripe API calls
│   │   ├── email_service.py # Transactional emails
│   │   └── user_service.py  # User CRUD
│   ├── middleware/
│   │   ├── auth_middleware.py   # JWT decorator
│   │   └── admin_middleware.py  # Role check
│   └── utils/
│       ├── responses.py     # Standardized JSON responses
│       └── errors.py        # Error handlers
├── tests/
│   ├── conftest.py          # Test fixtures
│   ├── test_auth.py
│   └── test_payments.py
└── wsgi.py                  # Production entry point
```

### Application Factory Pattern (Critical)
```python
# app/__init__.py
def create_app(config_name=None):
    app = Flask(__name__)
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(f'app.config.{config_name}.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, origins=app.config['ALLOWED_ORIGINS'])
    
    from app.routes import register_blueprints
    register_blueprints(app)
    return app
```

### Extensions — Circular Import Prevention
```python
# app/extensions.py — instantiate WITHOUT app, init in factory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()
migrate = Migrate()
```

### Config Pattern — Never Use If Statements
```python
# base.py
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

# production.py
from app.config.base import Config
class Config(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

---

## OWASP Top 10 — Flask Security Checklist

### Must-Have Security Extensions
```python
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from flask_talisman import Talisman  # Forces HTTPS + security headers

csrf = CSRFProtect(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["100 per hour"])
talisman = Talisman(app, force_https=True)
```

### OWASP Top 10 — Applied to Flask

| Risk | Flask Fix |
|------|-----------|
| A01 Broken Access Control | RBAC decorators, check tenant_id on every query |
| A02 Cryptographic Failures | Flask-Talisman (HTTPS), bcrypt passwords, secure sessions |
| A03 Injection | SQLAlchemy ORM (parameterized), never raw SQL with user input |
| A04 Insecure Design | Service layer, principle of least privilege |
| A05 Security Misconfiguration | Env vars for secrets, no DEBUG in prod |
| A06 Vulnerable Components | pip-audit, keep requirements.txt updated |
| A07 Auth Failures | Flask-Limiter (rate limit login), secure session flags |
| A08 Software Integrity | Verify webhook signatures (Stripe sig check) |
| A09 Logging Failures | Structured logs, log auth events |
| A10 SSRF | Validate/whitelist external URLs before requests |

### Session Security Config
```python
app.config['SESSION_COOKIE_SECURE'] = True      # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True     # No JS access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict' # No CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 min timeout
```

### Rate Limiting (Brute Force Prevention)
```python
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # 5 attempts per minute
def login():
    ...
```

---

## SQLite in Production — What We Need to Know

### The Verdict: SQLite is Fine for Our Stage
- Under 500 write TPS: SQLite wins
- Under 100GB data: SQLite fine
- Under 1M users: SQLite fine
- Read-heavy apps (our apps are): SQLite is 2-37x FASTER than Postgres

### The PRAGMAs That Matter (Set on Every Connection!)
```sql
PRAGMA journal_mode = WAL;       -- Concurrent reads during writes (CRITICAL)
PRAGMA synchronous = NORMAL;     -- 2x write speedup vs FULL
PRAGMA mmap_size = 268435456;    -- 256MB memory-mapped I/O
PRAGMA cache_size = -64000;      -- 64MB page cache
PRAGMA busy_timeout = 5000;      -- 5s wait on lock contention
PRAGMA foreign_keys = ON;        -- Enforce referential integrity
```

In Python/Flask:
```python
@app.teardown_appcontext
def close_db(error):
    pass

def get_db():
    conn = sqlite3.connect('/data/app.db')
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn
```

### When to Upgrade to PostgreSQL
| Signal | Threshold |
|--------|-----------|
| Write TPS | >500 sustained |
| DB size | >50-100GB |
| Backend team | >3 engineers |
| Multi-region | Any |

### Litestream — Our Backup Strategy (When We Move Off Railway)
- Continuously replicates WAL changes to S3
- Sub-second lag, <1ms overhead
- Cost: ~$0.50/month per 1GB DB
- Restore: single command
- **PLAN: Add this when we migrate to Fly.io**

---

## What I'm Changing in Our Apps Going Forward

1. **Add WAL PRAGMA** to all SQLite connections at startup
2. **Refactor toward service layer** — start with new features
3. **Add Flask-Limiter** to all login routes (5/min limit)
4. **Set session cookie flags** (secure, httponly, samesite) in all apps
5. **Never put secrets in code** — all via os.environ
6. **Application factory pattern** for all new apps
