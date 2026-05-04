# Wednesday Pilot Session Plan
## "Your First AI Agent + Your First App"
*For: Jay's first in-person student | Date: 2026-05-07*
*Duration: 2–3 hours | Location: In-person*

---

## 🎯 Session Goal
Student leaves Wednesday with:
1. **A live AI agent** deployed and accessible from their phone
2. **A working web app** specific to their business (or a strong start on it)
3. **Understanding** of how to keep building on their own
4. **Excitement** — they have to FEEL the power of what they just did

---

## ⏱️ Session Timeline

| Time | Activity |
|------|----------|
| 0:00–0:15 | Welcome + Discovery |
| 0:15–0:45 | The Big Picture (slides/talk) |
| 0:45–1:30 | Build: AI Agent (hands-on) |
| 1:30–1:45 | Break + celebrate milestone 1 |
| 1:45–2:30 | Build: Their First App (hands-on) |
| 2:30–2:45 | Wrap up + homework + next steps |

---

## 🔑 Opening Question (Do This First — Before Anything Else)

Sit down, open a notepad, and ask:

> **"What's one thing in your business that takes too much of your time every week — something repetitive, something you wish just happened automatically?"**

Write their answer down. Everything you build today should connect back to this answer. At the end of the session, say: *"Remember what you told me at the start? You now have the tool that handles it."*

---

## Part 1: The Big Picture (15–20 min)

**Goal:** They understand WHY this matters before they touch anything.

### Talk Track (Script)

*"Let me show you something before we start building."*

Pull up your apps — EcDash, AI Agent Widget, Sweet Spot, Contractor Pro — and give a 2-minute tour.

*"Every one of these apps runs 24/7 without me. Customers can place orders, ask questions, get notified — I don't have to be there. I built all of these using AI. No developer. No coding bootcamp. Just me, an AI, and a clear idea of what I needed.*

*Today you're going to build your first one. By the time you leave here, you'll have a live AI agent with your business name on it that you can share with your customers from your phone. Let's go."*

### Key Points to Hit
- AI agents are not chatbots — they take action
- You don't write code — you describe what you want
- Everything we build today is live on the internet, not just on your computer
- This is the same process Jay uses for every app

---

## Part 2: Build the AI Agent (45 min)

### Step 1: Write the System Prompt Together (15 min)

Open a Google Doc or notepad. Ask them:
- "What's your business name?"
- "What do customers usually ask you?"
- "What do you want the agent to be able to do? What should it NOT do?"
- "What's your tone — casual and friendly, or formal and professional?"

Then fill in the template together:

```
You are [NAME], the AI assistant for [BUSINESS NAME].

ABOUT US:
[2-3 sentences about what the business does]

YOUR JOB:
- Help customers with [common question 1]
- Help customers with [common question 2]
- Collect customer name and phone number before helping them
- Mention that a real person will follow up for anything complex

YOUR RULES:
- Always be friendly
- Never make up prices — say "I'll have someone get back to you on that"
- If someone asks something you don't know, say "Let me have [their name] follow up with you"

YOUR TONE:
[Their answer]
```

### Step 2: Create the Agent (15 min)

Go to: **https://ai.widget.alexanderai.site**

Walk them through:
1. Create New Agent
2. Paste the system prompt
3. Pick their emoji and brand color
4. Hit Deploy
5. Copy the public URL

*"Text that link to yourself right now. Open it on your phone. You just deployed an AI agent."*

**🎉 Milestone 1 — Celebrate this.** Let them play with it for 5 minutes.

### Step 3: Train It (10 min)

Ask: "What's something a customer would ask that has a specific answer — a price, a policy, hours, something like that?"

Have them type a quick FAQ document:
```
Q: What are your hours?
A: [their answer]

Q: How much does [service/product] cost?
A: [their answer]

Q: How do I place an order?
A: [their answer]
```

Upload it to the knowledge base. Test it — ask the agent the questions they just wrote. Watch it answer correctly.

*"Your agent now knows your business."*

---

## ☕ Break (15 min)
Let them show their agent to someone on their phone. Let the excitement breathe.

---

## Part 3: Build Their First App (45 min)

**Pick the right starting point based on their business:**

| Business Type | What to Build |
|---|---|
| Retail / Products | Simple order intake form |
| Service (contractor, cleaner, etc.) | Job request form with notification |
| Food / Specialty | Custom order form |
| Any | Customer contact/inquiry form with email alert |

**If time is tight, go with the universal option: a contact/inquiry form with email notification.** Every business can use it and it teaches everything.

### Step 1: Plan It Together (10 min)

Fill in the App Planning Canvas on paper:
```
App Name: _______________________________
What does it do? (one sentence): __________
Who uses it? (customer / staff / both): ____
What does it need to remember?
  - Customer name
  - Phone number
  - [their specific fields]
What pages does it need?
  - Submission form (customer-facing)
  - Admin view (owner sees all submissions)
```

### Step 2: Use AI to Build It (15 min)

Open KiloClaw. Use this prompt (fill in their details):

```
Build me a simple Flask web app called "[APP NAME]".

PURPOSE: [one sentence from their canvas]

PAGES:
1. Home page with a form for customers to submit [their info]
2. Admin page (password protected) showing all submissions in a table

DATABASE (SQLite):
Table: submissions
Fields: id, name, phone, email, message, created_at

STYLE: Clean, modern, mobile-friendly. Dark theme. 
Primary color: [their brand color or #6366f1].
Include the business name "[BUSINESS NAME]" in the header.
Include a /health endpoint returning {"status": "ok"}.
```

While it generates: explain what's happening, what each part does.

### Step 3: Deploy to Railway (15 min)

1. Create a GitHub repo (help them if needed)
2. Push the code
3. Connect to Railway → Deploy
4. Add `SECRET_KEY` env var
5. Watch it go live

*"Go to that URL on your phone."*

**🎉 Milestone 2 — They have a live web app.** 

### Bonus: Add Email Notification (if time allows, 5 min)
Add the email snippet to the form submission handler so they get an email every time someone submits. This is the "wow" moment — submit the form, watch the email arrive.

---

## 🎁 What They Leave With

1. **Their agent URL** — share with customers immediately
2. **Their app URL** — put the link on their website or send to customers
3. **The embed code** — how to put the agent chat widget on any page
4. **The homework sheet** (see below)
5. **Access to the course** (when launched) — they're student #1

---

## 📋 Homework Sheet (Print This or Send It)

```
YOUR HOMEWORK — Build on What We Started Today
================================================

1. SHARE YOUR AGENT
   Your agent URL: ___________________________
   Send it to 3 customers or friends and ask:
   "Does this feel helpful? What would make it better?"

2. TRAIN YOUR AGENT MORE
   Write 10 more FAQ answers and upload them to your knowledge base.
   Test each one.

3. SUBMIT ONE REAL FORM
   Use your app as if you're a customer.
   Does it work the way you expected?
   Write down one thing you want to change.

4. THINK ABOUT MODULE 2
   What's the NEXT thing in your business you want to automate?
   Write it down. We'll build it next session.

QUESTIONS? Contact Jay: [contact info]
```

---

## 📹 Recording Checklist (For Jay)

- [ ] Screen recording running before student arrives (OBS or Loom)
- [ ] Record the full session
- [ ] Capture: the opening question and their answer
- [ ] Capture: the moment their agent goes live
- [ ] Capture: the moment their app goes live
- [ ] Ask for a quick 60-second testimonial at the end ("How do you feel about what you just built?")
- [ ] These clips become your course trailer + Module 1 introduction

---

## 💡 Tips for the Session

- **Follow their energy.** If they're more excited about the agent than the app, spend more time there.
- **Let them type.** Don't take over the keyboard. Guide with words.
- **Celebrate every milestone.** These are genuinely impressive moments for a first-timer.
- **Write down every question they ask.** Each one is a future lesson or FAQ.
- **Don't try to teach everything.** One session = two deliverables max.
