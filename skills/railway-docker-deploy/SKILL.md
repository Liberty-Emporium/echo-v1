# Railway Docker Deploy Skill
> Lessons learned deploying Python + Node.js apps on Railway. Hard-won.

---

## THE #1 RULE: Use a Dockerfile when you need multiple runtimes

nixpacks is great for pure Python or pure Node apps. The moment you need BOTH:
- Node is only available at **build time**, not runtime
- `npm install -g` puts binaries in a path that gunicorn/Flask can't see
- `npx` resolves to nothing if npm global bin isn't on PATH at runtime
- `shutil.which()` returns None even if the package is installed

**Always use a Dockerfile for Python + Node.** nixpacks will fight you.

---

## Working Dockerfile: Python + Node + Chromium + FFmpeg

```dockerfile
FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        chromium \
        curl ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*

# Node.js 22 via NodeSource — available at RUNTIME (not just build)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python deps first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Node deps — npm ci uses package-lock.json for reproducible installs
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Tell HyperFrames (or any headless Chrome tool) where Chrome is
ENV HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium

COPY . .

EXPOSE 8080
CMD gunicorn app:app --timeout 300 --workers 2 --worker-class gthread --threads 4 --bind 0.0.0.0:${PORT:-8080}
```

---

## nixpacks.toml — what NOT to do

```toml
# ❌ WRONG — this replaces pip install entirely:
[phases.install]
cmds = ["npm install"]

# ❌ ALSO WRONG — nodejs_22 is build-only, not runtime:
[phases.setup]
nixPkgs = ["ffmpeg", "nodejs_22"]
```

If you must use nixpacks with node, add BOTH commands:
```toml
[phases.install]
cmds = ["pip install -r requirements.txt", "npm install"]
```

---

## Finding npm binaries reliably (Python)

```python
import os, shutil, subprocess

def find_node_bin(name: str) -> str | None:
    """Find an npm-installed binary. Checks local node_modules first."""
    here = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Local node_modules (most reliable on Railway)
    local = os.path.join(here, 'node_modules', '.bin', name)
    if os.path.isfile(local):
        return local
    
    # 2. /app/node_modules (Railway Docker workdir)
    app_local = f'/app/node_modules/.bin/{name}'
    if os.path.isfile(app_local):
        return app_local
    
    # 3. PATH
    return shutil.which(name)
```

---

## Railway data persistence — CRITICAL

Railway containers are **ephemeral**. Every deploy wipes:
- Any files written at runtime (users.json, uploads, etc.)
- Anything not in the Docker image or a mounted volume

**Solution:** Add a Railway Volume and set `DATA_DIR` env var to the mount path.

```
Railway Dashboard → your service → Volumes → Add Volume
Mount path: /data
Then set env var: DATA_DIR=/data
```

In Python:
```python
DATA_DIR = os.environ.get('DATA_DIR', os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
```

Without a volume: **user accounts, inventory changes, and uploads reset on every deploy.**

---

## Railway deploy checklist

- [ ] Dockerfile present? (required for Python + Node)
- [ ] `package.json` + `package-lock.json` committed? (`npm ci` needs both)
- [ ] `node_modules/` in `.gitignore`? (don't commit, let `npm ci` build it)
- [ ] `DATA_DIR` env var pointing to a persistent volume?
- [ ] `PORT` env var used in CMD? Railway assigns a random port
- [ ] Gunicorn `--timeout 300` for long video renders?
- [ ] Health check route (`/health`) returning JSON?

---

## Common Railway errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `[Errno 2] No such file or directory: 'npx'` | npx not on PATH at runtime | Use Dockerfile + npm ci |
| `binary not found` | nixpacks nodejs_22 = build only | Switch to Dockerfile |
| Users/data reset on deploy | No persistent volume | Add Railway Volume |
| `SIGTERM` on npm install | nixpacks phase timeout | Use Dockerfile instead |
| `pip install` skipped | nixpacks install cmds override | Include pip in cmds array |
