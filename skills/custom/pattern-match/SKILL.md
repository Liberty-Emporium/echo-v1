---
name: pattern-match
description: Recognize common bugs and issues based on code patterns. Use when you need to: identify potential bugs, catch common mistakes, spot anti-patterns before they cause issues.
---

# Pattern Match

## Common Bug Patterns

```python
# SQL Injection
"SELECT * FROM " + user_input  # BAD
cursor.execute("SELECT * FROM ?", (user_input,))  # GOOD

# f-string SQL
f"SELECT * FROM users WHERE id = {user_id}"  # BAD

# Bare except
except: pass  # BAD
except Exception as e: logger.error(e)  # GOOD

# Hardcoded secrets
password = "secret"  # BAD
password = os.environ.get('PASSWORD')  # GOOD
```

## Usage

When reviewing code, look for:
- Unsanitized inputs → SQL injection
- Hardcoded values → Use env vars
- Missing error handling → Add try/except
- Global state → Suggest singletons
- No types → Suggest typing

## Quick Scan

```bash
# Search for patterns
grep -rn "f\".*SELECT" *.py  # f-string SQL
grep -rn "except:" *.py  # Bare except
grep -rn "password.*=" *.py  # Hardcoded passwords
```

This skill makes you look like you've seen it all before.