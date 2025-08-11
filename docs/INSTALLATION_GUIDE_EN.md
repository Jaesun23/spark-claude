# SPARK Installation Guide

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

This makes SPARK available in all your projects.

---

## 🎯 Installation Options

### 1. Global Installation (~/.claude/)

**Advantages:**
- SPARK available in all projects
- Install once, use everywhere
- Centralized updates

**Disadvantages:**
- Difficult to customize per project
- Potential conflicts with other global agents

**Selection Scenario:**
```
=== Choose Installation Location ===
1) Global installation (~/.claude/)  ← Select this
```

### 2. Project-Specific Installation

**Advantages:**
- Independent configuration per project
- Version control friendly
- Easy team sharing

**Disadvantages:**
- Installation needed for each project
- Duplicate disk space usage

**Selection Scenario:**
```
=== Choose Installation Location ===
2) Project-specific installation (project/.claude/)  ← Select this
Enter project directory path: /Users/jason/my-project
```

### 3. Current Project Installation (./.claude/)

**Purpose:**
- Install directly in current directory
- Overwrite existing SPARK configuration
- Primarily for SPARK development and testing

**Use Case:**
- SPARK developers testing changes
- Temporary installations

---

## 🔧 Component Selection

### Available Components

#### 1. SPARK Agents (16 agents)
- 16 specialized agent files
- Callable via Task tool
- Essential component

#### 2. Single Agent Commands
- `/spark-implement`, `/spark-test`, etc.
- Direct shortcuts for each agent
- Namespace support (prevents conflicts)

#### 3. Multi-Agent Pipelines
- `/spark-launch` - 5 agent sequence
- `/spark-optimize` - Performance optimization pipeline
- **Hooks and workflows automatically included**

#### 4. Hook Scripts
- Persona router
- Quality gates
- Required for multi-agent pipelines

#### 5. Workflow Configuration
- Task state management
- Inter-agent context sharing

### Selection Example

```
=== Select Installation Components ===

1) Install SPARK agents (16 agents)? (Y/n): y
✓ Agent installation scheduled

2) Install single agent commands? (Y/n): y
✓ Command installation scheduled

3) Install multi-agent pipelines? (requires hooks) (Y/n): y
✓ Multi-agent pipeline installation scheduled
✓ Hooks and workflows automatically included
```

---

## ⚙️ Post-Installation Setup

### 1. Restart Claude Code

You must restart Claude Code after installation to load new configurations.

### 2. Verify Installation

```bash
# Check agents
ls ~/.claude/agents/

# Check commands
ls ~/.claude/commands/

# Check configuration
cat ~/.claude/settings.json
```

### 3. First Use

```bash
# Single agent call
/spark-implement "create user authentication"

# Multi-agent pipeline
/spark-launch "new dashboard feature"
```

---

## 🔍 Troubleshooting

### 1. Command Conflicts

**Problem:** "Command already exists" error

**Solution:**
```bash
# Use namespace during reinstallation
./scripts/install.sh
# After selecting global installation
Use namespace? (e.g., /spark:implement) (Y/n): y
Enter namespace prefix (default: spark): myproject
```

Now use as `/myproject:implement`

### 2. JSON File Not Found

**Problem:** Agents can't find `current_task.json`

**Solution:** 
v3.0 automatically checks fallback paths:
1. First check `~/.claude/workflows/`
2. If not found, check `.claude/workflows/`

Manual initialization if needed:
```bash
mkdir -p ~/.claude/workflows
echo '{}' > ~/.claude/workflows/current_task.json
echo '{}' > ~/.claude/workflows/unified_context.json
```

### 3. Hooks Not Executing

**Problem:** Multi-agent pipelines not working

**Check:**
```bash
# Verify hook configuration in settings.json
cat ~/.claude/settings.json | grep hooks

# Check hook file permissions
ls -la ~/.claude/hooks/*.py

# Grant execution permissions
chmod +x ~/.claude/hooks/*.py
```

### 4. Symbolic Link Issues

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

### Remove Global Installation

```bash
# Backup (optional)
cp -r ~/.claude ~/.claude.backup

# Remove only SPARK components
rm -rf ~/.claude/agents/*-spark.md
rm -rf ~/.claude/commands/spark-*.json
rm -rf ~/.claude/hooks/spark_*.py

# Or complete removal
rm -rf ~/.claude
```

### Remove Project-Specific Installation

```bash
cd /your/project
rm -rf .claude
```

---

## 📊 Installation Method Comparison

| Item | Global Installation | Project-Specific Installation |
|------|---------------------|-------------------------------|
| Location | ~/.claude/ | project/.claude/ |
| Scope | All projects | Specific project only |
| Hook Path | $HOME/.claude/hooks/ | $CLAUDE_PROJECT_DIR/.claude/hooks/ |
| Workflows | ~/.claude/workflows/ | project/.claude/workflows/ |
| Updates | Once only | Per project |
| Team Sharing | Difficult | Git shareable |
| Conflicts | Possible (solved with namespace) | None |

---

## 🎯 Recommended Installation Configurations

### Individual Developer
- **Global Installation** + **All Components**
- Immediately available in all projects

### Team Project
- **Project-Specific Installation** + **Selective Components**
- Share with team via Git
- Per-project customization

### SPARK Testing/Development
- **Current Project Installation**
- For development and testing

---

## 📚 Additional Documentation

- [SPARK Agents Guide](./SPARK_AGENTS_GUIDE.md)
- [Claude Code Guidelines](./CLAUDE_CODE_GUIDELINES.md)
- [Token Management](./TOKEN_AND_RESOURCE_MANAGEMENT.md)
- [Architecture Guide](./SPARK_INTEGRATED_ARCHITECTURE.md)

---

## 💬 Support

If you have issues or questions:
- GitHub Issues: [https://github.com/Jaesun23/spark-claude/issues](https://github.com/Jaesun23/spark-claude/issues)
- Documentation: [SPARK_AGENTS_GUIDE.md](./SPARK_AGENTS_GUIDE.md)

---

*SPARK v3.5 - Advanced multi-agent system created through collaboration between Jason and AI assistants*