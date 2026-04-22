# Overseer Admin Panel Patterns

## Overseer Login & Role Check

```python
def overseer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') not in ('overseer', 'admin') and \
           session.get('username') not in ('admin', 'overseer'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
```

## Tenant Health Dashboard

```python
@app.route('/overseer')
@overseer_required
def overseer():
    tenants = _get_tenant_health()
    return render_template('overseer.html', tenants=tenants)

def _get_tenant_health():
    import datetime as _dt
    stores = []
    if not os.path.exists(CUSTOMERS_DIR):
        return stores
    for slug in os.listdir(CUSTOMERS_DIR):
        cfg_path = os.path.join(CUSTOMERS_DIR, slug, 'config.json')
        if not os.path.isdir(os.path.join(CUSTOMERS_DIR, slug)):
            continue
        try:
            import json
            cfg = json.load(open(cfg_path)) if os.path.exists(cfg_path) else {}
        except Exception:
            cfg = {}

        status    = get_trial_status(slug)
        trial_end = cfg.get('trial_ends', '')
        days_left = 0
        if status == 'active' and trial_end:
            days_left = max(0, (_dt.datetime.fromisoformat(trial_end)
                                - _dt.datetime.utcnow()).days)

        # Estimate MRR
        mrr = 20.0 if cfg.get('plan') == 'starter' else \
              49.0 if cfg.get('plan') == 'pro' else 0

        stores.append({
            'slug':       slug,
            'company':    cfg.get('company', slug),
            'email':      cfg.get('email', ''),
            'plan':       cfg.get('plan', 'trial'),
            'status':     status,
            'days_left':  days_left,
            'trial_ends': trial_end,
            'created_at': cfg.get('created_at', ''),
            'mrr':        mrr,
        })

    return sorted(stores, key=lambda x: (x['plan'] != 'paid', x.get('created_at','')), reverse=True)
```

## Overseer Impersonation

```python
@app.route('/overseer/impersonate/<slug>')
@overseer_required
def overseer_impersonate(slug):
    try:
        slug = _sanitize_slug(slug)
    except ValueError:
        flash('Invalid slug.', 'error')
        return redirect(url_for('overseer'))
    session['impersonating_slug'] = slug
    flash(f'Now viewing as: {slug}', 'info')
    return redirect(url_for('dashboard'))

@app.route('/overseer/exit')
def overseer_exit():
    session.pop('impersonating_slug', None)
    flash('Exited client view.', 'info')
    return redirect(url_for('overseer'))
```

## Manual Plan Override

```python
@app.route('/overseer/set-plan', methods=['POST'])
@overseer_required
@csrf_required
def overseer_set_plan():
    slug = request.form.get('slug', '').strip()
    plan = request.form.get('plan', 'trial')
    try:
        slug = _sanitize_slug(slug)
    except ValueError:
        return jsonify({'error': 'Invalid slug'}), 400
    cfg = get_tenant_config(slug)
    cfg['plan'] = plan
    if plan == 'paid':
        cfg['plan_status'] = 'active'
    save_tenant_config(cfg, slug)
    return jsonify({'ok': True, 'slug': slug, 'plan': plan})
```

## Overseer Template (key sections)

```html
<!-- Tenant health table -->
<table class="table">
  <thead>
    <tr>
      <th>Company</th><th>Plan</th><th>Status</th>
      <th>Days Left</th><th>MRR</th><th>Actions</th>
    </tr>
  </thead>
  <tbody>
    {% for t in tenants %}
    <tr>
      <td>{{ t.company }}<br><small>{{ t.slug }}</small></td>
      <td><span class="badge">{{ t.plan }}</span></td>
      <td>
        {% if t.status == 'active' %}🟢 Active
        {% elif t.status == 'paid'  %}💳 Paid
        {% else                     %}🔴 Expired{% endif %}
      </td>
      <td>{{ t.days_left if t.status == 'active' else '—' }}</td>
      <td>${{ t.mrr }}/mo</td>
      <td>
        <a href="/overseer/impersonate/{{ t.slug }}" class="btn btn-sm btn-ghost">View As</a>
        <button onclick="setPlan('{{ t.slug }}','paid')" class="btn btn-sm btn-success">→ Paid</button>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

## Tenant Data Export

```python
@app.route('/overseer/export/<slug>')
@overseer_required
def overseer_export(slug):
    import zipfile, io
    try:
        slug = _sanitize_slug(slug)
    except ValueError:
        abort(400)
    tdir   = os.path.join(CUSTOMERS_DIR, slug)
    buf    = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(tdir):
            for fname in files:
                full    = os.path.join(root, fname)
                arcname = os.path.relpath(full, tdir)
                zf.write(full, arcname)
    buf.seek(0)
    from flask import send_file
    return send_file(buf, mimetype='application/zip',
                     download_name=f'{slug}-export.zip', as_attachment=True)
```
