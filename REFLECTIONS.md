# REFLECTIONS.md — Echo's Permanent Lesson Playbook

*Updated after every session. These are hard-won lessons turned into rules.*

---

## 2026-04-18 — New KiloClaw Instance Setup

**REFLECTION:** `exec.security: "allowlist"` blocks ALL commands including `openclaw` CLI itself unless patterns are pre-configured. Setting it breaks everything.
**VERIFIED:** Yes — blocked all exec calls after config change, including `openclaw cron list`.
**STATUS:** Always use `security: "full"` + `ask: "off"`. Do not change security mode without pre-configuring the allowlist patterns first.
**APPLIES TO:** All KiloClaw instances

---

**REFLECTION:** echo-v1 must be cloned to `/root/.openclaw/workspace/echo-v1` OR a symlink must exist there — that's the hardcoded `WORKSPACE` path in `save-brain.sh`.
**VERIFIED:** Yes — save-brain.sh failed with "No such file or directory" when cloned to `/root/.openclaw/echo-v1`.
**STATUS:** Created symlink. Future instances: clone directly to `/root/.openclaw/workspace/echo-v1`.
**APPLIES TO:** echo-v1, save-brain.sh

---

**REFLECTION:** GitLab protected `main` branch cannot be force-pushed. When local is behind remote, use `git pull gitlab main --rebase` then push normally.
**VERIFIED:** Yes — `git push --force` rejected by GitLab with "pre-receive hook declined".
**STATUS:** Always use rebase pattern for GitLab sync. Never force-push to main on GitLab.
**APPLIES TO:** All repos with GitLab mirror

---

**REFLECTION:** Symlinks inside a git repo get committed as symlink objects. Created `workspace/echo-v1 → /root/.openclaw/echo-v1` symlink which got staged and committed, breaking the repo.
**VERIFIED:** Yes — appeared as `create mode 120000 echo-v1` in commit.
**STATUS:** Add `echo-v1` to `.gitignore` in workspace. Never create symlinks inside a tracked git repo.
**APPLIES TO:** echo-v1

---

**REFLECTION:** When credentials are shared in chat (GitHub PAT, GitLab token), remind Jay to rotate them — they're now in chat history. Not urgent if channel is private, but good hygiene.
**VERIFIED:** Preventive.
**STATUS:** Always mention rotation when tokens are shared in chat.
**APPLIES TO:** All credential handling

---

## 2026-04-17 — AI Agent Widget + Demo Sites

**REFLECTION:** OpenRouter model IDs require provider prefix: `google/gemini-flash-1.5`, not `gemini-flash-1.5`.
**VERIFIED:** Yes — short IDs caused API failures.
**STATUS:** Added MODEL_ALIASES map + normalize_model() function + startup migration. Applied to AI Agent Widget.
**APPLIES TO:** Any app using OpenRouter

---

**REFLECTION:** Railway static Python apps need three files: `requirements.txt` (signals Python), `Procfile` (`web: python3 server.py`), and `server.py` bound to `0.0.0.0:$PORT`.
**VERIFIED:** Yes — 502 errors until all three present.
**STATUS:** Added to railway-deploy skill. Required for every Railway Python deployment.
**APPLIES TO:** All Railway Python apps

---

## 2026-04-16 — Multi-Tenant Mastery + CI/CD

**REFLECTION:** GitHub Actions CI/CD eliminates manual Railway redeploys entirely. One `workflow.yml` per repo runs: syntax check → flake8 → push → wait 90s → health check with 8 retries.
**VERIFIED:** Yes — deployed to all 7 apps successfully.
**STATUS:** Template in `scripts/`. Apply to every new app from day one.
**APPLIES TO:** All apps

---

**REFLECTION:** Consignment Solutions URL is `https://web-production-43ce4.up.railway.app` — the project name didn't become the URL because of Railway naming rules at creation time.
**VERIFIED:** Yes — confirmed correct URL.
**STATUS:** Documented in MEMORY.md app list and railway-deploy skill.
**APPLIES TO:** Consignment Solutions

---

**REFLECTION:** Every multi-tenant query MUST include `tenant_id` filter. Missing it is the #1 security bug in multi-tenant SaaS — User A can see User B's data.
**VERIFIED:** Preventive.
**STATUS:** Added to multi-tenant-upgrade skill as first rule. Check every new route.
**APPLIES TO:** All multi-tenant apps

---

## 2026-04-14 — Self-Education Session

**REFLECTION:** SQLite WAL mode must be set at every DB connection: `PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA foreign_keys=ON`. Without it, readers block writers under load.
**VERIFIED:** Research confirmed.
**STATUS:** Added to lessons-learned.md. Apply to all new apps and audit existing ones.
**APPLIES TO:** All apps using SQLite

---

**REFLECTION:** Stripe idempotency keys prevent double-charges on retry. Format: `f"{action}_{user_id}_{date_string}"`. Required on every Stripe call that moves money.
**VERIFIED:** Stripe docs confirmed.
**STATUS:** Added to stripe-billing skill as Critical Rule #1.
**APPLIES TO:** All apps with Stripe

---

**REFLECTION:** jay-portfolio uses `master` branch, NOT `main`. Always check `git branch --show-current` before first push to any repo.
**VERIFIED:** Yes — caused failed deploys early on.
**STATUS:** Added to railway-deploy skill Critical Rules. Check branch every time.
**APPLIES TO:** jay-portfolio, general git practice

---
