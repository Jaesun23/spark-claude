# 📚 SPARK Parallel Multi-Team Implementation Guide

## Quick Start

### 1. Generate Team Agents
```bash
python3 .claude/agents/team_agent_generator.py
```

### 2. Execute Parallel Tasks
```bash
# For 2호 to execute:
/multi_implement TASK-API-01 TASK-UI-02 TASK-SEC-03 TASK-DATA-04
```

## 🔄 Complete Workflow

### Phase 1: Initialization (Sequential)
2호 receives `/multi_implement` command and:
1. Parses task IDs
2. Allocates tasks to teams (max 4)
3. Creates team JSON contexts
4. Initializes coordination file

### Phase 2: Implementation (Parallel)
2호 executes **simultaneously**:
```python
# All teams called at once!
Task("team1_implementer", "Implement TASK-API-01 from team1_current_task.json")
Task("team2_implementer", "Implement TASK-UI-02 from team2_current_task.json")
Task("team3_implementer", "Implement TASK-SEC-03 from team3_current_task.json")
Task("team4_implementer", "Implement TASK-DATA-04 from team4_current_task.json")
```

Each team:
- Reads their JSON context
- Implements assigned files
- Updates JSON with results
- Exits for orchestrator control

### Phase 3: Quality Gates (Parallel)
After ALL implementations complete:
```python
# Again, all teams simultaneously!
Task("team1_quality", "Run quality gates on team1 implementation")
Task("team2_quality", "Run quality gates on team2 implementation")
Task("team3_quality", "Run quality gates on team3 implementation")
Task("team4_quality", "Run quality gates on team4 implementation")
```

### Phase 4: Testing (Parallel)
After ALL quality gates pass:
```python
Task("team1_tester", "Write tests for team1 implementation")
Task("team2_tester", "Write tests for team2 implementation")
Task("team3_tester", "Write tests for team3 implementation")
Task("team4_tester", "Write tests for team4 implementation")
```

### Phase 5: Review (Sequential)
Single reviewer for all teams:
```python
Task("reviewer", "Review all team implementations for architecture consistency")
```

### Phase 6: Report (Sequential)
Final consolidated report:
```python
Task("reporter", "Generate final report for all team implementations")
```

## 📊 JSON Context Flow

### Team Context Structure
Each team has `team[1-4]_current_task.json`:

```json
{
  "team_id": "team1",
  "task_id": "TASK-API-01",
  "status": "in_progress",
  "phase": "implementation",
  "assigned_files": ["src/api/auth.py"],
  "implementation_details": {
    "files_created": [],
    "files_modified": [],
    "functions_added": []
  },
  "quality_gates": {
    "syntax_validation": "pending",
    "type_verification": "pending"
  },
  "communication": {
    "messages_for_orchestrator": [],
    "blockers": []
  }
}
```

### Coordination File
`multi_task_coordination.json` tracks overall progress:

```json
{
  "session_id": "multi_20250808",
  "active_teams": 4,
  "teams": {
    "team1": {"status": "ACTIVE", "phase": "implementation"},
    "team2": {"status": "ACTIVE", "phase": "implementation"},
    "team3": {"status": "ACTIVE", "phase": "quality"},
    "team4": {"status": "BLOCKED", "phase": "implementation"}
  },
  "overall_progress": 45
}
```

## 🔒 Handling Shared Resources

### Lock Acquisition
When teams need to modify shared files (constants.py, types.py):

```python
# Team agent code
if FileLockManager.acquire_lock("src/constants.py", "team1"):
    # Modify file
    edit_file("src/constants.py")
    FileLockManager.release_lock("src/constants.py", "team1")
else:
    # Add to blockers
    context["communication"]["blockers"].append(
        "Cannot acquire lock on src/constants.py"
    )
```

### Lock Timeout
Locks auto-expire after 30 seconds to prevent deadlocks.

## 🎯 2호's Orchestration Role

### Key Responsibilities
1. **Task Allocation**: Distribute tasks to teams
2. **Parallel Invocation**: Call multiple agents simultaneously
3. **Phase Synchronization**: Wait for all teams before next phase
4. **Quality Enforcement**: Retry failed quality checks
5. **Progress Tracking**: Monitor via JSON contexts
6. **Conflict Resolution**: Handle lock conflicts and blockers

### Orchestration Commands
```python
# Initialize parallel execution
orchestrator = MultiTeamOrchestrator()
result = orchestrator.handle_multi_implement(task_ids)

# Handle team completion
orchestrator.handle_team_completion("team1", "implementation")

# Check phase completion
if orchestrator.all_teams_completed_phase("implementation"):
    proceed_to_quality_phase()
```

## 📈 Performance Metrics

### Parallelization Benefits
| Tasks | Sequential Time | Parallel Time | Speedup |
|-------|-----------------|---------------|---------|
| 2     | 2 hours        | 1.1 hours     | 1.8x    |
| 3     | 3 hours        | 1.2 hours     | 2.5x    |
| 4     | 4 hours        | 1.3 hours     | 3.1x    |

### Token Efficiency
- Base SPARK: 5,100 tokens per agent
- Multi-team overhead: +500 tokens for coordination
- Total efficiency maintained at >85%

## 🚨 Troubleshooting

### Common Issues

#### 1. Team Blocked on Lock
**Symptom**: Team reports blocker in JSON
**Solution**: 
- Check `file_locks.json` for expired locks
- Manually release if needed
- Consider sequential modification for critical files

#### 2. Quality Gate Failures
**Symptom**: Team stuck in quality retry loop
**Solution**:
- Check retry count (max 3)
- Review specific violations in JSON
- May need manual intervention for complex issues

#### 3. Phase Synchronization Delay
**Symptom**: One team much slower than others
**Solution**:
- Check team's JSON for blockers
- Consider reassigning task to faster team
- Implement timeout for phase completion

## 🎓 Best Practices

### Task Allocation
1. **Group related files** to same team
2. **Minimize shared dependencies** between teams
3. **Balance complexity** across teams
4. **Reserve Team 4** for smaller tasks

### JSON Communication
1. **Always update progress** in JSON
2. **Report blockers immediately**
3. **Include detailed error messages**
4. **Track all file modifications**

### Quality Standards
1. **Never skip quality gates**
2. **Fix violations before proceeding**
3. **Maintain 95%+ test coverage**
4. **Document all public functions**

## 🔮 Advanced Features

### Dynamic Team Scaling
```python
# Adjust team count based on load
if len(task_ids) <= 2:
    use_teams = 2  # More efficient for small loads
else:
    use_teams = min(4, len(task_ids))
```

### Smart Task Allocation
```python
# Allocate by complexity
complex_tasks = [t for t in tasks if t.complexity > 0.7]
simple_tasks = [t for t in tasks if t.complexity <= 0.7]

# Give complex tasks to experienced teams
allocate_to_team1(complex_tasks[0])
distribute_remaining(simple_tasks)
```

### Conflict Prediction
```python
# Predict file conflicts before execution
def predict_conflicts(task_allocations):
    file_usage = {}
    for team, task in task_allocations.items():
        for file in task.files:
            if file in file_usage:
                print(f"⚠️ Conflict predicted: {file}")
            file_usage[file] = team
```

## 📝 Example Session

### Input
```
/multi_implement TASK-API-01 TASK-UI-02 TASK-SEC-03
```

### Execution Flow
```
1. [INIT] Allocate: team1=API, team2=UI, team3=SEC
2. [IMPL] Parallel: team1_implementer, team2_implementer, team3_implementer
3. [WAIT] All teams complete implementation
4. [QUAL] Parallel: team1_quality, team2_quality, team3_quality
5. [RETRY] team2_quality (1 violation found)
6. [TEST] Parallel: team1_tester, team2_tester, team3_tester
7. [REVIEW] Single: reviewer (check all implementations)
8. [REPORT] Single: reporter (generate final report)
```

### Output
```json
{
  "session": "multi_20250808",
  "duration": "1.2 hours",
  "teams_used": 3,
  "files_created": 12,
  "files_modified": 18,
  "tests_added": 45,
  "coverage": "96.5%",
  "quality_violations": 0,
  "status": "SUCCESS"
}
```

## 🚀 Getting Started

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Generate team agents**:
```bash
python3 .claude/agents/team_agent_generator.py
```

3. **Test with 2 tasks**:
```
/multi_implement TASK-TEST-01 TASK-TEST-02
```

4. **Monitor progress**:
```bash
watch -n 5 'cat .claude/workflows/multi_task_coordination.json | jq .overall_progress'
```

---

*With this parallel architecture, SPARK achieves enterprise-scale development velocity while maintaining its hallmark quality standards.*