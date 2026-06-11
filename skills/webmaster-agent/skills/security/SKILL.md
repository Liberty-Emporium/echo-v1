---
name: webmaster-security
description: Security hardening, vulnerability scanning, and incident response for agent webmasters
version: 1.0.0
platforms: [linux, macos]
---

# Webmaster Security Skill

## When to use
- Setting up server security
- Investigating suspicious activity
- Hardening a new server
- Responding to security incidents

## Initial Server Hardening Checklist

### 1. System Updates
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades
```

### 2. SSH Hardening
```bash
# Edit /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2

# Restart SSH
sudo systemctl restart sshd
```

### 3. Firewall Setup (UFW)
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 22/tcp      # SSH (or use Tailscale SSH)
sudo ufw enable
sudo ufw status verbose
```

### 4. Fail2Ban
```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Check status
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

### 5. Automatic Security Updates
```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Security Scanning

### Quick Scan Script
```bash
#!/bin/bash
# Save as /usr/local/bin/security-scan.sh
echo "=== Security Scan $(date) ==="

echo "--- Failed SSH Attempts (last 24h) ---"
sudo grep "Failed password" /var/log/auth.log | grep "$(date +%b' '%d)" | wc -l

echo "--- Open Ports ---"
sudo ss -tlnp | grep LISTEN

echo "--- Sudo Users ---"
grep -E '^sudo:|^wheel:' /etc/group

echo "--- World-Writable Files in /etc ---"
find /etc -type f -perm -002 2>/dev/null

echo "--- Running Processes (high CPU) ---"
ps aux --sort=-%cpu | head -10

echo "--- Recent Logins ---"
last -20

echo "--- Firewall Status ---"
sudo ufw status | head -5
```

## Incident Response Playbook

### Level 1: Suspicious Activity
1. Check logs: `sudo tail -100 /var/log/auth.log`
2. Check processes: `ps aux --sort=-%cpu`
3. Check connections: `ss -tlnp`
4. If SSH brute force: `sudo fail2ban-client set sshd banip IP_ADDRESS`

### Level 2: Confirmed Breach Attempt
1. Block IP: `sudo ufw deny from IP_ADDRESS`
2. Ban with Fail2Ban: `sudo fail2ban-client set sshd banip IP_ADDRESS`
3. Check for backdoors: `find / -name "*.sh" -mtime -1 2>/dev/null`
4. Check crontab: `sudo crontab -l` and `sudo ls /etc/cron.d/`
5. Report to owner

### Level 3: Active Compromise
1. Isolate: `sudo ufw default deny incoming`
2. Preserve evidence: `sudo cp /var/log/auth.log /tmp/auth.log.backup`
3. Check for rootkits: `sudo apt install rkhunter && sudo rkhunter --check`
4. Change all passwords
5. Report to owner immediately
6. Consider rebuilding from known-good backup

## Security Headers for Web Servers

### Nginx
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### Apache
```apache
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

## Pitfalls
- Don't disable password auth until SSH keys are confirmed working
- Always test firewall rules before applying — you can lock yourself out
- Don't ban your own IP in Fail2Ban
- Keep logs — they're evidence if something goes wrong
- Security is a process, not a one-time setup

## Verification
```bash
# Test SSH config
sudo sshd -t

# Test nginx config
sudo nginx -t

# Verify firewall
sudo ufw status verbose

# Check fail2ban
sudo fail2ban-client status

# Test SSL rating
# Visit: https://www.ssllabs.com/ssltest/
```
