# Module 2 — Your First AI Agent
## "From Zero to a Live, Deployed Agent"

*Duration: ~2.5 hours | 4 Lessons*
*HANDS-ON — student deploys a real working agent by end of module*

---

## 🎯 Module Goal
Student leaves with:
- A live AI agent deployed on the internet
- Understanding of how to configure, prompt, and customize an agent
- Their agent answering questions specific to their business

**Module Deliverable:** A working AI agent with a public URL they can share with customers or staff.

---

## 📚 Lessons

### Lesson 2.1 — Setting Up Your AI Workspace
**Core Message:** Before you build, you set up your workbench. Takes 15 minutes, saves hours later.

**Script Topics:**
- Logging into KiloClaw for the first time
- Understanding the interface: what each section does
- Connecting your OpenRouter API key (so the AI has a brain)
- Your first test: ask it something, see it respond

**Slide Outline:**
1. Title: "Setting Up Your Workspace"
2. KiloClaw dashboard overview — annotated screenshot
3. Where to add your OpenRouter API key
4. Test prompt: "Tell me about my business" → how to interpret the response
5. What "tokens" are and why they matter for cost
6. Pricing reality check: $5 of OpenRouter credits = thousands of messages

**Follow-Along Guide:**
- [ ] Log into KiloClaw
- [ ] Navigate to Settings → API Keys
- [ ] Paste your OpenRouter API key
- [ ] Open a new chat window
- [ ] Type: "Hello, what can you help me with?"
- [ ] Screenshot your first response — milestone moment!

---

### Lesson 2.2 — The Art of the System Prompt
**Core Message:** The system prompt is your agent's job description. Write it well and it works great. Write it poorly and it goes rogue.

**Script Topics:**
- What a system prompt is and why it matters
- The 5 parts of a great system prompt: Role, Context, Rules, Tone, Limits
- Live example: Jay writes a system prompt for a cake shop agent
- Common mistakes: too vague, too long, no rules
- The "hired employee" mental model — write it like an employee handbook

**Slide Outline:**
1. Title: "The System Prompt — Your Agent's Job Description"
2. What happens without one (demo — chaotic response)
3. What happens with one (demo — focused, on-brand response)
4. The 5 parts template
5. Live example: Sweet Spot Cakes agent prompt
6. Live example: Contractor agent prompt
7. Your turn — fill in the template for YOUR business

**Follow-Along Guide:**
**System Prompt Template:**
```
You are [NAME], the AI assistant for [BUSINESS NAME].

ABOUT US:
[2-3 sentences about what the business does]

YOUR JOB:
- Help customers with [task 1]
- Answer questions about [topic 1], [topic 2]
- Collect [customer name / phone / order details] when needed

YOUR RULES:
- Always be friendly and professional
- Never make up prices — say "I'll have someone confirm that for you"
- Never discuss competitors
- If you don't know something, say: "Let me have Jay get back to you on that"

YOUR TONE:
[Friendly and casual / Professional and formal / Warm and personal]
```

- Write YOUR system prompt in this template before moving on

---

### Lesson 2.3 — Deploying Your Agent (Putting It on the Internet)
**Core Message:** An agent that only lives on your computer helps no one. We put it live in 20 minutes.

**Script Topics:**
- What "deploying" means (plain English: putting it somewhere anyone can reach it)
- Using the AI Agent Widget app to create a hosted agent
- Getting a public URL for your agent
- Testing it from a phone (the real test)
- The embed code: how to put it on any website

**Slide Outline:**
1. Title: "Going Live — Your Agent on the Internet"
2. What deployment means — diagram
3. AI Agent Widget walkthrough — creating a new agent
4. Name, tagline, emoji, brand color — making it yours
5. The public URL — share this anywhere
6. The embed snippet — paste this in any website
7. "You now have something most businesses don't"

**Follow-Along Guide:**
- [ ] Go to https://ai.widget.alexanderai.site
- [ ] Log in (instructor provides credentials for course participants)
- [ ] Click "Create New Agent"
- [ ] Paste your system prompt from Lesson 2.2
- [ ] Set your name, emoji, and brand color
- [ ] Click Deploy
- [ ] Copy your public URL
- [ ] Open it on your phone and have a conversation with your agent
- [ ] Screenshot — this is your first live AI deployment!

---

### Lesson 2.4 — Teaching Your Agent About Your Business
**Core Message:** A generic agent is okay. An agent that knows YOUR prices, YOUR policies, and YOUR products is a superpower.

**Script Topics:**
- Knowledge base: uploading documents, FAQs, price lists
- How the agent searches its knowledge (RAG — in plain English: "it reads your docs before answering")
- What to upload: FAQs, product list, service menu, policies
- Testing: ask it something that's ONLY in your documents
- Updating: how to keep it current as your business changes

**Slide Outline:**
1. Title: "Teaching Your Agent — Knowledge Base"
2. Generic vs. trained agent — side by side demo
3. What RAG means without the jargon ("it looks it up before answering")
4. What to upload — checklist
5. Live demo: uploading a price list and testing it
6. How to update when prices/services change
7. "Your agent knows your business now"

**Follow-Along Guide:**
**What to prepare for your knowledge base:**
- [ ] Write a simple FAQ (10 common customer questions + answers)
- [ ] Write your service/product list with prices
- [ ] Write your hours, location, and contact info
- [ ] Write your policies (returns, cancellations, turnaround time)
- Upload each as a plain .txt or .pdf file
- Test: ask your agent a question that's ONLY in those documents
- Does it answer correctly? If not, improve the document and re-upload

---

## ✅ Module 2 Completion Checklist
- [ ] OpenRouter API key connected to KiloClaw
- [ ] System prompt written for YOUR business
- [ ] Agent created in AI Agent Widget
- [ ] Public URL live and tested from phone
- [ ] Knowledge base uploaded (FAQ, prices, policies)
- [ ] Agent answers 5 real customer questions correctly
- [ ] Ready for Module 3: Building Your First App
