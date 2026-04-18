# email-drip

**Version:** 1.0.0
**Created:** 2026-04-18
**Author:** Echo

## Description

Trial onboarding and lifecycle email drip sequences for Jay's Flask SaaS apps. Pure Python + SMTP — no external service required. Covers welcome, activation, conversion, and churn prevention emails.

## Research-Backed Email Sequence

Per research: **trials without email convert at 15-20%. With email: 30-40%.** This is 2x revenue from the same signups.

### The Proven SaaS Onboarding Sequence

| Day | Email | Subject Line | Goal |
|-----|-------|-------------|------|
| 0 | Welcome | Welcome to [App]! Here's how to get started | Orient |
| 1 | Quick win | Complete your first [action] in 5 minutes | Activate |
| 3 | Feature highlight | Have you discovered [key feature] yet? | Educate |
| 7 | Halfway check-in | You're halfway through your trial — here's your progress | Support |
| 10 | Urgency | 4 days left — here's what you'll lose | Urgency |
| 13 | Final warning | Your trial ends tomorrow | Final push |
| 14 | Expired | Your trial has ended | Re-engage |

## Environment Variables Required

```bash
SMTP_HOST=smtp.gmail.com        # or smtp.sendgrid.net etc
SMTP_PORT=587
SMTP_USER=notifications@alexanderaiis.com
SMTP_PASS=your-app-password     # Gmail app password
FROM_EMAIL=notifications@alexanderaiis.com
FROM_NAME=Alexander AI Integrated Solutions
APP_NAME=Your App Name
APP_URL=https://your-app.up.railway.app
```

## Core Implementation

### email_service.py — Drop into any app

```python
import smtplib
import os
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone, timedelta

SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASS = os.environ.get('SMTP_PASS', '')
FROM_EMAIL = os.environ.get('FROM_EMAIL', SMTP_USER)
FROM_NAME = os.environ.get('FROM_NAME', 'Alexander AI')
APP_NAME = os.environ.get('APP_NAME', 'Your App')
APP_URL = os.environ.get('APP_URL', 'https://example.com')

def send_email(to_email, subject, html_body, text_body=None):
    """Send email in background thread — never block a route."""
    def _send():
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
            msg['To'] = to_email
            if text_body:
                msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        except Exception as e:
            print(f"[EMAIL ERROR] {e}")
    threading.Thread(target=_send, daemon=True).start()

# ── Email Templates ───────────────────────────────────────────

def send_welcome(to_email, name):
    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px">
      <h2 style="color:#1a1a2e">Welcome to {APP_NAME}, {name}! 🎉</h2>
      <p>You're on a 14-day free trial. Here's how to get the most out of it:</p>
      <ol>
        <li>Complete your profile setup</li>
        <li>Try the main feature (it takes under 5 minutes)</li>
        <li>Check your dashboard — your data is already there</li>
      </ol>
      <a href="{APP_URL}/dashboard" style="background:#4f46e5;color:white;padding:12px 24px;
         border-radius:6px;text-decoration:none;display:inline-block;margin-top:16px">
        Get Started →
      </a>
      <p style="color:#666;margin-top:24px">Questions? Just reply to this email.</p>
    </div>"""
    send_email(to_email, f"Welcome to {APP_NAME}! Here's how to get started", html)

def send_day1_activation(to_email, name):
    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px">
      <h2 style="color:#1a1a2e">Quick win: 5 minutes to your first result</h2>
      <p>Hi {name},</p>
      <p>Most users who complete their first action in {APP_NAME} end up staying long-term. 
         It only takes 5 minutes.</p>
      <a href="{APP_URL}/dashboard" style="background:#4f46e5;color:white;padding:12px 24px;
         border-radius:6px;text-decoration:none;display:inline-block;margin-top:16px">
        Do It Now →
      </a>
    </div>"""
    send_email(to_email, f"Complete your first action in {APP_NAME} (5 min)", html)

def send_day7_checkin(to_email, name):
    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px">
      <h2 style="color:#1a1a2e">You're halfway through your trial</h2>
      <p>Hi {name}, you have 7 days left.</p>
      <p>If {APP_NAME} has been useful, now's a great time to upgrade and lock in your data.</p>
      <a href="{APP_URL}/settings/billing" style="background:#16a34a;color:white;padding:12px 24px;
         border-radius:6px;text-decoration:none;display:inline-block;margin-top:16px">
        See Plans →
      </a>
      <p style="color:#666;margin-top:24px">Not finding value yet? Reply and tell us what's missing.</p>
    </div>"""
    send_email(to_email, f"You're halfway through your {APP_NAME} trial", html)

def send_day10_urgency(to_email, name):
    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px">
      <h2 style="color:#dc2626">4 days left in your trial</h2>
      <p>Hi {name},</p>
      <p>When your trial ends, you'll lose access to:</p>
      <ul>
        <li>All your data and history</li>
        <li>Your saved settings and preferences</li>
        <li>Everything you've built so far</li>
      </ul>
      <p>Don't lose your progress. Upgrade now for as little as a coffee a day.</p>
      <a href="{APP_URL}/settings/billing" style="background:#dc2626;color:white;padding:12px 24px;
         border-radius:6px;text-decoration:none;display:inline-block;margin-top:16px">
        Upgrade Before It's Gone →
      </a>
    </div>"""
    send_email(to_email, f"4 days left — don't lose your {APP_NAME} data", html)

def send_day13_final(to_email, name):
    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px">
      <h2 style="color:#dc2626">Your trial ends tomorrow</h2>
      <p>Hi {name},</p>
      <p>Last chance to keep everything you've built in {APP_NAME}.</p>
      <p>Upgrade today and get your first month for the price shown.</p>
      <a href="{APP_URL}/settings/billing" style="background:#dc2626;color:white;padding:12px 24px;
         border-radius:6px;text-decoration:none;display:inline-block;margin-top:16px">
        Upgrade Now — Last Chance →
      </a>
    </div>"""
    send_email(to_email, f"⚠️ Your {APP_NAME} trial ends TOMORROW", html)

def send_trial_expired(to_email, name):
    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px">
      <h2>Your {APP_NAME} trial has ended</h2>
      <p>Hi {name},</p>
      <p>Your free trial has expired. Your data is safe — we've kept it for 30 days.</p>
      <p>Ready to continue? Pick a plan and pick up right where you left off.</p>
      <a href="{APP_URL}/settings/billing" style="background:#4f46e5;color:white;padding:12px 24px;
         border-radius:6px;text-decoration:none;display:inline-block;margin-top:16px">
        Reactivate My Account →
      </a>
      <p style="color:#999;font-size:0.85rem;margin-top:24px">
        Data deleted after 30 days of inactivity.
      </p>
    </div>"""
    send_email(to_email, f"Your {APP_NAME} trial has ended — your data is waiting", html)

def send_payment_failed(to_email, name):
    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;padding:24px">
      <h2 style="color:#dc2626">Payment failed for {APP_NAME}</h2>
      <p>Hi {name},</p>
      <p>We couldn't process your payment. Your account will stay active for 3 more days 
         while you update your billing info.</p>
      <a href="{APP_URL}/settings/billing" style="background:#dc2626;color:white;padding:12px 24px;
         border-radius:6px;text-decoration:none;display:inline-block;margin-top:16px">
        Update Payment Method →
      </a>
    </div>"""
    send_email(to_email, f"⚠️ Payment failed — action required for {APP_NAME}", html)
```

### drip_scheduler.py — Background job to send sequence

```python
import sqlite3
from datetime import datetime, timezone, timedelta
from email_service import (
    send_day1_activation, send_day7_checkin,
    send_day10_urgency, send_day13_final, send_trial_expired
)

DB_PATH = os.environ.get('DB_PATH', '/data/app.db')

def run_drip_scheduler():
    """Call this once per hour from a background thread or cron."""
    now = datetime.now(timezone.utc)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    users = conn.execute(
        "SELECT * FROM users WHERE plan='trial' AND plan_status='active'"
    ).fetchall()

    for user in users:
        trial_start = datetime.fromisoformat(user['created_at'])
        days_in = (now - trial_start).days
        email = user['email']
        name = user.get('name', 'there')
        sent = user.get('drip_sent', '') or ''

        if days_in >= 1 and 'day1' not in sent:
            send_day1_activation(email, name)
            _mark_sent(conn, user['id'], sent, 'day1')
        elif days_in >= 7 and 'day7' not in sent:
            send_day7_checkin(email, name)
            _mark_sent(conn, user['id'], sent, 'day7')
        elif days_in >= 10 and 'day10' not in sent:
            send_day10_urgency(email, name)
            _mark_sent(conn, user['id'], sent, 'day10')
        elif days_in >= 13 and 'day13' not in sent:
            send_day13_final(email, name)
            _mark_sent(conn, user['id'], sent, 'day13')
        elif days_in >= 14 and 'expired' not in sent:
            send_trial_expired(email, name)
            _mark_sent(conn, user['id'], sent, 'expired')

    conn.commit()
    conn.close()

def _mark_sent(conn, user_id, current, new_tag):
    updated = f"{current},{new_tag}".strip(',')
    conn.execute("UPDATE users SET drip_sent=? WHERE id=?", (updated, user_id))
```

## DB Column Required

```sql
ALTER TABLE users ADD COLUMN drip_sent TEXT DEFAULT '';
```

## Start Scheduler in app.py

```python
import threading, time
from drip_scheduler import run_drip_scheduler

def drip_worker():
    while True:
        try:
            run_drip_scheduler()
        except Exception as e:
            print(f"[DRIP ERROR] {e}")
        time.sleep(3600)  # run every hour

threading.Thread(target=drip_worker, daemon=True).start()
```

## Per-App Checklist

- [ ] Add SMTP env vars to Railway
- [ ] Copy email_service.py and drip_scheduler.py to app
- [ ] Add `drip_sent` column to users table
- [ ] Call `send_welcome()` in signup route
- [ ] Start drip_worker thread in app.py
- [ ] Test with your own email before deploying
