# SKILLS.md - Echo's Skills System

This is **the most important file** for Echo's long-term growth and memory.

## The Skills Philosophy

**Echo can create skills, store them on GitHub, and use them forever.**

When Echo creates a skill:
1. Build the skill with Python files, scripts, documentation
2. Store it in `skills/custom/` on GitHub
3. Document it in this file
4. Use it anytime in the future

This way Echo doesn't have to create skills on the fly - they're stored and ready to use.

## Default Skills (43)

These come pre-installed with OpenClaw:

1. 1password, apple-notes, apple-reminders, bear-notes
2. blogwatcher, blucli, bluebubbles, camsnap, canvas
3. clawhub, coding-agent, discord, eightctl, gemini
4. gh-issues, gifgrep, gog, goplaces, healthcheck
5. himalaya, imsg, mcporter, model-usage, nano-pdf
6. node-connect, notion, obsidian, openai-whisper
7. openai-whisper-api, openhue, oracle, ordercli, peekaboo
8. sag, session-logs, sherpa-onnx-tts, slack, songsee
9. sonoscli, spotify-player, things-mac, trello, voice-call, wacli

## Custom Skills (32) - Stored in GitHub

All custom skills are stored in: `skills/custom/`

See `skills/custom/README.md` for the full list of skills we've created.

## How to Create a New Skill

When you need a new skill:

1. Create folder: `skills/custom/<skill-name>/`
2. Add `SKILL.md` - Description and metadata
3. Add Python scripts, config files, etc.
4. Upload to GitHub: `skills/custom/<skill-name>/`
5. Update this file with the new skill
6. Update `skills/custom/README.md`

## Skills Storage Location

All custom skills are stored on GitHub:
```
https://github.com/Liberty-Emporium/echo-v1/tree/main/skills/custom/
```

## This is Echo's Legacy

This skills system allows Echo to:
- Build skills once, use forever
- Share skills with others
- Grow smarter over time
- Be useful 20+ years from now
- Pass knowledge to others Jay cares about

---
*Version: 1.0.0 - Created 2026-04-11*
