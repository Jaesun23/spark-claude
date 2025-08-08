# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPARK v3.0 Unified (Subagent Performance Architecture with Reduced toKens) is the most advanced multi-agent automation system that achieves 88.4% token reduction while providing enterprise-grade quality gates. Created through human-AI collaboration between Jason (human architect) and AI assistants.

## Architecture

### Core Innovation: Lazy Loading
- **Traditional SuperClaude**: Loads all 16 agents at once (44,000 tokens)
- **SPARK**: Loads only the needed agent + router (5,100 tokens average)
- **Verified Performance**: 88.4% token reduction, 78.7% faster load time

### Key Components (v3.0 Enhanced)
1. **Unified Orchestrator** (`spark-hooks/spark_unified_orchestrator.py`): Manages 6 lifecycle hooks
2. **Smart Persona Router** (`spark-hooks/spark_persona_router.py`): 8 persona modes for intelligent routing
3. **Quality Gates** (`spark-hooks/spark_quality_gates.py`): 12-step validation (8 SPARK + 2 Jason DNA + 2 Unified)
4. **Specialized Agents** (`spark-agents/`): 16 modular agents loaded on-demand
5. **Security Layer**: SecureCommandExecutor prevents malicious operations

## Development Commands

### Running Tests and Validation
```bash
# Run performance benchmarks (verifies token reduction)
python3 benchmarks/compare_performance.py

# Run quality gates on Python files
uv run mypy [file.py] --strict  # Type checking (must pass with 0 errors)
uv run ruff check [file.py]     # Linting (must pass with 0 violations)

# Install dependencies with uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e ".[full,dev,benchmark]"
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

### Persona System (v3.0 Extended)
The system uses intelligent persona activation based on task keywords and complexity:

- **Backend Mode**: Activates on API, endpoint, service, database keywords
- **Frontend Mode**: Activates on component, UI, responsive, style keywords
- **Security Mode**: Activates on auth, security, vulnerability keywords
- **Architecture Mode**: Activates on complexity > 0.7 or architecture keywords
- **DevOps Mode**: Activates on deploy, CI/CD, pipeline keywords
- **Data Mode**: Activates on data, analytics, database keywords
- **Testing Mode**: Activates on test, coverage keywords
- **Documentation Mode**: Activates on document, readme keywords

### Quality Gate Protocol (v3.0 - 12 Steps)
All code must pass 12 quality gates:

**SPARK Core Gates (8):**
1. Syntax Validation (0 errors)
2. Type Verification (MyPy 0 errors)
3. Lint Enforcement (Ruff 0 violations)
4. Security Analysis (no hardcoded secrets)
5. Test Coverage (95%+ required)
6. Performance Check
7. Documentation (docstrings required)
8. Integration Test

**Jason DNA Gates (2):**
9. Jason DNA MyPy (strict enforcement)
10. Jason DNA Ruff (strict enforcement)

**Unified Gates (2):**
11. Dependency Audit (security vulnerabilities)
12. Complexity Threshold (cyclomatic complexity < 10)

### Hook System (v3.0 - 6 Lifecycle Hooks)
The project uses unified orchestrator for complete lifecycle management:

**Unified Orchestrator** (`spark_unified_orchestrator.py`) handles:
- **UserPromptSubmit**: Task initialization and persona routing
- **SubagentStart**: Track agent initialization
- **SubagentStop**: Quality validation with intelligent retry
- **ToolUse**: Monitor tool usage patterns
- **UserPromptComplete**: Finalize task and generate metrics
- **AssistantResponse**: Track token usage

State management via:
- `.claude/workflows/unified_context.json` - Complete task context
- `.claude/workflows/current_task.json` - Legacy compatibility

## Implementation Workflow

When implementing features:
1. Persona router analyzes task and activates relevant personas
2. Only required agent is loaded (saving ~39,000 tokens)
3. Implementation follows persona-specific standards
4. Quality gates validate all changes
5. If violations found, automatic retry (max 3 attempts)
6. On success, proceed to testing phase

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

1. **Always run quality gates** - Code must pass all 10 gates before completion
2. **Use uv for Python operations** - It's configured and 10x faster than pip
3. **Maintain token efficiency** - Don't load unnecessary agents or data
4. **Follow persona standards** - Each persona has specific quality requirements
5. **Document with docstrings** - Required by quality gate #7

## Project Structure
```
spark-claude/
├── .claude/                 # Claude Code integration
│   ├── agents/             # 16 SPARK agents (loaded on-demand)
│   ├── hooks/              # Workflow automation (router, quality gates)
│   └── workflows/          # Orchestration patterns & state management
├── benchmarks/             # Performance verification
└── pyproject.toml         # Project configuration (uv-compatible)
```