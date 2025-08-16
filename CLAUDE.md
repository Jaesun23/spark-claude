# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPARK v3.8 (Subagent Performance Architecture with Reduced toKens) is a traits-based multi-agent orchestration system for Claude Code. Inspired by SuperClaude's persona system but developed as an independent project, SPARK achieves 95.5% token reduction by loading only the required agent on-demand rather than all 28 agents simultaneously.

### Evolution History
- **v3.0**: Initial SPARK release with lazy loading, token optimization, and workflow automation
- **v3.5**: Stabilization with enhanced quality gates and refined hook system
- **v3.8**: Revolutionary TRAITS system replacing persona scanning with 3-5 instant traits

## Core Architecture

### Three-Layer System
1. **Router Layer** (`.claude/hooks/spark_persona_router.py`): Analyzes tasks and selects optimal agent
2. **Orchestration Layer** (`.claude/hooks/spark_unified_orchestrator.py`): Manages agent lifecycle via 6 hooks
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
```bash
# Must pass ALL checks with 0 errors/violations
uv run mypy [file.py] --strict          # Type checking
uv run ruff check [file.py]             # Linting
uv run black [file.py]                  # Formatting
uv run pytest tests/                    # Unit tests (95% coverage required)

# Performance verification
python3 benchmarks/compare_performance.py
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

## Quality Gates System

### Mandatory Validation (16/18 Python agents)
1. **Syntax validation** (0 errors)
2. **Type checking** (mypy --strict, 0 errors)
3. **Linting** (ruff --strict, 0 violations)
4. **Security analysis** (OWASP + secrets scan)
5. **Test coverage** (Unit 95%, Integration 85%)
6. **Performance check**
7. **Documentation** (docstrings required)
8. **Integration testing**

### Self-Validation
- Maximum 3 retry attempts
- SubagentStop hook intervention on failure
- Automatic quality report generation

## Agent Reporting System

### Report Requirements
All agents generate mandatory reports after task completion:
- **Location**: `/docs/agents-task/[agent-name]/[task_name]_[timestamp].md`
- **Detailed reports** (7 agents): 500-800+ lines
- **Concise reports** (21 agents): 150-300 lines
- **Evidence-based**: File paths, line numbers, metrics
- **Templates**: Available at `/docs/templates/agent-reports/`

## Multi-Team Parallel Execution

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

## Documentation References

- **README.md**: Project overview and setup
- **pyproject.toml**: Dependencies and tool configurations
- **benchmarks/compare_performance.py**: Token efficiency verification
- **tests/**: Test suite and examples