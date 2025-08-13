# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPARK v3.5 (Subagent Performance Architecture with Reduced toKens) is a multi-agent orchestration system for Claude Code that achieves significant token reduction through lazy-loading architecture. Unlike traditional approaches that load all agents simultaneously, SPARK loads only the required agent on-demand.

## Development Commands

### Setup and Installation
```bash
# Install with uv (recommended - 10x faster than pip)
uv venv
source .venv/bin/activate
uv pip install -e ".[full,dev,benchmark]"

# Alternative: traditional pip
pip install -e ".[full,dev,benchmark]"
```

### Quality Gates (Must Pass All 8 Steps)
```bash
# Run complete quality validation
uv run mypy [file.py] --strict    # Type checking (0 errors required)
uv run ruff check [file.py]       # Linting (0 violations required)
uv run black [file.py]             # Code formatting
uv run pytest tests/               # Test suite

# Performance verification
python3 benchmarks/compare_performance.py  # Verify token efficiency
```

### Testing Hooks
```bash
# Test unified orchestrator
echo '{"prompt": "implement API endpoint"}' | python3 .claude/hooks/spark_unified_orchestrator.py

# Test persona router
echo '{"prompt": "implement API endpoint"}' | python3 .claude/hooks/spark_persona_router.py

# Test quality gates (requires current_task.json)
echo '{}' | python3 .claude/hooks/spark_quality_gates.py
```

## Architecture

### Three-Layer System Design

1. **Router Layer** (`spark_persona_router.py`): Analyzes tasks and determines optimal agent selection
2. **Orchestration Layer** (`spark_unified_orchestrator.py`): Manages agent lifecycle through 6 hooks
3. **Agent Layer** (16 specialized agents in `.claude/agents/`): Each implements 5-Phase methodology

### Token Management (Critical)

**90K Token Limit for All Agents:**
- Each agent gets independent 200K context window
- Write operations double token consumption (memory + output)
- Context accumulates and cannot be cleared during execution
- Practical limit is 90K to avoid hard termination at 200K
- All agents now include Token Safety Protocol with pre-task assessment

#### Agent Token Consumption Table

| Agent | File Size | Token Usage | Purpose |
|-------|-----------|-------------|---------|
| **indexer-spark** | 7,172 bytes | ~1,793 tokens | Command discovery |
| **tasker-spark** | 9,593 bytes | ~2,398 tokens | Project management |
| **explainer-spark** | 10,006 bytes | ~2,501 tokens | Concept explanation |
| **loader-spark** | 10,023 bytes | ~2,505 tokens | Project loading |
| **estimater-spark** | 10,452 bytes | ~2,613 tokens | Time estimation |
| **documenter-spark** | 10,539 bytes | ~2,634 tokens | Documentation |
| **cleaner-spark** | 10,658 bytes | ~2,664 tokens | Code cleanup |
| **gitter-spark** | 10,681 bytes | ~2,670 tokens | Git workflow |
| **spawner-spark** | 11,453 bytes | ~2,863 tokens | Multi-task orchestration |
| **builder-spark** | 11,829 bytes | ~2,957 tokens | Build optimization |
| **troubleshooter-spark** | 11,971 bytes | ~2,992 tokens | Issue resolution |
| **analyzer-spark** | 12,299 bytes | ~3,074 tokens | System analysis |
| **improver-spark** | 12,553 bytes | ~3,138 tokens | Code improvement |
| **designer-spark** | 12,640 bytes | ~3,160 tokens | System design |
| **tester-spark** | 13,796 bytes | ~3,449 tokens | Testing |
| **implementer-spark** | 14,965 bytes | ~3,741 tokens | Implementation |

**Key Metrics:**
- Average agent size: ~2,800 tokens
- Traditional approach (all agents): ~44,000 tokens
- Token savings: 93.6% reduction per request

### Agent Communication Pattern

- **No Direct Communication**: Agents cannot call other agents
- **JSON Context Relay**: State passed through `.claude/workflows/*.json`
- **Orchestrator Control**: Only Claude CODE can invoke multiple agents via Task tool  
- **Parallel Execution**: Use "multiple tools in one message" pattern for true parallelism

### Quality Gates (Jason's 8-Step Protocol)

1. Syntax Validation (0 errors)
2. MyPy --strict (type checking, 0 errors)
3. Ruff --strict (linting, 0 violations)
4. Security Analysis (OWASP + secrets scan)
5. Test Coverage (Unit 95%, Integration 85%)
6. Performance Check
7. Documentation Validation (docstrings required)
8. Integration Testing

### Hook System (6 Lifecycle Hooks)

**Unified Orchestrator** handles:
- `UserPromptSubmit`: Task initialization and routing
- `SubagentStart`: Agent initialization tracking
- `SubagentStop`: Quality validation with retry (max 3)
- `ToolUse`: Tool usage monitoring
- `UserPromptComplete`: Task finalization
- `AssistantResponse`: Token usage tracking

## Implementation Workflow

1. Router analyzes task → activates personas based on keywords/complexity
2. Load only required agent (saves ~39,000 tokens)
3. Execute with parallel Tasks when possible
4. Quality gates validate all changes
5. Automatic retry on violations (max 3 attempts)
6. Results stored in JSON for next phase

## Critical Principles

### Task Tool Usage
- **ONLY Claude CODE can use Task tool** to call agents
- Agents work independently through JSON communication
- No agent-to-agent direct calls allowed

### Parallel Execution
- All parallel agents must complete before proceeding
- Synchronization prevents race conditions
- Results collected only after all agents finish

### Token Safety Protocol
- All agents calculate token usage before starting
- Abort if estimated > 90K tokens with JSON logging
- Default compression reduces tokens by 30-50%
- Write operations always double token cost

## Project Structure
```
spark-claude/
├── .claude/
│   ├── agents/              # 16 specialized agents (lazy-loaded)
│   ├── hooks/               # Orchestration and routing
│   └── workflows/           # JSON state management
├── benchmarks/              # Performance verification
├── docs/                    # Documentation including TOKEN_AND_RESOURCE_MANAGEMENT.md
└── pyproject.toml          # uv-compatible configuration
```

## Agent Reference

For detailed agent usage patterns and invocation guidelines, see:
- **[SPARK Agents Guide](docs/SPARK_AGENTS_GUIDE.md)** - Complete agent documentation
- **[Token Management](docs/TOKEN_AND_RESOURCE_MANAGEMENT.md)** - Token optimization strategies