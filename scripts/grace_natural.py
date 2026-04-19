#!/usr/bin/env python3
"""
Grace Natural Language Wrapper
Echo calls this to parse Jay's natural language instructions
and translate them into grace_caregiver.py commands.

Example inputs:
  "Add blood pressure pill, Lisinopril, 10mg, every morning at 8am"
  "Add a doctor appointment, Dr. Smith, April 25th at 2pm, at 123 Main St"
  "Add task: call the pharmacy tomorrow"
  "Remove Lisinopril"
  "Set Mom's name to Dorothy"
  "What medications does Mom have?"
"""

import subprocess
import sys
import os
import re
from datetime import datetime, date, timedelta

SCRIPT = os.path.join(os.path.dirname(__file__), "grace_caregiver.py")
GRACE_PIN = os.environ.get("GRACE_PIN", "1234")

def parse_time(text):
    """Parse time from natural language."""
    text = text.lower().strip()
    # "8am", "8:00am", "8:00", "20:00", "8 am"
    patterns = [
        (r'(\d{1,2}):(\d{2})\s*(am|pm)', lambda m: f"{int(m.group(1)) + (12 if m.group(3)=='pm' and int(m.group(1))!=12 else 0):02d}:{m.group(2)}"),
        (r'(\d{1,2})\s*(am|pm)',          lambda m: f"{int(m.group(1)) + (12 if m.group(2)=='pm' and int(m.group(1))!=12 else 0):02d}:00"),
        (r'(\d{2}):(\d{2})',              lambda m: f"{m.group(1)}:{m.group(2)}"),
        (r'noon|12pm',                    lambda m: "12:00"),
        (r'midnight',                     lambda m: "00:00"),
        (r'morning',                      lambda m: "08:00"),
        (r'afternoon',                    lambda m: "14:00"),
        (r'evening|night',                lambda m: "19:00"),
        (r'bedtime',                      lambda m: "21:00"),
    ]
    for pattern, formatter in patterns:
        m = re.search(pattern, text)
        if m:
            try:
                return formatter(m)
            except:
                pass
    return "08:00"  # default

def parse_date(text):
    """Parse date from natural language."""
    text = text.lower().strip()
    today = date.today()

    if 'today' in text:
        return today.isoformat()
    if 'tomorrow' in text:
        return (today + timedelta(days=1)).isoformat()
    if 'monday' in text or 'next monday' in text:
        days = (0 - today.weekday()) % 7 or 7
        return (today + timedelta(days=days)).isoformat()

    # Month day patterns: "april 25", "apr 25th", "25th april"
    months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
              'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12,
              'january':1,'february':2,'march':3,'april':4,'june':6,
              'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}

    for month_name, month_num in months.items():
        pattern = rf'{month_name}\s+(\d{{1,2}})'
        m = re.search(pattern, text)
        if m:
            day = int(m.group(1))
            year = today.year
            try:
                d = date(year, month_num, day)
                if d < today:
                    d = date(year + 1, month_num, day)
                return d.isoformat()
            except:
                pass

    # YYYY-MM-DD
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    return (today + timedelta(days=7)).isoformat()  # default: 1 week

def run_grace(args):
    """Run grace_caregiver.py with given args."""
    cmd = ["python3", SCRIPT] + args
    env = {**os.environ, "GRACE_PIN": GRACE_PIN}
    print(f"🤖 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, env=env, capture_output=False)
    return result.returncode == 0

def handle_instruction(instruction):
    """Parse and execute a natural language instruction."""
    text = instruction.lower().strip()

    # ── Add Medication ──────────────────────────────────────────────────────
    if any(w in text for w in ["add med", "add medication", "add pill", "add drug",
                                 "medication:", "take ", "remind.*med", "blood pressure",
                                 "tablet", "capsule"]):
        # Extract name - look for quoted or capitalized drug names
        name = None

        # Try quoted name first
        m = re.search(r'"([^"]+)"|\'([^\']+)\'', instruction)
        if m:
            name = m.group(1) or m.group(2)

        # Try to find capitalized drug name
        if not name:
            words = instruction.split()
            for i, w in enumerate(words):
                if w[0].isupper() and len(w) > 2 and w.lower() not in ['add','pill','med','medication','take','remind']:
                    name = w.rstrip('.,')
                    break

        # Fallback: ask user
        if not name:
            name = input("💊 Medication name: ").strip()

        # Extract dose
        dose_m = re.search(r'(\d+\s*mg|\d+\s*mcg|\d+\s*ml|\d+\s*tablet|\d+\s*pill)', text, re.IGNORECASE)
        dose = dose_m.group(0) if dose_m else ""

        # Extract times
        times = []
        time_phrases = re.findall(r'(?:at\s+)?(\d{1,2}(?::\d{2})?\s*(?:am|pm)|morning|afternoon|evening|night|bedtime|noon|midnight|\d{2}:\d{2})', text)
        for tp in time_phrases:
            t = parse_time(tp)
            if t not in times:
                times.append(t)
        if not times:
            times = ["08:00"]

        print(f"\n💊 Adding medication:")
        print(f"   Name: {name}")
        print(f"   Dose: {dose or '(not specified)'}")
        print(f"   Times: {', '.join(times)}")

        args = ["add_med", "--name", name]
        if dose: args += ["--dose", dose]
        args += ["--times"] + times
        return run_grace(args)

    # ── Add Appointment ─────────────────────────────────────────────────────
    elif any(w in text for w in ["appointment", "doctor", "dentist", "dr.", "visit", "checkup", "check-up"]):
        # Extract title/doctor
        title = None
        m = re.search(r'"([^"]+)"', instruction)
        if m:
            title = m.group(1)

        if not title:
            # Look for "Dr." pattern
            dr_m = re.search(r'(Dr\.?\s+\w+|Doctor\s+\w+)', instruction, re.IGNORECASE)
            if dr_m:
                title = dr_m.group(0)

        if not title:
            # Look after "appointment" keyword
            am = re.search(r'appointment[,\s]+([^,\n]+)', instruction, re.IGNORECASE)
            if am:
                title = am.group(1).strip()[:50]

        if not title:
            title = input("📅 Appointment title: ").strip()

        appt_date = parse_date(text)
        appt_time = parse_time(text)

        # Location
        loc_m = re.search(r'(?:at|@|location:?)\s+([^,\n]{5,50})', instruction, re.IGNORECASE)
        location = loc_m.group(1).strip() if loc_m else ""

        print(f"\n📅 Adding appointment:")
        print(f"   Title: {title}")
        print(f"   Date: {appt_date}")
        print(f"   Time: {appt_time}")
        if location: print(f"   Location: {location}")

        args = ["add_appointment", "--name", title, "--date", appt_date, "--time", appt_time]
        if location: args += ["--location", location]
        # Doctor is same as title for now
        args += ["--doctor", title]
        return run_grace(args)

    # ── Add Task ────────────────────────────────────────────────────────────
    elif any(w in text for w in ["task", "remind", "todo", "to-do", "to do", "don't forget", "remember to"]):
        # Extract task name
        task_m = re.search(r'(?:task:|remind.*?to|remember to|todo:|add task:?)\s+(.+)', text, re.IGNORECASE)
        if task_m:
            task_title = task_m.group(1).strip().rstrip('.')
        else:
            task_title = instruction.strip()

        due_date = parse_date(text)
        due_time = ""
        if any(w in text for w in ["am", "pm", ":"]):
            due_time = parse_time(text)

        print(f"\n✅ Adding task:")
        print(f"   Task: {task_title}")
        print(f"   Due: {due_date}{' at ' + due_time if due_time else ''}")

        args = ["add_task", "--name", task_title, "--due_date", due_date]
        if due_time: args += ["--due_time", due_time]
        return run_grace(args)

    # ── Remove Medication ───────────────────────────────────────────────────
    elif any(w in text for w in ["remove", "delete", "stop taking", "discontinue"]):
        name_m = re.search(r'(?:remove|delete|stop)\s+(?:the\s+)?([A-Za-z][a-z]+(?:\s+[A-Za-z][a-z]+)?)', instruction, re.IGNORECASE)
        name = name_m.group(1) if name_m else input("💊 Medication name to remove: ").strip()
        print(f"\n🗑️  Removing: {name}")
        return run_grace(["remove_med", "--name", name])

    # ── Set Name ────────────────────────────────────────────────────────────
    elif "name" in text and any(w in text for w in ["set", "change", "update", "call her", "call him"]):
        name_m = re.search(r'(?:to|is|name:?)\s+([A-Z][a-z]+)', instruction)
        name = name_m.group(1) if name_m else input("📝 Name: ").strip()
        return run_grace(["set_name", "--name", name])

    # ── Screenshot ──────────────────────────────────────────────────────────
    elif any(w in text for w in ["screenshot", "show me", "how does it look"]):
        return run_grace(["screenshot", "--output", "grace_screenshot.png"])

    # ── List Meds ───────────────────────────────────────────────────────────
    elif any(w in text for w in ["list", "what meds", "show meds", "medications"]):
        return run_grace(["list_meds"])

    else:
        print(f"🤔 I didn't understand: '{instruction}'")
        print("Try: 'add medication [name] [dose] at [time]'")
        print("Or:  'add appointment [title] on [date] at [time]'")
        print("Or:  'add task [title] tomorrow'")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        instruction = " ".join(sys.argv[1:])
    else:
        instruction = input("🤖 What do you want to do for Mom? ")

    success = handle_instruction(instruction)
    sys.exit(0 if success else 1)
