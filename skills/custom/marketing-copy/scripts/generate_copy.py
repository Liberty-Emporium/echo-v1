#!/usr/bin/env python3
"""
marketing-copy — Generate high-converting copy for Jay's SaaS apps
Usage: python3 generate_copy.py --app <name> --type email|landing|ad|social
"""
import argparse
import sys

APPS = {
    "liberty-inventory": {
        "name": "Liberty Inventory",
        "tagline": "The all-in-one inventory system for thrift stores & resellers",
        "price_startup": "$99",
        "price_monthly": "$20/mo",
        "trial": "14-day free trial",
        "pain": "drowning in spreadsheets, losing track of inventory, missing sales",
        "outcome": "organized inventory, faster sales, more profit",
        "audience": "thrift store owners, resellers, consignment shops",
        "key_features": ["Smart inventory tracking", "AI-powered product descriptions", "Sales analytics", "Multi-store support"],
        "url": "https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app",
    },
    "dropship-shipping": {
        "name": "Dropship Shipping (Andy)",
        "tagline": "Fully automated dropshipping CRM — set it and forget it",
        "price_startup": "$299",
        "price_monthly": "included",
        "trial": "demo available",
        "pain": "manually tracking orders, losing suppliers, missing shipments",
        "outcome": "automated order flow, happy customers, more revenue",
        "audience": "dropshippers, ecommerce sellers, online store owners",
        "key_features": ["Automated order processing", "Supplier management", "Shipment tracking", "Customer CRM"],
        "url": "https://dropship-shipping-production.up.railway.app",
    },
    "consignment-solutions": {
        "name": "Consignment Solutions",
        "tagline": "Modern consignment management for antique stores & boutiques",
        "price_startup": "$69.95",
        "price_monthly": "$20/mo",
        "trial": "14-day free trial",
        "pain": "manual vendor tracking, missed settlements, inventory chaos",
        "outcome": "automated vendor payouts, organized inventory, happy consignors",
        "audience": "consignment store owners, antique dealers, boutique owners",
        "key_features": ["Vendor portals", "Auto rent settlement", "Square POS integration", "AI assistant"],
        "url": "https://web-production-43ce4.up.railway.app",
    },
    "contractor-pro": {
        "name": "Contractor Pro AI",
        "tagline": "AI-powered project management for contractors",
        "price_startup": "no setup fee",
        "price_monthly": "$99/mo",
        "trial": "first month free",
        "pain": "losing bids, missing deadlines, juggling clients",
        "outcome": "more bids won, projects on time, clients happy",
        "audience": "contractors, builders, tradespeople, construction companies",
        "key_features": ["AI bid writing", "Project timeline management", "Client communication", "Invoice automation"],
        "url": "https://contractor-pro-ai-production.up.railway.app",
    },
    "pet-vet": {
        "name": "Pet Vet AI",
        "tagline": "AI pet health diagnosis — instant answers for worried pet owners",
        "price_startup": "no setup fee",
        "price_monthly": "$9.99/mo",
        "trial": "first diagnosis free",
        "pain": "expensive vet bills, 2am pet emergencies, not knowing what's wrong",
        "outcome": "quick answers, peace of mind, know when to see the vet",
        "audience": "pet owners, dog owners, cat owners, animal lovers",
        "key_features": ["Instant symptom analysis", "Breed-specific advice", "Emergency triage", "Vet visit guidance"],
        "url": "https://pet-vet-ai-production.up.railway.app",
    },
    "keep-your-secrets": {
        "name": "Jay's Keep Your Secrets",
        "tagline": "Secure API key management — never lose a key again",
        "price_startup": "no setup fee",
        "price_monthly": "$14.99/mo",
        "trial": "7-day free trial",
        "pain": "API keys scattered everywhere, security breaches, rotated tokens breaking apps",
        "outcome": "all keys in one secure place, team access control, zero breaches",
        "audience": "developers, SaaS founders, tech teams, API users",
        "key_features": ["Encrypted key storage", "Team access control", "Key rotation alerts", "API audit logs"],
        "url": "https://ai-api-tracker-production.up.railway.app",
    },
}

def email_sequence(app):
    a = APPS[app]
    print(f"\n{'='*60}")
    print(f"EMAIL SEQUENCE: {a['name']}")
    print(f"{'='*60}\n")

    emails = [
        {
            "day": 0, "subject": f"Welcome to {a['name']} 🎉",
            "body": f"""Hi {{{{first_name}}}},

Welcome! You just made a smart decision.

{a['name']} is going to fix the problem of {a['pain']}.

Here's your first step — log in and do ONE thing right now:
→ {a['key_features'][0]}

That's it. Just one thing. It takes 5 minutes and you'll immediately see the difference.

→ Log in now: {a['url']}

Your {a['trial']} starts today. I'll check in with you in a few days.

— Jay Alexander
Founder, {a['name']}

P.S. Reply to this email if you need anything. I read every message."""
        },
        {
            "day": 3, "subject": f"Quick check-in — are you getting value from {a['name']}?",
            "body": f"""Hi {{{{first_name}}}},

3 days in. How's it going?

The #1 thing I see new users miss is: {a['key_features'][1]}

If you haven't tried that yet, do it today. It's the feature that makes everything click.

You've got {a['trial']} — don't let it go to waste.

→ Try it now: {a['url']}

— Jay"""
        },
        {
            "day": 7, "subject": f"One week in — here's what you should have by now",
            "body": f"""Hi {{{{first_name}}}},

One week with {a['name']}. By now you should:

✅ {a['key_features'][0]}
✅ {a['key_features'][1]}
✅ Starting to see {a['outcome']}

If you're not there yet — reply and tell me what's blocking you. I'll personally help.

If you ARE getting value — consider locking in your account before your trial ends.

Plans start at just {a['price_monthly']}.

→ Upgrade: {a['url']}

— Jay"""
        },
        {
            "day": 12, "subject": f"⚠️ Your {a['name']} trial ends in 2 days",
            "body": f"""Hi {{{{first_name}}}},

Your free trial ends in 2 days.

Everything you've set up — your data, your settings, your work — disappears when it expires.

Don't lose it. Upgrade now for just {a['price_monthly']}.

→ Keep my account: {a['url']}

Takes 2 minutes. No surprises.

— Jay"""
        },
        {
            "day": 14, "subject": f"Last chance — your {a['name']} trial expires today",
            "body": f"""Hi {{{{first_name}}}},

Today's the last day.

I'll keep this short: if {a['name']} helped you even once, it's worth {a['price_monthly']}.

That's less than a coffee a week.

→ Upgrade before midnight: {a['url']}

If you're not ready, no pressure — but reply and tell me why. I want to make this better.

— Jay"""
        },
    ]

    for e in emails:
        print(f"--- Day {e['day']} ---")
        print(f"Subject: {e['subject']}")
        print(f"\n{e['body']}\n")

def landing_page_copy(app):
    a = APPS[app]
    print(f"\n{'='*60}")
    print(f"LANDING PAGE COPY: {a['name']}")
    print(f"{'='*60}\n")

    print(f"""HERO SECTION
============
Headline: Stop {a['pain'].split(',')[0].capitalize()}
Subheadline: {a['tagline']}
CTA Button: Start Your {a['trial'].title()} →
Under CTA: No credit card required. Setup in 5 minutes.

BENEFITS SECTION
================
✅ {a['key_features'][0]} — Save hours every week
✅ {a['key_features'][1]} — Built for {a['audience'].split(',')[0]}
✅ {a['key_features'][2]} — Know exactly what's happening

PRICING SECTION
===============
{"One-time: " + a['price_startup'] + " • " if a['price_startup'] != 'no setup fee' else ""}Monthly: {a['price_monthly']}
{a['trial'].capitalize()} included. Cancel anytime.

SOCIAL PROOF
============
"[This app] saved me X hours per week." — [Customer Name], [City]
★★★★★ "Finally, software that just works."
Used by [X]+ {a['audience'].split(',')[0]}s

FAQ
===
Q: Do I need technical skills?
A: No. If you can use email, you can use {a['name']}.

Q: What happens after my trial?
A: You choose a plan or your data is safely exported. No surprises.

Q: Is my data secure?
A: Yes. Encrypted at rest, backed up daily, hosted on Railway.

FOOTER CTA
==========
Ready to fix {a['pain'].split(',')[0]}?
→ Start Free Today: {a['url']}
""")

def ad_copy(app):
    a = APPS[app]
    print(f"\n{'='*60}")
    print(f"AD COPY: {a['name']}")
    print(f"{'='*60}\n")

    print(f"""GOOGLE ADS (30 char headlines)
==============================
H1: {a['name'][:25]} Trial
H2: Fix {a['pain'].split(',')[0][:22]}
H3: Start Free Today

Description (90 chars):
{a['tagline']}. {a['trial'].capitalize()}. {a['price_monthly']}.

FACEBOOK/INSTAGRAM AD
=====================
Hook: Are you still {a['pain'].split(',')[0]}?

{a['name']} was built for {a['audience'].split(',')[0]}s who are done with that.

→ {a['key_features'][0]}
→ {a['key_features'][1]}
→ {a['key_features'][2]}

{a['trial'].capitalize()}. No credit card.

[Try it free] → {a['url']}

X/TWITTER POST
==============
Built a tool for {a['audience'].split(',')[0]}s tired of {a['pain'].split(',')[0]}.

{a['name']} — {a['tagline']}

{a['trial'].capitalize()} → {a['url']}

#SaaS #{a['audience'].split(',')[0].replace(' ', '')}
""")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate marketing copy for Jay's apps")
    parser.add_argument("--app", required=True, choices=list(APPS.keys()), help="App to generate copy for")
    parser.add_argument("--type", choices=["email", "landing", "ad", "all"], default="all")
    args = parser.parse_args()

    if args.type in ("email", "all"):
        email_sequence(args.app)
    if args.type in ("landing", "all"):
        landing_page_copy(args.app)
    if args.type in ("ad", "all"):
        ad_copy(args.app)
