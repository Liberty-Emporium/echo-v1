---
name: code-reader
description: Quickly understand and explain large codebases. Use when you need to: understand a new project, explain code to others, find the right function, navigate unfamiliar code.
---

# Code Reader

## Quick Analysis

1. **Find entry points**: `grep -n "def main\|if __name__" *.py`
2. **Find routes**: `grep -n "@app.route\|@bp.route" *.py`
3. **Find imports**: `grep -n "^import\|^from" *.py | head -20`
4. **Find config**: `*.env, config.py, settings.py`

## Explain Code

When asked to explain:
- Start with purpose (what does it do?)
- Show key functions
- Explain data flow
- Note dependencies

## Navigation

```bash
# Find a function
grep -n "def my_func" *.py

# Find where variable is used
grep -rn "my_var" *.py

# Find imports of a module
grep -rn "from my_module" *.py
```

A 50-year vet knows: read the entry point, trace the flow, check the config.