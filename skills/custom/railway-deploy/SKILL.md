# railway-deploy

**Version:** 1.0.0
**Created:** 2026-04-13
**Author:** Echo

## Description

Full Railway deploy cycle: detect branch, push code, wait for deployment, verify URL is live, return confirmation. Eliminates manual push + wait + curl check cycle.

Born from: multiple failed pushes to `main` when repo was on `master` during 2026-04-13 session.

## When To Use

- After making code changes to any Railway-hosted repo
- Before telling Jay "it's deployed"
- When verifying a new feature is live on Railway

## Steps

1. **Detect branch:** `git branch --show-current`
2. **Set auth remote:** `git remote set-url origin https://$(cat /root/.secrets/github_token)@github.com/Liberty-Emporium/REPO.git`
3. **Push:** `git push origin BRANCH`
4. **Wait 25-30 seconds** (Railway build time)
5. **Verify:** `curl -o /dev/null -w "%{http_code}" URL`
6. **Check content:** `curl -s URL | grep "EXPECTED_STRING"`
7. **Report** success or failure to Jay

## Critical Rules

- **jay-portfolio uses `master` NOT `main`** — always check branch first
- Always check branch with `git branch` before first push to any repo
- Railway wipes `/static/uploads/` on every deploy — use base64 for images
- Default wait time: 25-30 seconds after push before verifying

## Railway App URLs

| App | URL |
|-----|-----|
| jay-portfolio | https://jay-portfolio-production.up.railway.app |
| liberty-inventory | https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app |
| dropship-shipping | https://dropship-shipping-production.up.railway.app |
| contractor-pro-ai | https://contractor-pro-ai-production.up.railway.app |
| pet-vet-ai | https://pet-vet-ai-production.up.railway.app |
| ai-api-tracker | https://ai-api-tracker-production.up.railway.app |
| consignment-solutions | https://web-production-43ce4.up.railway.app |
