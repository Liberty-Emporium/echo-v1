---
name: code-review
description: Catch issues before deployment. Use when you need to: review PRs, find bugs, do pre-deploy checks.
---

# Code Review

## Checklist

### Security
- [ ] No secrets in code
- [ ] Inputs sanitized
- [ ] Auth checks in place
- [ ] No SQL injection

### Functionality  
- [ ] Does what it's supposed to?
- [ ] Edge cases handled?
- [ ] Error handling exists?

### Code Quality
- [ ] Names are clear?
- [ ] Functions are small?
- [ ] No duplicate code?
- [ ] Tests included?

### Performance
- [ ] No N+1 queries?
- [ ] Proper pagination?
- [ ] No memory leaks?

## Quick Review Commands

```bash
# Check complexity
flake8 --max-complexity=10 .

# Check types  
mypy .

# Run tests
pytest -v
```

## Comment Style

- ❌ "This is wrong"
- ✅ "Consider using X here because..."

A good review makes the team better, not just the code.