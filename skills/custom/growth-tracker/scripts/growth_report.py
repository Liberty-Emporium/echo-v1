#!/usr/bin/env python3
"""
growth-tracker — Track signups, conversions, churn and revenue
Usage: python3 growth_report.py --app <name> --db <path-to-sqlite>
"""
import sys
import os
import argparse
import sqlite3
import datetime
import urllib.request
import urllib.error
import json

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
RESET  = "\033[0m"

APPS = {
    "liberty-inventory": {"url": "https://liberty-emporium-and-thrift-inventory-app-production.up.railway.app", "price": 20, "startup": 99},
    "consignment-solutions": {"url": "https://web-production-43ce4.up.railway.app", "price": 20, "startup": 69.95},
    "contractor-pro": {"url": "https://contractor-pro-ai-production.up.railway.app", "price": 99, "startup": 0},
    "dropship-shipping": {"url": "https://dropship-shipping-production.up.railway.app", "price": 0, "startup": 299},
    "pet-vet": {"url": "https://pet-vet-ai-production.up.railway.app", "price": 9.99, "startup": 0},
    "keep-your-secrets": {"url": "https://ai-api-tracker-production.up.railway.app", "price": 14.99, "startup": 0},
}

def header(text):
    print(f"\n{BLUE}{'='*55}")
    print(f"  {text}")
    print(f"{'='*55}{RESET}")

def metric(label, value, target=None, unit="", good_direction="up"):
    if target:
        ratio = value / target if target else 0
        if good_direction == "up":
            color = GREEN if ratio >= 1.0 else YELLOW if ratio >= 0.5 else RED
        else:
            color = GREEN if ratio <= 1.0 else YELLOW if ratio <= 1.5 else RED
        bar = int(min(ratio, 1.0) * 20)
        bar_str = "█" * bar + "░" * (20 - bar)
        print(f"  {label:<30} {color}{value}{unit}{RESET} / {target}{unit}  [{bar_str}]")
    else:
        print(f"  {label:<30} {value}{unit}")

def check_health(url):
    try:
        req = urllib.request.Request(f"{url}/health", headers={"User-Agent": "GrowthTracker/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            return data.get("status") == "ok"
    except Exception:
        try:
            req = urllib.request.Request(f"{url}/ping", headers={"User-Agent": "GrowthTracker/1.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                return r.status == 200
        except Exception:
            return False

def analyze_db(db_path):
    """Pull metrics directly from app SQLite database."""
    if not os.path.exists(db_path):
        print(f"{YELLOW}Database not found: {db_path}{RESET}")
        return None

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        results = {}

        now = datetime.datetime.utcnow()
        week_ago = (now - datetime.timedelta(days=7)).isoformat()
        month_ago = (now - datetime.timedelta(days=30)).isoformat()

        # Try to get user/customer tables
        tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        results["tables"] = tables

        # Customers/tenants
        for table in ["customers", "client_configs", "tenants", "users"]:
            if table in tables:
                total = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                results[f"total_{table}"] = total

                # Recent signups
                for col in ["created_at", "signup_date", "joined_at", "date_added"]:
                    try:
                        recent = c.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} > ?", (week_ago,)).fetchone()[0]
                        results[f"new_{table}_7d"] = recent
                        monthly = c.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} > ?", (month_ago,)).fetchone()[0]
                        results[f"new_{table}_30d"] = monthly
                        break
                    except Exception:
                        continue

        # Trial data
        for table in tables:
            if "trial" in table.lower():
                total = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                results[f"trials_{table}"] = total

        # Metrics table (added last night)
        if "metrics" in tables:
            metrics_data = c.execute("SELECT metric, SUM(value) FROM metrics GROUP BY metric").fetchall()
            results["metrics"] = {row[0]: row[1] for row in metrics_data}

        conn.close()
        return results
    except Exception as e:
        print(f"{YELLOW}DB analysis error: {e}{RESET}")
        return None

def all_apps_report():
    header("ALL APPS — PORTFOLIO HEALTH CHECK")
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    print(f"  Generated: {today}\n")

    total_mrr = 0
    print(f"  {'App':<30} {'Status':<10} {'Monthly Price':<15}")
    print(f"  {'-'*55}")

    for app_id, app in APPS.items():
        alive = check_health(app["url"])
        status = f"{GREEN}● UP{RESET}" if alive else f"{RED}● DOWN{RESET}"
        mrr = app["price"]
        print(f"  {app_id:<30} {status:<20} ${mrr}/mo")

    print(f"\n  {BLUE}Revenue Targets{RESET}")
    targets = [
        ("Liberty Inventory", 20, 50, 1000),
        ("Consignment Solutions", 20, 50, 1000),
        ("Contractor Pro AI", 99, 20, 1980),
        ("Dropship Shipping", 299, 20, 5980),
        ("Pet Vet AI", 9.99, 200, 1998),
        ("Keep Your Secrets", 14.99, 100, 1499),
    ]
    print(f"\n  {'App':<28} {'$/user':<10} {'Target users':<15} {'Target MRR'}")
    print(f"  {'-'*65}")
    target_total = 0
    for name, price, users, mrr in targets:
        print(f"  {name:<28} ${price:<9} {users:<15} ${mrr:,}")
        target_total += mrr
    print(f"  {'-'*65}")
    print(f"  {'TOTAL TARGET MRR':<53} ${target_total:,}")
    print(f"\n  {YELLOW}To hit $13,457 MRR you need ~440 paying users across all apps.{RESET}")

def single_app_report(app_id, db_path=None):
    if app_id not in APPS:
        print(f"{RED}Unknown app: {app_id}{RESET}")
        print(f"Available: {', '.join(APPS.keys())}")
        sys.exit(1)

    app = APPS[app_id]
    header(f"GROWTH REPORT: {app_id.upper()}")

    # Health
    alive = check_health(app["url"])
    status = f"{GREEN}● ONLINE{RESET}" if alive else f"{RED}● OFFLINE — CRITICAL{RESET}"
    print(f"  Status: {status}")
    print(f"  URL: {app['url']}")
    print(f"  Monthly Revenue: ${app['price']}/user")

    # DB analysis
    if db_path:
        print(f"\n  {BLUE}[Database Metrics]{RESET}")
        data = analyze_db(db_path)
        if data:
            for k, v in data.items():
                if k != "tables" and k != "metrics":
                    print(f"  {k}: {v}")
            if "metrics" in data:
                print(f"\n  {BLUE}[Tracked Events]{RESET}")
                for event, count in data["metrics"].items():
                    print(f"  {event}: {count}")
    else:
        print(f"\n  {YELLOW}Tip: Pass --db /data/app.db to see signup/conversion data{RESET}")

    # Growth advice
    print(f"\n  {BLUE}[Growth Recommendations]{RESET}")
    advice = [
        "✅ Email onboarding sequence — auto-sends to all new trial users",
        "📈 Add Google Analytics or Plausible for traffic data",
        "💬 Add live chat (Tawk.to is free) — converts 2-3x better",
        "🎯 Add exit intent popup on landing page — capture leads before they leave",
        "⭐ Add social proof — even 5 testimonials doubles conversions",
        "📧 Set up weekly digest email to active users — reduces churn",
        f"💰 Consider annual plan (${ int(app['price'] * 10)}/yr = 2 months free) — increases LTV 40%",
    ]
    for a in advice:
        print(f"  {a}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", default="all", help="App name or 'all'")
    parser.add_argument("--db", default=None, help="Path to SQLite database")
    args = parser.parse_args()

    if args.app == "all":
        all_apps_report()
    else:
        single_app_report(args.app, args.db)
