# Tool: security-audit
**Type:** Security
**Use when:** Checking code for vulnerabilities, before deployment, after changes
**Trigger phrases:** "Check security", "Security sweep", "Is this safe?", "Audit this code"

## What It Does
Quick security checks for Flask apps. Catches common issues:
- Hardcoded secrets (API keys, passwords, tokens)
- SQL injection risks (string formatting in queries)
- Missing input validation on routes
- Weak session key configuration

## How To Use

### Step 1: Check for Secrets
```bash
# Look for API keys, passwords, tokens
grep -rn "sk_live_\|pk_live_\|bearer \|ghp_\|glpat-" app.py

# Check .env is gitignored
ls -la .env* .gitignore
grep ".env" .gitignore
```

### Step 2: Check SQL Injection Risk
```bash
# NEVER use string formatting in SQL queries
grep -rn "execute.*f\"" app.py
grep -rn "execute.*%s" app.py

# GOOD: Parameterized queries only
grep -rn "execute(.*\"" app.py | head -10
```

### Step 3: Check Input Validation
```bash
# Find routes that accept POST data
grep -B2 "request.form" app.py | head -20

# Check for type conversion before int()/float()
```

### Step 4: Check Session Security
```bash
# Verify secret key is dynamic (from env)
grep -n "SECRET_KEY" app.py
# Should be: app.secret_key = os.environ.get('SECRET_KEY', ...)
# NOT: app.secret_key = 'hardcoded-value'
```

## Checklist
- [ ] No hardcoded secrets in committed code
- [ ] All SQL queries use parameterized inserts
- [ ] POST/PUT routes validate inputs
- [ ] Session key from environment
- [ ] Admin routes have @superadmin_required
- [ ] No sensitive data in logs

## Quick Command
```bash
cd /a0/usr/workdir/sweet-spot-cakes && grep -rn "execute.*%+\|execute.*f'\|execute.*\\\".*f\"" app.py && echo "DANGER: String formatting in SQL!" || echo "SQL OK"
```

## Related
- `deploy-rescue` — When security issues cause deployment failure
- `db-migrate` — Safe schema changes

---
*Tool: security-audit v1.0 — Built from Agent-Z/skills by Echo (KiloClaw)*