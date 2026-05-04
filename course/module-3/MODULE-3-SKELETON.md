# Module 3 — Building Your First App
## "From Idea to Live Web App in a Day"

*Duration: ~3 hours | 5 Lessons*
*HANDS-ON — student deploys their first real web app*

---

## 🎯 Module Goal
Student leaves with:
- A real web app live on Railway with a public URL
- Understanding of how Flask, databases, and Railway work together
- A working app tailored to THEIR business (intake form, order form, simple dashboard)

**Module Deliverable:** A live web app on Railway that does one real thing for their business.

---

## 📚 Lessons

### Lesson 3.1 — How Web Apps Work (Plain English)
**Core Message:** A web app is just a set of instructions that lives on a computer in the cloud. Nothing more.

**Script Topics:**
- The 3 parts of every web app: frontend (what you see), backend (what it does), database (what it remembers)
- Flask as the backend engine — "it's the kitchen, not the dining room"
- SQLite as the database — "it's a spreadsheet that your app can read and write automatically"
- Railway as the host — "it's the building your app lives in"
- How a request flows: browser → Railway → Flask → database → back to browser

**Slide Outline:**
1. Title: "How Web Apps Work"
2. The 3 layers diagram — Frontend / Backend / Database
3. Flask explained — "the kitchen"
4. SQLite explained — "the filing cabinet"
5. Railway explained — "the building"
6. The full request flow — animated diagram
7. "You're going to build all three layers today"

**Follow-Along Guide:**
- No build yet — this is conceptual
- Draw the 3-layer diagram yourself (pen and paper)
- Label each layer with YOUR business example:
  - Frontend: "The page where my customers place cake orders"
  - Backend: "The code that saves the order and sends me a notification"
  - Database: "The list of all orders with customer names and details"

---

### Lesson 3.2 — Your First App: Planning Before Building
**Core Message:** 10 minutes of planning saves 10 hours of rebuilding.

**Script Topics:**
- The App Planning Canvas: 5 questions before you write a line of code
  1. What does this app DO? (one sentence)
  2. Who uses it? (customer, staff, admin, or all three?)
  3. What does it need to REMEMBER? (database fields)
  4. What does it need to SHOW? (pages/views)
  5. What does it need to DO? (actions/buttons)
- Example: planning a custom order intake form for a cake shop
- Example: planning a job request form for a contractor
- Example: planning an inventory check-in app for a retail store

**Slide Outline:**
1. Title: "Plan Before You Build"
2. The 5-question App Planning Canvas
3. Cake shop example — filled in canvas
4. Contractor example — filled in canvas
5. "Now fill yours in — this becomes your build spec"
6. How Jay turns a canvas into a prompt for AI to build
7. Preview: in the next lesson, we hand this to AI and it builds the skeleton

**Follow-Along Guide:**
**App Planning Canvas — fill this out:**
```
MY APP NAME: _______________________________

1. WHAT DOES IT DO? (one sentence):
   _________________________________________

2. WHO USES IT?
   [ ] Customers  [ ] Staff  [ ] Admin  [ ] All

3. WHAT DOES IT REMEMBER? (database fields — list 5-10):
   - _______________________________________
   - _______________________________________
   - _______________________________________
   - _______________________________________
   - _______________________________________

4. WHAT PAGES DOES IT HAVE?
   - Page 1: ________________________________ (what it shows)
   - Page 2: ________________________________
   - Page 3: ________________________________

5. WHAT ACTIONS CAN USERS TAKE?
   - Button/action 1: _______________________
   - Button/action 2: _______________________
   - Button/action 3: _______________________
```

---

### Lesson 3.3 — Using AI to Build Your App Skeleton
**Core Message:** You don't write the code. You describe what you want. AI writes the code. You review and improve.

**Script Topics:**
- How to turn your App Planning Canvas into a build prompt
- The anatomy of a good build prompt: context, stack, pages, database, style
- Live demo: Jay feeds a prompt to KiloClaw and gets a working Flask app skeleton
- What to look for in the generated code (even if you can't read code)
- The review loop: test → find something wrong → describe it → fix it

**Slide Outline:**
1. Title: "Tell AI What to Build"
2. Your canvas → your prompt (transformation)
3. The build prompt template
4. Live demo walkthrough — prompt → code → running app
5. "You don't need to understand every line — you need to understand what it does"
6. The review loop diagram
7. Your turn — write your build prompt

**Follow-Along Guide:**
**Build Prompt Template:**
```
Build me a Flask web app with the following spec:

APP NAME: [your app name]
PURPOSE: [one sentence from your canvas]
USERS: [who uses it]

PAGES:
1. [page name] — [what it shows/does]
2. [page name] — [what it shows/does]
3. [page name] — [what it shows/does]

DATABASE (SQLite):
Table: [table name]
Fields: [field 1], [field 2], [field 3], [field 4]...

STYLE: Dark theme, mobile-friendly, clean modern design.
Use Flask, SQLite, Jinja2 templates, and plain CSS.
Include a /health endpoint that returns {"status": "ok"}.
```

- Paste this into KiloClaw
- Copy the generated code into a new folder on your computer
- Run it locally first (instructor will guide)

---

### Lesson 3.4 — Deploying to Railway (Live in 20 Minutes)
**Core Message:** Local is practice. Railway is real. Let's go real.

**Script Topics:**
- Pushing your code to GitHub (the save step)
- Connecting GitHub to Railway (the deploy step)
- Railway environment variables — what they are and why they matter
- Watching your first deploy: reading the logs
- Visiting your live URL for the first time

**Slide Outline:**
1. Title: "Deploying to Railway"
2. Local → GitHub → Railway flow diagram
3. GitHub: creating a repo and pushing code (screenshots)
4. Railway: new project → connect GitHub → deploy
5. Environment variables explained (SECRET_KEY, DATABASE_URL)
6. Reading deploy logs — what success looks like vs. errors
7. "Your app is live. Anyone in the world can use it right now."

**Follow-Along Guide:**
- [ ] Create a new GitHub repo for your app
- [ ] Push your code: `git add . && git commit -m "first commit" && git push`
- [ ] Log into Railway → New Project → Deploy from GitHub
- [ ] Select your repo
- [ ] Add environment variables:
  - `SECRET_KEY` = any long random string
  - `PORT` = 5000
- [ ] Watch the deploy logs
- [ ] Click your Railway URL when it goes green
- [ ] Screenshot your live app — you just deployed a web app! 🎉

---

### Lesson 3.5 — Making It Yours (Customization & Polish)
**Core Message:** A working app and a good-looking app are not the same thing. This lesson closes the gap.

**Script Topics:**
- Adding your business name, logo, and colors
- Making it mobile-friendly (responsive design basics)
- The 3 things that make an app feel professional: consistent colors, readable fonts, clear buttons
- Adding a simple login/password so strangers can't access your data
- Quick wins: favicon, page title, footer with your business info

**Slide Outline:**
1. Title: "Polish — Making It Look Like Yours"
2. Before/after screenshots (bare vs. branded)
3. CSS variables — one place to change all your colors
4. Mobile preview — how to check it on your phone
5. Adding a simple password page
6. The 3-second test: does a stranger know what this app does in 3 seconds?
7. "Now it's yours"

**Follow-Along Guide:**
- [ ] Update the app name in base.html to your business name
- [ ] Change the primary color to your brand color
- [ ] Add your business tagline to the homepage
- [ ] Test it on your phone
- [ ] Add a simple admin password (instructor provides code snippet)
- [ ] Redeploy to Railway
- [ ] Share your live URL in the course community 🎉

---

## ✅ Module 3 Completion Checklist
- [ ] App Planning Canvas completed
- [ ] Build prompt written
- [ ] App generated and running locally
- [ ] Code pushed to GitHub
- [ ] App live on Railway with a public URL
- [ ] App customized with your brand name and colors
- [ ] Mobile tested
- [ ] URL shared in community
- [ ] Ready for Module 4: Automation & Connections
