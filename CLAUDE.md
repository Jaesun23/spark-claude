# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPARK v3.5 (Subagent Performance Architecture with Reduced toKens) is the most advanced multi-agent automation system that achieves 88.4% token reduction while providing enterprise-grade quality gates. Created through human-AI collaboration between Jason (human architect) and AI assistants.

## Architecture

### Core Innovation: Lazy Loading
- **Traditional SuperClaude**: Loads all 16 agents at once (44,000 tokens)
- **SPARK**: Loads only the needed agent + router (5,100 tokens average)
- **Verified Performance**: 88.4% token reduction, 78.7% faster load time

### Key Components (v3.5 Enhanced - SuperClaude Inspired)
1. **Unified Orchestrator** (`spark-hooks/spark_unified_orchestrator.py`): 6 lifecycle hooks with intelligent routing
2. **Smart Persona Router** (`spark-hooks/spark_persona_router.py`): 8 persona modes for optimal agent selection
3. **Quality Gates** (`spark-hooks/spark_quality_gates.py`): Jason's 8-step strict validation system
4. **16 Specialized Agents** (`.claude/agents/`): Each incorporating SuperClaude 5-Phase methodology
5. **Task Orchestration**: Parallel execution by calling multiple Tasks in ONE MESSAGE
6. **Security Layer**: SecureCommandExecutor prevents malicious operations

### SuperClaude Integration (v3.5)
All 16 agents now incorporate SuperClaude methodology patterns:
- **5-Phase Execution**: Discovery → Foundation → Enhancement → Integration → Validation  
- **Wave Mode**: Automatically activated for complex tasks (complexity ≥0.7)
- **Persona Collaboration**: Backend, Frontend, Security, Architecture personas work together
- **Evidence-Based Analysis**: All findings backed by concrete evidence and metrics

*Note: These implementations aim to closely follow SuperClaude patterns while adapting to SPARK's efficient architecture.*

## Development Commands

### Setup and Installation
```bash
# Install with uv (recommended - 10x faster than pip)
uv venv
source .venv/bin/activate
uv pip install -e ".[full,dev,benchmark]"

# Or with traditional pip
pip install -e ".[full,dev,benchmark]"
```

### Running Tests and Validation
```bash
# Run performance benchmarks (verifies 88.4% token reduction)
python3 benchmarks/compare_performance.py

# Quality gates (must pass all 8 steps)
uv run mypy [file.py] --strict  # Type checking (0 errors required)
uv run ruff check [file.py]     # Linting (0 violations required)
uv run black [file.py]         # Code formatting
uv run pytest tests/           # Run test suite

# Run single test file
uv run pytest tests/test_specific.py -v
```

### Development Workflow
```bash
# Build project (if building standalone)
python -m build

# Run benchmarks to verify performance
python benchmarks/compare_performance.py

# Lint entire project
uv run ruff check .
uv run mypy .

# Format code
uv run black .
```

### Testing Hooks
```bash
# Test unified orchestrator (v3.0)
echo '{"prompt": "implement API endpoint"}' | python3 .claude/hooks/spark_unified_orchestrator.py

# Test persona router
echo '{"prompt": "implement API endpoint"}' | python3 .claude/hooks/spark_persona_router.py

# Test quality gates (requires current_task.json)
echo '{}' | python3 .claude/hooks/spark_quality_gates.py
```

## Code Architecture

### High-Level System Design
SPARK v3.5 implements a **lazy-loading multi-agent architecture** with three core layers:

1. **Router Layer**: `spark_persona_router.py` analyzes incoming tasks and determines optimal agent(s)
2. **Orchestration Layer**: `spark_unified_orchestrator.py` manages agent lifecycle through 6 hooks
3. **Agent Layer**: 16 specialized agents, each implementing SuperClaude 5-Phase methodology

The system achieves 88.4% token efficiency by loading only the required agent instead of all 16 agents simultaneously.

### Persona System (v3.5 Enhanced)
The system uses intelligent persona activation based on task keywords and complexity:

- **Backend Mode**: Activates on API, endpoint, service, database keywords
- **Frontend Mode**: Activates on component, UI, responsive, style keywords  
- **Security Mode**: Activates on auth, security, vulnerability keywords
- **Architecture Mode**: Activates on complexity > 0.7 or architecture keywords
- **DevOps Mode**: Activates on deploy, CI/CD, pipeline keywords
- **Data Mode**: Activates on data, analytics, database keywords
- **Testing Mode**: Activates on test, coverage keywords
- **Documentation Mode**: Activates on document, readme keywords

### Agent Communication Pattern
Agents operate independently but coordinate through JSON-based context relay:
- **No Direct Communication**: Agents cannot communicate with each other directly
- **Context Passing**: State and results passed through `.claude/workflows/` JSON files  
- **Orchestrator Control**: Only the main orchestrator can invoke multiple agents
- **Task Pattern**: Use "Task Task Task → 시작!" for true parallel execution

### Quality Gate Protocol (Jason's 8-Step Strict Approach - FIXED)
All code must pass 8 quality gates with strict enforcement (no more duplicates):

**Jason's Efficient 8-Step Quality Gates (Fixed Configuration):**
1. Syntax Validation (0 errors)
2. **MyPy --strict** (strongest type checking, 0 errors)
3. **Ruff --strict** (strongest linting, 0 violations)
4. Security Analysis (OWASP + enhanced, no hardcoded secrets)
5. **Realistic Test Coverage**: Unit 95%, Integration 85%, Overall 90%
6. Performance Check
7. Documentation Validation (docstrings required)
8. Integration Testing

**Note**: Fixed duplicate quality gate issues that were causing configuration confusion.

### Hook System (v3.0 - 6 Lifecycle Hooks)
The project uses unified orchestrator for complete lifecycle management:

**Fixed Unified Orchestrator** (`spark_unified_orchestrator.py`) handles:
- **UserPromptSubmit**: Fixed task initialization and persona routing (no more hanging)
- **SubagentStart**: Track agent initialization
- **SubagentStop**: Fixed quality validation with intelligent retry (no "phase2 진행할까요?")
- **ToolUse**: Monitor tool usage patterns
- **UserPromptComplete**: Finalize task and generate metrics
- **AssistantResponse**: Track token usage

**Critical Fix**: Eliminated "nonsensical" configurations that caused agents to hang between phases.

State management via:
- `.claude/workflows/unified_context.json` - Complete task context
- `.claude/workflows/current_task.json` - Legacy compatibility

## Implementation Workflow (FIXED)

When implementing features:
1. Persona router analyzes task and activates relevant personas
2. Only required agent is loaded (saving ~39,000 tokens)
3. **Task 동시 호출**: Use "Task Task Task → 시작!" for parallel execution
4. Implementation follows persona-specific standards
5. **Fixed quality gates** validate all changes (no duplicates, realistic targets)
6. If violations found, automatic retry (max 3 attempts)
7. **No phase hanging**: Smooth progression through all phases
8. On success, proceed to testing phase

## Important Context

### Token Efficiency Metrics (Verified)
- SuperClaude: 44,000 tokens per request
- SPARK: 5,100 tokens average (88.4% reduction)
- Cost savings: $0.78 per request

### File Naming Convention
- Agents use `-spark` suffix (e.g., `implementer-spark.md`)
- Hooks use `spark_` prefix (e.g., `spark_persona_router.py`)
- Workflows use `-spark` suffix

### State Management
- Task state stored in `.claude/workflows/current_task.json`
- Includes persona activation, quality results, routing decisions
- Updated by hooks throughout workflow

## Critical Requirements

1. **Always run quality gates** - Code must pass all 8 strict gates before completion
2. **Use uv for Python operations** - It's configured and 10x faster than pip
3. **Maintain token efficiency** - Don't load unnecessary agents or data
4. **Follow persona standards** - Each persona has specific quality requirements
5. **Document with docstrings** - Required by quality gate #7

## Agent Usage

For detailed agent invocation guidelines and usage patterns, see:
**📚 [SPARK Agents Guide](docs/SPARK_AGENTS_GUIDE.md)** - Complete documentation for all 16 agents

## Project Structure
```
spark-claude/
├── .claude/                 # Claude Code integration
│   ├── agents/             # 16 SPARK agents (loaded on-demand)
│   ├── hooks/              # Workflow automation (router, quality gates)
│   └── workflows/          # Orchestration patterns & state management
├── benchmarks/             # Performance verification
├── docs/                   # Documentation
└── pyproject.toml         # Project configuration (uv-compatible)
```

## 🚨 Critical Architectural Principles

### Task Tool Usage
**ONLY 2호 (Number Two) can use the Task tool to call agents.**
- Agents CANNOT call other agents
- All orchestration decisions belong to 2호
- Agents work independently and communicate through JSON files

### Parallel Execution Synchronization
**All parallel agents must complete before proceeding:**
- If team1 finishes early, it waits for team2, team3, team4
- 2호 collects results only after ALL agents complete
- This ensures consistency and prevents race conditions

---