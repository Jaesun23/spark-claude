# ⚡ SPARK: Efficient Multi-Agent System for Claude Code

> **Subagent Performance Architecture with Reduced toKens**  
> An intelligent agent orchestration system that loads only what you need, when you need it.

[![Version](https://img.shields.io/badge/version-3.5-gold?style=for-the-badge)](docs/SPARK_AGENTS_GUIDE.md)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blue?style=for-the-badge)](https://claude.ai/code)

## What is SPARK?

SPARK is a lazy-loading multi-agent system for [Claude Code](https://claude.ai/code) that intelligently loads only the required agents on-demand, rather than loading everything upfront. This results in faster responses, lower token usage, and better resource management.

### Key Features

- **16 Specialized Agents**: Each focused on specific tasks (implementation, testing, analysis, etc.)
- **Lazy Loading Architecture**: Load only the agent you need, not all 16 at once
- **Smart Routing**: Automatically selects the optimal agent based on your task
- **Quality Gates**: 8-step validation ensuring production-ready code
- **Parallel Execution**: Run multiple independent tasks simultaneously
- **Token Safety Protocol**: All agents now include 90K token limit protection

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

### Architecture Overview

SPARK uses a three-layer architecture:

1. **Router Layer**: Analyzes your request and determines which agent to load
2. **Orchestration Layer**: Manages agent lifecycle and coordination
3. **Agent Layer**: 16 specialized agents, each with specific expertise

### Token Management

Unlike traditional approaches that load all documentation and context upfront, SPARK:
- Loads only the specific agent needed for your task
- Implements compression by default (30-50% reduction)
- Includes pre-task token assessment to prevent overflow
- Sets practical limit at 90K tokens (safe margin from 200K hard limit)

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

## Available Agents

| Agent | Purpose | Command Example |
|-------|---------|-----------------|
| implementer-spark | Feature implementation | "implement REST API endpoints" |
| tester-spark | Test creation | "write unit tests with 95% coverage" |
| analyzer-spark | Code analysis | "analyze architecture and find issues" |
| designer-spark | System design | "design microservice architecture" |
| troubleshooter-spark | Debugging | "fix the memory leak issue" |
| documenter-spark | Documentation | "create API documentation" |
| improver-spark | Code improvement | "refactor for better performance" |
| cleaner-spark | Technical debt | "remove dead code and update deps" |
| builder-spark | Build optimization | "optimize webpack configuration" |
| estimator-spark | Project estimation | "estimate time for new features" |
| explainer-spark | Education | "explain how async/await works" |
| gitter-spark | Git workflows | "set up branching strategy" |
| spawner-spark | Multi-task orchestration | "coordinate full-stack deployment" |
| loader-spark | Project onboarding | "analyze and load project context" |
| indexer-spark | Command navigation | "list available commands" |
| tasker-spark | Project management | "create task breakdown structure" |

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
```

## Project Structure

```
spark-claude/
├── .claude/
│   ├── agents/          # 16 specialized agents
│   ├── hooks/           # Orchestration and routing
│   └── workflows/       # State management
├── benchmarks/          # Performance tests
├── docs/                # Documentation
├── scripts/             # Installation scripts
└── tests/               # Test suite
```

## Documentation

- [SPARK Agents Guide](docs/SPARK_AGENTS_GUIDE.md) - Detailed agent documentation
- [Token Management](docs/TOKEN_AND_RESOURCE_MANAGEMENT.md) - Token optimization strategies
- [Installation Guide](docs/INSTALLATION_GUIDE.md) - Setup instructions
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