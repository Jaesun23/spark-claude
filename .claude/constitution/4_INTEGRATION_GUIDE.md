# SPARK Integration Guide
## Detailed Standards for Agent-Command Integration

**Part of**: SPARK Constitution v1.2
**Core Document**: See **CONSTITUTION.md** for foundational principles
**Last Updated**: 2025-10-30

This guide expands on **Article IV: Integration Standards** with detailed specifications, examples, and best practices.

---

## Table of Contents

1. [JSON State Management](#section-41-json-state-management)
2. [Evidence Requirements by Agent](#section-42-evidence-requirements-by-agent)
3. [Completion Criteria](#section-43-completion-criteria)

---

## Section 4.1: JSON State Management

### The Communication Protocol

Agents communicate through structured state files, not through direct message passing.

**Philosophy**: State files provide:
- **Persistence**: Survives agent completion
- **Transparency**: 2号 can inspect progress
- **Verification**: Commands can validate claims
- **Debugging**: Failed states preserve error info

### State File Locations

```
~/.claude/workflows/current_task.json         # Main task state
~/.claude/workflows/team1_current_task.json   # Team 1 parallel work
~/.claude/workflows/team2_current_task.json   # Team 2 parallel work
~/.claude/workflows/team3_current_task.json   # Team 3 parallel work
~/.claude/workflows/team4_current_task.json   # Team 4 parallel work
~/.claude/workflows/team5_current_task.json   # Team 5 parallel work
```

**File Organization**:
- **current_task.json**: Single agent or sequential agent chain
- **team{N}_current_task.json**: Parallel execution (multi-implement)
- Each team has independent state for parallel work

### Standard State Structure

**Complete Structure**:

```json
{
  "id": "spark_20251030_143022",
  "version": "4.3",
  "agent": "implementer-spark",
  "task_description": "Implement user authentication API",
  "state": {
    "status": "completed",
    "phase": 5,
    "started_at": "2025-10-30T14:30:22Z",
    "completed_at": "2025-10-30T15:45:18Z"
  },
  "quality": {
    "step_1_architecture": {
      "imports": 0,
      "circular": 0
    },
    "step_2_foundation": {
      "syntax": 0,
      "types": 0
    },
    "step_3_standards": {
      "formatting": 0,
      "conventions": 0
    },
    "step_4_operations": {
      "logging": 0,
      "security": 0
    },
    "step_5_quality": {
      "linting": 0,
      "complexity": 0
    },
    "step_6_testing": {
      "coverage": 0.97,
      "tests_total": 45,
      "tests_passed": 45,
      "tests_failed": 0
    },
    "step_7_documentation": {
      "docstrings": 0,
      "readme": 0
    },
    "step_8_integration": {
      "final": 0
    },
    "violations_total": 0,
    "can_proceed": true
  },
  "evidence": {
    "files_created": [
      "src/auth/api.py",
      "src/auth/models.py",
      "tests/test_auth_api.py"
    ],
    "tests_executed": true,
    "coverage_report": "htmlcov/index.html"
  }
}
```

### State Field Definitions

#### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier: `spark_YYYYMMDD_HHMMSS` |
| `version` | string | Yes | SPARK version: `"4.3"` |
| `agent` | string | Yes | Agent name: `"implementer-spark"` |
| `task_description` | string | No | Brief task description |

#### State Object

| Field | Type | Required | Values | Description |
|-------|------|----------|--------|-------------|
| `status` | string | Yes | `pending`, `running`, `completed`, `failed` | Current execution status |
| `phase` | number | Yes | 0-6 | Current phase number |
| `started_at` | string | Yes | ISO8601 | Task start timestamp |
| `completed_at` | string | No | ISO8601 | Task completion timestamp |

#### Quality Object

**Structure**: Quality metrics organized by implementation steps

Each step has specific metrics:

**Step 1: Architecture**
```json
"step_1_architecture": {
  "imports": 0,        // Import violations
  "circular": 0        // Circular dependency violations
}
```

**Step 2: Foundation**
```json
"step_2_foundation": {
  "syntax": 0,         // Syntax errors
  "types": 0           // Type errors
}
```

**Step 3: Standards**
```json
"step_3_standards": {
  "formatting": 0,     // Formatting violations
  "conventions": 0     // Naming convention violations
}
```

**Step 4: Operations**
```json
"step_4_operations": {
  "logging": 0,        // Logging standard violations
  "security": 0        // Security issues
}
```

**Step 5: Quality**
```json
"step_5_quality": {
  "linting": 0,        // Linting violations (ruff)
  "complexity": 0      // Complexity violations
}
```

**Step 6: Testing** (Critical for implementer/tester)
```json
"step_6_testing": {
  "coverage": 0.95,    // Coverage percentage (0.0-1.0)
  "tests_total": 45,   // Total test count
  "tests_passed": 45,  // Passed test count
  "tests_failed": 0    // Failed test count (MUST be 0)
}
```

**Step 7: Documentation**
```json
"step_7_documentation": {
  "docstrings": 0,     // Missing docstring violations
  "readme": 0          // README issues
}
```

**Step 8: Integration**
```json
"step_8_integration": {
  "final": 0           // Final integration violations
}
```

**Overall Quality**
```json
"violations_total": 0,    // Sum of ALL violations (MUST be 0)
"can_proceed": true       // Whether work can proceed (MUST be true)
```

### Agent Responsibilities

#### Phase 0: Read State

```python
def phase_0_read_state(self):
    """Read existing state or create new."""

    state_file = "~/.claude/workflows/current_task.json"

    if exists(state_file):
        # Read existing state
        self.state = read_json(state_file)

        # Check if continuation or retry
        if self.state["state"]["status"] == "failed":
            print("Retrying failed task...")
        elif self.state["state"]["status"] == "running":
            print("Continuing interrupted task...")
    else:
        # Create new state
        self.state = {
            "id": f"spark_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "version": "4.3",
            "agent": self.agent_name,
            "state": {
                "status": "running",
                "phase": 0,
                "started_at": datetime.now().isoformat()
            },
            "quality": self._init_quality_metrics()
        }
```

#### Throughout Execution: Update State

```python
def update_phase(self, phase: int):
    """Update current phase in state."""

    self.state["state"]["phase"] = phase
    write_json("~/.claude/workflows/current_task.json", self.state)

def record_violation(self, step: str, violation_type: str, count: int):
    """Record quality violations."""

    self.state["quality"][step][violation_type] = count
    self._recalculate_total_violations()
    write_json("~/.claude/workflows/current_task.json", self.state)
```

#### Phase 5A: Write Final State

```python
def phase_5a_record_metrics(self):
    """Record final quality metrics."""

    # Run all quality checks
    ruff_violations = self.run_ruff_check()
    mypy_violations = self.run_mypy_check()
    test_results = self.run_pytest()

    # Record in state
    self.state["quality"]["step_5_quality"]["linting"] = ruff_violations
    self.state["quality"]["step_2_foundation"]["types"] = mypy_violations
    self.state["quality"]["step_6_testing"] = {
        "coverage": test_results["coverage"],
        "tests_total": test_results["total"],
        "tests_passed": test_results["passed"],
        "tests_failed": test_results["failed"]
    }

    # Calculate total violations
    self._recalculate_total_violations()

    # Set can_proceed flag
    self.state["quality"]["can_proceed"] = (
        self.state["quality"]["violations_total"] == 0
    )

    # Mark completion
    self.state["state"]["status"] = "completed"
    self.state["state"]["completed_at"] = datetime.now().isoformat()

    # Write final state
    write_json("~/.claude/workflows/current_task.json", self.state)
```

#### Phase 5B: Quality Gates Check

Agents do NOT modify state in Phase 5B - they only verify it passes.

### 2号 Responsibilities

#### Before Agent Invocation: Initialize State

```python
def initialize_agent_state(agent_name: str, task_description: str):
    """Initialize state before calling agent."""

    state = {
        "id": f"spark_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "version": "4.3",
        "agent": agent_name,
        "task_description": task_description,
        "state": {
            "status": "pending",
            "phase": 0,
            "started_at": datetime.now().isoformat()
        },
        "quality": init_quality_structure()
    }

    write_json("~/.claude/workflows/current_task.json", state)
```

#### After Agent Completion: Validate State

```python
def validate_agent_state(agent_name: str) -> tuple[bool, str]:
    """Validate agent state after completion."""

    state = read_json("~/.claude/workflows/current_task.json")

    # Universal checks
    if state["state"]["status"] != "completed":
        return False, f"Status is {state['state']['status']}"

    if state["quality"]["violations_total"] != 0:
        return False, f"{state['quality']['violations_total']} violations"

    if not state["quality"]["can_proceed"]:
        return False, "can_proceed is false"

    # Agent-specific checks
    if agent_name == "implementer-spark":
        coverage = state["quality"]["step_6_testing"]["coverage"]
        if coverage < 0.95:
            return False, f"Coverage {coverage:.1%} < 95%"

    return True, "Success"
```

#### After Successful Workflow: Delete State

```python
def cleanup_state():
    """Delete state after successful completion."""

    state_file = "~/.claude/workflows/current_task.json"

    if exists(state_file):
        state = read_json(state_file)

        if state["state"]["status"] == "completed" and \
           state["quality"]["violations_total"] == 0:
            os.remove(state_file)
            print("✅ State cleaned up")
```

### State Transitions

**Valid State Transitions**:

```
pending → running → completed ✅
pending → running → failed ❌
failed → running (retry) → completed ✅
running → failed ❌
```

**Invalid Transitions**:

```
pending → completed ❌ (must go through running)
failed → completed ❌ (must retry through running)
completed → running ❌ (completed is terminal)
```

### State File Examples

#### Example 1: Successful Implementer

```json
{
  "id": "spark_20251030_143022",
  "version": "4.3",
  "agent": "implementer-spark",
  "task_description": "Implement user login endpoint",
  "state": {
    "status": "completed",
    "phase": 5,
    "started_at": "2025-10-30T14:30:22Z",
    "completed_at": "2025-10-30T15:45:18Z"
  },
  "quality": {
    "step_1_architecture": { "imports": 0, "circular": 0 },
    "step_2_foundation": { "syntax": 0, "types": 0 },
    "step_3_standards": { "formatting": 0, "conventions": 0 },
    "step_4_operations": { "logging": 0, "security": 0 },
    "step_5_quality": { "linting": 0, "complexity": 0 },
    "step_6_testing": {
      "coverage": 0.98,
      "tests_total": 23,
      "tests_passed": 23,
      "tests_failed": 0
    },
    "step_7_documentation": { "docstrings": 0, "readme": 0 },
    "step_8_integration": { "final": 0 },
    "violations_total": 0,
    "can_proceed": true
  },
  "evidence": {
    "files_created": ["src/auth/login.py", "tests/test_login.py"],
    "coverage_report": "htmlcov/index.html"
  }
}
```

#### Example 2: Failed with Violations

```json
{
  "id": "spark_20251030_160000",
  "version": "4.3",
  "agent": "implementer-spark",
  "state": {
    "status": "failed",
    "phase": 5,
    "started_at": "2025-10-30T16:00:00Z",
    "completed_at": "2025-10-30T16:30:00Z"
  },
  "quality": {
    "step_1_architecture": { "imports": 0, "circular": 0 },
    "step_2_foundation": { "syntax": 0, "types": 5 },
    "step_3_standards": { "formatting": 12, "conventions": 3 },
    "step_4_operations": { "logging": 0, "security": 0 },
    "step_5_quality": { "linting": 23, "complexity": 0 },
    "step_6_testing": {
      "coverage": 0.87,
      "tests_total": 15,
      "tests_passed": 13,
      "tests_failed": 2
    },
    "step_7_documentation": { "docstrings": 8, "readme": 0 },
    "step_8_integration": { "final": 0 },
    "violations_total": 51,
    "can_proceed": false
  },
  "error_details": {
    "type_errors": ["src/auth/login.py:45: Missing type annotation"],
    "linting_errors": ["F841: Local variable 'unused' is assigned but never used"],
    "test_failures": ["test_invalid_credentials FAILED"]
  }
}
```

---

## Section 4.2: Evidence Requirements by Agent

### The Proof Principle

Different agent types require different forms of evidence, but ALL require proof.

### Analyzer Evidence Requirements

**Minimum Requirements**:
- **Evidence items**: 8-12 minimum across all analyzed dimensions
- **Format**: `file_path:line_number` for every finding
- **Content**: Code snippet OR metric for each evidence item
- **Validation**: Evidence validation must pass before Phase 3

**Evidence Item Structure**:

```python
evidence_item = {
    "file_path": "src/api/handler.py",
    "line_number": 145,
    "code": "api_key = os.getenv('KEY')",  # OR
    "metric": {"response_time": "2.5s"},
    "category": "security",
    "severity": "high",
    "description": "Hardcoded API key detected"
}
```

**Complete Evidence Collection**:

```json
{
  "evidence_count": 26,
  "dimensions_analyzed": ["performance", "security", "architecture"],
  "evidence_items": [
    {
      "file_path": "src/api/users.py",
      "line_number": 45,
      "code": "users = db.query('SELECT * FROM users')",
      "category": "performance",
      "severity": "high",
      "description": "N+1 query pattern"
    },
    {
      "file_path": "src/auth/login.py",
      "line_number": 78,
      "code": "@app.post('/login')",
      "category": "security",
      "severity": "critical",
      "description": "No authentication on login endpoint"
    }
    // ... 24 more items
  ]
}
```

**Validation**:

```python
def validate_analyzer_evidence(state: dict) -> bool:
    """Validate analyzer collected sufficient evidence."""

    evidence = state.get("evidence", {})

    # Check minimum count
    if evidence.get("evidence_count", 0) < 8:
        return False

    # Check each item has file:line
    for item in evidence.get("evidence_items", []):
        if not item.get("file_path") or not item.get("line_number"):
            return False

    # Check dimensions analyzed
    if not evidence.get("dimensions_analyzed"):
        return False

    return True
```

### Implementer Evidence Requirements

**Minimum Requirements**:
- **Test execution**: pytest must run and output captured
- **Quality metrics**: Ruff, MyPy before/after counts
- **Coverage**: Percentage per file, overall >= 95%
- **Test results**: All tests must pass (failures == 0)

**Evidence Structure**:

```json
{
  "files_created": [
    "src/auth/api.py",
    "src/auth/models.py",
    "tests/test_auth_api.py"
  ],
  "files_modified": [
    "src/main.py"
  ],
  "test_execution": {
    "command": "pytest tests/test_auth_api.py -v --cov=src/auth",
    "output": "===== test session starts =====\n...",
    "total": 23,
    "passed": 23,
    "failed": 0,
    "duration": "2.45s"
  },
  "coverage": {
    "overall": 0.98,
    "files": {
      "src/auth/api.py": 1.0,
      "src/auth/models.py": 0.96
    }
  },
  "quality_before": {
    "ruff": 45,
    "mypy": 12
  },
  "quality_after": {
    "ruff": 0,
    "mypy": 0
  }
}
```

**Validation**:

```python
def validate_implementer_evidence(state: dict) -> bool:
    """Validate implementer provided execution proof."""

    quality = state["quality"]

    # Check tests executed
    if quality["step_6_testing"]["tests_total"] == 0:
        return False

    # Check all tests passed
    if quality["step_6_testing"]["tests_failed"] != 0:
        return False

    # Check coverage
    if quality["step_6_testing"]["coverage"] < 0.95:
        return False

    # Check quality metrics
    if quality["violations_total"] != 0:
        return False

    return True
```

### Tester Evidence Requirements

**Minimum Requirements**:
- **Test execution logs**: Full pytest output
- **Coverage report**: Per-file percentages
- **Test file paths**: List of all test files with test counts
- **Pass rate**: 100% (test_pass_rate == 1.0)

**Evidence Structure**:

```json
{
  "test_files": [
    {
      "path": "tests/test_auth_api.py",
      "tests": 23,
      "passed": 23,
      "failed": 0
    },
    {
      "path": "tests/test_auth_models.py",
      "tests": 15,
      "passed": 15,
      "failed": 0
    }
  ],
  "coverage": {
    "unit": 0.97,
    "integration": 0.89,
    "overall": 0.95,
    "files": {
      "src/auth/api.py": 1.0,
      "src/auth/models.py": 0.96,
      "src/auth/utils.py": 0.92
    }
  },
  "execution_log": "pytest output...",
  "test_pass_rate": 1.0,
  "tests_total": 38,
  "tests_passed": 38,
  "tests_failed": 0
}
```

**Validation**:

```python
def validate_tester_evidence(state: dict) -> bool:
    """Validate tester executed tests properly."""

    evidence = state.get("evidence", {})

    # Check 100% pass rate
    if evidence.get("test_pass_rate") != 1.0:
        return False

    # Check tests executed
    if evidence.get("tests_total", 0) == 0:
        return False

    # Check coverage targets
    coverage = evidence.get("coverage", {})
    if coverage.get("unit", 0) < 0.95:
        return False
    if coverage.get("integration", 0) < 0.85:
        return False

    return True
```

### Designer Evidence Requirements

**Minimum Requirements**:
- **Architecture diagram**: Image file or ASCII diagram
- **API specifications**: OpenAPI 3.0 or GraphQL schema
- **Data models**: ERD or database schema
- **Technology stack**: Decisions with rationale

**Evidence Structure**:

```json
{
  "artifacts": {
    "architecture_diagram": "docs/architecture.png",
    "api_spec": "docs/openapi.yaml",
    "data_model": "docs/erd.png",
    "tech_stack": "docs/tech_decisions.md"
  },
  "api_endpoints": 15,
  "data_entities": 8,
  "design_decisions": [
    {
      "area": "Authentication",
      "decision": "JWT with refresh tokens",
      "rationale": "Stateless, scalable, industry standard"
    }
  ],
  "validation": {
    "api_completeness": 1.0,
    "model_coverage": 1.0,
    "documentation_complete": true
  }
}
```

**Validation**:

```python
def validate_designer_evidence(state: dict) -> bool:
    """Validate designer produced required artifacts."""

    evidence = state.get("evidence", {})
    artifacts = evidence.get("artifacts", {})

    # Check required artifacts exist
    required = ["architecture_diagram", "api_spec", "data_model"]
    for artifact in required:
        if not artifacts.get(artifact):
            return False

    # Check validation metrics
    validation = evidence.get("validation", {})
    if validation.get("api_completeness", 0) != 1.0:
        return False

    return True
```

### Documenter Evidence Requirements

**Minimum Requirements**:
- **Documentation files**: List of created/updated files
- **Example code verification**: All examples must execute successfully
- **API coverage**: 100% of public APIs documented
- **Completeness**: Parameters, returns, errors all documented

**Evidence Structure**:

```json
{
  "files_created": [
    "docs/api/authentication.md",
    "docs/api/users.md",
    "docs/guides/quick_start.md"
  ],
  "api_coverage": {
    "total_apis": 45,
    "documented": 45,
    "percentage": 1.0
  },
  "example_validation": {
    "total_examples": 23,
    "executed": 23,
    "passed": 23,
    "failed": 0
  },
  "completeness": {
    "parameters": 1.0,
    "returns": 1.0,
    "errors": 1.0,
    "examples": 1.0
  }
}
```

**Validation**:

```python
def validate_documenter_evidence(state: dict) -> bool:
    """Validate documenter completed documentation."""

    evidence = state.get("evidence", {})

    # Check API coverage
    coverage = evidence.get("api_coverage", {})
    if coverage.get("percentage", 0) != 1.0:
        return False

    # Check examples validated
    examples = evidence.get("example_validation", {})
    if examples.get("failed", 0) != 0:
        return False

    # Check completeness
    completeness = evidence.get("completeness", {})
    for aspect in ["parameters", "returns", "errors"]:
        if completeness.get(aspect, 0) != 1.0:
            return False

    return True
```

---

## Section 4.3: Completion Criteria

### Universal Criteria (All Agents)

**Base Function**:

```python
def is_agent_complete(state: dict) -> bool:
    """
    Universal completion check for all agents.

    Returns True only if ALL criteria met.
    """
    return (
        state["state"]["status"] == "completed" and
        state["quality"]["violations_total"] == 0 and
        state["quality"]["can_proceed"] == True
    )
```

**Explanation**:
- `status == "completed"`: Agent marked work as done
- `violations_total == 0`: Zero quality violations
- `can_proceed == True`: Quality gates passed

**All three MUST be true.** If any is false, agent is not complete.

### Agent-Specific Criteria

Each agent type has additional requirements beyond universal criteria.

#### Implementer Completion

```python
def is_implementer_complete(state: dict) -> bool:
    """Implementer-specific completion criteria."""

    # Universal checks
    if not is_agent_complete(state):
        return False

    quality = state["quality"]

    # Test coverage >= 95%
    coverage = quality["step_6_testing"]["coverage"]
    if coverage < 0.95:
        return False

    # All tests passed
    if quality["step_6_testing"]["tests_failed"] != 0:
        return False

    # At least some tests exist
    if quality["step_6_testing"]["tests_total"] == 0:
        return False

    return True
```

**Requirements**:
- ✅ Universal criteria met
- ✅ Coverage >= 95%
- ✅ Zero test failures
- ✅ At least 1 test exists

#### Analyzer Completion

```python
def is_analyzer_complete(state: dict) -> bool:
    """Analyzer-specific completion criteria."""

    # Universal checks
    if not is_agent_complete(state):
        return False

    evidence = state.get("evidence", {})

    # Minimum evidence count
    if evidence.get("evidence_count", 0) < 8:
        return False

    # All requested dimensions analyzed
    dimensions_requested = state.get("dimensions_requested", [])
    dimensions_analyzed = evidence.get("dimensions_analyzed", [])

    if not all(dim in dimensions_analyzed for dim in dimensions_requested):
        return False

    return True
```

**Requirements**:
- ✅ Universal criteria met
- ✅ Minimum 8 evidence items
- ✅ All requested dimensions analyzed

#### Tester Completion

```python
def is_tester_complete(state: dict) -> bool:
    """Tester-specific completion criteria."""

    # Universal checks
    if not is_agent_complete(state):
        return False

    evidence = state.get("evidence", {})

    # 100% test pass rate
    if evidence.get("test_pass_rate", 0) != 1.0:
        return False

    # Coverage targets met
    coverage = evidence.get("coverage", {})
    if coverage.get("unit", 0) < 0.95:
        return False
    if coverage.get("integration", 0) < 0.85:
        return False

    return True
```

**Requirements**:
- ✅ Universal criteria met
- ✅ 100% test pass rate
- ✅ Unit coverage >= 95%
- ✅ Integration coverage >= 85%

#### Designer Completion

```python
def is_designer_complete(state: dict) -> bool:
    """Designer-specific completion criteria."""

    # Universal checks
    if not is_agent_complete(state):
        return False

    evidence = state.get("evidence", {})
    validation = evidence.get("validation", {})

    # All design phases complete
    if not validation.get("all_phases_complete", False):
        return False

    # Validation criteria met
    if validation.get("api_completeness", 0) != 1.0:
        return False

    if validation.get("model_coverage", 0) != 1.0:
        return False

    return True
```

**Requirements**:
- ✅ Universal criteria met
- ✅ All design phases complete
- ✅ 100% API completeness
- ✅ 100% model coverage

#### Documenter Completion

```python
def is_documenter_complete(state: dict) -> bool:
    """Documenter-specific completion criteria."""

    # Universal checks
    if not is_agent_complete(state):
        return False

    evidence = state.get("evidence", {})

    # 100% API coverage
    api_coverage = evidence.get("api_coverage", {})
    if api_coverage.get("percentage", 0) != 1.0:
        return False

    # All examples validated
    examples = evidence.get("example_validation", {})
    if examples.get("failed", 0) != 0:
        return False

    # Completeness checks
    completeness = evidence.get("completeness", {})
    for aspect in ["parameters", "returns", "errors"]:
        if completeness.get(aspect, 0) != 1.0:
            return False

    return True
```

**Requirements**:
- ✅ Universal criteria met
- ✅ 100% API coverage
- ✅ All examples execute successfully
- ✅ Complete documentation (parameters, returns, errors)

### Completion Verification Workflow

**Complete Verification Function**:

```python
def verify_agent_completion(agent_name: str) -> tuple[bool, str]:
    """
    Comprehensive completion verification.

    Returns:
        (success, message): True if complete, with explanation
    """

    # Read state
    try:
        state = read_json("~/.claude/workflows/current_task.json")
    except FileNotFoundError:
        return False, "State file not found"

    # Universal checks
    if not is_agent_complete(state):
        status = state["state"]["status"]
        violations = state["quality"]["violations_total"]
        can_proceed = state["quality"]["can_proceed"]

        if status != "completed":
            return False, f"Status: {status} (not completed)"
        if violations != 0:
            return False, f"{violations} violations remain"
        if not can_proceed:
            return False, "Quality gates failed"

    # Agent-specific checks
    if agent_name == "implementer-spark":
        success, msg = verify_implementer_specific(state)
        if not success:
            return False, f"Implementer: {msg}"

    elif agent_name == "analyzer-spark":
        success, msg = verify_analyzer_specific(state)
        if not success:
            return False, f"Analyzer: {msg}"

    elif agent_name == "tester-spark":
        success, msg = verify_tester_specific(state)
        if not success:
            return False, f"Tester: {msg}"

    elif agent_name == "designer-spark":
        success, msg = verify_designer_specific(state)
        if not success:
            return False, f"Designer: {msg}"

    elif agent_name == "documenter-spark":
        success, msg = verify_documenter_specific(state)
        if not success:
            return False, f"Documenter: {msg}"

    # All checks passed
    return True, "Agent completed successfully"
```

---

## Summary

This guide provides detailed specifications for SPARK integration:

1. **JSON State Management**: Structured communication through state files
2. **Evidence Requirements**: Agent-specific proof requirements
3. **Completion Criteria**: Universal + agent-specific validation

**Key Principle**: Evidence is mandatory. Claims without proof are worthless. State files provide transparent, verifiable communication between agents and commands.

---

**Related Documents**:
- **CONSTITUTION.md** - Core principles
- **AGENT_DESIGN_GUIDE.md** - Agent design standards
- **COMMAND_DESIGN_GUIDE.md** - Command orchestration
- **TEMPLATES.md** - Quick-start templates
