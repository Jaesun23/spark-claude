# /multi-implement - SPARK Parallel Multi-Team Implementation

**Purpose**: Execute multiple implementation tasks in parallel using up to 4 teams with JSON context relay

## 🚨 CRITICAL: ONE MESSAGE WITH MULTIPLE TOOL CALLS 🚨

### **THE GOLDEN RULE FOR PARALLEL EXECUTION:**
```
YOU MUST USE A SINGLE MESSAGE WITH MULTIPLE TASK TOOL CALLS!
DO NOT SEND SEPARATE MESSAGES FOR EACH TASK!
```

## ⚡ IMMEDIATE EXECUTION PROTOCOL

### **AS SOON AS YOU RECEIVE /multi-implement:**

```python
# ✅ CORRECT - ALL IN ONE MESSAGE:
[Single Message]
├── Task("implementer-spark", "Team1: {task1} Read team1_current_task.json")
├── Task("implementer-spark", "Team2: {task2} Read team2_current_task.json")  
├── Task("implementer-spark", "Team3: {task3} Read team3_current_task.json")
└── Task("implementer-spark", "Team4: {task4} Read team4_current_task.json")
[Wait for all to complete]

# ❌ WRONG - SEQUENTIAL MESSAGES:
Message 1: Task("implementer-spark", "Team1...")
Message 2: Task("implementer-spark", "Team2...")  # NO! This waits for Team1!
Message 3: Task("implementer-spark", "Team3...")  # NO! This waits for Team2!
Message 4: Task("implementer-spark", "Team4...")  # NO! This waits for Team3!
```

### **EXECUTION STEPS:**
1. **PREPARE**: Create all team JSON files (team1_current_task.json, etc.)
2. **LAUNCH ALL AT ONCE**: Single message with 4 Task tool calls
3. **WAIT**: For all 4 teams to complete
4. **TEST ALL AT ONCE**: Single message with 4 tester Task calls
5. **REPORT**: Consolidate results

⚠️ **REMEMBER**: If you send Task calls in separate messages, they run SEQUENTIALLY, not in PARALLEL!

## 📝 Orchestration Process

### Phase 0: Task Allocation
Analyze tasks and allocate to teams:
1. Parse task IDs from command
2. Create team JSON files with task details:
   ```python
   # For each team, create team#_current_task.json from template
   # If team1_current_task.json doesn't exist:
   cp ~/.claude/workflows/team_current_task_template.json ~/.claude/workflows/team1_current_task.json
   # Then update with team-specific task details
   ```
3. Identify shared resources needing locks

### Phase 1: Parallel Implementation
Call all assigned teams SIMULTANEOUSLY (not sequentially):
```
# ALL FOUR CALLS AT ONCE - NO WAITING BETWEEN!
Task("team1-implementer-spark", "{task1}")
Task("team2-implementer-spark", "{task2}")
Task("team3-implementer-spark", "{task3}")
Task("team4-implementer-spark", "{task4}")
```

Each team implementer:
- Automatically reads their team#_current_task.json file
- Implements only their assigned feature
- Updates their JSON file with 'implementation' section
- Runs self-validation before exit (recommended)
- Respects file locks for shared resources

### Phase 1.5: Claude CODE Implementation Review
After all implementations complete, Claude CODE reviews all team results:

```python
# Claude CODE reviews each team's results
1. Read team1_current_task.json (check 'implementation' section)
2. Read team2_current_task.json (check 'implementation' section)  
3. Read team3_current_task.json (check 'implementation' section)
4. Read team4_current_task.json (check 'implementation' section)

# Decision for each team:
✅ If team results satisfactory → Proceed to Phase 2
❌ If issues found → Re-call that team's implementer
```

### Phase 2: Parallel Testing
After Claude CODE approves all implementations, call testers:
```
Task("team1-tester-spark", "Test Team 1 implementation")
Task("team2-tester-spark", "Test Team 2 implementation")
Task("team3-tester-spark", "Test Team 3 implementation")
Task("team4-tester-spark", "Test Team 4 implementation")
```

Each team tester:
- Automatically reads their team#_current_task.json
- Creates comprehensive tests (95% coverage target)
- Updates their JSON file with 'testing' section
- Runs self-validation before exit (recommended)

### Phase 2.5: Claude CODE Testing Review
After all testing complete, Claude CODE reviews all test results:

```python
# Claude CODE reviews each team's test results
1. Read team1_current_task.json (check 'testing' section)
2. Read team2_current_task.json (check 'testing' section)
3. Read team3_current_task.json (check 'testing' section)  
4. Read team4_current_task.json (check 'testing' section)

# Decision for each team:
✅ If test coverage ≥95% and all tests pass → Proceed to Phase 3
❌ If issues found → Re-call that team's tester
```

### Phase 3: Parallel Documentation
After Claude CODE approves all testing, call documenters:
```
Task("team1-documenter-spark", "Document Team 1 work")
Task("team2-documenter-spark", "Document Team 2 work")
Task("team3-documenter-spark", "Document Team 3 work")
Task("team4-documenter-spark", "Document Team 4 work")
```

Each team documenter:
- Automatically reads their team#_current_task.json
- Documents implementation and test results
- Updates their JSON file with 'documentation' section
- Runs self-validation before exit (recommended)

### Phase 3.5: Claude CODE Documentation Review
After all documentation complete, Claude CODE reviews all documentation results:

```python
# Claude CODE reviews each team's documentation
1. Read team1_current_task.json (check 'documentation' section)
2. Read team2_current_task.json (check 'documentation' section)
3. Read team3_current_task.json (check 'documentation' section)
4. Read team4_current_task.json (check 'documentation' section)

# Decision for each team:
✅ If documentation complete → Mark team as finished
❌ If issues found → Re-call that team's documenter
```

### Phase 4: Final Consolidation
After all teams pass all phases, Claude CODE provides final report:

```python
# Final multi-team implementation report
- Summary of all team implementations
- Consolidated quality metrics
- Integration points and dependencies
- Overall project completion status
```

## 💡 Quality Criteria

Same as single implementation:
- MyPy strict: 0 errors
- Ruff: 0 violations
- Test coverage: ≥95%
- Security scan: 0 issues
- Documentation: Complete

## 🔧 JSON Context Structure

Each team's JSON file (team#_current_task.json) contains:
```json
{
  "team_id": "team1",
  "task_id": "TASK-API-01",
  "status": "implementing|testing|documenting|completed",
  "task_details": {
    "description": "Implement user authentication endpoint",
    "files_to_modify": ["api/auth.py"],
    "requirements": ["JWT support", "Refresh tokens"]
  },
  "implementation": {
    "agent": "team1-implementer-spark",
    "timestamp": "ISO-8601",
    "status": "completed",
    "files_created": ["api/auth.py"],
    "files_modified": ["main.py"],
    "quality_metrics": {
      "linting_passed": true,
      "type_checking_passed": true
    }
  },
  "testing": {
    "agent": "team1-tester-spark",
    "timestamp": "ISO-8601",
    "status": "completed",
    "test_files": ["tests/test_auth.py"],
    "coverage": 96,
    "all_tests_pass": true
  },
  "documentation": {
    "agent": "team1-documenter-spark",
    "timestamp": "ISO-8601",
    "status": "completed",
    "docs_created": ["docs/auth_api.md"],
    "readme_updated": true
  },
  "locks_held": ["constants.py"],
  "self_validated": true
}
```

## 🔒 File Lock Management

For shared resources (constants.py, types.py):
- Teams request locks through JSON
- Orchestrator manages lock allocation
- 30-second timeout prevents deadlocks

## 🚀 Usage Examples

```bash
# 2 tasks in parallel
/multi-implement "TASK-API-01" "TASK-UI-02"

# 4 tasks in parallel 
/multi-implement "TASK-API-01" "TASK-UI-02" "TASK-SEC-03" "TASK-DATA-04"

# With task descriptions
/multi-implement "Create user auth endpoint" "Build dashboard component" "Add security middleware" "Implement data pipeline"
```

## 📊 Performance Benefits

- **2 tasks**: ~1.8x faster than sequential
- **3 tasks**: ~2.5x faster than sequential
- **4 tasks**: ~3.1x faster than sequential

## ⚠️ Limitations

- Maximum 4 teams (context window constraint)
- All teams wait for slowest to complete each phase
- Shared file modifications are serialized
- No direct agent-to-agent communication