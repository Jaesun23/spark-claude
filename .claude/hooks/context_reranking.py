#!/usr/bin/env python3
"""
DNA v4.0 Context Re-ranking Hook

UserPromptSubmit hook that injects relevant context at the top of each prompt.
This prevents Context Rot by ensuring core decisions are always visible.

Usage: Configured in settings.json as UserPromptSubmit hook
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_project_dir() -> Path:
    """Get the project directory from environment or current working directory."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        return Path(project_dir)
    return Path.cwd()


def load_context_summary(project_dir: Path) -> dict | None:
    """Load the context summary file if it exists."""
    summary_path = project_dir / "docs" / "context" / "context_summary.json"
    if summary_path.exists():
        try:
            with open(summary_path, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None
    return None


def should_inject_context(prompt: str) -> bool:
    """Determine if context should be injected based on prompt content."""
    prompt_lower = prompt.lower()

    # Check for explicit stage commands
    stage_commands = ["/stage1", "/stage2", "/stage3", "/stage4"]
    if any(cmd in prompt_lower for cmd in stage_commands):
        return True

    # Check for DNA-related keywords
    dna_keywords = [
        "family", "nfr", "adr", "blueprint", "architecture",
        "패밀리", "아키텍처", "청사진", "설계",
        "layer 1", "layer 2", "layer 3",
        "stage 1", "stage 2", "stage 3", "stage 4",
        "bootstrap", "constraint", "제약",
    ]
    if any(keyword in prompt_lower for keyword in dna_keywords):
        return True

    return False


def get_current_stage(prompt: str) -> int:
    """Detect current stage from prompt content."""
    prompt_lower = prompt.lower()

    if "/stage1" in prompt_lower or "stage 1" in prompt_lower:
        return 1
    elif "/stage2" in prompt_lower or "stage 2" in prompt_lower:
        return 2
    elif "/stage3" in prompt_lower or "stage 3" in prompt_lower:
        return 3
    elif "/stage4" in prompt_lower or "stage 4" in prompt_lower:
        return 4

    return 0  # No specific stage detected


def build_context_prefix(summary: dict, current_stage: int) -> str:
    """Build the context prefix to inject into the prompt."""
    if not summary:
        return ""

    core = summary.get("core_decisions", {})

    # Build context based on what's been decided
    context_parts = []

    # Always include family if decided
    family = core.get("family", {})
    if family.get("code"):
        context_parts.append(f"Family: {family['code']}")

    # Include NFR priority if decided
    nfr = core.get("nfr_priority", {})
    if nfr.get("order"):
        context_parts.append(f"NFR Priority: {', '.join(nfr['order'])}")

    # Include key constraints if in stage 2+
    if current_stage >= 2:
        constraints = core.get("key_constraints", {})
        if constraints.get("items"):
            context_parts.append(f"Key Constraints: {', '.join(constraints['items'][:3])}")

    # Include tech stack if in stage 3+
    if current_stage >= 3:
        tech = core.get("tech_stack", {})
        if tech.get("items"):
            tech_items = [f"{k}: {v}" for k, v in list(tech["items"].items())[:3]]
            context_parts.append(f"Tech Stack: {'; '.join(tech_items)}")

    if not context_parts:
        return ""

    # Format the prefix
    prefix = """[DNA v4.0 CORE CONTEXT - Must Comply]
{}

These decisions must be respected in all work.
---

""".format("\n".join(context_parts))

    return prefix


def main():
    """Main hook function."""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # If we can't parse input, just exit successfully (don't block)
        sys.exit(0)

    prompt = input_data.get("prompt", "")

    # Check if this prompt is DNA-related
    if not should_inject_context(prompt):
        # Not DNA-related, just pass through without injection
        sys.exit(0)

    # Get project directory
    project_dir = get_project_dir()

    # Load context summary
    summary = load_context_summary(project_dir)

    if not summary:
        # No context yet, just pass through
        sys.exit(0)

    # Check if any core decisions have been made
    core = summary.get("core_decisions", {})
    family_code = core.get("family", {}).get("code", "")
    if not family_code:
        # No decisions yet, nothing to inject
        sys.exit(0)

    # Detect current stage
    current_stage = get_current_stage(prompt)
    if current_stage == 0:
        # Try to get from summary
        current_stage = summary.get("current_stage", 0)

    # Build context prefix
    prefix = build_context_prefix(summary, current_stage)

    if prefix:
        # Output the modified prompt
        # Note: For UserPromptSubmit, we print to stdout to add context
        print(prefix)

    sys.exit(0)


if __name__ == "__main__":
    main()
