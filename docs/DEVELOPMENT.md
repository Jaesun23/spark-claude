# SPARK v3.8 Development Guide

Complete development reference covering hooks, guidelines, token management, and multi-team workflows for SPARK system development and customization.

## Hook System

### 5 Essential Hooks (Streamlined from 10)

**Core Hooks:**
- `spark_persona_router.py` - Agent selection logic
- `spark_phase_manager.py` - 5-Phase execution management
- `spark_quality_gates.py` - 8-step quality validation protocol
- `spark_core_utils.py` - Shared utilities and state management
- `file_lock_manager.py` - Thread-safe parallel execution

### Official Anthropic Hook Events

**Available Events (Only 8 exist):**
- `UserPromptSubmit` - When user submits prompt → Execute Persona Router
- `SubagentStop` - When subagent completes → Validate Quality Gates
- `PreToolUse` - Before tool usage → Security validation (optional)
- `PostToolUse` - After tool usage → Logging/monitoring (optional)
- `Stop` - Before Claude response completes → Final validation (optional)
- `PreCompact` - Before conversation compression → State saving (optional)
- `SessionStart` - Session starts/resumes → Context loading (optional)
- `Notification` - Sending notifications → Notification handling (optional)

**Non-Existent Events (NEVER use):**
- `subagentStart` ❌
- `toolUse` ❌
- `userPromptComplete` ❌
- `assistantResponse` ❌
- `agentStop` ❌

### Hook Configuration Structure

**.claude/settings.json:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "description": "SPARK Persona Router",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/spark_persona_router.py",
            "timeout": 60
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "description": "Quality Gates Validation",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/spark_quality_gates.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Hook Exit Codes

| Exit Code | Behavior | When to Use |
|-----------|----------|-------------|
| **0** | Success - Continue normally, stdout added to context | Normal completion |
| **2** | Block - Stop operation, stderr passed to Claude | Quality failure, retry needed |
| **Other** | Error - Continue operation, stderr shown to user only | Non-blocking warnings |

### Hook Exit Code 2 Behavior by Event

| Hook Event | Exit Code 2 Effect |
|------------|-------------------|
| `UserPromptSubmit` | Blocks prompt processing, deletes prompt, shows stderr to user only |
| `SubagentStop` | Blocks agent completion, shows stderr to subagent for retry |
| `PreToolUse` | Blocks tool execution, shows stderr to Claude |
| `PostToolUse` | Shows stderr to Claude (tool already executed) |
| `Stop` | Blocks response completion, shows stderr to Claude |
| Others | No blocking effect, shows stderr to user only |

---

## Claude Code Guidelines

### Core Standards Compliance

**Hook System Requirements:**
- Use only the 8 official Anthropic hook events
- Implement proper JSON input/output handling
- Follow timeout guidelines (default: 60 seconds)
- Use correct exit codes for flow control

**Command Structure:**
```json
{
  "name": "command-name",
  "description": "Command description",
  "instructions": "Detailed instructions for execution",
  "when": "When to use this command"
}
```

**Security Best Practices:**
- Validate all input parameters
- Sanitize file paths and commands
- Use proper error handling and logging
- Implement timeout mechanisms
- Never expose sensitive information in logs

### JSON Input/Output Standards

**Hook Input Structure:**
```json
{
  "session_id": "unique_session_identifier",
  "prompt": "user_submitted_prompt",
  "context": {
    "project_path": "/path/to/project",
    "active_files": ["file1.py", "file2.js"],
    "recent_changes": []
  }
}
```

**Hook Output Structure:**
```json
{
  "continue": true,
  "enhanced_prompt": "original_prompt_with_enhancements",
  "context_additions": {
    "complexity": 0.75,
    "personas": ["Backend", "Security"],
    "quality_gates": true
  },
  "metadata": {
    "execution_time": 1.2,
    "tokens_estimated": 15000
  }
}
```

---

## Token Management

### SPARK v3.5 Token Safety Protocol

**Pre-Task Assessment (Mandatory for all agents):**
```yaml
Phase 1 - Context Calculation:
  - Agent definition: ~10K tokens
  - User instructions: 2-5K tokens
  - Source code context: 5-15K tokens
  - Team coordination: 3-5K tokens (if applicable)

Phase 2 - Write Operation Estimation:
  - Generated content size × 2 (memory + write)
  - Multiple files: each file × 2
  - Documentation generation: high token cost

Phase 3 - Abort Criteria:
  - If estimated total > 90K tokens → ABORT
  - Log to ~/.claude/workflows/task_aborted.json
  - Recommend task splitting
```

### The 90K Practical Limit

**Mathematical Breakdown:**
```yaml
200K Context Window (Claude 3.5 Sonnet)
÷ 2 = 100K (Write tool doubling factor)
- 10K (Initial context overhead)
= 90K (Actual working capacity per agent)
```

**Token Doubling Reality:**
```yaml
Example - Creating 1000-line file:
  - Generate in memory: 15K tokens
  - Write tool output: 15K tokens (duplicate)
  - Total cost: 30K tokens for one file
```

### FileLockManager Integration Impact

**Team Coordination Overhead:**
- FileLockManager adds ~2K tokens per team agent
- Each team JSON file adds ~1K tokens to context
- 4 teams = ~12K additional token overhead
- Total v3.5 overhead: 15K tokens for multi-team coordination

**Team Agent Token Distribution:**
```yaml
200K context window ÷ 4 teams = 50K base per team
- FileLockManager overhead: 3K
- Team JSON context: 2K
- Base agent context: 10K
= 35K working capacity per team agent
```

### Compression Strategies

**When Required:** All agents must explicitly request compression
- Use standard abbreviations: API, CLI, SDK, UI, DB, etc.
- Focus on essential information, link to external resources
- Symbol/abbreviation use reduces tokens by 30-50%
- Information loss is minimal with proper compression

**High-Risk Scenarios:**
- Full API documentation (can exceed 50K with Write doubling)
- Multiple guide creation (each file doubles token consumption)
- Architecture documentation with ASCII diagrams
- Comprehensive user manuals (consider splitting into chapters)

---

## Multi-Team Parallel Development

### Multi-Implement Command

**Purpose:** 4-team parallel execution for independent tasks

**When to Use:**
- Multiple independent features (no shared dependencies)
- API endpoints that don't share models
- Separate UI components
- Independent microservices
- Different modules or packages

**When NOT to Use:**
- Interdependent features
- Tasks modifying the same files extensively
- Sequential workflows (A must complete before B)
- Single large feature that can't be split

### Command Syntax
```bash
# Basic usage
/multi-implement "User auth endpoint" "Dashboard component" "Security middleware" "Data pipeline"

# With task IDs
/multi-implement "TASK-API-01" "TASK-UI-02" "TASK-SEC-03" "TASK-DATA-04"

# 2-3 tasks also work
/multi-implement "Feature A" "Feature B"
```

### Execution Architecture
```
Claude CODE (Orchestrator)
├─ Parse tasks → Auto-generate team JSON templates
├─ FileLockManager ensures resource safety
├─ Call 4 teams SIMULTANEOUSLY (true parallelism)
├─ Wait for ALL to complete
└─ Coordinate shared resources

Team Execution:
├── team1-implementer-spark → team1_task.json
├── team2-implementer-spark → team2_task.json
├── team3-implementer-spark → team3_task.json
└── team4-implementer-spark → team4_task.json
```

### Team JSON Template System

**Auto-Generated Templates:** `~/.claude/workflows/team{1-4}_task.json`

**Template Structure:**
```json
{
  "team_id": "team1",
  "status": "ready",
  "created_at": "auto-timestamp",
  "task_details": {
    "description": "assigned_task_description",
    "complexity": 0.5,
    "estimated_time": "15-30 minutes"
  },
  "implementation": {
    "target_files": ["auth.py", "models.py"],
    "dependencies": [],
    "testing_required": true
  },
  "file_locks": {
    "requested": [],
    "acquired": [],
    "timeout": 300
  }
}
```

### Parallel Execution Phases

**Phase 1: Initialization**
- Parse command and extract tasks
- Validate task independence
- Create team JSON files with task details
- Identify potential resource conflicts

**Phase 2: Parallel Implementation**
```python
# ALL CALLS AT ONCE - TRUE PARALLELISM
Task("team1-implementer-spark", task1_with_json)
Task("team2-implementer-spark", task2_with_json)
Task("team3-implementer-spark", task3_with_json)
Task("team4-implementer-spark", task4_with_json)
# WAIT for ALL teams to complete
```

**Phase 3: Parallel Testing**
```python
# After implementation, test in parallel
Task("team1-tester-spark", test1)
Task("team2-tester-spark", test2)
Task("team3-tester-spark", test3)
Task("team4-tester-spark", test4)
# WAIT for ALL tests to complete
```

**Phase 4: Consolidation**
- Claude CODE reviews all team results
- Generates unified report
- Handles any integration needs

---

## Quality Gates (8-Step Protocol)

**Jason's Quality Requirements (All must pass):**

1. **Syntax Validation** → 0 errors required
2. **Type Checking** → `mypy --strict` (0 errors required)
3. **Linting** → `ruff --strict` (0 violations required)
4. **Security Analysis** → OWASP compliance + secrets scan
5. **Test Coverage** → Unit 95%, Integration 85%
6. **Performance Check** → O(n) complexity preferred, no N+1 queries
7. **Documentation** → Required docstrings and inline comments
8. **Integration Testing** → End-to-end scenario validation

### Quality Gate Implementation

**Validation Commands:**
```bash
# Type checking
mypy [file.py] --strict

# Linting
ruff check [file.py] --strict

# Test coverage
pytest tests/ --cov=src --cov-report=term-missing

# Security scan
bandit -r src/
```

**Automatic Retry Logic:**
- Failed quality gates trigger automatic retry (max 3 attempts)
- Each retry includes specific guidance about failed checks
- Final failure blocks completion and requires manual intervention

---

## Development Workflow

### Single Agent Development
```python
# Simple task (complexity < 0.3)
# Claude CODE handles directly, no agent needed

# Standard task (0.3-0.7)
Task("implementer-spark", "implement JWT authentication")
# Quality gates validate automatically
# Results stored in JSON for next phase

# Complex task (≥ 0.7)
# Multiple agents in sequence or parallel
```

### Multi-Agent Pipeline Development
```python
# Sequential pipeline
result1 = Task("analyzer-spark", "analyze system requirements")
result2 = Task("implementer-spark", f"implement based on {result1}")
result3 = Task("tester-spark", f"test implementation {result2}")

# Parallel pipeline
Task("team1-implementer-spark", "backend API")
Task("team2-implementer-spark", "frontend components")
Task("team3-implementer-spark", "database schema")
Task("team4-implementer-spark", "authentication service")
# All complete before proceeding to integration
```

### Error Handling and Recovery

**Common Issues:**
- Token limit exceeded → Split into smaller tasks
- Quality gates failed → Review specific failures, retry with fixes
- File conflicts in parallel execution → FileLockManager handles automatically
- Agent timeout → Increase complexity estimate, retry with more context

**Debugging Tools:**
```bash
# Check JSON state files
cat ~/.claude/workflows/current_task.json

# Review quality gate logs
tail -f ~/.claude/logs/quality_gates.log

# Monitor FileLockManager status
cat ~/.claude/workflows/file_locks.json
```

---

## Best Practices

### DO's ✅
1. **Follow 8-step quality gates** - No exceptions, they prevent technical debt
2. **Use appropriate complexity estimates** - Triggers correct persona activation
3. **Leverage parallel execution** - For independent tasks only
4. **Trust FileLockManager** - Handles resource conflicts automatically
5. **Provide detailed context** - Reduces token usage through fewer clarifications
6. **Use JSON state files** - Maintains context between agents
7. **Implement proper error handling** - Graceful failure and recovery

### DON'Ts ❌
1. **Don't bypass quality gates** - Leads to technical debt accumulation
2. **Don't use parallel execution for dependent tasks** - Causes integration issues
3. **Don't ignore token limits** - Results in hard termination at 200K
4. **Don't skip testing phases** - Quality over speed
5. **Don't modify team coordination files manually** - Let hooks handle it
6. **Don't use non-existent hook events** - Follow official Anthropic documentation
7. **Don't exceed 90K token estimate** - Abort and split tasks instead

### Performance Optimization
- Use specific agents for specific tasks (avoid generic approaches)
- Provide clear, detailed context upfront to prevent clarification loops
- Leverage lazy-loading architecture (only loads required agents)
- Use compression when explicitly needed to reduce token consumption
- Monitor token usage and split large tasks proactively

### Security Considerations
- Validate all user inputs in hooks
- Sanitize file paths and command parameters
- Use proper timeout mechanisms to prevent hanging processes
- Never log or expose sensitive information
- Follow principle of least privilege for file access

---

## Advanced Development

### Custom Hook Development

**Hook Template:**
```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def main():
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Process input
        result = process_hook(input_data)
        
        # Output result
        print(json.dumps(result))
        sys.exit(0)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def process_hook(data):
    # Custom hook logic here
    return {
        "continue": True,
        "enhanced_prompt": data.get("prompt", ""),
        "context_additions": {}
    }

if __name__ == "__main__":
    main()
```

### Custom Agent Development

**Agent Definition Template:**
```markdown
---
name: custom-agent-spark
tools: Read, Write, Edit, Bash, TodoWrite
---

You are custom-agent-spark, specialized in [SPECIFIC PURPOSE].

## MANDATORY INITIALIZATION
Before ANY work, you MUST:
1. Read `.claude/workflows/current_task.json` for task context
2. Check previous results from relevant JSON files
3. Understand project requirements and standards

## WORK INSTRUCTIONS
[Specific instructions for this agent]

## MANDATORY OUTPUT
After completing work, you MUST:
1. Write results to appropriate JSON file
2. Update TodoWrite with completion status
3. Pass context to next agent if needed
```

### Testing and Validation

**Hook Testing:**
```bash
# Test hook with sample input
echo '{"prompt": "test prompt", "session_id": "test"}' | python3 hook_script.py

# Validate hook output format
python3 -c "import json; json.loads(open('output.json').read())"
```

**Agent Testing:**
```bash
# Test agent in isolation
echo '{"task": "test implementation"}' > ~/.claude/workflows/current_task.json
# Run agent and verify output
```

---

This development guide covers all essential aspects of SPARK v3.5 development, from basic hook implementation to advanced multi-team coordination. For specific agent usage, see [AGENTS.md](./AGENTS.md), and for system architecture details, see [ARCHITECTURE.md](./ARCHITECTURE.md).