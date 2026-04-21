#!/usr/bin/env python3
"""
Liberty-Emporium Browser Test Suite
Runs real Chromium browser tests against all apps using browser-use.

Usage:
    python3 browser_suite.py                          # run ALL tests
    python3 browser_suite.py --test rooms             # one test
    python3 browser_suite.py --test rooms estimate    # multiple tests
    python3 browser_suite.py --list                   # show available tests

Available tests:
    floodclaim_login    FloodClaim Pro  - Login + dashboard loads
    floodclaim_rooms    FloodClaim Pro  - Add room + line item to claim
    floodclaim_estimate FloodClaim Pro  - AI Estimate generation
    floodclaim_delete   FloodClaim Pro  - Delete button is separate (safety check)
    ai_widget_signup    AI Agent Widget - New user signup + dashboard
    ai_widget_pricing   AI Agent Widget - Pricing page content
    ecdash_login        EcDash          - Login + dashboard panels load
    ecdash_chat         EcDash          - Echo chat responds
    petvet_finder       Pet Vet AI      - Vet search returns results
    grace_home          Grace           - Home page + greeting visible
    grace_ai            Grace           - AI responds to a message
    kys_login           Keep Your Secrets - Login + key list loads
    contractor_login    Contractor Pro AI - Login + dashboard loads
"""

import asyncio, os, sys, time, argparse

# ── LLM setup ─────────────────────────────────────────────────────────────────
def get_llm():
    try:
        raw = open(os.path.expanduser('~/.env')).read().strip()
        key = raw.split('=', 1)[1].strip() if '=' in raw else raw
    except Exception:
        key = os.environ.get('OPENROUTER_API_KEY', '')
    if not key:
        print('ERROR: no API key found in ~/.env or OPENROUTER_API_KEY')
        sys.exit(1)
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model='openai/gpt-4o-mini',
        openai_api_key=key,
        base_url='https://openrouter.ai/api/v1',
    )

# ── Runner ────────────────────────────────────────────────────────────────────
async def run_agent(task: str, timeout: int = 120) -> str:
    from browser_use import Agent
    llm = get_llm()
    agent = Agent(task=task, llm=llm)
    try:
        res = await asyncio.wait_for(agent.run(), timeout=timeout)
        return str(res.final_result() or '').strip()
    except asyncio.TimeoutError:
        return 'TIMEOUT after ' + str(timeout) + 's'
    except Exception as e:
        return f'ERROR: {e}'

def has(output: str, *words) -> bool:
    """True if ALL words appear in output (case-insensitive)."""
    lo = output.lower()
    return all(w.lower() in lo for w in words)

def has_any(output: str, *words) -> bool:
    lo = output.lower()
    return any(w.lower() in lo for w in words)

def has_dollar(output: str) -> bool:
    import re
    return bool(re.search(r'\$[\d,]+\.?\d*', output))

# ── Credentials ───────────────────────────────────────────────────────────────
FLOOD_URL   = 'https://billy-floods.up.railway.app'
FLOOD_EMAIL = 'admin@floodclaimpro.com'
FLOOD_PASS  = 'admin1234'

WIDGET_URL     = 'https://ai-agent-widget-production.up.railway.app'
ECDASH_URL     = 'https://jay-portfolio-production.up.railway.app'
PETVET_URL     = 'https://pet-vet-ai-production.up.railway.app'
GRACE_URL      = 'https://moms-ai-helper.up.railway.app'
KYS_URL        = 'https://ai-api-tracker-production.up.railway.app'
CONTRACTOR_URL = 'https://contractor-pro-ai-production.up.railway.app'

LOGIN_NOTE = 'IMPORTANT: login with EXACTLY '

# ── Test definitions ──────────────────────────────────────────────────────────
TESTS = {}

def test(name, label, app, icon, task_str, pass_fn, timeout=90):
    TESTS[name] = {
        'label': label, 'app': app, 'icon': icon,
        'task': task_str, 'pass_fn': pass_fn, 'timeout': timeout,
    }

test(
    name='floodclaim_login',
    label='Login + Dashboard loads',
    app='FloodClaim Pro', icon='🌊',
    task_str=f'''{LOGIN_NOTE}email={FLOOD_EMAIL} password={FLOOD_PASS}. Do NOT try any other passwords.
Go to {FLOOD_URL} and log in.
Tell me: 1) Does the dashboard show a list of claims? 2) How many claims are listed?''',
    pass_fn=lambda o: has_any(o, 'yes', 'claim', 'dashboard', 'gonzalez', 'thompson', 'moore') and not has(o, 'error', 'failed'),
)

test(
    name='floodclaim_rooms',
    label='Add Room + Line Item',
    app='FloodClaim Pro', icon='🌊',
    task_str=f'''{LOGIN_NOTE}email={FLOOD_EMAIL} password={FLOOD_PASS}. Do NOT try any other passwords.
Go to {FLOOD_URL} and log in. Click View next to Robert Thompson.
Add a room named "Test Kitchen". Add a line item: description=Replace subfloor, qty=80, unit=sf, unit_cost=3.25.
Tell me: 1) Room added? 2) Line item added? 3) Subtotal for Test Kitchen?''',
    pass_fn=lambda o: has_any(o, 'yes', 'added', 'success') and has_dollar(o),
    timeout=120,
)

test(
    name='floodclaim_estimate',
    label='AI Estimate generation',
    app='FloodClaim Pro', icon='🌊',
    task_str=f'''{LOGIN_NOTE}email={FLOOD_EMAIL} password={FLOOD_PASS}. Do NOT try any other passwords.
Go to {FLOOD_URL} and log in. Click View next to James & Patricia Moore.
Click the green AI Estimate button. Wait 90 seconds.
Tell me the Grand Total dollar amount from the estimate.''',
    pass_fn=lambda o: has_dollar(o),
    timeout=180,
)

test(
    name='floodclaim_delete_safety',
    label='Delete button is separate (no mis-click)',
    app='FloodClaim Pro', icon='🌊',
    task_str=f'''{LOGIN_NOTE}email={FLOOD_EMAIL} password={FLOOD_PASS}. Do NOT try any other passwords.
Go to {FLOOD_URL} and log in.
Look at the claims table. Are the "View →" button and the 🗑 delete button in SEPARATE columns?
Do NOT click delete. Just tell me: are they in separate cells/columns? Yes or No?''',
    pass_fn=lambda o: has(o, 'yes'),
)

test(
    name='ai_widget_signup',
    label='New user signup + dashboard',
    app='AI Agent Widget', icon='🤖',
    task_str=f'''Go to {WIDGET_URL}/signup.
Sign up with a random test email like test-abc123@test.com and password TestPass123!
Tell me: 1) Did signup succeed? 2) Did it reach /dashboard? 3) Is there an option to create an agent?''',
    pass_fn=lambda o: has_any(o, 'yes', 'dashboard', 'success', 'agent'),
    timeout=60,
)

test(
    name='ai_widget_pricing',
    label='Pricing page content',
    app='AI Agent Widget', icon='🤖',
    task_str=f'''Go to {WIDGET_URL}/pricing.
Tell me: 1) What plans are listed? 2) What are the prices? 3) Is there an Installation service listed?''',
    pass_fn=lambda o: has_dollar(o) and has_any(o, 'pro', 'plan', 'basic', 'install'),
    timeout=45,
)

test(
    name='ecdash_login',
    label='Login + all sidebar panels load',
    app='EcDash', icon='🎛️',
    task_str=f'''Go to {ECDASH_URL}/login and log in with password liberty2026.
After logging in, click through these sidebar items: Overview, Projects, To-Do List, Quick Links.
Tell me: 1) Did login work? 2) Did each panel load without errors? 3) Any broken panels?''',
    pass_fn=lambda o: has_any(o, 'yes', 'loaded', 'success', 'work') and not has(o, 'broken', '500', 'error'),
    timeout=90,
)

test(
    name='ecdash_chat',
    label='Echo chat responds',
    app='EcDash', icon='🎛️',
    task_str=f'''Go to {ECDASH_URL}/login and log in with password liberty2026.
Navigate to the Chat page (sidebar: Chat with EcDash or /chat).
Send this message: "Hello Echo, what apps do we have in the Liberty-Emporium portfolio?"
Tell me: 1) Did the chat send? 2) What did Echo reply? (copy first 100 chars of reply)''',
    pass_fn=lambda o: has_any(o, 'liberty', 'app', 'flood', 'portfolio', 'widget', 'pet'),
    timeout=90,
)

test(
    name='petvet_finder',
    label='Vet finder returns results',
    app='Pet Vet AI', icon='🐾',
    task_str=f'''Go to {PETVET_URL} and log in (try email admin@petvetai.com password admin1234, or just visit the site if no login needed).
Use the vet finder to search for vets near "Greensboro, NC".
Tell me: 1) Did it find any vets? 2) How many? 3) Name one vet listed.''',
    pass_fn=lambda o: has_any(o, 'vet', 'animal', 'clinic', 'hospital', 'care') and not has(o, 'error', 'none found', '0 vet'),
    timeout=90,
)

test(
    name='grace_home',
    label='Home page loads + greeting visible',
    app='Grace', icon='💜',
    task_str=f'''Go to {GRACE_URL}.
Tell me: 1) Does the page load? 2) Is there a greeting (Good morning/afternoon/evening)? 
3) Is there a big GRACE button or FAB button visible? 4) Is there a bottom navigation bar?''',
    pass_fn=lambda o: has_any(o, 'yes', 'good morning', 'good afternoon', 'good evening', 'grace', 'visible'),
    timeout=45,
)

test(
    name='grace_ai',
    label='Grace AI responds to a message',
    app='Grace', icon='💜',
    task_str=f'''Go to {GRACE_URL}.
Find the Grace chat interface or TALK button and send this message: "Hello Grace, what can you help me with today?"
Tell me: 1) Did Grace respond? 2) What did she say? (copy first 80 chars of response)''',
    pass_fn=lambda o: has_any(o, 'yes', 'grace', 'help', 'i can', 'medication', 'remind', 'appointment'),
    timeout=60,
)

test(
    name='kys_login',
    label='Login + key list visible',
    app='Keep Your Secrets', icon='🔐',
    task_str=f'''Go to {KYS_URL} and log in (try admin@keepyoursecrets.com / admin1234, or whatever works).
Tell me: 1) Did login work? 2) Is there a list of API keys or secrets? 3) Is there an "Add Key" button?''',
    pass_fn=lambda o: has_any(o, 'yes', 'key', 'secret', 'api', 'add', 'dashboard'),
    timeout=60,
)

test(
    name='contractor_login',
    label='Login + dashboard loads',
    app='Contractor Pro AI', icon='🔨',
    task_str=f'''Go to {CONTRACTOR_URL} and log in (try admin@contractorpro.com / admin1234, or whatever the login is).
Tell me: 1) Did login work? 2) What do you see on the dashboard? 3) Any errors?''',
    pass_fn=lambda o: has_any(o, 'yes', 'dashboard', 'estimate', 'project', 'contractor') and not has(o, '500'),
    timeout=60,
)

# ── Runner ────────────────────────────────────────────────────────────────────
def print_header(text):
    print(f'\n{"="*60}')
    print(f' {text}')
    print('='*60)

def print_result(label, passed, detail=''):
    icon = '✅ PASS' if passed else '❌ FAIL'
    print(f' {icon}: {label}')
    if detail:
        print(f'   → {detail[:160]}')

async def run_test(name: str) -> dict:
    t = TESTS[name]
    print_header(f'{t["icon"]}  {t["app"]} — {t["label"]}')
    start = time.time()
    output = await run_agent(t['task'], timeout=t['timeout'])
    elapsed = round(time.time() - start, 1)
    passed = t['pass_fn'](output)
    print(f'\n📄 Agent output:\n {output}\n')
    print_result(t['label'], passed, f'{elapsed}s')
    return {'name': name, 'label': t['label'], 'app': t['app'],
            'passed': passed, 'output': output, 'elapsed': elapsed}

async def main():
    parser = argparse.ArgumentParser(description='Liberty-Emporium Browser Test Suite')
    parser.add_argument('--test', nargs='*', help='Test(s) to run')
    parser.add_argument('--list', action='store_true', help='List all tests')
    args = parser.parse_args()

    if args.list:
        print('\nAvailable tests:')
        for name, t in TESTS.items():
            print(f'  {name:<28} {t["icon"]} {t["app"]} — {t["label"]}')
        return

    to_run = args.test if args.test else list(TESTS.keys())
    invalid = [n for n in to_run if n not in TESTS]
    if invalid:
        print(f'Unknown tests: {invalid}')
        print(f'Available: {list(TESTS.keys())}')
        sys.exit(1)

    print(f'\n🧪 Liberty-Emporium Browser Test Suite')
    print(f'   Running {len(to_run)} test(s) in Chromium...\n')

    results = []
    for name in to_run:
        r = await run_test(name)
        results.append(r)

    # Summary
    passed  = [r for r in results if r['passed']]
    failed  = [r for r in results if not r['passed']]
    print(f'\n{"="*60}')
    print(f' RESULTS — {len(passed)}/{len(results)} passed')
    print('='*60)
    for r in results:
        icon = '✅' if r['passed'] else '❌'
        print(f' {icon}  [{r["app"]}] {r["label"]}  ({r["elapsed"]}s)')
    if failed:
        print(f'\n❌ FAILED:')
        for r in failed:
            print(f'  • {r["app"]}: {r["label"]}')
            print(f'    Output: {r["output"][:100]}')
    print('='*60)

if __name__ == '__main__':
    asyncio.run(main())
