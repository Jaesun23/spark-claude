# SPARK - Universal Expert Agent Framework

> **SPARK** = **S**ubagent **P**erformance **A**rchitecture with **R**educed to**K**ens

This file provides guidance to Claude Code when working with this repository.

---

## 🎯 Project Identity

### What is SPARK?

SPARK is a **multi-agent orchestration framework** that enables specialized expert agents to collaborate efficiently through on-demand loading and strict quality enforcement.

**Born from necessity**: SuperClaude consumed 44,000 tokens per request by loading all personas simultaneously. SPARK achieved **88.4% token reduction** (44K → 5.1K) by loading only the required agents.

**Current State** (v4.3):
- ✅ 21 Specialized Agents (6 core + 15 team)
- ✅ Plugin-based Distribution
- ✅ SPARK Constitution v1.2
- ✅ **Domain**: Software Development

**Vision**:
> SPARK started with software development, but the ultimate goal is to create expert agents for **all domains and all types of work**.

Future domains:
- Software Development (current) ✅
- Data Analysis & Science
- Writing & Editing
- Research & Learning
- Design & Creative
- Business & Consulting
- Legal & Compliance
- Healthcare & Medicine
- Education & Training
- ... (unlimited expansion)

### The Journey

```
2025-08-08  v1.0  Problem Discovery      → 44K tokens identified
2025-08-11  v2.0  SPARK Concept Born     → MAS framework
2025-08-13  v3.0  First Implementation   → 81.8% reduction
2025-08-17  v4.0  Quality Evolution      → Phase 5B mandatory
2025-08-19  v4.1  Final Architecture     → 88.4% achieved ✅
2025-08-23  v4.2  Code Enhancement       → Trait-based
2025-09-05  v4.3  Current System         → Plugin-based
```

**Detailed History**: See [00-SPARK-HISTORY-INDEX.md](./docs/history/00-SPARK-HISTORY-INDEX.md)

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Jaesun23/spark-claude

# Setup environment (recommended: uv)
uv venv && source .venv/bin/activate
uv pip install -e ".[full,dev,benchmark]"

# Verify installation
ruff check .
mypy .
pytest tests/
```

### Basic Usage

**Single Agent**:
```bash
# Analyze system
/spark-analyze "performance bottlenecks"

# Implement feature
/spark-implement "user authentication"

# Create tests
/spark-test "authentication module"
```

**Pipeline (Sequential)**:
```bash
# Full workflow
/spark "add payment processing feature"
# → analyze → implement → test → document
```

**Parallel Execution**:
```bash
# Multiple tasks simultaneously
/multi-implement "task1,task2,task3,task4,task5"
```

### Example Workflow

```
1. Analyze codebase
   /spark-analyze "API performance"

2. Review quality
   Task("qc-spark", "fix all ruff violations")

3. Implement improvements
   /spark-implement "cache layer for API"

4. Comprehensive testing
   /spark-test "cache implementation"

5. Documentation
   /spark-document "cache architecture"
```

---

## 🏗️ Architecture

### 3-Layer System

```
┌─────────────────────────────────────┐
│  Layer 1: Router                    │
│  spark_persona_router.py            │
│  → Analyzes task                    │
│  → Selects optimal agent            │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Layer 2: Quality Gates             │
│  spark_quality_gates.py             │
│  → Verifies agent claims            │
│  → Enforces quality standards       │
└─────────────┬───────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Layer 3: Agent Layer               │
│  21 specialized agents              │
│  → 6 core + 15 team                 │
│  → Trait-based personas             │
└─────────────────────────────────────┘
```

### 21 Specialized Agents

**6 Core Agents** (Primary Specialists):

1. **analyzer-spark** (v2.0)
   - Multi-dimensional system analysis
   - Evidence-based reporting (file:line)
   - 12+ evidence items mandatory

2. **implementer-spark**
   - Feature implementation
   - 95% test coverage requirement
   - Zero-defect delivery

3. **tester-spark**
   - Comprehensive testing
   - 95% unit / 85% integration coverage
   - E2E critical paths

4. **designer-spark**
   - System architecture
   - API specifications
   - UX/UI design

5. **documenter-spark**
   - API documentation
   - User guides
   - Architecture docs

6. **qc-spark**
   - Quality violations cleanup
   - Ruff/MyPy corrections
   - 5-phase inspection

**15 Team Agents** (Parallel Execution):
- 5 teams × 3 roles (implementer, tester, documenter)
- Used exclusively for parallel execution
- Supports `/multi-implement` command

### Plugin Structure

```
spark-claude/
├── .claude/
│   ├── agents/          # 21 agent definitions
│   ├── commands/        # Slash commands
│   ├── hooks/          # Router & Quality Gates
│   ├── constitution/   # v1.2 (English + Korean)
│   └── workflows/      # JSON state files
├── docs/               # Core documentation
├── benchmarks/         # Performance tests
└── tests/             # Quality tests
```

### Token Management

**Safety Protocol**:
- Hard limit: 200K tokens per request
- Practical limit: 90K tokens (safety margin)
- Agent sizes: ~1K (team) to ~3.9K (implementer)
- Write operations: 2x token consumption

**Current Achievement**:
```
SuperClaude: 44,000 tokens (all personas)
SPARK v4.3:   5,100 tokens (on-demand)
Reduction:    88.4% ✅
```

### JSON State Management

**Location**: `~/.claude/workflows/current_task.json`

**Structure**:
```json
{
  "id": "spark_YYYYMMDD_HHMMSS",
  "version": "4.3",
  "agent": "implementer-spark",
  "state": {
    "status": "completed",
    "current_phase": 5
  },
  "quality": {
    "violations_total": 0,
    "can_proceed": true,
    "step_6_testing": {
      "ruff_violations": 0,
      "mypy_errors": 0,
      "coverage": 0.97
    }
  }
}
```

**Team Agents**: Separate state files (`team1_current_task.json`, etc.)

---

## 📖 Usage Guide

### Single Agent Commands

```bash
/spark-analyze <scope>        # Multi-dimensional analysis
/spark-implement <feature>    # Feature implementation
/spark-test <target>          # Comprehensive testing
/spark-design <system>        # Architecture & design
/spark-document <topic>       # Documentation
Task("qc-spark", "fix ...")   # Quality cleanup (direct Task call)
```

### Pipeline Commands

Sequential phase execution:

```bash
/spark <task>                 # Full: analyze → implement → test → document
/spark-refactor <module>      # analyze → improve → test
/spark-audit <system>         # analyze → troubleshoot → document
/spark-migrate <legacy>       # analyze → design → implement → test
/spark-optimize <scope>       # analyze → improve → test
/spark-launch <feature>       # design → implement → test → document → git
```

### Parallel Execution

Up to 5 tasks simultaneously:

```bash
/multi-implement task1,task2,task3,task4,task5

# Uses team agents:
# team1-implementer-spark → task1
# team2-implementer-spark → task2
# ... etc.
```

### Quality Gates

**8-Step Framework**:
1. Syntax Validation (0 errors)
2. Type Checking (`mypy --strict`)
3. Linting (`ruff --strict`)
4. Security (OWASP compliance)
5. Test Coverage (95% unit / 85% integration)
6. Performance (O(n) verification)
7. Documentation (100% docstrings)
8. Integration (E2E passing)

**Enforcement**: Phase 5B mandatory for all agents

---

## 🛠️ Development Guide

### Adding New Agents

**For Software Development Domain**:
1. Define agent in `.claude/agents/{name}-spark.md`
2. Follow trait-based format:

```markdown
---
name: {agent-name}-spark
version: 4.3
domain: software-development
---

# Traits (성격/특성)
- Trait 1
- Trait 2

# Protocols (작업 프로토콜)
## Phase 1: Task Understanding
## Phase 2: Planning
## Phase 3: Execution
## Phase 4: Verification
## Phase 5: Quality Gates
  - 5A: Metrics recording
  - 5B: Gates execution (MANDATORY)
```

3. Add to router (`spark_persona_router.py`)
4. Add tests
5. Update documentation

**For New Domains** (Future):
1. Create domain-specific constitution
2. Define domain agents
3. Adapt quality gates for domain
4. Test domain expertise
5. Document domain usage

### Constitution Compliance

All agents must follow **SPARK Constitution v1.2**:

**5 Core Documents**:
1. Core Principles
2. Quality Standards
3. Work Protocols
4. Communication
5. Evolution

**Available in**:
- English: `.claude/constitution/`
- Korean: `.claude/constitution/ko/`

**Key Requirements**:
- Evidence-based reporting (file:line)
- Phase 5B mandatory execution
- 0 violations tolerance
- Adaptive, iterative workflow

### Testing & Quality

**Pre-commit Hooks**:
```bash
# Auto-run on git commit
ruff check .
mypy .
pytest tests/ --cov
```

**CI/CD Pipeline**:
- Syntax validation
- Type checking
- Linting
- Test coverage (95%+)
- E2E tests

**Quality Verification**:
```bash
# Agent self-validation
echo '{"subagent": "implementer-spark"}' | \
python3 ~/.claude/hooks/spark_quality_gates.py
```

### Plugin Distribution

**Current**: Integrated into project
**Future**: Plugin marketplace

**Installation** (when plugin-based):
```bash
# Option 1: Global
~/.claude/plugins/spark/

# Option 2: Project-specific
project/.claude/plugins/spark/
```

---

## 📚 Reference

### Version History

**Complete History**: [00-SPARK-HISTORY-INDEX.md](./docs/history/00-SPARK-HISTORY-INDEX.md)

**Individual Versions**:
- [v1.0 - SuperClaude Analysis](./docs/history/01-v1.0-SuperClaude-Analysis.md)
- [v2.0 - Research Foundation](./docs/history/02-v2.0-Research-Foundation.md)
- [v3.0 - Initial Implementation](./docs/history/03-v3.0-Initial-Implementation.md)
- [v4.0 - Quality Evolution](./docs/history/04-v4.0-Quality-Evolution.md)
- [v4.1 - Final Architecture](./docs/history/05-v4.1-Final-Architecture.md)
- [v4.2-v4.3 - Current](./docs/history/06-v4.2-v4.3-Current.md)

### Git Histories

- [SPARK_CLAUDE_GIT_HISTORY_v4.1_AFTER.txt](./docs/history/SPARK_CLAUDE_GIT_HISTORY_v4.1_AFTER.txt) - 73 commits (v4.1 이후)
- [DNA_METHODOLOGY_GIT_HISTORY.txt](./docs/history/DNA_METHODOLOGY_GIT_HISTORY.txt) - 51 commits (DNA 방법론)

### Key Documents

**Core Documentation**:
- [ARCHITECTURE.md](./docs/ARCHITECTURE.md) - System architecture
- [SPARK_CONSTITUTION.md](./docs/SPARK_CONSTITUTION.md) - Agent behavior
- [TEAM_AGENTS.md](./docs/TEAM_AGENTS.md) - Parallel execution

**Constitution v1.2**:
- English: `.claude/constitution/`
- Korean: `.claude/constitution/ko/`

**Archives**:
```
/Users/jason/Documents/개발아카이브/spark-claude-archive/
├── v1.0-SuperClaude-Analysis/
├── v2.0-Research-Foundation/
├── v3.0-Initial-Implementation/
│   └── SPARK_Development_Chronology_20250118.md
├── v4.0-Quality-Evolution/
├── v4.1-Final-Architecture/ (2025-08-22 공식 아카이브)
└── ARCHIVE_README.md
```

### Related Projects

**DNA Methodology**: AI collaboration framework
- Repository: https://github.com/Jaesun23/dna-methodology
- Purpose: 9-Stage design methodology for AI projects
- Relation: SPARK (tool) + DNA (methodology) = Complete AI collaboration

### Contact

**Jason Park**
- Email: jaesun23@gmail.com
- GitHub: https://github.com/Jaesun23
- SPARK: https://github.com/Jaesun23/spark-claude

---

## 🤖 For Claude Code (2호)

### Critical Execution Protocol

When receiving SPARK commands, **MUST** follow this exact pattern:

**Single Agent**:
```python
1. IMMEDIATELY CALL:
   Task("agent-name-spark", user_request)

2. WAIT for completion

3. CHECK ~/.claude/workflows/current_task.json:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"

4. DECISION:
   ✅ ALL MET → Report success
   ❌ ANY FAILED → Retry with feedback (max 3 attempts)
```

**Parallel Execution** (MUST be in ONE message):
```python
Task("team1-implementer-spark", task1)
Task("team2-implementer-spark", task2)
Task("team3-implementer-spark", task3)
Task("team4-implementer-spark", task4)
Task("team5-implementer-spark", task5)
# WAIT for ALL to complete
```

### Common Pitfalls to Avoid

❌ **DON'T**:
- Load multiple agents unnecessarily
- Sequential Task calls for parallel execution
- Skip quality gate validation
- Forget to check JSON state
- Ignore write operations (2x tokens!)

✅ **DO**:
- Load one agent at a time (unless parallel)
- Check JSON state after agent completion
- Verify all quality gates passed
- Monitor token consumption
- Follow Constitution v1.2

### Token Safety

**Limits**:
- Hard limit: 200K tokens
- Practical limit: 90K tokens (safety)
- Per agent: 1K-3.9K tokens

**Safety Protocol**:
- Check token budget before agent call
- Write operations = 2x consumption
- Compression available (30-50% reduction)

### Quality Verification

**After agent completion**:
```bash
# Verify quality gates
cat ~/.claude/workflows/current_task.json | \
jq '.quality.violations_total'

# Expected: 0
```

**Quality Gates Script**:
```bash
python3 ~/.claude/hooks/spark_quality_gates.py
```

Returns:
- ✅ "Quality gates PASSED"
- 🚫 "Quality gates FAILED" (+ violation details)

---

## 🎓 Key Principles

### 1. Quality is Non-Negotiable
> "Optional quality checks are ignored. Only MANDATORY enforcement works."

### 2. Evidence-Based Work
All analysis must include:
- file:line references
- Minimum 12 evidence items
- Concrete, verifiable facts

### 3. Agent Isolation
- Agents CANNOT call other agents
- Only Claude Code uses Task tool
- Prevents circular dependencies

### 4. Trait-Based Design
```
Agent = Traits (personality) + Protocols (workflow)
```

### 5. Universal Framework
SPARK is domain-agnostic:
- Current: Software development
- Future: All domains
- Principle: Expert agents for any field

---

## 🔮 Future Roadmap

### Short-term
- ✅ Skills integration
- ✅ Plugin marketplace
- ⏳ More specialized software agents

### Long-term
- 🎯 **Domain expansion**: Data science, writing, research, etc.
- 🎯 **Cross-domain collaboration**: Software + Data + Business agents
- 🎯 **Learning across sessions**: Agent improvement over time
- 🎯 **Community contributions**: Open agent ecosystem

### Vision
> "A universal framework where expert agents collaborate across all domains to solve any problem with guaranteed quality."

---

*Last Updated: 2025-12-01*
*SPARK Version: v4.3 (Plugin-based)*
*Constitution: v1.2*
*Total Journey: 4 months (Aug 2025 - present)*
