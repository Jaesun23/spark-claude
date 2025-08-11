# SPARK v3.5 Installation Guide

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Installation Options](#installation-options)
3. [Component Selection](#component-selection)
4. [Post-Installation Setup](#post-installation-setup)
5. [Troubleshooting](#troubleshooting)
6. [Uninstallation](#uninstallation)

---

## 🚀 Quick Start

### Basic Installation (Global)

```bash
# 1. Clone SPARK repository
git clone https://github.com/Jaesun23/spark-claude.git
cd spark-claude

# 2. Run installation script
./scripts/install.sh

# 3. Restart Claude Code
```

This enables SPARK across all your projects.

---

## 🎯 Installation Options

### 1. Global Installation (~/.claude/)

**Advantages:**
- SPARK available in all projects
- One-time installation
- Centralized updates

**Disadvantages:**
- Limited per-project customization
- Potential conflicts with other global agents

**Selection scenario:**
```
=== Installation Location ===
1) Global installation (~/.claude/)  ← Choose this
```

### 2. Project-Specific Installation

**Advantages:**
- Independent project settings
- Version control friendly
- Easy team sharing

**Disadvantages:**
- Installation needed per project
- Duplicate disk space usage

**Selection scenario:**
```
=== Installation Location ===
2) Project-specific installation (project/.claude/)  ← Choose this
Project directory path: /Users/jason/my-project
```

### 3. Current Project Installation (./.claude/)

**Purpose:**
- Direct installation in current directory
- Overwrites existing SPARK settings
- Primarily for SPARK development and testing

**Use cases:**
- SPARK developer testing changes
- Temporary installation

---

## 🔧 Component Selection

### Available Components

#### 1. SPARK Agents (28 total)
- **16 Base agents**: Core functionality agents
- **12 Team agents**: Multi-team parallel execution (team1-4)
- Callable via Task tool
- Essential component

#### 2. Single Agent Commands
- `/spark-implement`, `/spark-test`, etc.
- Direct shortcuts to individual agents
- Namespace support (conflict prevention)

#### 3. Multi-Agent Pipelines
- `/spark-launch` - 5-agent sequential execution
- `/spark-optimize` - Performance optimization pipeline
- **Hooks and workflows automatically included**

#### 4. Hook Scripts (5 hooks)
- **spark_persona_router.py** - Agent selection logic
- **spark_phase_manager.py** - 5-Phase execution management  
- **spark_quality_gates.py** - Quality validation (8-step protocol)
- **spark_core_utils.py** - Shared utilities
- **file_lock_manager.py** - FileLockManager integration
- Required for multi-agent pipelines

#### 5. Workflow Settings
- Task state management
- Inter-agent context sharing
- Team JSON template system

### Selection Example

```
=== Installation Components ===

1) SPARK agents (28 total) install? (Y/n): y
✓ Agents installation planned

2) Single agent commands install? (Y/n): y
✓ Commands installation planned

3) Multi-agent pipelines install? (requires hooks) (Y/n): y
✓ Multi-agent pipelines installation planned
✓ Hooks and workflows automatically included
```

---

## ⚙️ Post-Installation Setup

### 1. Restart Claude Code

After installation, Claude Code must be restarted for new settings to load.

### 2. Installation Verification

```bash
# Check agents
ls ~/.claude/agents/

# Check commands
ls ~/.claude/commands/

# Check settings
cat ~/.claude/settings.json

# Check hooks (should be 5 files)
ls ~/.claude/hooks/
```

### 3. First Use

```bash
# Single agent call
/spark-implement "create user authentication"

# Multi-agent pipeline
/spark-launch "new dashboard feature"

# Team parallel execution
/multi-implement "API endpoint" "UI component" "Tests" "Documentation"
```

---

## 🔍 Troubleshooting

### 1. Command Conflicts

**Problem:** "Command already exists" error

**Solution:**
```bash
# Use namespace during reinstallation
./scripts/install.sh
# Choose global installation, then
Use namespace? (e.g., /spark:implement) (Y/n): y
Namespace prefix (default: spark): myproject
```

Now use `/myproject:implement` format

### 2. Missing JSON Files

**Problem:** Agents cannot find `current_task.json`

**Solution:** 
v3.5 automatically checks fallback paths:
1. First checks `~/.claude/workflows/`
2. Falls back to `.claude/workflows/`

Manual initialization if needed:
```bash
mkdir -p ~/.claude/workflows
echo '{}' > ~/.claude/workflows/current_task.json
echo '{}' > ~/.claude/workflows/unified_context.json
# Initialize team templates
echo '{"team_id": "team1", "status": "ready"}' > ~/.claude/workflows/team1_task.json
echo '{"team_id": "team2", "status": "ready"}' > ~/.claude/workflows/team2_task.json
echo '{"team_id": "team3", "status": "ready"}' > ~/.claude/workflows/team3_task.json
echo '{"team_id": "team4", "status": "ready"}' > ~/.claude/workflows/team4_task.json
```

### 3. Hooks Not Executing

**Problem:** Multi-agent pipelines not working

**Verification:**
```bash
# Check hooks in settings.json
cat ~/.claude/settings.json | grep hooks

# Check hook file permissions
ls -la ~/.claude/hooks/*.py

# Grant execution permissions
chmod +x ~/.claude/hooks/*.py

# Verify 5 hook files exist
ls ~/.claude/hooks/spark_*.py ~/.claude/hooks/file_lock_manager.py
```

### 4. FileLockManager Issues

**Problem:** Team parallel execution conflicts

**Solution:**
FileLockManager is now integrated into StateManager. Verify:
```bash
# Check if FileLockManager is properly integrated
grep -n "FileLockManager" ~/.claude/hooks/spark_core_utils.py
```

### 5. Symbolic Link Issues

**Problem:** `~/.claude` is a symbolic link

**Solution:**
Installation script automatically detects and handles this.
Manual verification:
```bash
# Check symbolic link
ls -la ~/.claude

# Check actual path
readlink ~/.claude
```

---

## 🗑️ Uninstallation

### Global Installation Removal

```bash
# Backup (optional)
cp -r ~/.claude ~/.claude.backup

# Remove SPARK components only
rm -rf ~/.claude/agents/*-spark.md
rm -rf ~/.claude/commands/spark-*.json
rm -rf ~/.claude/hooks/spark_*.py ~/.claude/hooks/file_lock_manager.py
rm -rf ~/.claude/workflows/team*_task.json

# Or complete removal
rm -rf ~/.claude
```

### Project-Specific Removal

```bash
cd /your/project
rm -rf .claude
```

---

## 📊 Installation Comparison Table

| Feature | Global Installation | Project-Specific |
|---------|-------------------|-----------------|
| Location | ~/.claude/ | project/.claude/ |
| Scope | All projects | Specific project only |
| Hook path | $HOME/.claude/hooks/ | $CLAUDE_PROJECT_DIR/.claude/hooks/ |
| Workflows | ~/.claude/workflows/ | project/.claude/workflows/ |
| Updates | Once only | Per project |
| Team sharing | Difficult | Git shareable |
| Conflict risk | Yes (namespace solution) | None |

---

## 🎯 Recommended Installation Configurations

### Individual Developer
- **Global installation** + **All components**
- Immediate availability across all projects

### Team Project
- **Project-specific installation** + **Selective components**
- Git-based team sharing
- Per-project customization

### SPARK Testing/Development
- **Current project installation**
- Development and testing purposes

---

## 🏗️ SPARK v3.5 Architecture Highlights

- **Lazy-loading agents**: Only load required agents (saves ~39K tokens)
- **FileLockManager integration**: Thread-safe parallel execution
- **5-hook system**: Streamlined from 10 hooks to 5 essential hooks
- **Team JSON templates**: Automatic generation for parallel teams
- **Token Safety Protocol**: 90K limit with pre-task assessment

---

## 📚 Additional Documentation

- [SPARK Agents Guide](./SPARK_AGENTS_GUIDE.md)
- [Multi-Implementation Guide](./MULTI_IMPLEMENT_GUIDE.md)
- [Hook System Guide](./SPARK_HOOK_GUIDE.md)
- [Token Management](./TOKEN_AND_RESOURCE_MANAGEMENT.md)

---

## 💬 Support

For issues or questions:
- GitHub Issues: [https://github.com/Jaesun23/spark-claude/issues](https://github.com/Jaesun23/spark-claude/issues)
- Documentation: [SPARK Agents Guide](./SPARK_AGENTS_GUIDE.md)

---

*SPARK v3.5 - Advanced multi-agent orchestration system with lazy-loading architecture and integrated FileLockManager*