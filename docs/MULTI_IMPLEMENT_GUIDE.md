# 🚀 Multi-Implement Guide - SPARK v3.5 4-Team Parallel Execution

## 📋 Overview

`/multi-implement` is SPARK v3.5's most powerful command that enables **4 teams to work in parallel** on independent implementation tasks. With integrated FileLockManager and automatic team JSON template generation, this achieves up to **3.1x faster execution** compared to sequential implementation.

## 🎯 When to Use Multi-Implement

### ✅ Perfect For:
- Multiple independent features (no shared dependencies)
- API endpoints that don't share models
- Separate UI components
- Independent microservices
- Different modules or packages

### ❌ Not Suitable For:
- Interdependent features
- Tasks that modify the same files extensively
- Sequential workflows (A must complete before B)
- Single large feature that can't be split

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Claude CODE (Orchestrator)                 │
│                                                         │
│  1. Parse tasks → Auto-generate team JSON templates     │
│  2. FileLockManager ensures resource safety             │
│  3. Call 4 teams SIMULTANEOUSLY (true parallelism)      │
│  4. Wait for ALL to complete                            │
│  5. Coordinate shared resources with lock management    │
└──────────────┬─────────────────────────────────────────┘
               │
               ├── Task → team1-implementer-spark → team1_task.json
               ├── Task → team2-implementer-spark → team2_task.json  
               ├── Task → team3-implementer-spark → team3_task.json
               └── Task → team4-implementer-spark → team4_task.json
                       ↓
               FileLockManager coordinates file access
```

## 📝 Command Syntax

```bash
# Basic usage with task IDs
/multi-implement "TASK-API-01" "TASK-UI-02" "TASK-SEC-03" "TASK-DATA-04"

# With task descriptions (more flexible)
/multi-implement "User auth endpoint" "Dashboard component" "Security middleware" "Data pipeline"

# 2-3 tasks also work
/multi-implement "Feature A" "Feature B"
```

## 🔄 Execution Phases

### Phase 1: Initialization (Claude CODE)
```python
1. Parse command and extract tasks
2. Validate task independence
3. Create team JSON files with task details
4. Identify potential resource conflicts
```

### Phase 2: Parallel Implementation
```python
# ALL CALLS AT ONCE - TRUE PARALLELISM!
Task("team1-implementer-spark", task1_with_json)
Task("team2-implementer-spark", task2_with_json)
Task("team3-implementer-spark", task3_with_json)
Task("team4-implementer-spark", task4_with_json)

# WAIT for ALL teams to complete
```

### Phase 3: Parallel Testing
```python
# After implementation, test in parallel
Task("team1-tester-spark", test1)
Task("team2-tester-spark", test2)
Task("team3-tester-spark", test3)
Task("team4-tester-spark", test4)

# WAIT for ALL tests to complete
```

### Phase 4: Consolidation
- Claude CODE reviews all team results
- Generates unified report
- Handles any integration needs

## 📊 Team JSON Template System

### Auto-Generated Team Templates

SPARK v3.5 automatically generates team JSON templates on installation:

**Template Location:** `~/.claude/workflows/team{1-4}_task.json`

```json
{
  "team_id": "team1",
  "status": "ready",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Runtime Task Structure

During execution, each team's JSON is populated with task details:

```json
{
  "team_id": "team1",
  "task_id": "TASK-API-01",
  "status": "implementing|testing|complete",
  "task_details": {
    "description": "Create user authentication endpoint",
    "files_to_modify": ["api/auth.py", "models/user.py"],
    "requirements": ["JWT tokens", "bcrypt hashing"],
    "estimated_complexity": 0.6
  },
  "implementation": {
    "files_created": ["api/auth.py"],
    "files_modified": ["models/user.py"],
    "quality_results": {
      "mypy": "passed",
      "ruff": "passed",
      "security": "passed",
      "coverage": 96.5
    },
    "token_usage": 15420
  },
  "testing": {
    "test_files": ["tests/test_auth.py"],
    "coverage": 96.5,
    "results": "All tests passed",
    "execution_time": "3.2s"
  },
  "file_locks": {
    "requested": ["models/user.py"],
    "acquired": ["models/user.py"],
    "released": [],
    "lock_manager": "FileLockManager"
  },
  "messages": ["Lock acquired for models/user.py", "Implementation completed"],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:05:42Z"
}
```

## 🔒 FileLockManager Integration

### Advanced Resource Lock Management

SPARK v3.5 integrates FileLockManager directly into the StateManager for thread-safe parallel execution:

#### Lock Acquisition Process
1. **Team requests lock** via JSON context
2. **FileLockManager allocates** (first-come-first-served)
3. **30-second timeout** prevents deadlocks
4. **Automatic release** on task completion or timeout
5. **Lock status tracking** in team JSON

#### Lock Request Format
```json
{
  "file_locks": {
    "requested": ["shared/constants.py", "models/base.py"],
    "operation": "modify",
    "priority": "normal",
    "timeout_seconds": 30,
    "reason": "Adding new constants for API endpoint"
  }
}
```

#### FileLockManager Features
- **Thread-safe operation**: Multiple teams can request locks simultaneously
- **Deadlock prevention**: Automatic timeout and release mechanisms
- **Lock inheritance**: Child processes inherit parent locks
- **Lock monitoring**: Real-time status tracking in team JSON files
- **Priority handling**: Normal/high priority lock requests

## ⚡ Performance Metrics

| Tasks | Sequential Time | Parallel Time | Speedup |
|-------|----------------|---------------|---------|
| 2     | 10 min         | 5.5 min       | 1.8x    |
| 3     | 15 min         | 6 min         | 2.5x    |
| 4     | 20 min         | 6.5 min       | 3.1x    |

*Note: Actual speedup depends on task complexity and dependencies*

## 🎯 Best Practices

### DO:
✅ Split large features into independent components
✅ Use clear task IDs or descriptions
✅ Plan file structure to minimize conflicts
✅ Let teams work on different directories
✅ Trust the parallel execution (don't interrupt)

### DON'T:
❌ Check on individual teams during execution
❌ Modify team JSON files manually
❌ Use for interdependent tasks
❌ Exceed 4 tasks (context window limit)
❌ Mix implementation with refactoring

## 🔧 Configuration

The `multi_implement.py` utility provides:
- Task validation
- Team agent generation
- Execution plan creation
- Resource conflict detection
- Progress tracking

## 💡 Example Scenarios

### Scenario 1: API Development
```bash
/multi-implement \
  "User registration endpoint" \
  "User login endpoint" \
  "Password reset endpoint" \
  "Profile update endpoint"
```

### Scenario 2: UI Components
```bash
/multi-implement \
  "Header component with navigation" \
  "Sidebar with menu items" \
  "Footer with links" \
  "Dashboard cards"
```

### Scenario 3: Microservices
```bash
/multi-implement \
  "Auth service setup" \
  "Payment service integration" \
  "Notification service" \
  "Analytics service"
```

## ⚠️ Limitations

1. **Maximum 4 teams** - Claude's context window constraint
2. **No direct communication** - Teams work independently
3. **Synchronous phases** - All teams wait for slowest
4. **File conflicts** - Shared file edits are serialized
5. **No mid-execution changes** - Can't modify tasks once started

## 🐛 Troubleshooting

### Teams not starting in parallel
- **CRITICAL**: Must call all Tasks in ONE MESSAGE (not separate messages)
- Verify team JSON templates exist: `ls ~/.claude/workflows/team*_task.json`
- Check template initialization: Each should contain `{"team_id": "teamX", "status": "ready"}`
- Ensure no syntax errors in command
- Verify FileLockManager is properly initialized

### File conflicts and lock issues
- Review `file_locks` section in team JSONs for lock status
- Check FileLockManager logs: `grep "FileLockManager" ~/.claude/workflows/team*_task.json`
- Verify lock timeout settings (default: 30 seconds)
- Check for deadlock situations in lock acquisition order
- Consider restructuring tasks to minimize shared file access
- Manual lock release if needed: Reset team JSON `file_locks.acquired` to `[]`

### Quality gate failures
- Each team runs independent quality checks
- Fix issues in respective team's implementation
- Re-run only the failed team

## 🔄 Team JSON Template Lifecycle

### 1. Installation Phase
```bash
# Auto-generated during SPARK installation
team1_task.json: {"team_id": "team1", "status": "ready"}
team2_task.json: {"team_id": "team2", "status": "ready"} 
team3_task.json: {"team_id": "team3", "status": "ready"}
team4_task.json: {"team_id": "team4", "status": "ready"}
```

### 2. Execution Phase  
```bash
# Populated with task details during /multi-implement
status: "ready" → "implementing" → "testing" → "complete"
```

### 3. Cleanup Phase
```bash
# Reset to template state after task completion
status: "complete" → "ready" (automatic cleanup)
```

### Manual Template Reset
```bash
# If templates get corrupted
echo '{"team_id": "team1", "status": "ready"}' > ~/.claude/workflows/team1_task.json
echo '{"team_id": "team2", "status": "ready"}' > ~/.claude/workflows/team2_task.json
echo '{"team_id": "team3", "status": "ready"}' > ~/.claude/workflows/team3_task.json
echo '{"team_id": "team4", "status": "ready"}' > ~/.claude/workflows/team4_task.json
```

## 📚 Related Documentation

- [SPARK Hook Guide](./SPARK_HOOK_GUIDE.md) - FileLockManager integration details
- [SPARK Agents Guide](./SPARK_AGENTS_GUIDE.md) - Team agent specifications
- [Token Management](./TOKEN_AND_RESOURCE_MANAGEMENT.md) - Resource optimization
- [Installation Guide](./INSTALLATION_GUIDE.md) - Team template setup

---

*Multi-Implement is SPARK v3.5's flagship feature for maximum parallel efficiency with FileLockManager safety. Use it for independent tasks to achieve dramatic speedups while maintaining data integrity!*