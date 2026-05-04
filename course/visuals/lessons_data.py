"""
Lesson step definitions for the Course Visual Capture Engine.
Each lesson has a title, subtitle, and a list of steps.
Step actions: navigate, screenshot, click, fill, scroll, wait
"""

BASE_URL = "https://ai.widget.alexanderai.site"

LESSONS = {

    # =========================================================================
    # MODULE 1 — THE FOUNDATION
    # =========================================================================

    "1-1": {
        "title": "Lesson 1.1 — What Is an AI Agent?",
        "subtitle": "Why your business needs one — and what's actually possible right now",
        "steps": [
            {"action": "navigate", "url": BASE_URL,
             "caption": "Step 1: Meet a Real AI Agent Platform",
             "desc": "This is the Alexander AI Agent Widget — a platform Jay built to deploy AI agents to any website. We're looking at a live agent platform before we build one."},
            {"action": "screenshot", "filename": "01-agent-widget-home.png",
             "caption": "Step 1: A Real AI Platform — Built by a Business Owner",
             "desc": "Jay Alexander built this entire platform himself using AI. No developer hired. No agency. This is what you'll be able to do by the end of this course."},

            {"action": "navigate", "url": "https://billy-floods.up.railway.app",
             "caption": "Step 2: A Real Business App — FloodClaim Pro",
             "desc": "FloodClaim Pro helps homeowners file insurance claims after flooding. Built with AI."},
            {"action": "screenshot", "filename": "02-floodclaim-app.png",
             "caption": "Step 2: FloodClaim Pro — Real App, Real Users",
             "desc": "This app is live right now. It has a database, a login system, a dashboard, and a workflow. A business owner built this with AI. You'll learn exactly how."},

            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app",
             "caption": "Step 3: Sweet Spot Custom Cakes",
             "desc": "A custom cake ordering app for a small bakery."},
            {"action": "screenshot", "filename": "03-sweet-spot-app.png",
             "caption": "Step 3: A Custom App for a Small Business",
             "desc": "Sweet Spot Custom Cakes lets customers order custom cakes, track their order, and get notified when it's ready. This is what YOUR business could have — not generic software, something built exactly for you."},

            {"action": "navigate", "url": "https://contractor-pro-ai-production.up.railway.app",
             "caption": "Step 4: Contractor Pro AI",
             "desc": "Built for contractors and service businesses."},
            {"action": "screenshot", "filename": "04-contractor-app.png",
             "caption": "Step 4: Contractor Pro AI — Built for Service Businesses",
             "desc": "Contractor Pro AI helps contractors manage jobs, generate quotes, and communicate with clients. Every app you've seen was built by one person using AI tools — your instructor. You're next."},

            {"action": "navigate", "url": "https://pet-vet-ai-production.up.railway.app",
             "caption": "Step 5: Pet Vet AI",
             "desc": "An AI-powered vet finder for pet owners."},
            {"action": "screenshot", "filename": "05-petvet-app.png",
             "caption": "Step 5: Pet Vet AI — Find a Vet Anywhere in the World",
             "desc": "Pet Vet AI uses your location to find nearby veterinarians and lets AI help you assess your pet's symptoms. Built with AI, deployed on Railway. Notice the polished design — this is what AI-assisted development looks like in 2025."},

            {"action": "navigate", "url": "https://jay-portfolio-production.up.railway.app",
             "caption": "Step 6: The Full Portfolio Dashboard",
             "desc": "The dashboard that connects all of Jay's apps."},
            {"action": "screenshot", "filename": "06-ecdash-portfolio.png",
             "caption": "Step 6: Your Instructor's App Network — 14 Live Apps",
             "desc": "This is what the end of the journey looks like. Fourteen live apps, all connected, all monitored, all built using AI. By the end of this course you'll have your first one. Let's get started."},
        ]
    },

    "1-2": {
        "title": "Lesson 1.2 — Your Business Automation Map",
        "subtitle": "Identify the #1 thing in your business that eats your time — and map how AI fixes it",
        "steps": [
            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app",
             "caption": "Example: Sweet Spot Cakes Before the App",
             "desc": "Let's walk through a real example of how a business problem becomes an app."},
            {"action": "screenshot", "filename": "01-sweet-spot-homepage.png",
             "caption": "Sweet Spot Cakes — A Real Business Problem Solved",
             "desc": "Before this app, the owner handled every order by phone and text message. Customers called at all hours. Orders got lost. Payment was cash or Venmo. Sound familiar? This app solved every one of those problems. Here's how we mapped it."},

            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app/order",
             "caption": "The Order Form — Old Problem, New Solution",
             "desc": "What used to be a phone call is now a structured form."},
            {"action": "screenshot", "filename": "02-order-form.png",
             "caption": "The Order Form — Customers Fill It Out Themselves",
             "desc": "Instead of taking orders by phone, customers fill this out online — any time, 24/7. Cake type, size, flavors, pickup date, special instructions — all captured in one place. No more missed calls. No more lost orders. The business owner checks their dashboard in the morning and sees every order."},

            {"action": "navigate", "url": "https://contractor-pro-ai-production.up.railway.app",
             "caption": "Another Example: Contractor Pro",
             "desc": "Same pattern for a service business."},
            {"action": "screenshot", "filename": "03-contractor-problem-solved.png",
             "caption": "Contractor Pro — Job Requests Without Phone Tag",
             "desc": "Contractors spend hours playing phone tag with potential clients. This app captures job requests, collects photos, generates quotes, and tracks jobs — all online. The automation map was simple: Customer contacts you → instead of a call, they fill a form → the AI drafts a quote → you approve it → it goes out automatically."},

            {"action": "navigate", "url": "https://ai.widget.alexanderai.site",
             "caption": "The AI Layer — Adding an Agent On Top",
             "desc": "Every app can have an AI agent added to it."},
            {"action": "screenshot", "filename": "04-ai-layer.png",
             "caption": "The AI Layer — Your Agent Works When You Don't",
             "desc": "Once your app is live, you add an AI agent on top of it. The agent answers questions, collects information, and hands off to the app — 24 hours a day, 7 days a week. Your job is to check in on what's happening, not to be the first line of contact for every customer."},
        ]
    },

    # =========================================================================
    # MODULE 2 — YOUR FIRST AI AGENT
    # =========================================================================

    "2-1": {
        "title": "Lesson 2.1 — Setting Up Your OpenRouter Account",
        "subtitle": "Get your AI API key in under 5 minutes — this is the key to everything",
        "steps": [
            {"action": "navigate", "url": "https://openrouter.ai",
             "caption": "Step 1: Go to OpenRouter.ai",
             "desc": "OpenRouter is the gateway to every major AI model — GPT-4, Claude, Gemini, and more."},
            {"action": "screenshot", "filename": "01-openrouter-home.png",
             "caption": "Step 1: OpenRouter Homepage",
             "desc": "OpenRouter is the service that powers your AI agents. Think of it as the electricity for your agents — without it, they don't run. The good news: getting set up is free and takes about 3 minutes. Click 'Sign In' in the top right."},

            {"action": "navigate", "url": "https://openrouter.ai/sign-in",
             "caption": "Step 2: Create Your Account",
             "desc": "Sign up for OpenRouter."},
            {"action": "screenshot", "filename": "02-openrouter-signin.png",
             "caption": "Step 2: Sign Up Page",
             "desc": "Click 'Sign Up' and create your account. You can use Google, GitHub, or your email. Once signed in, you'll be taken to your dashboard. We need one thing from here: your API key."},

            {"action": "navigate", "url": "https://openrouter.ai/keys",
             "caption": "Step 3: Get Your API Key",
             "desc": "Navigate to the API keys section."},
            {"action": "screenshot", "filename": "03-openrouter-keys.png",
             "caption": "Step 3: The API Keys Page",
             "desc": "This is the API Keys page. Click '+ Create Key'. Give it a name like 'My First Agent' and click Create. You'll see a long string starting with sk-or-v1-... — that's your key. COPY IT NOW and save it somewhere safe (a notes app or password manager). You only see it once."},

            {"action": "navigate", "url": "https://openrouter.ai/models",
             "caption": "Step 4: Browse the Available Models",
             "desc": "See which AI models you can use with your key."},
            {"action": "screenshot", "filename": "04-openrouter-models.png",
             "caption": "Step 4: All the AI Models Available to You",
             "desc": "With your OpenRouter key, you have access to ALL of these models. GPT-4o, Claude 3.5, Gemini, Llama, Mistral — everything. Many have free tiers. We'll start with GPT-4o Mini for your agent — it's fast, cheap, and excellent for customer conversations. You can switch models any time without changing your agent's code."},

            {"action": "navigate", "url": BASE_URL,
             "caption": "Step 5: Back to Agent Widget — You're Ready",
             "desc": "With your API key in hand, you're ready to create your first agent."},
            {"action": "screenshot", "filename": "05-ready-to-build.png",
             "caption": "Step 5: You Have Everything You Need",
             "desc": "You now have: (1) an OpenRouter account, (2) an API key copied and saved, (3) access to every major AI model. Head to the Agent Widget and let's build your first agent in the next lesson."},
        ]
    },

    "2-2": {
        "title": "Lesson 2.2 — Writing Your System Prompt",
        "subtitle": "The most important skill: how to tell your agent exactly who it is and what to do",
        "steps": [
            {"action": "navigate", "url": BASE_URL,
             "caption": "Step 1: Open the Agent Widget",
             "desc": "Navigate to the platform where we'll build."},
            {"action": "screenshot", "filename": "01-intro.png",
             "caption": "What Is a System Prompt?",
             "desc": "Before we open the form, understand this: the system prompt is the single most important thing you'll write for your AI agent. It determines everything — how it sounds, what it says, what it refuses to say, and how helpful it is. A bad system prompt = a frustrating bot. A great system prompt = a superstar employee who works 24/7."},

            {"action": "navigate", "url": BASE_URL + "/agent/new",
             "caption": "Step 2: Open the New Agent Form",
             "desc": "Navigate to the agent creation form."},
            {"action": "screenshot", "filename": "02-system-prompt-field.png",
             "caption": "Step 2: The System Prompt Field",
             "desc": "This is the System Prompt field — the big text area in the middle of the form. It's the secret instruction that shapes everything your agent says. The customer never sees it. Only the agent does. It reads this before every single conversation."},

            {"action": "fill", "selector": "textarea[name='system_prompt']",
             "value": (
                 "You are Alex, the friendly AI assistant for Liberty Emporium.\n\n"
                 "YOUR JOB:\n"
                 "- Welcome customers warmly when they arrive\n"
                 "- Answer questions about our products, hours, and policies\n"
                 "- Help customers track orders if they provide their order number\n"
                 "- Collect contact info from customers who want a callback\n\n"
                 "TONE: Friendly, warm, professional. Not robotic. Like talking to a helpful person.\n\n"
                 "RULES:\n"
                 "- Never invent prices or policies — say 'Let me have our team confirm that'\n"
                 "- If a customer is angry, stay calm and offer to escalate to a human\n"
                 "- Keep responses under 3 sentences when possible\n"
                 "- Always end with 'Is there anything else I can help you with today?'"
             ),
             "caption": "Step 3: Filling In a Real System Prompt",
             "desc": "Let's fill in a real system prompt together. Notice the structure: WHO (Alex, the assistant for Liberty Emporium), JOB (what it does), TONE (how it sounds), RULES (what it never does). This template works for any business — just replace the name and details with yours."},
            {"action": "screenshot", "filename": "03-prompt-filled.png",
             "caption": "Step 3: A Complete System Prompt",
             "desc": "This is a complete system prompt. Notice it covers four things: Identity (who the agent is), Job (what it does), Tone (how it speaks), Rules (what it won't do). That four-part structure is all you need for 90% of business agents. Copy this template and fill in your business details."},

            {"action": "navigate", "url": "https://chat.openai.com",
             "caption": "Step 4: Test Your Prompt With ChatGPT First",
             "desc": "Before building, test your system prompt in ChatGPT."},
            {"action": "screenshot", "filename": "04-test-with-chatgpt.png",
             "caption": "Step 4: Pro Tip — Test Your Prompt in ChatGPT First",
             "desc": "Here's a pro tip: before putting your system prompt into the Agent Widget, test it in ChatGPT first. Paste your prompt as the first message, then pretend to be a customer. Ask it tough questions. See how it responds. Refine it until it sounds exactly right. This saves you time and makes your live agent much better from day one."},

            {"action": "navigate", "url": BASE_URL + "/agent/new",
             "caption": "Step 5: Back to Agent Widget — Ready to Build",
             "desc": "With your tested system prompt, go back and build."},
            {"action": "screenshot", "filename": "05-back-to-build.png",
             "caption": "Step 5: You Know How to Write a System Prompt",
             "desc": "You now know the most important skill in AI agent building: how to write a system prompt that makes your agent sound exactly right for your business. In the next lesson, we deploy it live. Let's go."},
        ]
    },

    "2-3": {
        "title": "Lesson 2.3 — Deploying Your Agent (Live in 20 Minutes)",
        "subtitle": "Watch every step: create an agent, configure it, and get a live URL",
        "steps": [

            {"action": "navigate", "url": BASE_URL,
             "caption": "Step 1: Go to the AI Agent Widget platform",
             "desc": "This is where you create and manage your AI agents."},
            {"action": "screenshot", "filename": "01-homepage.png",
             "caption": "Step 1: The AI Agent Widget Homepage",
             "desc": "This is the homepage. Notice it says 'Add an AI Agent to Any Website in 60 Seconds' — that's exactly what we're going to do. Click 'Login' in the top right to get started."},

            {"action": "navigate", "url": BASE_URL + "/login",
             "caption": "Step 2: Go to the Login Page",
             "desc": "Navigate to the login page."},
            {"action": "screenshot", "filename": "02-login-page.png",
             "caption": "Step 2: The Login Page",
             "desc": "Enter your email and password. Click Sign In to go to your dashboard."},
            {"action": "fill", "selector": "input[name='email']",
             "value": "course.student@alexanderai.site",
             "caption": "Step 3: Enter your email", "desc": "Type your email address."},
            {"action": "fill", "selector": "input[name='password']",
             "value": "CourseDemo2026!",
             "caption": "Step 4: Enter your password", "desc": "Type your password."},
            {"action": "screenshot", "filename": "03-login-filled.png",
             "caption": "Step 4: Login details filled in",
             "desc": "Both fields are filled in. Click Sign In."},
            {"action": "click", "selector": "button[type='submit']",
             "caption": "Step 5: Click Sign In", "desc": "Clicking Sign In."},

            {"action": "screenshot", "filename": "04-dashboard.png",
             "caption": "Step 5: Your Dashboard",
             "desc": "Welcome to your dashboard! This is where all your agents live. Click 'New Agent' to get started."},

            {"action": "navigate", "url": BASE_URL + "/agent/new",
             "caption": "Step 6: Open the New Agent Form",
             "desc": "Navigate to the create agent form."},
            {"action": "screenshot", "filename": "05-new-agent-form.png",
             "caption": "Step 6: The Agent Creation Form",
             "desc": "This form configures everything about your agent: Name, Tagline, Brand Color, Avatar Emoji, System Prompt, AI Model, and API Key. We'll fill each one in together."},

            {"action": "fill", "selector": "input[name='name']", "value": "Aria",
             "caption": "Step 7: Name your agent", "desc": "Give your agent a name. We're using 'Aria'."},
            {"action": "fill", "selector": "input[name='tagline']",
             "value": "Here to help you 24/7",
             "caption": "Step 8: Add a tagline", "desc": "A short welcome line for the chat header."},
            {"action": "screenshot", "filename": "06-name-tagline-filled.png",
             "caption": "Step 8: Name and Tagline filled in",
             "desc": "Your agent has a name and tagline. Now scroll down to the System Prompt."},

            {"action": "fill", "selector": "textarea[name='system_prompt']",
             "value": (
                 "You are Aria, the friendly AI assistant for Demo Business.\n\n"
                 "YOUR JOB:\n"
                 "- Welcome every customer warmly\n"
                 "- Answer questions about our products and services\n"
                 "- Collect the customer's name and phone number if they need follow-up\n"
                 "- Be helpful, concise, and professional\n\n"
                 "YOUR RULES:\n"
                 "- Never make up prices — say 'I will have someone confirm that for you'\n"
                 "- If you don't know something, say 'Let me have our team follow up'\n"
                 "- Keep responses short and easy to read\n"
                 "- Always end with an offer to help further"
             ),
             "caption": "Step 9: Write your System Prompt",
             "desc": "The System Prompt is your agent's job description — the most important field. It tells the AI who it is, what it does, and how to behave."},
            {"action": "screenshot", "filename": "07-system-prompt-filled.png",
             "caption": "Step 9: System Prompt entered",
             "desc": "Notice the structure: WHO (Aria), WHAT (welcome, answer, collect info), RULES (no made-up prices, keep it short). This works for any business."},

            {"action": "click", "selector": "#emojiTrigger",
             "caption": "Step 10: Open the Emoji Picker", "desc": "Click the emoji picker button."},
            {"action": "screenshot", "filename": "08-emoji-picker-open.png",
             "caption": "Step 10: Choose Your Avatar Emoji",
             "desc": "Browse categories and click any emoji to select it. Pick something that fits your brand."},
            {"action": "click", "selector": "#emojiGrid button:first-child",
             "caption": "Step 10b: Select an emoji", "desc": "Click any emoji to select it."},

            {"action": "scroll", "y": 600, "caption": "Scrolling to AI Model section", "desc": ""},
            {"action": "screenshot", "filename": "09-model-selection.png",
             "caption": "Step 11: Choose Your AI Model",
             "desc": "GPT-4o Mini is the best starting point — fast, affordable, great for customer conversations."},

            {"action": "scroll", "y": 400, "caption": "Scrolling to API Key", "desc": ""},
            {"action": "screenshot", "filename": "10-api-key-field.png",
             "caption": "Step 12: Enter Your OpenRouter API Key",
             "desc": "Paste the API key you got from openrouter.ai/keys. It's stored encrypted and never shared."},
            {"action": "fill", "selector": "input[name='api_key']",
             "value": "sk-or-v1-course-demo-illustration-key",
             "caption": "Step 12b: Paste your API key", "desc": "Paste your key here."},
            {"action": "screenshot", "filename": "11-api-key-entered.png",
             "caption": "Step 12: API Key entered",
             "desc": "The key shows as dots for security. Leave Allowed Origins as * for now."},

            {"action": "scroll", "y": 300, "caption": "Scrolling to Create Agent button", "desc": ""},
            {"action": "screenshot", "filename": "12-ready-to-create.png",
             "caption": "Step 13: Everything Set — Click Create Agent",
             "desc": "All fields filled. Click the purple 'Create Agent' button."},
            {"action": "click", "selector": "button[type='submit']",
             "caption": "Step 13: Clicking Create Agent...", "desc": "Submitting."},
            {"action": "wait", "seconds": 3, "caption": "Deploying...", "desc": ""},
            {"action": "screenshot", "filename": "13-agent-created.png",
             "caption": "Step 13: Agent Created!",
             "desc": "Your agent is live. You'll see the agent detail page with its configuration and a public chat link."},

            {"action": "navigate", "url": BASE_URL + "/dashboard",
             "caption": "Step 14: Back to Dashboard", "desc": ""},
            {"action": "screenshot", "filename": "14-dashboard-with-agent.png",
             "caption": "Step 14: Your Dashboard with Your First Agent",
             "desc": "Your agent lives on your dashboard. Click it to edit, view analytics, get the embed code, or share the public chat link."},
        ]
    },

    # =========================================================================
    # MODULE 3 — BUILDING YOUR FIRST APP
    # =========================================================================

    "3-3": {
        "title": "Lesson 3.3 — Using AI to Build Your App Skeleton",
        "subtitle": "You describe what you want. AI writes the code. You review and deploy.",
        "steps": [
            {"action": "navigate", "url": "https://github.com",
             "caption": "Step 1: Where the Code Will Live",
             "desc": "Before we build, a look at where everything ends up."},
            {"action": "screenshot", "filename": "01-github-overview.png",
             "caption": "Step 1: GitHub — Your Code's Home",
             "desc": "Everything we build gets saved to GitHub first, then deployed to Railway. GitHub = save button. Railway = publish button."},

            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app",
             "caption": "Step 2: The App We're Reverse-Engineering",
             "desc": "We'll use Sweet Spot Cakes as our blueprint."},
            {"action": "screenshot", "filename": "02-sweet-spot-reference.png",
             "caption": "Step 2: Sweet Spot Cakes — Your Blueprint",
             "desc": "Here's our reference app. Notice the structure: a homepage, an order form, a login for the owner, and an admin dashboard to see orders. That's the pattern. Every business app you build will follow this same structure — just with different fields and your brand colors."},

            {"action": "navigate", "url": "https://billy-floods.up.railway.app",
             "caption": "Step 3: Another Blueprint — FloodClaim Pro",
             "desc": "Different business, same pattern."},
            {"action": "screenshot", "filename": "03-floodclaim-reference.png",
             "caption": "Step 3: FloodClaim Pro — Same Pattern, Different Business",
             "desc": "Different business, same pattern: public landing page → user form → owner dashboard. Every app in this course follows this architecture because it works for every type of business. Once you understand this pattern, you can build anything."},

            {"action": "navigate", "url": "https://contractor-pro-ai-production.up.railway.app",
             "caption": "Step 4: One More — Contractor Pro",
             "desc": "Service business, same pattern."},
            {"action": "screenshot", "filename": "04-contractor-reference.png",
             "caption": "Step 4: Contractor Pro — The Pattern Works Everywhere",
             "desc": "Contracting business. Same pattern. This is the power of learning the architecture — once you see it, you can't unsee it. Now let's build your version with AI writing the code."},

            {"action": "navigate", "url": "https://claude.ai",
             "caption": "Step 5: Open Your AI Coding Tool",
             "desc": "Claude, ChatGPT, or KiloClaw — pick your AI assistant."},
            {"action": "screenshot", "filename": "05-ai-tool.png",
             "caption": "Step 5: Your AI Coding Partner",
             "desc": "Open your AI assistant — Claude.ai, ChatGPT, or your KiloClaw instance. This is where you describe your app in plain English and the AI writes the code. You don't need to know Python. You don't need to know Flask. You just need to describe what you want."},

            {"action": "navigate", "url": "https://jay-portfolio-production.up.railway.app",
             "caption": "Step 6: The Payoff — All Apps, One Dashboard",
             "desc": "Your app will join this network."},
            {"action": "screenshot", "filename": "06-portfolio-payoff.png",
             "caption": "Step 6: This Is What You're Building Toward",
             "desc": "Every app you build with this method ends up in a dashboard like this — monitored, connected, and working for your business 24/7. In the next lesson, we write the exact prompt to give your AI assistant and generate your app's code. The lesson after that, we deploy it live."},
        ]
    },

    "3-4": {
        "title": "Lesson 3.4 — Deploying Your App to Railway",
        "subtitle": "Go from local code to a live URL anyone in the world can visit",
        "steps": [
            {"action": "navigate", "url": "https://railway.com",
             "caption": "Step 1: Go to railway.com", "desc": "Railway hosts your app on the internet."},
            {"action": "screenshot", "filename": "01-railway-homepage.png",
             "caption": "Step 1: Railway Homepage",
             "desc": "Railway is where your app lives. Free to start — no credit card needed. Click 'Login' to get started."},

            {"action": "navigate", "url": "https://railway.com/login",
             "caption": "Step 2: Railway Login Page", "desc": "Sign in to Railway."},
            {"action": "screenshot", "filename": "02-railway-login.png",
             "caption": "Step 2: Railway Login Page",
             "desc": "Sign in with GitHub. This connects your code repository to Railway so deploying later is automatic."},

            {"action": "navigate", "url": "https://github.com",
             "caption": "Step 3: GitHub — Where Your Code Lives", "desc": ""},
            {"action": "screenshot", "filename": "03-github-homepage.png",
             "caption": "Step 3: GitHub Homepage",
             "desc": "GitHub is your code's home. Think of it like Google Drive for your app files. Sign up free at github.com if you haven't already."},

            {"action": "navigate", "url": "https://github.com/new",
             "caption": "Step 4: Create a New Repo", "desc": ""},
            {"action": "screenshot", "filename": "04-github-new-repo.png",
             "caption": "Step 4: Create a New GitHub Repository",
             "desc": "Create a new repo: name it after your app (no spaces), set it Private, click 'Create repository'."},

            {"action": "navigate", "url": "https://github.com",
             "caption": "Step 5: Push Your Code", "desc": ""},
            {"action": "screenshot", "filename": "05-github-push-commands.png",
             "caption": "Step 5: Push Your Code to GitHub",
             "desc": "After creating the repo, GitHub shows you the commands. Run these three in your terminal from your app folder. I'll walk you through each one."},

            {"action": "navigate", "url": "https://railway.com",
             "caption": "Step 6: Back to Railway — New Project", "desc": ""},
            {"action": "screenshot", "filename": "06-railway-new-project.png",
             "caption": "Step 6: Railway Dashboard — Create New Project",
             "desc": "In Railway, click '+ New Project'. Railway connects to GitHub and pulls your code automatically."},

            {"action": "navigate", "url": "https://railway.com/new",
             "caption": "Step 7: Deploy from GitHub Repo", "desc": ""},
            {"action": "screenshot", "filename": "07-railway-deploy-options.png",
             "caption": "Step 7: Choose Deploy from GitHub Repo",
             "desc": "Click 'Deploy from GitHub Repo'. Railway asks permission to access GitHub the first time — click Authorize. Then pick your repo from the list."},

            {"action": "navigate", "url": "https://railway.com",
             "caption": "Step 8: Add Environment Variables", "desc": ""},
            {"action": "screenshot", "filename": "08-railway-env-vars.png",
             "caption": "Step 8: Setting Environment Variables",
             "desc": "After connecting, click Variables in your Railway service. Add at minimum: SECRET_KEY (any long random text) and PORT set to 5000. These are private — never in your code."},

            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app",
             "caption": "Step 9: This Is What Success Looks Like", "desc": ""},
            {"action": "screenshot", "filename": "09-live-app-example.png",
             "caption": "Step 9: A Real App Deployed on Railway",
             "desc": "Sweet Spot Custom Cakes — built and deployed using this exact process. Real URL, 24/7, built by a business owner with AI. Your app will look just like this."},

            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app/health",
             "caption": "Step 10: Check the /health Endpoint", "desc": ""},
            {"action": "screenshot", "filename": "10-health-check.png",
             "caption": "Step 10: The /health Endpoint — Your App's Pulse",
             "desc": "Every app includes a /health URL. It returns status: ok when your deploy succeeded. If it fails, Railway shows the error in the build log so you can fix it."},

            {"action": "navigate", "url": "https://contractor-pro-ai-production.up.railway.app",
             "caption": "Step 11: Another Live App — Contractor Pro", "desc": ""},
            {"action": "screenshot", "filename": "11-contractor-app.png",
             "caption": "Step 11: Contractor Pro AI — Also on Railway",
             "desc": "Another example. Notice the URL: contractor-pro-ai-production.up.railway.app. Every app you build gets a URL like this. Real. Live. Shareable."},

            {"action": "navigate", "url": "https://railway.com",
             "caption": "Step 12: Your Update Workflow", "desc": ""},
            {"action": "screenshot", "filename": "12-railway-redeploy.png",
             "caption": "Step 12: Updating Is Automatic",
             "desc": "Once deployed, updating is easy: make a change → push to GitHub → Railway redeploys automatically. No server management. No downtime. Your workflow: code it, push it, it's live."},
        ]
    },

    # =========================================================================
    # MODULE 4 — AUTOMATION & NOTIFICATIONS
    # =========================================================================

    "4-1": {
        "title": "Lesson 4.1 — Customer Notifications: Text & Email",
        "subtitle": "Automatically notify customers when their order is ready — and remind them to pay",
        "steps": [
            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app",
             "caption": "Step 1: The Business Problem We're Solving",
             "desc": "Sweet Spot Cakes — orders come in, but customers need to know their status."},
            {"action": "screenshot", "filename": "01-sweet-spot-orders.png",
             "caption": "Step 1: The Problem — Manual Follow-Up Is Exhausting",
             "desc": "Right now, when a cake order comes in and is ready, the business owner has to text or call the customer manually. Every. Single. Time. We're going to automate that. When an order status changes to 'Ready', the customer gets an automatic text message AND email. Zero manual work."},

            {"action": "navigate", "url": "https://www.twilio.com",
             "caption": "Step 2: Twilio — Your Text Message Engine",
             "desc": "Twilio is the service that sends text messages from your app."},
            {"action": "screenshot", "filename": "02-twilio-home.png",
             "caption": "Step 2: Twilio — Text Messaging for Your App",
             "desc": "Twilio is what sends text messages from your app to your customers. It's used by Uber, Airbnb, and millions of small businesses. Free trial available — no credit card needed to start. Sign up, and Twilio gives you a phone number and $15 in free credits. That's 500+ free text messages to test with."},

            {"action": "navigate", "url": "https://www.twilio.com/try-twilio",
             "caption": "Step 3: Sign Up for Twilio",
             "desc": "Create your Twilio account."},
            {"action": "screenshot", "filename": "03-twilio-signup.png",
             "caption": "Step 3: Sign Up for a Free Twilio Account",
             "desc": "Create your free account. Twilio will give you: (1) A trial phone number to send texts from, (2) An Account SID (your username), (3) An Auth Token (your password). Save all three. We'll add them to your app's environment variables on Railway."},

            {"action": "navigate", "url": "https://sendgrid.com",
             "caption": "Step 4: SendGrid — Your Email Engine",
             "desc": "SendGrid handles transactional emails from your app."},
            {"action": "screenshot", "filename": "04-sendgrid-home.png",
             "caption": "Step 4: SendGrid — Email Notifications From Your App",
             "desc": "SendGrid sends emails from your app to your customers. It's free for up to 100 emails/day — more than enough for most small businesses to start. You'll set up one API key and it handles all your order confirmation and notification emails automatically."},

            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app",
             "caption": "Step 5: Back to the App — What We're Adding",
             "desc": "Let's see the app with notifications in mind."},
            {"action": "screenshot", "filename": "05-notification-flow.png",
             "caption": "Step 5: The Notification Flow We're Building",
             "desc": "Here's what we're building: (1) Customer places order → they get a confirmation email automatically, (2) Owner marks order as 'Ready' → customer gets a text message + email, (3) Order hasn't been paid? → reminder text goes out automatically after 24 hours. Three automations. Zero manual work. Let's build it."},

            {"action": "navigate", "url": "https://contractor-pro-ai-production.up.railway.app",
             "caption": "Step 6: Same Pattern on Contractor Pro",
             "desc": "This notification pattern works on any app."},
            {"action": "screenshot", "filename": "06-contractor-notifications.png",
             "caption": "Step 6: Notifications Work on Every App You Build",
             "desc": "This same pattern works on every app in your portfolio. Contractor Pro: job received → send text, quote approved → send email. Drop Shipping: order shipped → send tracking text. Any app with a status change or a form submission can trigger a notification. Learn it once, use it everywhere."},
        ]
    },

    # =========================================================================
    # MODULE 5 — BUSINESS PLAYBOOKS
    # =========================================================================

    "5-1": {
        "title": "Lesson 5.1 — Pick Your Business Playbook",
        "subtitle": "See exactly what to build for your type of business — with real examples already live",
        "steps": [
            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app",
             "caption": "Playbook A: Food & Bakery Businesses",
             "desc": "If you run a food business, here's your playbook."},
            {"action": "screenshot", "filename": "01-playbook-food.png",
             "caption": "Playbook A: Food & Bakery — What to Build",
             "desc": "If you run a food business (bakery, catering, meal prep, restaurant), this is your stack: (1) Online order form with pickup date and special instructions, (2) AI agent on your website to answer menu questions 24/7, (3) Automated text when order is ready, (4) Dashboard to manage all orders in one place. Sweet Spot Cakes is the live proof of concept."},

            {"action": "navigate", "url": "https://contractor-pro-ai-production.up.railway.app",
             "caption": "Playbook B: Contractors & Service Businesses",
             "desc": "If you run a service business, here's your stack."},
            {"action": "screenshot", "filename": "02-playbook-contractor.png",
             "caption": "Playbook B: Contractors & Service Businesses",
             "desc": "If you run a contracting, cleaning, landscaping, or other service business: (1) Online job request form with photo upload, (2) AI agent that answers questions and collects lead info, (3) Automated quote generation, (4) Customer notification when job is scheduled and when it's complete. Contractor Pro is the live example."},

            {"action": "navigate", "url": "https://billy-floods.up.railway.app",
             "caption": "Playbook C: Insurance & Claims",
             "desc": "If you work in insurance or legal, here's your stack."},
            {"action": "screenshot", "filename": "03-playbook-claims.png",
             "caption": "Playbook C: Insurance, Legal & Documentation",
             "desc": "If you work in insurance, legal, or any field where you collect documentation from clients: (1) Guided intake form that walks clients through exactly what to submit, (2) AI agent that explains the process and answers questions, (3) Document checklist with upload functionality, (4) Case tracking dashboard. FloodClaim Pro is the live example."},

            {"action": "navigate", "url": "https://pet-vet-ai-production.up.railway.app",
             "caption": "Playbook D: Health & Wellness",
             "desc": "If you're in health, wellness, or pet care."},
            {"action": "screenshot", "filename": "04-playbook-health.png",
             "caption": "Playbook D: Health, Wellness & Pet Care",
             "desc": "If you run a wellness business, veterinary practice, or health service: (1) AI agent that does initial intake and symptom assessment, (2) Appointment request form, (3) Location-based service finder, (4) Follow-up reminders. Pet Vet AI is the live proof — it finds vets near you and uses AI to help assess your pet's needs."},

            {"action": "navigate", "url": "https://shop.alexanderai.site",
             "caption": "Playbook E: E-Commerce & Drop Shipping",
             "desc": "If you sell products online."},
            {"action": "screenshot", "filename": "05-playbook-ecommerce.png",
             "caption": "Playbook E: E-Commerce & Drop Shipping",
             "desc": "If you sell products online: (1) Product catalog with one-click import from suppliers, (2) AI agent that recommends products based on customer needs, (3) Automated order fulfillment via CJ Dropshipping or similar, (4) Order tracking with automated customer notifications. The Drop Shipping app is the live example."},

            {"action": "navigate", "url": "https://jay-portfolio-production.up.railway.app",
             "caption": "Your Playbook + AI Agent + Notifications = Done",
             "desc": "Every playbook follows the same architecture."},
            {"action": "screenshot", "filename": "06-all-playbooks.png",
             "caption": "Every Playbook Lives in the Same Dashboard",
             "desc": "Regardless of which playbook you follow, the end result is the same: your app is live, monitored, and showing up in a dashboard like this. By the end of this module you'll have identified exactly which playbook fits your business and know precisely what to build next. The architecture is the same. The details are yours."},
        ]
    },

}
