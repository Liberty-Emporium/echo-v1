---
name: deployment
description: Deploy applications to cloud platforms. Use when you need to deploy to Railway, Render, AWS, or debug deployment issues.
---

# Deployment

## Railway (Recommended)

### Setup
```bash
npm i -g @railway/cli
railway login
railway init
```

### Deploy
```bash
railway up
railway up --prod
railway logs
railway status
```

### Environment
```bash
railway variables set DATABASE_URL=...
railway variables set SECRET_KEY=...
railway run python manage.py migrate
```

## Render

### YAML (render.yaml)
```yaml
services:
  - type: web
    name: myapp
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: DATABASE_URL
        sync: false
```

## Common Issues

### 500 Error on Deploy
1. Check `railway logs` for errors
2. Verify environment variables set
3. Check for missing dependencies
4. Verify port (usually $PORT or 5000)

### Static Files Not Loading
```python
# Flask - add static folder
app = Flask(__name__, static_folder='static')

# Or use WhiteNoise
from whitenoise import WhiteNoise
app.wsgi_app = WhiteNoise(app.wsgi_app)
```

### Database Connection
- Use full connection string: `postgres://user:pass@host:5432/db`
- Check SSL requirements
- Run migrations after deploy

## Health Checks

```bash
curl https://yourapp.railway.app/health
# Should return 200 OK
```