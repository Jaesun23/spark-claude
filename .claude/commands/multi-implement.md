# /multi-implement - SPARK Parallel Multi-Team Implementation

**Purpose**: Execute multiple implementation tasks in parallel using up to 4 teams with JSON context relay

## 🚀 Parallel Multi-Team Workflow

Orchestrates up to 4 teams working simultaneously on independent tasks with quality gates and testing.

### Workflow Architecture
```
2호 (Orchestrator)
    └── Task Tool (Parallel Calls)
        ├── Team1 → team1_current_task.json
        ├── Team2 → team2_current_task.json
        ├── Team3 → team3_current_task.json
        └── Team4 → team4_current_task.json
```

## 📝 Orchestration Process

### Phase 0: Task Allocation
2호 analyzes tasks and allocates to teams:
1. Parse task IDs from command
2. Create team JSON files with task details
3. Identify shared resources needing locks

### Phase 1: Parallel Implementation
2호 calls all assigned teams simultaneously:
```
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
After all implementations complete, 2호 calls testers:
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
After testing complete, 2호 calls documenters:
```
Task("team1-documenter-spark", doc_prompt)
Task("team2-documenter-spark", doc_prompt)
Task("team3-documenter-spark", doc_prompt)
Task("team4-documenter-spark", doc_prompt)
```

### Phase 4: Consolidation
2호 reviews all team JSONs and provides final report.

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
- 2호 manages lock allocation
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