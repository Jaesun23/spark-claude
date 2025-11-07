# SPARK v4.3 - AI Agent Orchestration System

**SPARK** (Subagent Performance Architecture with Reduced toKens) is a traits-based multi-agent orchestration system achieving 95.5% token reduction by loading only the required agent on-demand from a pool of 21 specialized agents.

**Constitution**: All agents follow SPARK Constitution v1.1

---

## 🎯 Core Architecture

### Three-Layer System

1. **Agent Layer** (21 specialists) - Expert identity with 7-section structure
2. **Command Layer** (12 workflows) - Complex multi-agent orchestration recipes
3. **Quality Gates** - Zero-tolerance verification system

### Token Efficiency

- **Progressive Disclosure**: Only descriptions loaded initially (~95 tokens/agent)
- **Full Load**: Agent body loaded only when selected (30-44K tokens)
- **Total Registry**: 21 agents = ~2.0K tokens (1% of context)

---

## 🤖 SPARK Agent Registry

### ✅ Core 4 Agents (Essential)

**analyzer-spark** - Multi-dimensional system analysis
- **Protocol**: EVIDENCE-BEFORE-REPORT + PROJECT-CONTEXT-DISCOVERY
- **Specialization**: 5-Phase Wave analysis, file:line evidence collection, 12+ items
- **When to Use**: System analysis, performance bottlenecks, security audits, technical debt evaluation
- **Output**: Evidence-based reports with concrete file:line references

**implementer-spark** - Feature implementation with zero defects
- **Protocol**: TEST-BEFORE-REPORT + PROJECT-CONTEXT-DISCOVERY
- **Specialization**: Phase 4 pytest mandatory, 95%+ coverage, 0 violations
- **When to Use**: API endpoints, authentication systems, database layers, UI components
- **Output**: Working code + comprehensive tests + 0 quality violations

**tester-spark** - Comprehensive testing
- **Protocol**: TEST-EXECUTION-BEFORE-REPORT
- **Specialization**: 95% unit, 85% integration, 100% E2E for critical paths
- **When to Use**: Test suite creation, coverage goal achievement, quality validation
- **Output**: Test suites with verified coverage metrics

**documenter-spark** - Technical documentation
- **Protocol**: VALIDATION-BEFORE-REPORT
- **Specialization**: Example code must execute, 100% API coverage
- **When to Use**: API docs, user guides, architecture documentation
- **Output**: Validated documentation with executable examples

### 🔧 Support 2 Agents (Optional)

**designer-spark** - System architecture design
- **Specialization**: Architecture patterns, API specifications, scalability design
- **When to Use**: New system design (> 3 hours complexity)

**qc-spark** - Quality violations cleanup
- **Specialization**: Ruff/MyPy fixes, 5-phase inspection, persist until success
- **When to Use**: Bulk fixes for 100+ violations

### 👥 Team Agents (15 - Parallel Execution)

5 teams × 3 roles (implementer, tester, documenter)
- **team1-{implementer,tester,documenter}-spark**
- **team2-{implementer,tester,documenter}-spark**
- **team3-{implementer,tester,documenter}-spark**
- **team4-{implementer,tester,documenter}-spark**
- **team5-{implementer,tester,documenter}-spark**

**When to Use**: `/multi-implement` command for parallel execution
**Principle**: Use only as many teams as tasks (2 tasks = team1, team2 only)

---

## 📋 Agent Delegation Protocol (MANDATORY)

### Provide Complete Project Context

When delegating work to agents, **ALWAYS provide project context**:

```python
# ✅ CORRECT: Complete task delegation with context
Task("implementer-spark", """
Task: Add user authentication endpoint

📋 Project Standards (MANDATORY - Read these first):
- PROJECT_STANDARDS.md - Logging, DB, error handling standards
- ARCHITECTURE.md - Layer structure, dependency rules
- docs/adr/*.md - Architecture decision records (if exist)

📂 Standard Modules (USE these, don't create new ones):
- common/logging/ - Use for all logging (don't use print or custom loggers)
- common/config/ - Use for all configuration
- common/db/ - Use for all database operations
- common/errors/ - Use for all error handling

⚠️ Quality Enforcement:
- Pre-commit hooks will verify compliance
- Quality gates will block if standards violated
- Do it right now to avoid rework later

If any required standards/modules are missing, STOP and request them.
""")

# ❌ WRONG: Task without context
Task("implementer-spark", "Add user authentication endpoint")
# Agent will guess, violate standards, fail quality gates
```

### Why This Matters

- **Proactive compliance**: Agent follows standards from the start
- **Avoid rework**: No `--no-verify` shortcuts or "fix later" excuses
- **Token efficiency**: Agent reads 3 docs (2K tokens) vs exploring randomly (50K tokens)
- **Quality gates pass**: First-time success instead of 3 retry cycles

### Information to Include

```typescript
interface AgentTask {
  // 1. Scope
  scope: string;           // What to work on

  // 2. Depth
  depth: "surface" | "moderate" | "deep";  // How deep to go

  // 3. Priorities
  priorities: string[];    // What matters most

  // 4. Constraints
  constraints: {
    time?: string;         // Time limit
    tokens?: number;       // Token budget
    specific?: string[];   // Specific requirements
  };

  // 5. Expected Output
  expectedOutput: string;  // What deliverable is needed
}
```

### Example: Good vs Bad Instructions

❌ **Bad** (incomplete):
```typescript
Task("analyzer-spark", "Analyze the system");
```

✅ **Good** (complete):
```typescript
Task("analyzer-spark", `
Task: Performance bottleneck analysis
Scope: API response time > 2 seconds
Depth: Function-level tracing
Priority: High-frequency endpoints
Output: 5 bottlenecks + file:line + solutions
`);
```

---

## 📁 State Management

### JSON State Files

```
~/.claude/workflows/current_task.json         # Main task state
~/.claude/workflows/team[1-5]_current_task.json  # Team-specific states
```

### State Structure

```json
{
  "id": "spark_YYYYMMDD_HHMMSS",
  "version": "4.3",
  "state": {
    "status": "pending|running|completed|failed"
  },
  "quality": {
    "violations_total": 0,
    "can_proceed": true
  }
}
```

### State Management Responsibilities

1. **Initialize**: Clear JSON state before agent call
2. **Verify**: Check state after agent completion
3. **Cleanup**: Delete state after successful completion

---

## ✅ Quality Verification

### Post-Completion Checklist

```python
def verify_agent_completion(agent_name: str) -> bool:
    """Verify agent work completion."""

    # 1. Read state file
    state = read_json("~/.claude/workflows/current_task.json")

    # 2. Check completion status
    if state["state"]["status"] != "completed":
        return False

    # 3. Check quality gates
    if not state["quality"]["can_proceed"]:
        return False

    # 4. Check violations
    if state["quality"]["violations_total"] != 0:
        return False

    # 5. Agent-specific validation
    if agent_name == "implementer-spark":
        # Must have test results
        if state["quality"]["step_6_testing"]["coverage"] < 0.95:
            return False

    return True
```

### Retry Strategy

- **1st Failure**: Provide general feedback
- **2nd Failure**: Point out specific issues
- **3rd Failure**: Provide explicit instructions
- **3+ Failures**: Escalate to user

### Quality Gates Execution

```bash
# Agent self-validation
echo '{"subagent": "implementer-spark", "self_check": true}' | \
python3 ~/.claude/hooks/spark_quality_gates.py

# Returns:
# ✅ "Quality gates PASSED"
# 🚫 "Quality gates FAILED"
```

---

## 🔄 Multi-Session Context Continuity

### Context Loss Prevention

> **Key Principle**: "Initial context is complete when you know everything, but later you'll forget"

Therefore:
- Initial documents: Write **as detailed as possible** when context is complete
- Document updates: Only need that one document, but initial creation needs all knowledge
- Checklists: **Lifeline** for future instances or agents

### Jason's 3-Phase Blueprint Process

**Phase 1: Blueprint** - Capture everything
- Purpose: Complete design document while context is intact
- Principle: Detailed enough for anyone to implement independently

**Phase 2: Task Breakdown** - Create LEGO blocks
- Purpose: Can't implement long blueprint at once, break into blocks
- Principle: Atomic task units, each 2-4 hours max

**Phase 3: Checklists** - Execution manual per block
- Purpose: Detailed checklist per task in separate files
- Principle: Self-contained execution (can execute with only that checklist)
- Result: All checklists complete = entire project complete

> **"If you can do it all at once, just use the blueprint. But when you can't, create 'complete' units even if it's tedious. Build the environment for success!"**

---

## 🔗 Agent Chain Patterns

### Basic Chain Patterns

**Full Implementation Chain**:
```
analyze → design → implement → test → document
```

**Refactoring Chain**:
```
analyze → implement → test
```

**Audit Chain**:
```
analyze → troubleshoot → document
```

**Migration Chain**:
```
analyze → design → implement → test
```

### Chain Execution Protocol

```python
async def execute_chain(agents: list, task: str):
    """Execute chain sequentially."""

    for i, agent in enumerate(agents):
        print(f"📍 Phase {i + 1}/{len(agents)}: {agent}")

        # Call agent
        await Task(agent, task)

        # Wait for completion
        await wait_for_completion()

        # Verify quality
        if not verify_quality():
            print("❌ Quality failed. Retrying...")
            await Task(agent, "Fix quality issues and rerun")

        print(f"✅ Phase {i + 1} complete!")
```

---

## 🚀 SPARK Commands

### Single Agent Commands

- `/spark-implement <feature>` - Feature implementation with quality gates
- `/spark-test <target>` - Create comprehensive tests (95% coverage target)
- `/spark-analyze <scope>` - Multi-dimensional system analysis
- `/spark-design <system>` - Architecture and API design
- `/spark-fix <issue>` - Troubleshoot and fix issues
- `/spark-improve <code>` - Performance optimization

### Pipeline Commands (Sequential Phases)

- `/spark-refactor <module>` - Refactor pipeline: analyze → improve → test
- `/spark-audit <system>` - Audit: analyze → troubleshoot → document
- `/spark-migrate <legacy>` - Migration: analyze → design → implement → test
- `/spark-optimize <scope>` - Optimize: analyze → improve → test
- `/spark-launch <feature>` - Complete: design → implement → test → document

### Parallel Execution

- `/multi-implement task1,task2,task3,task4,task5` - Execute up to 5 tasks in parallel

---

## 💡 SPARK Philosophy

### Zero-Tolerance Quality

- **Ruff violations**: 0
- **MyPy errors**: 0
- **Test coverage**: 95%+
- **All tests**: Pass

### Complete Deliverables

- Start = Finish
- No "Continue?" prompts
- Reject partial work
- Only deliver complete results

### Token Efficiency

- **Progressive Disclosure**: Load descriptions only (~95 tokens/agent)
- **On-Demand Loading**: Full agent body loaded only when selected
- **State Communication**: JSON files for agent-to-orchestrator communication
- **Safety Limits**: 90K token safety protocol in all agents

---

## 📊 Token Management

### Safety Limits

- **Hard limit**: 200K tokens per agent context
- **Practical limit**: 90K tokens (safety margin)
- **Write operations**: Double token consumption
- **Agent sizes**: ~1K (team agents) to ~3.9K (implementer-spark)

### Critical Rules

- Agents CANNOT call other agents (only orchestrator uses Task tool)
- Write operations consume 2x tokens (memory + output)
- All agents include 90K token safety protocol
- Compression available for 30-50% reduction

---

## 🎯 Common Pitfalls to Avoid

1. **Loading multiple agents unnecessarily** - Use one at a time
2. **Sequential Task calls for parallel work** - Must be simultaneous
3. **Skipping quality gate validation** - Always verify JSON state
4. **Not checking JSON after completion** - Critical for retry decisions
5. **Forgetting Write doubles token use** - Plan accordingly
6. **Task without project context** - Always provide standards/modules

---

## 📚 Key File Locations

- **Agent definitions**: `agents/*-spark.md` (in this plugin)
- **Command definitions**: `commands/spark-*.md` (in this plugin)
- **Quality gates script**: `~/.claude/hooks/spark_quality_gates.py`
- **JSON states**: `~/.claude/workflows/*.json`
- **Constitution**: `.claude/SPARK_CONSTITUTION.md` (in project)

---

## 🏆 SPARK Success Metrics

- **Token Reduction**: 95.5% (vs loading all agents)
- **Quality Gates**: Zero-tolerance (0 violations required)
- **Test Coverage**: 95%+ unit, 85%+ integration
- **Agent Count**: 21 specialists (6 core + 15 team)
- **Parallel Capacity**: 5 teams simultaneous execution

---

**Remember**: SPARK is not just a tool - it's a philosophy of quality, efficiency, and systematic excellence. Every agent follows Constitution v1.1, every deliverable meets zero-tolerance standards, and every execution is token-optimized through progressive disclosure.

Use SPARK agents when you need **verified quality**, not just quick results. 🚀
