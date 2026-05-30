# SKILL: Deployment Automation

> One-command deployment to Railway, Vercel, Render.

## Railway (Primary)
```bash
npm install -g @railway/cli
railway login
railway init
railway up
railway logs
railway variables set KEY=value
```

## Railway Config
```json
{
  "build": { "builder": "NIXPACKS" },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 60
  }
}
```

## Vercel (Frontend)
```bash
npm install -g vercel
vercel --prod
vercel env add KEY production
```

## Docker (Universal)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser --disabled-password appuser
USER appuser
EXPOSE 8000
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "2"]
```

## Health Check (Required)
```python
@app.get("/health")
async def health():
    checks = {}
    try:
        db.execute("SELECT 1"); checks["database"] = "ok"
    except: checks["database"] = "error"
    return {"status": "ok", "checks": checks}
```

## Security Headers
```python
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])
```
