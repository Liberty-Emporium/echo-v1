# Module 4 — Automation & Connections
## "Making Your Tools Work Together (While You Sleep)"

*Duration: ~2.5 hours | 4 Lessons*
*HANDS-ON — student sets up at least one real working automation*

---

## 🎯 Module Goal
Student leaves with:
- At least one live automation running (email OR text notification)
- Understanding of how to connect their app to outside services
- A plan for the full automation network they want to build

**Module Deliverable:** A real automation — when something happens in their app, it automatically notifies them or their customer.

---

## 📚 Lessons

### Lesson 4.1 — What Automation Really Means for Your Business
**Core Message:** Automation means the work happens whether you're in the building or not.

**Script Topics:**
- The difference between manual, semi-automated, and fully automated
- Real examples from Jay's apps:
  - Order placed → customer gets confirmation text automatically
  - New appointment booked → staff gets notified by email
  - Inventory item low → alert sent to owner
  - Payment overdue → reminder sent to customer
- The "sleeping owner" test: does this still work at 2am when you're asleep?
- Where most businesses stop (manual) and where you're going (automated)

**Slide Outline:**
1. Title: "What Automation Really Means"
2. The 3 levels: Manual / Semi-Auto / Fully Auto — diagram
3. Time cost of manual vs. automated — real numbers
4. 10 automation examples across different business types
5. The "sleeping owner" test
6. Your automation wishlist — fill in 3 automations you want
7. "We're building #1 today. The rest follow the same pattern."

**Follow-Along Guide:**
- Write your 3 automation wishes:
  1. When _________ happens, I want _________ to happen automatically
  2. When _________ happens, I want _________ to happen automatically
  3. When _________ happens, I want _________ to happen automatically
- Circle the one that would save you the most time or delight your customers most
- That's what we build in Lesson 4.2

---

### Lesson 4.2 — Email Notifications: Your App Talks to You
**Core Message:** Every time something important happens in your app, you get an email. Set it once, never miss a thing.

**Script Topics:**
- How email sending works in a Flask app (SMTP)
- Using Gmail as your sender (free, reliable)
- The notification email template: what to include
- Triggering it from your app: "when a form is submitted, send this email"
- Testing it end-to-end

**Slide Outline:**
1. Title: "Email Notifications"
2. How app → email works (diagram)
3. Gmail App Password setup — step by step
4. The Flask email code (explained line by line in plain English)
5. The notification email template
6. Testing: submit the form, watch the email arrive
7. "You'll never miss an order, inquiry, or alert again"

**Follow-Along Guide:**
```python
# Email notification snippet — add to your Flask app
import smtplib
from email.mime.text import MIMEText

def send_notification(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your-business@gmail.com'
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your-business@gmail.com', 'YOUR_APP_PASSWORD')
        smtp.send_message(msg)
```
- [ ] Create a Gmail App Password (Google Account → Security → App Passwords)
- [ ] Add EMAIL_USER and EMAIL_PASS to Railway environment variables
- [ ] Add the send_notification function to your app
- [ ] Call it when a form is submitted
- [ ] Test: fill in your form, check your email within 30 seconds

---

### Lesson 4.3 — Text Message Notifications (SMS)
**Core Message:** Email is for you. Text is for your customer. Both are automated.

**Script Topics:**
- Why text works better than email for customer-facing notifications
- Twilio: the easiest way to send texts from an app (free trial sends 15 texts)
- The 3 texts every business should send: confirmation, reminder, ready/complete
- Setting up Twilio and getting your API credentials
- Adding SMS to your app alongside email

**Slide Outline:**
1. Title: "Text Message Notifications"
2. Email vs. SMS open rates — why texts win for customers
3. The 3 texts every business needs
4. Twilio setup walkthrough
5. The SMS code snippet — explained plain English
6. Triggering it from your form
7. "Your customer gets a text the second they place an order"

**Follow-Along Guide:**
```python
# SMS notification snippet — Twilio
from twilio.rest import Client

def send_sms(to_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_='+1XXXXXXXXXX',  # your Twilio number
        to=to_number
    )
```
- [ ] Sign up at twilio.com (free trial — no credit card needed to test)
- [ ] Get your Account SID, Auth Token, and phone number
- [ ] Add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE to Railway env vars
- [ ] Add SMS to the same form submission handler as email
- [ ] Test: submit form, customer phone receives text ✅

**The 3 SMS Templates:**
```
ORDER CONFIRMATION:
"Hi [Name]! Your order at [Business] has been received. 
We'll have it ready by [date/time]. Questions? Call [phone]."

REMINDER:
"Hi [Name], just a reminder that your [appointment/order] 
at [Business] is [tomorrow / in 2 hours]. See you then!"

READY/COMPLETE:
"Hi [Name]! Your [order/item] at [Business] is ready 
for pickup. Come by anytime during [hours]. Thank you!"
```

---

### Lesson 4.4 — Connecting Your Apps (The Network Vision)
**Core Message:** One app is useful. Ten apps that talk to each other is a business operating system.

**Script Topics:**
- Jay's vision: the Liberty-Emporium app network
- How apps share data via APIs (plain English: apps talk to each other the way apps talk to users — over the internet)
- EcDash as the control plane: one dashboard to see everything
- The credential vault: one place for all your API keys
- Phase-by-phase: how to grow from 1 app → full network
- What this looks like in 12 months: a self-managing app ecosystem

**Slide Outline:**
1. Title: "The Network Vision"
2. One app diagram
3. Three apps diagram — starting to connect
4. Ten apps diagram — the full network
5. Jay's actual app network — live screenshot of EcDash
6. The credential vault concept
7. "You started with an agent. Now you're building an ecosystem."
8. Your 12-month roadmap — fill in 3 apps you want to build

**Follow-Along Guide:**
- Draw your own app network:
  - Center: YOUR BUSINESS NAME
  - Spokes: each app or tool you want connected
  - Label what each one does
  - Mark: which one did you already build in Module 3?
- This drawing is your roadmap for the rest of the course and beyond

---

## ✅ Module 4 Completion Checklist
- [ ] Automation wishlist written (3 items)
- [ ] Email notification working in your app
- [ ] SMS notification working in your app
- [ ] Customer receives text on form submission
- [ ] App network drawing completed
- [ ] 12-month app roadmap started
- [ ] Ready for Module 5: Real Business Playbooks
