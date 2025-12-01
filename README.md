# ⚡ SPARK - Universal Expert Agent Framework

> **Subagent Performance Architecture with Reduced toKens**
> A multi-agent orchestration framework for creating specialized expert agents across all domains.

[![Version](https://img.shields.io/badge/version-4.3.0-gold?style=for-the-badge)](spark-plugin/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-2.0%2B-blue?style=for-the-badge)](https://claude.ai/code)
[![Token Reduction](https://img.shields.io/badge/Token%20Reduction-88.4%25-green?style=for-the-badge)](#key-achievements)

## 🎯 Vision

**Current**: SPARK enables software development with 21 specialized agents
**Future**: SPARK will support expert agents for **all domains and all types of work**

> "현재는 소프트웨어 개발이 전부이지만 최종목표는 모든 분야의 다양한 유형의 작업에 전문가 에이전트를 생성하는 것입니다." - Jason

**Future Domains**:
- Software Development ✅ (current)
- Data Analysis & Science
- Writing & Editing
- Research & Learning
- Design & Creative
- Business & Consulting
- Legal & Compliance
- Healthcare & Medicine
- Education & Training
- ... (unlimited expansion)

## What is SPARK?

SPARK v4.3 is a **plugin-based multi-agent orchestration framework** for [Claude Code](https://claude.ai/code), featuring:

- 🎯 **21 Specialized Agents** (6 core + 15 team) with domain expertise
- 🛡️ **Zero-Tolerance Quality Gates** (Ruff 0, MyPy 0, Coverage 95%+)
- ⚡ **88.4% Token Reduction** (44,000 → 5,100 tokens through on-demand loading)
- 📦 **Plugin Distribution** (instantly installable, version-controlled)
- 📜 **Constitution v1.2** (English + Korean behavior standards)

## 🏆 Key Achievements

From 4 months of development (2025-08-08 to 2025-12-01):

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Tokens/Request** | 44,000 | 5,100 | **88.4% reduction** ✅ |
| **Agent Count** | 11 (monolithic) | 21 (specialized) | **+91% specialization** |
| **Quality Gates** | Optional | MANDATORY | **100% enforcement** |
| **Pass Rate** | 60-70% | 95-100% target | **+40% quality** |
| **Coverage** | 60% | 95%/85% (unit/int) | **+58% coverage** |

**Journey Timeline**:
```
2025-08-08  v1.0  Problem Discovery      → 44K tokens identified
2025-08-11  v2.0  SPARK Concept Born     → MAS framework
2025-08-13  v3.0  First Implementation   → 81.8% reduction
2025-08-17  v4.0  Quality Evolution      → Phase 5B mandatory
2025-08-19  v4.1  Final Architecture     → 88.4% achieved ✅
2025-08-23  v4.2  Code Enhancement       → Trait-based personas
2025-09-05  v4.3  Current System         → Plugin-based distribution
2025-11-08  ---   DNA Methodology        → AI collaboration framework
```

**Complete History**: See [00-SPARK-HISTORY-INDEX.md](./00-SPARK-HISTORY-INDEX.md) for detailed version-by-version documentation.

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

**Core Documentation**:
- [CLAUDE.md](./CLAUDE.md) - Complete SPARK guide for Claude Code (594 lines)
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture and design
- [SPARK_CONSTITUTION.md](./SPARK_CONSTITUTION.md) - Agent behavior standards v1.2

**Version History** (8 documents):
- [00-SPARK-HISTORY-INDEX.md](./00-SPARK-HISTORY-INDEX.md) - Complete history overview
- [v1.0-SuperClaude-Analysis.md](./v1.0-SuperClaude-Analysis.md) - Problem discovery (Aug 8-10)
- [v2.0-Research-Foundation.md](./v2.0-Research-Foundation.md) - SPARK concept birth (Aug 11-12)
- [v3.0-Initial-Implementation.md](./v3.0-Initial-Implementation.md) - First working system (Aug 13-16)
- [v4.0-Quality-Evolution.md](./v4.0-Quality-Evolution.md) - Quality gates establishment (Aug 17-18)
- [v4.1-Final-Architecture.md](./v4.1-Final-Architecture.md) - 88.4% achieved (Aug 19-22)
- [v4.2-v4.3-Current.md](./v4.2-v4.3-Current.md) - Plugin architecture (Aug 23-present)

**Git Histories**:
- [SPARK_CLAUDE_GIT_HISTORY_v4.1_AFTER.txt](./SPARK_CLAUDE_GIT_HISTORY_v4.1_AFTER.txt) - 73 commits from v4.1 onwards
- [DNA_METHODOLOGY_GIT_HISTORY.txt](./DNA_METHODOLOGY_GIT_HISTORY.txt) - 51 commits for AI collaboration methodology

## Architecture

### Progressive Disclosure

SPARK achieves 88.4% token reduction through on-demand agent loading:

1. **Router Analysis** (~5K tokens): 2호 (Claude Code orchestrator) analyzes task
2. **Agent Selection**: Selects optimal agent from 21 specialists
3. **Full Load** (5-8K tokens): Selected agent's complete definition loaded
4. **Execution**: Agent works with quality gates enforcement
5. **Verification**: State validated, violations checked (must be 0)

**Token Efficiency**:
- Traditional approach: Load all agents upfront (44K+ tokens) ❌
- SPARK approach: Load only what's needed (5.1K tokens average) ✅
- **Result**: 88.4% reduction, 8.6x more efficient

### Three-Layer System

```
┌─────────────────────────────────────┐
│  Layer 1: Router                    │
│  spark_persona_router.py            │
│  - Task analysis                    │
│  - Agent selection                  │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Layer 2: Quality Gates             │
│  spark_quality_gates.py             │
│  - Validation                       │
│  - Enforcement                      │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Layer 3: Agent Layer               │
│  .claude/agents/*-spark.md          │
│  - 21 specialized agents            │
│  - 6 core + 15 team                 │
└─────────────────────────────────────┘
```

### Quality Gates System

All agents follow **zero-tolerance quality standards**:

**8-Step Quality Validation**:
1. Syntax errors: 0
2. Type errors: 0 (mypy --strict)
3. Linting violations: 0 (ruff --strict)
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
│   ├── constitution/          # SPARK Constitution v1.2
│   ├── anthropic-engineering/ # Research materials
│   └── *.md                   # Design documents
├── v1.0-SuperClaude-Analysis.md      # Version history
├── v2.0-Research-Foundation.md
├── v3.0-Initial-Implementation.md
├── v4.0-Quality-Evolution.md
├── v4.1-Final-Architecture.md
├── v4.2-v4.3-Current.md
├── 00-SPARK-HISTORY-INDEX.md         # Complete history index
├── CLAUDE.md                          # For Claude Code
├── ARCHITECTURE.md                    # System architecture
├── SPARK_CONSTITUTION.md              # Agent standards
└── README.md                          # This file
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

### Constitution v1.2

All agents follow SPARK Constitution v1.2 principles:

- **EVIDENCE/TEST-BEFORE-REPORT**: Protocols requiring proof before claims
- **PROJECT-CONTEXT-DISCOVERY**: Agents discover and follow project standards
- **Zero-Tolerance Quality**: All violations must be 0 to proceed
- **90K Token Safety**: All agents include safety protocols
- **Flexible Phases**: Workflow adapts to task complexity

See `docs/constitution/` for complete constitution documents (English + Korean).

### Key Files

- `spark-plugin/CLAUDE.md` - SPARK usage guide (read by Claude Code)
- `CLAUDE.md` - Complete project guide with vision and history
- `ARCHITECTURE.md` - System architecture and design
- `SPARK_CONSTITUTION.md` - Agent behavior standards v1.2
- `docs/constitution/1_CONSTITUTION.md` - Detailed constitution
- `docs/constitution/2_AGENT_DESIGN_GUIDE.md` - Agent design principles
- `docs/AGENT_DESCRIPTION_UNDERSTANDING.md` - Description as decision algorithm

## Project Evolution

### From SuperClaude to Universal Framework

**SuperClaude (Original - Aug 2025)**:
- Monolithic 11-persona system
- All personas loaded simultaneously
- ~44,000 tokens per request
- 60-70% pass rate
- 300+ quality violations

**SPARK v3.0 (First Implementation - Aug 13-16, 2025)**:
- 20 specialized agents with isolation
- On-demand loading architecture
- 8,000 tokens (81.8% reduction)
- JSON state management
- Quality gates introduced

**SPARK v4.0 (Quality Evolution - Aug 17-18, 2025)**:
- Phase 5B MANDATORY enforcement
- 8-step quality gates framework
- "Optional quality checks are ignored" lesson learned
- Quality system restored (400+ → <50 violations)

**SPARK v4.1 (Final Architecture - Aug 19-22, 2025)**:
- **88.4% token reduction achieved** ✅
- 28 agents (16 primary + 12 team)
- 3-layer system (Router → Quality Gates → Agents)
- Production-ready completion
- Last official archive (2025-08-22)

**SPARK v4.2-v4.3 (Current - Aug 23-present)**:
- Trait-based persona format (Traits + Protocols)
- Code-based behavior protocols (dual-layer enforcement)
- 21 agents (6 core + 15 team) - focused specialization
- Plugin-based distribution
- SPARK Constitution v1.2 (English + Korean)
- DNA Methodology v4.0 integration

**Future (Universal Expert Agent Framework)**:
- Expand beyond software development
- Support all domains and work types
- Maintain quality standards across domains
- Community-contributed domain agents

### Version History

For complete timeline and detailed analysis, see:
- [00-SPARK-HISTORY-INDEX.md](./00-SPARK-HISTORY-INDEX.md) - Navigation and overview
- Individual version documents (v1.0 through v4.3)
- Git history files (SPARK + DNA methodology)

## About This Project

SPARK was created through collaboration between:

- **Jason** ([@Jaesun23](https://github.com/Jaesun23)) - Human architect and project lead
- **1호 (Claude Desktop)** - Design and architecture partner
- **2호 (Claude Code)** - Implementation and refinement partner

*A demonstration of human-AI collaboration in building enterprise-grade developer tools.*

> "한계극복!!! 그 방법은 '환경'을 만드는 것!" - Jason

### Related Projects

- **[DNA Methodology](https://github.com/Jaesun23/dna-methodology)** - AI collaboration methodology v4.0
  - 9-Stage software design process
  - 11 DNA Systems (common modules)
  - Relationship: SPARK (tool) + DNA (methodology) = Complete AI collaboration

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

- Follow SPARK Constitution v1.2 principles
- Maintain 7-section agent structure
- Include Triggering Conditions in agent descriptions
- Add Example Usage Scenarios
- Test all quality gates pass
- Document new features in CLAUDE.md

### Adding New Domain Support

To expand SPARK to new domains:

1. Study existing agents as templates
2. Define domain-specific quality standards
3. Create specialized agents for the domain
4. Write domain-specific commands
5. Add to CLAUDE.md with examples
6. Submit PR with documentation

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Resources

- **GitHub**: [Jaesun23/spark-claude](https://github.com/Jaesun23/spark-claude)
- **Issues**: [GitHub Issues](https://github.com/Jaesun23/spark-claude/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Jaesun23/spark-claude/discussions)
- **Claude Code**: [claude.ai/code](https://claude.ai/code)
- **DNA Methodology**: [Jaesun23/dna-methodology](https://github.com/Jaesun23/dna-methodology)

## Acknowledgments

이 시스템은 Jason과 2호(Claude Code)의 4개월간 협업으로 탄생했습니다.

SuperClaude에서 SPARK로, 그리고 DNA 방법론으로 이어지는 여정은 AI 협업의 가능성을 보여주었습니다.

**Key Lessons**:
1. 모놀리식은 비효율적 (44K → 5.1K tokens)
2. 데이터 기반 설계 (78% 협업 패턴 발견)
3. Quality는 타협 불가 (MANDATORY enforcement)
4. 자동화가 핵심 (manual checks fail)
5. 점진적 개선 (v1.0 → v4.3)
6. Trait-based의 가치 (명확한 특성 정의)
7. Constitution의 필요성 (공통 규범)

---

<p align="center">
  <i>Built with passion by Jason, 1호, and 2호</i><br>
  <i>One human, two AIs, infinite possibilities</i><br>
  <br>
  <b>From software development to universal expertise</b><br>
  <i>SPARK: Where specialization meets orchestration</i>
</p>
