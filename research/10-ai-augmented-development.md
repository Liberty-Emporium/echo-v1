# AI-Augmented Development
_Research compiled: 2026-04-22_

---

## 1. Code Generation Evaluation (Not Just Generation)

The hardest part isn't generating code — it's knowing whether generated code is correct, safe, and production-ready.

### Evaluation Framework for Generated Code

**Correctness Checks:**
1. **Syntax validity** — does it parse without errors?
2. **Type correctness** — do types match? (`tsc --noEmit`, `mypy`, `pyright`)
3. **Test passage** — run existing test suite
4. **Edge case coverage** — null inputs, empty arrays, max values, concurrent access
5. **Logic correctness** — does the algorithm actually solve the stated problem?

**Quality Checks:**
1. **Security scan** — `bandit` (Python), `semgrep`, `npm audit`, `eslint-plugin-security`
2. **Static analysis** — `ruff`, `pylint`, `eslint`, `sonarqube`
3. **Dependency safety** — are new imports trustworthy?
4. **Idempotency** — can this run twice safely?
5. **Error handling** — what happens when it fails?

**Integration Checks:**
1. **API contract** — does it match the interface callers expect?
2. **DB schema** — are column names/types correct?
3. **Environment assumptions** — does it assume env vars, files, services that exist?
4. **Backward compatibility** — does it break existing callers?

### The "Works on First Try" Trap
Generated code that *appears* to work is the most dangerous kind:
```python
# AI generated — looks correct, has subtle bug
def get_user_orders(user_id):
    orders = db.execute(f"SELECT * FROM orders WHERE user_id = {user_id}")
    # SQL injection vulnerability — slipped past visual review
    return orders.fetchall()
```

**Rule: Treat AI-generated code as untrusted code review, not trusted colleague code.**

### Automated Evaluation Pipeline
```
Generated Code
    ↓
Static Analysis (linter, type checker)
    ↓
Security Scan (bandit/semgrep)
    ↓
Unit Tests (existing test suite)
    ↓
Integration Tests (spin up test DB, call endpoints)
    ↓
Review diff (what changed vs before)
    ↓
Human approval gate (for production changes)
```

---

## 2. Self-Debugging Loops

AI agents can debug themselves by executing code, reading errors, and iterating.

### Effective Self-Debugging Pattern
```
1. Write code
2. Execute
3. Read error/output
4. Hypothesize root cause
5. Make targeted fix (smallest possible change)
6. Re-execute
7. Verify fix didn't break other things
```

### Common Self-Debugging Pitfalls
**Pitfall 1: Chasing symptoms, not root cause**
```
Error: AttributeError: 'NoneType' has no attribute 'id'
Bad fix: add `if result is not None:` everywhere
Good fix: understand why result is None — DB query returns nothing, wrong ID, etc.
```

**Pitfall 2: Over-engineering the fix**
```
Bug: function returns wrong value for edge case
Bad fix: rewrite entire function
Good fix: add targeted edge case handling
```

**Pitfall 3: Breaking other things**
Always run the test suite after each fix. A fix that resolves one error but breaks 5 tests is not a fix.

**Pitfall 4: Infinite retry loops**
Set a maximum iteration count. If not fixed in N attempts, escalate (ask human, add logging, take different approach).

### Instrumentation for Debugging
```python
# Add strategic logging before debugging runs
import logging
logging.basicConfig(level=logging.DEBUG)

# Add type assertions at function boundaries
def process_order(order_id: int) -> dict:
    assert isinstance(order_id, int), f"Expected int, got {type(order_id)}"
    result = db.get_order(order_id)
    assert result is not None, f"Order {order_id} not found"
    return result
```

---

## 3. Tool Use & Environment Awareness

### What Good Tool Use Looks Like
1. **Right tool for the job** — don't use a shell command when a library call exists
2. **Check before acting** — read file before editing; check if service exists before calling
3. **Minimal footprint** — don't install unnecessary dependencies
4. **Idempotent actions** — operations that can be safely repeated
5. **Rollback awareness** — know how to undo what you did

### Environment Awareness Checklist
Before executing any code:
- What OS/environment is this? (production vs dev vs test)
- What permissions do I have?
- What services are available? (DB, Redis, external APIs)
- What are the current env vars?
- Is this a stateful operation? Can it be undone?
- What's the blast radius if this fails?

```bash
# Gather environment context
python3 --version
pip list | grep -E "flask|sqlalchemy|redis"
echo $DATABASE_URL
ps aux | grep gunicorn
df -h  # disk space
free -m  # memory
```

### Tool Composition Patterns
**Read-before-write:**
```python
# Always read current state before modifying
content = read_file('config.json')
config = json.loads(content)
config['new_key'] = 'value'
write_file('config.json', json.dumps(config, indent=2))
```

**Dry-run first:**
```bash
# Test what would happen before doing it
rsync --dry-run -av src/ dest/
git diff --stat HEAD  # see what changed before committing
```

**Targeted changes:**
```python
# Don't replace the whole file — make surgical edits
# Bad: rewrite entire 500-line config
# Good: find the one setting that needs changing
```

---

## 4. Planning vs Execution Separation

### The Planning Phase
Before writing any code, a good AI agent should:
1. **Understand the task** — what's the actual goal, not just the stated request?
2. **Identify unknowns** — what do I need to know that I don't know?
3. **Map dependencies** — what does this change touch?
4. **Define success criteria** — how will I know it worked?
5. **Identify risks** — what could go wrong?
6. **Plan rollback** — how do I undo this if it fails?

### The Execution Phase
1. **Small, verifiable steps** — don't write 500 lines without testing
2. **Test each step** — run, verify, then continue
3. **Commit checkpoints** — working state before big changes
4. **Compare actual vs expected** at each step
5. **Stop if assumptions violated** — don't continue blindly

### When to Re-Plan vs Push Through
**Re-plan when:**
- The error reveals a fundamentally wrong assumption
- The scope has grown significantly
- A dependency doesn't exist as expected
- Security/safety concern discovered

**Push through when:**
- It's a syntax error or typo
- The fix is clear and targeted
- Tests still pass after fix

### Task Decomposition
Complex tasks should be decomposed into independent subtasks:
```
Task: "Add Stripe payments to FloodClaim Pro"

Subtasks:
1. Read current order/payment model in app.py
2. Check existing Stripe integration patterns in our other apps
3. Add Stripe checkout route (isolated, testable)
4. Add webhook handler (isolated)
5. Update order model with payment status fields
6. Add payment UI to templates
7. Test with Stripe test mode
8. Deploy and verify

Each subtask: plan → implement → test → commit
```

---

## 5. Prompt Engineering for Code Tasks

### Effective Code Generation Prompts
```
BAD:  "Write a function to handle payments"
GOOD: "Write a Flask route at POST /payments/create that:
       - Accepts JSON: {order_id, amount_cents, stripe_token}
       - Validates order exists in SQLite DB via order_id
       - Creates Stripe PaymentIntent using stripe.PaymentIntents.create()
       - Updates order.status to 'paid' and order.stripe_pi to payment intent ID
       - Returns JSON: {success: true, pi_id: ...} or {error: ...}
       - Uses existing get_db() pattern from line 35 of app.py
       - Handles stripe.error.CardError specifically"
```

### Context is Everything
The more context provided, the better the output:
- **Existing code patterns** — "use the same pattern as the login route"
- **Database schema** — exact column names and types
- **Error examples** — "it fails with this traceback..."
- **Constraints** — "must not use external libraries", "must work with Python 3.9"
- **What was already tried** — "I tried X and got error Y"

### Iterative Refinement
```
Round 1: Generate basic implementation
Round 2: "Now add error handling for when the DB is locked"
Round 3: "Add input validation — order_id must be int, amount must be > 0"
Round 4: "Add a test for this function"
```

---

## 6. Agent Architecture Patterns

### ReAct (Reasoning + Acting)
```
Thought: I need to find the kitchen route bug
Action: grep for "/kitchen" in app.py
Observation: Found route at line 1134
Thought: The query uses t.location — check if that column exists
Action: Read _ensure_kitchen_tables function
Observation: Column not guaranteed on old DBs
Thought: Need ALTER TABLE migration
Action: Add migration code
Observation: Syntax OK, tests pass
Thought: Deploy fix
Action: git commit && git push
```

### Tool-Augmented LLMs
Modern AI agents are most effective with:
- **Code execution** — run and verify, not just generate
- **File system access** — read real code, not hallucinate it
- **Web search** — get current docs, not training data (which may be stale)
- **Memory** — persist context across sessions (exactly what echo-v1 is!)
- **Shell access** — run tests, check services, examine logs

### Key Agent Failure Modes
1. **Hallucination** — inventing API methods that don't exist
2. **Context loss** — forgetting constraints set earlier in conversation
3. **Scope creep** — solving adjacent problems not asked for
4. **Overconfidence** — deploying untested changes
5. **Loop behavior** — retrying same failing approach
6. **Anchoring** — fixating on first hypothesis even when wrong

### Mitigations
1. **Read actual source code** — don't trust memory for API signatures
2. **Verify before acting** — check the thing exists before modifying it
3. **Short feedback loops** — test after every change
4. **Explicit constraints** — restate requirements before each implementation step
5. **Diversity of approaches** — if approach A fails twice, try approach B
6. **Human checkpoints** — escalate uncertain decisions

---

## Key Takeaways
1. **Eval > generate** — knowing if code is correct matters more than generating it fast
2. **Automated test pipelines** — run linter + security scan + tests on every generated change
3. **Self-debugging needs constraints** — max retries, root cause focus, test verification
4. **Environment awareness first** — understand context before acting
5. **Plan → small steps → verify → repeat** — not "generate and pray"
6. **Specific prompts** — exact schemas, patterns, constraints → better output
7. **Tools make agents real** — execution + file access + memory = capability

---
_Sources: ReAct paper (Yao et al.), Reflexion paper, LangChain agent docs, OpenAI function calling docs, experience_
