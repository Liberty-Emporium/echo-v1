# Skill: browser-tester

Test any Flask or Django web app using a real Playwright Chromium browser.
Captures HTTP errors, JavaScript exceptions, console warnings, missing content, and redirects.

## When to Use

- User says "test the app", "run browser tests", "check for errors"
- After deploying a fix — verify nothing else broke
- Proactive health check on any Liberty-Emporium app

## Quick Usage

```bash
# Test one app with defaults (reads from scripts/app_configs.py)
python3 echo-v1/skills/custom/browser-tester/scripts/browser_test.py --app gymforge

# Test any app by URL (auto-detects login form)
python3 echo-v1/skills/custom/browser-tester/scripts/browser_test.py \
  --url https://myapp.up.railway.app \
  --email admin@example.com \
  --password secret123 \
  --pages "/" "/dashboard/" "/settings/"

# Test multiple known apps
python3 echo-v1/skills/custom/browser-tester/scripts/browser_test.py --app all

# Watch it run (show browser window)
python3 echo-v1/skills/custom/browser-tester/scripts/browser_test.py --app gymforge --headed

# GymForge multi-role test (built-in preset)
python3 echo-v1/skills/custom/browser-tester/scripts/browser_test.py --app gymforge --roles all
```

## Output

- Color-coded terminal: ✅ pass / ⚠️ warning / ❌ error per page
- JSON results saved to `/tmp/browser_test_results.json`
- Summary line: `Total hard errors: N`

## Requirements

- `playwright` Python package + Chromium: `pip install playwright && playwright install chromium`
- Both are installed on fresh boot via `bootstrap.sh`

## App Config File

Edit `scripts/app_configs.py` to add new apps. Each entry has:
- `url` — base URL
- `login_email` / `login_password` — credentials
- `login_path` — login URL (default: `/auth/login/`)
- `pages` — list of `(path, label, [keywords])` tuples

## Errors Captured

| Type | What |
|------|------|
| HTTP 4xx/5xx | Server/client errors on any page load |
| JS exceptions | Uncaught JavaScript errors |
| Console errors | `console.error()` calls |
| Missing keywords | Expected text not found in page body |
| Redirect loops | Landing on wrong page after navigation |

## Notes

- Each role gets a fresh browser context (separate cookies/session)
- `ALLOWED_HOSTS` errors on Railway show as 400 — check env vars
- Tailwind CDN warning is expected and filtered from error counts
- Use `--timeout 30` to increase page load timeout on slow Railway cold starts
