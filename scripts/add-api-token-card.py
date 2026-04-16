#!/usr/bin/env python3
"""
add-api-token-card.py
=====================
Injects an admin-only API token generator card into each app's settings page.
- Adds /api/token/ui POST + DELETE routes to app.py
- Adds the UI card to the settings/admin template (admin-only, hidden from regular users)
- Pushes to GitHub

Usage: python3 add-api-token-card.py
"""

import subprocess, base64, json, sys, re

GH_TOKEN = open('/root/.secrets/github_token').read().strip()
ORG = "Liberty-Emporium"

# Per-app config: repo, branch, app.py path, template path, admin session check
APPS = [
    {
        "repo":     "Consignment-Solutions",
        "branch":   "main",
        "template": "templates/settings.html",
        "admin_check": "session.get('super_admin_id')",
        "jinja_check": "session.get('super_admin_id')",
    },
    {
        "repo":     "Contractor-Pro-AI",
        "branch":   "main",
        "template": "templates/settings.html",
        "admin_check": "session.get('role') == 'admin'",
        "jinja_check": "session.get('role') == 'admin'",
    },
    {
        "repo":     "Pet-Vet-AI",
        "branch":   "master",
        "template": "templates/settings.html",
        "admin_check": "session.get('is_admin')",
        "jinja_check": "session.get('is_admin')",
    },
    {
        "repo":     "Dropship-Shipping",
        "branch":   "main",
        "template": "templates/my_settings.html",
        "admin_check": "session.get('role') == 'admin'",
        "jinja_check": "session.get('role') == 'admin'",
    },
]

# The backend routes to inject (parameterized per admin_check)
ROUTES_TEMPLATE = '''
# ── Admin-only API token UI routes ───────────────────────────────────────────
@app.route('/api/token/ui', methods=['POST'])
def api_token_ui_generate():
    if not {admin_check}:
        return jsonify({{'error': 'Admin only'}}), 403
    import secrets as _s, hashlib as _h, datetime as _dt
    user_id = session.get('user_id') or session.get('super_admin_id') or 1
    label = 'ui-generated'
    raw_token = _s.token_urlsafe(48)
    token_hash = _h.sha256(raw_token.encode()).hexdigest()
    expires_at = (_dt.datetime.utcnow() + _dt.timedelta(days=365)).isoformat()
    conn = get_db()
    try:
        conn.execute('CREATE TABLE IF NOT EXISTS api_tokens (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, token_hash TEXT UNIQUE, label TEXT, expires_at TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
        conn.execute('DELETE FROM api_tokens WHERE user_id=? AND label=?', (user_id, label))
        conn.execute('INSERT INTO api_tokens (user_id,token_hash,label,expires_at) VALUES (?,?,?,?)', (user_id, token_hash, label, expires_at))
        conn.commit()
    finally:
        conn.close()
    return jsonify({{'success':True,'api_token':raw_token,'expires_at':expires_at}})

@app.route('/api/token/ui', methods=['DELETE'])
def api_token_ui_revoke():
    if not {admin_check}:
        return jsonify({{'error': 'Admin only'}}), 403
    user_id = session.get('user_id') or session.get('super_admin_id') or 1
    conn = get_db()
    try:
        conn.execute('DELETE FROM api_tokens WHERE user_id=? AND label=?', (user_id, 'ui-generated'))
        conn.commit()
    finally:
        conn.close()
    return jsonify({{'success':True}})

'''

# The UI card HTML to inject before </div>\n</div> or before {% endblock %}
UI_CARD_TEMPLATE = '''
  {{% if {jinja_check} %}}
  <!-- Admin-only API Access Card -->
  <div class="card" style="margin-top:24px;padding:20px;">
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:14px;">
      <strong>&#x1F916; API Access Token</strong>
      <span style="font-size:0.78rem;opacity:.6;">Admin only &mdash; for programmatic access</span>
    </div>
    <div id="apiTokenBox" style="display:none;margin-bottom:14px;">
      <label style="font-size:0.82rem;opacity:.7;display:block;margin-bottom:6px;">Your API Token (shown once &mdash; copy it now!)</label>
      <div style="display:flex;gap:8px;align-items:center;">
        <input type="text" id="apiTokenValue" readonly style="font-family:monospace;font-size:0.82rem;flex:1;cursor:text;">
        <button type="button" onclick="copyApiToken()" class="btn btn-outline btn-sm">&#x1F4CB; Copy</button>
      </div>
      <p style="margin-top:8px;font-size:0.78rem;color:#fbbf24;">&#x26A0;&#xFE0F; Save this token now &mdash; it won't be shown again. Use as: <code>Authorization: Bearer TOKEN</code></p>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;">
      <button type="button" onclick="generateApiToken()" class="btn btn-primary btn-sm" id="genApiBtn">&#x26A1; Generate Token</button>
      <button type="button" onclick="revokeApiToken()" class="btn btn-outline btn-sm" style="color:#f87171;border-color:#f87171;">&#x1F5D1;&#xFE0F; Revoke</button>
    </div>
  </div>
  {{% endif %}}
'''

UI_JS = '''
<script>
async function generateApiToken() {
  const btn = document.getElementById('genApiBtn');
  btn.disabled = true; btn.textContent = 'Generating...';
  try {
    const res = await fetch('/api/token/ui', {method:'POST', credentials:'same-origin', headers:{'Content-Type':'application/json'}});
    const data = await res.json();
    if (data.api_token) {
      document.getElementById('apiTokenValue').value = data.api_token;
      document.getElementById('apiTokenBox').style.display = 'block';
      btn.textContent = '✓ Generated';
    } else { alert(data.error || 'Failed'); btn.textContent = '⚡ Generate Token'; }
  } catch(e) { alert(e.message); btn.textContent = '⚡ Generate Token'; }
  btn.disabled = false;
}
async function revokeApiToken() {
  if (!confirm('Revoke token?')) return;
  const res = await fetch('/api/token/ui', {method:'DELETE', credentials:'same-origin', headers:{'Content-Type':'application/json'}});
  const data = await res.json();
  if (data.success) { document.getElementById('apiTokenBox').style.display='none'; alert('✅ Revoked.'); }
}
function copyApiToken() {
  navigator.clipboard.writeText(document.getElementById('apiTokenValue').value).then(() => {
    const btn = event.target; btn.textContent = '✅ Copied!'; setTimeout(()=>btn.textContent='📋 Copy',2000);
  });
}
</script>
'''

def gh_get(repo, path, branch):
    result = subprocess.run([
        "curl", "-s",
        f"https://api.github.com/repos/{ORG}/{repo}/contents/{path}?ref={branch}",
        "-H", f"Authorization: token {GH_TOKEN}"
    ], capture_output=True, text=True)
    return json.loads(result.stdout)

def gh_put(repo, path, branch, content_b64, sha, message):
    payload = json.dumps({"message": message, "content": content_b64, "sha": sha, "branch": branch})
    result = subprocess.run([
        "curl", "-s", "-X", "PUT",
        f"https://api.github.com/repos/{ORG}/{repo}/contents/{path}",
        "-H", f"Authorization: token {GH_TOKEN}",
        "-H", "Content-Type: application/json",
        "-d", payload
    ], capture_output=True, text=True)
    data = json.loads(result.stdout)
    return data.get("commit", {}).get("sha", "ERROR: " + result.stdout[:200])

def process_app(cfg):
    repo     = cfg["repo"]
    branch   = cfg["branch"]
    tmpl     = cfg["template"]
    adm      = cfg["admin_check"]
    jinja    = cfg["jinja_check"]

    print(f"\n{'='*50}")
    print(f"Processing: {repo}")

    # ── 1. Patch app.py ──────────────────────────────
    app_data = gh_get(repo, "app.py", branch)
    if "content" not in app_data:
        print(f"  ❌ app.py not found: {app_data.get('message')}")
        return

    app_src = base64.b64decode(app_data["content"]).decode("utf-8")

    if "/api/token/ui" in app_src:
        print(f"  ⏭️  app.py already has /api/token/ui — skipping")
    else:
        # Find last @app.route to inject before it, or just append before if __name__
        inject_routes = ROUTES_TEMPLATE.format(admin_check=adm)
        if "if __name__" in app_src:
            app_src = app_src.replace("if __name__", inject_routes + "if __name__", 1)
        else:
            app_src += inject_routes

        new_b64 = base64.b64encode(app_src.encode()).decode()
        sha = app_put = gh_put(repo, "app.py", branch, new_b64, app_data["sha"],
                               "🔧 Add admin-only /api/token/ui routes")
        print(f"  ✅ app.py patched → {sha[:12]}")

    # ── 2. Patch template ────────────────────────────
    tmpl_data = gh_get(repo, tmpl, branch)
    if "content" not in tmpl_data:
        print(f"  ❌ template {tmpl} not found: {tmpl_data.get('message')}")
        return

    tmpl_src = base64.b64decode(tmpl_data["content"]).decode("utf-8")

    if "generateApiToken" in tmpl_src:
        print(f"  ⏭️  Template already has API card — skipping")
        return

    card_html = UI_CARD_TEMPLATE.format(jinja_check=jinja)

    # Inject card before {% endblock %} of content block
    if "{% endblock %}" in tmpl_src:
        # Insert before the last endblock
        idx = tmpl_src.rfind("{% endblock %}")
        tmpl_src = tmpl_src[:idx] + card_html + "\n" + tmpl_src[idx:]
    else:
        tmpl_src += card_html

    # Inject JS before </body> or at end
    if "</body>" in tmpl_src:
        tmpl_src = tmpl_src.replace("</body>", UI_JS + "\n</body>", 1)
    elif "{% endblock %}" in tmpl_src:
        tmpl_src += "\n{% block extra_js %}{% endblock %}\n" + UI_JS
    else:
        tmpl_src += UI_JS

    new_b64 = base64.b64encode(tmpl_src.encode()).decode()
    sha = gh_put(repo, tmpl, branch, new_b64, tmpl_data["sha"],
                 "✨ Add admin-only API token card to settings")
    print(f"  ✅ {tmpl} patched → {sha[:12]}")


if __name__ == "__main__":
    for app_cfg in APPS:
        process_app(app_cfg)
    print("\n\n✅ All done! All apps now have admin-only API token cards.")
