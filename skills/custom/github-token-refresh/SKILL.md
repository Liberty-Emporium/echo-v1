# github-token-refresh

Detect when the GitHub token is expired or about to expire and alert Jay.

## When to use
- Any time a GitHub API call returns 401
- At session start as a quick check
- When Jay shares a new token in chat

## Check if token is valid
```bash
GH_TOKEN=$(cat /root/.secrets/github_token)
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token $GH_TOKEN" \
  https://api.github.com/user)
echo "Token status: $STATUS"
```
- 200 = valid
- 401 = expired or invalid
- 403 = rate limited

## When token expires
1. Tell Jay: "Hey Jay, the GitHub token has expired. Can you generate a new one?"
2. Jay goes to: github.com → Settings → Developer Settings → Personal Access Tokens → Fine-grained
3. Required scopes: repo (read/write), workflow, admin:org (for org repos)
4. Jay shares new token
5. Update: `echo -n "NEW_TOKEN" > /root/.secrets/github_token`
6. Update remote URLs in all cloned repos:
   ```bash
   cd /root/.openclaw/workspace/echo-v1
   git remote set-url origin "https://x-access-token:NEW_TOKEN@github.com/Liberty-Emporium/echo-v1.git"
   ```
7. Update credentials.md

## Token storage locations
- `/root/.secrets/github_token` — main token file
- `memory/credentials.md` — documentation (not the raw token)
- Git remote URLs in each cloned repo

## Note from REFLECTIONS.md
When credentials are shared in chat, remind Jay to rotate them — they're now in chat history.
