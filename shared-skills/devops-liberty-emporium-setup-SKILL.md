---
name: liberty-emporium-setup
description: Complete infrastructure setup for Liberty Emporium - APIs, repos, and access keys
trigger: Setup or bootstrap for Liberty Emporium
---

# Liberty Emporium Infrastructure

## Repositories
- **Main (primary):** https://github.com/Liberty-Emporium/echo-v1
- **Backup:** https://gitlab.com/Liberty-Emporium/echo-v1
- **SmokeStack SaaS:** https://github.com/Liberty-Emporium/vape-shop-saas (formerly vape-shop-saas, deployed on Railway)

## API Keys (check secrets manager first — ROTATED PER SESSION)
⚠️ These are SNAPSHOT values from prior sessions. Verify with `curl` before using.
See `references/bootstrap-2026-05-17.md` for a non-KiloClaw bootstrap session log.
See `references/multi-repo-canonical-paths.md` for repo clone locations and divergence detection.
- **EcDash:** u8aKEAXz-ulQyaGLa11ALMR0LYUv98a6pZuiP4ErXXY
- **Railway:** 00830a2f-e287-427c-bc10-910dfe2485e8
- **GitHub:** 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 (will be replaced after use)
- **GitLab (backup):** glpat-REaaQKR714sP1xZJ05-snWM6MQpvOjEKdTptODRtNg8

## Other Keys
- **Cal.com API:** cal_live_ee5d46c871de452619a7388c674a3c7f
- **Tailscale Auth Key:** tskey-auth-kwJBbBAg4P11CNTRL-sGbec1YDUdhpavFYxfqNehVJ1UypVREWX

## Bootstrap

### Standard (KiloClaw, as root)
Run after every reboot/redeploy:
```bash
bash /root/.openclaw/workspace/echo-v1/scripts/bootstrap.sh
```

### Non-KiloClaw / Non-Root (dev machine, Hermes session)
When running as `mingo` or another non-root user:
- Secrets live in `~/.secrets/` (not `/root/.secrets/`)
- The echo-v1 brain may already exist at `/tmp/echo-v1` — use it or clone fresh
- Clone to `~/echo-v1-brain/` as a writable workspace
- Tailscale step will fail — skip it
- Dashboard notes/brain sync need `ecdash_token` which may not be available
- Core steps that still work: pip tools, git config, secrets dir, clone + GitLab remote setup, EcDash health check

### Token Verification (before attempting pushes)
```bash
# GitHub
curl -s -o /dev/null -w "HTTP %{http_code}" -H "Authorization: token <PAT>" https://api.github.com/user

# GitLab
curl -s -o /dev/null -w "HTTP %{http_code}" -H "PRIVATE-TOKEN: <PAT>" https://gitlab.com/api/v4/user
```
Always verify tokens before using them — Jay's tokens expire or get rotated after use.

## Tailscale SSH Access

When accessing user machines via Tailscale (e.g., checking Hermes Workspace status):

1. **Ping first** to confirm reachability:
   ```bash
   ping -c 3 <tailnet-ip>
   ```

2. **SSH via Tailscale** — use the MagicDNS name (e.g., `jay-upstairs`) not the IP:
   ```bash
   tailscale ssh <hostname>
   ```
   If the user is authorized in Tailscale ACLs, this handles auth automatically.

3. **Fallback: regular SSH with key auth** — if `tailscale ssh` fails, use standard SSH with this server's pubkey already authorized on the remote:
   - This server's ED25519 pubkey: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBZa5gN/jrzeqn1SbhUBMGCikkujt6DI3LG2EsN10CJu gymforge-deploy`
   - Remote machine needs this added to `~/.ssh/authorized_keys`
   ```bash
   ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null <tailnet-ip>
   ```

### Pitfalls
- **ssh-askpass not found / Permission denied**: SSH key auth not set up on remote. Have the user run: `mkdir -p ~/.ssh && echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBZa5gN/jrzeqn1SbhUBMGCikkujt6DI3LG2EsN10CJu gymforge-deploy" >> ~/.ssh/authorized_keys`
- **Host key verification failed**: Use `-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null` or add the host to known_hosts first
- **ED25519 host key unknown**: Tailscale SSH validates host keys against the coordination server — ensure both sides are on the same Tailnet

## Expanding Echo's Skill Library

After bootstrap, expand skills from the hub (target: 100+). Useful Liberty Emporium categories:
- **Security:** 1password, adversarial-ux-test, domain-intel, scrapling, oss-forensics, sherlock
- **Infra:** docker-management
- **AI/ML:** chroma, fastmcp, instructor, guidance, huggingface-tokenizers, peft-fine-tuning, nemo-curator
- **Marketing:** meme-generation, concept-diagrams
- **Tools:** duckduckgo-search, gitnexus-explorer, honcho, qmd, telephony, page-agent, one-three-one-rule

### Pitfalls
- **`-y` flag required** for non-interactive installs: `hermes skills install <name> -y`
- **GitHub rate limit** (60/hr unauthenticated) blocks installs. Set `GITHUB_TOKEN` in `~/.hermes/.env` or use `gh auth login` to raise to 5,000/hr. A fresh PAT from Jay unblocks this.
- **Finance skills** (3-statement-model, comps-analysis, dcf-model, excel-author) are rate-limit sensitive — install early before other hub fetches consume the quota.

## Multi-Repo Canonical Paths

When working on projects with multiple clones (FloodClaims, etc.), always verify which local path is canonical before making changes. See `references/multi-repo-canonical-paths.md` for the divergence detection protocol, known repo locations, and Liberty Oil migration notes.

## Important Notes
- Only spawn sub-agents from GitHub repo for image analysis
- GitLab is backup only
- Regular backups to BOTH GitHub and GitLab

### GitLab Push Pitfalls
- **Merge conflict on first push**: The GitLab remote may have newer commits from KiloClaw. Pull first: `git pull gitlab main --no-rebase`. For status JSON files (`sweet-spot-status.json`, etc.), resolve with `git checkout --theirs <file>` — GitLab is the backup and has the latest from KiloClaw.
- **Token expired**: GitHub tokens expire or get rotated after each session. Verify before attempting push (see Token Verification above). If GitHub is down, push to GitLab only — that's what it's for.

### Repo Naming: liberty-agent vs liberty-agent-puppy
- **`liberty-agent`** = Background service for Alexander AI customers (cloud-deployed, NOT USB)
- **`liberty-agent-puppy`** = USB Repair Agent for Puppy Linux (bootable, offline-capable)
- These are **completely different projects**. Don't mix them up.
- `liberty-agent-puppy` branch is `master` (not `main`)

### GitHub SSH Push Pattern
When HTTPS tokens are expired/blocked, use SSH:
```bash
# Check if SSH works
git ls-remote git@github.com:Liberty-Emporium/<repo>.git

# Switch remote to SSH
git remote set-url origin git@github.com:Liberty-Emporium/<repo>.git

# Push
git push origin main  # or master
```
SSH key is pre-deployed on this machine. Works for all Liberty Emporium repos.

### GitHub Push Protection — History Rewrite
When old tokens leaked into commit history (e.g., in `memory/*.md` files that captured session credentials), GitHub push protection blocks ALL pushes — even ones that don't touch the offending file. The commit is already on the remote and push protection scans the full ancestor chain.

**Symptoms:**
```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Push cannot contain secrets
remote:   —— GitHub Personal Access Token ——————————————————————
remote:     locations:
remote:       - commit: <SHA>
remote:         path: memory/2026-05-13.md:11
```

**Resolution — rewrite history to redact the token:**

1. Identify the offending commit + token:
   ```bash
   git show <SHA>:<path> | grep -n "ghp_"
   ```

2. Rewrite from the offending commit's parent forward:
   ```bash
   git filter-branch -f --tree-filter \
     'if [ -f <path> ]; then sed -i "s/<OLD_TOKEN>/REDACTED/" <path>; fi' \
     <SHA>^..HEAD
   ```
   Key: `SHA^` (parent) is critical — running from `SHA..HEAD` excludes the offending commit itself.

3. Verify the token is gone:
   ```bash
   git grep "<OLD_TOKEN>"  # should return nothing
   ```

4. Restore any files the filter-branch accidentally nuked (from a prior failed attempt):
   ```bash
   git checkout gitlab/main -- <path>
   sed -i 's/<OLD_TOKEN>/REDACTED/' <path>
   git add <path> && git commit -m "fix: redact old token from <file>"
   ```

5. Force push:
   ```bash
   git push --force origin main
   ```

**Pitfalls:**
- Use `--tree-filter` (not `--index-filter`) when the token is inside file content
- Range MUST include the offending commit (`SHA^..HEAD`, not `SHA..HEAD`)
- After a failed filter-branch, `git checkout gitlab/main -- <file>` to recover lost files — GitLab has the authoritative backup
- `--force` push rewrites remote history; coordinate if multiple writers
- **Prevention**: NEVER save raw tokens in memory files. Use `REDACTED` or reference "stored in /root/.secrets/"
