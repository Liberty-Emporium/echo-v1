---
name: legacy-whisper
description: Work confidently with old, messy code. Use when you need to: modify old codebases, fix legacy bugs, extend ancient features.
---

# Legacy Whisper

## The Golden Rules

1. **Don't rewrite what works** - If it runs, don't touch
2. **Test first** - Add tests before any change
3. **Match the style** - Old code uses old patterns
4. **Small changes** - One thing at a time

## Common Legacy Patterns

```python
# Global state
global_db = None

# Cached globals
MY_CACHE = {}

# Old-style classes
class Old(object):
    pass

# No types
def func(x, y):
    return x + y
```

## Working Rules

- **Read more, type less**
- **Copy existing patterns exactly**
- **When confused, print() is your friend**
- **Comment what you're doing**
- **Don't fix multiple things at once**

## Questions to Ask

1. Does it work now?
2. What's the minimal change needed?
3. What's the test?