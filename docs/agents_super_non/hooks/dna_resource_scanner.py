#!/usr/bin/env python3
"""
DNA Resource Scanner Hook
Scans relevant DNA system resources based on task ID and updates current_task.json
"""

import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any

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

def update_current_task_json(dna_resources: dict[str, Any]) -> None:
    """Update current_task.json with DNA resources"""
    task_json_path = Path(".claude/workflows/current_task.json")

    try:
        if task_json_path.exists():
            with open(task_json_path) as f:
                current_task = json.load(f)
        else:
            # Initialize from template
            template_path = Path(".claude/workflows/current_task_template.json")
            with open(template_path) as f:
                current_task = json.load(f)

        # Update DNA resources
        current_task["dna_resources"] = dna_resources
        current_task["current_phase"] = "dna_scanning"
        current_task["pipeline_progress"]["dna_scanning"] = "completed"

        # Write back
        with open(task_json_path, "w") as f:
            json.dump(current_task, f, indent=2)

        logger.info(f"✅ DNA resources scanned: {len(dna_resources['available_constants'])} constants, "
                   f"{len(dna_resources['available_types'])} types, "
                   f"{len(dna_resources['available_functions'])} functions")

    except Exception as e:
        logger.error(f"Error updating current_task.json: {e}")

def main() -> None:
    """Main hook function"""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        # Extract prompt
        prompt = input_data.get("prompt", "")

        # Check if this is an implement command
        match = re.search(r"/implement\s+(TASK-[A-Z0-9-]+|.*\.md)", prompt)
        if not match:
            sys.exit(0)

        task_ref = match.group(1)

        # Extract task ID
        task_match = re.search(r"TASK-[A-Z0-9-]+", task_ref)
        if not task_match:
            logger.warning("Could not extract task ID from prompt")
            sys.exit(0)

        task_id = task_match.group(0)

        # Get DNA system
        dna_system = extract_dna_system(task_id)
        if not dna_system:
            logger.warning(f"Could not determine DNA system for task {task_id}")
            sys.exit(0)

        logger.info(f"🧬 Scanning DNA resources for {dna_system} system...")

        # Get project root
        project_root = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))

        # Scan DNA resources
        dna_resources = scan_dna_resources(dna_system, project_root)

        # Update current_task.json
        update_current_task_json(dna_resources)

        # Add context for Claude
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    f"🧬 DNA Resources Pre-scanned for {dna_system} system:\n"
                    f"- {len(dna_resources['available_constants'])} constants available\n"
                    f"- {len(dna_resources['available_types'])} types available\n"
                    f"- {len(dna_resources['available_functions'])} functions available\n\n"
                    "These resources have been saved to current_task.json for Implementer to use."
                )
            }
        }
        print(json.dumps(output))

    except Exception as e:
        logger.error(f"❌ DNA scanner error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
