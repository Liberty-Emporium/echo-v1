# Skill: template-debug
**Type:** Debugging
**Use when:** Page looks wrong, CSS broken, nav bar error, Jinja2 error
**Trigger phrases:** "Page looks wrong", "CSS broken", "Nav bar error", "Template issue", "Jinja2 error"

## What It Does
Systematically find and fix HTML/CSS/Jinja2 template issues in Flask apps.

## Common Problems & Fixes

| Symptom | Likely Cause |
|---------|-------------|
| Class name mashed together (nav-itemactive) | Missing space in Jinja2 conditional |
| Wrong page highlighted in nav | Active state logic error |
| Blank page area | Missing `{% block content %}` or `{% extends %}` |
| 500 Internal Server Error | Jinja2 syntax error in template |
| CSS not applying | Missing `{% block extra_css %}` or class typo |

## How To Use

### Step 1: Identify Which Template
```bash
# Find which template renders the route
grep -n "render_template" app.py | grep "/route-name"

# Check the template file
grep -n "class=\"nav-item" templates/base.html
```

### Step 2: Fix Common Patterns

**Missing Space in Conditional Class:**
```jinja2
# BAD
class="nav-item {% if '/prep-sheet' in request.path %}active{% endif %}"
# Result: "nav-itemactive"

# GOOD
class="nav-item {% if '/prep-sheet' in request.path %} active {% endif %}"
# Result: "nav-item active"
```

**Wrong Active State Logic:**
```jinja2
# BAD — catches partial paths
{% if '/orders' in request.path %}

# GOOD — exact match or starts with
{% if request.path == '/orders' or request.path.startswith('/orders/') %}
```

**Missing Block Content:**
```jinja2
# Child template must define content block
{% extends 'base.html' %}
{% block content %}
  <!-- page content here -->
{% endblock %}
```

### Step 3: Validate Before Commit
```bash
# Check Jinja2 syntax
python -c "from jinja2 import Environment; env = Environment(); env.from_string(open('templates/base.html').read())"

# Validate all templates
cd templates && for f in *.html; do python -c "from jinja2 import Environment; env = Environment(); env.from_string(open('$f').read())" && echo "OK: $f"; done
```

## Quick Commands
```bash
# Find all nav-item references
grep -rn "nav-item" templates/

# Find class attributes with Jinja2 conditionals
grep -rn 'class=".*{%' templates/
```

## Related
- `deploy-rescue` — When template errors cause boot failure
- `security-audit` — Check for XSS in template rendering

---
*Skill: template-debug v1.0 — Absorbed from Agent-Z, enhanced by Echo (KiloClaw)*