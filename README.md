# ⚡ SPARK v4.1: Unified Phase-Based Multi-Agent System for Claude Code

> **Subagent Performance Architecture with Reduced toKens**  
> A revolutionary traits-based agent orchestration system with unified phase structure and mandatory quality gates.

[![Version](https://img.shields.io/badge/version-4.1-gold?style=for-the-badge)](docs/spark-agent-phase-structure-v4.1.md)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blue?style=for-the-badge)](https://claude.ai/code)

## What is SPARK?

SPARK v3.8 is an independent multi-agent system for [Claude Code](https://claude.ai/code), inspired by SuperClaude's persona system but built from scratch with revolutionary improvements. Through its TRAITS system, each agent instantly activates 3-5 specific traits instead of scanning 11 personas, achieving 35% cognitive load reduction while maintaining lazy-loading efficiency.

### Project Evolution
- **v3.0**: Initial release with lazy loading, 95.5% token reduction, workflow automation
- **v3.5**: Stabilization update with enhanced quality gates and refined hooks
- **v3.8**: TRAITS revolution - replacing persona scanning with instant trait activation
- **v4.1**: Unified Phase structure with JSON state management and 8-step quality gates

### Key Features

- **TRAITS System**: Dynamic trait activation replacing 11-persona scanning (35% cognitive load reduction)
- **28 Specialized Agents**: 16 primary agents + 12 team agents using 3-5 traits each
- **Lazy Loading Architecture**: Load only the agent you need, not all 28 at once
- **Smart Routing**: Automatically selects the optimal agent based on your task
- **Quality Gates**: 8-step validation ensuring production-ready code
- **Parallel Execution**: Run multiple independent tasks simultaneously
- **Token Safety Protocol**: All agents include 90K token limit protection
- **Mandatory Reporting System**: All agents generate detailed task completion reports
- **Miller's 7±2 Validation**: Trait count optimized for human cognitive limits

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Jaesun23/spark-claude.git
cd spark-claude

# Run the interactive installer
./scripts/install.sh

# Or manual setup with uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e ".[full,dev,benchmark]"
```

### Basic Usage

Simply use natural language commands in Claude Code:

```bash
# Single agent commands
"implement user authentication with JWT"
"analyze this codebase for performance issues"
"write comprehensive tests for the API"
"design a scalable microservice architecture"

# Multi-agent pipelines
"analyze, improve, and test the payment module"
"refactor and document the legacy authentication system"
```

## Advanced Usage

### Custom Command Definitions

SPARK allows you to define custom commands that chain multiple agents for complex workflows:

```markdown
# Example: /implement-spark command definition
---
name: implement-spark
description: Comprehensive implementation with analysis, coding, testing, and documentation
agents:
  - analyzer-spark    # First analyze the requirements
  - designer-spark    # Design the architecture
  - implementer-spark # Implement the solution
  - tester-spark      # Create comprehensive tests
  - documenter-spark  # Generate documentation
---
```

### Hook-Based Workflows

For even more control, you can implement custom hooks to create sophisticated automation:

```python
# Example: Quality gate hook that runs after each agent
class QualityGateHook:
    def on_subagent_stop(self, result):
        if not self.validate_quality(result):
            return self.retry_with_guidance(result)
        return self.proceed_to_next_phase()
```

### Chaining Subagents

Create powerful multi-step workflows by chaining agents:

```bash
# Simple chain
/spark-refactor "analyze → improve → test → document"

# Complex pipeline with conditions
/spark-pipeline "
  if complexity > 0.7:
    designer-spark → implementer-spark
  else:
    implementer-spark
  always:
    tester-spark → documenter-spark
"
```

For detailed examples and templates, see:
- **Command definitions**: `.claude/commands/implement-spark.md`
- **Hook implementations**: `.claude/hooks/`
- **Workflow patterns**: `.claude/workflows/`

## How It Works

### TRAITS Architecture Overview

SPARK v3.8 uses a three-layer architecture with traits-based behavioral dynamics:

1. **Router Layer**: Analyzes your request and determines which agent to load
2. **Orchestration Layer**: Manages agent lifecycle and trait activation
3. **Agent Layer**: 28 specialized agents using TRAITS methodology
   - 16 primary agents with domain-specific traits (시스템_사고, 분석적_추론, etc.)
   - 12 team agents for parallel execution with collaboration traits

### What are TRAITS?

TRAITS (Trait-Reactive Adaptive Intelligence Technology System) replaces the traditional 11-persona scanning with immediate activation of 3-5 core behavioral traits:

- **시스템_사고** (Systems Thinking): Holistic system understanding
- **분석적_추론** (Analytical Reasoning): Logical decomposition
- **증거_기반_실천** (Evidence-Based Practice): Data-driven decisions
- **체계적_실행** (Systematic Execution): Structured implementation
- **단순성_우선** (Simplicity First): Elegant solutions

Each agent has a unique combination of traits that define its behavior and approach.

### Token Management

Unlike traditional approaches that load all documentation and context upfront, SPARK:
- Loads only the specific agent needed for your task
- Implements compression by default (30-50% reduction)
- Includes pre-task token assessment to prevent overflow
- Sets practical limit at 90K tokens (safe margin from 200K hard limit)

#### Agent Token Usage

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
| **implementer-spark** | 15,476 bytes | ~3,869 tokens | Implementation |
| **team agents (12)** | 3,261-4,432 bytes | ~815-1,108 tokens | Parallel execution |

**Token Usage (Updated):**
- **Total agents**: 28 (16 primary + 12 team)
- **Average token usage**: ~2,370 tokens per agent
- **Single agent**: 1.5-2.5% of 200K context window
- **Token savings**: 95.5% reduction vs. loading all agents

### Quality Assurance

Every code change passes through 8 quality gates:

1. Syntax validation
2. Type checking (MyPy --strict)
3. Linting (Ruff --strict)
4. Security analysis
5. Test coverage (Unit 95%, Integration 85%)
6. Performance validation
7. Documentation check
8. Integration testing

## Available Agents with TRAITS

### Primary Agents (16) - Each with Unique Trait Combinations

| Agent | Core Traits | Purpose | Command Example |
|-------|-------------|---------|-----------------|
| implementer-spark | 체계적_실행, 단순성_우선, 꼼꼼함, 구조적_무결성, 협업_지향 | Feature implementation | "implement REST API endpoints" |
| tester-spark | 체계적_실행, 꼼꼼함, 증거_기반_실천, 위험_평가 | Test creation | "write unit tests with 95% coverage" |
| analyzer-spark | 시스템_사고, 분석적_추론, 증거_기반_실천, 회의주의 | Code analysis | "analyze architecture and find issues" |
| designer-spark | 장기적_사고, 추상화_능력, 시스템_사고, 사용자_중심_사고, 위험_평가 | System design | "design microservice architecture" |
| troubleshooter-spark | 분석적_추론, 증거_기반_실천, 근본_원인_분석, 침착함 | Debugging | "fix the memory leak issue" |
| documenter-spark | 명확한_의사소통, 지식_구조화, 사용자_중심_사고, 공감 | Documentation | "create API documentation" |
| improver-spark | 근본_원인_분석, 반복적_개선, 측정_우선, 실용주의 | Code improvement | "refactor for better performance" |
| cleaner-spark | 단순성_우선, 체계적_실행, 근본_원인_분석, 위험_평가 | Technical debt | "remove dead code and update deps" |
| builder-spark | 자동화, 프로세스_최적화, 시스템_사고, 측정_우선 | Build optimization | "optimize webpack configuration" |
| estimater-spark | 분석적_추론, 증거_기반_실천, 위험_평가, 확률론적_사고 | Project estimation | "estimate time for new features" |
| explainer-spark | 명확한_의사소통, 지식_구조화, 공감, 스캐폴딩 | Education | "explain how async/await works" |
| gitter-spark | 시스템_사고, 체계적_실행, 자동화, 표준화 | Git workflows | "set up branching strategy" |
| spawner-spark | 시스템_사고, 전략적_사고, 자원_최적화, 위험_평가 | Multi-task orchestration | "coordinate full-stack deployment" |
| loader-spark | 분석적_추론, 시스템_사고, 패턴_인식, 지식_구조화 | Project onboarding | "analyze and load project context" |
| indexer-spark | 지식_구조화, 명확한_의사소통, 문제_해결 | Command navigation | "list available commands" |
| tasker-spark | 계획성, 장기적_사고, 체계적_실행, 우선순위_설정 | Project management | "create task breakdown structure" |

### Team Agents (12) - For Parallel Execution

Each team agent inherits the same traits as their primary counterparts but with enhanced collaboration focus:

| Team | Agents | Shared Traits | Purpose |
|------|--------|---------------|---------|
| **Team 1** | team1-implementer/tester/documenter-spark | 협업_지향 + role-specific traits | Independent parallel implementation |
| **Team 2** | team2-implementer/tester/documenter-spark | 협업_지향 + role-specific traits | Independent parallel implementation |
| **Team 3** | team3-implementer/tester/documenter-spark | 협업_지향 + role-specific traits | Independent parallel implementation |
| **Team 4** | team4-implementer/tester/documenter-spark | 협업_지향 + role-specific traits | Independent parallel implementation |

**Usage**: For large tasks requiring parallel execution across multiple domains simultaneously.

## New Features in v4.1 - Unified Phase Structure

### 📊 Unified Phase Structure (v4.1)
- **Phase 0**: Universal task initialization for all 28 agents
- **Phase 1-3**: Agent-specific work phases
- **Phase 4**: Quality validation (16 agents)
- **Phase 5**: Two-part completion:
  - Part A: Agent-specific completion work
  - Part B: Universal JSON update & quality gates

### 🧬 TRAITS System (from v3.8)
- **Dynamic Trait Activation**: 3-5 traits per agent instead of 11 personas
- **35% Cognitive Load Reduction**: No more "쫘라락~!" persona scanning
- **Miller's 7±2 Theory**: Scientifically optimized trait count

### 🔒 8-Step Quality Gates System (v4.1)
All agents execute these mandatory checks with numeric recording:
1. **Architecture**: Import structure, circular dependencies, domain boundaries
2. **Foundation**: Syntax validation, type checking
3. **Standards**: Code formatting, naming conventions
4. **Operations**: Logging, security, configuration
5. **Quality**: Linting, complexity metrics
6. **Testing**: Coverage targets (95% unit, 85% integration)
7. **Documentation**: Docstrings, README files
8. **Integration**: Final system checks

**Zero tolerance**: All violations must be 0 to proceed

### 📊 Mandatory Reporting System
All agents now generate comprehensive reports after task completion:

**Report Categories:**
- **Detailed Reports** (7 analysis/design agents): 500-800+ lines with comprehensive findings
- **Concise Reports** (21 execution agents): 150-300 lines with essential metrics

**Report Location:** `/docs/agents-task/[agent-name]/[task_name]_[timestamp].md`

**Features:**
- Evidence-based findings with file paths and line numbers
- Quality metrics and performance impact measurements
- Next steps and handoff documentation for team coordination
- Template library available at `/docs/templates/agent-reports/`

### ⚡ Multi-Team Parallel Execution
Execute large-scale tasks with up to 4 teams working simultaneously:

```bash
# Example: Full-stack implementation with 4 parallel teams
"Implement user management system across all layers"
# Automatically delegates to:
# Team 1: Backend API implementation
# Team 2: Database schema and queries  
# Team 3: Frontend components
# Team 4: Testing and documentation
```

**Benefits:**
- Up to 4x faster execution for complex multi-domain tasks
- Independent team coordination via JSON state management
- Each team includes implementer + tester + documenter for complete coverage

## Development

### Running Tests

```bash
# Quality validation
uv run mypy [file.py] --strict    # Type checking
uv run ruff check [file.py]       # Linting
uv run pytest tests/               # Unit tests

# Performance verification
python3 benchmarks/compare_performance.py
```

### Testing Hooks

```bash
# Test the routing system
echo '{"prompt": "implement API"}' | python3 .claude/hooks/spark_persona_router.py

# Test quality gates
echo '{}' | python3 .claude/hooks/spark_quality_gates.py

# Test agent self-validation
echo '{"subagent": "implementer-spark", "self_check": true}' | python3 .claude/hooks/spark_quality_gates.py
```

## Project Structure

```
spark-claude/
├── .claude/
│   ├── agents/          # 28 specialized agents (16 primary + 12 team)
│   ├── hooks/           # Orchestration and routing
│   └── workflows/       # State management
├── benchmarks/          # Performance tests
├── docs/
│   ├── agents-task/     # Agent-generated reports
│   └── templates/       # Report templates
├── scripts/             # Installation scripts
└── tests/               # Test suite
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and components
- [Phase Structure Guide](docs/spark-agent-phase-structure-v4.1.md) - Universal phase execution patterns
- [Team Agents Guide](docs/spark-team-agents-guide-v4.1.md) - Multi-team parallel coordination
- [Installation](docs/INSTALLATION.md) - Setup instructions
- [Development](docs/DEVELOPMENT.md) - Development guide
- [Agents List](docs/AGENTS.md) - All 28 agents documentation
- [CLAUDE.md](CLAUDE.md) - Instructions for Claude Code instances

## About This Project

SPARK was created through a unique collaboration between one human developer and two Claude AI instances, demonstrating the power of human-AI teamwork in building complex software systems.

### The Development Team

- **Jason** - Human architect and project lead who envisioned and directed SPARK
- **1호 (Claude AI)** - Claude Desktop AI who collaborates on design, architecture, and problem-solving
- **2호 (Claude CODE)** - Claude Code AI who implements, tests, and refines the codebase

*This entire system was built by a team of one human and two AI assistants working together - proving that individual developers partnering with AI can create enterprise-grade tools that would traditionally require large teams.*

## Contributing

We welcome contributions! Please feel free to submit issues and pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/Jaesun23/spark-claude/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Jaesun23/spark-claude/discussions)

---

<p align="center">
  <i>Built with passion by Jason, 1호 (Claude AI), and 2호 (Claude CODE)</i><br>
  <i>One human, two AIs, infinite possibilities</i>
</p>