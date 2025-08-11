# 🪝 SPARK v3.5 Hook System Guide (5 Essential Hooks)

## 📋 Overview

The SPARK v3.5 Hook System has been streamlined from 10 hooks to 5 essential hooks, leveraging official Anthropic Claude Code Hook events to implement automated workflows with integrated FileLockManager support.

## 🎆 SPARK v3.5 Changes

### ❌ **Hooks Removed (Obsolete)**
- ❌ spark_pipeline_orchestrator.py
- ❌ spark_test_runner.py  
- ❌ spark_token_validator.py
- ❌ spark_unified_orchestrator.py
- ❌ spark_validator.py

### ✅ **Essential Hooks Remaining (5)**
- ✅ spark_persona_router.py
- ✅ spark_phase_manager.py
- ✅ spark_quality_gates.py
- ✅ spark_core_utils.py
- ✅ file_lock_manager.py (integrated)

### 🆕 **Key Improvements**
- **FileLockManager Integration**: Thread-safe parallel execution
- **Streamlined Architecture**: 50% reduction in hook complexity
- **Automated Team JSON**: Auto-generation of team templates
- **Enhanced Quality Gates**: Jason's 8-step protocol with retry logic

## ✅ Official Anthropic Hook Events (Only 8 Exist)

| Hook Event | Purpose | SPARK Usage |
|------------|---------|-------------|
| **UserPromptSubmit** | When user submits prompt | Execute Persona Router |
| **SubagentStop** | When subagent completes work | Validate Quality Gates |
| **PreToolUse** | Before tool usage | Security validation (optional) |
| **PostToolUse** | After tool usage | Logging/monitoring (optional) |
| **Stop** | Just before Claude response completes | Final validation (optional) |
| **PreCompact** | Before conversation compaction | State saving (optional) |
| **SessionStart** | When session starts/resumes | Context loading (optional) |
| **Notification** | When sending notifications | Notification handling (optional) |

## ⚠️ Non-Existent Hook Events (Never Use)

```python
# ❌ These events do NOT exist!
"subagentStart"      # ❌ Does not exist
"toolUse"           # ❌ Only PreToolUse/PostToolUse exist
"userPromptComplete" # ❌ Does not exist
"assistantResponse"  # ❌ Does not exist
"agentStop"         # ❌ SubagentStop is the correct name
```

## 📁 Hook Configuration File Structure

### .claude/settings.json
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
        "description": "Jason's 8-Step Quality Gates",
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

## 📊 Hook Exit Code Meanings

| Exit Code | Action | Description |
|-----------|--------|-------------|
| **0** | Success | Continue normally, add stdout to context |
| **2** | Block | Block operation, pass stderr to Claude |
| **Other** | Error | Continue operation, show stderr to user only |

## 📥 Hook Input JSON Structure

### UserPromptSubmit
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/conversation.jsonl",
  "cwd": "/project/path",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "User's input prompt"
}
```

### SubagentStop
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/conversation.jsonl",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false
}
```

## 📤 Hook Output JSON Structure

### UserPromptSubmit Output
```json
{
  "continue": true,
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Additional context information to add"
  }
}
```

### SubagentStop Output
```json
{
  "decision": "block",  // or undefined to continue
  "reason": "Quality gates failed: syntax_validation, type_checking"
}
```

## 🔧 SPARK Hook Implementation Patterns

### 1. spark_persona_router.py (UserPromptSubmit)
```python
#!/usr/bin/env python3
import json
import sys

def main():
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
        prompt = input_data.get("prompt", "")
        
        # Analyze prompt and activate personas
        personas = analyze_prompt(prompt)
        
        # Add context
        output = {
            "continue": True,
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"Activated personas: {personas}"
            }
        }
        
        print(json.dumps(output))
        sys.exit(0)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 2. spark_quality_gates.py (SubagentStop)
```python
#!/usr/bin/env python3
import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
        
        # Perform quality validation
        validation_results = run_quality_gates()
        
        if not all(validation_results.values()):
            # Block on quality gate failure
            failed_gates = [k for k, v in validation_results.items() if not v]
            output = {
                "decision": "block",
                "reason": f"Quality gates failed: {', '.join(failed_gates)}"
            }
            print(json.dumps(output))
            sys.exit(2)  # Exit code 2 to block
        
        # Success
        print(json.dumps({"continue": True}))
        sys.exit(0)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## 🔒 Security Considerations

### Required Validation
```python
def validate_command(command: str) -> bool:
    """Block dangerous commands"""
    dangerous_patterns = [
        'rm -rf /', 'dd if=', ':(){ :|:& };:',
        '> /dev/sda', 'mkfs.', 'format ',
        '; rm ', '&& rm ', '| rm ',
        'eval(', 'exec(', '__import__'
    ]
    
    command_lower = command.lower()
    return not any(pattern in command_lower for pattern in dangerous_patterns)
```

### Path Validation
```python
def validate_path(path: str) -> bool:
    """Prevent path traversal attacks"""
    return not ('..' in path or path.startswith('/'))
```

## 🔒 Agent Self-Validation System (New!)

### Overview
A two-tier validation system that allows agents to self-validate before exit, reducing retry cycles and improving quality.

### Tier 1: Agent Self-Validation (Recommended)
Agents can validate their own work before exiting:

```bash
# Agent runs self-validation
echo '{"subagent": "implementer-spark", "self_check": true}' | \
python3 ~/.claude/hooks/spark_quality_gates.py
```

#### Self-Validation Flow
```mermaid
graph TD
    A[Agent Completes Work] --> B[Run Self-Validation]
    B --> C{Validation Pass?}
    C -->|Yes| D[Mark self_validated in state]
    D --> E[Exit Agent]
    C -->|No| F[Show Actionable Fixes]
    F --> G[Agent Fixes Issues]
    G --> B
    E --> H[SubagentStop Hook]
    H --> I{Already Self-Validated?}
    I -->|Yes| J[Skip Validation - Continue]
    I -->|No| K[Run Full Validation]
```

#### Actionable Fix Messages
```
🚫 VALIDATION FAILED - Fix these issues before exiting:

• Implementation Verification:
  - Claimed file does not exist: /src/api/auth.py
  - API endpoint not found in code: POST /api/login

📋 ACTION REQUIRED:
📝 Create the missing file: /src/api/auth.py
🔌 Add the missing API endpoint to your code
```

### Tier 2: Hook Validation (Fallback)
If agent skips self-validation, SubagentStop hook enforces quality:

#### Duplicate Prevention Logic
```python
# In SubagentStop hook
if state.get("self_validated_by") == subagent_name:
    if time_since_validation < 5_minutes:
        return "continue"  # Skip duplicate validation
```

### Validation Gates

#### ImplementationVerificationGate
- Verifies files_created actually exist
- Checks files_modified were really changed (git diff)
- Searches for claimed API endpoints in code
- Validates database changes through migration files

#### TestVerificationGate  
- Verifies test files exist
- Runs pytest/jest to verify tests pass
- Checks actual coverage vs claimed coverage
- Counts test functions vs claimed count

## 📝 State Management

### State File Locations
```
.claude/workflows/
├── unified_context.json      # Unified context
├── current_task.json         # Current task state
├── team1_current_task.json   # Team-specific task state
└── state.json                # Validation state & self-validation tracking
```

### State Structure
```json
{
  "task_id": "abc123",
  "prompt": "Original request",
  "personas": ["Backend Developer", "Security Expert"],
  "quality_gates": {
    "syntax_validation": "passed",
    "type_checking": "passed",
    "linting": "failed"
  },
  "retry_count": 1,
  "state": "retrying",
  "self_validated_by": "implementer-spark",
  "self_validated_at": "2025-01-11T12:30:00.000Z",
  "implementation_verification": {
    "verified_at": "2025-01-11T12:30:00.000Z",
    "verification_passed": true,
    "verification_results": {
      "claimed_files": ["api.py", "auth.py"],
      "actual_files": ["api.py", "auth.py"],
      "discrepancies": []
    }
  },
  "test_verification": {
    "verified_at": "2025-01-11T12:35:00.000Z",
    "verification_passed": true,
    "verification_results": {
      "claimed_coverage": 95,
      "actual_coverage": 96,
      "claimed_test_files": ["test_api.py"],
      "actual_test_files": ["test_api.py"]
    }
  }
}
```

## 🚀 Hook Activation Workflow

### Standard Workflow (Without Self-Validation)
```mermaid
graph TD
    A[User Prompt] --> B[UserPromptSubmit Hook]
    B --> C[Execute Persona Router]
    C --> D[Select Appropriate Agent]
    D --> E[Agent Performs Work]
    E --> F[SubagentStop Hook]
    F --> G{Quality Gates Pass?}
    G -->|Yes| H[Task Complete]
    G -->|No| I[Retry or Fail]
```

### Enhanced Workflow (With Self-Validation)
```mermaid
graph TD
    A[User Prompt] --> B[UserPromptSubmit Hook]
    B --> C[Execute Persona Router]
    C --> D[Select Agent]
    D --> E[Agent Works]
    E --> F[Self-Validate?]
    F -->|Yes| G[Run Validation]
    G --> H{Pass?}
    H -->|No| I[Fix & Retry]
    I --> G
    H -->|Yes| J[Mark Validated]
    F -->|No| K[Exit Agent]
    J --> K
    K --> L[SubagentStop Hook]
    L --> M{Already Validated?}
    M -->|Yes| N[Skip - Continue]
    M -->|No| O[Run Validation]
    O --> P{Pass?}
    P -->|Yes| Q[Complete]
    P -->|No| R[Claude CODE Retry]
```

## 🔍 Debugging

### Verify Hook Execution
```bash
# Check hook status
/hooks

# Run in debug mode
claude --debug

# Check hook logs
tail -f ~/.claude/logs/hooks.log
```

### Common Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Hook not executing | settings.json configuration error | Check file path and permissions |
| Exit code 2 not working | JSON output format error | Verify decision field |
| Context not being added | Exit code is not 0 | Confirm sys.exit(0) |

## 📚 References

- [Anthropic Hook Guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)
- [Hook Reference](https://docs.anthropic.com/en/docs/claude-code/hooks-reference)
- [CLAUDE_CODE_GUIDELINES.md](./CLAUDE_CODE_GUIDELINES.md)

---

*This guide is the official documentation for implementing the SPARK v3.5 Hook System.*