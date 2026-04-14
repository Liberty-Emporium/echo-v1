# security-audit

Deep security audit of Jay's apps. Uses nmap, sqlmap, gobuster + custom Python checks.
Finds vulnerabilities before bad guys do.

## Usage

```
Security audit: <URL> [--deep] [--fix]
```

## What It Does

### Phase 1 — Recon
- nmap service/version fingerprint
- HTTP headers analysis
- gobuster hidden route discovery (SecLists wordlist)

### Phase 2 — Vulnerability Scan
- sqlmap automated SQL injection test on all forms
- XSS reflection check on all inputs
- IDOR check (can you access other users' data?)
- Auth bypass attempts
- Insecure direct object reference on /product/<sku>, /store/<slug>

### Phase 3 — Code Analysis (when source available)
- Hardcoded secrets scan
- Dangerous function usage (eval, exec, os.system)
- Missing CSRF protection on forms
- Password hashing strength check
- Session configuration review

### Phase 4 — Report
- Severity rating: CRITICAL / HIGH / MEDIUM / LOW
- Remediation steps for each finding
- Saves report to /tmp/security-report-<date>.md

## Tools Required
- nmap (apt-get install nmap)
- sqlmap (apt-get install sqlmap)  
- gobuster (apt-get install gobuster)
- SecLists wordlist (download from GitHub)

## Script

`scripts/audit.py`

## Example

```bash
python3 skills/custom/security-audit/scripts/audit.py \
  --url https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app \
  --deep
```
