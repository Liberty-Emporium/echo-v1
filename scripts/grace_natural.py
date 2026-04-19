#!/usr/bin/env python3
"""
Grace Natural Language Wrapper
Echo calls this to parse Jay's natural language instructions
and translate them into grace_caregiver.py commands.

Examples:
  "Add Lisinopril 10mg every morning at 8am and evening at 8pm"
  "Add blood pressure pill, 10mg, morning and night"
  "Add doctor appointment Dr. Smith April 25th at 2pm at 123 Main St"
  "Add task: call the pharmacy tomorrow"
  "Remove Lisinopril"
  "Set name to Dorothy"
"""

import subprocess, sys, os, re
from datetime import datetime, date, timedelta

SCRIPT = os.path.join(os.path.dirname(__file__), "grace_caregiver.py")
GRACE_PIN = os.environ.get("GRACE_PIN", "1234")

VENV_PYTHON = "/root/playwright-env/bin/python3"
PYTHON = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

SKIP_WORDS = {
    'add','pill','med','medication','take','remind','every','morning','evening',
    'night','afternoon','daily','twice','times','and','the','for','mom','her',
    'his','my','a','an','drug','vitamin','supplement','at','am','pm','mg','mcg',
    'ml','tablet','capsule','each','once','per','day','dose','dosage','some',
    'please','can','you','could','i','want','to','need'
}

def parse_time(text):
    text = text.lower().strip()
    m = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)', text)
    if m:
        h = int(m.group(1))
        if m.group(3) == 'pm' and h != 12: h += 12
        if m.group(3) == 'am' and h == 12: h = 0
        return f"{h:02d}:{m.group(2)}"
    m = re.search(r'(\d{1,2})\s*(am|pm)', text)
    if m:
        h = int(m.group(1))
        if m.group(2) == 'pm' and h != 12: h += 12
        if m.group(2) == 'am' and h == 12: h = 0
        return f"{h:02d}:00"
    m = re.search(r'(\d{2}):(\d{2})', text)
    if m: return f"{m.group(1)}:{m.group(2)}"
    if 'noon' in text or '12pm' in text: return "12:00"
    if 'midnight' in text: return "00:00"
    if 'morning' in text: return "08:00"
    if 'afternoon' in text: return "14:00"
    if 'evening' in text or 'night' in text: return "19:00"
    if 'bedtime' in text: return "21:00"
    return "08:00"

def parse_date(text):
    text = text.lower().strip()
    today = date.today()
    if 'today' in text: return today.isoformat()
    if 'tomorrow' in text: return (today + timedelta(days=1)).isoformat()
    weekdays = {'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6}
    for day, wd in weekdays.items():
        if day in text:
            days_ahead = (wd - today.weekday()) % 7 or 7
            return (today + timedelta(days=days_ahead)).isoformat()
    months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,
              'sep':9,'oct':10,'nov':11,'dec':12,'january':1,'february':2,
              'march':3,'april':4,'june':6,'july':7,'august':8,'september':9,
              'october':10,'november':11,'december':12}
    for mn, mv in months.items():
        m = re.search(rf'{mn}\w*\s+(\d{{1,2}})', text)
        if m:
            try:
                d = date(today.year, mv, int(m.group(1)))
                if d < today: d = date(today.year + 1, mv, int(m.group(1)))
                return d.isoformat()
            except: pass
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
    if m: return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return (today + timedelta(days=7)).isoformat()

def extract_name(instruction):
    """Extract the first meaningful word (drug/appointment/task name)."""
    m = re.search(r'"([^"]+)"|\'([^\']+)\'', instruction)
    if m: return m.group(1) or m.group(2)
    for w in instruction.split():
        clean = w.rstrip('.,;:').lower()
        if clean not in SKIP_WORDS and len(clean) > 2 and not re.match(r'^\d', clean):
            return w.rstrip('.,;:')
    return None

def run_grace(args):
    cmd = [PYTHON, SCRIPT] + args
    env = {**os.environ, "GRACE_PIN": GRACE_PIN}
    print(f"🤖 Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, env=env)
    return result.returncode == 0

def handle_instruction(instruction):
    text = instruction.lower().strip()

    # ── Remove ──────────────────────────────────────────────────────────────
    if any(w in text for w in ["remove", "delete", "stop taking", "discontinue"]):
        m = re.search(r'(?:remove|delete|stop taking|discontinue)\s+(?:the\s+)?(.+)', instruction, re.IGNORECASE)
        name = m.group(1).strip() if m else input("💊 What to remove? ").strip()
        print(f"\n🗑️  Removing: {name}")
        return run_grace(["remove_med", "--name", name])

    # ── Set Name ────────────────────────────────────────────────────────────
    if re.search(r'set.*(name|call)', text) or re.search(r"(call|name).*is\s+\w+", text):
        m = re.search(r'(?:to|is|name:?)\s+([A-Za-z]+)', instruction, re.IGNORECASE)
        name = m.group(1) if m else input("📝 Name: ").strip()
        return run_grace(["set_name", "--name", name])

    # ── Add Appointment ─────────────────────────────────────────────────────
    if any(w in text for w in ["appointment", "dentist", "dr.", "doctor visit", "checkup", "check-up", "clinic"]):
        m = re.search(r'"([^"]+)"', instruction)
        title = m.group(1) if m else None
        if not title:
            dr = re.search(r'(Dr\.?\s+\w+|Doctor\s+\w+)', instruction, re.IGNORECASE)
            title = dr.group(0) if dr else None
        if not title:
            am = re.search(r'appointment[,\s]+([^,\n@at]{3,40})', instruction, re.IGNORECASE)
            title = am.group(1).strip() if am else input("📅 Appointment title: ").strip()

        appt_date = parse_date(text)
        appt_time = parse_time(text)
        loc_m = re.search(r'(?:at|@|location:?)\s+(\d[^,\n]{4,50})', instruction, re.IGNORECASE)
        location = loc_m.group(1).strip() if loc_m else ""

        print(f"\n📅 Adding appointment: {title} on {appt_date} at {appt_time}")
        if location: print(f"   📍 {location}")

        args = ["add_appointment", "--name", title, "--date", appt_date, "--time", appt_time, "--doctor", title]
        if location: args += ["--location", location]
        return run_grace(args)

    # ── Add Task ────────────────────────────────────────────────────────────
    if any(w in text for w in ["task", "remind", "todo", "to-do", "don't forget", "remember to", "call ", "buy ", "pick up"]):
        # Don't match if it has a dose (that's a med)
        has_dose = bool(re.search(r'\d+\s*(mg|mcg|ml)', text))
        if not has_dose:
            m = re.search(r'(?:task:|remind.*?to|remember to|todo:?|add task:?|task:?)\s+(.+)', instruction, re.IGNORECASE)
            task_title = m.group(1).strip().rstrip('.') if m else instruction.strip()
            due_date = parse_date(text)
            due_time = parse_time(text) if re.search(r'\d+\s*(am|pm)|\d{2}:\d{2}', text) else ""
            print(f"\n✅ Adding task: {task_title} — due {due_date}{' at '+due_time if due_time else ''}")
            args = ["add_task", "--name", task_title, "--due_date", due_date]
            if due_time: args += ["--due_time", due_time]
            return run_grace(args)

    # ── Add Medication (catches anything with a dose OR med keywords) ────────
    has_dose = bool(re.search(r'\d+\s*(mg|mcg|ml|tablet|pill|capsule)', text, re.IGNORECASE))
    has_med_kw = any(w in text for w in [
        "medication","med ","pill","tablet","capsule","blood pressure","cholesterol",
        "insulin","aspirin","vitamin","supplement","add med","drug"
    ])

    if has_dose or has_med_kw or re.match(r'^add\s+[a-z]', text):
        name = extract_name(instruction)
        if not name:
            name = input("💊 Medication name: ").strip()

        dose_m = re.search(r'(\d+\s*(?:mg|mcg|ml|tablet|pill|capsule))', instruction, re.IGNORECASE)
        dose = dose_m.group(0) if dose_m else ""

        # Extract all times mentioned
        times = []
        for tp in re.findall(r'\d{1,2}(?::\d{2})?\s*(?:am|pm)|\d{2}:\d{2}|morning|afternoon|evening|night|bedtime|noon', text):
            t = parse_time(tp)
            if t not in times:
                times.append(t)
        if not times: times = ["08:00"]

        print(f"\n💊 Adding medication: {name}")
        print(f"   Dose: {dose or '(not specified)'}")
        print(f"   Times: {', '.join(times)}")

        args = ["add_med", "--name", name]
        if dose: args += ["--dose", dose]
        args += ["--times"] + times
        return run_grace(args)

    # ── Screenshot ──────────────────────────────────────────────────────────
    if any(w in text for w in ["screenshot", "show me", "how does it look"]):
        return run_grace(["screenshot"])

    # ── List ────────────────────────────────────────────────────────────────
    if any(w in text for w in ["list", "what meds", "show meds", "what does mom have"]):
        return run_grace(["list_meds"])

    print(f"🤔 I didn't understand: '{instruction}'")
    print("Try:")
    print("  'Add Lisinopril 10mg every morning at 8am'")
    print("  'Add doctor appointment Dr. Smith April 25th at 2pm'")
    print("  'Add task: call the pharmacy tomorrow'")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        instruction = " ".join(sys.argv[1:])
    else:
        instruction = input("🤖 What do you want to do for Mom? ")
    sys.exit(0 if handle_instruction(instruction) else 1)
