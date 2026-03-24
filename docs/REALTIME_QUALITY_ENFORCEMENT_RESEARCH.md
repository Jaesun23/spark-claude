# Real-Time Quality Enforcement System Research

**Research Date**: 2025-11-09
**Researchers**: Jason & 2호 (Claude Code)
**Purpose**: Design Google-style consistency enforcement for SPARK agents

---

## Executive Summary

This research investigates how to achieve **Google-scale code consistency** in SPARK multi-agent systems through real-time quality enforcement. The goal is to ensure agents write correct, standards-compliant code **during execution**, not just at commit time.

**Key Finding**: SPARK already has 75% of the required infrastructure. We need to strengthen enforcement at critical checkpoints.

---

## 1. SPARK-Claude Project Direction

### Core Philosophy: "Progressive Disclosure + Zero Tolerance + Plugin Distribution"

```yaml
Evolution:
  Origin: Super Claude (MCP) → Monolithic 11-persona, 600K+ tokens
  v3.0-4.2: Multi-agent System → 32 agents, lazy loading
  v4.3 (Current): Plugin System → 21 agents, 95.5% token reduction

Foundational Principles:
  - Traits-based Persona (≤5 traits per agent)
  - 3-Layer Architecture (CLAUDE.md, Commands, Agents)
  - Agent Isolation Model (Task tool only, independent sessions)
  - Evidence-Before-Report (no claims without proof)
  - Zero Tolerance Quality (violations = 0 enforced)
```

### Constitution v1.2 Key Principles

**1. Traits over Tasks**
- Define agents by WHO they are (characteristics), not WHAT they do (job functions)
- Example: "Evidence-Based Practice" trait → naturally thorough analysis
- Anti-pattern: "Analyzer + Implementer + Tester" role mixing → cognitive dissonance

**2. Separation of Concerns**
- **Layer 1 (CLAUDE.md)**: "What agents exist, when to use them, how 2号 orchestrates"
- **Layer 2 (Commands)**: "Pre-packaged workflows assisting 2号's orchestration"
- **Layer 3 (Agents)**: "How agents perform their expertise"
- Content in wrong layer = violation

**3. Agent Isolation Model**
- Agents are independent sessions spawned by Task tool
- Zero communication between running agent and 2호/other agents
- JSON files are the ONLY inter-session communication mechanism
- Agents CANNOT call other agents (no Task tool access)

**4. Proactive Context over Reactive Validation**
- OLD: Let agents explore → hook catches violations later (50K tokens wasted)
- NEW: Provide PROJECT_STANDARDS.md upfront → agent follows from start (2K tokens)
- Result: 96% token reduction, 83% time reduction

---

## 2. What Agents MUST Receive When Starting Work

### Constitution v1.2 Section 2.5: Project Context Protocol

**Mandatory Context Template**:

```python
# ✅ CORRECT: Complete task delegation with context
Task("implementer-spark", """
Task: Add user authentication endpoint

📋 Project Standards (MANDATORY - Read these first):
- PROJECT_STANDARDS.md - Logging, DB, error handling standards
- ARCHITECTURE.md - Layer structure, dependency rules
- docs/adr/*.md - Architecture decision records (if exist)

📂 Standard Modules (USE these, don't create new ones):
- common/logging/ - Use for all logging (don't use print or custom loggers)
- common/config/ - Use for all configuration
- common/db/ - Use for all database operations
- common/errors/ - Use for all error handling

⚠️ Quality Enforcement:
- Pre-commit hooks will verify compliance
- Quality gates will block if standards violated
- Do it right NOW to avoid rework later

If any required standards/modules are missing, STOP and request them.

Scope: [범위]
Depth: surface|moderate|deep
Priority: [우선순위]
Expected Output: [예상 결과물]
""")

# ❌ WRONG: Task without context
Task("implementer-spark", "Add user authentication endpoint")
# Agent will guess, violate standards, fail quality gates
```

### Why This Matters

**Token Efficiency**:
- Agent reads 3 docs (2K tokens) vs exploring randomly (50K tokens)
- 96% token reduction

**Time Efficiency**:
- 5 minutes to read standards vs 30 minutes to explore
- 83% time reduction

**Quality Improvement**:
- Proactive compliance from start
- First-time quality gates success
- No "fix later" or `--no-verify` shortcuts

### Agent Phase 0 Enforcement

From `implementer-spark.md:143-149`:

```markdown
**Phase 0: Task Understanding & Project Context Discovery**
- Read 2号's implementation brief
- **CRITICAL: Verify project context provided**
  ❌ If PROJECT_STANDARDS.md not provided → STOP, request it
  ❌ If ARCHITECTURE.md not provided → STOP, request it
  ❌ If standard modules (common/* or shared/*) not provided → STOP, request them
- **Read project standards FIRST** (saves 50K tokens later)
```

**Current Problem**: This is "SHOULD" behavior, not "MUST" behavior. Agents sometimes skip verification.

**Required Fix**: Make Phase 0 verification blocking with automatic rejection.

---

## 3. File Structure and Roles

### Layer 1 - CLAUDE.md (2号's System Prompt & Memory)

```yaml
File: spark-plugin/CLAUDE.md
Responsibility: "What agents exist, when to use them, how 2호 orchestrates"

Content:
  - Agent Registry (21 agents × ~95 tokens/description = ~2K tokens)
    └─ analyzer-spark - Multi-dimensional system analysis
       - Protocol: EVIDENCE-BEFORE-REPORT + PROJECT-CONTEXT-DISCOVERY
       - When to Use: System analysis, bottlenecks, security audits
       - Output: Evidence-based reports with file:line references

  - Delegation Protocol (MANDATORY project context)
    └─ Complete task template with PROJECT_STANDARDS.md
    └─ Information to include: scope, depth, priorities, constraints

  - State Management (JSON files)
    └─ ~/.claude/workflows/current_task.json
    └─ ~/.claude/workflows/team[1-5]_current_task.json

  - Quality Verification
    └─ Post-completion checklist
    └─ JSON validation criteria

Token Budget: ~400-600 lines total
Forbidden: ❌ Agent internals, traits, phase implementations
Who Reads: 2号 (Claude Code orchestrator) only
```

**Example - Agent Registry Entry**:
```markdown
**implementer-spark** - Feature implementation with zero defects
- **Protocol**: TEST-BEFORE-REPORT + PROJECT-CONTEXT-DISCOVERY
- **Specialization**: Phase 4 pytest mandatory, 95%+ coverage, 0 violations
- **When to Use**: API endpoints, authentication systems, database layers, UI components
- **Output**: Working code + comprehensive tests + 0 quality violations
```

---

### Layer 2 - Commands (.claude/commands/*.md)

```yaml
Files: spark-plugin/commands/*.md (12 commands)
Responsibility: "Pre-packaged workflows that assist 2号's orchestration"

Content:
  - Pre-execution checklists (project context verification)
  - Agent invocation sequences (define order)
  - Validation protocols (JSON state checks)
  - Retry strategies (max 3 attempts, escalating feedback)

Token Budget: ~300-500 lines per command
Forbidden: ❌ Agent internal logic, traits definitions, phase details
Who Reads: 2号 only (agents never see commands)
```

**Why Commands Exist** (Constitution Section 1.2.1):
> "Agents cannot call other agents → 2号 MUST orchestrate all multi-agent workflows. Commands exist because 2号 cannot memorize all orchestration protocols."

**Example - spark-implement.md:82-95**:
```markdown
PHASE 1: Implementation
1. Task("implementer-spark", user_request)
2. Wait for completion
3. Check JSON: ~/.claude/workflows/current_task.json
   ✅ PASS CONDITIONS:
   - state.status == "completed"
   - quality.violations_total == 0
   - quality.can_proceed == true
   - len(output.files.created) > 0 OR len(output.files.modified) > 0

   ❌ FAIL → Retry: Task("implementer-spark", "Fix violations: [specific issues]")
   Maximum 3 retries, then abort with error report.

PHASE 2: Testing
4. Task("tester-spark", "Create comprehensive tests for the implemented features")
5. Wait for completion
6. Check JSON: coverage >= 95%, all tests passing
   ✅ PASS → Proceed to Phase 3
   ❌ FAIL → Retry with specific coverage gaps

PHASE 3: Documentation
7. Task("documenter-spark", "Document the implemented features")
8. Validate: Examples executable, API coverage 100%
9. Report completion to user
```

**Command Validation Protocol**:
```typescript
interface ValidationCriteria {
  // After every agent invocation
  status: "completed";
  violations_total: 0;
  can_proceed: true;

  // Agent-specific
  implementer: {
    files_changed: number > 0;
    tests_passed: number > 0;
  };

  tester: {
    coverage: number >= 95;
    test_failures: 0;
  };

  documenter: {
    examples_executable: true;
    api_coverage: 100;
  };
}
```

---

### Layer 3 - Agents (.claude/agents/*.md)

```yaml
Files: spark-plugin/agents/*.md (21 agents)
Responsibility: "How the agent performs its expertise"

Content:
  1. YAML Frontmatter
     - name, description (decision algorithm for 2号)
     - tools, model, color

  2. Core Identity & Traits (Natural Language Persona)
     - ≤5 traits defining WHO the agent is
     - Concrete, behavioral traits (not abstract)

  3. Behavior Protocol (Code-Based Rules)
     - QUALITY_REQUIREMENTS = {violations: 0}
     - FORBIDDEN_FIX_PATTERNS = ["sed -i", "--fix"]
     - Validation methods

  4. Professional Workflow Methodology
     - Phase 0: Task Understanding & Project Context Discovery
     - Phase 1-N: Domain Work (flexible, iterative)
     - Phase N+1: Quality Verification (MANDATORY)

  5. Quality Gates (Phase 5A/5B)
  6. Multi-Session Support
  7. 90K Token Safety Protocol
  8. Example Usage Scenarios

Token Budget: 400-700 lines per agent (post-Constitution)
Forbidden: ❌ 2号 orchestration logic, command logic
Who Reads: The agent itself (loaded only when Task is called)
```

**7-Section Structure - implementer-spark Example**:

**Section 1: YAML Frontmatter**
```yaml
---
name: implementer-spark
description: |
  Feature implementation specialist ensuring zero-defect code
  delivery with comprehensive testing. Use for API endpoints,
  authentication systems, database layers, UI components.
tools: [Bash, Read, Edit, Write, TodoWrite, WebSearch, ...]
model: sonnet
color: pink
---
```

**Section 2: Core Identity & Traits**
```markdown
## Core Identity & Traits (Natural Language Persona)

**Systematic Execution:** You analyze requirements methodically, create
structured implementation plans, and execute from foundation through
business logic to quality verification in a disciplined manner.

**Simplicity-First:** You favor elegant, straightforward solutions that
penetrate to the essence of the problem rather than complex implementations.

**Attention to Detail:** You meticulously handle edge cases, implement
comprehensive logging and error handling, validate all inputs.

**Structural Integrity:** You strictly adhere to architectural layers,
never create circular dependencies, ensure zero static analysis errors.

**Collaboration-Oriented:** You write highly readable, maintainable code
that enables testing specialists and documentation experts to understand.
```

**Section 3: Behavior Protocol**
```python
class ImplementerBehavior:
    """Concrete behavioral rules that MUST be followed."""

    QUALITY_REQUIREMENTS = {
        "ruff_errors": 0,           # Must be exactly 0
        "mypy_errors": 0,           # Must be exactly 0
        "black_violations": 0,      # Must be exactly 0
        "test_failures": 0,         # CRITICAL!
    }

    FORBIDDEN_FIX_PATTERNS = [
        "sed -i",           # NEVER bulk edit
        "awk",              # NEVER script replacements
        "--fix",            # NEVER auto-fix flags
        "--unsafe-fixes",   # ABSOLUTELY NEVER
    ]

    def fix_quality_issues(self, issues: list) -> None:
        """Fix quality issues ONE BY ONE manually.

        WHY: Automated scripts ALWAYS damage working code.
        They cannot understand context and will destroy
        valid code patterns while trying to fix errors.
        """
        for issue in issues:
            self.read_error_context(issue)
            self.understand_root_cause(issue)
            self.apply_surgical_fix(issue)
            self.verify_fix_safety(issue)
```

**Section 4: Workflow Methodology**
```markdown
## Professional Workflow Methodology

1. 대상 인식 → What am I implementing?
2. 깊이 판단 → How complete? (MVP vs production-ready)
3. 방법 선택 → What approach? (architecture, patterns, libraries)
4. 작업 실행 → Write code, add tests, ensure quality
5. 결과 관찰 → Run tests, check quality tools
6. 해석 → Does this meet requirements?
7. 충분성 판단 → Sufficient? → If no, iterate from step 4

### Phase Structure (Flexible)

**Phase 0: Task Understanding & Project Context Discovery**
- Read 2号's implementation brief
- CRITICAL: Verify project context provided
  ❌ If PROJECT_STANDARDS.md not provided → STOP
  ❌ If ARCHITECTURE.md not provided → STOP
- Read project standards FIRST (saves 50K tokens)

**Phase 1: Design & Planning**
- Analyze requirements, identify modules/classes
- Design data models, API contracts

**Phase 2-3: Implementation** (iterative)
- Write code incrementally
- Add logging, error handling
- Manual quality fixes (no --fix flags)

**Phase 4: Testing** (MANDATORY)
- Write comprehensive tests
- Run pytest with coverage
- Achieve 95%+ coverage target

**Phase 5A: Quality Metrics Recording**
- Run ruff check . --exit-zero --statistics
- Run mypy . --strict
- Run pytest --cov=src --cov-fail-under=95
- Record all metrics

**Phase 5B: Quality Gates Execution**
- Verify violations_total == 0
- If FAILED → manual fixes, max 3 retries
- If PASSED → report completion
```

---

## 4. Plugin System Architecture

### Distribution Model (v4.3)

```
spark-claude/
├── spark-plugin/              # Distributable plugin package
│   ├── .claude-plugin/
│   │   ├── plugin.json        # Metadata (name, version, author)
│   │   └── marketplace.json   # Local marketplace config
│   ├── CLAUDE.md              # Complete SPARK usage guide
│   ├── README.md              # User documentation
│   ├── agents/                # 21 agent definitions
│   │   ├── analyzer-spark.md
│   │   ├── implementer-spark.md
│   │   ├── tester-spark.md
│   │   ├── documenter-spark.md
│   │   ├── designer-spark.md
│   │   ├── qc-spark.md
│   │   └── team[1-5]-*.md     # 15 team agents
│   └── commands/              # 12 SPARK commands
│       ├── spark-implement.md
│       ├── spark-analyze.md
│       ├── multi-implement.md
│       └── ...
└── docs/                      # Development docs (not distributed)
    ├── docs-backup/           # Previous documentation archive
    └── constitution/          # SPARK Constitution v1.2
```

### Installation

```bash
# 1. Add local marketplace
/plugin marketplace add /path/to/spark-claude/spark-plugin

# 2. Install plugin
/plugin install spark-agents@spark-dev-marketplace

# 3. Verify
/context  # Shows 21 agents as "Plugin" type
```

### Progressive Disclosure Mechanism

**How It Works**:
```
1. Initial Load: Only agent descriptions loaded (~2K tokens, 1% of context)
   └─ 21 agents × ~95 tokens/description = ~2.0K tokens

2. Selection: 2号 analyzes task → selects optimal agent
   └─ Based on description's "When to Use" section

3. Full Load: Only selected agent's body loaded (30-44K tokens)
   └─ Agent file content loaded into agent session

Traditional Approach: Load all agents upfront (600K+ tokens) ❌
```

**Token Efficiency**:
```
SPARK v4.3 (Progressive Disclosure):
- Registry load: ~2K tokens (21 descriptions)
- Agent execution: 30-44K tokens (1 agent)
- Total: ~35-46K tokens
- Efficiency: 95.5% reduction

Traditional (Pre-load All):
- All agents loaded: 600K+ tokens
- Wasted tokens: 560K+ (agents not used)
- Result: Context overflow, slow performance
```

**Benefits**:
- ✅ **Instantly installable**: One command installs all 21 agents
- ✅ **Self-documenting**: CLAUDE.md included in plugin
- ✅ **Version controlled**: plugin.json manages versions
- ✅ **Portable**: Works across all projects automatically
- ✅ **Efficient**: 95.5% token reduction through lazy loading

### Plugin Metadata

**plugin.json**:
```json
{
  "name": "spark-agents",
  "description": "SPARK v4.3 - 21 specialized AI agents with zero-tolerance quality gates and 95.5% token reduction",
  "version": "4.3.0",
  "author": {
    "name": "Jason (Jaesun23)",
    "email": "jaesun23@users.noreply.github.com"
  }
}
```

---

## 5. Real-Time Quality Enforcement Design

### Current State Analysis

SPARK already implements **4-layer quality system**:

```
Layer 1 (Proactive): Project Context Protocol
├─ 2号 provides PROJECT_STANDARDS.md to agents
├─ Status: ⚠️ "SHOULD" not "MUST" (sometimes skipped)
└─ Fix: Make mandatory with blocking enforcement

Layer 2 (Phase 0): Agent Context Discovery
├─ Agents read standards in Phase 0
├─ Status: ⚠️ Weak validation (read but not applied)
└─ Fix: Add verification checkpoints in Phase 0

Layer 3 (Phase 5A/5B): Quality Gates
├─ Phase 5A: Record metrics (ruff, mypy, pytest)
├─ Phase 5B: Verify violations == 0
├─ Status: ✅ Working well
└─ Enhancement: Automate Phase 5B validation

Layer 4 (Git): Pre-commit Hooks
├─ Project-level .pre-commit-config.yaml
├─ Status: ✅ Working (ruff --fix, mypy, black)
└─ Enhancement: Standardize across projects
```

### Gap Analysis

**Missing Layer: Write/Edit Immediate Validation**

```
Current Flow:
Agent writes code → (multiple edits) → Phase 5A → ❌ 100 errors found!

Desired Flow:
Agent writes code → ✅ Immediate check → Fix → ✅ → Next edit
```

**Problem**: Agents can accumulate violations during Phase 2-3, only discovering them in Phase 5A.

**Solution**: Add on_file_write hook for immediate validation.

---

### Proposed: 5-Layer Real-Time Enforcement System

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 0: Standards Definition (Project-Level)              │
│ ├─ PROJECT_STANDARDS.md (logging, DB, error handling)      │
│ ├─ ARCHITECTURE.md (layers, dependencies, boundaries)      │
│ ├─ pyproject.toml (ruff, mypy, black, pytest config)       │
│ └─ .pre-commit-config.yaml (git hooks)                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Context Provision (MANDATORY)                     │
│ ├─ 2号 MUST provide PROJECT_STANDARDS.md in Task call      │
│ ├─ Blocking: Reject tasks without required context         │
│ └─ Template: Complete task delegation (scope, depth, etc)  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Phase 0 Verification (Agent)                      │
│ ├─ Read PROJECT_STANDARDS.md, ARCHITECTURE.md              │
│ ├─ Verify understanding with checklist                     │
│ ├─ STOP if context missing or unclear                      │
│ └─ Record context hash for Phase 5 validation              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Write/Edit Immediate Check (NEW - Experimental)   │
│ ├─ Hook: on_file_write triggers after Write/Edit tool      │
│ ├─ Run: ruff check --fix {file} (0.1s)                     │
│ ├─ Run: mypy --strict {file} (0.5s)                        │
│ ├─ Block: If errors found, show to agent immediately       │
│ └─ Benefit: Catch violations in real-time, not Phase 5     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Quality Gates Phase 5A/5B (Comprehensive)         │
│ ├─ Phase 5A: Record all metrics (ruff, mypy, pytest)       │
│ ├─ Phase 5B: Verify violations_total == 0                  │
│ ├─ Manual fixes only (no --fix flags in Phase 5B)          │
│ └─ Max 3 retries, then fail                                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: Git Pre-commit Hooks (Final Defense)              │
│ ├─ Ruff --fix, mypy, black, trailing-whitespace            │
│ ├─ Architecture validation (custom hooks)                  │
│ ├─ Auto-fix where safe, block on errors                    │
│ └─ Already implemented in memory-one-spark project         │
└─────────────────────────────────────────────────────────────┘
```

### Implementation Plan

#### Phase 1: Strengthen Existing Layers (Immediate)

**1.1 Make Layer 1 Mandatory** (Update CLAUDE.md)
```markdown
## Agent Delegation Protocol (MANDATORY - ENFORCED)

2号 MUST provide complete project context when calling any agent:

✅ REQUIRED in every Task call:
- PROJECT_STANDARDS.md path
- ARCHITECTURE.md path
- Standard modules list (common/*, shared/*)
- Expected quality metrics (coverage %, max violations)

❌ BLOCKING: Task calls WITHOUT context will be rejected.

Template:
Task("implementer-spark", """
Task: [description]

📋 MANDATORY CONTEXT:
- PROJECT_STANDARDS: docs/PROJECT_STANDARDS.md
- ARCHITECTURE: docs/ARCHITECTURE.md
- STANDARD_MODULES: common/{logging,config,db,errors}

📊 QUALITY TARGETS:
- Test coverage: 95%+
- Ruff violations: 0
- MyPy errors: 0

[... rest of task description ...]
""")
```

**1.2 Strengthen Phase 0 Validation** (Update all agent files)
```markdown
**Phase 0: Task Understanding & Project Context Discovery**

STEP 1: Verify Context Provided
```bash
# BLOCKING CHECKS (fail immediately if missing)
if "PROJECT_STANDARDS" not in task_description:
    STOP and report: "❌ PROJECT_STANDARDS.md not provided. Cannot proceed."
if "ARCHITECTURE" not in task_description:
    STOP and report: "❌ ARCHITECTURE.md not provided. Cannot proceed."
```

STEP 2: Read and Verify Understanding
```bash
# Read standards
read PROJECT_STANDARDS.md
read ARCHITECTURE.md

# Verify understanding with checklist
- [ ] Logging: Which module? (common/logging/)
- [ ] Config: Which module? (common/config/)
- [ ] DB: Which module? (common/db/)
- [ ] Errors: Which module? (common/errors/)
- [ ] Layer rules: What dependencies allowed?
```

STEP 3: Record Context Hash
```python
# Save to JSON for Phase 5 validation
{
  "context_verification": {
    "standards_read": True,
    "architecture_read": True,
    "modules_identified": ["common/logging", "common/config", ...],
    "phase0_complete": True
  }
}
```

If ANY check fails → STOP, request clarification.
```

#### Phase 2: Add Layer 3 (Experimental - Requires Testing)

**2.1 Create on_file_write Hook**

File: `.claude/hooks/on_file_write.py`
```python
#!/usr/bin/env python3
"""
Real-time quality validation on file write/edit.
Triggers immediately after Write/Edit tool use.

EXPERIMENTAL: Requires Claude Code hooks support.
Constitution v1.2 Section 1.2.2 - Hooks are experimental.
"""

import subprocess
import sys
from pathlib import Path

def validate_file(file_path: str) -> bool:
    """
    Validate file immediately after write/edit.

    Returns:
        True if validation passed
        False if violations found (blocks operation)
    """
    path = Path(file_path)

    # Skip non-Python files
    if path.suffix != ".py":
        return True

    # Skip test files (different rules)
    if "test_" in path.name or path.parts[-2] == "tests":
        return True

    violations = []

    # Check 1: Ruff (fast, 0.1s)
    result = subprocess.run(
        ["ruff", "check", "--exit-zero", str(path)],
        capture_output=True,
        text=True
    )
    if result.returncode != 0 or result.stdout.strip():
        violations.append(f"RUFF: {result.stdout}")

    # Check 2: MyPy (slower, 0.5s, but critical)
    result = subprocess.run(
        ["mypy", "--strict", "--no-error-summary", str(path)],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        violations.append(f"MYPY: {result.stdout}")

    # Report results
    if violations:
        print(f"❌ Quality violations in {path.name}:")
        for v in violations:
            print(f"  {v}")
        print(f"\n🚫 Fix these violations before proceeding.")
        return False

    print(f"✅ Quality check passed: {path.name}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: on_file_write.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_file(file_path)
    sys.exit(0 if success else 1)
```

**2.2 Register Hook in settings.json**

File: `.claude/settings.json`
```json
{
  "hooks": {
    "on_file_write": {
      "script": ".claude/hooks/on_file_write.py",
      "args": ["{file_path}"],
      "blocking": true,
      "timeout": 5000
    }
  }
}
```

**2.3 Testing Protocol**

```bash
# Test 1: Write file with violations
# Expected: Hook blocks, shows errors

# Test 2: Write file without violations
# Expected: Hook passes silently

# Test 3: Performance test
# Expected: Hook completes in <1 second

# Test 4: Edge cases
# - Non-Python files (should skip)
# - Test files (should skip)
# - Large files (should timeout gracefully)
```

**IMPORTANT**: This is EXPERIMENTAL. Constitution v1.2 Section 1.2.2 states hooks are experimental and require thorough testing before production use.

#### Phase 3: Automate Layer 4 Validation

**3.1 Quality Gates Auto-Validation Script**

File: `.claude/hooks/validate_quality_gates.py`
```python
#!/usr/bin/env python3
"""
Automated quality gates validation for Phase 5B.
Reads current_task.json and verifies all metrics.
"""

import json
import sys
from pathlib import Path

def validate_quality_gates(task_json_path: str) -> dict:
    """
    Validate quality gates from task JSON.

    Returns:
        {
            "passed": bool,
            "violations": list[str],
            "metrics": dict
        }
    """
    # Read task JSON
    with open(task_json_path) as f:
        task = json.load(f)

    violations = []

    # Universal checks
    if task["quality"]["violations_total"] != 0:
        violations.append(
            f"violations_total = {task['quality']['violations_total']} (expected 0)"
        )

    if not task["quality"]["can_proceed"]:
        violations.append("can_proceed = False")

    if task["state"]["status"] != "completed":
        violations.append(f"status = {task['state']['status']} (expected 'completed')")

    # Agent-specific checks
    agent = task["agent"]

    if agent == "implementer-spark":
        if task.get("tests", {}).get("failed", 0) > 0:
            violations.append(f"test failures = {task['tests']['failed']}")
        if task.get("coverage", {}).get("percent", 0) < 95:
            violations.append(f"coverage = {task['coverage']['percent']}% (target 95%)")

    if agent == "tester-spark":
        if task.get("coverage", {}).get("percent", 0) < 95:
            violations.append(f"unit coverage = {task['coverage']['percent']}% (target 95%)")

    if agent == "analyzer-spark":
        if len(task.get("evidence", [])) < 8:
            violations.append(f"evidence items = {len(task['evidence'])} (minimum 8)")

    # Return results
    return {
        "passed": len(violations) == 0,
        "violations": violations,
        "metrics": task.get("quality", {})
    }

if __name__ == "__main__":
    result = validate_quality_gates(sys.argv[1])

    if result["passed"]:
        print("✅ Quality gates PASSED")
        sys.exit(0)
    else:
        print("🚫 Quality gates FAILED")
        for v in result["violations"]:
            print(f"  - {v}")
        sys.exit(1)
```

**3.2 Update Phase 5B in All Agents**

```markdown
**Phase 5B: Quality Gates Execution**

```bash
# Automated validation
python ~/.claude/hooks/validate_quality_gates.py ~/.claude/workflows/current_task.json

# Check result
if validation_passed:
    ✅ All quality gates passed
    → Record completion timestamp
    → Report success to 2号
else:
    🚫 Quality gates FAILED
    → Review violations list
    → Manual fixes (no --fix flags)
    → Re-run Phase 5A
    → Retry Phase 5B (max 3 attempts)
```

CRITICAL: If max retries exceeded (3), STOP and report failure with full violation details.
```

---

### Google-Style Consistency Comparison

```
┌──────────────────────────────────────────────────────────────┐
│                    Google Engineering                        │
├──────────────────────────────────────────────────────────────┤
│ 1. Style Guide (google.github.io/styleguide/pyguide.html)   │
│    ├─ Comprehensive coding standards                        │
│    ├─ Auto-formatter (Pyink/Black) configuration            │
│    └─ Editor integration (Vim, Emacs settings)              │
│                                                              │
│ 2. Code Review (Critique, Gerrit)                           │
│    ├─ Pre-submit checks (lint, type, test)                  │
│    ├─ Automated reviewers (blocking)                        │
│    └─ Human review required                                 │
│                                                              │
│ 3. Continuous Integration                                   │
│    ├─ Pre-submit: Fast checks (5-10 min)                    │
│    ├─ Post-submit: Full suite (30+ min)                     │
│    └─ Auto-revert on failures                               │
│                                                              │
│ 4. Monorepo Standards                                        │
│    ├─ Bazel build system (hermetic, reproducible)           │
│    ├─ Shared libraries (//base, //util)                     │
│    └─ Consistent structure across 2B+ LOC                   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    SPARK Equivalent                          │
├──────────────────────────────────────────────────────────────┤
│ 1. PROJECT_STANDARDS.md + pyproject.toml                    │
│    ├─ Project-specific coding standards                     │
│    ├─ Ruff/Black/MyPy configuration                         │
│    └─ Agent reads in Phase 0 (proactive)                    │
│                                                              │
│ 2. Quality Gates (Phase 5A/5B)                              │
│    ├─ Pre-completion checks (ruff, mypy, pytest)            │
│    ├─ Automated validation (blocking)                       │
│    └─ Manual fixes required (no auto-fix)                   │
│                                                              │
│ 3. Multi-Layer Enforcement                                  │
│    ├─ Layer 3: Write/edit immediate check (experimental)    │
│    ├─ Layer 4: Quality gates comprehensive                  │
│    └─ Layer 5: Pre-commit hooks                             │
│                                                              │
│ 4. Plugin Distribution                                       │
│    ├─ Portable agents (work across projects)                │
│    ├─ Standard modules (common/*, shared/*)                 │
│    └─ Consistent structure via Constitution                 │
└──────────────────────────────────────────────────────────────┘
```

**Key Similarity**: Both enforce standards **proactively** (before errors accumulate) and **automatically** (minimal human intervention).

**SPARK Advantage**: Agent-aware enforcement (different agents have different quality requirements).

**Google Advantage**: Monorepo scale (2B+ lines), decades of refinement.

---

## 6. Next Steps

### Immediate Actions (Week 1)

1. **Strengthen Layer 1** (2 hours)
   - Update `spark-plugin/CLAUDE.md` with MANDATORY context protocol
   - Add blocking checks in delegation section
   - Test with implementer-spark task

2. **Strengthen Layer 2** (4 hours)
   - Update all 6 core agent Phase 0 sections
   - Add context verification checklist
   - Add STOP conditions for missing context

3. **Document Standards** (3 hours)
   - Create PROJECT_STANDARDS.md template
   - Create ARCHITECTURE.md template
   - Add to docs/ and spark-plugin/examples/

### Experimental Phase (Week 2-3)

4. **Prototype Layer 3 Hook** (8 hours)
   - Implement on_file_write.py
   - Test with small project (10-20 files)
   - Measure performance impact (<1s acceptable)
   - Document findings

5. **Evaluate Hook Viability** (4 hours)
   - Test with memory-one-spark project
   - Collect metrics (false positives, performance)
   - Decision: Adopt, refine, or defer

### Long-term (Month 2-3)

6. **Standardize Across Projects** (ongoing)
   - Roll out PROJECT_STANDARDS.md to all projects
   - Update pre-commit configs consistently
   - Create project setup script

7. **Constitution v1.3** (when ready)
   - If hooks prove viable: Promote from experimental
   - Add Layer 3 to official architecture
   - Update all agent definitions

---

## 7. Open Questions

1. **Hook Performance**: Will on_file_write hook slow down agents too much?
   - Hypothesis: 0.5-1s per file is acceptable
   - Need: Benchmark on real projects

2. **Hook Reliability**: Can hooks catch all violations?
   - Hypothesis: 80-90% catch rate (good enough)
   - Need: False positive/negative analysis

3. **Context Provision Enforcement**: How to make Layer 1 truly mandatory?
   - Option A: Update 2호's system prompt with blocking check
   - Option B: Add validation in Task tool (requires Claude Code changes)
   - Option C: Post-hoc validation in agent Phase 0 (current approach)

4. **Standards Template Maintenance**: Who updates PROJECT_STANDARDS.md?
   - Best practice: Human architect (Jason) reviews quarterly
   - Agents can propose updates via PRs
   - Version control in git

---

## 8. Conclusion

SPARK already implements **75% of Google-style quality enforcement**:
- ✅ Proactive context provision (PROJECT_STANDARDS.md)
- ✅ Phase 0 verification (agents read standards)
- ✅ Quality gates (Phase 5A/5B with 0 violations)
- ✅ Git pre-commit hooks (ruff, mypy, black)

**Missing 25%**:
- ⚠️ Real-time write/edit validation (experimental hooks)
- ⚠️ Truly mandatory context provision (currently "should", not "must")
- ⚠️ Automated Phase 5B validation (currently manual)

**Recommendation**: Strengthen existing layers first (Week 1), then experiment with Layer 3 hooks (Week 2-3). Don't rush hooks into production—Constitution v1.2 Section 1.2.2 warns they're experimental for good reason.

**Success Metrics**:
- Quality gates first-time pass rate: Target 90%+ (currently ~70%)
- Token efficiency: Maintain 95%+ reduction
- Agent rework rate: Target <10% (currently ~30%)

Jason이 원하시는 **"작업하면서 제대로 작업하기"**는 Layer 1+2 강화만으로도 80% 달성 가능해요. Layer 3는 나머지 20%를 위한 최적화입니다.

---

**Research Complete**: 2025-11-09
**Next Action**: Review with Jason → Prioritize implementation phases → Begin Week 1 tasks
