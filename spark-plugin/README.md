# SPARK Agents Plugin

SPARK v4.3 - Subagent Performance Architecture with Reduced toKens

## Overview

The SPARK Agents Plugin provides 21 specialized AI agents (6 core + 15 team) with zero-tolerance quality gates, achieving 95.5% token reduction through on-demand agent loading.

## Features

- **21 Specialized Agents**: 6 core agents + 15 team agents for parallel execution
- **Zero-Tolerance Quality**: Ruff 0, MyPy 0, Coverage 95%+, Tests 100% pass
- **Token Efficiency**: 95.5% token reduction through lazy-loading architecture
- **Parallel Execution**: Multi-team coordination for complex tasks
- **Quality Gates**: Automatic validation with 8-step strict protocol

## Core Agents (6)

### analyzer-spark
Multi-dimensional system analysis with evidence-based investigation
- **Usage**: `/spark-analyze <scope>`
- **Protocols**: EVIDENCE-BEFORE-REPORT + PROJECT-CONTEXT-DISCOVERY
- **Expertise**: Performance, security, quality, architecture analysis

### implementer-spark
Feature implementation with zero defects
- **Usage**: `/spark-implement <feature>`
- **Protocols**: TEST-BEFORE-REPORT + PROJECT-CONTEXT-DISCOVERY
- **Expertise**: API endpoints, authentication, data layers, UI components

### tester-spark
Comprehensive testing with coverage targets
- **Usage**: `/spark-test <target>`
- **Protocols**: TEST-EXECUTION-BEFORE-REPORT
- **Expertise**: 95% unit, 85% integration, 100% E2E critical paths

### documenter-spark
Technical documentation creation
- **Usage**: Available through pipelines
- **Protocols**: VALIDATION-BEFORE-REPORT
- **Expertise**: API docs, user guides, architecture documentation

### designer-spark
System architecture and API design
- **Usage**: `/spark-design <system>`
- **Expertise**: Architecture patterns, API specifications, scalability

### qc-spark
Quality violations cleanup (Direct Task calls only)
- **Usage**: `Task("qc-spark", "fix ruff violations")`
- **Expertise**: Ruff/MyPy fixes, 5-phase inspection, persist until success

## Team Agents (15)

5 teams × 3 roles for parallel execution:
- **team[1-5]-implementer-spark**: Parallel implementation specialists
- **team[1-5]-tester-spark**: Parallel testing specialists
- **team[1-5]-documenter-spark**: Parallel documentation specialists

**Usage**: `/multi-implement task1,task2,task3,task4,task5`

## Pipeline Commands

Sequential multi-agent workflows:

- `/spark-launch <feature>` - Complete: design → implement → test → document
- `/spark-refactor <module>` - Refactor: analyze → improve → test
- `/spark-audit <system>` - Audit: analyze → troubleshoot → document
- `/spark-migrate <legacy>` - Migration: analyze → design → implement → test
- `/spark-optimize <scope>` - Optimize: analyze → improve → test

## Installation

### Via Claude Code Plugin System

```bash
# Add SPARK marketplace (when available)
/plugin marketplace add Jaesun23/spark-claude

# Install SPARK plugin
/plugin install spark-agents@spark-claude
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/Jaesun23/spark-claude.git
cd spark-claude

# Run installation script
./scripts/install.sh
```

## Requirements

- Claude Code 2.0.0+
- Git (for commit/push operations)
- Python 3.8+ (for quality gates)
- GitHub CLI (`gh`) for PR creation (optional)

## Quick Start

After installation, try these commands:

```bash
# Single agent implementation
/spark-implement "create JWT authentication"

# System analysis
/spark-analyze "identify performance bottlenecks"

# Comprehensive testing
/spark-test "achieve 95% coverage"

# Complete feature pipeline
/spark-launch "new dashboard with real-time updates"

# Parallel team execution
/multi-implement "API endpoints" "UI components" "Tests" "Documentation"
```

## Quality Standards

All SPARK agents follow strict quality protocols:

- **Ruff**: 0 violations
- **MyPy**: 0 type errors
- **Coverage**: 95%+ unit, 85%+ integration
- **Tests**: 100% pass rate
- **Evidence**: file:line references required

## Architecture

### Three-Layer System

1. **Agent Layer**: 21 specialized agents (lazy-loaded)
2. **Quality Gates**: 8-step validation protocol
3. **Orchestration**: Task coordination and state management

### Token Efficiency

- **On-demand loading**: Only required agent loaded (~1-4K tokens)
- **Compression**: 30-50% reduction when needed
- **Safety limit**: 90K tokens with pre-task assessment
- **Result**: 95.5% token reduction vs loading all agents

## Configuration

### Project Standards

SPARK agents work best with project standards:

```markdown
# PROJECT_STANDARDS.md
- Logging standards
- Error handling patterns
- Database conventions
- Code style guidelines
```

### Agent Delegation

When delegating to agents, provide context:

```python
Task("implementer-spark", """
Task: Add user authentication

📋 Standards (read these first):
- PROJECT_STANDARDS.md
- ARCHITECTURE.md

📂 Use existing modules:
- common/logging/
- common/config/
- common/db/
""")
```

## Troubleshooting

### Quality Gates Failing

```bash
# Check violations
ruff check .
mypy .
pytest tests/ --cov

# Let QC agent fix
Task("qc-spark", "fix all quality violations")
```

### Agent Not Found

```bash
# Verify installation
ls ~/.claude/plugins/*/spark-agents/agents/

# Reinstall if needed
/plugin uninstall spark-agents
/plugin install spark-agents@spark-claude
```

## Documentation

- **Complete Guide**: `docs/SPARK_COMPLETE_GUIDE.md`
- **Agent Definitions**: `agents/*.md`
- **Constitution**: `.claude/SPARK_CONSTITUTION.md`
- **GitHub**: https://github.com/Jaesun23/spark-claude

## Version

**4.3.0** - Native Claude Code Plugin Support

## Author

Jason (Jaesun23)
- GitHub: https://github.com/Jaesun23
- Repository: https://github.com/Jaesun23/spark-claude

## License

MIT License - See LICENSE file for details

---

**Built with ❤️ for the Claude Code community**
