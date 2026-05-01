"""
Liberty-Emporium App Configurations for browser-tester skill.
Edit this file to add/update apps. Used by browser_test.py.
"""

APPS = {
    # ── GymForge ──────────────────────────────────────────────────────────────
    "gymforge": {
        "name": "GymForge",
        "url": "https://web-production-1c23.up.railway.app",
        "login_path": "/auth/login/",
        "roles": [
            {
                "role": "owner",
                "email": "jay@gymforge.com",
                "password": "GymForge2026!",
                "pages": [
                    ("/owner/",              "dashboard",        ["Dashboard", "Gym"]),
                    ("/owner/tiers/",        "membership tiers", ["Tier", "Plan", "Member"]),
                    ("/owner/staff/",        "staff list",       ["Staff"]),
                    ("/owner/leads/",        "leads",            ["Lead"]),
                    ("/owner/branding/",     "branding",         ["Brand", "Gym"]),
                    ("/owner/schedule/",     "schedule",         ["Schedule", "Class"]),
                    ("/owner/analytics/",    "analytics",        ["Analytic", "Stat"]),
                ],
            },
            {
                "role": "manager",
                "email": "manager@demo.gymforge.com",
                "password": "Demo2026!",
                "pages": [
                    ("/manager/",          "dashboard",  ["Dashboard", "Manager"]),
                    ("/manager/schedule/", "schedule",   ["Schedule", "Class"]),
                    ("/manager/shifts/",   "shifts",     ["Shift", "Staff"]),
                    ("/manager/checkins/", "check-ins",  ["Check"]),
                ],
            },
            {
                "role": "trainer",
                "email": "trainer@demo.gymforge.com",
                "password": "Demo2026!",
                "pages": [
                    ("/trainer/",               "client list",   ["Client", "Member"]),
                    ("/trainer/appointments/",  "appointments",  ["Appointment"]),
                    ("/trainer/workout-plans/", "workout plans", ["Plan", "Workout"]),
                ],
            },
            {
                "role": "front_desk",
                "email": "front_desk@demo.gymforge.com",
                "password": "Demo2026!",
                "pages": [
                    ("/desk/",                "dashboard",      ["Check", "Front"]),
                    ("/desk/checkin/manual/", "manual check-in",["Check", "Member"]),
                    ("/desk/members/",        "member lookup",  ["Member"]),
                ],
            },
            {
                "role": "cleaner",
                "email": "cleaner@demo.gymforge.com",
                "password": "Demo2026!",
                "pages": [
                    ("/cleaner/",         "dashboard",    ["Task", "Cleaner"]),
                    ("/cleaner/tasks/",   "task list",    ["Task"]),
                    ("/cleaner/summary/", "shift summary",["Shift", "Summary"]),
                ],
            },
            {
                "role": "nutritionist",
                "email": "nutritionist@demo.gymforge.com",
                "password": "Demo2026!",
                "pages": [
                    ("/nutritionist/",              "client list",    ["Client", "Member"]),
                    ("/nutritionist/appointments/", "appointments",   ["Appointment"]),
                    ("/nutritionist/plans/",        "nutrition plans",["Plan", "Nutrition"]),
                ],
            },
            {
                "role": "member",
                "email": "member@demo.gymforge.com",
                "password": "Demo2026!",
                "pages": [
                    ("/app/",                    "member home",    ["Gym", "Welcome"]),
                    ("/app/classes/",            "class schedule", ["Class", "Schedule"]),
                    ("/app/workouts/",           "workouts",       ["Workout"]),
                    ("/app/classes/my-bookings/","my bookings",    ["Booking", "Class"]),
                ],
            },
        ],
        # Public pages (no login needed)
        "public_pages": [
            ("/",        "landing page", ["Gym", "Membership", "Join"]),
            ("/health/", "health check", ["ok"]),
        ],
    },

    # ── FloodClaim Pro ────────────────────────────────────────────────────────
    "floodclaim": {
        "name": "FloodClaim Pro",
        "url": "https://billy-floods.up.railway.app",
        "login_path": "/auth/login/",
        "public_pages": [
            ("/",        "home",         ["FloodClaim", "Claim"]),
            ("/health/", "health check", ["ok"]),
            ("/sales",   "sales page",   ["FloodClaim", "Pro"]),
        ],
        "roles": [
            {
                "role": "admin",
                "email": "admin@floodclaim.com",
                "password": "admin",
                "pages": [
                    ("/dashboard/", "dashboard", ["Claim", "Dashboard"]),
                ],
            },
        ],
    },

    # ── EcDash ────────────────────────────────────────────────────────────────
    "ecdash": {
        "name": "EcDash",
        "url": "https://jay-portfolio-production.up.railway.app",
        "login_path": "/login",
        "public_pages": [
            ("/",        "home",   ["Dashboard", "Portfolio", "Jay"]),
            ("/health/", "health", ["ok"]),
        ],
        "roles": [],
    },

    # ── AI Agent Widget ───────────────────────────────────────────────────────
    "ai-widget": {
        "name": "AI Agent Widget",
        "url": "https://ai-agent-widget-production.up.railway.app",
        "login_path": "/auth/login/",
        "public_pages": [
            ("/",        "home",   ["Widget", "AI", "Agent"]),
            ("/health/", "health", ["ok"]),
        ],
        "roles": [],
    },

    # ── Pet Vet AI ────────────────────────────────────────────────────────────
    "petvet": {
        "name": "Pet Vet AI",
        "url": "https://pet-vet-ai-production.up.railway.app",
        "login_path": "/auth/login/",
        "public_pages": [
            ("/",        "home",   ["Vet", "Pet"]),
            ("/health/", "health", ["ok"]),
        ],
        "roles": [],
    },

    # ── Liberty Oil ───────────────────────────────────────────────────────────
    "liberty-oil": {
        "name": "Liberty Oil & Propane",
        "url": "https://liberty-oil-propane.up.railway.app",
        "public_pages": [
            ("/", "home", ["Liberty", "Oil", "Propane"]),
        ],
        "roles": [],
    },
}

# Shortcut: test all apps with --app all
ALL_APPS = list(APPS.keys())
