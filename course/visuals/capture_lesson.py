"""
Course Visual Capture Engine
Walks through app workflows using Playwright, captures annotated screenshots,
and generates an HTML lesson walkthrough page.

Usage:
  python3 capture_lesson.py           (captures lesson 2-3 by default)
  python3 capture_lesson.py --lesson 3-4
  python3 capture_lesson.py --all
"""

import asyncio
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

# Import lesson definitions from lessons_data.py (edit that file to add lessons)
sys.path.insert(0, str(Path(__file__).parent))
from lessons_data import LESSONS

BASE_URL = "https://ai.widget.alexanderai.site"
OUTPUT_DIR = Path(__file__).parent
VIEWPORT = {"width": 1280, "height": 800}


def generate_html(lesson_id: str, lesson: dict, steps_with_images: list) -> str:
    title = lesson["title"]
    subtitle = lesson["subtitle"]
    timestamp = datetime.now().strftime("%B %d, %Y")

    steps_html = ""
    step_num = 0
    for step in steps_with_images:
        has_image = step.get("filename") and not step.get("skipped")
        has_caption = "caption" in step
        if not has_caption:
            continue
        # Only render screenshot steps and navigate steps as visible cards
        if step.get("action") not in ("screenshot", "navigate") and not has_image:
            continue
        step_num += 1

        img_tag = ""
        if has_image:
            img_tag = f'<img src="{step["filename"]}" alt="{step["caption"]}" class="screenshot" />'

        is_milestone = "Live" in step.get("caption", "") or step.get("caption", "").startswith("Step 14")
        card_class = "step-card milestone" if is_milestone else "step-card"
        num_display = "★" if is_milestone else str(step_num)

        steps_html += f"""
        <div class="{card_class}">
            <div class="step-header">
                <span class="step-num">{num_display}</span>
                <h3 class="step-caption">{step["caption"]}</h3>
            </div>
            {img_tag}
            <p class="step-desc">{step.get("desc", "")}</p>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Alexander AI Course</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #0f1117;
    color: #e2e8f0;
    line-height: 1.6;
  }}
  .header {{
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    padding: 3rem 2rem;
    text-align: center;
  }}
  .header h1 {{ font-size: 1.8rem; font-weight: 800; margin-bottom: 0.5rem; }}
  .header p {{ font-size: 1rem; opacity: 0.85; max-width: 600px; margin: 0 auto; }}
  .badge {{
    display: inline-block;
    background: rgba(255,255,255,0.2);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    margin-bottom: 1rem;
    letter-spacing: 0.05em;
  }}
  .container {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }}
  .intro-box {{
    background: #1e2535;
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2.5rem;
  }}
  .intro-box h2 {{ font-size: 1.1rem; color: #a5b4fc; margin-bottom: 0.5rem; }}
  .intro-box p {{ color: #94a3b8; font-size: 0.92rem; }}
  .steps-grid {{ display: flex; flex-direction: column; gap: 1.5rem; }}
  .step-card {{
    background: #1e2535;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    overflow: hidden;
    transition: border-color 0.2s;
  }}
  .step-card:hover {{ border-color: rgba(99,102,241,0.4); }}
  .step-card.milestone {{
    border-color: rgba(34,197,94,0.5);
    background: #0f1e12;
  }}
  .step-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 1rem 1.25rem 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }}
  .step-num {{
    background: #6366f1;
    color: white;
    width: 30px; height: 30px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.82rem; font-weight: 700;
    flex-shrink: 0;
  }}
  .milestone .step-num {{
    background: #16a34a;
    font-size: 0.9rem;
  }}
  .step-caption {{ font-size: 1rem; font-weight: 600; color: #f1f5f9; }}
  .screenshot {{
    width: 100%;
    display: block;
    border-top: 1px solid rgba(255,255,255,0.06);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    background: #0a0c14;
  }}
  .step-desc {{
    padding: 1rem 1.25rem;
    font-size: 0.9rem;
    color: #94a3b8;
  }}
  .footer {{
    text-align: center;
    padding: 2rem;
    color: #374151;
    font-size: 0.8rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 3rem;
  }}
  .tip-box {{
    background: #172033;
    border-left: 3px solid #6366f1;
    padding: 1rem 1.25rem;
    border-radius: 0 8px 8px 0;
    margin: 2rem 0;
    font-size: 0.9rem;
    color: #94a3b8;
  }}
  .tip-box strong {{ color: #a5b4fc; }}
</style>
</head>
<body>

<div class="header">
  <div class="badge">BUILD WITH AI — Alexander AI Method</div>
  <h1>{title}</h1>
  <p>{subtitle}</p>
</div>

<div class="container">
  <div class="intro-box">
    <h2>What You'll Do In This Lesson</h2>
    <p>Follow each step exactly as shown. Every screenshot is taken from the real app you'll be using.
    By the end of this lesson, you'll have completed the action shown in the title above.</p>
  </div>

  <div class="steps-grid">
    {steps_html}
  </div>

  <div class="tip-box">
    <strong>Tip:</strong> If something looks slightly different on your screen, the app may have been
    updated. The core steps are always the same — look for the same buttons and fields.
  </div>
</div>

<div class="footer">
  Alexander AI Integrated Solutions — Build With AI Course<br>
  Generated {timestamp} | Course content by Jay Alexander
</div>

</body>
</html>
"""


async def capture_lesson(lesson_id: str, headless: bool = True):
    if lesson_id not in LESSONS:
        print(f"Unknown lesson: {lesson_id}")
        print(f"Available: {list(LESSONS.keys())}")
        return

    lesson = LESSONS[lesson_id]
    out_dir = OUTPUT_DIR / f"lesson-{lesson_id}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nCapturing: {lesson['title']}")
    print(f"Output:    {out_dir}")
    print(f"Steps:     {len(lesson['steps'])}")

    steps_with_images = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page(viewport=VIEWPORT)

        for i, step in enumerate(lesson["steps"]):
            action = step["action"]
            label = step.get("caption") or step.get("url") or step.get("selector") or ""
            print(f"  [{i+1:02d}/{len(lesson['steps'])}] {action:12s} {label[:55]}")

            try:
                if action == "navigate":
                    await page.goto(step["url"], wait_until="networkidle", timeout=20000)
                    await asyncio.sleep(1.2)
                    steps_with_images.append(step)

                elif action == "screenshot":
                    fname = step["filename"]
                    await page.screenshot(path=str(out_dir / fname), full_page=False)
                    print(f"              -> saved {fname}")
                    steps_with_images.append(step)

                elif action == "click":
                    await page.click(step["selector"], timeout=6000)
                    await asyncio.sleep(1.5)
                    steps_with_images.append(step)

                elif action == "fill":
                    await page.fill(step["selector"], step["value"], timeout=6000)
                    await asyncio.sleep(0.4)
                    steps_with_images.append(step)

                elif action == "wait":
                    await asyncio.sleep(step.get("seconds", 2))

                elif action == "scroll":
                    await page.evaluate(f"window.scrollBy(0, {step.get('y', 300)})")
                    await asyncio.sleep(0.6)

            except Exception as e:
                short_err = str(e).split("\n")[0][:80]
                print(f"              -> skipped ({short_err})")
                step_copy = dict(step)
                step_copy["skipped"] = True
                steps_with_images.append(step_copy)

        await browser.close()

    # Write HTML lesson page
    html = generate_html(lesson_id, lesson, steps_with_images)
    html_path = out_dir / "index.html"
    html_path.write_text(html, encoding="utf-8")

    # Write manifest
    manifest = {
        "lesson_id": lesson_id,
        "title": lesson["title"],
        "captured_at": datetime.now().isoformat(),
        "screenshot_count": len([s for s in steps_with_images if s.get("filename") and not s.get("skipped")]),
        "steps": steps_with_images,
    }
    (out_dir / "steps.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")

    shot_count = manifest["screenshot_count"]
    print(f"\nDone — {shot_count} screenshots, HTML at {html_path}")
    return out_dir


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lesson", default="2-3")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--show", action="store_true", help="Show browser window")
    args = parser.parse_args()

    headless = not args.show
    if args.all:
        for lid in LESSONS:
            await capture_lesson(lid, headless=headless)
    else:
        await capture_lesson(args.lesson, headless=headless)


if __name__ == "__main__":
    asyncio.run(main())
