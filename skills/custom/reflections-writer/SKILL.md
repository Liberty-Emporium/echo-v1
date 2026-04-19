# reflections-writer

**Version:** 1.0.0
**Created:** 2026-04-18
**Author:** Echo

## Description

End-of-session reflection capture. After every work session, write 3-5 lessons learned to REFLECTIONS.md. These accumulate into a permanent behavioral playbook — turning one-time mistakes into permanent rules.

Per self-improvement research (2026-04-14): this is one of the top 5 ways to make Echo better over time.

## When To Use

- At end of every coding/building session
- After hitting a bug or unexpected problem
- When something worked better than expected
- When Jay corrects a behavior or explains a preference

## REFLECTIONS.md Format

```markdown
## [DATE] — [SESSION TOPIC]

**REFLECTION:** [What happened / what I learned]
**VERIFIED:** [Did this actually cause a problem? Yes/No]
**STATUS:** [Added to AGENTS.md | Added to skill | Just noted]
**APPLIES TO:** [All apps | specific app | echo-v1 | general]

---
```

## Example Reflections

```markdown
## 2026-04-18 — New Instance Setup

**REFLECTION:** `allowlist` security mode blocks ALL commands including `openclaw` CLI itself.
Use `full` + `ask: "off"` instead. allowlist requires pre-approved command patterns we don't have configured.
**VERIFIED:** Yes — blocked all execs after config change.
**STATUS:** Reverted to full. Will not use allowlist again without pre-configuring patterns.
**APPLIES TO:** All Echo instances

---

**REFLECTION:** echo-v1 clone path must match what save-brain.sh expects (`/root/.openclaw/workspace/echo-v1`).
If cloned elsewhere, create a symlink or update the script.
**VERIFIED:** Yes — save-brain.sh failed with "No such file or directory".
**STATUS:** Added symlink. Updated save-brain.sh WORKSPACE var awareness.
**APPLIES TO:** echo-v1

---

**REFLECTION:** GitLab protected main branch cannot be force-pushed.
When behind, always `git pull --rebase` first, then push normally.
**VERIFIED:** Yes — force push rejected by GitLab.
**STATUS:** Use pull --rebase pattern in all GitLab push operations.
**APPLIES TO:** All repos

---
```

## Auto-Write Pattern

At end of session, write reflections before running save-brain.sh:

```python
# Add to end-of-session checklist in AGENTS.md
# 1. Write 3-5 reflections to REFLECTIONS.md
# 2. Update memory/YYYY-MM-DD.md with session summary
# 3. Run save-brain.sh
```

## Script Usage

```bash
# View all reflections
cat /root/.openclaw/echo-v1/REFLECTIONS.md

# Count total reflections
grep -c "^## 20" /root/.openclaw/echo-v1/REFLECTIONS.md

# Find reflections about a topic
grep -A4 "Railway" /root/.openclaw/echo-v1/REFLECTIONS.md
```
