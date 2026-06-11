---
name: webmaster-backup
description: Backup and disaster recovery for agent webmasters — automated backups, verification, and restoration
version: 1.0.0
platforms: [linux, macos]
---

# Webmaster Backup & Recovery Skill

## When to use
- Setting up automated backups
- Recovering from data loss
- Migrating to a new server
- Testing disaster recovery

## Backup Strategy: 3-2-1 Rule
- **3** copies of data
- **2** different storage types
- **1** offsite backup

## Free Backup Tools

| Tool | Type | Encryption | Dedup | Best For |
|------|------|-----------|-------|----------|
| **rsync** | File sync | No | No | Local backups |
| **rclone** | Cloud sync | Yes | No | Google Drive, S3 |
| **restic** | Deduplicated | Yes | Yes | Efficient backups |
| **BorgBackup** | Deduplicated | Yes | Yes | Compressed backups |

## Automated Backup Script

Save as `/usr/local/bin/agent-backup.sh`:

```bash
#!/bin/bash
set -euo pipefail

DATE=$(date +%Y-%m-%d_%H-%M)
BACKUP_DIR="/backups/$DATE"
LOG="/var/log/webmaster-backup.log"

mkdir -p "$BACKUP_DIR"

echo "$(date): Starting backup $DATE" | tee -a "$LOG"

# 1. Website files
tar czf "$BACKUP_DIR/www.tar.gz" -C /var/www/ . 2>/dev/null && \
  echo "  ✓ Website files backed up" | tee -a "$LOG"

# 2. Databases (MySQL)
if command -v mysqldump &>/dev/null; then
  mysqldump --all-databases --single-transaction 2>/dev/null | \
    gzip > "$BACKUP_DIR/mysql.sql.gz" && \
    echo "  ✓ MySQL databases backed up" | tee -a "$LOG"
fi

# 3. Databases (PostgreSQL)
if command -v pg_dumpall &>/dev/null; then
  sudo -u postgres pg_dumpall 2>/dev/null | \
    gzip > "$BACKUP_DIR/postgres.sql.gz" && \
    echo "  ✓ PostgreSQL databases backed up" | tee -a "$LOG"
fi

# 4. SSL certificates
tar czf "$BACKUP_DIR/ssl.tar.gz" -C /etc/letsencrypt/ . 2>/dev/null && \
  echo "  ✓ SSL certificates backed up" | tee -a "$LOG"

# 5. Nginx config
tar czf "$BACKUP_DIR/nginx.tar.gz" -C /etc/nginx/ . 2>/dev/null && \
  echo "  ✓ Nginx config backed up" | tee -a "$LOG"

# 6. Crontabs
sudo crontab -l > "$BACKUP_DIR/crontab.txt" 2>/dev/null
sudo tar czf "$BACKUP_DIR/cron.tar.gz" /etc/cron.d/ /etc/cron.daily/ 2>/dev/null && \
  echo "  ✓ Cron jobs backed up" | tee -a "$LOG"

# 7. System packages
dpkg --get-selections > "$BACKUP_DIR/packages.txt" && \
  echo "  ✓ Package list saved" | tee -a "$LOG"

# 8. Tailscale config
sudo cp /var/lib/tailscale/tailscaled.state "$BACKUP_DIR/tailscale.state" 2>/dev/null && \
  echo "  ✓ Tailscale state backed up" | tee -a "$LOG"

# Sync to remote (if rclone configured)
if command -v rclone &>/dev/null; then
  rclone sync "$BACKUP_DIR" "remote:backups/$(hostname)/$DATE" 2>/dev/null && \
    echo "  ✓ Synced to remote storage" | tee -a "$LOG"
fi

# Cleanup: keep 7 local backups
find /backups/ -maxdepth 1 -mtime +7 -type d -exec rm -rf {} \; 2>/dev/null

# Report size
SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo "$(date): Backup complete. Size: $SIZE" | tee -a "$LOG"
```

```bash
chmod +x /usr/local/bin/agent-backup.sh
```

## Cron Setup
```bash
# Daily backup at 3 AM
0 3 * * * /usr/local/bin/agent-backup.sh

# Weekly full system backup (Sunday)
0 4 * * 0 /usr/local/bin/agent-backup.sh full
```

## Restore Procedure

```bash
# 1. Restore website files
sudo tar xzf /backups/latest/www.tar.gz -C /var/www/

# 2. Restore databases
gunzip < /backups/latest/mysql.sql.gz | mysql

# 3. Restore SSL
sudo tar xzf /backups/latest/ssl.tar.gz -C /etc/letsencrypt/

# 4. Restore nginx
sudo tar xzf /backups/latest/nginx.tar.gz -C /etc/nginx/
sudo nginx -t && sudo systemctl restart nginx

# 5. Restore crontabs
sudo crontab /backups/latest/crontab.txt
```

## Pitfalls
- Always test restores — an untested backup is not a backup
- Don't store backups on the same disk as the data
- Encrypt backups that contain sensitive data
- Monitor backup logs — silent failures are common
- Keep offsite copies (cloud, different physical location)

## Verification
```bash
# Check last backup
ls -la /backups/ | tail -5

# Verify backup integrity
tar tzf /backups/latest/www.tar.gz | head -5

# Test restore to temp directory
mkdir /tmp/restore-test
tar xzf /backups/latest/www.tar.gz -C /tmp/restore-test
ls /tmp/restore-test/
rm -rf /tmp/restore-test
```
