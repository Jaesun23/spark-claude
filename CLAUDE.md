# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPARK (Subagent Performance Architecture with Reduced toKens) is an optimized version of the SuperClaude framework that achieves 88% token reduction while maintaining full functionality. Created through human-AI collaboration between Jason (human architect) and AI assistants.

## Architecture

### Core Innovation: Lazy Loading
- **Traditional SuperClaude**: Loads all 16 agents at once (44,000 tokens)
- **SPARK**: Loads only the needed agent + router (5,100 tokens average)
- **Verified Performance**: 88.4% token reduction, 78.7% faster load time

### Key Components
1. **Smart Persona Router** (`spark-hooks/spark_persona_router.py`): Analyzes tasks and activates only needed personas
2. **Quality Gates** (`spark-hooks/spark_quality_gates.py`): 10-step validation (8 SPARK + 2 Jason DNA)
3. **Specialized Agents** (`spark-agents/`): 16 modular agents loaded on-demand

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
# Test persona router
echo '{"prompt": "implement API endpoint"}' | python3 spark-hooks/spark_persona_router.py

# Test quality gates (requires current_task.json)
echo '{}' | python3 spark-hooks/spark_quality_gates.py
```

## Code Architecture

### Persona System
The system uses intelligent persona activation based on task keywords and complexity:

- **Backend Mode**: Activates on API, endpoint, service, database keywords
- **Security Mode**: Activates on auth, security, vulnerability keywords  
- **Frontend Mode**: Activates on component, UI, responsive keywords
- **Architect Mode**: Activates on complexity > 0.7 or architecture keywords

### Quality Gate Protocol
All code must pass 10 quality gates:
1. Syntax Validation (0 errors)
2. Type Verification (MyPy 0 errors)
3. Lint Enforcement (Ruff 0 violations)
4. Security Analysis (no hardcoded secrets)
5. Test Integration (tests must exist)
6. Performance Check
7. Documentation (docstrings required)
8. Integration Test
9. Jason DNA MyPy (strict enforcement)
10. Jason DNA Ruff (strict enforcement)

### Hook System
The project uses hooks for workflow automation:
- **UserPromptSubmit Hook**: `spark_persona_router.py` - Activates personas based on task
- **SubagentStop Hook**: `spark_quality_gates.py` - Validates code quality
- Hooks read/write to `.claude/workflows/current_task.json` for state management

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