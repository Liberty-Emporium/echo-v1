import urllib.request, json, time, os

apps = {
    "FloodClaims Pro": "https://billy-floods.up.railway.app",
    "EcDash": "https://alexanderai.site",
    "Sweet Spot Cakes": "https://sweet-spot-cakes.up.railway.app",
    "AI Agent Widget": "https://ai-agent-widget-production.up.railway.app",
    "Remote Repair": "https://web-production-9cc1c.up.railway.app",
    "Agents Dashboard": "https://agents.alexanderai.site",
    "Shop": "https://shop.alexanderai.site",
    "Voice Makeover": "https://voice-make-over.alexanderai.site",
    "AI Widget": "https://ai-widget.alexanderai.site",
    "Consignment": "https://consignment.ai.solutions.alexanderai.site",
    "Contractor Pro": "https://contractor.ai.solutions.alexanderai.site",
    "Pet Vet AI": "https://ai-vet-tech.alexanderai.site",
    "LE Thrift": "https://liberty-emporium-thrift.alexanderai.site",
    "Gym Forge": "https://gymforge.ai.alexanderai.site",
    "IT Courses": "https://web-production-8bbc54.up.railway.app",
    "Luxury Rentals": "https://luxury-rentals-demo-production.up.railway.app",
    "Liberty Oil": "https://libertyoilandpropane.com",
}

results = {}
for name, url in apps.items():
    start = time.time()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'OWL-Monitor/1.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        elapsed_ms = round((time.time() - start) * 1000, 1)
        results[name] = {"status": "up", "http_code": resp.status, "response_ms": elapsed_ms}
    except Exception as e:
        elapsed_ms = round((time.time() - start) * 1000, 1)
        results[name] = {"status": "down", "http_code": 0, "response_ms": 0, "error": str(e)[:200]}

# Read previous state
state_path = "/home/lol/Desktop/openclaw/echo-v1/communications/monitor_state.json"
previous_state = {}
if os.path.exists(state_path):
    try:
        with open(state_path, 'r') as f:
            previous_state = json.load(f)
    except:
        pass

# Write new state
output = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "results": results
}
os.makedirs(os.path.dirname(state_path), exist_ok=True)
with open(state_path, 'w') as f:
    json.dump(output, f, indent=2)

# Summary
up_count = sum(1 for r in results.values() if r["status"] == "up")
down_count = sum(1 for r in results.values() if r["status"] == "down")

print(f"--- APP HEALTH CHECK: {output['timestamp']} ---")
print(f"UP: {up_count}/{len(apps)}  |  DOWN: {down_count}/{len(apps)}")
print()

if down_count > 0:
    print("DOWN APPS:")
    for name, r in results.items():
        if r["status"] == "down":
            print(f"  ❌ {name}: {r.get('error', 'Unknown error')[:120]}")
    print()

# Check for newly down apps (were UP before, now DOWN)
if previous_state and "results" in previous_state:
    prev_results = previous_state["results"]
    newly_down = []
    for name, r in results.items():
        if r["status"] == "down" and name in prev_results:
            if prev_results[name].get("status") == "up":
                newly_down.append(name)
    if newly_down:
        print("⚠️  NEWLY DOWN (were UP last check):")
        for name in newly_down:
            print(f"  🔴 {name}")

print()
for name, r in results.items():
    icon = "✅" if r["status"] == "up" else "❌"
    ms = f"{r['response_ms']}ms" if r['status'] == 'up' else 'N/A'
    code = r.get('http_code', '-')
    print(f"  {icon} {name} | {r['status'].upper()} | HTTP {code} | {ms}")
