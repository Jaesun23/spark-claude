# 📘 Anthropic Claude Code Guidelines - Core Summary

> **Essential Guidelines for Claude Code Hooks, Slash Commands, and Subagents Implementation**
> 
> *This document is based on official Anthropic documentation and must be strictly followed when implementing all SPARK system components.*

## 🎯 Purpose
- Ensure Anthropic standards compliance when implementing Hooks, Slash Commands, and Subagents
- Prevent errors from using non-existent features
- Guarantee correct JSON format and Exit Code usage
- Apply security best practices

---

## 📌 Hook System Core Guidelines

### ✅ Existing Hook Events (Only 8 Available)
```json
{
  "hooks": {
    "PreToolUse": [...],        // Before tool execution
    "PostToolUse": [...],       // After tool execution  
    "UserPromptSubmit": [...],  // When user submits prompt
    "Stop": [...],              // Just before Claude response completion
    "SubagentStop": [...],      // Just before subagent response completion
    "PreCompact": [...],        // Before conversation compression
    "SessionStart": [...],      // When session starts/resumes
    "Notification": [...]       // When sending notifications
  }
}
```

### ❌ Non-Existent Hook Events (NEVER USE)
- `subagentStart` ❌
- `toolUse` ❌ 
- `userPromptComplete` ❌
- `assistantResponse` ❌
- `lifecycleStart` ❌
- `taskComplete` ❌

### 🏗️ Correct Hook Structure
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",  // Only for PreToolUse, PostToolUse, PreCompact
        "description": "Hook description",  // Optional
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script1.py",
            "timeout": 60  // Optional, defaults to 60 seconds
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script2.py"
            // Multiple commands allowed in same hook
          }
        ]
      },
      {
        "description": "Additional validation layer",  // Multiple hooks per event allowed
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script3.py"
          }
        ]
      }
    ]
  }
}
```

### 📊 Hook Exit Code Behavior
| Exit Code | Behavior |
|-----------|----------|
| **0** | Success. stdout shown in transcript mode (UserPromptSubmit, SessionStart add to context) |
| **2** | Block. stderr passed to Claude for automatic handling |
| **Other** | Non-blocking error. stderr shown to user only, continues execution |

### 🔧 Exit Code 2 Behavior by Hook
| Hook Event | Exit Code 2 Behavior |
|------------|----------------------|
| `PreToolUse` | Blocks tool call, shows stderr to Claude |
| `PostToolUse` | Shows stderr to Claude (tool already executed) |
| `UserPromptSubmit` | Blocks prompt processing, deletes prompt, shows stderr to user only |
| `Stop` | Blocks stopping, shows stderr to Claude |
| `SubagentStop` | Blocks stopping, shows stderr to subagent |
| `PreCompact` | Blocks compression |
| `SessionStart` | No effect, shows stderr to user only |
| `Notification` | No effect, shows stderr to user only |

### 📋 Advanced JSON Output Format

#### Common JSON Fields
```json
{
  "continue": true,           // Whether Claude should continue (default: true)
  "stopReason": "string",     // Shown to user when continue is false
  "suppressOutput": true      // Hide stdout from transcript (default: false)
}
```

#### PreToolUse Specific Fields
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "Reason for decision (shown to user)"
  }
}
```

#### UserPromptSubmit Specific Fields
```json
{
  "decision": "block" | undefined,
  "reason": "Reason for blocking",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit", 
    "additionalContext": "Context to add"
  }
}
```

#### PostToolUse Specific Fields
```json
{
  "decision": "block" | undefined,
  "reason": "Reason for blocking (passed to Claude)"
}
```

#### Stop Specific Fields
```json
{
  "decision": "block" | undefined,
  "reason": "Reason why should continue (required)"
}
```

#### SubagentStop Specific Fields
```json
{
  "decision": "block" | undefined,
  "reason": "Reason why should continue (required)"
}
```

#### SessionStart Specific Fields
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context to add on session start"
  }
}
```

#### PreCompact Specific Fields
```json
{
  // PreCompact has no special JSON output
  // Control only via exit code (0=success, 2=block, other=error)
}
```

#### Notification Specific Fields
```json
{
  // Notification has no special JSON output
  // Control only via exit code (0=success, other=error)
}
```

### 📥 Hook Input JSON Structure

#### Common Input Fields
```json
{
  "session_id": "string",
  "transcript_path": "string",  // Conversation JSON path
  "cwd": "string",             // Working directory when hook executes
  "hook_event_name": "string"
}
```

#### PreToolUse Input
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../conversation.jsonl",
  "cwd": "/Users/.../project",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

#### PostToolUse Input
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../conversation.jsonl", 
  "cwd": "/Users/.../project",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

#### UserPromptSubmit Input
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../conversation.jsonl",
  "cwd": "/Users/.../project", 
  "hook_event_name": "UserPromptSubmit",
  "prompt": "User input prompt content"
}
```

#### Stop/SubagentStop Input
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../conversation.jsonl",
  "hook_event_name": "Stop", // or "SubagentStop"
  "stop_hook_active": true  // Whether Stop Hook is already running
}
```

#### SessionStart Input
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../conversation.jsonl",
  "hook_event_name": "SessionStart",
  "source": "startup" | "resume" | "clear"
}
```

#### PreCompact Input
```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../conversation.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "manual" | "auto",
  "custom_instructions": "User-specified compression instructions"
}
```

#### Notification Input
```json
{
  "session_id": "abc123", 
  "transcript_path": "/Users/.../.claude/projects/.../conversation.jsonl",
  "cwd": "/Users/.../project",
  "hook_event_name": "Notification",
  "message": "Notification message content"
}
```

---

## 🚀 Slash Commands Core Guidelines

### 📁 File Location and Priority
1. **Project commands**: `.claude/commands/` (high priority)
2. **User commands**: `~/.claude/commands/` (low priority)

### 📝 Correct File Structure
```markdown
---
allowed-tools: Tool1, Tool2, Tool3
argument-hint: [arg1] [arg2]
description: Command description
model: sonnet
---

# Command content

$ARGUMENTS placeholder can be used

## Bash Command Execution (optional)
- Current status: !`git status`
- File contents: @src/file.js
```

### 🔑 Frontmatter Fields
| Field | Required | Description |
|-------|----------|-------------|
| `allowed-tools` | No | List of allowed tools (inherits if empty) |
| `argument-hint` | No | Argument hints for autocomplete |
| `description` | No | Command description (uses first line if empty) |
| `model` | No | Model to use (inherits if empty) |

### ⚠️ Important Rules
- **Filename = Command name**: `optimize.md` → `/optimize`
- **Namespacing**: `frontend/component.md` → `/frontend:component`
- **Argument passing**: Use `$ARGUMENTS` placeholder
- **Bash execution**: `!` prefix to execute commands (needs Bash in allowed-tools)
- **File reference**: `@` prefix to include file contents

---

## 🤖 Subagents Core Guidelines

### 📁 File Location and Priority
1. **Project subagents**: `.claude/agents/` (high priority)
2. **User subagents**: `~/.claude/agents/` (low priority)

### 📝 Correct YAML Frontmatter
```markdown
---
name: agent-name-in-kebab-case
description: Explain when this agent should be used
tools: Tool1, Tool2, Tool3  # Optional - inherits all tools if empty
---

The agent's system prompt is written here.
Clearly define roles, capabilities, and problem-solving approach.

Include specific instructions, best practices, and constraints.
```

### 📋 Required Fields
| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Unique identifier in lowercase-kebab-case |
| `description` | ✅ | Purpose and usage timing description |
| `tools` | ❌ | Specific tools only (inherits all if empty) |

### 🎯 Description Writing Tips
- **Be specific**: "Code review expert" ❌ → "PROACTIVELY review quality, security, maintainability after code writing/modification" ✅
- **State usage timing**: "Use PROACTIVELY when...", "MUST BE USED for..."
- **Include keywords**: Include relevant keywords for automatic delegation

### 🛠️ Tool Permission Settings
```yaml
# Inherit all tools (recommended)
tools: # Omit field

# Allow specific tools only
tools: Read, Edit, Bash, Grep

# MCP tools included (automatically inherited)
# MCP tools auto-included when tools field is omitted

# ❌ NEVER include Task tool (subagents cannot call other subagents)
# tools: Read, Task  # Don't do this!
```

### ⚠️ **Important: Subagent Tool Usage Restrictions**
```yaml
Core Principle:
  - Subagents can only use tools defined in frontmatter
  - Undefined tools are "not even considered for use"
  - Task tool must NEVER be included in frontmatter
  
Example:
  tools: Read, Edit, Bash  # Only these 3 can be used
  → Write tool won't be used (not defined)
  → Including Task tool causes errors (subagents cannot call other subagents)
```

### 🔄 **Important Subagent Execution Principles**

#### ⚠️ Main Agent Suspension State
```
When main agent calls subagent:
┌─────────────────┐
│ Main Agent      │ ─── Calls subagent
│ (Suspended 🛑)  │     ↓
└─────────────────┘   ┌─────────────────┐
                      │ Subagent        │ ← Active state ▶️
                      │ (Working)       │
                      └─────────────────┘
```

**Core Rules**:
- **Main agent suspends immediately upon subagent call** 🛑
- **Only subagent performs work in active state** ▶️
- **Control returns to main agent after subagent completion** 🔄
- **No concurrent execution**: Only one agent active at a time

#### 📝 Correct Subagent Delegation Pattern
```bash
# ✅ Correct pattern
"I'll use the Task tool to delegate this to implementer-spark"
→ Main agent suspends, implementer-spark activates

# ❌ Incorrect pattern  
"I'll help implement this myself while also using implementer-spark"
→ Impossible! Main agent becomes suspended
```

#### 🎯 Delegation Considerations
1. **Complete context transfer**: Enable subagent to work independently
2. **Clear work scope**: Specify exactly what subagent should do
3. **Provide all necessary information**: No communication possible with main agent
4. **Result handling plan**: Plan how to handle results after subagent completion

### ⚡ **Concurrent Tool Calls and Parallel Processing**

#### 🚀 Concurrent Tool Call Principles
```yaml
Claude Code:
  - Supports parallel tool calls: Multiple tools in single response
  - Independent tasks execute simultaneously: I/O wait time optimization
  
⚠️ Important: Must be "truly concurrent" calls (all tools in single response)!
```

#### 📋 Correct Concurrent Call Pattern
```xml
<!-- ✅ Correct concurrent calls (all in single response) -->
<function_calls>
<invoke name="Read">
<parameter name="file_path">file1.py</parameter>
</invoke>
<invoke name="Read">
<parameter name="file_path">file2.py</parameter>
</invoke>
<invoke name="Grep">
<parameter name="pattern">function</parameter>
</invoke>
<invoke name="Bash">
<parameter name="command">git status</parameter>
</invoke>
</function_calls>

<!-- ❌ Wrong sequential calls (split across multiple responses) -->
First response:
<function_calls>
<invoke name="Read">
<parameter name="file_path">file1.py</parameter>
</invoke>
</function_calls>

Second response:
<function_calls>
<invoke name="Read">
<parameter name="file_path">file2.py</parameter>
</invoke>
</function_calls>
```

#### 🚀 Parallel Processing Benefits
```yaml
Claude Code Parallel Processing Benefits:
  - Concurrent execution of independent tasks
  - Parallel git commands, file reading, searches
  - I/O wait time optimization for performance improvement
  - Significant time savings vs sequential processing
```

#### 💡 Concurrent Call Optimization Tips
```python
# ✅ Bundle independent tasks for concurrent calls
Parallelizable tasks:
  - Multiple file reads (Read)
  - Multiple directory searches (Grep, Glob)
  - Independent bash commands
  - Git status check operations

# ❌ Sequential processing for dependent tasks
Sequential processing needed:
  - File read → edit → save
  - git add → git commit → git push
  - Test execution → result analysis → report generation
```

#### 🎯 SPARK Agent Optimization Patterns
```yaml
Implementer-Spark:
  - Analysis phase: Read + Grep + Glob parallel calls
  - Implementation phase: Simultaneous editing of independent files
  - Validation phase: Test + lint + type check parallel execution

Analyzer-Spark:
  - Multi-file simultaneous analysis
  - Multiple search pattern parallel execution
  - Concurrent metrics collection

Tester-Spark:
  - Multiple test file simultaneous creation
  - Parallel test execution
  - Coverage + lint + security check concurrent execution
```

---

## 🔒 Security Best Practices

### ✅ Mandatory Compliance
- **Use absolute paths**: `~/scripts/check.sh` ✅, `check.sh` ❌
- **No sudo usage**: Hooks run with user permissions only
- **Watch sensitive file patterns**: `.env`, `.ssh/*`, `secrets.*` etc.
- **Validate input paths**: Reject `../` paths, verify expected formats
- **Quote variables**: Use `"$VAR"` to prevent injection
- **Maintain error checking**: Avoid `set +e`

### 🚫 Dangerous Patterns (Must Block)
```python
# Example of dangerous command blocking in hooks
dangerous_patterns = [
    'rm -rf /', 'dd if=', ':(){ :|:& };:',
    '> /dev/sda', 'mkfs.', 'format ',
    '; rm ', '&& rm ', '| rm ',
    'eval(', 'exec(', '__import__',
    'curl ... | sh', '| bash'
]
```

### 🛡️ Safe Hook Writing Template
```python
#!/usr/bin/env python3
import json
import sys
import os

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # Input validation
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        
        # Business logic processing
        result = process_hook(input_data)
        
        # JSON output (optional)
        if result:
            print(json.dumps(result))
        
        sys.exit(0)
        
    except Exception as e:
        # Error handling
        print(f"Hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 📊 SPARK System Application Principles

### 🎯 Hook Usage Guidelines
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "description": "SPARK Persona Router - Task routing and persona activation",
        "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/spark_persona_router.py"}]
      }
    ],
    "SubagentStop": [
      {
        "description": "SPARK Quality Gates - Multi-point validation with retry",
        "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/spark_quality_gates.py"}]
      }
    ]
  }
}
```

### 🚀 Command Structure Principles
- **Clear phase definition**: Phase 1, Phase 2, Phase 3...
- **Specify progression conditions**: "Phase X → Phase Y progression conditions"
- **Confirm hook signals**: "SubagentStop hook returns 'continue' signal"
- **Define failure conditions**: Clear criteria for retry vs termination

### 🤖 Subagent Design Principles
- **Single responsibility**: Handle one clear role only
- **Detailed prompts**: Include specific instructions and examples
- **Minimize tool permissions**: Allow only necessary tools
- **Version control**: Include project subagents in Git
- **Ensure independence**: Provide complete context (no main agent communication)
- **Clear completion criteria**: Define clearly when work is completed

---

## 🚨 Absolute Prohibitions

### ❌ Hook Related
- Using non-existent hook events
- Calling same script from all hooks
- Ignoring exit code meanings
- JSON format errors

### ❌ Commands Related
- Direct Task tool call instructions
- Multi-phase commands without progression conditions
- Frontmatter field typos
- Bash execution without security validation
- Commands requiring arguments without $ARGUMENTS

### ❌ Subagents Related
- Missing required fields (name, description)
- Vague descriptions
- Excessive permission grants
- YAML syntax errors
- Assuming concurrent execution with main agent
- Including Task tool in frontmatter (subagents cannot call other subagents)
- Expecting to use tools not defined in frontmatter
- Mismatch between tools field and actual tool usage

---

## 📚 References

### Official Documentation
- [Hook Guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)
- [Hooks Reference](https://docs.anthropic.com/en/docs/claude-code/hooks-reference)
- [Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Subagents](https://docs.anthropic.com/en/docs/claude-code/subagents)

### Environment Variables
- `$CLAUDE_PROJECT_DIR`: Project root directory absolute path

### Debugging
```bash
# Check detailed hook execution information
claude --debug

# Check hook status  
/hooks

# Validate configuration
/config
```

---

## ✅ Checklist

### Hook Implementation
- [ ] Use only existing Hook events (8 types: PreToolUse, PostToolUse, UserPromptSubmit, Stop, SubagentStop, PreCompact, SessionStart, Notification)
- [ ] Apply correct JSON structure
- [ ] Follow exit code meanings (0=success, 2=block, other=non-blocking error)
- [ ] Include security validation (absolute paths, input validation)
- [ ] Implement error handling (try-catch, stderr usage)
- [ ] Utilize $CLAUDE_PROJECT_DIR environment variable

### Command Implementation
- [ ] Use correct Frontmatter (allowed-tools, argument-hint, description, model)
- [ ] Specify progression conditions (for multi-phase)
- [ ] Correctly use $ARGUMENTS
- [ ] Consider security (quote variables in Bash, block dangerous commands)
- [ ] Properly utilize namespacing

### Subagent Implementation
- [ ] Include all required fields (name, description)
- [ ] Write specific descriptions (specify when to use)
- [ ] Set appropriate tool permissions (principle of least privilege)
- [ ] Write detailed system prompts (roles, capabilities, constraints)
- [ ] Provide complete context for independent execution
- [ ] Absolutely prohibit Task tool inclusion (exclude from frontmatter tools field)
- [ ] Recognize only defined tools are usable (undefined tools in frontmatter are unusable)
- [ ] Confirm all tools are inherited when tools field is omitted

---

*Follow these guidelines to build stable and efficient SPARK systems.*