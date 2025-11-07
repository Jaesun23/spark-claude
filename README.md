# ⚡ SPARK v4.3 Plugin

> **Subagent Performance Architecture with Reduced toKens**
> A traits-based multi-agent orchestration system distributed as a Claude Code plugin.

[![Version](https://img.shields.io/badge/version-4.3.0-gold?style=for-the-badge)](spark-plugin/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-2.0%2B-blue?style=for-the-badge)](https://claude.ai/code)

## What is SPARK?

SPARK v4.3 is a **plugin-based multi-agent system** for [Claude Code](https://claude.ai/code), featuring 21 specialized agents with zero-tolerance quality gates and 95.5% token reduction through progressive disclosure.

### Key Innovation: Plugin Distribution

SPARK is now distributed as a **Claude Code plugin**, making it:
- **Instantly installable**: One command to install all 21 agents
- **Self-documenting**: Complete usage guide included in plugin
- **Version controlled**: Plugin system handles updates
- **Portable**: Works across all projects automatically

## Quick Start

### Installation

```bash
# 1. Install Claude Code 2.0+ (native installer)
# Download from: https://claude.ai/code

# 2. Add SPARK plugin marketplace (for development)
/plugin marketplace add /path/to/spark-claude/spark-plugin

# 3. Install SPARK plugin
/plugin install spark-agents@spark-dev-marketplace

# 4. Verify installation
/context
# You should see 21 agents listed as "Plugin" type
```

### Basic Usage

SPARK agents work through natural language or slash commands:

```bash
# Implementation with quality gates
/spark-implement "Create user authentication with JWT tokens"

# Multi-dimensional analysis
/spark-analyze "Find performance bottlenecks in API layer"

# Comprehensive testing
/spark-test "Achieve 95% coverage for payment module"

# Complete feature pipeline
/spark-launch "Build notification system with email and SMS"
```

## What's Included

### 🤖 21 Specialized Agents

**6 Core Agents**:
- `analyzer-spark` - Multi-dimensional system analysis with evidence collection
- `implementer-spark` - Zero-defect implementation with 95%+ test coverage
- `tester-spark` - Comprehensive testing (95% unit, 85% integration)
- `documenter-spark` - Validated documentation with executable examples
- `designer-spark` - Scalable architecture design
- `qc-spark` - Quality violations cleanup with 5-phase inspection

**15 Team Agents**:
- 5 teams × 3 roles (implementer, tester, documenter)
- Enables parallel execution of up to 5 tasks simultaneously
- Independent coordination via JSON state management

### 📜 12 SPARK Commands

**Single Agent Commands**:
- `/spark-implement` - Feature implementation with quality gates
- `/spark-test` - Comprehensive test creation
- `/spark-analyze` - Multi-dimensional analysis
- `/spark-design` - Architecture design
- `/spark-fix` - Systematic troubleshooting
- `/spark-improve` - Performance optimization

**Pipeline Commands** (Multi-agent workflows):
- `/spark-refactor` - analyze → improve → test
- `/spark-audit` - analyze → troubleshoot → document
- `/spark-migrate` - analyze → design → implement → test
- `/spark-optimize` - analyze → improve → test
- `/spark-launch` - design → implement → test → document

**Parallel Execution**:
- `/multi-implement` - Execute up to 5 tasks in parallel

### 📚 Complete Documentation

The plugin includes comprehensive documentation in `spark-plugin/CLAUDE.md`:
- Agent registry with specializations
- Delegation protocol with project context requirements
- State management via JSON files
- Quality verification with zero-tolerance gates
- Multi-session context strategies
- Agent chain patterns

## Architecture

### Progressive Disclosure

SPARK achieves 95.5% token reduction through progressive disclosure:

1. **Description Load** (~95 tokens/agent): Only descriptions loaded initially
2. **Selection**: Claude Code selects optimal agent based on task
3. **Full Load** (30-44K tokens): Selected agent's full body loaded on demand

**Token Efficiency**:
- 21 agent descriptions: ~2.0K tokens (1% of context)
- Single agent execution: 30-44K tokens
- Traditional approach: Load all agents upfront (600K+ tokens) ❌

### Quality Gates System

All agents follow **zero-tolerance quality standards**:

**8-Step Quality Validation**:
1. Syntax errors: 0
2. Type errors: 0
3. Linting violations: 0
4. Security issues: 0
5. Test coverage: ≥95% (unit), ≥85% (integration)
6. Documentation: 100% completeness
7. All tests: Pass
8. Integration: Clean

**Quality Gate Execution**:
```bash
# Agent self-validation
echo '{"subagent": "implementer-spark", "self_check": true}' | \
python3 ~/.claude/hooks/spark_quality_gates.py

# Returns:
# ✅ "Quality gates PASSED"
# 🚫 "Quality gates FAILED"
```

### State Management

Agents communicate via JSON state files:

```
~/.claude/workflows/current_task.json         # Main task
~/.claude/workflows/team[1-5]_current_task.json  # Team tasks
```

**State Structure**:
```json
{
  "id": "spark_YYYYMMDD_HHMMSS",
  "version": "4.3",
  "state": {"status": "pending|running|completed|failed"},
  "quality": {
    "violations_total": 0,
    "can_proceed": true
  }
}
```

## Project Structure

```
spark-claude/
├── spark-plugin/              # Plugin package (distributable)
│   ├── .claude-plugin/
│   │   ├── plugin.json        # Plugin metadata
│   │   └── marketplace.json   # Local marketplace config
│   ├── CLAUDE.md              # Complete SPARK usage guide
│   ├── README.md              # User documentation
│   ├── agents/                # 21 agent definitions
│   │   ├── analyzer-spark.md
│   │   ├── implementer-spark.md
│   │   ├── tester-spark.md
│   │   ├── documenter-spark.md
│   │   ├── designer-spark.md
│   │   ├── qc-spark.md
│   │   └── team[1-5]-*.md     # 15 team agents
│   └── commands/              # 12 SPARK commands
│       ├── spark-implement.md
│       ├── spark-analyze.md
│       ├── multi-implement.md
│       └── ...
├── docs/                      # Development documentation
│   ├── constitution/          # SPARK Constitution v1.1
│   ├── anthropic-engineering/ # Research materials
│   └── *.md                   # Design documents
└── README.md                  # This file
```

## Development

This repository is a **plugin development project** for SPARK.

### Working on SPARK Plugin

```bash
# 1. Clone the repository
git clone https://github.com/Jaesun23/spark-claude.git
cd spark-claude

# 2. Edit agents or commands
# - Agents: spark-plugin/agents/*.md
# - Commands: spark-plugin/commands/*.md
# - Documentation: spark-plugin/CLAUDE.md

# 3. Test changes
# Restart Claude Code to reload plugin

# 4. Verify
/context  # Check agents load correctly
```

### Constitution v1.1

All agents follow SPARK Constitution v1.1 principles:

- **EVIDENCE/TEST-BEFORE-REPORT**: Protocols requiring proof before claims
- **PROJECT-CONTEXT-DISCOVERY**: Agents discover and follow project standards
- **Zero-Tolerance Quality**: All violations must be 0 to proceed
- **90K Token Safety**: All agents include safety protocols
- **Flexible Phases**: Workflow adapts to task complexity

See `docs/constitution/` for complete constitution documents.

### Key Files

- `spark-plugin/CLAUDE.md` - SPARK usage guide (read by Claude Code)
- `docs/constitution/1_CONSTITUTION.md` - SPARK Constitution v1.1
- `docs/constitution/2_AGENT_DESIGN_GUIDE.md` - Agent design principles
- `docs/AGENT_DESCRIPTION_UNDERSTANDING.md` - Description as decision algorithm

## Project Evolution

### From Super Claude to SPARK Plugin

SPARK began as a conversion of Super Claude's persona system into a specialized multi-agent architecture:

**Super Claude (Original)**:
- Monolithic 11-persona system
- All personas loaded simultaneously
- ~600K tokens for full context

**SPARK v3.0-4.2** (Multi-agent System):
- 32 specialized agents (17 primary + 15 team)
- Lazy loading architecture
- Installed via `~/.claude/agents/` and `~/.claude/commands/`

**SPARK v4.3** (Plugin System):
- 21 agents (6 core + 15 team)
- Distributed as Claude Code plugin
- Progressive disclosure (95.5% token reduction)
- Self-contained with complete documentation

### Version History

- **v3.0**: Initial multi-agent system with lazy loading
- **v3.5**: Quality gates and refined hooks
- **v3.8**: TRAITS revolution (trait-based behavior)
- **v4.1**: Unified Phase structure with JSON state
- **v4.3**: Plugin-based distribution with progressive disclosure

## About This Project

SPARK was created through collaboration between:

- **Jason** ([@Jaesun23](https://github.com/Jaesun23)) - Human architect and project lead
- **1호 (Claude Desktop)** - Design and architecture partner
- **2호 (Claude Code)** - Implementation and refinement partner

*A demonstration of human-AI collaboration in building enterprise-grade developer tools.*

## Contributing

We welcome contributions! SPARK is an open-source project.

### How to Contribute

1. Fork the repository
2. Create feature branch (`git checkout -b feature/your-feature`)
3. Make changes to `spark-plugin/` (agents, commands, or docs)
4. Test with local plugin installation
5. Commit changes (`git commit -m 'Add your feature'`)
6. Push to branch (`git push origin feature/your-feature`)
7. Open Pull Request

### Development Guidelines

- Follow SPARK Constitution v1.1 principles
- Maintain 7-section agent structure
- Include Triggering Conditions in agent descriptions
- Add Example Usage Scenarios
- Test all quality gates pass

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Resources

- **GitHub**: [Jaesun23/spark-claude](https://github.com/Jaesun23/spark-claude)
- **Issues**: [GitHub Issues](https://github.com/Jaesun23/spark-claude/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Jaesun23/spark-claude/discussions)
- **Claude Code**: [claude.ai/code](https://claude.ai/code)

---

<p align="center">
  <i>Built with passion by Jason, 1호, and 2호</i><br>
  <i>One human, two AIs, infinite possibilities</i>
</p>
