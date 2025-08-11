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
2. Create team JSON files with task details
3. Identify shared resources needing locks

### Phase 1: Parallel Implementation
Call all assigned teams SIMULTANEOUSLY (not sequentially):
```
# ALL FOUR CALLS AT ONCE - NO WAITING BETWEEN!
Task("team1-implementer-spark", prompt_with_json_path)
Task("team2-implementer-spark", prompt_with_json_path)
Task("team3-implementer-spark", prompt_with_json_path)
Task("team4-implementer-spark", prompt_with_json_path)
```

Each implementer:
- Reads their team JSON file for task details
- Implements the feature
- Updates JSON with results before exit
- Respects file locks for shared resources

### Phase 2: Parallel Testing
After all implementations complete, call testers:
```
Task("team1-tester-spark", test_prompt)
Task("team2-tester-spark", test_prompt)
Task("team3-tester-spark", test_prompt)
Task("team4-tester-spark", test_prompt)
```

Each tester:
- Reads team JSON for implementation details
- Creates comprehensive tests (95% coverage target)
- Updates JSON with test results

### Phase 3: Parallel Documentation
After testing complete, call documenters:
```
Task("team1-documenter-spark", doc_prompt)
Task("team2-documenter-spark", doc_prompt)
Task("team3-documenter-spark", doc_prompt)
Task("team4-documenter-spark", doc_prompt)
```

### Phase 4: Consolidation
Review all team JSONs and provide final report.

## 💡 Quality Criteria

Same as single implementation:
- MyPy strict: 0 errors
- Ruff: 0 violations
- Test coverage: ≥95%
- Security scan: 0 issues
- Documentation: Complete

## 🔧 JSON Context Structure

Each team's JSON file contains:
```json
{
  "team_id": "team1",
  "task_id": "TASK-API-01",
  "status": "implementing",
  "task_details": {
    "description": "...",
    "files_to_modify": [],
    "requirements": []
  },
  "implementation": {
    "files_created": [],
    "files_modified": [],
    "quality_results": {}
  },
  "testing": {
    "test_files": [],
    "coverage": 0,
    "results": {}
  },
  "locks_held": [],
  "messages": []
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