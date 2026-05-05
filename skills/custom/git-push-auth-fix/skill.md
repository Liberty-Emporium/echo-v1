# Skill: git-push-auth-fix

## Purpose
Diagnose and fix Git push failures (403, 401, credential prompts).

## Trigger Phrases
- "Git push failed", "Permission denied to GitHub"
- "Password authentication not supported"
- "Can't push to GitHub", "Token authentication failed"
- "Git keeps asking for password", "Credential helper broke"

## When to Use
- `git push` returns `403 Forbidden` or `401 Unauthorized`
- Git keeps prompting for username/password
- Token works via API but not via `git push`
- GitHub secret scanning detected exposed token
- Need to update remote URL with new token

## Steps

### Step 1: Test Token Validity
```bash
# Test GitHub API with the token
curl -s -H "Authorization: token $TOKEN" "https://api.github.com/user" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('login'), d.get('message', 'OK'))"

# Test GitLab
curl -s --header "PRIVATE-TOKEN: $TOKEN" "https://gitlab.com/api/v4/user" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('username', d.get('message')))"
```

### Step 2: Check Current Remote URL
```bash
git remote -v
# Check if token is embedded (bad — gets scanned by GitHub secret scanning)
# git remote set-url origin "https://ghp_TOKEN@github.com/owner/repo.git"
```

### Step 3: Check Credential Helper
```bash
git config --global credential.helper
git config --global --list | grep cred
cat ~/.git-credentials
cat ~/.netrc
```

### Step 4: Fix Credential Storage
```bash
# Store credentials in netrc (alternative to git-credentials)
echo "machine github.com login ghp_TOKEN password TOKEN" > ~/.netrc
chmod 600 ~/.netrc

# OR use git store helper
git config --global credential.helper store
echo "https://TOKEN@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials
```

### Step 5: Remove Token from Remote URL
```bash
# Use SSH URL instead (if SSH key is added to GitHub)
git remote set-url origin "git@github.com:owner/repo.git"

# OR use HTTPS without embedding token in URL
git remote set-url origin "https://github.com/owner/repo.git"

# Then configure credentials separately (not in URL)
git config --global credential.helper store
```

### Step 6: If GitHub Says "Password Authentication Not Supported"
This means the token is either:
1. Invalid/expired → Get a new token
2. Insufficient permissions → Token needs `repo` scope for private repos
3. Wrong token format → Use `ghp_` prefix for GitHub PATs

Get a new token:
1. Go to https://github.com/settings/tokens
2. Generate new token (classic) with `repo` scope
3. Update credentials:
```bash
git remote set-url origin "https://ghp_NEWTOKEN@github.com/owner/repo.git"
echo "https://NEWTOKEN@github.com" > ~/.git-credentials
```

### Step 7: If Token Was Exposed (Secret Scanning)
1. **Revoke the exposed token immediately** at https://github.com/settings/tokens
2. Clean from git history:
```bash
# Remove leaked file from all commits
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch PATH/TO/FILE' -- --all

# Force push clean history
git push origin main --force
```

3. Get a fresh token and update:
```bash
git remote set-url origin "https://ghp_NEWTOKEN@github.com/owner/repo.git"
echo "https://NEWTOKEN@github.com" > ~/.git-credentials
git push origin main --force
```

### Step 8: For GitLab (Similar Process)
```bash
# Test token
curl -s --header "PRIVATE-TOKEN: $TOKEN" "https://gitlab.com/api/v4/user"

# Add GitLab remote
git remote add gitlab "https://gitlab.com/owner/repo.git"

# Store credentials
echo "machine gitlab.com login glpat-TOKEN password TOKEN" > ~/.netrc
chmod 600 ~/.netrc
```

## Quick Reference: Token Formats
| Provider | Format | Where to Get |
|----------|--------|-------------|
| GitHub | `ghp_xxxxxxxxxxxxxxxxxxxx` | github.com/settings/tokens |
| GitHub (fine-grained) | `github_pat_xxxxxxxx` | github.com/settings/tokens |
| GitLab | `glpat-xxxxxxxxxxxxxxxxxxxx` | gitlab.com/-/profile/personal_access_tokens |

## Quick Fix (Most Common Case)
```bash
# 1. Get fresh token
# 2. Update remote URL
git remote set-url origin "https://ghp_NEWTOKEN@github.com/owner/repo.git"

# 3. Store it
echo "https://NEWTOKEN@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials
git config --global credential.helper store

# 4. Push
git push origin main
```

## Related Skills
- `branding-rebrand-app` — push rebranded code to GitHub
- `github-actions-desktop-build` — trigger builds via GitHub Actions when local push is fixed