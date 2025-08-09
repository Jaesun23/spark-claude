#!/usr/bin/env python3
"""
SubagentStop hook - Intelligent Conditional Routing
Tracks subagent completion and provides routing decisions for 2호
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


def determine_next_action(current_task: dict) -> dict:
    """
    Determine next action based on quality gates and iteration count
    Returns routing decision for 2호 to follow
    """
    current_agent = current_task.get("current_agent", "unknown")
    current_phase = current_task.get("current_phase", "unknown")
    quality_gates = current_task.get("quality_gates", {})
    iteration = current_task.get("iteration_tracking", {}).get("current_iteration", 1)
    max_iterations = current_task.get("iteration_tracking", {}).get("max_iterations", 3)
    
    # Quality Check #1 (after Implementer)
    if current_phase == "implementation" or current_agent == "implementer":
        violations = [
            quality_gates.get("ruff_violations", 0),
            quality_gates.get("mypy_errors", 0),
            quality_gates.get("magic_numbers", 0),
            quality_gates.get("any_types", 0),
            quality_gates.get("import_violations", 0)
        ]
        
        # Filter out None values and sum
        total_violations = sum(v for v in violations if v is not None and v > 0)
        
        if total_violations > 0:
            if iteration < max_iterations:
                return {
                    "next_action": "quality_check_1",
                    "reason": f"Found {total_violations} violations. Running Quality Check #1.",
                    "specific_instructions": "Run quality agent to identify specific issues"
                }
            else:
                return {
                    "next_action": "escalate",
                    "reason": f"Max iterations ({max_iterations}) reached with {total_violations} violations",
                    "specific_instructions": "Manual intervention required - violations persist after max attempts"
                }
        else:
            return {
                "next_action": "proceed_to_tester",
                "reason": "Implementation passed initial quality checks",
                "specific_instructions": "Run tester agent to create comprehensive tests"
            }
    
    # Quality Check #1 Result (after Quality agent runs post-implementation)
    elif current_phase == "quality_check_1" or (current_agent == "quality" and "test" not in str(current_phase)):
        violations = quality_gates.get("ruff_violations", 0) or 0
        violations += quality_gates.get("mypy_errors", 0) or 0
        violations += quality_gates.get("magic_numbers", 0) or 0
        violations += quality_gates.get("any_types", 0) or 0
        
        if violations > 0:
            if iteration < max_iterations:
                # Update iteration count
                current_task["iteration_tracking"]["current_iteration"] = iteration + 1
                return {
                    "next_action": "retry_implementer",
                    "reason": f"{violations} violations found. Iteration {iteration}/{max_iterations}",
                    "specific_instructions": f"Return to implementer to fix {violations} violations. Check fix_suggestions in current_task.json"
                }
            else:
                return {
                    "next_action": "escalate",
                    "reason": f"Quality gates failed after {max_iterations} iterations",
                    "specific_instructions": "Escalate to human - persistent quality issues"
                }
        else:
            return {
                "next_action": "proceed_to_tester",
                "reason": "Quality Check #1 passed - zero violations",
                "specific_instructions": "Run tester agent to achieve 95%+ coverage"
            }
    
    # After Tester
    elif current_phase == "testing" or current_agent == "tester":
        coverage = quality_gates.get("test_coverage", 0) or 0
        
        if coverage < 95:
            return {
                "next_action": "quality_check_2",
                "reason": f"Test coverage {coverage}% below 95% target",
                "specific_instructions": "Run quality agent to check test quality and coverage"
            }
        else:
            return {
                "next_action": "quality_check_2",
                "reason": f"Tests complete with {coverage}% coverage",
                "specific_instructions": "Run quality agent for final validation"
            }
    
    # Quality Check #2 Result (after Quality agent runs post-test)
    elif current_phase == "quality_check_2" or (current_agent == "quality" and "test" in str(current_phase)):
        coverage = quality_gates.get("test_coverage", 0) or 0
        test_issues = quality_gates.get("test_quality_issues", 0) or 0
        
        if coverage < 95 or test_issues > 0:
            if iteration < max_iterations:
                return {
                    "next_action": "retry_tester",
                    "reason": f"Coverage {coverage}% or {test_issues} test quality issues",
                    "specific_instructions": "Return to tester to improve coverage and fix test issues"
                }
            else:
                return {
                    "next_action": "proceed_with_warnings",
                    "reason": f"Max iterations reached. Coverage: {coverage}%",
                    "specific_instructions": "Proceed to reviewer with warnings about test coverage"
                }
        else:
            return {
                "next_action": "proceed_to_reviewer",
                "reason": "Quality Check #2 passed",
                "specific_instructions": "Run reviewer agent for architecture validation"
            }
    
    # After Reviewer
    elif current_agent == "reviewer":
        return {
            "next_action": "proceed_to_reporter",
            "reason": "Architecture review complete",
            "specific_instructions": "Run reporter agent to generate final comprehensive report"
        }
    
    # After Reporter (workflow complete)
    elif current_agent == "reporter":
        return {
            "next_action": "workflow_complete",
            "reason": "All agents have completed successfully",
            "specific_instructions": "Workflow complete. Check final_report in current_task.json"
        }
    
    # Default/Unknown state
    else:
        return {
            "next_action": "continue",
            "reason": f"Current agent: {current_agent}, phase: {current_phase}",
            "specific_instructions": "Continue with standard workflow"
        }


def main() -> None:
    try:
        # Read JSON from stdin
        input_data = json.load(sys.stdin)
        
        # Subagent info
        session_id = input_data.get("session_id", "unknown")
        hook_event_name = input_data.get("hook_event_name", "SubagentStop")
        transcript_path = input_data.get("transcript_path", "")
        
        print(f"🤖 Subagent completed (Session: {session_id[:8]}...)", file=sys.stderr)
        
        # Update current_task.json
        task_file = os.path.join(
            os.environ.get("CLAUDE_PROJECT_DIR", "."),
            ".claude/workflows/current_task.json",
        )
        
        if os.path.exists(task_file):
            try:
                with Path(task_file).open() as f:
                    current_task = json.load(f)
                
                # Get routing decision
                routing = determine_next_action(current_task)
                
                # Update routing decision in task file
                current_task["routing_decision"] = routing
                
                # Save updated task file
                with Path(task_file).open("w") as f:
                    json.dump(current_task, f, indent=2)
                
                # Display routing decision clearly for 2호
                print("\n" + "="*60, file=sys.stderr)
                print("📍 ROUTING DECISION FOR 2호 (ORCHESTRATOR)", file=sys.stderr)
                print("="*60, file=sys.stderr)
                print(f"✅ Next Action: {routing['next_action']}", file=sys.stderr)
                print(f"📝 Reason: {routing['reason']}", file=sys.stderr)
                print(f"🎯 Instructions: {routing['specific_instructions']}", file=sys.stderr)
                print("="*60 + "\n", file=sys.stderr)
                
                # Provide specific guidance based on next action
                if routing['next_action'] == "retry_implementer":
                    print("🔄 ACTION REQUIRED: Call implementer agent again with fix_suggestions", file=sys.stderr)
                    print("   Command: Use Task tool with subagent_type='implementer'", file=sys.stderr)
                    print(f"   Include: Review fix_suggestions in current_task.json", file=sys.stderr)
                    
                elif routing['next_action'] == "quality_check_1":
                    print("🔍 ACTION REQUIRED: Run Quality Check #1", file=sys.stderr)
                    print("   Command: Use Task tool with subagent_type='quality'", file=sys.stderr)
                    print("   Focus: Check implementation quality", file=sys.stderr)
                    
                elif routing['next_action'] == "proceed_to_tester":
                    print("✅ ACTION REQUIRED: Proceed to testing phase", file=sys.stderr)
                    print("   Command: Use Task tool with subagent_type='tester'", file=sys.stderr)
                    print("   Target: 95%+ coverage", file=sys.stderr)
                    
                elif routing['next_action'] == "quality_check_2":
                    print("🔍 ACTION REQUIRED: Run Quality Check #2", file=sys.stderr)
                    print("   Command: Use Task tool with subagent_type='quality'", file=sys.stderr)
                    print("   Focus: Validate test coverage and quality", file=sys.stderr)
                    
                elif routing['next_action'] == "retry_tester":
                    print("🔄 ACTION REQUIRED: Improve test coverage", file=sys.stderr)
                    print("   Command: Use Task tool with subagent_type='tester'", file=sys.stderr)
                    print("   Focus: Add missing test cases", file=sys.stderr)
                    
                elif routing['next_action'] == "proceed_to_reviewer":
                    print("🏗️ ACTION REQUIRED: Architecture review", file=sys.stderr)
                    print("   Command: Use Task tool with subagent_type='reviewer'", file=sys.stderr)
                    
                elif routing['next_action'] == "proceed_to_reporter":
                    print("📊 ACTION REQUIRED: Generate final report", file=sys.stderr)
                    print("   Command: Use Task tool with subagent_type='reporter'", file=sys.stderr)
                    
                elif routing['next_action'] == "workflow_complete":
                    print("🎉 WORKFLOW COMPLETE!", file=sys.stderr)
                    print("   All agents have finished successfully", file=sys.stderr)
                    print("   Review final_report in current_task.json", file=sys.stderr)
                    
                elif routing['next_action'] == "escalate":
                    print("⚠️ ESCALATION REQUIRED", file=sys.stderr)
                    print("   Manual intervention needed", file=sys.stderr)
                    print("   Check current_task.json for details", file=sys.stderr)
                
            except Exception as e:
                print(f"⚠️ Error updating task status: {e}", file=sys.stderr)
        else:
            print("⚠️ current_task.json not found. Initialize workflow first.", file=sys.stderr)
        
        sys.exit(0)
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()