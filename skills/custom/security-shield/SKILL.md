---
name: security-shield
description: Audit and validate skills before loading. Checks for malicious code, suspicious patterns, data exfiltration risks, and reputation signals. Use when installing new skills, cloning repos, or before executing unknown skill code.
---

# Security Shield

This skill protects against malicious or low-quality skills by providing security auditing capabilities.

## Usage

When asked to install or use a new skill:
1. Use the audit-skill tool to validate it first
2. Check the reputation score
3. Review flagged issues before proceeding

## Tools

### audit-skill

Validates a skill directory or repo for security issues.

**Parameters:**
- `path`: Path to skill directory or GitHub repo URL
- `quick`: If true, only run quick scans (default: false)

**Checks performed:**
- Malicious code patterns (exec, eval, base64, crypto)
- Network call suspicious domains
- Data exfiltration attempts (unexpected file writes, network uploads)
- Obfuscated code detection
- Missing dependencies or outdated packages
- Suspicious file operations

**Returns:** JSON with:
- `safe`: boolean - whether skill passes basic checks
- `issues`: array of issues found (severity: high/medium/low)
- `score`: 0-100 trust score
- `recommendation`: allow/block/review

### check-reputation

Checks GitHub author reputation.

**Parameters:**
- `repo_url`: GitHub repository URL

**Returns:**
- `author`: author info
- `stars`, `forks`: popularity metrics
- `account_age`: days since created
- `recent_commits`: activity level
- `score`: 0-100 reputation score

### review-skill-code

Deep review of skill code for hidden threats.

**Parameters:**
- `path`: Path to skill directory

**Returns:** Detailed analysis of:
- All network calls made by the skill
- File system access patterns
- Environment variable usage
- External command executions

## Severity Levels

- **CRITICAL**: Immediate block - clear malicious intent
- **HIGH**: Block - significant security risk
- **MEDIUM**: Review - requires human approval
- **LOW**: Warning - best practices violation
- **INFO**: Notice - informational only

## Default Policy

```
ALLOW if: score >= 80 and no CRITICAL/HIGH issues
REVIEW if: score >= 50 or has MEDIUM issues  
BLOCK if: score < 50 or has any CRITICAL/HIGH issues
```

## Examples

**Quick audit:**
```
audit-skill(path="/path/to/skill", quick=true)
```

**Full audit with reputation:**
```
check-reputation(repo_url="https://github.com/author/skill-name")
audit-skill(path="/path/to/skill", quick=false)
```

**Before loading unknown skill:**
```
# Always run before installing new skills
audit-skill(path="https://github.com/user/suspicious-skill")
```

## Notes

- Always run audit before loading skills from unknown sources
- Check reputation for skills from untrusted authors
- If in doubt, ask user before proceeding
- Some false positives are acceptable - better safe than sorry
- Document any manual approvals in session
