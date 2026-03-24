# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## SPARK's Core Purpose

SPARK is the **systematic enforcement layer** in Jason's development methodology — not just agent orchestration.

**Key Insight**: Guidelines that say "please do X" get ignored. System enforcement that **blocks** invalid states works.

```
[Human-Driven] Architecture → ADR → Blueprint (ultra-detailed)
─────────────────────────────────────── SPARK STARTS HERE ───
[SPARK-Enforced] Task Breakdown → Checklists → Implementation
```

SPARK enforces Jason's 3 principles from 5 failed projects:

1. **Very Specific Plans (Blueprint)**: "JWT-based auth with POST /auth/login, 5 failures → 30min lock, Redis 1hr TTL" — not "Build auth"
2. **Precise Instructions (Checklist)**: Each task item is testable and verifiable — not "Write tests for auth"
3. **Limited Context (Lego Blocks)**: Only the 30 lines of blueprint relevant to this task, not all 5000

### Enforcement over Guidelines

```python
# ❌ WEAK: "Please don't use print()" → AI ignores
# ✅ STRONG: System blocks it
if "print(" in code:
    BLOCK "❌ print() forbidden. Use structlog."
if mypy_errors > 0:
    BLOCK "❌ Type errors must be 0"
```

### 4-Layer Enforcement Design

```
Layer 1: Environment (Before) — Blueprint/standards exist? Tools installed?
Layer 2: Focus (During)       — Read ONLY specified blueprint lines, ONLY this checklist
Layer 3: Real-time (During)   — on_file_write: immediate ruff/mypy, print() block
Layer 4: Completion (After)   — Quality gates, pre-commit hooks, 0 violations
```

---

## Project Overview

SPARK (Subagent Performance Architecture with Reduced toKens) — traits-based multi-agent orchestration achieving 95.5% token reduction via on-demand agent loading.

- **Package version**: See `pyproject.toml`
- **Constitution**: `docs/docs-backup/constitution/1_CONSTITUTION.md`
- **Agents**: 7 core + 15 team = 22 total

## Development Commands

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e ".[full,dev,benchmark]"

# Quality checks
ruff check .                    # Linting
mypy .                          # Type checking
black . --check                 # Format checking
pytest tests/                   # All tests
pytest tests/test_specific.py   # Single test

# Benchmark
python benchmarks/run_benchmarks.py
```

## Project Structure

```
spark-plugin/                  # SPARK plugin (distributable)
├── agents/                    # 22 agent definitions (*-spark.md)
├── commands/                  # 12 workflow commands (spark-*.md, multi-implement.md)
├── hooks/                     # Hook scripts
├── skills/                    # Plugin skills
├── CLAUDE.md                  # Plugin-specific context (agent registry, delegation protocol)
└── README.md
docs/                          # Methodology guides & research
├── docs-backup/               # Archived docs (constitution, design guides)
│   └── constitution/          # SPARK Constitution v1.2
├── ADR_GUIDE.md
├── BLUEPRINT_GUIDE.md
├── CHECKLIST_GUIDE.md
├── TASK_BREAKDOWN_GUIDE.md
├── CORE_METHODOLOGY.md
└── PROJECT_STANDARDS_GUIDE.md
tests/                         # Test suites
benchmarks/                    # Performance benchmarks
```

## Core Agents (7)

| Agent | Purpose |
|-------|---------|
| `analyzer-spark` | Multi-dimensional system analysis, evidence-based |
| `implementer-spark` | Feature implementation, 95% test coverage |
| `tester-spark` | Comprehensive testing (95% unit, 85% integration) |
| `documenter-spark` | API docs, user guides, architecture docs |
| `designer-spark` | System architecture and API design |
| `qc-spark` | Quality violations cleanup, 5-phase inspection |
| `diagnostician-spark` | Systematic diagnosis and root cause analysis |

**Team Agents (15)**: 5 teams × 3 roles (implementer, tester, documenter) for parallel execution.

## SPARK Commands

### Single Agent
- `/spark-implement <feature>` — Feature implementation with quality gates
- `/spark-test <target>` — Comprehensive tests (95% coverage target)
- `/spark-analyze <scope>` — Multi-dimensional system analysis
- `/spark-design <system>` — Architecture and API design
- `/spark-fix <issue>` — Troubleshoot and fix issues
- `/spark-improve <code>` — Performance optimization
- `Task("qc-spark", "fix ruff violations")` — Quality violations (direct Task call)

### Pipeline (Sequential)
- `/spark-refactor <module>` — analyze → improve → test
- `/spark-audit <system>` — analyze → troubleshoot → document
- `/spark-migrate <legacy>` — analyze → design → implement → test
- `/spark-optimize <scope>` — analyze → improve → test
- `/spark-launch <feature>` — design → implement → test → document

### Parallel
- `/multi-implement task1,task2,...` — Up to 5 tasks in parallel via team agents

## Execution Protocol

When receiving SPARK commands:

```python
# Single agent:
1. Task("agent-name-spark", user_request)
2. WAIT for completion
3. CHECK quality state:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"
4. ✅ ALL MET → Success | ❌ ANY FAILED → Retry (max 3)

# Parallel (MUST be ONE message):
Task("team1-implementer-spark", task1)
Task("team2-implementer-spark", task2)
# ... up to team5
# WAIT for ALL
```

### Phase Structure

- **Phase 0**: Task Understanding (read instructions)
- **Phase 1-N**: Domain work (agent-specific, iterative)
- **Final Phase**: Quality verification (MANDATORY — 0 violations to proceed)

Agents use professional judgment, not mechanical checklists. Iteration between phases is expected.

## Token Management

- **Hard limit**: 200K tokens per agent
- **Practical limit**: 90K tokens (safety margin)
- **Write operations**: 2x token consumption
- Agents CANNOT call other agents (only Claude Code uses Task tool)

## JSON State Management

```
~/.claude/workflows/current_task.json           # Main task state
~/.claude/workflows/team[1-5]_current_task.json  # Team-specific states
```

```json
{
  "id": "spark_YYYYMMDD_HHMMSS",
  "state": {"status": "pending|running|completed|failed"},
  "quality": {"violations_total": 0, "can_proceed": true}
}
```

## Common Pitfalls

- Loading multiple agents unnecessarily (one at a time)
- Sequential Task calls for parallel work (must be simultaneous)
- Skipping quality gate verification
- Not checking state after agent completion
- Forgetting write operations double token use

## Key File Locations

| What | Where |
|------|-------|
| Agent definitions | `spark-plugin/agents/*-spark.md` |
| Command definitions | `spark-plugin/commands/spark-*.md`, `spark-plugin/commands/multi-implement.md` |
| Plugin context | `spark-plugin/CLAUDE.md` |
| Constitution | `docs/docs-backup/constitution/1_CONSTITUTION.md` |
| Methodology guides | `docs/*.md` |
| Tests | `tests/` |
| Benchmarks | `benchmarks/` |
