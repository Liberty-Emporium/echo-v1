# Content Production Reference

## The Most Important Rule

**Audio quality beats video quality.** Bad video with clear audio is watchable. Good video with muffled, echoing, or noisy audio is not. If you invest in one thing, invest in a microphone.

## Minimum Viable Setup

| Component | Budget Option | Upgrade |
|-----------|--------------|---------|
| Microphone | Blue Snowball (~$50) or HyperX SoloCast | Blue Yeti, Rode NT-USB |
| Camera | Built-in webcam or phone | Logitech C920, Sony ZV-E10 |
| Lighting | Face a window (natural light) | $30–50 ring light |
| Background | Plain wall or tidy bookshelf | Virtual background, dedicated backdrop |
| Recording | Free (OBS, Zoom solo, Loom free) | Camtasia, ScreenFlow |

You can start with a $50 USB mic + your laptop webcam + a window and produce professional results.

## Recording Tools

### Free
| Tool | Best For | Platform |
|------|----------|----------|
| OBS Studio | Full control, screen + cam + audio | Win/Mac/Linux |
| Loom (free) | Quick screen recordings, up to 5 min | Win/Mac/Web |
| Zoom (solo) | Simple recording with screen share | Win/Mac |
| DaVinci Resolve | Professional video editing | Win/Mac/Linux |

### Paid
| Tool | Best For | Price |
|------|----------|-------|
| Camtasia | All-in-one record + edit | ~$180/yr |
| ScreenFlow | Mac recording + editing | $169 one-time |
| Loom (paid) | Quick recordings + cloud storage | $12.50/mo |
| Descript | Record, transcribe, edit by text | $12–$24/mo |
| ScreenPal | Simple tutorials | Free / $3/mo |

**Recommendation for most creators:** Start with OBS (free) for recording + DaVinci Resolve (free) for editing. Upgrade to Camtasia when you want an all-in-one workflow.

## OBS Studio Quick Setup

1. Download from obsproject.com, run auto-configuration wizard → "Optimize for recording"
2. Create scenes:
   - **Slides + Webcam** — Display Capture + Video Capture Device (webcam in corner)
   - **Full Screen Demo** — Display Capture only
   - **Camera Only** — Video Capture Device only
3. Settings → Output: Recording Quality = "High Quality, Medium File Size"; Format = MKV
4. Settings → Video: 1920×1080, 30fps
5. Map scenes to number keys (1, 2, 3) for quick switching

## Content Formats

### Video Lessons
Best for: demonstrations, walkthroughs, personal connection, motivation

- **Talking head:** face to camera, good for introductions and conceptual content
- **Screen recording + voiceover:** ideal for software demos, technical content
- **Slides + voiceover:** good for frameworks, data, structured explanations
- **Mix:** webcam in corner while screen recording — most engaging for tutorials

### Text Lessons
Best for: reference material, step-by-step instructions, checklists

- Use when students will return to re-read (procedures, cheat sheets)
- Add code blocks, callouts, numbered lists — scannable structure matters

### Downloadables
Best for: worksheets, templates, checklists, swipe files

- PDFs for fixed-layout content (worksheets, frameworks)
- Canva or Google Doc links for editable templates students can copy
- Spreadsheets for calculators, planners, trackers

### Quizzes
Best for: knowledge checks, self-assessment, certificate requirements

- 3–5 questions per module max
- Use to reinforce key concepts, not trick students
- Completion-based (not grade-gated) for most courses

## Recording Best Practices

**Pre-recording checklist:**
- [ ] Close all unnecessary apps and browser tabs
- [ ] Turn off notifications (email, Slack, phone — especially calendar pop-ups)
- [ ] Clean desktop; hide personal files and browser bookmarks
- [ ] Do a 30-second test recording to check audio levels
- [ ] Have your outline/script visible (second monitor or printed)
- [ ] Glass of water nearby

**During recording:**
- Speak slightly slower than conversational speed (viewers can 2x, they can't un-mumble)
- Narrate your actions: "Now I'll click Settings in the top right..."
- Pause 1–2 seconds between major concepts
- Record in 5–10 minute segments (easier to edit than one long take)
- If you flub a sentence, just pause and redo that section — don't restart
- Move your cursor deliberately; hover over important elements 2–3 seconds

**Audio tips:**
- Record in a small, soft-furnished room (clothes closet = surprisingly good)
- Turn off fans, HVAC, and appliances during takes
- Use noise suppression (OBS has a built-in filter; Krisp or NVIDIA RTX Voice for real-time)
- Microphone 6–12 inches from mouth, slightly off-axis to avoid plosives (p/b sounds)

## Editing Guidelines

**What to cut:**
- Long pauses (>2–3 seconds)
- "Uhh," "umm," false starts
- Dead air at beginning and end of clips
- Repeated takes (keep the best one)

**What to add:**
- Intro title card (consistent across all lessons)
- Chapter markers or timestamps
- Text annotations, callouts, zoom-ins for key moments
- Fade in/out at start and end

**Export settings:**
- Format: MP4 (H.264)
- Resolution: 1080p (1920×1080)
- Frame rate: 30fps
- Bitrate: 8–15 Mbps for course video (balance quality vs. file size)

## AI-Assisted Production

- **Descript:** Record and edit video by editing the transcript — cut filler words automatically
- **Whisper (OpenAI):** Free, local transcription to generate .srt subtitle files
- **ElevenLabs / Synthesia:** AI voiceover or AI avatar for slides-only courses (no webcam)
- **Canva / Adobe Express:** Slide templates, thumbnail design, worksheet graphics

## Lesson Length Guidelines

| Content type | Target length |
|-------------|---------------|
| Introduction / welcome | 2–5 min |
| Concept lesson | 5–10 min |
| Demo / walkthrough | 8–15 min |
| Case study | 5–12 min |
| Q&A / bonus | 10–20 min |
| Live session / webinar | 45–90 min |

Break anything over 15 minutes into parts. Students on mobile appreciate shorter segments.
