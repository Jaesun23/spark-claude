# SPARK Plugin — Agent Orchestration System

SPARK (Subagent Performance Architecture with Reduced toKens) — traits-based multi-agent orchestration with 95.5% token reduction via on-demand agent loading.

All agents follow SPARK Constitution v1.2 (`docs/docs-backup/constitution/1_CONSTITUTION.md`).

---

## Agent Registry

### Core Agents (7)

**analyzer-spark** — Multi-dimensional system analysis
- Protocol: EVIDENCE-BEFORE-REPORT + PROJECT-CONTEXT-DISCOVERY
- Specialization: 5-Phase Wave analysis, file:line evidence, 12+ items
- When: System analysis, bottlenecks, security audits, tech debt

**implementer-spark** — Feature implementation with zero defects
- Protocol: TEST-BEFORE-REPORT + PROJECT-CONTEXT-DISCOVERY
- Specialization: Phase 4 pytest mandatory, 95%+ coverage, 0 violations
- When: API endpoints, auth, database layers, UI components

**tester-spark** — Comprehensive testing
- Protocol: TEST-EXECUTION-BEFORE-REPORT
- Specialization: 95% unit, 85% integration, 100% E2E critical paths
- When: Test suite creation, coverage goals, quality validation

**documenter-spark** — Technical documentation
- Protocol: VALIDATION-BEFORE-REPORT
- Specialization: Executable examples, 100% API coverage
- When: API docs, user guides, architecture documentation

**designer-spark** — System architecture design
- Specialization: Architecture patterns, API specs, scalability
- When: New system design (> 3 hours complexity)

**qc-spark** — Quality violations cleanup
- Specialization: Ruff/MyPy fixes, 5-phase inspection, persist until success
- When: Bulk fixes for 100+ violations

**diagnostician-spark** — Systematic diagnosis
- Specialization: Root cause analysis, convergent investigation
- When: Vague errors, failed debugging attempts, system health assessment

### Team Agents (15 — Parallel Execution)

5 teams × 3 roles (implementer, tester, documenter):
- `team[1-5]-implementer-spark`
- `team[1-5]-tester-spark`
- `team[1-5]-documenter-spark`

Use only as many teams as tasks (2 tasks = team1, team2 only).

---

## Agent Delegation Protocol (MANDATORY)

When delegating work to agents, **always provide complete context**:

```python
# ✅ CORRECT: Complete task delegation
Task("implementer-spark", """
Task: Add user authentication endpoint

📋 Project Standards (MANDATORY):
- PROJECT_STANDARDS.md — Logging, DB, error handling
- ARCHITECTURE.md — Layer structure, dependency rules

📂 Standard Modules (USE these, don't create new):
- common/logging/ — All logging
- common/config/ — All configuration
- common/db/ — All database operations
- common/errors/ — All error handling

⚠️ Quality Enforcement:
- Pre-commit hooks verify compliance
- Quality gates block if standards violated
""")

# ❌ WRONG: Task without context
Task("implementer-spark", "Add user authentication endpoint")
# Agent will guess, violate standards, fail quality gates
```

### Why This Matters
- **Proactive compliance**: Agent follows standards from the start
- **Token efficiency**: Agent reads 3 docs (~2K tokens) vs exploring randomly (~50K tokens)
- **First-time success**: No retry cycles

### Task Structure

```typescript
interface AgentTask {
  scope: string;              // What to work on
  depth: "surface" | "moderate" | "deep";
  priorities: string[];       // What matters most
  constraints: {
    time?: string;
    tokens?: number;
    specific?: string[];
  };
  expectedOutput: string;     // Expected deliverable
}
```

---

## Quality Verification

### Post-Completion Check

1. Read state: `~/.claude/workflows/current_task.json`
2. `state.status == "completed"`
3. `quality.can_proceed == true`
4. `quality.violations_total == 0`

### Retry Strategy

- **1st failure**: General feedback
- **2nd failure**: Point out specific issues
- **3rd failure**: Explicit instructions
- **3+ failures**: Escalate to user

---

## Multi-Session Context

> "Initial context is complete when you know everything, but later you'll forget"

- Initial documents: Write **as detailed as possible** when context is intact
- Checklists: **Lifeline** for future instances or agents
- Blueprint → Task Breakdown → Checklists: each self-contained and executable

---

## Plugin File Structure

```
agents/          # 22 agent definitions (*-spark.md)
commands/        # 12 workflow commands (spark-*.md, multi-implement.md)
hooks/           # Hook scripts
skills/          # Plugin skills
CLAUDE.md        # This file
README.md
```
