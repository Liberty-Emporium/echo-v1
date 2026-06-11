---
name: self-evolving-agents
description: Self-evolving AI agent patterns — autonomous skill discovery, reflection loops, experience-based learning, and continuous improvement without human intervention
version: 1.0.0
platforms: [linux, macos, windows]
---

# Self-Evolving Agents

## When to use
- Building agents that improve over time without human intervention
- Creating autonomous research agents
- Implementing reflection and self-correction patterns
- Designing multi-agent systems that share learned skills

## The Paradigm Shift (2026)

> "The era of static, manually-configured AI agents is over. 2026 is the year of self-evolving agents that learn, adapt, and improve autonomously."

The key insight: **agents don't just execute tasks — they learn from every execution**.

## Core Pattern: The Reflection Loop

```
┌──────────────────────────────────────────────────────────────┐
│                    REFLECTION LOOP                            │
│                                                              │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐ │
│  │ EXECUTE  │───►│ OBSERVE  │───►│ REFLECT  │───►│ EVOLVE │ │
│  │          │    │          │    │          │    │        │ │
│  │ Do the   │    │ What     │    │ What     │    │ Update │ │
│  │ task     │    │ happened?│    │ worked?  │    │ skills │ │
│  │          │    │          │    │ What      │    │        │ │
│  │          │    │          │    │ failed?   │    │        │ │
│  └─────────┘    └──────────┘    └──────────┘    └───┬────┘ │
│                                                      │      │
│                                                      ▼      │
│                                               ┌──────────┐ │
│                                               │  SHARE   │ │
│                                               │  (push   │ │
│                                               │  to git) │ │
│                                               └──────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## The 4 Stages of Self-Evolution

### Stage 1: Execute
Perform the task using current knowledge and skills.

### Stage 2: Observe
Record what happened:
- What was the input?
- What action was taken?
- What was the output?
- Were there any errors?
- How long did it take?

### Stage 3: Reflect
Analyze the outcome:
- Did it work? Why or why not?
- What could be done better?
- Is this a pattern (recurring success or failure)?
- What's the general principle here?

### Stage 4: Evolve
Update the agent's knowledge:
- Save new skill to procedural memory
- Update success/failure statistics
- Modify approach for next time
- Share learnings with other agents

## Implementation: Reflection Engine

```python
import json
from datetime import datetime
from pathlib import Path

class ReflectionEngine:
    def __init__(self, memory_dir="~/.hermes/memory"):
        self.memory_dir = Path(memory_dir).expanduser()
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.experience_file = self.memory_dir / "experiences.jsonl"
        self.skills_file = self.memory_dir / "learned_skills.json"

    def execute_with_reflection(self, task_name, action_fn, context=None):
        """Execute a task and learn from the result."""
        start_time = datetime.now()
        error = None
        result = None

        try:
            result = action_fn()
            success = True
        except Exception as e:
            error = str(e)
            success = False
            result = None

        duration = (datetime.now() - start_time).total_seconds()

        # Record experience
        experience = {
            "task": task_name,
            "success": success,
            "error": error,
            "duration": duration,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }
        self._append_experience(experience)

        # Reflect and evolve
        if success:
            self._learn_from_success(task_name, experience)
        else:
            self._learn_from_failure(task_name, experience)

        if error:
            raise  # Re-raise after logging
        return result

    def _append_experience(self, experience):
        with open(self.experience_file, "a") as f:
            f.write(json.dumps(experience) + "\n")

    def _learn_from_success(self, task_name, experience):
        """Extract what worked and save as a skill."""
        skills = self._load_skills()
        if task_name not in skills:
            skills[task_name] = {
                "attempts": 0,
                "successes": 0,
                "avg_duration": 0,
                "last_success": None,
                "tips": []
            }

        s = skills[task_name]
        s["attempts"] += 1
        s["successes"] += 1
        s["avg_duration"] = (
            (s["avg_duration"] * (s["successes"] - 1) + experience["duration"])
            / s["successes"]
        )
        s["last_success"] = experience["timestamp"]
        self._save_skills(skills)

    def _learn_from_failure(self, task_name, experience):
        """Extract what went wrong and how to avoid it."""
        skills = self._load_skills()
        if task_name not in skills:
            skills[task_name] = {
                "attempts": 0,
                "successes": 0,
                "failures": [],
                "tips": []
            }

        s = skills[task_name]
        s["attempts"] += 1
        s["failures"].append({
            "error": experience["error"],
            "timestamp": experience["timestamp"],
            "context": experience["context"]
        })
        # Keep only last 10 failures
        s["failures"] = s["failures"][-10:]
        self._save_skills(skills)

    def get_success_rate(self, task_name):
        skills = self._load_skills()
        if task_name in skills:
            s = skills[task_name]
            if s["attempts"] > 0:
                return s["successes"] / s["attempts"]
        return 0.0

    def get_tips(self, task_name):
        """Get learned tips for a task."""
        skills = self._load_skills()
        if task_name in skills:
            return skills[task_name].get("tips", [])
        return []

    def _load_skills(self):
        if self.skills_file.exists():
            return json.loads(self.skills_file.read_text())
        return {}

    def _save_skills(self, skills):
        self.skills_file.write_text(json.dumps(skills, indent=2))
```

## Skill Discovery Pattern

Agents can discover new skills by analyzing their experience history:

```python
class SkillDiscovery:
    def __init__(self, reflection_engine):
        self.engine = reflection_engine

    def discover_patterns(self):
        """Analyze experience history to discover reusable patterns."""
        experiences = self._load_experiences()

        # Group by task type
        by_task = {}
        for exp in experiences:
            task = exp["task"]
            if task not in by_task:
                by_task[task] = []
            by_task[task].append(exp)

        # Find patterns
        patterns = []
        for task, exps in by_task.items():
            successes = [e for e in exps if e["success"]]
            failures = [e for e in exps if not e["success"]]

            if len(successes) >= 3:
                # Reliable pattern found
                avg_duration = sum(e["duration"] for e in successes) / len(successes)
                patterns.append({
                    "type": "reliable_skill",
                    "task": task,
                    "success_rate": len(successes) / len(exps),
                    "avg_duration": avg_duration,
                    "recommendation": f"Task '{task}' is reliable ({len(successes)}/{len(exps)} successes)"
                })

            if len(failures) >= 3:
                # Recurring problem
                error_types = {}
                for f in failures:
                    err = f["error"].split(":")[0]
                    error_types[err] = error_types.get(err, 0) + 1
                most_common = max(error_types, key=error_types.get)
                patterns.append({
                    "type": "recurring_problem",
                    "task": task,
                    "most_common_error": most_common,
                    "count": error_types[most_common],
                    "recommendation": f"Task '{task}' frequently fails with: {most_common}"
                })

        return patterns

    def generate_skill_suggestions(self):
        """Generate new skill suggestions based on patterns."""
        patterns = self.discover_patterns()
        suggestions = []
        for p in patterns:
            if p["type"] == "reliable_skill" and p["success_rate"] > 0.8:
                suggestions.append({
                    "action": "formalize_skill",
                    "task": p["task"],
                    "reason": f"High success rate ({p['success_rate']:.0%})"
                })
            elif p["type"] == "recurring_problem":
                suggestions.append({
                    "action": "investigate_and_fix",
                    "task": p["task"],
                    "reason": f"Recurring error: {p['most_common_error']}"
                })
        return suggestions
```

## Multi-Agent Skill Sharing

When one agent learns something, it should share with others:

```python
class SkillSharing:
    def __init__(self, skill_repo_path="~/agent-skills"):
        self.repo_path = Path(skill_repo_path).expanduser()

    def share_skill(self, skill_name, skill_content, source_agent):
        """Share a learned skill with other agents via git."""
        skill_dir = self.repo_path / "learned" / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Write SKILL.md
        skill_md = f"""---
name: {skill_name}
description: Auto-learned skill from {source_agent}
version: 1.0.0
platforms: [linux, macos, windows]
---

# {skill_name}

> Auto-learned by {source_agent} on {datetime.now().strftime('%Y-%m-%d')}

{skill_content}
"""
        (skill_dir / "SKILL.md").write_text(skill_md)

        # Push to shared repo
        os.system(f"cd {self.repo_path} && git add . && git commit -m 'Learn: {skill_name} from {source_agent}' && git push")

    def pull_new_skills(self):
        """Pull new skills learned by other agents."""
        os.system(f"cd {self.repo_path} && git pull")
```

## Research Sources (2026)

### Key Papers
- "A Survey of Self-Evolving Agents: On Path to Artificial Super Intelligence" (arXiv:2507.21046)
- "Self-Improving AI Agents: RL and Continual Learning" (Samsung Research)
- Andrej Karpathy's Auto-Research: AI Self-Improvement

### Key Frameworks
- **EvoScientist** — outperforms 7 open-source systems in scientific idea generation
- **GenericAgent** — self-evolving agent framework
- **Open Agents** — open-source self-evolving agents
- **SOL Framework** — Self-Initiated Open World Learning

### Key Insight from Reddit (r/singularity)
> "Continual Learning is Solved in 2026" — The research problems are now algorithmic/applied math problems, not fundamental barriers.

## Best Practices

1. **Always reflect** — Every task execution should produce a learning
2. **Rate importance** — Failures are more important than successes
3. **Share immediately** — Don't hoard knowledge, push to shared repo
4. **Verify before trusting** — New skills should be tested before relying on them
5. **Prune bad skills** — If a skill consistently fails, remove it
6. **Combine with memory** — Self-evolution requires persistent memory
7. **Set boundaries** — Agents should not modify their own core code without approval

## Pitfalls
- Don't let agents modify their own prompt/system message
- Don't allow unbounded self-modification — set clear boundaries
- Don't trust untested skills — verify before using in production
- Don't forget to back up — learned skills are valuable
- Don't let reflection loops run infinitely — set max iterations

## Verification
```python
# Test reflection engine
engine = ReflectionEngine("/tmp/test-memory")

# Simulate successful task
result = engine.execute_with_reflection(
    "test_task",
    lambda: "success",
    context={"input": "test"}
)
assert result == "success"
assert engine.get_success_rate("test_task") == 1.0

# Simulate failing task
try:
    engine.execute_with_reflection(
        "failing_task",
        lambda: (_ for _ in ()).throw(Exception("test error"))
    )
except:
    pass
assert engine.get_success_rate("failing_task") == 0.0

print("Reflection engine: OK")
```
