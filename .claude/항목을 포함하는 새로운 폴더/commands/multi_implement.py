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
    """Parse /multi_implement or /multi-implement command to extract task IDs"""
    parts = command.strip().split()
    
    if not parts or (parts[0] != "/multi_implement" and parts[0] != "/multi-implement"):
        return []
    
    # Extract task IDs (everything after command)
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
            f"{team_id}-implementer-spark",  # Correct SPARK agent name
            f"{team_id}-tester-spark",        # Correct SPARK agent name
            f"{team_id}-documenter-spark"     # Correct SPARK agent name
        ]
    
    # No shared agents in SPARK v4.1
    
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
                "Phase 0: Initialization",
                "Phase 1-3: Implementation", 
                "Phase 4: Testing",
                "Phase 5A: Documentation",
                "Phase 5B: Quality Gates"  # v4.1 8-step quality validation
            ],
            "parallel_phases": ["Phase 1-3: Implementation", "Phase 4: Testing"],
            "sequential_phases": ["Phase 0: Initialization", "Phase 5A: Documentation", "Phase 5B: Quality Gates"]
        },
        "agents_required": generate_team_agents(num_teams),
        "estimated_time": estimate_completion_time(num_teams, task_ids),
        "instructions": [],
        "initialization_required": True  # Flag to indicate team JSON reset needed
    }
    
    # Assign tasks to teams
    for i in range(num_teams):
        team_id = f"team{i+1}"
        plan["teams"][team_id] = {
            "task_id": task_ids[i],
            "status": "assigned",
            "context_file": f"{team_id}_current_task.json"
        }
    
    # Generate execution instructions (v4.1 Phase structure)
    plan["instructions"] = [
        f"Phase 0: Initialize {num_teams} team JSON files with v4.1 structure",
        f"Phase 1-3: Execute {num_teams} teams in parallel for implementation",
        f"Phase 4: Execute {num_teams} teams in parallel for testing (95% coverage)",
        f"Phase 5A: Execute {num_teams} teams in parallel for documentation",
        f"Phase 5B: Run 8-step quality gates verification",
        "➡️ Each team MUST update quality section with actual measurements",
        "➡️ Run: echo '{\"subagent\": \"team[N]-implementer-spark\", \"self_check\": true}' | python3 ~/.claude/hooks/spark_quality_gates.py",
        "❌ 모든 오류가 0이 아니면 작업종료 불가능합니다"
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

def initialize_team_json_files(plan: Dict[str, Any], config_path: Path) -> None:
    """Initialize team JSON files with v4.1 structure"""
    workflows_dir = config_path.parent
    
    for team_id, team_data in plan["teams"].items():
        team_file = workflows_dir / f"{team_id}_current_task.json"
        
        # Create v4.1 compliant team JSON
        team_json = {
            "id": f"spark_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{team_id}",
            "version": "4.1",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            
            "task": {
                "prompt": f"Task {team_data['task_id']} assigned to {team_id}",
                "complexity": 0.5,
                "execution_mode": "parallel",
                "team_id": team_id
            },
            
            "state": {
                "current_agent": f"{team_id}-implementer-spark",
                "current_phase": 0,
                "phase_name": "Phase 0: Initialization",
                "status": "pending",
                "pipeline": [
                    f"{team_id}-implementer-spark",
                    f"{team_id}-tester-spark",
                    f"{team_id}-documenter-spark"
                ],
                "completed_agents": [],
                "errors": []
            },
            
            "quality": {
                "step_1_architecture": {"imports": 0, "circular": 0, "domain": 0},
                "step_2_foundation": {"syntax": 0, "types": 0},
                "step_3_standards": {"formatting": 0, "conventions": 0},
                "step_4_operations": {"logging": 0, "security": 0, "config": 0},
                "step_5_quality": {"linting": 0, "complexity": 0},
                "step_6_testing": {"coverage": -1},
                "step_7_documentation": {"docstrings": 0, "readme": 0},
                "step_8_integration": {"final": 0},
                "violations_total": 0,
                "can_proceed": False
            },
            
            "output": {
                "files": {"created": [], "modified": []},
                "tests": {"unit": 0, "integration": 0, "e2e": 0},
                "docs": {"api": False, "readme": False, "changelog": False}
            }
        }
        
        # Write team JSON file (overwriting any existing file)
        with open(team_file, 'w') as f:
            json.dump(team_json, f, indent=2)
        
        print(f"✅ Initialized {team_file.name} with {team_data['task_id']}")

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
            "step_1_architecture": "0 violations (imports, circular, domain)",
            "step_2_foundation": "0 errors (syntax, types)",
            "step_3_standards": "0 violations (formatting, conventions)",
            "step_4_operations": "0 issues (logging, security, config)",
            "step_5_quality": "0 violations (linting, complexity)",
            "step_6_testing": "95% coverage minimum",
            "step_7_documentation": "0 missing (docstrings, readme)",
            "step_8_integration": "0 errors (final checks)",
            "enforcement": "모든 오류가 0이 아니면 작업종료 불가능합니다"
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
    
    # Initialize team JSON files with task assignments
    initialize_team_json_files(plan, config_path)
    
    print(f"\n✅ Configuration saved to {config_path}")
    print(f"🚀 Ready to execute {len(validation['task_ids'])} tasks in parallel with {plan['team_count']} teams")
    print("\n⚠️  IMPORTANT v4.1 Requirements:")
    print("  1. Each team MUST update quality section in Phase 5B")
    print("  2. All 8 quality steps MUST have 0 violations")
    print("  3. Run self-validation before completion:")
    print("     echo '{\"subagent\": \"teamN-implementer-spark\", \"self_check\": true}' | \\")
    print("     python3 ~/.claude/hooks/spark_quality_gates.py")
    print("\n🚫 품질게이트를 통과하지 못하면 작업종료 불가능합니다!")

def generate_example_invocation(plan: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate example Task invocations for 2호"""
    
    examples = []
    
    # Implementation phase
    impl_tasks = []
    for team_id in plan["teams"]:
        task_id = plan["teams"][team_id]["task_id"]
        impl_tasks.append({
            "description": f"{team_id} Implementation - {task_id}",
            "prompt": f"Read {team_id}_current_task.json and implement {task_id}. Follow v4.1 Phase structure. Update quality section in Phase 5B.",
            "subagent_type": f"{team_id}-implementer-spark"  # Correct agent name
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
            "description": f"{team_id} Testing",
            "prompt": f"Test {team_id} implementation. Achieve 95% coverage. Update JSON quality.step_6_testing.coverage.",
            "subagent_type": f"{team_id}-tester-spark"  # Correct agent name
        })
    
    examples.append({
        "phase": "quality",
        "instruction": "After implementation completes, call all teams:",
        "tasks": quality_tasks
    })
    
    return examples

if __name__ == "__main__":
    main()