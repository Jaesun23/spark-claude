# SPARK Team Agents Guide v4.3 - Multi-Team Parallel Execution

## 📖 Document Overview

This guide provides comprehensive documentation for SPARK's 15 team agents (team1-5 × implementer/tester/documenter) that enable parallel multi-team execution. These specialized agents coordinate through JSON files to deliver large-scale implementations efficiently.

**Target Audience**: SPARK system developers, team coordinators, parallel execution users  
**Complexity Level**: Advanced  
**Last Updated**: September 2025

---

## 🎯 Team Agent Architecture

### System Overview

The SPARK team agent system enables up to **5 teams working in parallel**, each with 3 specialized agents:

```
Team Structure (15 Total Agents):
├── Team 1: Backend Services
│   ├── team1-implementer-spark
│   ├── team1-tester-spark
│   └── team1-documenter-spark
├── Team 2: Frontend Components  
│   ├── team2-implementer-spark
│   ├── team2-tester-spark
│   └── team2-documenter-spark
├── Team 3: Database Layer
│   ├── team3-implementer-spark
│   ├── team3-tester-spark
│   └── team3-documenter-spark
├── Team 4: Integration & Testing
│   ├── team4-implementer-spark
│   ├── team4-tester-spark
│   └── team4-documenter-spark
└── Team 5: DevOps & Deployment
    ├── team5-implementer-spark
    ├── team5-tester-spark
    └── team5-documenter-spark
```

### Key Characteristics

- **Independent Execution**: Each team works autonomously on assigned tasks
- **JSON Coordination**: Communication via team-specific JSON files  
- **Resource Locking**: Prevents conflicts on shared files
- **Sequential Handoff**: Within each team: implementer → tester → documenter
- **Parallel Teams**: All 5 teams can execute simultaneously

---

## 📁 JSON File Management System

### 1. Team-Specific Task Files

Each team has a dedicated JSON file for coordination:

**File Locations**:
```bash
~/.claude/workflows/team1_current_task.json
~/.claude/workflows/team2_current_task.json  
~/.claude/workflows/team3_current_task.json
~/.claude/workflows/team4_current_task.json

# Fallback locations:
.claude/workflows/team1_current_task.json
.claude/workflows/team2_current_task.json
.claude/workflows/team3_current_task.json
.claude/workflows/team4_current_task.json
```

**JSON Structure**:
```json
{
  "parent_task_id": "task_20250818_140532",
  "team_id": "team1",
  "team_assignment": {
    "focus": "backend API services",
    "description": "Implement user authentication and session management APIs",
    "files_responsible": [
      "api/auth/",
      "models/user.py",
      "services/auth_service.py",
      "middleware/auth_middleware.py"
    ],
    "shared_dependencies": [
      "constants.py",
      "types.py",
      "config/database.py"
    ],
    "integration_points": [
      "database connection",
      "session storage",
      "JWT token management"
    ]
  },
  "state": {
    "current_agent": "team1-implementer-spark",
    "current_phase": 2,
    "status": "running",
    "started_at": "2025-08-18T14:05:32Z",
    "updated_at": "2025-08-18T14:15:45Z",
    "estimated_completion": "2025-08-18T15:30:00Z"
  },
  "handoff_chain": [
    {
      "agent": "team1-implementer-spark",
      "status": "running",
      "started_at": "2025-08-18T14:05:32Z"
    },
    {
      "agent": "team1-tester-spark", 
      "status": "pending",
      "depends_on": "team1-implementer-spark"
    },
    {
      "agent": "team1-documenter-spark",
      "status": "pending", 
      "depends_on": "team1-tester-spark"
    }
  ],
  "resource_locks": {
    "requested": ["constants.py", "config/database.py"],
    "granted": ["constants.py"],
    "waiting_for": ["config/database.py"],
    "lock_timeout": 900
  },
  "progress_tracking": {
    "files_created": 5,
    "files_modified": 8,
    "tests_written": 12,
    "coverage_achieved": "85%"
  },
  "coordination": {
    "blocks_teams": [],
    "blocked_by_teams": ["team3"],
    "shared_resources_with": ["team3", "team4"],
    "integration_dependencies": [
      "team3: database schema",
      "team4: integration tests"
    ]
  }
}
```

### 2. Resource Locking System

**File**: `~/.claude/workflows/file_locks.json`

```json
{
  "locks": {
    "constants.py": {
      "locked_by": "team1-implementer-spark",
      "locked_at": "2025-08-18T14:10:30Z",
      "lock_duration": 900,
      "lock_expires_at": "2025-08-18T14:25:30Z",
      "reason": "Adding authentication constants and enums",
      "estimated_changes": "15-20 lines"
    },
    "config/database.py": {
      "locked_by": "team3-implementer-spark", 
      "locked_at": "2025-08-18T14:08:15Z",
      "lock_duration": 1200,
      "lock_expires_at": "2025-08-18T14:28:15Z",
      "reason": "Adding user table schema and indexes",
      "estimated_changes": "50+ lines"
    }
  },
  "queue": [
    {
      "agent": "team1-implementer-spark",
      "file": "config/database.py",
      "requested_at": "2025-08-18T14:11:15Z",
      "priority": "high",
      "reason": "Need to add session table configuration"
    },
    {
      "agent": "team2-implementer-spark",
      "file": "constants.py", 
      "requested_at": "2025-08-18T14:12:00Z",
      "priority": "medium",
      "reason": "Frontend API endpoint constants"
    }
  ],
  "lock_history": [
    {
      "file": "types.py",
      "locked_by": "team1-implementer-spark",
      "duration": 450,
      "released_at": "2025-08-18T14:05:00Z",
      "changes_made": "Added User and Session type definitions"
    }
  ]
}
```

---

## 🔧 Team Agent Initialization Protocol

### Phase 0: Team-Specific Initialization

Each team agent follows this enhanced Phase 0 protocol:

#### Step 1: Read Team Assignment
```bash
# Team 1 agents read:
cat ~/.claude/workflows/team1_current_task.json || cat .claude/workflows/team1_current_task.json

# Team 2 agents read:  
cat ~/.claude/workflows/team2_current_task.json || cat .claude/workflows/team2_current_task.json

# And so on for teams 3 and 4
```

#### Step 2: Parse Team Context
Extract critical information:
```json
{
  "my_team": "team1",
  "my_focus": "backend API services", 
  "my_files": ["api/auth/", "models/user.py"],
  "shared_files": ["constants.py", "types.py"],
  "integration_dependencies": ["team3: database schema"]
}
```

#### Step 3: Check Resource Requirements
Before starting work:
```bash
# Check if shared files need locking
files_to_lock = ["constants.py", "config/database.py"]

# Request locks if needed
for file in files_to_lock:
    request_lock(file, team_agent_name, estimated_duration)
```

#### Step 4: Update Team Status
```json
{
  "state": {
    "current_agent": "team1-implementer-spark",
    "current_phase": 1,
    "status": "running",
    "started_at": "2025-08-18T14:05:32Z",
    "updated_at": "2025-08-18T14:05:35Z"
  }
}
```

---

## ⚡ Team Coordination Patterns

### 1. Intra-Team Handoffs (Sequential)

Within each team, agents hand off work sequentially:

```
team[X]-implementer-spark
         │
         │ (completes Phase 5B)
         ▼
team[X]-tester-spark  
         │
         │ (completes Phase 5B)
         ▼
team[X]-documenter-spark
         │
         │ (completes Phase 5B)
         ▼
    Team Complete
```

**Handoff Process**:
1. **Implementer completes** → Updates team JSON with implementation status
2. **Tester reads team JSON** → Finds tests to write and files to validate
3. **Tester completes** → Updates team JSON with test results
4. **Documenter reads team JSON** → Creates documentation for team's work

### 2. Inter-Team Dependencies

Teams coordinate for shared resources and dependencies:

```
Team 1 (Backend)     Team 3 (Database)
      │                      │
      │ needs database        │ creates schema
      │ schema               │
      └──────────────────────┘
           coordination via
           resource locks &
           JSON file updates
```

**Dependency Resolution**:
- **Blocking Dependencies**: Team 1 waits for Team 3's database schema
- **Resource Conflicts**: Use file locking for shared files
- **Integration Points**: Document in team JSON files

### 3. Parallel Execution Synchronization

All teams execute in parallel but coordinate through:

```
Main Task Orchestrator
         │
         ├─── spawns Team 1 (implementer)
         ├─── spawns Team 2 (implementer)  
         ├─── spawns Team 3 (implementer)
         └─── spawns Team 4 (implementer)
              │
              │ (all execute Phase 0-5 independently)
              │
         ┌────┴────┬────────┬────────┐
         │         │        │        │
     Team 1    Team 2   Team 3   Team 4
   Complete  Complete Complete Complete
         │         │        │        │
         └────┬────┴────────┴────────┘
              │
         Final Integration
         & Master Report
```

---

## 🔐 Resource Locking Protocol

### Lock Request Process

```python
# Pseudocode for resource locking
def request_file_lock(file_path, agent_name, duration_seconds, reason):
    lock_file = read_file_locks_json()
    
    if file_path in lock_file.locks:
        # File already locked, add to queue
        add_to_queue(file_path, agent_name, reason)
        wait_for_lock_release(file_path)
    else:
        # Grant lock immediately
        grant_lock(file_path, agent_name, duration_seconds, reason)
    
    return lock_granted
```

### Lock Release Process

```python
def release_file_lock(file_path, agent_name):
    lock_file = read_file_locks_json()
    
    if lock_file.locks[file_path].locked_by == agent_name:
        # Release lock and process queue
        remove_lock(file_path)
        process_queue_for_file(file_path)
        update_lock_history(file_path, agent_name)
    
    return lock_released
```

### Common Shared Files

Files that typically require locking:

```python
COMMONLY_SHARED_FILES = [
    "constants.py",           # Application constants
    "types.py",              # Type definitions  
    "config/database.py",    # Database configuration
    "config/settings.py",    # Application settings
    "utils/helpers.py",      # Utility functions
    "middleware/",           # Shared middleware
    "models/base.py",        # Base model classes
    "api/exceptions.py",     # API exception definitions
]
```

---

## 📊 Team Progress Tracking

### Individual Team Metrics

Each team tracks progress in their JSON file:

```json
{
  "progress_tracking": {
    "implementation_progress": {
      "files_created": 8,
      "files_modified": 12,
      "lines_of_code": 1247,
      "functions_implemented": 23,
      "classes_created": 6
    },
    "testing_progress": {
      "unit_tests_written": 18,
      "integration_tests": 5,
      "test_coverage": "87%",
      "tests_passing": 22,
      "tests_failing": 1
    },
    "documentation_progress": {
      "api_endpoints_documented": 12,
      "examples_created": 8,
      "guides_written": 3,
      "diagrams_created": 2
    }
  }
}
```

### Cross-Team Coordination Metrics

```json
{
  "coordination_metrics": {
    "resource_lock_requests": 3,
    "resource_lock_wait_time": 45,
    "integration_dependencies": 2,
    "blocking_other_teams": false,
    "blocked_by_other_teams": true,
    "shared_file_conflicts": 1
  }
}
```

---

## 🚨 Team Agent Error Handling

### 1. Token Limit Exceeded

When a team agent approaches token limits:

```json
{
  "status": "aborted",
  "abort_reason": "token_limit_exceeded",
  "team": "team2",
  "agent": "team2-implementer-spark",
  "estimated_tokens": 92000,
  "token_limit": 90000,
  "recommendation": "Split team2 frontend task into smaller components",
  "partial_work_saved": true,
  "restart_strategy": "component-by-component implementation"
}
```

**File Location**: `~/.claude/workflows/team2_task_aborted.json`

### 2. Resource Lock Timeout

When resource locks expire:

```json
{
  "error_type": "lock_timeout",
  "team": "team1", 
  "agent": "team1-implementer-spark",
  "file": "constants.py",
  "lock_duration": 900,
  "actual_wait": 1200,
  "resolution": "proceed_without_lock",
  "alternative_approach": "create_team_specific_constants"
}
```

### 3. Dependency Blocking

When team dependencies cannot be resolved:

```json
{
  "error_type": "dependency_blocking",
  "team": "team1",
  "blocked_by": "team3",
  "dependency": "database schema for User table",
  "wait_timeout": 1800,
  "resolution": "mock_dependency",
  "mock_implementation": "temporary User schema for development"
}
```

---

## 🎛️ Team Agent Command Patterns

### Single Team Execution

```bash
# Execute single team with all 3 agents
Task("team1-implementer-spark", "backend authentication system")
# Wait for completion, then:
Task("team1-tester-spark", "test backend authentication")  
# Wait for completion, then:
Task("team1-documenter-spark", "document authentication API")
```

### Parallel Multi-Team Execution

```bash
# ✅ CORRECT: All teams started simultaneously
Task("team1-implementer-spark", "backend services")
Task("team2-implementer-spark", "frontend components") 
Task("team3-implementer-spark", "database layer")
Task("team4-implementer-spark", "integration testing")

# Wait for ALL to complete Phase 5B, then continue with testing phase
```

### Mixed Execution (Some Teams Parallel)

```bash
# Start critical path teams first
Task("team1-implementer-spark", "core backend")
Task("team3-implementer-spark", "database foundation")

# Wait for foundational work, then start dependent teams
Task("team2-implementer-spark", "frontend (depends on backend APIs)")
Task("team4-implementer-spark", "integration (depends on both)")
```

---

## 📈 Performance Optimization

### Token Efficiency per Team

```python
TEAM_AGENT_TOKEN_USAGE = {
    "team1-implementer-spark": 1108,  # Smallest team agent
    "team1-tester-spark": 856,       # Most efficient tester
    "team1-documenter-spark": 815,   # Most efficient documenter
    "team2-implementer-spark": 1084,
    "team3-implementer-spark": 1096,
    "team4-implementer-spark": 1072
}

# Total for 4-team parallel execution: ~12K tokens
# vs Single implementer-spark: 3869 tokens
# Overhead: 3.1x for 4x parallelism = efficient scaling
```

### Parallel Efficiency Gains

```
Single Agent Execution: 4 sequential phases × 15 minutes = 60 minutes
4-Team Parallel: 4 parallel phases × 15 minutes = 15 minutes  
Efficiency Gain: 75% reduction in total execution time
```

### Resource Contention Mitigation

```python
OPTIMIZATION_STRATEGIES = [
    "Stagger team start times by 30 seconds",
    "Pre-allocate shared file locks based on predicted usage", 
    "Use team-specific temporary files to reduce contention",
    "Implement exponential backoff for lock requests",
    "Prioritize critical path teams for shared resources"
]
```

---

## 🔍 Debugging Team Agent Issues

### Common Issues and Solutions

#### 1. Team JSON File Not Found
```bash
# Check both possible locations
ls ~/.claude/workflows/team1_current_task.json
ls .claude/workflows/team1_current_task.json

# Create minimal team JSON if missing
echo '{"team_id": "team1", "state": {"status": "pending"}}' > ~/.claude/workflows/team1_current_task.json
```

#### 2. Resource Lock Deadlocks
```bash
# Check current locks
cat ~/.claude/workflows/file_locks.json

# Manually release stuck locks (emergency only)
echo '{"locks": {}, "queue": []}' > ~/.claude/workflows/file_locks.json
```

#### 3. Team Coordination Failures
```bash
# Check all team statuses
for i in {1..4}; do
  echo "Team $i status:"
  jq '.state.status' ~/.claude/workflows/team${i}_current_task.json 2>/dev/null || echo "No file"
done
```

### Monitoring Commands

```bash
# Real-time team progress monitoring
watch -n 5 'for i in {1..4}; do echo "Team $i: $(jq -r ".state.current_agent + \" (\" + .state.status + \")\"" ~/.claude/workflows/team${i}_current_task.json 2>/dev/null)"; done'

# Resource lock monitoring  
watch -n 10 'echo "Active Locks:"; jq -r ".locks | keys[]" ~/.claude/workflows/file_locks.json 2>/dev/null'
```

---

## ✅ Best Practices

### 1. Team Assignment Strategy
- **Team 1**: Core backend services and APIs
- **Team 2**: Frontend components and UI
- **Team 3**: Database, data models, and persistence  
- **Team 4**: Testing, integration, and DevOps

### 2. Resource Management
- Request shortest possible lock durations
- Release locks immediately after use
- Use team-specific file naming when possible
- Document shared resource usage in team JSON

### 3. Dependency Coordination
- Clearly document inter-team dependencies
- Use mock implementations for blocked dependencies
- Communicate integration points early in Phase 1

### 4. Error Recovery
- Save partial work before aborting on token limits
- Provide clear restart strategies in abort files  
- Use fallback approaches for blocked resources

### 5. Quality Assurance
- Each team runs full quality gates in Phase 5B
- Test integration points between teams
- Validate shared file changes don't break other teams

---

## 📚 Related Documentation

- **Main Phase Structure**: `/docs/spark-agent-phase-structure-v4.1.md`
- **Quality Gates**: `/docs/8-step-quality-gates-mandatory.md`  
- **Agent Reporting**: `/docs/SPARK_AGENT_REPORTING_UPDATE.md`
- **Architecture**: `/docs/ARCHITECTURE.md`

---

## 🔄 Version History

- **v4.1**: Complete team agent coordination guide
- **v4.0**: Enhanced resource locking and dependency management
- **v3.8**: Initial team agent implementation with TRAITS system
- **v3.5**: Basic parallel execution support

---

**📍 Documentation Location**: `/docs/spark-team-agents-guide-v4.1.md`  
**Word Count**: ~3,200 words  
**Sections**: 18 major sections with detailed examples  
**JSON Examples**: 15+ complete configuration examples