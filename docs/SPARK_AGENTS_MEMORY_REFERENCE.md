# 🧠 SPARK Agents Memory Reference (Claude CODE Exclusive)

> **Core information for Claude CODE memory storage only**
> *Complex explanations removed, immediately actionable reference*

---

## 🎯 28 SPARK Agents Quick Selection Guide

### 🔥 Core 4 Agents (Highest Priority)
1. **implementer-spark** → Implementation (all personas auto-activated)
2. **analyzer-spark** → Analysis/debugging (multi-dimensional analysis)
3. **tester-spark** → Testing (95% coverage)
4. **designer-spark** → Design (architecture/UI/UX)

### 🎪 16 Base Agents + 12 Team Agents (28 Total)
**Base Agents**: analyzer, implementer, tester, designer, documenter, troubleshooter, improver, cleaner, explainer, estimator, gitter, builder, spawner, indexer, tasker, loader

**Team Agents**: team1-4 × (implementer, tester, documenter) = 12 specialized team agents

### 📊 Situation-Based Agent Matching

| Situation | Agent | Command Example |
|------|----------|-------------|
| "Fix bug" | troubleshooter-spark | `/spark-troubleshoot "fix login error"` |
| "Improve performance" | analyzer-spark → improver-spark | `/spark-analyze "find bottlenecks"` |
| "Write tests" | tester-spark | `/spark-test "create unit tests"` |
| "Create documentation" | documenter-spark | `/spark-document "API docs"` |
| "Clean up code" | cleaner-spark | `/spark-clean "remove dead code"` |
| "Explain" | explainer-spark | `/spark-explain "how auth works"` |
| "Estimate time" | estimator-spark | `/spark-estimate "new feature"` |
| "Git operations" | gitter-spark | `/spark-git "commit changes"` |
| "Build/Deploy" | builder-spark | `/spark-build "deploy to prod"` |
| "Multi-tasks" | spawner-spark | `/spark-spawn "parallel tasks"` |
| "Find command" | indexer-spark | `/spark-index "list commands"` |
| "Manage tasks" | tasker-spark | `/spark-task "manage todos"` |
| "Load project" | loader-spark | `/spark-load "project context"` |

---

## ⚡ Task Parallel Calling Pattern (Critical!)

```javascript
// ✅ Correct Pattern - True Parallel Execution
Task Task Task Task → Start!

// ❌ Wrong Pattern - Sequential Execution
Task 1 Complete → Task 2 Start → Task 3 Start
```

---

## 🎭 Persona Auto-Activation Keywords

| Persona | Trigger Keywords |
|----------|--------------|
| **Backend** | API, endpoint, service, database, server |
| **Frontend** | component, UI, responsive, style, React |
| **Security** | auth, security, vulnerability, OWASP |
| **Architecture** | complexity > 0.7, design, scalable |
| **DevOps** | deploy, CI/CD, pipeline, Docker |
| **Data** | data, analytics, database, ETL |
| **Testing** | test, coverage, TDD, unit |
| **Documentation** | document, readme, API docs |

---

## 🔧 Essential Agent Information

### implementer-spark (Implementation)
```json
{
  "task": "implementation content",
  "complexity": 0.1-1.0,  // 0.7+ = architecture mode
  "context": "existing code patterns"
}
```

### analyzer-spark (Analysis)
```json
{
  "target": "file/directory/system",
  "focus": ["performance", "security", "quality"],
  "depth": "quick|standard|deep"
}
```

### tester-spark (Testing)
```json
{
  "coverage_target": {"unit": 95, "integration": 85},
  "framework": "jest|pytest|mocha",
  "focus": ["edge_cases", "happy_path", "security"]
}
```

### designer-spark (Design)
```json
{
  "type": "architecture|api|ui",
  "requirements": ["functionality", "performance", "security"],
  "constraints": ["technical", "business", "regulatory"]
}
```

---

## 📊 Quality Gates (Jason's 8-Step)

1. **Syntax Validation** → 0 errors
2. **Type Checking** → mypy --strict (0 errors)
3. **Linting** → ruff --strict (0 violations)
4. **Security Analysis** → OWASP + secrets scan
5. **Test Coverage** → Unit 95%, Integration 85%
6. **Performance Check** → O(n) complexity, no N+1
7. **Documentation Validation** → Docstrings required
8. **Integration Testing** → E2E scenarios pass

---

## 🚀 Multi-Agent Pipelines

| Pipeline | Agent Sequence | Purpose |
|------------|--------------|------|
| **/spark-launch** | analyze → design → implement → test → document | Complete feature development |
| **/spark-refactor** | analyze → clean → improve → test | Code improvement |
| **/spark-audit** | analyze → troubleshoot → tester → documenter | Security/performance audit |
| **/spark-migrate** | analyze → design → implement → test → deploy | System migration |
| **/spark-optimize** | analyze → improve → test → build → deploy | Performance optimization |

---

## 🔴 Critical Constraints

1. **Agents cannot call other agents** (Only Claude CODE can use Task)
2. **Parallel execution requires single message with multiple Tasks** (Sequential calls = sequential execution)
3. **Information passed only via JSON context** (No direct communication)
4. **Quality gates auto-execute after SubagentStop**
5. **Maximum 3 retries** (On quality failures)
6. **FileLockManager prevents file conflicts** (Automatic parallel execution safety)

---

## 📁 State File Locations

```
~/.claude/workflows/current_task.json      # Global installation
.claude/workflows/current_task.json        # Project-specific
.claude/workflows/team1-4_current_task.json # Team-specific templates
```

**Fallback Pattern**: First check `~/.claude` → Then check `.claude`
**FileLockManager**: Prevents concurrent file access conflicts

---

## 🎯 Agent Selection Flow

```
1. Task Complexity Assessment
   → 0.7+ : Designer first
   → 0.3-0.7 : Implementer directly
   → 0.3- : Simple task

2. Task Type Assessment
   → Bug: Troubleshooter
   → New feature: Designer → Implementer
   → Improvement: Analyzer → Improver
   → Cleanup: Cleaner

3. Parallel Capability Assessment
   → Independent: Task Task Task → Start!
   → Dependent: Sequential execution
```

---

## 💡 Pro Tips

- **Token Savings**: Call only necessary agents (significant reduction on average)
- **Quality First**: All 8 quality gates must pass
- **Maximize Parallel**: Execute independent tasks simultaneously
- **Context Maintenance**: State management via JSON files
- **Leverage Retries**: Automatic 3-attempt retry on failures
- **File Safety**: FileLockManager prevents conflicts in parallel execution

---

*This document is optimized for Claude CODE memory storage.*
*For detailed information, see `/docs/SPARK_AGENTS_GUIDE.md`*