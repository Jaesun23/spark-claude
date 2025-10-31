# Claude Code Hooks and Agent Configuration

**Document Version**: 1.0
**Last Updated**: 2025-10-31
**Source**: Anthropic Official Documentation & SPARK Project Analysis

This document provides comprehensive reference for Claude Code hooks functionality and agent YAML frontmatter configuration based on official Anthropic documentation and real-world SPARK implementation.

---

## Part 1: Claude Code Hooks

### 1.1 What Are Hooks?

**Definition**: Hooks are automated shell commands that execute at specific points during Claude Code's lifecycle, enabling custom validation, permissions, context injection, and automation.

**Key Characteristic**: Hooks execute **automatically and transparently**—Claude Code (2号) and agents are **unaware** that hooks have executed. This is not background processing; rather, hooks intercept specific events and execute before Claude/agents continue.

**Example**: When a user submits a prompt, a `UserPromptSubmit` hook can:
- Inject additional context into Claude's reasoning
- Validate the prompt format
- Block certain types of requests
- All of this happens **before** Claude sees the prompt

### 1.2 How Hooks Work

**Communication Mechanism**:
1. **Input**: Hooks receive JSON data via `stdin` containing session and event-specific information
2. **Processing**: Hook script executes shell commands/logic
3. **Output**: Hooks communicate back through:
   - Exit codes (0 = success, 2 = blocking error, other = non-blocking error)
   - Optional JSON output to `stdout`

**Bidirectional Control**: Hooks can:
- Block or approve tool executions
- Inject context into Claude's reasoning
- Modify tool inputs before execution
- Add validation logic to workflows

### 1.3 Available Hook Types

#### Tool-Related Hooks

**PreToolUse**
- **Trigger**: After Claude creates tool parameters but **before** processing the call
- **Purpose**: Validate, modify, or block tool execution
- **Supports Matchers**: Can target specific tools like `Bash`, `Write`, `Edit`, `Read`, `WebFetch`, etc.
- **Use Case**: Enforce coding standards, prevent dangerous operations, validate paths

**PostToolUse**
- **Trigger**: Immediately after successful tool completion
- **Purpose**: React to tool results, log operations, trigger follow-up actions
- **Access**: Both tool inputs and tool responses
- **Use Case**: Automatic formatting, quality checks, notification triggers

#### Event-Based Hooks

**UserPromptSubmit**
- **Trigger**: When user submits a prompt
- **Purpose**: Validate or inject context before Claude processes input
- **Context Injection**: Hook stdout is added as system context to Claude
- **Use Case**: Load project standards, inject custom guidelines, validate request format

**Notification**
- **Trigger**: When Claude sends notifications (permission requests, idle waiting)
- **Purpose**: React to notification events
- **Use Case**: Auto-approve certain permissions, log permission requests

**Stop/SubagentStop**
- **Trigger**: When agents finish responding
- **Purpose**: Intervene before completion, cleanup tasks
- **Use Case**: Save session state, trigger cleanup scripts

#### Lifecycle Hooks

**SessionStart**
- **Trigger**: At session initialization or resume
- **Purpose**: Setup development environment, load context
- **Environment Persistence**: Can write to `$CLAUDE_ENV_FILE` to persist variables
- **Use Case**: Load project configuration, activate virtual environments, set standards

**SessionEnd**
- **Trigger**: During session termination
- **Purpose**: Cleanup tasks, save state
- **Use Case**: Deactivate environments, save session logs

**PreCompact**
- **Trigger**: Before context compaction (manual or automatic)
- **Purpose**: Preserve important information before compaction
- **Use Case**: Save critical context, log pre-compaction state

### 1.4 Configuration Format

**Location**: Settings files at three scopes:
- Global: `~/.claude/settings.json`
- Project: `.claude/settings.json`
- Local: `.claude/settings.local.json` (gitignored)

**Structure**:
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-script.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**Key Elements**:
- **matcher**: Regex patterns for tool names (case-sensitive). Use `*` or `""` to match all tools
- **command**: Bash commands or script paths. Use `$CLAUDE_PROJECT_DIR` for project-relative paths
- **timeout**: Optional per-command limit in seconds (default: 60, max: implementation-dependent)

### 1.5 Hook Input Structure

**Common Fields** (all hooks receive):
```json
{
  "session_id": "unique_session_identifier",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/working/directory",
  "permission_mode": "auto|manual",
  "hook_event_name": "PreToolUse|PostToolUse|etc"
}
```

**Event-Specific Fields**:
- **PreToolUse/PostToolUse**: `tool_name`, `tool_input`, `tool_output` (PostToolUse only)
- **UserPromptSubmit**: `user_prompt`, `prompt_metadata`
- **SessionStart**: `session_metadata`, `environment_vars`

### 1.6 Hook Output Methods

**Method 1: Exit Codes (Simple)**
```bash
#!/bin/bash
# Success: stdout shown in transcript mode (except UserPromptSubmit/SessionStart where it's added as context)
exit 0

# Blocking error: stderr fed to Claude for handling
echo "Critical validation failed" >&2
exit 2

# Non-blocking error: stderr shown to user
echo "Warning: minor issue detected" >&2
exit 1
```

**Method 2: JSON Output (Advanced)**
```json
{
  "continue": true,
  "stopReason": "optional message",
  "decision": "allow|deny|block|undefined",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "string to inject into Claude's context"
  }
}
```

**Decision Values**:
- `allow`: Permit operation
- `deny`: Refuse but don't block Claude entirely
- `block`: Hard stop with error
- `undefined`: Let default behavior proceed

### 1.7 Security Considerations

**Critical Warnings**:
> "Claude Code hooks execute arbitrary shell commands on your system automatically. By using hooks, you acknowledge that you are solely responsible for the commands you configure."

Hooks can:
- Modify or delete any files your user account can access
- Execute arbitrary code
- Access sensitive data
- Communicate with external systems

**Best Practices**:
1. **Validate and sanitize** all inputs strictly
2. **Quote shell variables**: Always use `"$VAR"` syntax
3. **Block path traversal**: Check for `..` in file paths
4. **Use absolute paths** for scripts
5. **Skip sensitive files**: `.env`, `.git/`, credentials
6. **Test thoroughly** in safe environments before production

### 1.8 Practical Example: Bash Command Validation

**Scenario**: Prevent use of deprecated `grep` command, enforce `rg` (ripgrep)

```python
#!/usr/bin/env python3
import json
import sys

# Read hook input
input_data = json.load(sys.stdin)

# Check if this is a Bash tool call
if input_data.get("tool_name") == "Bash":
    command = input_data.get("tool_input", {}).get("command", "")

    # Detect deprecated grep usage (not in pipeline)
    if "grep" in command and "|" not in command:
        # Send error message to stderr
        print("Use 'rg' (ripgrep) instead of 'grep' for better performance", file=sys.stderr)

        # Exit with code 2 to BLOCK execution
        sys.exit(2)

# Allow execution
sys.exit(0)
```

**Configuration**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validate_bash.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### 1.9 SPARK Project Hook Usage

**Quality Gates Hook** (`spark_quality_gates.py`):
- **Trigger**: PostToolUse (after agent writes JSON state)
- **Purpose**: Verify agent claims vs actual code quality
- **Checks**: Ruff violations, MyPy errors, test coverage, evidence counts
- **Output**: Blocks agent completion if quality gates fail

**Execution Flow**:
```
Agent → Writes JSON State → PostToolUse Hook Triggers
  → spark_quality_gates.py reads JSON
  → Runs ruff, mypy, pytest
  → Compares actual results vs JSON claims
  → Exit 0 (pass) or Exit 2 (block with violations)
```

**Key Insight**: Agents are **unaware** that quality gates run. They complete their work, write JSON, and the hook validates independently before 2号 resumes.

### 1.10 Advanced Features

**Plugin Integration**:
- Plugins can define hooks in `hooks/hooks.json`
- Automatically merged with user configurations
- Reference plugin files via `${CLAUDE_PLUGIN_ROOT}`

**MCP Tool Support**:
- Hooks work with Model Context Protocol tools
- Naming pattern: `mcp__<server>__<tool>`
- Example matcher: `mcp__memory__.*` matches all memory server tools

**Environment Persistence**:
- SessionStart hooks can write to `$CLAUDE_ENV_FILE`
- Persists environment variables for subsequent bash commands
- Enables complex setup workflows across session

**Parallel Execution**:
- All matching hooks run in parallel (not sequential)
- 60-second default timeout per command
- Hooks execute in current directory with `CLAUDE_PROJECT_DIR` available

---

## Part 2: Agent YAML Frontmatter Configuration

### 2.1 Overview

**Purpose**: YAML frontmatter defines agent metadata and configuration, loaded into Claude Code's system prompt when agent is invoked.

**Location**:
- User-level: `~/.claude/agents/*.md`
- Project-level: `.claude/agents/*.md`

**Progressive Disclosure**: At startup, Claude Code pre-loads only the `name` and `description` of every agent, providing just enough information for 2号 to know when each agent should be used without loading full context.

### 2.2 YAML Frontmatter Structure

**Basic Structure**:
```yaml
---
name: agent-name
description: Detailed description of when to use this agent
tools: tool1, tool2, tool3
model: sonnet|haiku|opus
color: red|blue|green|etc
---
```

### 2.3 Frontmatter Fields

#### Required Fields

**name** (string, required)
- **Purpose**: Unique identifier for the agent
- **Format**: lowercase with hyphens (e.g., `analyzer-spark`, `team1-implementer-spark`)
- **Used By**: 2号 when calling `Task("name", "instructions")`
- **Constraint**: Must be unique across all agents

**description** (string, required)
- **Purpose**: Detailed explanation of when to use this agent
- **Length**: Can be extensive (100-500+ words)
- **Content**: Triggering conditions, use cases, examples, specialization
- **Loaded**: Into 2号's system prompt for agent selection
- **Critical**: This is how 2号 decides which agent to use

**Example** (from SPARK):
```yaml
description: Use this agent when you need comprehensive multi-dimensional system
  analysis following trait-based dynamic persona principles with systematic 5-phase
  methodology. Perfect for architectural assessments, performance bottleneck
  identification, security audits, technical debt evaluation, and complex system
  reviews where evidence-based analysis is critical.
```

#### Optional Fields

**tools** (comma-separated list, optional)
- **Purpose**: Specific tools this agent can use
- **Format**: `tool1, tool2, tool3` (comma-separated, no spaces after commas recommended)
- **Available Tools**:
  - File operations: `Read`, `Write`, `Edit`, `MultiEdit`, `Glob`, `Grep`, `LS`
  - Execution: `Bash`, `BashOutput`, `KillBash`
  - Web: `WebFetch`, `WebSearch`
  - Notebook: `NotebookEdit`
  - Utility: `TodoWrite`
  - MCP Tools: `mcp__<server>__<tool>` format
- **Default**: If omitted, agent has access to all tools (except `Task`)
- **Use Case**: Restrict agents to specific tool subsets for safety or specialization

**Example** (from SPARK analyzer-spark):
```yaml
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, TodoWrite,
  WebSearch, mcp__sequential-thinking__sequentialthinking,
  mcp__context7__resolve-library-id, mcp__context7__get-library-docs
```

**model** (string, optional)
- **Purpose**: Specify which Claude model variant to use
- **Values**:
  - `sonnet`: Claude Sonnet (default, balanced)
  - `haiku`: Claude Haiku (fast, cost-effective)
  - `opus`: Claude Opus (most capable, expensive)
- **Default**: If omitted, inherits from parent session (usually `sonnet`)
- **Use Case**: Use `haiku` for simple tasks, `opus` for complex reasoning

**color** (string, optional)
- **Purpose**: Visual identification in Claude Code UI
- **Values**: `red`, `blue`, `green`, `yellow`, `orange`, `purple`, `pink`, `cyan`, etc.
- **Use Case**: Team differentiation (e.g., all team1 agents = red, team2 = blue)
- **Default**: If omitted, uses default UI color

**Example Color Usage** (from SPARK):
- Core agents: `analyzer-spark` (red), `implementer-spark` (pink), `tester-spark` (orange)
- Team agents: `team1-*` (red/green/orange), `team2-*` (blue/yellow/pink)

### 2.4 Real-World Examples from SPARK

#### Example 1: Core Agent (analyzer-spark)

```yaml
---
name: analyzer-spark
description: Use this agent when you need comprehensive multi-dimensional system
  analysis following trait-based dynamic persona principles with systematic 5-phase
  methodology. Perfect for architectural assessments, performance bottleneck
  identification, security audits, technical debt evaluation, and complex system
  reviews where evidence-based analysis is critical.
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, TodoWrite,
  WebSearch, mcp__sequential-thinking__sequentialthinking,
  mcp__context7__resolve-library-id, mcp__context7__get-library-docs
model: sonnet
color: red
---
```

**Analysis**:
- **Comprehensive description**: Clear triggering conditions and use cases
- **Extensive tools**: Includes MCP tools for deep thinking and documentation lookup
- **Model**: Sonnet for balanced performance
- **Color**: Red for critical analysis work

#### Example 2: Team Agent (team1-implementer-spark)

```yaml
---
name: team1-implementer-spark
description: Team 1 implementation specialist for multi-team parallel execution.
  Reads from team1_current_task.json and updates team1-specific sections.
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, TodoWrite,
  WebSearch, mcp__sequential-thinking__sequentialthinking,
  mcp__context7__resolve-library-id, mcp__context7__get-library-docs,
  mcp__time__get_current_time
model: sonnet
color: red
---
```

**Analysis**:
- **Team-specific**: Clear identification as Team 1's implementer
- **JSON state reference**: Explicitly mentions reading from `team1_current_task.json`
- **Time tools**: Includes `mcp__time__get_current_time` for timestamping
- **Color**: Red to visually identify as Team 1

#### Example 3: Specialized Agent (qc-spark)

```yaml
---
name: qc-spark
description: Quality control specialist systematically eliminating violations with
  zero-tolerance standards. Use when you need comprehensive quality inspection,
  batch violation fixes, or preparation for production deployment where zero
  defects are required.
tools: Glob, Grep, Read, WebFetch, TodoWrite, WebSearch, BashOutput, KillBash,
  Edit, MultiEdit, Write, NotebookEdit, Bash,
  mcp__sequential-thinking__sequentialthinking, mcp__time__get_current_time
model: sonnet
color: red
---
```

**Analysis**:
- **Specialized purpose**: Quality control with zero-tolerance focus
- **Process control tools**: Includes `BashOutput`, `KillBash` for managing long-running checks
- **Notebook support**: `NotebookEdit` for fixing Jupyter notebooks
- **Systematic approach**: Description emphasizes systematic elimination

#### Example 4: Extensive Description (root-cause-analyzer)

```yaml
---
name: root-cause-analyzer
description: Use this agent when you need to investigate and analyze problems in
  software projects through systematic evidence collection and root cause analysis.
  This agent excels at transforming complex technical issues into clear, documented
  solutions.

  **Triggering Conditions**:
  - System failures, bugs, or unexpected behaviors requiring deep investigation
  - Performance degradation or reliability issues needing root cause identification
  - Architecture decisions requiring evidence-based analysis
  - Code quality issues requiring systematic diagnosis
  - Integration problems or dependency conflicts
  - Technical debt assessment and prioritization
  - Post-mortem analysis after incidents

  **Example Usage Scenarios**:

  <example>
  Context: User encounters intermittent test failures in CI/CD pipeline.

  User: "Our tests are failing randomly in CI but pass locally. Can you help?"

  Assistant: "I'll use the Task tool to launch the root-cause-analyzer agent to
  systematically investigate this issue."

  <agent_invocation>
  Task("root-cause-analyzer", "Investigate intermittent CI test failures: tests
  pass locally but fail randomly in CI pipeline")
  </agent_invocation>

  <commentary>
  The root-cause-analyzer agent will collect evidence from CI logs, test outputs,
  timing data, and environment configurations to identify the root cause (likely
  race conditions, timing dependencies, or environment differences) and provide a
  documented solution.
  </commentary>
  </example>

  [... additional examples ...]
model: sonnet
---
```

**Analysis**:
- **Extensive guidance**: 500+ word description with structured sections
- **Clear triggering conditions**: Bulleted list of when to use
- **Concrete examples**: Full conversation examples showing usage
- **Educational**: Teaches 2号 exactly how to invoke this agent
- **Pattern**: This is a "teaching description" that trains 2号's decision-making

### 2.5 Description Best Practices

Based on SPARK implementation analysis:

**1. Start with Summary**
- First sentence: High-level purpose
- Keywords: Specialization area (e.g., "multi-dimensional system analysis")

**2. Specify Triggering Conditions**
- When to use this agent
- What types of problems it solves
- What distinguishes it from other agents

**3. Provide Concrete Examples (Optional)**
- Conversation snippets showing invocation
- Helps 2号 pattern-match user requests to agents

**4. Highlight Unique Capabilities**
- What makes this agent special
- What methodology/protocol it follows
- What quality standards it enforces

**5. Use Structured Format**
```yaml
description: [Summary sentence]. [Core purpose]. [Methodology].

  Perfect for [use case 1], [use case 2], [use case 3].

  [Optional: Triggering conditions section]

  [Optional: Example scenarios]
```

### 2.6 Tool Selection Strategy

**All Tools (Default)**:
- **When**: Agent needs maximum flexibility
- **Omit** `tools` field entirely
- **Example**: General-purpose agents

**Restricted Tool Set**:
- **When**: Safety, specialization, or token optimization
- **Specify**: Only tools actually needed
- **Example**: `qc-spark` (quality checks don't need web access)

**MCP Tools**:
- **Format**: `mcp__<server>__<tool>`
- **Example**: `mcp__sequential-thinking__sequentialthinking`
- **Use Case**: Advanced reasoning, memory, external services

**Common Tool Combinations**:

**Read-Only Analysis**:
```yaml
tools: Glob, Grep, Read, WebFetch, TodoWrite
```

**Code Modification**:
```yaml
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write, TodoWrite
```

**Full Development**:
```yaml
tools: Bash, Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, TodoWrite,
  WebSearch, mcp__sequential-thinking__sequentialthinking
```

### 2.7 Model Selection Guidelines

**Use `sonnet` (default) when**:
- Balanced performance and cost needed
- General-purpose tasks
- Most SPARK agents use this

**Use `haiku` when**:
- Simple, repetitive tasks
- Fast turnaround needed
- Cost optimization critical
- Example: Simple file renaming, basic transformations

**Use `opus` when**:
- Complex reasoning required
- Highest quality output needed
- Cost is not a concern
- Example: Architectural design decisions, complex refactoring

### 2.8 SPARK-Specific Patterns

**Team Agent Naming**:
```
team[1-5]-[role]-spark
```
- Examples: `team1-implementer-spark`, `team3-tester-spark`
- Color coded by team for visual identification

**Core Agent Naming**:
```
[domain]-spark
```
- Examples: `analyzer-spark`, `implementer-spark`, `tester-spark`
- Domain clearly identifies specialization

**JSON State Reference**:
- Team agents mention specific JSON file in description
- Example: "Reads from team1_current_task.json"
- Helps agent know where to find task context

**Constitutional Alignment**:
- All descriptions mention following SPARK Constitution
- Example: "following trait-based dynamic persona principles"
- Ensures agents know they're part of larger system

---

## Part 3: Integration - Hooks and Agents Together

### 3.1 How They Complement Each Other

**Agents**:
- Define **what work to do** (traits, workflow, protocols)
- Execute tasks in isolated sessions
- Write results to JSON state files

**Hooks**:
- Define **automated validation and enforcement**
- Execute transparently without agent awareness
- Verify agent claims and enforce standards

### 3.2 SPARK Quality Gates Pattern

**Flow**:
```
2号 → Task("implementer-spark", task)
  → Agent spawns, executes implementation
  → Agent writes current_task.json with quality claims
  → PostToolUse hook triggers (spark_quality_gates.py)
    → Hook reads JSON
    → Hook runs ruff, mypy, pytest
    → Hook compares claims vs reality
    → Hook exits 0 (pass) or 2 (block)
  → Agent completes
2号 resumes → Reads JSON, sees pass/fail status
```

**Agent is Unaware**:
- Agent thinks it just wrote JSON and completed
- Hook verification happens "invisibly"
- 2号 sees final validated result

### 3.3 Context Injection Pattern

**UserPromptSubmit Hook**:
```bash
#!/bin/bash
# Inject project standards into every request
cat /path/to/PROJECT_STANDARDS.md
exit 0
```

**Effect**:
- User submits: "Implement authentication"
- Hook executes, outputs standards document
- Claude receives: [Project Standards] + "Implement authentication"
- Agent invoked with full standards context

**Agent is Unaware**:
- Agent doesn't know standards were injected
- Agent just sees them in system prompt
- Natural behavior adaptation

### 3.4 Pre-Execution Validation Pattern

**PreToolUse Hook for Bash**:
```python
# Block dangerous commands
if "rm -rf /" in command:
    print("BLOCKED: Dangerous command detected", file=sys.stderr)
    sys.exit(2)
```

**Effect**:
- Agent tries to run `Bash("rm -rf /tmp")`
- Hook intercepts, blocks execution
- Agent receives error about blocked command
- Agent must revise approach

### 3.5 Design Philosophy

**Separation of Concerns**:
- **Agents**: Expertise and execution
- **Hooks**: Validation and enforcement
- **2号**: Orchestration and decision-making

**Zero Trust**:
- Agents are not trusted to self-validate
- Hooks provide independent verification
- Quality gates enforce standards automatically

**Transparency**:
- Agents work naturally without hook awareness
- Hooks operate silently in background
- System maintains integrity without agent cooperation

---

## Part 4: Summary and Key Takeaways

### 4.1 Hooks Key Points

1. **Automatic Execution**: Hooks trigger on events, not agent calls
2. **Transparent Operation**: Agents/2号 unaware of hook execution
3. **Bidirectional Control**: Can block, allow, or inject context
4. **Security Critical**: Execute arbitrary commands, require careful design
5. **Flexible Integration**: Plugins, MCP tools, environment persistence

### 4.2 Agent Frontmatter Key Points

1. **Progressive Disclosure**: Only name/description loaded initially
2. **Description is Critical**: How 2号 selects agents
3. **Tools Optional**: Default = all tools (except Task)
4. **Model Flexibility**: Choose per agent (sonnet/haiku/opus)
5. **Color for Organization**: Visual identification in UI

### 4.3 SPARK Implementation Insights

**Hooks in SPARK**:
- Quality gates for zero-tolerance enforcement
- Context injection for standards compliance
- Validation before execution

**Agent Design in SPARK**:
- Extensive descriptions with triggering conditions
- Trait-based personas (maximum 5 traits)
- Constitutional alignment throughout
- Team agents for parallel execution
- JSON state for inter-agent communication

### 4.4 Best Practices

**For Hooks**:
1. Always validate and sanitize inputs
2. Use exit code 2 for blocking errors
3. Test extensively before production
4. Document hook behavior clearly
5. Consider security implications

**For Agent Frontmatter**:
1. Write detailed, specific descriptions
2. Include concrete triggering conditions
3. Specify tools only when restriction needed
4. Use appropriate model for task complexity
5. Maintain consistency in naming conventions

---

## References

- **Official Documentation**: [https://docs.claude.com/en/docs/claude-code/hooks](https://docs.claude.com/en/docs/claude-code/hooks)
- **SPARK Constitution**: `.claude/SPARK_CONSTITUTION.md`
- **SPARK Agents**: `.claude/agents/*.md`
- **Quality Gates Implementation**: `.claude/hooks/spark_quality_gates.py`
