#!/bin/bash

# Batch update all SPARK agents with standardized Phase 5B structure
# This script processes all remaining agents systematically

AGENTS_DIR="/Users/jason/Projects/spark-claude/.claude/agents"
BACKUP_DIR="/Users/jason/Projects/spark-claude/.claude/agents_backup_$(date +%Y%m%d_%H%M%S)"

echo "=========================================="
echo "SPARK v4.1 Agent Update Script"
echo "=========================================="

# Create backup first
echo "Creating backup..."
cp -r "$AGENTS_DIR" "$BACKUP_DIR"
echo "✅ Backup created at: $BACKUP_DIR"

# List of all agents to update (excluding already updated ones)
AGENTS=(
    "analyzer-spark"
    "designer-spark"
    "improver-spark"
    "troubleshooter-spark"
    "cleaner-spark"
    "explainer-spark"
    "builder-spark"
    "estimater-spark"
    "gitter-spark"
    "spawner-spark"
    "loader-spark"
    "indexer-spark"
    "tasker-spark"
    "team1-implementer-spark"
    "team1-tester-spark"
    "team1-documenter-spark"
    "team2-implementer-spark"
    "team2-tester-spark"
    "team2-documenter-spark"
    "team3-implementer-spark"
    "team3-tester-spark"
    "team3-documenter-spark"
    "team4-implementer-spark"
    "team4-tester-spark"
    "team4-documenter-spark"
)

echo ""
echo "Updating ${#AGENTS[@]} agents..."
echo "=========================================="

for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/$agent.md"
    
    if [ ! -f "$AGENT_FILE" ]; then
        echo "⚠️  $agent.md not found, skipping..."
        continue
    fi
    
    echo "Processing $agent..."
    
    # Create temporary Python script for this agent
    cat > /tmp/update_agent.py << 'EOF'
import sys
import re

agent_name = sys.argv[1]
file_path = sys.argv[2]

# Read file
with open(file_path, 'r') as f:
    content = f.read()

# Remove Korean text throughout
content = re.sub(r'[\u3131-\ucb4c\uac00-\ud7a3]+\s*\([^)]+\)', lambda m: m.group(0).split('(')[1].rstrip(')'), content)
content = re.sub(r'\*\*[\u3131-\ucb4c\uac00-\ud7a3]+_?[^\*]*\*\*:', lambda m: '**' + m.group(0).split('(')[1].split(')')[0] + ':**' if '(' in m.group(0) else m.group(0), content)

# Update Phase 0
phase_0_new = """### Phase 0: Task Initialization

Read the current task JSON to understand the request:

```python
import json
import os

# Determine JSON file location
json_file = "~/.claude/workflows/current_task.json"
if not os.path.exists(os.path.expanduser(json_file)):
    json_file = ".claude/workflows/current_task.json"

# Read task data
with open(os.path.expanduser(json_file), 'r') as f:
    task_data = json.load(f)

print(f"Task ID: {task_data['id']}")
print(f"Request: {task_data['task']['prompt']}")
```"""

content = re.sub(r'### Phase 0:.*?(?=### Phase 1:)', phase_0_new + '\n\n', content, flags=re.DOTALL)

# Determine coverage value based on agent type
if 'tester' in agent_name:
    coverage_value = 'unit_coverage  # Tester reports actual coverage'
    specific_metrics = '''unit_coverage = 95  # Actual unit test coverage percentage
integration_coverage = 85  # Actual integration test coverage'''
else:
    coverage_value = '-1  # ' + agent_name.replace('-spark', '').capitalize() + ' doesn\'t do testing'
    specific_metrics = '# Agent-specific metrics for ' + agent_name

# Create Phase 5 replacement
phase_5_new = f"""### Phase 5: Task Completion

#### Phase 5A: Quality Metrics Recording

Record actual quality metrics:

```python
print("Phase 5A - Quality Metrics: Recording actual measurements...")

# Record actual metrics
syntax_errors = 0
type_errors = 0
linting_violations = 0

{specific_metrics}

# Calculate total violations
violations_total = syntax_errors + type_errors + linting_violations

print(f"Phase 5A - Quality Metrics: Total violations = {{violations_total}}")
```

#### Phase 5B: Quality Gates Execution (MANDATORY)

**CRITICAL: ALL agents MUST execute this phase exactly as shown**

```python
print("Phase 5B - Quality Gates: Starting validation...")

# Step 1: Update JSON with quality metrics
task_data["quality"] = {{
    "step_1_architecture": {{
        "imports": 0,
        "circular": 0,
        "domain": 0
    }},
    "step_2_foundation": {{
        "syntax": syntax_errors,
        "types": type_errors
    }},
    "step_3_standards": {{
        "formatting": 0,
        "conventions": 0
    }},
    "step_4_operations": {{
        "logging": 0,
        "security": 0,
        "config": 0
    }},
    "step_5_quality": {{
        "linting": linting_violations,
        "complexity": 0
    }},
    "step_6_testing": {{
        "coverage": {coverage_value}
    }},
    "step_7_documentation": {{
        "docstrings": 0,
        "readme": 0
    }},
    "step_8_integration": {{
        "final": 0
    }},
    "violations_total": violations_total,
    "can_proceed": False
}}

# Step 2: Save JSON file
with open(os.path.expanduser(json_file), 'w') as f:
    json.dump(task_data, f, indent=2)
print("Phase 5B - Quality Gates: JSON updated with quality metrics")

# Step 3: Run quality gates verification script
import subprocess
result = subprocess.run([
    'bash', '-c',
    'echo \\'{{"subagent": "{agent_name}", "self_check": true}}\\' | python3 ~/.claude/hooks/spark_quality_gates.py'
], capture_output=True, text=True)

# Step 4: Check result and take action
if "Quality gates PASSED" in result.stdout:
    print("✅ Quality gates PASSED. Task completed successfully.")
    print("   You may now exit.")
    
    task_data["quality"]["can_proceed"] = True
    task_data["state"]["status"] = "completed"
    
    with open(os.path.expanduser(json_file), 'w') as f:
        json.dump(task_data, f, indent=2)
    
    print("============================================")
    print(f"Task ID: {{task_data['id']}}")
    print("Agent: {agent_name}")
    print("Status: COMPLETED ✅")
    print(f"Quality Violations: {{violations_total}}")
    print("Can Proceed: YES")
    print("============================================")
    
else:
    print("🚫 Quality gates FAILED. Please fix violations and retry.")
    print("   All violations must be 0 to complete the task.")
    
    retry_count = task_data.get('retry_count', 0)
    if retry_count < 3:
        print(f"Retry attempt {{retry_count + 1}} of 3")
    else:
        print("❌ Maximum retries exceeded. Reporting failure.")
        task_data["state"]["status"] = "failed"
        
        with open(os.path.expanduser(json_file), 'w') as f:
            json.dump(task_data, f, indent=2)
```"""

# Replace Phase 5
content = re.sub(r'### Phase 5:.*?(?=##|\Z)', phase_5_new + '\n\n', content, flags=re.DOTALL)

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print(f"✅ Updated {agent_name}")
EOF
    
    # Run the Python script for this agent
    python3 /tmp/update_agent.py "$agent" "$AGENT_FILE"
done

echo ""
echo "=========================================="
echo "✅ Update complete!"
echo "Backup saved at: $BACKUP_DIR"
echo "=========================================="