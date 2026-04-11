---
name: debugging
description: Debug running applications, read logs, trace errors, and diagnose issues in production. Use when you need to debug runtime errors, check logs, or trace through code.
---

# Debugging

## Python/Flask

### Enable Debug Mode
```python
app.run(debug=True)
# or
export FLASK_DEBUG=1
flask run
```

### Print Debugging
```python
import pprint
pprint.pprint(variable)

# In templates
{{ debug(value) }}
```

### PDB Debugger
```python
import pdb; pdb.set_trace()
# Commands: n (next), s (step), c (continue), p variable
```

### Debug Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Processing {items}")
```

## Node.js

### Debug
```bash
NODE_DEBUG=http,https node server.js
npm run debug  # if configured
```

### ndb / inspect
```bash
node --inspect server.js
# Then open chrome://inspect
```

## Reading Logs

### Railway Logs
```bash
railway logs -f
railway logs --num 100
```

### Heroku Logs
```bash
heroku logs --tail
heroku logs --ps web.1
```

## Common Issues

### 404 Not Found
- Check route spelling
- Check trailing slashes
- Check URL prefix

### 500 Internal Error
- Check logs for traceback
- Missing environment variable
- Database connection failed

### Connection Refused
- Service down
- Wrong port
- Firewall blocking

### Slow Response
- Database query unoptimized
- N+1 query problem
- Missing index

## Trace Flow

1. **Identify the error** - What's the actual error message?
2. **Find the code** - Which line/file?
3. **Check the inputs** - What data went in?
4. **Add logging** - What does it show?
5. **Fix and test** - Verify the fix