# Security Toolkit — Echo's Hacker Arsenal

## Goal
Audit and harden Jay's 7 Railway apps. Find vulnerabilities before bad guys do.

## Tools Available (installed 2026-04-14)
- `nmap` — port scanning, service fingerprinting
- `sqlmap` — automated SQL injection testing
- `gobuster` — hidden route/directory brute forcing
- `python3` — custom exploit scripts

## Tools to Install When Needed
- `nikto` — web vulnerability scanner (not in apt, install from GitHub)
- `hydra` — password brute forcing (for testing login rate limits)
- `wfuzz` — web fuzzing

## Wordlists
- `/usr/share/nmap/nselib/` — nmap scripts
- Download SecLists: https://github.com/danielmiessler/SecLists

## Key Vulnerabilities to Check in Jay's Apps
1. **Password hashing** — currently SHA-256 (weak). Fix: bcrypt
2. **SQL injection** — check all user inputs in sqlite queries
3. **IDOR** — can user A access user B's data by changing slug/id?
4. **Auth bypass** — can you reach admin routes without login?
5. **XSS** — is user input sanitized before rendering?
6. **CSRF** — are forms protected?
7. **Secrets in code** — any hardcoded keys?
8. **Rate limiting** — added to login but check all sensitive routes

## Apps to Audit
1. Liberty Inventory — https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app
2. Dropship Shipping — https://dropship-shipping-production.up.railway.app
3. Consignment Solutions — https://web-production-43ce4.up.railway.app
4. Jay Portfolio — https://jay-portfolio-production.up.railway.app
5. Contractor Pro AI — https://contractor-pro-ai-production.up.railway.app
6. Pet Vet AI — https://pet-vet-ai-production.up.railway.app
7. Jay's Keep Your Secrets — https://ai-api-tracker-production.up.railway.app

## Methodology
1. Gobuster — find hidden routes
2. sqlmap — test all form inputs
3. Manual code review — check auth, IDOR, secrets
4. Fix everything found
5. Document in audit report

---
*Created: 2026-04-14*
