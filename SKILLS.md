# Skills
## Echo-v1 Operator Skill Set

**Last Updated:** 2026-05-21
**Version:** 3.0 (OpenClaw Native Skills Integration)

---

## Core Skills (Built-in)

### 1. deploy-watcher
Monitors Railway deployments, detects failures, triggers alerts.
- Trigger: "watch deploy", "monitor", "deployment status"
- Type: Monitoring
- Source: echo-v1/core

### 2. logging
Centralized logging for all Liberty-Emporium operations.
- Trigger: "log this", "check logs", "logging"
- Type: Context Management
- Source: echo-v1/core

### 3. agent-sync
Keeps all agents synchronized with the latest context.
- Trigger: "sync agents", "agent update", "sync status"
- Type: Coordination
- Source: echo-v1/core

### 4. ecdash-client
Interacts with EcDash control plane API.
- Trigger: "call EcDash", "control plane", "ecdash"
- Type: Integration
- Source: echo-v1/core

---

## OpenClaw Native Skills

### 5. acp-router ⭐ NEW
Route plain-language requests for Pi, Claude Code, Cursor, Copilot, OpenClaw ACP, OpenCode, Gemini CLI, Qwen, Kiro, Kimi, iFlow, Factory Droid, Kilocode, or explicit ACP harness work.
- Trigger: "run in Claude Code", "use Cursor", "Gemini CLI", "openclaw ACP"
- Type: ACP Harness Routing
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/dist/extensions/acpx/skills/acp-router/SKILL.md
- Notes: For coding-agent thread requests, use only `sessions_spawn` for thread creation

### 6. blogwatcher ⭐ NEW
Monitor blogs and RSS/Atom feeds for updates.
- Trigger: "check blogs", "RSS feed updates", "blog watcher"
- Type: Feed Monitoring
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/blogwatcher/SKILL.md
- Install: `go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest`

### 7. browser-automation ⭐ NEW
Control web pages with OpenClaw browser tool, especially multi-step flows, login checks, tab management.
- Trigger: "automate browser", "login check", "multi-step web flow"
- Type: Web Automation
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/dist/extensions/browser/skills/browser-automation/SKILL.md
- Notes: Use for anything beyond single page checks

### 8. clawhub ⭐ NEW
Search, install, update, sync, or publish agent skills.
- Trigger: "install skill", "clawhub", "search skills"
- Type: Skill Management
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/clawhub/SKILL.md
- Install: `npm i -g clawhub`

### 9. gh-issues ⭐ NEW
Fetch GitHub issues, delegate fixes to subagents, open PRs, watch reviews.
- Trigger: "fix GitHub issues", "auto-fix issues", "PR review handler"
- Type: GitHub Automation
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/gh-issues/SKILL.md
- Notes: Uses curl + GitHub REST API (no gh CLI dependency)

### 10. gifgrep ⭐ NEW
Search GIF providers (Tenor/Giphy) with CLI/TUI, download results, extract stills/sheets.
- Trigger: "search GIFs", "find GIF", "GIF download"
- Type: GIF Search & Download
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/gifgrep/SKILL.md
- Install: `brew install steipete/tap/gifgrep` or `go install github.com/steipete/gifgrep/cmd/gifgrep@latest`

### 11. github ⭐ NEW
Use gh CLI for GitHub issues, PR status, CI/logs, comments, reviews, releases.
- Trigger: "check PR status", "GitHub issues", "view CI logs"
- Type: GitHub CLI
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/github/SKILL.md
- Install: `brew install gh`
- Notes: Only specify `--repo owner/repo` when not in git directory

### 12. gog ⭐ NEW
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.
- Trigger: "Gmail", "Google Calendar", "Google Drive", "send email"
- Type: Google Workspace
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/gog/SKILL.md
- Install: `brew install steipete/tap/gogcli`
- Notes: Requires OAuth setup

### 13. healthcheck ⭐ NEW
Audit and harden hosts running OpenClaw for SSH, firewall, updates, exposure, cron checks.
- Trigger: "security audit", "harden host", "check security"
- Type: Security Auditing
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/healthcheck/SKILL.md
- Notes: Recommend running with state-of-the-art model

### 14. himalaya ⭐ NEW
Use himalaya to list, read, search, compose, reply, forward, and organize IMAP/SMTP email.
- Trigger: "email", "IMAP", "SMTP", "compose email"
- Type: Email CLI
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/himalaya/SKILL.md
- Install: `brew install himalaya`
- Notes: Configuration file at `~/.config/himalaya/config.toml`

### 15. mcporter ⭐ NEW
List, configure, authenticate, call, and inspect MCP servers/tools over HTTP or stdio.
- Trigger: "MCP server", "mcporter", "call MCP tool"
- Type: MCP Server Management
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/mcporter/SKILL.md
- Install: `npm i -g mcporter`

### 16. node-connect ⭐ NEW
Diagnose OpenClaw Android, iOS, or macOS node pairing, QR/setup code, route, auth, and connection failures.
- Trigger: "can't connect node", "node pairing failed", "QR code issue"
- Type: Node Pairing Diagnostics
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/node-connect/SKILL.md
- Notes: Always run `openclaw qr --json` for canonical checks

### 17. obsidian ⭐ NEW
Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.
- Trigger: "Obsidian notes", "vault", "create note"
- Type: Note Management
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/obsidian/SKILL.md
- Install: `brew install yakitrak/yakitrak/obsidian-cli`
- Notes: Vault config at `~/Library/Application Support/obsidian/obsidian.json`

### 18. openai-whisper ⭐ NEW
Local speech-to-text with the Whisper CLI (no API key).
- Trigger: "transcribe audio", "speech to text", "whisper"
- Type: Audio Transcription
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/openai-whisper/SKILL.md
- Install: `brew install openai-whisper`
- Notes: Models download to `~/.cache/whisper`

### 19. session-logs ⭐ NEW
Search and analyze your own session logs (older/parent conversations) using jq.
- Trigger: "what was said before", "older conversation", "search history"
- Type: Session Log Analysis
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/session-logs/SKILL.md
- Requires: jq, ripgrep
- Notes: Location: `$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/`

### 20. skill-creator ⭐ NEW
Create, edit, improve, tidy, review, audit, or restructure AgentSkills and SKILL.md files.
- Trigger: "create skill", "edit SKILL.md", "skill creator"
- Type: Skill Development
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/skill-creator/SKILL.md
- Notes: Use `init_skill.py` to generate templates

### 21. slack ⭐ NEW
Use Slack tool to react, pin/unpin, send, edit, delete messages, or fetch Slack member info.
- Trigger: "Slack message", "react to Slack", "Slack pin"
- Type: Slack Integration
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/slack/SKILL.md
- Notes: Uses bot token configured for OpenClaw

### 22. summarize ⭐ NEW
Summarize or transcribe URLs, YouTube/videos, podcasts, articles, transcripts, PDFs, and local files.
- Trigger: "summarize this", "what's this link about", "transcribe YouTube"
- Type: Content Summarization
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/summarize/SKILL.md
- Install: `brew install steipete/tap/summarize`
- Notes: Default model: `google/gemini-3-flash-preview`

### 23. taskflow ⭐ NEW
Coordinate multi-step detached tasks as one durable TaskFlow job with owner context, state, waits, and child tasks.
- Trigger: "taskflow", "detached task", "background job"
- Type: Task Orchestration
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/taskflow/SKILL.md
- Notes: Use for jobs that outlive one prompt or detached run

### 24. taskflow-inbox-triage ⭐ NEW
Example TaskFlow pattern for inbox triage, intent routing, waiting on replies, and later summaries.
- Trigger: "inbox triage", "route messages", "TaskFlow example"
- Type: TaskFlow Pattern Example
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/taskflow-inbox-triage/SKILL.md

### 25. tmux ⭐ NEW
Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.
- Trigger: "tmux session", "send keys to tmux", "scrape tmux output"
- Type: Terminal Multiplexer Control
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/tmux/SKILL.md
- Install: `brew install tmux`
- Notes: Essential for managing Claude Code sessions

### 26. video-frames ⭐ NEW
Extract frames or short clips from videos using ffmpeg.
- Trigger: "extract frame", "video thumbnail", "frame from video"
- Type: Video Processing
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/video-frames/SKILL.md
- Install: `brew install ffmpeg`
- Notes: Use `--time` for "what is happening around here?"

### 27. weather ⭐ NEW
Get current weather, rain, temperature, and forecasts for locations or travel planning.
- Trigger: "weather", "forecast", "temperature", "will it rain"
- Type: Weather Information
- Source: /opt/openclaw/npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md
- Notes: Uses wttr.in (no API key needed)

---

## Custom Skills (Echo-v1 Specific)

### 28. deploy-rescue ⭐ ECHO
Diagnoses and fixes Railway deployment failures.
- Trigger: "Railway is down", "App crashed on deploy", "Fix deployment", "Deploy rescue"
- Type: Diagnostic & Recovery
- Location: `skills/custom/deploy-rescue/skill.md`

### 29. security-audit ⭐ ECHO
Scans for security vulnerabilities in Flask apps.
- Trigger: "Check security", "Security sweep", "Is this safe?", "Audit this code"
- Type: Security
- Location: `skills/custom/security-audit/skill.md`

### 30. db-migrate ⭐ ECHO
Safe SQLite schema migrations for production.
- Trigger: "Add column to table", "Database migration needed", "Fix missing column", "Schema change"
- Type: Database
- Location: `skills/custom/db-migrate/skill.md`

### 31. rollback-ready ⭐ ECHO
Fast emergency rollback procedures.
- Trigger: "Undo last push", "Rollback to working version", "Site is broken", "Revert now", "Emergency rollback"
- Type: Recovery
- Location: `skills/custom/rollback-ready/skill.md`

### 32. template-debug ⭐ ECHO
Fixes Jinja2/HTML/CSS template issues.
- Trigger: "Page looks wrong", "CSS broken", "Nav bar error", "Template issue", "Jinja2 error"
- Type: Debugging
- Location: `skills/custom/template-debug/skill.md`

### 33. branding-rebrand-app ⭐ ECHO
Fork open-source app and apply full custom branding.
- Trigger: "Rebrand this app", "Put my logo on the app", "Apply branding"
- Type: Branding
- Location: `skills/custom/branding-rebrand-app/skill.md`

### 34. railway-deploy-fix ⭐ ECHO
Diagnose and fix Railway deployment issues (hangs, VOLUME errors, env vars).
- Trigger: "Railway is hanging", "Fix Railway", "Dockerfile VOLUME error"
- Type: Deployment
- Location: `skills/custom/railway-deploy-fix/skill.md`

### 35. github-actions-desktop-build ⭐ ECHO
Build cross-platform desktop installers via GitHub Actions.
- Trigger: "Build for Windows", "Build for Mac", "Get the .exe"
- Type: Build & Release
- Location: `skills/custom/github-actions-desktop-build/skill.md`

### 36. web-pet-widget ⭐ ECHO
Add animated floating mascot companion to web app via WebSocket bridge.
- Trigger: "Add the pet", "Floating mascot", "The little guy is missing"
- Type: Feature
- Location: `skills/custom/web-pet-widget/skill.md`

### 37. git-push-auth-fix ⭐ ECHO
Fix git push authentication failures (403, 401, credential issues).
- Trigger: "Git push failed", "Permission denied", "Can't push"
- Type: DevOps
- Location: `skills/custom/git-push-auth-fix/skill.md`

---

## Tool Suite (Echo-v1 Operator Tools)

The following tools are also available in the workspace `tools/` directory:

### 1. deploy-rescue
**Type:** Diagnostic & Recovery
**Use when:** Railway deployment fails, app crashes on boot, worker won't start
**File:** `tools/deploy-rescue.md`

### 2. security-audit
**Type:** Security
**Use when:** Checking code for vulnerabilities, before deployment, after changes
**File:** `tools/security-audit.md`

### 3. rollback-ready
**Type:** Recovery
**Use when:** Production is broken and you need to revert FAST
**File:** `tools/rollback-ready.md`

### 4. db-migrate
**Type:** Database
**Use when:** Need to add columns/tables, schema changes, "no such column" errors
**File:** `tools/db-migrate.md`

### 5. template-debug
**Type:** Debugging
**Use when:** Page looks wrong, CSS broken, nav bar error, Jinja2 error
**File:** `tools/template-debug.md`

### 6. quick-status
**Type:** Health Check
**Use when:** Starting session, checking if anything is down, routine check
**File:** `tools/quick-status.md`

### 7. backup-verify
**Type:** Disaster Recovery
**Use when:** After significant changes, periodic verification, pre-deployment check
**File:** `tools/backup-verify.md`

### 8. memory-sync
**Type:** Context Management
**Use when:** Starting session, need current project state, resuming work
**File:** `tools/memory-sync.md`

### 9. session-log
**Type:** Memory
**Use when:** End of session, significant changes made, new information learned
**File:** `tools/session-log.md`

---

## Skill Usage Guide

When a user describes a problem:
1. Match trigger phrases to skill
2. Load skill file from appropriate location
3. Follow the step-by-step guide
4. Use related skills for complex issues

Example flow:
- User: "App crashed on deploy, help!"
- Match: `deploy-rescue` skill (Echo-v1 custom)
- Load from: `skills/custom/deploy-rescue/skill.md`
- Follow steps to diagnose → fix → verify

For OpenClaw native skills, check `/opt/openclaw/npm-global/lib/node_modules/openclaw/skills/` or `/opt/openclaw/npm-global/lib/node_modules/openclaw/dist/extensions/` directories.

---

*Skills v3.0 — Enhanced by Echo (KiloClaw) on 2026-05-21*
*Integrated all OpenClaw native skills + Echo-v1 custom skills*