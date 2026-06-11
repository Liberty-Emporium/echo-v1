---
name: llm-resilient-api
description: Production-grade retry patterns and error handling for LLM API calls — exponential backoff, circuit breaker, multi-provider fallback
version: 1.0.0
platforms: [linux, macos, windows]
---

# LLM Resilient API Patterns

## When to use
- Building AI agents that call LLM APIs in production
- Cron jobs and automated agents using LLM APIs
- Any system that must not crash on rate limits or transient errors

## Key Principle
> "An AI agent that crashes on a 429 rate limit is not production-ready. Build resilience into every API call."

## Error Response Strategies

| HTTP Code | Meaning | Strategy |
|-----------|---------|----------|
| 429 | Rate limit | Exponential backoff + retry |
| 500/502/503 | Server error | Retry with backoff |
| 400 | Bad request | Fix request, don't retry |
| 401/403 | Auth failure | Alert immediately, don't retry |
| 413 | Context too long | Reduce prompt, retry |
| 408 | Timeout | Retry with reduced prompt |

## Pattern 1: Retry with Exponential Backoff + Jitter
- Base delay doubles each attempt (1s, 2s, 4s, 8s...)
- Cap max delay at 60s
- Add 50% jitter to spread retry timing
- Never retry 401/403 (auth errors)

## Pattern 2: Robust LLM Client
- Respect `Retry-After` header on 429
- Track tokens used, latency, provider
- Configurable max retries, timeout, max_tokens

## Pattern 3: Structured Output with Validation
- Request JSON schema with `strict: true`
- Validate response with jsonschema
- On validation failure, append error feedback and retry
- Max 2 validation retries

## Pattern 4: Multi-Provider Fallback
- Configure multiple providers in priority order
- Try next provider on failure
- Example: OpenRouter → OpenAI → Anthropic

## Pattern 5: Circuit Breaker
- After N consecutive failures, stop calling provider
- Cooldown period before retrying
- Prevents cascading failures

## Liberty Emporium Use Case
All cron jobs and automated agents must use these patterns. The intelligence gathering cron hits LLM APIs every 2 hours — if it crashes on a 429, Jay doesn't get his reports.

## Source
Based on OpenAI API error codes documentation and production agent patterns.
Full version with code: `references/llm-resilient-api-full.md`
