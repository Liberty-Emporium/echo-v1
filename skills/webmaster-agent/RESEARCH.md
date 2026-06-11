# 🔧 WEBMASTER AGENT — Complete Research & Skill Library
## An AI Agent's Guide to Being a Webmaster

**Created:** June 10, 2026
**Author:** Mingo (AI Agent Research Division)
**Purpose:** Comprehensive guide for AI agents performing webmaster duties across Tailscale networks
**Shareable:** YES — designed to be shared with other agents via GitHub/GitLab

---

## TABLE OF CONTENTS

1. [What is an Agentic Webmaster?](#1-what-is-an-agentic-webmaster)
2. [Core Webmaster Skills Matrix](#2-core-webmaster-skills-matrix)
3. [Tailscale Integration for Agents](#3-tailscale-integration-for-agents)
4. [Website Monitoring & Health](#4-website-monitoring--health)
5. [SSL/TLS Certificate Management](#5-ssltls-certificate-management)
6. [DNS Management](#6-dns-management)
7. [Security Hardening](#7-security-hardening)
8. [Backup & Disaster Recovery](#8-backup--disaster-recovery)
9. [Performance Optimization](#9-performance-optimization)
10. [Agent-to-Agent Skill Sharing](#10-agent-to-agent-skill-sharing)
11. [New Ideas & Innovations](#11-new-ideas--innovations)
12. [Daily Operations Checklist](#12-daily-operations-checklist)

---

## 1. WHAT IS AN AGENTIC WEBMASTER?

An **Agentic Webmaster** is an AI agent that autonomously manages websites, servers, and network infrastructure on behalf of a human owner. Unlike traditional webmasters who work 9-5, an agentic webmaster:

- **Monitors 24/7** — never sleeps, never misses an alert
- **Self-heals** — detects and fixes issues before the human knows
- **Learns continuously** — improves from every incident
- **Shares knowledge** — documents everything for other agents
- **Operates across networks** — uses Tailscale to manage remote machines

### Key Principle: "Fix First, Report After"
The human owner should never have to tell the agent to fix something. The agent should already be working on it.

### Key Principle: "Research Before Acting"
Before making changes, the agent should research best practices, check documentation, and plan the approach.

---

## 2. CORE WEBMASTER SKILLS MATRIX

| Skill Category | Priority | Frequency | Tools Needed |
|---------------|----------|-----------|-------------|
| Uptime Monitoring | CRITICAL | Continuous | UptimeRobot (free), curl, ping |
| SSL Certificate Management | CRITICAL | Weekly check | Certbot, Let's Encrypt, acme.sh |
| DNS Management | HIGH | As needed | Cloudflare API, Namecheap API |
| Security Scanning | HIGH | Daily | nmap, fail2ban, ClamAV |
| Backup Management | HIGH | Daily | rsync, rclone, restic |
| Performance Monitoring | MEDIUM | Hourly | htop, netdata, Lighthouse |
| Log Analysis | MEDIUM | Daily | journalctl, goaccess |
| Firewall Management | MEDIUM | As needed | ufw, iptables |
| Software Updates | MEDIUM | Weekly | apt, snap, npm |
| Content Updates | LOW | As needed | git, CMS API |

---

## 3. TAILSCALE INTEGRATION FOR AGENTS

### What is Tailscale?
Tailscale creates a **private encrypted mesh network** (called a "Tailnet") between devices. For agents, this means:

- **Secure remote access** to any machine in the tailnet
- **No public SSH exposure** — all traffic is encrypted via WireGuard
- **Identity-based access** — no SSH keys to manage
- **Works across networks** — home, office, cloud, VPS

### Tailscale SSH for Agents

Tailscale SSH replaces traditional SSH key management with identity-based authentication:

```bash
# Enable Tailscale SSH on a host
tailscale set --ssh

# Connect from another machine in the tailnet
ssh user@hostname.tailnet-name.ts.net
```

**Key Benefits for Agents:**
- No SSH key distribution needed
- Access controlled via ACL policies
- Session recording for audit trails
- User revocation in seconds (update ACL)
- Works with automation (ansible, scripts)

### Tailscale ACL Policy Example for Agent Access

```json
{
  "ssh": [
    {
      "action": "accept",
      "src": ["group:agents"],
      "dst": ["tag:servers"],
      "users": ["autogroup:nonroot", "root"]
    }
  ],
  "acls": [
    {
      "action": "accept",
      "src": ["group:agents"],
      "dst": ["tag:servers:*"]
    }
  ]
}
```

### Tailscale Serve Mode (Recommended for Agent Gateways)

```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" }
  }
}
```

This exposes the agent gateway on the Tailnet without public internet exposure.

### Tailscale + Agent Communication Pattern

```
[Agent A on Machine 1] ←──Tailscale──→ [Agent B on Machine 2]
         ↓                                    ↓
    tailscale ssh                      tailscale ssh
         ↓                                    ↓
[Execute remote commands]          [Execute remote commands]
         ↓                                    ↓
[Report back to owner]             [Report back to owner]
```

### Tailscale Best Practices for Agents

1. **Always use Serve mode** for agent gateways (not Funnel)
2. **Use ACLs** to restrict which agents can access which machines
3. **Enable check mode** for sensitive operations (requires re-auth)
4. **Use tags** to group machines by function (web, db, monitoring)
5. **Set `resetOnExit: true`** to clean up Tailscale config when agents stop
6. **Monitor Tailscale status** — `tailscale status` should be in daily checks

---

## 4. WEBSITE MONITORING & HEALTH

### Free Monitoring Tools

| Tool | Free Tier | Monitors | Best For |
|------|-----------|----------|----------|
| **UptimeRobot** | 50 monitors | HTTP, ping, port, keyword, SSL | General uptime |
| **Better Stack** | 10 monitors | HTTP, ping, SSL | Clean UI |
| **Hetrix Tools** | 1 monitor | Uptime, blacklist | Blacklist monitoring |
| **Google Search Console** | Unlimited | SEO, indexing | Search visibility |

### Agent Monitoring Script Pattern

```bash
#!/bin/bash
# Agent Health Check Script
# Run via cron every 5 minutes

URLS=(
  "https://example.com"
  "https://api.example.com/health"
  "https://admin.example.com"
)

for url in "${URLS[@]}"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url")
  if [ "$STATUS" != "200" ]; then
    # Log the failure
    echo "$(date): $url returned $STATUS" >> /var/log/agent-monitor.log
    # Attempt auto-heal
    systemctl restart nginx 2>/dev/null
    # Notify owner
    # (agent sends message via Telegram)
  fi
done
```

### What to Monitor

1. **HTTP Status Codes** — 200 OK, 301/302 redirects, 4xx errors, 5xx errors
2. **Response Time** — Alert if > 3 seconds
3. **SSL Expiry** — Alert if < 30 days remaining
4. **Disk Space** — Alert if > 85% used
5. **Memory Usage** — Alert if > 90% used
6. **CPU Load** — Alert if load average > CPU count
7. **Service Status** — nginx, mysql, postgresql, docker
8. **Certificate Transparency** — Monitor for unauthorized certs

---

## 5. SSL/TLS CERTIFICATE MANAGEMENT

### Let's Encrypt with Certbot (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renewal (built-in cron)
sudo certbot renew --dry-run
```

### Certificate Monitoring

```bash
# Check expiry date
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Check expiry in days
EXPIRY=$(echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s)
NOW_EPOCH=$(date +%s)
DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))
echo "SSL expires in $DAYS_LEFT days"
```

### Best Practices

1. **Auto-renewal** — Certbot sets up a systemd timer automatically
2. **Monitor expiry** — Alert at 30, 14, 7, 3, 1 days before expiry
3. **Use DNS challenge** — For internal services not accessible via HTTP
4. **Wildcard certs** — `*.example.com` for subdomains
5. **HSTS header** — Always include `Strict-Transport-Security`
6. **OCSP Stapling** — Enable for faster SSL handshakes

---

## 6. DNS MANAGEMENT

### Free DNS Providers

| Provider | Free Tier | API | Notes |
|----------|-----------|-----|-------|
| **Cloudflare** | Unlimited | Yes | Best overall, CDN included |
| **Namecheap** | Limited | Yes | Budget option |
| **DuckDNS** | Unlimited | Yes | Simple, no frills |
| **No-IP** | 3 hosts | Yes | Dynamic DNS |

### Cloudflare API for Agents

```bash
# Update DNS record via API
curl -X PUT "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records/RECORD_ID" \
  -H "Authorization: Bearer CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"A","name":"example.com","content":"NEW_IP","ttl":120}'
```

### DNS Best Practices

1. **Low TTL** for dynamic IPs (60-300 seconds)
2. **High TTL** for static records (3600+ seconds)
3. **CAA records** — Restrict which CAs can issue certs
4. **SPF/DKIM/DMARC** — Email authentication records
5. **Monitor DNS propagation** — Use `dig` or `nslookup`

---

## 7. SECURITY HARDENING

### Essential Security Checks

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Check for failed SSH attempts
sudo grep "Failed password" /var/log/auth.log | tail -20

# 3. Check open ports
sudo ss -tlnp

# 4. Check firewall status
sudo ufw status verbose

# 5. Check for suspicious processes
ps aux --sort=-%cpu | head -20

# 6. Check disk usage
df -h

# 7. Check for modified files in last 24 hours
find /var/www -mtime -1 -type f
```

### Security Best Practices

1. **Fail2Ban** — Auto-ban IPs with too many failed logins
2. **UFW Firewall** — Only allow necessary ports (80, 443, Tailscale)
3. **Disable root SSH** — Use sudo users only
4. **SSH key-only auth** — Disable password authentication
5. **Automatic security updates** — `unattended-upgrades`
6. **File permissions** — Web files: 644, directories: 755
7. **Remove default pages** — Delete server info pages
8. **Security headers** — CSP, X-Frame-Options, X-Content-Type-Options

### Security Headers to Add

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

---

## 8. BACKUP & DISASTER RECOVERY

### Backup Strategy: 3-2-1 Rule

- **3** copies of data
- **2** different storage types
- **1** offsite backup

### Free Backup Tools

| Tool | Type | Best For |
|------|------|----------|
| **rsync** | File sync | Local backups |
| **rclone** | Cloud sync | Google Drive, S3, Backblaze |
| **restic** | Deduplicated | Encrypted backups |
| **BorgBackup** | Deduplicated | Compressed, encrypted |
| **Duplicati** | GUI-based | Windows/Linux |

### Agent Backup Script Pattern

```bash
#!/bin/bash
# Daily backup script for agent webmaster

BACKUP_DIR="/backups/$(date +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"

# Backup website files
tar czf "$BACKUP_DIR/www.tar.gz" /var/www/

# Backup databases
mysqldump -u root --all-databases | gzip > "$BACKUP_DIR/mysql.sql.gz"

# Backup configs
tar czf "$BACKUP_DIR/etc.tar.gz" /etc/nginx/ /etc/letsencrypt/ /etc/crontab

# Sync to remote (rclone configured separately)
rclone sync "$BACKUP_DIR" remote:backups/$(hostname)/

# Keep only 7 days locally
find /backups/ -maxdepth 1 -mtime +7 -type d -exec rm -rf {} \;
```

---

## 9. PERFORMANCE OPTIMIZATION

### Quick Performance Wins

1. **Enable gzip compression** in nginx
2. **Enable browser caching** for static assets
3. **Optimize images** — WebP format, proper sizing
4. **Minify CSS/JS** — Reduce file sizes
5. **Use a CDN** — Cloudflare free tier
6. **Database optimization** — Index queries, clean old data
7. **PHP OPcache** — If using PHP
8. **HTTP/2** — Enable in nginx

### Performance Monitoring Commands

```bash
# Real-time server stats
htop
# or
glances

# Network connections
ss -s

# Disk I/O
iostat -x 1

# Web server access log analysis
goaccess /var/log/nginx/access.log -o /tmp/report.html

# Page speed (Lighthouse)
lighthouse https://example.com --output html --output-path /tmp/lighthouse.html
```

---

## 10. AGENT-TO-AGENT SKILL SHARING

### The SKILL.md Format

Skills are **Markdown files** that teach agents how to do specific tasks. The format:

```markdown
---
name: skill-name
description: What this skill does
version: 1.0.0
platforms: [linux, macos, windows]
---

# Skill Title

## When to use
Trigger conditions...

## Steps
1. First step
2. Second step

## Pitfalls
What to watch out for...

## Verification
How to confirm it worked...
```

### How to Share Skills Between Agents

**Method 1: GitHub/GitLab Repository**
```
agent-skills/
├── webmaster/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── backup.sh
│   │   └── monitor.sh
│   └── references/
│       └── nginx-config.md
├── security/
│   ├── SKILL.md
│   └── scripts/
└── monitoring/
    ├── SKILL.md
    └── scripts/
```

**Method 2: Tailscale File Sharing**
```bash
# Share skill directory via Tailscale
tailscale serve --bg file:///home/agent/skills/

# Other agents access via:
# http://agent-machine.tailnet-name.ts.net:443/
```

**Method 3: Git-based Sync**
```bash
# Agent A pushes new skill
cd /home/agent/skills
git add .
git commit -m "Add webmaster monitoring skill"
git push origin main

# Agent B pulls updates
cd /home/agent/skills
git pull origin main
```

### Best Practices for Shareable Skills

1. **YAML frontmatter** — Always include name, description, version
2. **Trigger conditions** — Clear "when to use" section
3. **Step-by-step** — Numbered steps with exact commands
4. **Pitfalls section** — What goes wrong and how to avoid it
5. **Verification** — How to confirm the skill worked
6. **No hardcoded secrets** — Use environment variables
7. **Test before sharing** — Verify on a clean system
8. **Version control** — Track changes with git

---

## 11. NEW IDEAS & INNOVATIONS

### Idea 1: Self-Healing Websites
An agent that doesn't just monitor but **auto-heals**:
- Detects 502 errors → restarts the service
- Detects high CPU → identifies the process → kills or throttles
- Detects disk full → cleans logs and temp files
- Detects SSL expiring → renews automatically

### Idea 2: Predictive Maintenance
Use patterns to predict issues before they happen:
- Disk filling up at 2%/day → will be full in 7 days → alert now
- Memory usage creeping up → possible memory leak → investigate
- Traffic spike pattern → prepare for load

### Idea 3: Multi-Agent Webmaster Team
Different agents specialize in different areas:
- **Monitor Agent** — Watches everything, sends alerts
- **Security Agent** — Scans for vulnerabilities, manages firewall
- **Backup Agent** — Handles all backup operations
- **Performance Agent** — Optimizes speed and caching
- **Content Agent** — Manages website content updates

### Idea 4: Agent Skill Marketplace
A shared repository where agents contribute and download skills:
- Rate skills by effectiveness
- Version control for skill updates
- Cross-agent compatibility testing
- Community contributions

### Idea 5: Voice-Controlled Server Management
Owner speaks to agent → agent executes:
- "Hey agent, how's the server?" → Full status report
- "Restart nginx" → Executes and confirms
- "Show me the logs" → Summarizes recent activity
- "Backup everything" → Runs full backup

### Idea 6: Automated Incident Response Playbook
When something goes wrong, the agent follows a playbook:
1. Detect issue
2. Classify severity (P1-P4)
3. Attempt auto-heal
4. If auto-heal fails, escalate to owner
5. Document incident
6. Update playbook with lessons learned

### Idea 7: Cross-Network Agent Coordination via Tailscale
Multiple agents on different networks coordinate:
- Agent A (home server) ↔ Agent B (cloud VPS) ↔ Agent C (office)
- Shared task queue via git
- Centralized monitoring dashboard
- Distributed backup (each agent backs up the others)

---

## 12. DAILY OPERATIONS CHECKLIST

### Morning Check (Automated)
- [ ] All websites responding (HTTP 200)
- [ ] SSL certificates valid (>30 days)
- [ ] Disk space OK (<85%)
- [ ] Memory usage OK (<90%)
- [ ] No failed SSH attempts overnight
- [ ] Backups completed successfully
- [ ] Tailscale connected to all peers
- [ ] No critical log errors

### Weekly Tasks
- [ ] System updates applied
- [ ] Security scan completed
- [ ] Backup integrity verified
- [ ] Performance report generated
- [ ] SSL certificate check
- [ ] DNS records verified
- [ ] Firewall rules reviewed

### Monthly Tasks
- [ ] Full security audit
- [ ] Disaster recovery test
- [ ] Skill library updated
- [ ] Performance trend analysis
- [ ] Cost optimization review
- [ ] Documentation updated

---

## APPENDIX: QUICK REFERENCE

### Essential Commands

```bash
# System
sudo apt update && sudo apt upgrade -y    # Update system
htop                                       # System monitor
df -h                                      # Disk usage
free -m                                    # Memory usage
uptime                                     # System uptime

# Web
sudo nginx -t                              # Test nginx config
sudo systemctl restart nginx               # Restart nginx
sudo certbot renew                         # Renew SSL
curl -I https://example.com               # Check headers

# Security
sudo ufw status                            # Firewall status
sudo fail2ban-client status                # Fail2Ban status
sudo tail -f /var/log/auth.log            # Auth logs
sudo tail -f /var/log/nginx/error.log     # Nginx errors

# Tailscale
tailscale status                           # Tailnet status
tailscale ping hostname                    # Ping tailnet peer
tailscale ssh user@hostname                # SSH via Tailscale

# Backup
rsync -avz /var/www/ /backup/www/         # Backup web files
mysqldump -u root -p dbname > backup.sql  # Backup database
rclone sync /backup remote:backups         # Sync to cloud
```

### Free Services Summary

| Service | Use | Limit |
|---------|-----|-------|
| UptimeRobot | Monitoring | 50 monitors |
| Let's Encrypt | SSL Certs | Unlimited |
| Cloudflare | DNS + CDN | Unlimited |
| Backblaze B2 | Cloud Storage | 10GB free |
| GitHub | Code/Skills Storage | Unlimited public |
| GitLab | Code/Skills Storage | Unlimited |
| DuckDNS | Dynamic DNS | Unlimited |

---

*This document is designed to be shared with other agents. Store it in a git repository for version control and easy distribution.*
*Last updated: June 10, 2026 by Mingo*
