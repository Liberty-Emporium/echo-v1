# jinja2-safe-css

**Version:** 1.0.0
**Created:** 2026-04-14
**Author:** Echo

## Description

Scan all Jinja2/Flask HTML templates for CSS patterns that will crash the template engine, and auto-fix them by wrapping in `{% raw %}...{% endraw %}` tags.

Born from: Dropship Shipping 500 error caused by `#aiPanel{...}` CSS being read as an unclosed Jinja2 comment.

## The Problem

Jinja2 uses `{#` to start a comment and `#}` to close it.
CSS ID selectors like `#myElement { ... }` appear INSIDE `{ }` blocks all the time.
When CSS has `{#id{`, Jinja2 reads it as an unclosed comment → TemplateSyntaxError → 500.

**Most dangerous CSS patterns:**
```css
@media(max-width:400px){#panel{width:100%;}}   ← CRASHES Jinja2
#element:hover{color:red;}                      ← safe (no {# pattern)
div{color:#333;}                                ← safe (# inside value, not selector)
```

## When To Use

- Before pushing ANY Flask app that has CSS with ID selectors
- After getting a mysterious 500 on a page that renders CSS
- When adding a floating panel, modal, or any component with `#id` CSS

## Detection Script

```python
import re, os, glob

def check_templates(template_dir):
    dangerous = []
    for path in glob.glob(f"{template_dir}/**/*.html", recursive=True):
        with open(path) as f:
            content = f.read()
        # Find {#id or {#anything that looks like CSS not a Jinja2 comment
        matches = re.finditer(r'\{#(?!\s)', content)
        for m in matches:
            line_num = content[:m.start()].count('\n') + 1
            dangerous.append((path, line_num, content[m.start():m.start()+40]))
    return dangerous

issues = check_templates('templates/')
for path, line, snippet in issues:
    print(f"⚠️  {path}:{line} → {snippet!r}")
```

## Fix Script

```python
import re

def fix_jinja2_css(filepath):
    with open(filepath) as f:
        content = f.read()

    # Find <style> blocks and wrap their content in {% raw %}...{% endraw %}
    def wrap_style(m):
        inner = m.group(1)
        if '{#' in inner and '{% raw %}' not in inner:
            return f'<style>{{% raw %}}{inner}{{% endraw %}}</style>'
        return m.group(0)

    fixed = re.sub(r'<style>(.*?)</style>', wrap_style, content, flags=re.DOTALL)

    with open(filepath, 'w') as f:
        f.write(fixed)
    print(f"Fixed: {filepath}")
```

## Rule

> **Before pushing any Flask app: grep templates for `{#` and wrap affected `<style>` blocks in `{% raw %}...{% endraw %}`**

Always check: `grep -rn "{#" templates/` — if output shows CSS lines, fix them.
