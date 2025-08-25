# Phase 5B: Quality Gates Execution Template

## CRITICAL: All agents MUST follow this exact protocol

### Phase 5B Implementation (REQUIRED for ALL agents)

```python
print("Phase 5B - Quality Gates: Starting validation...")

# Step 1: Save current JSON with quality metrics
import json
with open(json_file, 'w') as f:
    json.dump(task_data, f, indent=2)
print("Phase 5B - Quality Gates: JSON updated with quality metrics")

# Step 2: Run quality gates verification
import subprocess
result = subprocess.run([
    'bash', '-c',
    f'echo \'{{"subagent": "{agent_name}", "self_check": true}}\' | python3 ~/.claude/hooks/spark_quality_gates.py'
], capture_output=True, text=True)

# Step 3: Check result and take action
if "Quality gates PASSED" in result.stdout:
    print("✅ Quality gates PASSED. Task completed successfully.")
    print("   You may now exit.")
    
    # Update JSON with final status
    task_data["quality"]["can_proceed"] = True
    task_data["state"]["status"] = "completed"
    
    with open(json_file, 'w') as f:
        json.dump(task_data, f, indent=2)
    
    # Exit successfully
    exit(0)
    
else:
    print("🚫 Quality gates FAILED. Please fix violations and retry.")
    print("   All violations must be 0 to complete the task.")
    
    # Parse specific violations from output
    violations = parse_violations(result.stdout)
    
    if retry_count < 3:
        print(f"Retry attempt {retry_count + 1} of 3")
        # Go back to Phase 4 and fix issues
        fix_violations(violations)
        retry_count += 1
    else:
        print("❌ Maximum retries exceeded. Reporting failure to 2호.")
        task_data["state"]["status"] = "failed"
        task_data["state"]["errors"].append("Quality gates failed after 3 attempts")
        
        with open(json_file, 'w') as f:
            json.dump(task_data, f, indent=2)
        
        exit(1)
```

## Key Points for Implementation:

1. **ALWAYS run quality gates** - No agent can skip this
2. **Use exact message format** - "Quality gates PASSED" or "Quality gates FAILED"
3. **Maximum 3 retries** - Then report failure
4. **Update JSON properly** - can_proceed and status fields
5. **Exit codes matter** - 0 for success, 1 for failure

## JSON File Selection:

```python
# Determine which JSON file to use
if "team1" in agent_name:
    json_file = "~/.claude/workflows/team1_current_task.json"
elif "team2" in agent_name:
    json_file = "~/.claude/workflows/team2_current_task.json"
elif "team3" in agent_name:
    json_file = "~/.claude/workflows/team3_current_task.json"
elif "team4" in agent_name:
    json_file = "~/.claude/workflows/team4_current_task.json"
else:
    json_file = "~/.claude/workflows/current_task.json"
```

## Quality Metrics Recording (Phase 5A):

```python
# Example of recording actual metrics
task_data["quality"]["step_2_foundation"]["syntax"] = count_syntax_errors()
task_data["quality"]["step_2_foundation"]["types"] = count_type_errors()
task_data["quality"]["step_5_quality"]["linting"] = count_linting_violations()

# Calculate total
violations_total = sum_all_violations()
task_data["quality"]["violations_total"] = violations_total

print(f"Phase 5A - Quality Metrics: Total violations = {violations_total}")
```

## Remember:
- Agents READ JSON but NEVER modify directly (except through proper API)
- Report progress via print statements
- Quality gates script does the verification
- 2호 makes final decisions based on JSON state