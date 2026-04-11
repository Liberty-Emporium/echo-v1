---
name: perf-tuner
description: Find and fix performance issues in code. Use when you need to: speed up slow code, find N+1 queries, optimize database calls, reduce memory usage.
---

# Perf Tuner

## Common Issues

1. **N+1 queries** - Loop with DB call inside
2. **Loading full tables** - SELECT * instead of columns
3. **No pagination** - Loading 10k items at once
4. **No caching** - Same query repeated

## Quick Checks

```python
# Slow? Add timing
import time; start=time.time()
# ... code ...
print(f"Took {time.time()-start}s")

# N+1? Watch queries
from django.db import connection
print(len(connection.queries))
```

## Fixes

- Use `select_related()` for FK
- Use `only()` for needed columns
- Add pagination
- Cache frequent queries