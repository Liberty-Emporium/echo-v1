# HEARTBEAT tasks

## EcDash Bridge Poll
Check for pending tasks from EcDash and execute them:

1. Fetch: GET https://jay-portfolio-production.up.railway.app/api/echo-bridge
   - Auth: Bearer token from /root/.secrets/ecdash_token
2. For each task with status="pending":
   - Read the task description
   - Execute it (write code, push to GitHub, check health, etc.)
   - PATCH /api/echo-bridge/<task_id> with status=done and response summary
   - Use X-Echo-Secret header from /root/.secrets/ecdash_webhook_secret (if set)
3. If no pending tasks → HEARTBEAT_OK
