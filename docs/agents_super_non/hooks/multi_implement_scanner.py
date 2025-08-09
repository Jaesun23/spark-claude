#!/usr/bin/env python3
"""
Multi-Implement Scanner Hook
Handles /multi_implement commands by scanning DNA resources for each team assignment
"""

import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, List

# Set up logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

# DNA system mapping
DNA_SYSTEM_MAP = {
    "S": "skeletal",
    "N": "nervous",
    "I": "immune",
    "E": "endocrine",
    "C": "circulatory",
    "SE": "sensory",
    "D": "digestive",
    "R": "reproductive"
}

def extract_dna_system(task_id: str) -> str:
    """Extract DNA system from task ID (e.g., TASK-N1-01 -> nervous)"""
    match = re.match(r"TASK-([A-Z]+)\d+-\d+", task_id)
    if match:
        prefix = match.group(1)
        return DNA_SYSTEM_MAP.get(prefix, "")
    return ""

def scan_dna_resources(dna_system: str, project_root: Path) -> dict[str, Any]:
    """Scan DNA system for available resources"""
    resources = {
        "target_system": dna_system,
        "available_constants": [],
        "available_types": [],
        "available_functions": [],
        "required_imports": []
    }

    dna_path = project_root / "src" / "dna" / dna_system

    if not dna_path.exists():
        logger.warning(f"DNA system path does not exist: {dna_path}")
        return resources

    # Scan for Python files
    for py_file in dna_path.glob("*.py"):
        if py_file.name == "__init__.py":
            continue

        try:
            with open(py_file, encoding="utf-8") as f:
                content = f.read()

            # Extract constants (UPPER_CASE variables)
            constants = re.findall(r"^([A-Z_]+)\s*=", content, re.MULTILINE)
            resources["available_constants"].extend(constants)

            # Extract types (TypedDict, Enum, Protocol, etc.)
            type_patterns = [
                r"class\s+(\w+)\(TypedDict\)",
                r"class\s+(\w+)\(Enum\)",
                r"class\s+(\w+)\(Protocol\)",
                r"class\s+(\w+)\(BaseModel\)",
                r"(\w+)\s*=\s*TypeVar",
                r"(\w+)\s*=\s*Union\[",
                r"(\w+)\s*=\s*dict\[",
                r"(\w+)\s*=\s*list\["
            ]
            for pattern in type_patterns:
                types_found = re.findall(pattern, content)
                resources["available_types"].extend(types_found)

            # Extract functions
            functions = re.findall(r"^def\s+(\w+)\(", content, re.MULTILINE)
            resources["available_functions"].extend(functions)

            # Generate import statements
            module_path = f"src.dna.{dna_system}.{py_file.stem}"

            if constants:
                resources["required_imports"].append(
                    f"from {module_path} import {', '.join(set(constants[:5]))}"
                )
            if types_found:
                resources["required_imports"].append(
                    f"from {module_path} import {', '.join(set(types_found[:5]))}"
                )

        except Exception as e:
            logger.error(f"Error scanning {py_file}: {e}")

    # Always include Endocrine constants
    if dna_system != "endocrine":
        endocrine_path = project_root / "src" / "dna" / "endocrine" / "constants.py"
        if endocrine_path.exists():
            resources["required_imports"].append(
                "from src.dna.endocrine.constants import (...relevant constants...)"
            )

    # Always include Skeletal types
    if dna_system != "skeletal":
        skeletal_path = project_root / "src" / "dna" / "skeletal" / "types.py"
        if skeletal_path.exists():
            resources["required_imports"].append(
                "from src.dna.skeletal.types import (...relevant types...)"
            )

    # Remove duplicates
    resources["available_constants"] = list(set(resources["available_constants"]))
    resources["available_types"] = list(set(resources["available_types"]))
    resources["available_functions"] = list(set(resources["available_functions"]))

    return resources

def update_team_task_json(team_id: str, task_id: str, dna_resources: dict[str, Any]) -> None:
    """Update team-specific current_task.json with DNA resources"""
    task_json_path = Path(f".claude/workflows/{team_id}_current_task.json")

    try:
        if task_json_path.exists():
            with open(task_json_path) as f:
                current_task = json.load(f)
        else:
            # Initialize basic structure
            current_task = {
                "team_id": team_id,
                "task_id": None,
                "status": "READY",
                "dna_resources": {},
                "assigned_checklist": None
            }

        # Update DNA resources and task assignment
        current_task["dna_resources"] = dna_resources
        current_task["task_id"] = task_id
        current_task["assigned_checklist"] = task_id
        current_task["status"] = "ASSIGNED"

        # Write back
        with open(task_json_path, "w") as f:
            json.dump(current_task, f, indent=2)

        logger.info(f"✅ {team_id}: {task_id} -> {dna_resources['target_system']} system")

    except Exception as e:
        logger.error(f"Error updating {team_id}_current_task.json: {e}")

def update_coordination_json(team_assignments: list[tuple[str, str]]) -> None:
    """Update multi_task_coordination.json with team assignments"""
    coord_json_path = Path(".claude/workflows/multi_task_coordination.json")

    try:
        if coord_json_path.exists():
            with open(coord_json_path) as f:
                coordination = json.load(f)
        else:
            logger.error(f"Coordination file not found: {coord_json_path}")
            return

        # Update team assignments
        coordination["overall_status"] = "ASSIGNED"
        coordination["current_phase"] = "implementation"

        for team_id, task_id in team_assignments:
            if team_id in coordination["teams"]:
                coordination["teams"][team_id]["assigned_task"] = task_id
                coordination["teams"][team_id]["status"] = "ASSIGNED"
                coordination["teams"][team_id]["current_phase"] = "implementation"

        # Mark unused teams as inactive
        used_teams = {team_id for team_id, _ in team_assignments}
        all_teams = {"team1", "team2", "team3", "team4"}
        for team_id in all_teams - used_teams:
            if team_id in coordination["teams"]:
                coordination["teams"][team_id]["status"] = "INACTIVE"

        # Write back
        with open(coord_json_path, "w") as f:
            json.dump(coordination, f, indent=2)

        logger.info(f"🎯 Multi-team coordination updated: {len(team_assignments)} teams assigned")

    except Exception as e:
        logger.error(f"Error updating coordination JSON: {e}")

def main() -> None:
    """Main hook function"""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        # Extract prompt
        prompt = input_data.get("prompt", "")

        # Check if this is a multi_implement command
        match = re.search(r"/multi_implement\s+((?:TASK-[A-Z0-9-]+\s*)+)", prompt)
        if not match:
            sys.exit(0)

        # Extract all task IDs
        task_string = match.group(1)
        task_ids = re.findall(r"TASK-[A-Z0-9-]+", task_string)

        if not task_ids:
            logger.warning("No valid task IDs found in multi_implement command")
            sys.exit(0)

        if len(task_ids) > 4:
            logger.warning(f"Too many tasks ({len(task_ids)}), limiting to 4")
            task_ids = task_ids[:4]

        logger.info(f"🚀 Multi-implement detected: {len(task_ids)} tasks")

        # Get project root
        project_root = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))

        # Assign tasks to teams sequentially
        teams = ["team1", "team2", "team3", "team4"]
        team_assignments = []

        for i, task_id in enumerate(task_ids):
            team_id = teams[i]

            # Get DNA system for this task
            dna_system = extract_dna_system(task_id)
            if not dna_system:
                logger.warning(f"Could not determine DNA system for task {task_id}")
                continue

            logger.info(f"🧬 {team_id}: Scanning {dna_system} system for {task_id}...")

            # Scan DNA resources
            dna_resources = scan_dna_resources(dna_system, project_root)

            # Update team-specific JSON
            update_team_task_json(team_id, task_id, dna_resources)

            team_assignments.append((team_id, task_id))

        # Update coordination JSON
        update_coordination_json(team_assignments)

        # Add context for Claude
        assignment_summary = "\n".join([
            f"- {team_id}: {task_id}" for team_id, task_id in team_assignments
        ])

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    f"🚀 Multi-Team Implementation Prepared:\n"
                    f"{assignment_summary}\n\n"
                    f"All team-specific DNA resources have been scanned and saved to team JSON files.\n"
                    f"Ready for parallel execution with {len(team_assignments)} teams."
                )
            }
        }
        print(json.dumps(output))

    except Exception as e:
        logger.error(f"❌ Multi-implement scanner error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
