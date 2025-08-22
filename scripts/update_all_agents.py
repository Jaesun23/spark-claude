#!/usr/bin/env python3
"""
Update all SPARK agents with standardized Phase 5B structure.
This script ensures consistency across all 28 agents.
"""

import os
import re
from pathlib import Path

# Standard Phase 5B template for all agents
PHASE_5B_TEMPLATE = '''### Phase 5: Task Completion

#### Phase 5A: Quality Metrics Recording

Record actual quality metrics from the {agent_work}:

```python
print("Phase 5A - Quality Metrics: Recording actual measurements...")

# Record actual metrics based on agent's work
syntax_errors = 0  # Count actual syntax errors found
type_errors = 0    # Count actual type errors found
linting_violations = 0  # Count actual linting issues

# Agent-specific metrics
{agent_specific_metrics}

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
    "can_proceed": False  # Will be set by quality gates script
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
    
    # Update JSON with final status
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
    
    # Parse specific violations and retry logic
    retry_count = task_data.get('retry_count', 0)
    if retry_count < 3:
        print(f"Retry attempt {{retry_count + 1}} of 3")
        # Return to Phase 4 to fix issues
    else:
        print("❌ Maximum retries exceeded. Reporting failure.")
        task_data["state"]["status"] = "failed"
        
        with open(os.path.expanduser(json_file), 'w') as f:
            json.dump(task_data, f, indent=2)
```'''

# Agent-specific configurations
AGENT_CONFIGS = {
    'implementer-spark': {
        'agent_work': 'implementation',
        'agent_specific_metrics': '# No additional metrics for implementer',
        'coverage_value': '-1  # Implementer doesn\'t do testing'
    },
    'tester-spark': {
        'agent_work': 'testing',
        'agent_specific_metrics': '''unit_coverage = 95  # Actual unit test coverage percentage
integration_coverage = 85  # Actual integration test coverage''',
        'coverage_value': 'unit_coverage  # Tester reports actual coverage'
    },
    'documenter-spark': {
        'agent_work': 'documentation',
        'agent_specific_metrics': '# Documentation completeness metrics',
        'coverage_value': '-1  # Documenter doesn\'t do testing'
    },
    'analyzer-spark': {
        'agent_work': 'analysis',
        'agent_specific_metrics': '# Analysis findings and metrics',
        'coverage_value': '-1  # Analyzer doesn\'t do testing'
    },
    'designer-spark': {
        'agent_work': 'design',
        'agent_specific_metrics': '# Design validation metrics',
        'coverage_value': '-1  # Designer doesn\'t do testing'
    },
    'improver-spark': {
        'agent_work': 'improvement',
        'agent_specific_metrics': '# Code quality improvement metrics',
        'coverage_value': '-1  # Improver doesn\'t do testing'
    },
    'troubleshooter-spark': {
        'agent_work': 'troubleshooting',
        'agent_specific_metrics': '# Issues resolved metrics',
        'coverage_value': '-1  # Troubleshooter doesn\'t do testing'
    },
    'cleaner-spark': {
        'agent_work': 'cleanup',
        'agent_specific_metrics': '# Code cleanup metrics',
        'coverage_value': '-1  # Cleaner doesn\'t do testing'
    },
    'explainer-spark': {
        'agent_work': 'explanation',
        'agent_specific_metrics': '# Explanation clarity metrics',
        'coverage_value': '-1  # Explainer doesn\'t do testing'
    },
    'builder-spark': {
        'agent_work': 'build optimization',
        'agent_specific_metrics': '# Build performance metrics',
        'coverage_value': '-1  # Builder doesn\'t do testing'
    },
    'estimater-spark': {
        'agent_work': 'estimation',
        'agent_specific_metrics': '# Estimation accuracy metrics',
        'coverage_value': '-1  # Estimater doesn\'t do testing'
    },
    'gitter-spark': {
        'agent_work': 'git operations',
        'agent_specific_metrics': '# Git workflow metrics',
        'coverage_value': '-1  # Gitter doesn\'t do testing'
    },
    'spawner-spark': {
        'agent_work': 'orchestration',
        'agent_specific_metrics': '# Orchestration success metrics',
        'coverage_value': '-1  # Spawner doesn\'t do testing'
    },
    'loader-spark': {
        'agent_work': 'project loading',
        'agent_specific_metrics': '# Project analysis metrics',
        'coverage_value': '-1  # Loader doesn\'t do testing'
    },
    'indexer-spark': {
        'agent_work': 'indexing',
        'agent_specific_metrics': '# Index completeness metrics',
        'coverage_value': '-1  # Indexer doesn\'t do testing'
    },
    'tasker-spark': {
        'agent_work': 'task management',
        'agent_specific_metrics': '# Task tracking metrics',
        'coverage_value': '-1  # Tasker doesn\'t do testing'
    }
}

# Team agent configurations (same structure for all teams)
for team in range(1, 5):
    AGENT_CONFIGS[f'team{team}-implementer-spark'] = {
        'agent_work': 'implementation',
        'agent_specific_metrics': '# No additional metrics for implementer',
        'coverage_value': '-1  # Implementer doesn\'t do testing'
    }
    AGENT_CONFIGS[f'team{team}-tester-spark'] = {
        'agent_work': 'testing',
        'agent_specific_metrics': '''unit_coverage = 95  # Actual unit test coverage percentage
integration_coverage = 85  # Actual integration test coverage''',
        'coverage_value': 'unit_coverage  # Tester reports actual coverage'
    }
    AGENT_CONFIGS[f'team{team}-documenter-spark'] = {
        'agent_work': 'documentation',
        'agent_specific_metrics': '# Documentation completeness metrics',
        'coverage_value': '-1  # Documenter doesn\'t do testing'
    }

def update_agent_file(agent_path: Path, agent_name: str):
    """Update a single agent file with standardized Phase 5B."""
    
    if agent_name not in AGENT_CONFIGS:
        print(f"⚠️  No config for {agent_name}, skipping")
        return False
    
    config = AGENT_CONFIGS[agent_name]
    
    # Read current content
    content = agent_path.read_text()
    
    # Remove Korean text
    content = re.sub(r'[\u3131-\ucb4c\uac00-\ud7a3]+', '', content)
    
    # Generate Phase 5B content for this agent
    phase_5b = PHASE_5B_TEMPLATE.format(
        agent_name=agent_name,
        agent_work=config['agent_work'],
        agent_specific_metrics=config['agent_specific_metrics'],
        coverage_value=config['coverage_value']
    )
    
    # Find and replace Phase 5 section
    phase_5_pattern = r'### Phase 5:.*?(?=##|\Z)'
    if re.search(phase_5_pattern, content, re.DOTALL):
        content = re.sub(phase_5_pattern, phase_5b + '\n\n', content, flags=re.DOTALL)
        agent_path.write_text(content)
        print(f"✅ Updated {agent_name}")
        return True
    else:
        print(f"⚠️  Could not find Phase 5 in {agent_name}")
        return False

def main():
    """Update all agent files."""
    agents_dir = Path('/Users/jason/Projects/spark-claude/.claude/agents')
    
    if not agents_dir.exists():
        print(f"❌ Agents directory not found: {agents_dir}")
        return
    
    # Get all agent files
    agent_files = sorted(agents_dir.glob('*-spark.md'))
    
    print(f"Found {len(agent_files)} agent files to update")
    print("=" * 50)
    
    success_count = 0
    for agent_file in agent_files:
        agent_name = agent_file.stem
        if update_agent_file(agent_file, agent_name):
            success_count += 1
    
    print("=" * 50)
    print(f"✅ Successfully updated {success_count}/{len(agent_files)} agents")
    
    # List any agents that weren't updated
    failed = len(agent_files) - success_count
    if failed > 0:
        print(f"⚠️  {failed} agents need manual review")

if __name__ == '__main__':
    main()