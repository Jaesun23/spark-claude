# SPARK v4.1 Agent System - Essential Guide for Claude Code

## 🎯 Core Architecture Rules
1. **Only Claude Code can use Task tool** - Agents CANNOT call other agents
2. **Parallel execution requires synchronization** - ALL agents must complete before proceeding
3. **Use single message with multiple Task calls** for true parallel execution (not sequential)

## 📚 28 SPARK Agents Overview

### Primary Agents (16)
1. **analyzer-spark** - Multi-dimensional system analysis with 5-phase methodology
2. **implementer-spark** - Builds production-ready features with 95% test coverage
3. **tester-spark** - Comprehensive testing (95% unit, 85% integration coverage)
4. **designer-spark** - Creates system designs and API specifications
5. **documenter-spark** - Creates API docs, user guides, architecture documents
6. **improver-spark** - Refactoring, optimization, technical debt reduction
7. **troubleshooter-spark** - Systematic debugging and issue resolution
8. **cleaner-spark** - Removes dead code, updates dependencies
9. **explainer-spark** - Explains concepts, patterns, and code
10. **builder-spark** - Optimizes build processes, CI/CD pipelines
11. **estimater-spark** - Evidence-based time and resource estimation
12. **gitter-spark** - Git strategy, branching, automation
13. **loader-spark** - Analyzes and loads project context
14. **indexer-spark** - Helps navigate SuperClaude commands
15. **tasker-spark** - Multi-session project management
16. **spawner-spark** - Coordinates complex multi-agent operations

### Team Agents (12) - For Parallel Execution
- **team1-implementer-spark**, **team1-tester-spark**, **team1-documenter-spark**
- **team2-implementer-spark**, **team2-tester-spark**, **team2-documenter-spark**
- **team3-implementer-spark**, **team3-tester-spark**, **team3-documenter-spark**
- **team4-implementer-spark**, **team4-tester-spark**, **team4-documenter-spark**

## 🎮 Command Patterns & Execution Types

### Single Agent Commands (Sequential)
```bash
/spark-implement "feature"    → implementer-spark
/spark-test "target"          → tester-spark  
/spark-analyze "scope"        → analyzer-spark
/spark-design "system"        → designer-spark
/spark-clean "project"        → cleaner-spark
/spark-fix "issue"            → troubleshooter-spark
```

### Agent Chaining Commands (Sequential Phases)
```bash
/spark "complex task"         → analyzer → implementer → tester → documenter
/spark-refactor "module"      → analyzer → improver → tester
/spark-audit "system"         → analyzer → troubleshooter → documenter
/spark-migrate "legacy"       → analyzer → designer → implementer → tester
```

### Parallel Execution Commands ⚠️ CRITICAL
```bash
/multi-implement task1,task2,task3,task4
```

## ⚠️ Critical Execution Rules for Claude Code

### For Parallel Execution - MUST READ:

#### ✅ CORRECT - All Task calls in ONE message
```python
# Single message with multiple Task invocations
Task("team1-implementer-spark", "Backend API endpoints")
Task("team2-implementer-spark", "Database layer") 
Task("team3-implementer-spark", "Authentication system")
Task("team4-implementer-spark", "Frontend components")
# All 4 agents start simultaneously
```

#### ❌ WRONG - Sequential messages break parallelism
```python
# First message
Task("team1-implementer-spark", task1)
# Wait for response...

# Second message (THIS BREAKS PARALLELISM!)
Task("team2-implementer-spark", task2)
```

### Common Mistakes to Avoid:
1. **Using generic agent for team tasks**: 
   - ❌ `Task("implementer-spark", "Team1: backend")`
   - ✅ `Task("team1-implementer-spark", "backend")`

2. **Sequential Task calls in separate messages**:
   - ❌ Call Task, wait for result, call next Task
   - ✅ Call all Tasks in one message, then wait

3. **Checking progress during parallel execution**:
   - ❌ Check team1 status while team2 is running
   - ✅ Wait for ALL teams to complete before checking

### Information to Provide to Agents:
1. **Always include**: Task context, requirements, constraints
2. **For improvements**: Current problems, desired outcomes
3. **For testing**: Coverage targets, test types needed
4. **For documentation**: Target audience, format required

### Quality Gates (v4.1 - Automatic):
All agents must achieve:
- **Syntax**: 0 errors required
- **Type checking**: 0 errors (MyPy strict)
- **Linting**: 0 violations (Ruff strict)
- **Security**: No hardcoded secrets
- **Test Coverage**: Unit 95%, Integration 85%
- **Documentation**: All functions documented

## 🚀 Immediate Action Protocol

When receiving commands, Claude Code should:
1. **Identify pattern**: Single, chaining, or parallel
2. **For single**: Call agent immediately with requirements
3. **For chaining**: Execute phases sequentially, wait for each
4. **For parallel**: Call ALL agents in ONE message, wait for ALL
5. **Never**: Check individual progress during parallel execution
6. **Always**: Wait for SubagentStop hook before proceeding

## 📊 Token Efficiency
- **Traditional**: 44,000 tokens (loads all agents)
- **SPARK v4.1**: 5,100 tokens (loads only needed agent)
- **Savings**: 88.4% reduction per request
- **90K token safety limit** per agent context

## 🔄 JSON State Management (v4.1)

### Files Used for Coordination:
```
~/.claude/workflows/
├── current_task.json           # Main task state
├── team1_current_task.json     # Team 1 state
├── team2_current_task.json     # Team 2 state
├── team3_current_task.json     # Team 3 state
├── team4_current_task.json     # Team 4 state
└── task_aborted.json           # Abort signals
```

### Important: How Agents Record Their Work
- **Agents READ JSON files** to understand their task
- **Agents NEVER WRITE JSON files directly** (prevents race conditions)
- **Agents REPORT progress via print statements** (e.g., `print("Phase 1: Complete")`)
- **Orchestrator hooks READ agent output** and update JSON files
- **Quality gates hook VALIDATES output** and records results in JSON
- This separation ensures thread-safety in parallel execution

## 💡 Quick Reference for Common Tasks

### Need to implement multiple features?
```python
# Use team agents in parallel
Task("team1-implementer-spark", "Feature A")
Task("team2-implementer-spark", "Feature B")
Task("team3-implementer-spark", "Feature C")
Task("team4-implementer-spark", "Feature D")
```

### Need to analyze then fix?
```python
# Sequential chaining
Task("analyzer-spark", "Analyze performance issues")
# Wait for completion
Task("troubleshooter-spark", "Fix identified issues")
```

### Need comprehensive project work?
```python
# Use spawner for complex orchestration
Task("spawner-spark", "Deploy full-stack application with monitoring")
```

## 📝 Remember:
- You (Claude Code) are the orchestrator
- Agents are your specialists
- Direct them wisely with complete requirements
- Always maintain parallel discipline
- Never let agents modify JSON files directly