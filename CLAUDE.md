# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPARK v4.1 (Subagent Performance Architecture with Reduced toKens) is a traits-based multi-agent orchestration system for Claude Code. Inspired by SuperClaude's persona system but developed as an independent project, SPARK achieves 95.5% token reduction by loading only the required agent on-demand rather than all 28 agents simultaneously.

### Evolution History
- **v3.0**: Initial SPARK release with lazy loading, token optimization, and workflow automation
- **v3.5**: Stabilization with enhanced quality gates and refined hook system
- **v3.8**: Revolutionary TRAITS system replacing persona scanning with 3-5 instant traits
- **v4.1**: Unified Phase structure with JSON state management and 8-step quality gates

## Core Architecture

### Three-Layer System
1. **Router Layer** (`.claude/hooks/spark_persona_router.py`): Analyzes tasks and selects optimal agent
2. **Quality Gates Layer** (`.claude/hooks/spark_quality_gates.py`): Compares agent claims vs actual measurements
3. **Agent Layer** (`.claude/agents/`): 28 specialized agents using TRAITS methodology
   - 16 primary agents: analyzer, designer, implementer, tester, documenter, improver, troubleshooter, cleaner, explainer, builder, estimater, gitter, spawner, loader, indexer, tasker
   - 12 team agents: team1-4 × (implementer/tester/documenter) for parallel execution

### TRAITS System (Revolutionary in v3.8)
Each agent now operates with 3-5 core traits, eliminating the 11-persona scanning overhead from earlier systems:
- **Traits**: Dynamic behavioral characteristics (e.g., 시스템_사고, 분석적_추론, 증거_기반_실천)
- **35% cognitive load reduction** vs persona scanning
- **Immediate trait activation** without scanning overhead
- **Miller's 7±2 cognitive theory** validation

## Development Commands

### Setup
```bash
# Recommended: uv (10x faster than pip)
uv venv && source .venv/bin/activate
uv pip install -e ".[full,dev,benchmark]"

# Alternative: pip
pip install -e ".[full,dev,benchmark]"
```

### Quality Validation (8-Step Protocol)

All agents must update the quality section in Phase 5B with actual measurements:
1. **Architecture**: imports=0, circular=0, domain=0
2. **Foundation**: syntax=0, types=0  
3. **Standards**: formatting=0, conventions=0
4. **Operations**: logging=0, security=0, config=0
5. **Quality**: linting=0, complexity=0
6. **Testing**: coverage≥95% (or -1 if not applicable)
7. **Documentation**: docstrings=0, readme=0
8. **Integration**: final=0

```bash
# Agent self-validation (compares claims vs reality)
echo '{"subagent": "implementer-spark", "self_check": true}' | 
python3 ~/.claude/hooks/spark_quality_gates.py

# Result messages:
# ✅ 품질게이트를 통과하였습니다. 작업을 정리하고 종료하시기 바랍니다.
# 🚫 품질게이트를 통과하지 못했습니다. 다시 오류수정하세요!!
#    모든 오류가 0이 아니면 작업종료 불가능합니다.
```

### Testing Hooks
```bash
# Test routing system
echo '{"prompt": "implement API endpoint"}' | python3 .claude/hooks/spark_persona_router.py

# Test quality gates
echo '{"subagent": "implementer-spark", "self_check": true}' | python3 .claude/hooks/spark_quality_gates.py

# Test orchestrator
echo '{"prompt": "analyze codebase"}' | python3 .claude/hooks/spark_unified_orchestrator.py
```

## Critical Token Management

### 90K Token Safety Limit
- **Hard limit**: 200K tokens per agent context
- **Practical limit**: 90K tokens (safety margin)
- **Write operations**: Double token consumption (memory + output)
- **Compression**: 30-50% reduction via default strategies
- **Pre-task assessment**: Mandatory for all agents

### Token Consumption by Agent
- **Smallest**: team agents (~815-1,108 tokens)
- **Average**: ~2,370 tokens per agent
- **Largest**: implementer-spark (~3,869 tokens)
- **Total savings**: 95.5% vs loading all agents

## Agent Communication Rules

### Task Tool Usage
- **ONLY Claude CODE** can use Task tool to invoke agents
- **Agents CANNOT** call other agents directly
- **JSON state files** for inter-agent communication
- **Parallel execution**: Multiple Task calls in ONE message

### JSON State Management
```python
# Team coordination files
~/.claude/workflows/team1_current_task.json
~/.claude/workflows/team2_current_task.json
~/.claude/workflows/team3_current_task.json
~/.claude/workflows/team4_current_task.json

# General workflow state
~/.claude/workflows/current_task.json
~/.claude/workflows/task_aborted.json
```

## Phase Structure (v4.1)

### Universal Phase Pattern
- **Phase 0**: Task Initialization (all agents)
- **Phase 1-3**: Agent-specific work
- **Phase 4**: Quality validation (some agents)
- **Phase 5**: Task Completion
  - Part A: Agent-specific completion
  - Part B: JSON update & quality gates (all agents)

### Quality Gates System

All agents record violations as numbers (0 = pass):
- **Zero tolerance**: All violations must be 0
- **Script verification**: Mandatory after JSON update
- **Maximum 3 retries**: Fix and re-validate
- **Numeric recording**: No ambiguous pass/fail

## JSON State Management (v4.1)

### Simplified Structure
```json
{
  "id": "spark_20250118_190418",
  "version": "4.1",
  "task": {
    "prompt": "user request",
    "execution_mode": "single|pipeline|parallel"
  },
  "state": {
    "current_agent": "agent-name",
    "status": "pending|running|completed|failed"
  },
  "quality": {
    "step_1_architecture": {"imports": 0, "circular": 0},
    "step_2_foundation": {"syntax": 0, "types": 0},
    // ... 8 steps total
    "violations_total": 0,
    "can_proceed": true
  }
}
```

## Multi-Team Parallel Execution

### Command Usage
```bash
# Initialize multi-team execution
/multi_implement TASK-001 TASK-002 TASK-003 TASK-004
```

### Usage Pattern
```python
# Invoke 4 teams simultaneously (MUST be in one message)
Task("team1-implementer-spark", "Backend services")
Task("team2-implementer-spark", "API layer") 
Task("team3-implementer-spark", "Database layer")
Task("team4-implementer-spark", "Frontend components")

# WRONG: Sequential calls break parallelism
Task("team1-implementer-spark", task1)
# wait for result...
Task("team2-implementer-spark", task2)  # This is sequential!
```

### Team Coordination
- Each team has dedicated JSON state file
- Independent execution with shared resource locks
- Automatic handoff between implementer → tester → documenter

## Project Structure
```
spark-claude/
├── .claude/
│   ├── agents/          # 28 TRAITS-based agents
│   ├── hooks/           # Router and orchestrator
│   └── workflows/       # JSON state management
├── benchmarks/          # Performance tests
├── docs/
│   ├── agents-task/     # Agent reports
│   └── templates/       # Report templates
├── scripts/             # Installation
└── tests/               # Test suite
```

## Agent Standard Structure

All agents follow this consistent structure:
1. **YAML frontmatter** (metadata)
2. **Core Identity & Traits** (3-5 traits defining behavior)
3. **5-Phase Methodology** (systematic approach)
4. **Trait-Driven Adaptations** (behavioral variations)
5. **Resource Requirements** (token budget, memory)
6. **Token Safety Protocol** (90K limit enforcement)
7. **Mandatory Reporting** (completion reports)

## Implementation Best Practices

### When Working with Agents
1. Always check token budget before starting
2. Use compression strategies for large tasks
3. Generate reports after completion
4. Update JSON state files for coordination
5. Run quality gates before marking complete

### Common Pitfalls to Avoid
- Loading multiple agents unnecessarily
- Forgetting Write operations double tokens
- Skipping quality gate validation
- Not updating team JSON files in parallel execution
- Attempting agent-to-agent direct calls

## Key v4.1 Updates

### Quality Gates System Enhancement
- **Purpose**: Verify agent honesty by comparing claimed vs actual measurements
- **Enforcement**: All violations must be 0 to proceed
- **Self-validation**: Agents run quality checks before completion
- **No JSON modification**: Quality gates only read and verify, never modify JSON files

### Multi-Team Implementation Updates
- **Agent names**: Fixed to match SPARK convention (team1-implementer-spark)
- **JSON structure**: Aligned with v4.1 template
- **Phase structure**: Matches 5-phase methodology with Phase 5B quality gates
- **Korean messages**: Clear pass/fail instructions

## Documentation References

- **README.md**: Project overview and setup
- **docs/ARCHITECTURE.md**: System design and components
- **docs/spark-agent-phase-structure-v4.1.md**: Phase execution patterns
- **docs/spark-team-agents-guide-v4.1.md**: Multi-team coordination
- **pyproject.toml**: Dependencies and configurations
- **benchmarks/**: Performance verification