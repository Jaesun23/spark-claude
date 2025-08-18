# SPARK Agent Phase Structure v4.1 - Complete Implementation Guide

## 📖 Document Overview

This document provides comprehensive documentation of the SPARK v3.8 agent phase structure, covering the standardized 6-phase methodology that all 28 agents follow, with detailed explanations of why phases vary and how the system coordinates across single, pipeline, and parallel execution modes.

**Target Audience**: SPARK system developers, agent creators, system architects  
**Complexity Level**: Intermediate to Advanced  
**Last Updated**: August 2025

---

## 🎯 Executive Summary

The SPARK v3.8 system implements a standardized 6-phase methodology across all 28 agents (16 primary + 12 team agents). This structure ensures consistent execution patterns while allowing agent-specific customization where needed.

### Key Phase Structure:
- **Phase 0**: Common initialization (all agents)
- **Phase 1-3**: Agent-specific core work phases
- **Phase 4**: Agent-specific quality validation (varies by agent type)
- **Phase 5 Part A**: Agent-specific completion work
- **Phase 5 Part B**: Common JSON update & verification (all agents)

---

## 📊 Complete Phase Structure Overview

### Phase 0: Task Initialization (모든 에이전트 공통)

**Purpose**: Standardized startup procedure for all agents  
**Duration**: 30-60 seconds  
**Common Across**: All 28 agents  

#### Step 1: Read JSON State
```bash
# For single/primary agents
cat ~/.claude/workflows/current_task.json || cat .claude/workflows/current_task.json

# For team agents
cat ~/.claude/workflows/team[1-4]_current_task.json || cat .claude/workflows/team[1-4]_current_task.json
```

#### Step 2: Update Status to Running
Every agent updates JSON with:
- `state.current_agent`: Agent name
- `state.current_phase`: 1 (starting Phase 1)
- `state.status`: "running"
- `updated_at`: Current timestamp

### Phase 1-3: Agent-Specific Core Work

These phases contain the unique methodology each agent follows for their specialized work.

#### Phase 1: Discovery/Analysis/Preparation
Each agent has a unique Phase 1 focused on:
- **analyzer-spark**: System exploration and complexity scoring
- **implementer-spark**: Existing codebase analysis and integration points
- **tester-spark**: Test scope analysis and existing test evaluation
- **documenter-spark**: Audience analysis and structure planning
- **designer-spark**: Requirements analysis and constraint identification

#### Phase 2: Foundation/Structure/Planning  
Each agent builds their foundational work:
- **implementer-spark**: API structures and data models
- **tester-spark**: Test infrastructure and framework setup
- **documenter-spark**: Information architecture design
- **cleaner-spark**: Cleanup planning and safety checks

#### Phase 3: Core Work/Implementation/Content
The main work phase where agents deliver their primary value:
- **implementer-spark**: Business logic implementation
- **tester-spark**: Test case creation and execution
- **documenter-spark**: Content creation with examples
- **troubleshooter-spark**: Root cause analysis

### Phase 4: Quality Validation (에이전트별 차별화)

**⚠️ IMPORTANT**: Phase 4 varies significantly between agents and some agents don't have it at all.

#### Agents WITH Phase 4:
- **implementer-spark**: Internal quality validation (ruff, mypy, black, bandit)
- **tester-spark**: Test execution and coverage validation
- **cleaner-spark**: Safety validation before cleanup execution
- **improver-spark**: Refactoring validation and regression testing

#### Agents WITHOUT Phase 4:
- **analyzer-spark**: Goes directly from Phase 3 to Phase 5
- **documenter-spark**: Quality review integrated into Phase 3
- **explainer-spark**: Educational content validation in Phase 3
- **estimater-spark**: Estimation validation in Phase 3

#### Why Phase 4 Varies:

1. **Quality Gates Requirement**: Implementation agents need extensive validation
2. **Risk Profile**: High-risk operations (implementer, cleaner) need validation phases
3. **Output Type**: Analysis and documentation agents validate during creation
4. **Time Constraints**: Some agents integrate validation to optimize workflow

### Phase 5: Task Completion & Reporting (2부분 구조)

Phase 5 is split into two parts to separate agent-specific completion work from common system coordination.

#### Part A: Agent-Specific Completion Work
Each agent has unique completion activities:
- **implementer-spark**: Test readiness preparation and handoff documentation
- **tester-spark**: Final test report generation and CI/CD integration
- **documenter-spark**: Final review, polish, and cross-references
- **analyzer-spark**: Report synthesis and priority matrix creation

#### Part B: Common JSON Update & Verification (모든 에이전트 공통)

**Universal across all 28 agents** - this ensures consistent system coordination:

##### Step 1: Execute 8-Step Quality Gates
Every agent runs standardized quality checks:
```bash
1. ruff check --extend-select I --fix .  # Import sorting + linting
2. black . --check                       # Code formatting 
3. mypy . --strict                       # Type checking
4. ruff check .                          # Final lint check
5. bandit -r . -f json                   # Security analysis
6. pytest --cov=. --cov-report=term-missing  # Test coverage (if tests exist)
7. find . -name "*.py" -exec python -m py_compile {} \;  # Syntax validation
8. pip-audit                             # Dependency vulnerability scan
```

##### Step 2: Update JSON State to Completed
```json
{
  "state": {
    "current_agent": "[agent_name]",
    "current_phase": "completed",
    "status": "completed",
    "completion_time": "[timestamp]",
    "quality_gates_passed": true,
    "final_report_path": "/docs/agents-task/[agent]/[report].md"
  }
}
```

##### Step 3: Generate Mandatory Report
All agents create standardized reports:
- **Location**: `/docs/agents-task/[agent-name]/[task]_[timestamp].md`
- **Detailed reports** (7 agents): 500-800+ lines
- **Concise reports** (21 agents): 150-300 lines

---

## 🔄 Workflow Execution Patterns

### 1. Single Agent Workflow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Phase 0   │───▶│  Phase 1-3  │───▶│   Phase 4   │
│Initialization│    │Agent-Specific│    │(If Required)│
└─────────────┘    │   Work      │    └─────────────┘
                   └─────────────┘           │
                                            ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Phase 5B   │◀───│  Phase 5A   │◀───│   Complete  │
│JSON Update &│    │Agent-Specific│    │             │
│ Verification│    │  Completion  │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Example**: `/spark-analyze "codebase performance"`
- Single analyzer-spark agent execution
- Reads from `current_task.json`
- Updates same file through all phases

### 2. Pipeline Workflow (Sequential Agents)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ analyzer-   │───▶│implementer- │───▶│  tester-    │───▶│documenter-  │
│   spark     │    │   spark     │    │   spark     │    │   spark     │
│ (Phase 0-5) │    │ (Phase 0-5) │    │ (Phase 0-5) │    │ (Phase 0-5) │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

Each agent:
- Reads current_task.json
- Updates status through phases
- Hands off to next agent
```

**Example**: `/spark "implement user authentication"`
- Sequential execution: analyzer → implementer → tester → documenter
- Shared state in `current_task.json`
- Each agent builds on previous work

### 3. Parallel Workflow (4 Teams)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Task Decomposition                         │
│                     (Main current_task.json)                       │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Team 1    │  │   Team 2    │  │   Team 3    │  │   Team 4    │
│ (Backend)   │  │ (Frontend)  │  │ (Database)  │  │ (Testing)   │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
       │                │                │                │
       ▼                ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│team1-impl   │  │team2-impl   │  │team3-impl   │  │team4-impl   │
│     ↓       │  │     ↓       │  │     ↓       │  │     ↓       │
│team1-test   │  │team2-test   │  │team3-test   │  │team4-test   │
│     ↓       │  │     ↓       │  │     ↓       │  │     ↓       │
│team1-doc    │  │team2-doc    │  │team3-doc    │  │team4-doc    │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘

Each team uses: team[1-4]_current_task.json
```

**Example**: `/multi-implement backend,frontend,database,testing`
- 12 team agents execute simultaneously (4 teams × 3 agents each)
- Independent JSON files for coordination
- Shared resource locking when needed

---

## 📁 JSON File Usage Patterns

### 1. Main Orchestration File
**File**: `~/.claude/workflows/current_task.json` or `.claude/workflows/current_task.json`

**Structure**:
```json
{
  "task_id": "task_20250818_140532",
  "original_request": "implement user authentication system",
  "state": {
    "current_agent": "implementer-spark",
    "current_phase": 3,
    "status": "running",
    "started_at": "2025-08-18T14:05:32Z",
    "updated_at": "2025-08-18T14:15:45Z"
  },
  "execution_context": {
    "execution_mode": "single|pipeline|parallel",
    "complexity_score": 0.75,
    "estimated_duration": "45 minutes"
  },
  "agents_chain": ["analyzer-spark", "implementer-spark", "tester-spark"],
  "results": {
    "analyzer-spark": {
      "status": "completed",
      "phase_5_completed": true,
      "report_path": "/docs/agents-task/analyzer-spark/auth_analysis_20250818.md"
    }
  }
}
```

### 2. Team-Specific Files
**Files**: 
- `~/.claude/workflows/team1_current_task.json`
- `~/.claude/workflows/team2_current_task.json`
- `~/.claude/workflows/team3_current_task.json`
- `~/.claude/workflows/team4_current_task.json`

**Structure**:
```json
{
  "parent_task_id": "task_20250818_140532",
  "team_id": "team1",
  "team_assignment": {
    "focus": "backend services",
    "files_responsible": ["api/", "models/", "services/"],
    "shared_dependencies": ["constants.py", "types.py"]
  },
  "state": {
    "current_agent": "team1-implementer-spark",
    "current_phase": 2,
    "status": "running"
  },
  "resource_locks": {
    "requested": ["constants.py"],
    "granted": ["constants.py"],
    "waiting_for": []
  },
  "handoff_chain": [
    "team1-implementer-spark",
    "team1-tester-spark", 
    "team1-documenter-spark"
  ]
}
```

### 3. Resource Locking File
**File**: `~/.claude/workflows/file_locks.json`

```json
{
  "locks": {
    "constants.py": {
      "locked_by": "team1-implementer-spark",
      "locked_at": "2025-08-18T14:10:30Z",
      "lock_duration": 900,
      "reason": "Adding authentication constants"
    }
  },
  "queue": [
    {
      "agent": "team3-implementer-spark",
      "file": "constants.py",
      "requested_at": "2025-08-18T14:11:15Z"
    }
  ]
}
```

### 4. Task Abortion File
**File**: `~/.claude/workflows/task_aborted.json`

```json
{
  "task_id": "task_20250818_140532",
  "aborted_by": "team2-implementer-spark",
  "abort_reason": "token_limit_exceeded",
  "abort_timestamp": "2025-08-18T14:20:15Z",
  "estimated_tokens": 95000,
  "token_limit": 90000,
  "recommendation": "Split frontend implementation into smaller components",
  "partial_completion": {
    "completed_agents": ["analyzer-spark", "team1-implementer-spark"],
    "in_progress": ["team2-implementer-spark"],
    "not_started": ["team3-implementer-spark", "team4-implementer-spark"]
  }
}
```

---

## 🎛️ Phase-Specific Coordination Mechanisms

### Phase 0 Coordination
- All agents start by reading appropriate JSON file
- Immediate status update to prevent conflicts
- Resource requirement assessment and lock requests

### Phase 1-3 Coordination
- Progress updates at phase transitions
- Shared resource access through locking mechanism
- Dependency verification before proceeding

### Phase 4 Coordination (Variable)
- Agents with Phase 4: Run validation and update status
- Agents without Phase 4: Skip directly to Phase 5A
- Quality gate failures trigger retry mechanisms

### Phase 5 Coordination
- **Part A**: Agent-specific completion work with progress updates
- **Part B**: Standardized quality gates and final JSON state update
- Mandatory report generation for all agents
- Resource lock release and cleanup

---

## 🚨 Critical System Rules

### 1. JSON State Management
- **NEVER** skip Phase 0 JSON reading
- **ALWAYS** update JSON at phase transitions
- **MANDATORY** Phase 5B JSON completion update
- Use absolute paths for JSON files

### 2. Resource Coordination
- Request locks for shared files (constants.py, types.py, config files)
- Honor lock timeouts and queuing system
- Release locks immediately after use

### 3. Team Agent Constraints
- Team agents work ONLY on assigned portions
- No direct communication between teams
- All coordination through JSON files
- Respect parent task context

### 4. Quality Gates
- All agents run 8-step quality gates in Phase 5B
- Zero tolerance for quality gate failures
- Maximum 3 retry attempts on failures
- Mandatory reports regardless of success/failure

### 5. Token Safety
- Pre-task token estimation mandatory
- Abort if estimated > 90K tokens
- Write operations double token consumption
- Team task splitting on token limit exceeded

---

## 📈 System Benefits

### 1. Consistency
- Standardized phase structure across all agents
- Predictable execution patterns
- Uniform quality assurance

### 2. Flexibility  
- Agent-specific customization in core work phases
- Optional Phase 4 based on agent requirements
- Adaptive JSON state management

### 3. Coordination
- Clear handoff mechanisms between agents
- Resource conflict prevention
- Parallel execution support

### 4. Quality Assurance
- Universal quality gates in Phase 5B
- Mandatory reporting and documentation
- Token safety enforcement

### 5. Scalability
- Support for 1-28 concurrent agents
- Team-based parallel execution
- Resource-aware scheduling

---

## 📚 Related Documentation

- **Team Agents Guide**: `/docs/spark-team-agents-guide-v4.1.md`
- **Agent Reporting System**: `/docs/SPARK_AGENT_REPORTING_UPDATE.md`
- **Quality Gates**: `/docs/8-step-quality-gates-mandatory.md`
- **Architecture Overview**: `/docs/ARCHITECTURE.md`

---

## 🔄 Version History

- **v4.1**: Added comprehensive phase structure documentation
- **v4.0**: Introduced Phase 5 Part A/B split
- **v3.8**: TRAITS system and standardized phase structure
- **v3.5**: Quality gates integration and team agent support

---

**📍 Documentation Location**: `/docs/spark-agent-phase-structure-v4.1.md`  
**Word Count**: ~2,100 words  
**Sections**: 15 major sections with detailed subsections  
**Examples**: 25+ code snippets and configuration examples