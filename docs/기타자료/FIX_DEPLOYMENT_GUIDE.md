# SPARK System Critical Fixes - Deployment Guide

## Overview

This guide provides instructions for deploying comprehensive fixes to the SPARK multi-agent system that address all critical issues identified by analyzer-spark.

## Fixed Issues

### 1. ✅ Hook JSON Output Compliance
- **Problem**: Hooks were outputting plain text instead of JSON
- **Solution**: Implemented `HookOutputFormatter` with proper JSON schemas
- **Files**: `spark_persona_router_fixed.py`, `spark_quality_gates_fixed.py`

### 2. ✅ Secure Command Execution
- **Problem**: Using `shell=True` created security vulnerabilities
- **Solution**: Implemented `SecureCommandExecutor` with safe subprocess calls
- **Files**: `spark_core_utils.py`

### 3. ✅ State Management System
- **Problem**: No `current_task.json` implementation
- **Solution**: Implemented `StateManager` with atomic file operations
- **Files**: `spark_core_utils.py`, creates `.claude/workflows/current_task.json`

### 4. ✅ Agent Chaining Architecture
- **Problem**: Agents couldn't pass data in pipelines
- **Solution**: Implemented `AgentChainManager` and `PipelineOrchestrator`
- **Files**: `spark_pipeline_orchestrator.py`

## Installation Instructions

### Option 1: Automated Installation (Recommended)

```bash
# Make installer executable
chmod +x install_fixed.sh

# Run installer with validation
./install_fixed.sh

# The installer will:
# - Backup existing installation
# - Deploy all fixed components
# - Install Python dependencies
# - Validate the installation
# - Create test and rollback scripts
```

### Option 2: Manual Installation

```bash
# 1. Backup existing hooks
cp -r ~/.claude/hooks ~/.claude/hooks_backup_$(date +%Y%m%d)

# 2. Copy fixed components
cp spark_core_utils.py ~/.claude/hooks/
cp spark_persona_router_fixed.py ~/.claude/hooks/spark_persona_router.py
cp spark_quality_gates_fixed.py ~/.claude/hooks/spark_quality_gates.py
cp spark_pipeline_orchestrator.py ~/.claude/hooks/
cp spark_validator.py ~/.claude/hooks/

# 3. Set permissions
chmod +x ~/.claude/hooks/*.py

# 4. Install dependencies
pip3 install mypy ruff pytest bandit pip-audit
```

## Testing the Fixes

### 1. Run Comprehensive Test Suite

```bash
# Run all tests
python3 test_fixes.py

# Expected output:
# ✅ Hook JSON Compliance: PASSED
# ✅ Secure Command Execution: PASSED
# ✅ State Management: PASSED
# ✅ Agent Chaining: PASSED
# ✅ Pipeline Orchestration: PASSED
# ✅ Quality Gates Integration: PASSED
# ✅ Hook Communication: PASSED
# ✅ Error Handling: PASSED
```

### 2. Run System Health Check

```bash
# Check overall system health
python3 ~/.claude/hooks/spark_validator.py health

# Validate hooks specifically
python3 ~/.claude/hooks/spark_validator.py hooks

# Test state management
python3 ~/.claude/hooks/spark_validator.py state
```

### 3. Test Individual Components

```bash
# Test persona router (should output JSON)
echo '{"prompt": "implement REST API"}' | python3 ~/.claude/hooks/spark_persona_router.py

# Test quality gates (should output JSON)
echo '{"subagent": "test", "cwd": "."}' | python3 ~/.claude/hooks/spark_quality_gates.py

# Test pipeline orchestrator
python3 ~/.claude/hooks/spark_pipeline_orchestrator.py status
```

## Using the Fixed System

### 1. Standard Task Execution

The fixed hooks will automatically activate when using SPARK commands:

```bash
/spark "implement user authentication API"
# - Persona router outputs proper JSON with additionalContext
# - State is saved to current_task.json
# - Quality gates validate with secure execution
```

### 2. Pipeline Execution

Use pipeline orchestrator for multi-agent workflows:

```python
# Start a pipeline
python3 ~/.claude/hooks/spark_pipeline_orchestrator.py start full-stack

# Check status
python3 ~/.claude/hooks/spark_pipeline_orchestrator.py status

# Advance pipeline
python3 ~/.claude/hooks/spark_pipeline_orchestrator.py advance implementer-spark
```

### 3. State Management

State is automatically managed in `~/.claude/workflows/current_task.json`:

```json
{
  "task_id": "spark_20240108_143022",
  "personas": ["Backend Developer"],
  "agents": ["implementer-spark"],
  "complexity": 0.7,
  "quality_gates": {
    "required": 8,
    "passed": 0,
    "results": {}
  },
  "pipeline": {
    "current_agent": "implementer-spark",
    "completed_agents": [],
    "data_passing": {}
  }
}
```

## Rollback Instructions

If issues occur, rollback to previous version:

```bash
# Use automated rollback
~/.claude/hooks/rollback.sh

# Or manual rollback
cp -r ~/.claude/hooks_backup_[date]/* ~/.claude/hooks/
```

## Verification Checklist

After installation, verify:

- [ ] Hooks output valid JSON (no plain text to stdout)
- [ ] No `shell=True` in subprocess calls
- [ ] State file created at `~/.claude/workflows/current_task.json`
- [ ] Pipeline commands can pass data between agents
- [ ] Quality gates use secure command execution
- [ ] All tests pass in `test_fixes.py`
- [ ] System health check shows "healthy"

## Key Improvements

### Security Enhancements
- **Path Sanitization**: Prevents directory traversal attacks
- **Command Injection Prevention**: No shell execution
- **Input Validation**: All inputs sanitized before use

### Performance Improvements
- **Atomic State Operations**: Prevents corruption
- **Efficient Data Passing**: Direct agent-to-agent communication
- **Optimized Quality Gates**: Parallel execution where possible

### Reliability Improvements
- **Error Recovery**: Graceful handling of failures
- **State Persistence**: Survives process restarts
- **Validation Suite**: Comprehensive testing utilities

## Troubleshooting

### Issue: Hooks not outputting JSON
**Solution**: Ensure you're using the fixed versions with `_fixed` suffix or run installer

### Issue: State file not created
**Solution**: Check `~/.claude/workflows/` directory exists and has write permissions

### Issue: Pipeline data not passing
**Solution**: Verify state management is working with `spark_validator.py state`

### Issue: Quality gates failing
**Solution**: Check Python dependencies are installed (mypy, ruff, pytest, bandit)

## Support

For issues or questions:
1. Run health check: `python3 ~/.claude/hooks/spark_validator.py health`
2. Check test results: `python3 test_fixes.py`
3. Review logs in stderr (all logging goes to stderr to avoid stdout contamination)

## Version Information

- **Fix Version**: 2.0.0
- **Compatible with**: SPARK 1.0.0+
- **Python Required**: 3.8+
- **Dependencies**: mypy, ruff, pytest, bandit, pip-audit

## Summary

All critical issues have been addressed:
- ✅ JSON output compliance (Anthropic spec compliant)
- ✅ Secure command execution (no shell injection)
- ✅ State management system (persistent task state)
- ✅ Agent chaining (multi-agent pipelines)
- ✅ Comprehensive validation (testing suite)

The SPARK system is now production-ready with enterprise-grade security and reliability.