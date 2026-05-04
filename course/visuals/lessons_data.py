"""
Lesson step definitions for the Course Visual Capture Engine.
Each lesson has a title, subtitle, and a list of steps.
Step actions: navigate, screenshot, click, fill, scroll, wait
"""

BASE_URL = "https://ai.widget.alexanderai.site"

LESSONS = {

    # ─────────────────────────────────────────────────────────────────────────
    # LESSON 2-3: Deploy Your First Agent
    # ─────────────────────────────────────────────────────────────────────────
    "2-3": {
        "title": "Lesson 2.3 — Deploying Your Agent (Live in 20 Minutes)",
        "subtitle": "Watch every step: create an agent, configure it, and get a live URL",
        "steps": [

            # Step 1 — Homepage
            {"action": "navigate", "url": BASE_URL,
             "caption": "Step 1: Go to the AI Agent Widget platform",
             "desc": "This is where you create and manage your AI agents."},
            {"action": "screenshot", "filename": "01-homepage.png",
             "caption": "Step 1: The AI Agent Widget Homepage",
             "desc": "This is the homepage. Notice it says 'Add an AI Agent to Any Website in 60 Seconds' — that's exactly what we're going to do. Click 'Login' in the top right to get started."},

            # Step 2 — Login
            {"action": "navigate", "url": BASE_URL + "/login",
             "caption": "Step 2: Go to the Login Page",
             "desc": "Navigate to the login page."},
            {"action": "screenshot", "filename": "02-login-page.png",
             "caption": "Step 2: The Login Page",
             "desc": "Enter the email and password your instructor set up for you. For course participants, accounts are pre-created. Type your email in the top field and your password below it."},
            {"action": "fill", "selector": "input[name='email']",
             "value": "course.student@alexanderai.site",
             "caption": "Step 3: Enter your email",
             "desc": "Type your email address."},
            {"action": "fill", "selector": "input[name='password']",
             "value": "CourseDemo2026!",
             "caption": "Step 4: Enter your password",
             "desc": "Type your password."},
            {"action": "screenshot", "filename": "03-login-filled.png",
             "caption": "Step 4: Login details filled in",
             "desc": "Both fields are filled in. Now click Sign In to go to your dashboard."},
            {"action": "click", "selector": "button[type='submit']",
             "caption": "Step 5: Click Sign In",
             "desc": "Click the button. You'll be taken to your dashboard."},

            # Step 3 — Dashboard
            {"action": "screenshot", "filename": "04-dashboard.png",
             "caption": "Step 5: Your Dashboard",
             "desc": "Welcome to your dashboard! This is where all your agents live. It's empty right now — that's fine. By the end of this lesson, your first agent will appear here. Click 'New Agent' to get started."},

            # Step 4 — New Agent Form
            {"action": "navigate", "url": BASE_URL + "/agent/new",
             "caption": "Step 6: Open the New Agent Form",
             "desc": "Navigate to the create agent form."},
            {"action": "screenshot", "filename": "05-new-agent-form.png",
             "caption": "Step 6: The Agent Creation Form",
             "desc": "This form is where you configure everything about your agent. Take a moment to look at what's here: Agent Name, Tagline, Brand Color, Avatar Emoji, System Prompt, AI Model, and API Key. We'll fill each one in together."},

            # Step 5 — Fill name & tagline
            {"action": "fill", "selector": "input[name='name']",
             "value": "Aria",
             "caption": "Step 7: Name your agent",
             "desc": "Give your agent a name. We're using 'Aria' for this demo. Yours should match your brand — 'Max', 'Sophie', 'Alex', or just 'Assistant'. This name appears in the chat header your customers see."},
            {"action": "fill", "selector": "input[name='tagline']",
             "value": "Here to help you 24/7",
             "caption": "Step 8: Add a tagline",
             "desc": "The tagline is a short welcome line that appears under your agent's name. Keep it warm — 'Here to help!', 'Ask me anything', 'Your 24/7 assistant'."},
            {"action": "screenshot", "filename": "06-name-tagline-filled.png",
             "caption": "Step 8: Name and Tagline filled in",
             "desc": "Good — your agent has a name and tagline. Now the most important part: the System Prompt. It's the text box below. Scroll down to see it."},

            # Step 6 — System prompt
            {"action": "fill", "selector": "textarea[name='system_prompt']",
             "value": (
                 "You are Aria, the friendly AI assistant for Demo Business.\n\n"
                 "YOUR JOB:\n"
                 "- Welcome every customer warmly\n"
                 "- Answer questions about our products and services\n"
                 "- Collect the customer's name and phone number if they need follow-up\n"
                 "- Be helpful, concise, and professional\n\n"
                 "YOUR RULES:\n"
                 "- Never make up prices — say 'I'll have someone confirm that for you'\n"
                 "- If you don't know something, say 'Let me have our team follow up with you'\n"
                 "- Keep responses short and easy to read\n"
                 "- Always end with an offer to help further"
             ),
             "caption": "Step 9: Write your System Prompt",
             "desc": "The System Prompt is your agent's job description — the most important field in this form. It tells the AI who it is, what it does, and how to behave. Think of it like writing an employee handbook for a new hire on their first day."},
            {"action": "screenshot", "filename": "07-system-prompt-filled.png",
             "caption": "Step 9: System Prompt entered",
             "desc": "Notice the structure: WHO the agent is (Aria), WHAT it does (welcome, answer, collect info), and the RULES it follows (no made-up prices, keep it short). This structure works for any business — just swap in your details."},

            # Step 7 — Emoji picker
            {"action": "click", "selector": "#emojiTrigger",
             "caption": "Step 10: Open the Emoji Picker",
             "desc": "Click the Avatar Emoji button to open the picker."},
            {"action": "screenshot", "filename": "08-emoji-picker-open.png",
             "caption": "Step 10: Choose Your Avatar Emoji",
             "desc": "The emoji picker shows categories across the top — Faces, People, Animals, Food, and more. Click any emoji to select it. Pick something that fits your brand: robot for tech, flower for a spa, cake for a bakery, house for real estate. This emoji appears in the chat widget header."},
            {"action": "click", "selector": "#emojiGrid button:first-child",
             "caption": "Step 10b: Select an emoji",
             "desc": "Click any emoji to select it. The picker closes and your choice is saved."},

            # Step 8 — Scroll to model
            {"action": "scroll", "y": 600,
             "caption": "Scrolling to AI Model section",
             "desc": "Scroll down to the AI Model selection."},
            {"action": "screenshot", "filename": "09-model-selection.png",
             "caption": "Step 11: Choose Your AI Model",
             "desc": "Here you choose which AI brain powers your agent. GPT-4o Mini is the best starting point for most businesses — it's fast, affordable, and great at customer conversations. You can always switch to a more powerful model like Claude or GPT-4o later as your needs grow."},

            # Step 9 — API Key
            {"action": "scroll", "y": 400,
             "caption": "Scrolling to API Key",
             "desc": "Scroll to the API & Security section."},
            {"action": "screenshot", "filename": "10-api-key-field.png",
             "caption": "Step 12: Enter Your OpenRouter API Key",
             "desc": (
                 "This is the only field requiring setup outside this app. "
                 "Your OpenRouter API key connects your agent to the AI models. "
                 "Getting one is free and takes 2 minutes: "
                 "(1) Go to openrouter.ai/keys, "
                 "(2) Sign up with Google or email, "
                 "(3) Click 'Create Key', "
                 "(4) Copy it and paste it here. "
                 "Your key is stored encrypted and never shared."
             )},
            {"action": "fill", "selector": "input[name='api_key']",
             "value": "sk-or-v1-course-demo-illustration-key",
             "caption": "Step 12b: Paste your API key",
             "desc": "Paste your OpenRouter API key. It will show as dots once you click away — that's correct, it's stored securely."},
            {"action": "screenshot", "filename": "11-api-key-entered.png",
             "caption": "Step 12: API Key entered",
             "desc": "The key shows as dots for security. The Allowed Origins field is set to * by default — leave it as-is. This means your agent works on any website. You can lock it to your specific domain later once you know where you're embedding it."},

            # Step 10 — Submit
            {"action": "scroll", "y": 300,
             "caption": "Scrolling to Create Agent button",
             "desc": "Scroll to the bottom of the form."},
            {"action": "screenshot", "filename": "12-ready-to-create.png",
             "caption": "Step 13: Everything Set — Click Create Agent",
             "desc": "All fields are filled: Name, Tagline, System Prompt, Emoji, AI Model, and API Key. One click and your agent goes live on the internet. Click the purple 'Create Agent' button."},
            {"action": "click", "selector": "button[type='submit']",
             "caption": "Step 13: Clicking Create Agent...",
             "desc": "Submitting the form now."},
            {"action": "wait", "seconds": 3,
             "caption": "Deploying...",
             "desc": "Give it a moment to save."},
            {"action": "screenshot", "filename": "13-agent-created.png",
             "caption": "Step 13: Agent Created",
             "desc": "Your agent has been created. You'll see the agent detail page with its configuration and a public chat link."},

            # Step 11 — Back to dashboard
            {"action": "navigate", "url": BASE_URL + "/dashboard",
             "caption": "Step 14: Back to Dashboard",
             "desc": "Navigate back to the dashboard."},
            {"action": "screenshot", "filename": "14-dashboard-with-agent.png",
             "caption": "Step 14: Your Dashboard with Your First Agent",
             "desc": "Your agent now lives on your dashboard. You can click it to edit, view analytics, get the embed code, or share the public chat link. Every agent you build in this course will appear here."},
        ]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # LESSON 3-4: Deploy to Railway
    # ─────────────────────────────────────────────────────────────────────────
    "3-4": {
        "title": "Lesson 3.4 — Deploying Your App to Railway",
        "subtitle": "Go from local code to a live URL anyone in the world can visit",
        "steps": [

            # Step 1 — Railway homepage
            {"action": "navigate", "url": "https://railway.com",
             "caption": "Step 1: Go to railway.com",
             "desc": "Railway is the hosting platform where your app will live on the internet. It's free to start — no credit card needed for the free tier."},
            {"action": "screenshot", "filename": "01-railway-homepage.png",
             "caption": "Step 1: Railway Homepage",
             "desc": "This is Railway. It's where thousands of developers deploy their apps. Notice the tagline — 'Deploy apps globally, instantly'. That's exactly what we're doing. Click 'Login' in the top right to get started."},

            # Step 2 — Login page
            {"action": "navigate", "url": "https://railway.com/login",
             "caption": "Step 2: Go to Login",
             "desc": "Navigate to the Railway login page."},
            {"action": "screenshot", "filename": "02-railway-login.png",
             "caption": "Step 2: Railway Login Page",
             "desc": "Railway lets you sign in with GitHub, Google, or email. We strongly recommend GitHub — it connects your code repository to Railway automatically, which is how you deploy later. If you don't have GitHub yet, we'll set that up first."},

            # Step 3 — GitHub (for context)
            {"action": "navigate", "url": "https://github.com",
             "caption": "Step 3: GitHub — Where Your Code Lives",
             "desc": "GitHub is where your code is stored before Railway deploys it."},
            {"action": "screenshot", "filename": "03-github-homepage.png",
             "caption": "Step 3: GitHub Homepage",
             "desc": "GitHub is your code's home. Think of it like Google Drive for your app's files. Every time you save (push) your code to GitHub, Railway can pick it up and redeploy automatically. Sign up at github.com if you haven't — it's free."},

            # Step 4 — New repo on GitHub
            {"action": "navigate", "url": "https://github.com/new",
             "caption": "Step 4: Create a New GitHub Repository",
             "desc": "Navigate to create a new repository on GitHub."},
            {"action": "screenshot", "filename": "04-github-new-repo.png",
             "caption": "Step 4: Create a New GitHub Repository",
             "desc": "This is where you create a new repository (a 'repo') — basically a folder in the cloud for your app's code. Fill in: (1) Repository name — use your app name, no spaces (e.g. my-cake-shop), (2) Set it to Private, (3) Leave everything else as-is. Then click 'Create repository'."},

            # Step 5 — Push code explanation
            {"action": "navigate", "url": "https://github.com",
             "caption": "Step 5: Push Your Code to GitHub",
             "desc": "After creating the repo, GitHub shows you the commands to push your code."},
            {"action": "screenshot", "filename": "05-github-push-commands.png",
             "caption": "Step 5: The Push Commands",
             "desc": "After creating your repo, GitHub shows you the exact commands to push your code. You'll run these three commands in your terminal from your app folder. Don't worry — I'll walk you through each one."},

            # Step 6 — Railway new project
            {"action": "navigate", "url": "https://railway.com",
             "caption": "Step 6: Back to Railway — Create New Project",
             "desc": "Navigate back to Railway to start a new project."},
            {"action": "screenshot", "filename": "06-railway-new-project.png",
             "caption": "Step 6: Railway Dashboard — New Project",
             "desc": "Once logged in to Railway, you'll see your dashboard. Click '+ New Project' to start deploying your app. Railway is about to connect to your GitHub and pull your code."},

            # Step 7 — Deploy from GitHub
            {"action": "navigate", "url": "https://railway.com/new",
             "caption": "Step 7: Deploy from GitHub Repo",
             "desc": "On the new project screen, Railway gives you several options."},
            {"action": "screenshot", "filename": "07-railway-deploy-options.png",
             "caption": "Step 7: Choose 'Deploy from GitHub Repo'",
             "desc": "Railway gives you several ways to start. Click 'Deploy from GitHub Repo'. Railway will ask permission to access your GitHub account the first time — click Authorize. Then you'll see a list of your repositories."},

            # Step 8 — Environment variables (diagram card — Railway requires login)
            {"action": "navigate", "url": "https://railway.com",
             "caption": "Step 8: Setting Environment Variables",
             "desc": "After connecting your GitHub repo, Railway starts your first deploy. Before it fully works, you need to add environment variables. In your Railway service: click Variables → Add Variable. You need at minimum: SECRET_KEY (paste any long random text — this is your app's security key) and PORT set to 5000. These are private and never visible in your code."},
            {"action": "screenshot", "filename": "08-railway-env-vars.png",
             "caption": "Step 8: Railway Login — Sign In With GitHub",
             "desc": "When you first go to railway.com/new, Railway asks you to log in. Click 'Continue with GitHub'. This grants Railway permission to read your repositories so it can deploy your code. You only do this once."},

            # Step 9 — Watching the deploy — show a real live app as proof
            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app",
             "caption": "Step 9: A Real Live App on Railway",
             "desc": "This is what success looks like."},
            {"action": "screenshot", "filename": "09-live-app-example.png",
             "caption": "Step 9: This is What Your Deployed App Looks Like",
             "desc": "This is Sweet Spot Custom Cakes — a real app built using this exact process and deployed on Railway. It has a real URL, runs 24/7, and was built using the same method you're learning right now. Your app will look just like this — with your business name, your colors, and your data."},

            # Step 10 — Health check on a real app
            {"action": "navigate", "url": "https://sweet-spot-cakes.up.railway.app/health",
             "caption": "Step 10: The Health Check Endpoint",
             "desc": "Every app we build includes a /health endpoint."},
            {"action": "screenshot", "filename": "10-health-check.png",
             "caption": "Step 10: The /health Endpoint — Your App's Pulse",
             "desc": "Every app you build includes a /health endpoint at yourapp.up.railway.app/health. It returns a simple JSON response: status: ok. Railway uses this to confirm your app started correctly. If it returns ok, your deploy succeeded. If it fails, Railway shows you the error in the build log so you can fix it."},

            # Step 11 — Another live app as extra proof
            {"action": "navigate", "url": "https://contractor-pro-ai-production.up.railway.app",
             "caption": "Step 11: Another Live App — Contractor Pro AI",
             "desc": "Every app in this course is already live on Railway."},
            {"action": "screenshot", "filename": "11-contractor-app.png",
             "caption": "Step 11: Contractor Pro AI — Also Live on Railway",
             "desc": "Here's another example: Contractor Pro AI — a full job request and quoting app for contractors, built and deployed on Railway using this same process. Notice the URL: contractor-pro-ai-production.up.railway.app. Every app you build in this course gets a URL like this. Real. Live. Shareable."},

            # Step 12 — The redeploy workflow
            {"action": "navigate", "url": "https://railway.com",
             "caption": "Step 12: The Update Workflow",
             "desc": "Once deployed, updating is effortless."},
            {"action": "screenshot", "filename": "12-railway-redeploy.png",
             "caption": "Step 12: Your Update Workflow From Here",
             "desc": "Once your app is live, updating it is simple. Make a change in your code → push it to GitHub → Railway detects the push and redeploys automatically. No manual steps. No server management. No downtime. Railway handles all of it. Your workflow becomes: code it, push it, it's live."},
        ]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # LESSON 3-3: Using AI to Build Your App (the build prompt)
    # ─────────────────────────────────────────────────────────────────────────
    "3-3": {
        "title": "Lesson 3.3 — Using AI to Build Your App Skeleton",
        "subtitle": "You describe what you want. AI writes the code. You review and deploy.",
        "steps": [
            {"action": "navigate", "url": "https://github.com",
             "caption": "Step 1: Where the Code Will Live",
             "desc": "Before we build, a quick look at where everything ends up."},
            {"action": "screenshot", "filename": "01-github-overview.png",
             "caption": "Step 1: GitHub — Your Code's Home",
             "desc": "Everything we build in this lesson gets saved to GitHub first, then deployed to Railway. Think of GitHub as the save button and Railway as the publish button."},
        ]
    },

}

