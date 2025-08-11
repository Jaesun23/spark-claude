#!/usr/bin/env python3
"""
Multi-Team Implementation Command
Enables parallel execution of up to 4 tasks simultaneously
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

def parse_command(command: str) -> List[str]:
    """Parse /multi_implement command to extract task IDs"""
    parts = command.strip().split()
    
    if not parts or parts[0] != "/multi_implement":
        return []
    
    # Extract task IDs (everything after /multi_implement)
    task_ids = parts[1:]
    
    # Validate task ID format (basic validation)
    valid_task_ids = []
    for task_id in task_ids:
        if task_id.startswith("TASK-") or task_id.startswith("task-"):
            valid_task_ids.append(task_id.upper())
    
    return valid_task_ids

def validate_tasks(task_ids: List[str]) -> Dict[str, Any]:
    """Validate task IDs and check for conflicts"""
    
    validation = {
        "valid": True,
        "task_count": len(task_ids),
        "warnings": [],
        "errors": []
    }
    
    # Check task count
    if len(task_ids) == 0:
        validation["valid"] = False
        validation["errors"].append("No valid task IDs provided")
    
    elif len(task_ids) == 1:
        validation["warnings"].append(
            "Only 1 task provided. Consider using /implement for single tasks"
        )
    
    elif len(task_ids) > 4:
        validation["warnings"].append(
            f"{len(task_ids)} tasks provided but max 4 teams available. "
            f"Tasks {', '.join(task_ids[4:])} will be queued"
        )
        task_ids = task_ids[:4]
    
    # Check for duplicates
    if len(task_ids) != len(set(task_ids)):
        validation["valid"] = False
        validation["errors"].append("Duplicate task IDs detected")
    
    validation["task_ids"] = task_ids[:4]  # Max 4 teams
    
    return validation

def generate_team_agents(num_teams: int) -> Dict[str, List[str]]:
    """Generate list of team agents needed for parallel execution"""
    
    agents = {}
    
    for i in range(1, num_teams + 1):
        team_id = f"team{i}"
        agents[team_id] = [
            f"{team_id}_implementer",
            f"{team_id}_quality",
            f"{team_id}_tester"
        ]
    
    # Add shared agents
    agents["shared"] = ["reviewer", "reporter"]
    
    return agents

def create_execution_plan(task_ids: List[str]) -> Dict[str, Any]:
    """Create detailed execution plan for parallel implementation"""
    
    num_teams = min(len(task_ids), 4)
    
    plan = {
        "command": "multi_implement",
        "timestamp": datetime.now().isoformat(),
        "task_ids": task_ids,
        "team_count": num_teams,
        "teams": {},
        "workflow": {
            "phases": [
                "initialization",
                "implementation", 
                "quality",
                "testing",
                "review",
                "report"
            ],
            "parallel_phases": ["implementation", "quality", "testing"],
            "sequential_phases": ["initialization", "review", "report"]
        },
        "agents_required": generate_team_agents(num_teams),
        "estimated_time": estimate_completion_time(num_teams, task_ids),
        "instructions": []
    }
    
    # Assign tasks to teams
    for i in range(num_teams):
        team_id = f"team{i+1}"
        plan["teams"][team_id] = {
            "task_id": task_ids[i],
            "status": "assigned",
            "context_file": f"{team_id}_current_task.json"
        }
    
    # Generate execution instructions
    plan["instructions"] = [
        f"Step 1: Initialize {num_teams} team contexts with task assignments",
        f"Step 2: Execute {num_teams} teams in parallel for implementation phase",
        "Step 3: Wait for all implementations to complete",
        f"Step 4: Execute {num_teams} teams in parallel for quality checks",
        "Step 5: Retry any teams with quality failures (max 3 retries)",
        f"Step 6: Execute {num_teams} teams in parallel for testing",
        "Step 7: Run unified architecture review across all implementations",
        "Step 8: Generate consolidated report of all team results"
    ]
    
    return plan

def estimate_completion_time(num_teams: int, task_ids: List[str]) -> Dict[str, str]:
    """Estimate completion time based on parallelization"""
    
    # Base estimates (in minutes)
    base_times = {
        "implementation": 30,
        "quality": 15,
        "testing": 20,
        "review": 10,
        "report": 5
    }
    
    # Calculate parallel vs sequential time
    sequential_time = sum(base_times.values()) * len(task_ids)
    parallel_time = sum(base_times.values()) + (len(task_ids) - num_teams) * 20
    
    return {
        "sequential_estimate": f"{sequential_time} minutes",
        "parallel_estimate": f"{parallel_time} minutes",
        "speedup": f"{sequential_time / parallel_time:.1f}x",
        "time_saved": f"{sequential_time - parallel_time} minutes"
    }

def generate_orchestration_config(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Generate configuration for the orchestrator"""
    
    config = {
        "orchestrator": "spark_multi_team_orchestrator",
        "action": "initialize_parallel_execution",
        "task_ids": plan["task_ids"],
        "team_allocation": {},
        "coordination_settings": {
            "max_parallel_teams": 4,
            "retry_on_quality_failure": True,
            "max_retries_per_team": 3,
            "lock_timeout_ms": 30000,
            "phase_timeout_minutes": 60
        },
        "quality_requirements": {
            "syntax_validation": "required",
            "type_verification": "required",
            "lint_enforcement": "required",
            "security_analysis": "required",
            "test_coverage": 95,
            "documentation_check": "required"
        },
        "output_settings": {
            "generate_team_reports": True,
            "generate_consolidated_report": True,
            "track_metrics": True,
            "log_execution": True
        }
    }
    
    # Set up team allocation
    for team_id, team_data in plan["teams"].items():
        config["team_allocation"][team_id] = team_data["task_id"]
    
    return config

def main():
    """Main entry point for multi_implement command"""
    
    # Get command from input
    if len(sys.argv) > 1:
        command = " ".join(sys.argv)
    else:
        command = input("Enter command: ")
    
    # Parse task IDs
    task_ids = parse_command(command)
    
    # Validate tasks
    validation = validate_tasks(task_ids)
    
    if not validation["valid"]:
        print(json.dumps({
            "error": "Validation failed",
            "details": validation["errors"]
        }, indent=2))
        sys.exit(1)
    
    # Show warnings if any
    if validation["warnings"]:
        for warning in validation["warnings"]:
            print(f"⚠️  {warning}")
    
    # Create execution plan
    plan = create_execution_plan(validation["task_ids"])
    
    # Generate orchestration config
    config = generate_orchestration_config(plan)
    
    # Output for 2호 to execute
    output = {
        "command": "multi_implement",
        "validation": validation,
        "execution_plan": plan,
        "orchestration_config": config,
        "next_action": "Please execute the parallel implementation workflow using the Task tool to invoke teams simultaneously",
        "example_invocation": generate_example_invocation(plan)
    }
    
    print(json.dumps(output, indent=2))
    
    # Save config for orchestrator (project-specific)
    # Use project root instead of global ~/.claude/
    import os
    project_dir = os.getenv('CLAUDE_PROJECT_DIR', '.')
    config_path = Path(project_dir) / ".claude" / "workflows" / "multi_implement_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to {config_path}")
    print(f"🚀 Ready to execute {len(validation['task_ids'])} tasks in parallel with {plan['team_count']} teams")

def generate_example_invocation(plan: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate example Task invocations for 2호"""
    
    examples = []
    
    # Implementation phase
    impl_tasks = []
    for team_id in plan["teams"]:
        task_id = plan["teams"][team_id]["task_id"]
        impl_tasks.append({
            "description": f"{team_id} Implementation - {task_id}",
            "prompt": f"Read {team_id}_current_task.json and implement {task_id}. Update JSON with results.",
            "subagent_type": f"{team_id}_implementer"
        })
    
    examples.append({
        "phase": "implementation",
        "instruction": "Call all teams simultaneously:",
        "tasks": impl_tasks
    })
    
    # Quality phase
    quality_tasks = []
    for team_id in plan["teams"]:
        quality_tasks.append({
            "description": f"{team_id} Quality Check",
            "prompt": f"Run quality gates on {team_id} implementation. Fix violations to 0.",
            "subagent_type": f"{team_id}_quality"
        })
    
    examples.append({
        "phase": "quality",
        "instruction": "After implementation completes, call all teams:",
        "tasks": quality_tasks
    })
    
    return examples

if __name__ == "__main__":
    main()