# Feature Patterns — Copy-Paste Blocks

## AI Chat (OpenRouter)

```python
def call_openrouter(messages, model, api_key, max_tokens=2000):
    import requests
    try:
        r = requests.post('https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {api_key}',
                     'HTTP-Referer': 'https://liberty-emporium.ai'},
            json={'model': model, 'messages': messages, 'max_tokens': max_tokens},
            timeout=30)
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        return f'AI error: {e}'

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    data  = request.get_json(silent=True) or {}
    msg   = data.get('message', '').strip()
    key   = get_setting('openrouter_api_key')
    model = get_setting('ai_model') or 'openai/gpt-4o-mini'
    if not msg or not key:
        return jsonify({'error': 'Missing message or API key'}), 400
    reply = call_openrouter([{'role': 'user', 'content': msg}], model, key)
    return jsonify({'reply': reply})
```

## KYS API Key Fetching

```python
def get_api_key_from_kys(service_name):
    """Fetch an API key from Keep Your Secrets at runtime."""
    kys_token = os.environ.get('KYS_API_TOKEN', '')
    if not kys_token: return None
    try:
        r = requests.get(
            f'https://ai-api-tracker-production.up.railway.app/api/key/{service_name}',
            headers={'Authorization': f'Bearer {kys_token}'},
            timeout=5)
        if r.status_code == 200:
            return r.json().get('key')
    except Exception:
        pass
    return None
```

## Willie AI Widget Integration

```python
# Add to base.html before </body>:
# <script src="https://ai-agent-widget-production.up.railway.app/widget/AGENT_ID.js"></script>

# Willie API auth (for server-side calls)
def willie_auth():
    auth  = request.headers.get('Authorization', '')
    token = auth.replace('Bearer ', '').strip()
    return bool(token and token == get_setting('willie_api_token'))
```

## EcDash Bridge — Post a Task

```python
def post_to_ecdash(task_text, task_type='info'):
    """Send a task/notification to EcDash bridge queue."""
    token = open('/root/.secrets/ecdash_token').read().strip() if os.path.exists('/root/.secrets/ecdash_token') else ''
    if not token: return
    try:
        requests.post(
            'https://jay-portfolio-production.up.railway.app/api/echo-bridge',
            headers={'Authorization': f'Bearer {token}'},
            json={'text': task_text, 'type': task_type},
            timeout=5)
    except Exception:
        pass
```

## Settings Table Pattern

```python
def get_setting(key, default=''):
    row = get_db().execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
    return row['value'] if row else default

def set_setting(key, value):
    db = get_db()
    db.execute('INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value',
               (key, value))
    db.commit()
```

DB table:
```sql
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT DEFAULT ''
);
```

## Stripe Checkout

```python
@app.route('/checkout', methods=['POST'])
@login_required
@csrf_required
def checkout():
    import stripe as _stripe
    _stripe.api_key = get_setting('stripe_secret_key')
    if not _stripe.api_key:
        flash('Stripe not configured — add key in Settings.', 'error')
        return redirect(url_for('settings'))
    session_obj = _stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price_data': {'currency': 'usd',
                                    'product_data': {'name': 'Service'},
                                    'unit_amount': 5000},  # $50.00
                     'quantity': 1}],
        mode='payment',
        success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('dashboard', _external=True),
    )
    return redirect(session_obj.url)
```

## File Upload with Validation

```python
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/upload', methods=['POST'])
@login_required
@csrf_required
def upload():
    f = request.files.get('file')
    if not f or not allowed_file(f.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    from werkzeug.utils import secure_filename
    fname = secure_filename(f.filename)
    path  = os.path.join(UPLOAD_DIR, fname)
    f.save(path)
    return jsonify({'ok': True, 'path': path})
```

## Mobile-First CSS Block (add to every base.html)

```css
html,body{overflow-x:hidden;max-width:100%;}
img{max-width:100%;height:auto;}
@media(max-width:768px){
  table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;}
  input,select,textarea{font-size:16px!important;}
  .form-row,.form-row-3{grid-template-columns:1fr!important;}
}
```

## Procfile

```
web: gunicorn app:app --workers 2 --timeout 120 --bind 0.0.0.0:$PORT
```

## railway.json

```json
{
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30,
    "restartPolicyType": "ON_FAILURE"
  }
}
```
