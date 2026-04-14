"""
ai_helper.py — Drop-in AI helper for Liberty Emporium Flask apps
Handles OpenRouter rate limits with retry, backoff, and model rotation.
Drop this file into any app root and import call_ai() or call_ai_safe().
"""

import time
import requests
import os
import logging

logger = logging.getLogger(__name__)

# Free model rotation — ordered by quality, tries each on rate limit
FREE_MODELS = [
    "qwen/qwen3-30b-a3b:free",
    "qwen/qwen3-14b:free",
    "meta-llama/llama-4-scout:free",
    "google/gemma-3-12b-it:free",
    "mistralai/mistral-7b-instruct:free",
]

FRIENDLY_ERRORS = {
    "rate_limit": "Our AI is busy right now. Please try again in 60 seconds.",
    "no_credits": "AI service temporarily unavailable. Please contact support.",
    "timeout": "AI is taking too long. Please try again.",
    "server_error": "AI service is down. Please try again in a few minutes.",
    "connection_error": "Cannot reach AI service. Please check your connection.",
}


def call_ai(messages, system_prompt=None, max_retries=3, timeout=30, models=None):
    """
    Call OpenRouter with automatic retry, exponential backoff, and model rotation.
    
    Args:
        messages: list of {"role": "user"/"assistant", "content": "..."}
        system_prompt: optional system message string
        max_retries: retries per model before rotating (default 3)
        timeout: request timeout in seconds (default 30)
        models: list of model IDs to try (default FREE_MODELS)
    
    Returns:
        (response_text: str, model_used: str)
    
    Raises:
        Exception with a user-friendly message string
    """
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set in environment")

    model_list = models or FREE_MODELS

    all_messages = []
    if system_prompt:
        all_messages.append({"role": "system", "content": system_prompt})
    all_messages.extend(messages)

    last_error = "unknown"

    for model in model_list:
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
                    timeout=timeout,
                )

                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        text = choices[0].get("message", {}).get("content", "")
                        if text and text.strip():
                            logger.info(f"AI success model={model} attempt={attempt + 1}")
                            return text.strip(), model
                    # Empty response — retry
                    logger.warning(f"Empty response from {model}, attempt {attempt + 1}")
                    last_error = "empty_response"
                    time.sleep(1)

                elif resp.status_code == 429:
                    wait = (2 ** attempt) + 0.5
                    logger.warning(f"Rate limited on {model} attempt {attempt + 1}, waiting {wait:.1f}s")
                    last_error = "rate_limit"
                    if attempt < max_retries - 1:
                        time.sleep(wait)
                    # else: fall through to next model

                elif resp.status_code == 402:
                    logger.error("OpenRouter: insufficient credits (402)")
                    last_error = "no_credits"
                    break  # No point retrying any model

                elif resp.status_code >= 500:
                    wait = 2 ** attempt
                    logger.warning(f"Server error {resp.status_code} on {model}, waiting {wait}s")
                    last_error = "server_error"
                    time.sleep(wait)

                else:
                    logger.error(f"Unexpected status {resp.status_code} from {model}: {resp.text[:200]}")
                    last_error = f"http_{resp.status_code}"
                    break  # Don't retry 4xx client errors

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on {model} attempt {attempt + 1}")
                last_error = "timeout"
                time.sleep(2 ** attempt)

            except requests.exceptions.ConnectionError:
                logger.error(f"Connection error on {model}")
                last_error = "connection_error"
                break

            except requests.exceptions.RequestException as e:
                logger.error(f"Request exception on {model}: {e}")
                last_error = "connection_error"
                break

    # All models and retries exhausted
    friendly_msg = FRIENDLY_ERRORS.get(last_error, "AI temporarily unavailable. Please try again.")
    raise Exception(friendly_msg)


def call_ai_safe(messages, system_prompt=None,
                 fallback_text="I'm unable to process that right now. Please try again shortly.",
                 models=None):
    """
    Like call_ai() but never raises — returns fallback_text on any error.
    Use in routes where you cannot show an error page (background tasks, webhooks, etc).
    
    Returns: response_text string (never raises)
    """
    try:
        text, _ = call_ai(messages, system_prompt=system_prompt, models=models)
        return text
    except Exception as e:
        logger.error(f"call_ai_safe: {e}")
        return fallback_text


def check_ai_health():
    """
    Quick health check — returns True if AI is reachable, False if rate-limited or down.
    Use in /health endpoints.
    """
    try:
        _, _ = call_ai(
            [{"role": "user", "content": "Reply with just the word OK."}],
            max_retries=1,
            timeout=10,
        )
        return True
    except Exception:
        return False
