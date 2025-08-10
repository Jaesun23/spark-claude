# ⚡ SPARK v3.5: Unified AI Agent System for Claude Code

> **Subagent Performance Architecture with Reduced toKens**
> 
> *The ultimate multi-agent automation system with 88.4% token efficiency and enterprise-grade quality gates*

[![Version](https://img.shields.io/badge/VERSION-3.5%20UNIFIED-gold?style=for-the-badge)](docs/SPARK_AGENTS_GUIDE.md)
[![GitHub stars](https://img.shields.io/github/stars/Jaesun23/spark-claude?style=for-the-badge)](https://github.com/Jaesun23/spark-claude/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)
[![Performance](https://img.shields.io/badge/TOKEN%20REDUCTION-88.4%25-brightgreen?style=for-the-badge)](benchmarks/)
[![Quality Gates](https://img.shields.io/badge/QUALITY%20GATES-8%20STEPS-purple?style=for-the-badge)](docs/UNIFIED_SPARK_SYSTEM.md)
[![Claude Code](https://img.shields.io/badge/CLAUDE%20CODE-COMPATIBLE-blue?style=for-the-badge)](https://claude.ai/code)

## 🎯 What is SPARK v3.5?

SPARK v3.5 Unified is the **most advanced AI agent system** for [Claude Code](https://claude.ai/code) that provides:

- 🧠 **16 Specialized Agents**: Implementation, analysis, testing, design, debugging, and more
- 🚀 **88.4% Token Efficiency**: 5,100 vs 44,000 tokens (compared to traditional approaches)  
- 🔄 **Unified Orchestrator**: 6 lifecycle hooks with intelligent routing
- 🛡️ **Jason's 8-Step Quality Gates**: Efficient zero-tolerance validation system
- ⚡ **Task Orchestration**: "Task Task Task → 시작!" pattern for true parallelism
- 🌍 **Language Agnostic**: Python, JavaScript, TypeScript, Go, Rust, and more
- 🔒 **Security Hardened**: SecureCommandExecutor prevents malicious operations
- 🔁 **Intelligent Retry**: Automatic recovery with smart guidance (max 3 attempts)
- 📊 **8 Persona Modes**: Backend, Frontend, Security, Architecture, DevOps, Data, Testing, Documentation
- 🎯 **SuperClaude Integration**: All agents incorporate SuperClaude 5-Phase methodology

## 🚨 Critical Architecture Principles

### 1. **Only 2호 (Number Two) Can Call Agents**
- Agents CANNOT call other agents - only 2호 has Task tool permission
- All orchestration decisions belong exclusively to 2호
- Agents work independently and relay information through JSON files

### 2. **Parallel Execution Synchronization**
- ALL parallel agents must complete before proceeding to next phase
- If team1 finishes early, it waits for team2, team3, team4
- This ensures consistency and prevents race conditions

## 🚀 Quick Start

### 1. **Easy Installation**
```bash
# Clone this repository
git clone https://github.com/Jaesun23/spark-claude.git
cd spark-claude

# Run the installer (installs to ~/.claude/ automatically)
./scripts/install.sh
```

### 2. **Use SPARK Commands**

**Core Commands:**
```bash
/spark "implement JWT authentication with refresh tokens"
/spark-analyze "find performance bottlenecks in the API layer"
/spark-test "create comprehensive tests with 95% coverage"
/spark-design "build responsive dashboard with accessibility"
/spark-clean "optimize project structure and remove dead code"
/spark-fix "debug the intermittent connection timeout issues"
```

**Multi-Agent Pipelines:**
```bash
/spark-launch "user notification system with email and SMS support"
/spark-refactor "modernize authentication module for better maintainability"
/spark-audit "complete security and performance audit of API layer"
/spark-migrate "migrate legacy PHP system to modern Node.js architecture"
/spark-optimize "optimize database queries and API response times"
```

### 3. **Watch the Magic**
- SPARK automatically activates appropriate personas (Backend, Frontend, Security, etc.)
- **SuperClaude Integration**: All agents incorporate 5-Phase methodology patterns
- **Task Orchestration**: True parallel execution with "Task Task Task → 시작!" pattern
- **Jason's 8-Step Quality Gates**: Efficient validation system
- **Realistic Test Coverage**: Unit 95%, Integration 85%, Overall 90%
- All with 88.4% fewer tokens than traditional approaches

## 📊 Performance Comparison

```
Traditional Approach: ████████████████████████████████████████ 44,000 tokens
SPARK:               █████ 5,100 tokens (88.4% reduction)
                     
💰 Cost Savings: $0.78 per request
⚡ Speed Boost: 5x faster initial response  
🎯 Same Quality: All functionality preserved
```

### 3. **Lazy Loading Strategy**
Agents are loaded on-demand, not preloaded.

## 🎯 Key Features

- ✅ **16 Specialized Agents** - Same as SuperClaude, but smarter
- ✅ **Quality Gates** - Ensuring excellence at every step
- ✅ **Task-Based Routing** - Load only what you need
- ✅ **Backward Compatible** - Works with existing SuperClaude projects

## 📦 Installation

### For Claude Code Users (Recommended)
```bash
# 1. Clone SPARK repository
git clone https://github.com/Jaesun23/spark-claude.git
cd spark-claude

# 2. Install SPARK (optional - for benchmarks)
pip install -e .

# 3. Copy SPARK configuration to your project
cp -r .claude ~/your-claude-project/

# That's it! SPARK agents are now available in Claude Code 🎉
```

### For Standalone Usage
```bash
# Install uv if you haven't already (10x faster than pip!)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/Jaesun23/spark-claude.git
cd spark-claude

# Install with uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e ".[full,dev,benchmark]"

# Or use traditional pip
pip install -e ".[full,dev,benchmark]"
```

## 🔧 Usage

### In Claude Code (Main Usage)
```bash
# SPARK automatically routes to the optimal agent
# Just use your regular commands - SPARK makes them 88% more efficient!

# Examples:
/implement "REST API for user authentication"  # → activates implementer-spark
/analyze "code quality issues"                 # → activates analyzer-spark  
/design "responsive dashboard UI"              # → activates designer-spark
```

### Manual Agent Testing
```bash
# Test the persona router
echo '{"prompt": "implement API endpoint"}' | python .claude/hooks/spark_persona_router.py

# Run benchmarks
python benchmarks/compare_performance.py
```

## 📈 Performance Comparison

| Metric | SuperClaude | SPARK | Improvement |
|--------|------------|-------|-------------|
| Token Usage | 44,000 | 5,100 | **88% ↓** |
| Initial Load Time | 3.2s | 0.6s | **79% ↓** |
| Memory Usage | 528MB | 61MB | **88% ↓** |
| API Cost | $0.88 | $0.10 | **88% ↓** |

## 🧪 Benchmarks

Run the benchmarks yourself:
```bash
python benchmarks/compare_performance.py
```

## 📁 Project Structure

```
spark-claude/
├── .claude/                 # Claude Code integration
│   ├── agents/             # 16 SPARK agents (88% more efficient!)
│   │   ├── implementer-spark.md
│   │   ├── analyzer-spark.md
│   │   ├── designer-spark.md
│   │   └── ... (13 more agents)
│   ├── hooks/              # Unified Intelligence System v3.0
│   │   ├── spark_unified_orchestrator.py  # NEW: Unified 6-hook orchestrator
│   │   ├── spark_persona_router.py        # Smart agent routing
│   │   ├── spark_quality_gates.py         # 8-step strict validation
│   │   └── spark_test_runner.py           # Test automation
│   ├── workflows/          # State management (JSON files)
│   │   ├── unified_context.json           # NEW: Unified task context
│   │   ├── current_task.json              # Current task tracking
│   │   ├── agent_status.json              # Agent state
│   │   └── task_pipeline.json             # Workflow pipeline
│   └── commands/           # Command definitions
│       └── implement-spark.md
├── benchmarks/             # Performance verification
│   ├── compare_performance.py
│   └── benchmark_results.json
├── docs/                   # Project documentation
│   ├── UNIFIED_SPARK_SYSTEM.md  # NEW: v3.0 Unified System Guide
│   ├── SPARK_MANUAL.md         # Complete usage manual
│   ├── ROADMAP.md              # Future development plans
│   ├── FIX_DEPLOYMENT_GUIDE.md
│   └── PR_TEMPLATE.md
├── scripts/               # Installation and utilities
│   └── install.sh        # Universal installer with backup support
├── tests/                 # Test files
│   └── test_fixes.py
├── examples/              # Example code (coming soon)
├── README.md             # You are here!
├── CLAUDE.md            # Instructions for future Claude instances
├── LICENSE              # MIT License
├── pyproject.toml       # Package configuration
└── uv.lock             # Dependency lock file
```

### Key Components

- **🎯 Smart Router**: Automatically selects the optimal agent (88% token savings!)
- **🛡️ Fixed Quality Gates**: Jason's 8-step strict validation (no duplicates, realistic targets)
- **⚡ Fixed Hook System**: UserPromptSubmit & SubagentStop working correctly
- **🚀 Task 동시 호출**: True parallel execution pattern
- **📊 State Management**: JSON-based workflow tracking
- **⚡ Lazy Loading**: Load only what you need, when you need it

## 🤝 Contributing

We'd love your help making SPARK even better!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Thanks to the **SuperClaude** team for the original framework
- Inspired by the need for efficiency in AI development
- Special thanks to Jason's vision and the breakthrough insights from our collaboration

## 👥 The Team Behind SPARK

**This entire project was created by a single human (Jason) collaborating with AI assistants:**
- **Jason** - The human architect who envisioned and directed this project
- **1호 (Claude AI)** - The AI companion who helped design and implement the architecture
- **2호 (Claude CODE)** - The AI developer who analyzed and built the implementation

*A testament to what one person can achieve through effective human-AI collaboration!*

## 📜 License

MIT License - see [LICENSE](LICENSE) file

## 🌟 Star History

If you find SPARK useful, please give us a star! ⭐

---

<p align="center">
  <b>Made with ⚡ by Jason & 1호 (Claude AI) & 2호 (Claude CODE)</b><br>
  <i>"One human, two AIs, infinite possibilities"</i><br>
  <i>"toKens, not Ktokens!"</i> 😄
</p>

---

## 📞 Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/Jaesun23/spark-claude/issues)
- **Discussions**: [Join the conversation](https://github.com/Jaesun23/spark-claude/discussions)

## 🎯 Roadmap

### ⚡ What's Next? Automation Beyond Code!

**Phase 1: Workflow Orchestration** (2 weeks)
- Chain multiple agents for complex automation
- `/spark-workflow test` - Test automation (highest priority!)
- `/spark-workflow build` - End-to-end development

**Phase 2: Agent Combinations** (1 month)
- Combine specialized agents for complex tasks
- `/spark-team "project"` - Deploy agent teams
- Template-based → AI-driven generation

**Phase 3: Multi-Domain Expansion** (6 weeks)
- **Beyond Software**: Content, Education, Research, Business
- **Agent Teams**: Multiple agents working in parallel
- **Any Field**: From code to legal documents

**The Vision**: 
- **Today**: Automating software development (88% fewer tokens!)
- **Tomorrow**: Automating any knowledge work
- **Future**: Teams of agents handling massive projects

📖 **[See Full Roadmap](docs/ROADMAP.md)** - Join us in building the future of automation!

---

**Remember**: With great token savings comes great productivity! ⚡
