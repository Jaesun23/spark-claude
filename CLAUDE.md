# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPARK v4.3 (Subagent Performance Architecture with Reduced toKens) is a traits-based multi-agent orchestration system achieving 95.5% token reduction by loading only the required agent on-demand from a pool of 32 specialized agents.

## Core Commands

### Development & Testing
```bash
# Setup environment (recommended: uv for 10x faster installation)
uv venv && source .venv/bin/activate
uv pip install -e ".[full,dev,benchmark]"

# Run quality checks
ruff check .                    # Linting
mypy .                          # Type checking
black . --check                 # Format checking
pytest tests/                   # Run all tests
pytest tests/test_specific.py  # Run single test file

# Benchmark agent performance
python benchmarks/run_benchmarks.py
```

### SPARK-Specific Commands

#### Single Agent Commands
- `/spark-implement <feature>` - Feature implementation with quality gates
- `/spark-test <target>` - Create comprehensive tests (95% coverage target)
- `/spark-analyze <scope>` - Multi-dimensional system analysis
- `/spark-design <system>` - Architecture and API design
- `/spark-clean` - Remove technical debt and dead code
- `/spark-fix <issue>` - Troubleshoot and fix issues
- `/spark-improve <code>` - Performance optimization and modernization
- `Task("qc-spark", "fix ruff violations")` - Quality violations cleanup (use direct Task calls)

#### Pipeline Commands (Sequential Phases)
- `/spark <complex-task>` - Full pipeline: analyze → implement → test → document
- `/spark-refactor <module>` - Refactor pipeline: analyze → improve → test
- `/spark-audit <system>` - Audit: analyze → troubleshoot → document
- `/spark-migrate <legacy>` - Migration: analyze → design → implement → test
- `/spark-optimize <scope>` - Optimize: analyze → improve → test
- `/spark-launch <feature>` - Complete: design → implement → test → document → git

#### Parallel Execution
- `/multi-implement task1,task2,task3,task4,task5` - Execute up to 5 tasks in parallel using team agents

## Architecture & Execution Flow

### Three-Layer System
1. **Router Layer** (`.claude/hooks/spark_persona_router.py`) - Analyzes task and selects optimal agent
2. **Quality Gates** (`.claude/hooks/spark_quality_gates.py`) - Verifies agent claims vs actual results  
3. **Agent Layer** (`.claude/agents/`) - 32 specialized agents (17 primary + 15 team)

### Critical Execution Protocol for Claude Code

When receiving SPARK commands, you MUST follow this exact pattern:

```python
# For single agent:
1. IMMEDIATELY CALL:
   Task("agent-name-spark", user_request)
2. WAIT for completion
3. CHECK ~/.claude/workflows/current_task.json:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"
4. DECISION:
   ✅ ALL MET → Report success
   ❌ ANY FAILED → Retry with feedback (max 3 attempts)

# For parallel execution (MUST be in ONE message):
Task("team1-implementer-spark", task1)
Task("team2-implementer-spark", task2)
Task("team3-implementer-spark", task3)
Task("team4-implementer-spark", task4)
Task("team5-implementer-spark", task5)
# WAIT for ALL to complete
```

### Phase Structure (All Agents)

Every agent follows this 5-phase structure:
- **Phase 0**: Task Initialization (read JSON state)
- **Phase 1-4**: Agent-specific work
- **Phase 5A**: Quality metrics recording
- **Phase 5B**: Quality gates execution (MANDATORY)
  - Must check for "Quality gates PASSED" or "Quality gates FAILED"
  - All violations must be 0 to proceed
  - Maximum 3 retry attempts

### Quality Gates Verification

```bash
# Agent self-validation
echo '{"subagent": "implementer-spark", "self_check": true}' | \
python3 ~/.claude/hooks/spark_quality_gates.py

# Returns English messages:
# ✅ "Quality gates PASSED"
# 🚫 "Quality gates FAILED"
```

## Token Management

### Safety Limits
- **Hard limit**: 200K tokens per agent context
- **Practical limit**: 90K tokens (safety margin)
- **Write operations**: Double token consumption
- **Agent sizes**: ~1K (team agents) to ~3.9K (implementer-spark)

### Critical Rules
- Agents CANNOT call other agents (only Claude Code uses Task tool)
- Write operations consume 2x tokens (memory + output)
- All agents include 90K token safety protocol
- Compression available for 30-50% reduction

## JSON State Management

Agents communicate via JSON state files:
```
~/.claude/workflows/current_task.json         # Main task state
~/.claude/workflows/team[1-5]_current_task.json  # Team-specific states
```

Structure:
```json
{
  "id": "spark_YYYYMMDD_HHMMSS",
  "version": "4.3",
  "state": {"status": "pending|running|completed|failed"},
  "quality": {
    "violations_total": 0,
    "can_proceed": true
  }
}
```

## Common Pitfalls to Avoid

- Loading multiple agents unnecessarily (use one at a time)
- Sequential Task calls for parallel execution (must be simultaneous)
- Skipping quality gate validation
- Not checking JSON state after agent completion
- Forgetting Write operations double token consumption

## Agent Specialization & Role Separation

### Primary Agents (17 total)
- **improver-spark**: Performance optimization, architecture modernization, context7 research
- **qc-spark**: Quality violations cleanup (ruff, mypy, pytest failures) with 5-phase inspection
- **analyzer-spark**: Multi-dimensional system analysis with multi-session support
- **implementer-spark**: Feature implementation with 95% test coverage requirement
- **tester-spark**: Comprehensive testing (95% unit, 85% integration) 
- **designer-spark**: System architecture and API design
- **documenter-spark**: API docs, user guides, architecture documentation
- **troubleshooter-spark**: Systematic debugging and issue resolution
- **cleaner-spark**: Dead code removal and dependency updates
- **explainer-spark**: Concept and pattern explanation
- **builder-spark**: Build process and CI/CD optimization
- **estimater-spark**: Evidence-based time and resource estimation
- **gitter-spark**: Git strategy, branching, automation
- **loader-spark**: Project context analysis and loading
- **indexer-spark**: SuperClaude command navigation
- **tasker-spark**: Multi-session project management
- **spawner-spark**: Complex multi-agent coordination

### Team Agents (15 total - 5 teams × 3 roles)
- **team[1-5]-implementer-spark**: Parallel implementation specialists
- **team[1-5]-tester-spark**: Parallel testing specialists  
- **team[1-5]-documenter-spark**: Parallel documentation specialists

### Critical Role Separation
- **Quality Control**: Use `qc-spark` for fixing violations (ruff, mypy, test failures)
- **Enhancement**: Use `improver-spark` for modernization and optimization
- **Multi-Session**: `analyzer-spark`, `improver-spark`, and `qc-spark` support progressive work

## Key File Locations

- **Agent definitions**: `.claude/agents/*-spark.md`
- **Command definitions**: `.claude/commands/spark-*.md`
- **Quality gates script**: `.claude/hooks/spark_quality_gates.py`
- **Router script**: `.claude/hooks/spark_persona_router.py`
- **JSON states**: `.claude/workflows/*.json`
- **Documentation**: `docs/SPARK_COMPLETE_GUIDE.md`