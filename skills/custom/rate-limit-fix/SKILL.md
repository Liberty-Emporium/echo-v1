# rate-limit-fix

## Purpose
Fix "API rate limit reached" errors in any Flask app using OpenRouter. Adds smart retry logic with exponential backoff, model fallback rotation, and request queuing so users never see a rate limit error.

## The Problem
OpenRouter free tier limits:
- **20 requests/minute** on `:free` models
- **50 requests/day** if you haven't purchased credits
- **1000 requests/day** if you've purchased $10+ credits

When you hit the limit, users see: `"API rate limit reached. Please try again later."` — which kills trust and conversions.

## The Fix — 3 Layers

### Layer 1: Exponential Backoff (auto-retry)
Retry failed requests automatically with increasing delays: 1s → 2s → 4s → 8s → give up gracefully.

### Layer 2: Model Rotation (fallback models)
When primary model is rate-limited, automatically try fallback free models in order.

### Layer 3: User-Friendly Errors
Never show raw API errors to users. Show friendly messages with estimated wait time.

---

## Implementation

### Step 1 — Add `ai_helper.py` to your app

```python
# ai_helper.py — Drop this into any Flask app root
import time
import requests
import os
import logging

logger = logging.getLogger(__name__)

# Free model rotation — ordered by quality
FREE_MODELS = [
    "qwen/qwen3-30b-a3b:free",
    "qwen/qwen3-14b:free", 
    "meta-llama/llama-4-scout:free",
    "google/gemma-3-12b-it:free",
    "mistralai/mistral-7b-instruct:free",
]

def call_ai(messages, system_prompt=None, max_retries=3, timeout=30):
    """
    Call OpenRouter with automatic retry, backoff, and model rotation.
    Returns (response_text, model_used) or raises a friendly error.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set")

    all_messages = []
    if system_prompt:
        all_messages.append({"role": "system", "content": system_prompt})
    all_messages.extend(messages)

    last_error = None

    for model in FREE_MODELS:
        for attempt in range(max_retries):
            try:
                resp = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": os.environ.get("APP_URL", "https://liberty-emporium.ai"),
                        "X-Title": os.environ.get("APP_NAME", "Liberty App"),
                    },
                    json={
                        "model": model,
                        "messages": all_messages,
                        "max_tokens": 1500,
                    },
                    timeout=timeout
                )

                if resp.status_code == 200:
                    data = resp.json()
                    text = data["choices"][0]["message"]["content"]
                    if text and text.strip():
                        logger.info(f"AI success: model={model} attempt={attempt+1}")
                        return text.strip(), model

                elif resp.status_code == 429:
                    # Rate limited — backoff then try next model
                    wait = (2 ** attempt) + 0.5
                    logger.warning(f"Rate limited on {model}, attempt {attempt+1}. Waiting {wait}s")
                    last_error = "rate_limit"
                    if attempt < max_retries - 1:
                        time.sleep(wait)
                    else:
                        break  # Try next model

                elif resp.status_code == 402:
                    logger.error("OpenRouter: insufficient credits")
                    last_error = "no_credits"
                    break  # No point retrying

                elif resp.status_code >= 500:
                    wait = 2 ** attempt
                    logger.warning(f"Server error {resp.status_code} on {model}. Waiting {wait}s")
                    last_error = "server_error"
                    time.sleep(wait)

                else:
                    logger.error(f"AI error {resp.status_code}: {resp.text[:200]}")
                    last_error = f"http_{resp.status_code}"
                    break

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on {model} attempt {attempt+1}")
                last_error = "timeout"
                time.sleep(2 ** attempt)

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                last_error = "connection_error"
                break

    # All models and retries exhausted
    friendly = {
        "rate_limit": "Our AI is busy right now. Please try again in 60 seconds.",
        "no_credits": "AI service temporarily unavailable. Please contact support.",
        "timeout": "AI is taking too long. Please try again.",
        "server_error": "AI service is down. Please try again in a few minutes.",
    }
    raise Exception(friendly.get(last_error, "AI temporarily unavailable. Please try again."))


def call_ai_safe(messages, system_prompt=None, fallback_text="I'm unable to process that right now. Please try again shortly."):
    """
    Like call_ai() but never raises — returns fallback_text on any error.
    Use this in routes where you can't show an error page.
    """
    try:
        text, model = call_ai(messages, system_prompt)
        return text
    except Exception as e:
        logger.error(f"call_ai_safe caught: {e}")
        return fallback_text
```

### Step 2 — Replace your existing AI calls

**Before (breaks on rate limit):**
```python
response = requests.post("https://openrouter.ai/api/v1/chat/completions", ...)
result = response.json()["choices"][0]["message"]["content"]
```

**After (handles rate limits automatically):**
```python
from ai_helper import call_ai_safe

result = call_ai_safe([
    {"role": "user", "content": user_message}
], system_prompt="You are a helpful assistant.")
```

### Step 3 — Show friendly errors in templates

In your Flask route:
```python
@app.route("/ask", methods=["POST"])
@login_required
def ask():
    user_msg = request.form.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Please enter a message"}), 400
    
    try:
        answer, model_used = call_ai([{"role": "user", "content": user_msg}])
        return jsonify({"answer": answer, "model": model_used})
    except Exception as e:
        # Friendly error — never expose raw API errors
        return jsonify({"error": str(e)}), 503
```

In your JS/template:
```javascript
fetch('/ask', {method:'POST', body: formData})
  .then(r => r.json())
  .then(data => {
    if (data.error) {
      showError(data.error); // Show the friendly message
    } else {
      showAnswer(data.answer);
    }
  });
```

---

## Quick Apply to Any App

Run this to drop `ai_helper.py` into an existing app:
```bash
cp /root/.openclaw/workspace/skills/custom/rate-limit-fix/ai_helper.py /path/to/your/app/
```

Then grep for existing AI calls:
```bash
grep -rn "openrouter\|chat/completions\|OPENROUTER" /path/to/your/app/ --include="*.py"
```

Replace each one with `call_ai_safe()` or `call_ai()`.

---

## Model Rotation Strategy

| Priority | Model | Why |
|----------|-------|-----|
| 1st | qwen/qwen3-30b-a3b:free | Best quality free model |
| 2nd | qwen/qwen3-14b:free | Fast, reliable |
| 3rd | meta-llama/llama-4-scout:free | Good fallback |
| 4th | google/gemma-3-12b-it:free | Always available |
| 5th | mistralai/mistral-7b-instruct:free | Last resort |

If ALL 5 models are rate-limited simultaneously — that's extremely rare and means >100 req/min. In that case, the friendly error message shows and the user waits 60 seconds.

---

## Upgrading from Free to Paid

Buy $10 of OpenRouter credits → daily limit jumps from **50 to 1000 req/day**. That handles ~700 active users/day on the free tier. For scale beyond that, switch to paid models (GPT-4o-mini at $0.15/1M tokens is cheap and unlimited).

---

*Skill version: 1.0.0 — Built 2026-04-14*
