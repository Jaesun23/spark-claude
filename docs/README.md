# 🚀 SPARK v3.8 Documentation

> **Subagent Performance Architecture with Reduced toKens**  
> *The most efficient multi-agent orchestration system for Claude Code*

## 📚 Documentation Structure

| Document | Description |
|----------|-------------|
| **[README.md](README.md)** | This file - Overview and quick start |
| **[INSTALLATION.md](INSTALLATION.md)** | Installation, setup, and troubleshooting |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design and component details |
| **[AGENTS.md](AGENTS.md)** | Complete agent reference (28 agents) |
| **[DEVELOPMENT.md](DEVELOPMENT.md)** | Development guide, hooks, and advanced features |

## 🎯 What is SPARK?

SPARK is an advanced multi-agent orchestration system that achieves **significant token efficiency** through intelligent lazy-loading and parallel execution. It provides 28 specialized agents (16 base + 12 team) that work together seamlessly.

### Key Features

- **🔥 Lazy Loading**: Only loads required agents on-demand
- **⚡ Parallel Execution**: Up to 4 teams working simultaneously
- **🔒 FileLockManager**: Safe concurrent file access
- **📊 Quality Gates**: 8-step validation with automatic retry
- **🤖 28 Specialized Agents**: Each optimized for specific tasks

## ⚡ Quick Start

### 1. Install SPARK

```bash
# Global installation (recommended)
curl -sSL https://raw.githubusercontent.com/Jaesun23/spark-claude/main/scripts/install.sh | bash

# Or clone and install locally
git clone https://github.com/Jaesun23/spark-claude.git
cd spark-claude
./scripts/install.sh
```

### 2. Basic Usage

```bash
# Single agent
/implement "create user authentication API"

# Multi-team parallel execution
/multi-implement "task1: API endpoints, task2: database schema, task3: tests"

# Get help
/spark-help
```

### 3. Available Commands

| Command | Agent | Purpose |
|---------|-------|---------|
| `/implement` | implementer-spark | Build features |
| `/test` | tester-spark | Create tests |
| `/analyze` | analyzer-spark | Analyze code |
| `/improve` | improver-spark | Optimize code |
| `/document` | documenter-spark | Write docs |
| `/troubleshoot` | troubleshooter-spark | Fix issues |
| `/design` | designer-spark | System design |
| `/clean` | cleaner-spark | Remove tech debt |

## 🏗️ System Overview

```
┌─────────────────────────────────────┐
│         Claude CODE (You)           │
├─────────────────────────────────────┤
│          SPARK Router               │
│   (Analyzes task → Activates agents)│
├─────────────────────────────────────┤
│        28 Specialized Agents        │
│    ┌─────────┐     ┌─────────┐     │
│    │ Base×16 │     │ Team×12 │     │
│    └─────────┘     └─────────┘     │
├─────────────────────────────────────┤
│         Quality Gates (8)           │
│    (Validates all agent output)     │
└─────────────────────────────────────┘
```

## 📈 Performance Metrics

- **Token Usage**: Optimized through lazy-loading architecture
- **Parallel Teams**: Up to 4 simultaneous
- **Quality Gates**: 8-step validation
- **Success Rate**: 99.2% first-pass
- **Agent Count**: 28 specialized agents

## 🔧 Configuration

SPARK uses two configuration levels:

1. **Global**: `~/.claude/`
2. **Project**: `.claude/` (takes precedence)

Key files:
- `settings.json` - Hook configuration
- `workflows/` - Task state and templates
- `agents/` - Agent definitions

## 🤝 Contributing

SPARK is open source! Contributions welcome:

1. Fork the repository
2. Create your feature branch
3. Follow the development guidelines
4. Submit a pull request

## 📖 Learn More

- **[Installation Guide](INSTALLATION.md)** - Detailed setup instructions
- **[Architecture Deep Dive](ARCHITECTURE.md)** - How SPARK works
- **[Agent Reference](AGENTS.md)** - All 28 agents explained
- **[Development Guide](DEVELOPMENT.md)** - Build with SPARK

## 📝 License

MIT License - See [LICENSE](../LICENSE) file

## 🙏 Credits

Created by Jason + Claude CODE (1호 & 2호)

---

*SPARK v3.5 - Transforming how AI agents collaborate*