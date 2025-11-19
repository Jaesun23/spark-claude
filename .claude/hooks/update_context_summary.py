#!/usr/bin/env python3
"""
DNA v4.0 Context Summary Update Hook

PostToolUse hook that updates context_summary.json when stage output files are written.
This ensures the summary always reflects the latest decisions.

Usage: Configured in settings.json as PostToolUse hook for Write tool
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def get_project_dir() -> Path:
    """Get the project directory from environment or current working directory."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        return Path(project_dir)
    return Path.cwd()


def extract_stage_number(file_path: str) -> int | None:
    """Extract stage number from file path like 'stage1_output.json'."""
    match = re.search(r"stage(\d+)_output\.json", file_path)
    if match:
        return int(match.group(1))
    return None


def load_stage_output(file_path: Path) -> dict | None:
    """Load a stage output file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError, FileNotFoundError):
        return None


def update_context_summary(project_dir: Path, stage_num: int, stage_data: dict) -> bool:
    """Update the context summary with new stage data."""
    summary_path = project_dir / "docs" / "context" / "context_summary.json"

    # Load existing summary or create new one
    if summary_path.exists():
        try:
            with open(summary_path, encoding="utf-8") as f:
                summary = json.load(f)
        except (json.JSONDecodeError, OSError):
            summary = create_empty_summary()
    else:
        summary = create_empty_summary()

    # Update based on stage
    if stage_num == 1:
        update_from_stage1(summary, stage_data)
    elif stage_num == 2:
        update_from_stage2(summary, stage_data)
    elif stage_num == 3:
        update_from_stage3(summary, stage_data)
    elif stage_num == 4:
        update_from_stage4(summary, stage_data)

    # Update common fields
    summary["current_stage"] = max(summary.get("current_stage", 0), stage_num)
    if stage_num not in summary.get("completed_stages", []):
        summary.setdefault("completed_stages", []).append(stage_num)
        summary["completed_stages"].sort()

    summary["validation_status"][f"stage{stage_num}"] = True
    summary["last_updated"] = datetime.now().isoformat()

    # Save updated summary
    try:
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        return True
    except OSError:
        return False


def create_empty_summary() -> dict:
    """Create an empty context summary structure."""
    return {
        "$schema": "DNA v4.0 Context Summary - Cross-Stage Reference",
        "version": "1.0",
        "project_name": "",
        "current_stage": 0,
        "completed_stages": [],
        "core_decisions": {
            "family": {"code": "", "decided_at": ""},
            "nfr_priority": {"order": [], "decided_at": ""},
            "key_constraints": {"items": [], "decided_at": ""},
            "tech_stack": {"items": {}, "decided_at": ""},
        },
        "stage_outputs": {
            "stage1": "docs/context/stage1_output.json",
            "stage2": "docs/context/stage2_output.json",
            "stage3": "docs/context/stage3_output.json",
            "stage4": "docs/context/stage4_output.json",
        },
        "validation_status": {
            "stage1": False,
            "stage2": False,
            "stage3": False,
            "stage4": False,
        },
        "last_updated": "",
    }


def update_from_stage1(summary: dict, stage_data: dict) -> None:
    """Update summary from Stage 1 output."""
    # Extract family
    family = stage_data.get("family", {})
    if family.get("code"):
        summary["core_decisions"]["family"] = {
            "code": family["code"],
            "decided_at": "stage1",
        }

    # Extract NFR priority
    nfr = stage_data.get("nfr_priority", {})
    if nfr.get("order"):
        summary["core_decisions"]["nfr_priority"] = {
            "order": nfr["order"],
            "decided_at": "stage1",
        }

    # Extract project name if available
    if stage_data.get("project_name"):
        summary["project_name"] = stage_data["project_name"]


def update_from_stage2(summary: dict, stage_data: dict) -> None:
    """Update summary from Stage 2 output."""
    # Extract key constraints
    constraints = []

    layer3 = stage_data.get("layer3_constraints", {})
    tech = layer3.get("technical", {})
    infra = layer3.get("infrastructure", {})

    # Add tech mandates
    if tech.get("tech_stack_mandates"):
        constraints.extend(tech["tech_stack_mandates"][:2])

    # Add compliance requirements
    if infra.get("compliance_requirements"):
        constraints.extend(infra["compliance_requirements"][:2])

    if constraints:
        summary["core_decisions"]["key_constraints"] = {
            "items": constraints,
            "decided_at": "stage2",
        }


def update_from_stage3(summary: dict, stage_data: dict) -> None:
    """Update summary from Stage 3 output."""
    # Extract bootstrap tech stack
    bootstrap = stage_data.get("bootstrap_elements", {})
    if bootstrap:
        summary["core_decisions"]["tech_stack"] = {
            "items": {k: v for k, v in bootstrap.items() if v},
            "decided_at": "stage3",
        }


def update_from_stage4(summary: dict, stage_data: dict) -> None:
    """Update summary from Stage 4 output."""
    # Stage 4 doesn't add new core decisions, but we mark it complete
    pass


def main():
    """Main hook function."""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Get tool information
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only process Write tool
    if tool_name != "Write":
        sys.exit(0)

    # Get file path
    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Check if this is a stage output file
    stage_num = extract_stage_number(file_path)
    if stage_num is None:
        sys.exit(0)

    # Get project directory
    project_dir = get_project_dir()

    # Load the stage output that was just written
    stage_output_path = Path(file_path)
    stage_data = load_stage_output(stage_output_path)

    if not stage_data:
        sys.exit(0)

    # Update context summary
    success = update_context_summary(project_dir, stage_num, stage_data)

    if success:
        # Log to stderr (visible to user)
        print(
            f"[DNA] Context summary updated for Stage {stage_num}",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
