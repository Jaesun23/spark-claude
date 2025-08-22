# Multi-Implement Command Guide

## Common Mistakes and Solutions

### ❌ Problem: Using Generic Agent Instead of Team Agents

**Wrong:**
```python
Task("implementer-spark", "Team 1: Implement API")
Task("implementer-spark", "Team 2: Implement Database") 
```

**Correct:**
```python
Task("team1-implementer-spark", "Implement API")
Task("team2-implementer-spark", "Implement Database")
```

**Why it matters:** 
- Generic agents don't read team-specific JSON files
- Breaks true parallel execution
- Causes confusion about task ownership

### ❌ Problem: Adding Team Prefix to Task Description

**Wrong:**
```python
Task("team1-implementer-spark", "Team 1: Implement API")
```

**Correct:**
```python
Task("team1-implementer-spark", "Implement API")
```

**Why it matters:**
- Team agents already know their team number
- They automatically read from team#_current_task.json
- Redundant prefixes cause confusion

### ❌ Problem: Sequential Task Calls

**Wrong:**
```python
# Message 1
Task("team1-implementer-spark", "...")
# Wait for result
# Message 2
Task("team2-implementer-spark", "...")
```

**Correct:**
```python
# Single Message with all calls
Task("team1-implementer-spark", "...")
Task("team2-implementer-spark", "...")
Task("team3-implementer-spark", "...")
Task("team4-implementer-spark", "...")
```

**Why it matters:**
- Sequential calls defeat the purpose of parallel execution
- Dramatically slower (no speed benefit)
- Wastes the multi-team architecture

## Pre-Execution Checklist

Before running /multi-implement:

- [ ] ✅ Using `team1-implementer-spark`, NOT `implementer-spark`
- [ ] ✅ Using `team2-implementer-spark`, NOT `implementer-spark`
- [ ] ✅ Using `team3-implementer-spark`, NOT `implementer-spark`
- [ ] ✅ Using `team4-implementer-spark`, NOT `implementer-spark`
- [ ] ✅ NO "Team1:" prefix in task descriptions
- [ ] ✅ All Task calls in ONE message
- [ ] ✅ Team JSON files will be auto-created

## Available Team Agents

```
Team 1: team1-implementer-spark, team1-tester-spark, team1-documenter-spark
Team 2: team2-implementer-spark, team2-tester-spark, team2-documenter-spark
Team 3: team3-implementer-spark, team3-tester-spark, team3-documenter-spark
Team 4: team4-implementer-spark, team4-tester-spark, team4-documenter-spark
```

**Never use for multi-implement:**
- `implementer-spark` (single task only)
- `tester-spark` (single task only)
- `documenter-spark` (single task only)

## Execution Flow

### Phase 1: Implementation (Parallel)
```python
# All in ONE message
Task("team1-implementer-spark", task1)
Task("team2-implementer-spark", task2)
Task("team3-implementer-spark", task3)
Task("team4-implementer-spark", task4)
```

### Phase 2: Testing (Parallel)
```python
# All in ONE message
Task("team1-tester-spark", "Test Team 1 implementation")
Task("team2-tester-spark", "Test Team 2 implementation")
Task("team3-tester-spark", "Test Team 3 implementation")
Task("team4-tester-spark", "Test Team 4 implementation")
```

### Phase 3: Documentation (Parallel)
```python
# All in ONE message
Task("team1-documenter-spark", "Document Team 1 work")
Task("team2-documenter-spark", "Document Team 2 work")
Task("team3-documenter-spark", "Document Team 3 work")
Task("team4-documenter-spark", "Document Team 4 work")
```

## Performance Benefits

- 2 tasks: 1.8x faster
- 3 tasks: 2.5x faster
- 4 tasks: 3.1x faster

But ONLY if you:
1. Use team-specific agents
2. Call all agents in one message
3. Let them run truly in parallel

## Root Cause of Confusion

The confusion often stems from:

1. **Similar naming** between generic and team agents
2. **Assumption** that generic agents can handle team prefixes
3. **Sequential thinking** instead of parallel thinking
4. **Not reading** the command documentation first

## Solution: Always Check First

```bash
# Before running any command:
1. Read ~/.claude/commands/{command}.md
2. Verify agent names
3. Check execution pattern
4. Then execute
```

---

*Last Updated: 2025-08-22*
*Version: 1.0*