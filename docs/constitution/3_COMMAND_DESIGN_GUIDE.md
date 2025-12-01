# SPARK Command Design Guide
## Detailed Standards for Creating Effective Commands

**Part of**: SPARK Constitution v1.2
**Core Document**: See **CONSTITUTION.md** for foundational principles
**Last Updated**: 2025-10-30

This guide expands on **Article III: Command Design Standards** with detailed specifications, examples, and best practices.

---

## Table of Contents

1. [Orchestration Responsibility](#section-31-orchestration-responsibility)
2. [Validation Protocols](#section-32-validation-protocols)
3. [Retry Strategies](#section-33-retry-strategies)
4. [Multi-Session Management](#section-34-multi-session-management)

---

## Section 3.1: Orchestration Responsibility

### The Conductor Principle

Commands orchestrate agents, they don't do the work.

**Core Analogy**: A command is like a conductor leading an orchestra:
- Conductor doesn't play instruments (agents do the work)
- Conductor coordinates timing and sequence (orchestration)
- Conductor ensures quality of performance (validation)
- Conductor handles problems that arise (retry logic)

### Command File Structure

**Standard Template**:

```markdown
---
name: spark-design
description: System architecture design with validation and multi-session support
---

# /spark-design Command

## 2号 Orchestration Protocol

### 1. INITIAL ASSESSMENT
[Check for existing state, resume or start new]

### 2. AGENT INVOCATION
[Call designer-spark with requirements]

### 3. VALIDATION
[Check current_task.json for completion criteria]

### 4. RETRY LOGIC
[If validation fails, provide feedback and retry]

### 5. MULTI-SESSION MANAGEMENT
[Track progress across sessions if needed]

### 6. REPORTING
[Inform user of results]
```

### Required Elements

Every command MUST include these sections:

#### 1. Initial Assessment

**Purpose**: Check if this is a new task or continuation

**What to Check**:
- Does state file exist?
- Is this a multi-session continuation?
- Are there partial results to resume from?

**Example**:
```python
# Check for existing state
state_file = "~/.claude/workflows/design_state.yaml"

if exists(state_file):
    print("📂 Found existing work. Resuming...")
    state = load_yaml(state_file)
    # Resume logic
else:
    print("🆕 Starting new design work...")
    # New work logic
```

#### 2. Agent Invocation

**Purpose**: Call the appropriate agent with clear requirements

**What to Include**:
- Task description
- Project context (standards, architecture docs)
- Standard modules to use
- Expected deliverables
- Quality requirements

**Example**:
```python
Task("designer-spark", f"""
Design RESTful API for {feature_name}.

📋 Project Standards (READ FIRST):
- {PROJECT_ROOT}/PROJECT_STANDARDS.md
- {PROJECT_ROOT}/ARCHITECTURE.md

🏗️ Standard Modules:
- common/errors/ → Error responses
- common/validation/ → Input validation

📦 Expected Deliverables:
- OpenAPI specification
- Data model diagrams
- API endpoint documentation

⚠️ Quality Requirements:
- All endpoints documented
- Error cases covered
- Validation rules specified
""")
```

#### 3. Validation

**Purpose**: Verify agent actually completed work successfully

**What to Check**:
- State file shows "completed" status
- Quality gates passed (can_proceed == true)
- Violations are zero
- Agent-specific criteria met

**Example**:
```python
def validate_completion():
    state = read_json("~/.claude/workflows/current_task.json")

    if state["state"]["status"] != "completed":
        return False, "Agent did not complete"

    if not state["quality"]["can_proceed"]:
        return False, "Quality gates failed"

    if state["quality"]["violations_total"] != 0:
        return False, f"{violations} violations remain"

    return True, "Success"
```

#### 4. Retry Logic

**Purpose**: Handle failures with increasingly specific feedback

**Strategy**:
- Attempt 1: General reminder
- Attempt 2: Specific issues listed
- Attempt 3: Explicit fix instructions
- After 3: Escalate to user

#### 5. Multi-Session Management (if applicable)

**Purpose**: Support large tasks that span multiple sessions

**What to Track**:
- Sessions completed vs planned
- Progress percentage
- Cumulative findings
- Next session focus

#### 6. User Communication

**Purpose**: Keep user informed of progress

**What to Report**:
- Work started
- Progress updates
- Completion status
- Next steps (if multi-session)

### Forbidden Content

Commands MUST NOT contain:

#### ❌ Agent Work

```markdown
# ❌ WRONG - Command doing agent work
def implement_feature():
    # Write code here...
    code = generate_implementation()
    write_file("src/feature.py", code)
```

**Why Wrong**: This is implementer-spark's job, not command's.

#### ❌ Agent Traits Definition

```markdown
# ❌ WRONG - Defining agent traits
Your traits as an implementer:
- Simplicity-First
- Structural Integrity
```

**Why Wrong**: Traits belong in agent definition, not command.

#### ❌ Agent Phase Logic

```markdown
# ❌ WRONG - Duplicating agent phases
Phase 1: Evidence gathering
Phase 2: Pattern analysis
Phase 3: Synthesis
```

**Why Wrong**: Phase logic belongs in agent, command only orchestrates.

### Command Examples

#### Example 1: Simple Single-Agent Command

```markdown
---
name: spark-analyze
description: System analysis with evidence collection
---

# /spark-analyze Command

## 1. INITIAL ASSESSMENT

Check for existing analysis state.

## 2. AGENT INVOCATION

Call analyzer-spark with user requirements:
- Include project context
- Specify analysis dimensions
- Define depth and scope

## 3. VALIDATION

Verify:
- Analysis complete
- Evidence collected (min 12 items)
- Quality gates passed

## 4. RETRY LOGIC

If validation fails:
- Attempt 1: "Complete evidence collection"
- Attempt 2: "Missing evidence in: {dimensions}"
- Attempt 3: "Collect file:line for each finding"

## 5. REPORTING

Show:
- Evidence count
- Dimensions analyzed
- Key findings summary
```

#### Example 2: Multi-Agent Chain Command

```markdown
---
name: spark-launch
description: Complete feature launch (design → implement → test → document)
---

# /spark-launch Command

## 1. INITIAL ASSESSMENT

Check progress through chain.

## 2. AGENT CHAIN INVOCATION

Execute sequence:
1. designer-spark → Architecture
2. implementer-spark → Code
3. tester-spark → Tests
4. documenter-spark → Docs

Validate after EACH agent before proceeding.

## 3. CHAIN VALIDATION

After each agent:
- Check completion
- Verify quality
- Confirm deliverables

Only proceed to next agent if current passed.

## 4. CHAIN RETRY LOGIC

If any agent fails:
- Retry that specific agent (max 3)
- If still fails, pause chain
- Report to user which agent failed

## 5. REPORTING

Show:
- Chain progress (2/4 agents complete)
- Current agent status
- Overall success/failure
```

---

## Section 3.2: Validation Protocols

### The Trust-But-Verify Principle

Agents claim completion, commands verify truth.

**Philosophy**: Agents are trustworthy but validation is mandatory. This isn't about distrust - it's about systematic verification.

### Validation Checklist

**Complete Validation Function**:

```python
def validate_agent_completion(agent_name: str) -> tuple[bool, str]:
    """
    Verify agent actually completed work successfully.

    Returns:
        (success, message): True if validation passed, with explanation
    """

    # 1. Read state file
    try:
        state = read_json("~/.claude/workflows/current_task.json")
    except FileNotFoundError:
        return False, "State file not found"

    # 2. Check completion status
    if state["state"]["status"] != "completed":
        status = state["state"]["status"]
        return False, f"Status is '{status}', not 'completed'"

    # 3. Check quality gates
    if not state["quality"]["can_proceed"]:
        return False, "Quality gates did not pass"

    # 4. Check violations
    violations = state["quality"]["violations_total"]
    if violations != 0:
        return False, f"{violations} violations remain"

    # 5. Agent-specific validation
    if agent_name == "implementer-spark":
        # Must have test results
        coverage = state["quality"]["step_6_testing"]["coverage"]
        if coverage < 0.95:
            return False, f"Coverage {coverage:.1%} < 95%"

        # Must have zero test failures
        if state["quality"]["step_6_testing"].get("failures", 0) != 0:
            return False, "Tests are failing"

    elif agent_name == "analyzer-spark":
        # Must have evidence
        evidence_count = state.get("evidence_count", 0)
        if evidence_count < 8:
            return False, f"Only {evidence_count} evidence items (need 8+)"

    elif agent_name == "tester-spark":
        # Must have 100% test pass rate
        if state["quality"].get("test_pass_rate", 0) != 1.0:
            return False, "Not all tests passing"

    elif agent_name == "documenter-spark":
        # Must have 100% API coverage
        if state["quality"].get("api_coverage", 0) != 1.0:
            return False, "Not all APIs documented"

    # All checks passed
    return True, "Validation successful"
```

### Validation Enforcement Rules

**Commands MUST**:
- Validate after EVERY agent invocation
- NOT proceed if validation fails
- Provide specific feedback for retry attempts
- Check both universal and agent-specific criteria

**Commands MUST NOT**:
- Skip validation "just this once"
- Proceed with partial success
- Trust agent claims without verification
- Ignore quality gate failures

### Validation Error Handling

**When validation fails**:

```python
success, message = validate_agent_completion(agent_name)

if not success:
    print(f"❌ Validation failed: {message}")

    # Check retry count
    if retry_count < 3:
        # Provide feedback and retry
        feedback = generate_retry_feedback(message, retry_count)
        Task(agent_name, feedback)
        retry_count += 1
    else:
        # Escalate to user
        print(f"⚠️ Agent failed after 3 attempts")
        print(f"Last error: {message}")
        print(f"Manual intervention required")
        return False
```

---

## Section 3.3: Retry Strategies

### The Persistence Principle

Failure is temporary, success is mandatory.

**Philosophy**: Most failures are fixable with better feedback. Systematic retries with escalating specificity usually succeed.

### Retry Decision Tree

**Complete Retry Handler**:

```python
def handle_agent_failure(
    agent_name: str,
    attempt: int,
    max_attempts: int = 3
) -> bool:
    """
    Systematic retry with learning.

    Args:
        agent_name: Name of the agent that failed
        attempt: Current attempt number (0-indexed)
        max_attempts: Maximum retries allowed

    Returns:
        True if should retry, False if should escalate
    """

    if attempt >= max_attempts:
        report_failure_to_user(agent_name, attempt)
        return False

    # Analyze failure
    state = read_json("~/.claude/workflows/current_task.json")
    violations = state["quality"]["violations_total"]
    issues = identify_specific_issues(state)

    # Generate feedback based on attempt number
    if attempt == 0:
        # First retry: General feedback
        feedback = f"""
        RETRY ATTEMPT 1/{max_attempts}

        Previous attempt failed validation.

        Please:
        - Review quality requirements
        - Fix all violations
        - Re-run quality checks
        - Verify all quality gates pass
        """

    elif attempt == 1:
        # Second retry: Specific issues
        feedback = f"""
        RETRY ATTEMPT 2/{max_attempts}

        Previous attempt failed with {violations} violations:

        {format_issues_list(issues)}

        Requirements:
        - Fix each issue individually
        - No automated scripts
        - Manual, careful fixes
        - Verify after each fix
        """

    else:
        # Third retry: Explicit instructions
        feedback = f"""
        RETRY ATTEMPT 3/{max_attempts} - FINAL ATTEMPT

        Still {violations} violations remaining.

        STEP-BY-STEP INSTRUCTIONS:
        1. Read the violation: {issues[0]}
        2. Understand the root cause
        3. Fix manually (NO automated scripts)
        4. Run quality check
        5. Verify violation gone
        6. Repeat for next violation

        DO NOT report complete until violations_total == 0

        This is your final attempt. Take time to fix properly.
        """

    # Retry with feedback
    print(f"🔄 Retrying {agent_name} (Attempt {attempt + 1}/{max_attempts})")
    Task(agent_name, feedback)
    return True
```

### Retry Guidelines

**Escalating Feedback**:

| Attempt | Feedback Level | Example |
|---------|----------------|---------|
| 1st | General | "Fix violations and re-run quality checks" |
| 2nd | Specific | "Fix these 5 specific issues: [list]" |
| 3rd | Explicit | "Step 1: Fix line 45. Step 2: Fix line 67. ..." |

**Progress Verification**:

Each retry MUST show progress:

```python
def verify_retry_progress(
    previous_violations: int,
    current_violations: int
) -> bool:
    """Verify that retry made progress."""

    if current_violations == 0:
        return True  # Success!

    if current_violations < previous_violations:
        return True  # Progress made

    if current_violations >= previous_violations:
        return False  # No progress or worse
```

**No Progress Example**:

```
Attempt 1: 157 violations
Attempt 2: 203 violations (WORSE - automated script caused more issues)
Attempt 3: 189 violations (Still no progress)
→ Escalate to user
```

**Good Progress Example**:

```
Attempt 1: 157 violations → Manual fixes
Attempt 2: 89 violations (PROGRESS - 68 fixed)
Attempt 3: 0 violations (SUCCESS!)
```

### Escalation Protocol

**After max attempts exceeded**:

```python
def report_failure_to_user(agent_name: str, attempts: int):
    """Report failure to user for manual intervention."""

    state = read_json("~/.claude/workflows/current_task.json")
    violations = state["quality"]["violations_total"]

    print(f"""
    ⚠️ {agent_name} FAILED AFTER {attempts} ATTEMPTS

    Final State:
    - Status: {state['state']['status']}
    - Violations: {violations}
    - Can proceed: {state['quality']['can_proceed']}

    Remaining Issues:
    {format_remaining_issues(state)}

    Manual intervention required:
    1. Review state file: ~/.claude/workflows/current_task.json
    2. Analyze specific violations
    3. Fix manually or adjust requirements
    4. Re-run command to retry

    Possible Actions:
    - Fix issues manually and retry
    - Adjust quality requirements
    - Report bug in agent definition
    - Escalate to Jason
    """)
```

---

## Section 3.4: Multi-Session Management

### The Continuity Principle

Large tasks span sessions, state must persist.

**Use Cases**:
- Large codebase analysis (> 100K tokens)
- Complex multi-step implementations
- Comprehensive documentation projects
- Multi-day feature development

### Multi-Session Protocol

#### State File Structure

**Location**: `~/.claude/workflows/{agent}_state.yaml`

**Structure**:

```yaml
# State file for multi-session work

analysis_id: "analyzer_20251028_143022"
version: "4.3"
sessions_planned: 3
sessions_completed: 1

progress:
  overall_percentage: 33
  components_completed: 12
  total_components: 36

last_session_summary: "Phase 1-2 complete: discovered 156 files, collected 89 evidence items"

next_session:
  session: 2
  focus: "Deep analysis of security and performance dimensions"
  priority: ["security_deep_dive", "performance_bottlenecks"]
  estimated_tokens: 45000

cumulative_findings:
  - category: "architecture"
    count: 23
    severity: "medium"
  - category: "performance"
    count: 15
    severity: "high"

key_findings:
  - "Critical: 15 N+1 query patterns found"
  - "High: No authentication on 8 admin endpoints"
  - "Medium: 23 circular imports detected"
```

#### Session Management in Commands

**Complete Multi-Session Handler**:

```python
def manage_multi_session(
    agent_name: str,
    user_request: str,
    state_file: str
) -> str:
    """
    Handle multi-session continuation.

    Returns:
        Status message for user
    """

    if exists(state_file):
        # Resume existing work
        state = load_yaml(state_file)
        session = state['sessions_completed'] + 1
        total = state['sessions_planned']

        print(f"📂 Resuming {agent_name} (Session {session}/{total})")
        print(f"Progress: {state['progress']['overall_percentage']}%")
        print(f"Components: {state['progress']['components_completed']}/{state['progress']['total_components']}")
        print(f"\nLast session: {state['last_session_summary']}")
        print(f"Next focus: {state['next_session']['focus']}")

        # Continue with context
        Task(agent_name, f"""
        CONTINUE FROM SAVED STATE:

        Session: {session} of {total}
        State file: {state_file}

        Previous Progress:
        {state['last_session_summary']}

        Cumulative Findings:
        {format_findings(state['cumulative_findings'])}

        THIS SESSION FOCUS:
        {state['next_session']['focus']}

        Priorities:
        {format_list(state['next_session']['priority'])}

        Continue where you left off and update state file with progress.
        """)
    else:
        # New multi-session work
        print(f"🆕 Starting new {agent_name} work")
        print(f"Request: {user_request}")

        Task(agent_name, f"""
        NEW MULTI-SESSION WORK:

        Request: {user_request}
        State file: {state_file}

        If this is too large for one session:
        1. Assess total scope
        2. Plan session breakdown
        3. Create state file with plan
        4. Complete what you can in this session
        5. Save progress to state file

        Otherwise, complete in this session.
        """)

    # Wait for completion
    wait_for_agent_completion()

    # Check if more sessions needed
    if exists(state_file):
        state = load_yaml(state_file)

        if state['sessions_completed'] < state['sessions_planned']:
            remaining = state['sessions_planned'] - state['sessions_completed']
            return f"""
            ⚠️ Multi-session work in progress

            Sessions completed: {state['sessions_completed']}/{state['sessions_planned']}
            Progress: {state['progress']['overall_percentage']}%

            To continue:
            /{command_name} --continue

            Estimated sessions remaining: {remaining}
            """
        else:
            return """
            ✅ All sessions complete!

            Multi-session work finished successfully.
            Review cumulative findings in final report.
            """
    else:
        return """
        ✅ Work complete!

        Completed in single session.
        """
```

#### Session Continuation

**User Experience**:

```bash
# First session
$ /spark-analyze large-codebase
📊 Analyzing large codebase...
⚠️ Multi-session work required (estimated 3 sessions)
Session 1/3 complete (33% progress)

To continue: /spark-analyze --continue

# Second session
$ /spark-analyze --continue
📂 Resuming analyzer-spark (Session 2/3)
Progress: 33%
Last session: Phase 1-2 complete
...
Session 2/3 complete (67% progress)

To continue: /spark-analyze --continue

# Third session
$ /spark-analyze --continue
📂 Resuming analyzer-spark (Session 3/3)
Progress: 67%
...
✅ All sessions complete!
```

#### Requirements

Multi-session support MUST ensure:

1. **State Persistence**: State files survive between sessions
2. **Progress Tracking**: Clear indication of completion percentage
3. **Seamless Continuation**: User can resume easily
4. **Final Synthesis**: Last session integrates all previous work
5. **Cleanup**: State file deleted after successful completion

#### State File Cleanup

```python
def cleanup_completed_state(state_file: str):
    """Remove state file after successful completion."""

    if exists(state_file):
        state = load_yaml(state_file)

        if state['sessions_completed'] >= state['sessions_planned']:
            # All sessions done, safe to delete
            os.remove(state_file)
            print(f"🗑️ Cleaned up state file: {state_file}")
```

---

## Summary

This guide provides detailed specifications for creating effective SPARK commands:

1. **Orchestration**: Commands coordinate agents, don't do their work
2. **Validation**: Trust but verify - systematic validation after each agent
3. **Retry**: Escalating feedback over 3 attempts
4. **Multi-Session**: Support for large tasks spanning multiple sessions

**Key Principle**: Commands are conductors, not performers. They ensure the orchestra (agents) plays in harmony.

---

**Related Documents**:
- **CONSTITUTION.md** - Core principles
- **AGENT_DESIGN_GUIDE.md** - Agent design standards
- **INTEGRATION_GUIDE.md** - Integration standards
- **TEMPLATES.md** - Quick-start templates
