# Playwright Test Visibility Options
_Researched 2026-04-22 — How Jay can see what Echo is testing_

## The 5 Options (Simple → Most Powerful)

### Option 1: Screenshots on Every Test ⭐ EASIEST
Auto-take a screenshot at each test step — saved to PNG files you open normally.
No extra tools. Works on Kali.

### Option 2: Headed Mode (Watch Live)
Browser window opens visually as tests run — you watch it click around in real time.
Requires a display (X11/GUI). Works on Kali desktop.

### Option 3: Video Recording (.webm)
Records the whole test run as a video file. Play it back in any browser after.

### Option 4: HTML Report
After tests run, open a beautiful interactive report in your browser — shows pass/fail, 
screenshots, videos, timing per test. Like a test dashboard.

### Option 5: Trace Viewer (Most Powerful)
Records EVERYTHING — every click, every DOM change, network requests.
Upload to trace.playwright.dev and time-travel through the test frame by frame.

---

## What I'm Going to Build

An upgraded test script that does **Options 1 + 3 + 4** automatically:
- Screenshots taken at every key step
- Video recorded of entire run
- HTML report generated at the end
- One command to open the report in your browser
