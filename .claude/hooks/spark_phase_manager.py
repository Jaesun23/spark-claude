#!/usr/bin/env python3
"""
SPARK Phase Manager - Solves phase transition hanging issues
Manages clear phase progression with explicit criteria and automatic advancement
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from spark_core_utils import StateManager, HookOutputFormatter

# Set up logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)


class PhaseDefinition:
    """Defines a workflow phase with clear progression criteria"""
    
    def __init__(
        self,
        name: str,
        description: str,
        agent: str,
        success_criteria: List[str],
        next_phase: Optional[str] = None,
        timeout_minutes: int = 30
    ):
        self.name = name
        self.description = description
        self.agent = agent
        self.success_criteria = success_criteria
        self.next_phase = next_phase
        self.timeout_minutes = timeout_minutes
    
    def check_completion_criteria(self, state: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Check if phase completion criteria are met"""
        passed_criteria = []
        failed_criteria = []
        
        for criterion in self.success_criteria:
            if self._evaluate_criterion(criterion, state):
                passed_criteria.append(criterion)
            else:
                failed_criteria.append(criterion)
        
        is_complete = len(failed_criteria) == 0
        return is_complete, failed_criteria
    
    def _evaluate_criterion(self, criterion: str, state: Dict[str, Any]) -> bool:
        """Evaluate a specific completion criterion"""
        
        # Quality gate criteria
        if criterion == "all_quality_gates_passed":
            quality_results = state.get("spark_quality_results", {})
            gates_passed = quality_results.get("gates_passed", 0)
            total_gates = quality_results.get("total_gates", 0)
            return gates_passed >= total_gates and total_gates > 0
        
        elif criterion == "syntax_errors_zero":
            quality_results = state.get("spark_quality_results", {})
            gate_results = quality_results.get("gate_results", {})
            syntax_result = gate_results.get("Syntax Validation", {})
            return syntax_result.get("passed", False)
        
        elif criterion == "linting_violations_zero":
            quality_results = state.get("spark_quality_results", {})
            gate_results = quality_results.get("gate_results", {})
            linting_result = gate_results.get("Code Linting", {})
            return linting_result.get("passed", False)
        
        elif criterion == "type_errors_zero":
            quality_results = state.get("spark_quality_results", {})
            gate_results = quality_results.get("gate_results", {})
            type_result = gate_results.get("Type Checking", {})
            return type_result.get("passed", False)
        
        elif criterion == "security_issues_zero":
            quality_results = state.get("spark_quality_results", {})
            gate_results = quality_results.get("gate_results", {})
            security_result = gate_results.get("Security Analysis", {})
            return security_result.get("passed", False)
        
        # Test coverage criteria
        elif criterion == "test_coverage_95_percent":
            test_results = state.get("test_results", {})
            coverage = test_results.get("coverage_percentage", 0)
            return coverage >= 95.0
        
        elif criterion == "all_tests_passing":
            test_results = state.get("test_results", {})
            failures = test_results.get("failures", 1)
            return failures == 0
        
        # Documentation criteria
        elif criterion == "readme_updated":
            docs_results = state.get("documentation_results", {})
            return docs_results.get("readme_updated", False)
        
        elif criterion == "api_documented":
            docs_results = state.get("documentation_results", {})
            return docs_results.get("api_documented", False)
        
        elif criterion == "docstrings_present":
            quality_results = state.get("spark_quality_results", {})
            gate_results = quality_results.get("gate_results", {})
            docs_result = gate_results.get("Documentation", {})
            return docs_result.get("passed", False)
        
        # Implementation criteria
        elif criterion == "implementation_complete":
            implementation_results = state.get("implementation_results", {})
            return implementation_results.get("complete", False)
        
        elif criterion == "code_files_created":
            implementation_results = state.get("implementation_results", {})
            files_created = implementation_results.get("files_created", [])
            return len(files_created) > 0
        
        # Hook system criteria
        elif criterion == "subagent_stop_continue":
            routing_decision = state.get("routing_decision", {})
            return routing_decision.get("next_action") == "proceed_to_next_phase"
        
        else:
            logger.warning(f"Unknown completion criterion: {criterion}")
            return False


class SPARKPhaseManager:
    """Manages SPARK workflow phases with explicit progression criteria"""
    
    def __init__(self):
        self.state_manager = StateManager()
        
        # Define standard SPARK workflow phases
        self.phases = {
            "implementation": PhaseDefinition(
                name="implementation",
                description="Code implementation with quality validation",
                agent="implementer-spark",
                success_criteria=[
                    "implementation_complete",
                    "code_files_created",
                    "all_quality_gates_passed",
                    "syntax_errors_zero",
                    "linting_violations_zero",
                    "type_errors_zero",
                    "security_issues_zero"
                ],
                next_phase="testing",
                timeout_minutes=45
            ),
            
            "testing": PhaseDefinition(
                name="testing",
                description="Comprehensive testing with 95% coverage target",
                agent="tester-spark",
                success_criteria=[
                    "all_tests_passing",
                    "test_coverage_95_percent"
                ],
                next_phase="documentation",
                timeout_minutes=30
            ),
            
            "documentation": PhaseDefinition(
                name="documentation",
                description="Complete documentation and final reporting",
                agent="documenter-spark",
                success_criteria=[
                    "readme_updated",
                    "api_documented",
                    "docstrings_present"
                ],
                next_phase=None,  # Final phase
                timeout_minutes=20
            ),
            
            "analysis": PhaseDefinition(
                name="analysis",
                description="Code analysis and investigation",
                agent="analyzer-spark",
                success_criteria=[
                    "implementation_complete"
                ],
                next_phase=None,  # Single phase workflow
                timeout_minutes=20
            ),
            
            "design": PhaseDefinition(
                name="design",
                description="UI/UX design and implementation",
                agent="designer-spark",
                success_criteria=[
                    "implementation_complete",
                    "all_quality_gates_passed"
                ],
                next_phase="testing",
                timeout_minutes=40
            )
        }
    
    def initialize_workflow(
        self,
        workflow_type: str,
        custom_phases: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Initialize a new workflow with phase management"""
        
        # Determine phases for workflow
        if custom_phases:
            phase_sequence = custom_phases
        elif workflow_type == "full_development":
            phase_sequence = ["implementation", "testing", "documentation"]
        elif workflow_type == "quick_implementation":
            phase_sequence = ["implementation"]
        elif workflow_type == "analysis_only":
            phase_sequence = ["analysis"]
        elif workflow_type == "ui_development":
            phase_sequence = ["design", "testing", "documentation"]
        else:
            phase_sequence = ["implementation", "testing", "documentation"]
        
        # Initialize workflow state
        workflow_state = {
            "workflow_id": f"spark_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "workflow_type": workflow_type,
            "phase_sequence": phase_sequence,
            "current_phase_index": 0,
            "current_phase": phase_sequence[0] if phase_sequence else None,
            "phase_statuses": {},
            "started_at": datetime.now().isoformat(),
            "estimated_completion": self._calculate_estimated_completion(phase_sequence),
            "auto_progression": True,
            "hanging_prevention": {
                "enabled": True,
                "max_retry_attempts": 3,
                "timeout_minutes": 60,
                "last_activity": datetime.now().isoformat()
            }
        }
        
        # Initialize each phase status
        for phase_name in phase_sequence:
            workflow_state["phase_statuses"][phase_name] = {
                "status": "pending",
                "started_at": None,
                "completed_at": None,
                "attempts": 0,
                "success_criteria_met": [],
                "failed_criteria": [],
                "agent_assigned": self.phases.get(phase_name, {}).get("agent", "unknown"),
                "timeout_minutes": self.phases.get(phase_name, {}).get("timeout_minutes", 30)
            }
        
        # Mark first phase as active
        if phase_sequence:
            workflow_state["phase_statuses"][phase_sequence[0]]["status"] = "active"
            workflow_state["phase_statuses"][phase_sequence[0]]["started_at"] = datetime.now().isoformat()
        
        # Update global state
        current_state = self.state_manager.read_state()
        current_state["workflow_management"] = workflow_state
        self.state_manager.write_state(current_state)
        
        return workflow_state
    
    def check_phase_progression(self, force_check: bool = False) -> Dict[str, Any]:
        """Check if current phase can progress to next phase"""
        
        current_state = self.state_manager.read_state()
        workflow_state = current_state.get("workflow_management", {})
        
        if not workflow_state.get("current_phase"):
            return {"can_progress": False, "reason": "No active workflow phase"}
        
        current_phase_name = workflow_state["current_phase"]
        current_phase = self.phases.get(current_phase_name)
        
        if not current_phase:
            return {"can_progress": False, "reason": f"Unknown phase: {current_phase_name}"}
        
        # Check completion criteria
        is_complete, failed_criteria = current_phase.check_completion_criteria(current_state)
        
        # Update phase status
        phase_status = workflow_state["phase_statuses"][current_phase_name]
        phase_status["failed_criteria"] = failed_criteria
        phase_status["success_criteria_met"] = [
            c for c in current_phase.success_criteria if c not in failed_criteria
        ]
        
        # Check for hanging conditions
        hanging_check = self._check_hanging_conditions(workflow_state, current_state)
        
        if is_complete:
            # Phase completed successfully
            phase_status["status"] = "completed"
            phase_status["completed_at"] = datetime.now().isoformat()
            
            # Progress to next phase
            next_phase_result = self._progress_to_next_phase(workflow_state)
            
            # Update state
            current_state["workflow_management"] = workflow_state
            self.state_manager.write_state(current_state)
            
            return {
                "can_progress": True,
                "reason": f"Phase '{current_phase_name}' completed successfully",
                "completed_phase": current_phase_name,
                "next_phase": next_phase_result.get("next_phase"),
                "workflow_complete": next_phase_result.get("workflow_complete", False),
                "success_criteria_met": phase_status["success_criteria_met"],
                "hanging_detected": False
            }
        
        elif hanging_check["hanging_detected"] or force_check:
            # Handle hanging situation
            return self._handle_hanging_phase(workflow_state, current_state, hanging_check)
        
        else:
            # Phase still in progress
            workflow_state["hanging_prevention"]["last_activity"] = datetime.now().isoformat()
            current_state["workflow_management"] = workflow_state
            self.state_manager.write_state(current_state)
            
            return {
                "can_progress": False,
                "reason": f"Phase '{current_phase_name}' criteria not met",
                "failed_criteria": failed_criteria,
                "success_criteria_met": phase_status["success_criteria_met"],
                "phase_status": "in_progress",
                "hanging_detected": False
            }
    
    def force_phase_progression(self, reason: str = "Manual override") -> Dict[str, Any]:
        """Force progression to next phase (emergency measure)"""
        
        current_state = self.state_manager.read_state()
        workflow_state = current_state.get("workflow_management", {})
        
        current_phase_name = workflow_state.get("current_phase")
        if not current_phase_name:
            return {"success": False, "reason": "No active phase to progress"}
        
        # Mark current phase as completed (with override flag)
        phase_status = workflow_state["phase_statuses"][current_phase_name]
        phase_status["status"] = "force_completed"
        phase_status["completed_at"] = datetime.now().isoformat()
        phase_status["override_reason"] = reason
        
        # Progress to next phase
        next_phase_result = self._progress_to_next_phase(workflow_state)
        
        # Update state
        current_state["workflow_management"] = workflow_state
        self.state_manager.write_state(current_state)
        
        logger.warning(f"🚨 Force progression applied: {current_phase_name} → {next_phase_result.get('next_phase', 'COMPLETE')}")
        logger.warning(f"   Reason: {reason}")
        
        return {
            "success": True,
            "forced_phase": current_phase_name,
            "next_phase": next_phase_result.get("next_phase"),
            "workflow_complete": next_phase_result.get("workflow_complete", False),
            "reason": reason
        }
    
    def _progress_to_next_phase(self, workflow_state: Dict[str, Any]) -> Dict[str, Any]:
        """Progress workflow to next phase"""
        
        current_index = workflow_state["current_phase_index"]
        phase_sequence = workflow_state["phase_sequence"]
        
        next_index = current_index + 1
        
        if next_index < len(phase_sequence):
            # Move to next phase
            next_phase_name = phase_sequence[next_index]
            workflow_state["current_phase_index"] = next_index
            workflow_state["current_phase"] = next_phase_name
            
            # Activate next phase
            next_phase_status = workflow_state["phase_statuses"][next_phase_name]
            next_phase_status["status"] = "active"
            next_phase_status["started_at"] = datetime.now().isoformat()
            
            return {
                "next_phase": next_phase_name,
                "workflow_complete": False
            }
        else:
            # Workflow completed
            workflow_state["current_phase"] = None
            workflow_state["completed_at"] = datetime.now().isoformat()
            workflow_state["status"] = "completed"
            
            return {
                "next_phase": None,
                "workflow_complete": True
            }
    
    def _check_hanging_conditions(
        self,
        workflow_state: Dict[str, Any],
        current_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check for hanging conditions that prevent phase progression"""
        
        hanging_prevention = workflow_state.get("hanging_prevention", {})
        if not hanging_prevention.get("enabled", False):
            return {"hanging_detected": False}
        
        current_phase_name = workflow_state.get("current_phase")
        phase_status = workflow_state["phase_statuses"][current_phase_name]
        
        # Check timeout
        started_at = phase_status.get("started_at")
        if started_at:
            from datetime import datetime, timezone
            start_time = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
            current_time = datetime.now(timezone.utc)
            elapsed_minutes = (current_time - start_time.replace(tzinfo=timezone.utc)).total_seconds() / 60
            
            timeout_minutes = phase_status.get("timeout_minutes", 30)
            if elapsed_minutes > timeout_minutes:
                return {
                    "hanging_detected": True,
                    "reason": "phase_timeout",
                    "details": f"Phase '{current_phase_name}' exceeded {timeout_minutes}min timeout",
                    "elapsed_minutes": round(elapsed_minutes, 1)
                }
        
        # Check for repeated "phase2 진행할까요?" patterns
        routing_decision = current_state.get("routing_decision", {})
        if routing_decision.get("retry_required") and phase_status.get("attempts", 0) > 2:
            return {
                "hanging_detected": True,
                "reason": "repeated_retry",
                "details": f"Phase '{current_phase_name}' has failed {phase_status['attempts']} times",
                "attempts": phase_status["attempts"]
            }
        
        # Check for missing progression criteria
        current_phase = self.phases.get(current_phase_name)
        if current_phase:
            _, failed_criteria = current_phase.check_completion_criteria(current_state)
            critical_criteria = ["syntax_errors_zero", "implementation_complete"]
            
            if any(c in failed_criteria for c in critical_criteria):
                phase_status["attempts"] = phase_status.get("attempts", 0) + 1
                if phase_status["attempts"] >= 3:
                    return {
                        "hanging_detected": True,
                        "reason": "critical_criteria_failed",
                        "details": f"Critical criteria failed after 3 attempts: {failed_criteria}",
                        "failed_criteria": failed_criteria
                    }
        
        return {"hanging_detected": False}
    
    def _handle_hanging_phase(
        self,
        workflow_state: Dict[str, Any],
        current_state: Dict[str, Any],
        hanging_check: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle hanging phase situations"""
        
        current_phase_name = workflow_state["current_phase"]
        hanging_reason = hanging_check.get("reason", "unknown")
        
        logger.warning(f"🚨 Hanging detected in phase '{current_phase_name}': {hanging_reason}")
        logger.warning(f"   Details: {hanging_check.get('details', 'No details available')}")
        
        # Update workflow state with hanging detection
        workflow_state["hanging_prevention"]["last_hanging_detection"] = datetime.now().isoformat()
        workflow_state["hanging_prevention"]["hanging_reason"] = hanging_reason
        
        # Apply hanging resolution strategy
        if hanging_reason == "phase_timeout":
            # Force progression due to timeout
            force_result = self.force_phase_progression(f"Timeout exceeded: {hanging_check.get('details')}")
            
            current_state["workflow_management"] = workflow_state
            self.state_manager.write_state(current_state)
            
            return {
                "can_progress": True,
                "reason": "Hanging resolved by timeout force progression",
                "hanging_detected": True,
                "resolution_strategy": "force_progression",
                "force_result": force_result
            }
        
        elif hanging_reason == "repeated_retry":
            # Skip problematic criteria and continue
            phase_status = workflow_state["phase_statuses"][current_phase_name]
            phase_status["status"] = "completed_with_issues"
            phase_status["completed_at"] = datetime.now().isoformat()
            phase_status["hanging_resolution"] = "skip_failed_criteria"
            
            next_phase_result = self._progress_to_next_phase(workflow_state)
            
            current_state["workflow_management"] = workflow_state
            self.state_manager.write_state(current_state)
            
            return {
                "can_progress": True,
                "reason": "Hanging resolved by skipping failed criteria",
                "hanging_detected": True,
                "resolution_strategy": "skip_criteria",
                "next_phase": next_phase_result.get("next_phase"),
                "workflow_complete": next_phase_result.get("workflow_complete", False)
            }
        
        elif hanging_reason == "critical_criteria_failed":
            # Provide specific guidance for critical failures
            failed_criteria = hanging_check.get("failed_criteria", [])
            
            current_state["workflow_management"] = workflow_state
            self.state_manager.write_state(current_state)
            
            return {
                "can_progress": False,
                "reason": "Critical criteria failures require resolution",
                "hanging_detected": True,
                "resolution_strategy": "provide_guidance",
                "failed_criteria": failed_criteria,
                "guidance": self._generate_failure_guidance(failed_criteria)
            }
        
        else:
            # Default hanging resolution
            current_state["workflow_management"] = workflow_state
            self.state_manager.write_state(current_state)
            
            return {
                "can_progress": False,
                "reason": f"Hanging detected but no resolution strategy for: {hanging_reason}",
                "hanging_detected": True,
                "resolution_strategy": "manual_intervention_required"
            }
    
    def _generate_failure_guidance(self, failed_criteria: List[str]) -> Dict[str, str]:
        """Generate specific guidance for failed criteria"""
        
        guidance = {}
        
        for criterion in failed_criteria:
            if criterion == "syntax_errors_zero":
                guidance[criterion] = "Fix syntax errors in code files. Run 'python -m py_compile file.py' or 'node --check file.js' to identify issues."
            
            elif criterion == "linting_violations_zero":
                guidance[criterion] = "Fix code style violations. Run 'ruff check .' or 'eslint .' to identify and fix issues."
            
            elif criterion == "type_errors_zero":
                guidance[criterion] = "Fix type checking errors. Run 'mypy .' or 'tsc --noEmit' to identify type issues."
            
            elif criterion == "implementation_complete":
                guidance[criterion] = "Complete the implementation. Ensure all required functions, classes, and modules are implemented."
            
            elif criterion == "all_quality_gates_passed":
                guidance[criterion] = "Ensure all Jason's 8-step strict quality gates pass: Syntax (0 errors), MyPy --strict (0 errors), Ruff --strict (0 violations), Security (OWASP + enhanced), Test Coverage 95%+, Performance, Documentation, Integration."
            
            else:
                guidance[criterion] = f"Address the failed criterion: {criterion}. Check documentation for specific requirements."
        
        return guidance
    
    def _calculate_estimated_completion(self, phase_sequence: List[str]) -> str:
        """Calculate estimated workflow completion time"""
        
        total_minutes = 0
        for phase_name in phase_sequence:
            phase = self.phases.get(phase_name)
            if phase:
                total_minutes += phase.timeout_minutes
        
        # Add buffer time
        total_minutes = int(total_minutes * 1.2)  # 20% buffer
        
        from datetime import datetime, timedelta
        estimated_time = datetime.now() + timedelta(minutes=total_minutes)
        return estimated_time.isoformat()
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status and phase information"""
        
        current_state = self.state_manager.read_state()
        workflow_state = current_state.get("workflow_management", {})
        
        if not workflow_state:
            return {"active": False, "reason": "No active workflow"}
        
        current_phase_name = workflow_state.get("current_phase")
        if not current_phase_name:
            return {
                "active": False,
                "workflow_complete": True,
                "workflow_state": workflow_state
            }
        
        # Get phase progress
        phase_statuses = workflow_state.get("phase_statuses", {})
        completed_phases = [name for name, status in phase_statuses.items() if status.get("status") == "completed"]
        total_phases = len(workflow_state.get("phase_sequence", []))
        
        progress_percentage = (len(completed_phases) / total_phases * 100) if total_phases > 0 else 0
        
        return {
            "active": True,
            "workflow_id": workflow_state.get("workflow_id"),
            "workflow_type": workflow_state.get("workflow_type"),
            "current_phase": current_phase_name,
            "phase_sequence": workflow_state.get("phase_sequence", []),
            "completed_phases": completed_phases,
            "progress_percentage": round(progress_percentage, 1),
            "phase_statuses": phase_statuses,
            "hanging_prevention": workflow_state.get("hanging_prevention", {}),
            "estimated_completion": workflow_state.get("estimated_completion")
        }


def main():
    """Main entry point for phase management operations"""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
        operation = input_data.get("operation", "check_progression")
        
        phase_manager = SPARKPhaseManager()
        
        if operation == "initialize_workflow":
            workflow_type = input_data.get("workflow_type", "full_development")
            custom_phases = input_data.get("custom_phases")
            
            result = phase_manager.initialize_workflow(workflow_type, custom_phases)
            
            output = {
                "success": True,
                "operation": "initialize_workflow",
                "result": result
            }
            
        elif operation == "check_progression":
            force_check = input_data.get("force_check", False)
            
            result = phase_manager.check_phase_progression(force_check)
            
            output = {
                "success": True,
                "operation": "check_progression", 
                "result": result
            }
            
        elif operation == "force_progression":
            reason = input_data.get("reason", "Manual force progression")
            
            result = phase_manager.force_phase_progression(reason)
            
            output = {
                "success": True,
                "operation": "force_progression",
                "result": result
            }
            
        elif operation == "workflow_status":
            result = phase_manager.get_workflow_status()
            
            output = {
                "success": True,
                "operation": "workflow_status",
                "result": result
            }
            
        else:
            output = {
                "success": False,
                "error": f"Unknown operation: {operation}",
                "available_operations": [
                    "initialize_workflow",
                    "check_progression", 
                    "force_progression",
                    "workflow_status"
                ]
            }
        
        # Output result
        print(json.dumps(output, indent=2))
        
        # Log operation
        logger.info(f"✅ Phase Manager operation '{operation}' completed")
        
        sys.exit(0)
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON input: {e}")
        error_output = {
            "success": False,
            "error": f"Invalid JSON input: {e}"
        }
        print(json.dumps(error_output))
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Phase Manager operation failed: {e}")
        logger.exception(e)
        error_output = {
            "success": False,
            "error": f"Operation failed: {e}"
        }
        print(json.dumps(error_output))
        sys.exit(1)


if __name__ == "__main__":
    main()