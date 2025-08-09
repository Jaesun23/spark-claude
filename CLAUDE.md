# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPARK v3.0 Unified (Subagent Performance Architecture with Reduced toKens) is the most advanced multi-agent automation system that achieves 88.4% token reduction while providing enterprise-grade quality gates. Created through human-AI collaboration between Jason (human architect) and AI assistants.

## Architecture

### Core Innovation: Lazy Loading
- **Traditional SuperClaude**: Loads all 16 agents at once (44,000 tokens)
- **SPARK**: Loads only the needed agent + router (5,100 tokens average)
- **Verified Performance**: 88.4% token reduction, 78.7% faster load time

### Key Components (v3.0 Enhanced - All Fixed)
1. **Fixed Unified Orchestrator** (`spark-hooks/spark_unified_orchestrator.py`): 6 lifecycle hooks working correctly
2. **Smart Persona Router** (`spark-hooks/spark_persona_router.py`): 8 persona modes for intelligent routing
3. **Fixed Quality Gates** (`spark-hooks/spark_quality_gates.py`): Jason's 8-step strict validation (no duplicates)
4. **Specialized Agents** (`spark-agents/`): 16 modular agents with realistic test coverage
5. **Task 동시 호출 System**: True parallel execution with "Task Task Task → 시작!" pattern
6. **Security Layer**: SecureCommandExecutor prevents malicious operations

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

## Agent Invocation Guidelines (for 2호)

### Analyzer-Spark Agent (Enhanced with SuperClaude 5-Phase)
When invoking analyzer-spark, provide:
```python
context = {
    "scope": "specific files or entire system",
    "focus": ["quality", "security", "performance", "architecture"],
    "depth": "quick|standard|deep",
    "complexity_hint": "estimated 0.0-1.0",
    "expected_time": "5min|30min|1hr",
    "specific_concerns": "what to investigate"
}
```

Example invocation:
```
Task("analyzer-spark", f"""
Analyze the multi-implement system in {target_path}
Focus: architecture, quality, performance
Depth: deep
Specific concerns: synchronization issues, JSON relay patterns
Expected complexity: 0.75
Please use SuperClaude 5-phase methodology
""")
```

**5-Phase Execution**:
1. **Scope Definition**: File discovery, complexity scoring
2. **Evidence Collection**: Pattern search, dependency tracing
3. **Pattern Analysis**: Anti-patterns, security issues, bottlenecks
4. **Hypothesis Testing**: Validate findings with evidence
5. **Synthesis**: Root causes, prioritized recommendations

### Improver-Spark Agent (5-Wave Progressive Pattern)
When invoking improver-spark, provide:
```python
context = {
    "target": "file, module, or system to improve",
    "strategy": "comprehensive|quick-wins|refactor|optimize",
    "focus": ["quality", "performance", "architecture", "security"],
    "iterations": "1-5 (for polish/refine operations)",
    "constraints": "backward compatibility, time limits, etc"
}
```

Example invocation:
```
Task("improver-spark", """
Improve the Redis atomic operations module
Strategy: comprehensive (use 5-wave pattern)
Focus: performance, error handling
Constraints: maintain backward compatibility

Please follow the 5-Wave pattern:
Wave 1: Discovery (find all TODOs, issues)
Wave 2: Pattern Analysis (identify root causes)
Wave 3: Planning (prioritize improvements)
Wave 4: Implementation (apply fixes)
Wave 5: Validation (verify improvements)
""")
```

**Wave Keywords** (auto-activates waves):
- Comprehensive, systematic, thorough, audit → 5-Wave mode
- Polish, refine, enhance, iteratively → Loop mode (3 iterations)

### Designer-Spark Agent (5-Phase Design Pattern)
When invoking designer-spark, provide:
```python
context = {
    "target": "system, component, or feature to design",
    "type": "architecture|api|component|database",
    "requirements": "functional and non-functional requirements",
    "constraints": "technical, business, timeline constraints",
    "format": "diagram|spec|code|documentation"
}
```

Example invocation:
```
Task("designer-spark", """
Design fundamental improvements for Memory V3
Based on: issues discovered by /improve command
Type: architecture

Please follow 5-Phase design:
Phase 1: Analyze requirements and constraints
Phase 2: Create design alternatives (at least 3)
Phase 3: Develop detailed specifications
Phase 4: Validate against best practices
Phase 5: Generate documentation and guides
""")
```

**Design Outputs**:
- Executive summary
- Alternative approaches with pros/cons
- Detailed specifications
- Implementation roadmap
- Migration strategy
- ADRs (Architecture Decision Records)

### Builder-Spark Agent (Enhanced with /sc:build Pattern)
When invoking builder-spark, provide:
```python
context = {
    "project_path": "path to existing project or '.' for current",
    "build_type": "dev|prod|test",
    "quality_mode": "strict|progressive|lenient",
    "optimization": "bundle-size|speed|quality",
    "report_detail": "summary|detailed|comprehensive"
}
```

Example invocation:
```
Task("builder-spark", """
Build and analyze the BioNeX project at /Users/jason/Projects/BioNeX
Build type: development
Quality mode: progressive (start lenient, gradually stricten)

Please follow the 4-Phase build process:
Phase 1: Analyze project structure and configuration
Phase 2: Validate dependencies and environment  
Phase 3: Execute build with quality checks
Phase 4: Generate report with 5-Wave improvement plan
""")
```

**Build Execution Phases**:
1. **Project Analysis**: Detect build system (pyproject.toml, package.json)
2. **Dependency Validation**: Check versions, test installations
3. **Quality Checks**: Run linters, type checkers, tests
4. **Report Generation**: Issues prioritized as 🔴 Critical, 🟡 Medium, 🟢 Low

**Progressive Quality Targets** (Jason's 8 Gates):
- **Linting**: Start <100 violations → <20 → 0
- **Type Checking**: Start <50 errors → <10 → 0  
- **Test Coverage**: Start >60% → >80% → >95%
- **Security**: Always 0 vulnerabilities required

**Output Example** (from BioNeX build):
- Found: 4,200+ Ruff violations, multiple MyPy errors
- Generated: 5-Wave improvement plan with specific commands
- Tracked: Progress with TodoWrite throughout process

### Tester-Spark Agent
When invoking tester-spark, provide:
```python
context = {
    "implementation_context": "what was built/changed",
    "test_types": ["unit", "integration", "e2e"],
    "coverage_targets": {"unit": 95, "integration": 85, "overall": 90},
    "specific_scenarios": "edge cases to test"
}
```

### Implementer-Spark Agent
When invoking implementer-spark, provide:
```python
context = {
    "requirements": "clear feature requirements",
    "file_paths": "where to implement",
    "quality_standards": "must pass 8 quality gates",
    "persona_hint": "backend|frontend|security|architecture"
}
```

### Documenter-Spark Agent
When invoking documenter-spark, provide:
```python
context = {
    "audience": "developers|users|stakeholders",
    "format": "markdown|wiki|api-docs|readme",
    "language": "en|es|fr|de|ja|zh|ko",
    "scope": "what to document"
}
```

### Tasker-Spark Agent (SuperClaude 5-Phase Project Management)
When invoking tasker-spark, provide:
```python
context = {
    "project_path": "/path/to/project or current directory",
    "operation": "analyze|plan|execute|monitor",
    "strategy": "systematic|agile|enterprise",
    "wave_mode": True,  # For complex projects
    "depth": "quick|standard|comprehensive"
}
```

Example invocation:
```
Task("tasker-spark", """
Analyze the project at /Users/jason/Projects/BlueprintAI
Establish comprehensive workflow and task stages

Please follow the 5-Phase Task Management Pattern:
Phase 1: Project Analysis & Discovery
Phase 2: Hierarchical Task Decomposition (Epic→Story→Task)
Phase 3: Dependency Mapping & Critical Path
Phase 4: Execution Workflow (5-Wave strategy)
Phase 5: Monitoring & Validation Plan

Use systematic strategy for comprehensive analysis.
Track progress with TodoWrite throughout.
Generate visual dependency graph and dashboard.
""")
```

**5-Phase Execution**:
1. **Project Analysis**: Structure scan, tech stack detection, state assessment
2. **Task Decomposition**: Epic→Story→Task hierarchy with status tracking
3. **Dependency Mapping**: Critical path, parallel work, bottlenecks
4. **Execution Workflow**: 5-Wave implementation (Discovery→Core→Integration→Quality→Deployment)
5. **Monitoring Plan**: Quality gates, metrics, risk tracking, dashboards

**Output Format**:
- Hierarchical task structure with icons (✅ complete, ⏳ in progress, 📝 planned)
- Mermaid dependency graph with critical path highlighted
- 5-Wave execution timeline
- Quality gate checklist (Jason's 8 steps)
- Real-time progress dashboard
- Risk assessment and mitigation plan

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