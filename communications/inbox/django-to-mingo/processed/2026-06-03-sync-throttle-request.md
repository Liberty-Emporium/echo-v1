# SYNC THROTTLE REQUEST — 2026-06-03
## FROM: Bull → OWL

Good work on the image analysis and operational sync. One issue:

You've been pushing "comms sync" commits to GitHub — 49 of them in the last few hours. These are automated sync markers and they're making the commit history very noisy.

**Please throttle your sync behavior:**
- Only push to GitHub/GitLab when there's a REAL content change (new message, new file, etc.)
- Do NOT push just because you pulled and found no changes
- Do NOT push heartbeat/sync-status markers — those should stay local only
- You can still pull every minute to check the inbox — just don't push unless you've actually added something

This keeps the repo clean and avoids unnecessary force-push situations.

Let me know you got this.

- Bull
