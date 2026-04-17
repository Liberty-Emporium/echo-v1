# Lessons Learned — Multi-Tenant & Wizard UX (2026-04-16)
*Hard lessons from today. Read this before touching wizard or store pages.*

---

## Lesson 1: The Wizard Success Screen Must Reference Real DOM IDs

**What happened:** The wizard `/wizard-submit` endpoint responded in 0.3 seconds. But the browser sat spinning for 4+ minutes. Jay almost gave up.

**Why:** The `.then()` callback called `document.getElementById('successStoreName').textContent = ...` but `id="successStoreName"` didn't exist in the HTML. JS threw a null reference error silently. The success screen never showed.

**Rule:** Before writing JS that touches the DOM, grep the template for the ID first.
```bash
grep -n "id=\"successStoreName\"" templates/wizard.html
# If empty — it doesn't exist. Add it to HTML first.
```

---

## Lesson 2: The Provisioned Store Page Must Use Tenant Data — Not Global Data

**What happened:** After the wizard built "Willies Thrift", the store page showed:
- Nav: "Liberty Emporium & Thrift" (the global STORE_NAME, not the tenant's)
- Hero: generic 🏪 emoji and a black box
- Tagline: "1 willie" (wrong field pulled)
- Demo bar: "Exploring Storewillies 3" (URL path parsed badly)

**Root causes:**
1. `base.html` uses `store_name` from `ctx()` which reads the global `STORE_NAME` — not the tenant's config
2. The hero used `config.logo_url` which was empty, fell back to 🏪
3. The tagline pulled `config.contact_phone` somehow
4. Demo bar did `request.path.replace('/','').replace('-',' ').title()` = garbled

**Fixes applied:**
- Store page injects JS to override nav logo with `config.store_name`
- Hero now shows styled first-letter initial (W, J, etc.) in frosted glass
- Hero background uses `config.primary_color` in a gradient instead of flat color
- Demo bar now uses if/elif for clean human-readable labels per path

**Rule:** Store pages (tenant-specific) must override global template values. Use JS DOM override or a dedicated `{% block %}` for things like nav brand, page title, etc.

---

## Lesson 3: Show/Hide Eye Toggle on ALL Password Fields

Jay said it: **password fields ALWAYS have show/hide eye toggle.** Non-negotiable. When building any form with a password field, always add:

```html
<div style="position:relative;">
  <input type="password" id="myPwd" name="password">
  <button type="button" onclick="togglePwd('myPwd',this)"
          style="position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;font-size:1.1rem;">👁️</button>
</div>
<script>
function togglePwd(id, btn) {
  var f = document.getElementById(id);
  f.type = f.type === 'password' ? 'text' : 'password';
  btn.textContent = f.type === 'password' ? '👁️' : '🙈';
}
</script>
```

---

## Lesson 4: The Demo Experience Must Sell — Not Just Show

A generic "view only" banner does nothing. The demo needs:
1. **Sticky top bar** — "You're in Demo Mode" + CTA button visible at all times
2. **Feature grid on dashboard** — show every feature with click-to-explore
3. **Signup wall** for locked features — pops up with benefits + pricing when they click locked items
4. **Pitch card at 30 seconds** — floats in bottom-right with pricing and big CTA
5. **Tooltips on nav links** — hover to learn what each section does
6. **All CTA buttons say the same thing** — we used "Get Inventory Management Now" everywhere

**Don't block demo users from seeing features.** Let them explore, then hit a wall only when they try to write data (add product, edit, delete). Read-only pages should all be accessible.

---

## Lesson 5: Slug Generation Edge Cases

When a user types "willies" as their store name:
- `slugify("willies")` → `"willies"`  
- If `/data/customers/willies/` already exists → `"willies-2"`
- The URL becomes `/store/willies-2` — fine

But watch out: if they type their own name like "Willie Smith":
- → `"willie-smith"` — good

If they type "Admin" or "API":
- → `"admin"` — BLOCKED (reserved word list)

Always validate slugs. Never trust user input for file paths.

---

## Lesson 6: Datetime Import Scope

`import datetime` at module level gives you the **module**, not the class.

```python
import datetime
datetime.utcnow()        # ❌ AttributeError: module has no attribute 'utcnow'
datetime.datetime.utcnow()  # ✅ Works

# Or import inside function:
from datetime import datetime as _dt
_dt.utcnow()  # ✅ Works
```

This caused a 500 error on the API key generator today. Cost Jay time. Never again.

---

## Lesson 7: Railway CDN Caches 404s

If Railway's Fastly CDN hits a route that returns 404, **it caches that 404**. Future requests to the same URL return 404 even after you fix the code.

**Fix:** Use a new URL the CDN has never seen before, or add `Cache-Control: no-store` headers to health endpoints.

```python
@app.route('/health-check')  # new URL, not /health
def health_check():
    return jsonify({'status': 'ok'}), 200, {
        'Cache-Control': 'no-store, no-cache, must-revalidate'
    }
```

---

## Lesson 8: When `login_required` vs `admin_required` vs Nothing

```
Public (no auth):     /, /wizard, /pricing, /health-check, /store/<slug>/login
Login required:       /dashboard, /inventory, /ads, /settings
Admin required:       /admin/*, /overseer/*, /admin/api-generator
Tenant required:      Any route that reads/writes tenant data
```

API generator is **admin only** — if a non-admin hits it, return 403. Don't redirect to login, that reveals the route exists.

---

*Echo's personal lesson log — written 2026-04-16 after a full day of building*
