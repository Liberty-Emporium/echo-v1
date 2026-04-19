#!/usr/bin/env python3
"""
Grace Caregiver Automation
Echo uses this to manage Mom's Grace app via Playwright
without Jay having to navigate the UI manually.

Usage:
  python3 grace_caregiver.py add_med --name "Lisinopril" --dose "10mg" --times "08:00" "20:00"
  python3 grace_caregiver.py add_appointment --title "Dr. Smith" --date "2026-04-25" --time "14:00" --doctor "Dr. Smith" --location "123 Main St"
  python3 grace_caregiver.py add_task --title "Call the pharmacy" --date "2026-04-20"
  python3 grace_caregiver.py list_meds
  python3 grace_caregiver.py remove_med --name "Lisinopril"
  python3 grace_caregiver.py set_name --name "Mom"
"""

import argparse
import os
import sys
import time
from playwright.sync_api import sync_playwright, expect

GRACE_URL = os.environ.get("GRACE_URL", "https://web-production-1015f.up.railway.app")
GRACE_PIN  = os.environ.get("GRACE_PIN", "1234")

def login_caregiver(page):
    """Log into Grace caregiver panel."""
    print(f"🔐 Logging into Grace caregiver panel...")
    page.goto(f"{GRACE_URL}/caregiver")
    page.wait_for_load_state("networkidle")

    # Enter PIN digit by digit using the PIN pad buttons
    for digit in GRACE_PIN:
        # Click the number button
        page.locator(f"button:has-text('{digit}')").first.click()
        time.sleep(0.1)

    # Submit
    page.locator("button[type='submit']").click()
    page.wait_for_url(f"{GRACE_URL}/caregiver/dashboard", timeout=10000)
    print("✅ Logged in!")

def add_med(page, name, dose="", times=None, notes="", color="#6366f1"):
    """Add a medication."""
    if times is None:
        times = ["08:00"]

    login_caregiver(page)
    print(f"💊 Adding medication: {name} ({dose}) at {', '.join(times)}")

    # Fill name
    page.locator("input[name='name']").first.fill(name)

    # Fill dose
    if dose:
        page.locator("input[name='dose']").first.fill(dose)

    # Set first time
    time_inputs = page.locator("input[name='times']")
    time_inputs.first.fill(times[0])

    # Add extra times
    for t in times[1:]:
        page.locator("button:has-text('+ Add another time')").click()
        time.sleep(0.2)
        # Fill the last time input
        all_times = page.locator("input[name='times']")
        all_times.last.fill(t)

    # Notes
    if notes:
        page.locator("input[name='notes']").first.fill(notes)

    # Submit
    page.locator("button[type='submit']:has-text('Add Medication')").click()
    page.wait_for_load_state("networkidle")

    # Check for success flash
    content = page.content()
    if "added" in content.lower() or name.lower() in content.lower():
        print(f"✅ {name} added successfully!")
        return True
    else:
        print(f"⚠️  Check Grace app to confirm {name} was added")
        return False

def add_appointment(page, title, date, time_str, doctor="", location="", notes="", remind_min=60):
    """Add an appointment."""
    login_caregiver(page)
    print(f"📅 Adding appointment: {title} on {date} at {time_str}")

    page.locator("input[name='title']").first.fill(title)
    if doctor:
        page.locator("input[name='doctor']").first.fill(doctor)
    if location:
        page.locator("input[name='location']").first.fill(location)

    page.locator("input[name='appt_date']").first.fill(date)
    page.locator("input[name='appt_time']").first.fill(time_str)

    if notes:
        # Find notes field if it exists
        notes_input = page.locator("input[name='notes']")
        if notes_input.count() > 0:
            notes_input.last.fill(notes)

    # Set reminder
    page.locator("select[name='remind_min']").first.select_option(str(remind_min))

    page.locator("button[type='submit']:has-text('Add Appointment')").click()
    page.wait_for_load_state("networkidle")

    content = page.content()
    if "added" in content.lower():
        print(f"✅ Appointment '{title}' added!")
        return True
    else:
        print(f"⚠️  Check Grace app to confirm appointment was added")
        return False

def add_task(page, title, due_date="", due_time=""):
    """Add a task."""
    login_caregiver(page)
    print(f"✅ Adding task: {title}")

    page.locator("input[name='title']").last.fill(title)
    if due_date:
        page.locator("input[name='due_date']").last.fill(due_date)
    if due_time:
        page.locator("input[name='due_time']").last.fill(due_time)

    page.locator("button[type='submit']:has-text('Add Task')").click()
    page.wait_for_load_state("networkidle")

    content = page.content()
    if "added" in content.lower():
        print(f"✅ Task '{title}' added!")
        return True
    else:
        print(f"⚠️  Check Grace app to confirm task was added")
        return False

def list_meds(page):
    """List all current medications."""
    login_caregiver(page)
    print("💊 Current medications:")
    content = page.content()
    # Parse med names from the page
    from playwright.sync_api import sync_playwright
    rows = page.locator(".card >> text=/.*mg|.*tablet|.*pill/i")
    meds = page.locator("[style*='border-radius: 50%'] + div")
    print(content[:500])  # Simple dump for now
    return content

def remove_med(page, name):
    """Remove a medication by name."""
    login_caregiver(page)
    print(f"🗑️ Removing medication: {name}")

    # Find the remove button next to the med
    med_rows = page.locator("div").filter(has_text=name)
    if med_rows.count() == 0:
        print(f"❌ Medication '{name}' not found")
        return False

    # Click remove button in that row
    remove_btn = med_rows.first.locator("button:has-text('Remove')")
    if remove_btn.count() > 0:
        page.on("dialog", lambda d: d.accept())
        remove_btn.click()
        page.wait_for_load_state("networkidle")
        print(f"✅ {name} removed!")
        return True
    else:
        print(f"❌ Could not find Remove button for '{name}'")
        return False

def set_name(page, name):
    """Update the user's name in settings."""
    login_caregiver(page)
    print(f"📝 Setting user name to: {name}")

    page.locator("input[name='user_name']").fill(name)
    page.locator("button[type='submit']:has-text('Save Settings')").click()
    page.wait_for_load_state("networkidle")
    print(f"✅ Name set to {name}!")

def take_screenshot(page, filename="grace_screenshot.png"):
    """Take a screenshot of Grace home page."""
    page.goto(GRACE_URL)
    page.wait_for_load_state("networkidle")
    page.screenshot(path=filename, full_page=True)
    print(f"📸 Screenshot saved: {filename}")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Grace Caregiver Automation")
    parser.add_argument("action", choices=[
        "add_med", "add_appointment", "add_task",
        "list_meds", "remove_med", "set_name", "screenshot"
    ])

    # Med args
    parser.add_argument("--name",     help="Name (med name, appointment title, task title, or user name)")
    parser.add_argument("--dose",     help="Medication dose (e.g. 10mg)")
    parser.add_argument("--times",    nargs="+", help="Time(s) for medication (e.g. 08:00 20:00)")
    parser.add_argument("--notes",    help="Notes")
    parser.add_argument("--color",    default="#6366f1", help="Medication color")

    # Appointment args
    parser.add_argument("--date",     help="Date (YYYY-MM-DD)")
    parser.add_argument("--time",     help="Time (HH:MM)")
    parser.add_argument("--doctor",   help="Doctor name")
    parser.add_argument("--location", help="Location")
    parser.add_argument("--remind",   type=int, default=60, help="Reminder minutes before (default 60)")

    # Task args
    parser.add_argument("--due_date", help="Due date (YYYY-MM-DD)")
    parser.add_argument("--due_time", help="Due time (HH:MM)")

    # Output
    parser.add_argument("--output",   default="grace_screenshot.png", help="Screenshot output path")
    parser.add_argument("--headless", action="store_true", default=True, help="Run headless (default)")
    parser.add_argument("--visible",  action="store_true", help="Run with visible browser")

    args = parser.parse_args()
    headless = not args.visible

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(viewport={"width": 390, "height": 844})  # iPhone size
        page = context.new_page()

        try:
            if args.action == "add_med":
                if not args.name:
                    print("❌ --name required for add_med"); sys.exit(1)
                add_med(page, args.name, args.dose or "", args.times or ["08:00"], args.notes or "")

            elif args.action == "add_appointment":
                if not args.name or not args.date or not args.time:
                    print("❌ --name, --date, --time required for add_appointment"); sys.exit(1)
                add_appointment(page, args.name, args.date, args.time,
                               args.doctor or "", args.location or "",
                               args.notes or "", args.remind)

            elif args.action == "add_task":
                if not args.name:
                    print("❌ --name required for add_task"); sys.exit(1)
                add_task(page, args.name, args.due_date or "", args.due_time or "")

            elif args.action == "list_meds":
                list_meds(page)

            elif args.action == "remove_med":
                if not args.name:
                    print("❌ --name required for remove_med"); sys.exit(1)
                remove_med(page, args.name)

            elif args.action == "set_name":
                if not args.name:
                    print("❌ --name required for set_name"); sys.exit(1)
                set_name(page, args.name)

            elif args.action == "screenshot":
                take_screenshot(page, args.output)

        except Exception as e:
            print(f"❌ Error: {e}")
            page.screenshot(path="grace_error.png")
            print("📸 Error screenshot saved: grace_error.png")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    main()
