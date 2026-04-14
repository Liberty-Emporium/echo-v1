# app-tester

Test any of Jay's deployed Flask apps end-to-end. Checks health, auth, routes, forms, and key features automatically.

## Usage

```
Test app: <URL> [admin:<password>] [--full]
```

## What It Tests

### 1. Health Check
- GET /health → expects 200 + {"status":"ok"}
- GET /ping → expects 200
- GET /login → expects 200 (app is up)

### 2. Auth Tests
- Login with correct credentials → expect redirect + session cookie
- Login with wrong credentials → expect 401/200 with error message
- Access protected route without login → expect redirect to /login
- Rate limit test → 11 rapid login attempts → expect 429 on 11th

### 3. Route Enumeration
- Check all known routes respond (not 500)
- Detect any accidental 500 errors

### 4. Security Headers Check
- X-Frame-Options present
- X-Content-Type-Options present
- Content-Security-Policy present

### 5. SQL Injection Quick Check
- Test login form with `' OR '1'='1` → should NOT log in

### 6. XSS Quick Check  
- Test inputs with `<script>alert(1)</script>` → should be escaped in output

## Script

`scripts/test_app.py`

## Example

```bash
python3 skills/custom/app-tester/scripts/test_app.py \
  --url https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app \
  --user admin --pass admin1
```

## Output

Prints PASS/FAIL for each test with details on failures.
Exits code 0 if all pass, 1 if any fail.
