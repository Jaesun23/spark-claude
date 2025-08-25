# 📚 SPARK v4.1 Documentation

## Quick Navigation

| Document | Description | Purpose |
|----------|-------------|---------|
| **[SPARK_COMPLETE_GUIDE.md](SPARK_COMPLETE_GUIDE.md)** | 🎯 **Start Here** - Complete system guide | Full reference for commands, agents, and workflows |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System architecture and design | Technical details and system components |
| **[INSTALLATION.md](INSTALLATION.md)** | Installation and setup guide | Getting started with SPARK |
| **[PHASE_STRUCTURE.md](PHASE_STRUCTURE.md)** | Agent phase structure details | Deep dive into 5-phase methodology |
| **[TEAM_AGENTS.md](TEAM_AGENTS.md)** | Multi-team parallel execution | Guide for parallel agent coordination |

## 🚀 Quick Start

```bash
# 1. Install SPARK
cd /path/to/project
git clone <spark-repo>
./scripts/install.sh

# 2. Basic Usage
/spark-implement "new feature"     # Single agent
/spark "complex task"              # Full pipeline
/multi-implement t1,t2,t3,t4      # Parallel execution
```

## 📊 System Overview

- **28 Specialized Agents**: Expert agents for every task
- **95.5% Token Reduction**: Efficient on-demand loading
- **8-Step Quality Gates**: Zero-tolerance verification
- **Parallel Execution**: 4x speedup with team agents

## 🎯 Most Common Commands

### For Development
- `/spark-implement` - Build new features
- `/spark-test` - Create comprehensive tests
- `/spark-document` - Generate documentation

### For Maintenance
- `/spark-analyze` - System analysis
- `/spark-refactor` - Code improvement
- `/spark-clean` - Remove technical debt

### For Complex Tasks
- `/spark` - Full development pipeline
- `/multi-implement` - Parallel execution
- `/spark-launch` - Complete feature launch

## 📖 Documentation Structure

```
docs/
├── README.md                 # This file - Overview
├── SPARK_COMPLETE_GUIDE.md   # Complete reference
├── ARCHITECTURE.md           # System design
├── INSTALLATION.md           # Setup guide
├── PHASE_STRUCTURE.md        # Agent phases
├── TEAM_AGENTS.md            # Parallel execution
└── templates/                # Report templates
    └── agent-reports/        # Agent report formats
```

## 💡 Key Concepts

### Quality Gates
All agents must pass 8-step verification with zero violations.

### Phase Structure
Every agent follows Phase 0-5, with mandatory Phase 5B quality gates.

### Token Management
90K token safety limit with automatic compression strategies.

### Parallel Execution
Team agents enable 4x parallel processing for complex tasks.

## 🔗 Related Resources

- **Agent Definitions**: `.claude/agents/`
- **Command Files**: `.claude/commands/`
- **Quality Gates**: `.claude/hooks/spark_quality_gates.py`
- **JSON States**: `.claude/workflows/`

---

*SPARK v4.1 - Production Ready*