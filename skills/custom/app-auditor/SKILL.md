---
name: app-auditor
description: Find, analyze, and fix errors in any application codebase. Use when you need to audit an app for bugs, run diagnostics, lint, type-check, or fix common errors. Supports Python (Flask/Django), Node.js (Express/React), and other frameworks.
---

# App Auditor

## Overview

Detects the language/framework of an app, runs appropriate diagnostics (linters, type checkers, tests), identifies errors, and optionally fixes them.

## Workflow

### Step 1: Detect Language & Framework

Check the project structure to identify what we're working with:

```
- Python: presence of requirements.txt, setup.py, pyproject.toml, Pipfile, *.py files
- Node.js: package.json, package-lock.json, node_modules/, *.js ts files
- Go: go.mod, *.go files
- Ruby: Gemfile, *.rb files
- PHP: composer.json, *.php files
```

### Step 2: Run Diagnostics

Based on detected language, run appropriate checks:

**Python (Flask/Django)**
```bash
# Static analysis
flake8 . --select=E9,F63,F7,F82
python -m py_compile *.py

# Flask-specific
python -c "from app import app" 2>&1 || true
python manage.py check 2>&1 || true  # Django

# Type checking (if present)
mypy . 2>&1 || true
```

**Node.js**
```bash
# Static analysis
npx eslint . 2>&1 || true
npx tsc --noEmit 2>&1 || true

# Build check
npm run build 2>&1 || true
npm run lint 2>&1 || true
```

**General (any language)**
```bash
# Check for syntax errors
find . -name "*.py" -o -name "*.js" -o -name "*.ts" | xargs -I {} python -m py_compile {} 2>&1 || true

# Look for common error patterns
grep -rn "except:" . --include="*.py" | grep -v "traceback\|logger" || true
grep -rn "TODO\|FIXME\|XXX\|HACK\|BUG" . --include="*.py" --include="*.js" || true

# Check for hardcoded secrets
grep -rn "password\s*=\s*['\"]" . --include="*.py" --include="*.js" || true
grep -rn "api[_-]?key\|secret\|token" . --include="*.py" --include="*.js" | grep -v "os.environ\|os.getenv" || true
```

### Step 3: Attempt Runtime Start

Try to start the app and capture any immediate errors:

**Python/Flask**
```bash
python app.py 2>&1 | head -50
python run.py 2>&1 | head -50
```

**Node.js**
```bash
node server.js 2>&1 | head -50
npm start 2>&1 | head -50
```

### Step 4: Report Findings

Compile a structured report:

```
## Audit Report: [repo name]
### Environment
- Language: Python/Node.js/etc.
- Framework: Flask/Django/Express/React/etc.

### Errors Found
1. [File:line] - [error description]
2. [File:line] - [error description]

### Warnings
1. [File:line] - [warning description]

### Suggested Fixes
- [Fix description]
```

### Step 5: Apply Fixes

For common errors, apply fixes:

- **Import errors**: Fix missing imports, incorrect paths
- **Syntax errors**: Correct syntax issues
- **Missing dependencies**: Add to requirements.txt/package.json
- **Type errors**: Fix type annotations
- **Linting errors**: Apply auto-fixable fixes where possible

## Auto-Fixable Issues

The skill can automatically fix:
- Missing newlines at EOF
- Trailing whitespace
- Auto-fixable ESLint rules (`npx eslint . --fix`)
- Auto-fixable flake8 (via pre-commit or autoflake)
- Common import ordering (isort)

Run with confirmation before applying fixes.