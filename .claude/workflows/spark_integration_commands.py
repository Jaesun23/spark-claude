#!/usr/bin/env python3
"""
SPARK Integration Commands
Commands that integrate with Claude Code following Jason's patterns:
- Task Task Task → 시작! 
- JSON-based context relay
- 2호 orchestration support
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))
sys.path.insert(0, str(Path(__file__).parent))

from spark_core_utils import StateManager
from spark_phase_manager import SPARKPhaseManager
from spark_pipeline_commands import (
    PipelineCommandFactory, 
    TaskDoubleCaller, 
    SequenceCommand,
    ParallelCommand
)


class SparkIntegrationCommands:
    """Main integration commands for SPARK system"""
    
    def __init__(self):
        self.state_manager = StateManager()
        self.phase_manager = SPARKPhaseManager()
        self.factory = PipelineCommandFactory()
        
    def task_task_task_sijak(self, task_description: str, agents_override: List[str] = None) -> Dict[str, Any]:
        """
        Implement Jason's Task Task Task Task → 시작! pattern
        
        This creates the simultaneous Task calls for parallel agent execution
        NO sequential confirmation steps - all agents start immediately
        """
        print("🚀 Task Task Task Task → 시작!")
        print(f"📋 Task: {task_description}")
        
        # Get current state
        state = self.state_manager.read_state()
        
        # If no state exists, need persona routing first
        if not state.get("personas") and not agents_override:
            return {
                "status": "routing_required",
                "message": "Please run persona routing first",
                "next_command": f'echo \'{{"prompt": "{task_description}"}}\' | python3 .claude/hooks/spark_persona_router.py'
            }
        
        # Determine agents to call simultaneously
        if agents_override:
            simultaneous_agents = agents_override
        else:
            # Extract task context and determine optimal agent combination
            personas = state.get("personas", [])
            complexity = state.get("complexity", 0.5)
            simultaneous_agents = self._determine_simultaneous_agents(personas, complexity, task_description)
        
        print(f"⚡ Calling {len(simultaneous_agents)} agents SIMULTANEOUSLY:")
        for i, agent in enumerate(simultaneous_agents, 1):
            print(f"   Task {i}: {agent}")
        print("🚀 시작!")
        
        # Create the parallel execution command
        parallel_cmd = ParallelCommand(simultaneous_agents)
        result = parallel_cmd.execute()
        
        # Add simultaneous calling metadata
        result["sijak_pattern"] = "Task Task Task Task → 시작!"
        result["simultaneous_agents"] = simultaneous_agents
        result["parallel_execution"] = True
        result["no_sequential_confirmation"] = True
        
        return result
    
    def dongsi_hocul(self, primary_task: str, support_tasks: List[str] = None, agents_list: List[str] = None) -> Dict[str, Any]:
        """
        Task 동시 호출 (Simultaneous Task Calling)
        Jason's pattern for coordinated multi-agent execution
        
        Key principle: Call ALL agents at once, no waiting for confirmations
        """
        print("⚡ Task 동시 호출 시작!")
        
        if agents_list:
            # Direct agent list provided
            all_agents = agents_list
        else:
            # Determine agents from state and tasks
            state = self.state_manager.read_state()
            personas = state.get("personas", ["Backend Developer"])
            
            # Use factory to determine agents
            workflow_result = self.factory.create_dongsi_workflow(primary_task, personas)
            if "agents_started" in workflow_result:
                # Extract agents from the parallel command result
                all_agents = workflow_result.get("all_agents", [])
            else:
                all_agents = ["implementer-spark"]  # fallback
        
        print(f"🎯 동시 호출 대상: {', '.join(all_agents)}")
        
        # Create TaskDoubleCaller instance for proper coordination
        caller = TaskDoubleCaller()
        
        # Execute simultaneous task calling
        primary_agent = all_agents[0] if all_agents else "implementer-spark"
        support_agents = all_agents[1:] if len(all_agents) > 1 else []
        
        result = caller.call_task_dongsi(primary_agent, support_agents, primary_task)
        
        print("✅ 동시 호출 완료! All agents executing in parallel")
        return result
    
    def json_context_relay(self, context_data: Dict[str, Any], target_agent: str) -> Dict[str, Any]:
        """
        JSON-based context relay between agents
        Ensures data flows properly in the pipeline
        """
        try:
            # Update current state with context
            state = self.state_manager.read_state()
            
            # Add relay information
            relay_info = {
                "relayed_at": context_data.get("timestamp", "unknown"),
                "target_agent": target_agent,
                "context_size": len(json.dumps(context_data)),
                "relay_type": "json_context"
            }
            
            # Store in pipeline data passing
            if "pipeline" not in state:
                state["pipeline"] = {"data_passing": {}}
            
            relay_key = f"context_relay_{target_agent}"
            state["pipeline"]["data_passing"][relay_key] = {
                "from": "system",
                "to": target_agent,
                "data": context_data,
                "relay_info": relay_info
            }
            
            # Save state
            success = self.state_manager.write_state(state)
            
            return {
                "status": "success" if success else "failed",
                "relay_key": relay_key,
                "target_agent": target_agent,
                "context_size": relay_info["context_size"]
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "message": str(e)
            }
    
    def inho_orchestration(self, orchestration_type: str = "standard") -> Dict[str, Any]:
        """
        2호 (Number Two) orchestration support
        Provides coordination for Claude Code (2호) operations
        """
        print("🤖 2호 오케스트레이션 활성화")
        
        state = self.state_manager.read_state()
        
        if orchestration_type == "standard":
            # Standard orchestration - follow workflow phases
            phase_status = self.phase_manager.check_phase_progression()
            current_phase = phase_status.get("current_phase")
            
            if current_phase:
                return {
                    "orchestration_active": True,
                    "current_phase": current_phase,
                    "inho_guidance": f"Execute {current_phase} phase following SPARK quality standards",
                    "next_actions": self._get_phase_actions(current_phase)
                }
            else:
                return {
                    "orchestration_active": False,
                    "message": "No active workflow phase - use task_task_task_sijak to initiate"
                }
        
        elif orchestration_type == "emergency":
            # Emergency orchestration - quick fixes
            return {
                "orchestration_type": "emergency",
                "inho_guidance": "Emergency mode activated - focus on critical fixes only",
                "quality_gates_relaxed": True
            }
        
        return {"status": "unknown_orchestration_type"}
    
    def _get_phase_actions(self, phase: str) -> List[str]:
        """Get recommended actions for a workflow phase"""
        phase_actions = {
            "analysis": [
                "Review requirements thoroughly",
                "Identify key components and dependencies", 
                "Determine technical approach",
                "Document assumptions and constraints"
            ],
            "architecture": [
                "Design system architecture",
                "Define component interfaces",
                "Plan data models and schemas",
                "Consider scalability and performance"
            ],
            "implementation": [
                "Implement core functionality",
                "Follow coding standards and patterns",
                "Add proper error handling",
                "Write unit tests for key functions"
            ],
            "frontend": [
                "Design user interfaces",
                "Implement responsive layouts",
                "Add interactive components",
                "Ensure accessibility compliance"
            ],
            "testing": [
                "Run comprehensive test suite",
                "Check code coverage metrics", 
                "Perform integration testing",
                "Validate edge cases and error scenarios"
            ],
            "security": [
                "Security vulnerability scanning",
                "Input validation and sanitization",
                "Authentication and authorization review",
                "Secrets and configuration audit"
            ],
            "documentation": [
                "Generate API documentation",
                "Write user guides and tutorials",
                "Document deployment procedures",
                "Create troubleshooting guides"  
            ],
            "deployment": [
                "Prepare deployment environment",
                "Configure CI/CD pipelines",
                "Deploy to staging/production",
                "Monitor deployment health"
            ]
        }
        
        return phase_actions.get(phase, ["Execute phase tasks according to requirements"])
    
    def _determine_simultaneous_agents(self, personas: List[str], complexity: float, task_description: str) -> List[str]:
        """
        Determine optimal combination of agents to call simultaneously
        Based on Jason's efficiency patterns
        """
        agents = []
        task_lower = task_description.lower()
        
        # Always include implementer as base
        agents.append("implementer-spark")
        
        # Frontend work detection
        frontend_keywords = ["ui", "component", "frontend", "design", "interface", "responsive"]
        if any(keyword in task_lower for keyword in frontend_keywords) or "Frontend Developer" in personas:
            agents.append("designer-spark")
        
        # Security work detection  
        security_keywords = ["auth", "security", "login", "permission", "encrypt"]
        if any(keyword in task_lower for keyword in security_keywords) or "Security Expert" in personas:
            agents.append("security-spark")
        
        # High complexity requires architecture
        if complexity > 0.7 or "System Architect" in personas or "architecture" in task_lower:
            agents.insert(0, "architect-spark")  # Put architect first
        
        # API/Backend specific
        api_keywords = ["api", "endpoint", "service", "database", "server"]
        if any(keyword in task_lower for keyword in api_keywords):
            # Keep implementer-spark as main, but might add analyzer
            if complexity > 0.6:
                agents.insert(0, "analyzer-spark")
        
        # Testing for complex tasks
        if complexity > 0.5 or "test" in task_lower:
            agents.append("tester-spark")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_agents = []
        for agent in agents:
            if agent not in seen:
                seen.add(agent)
                unique_agents.append(agent)
        
        return unique_agents[:4]  # Limit to 4 simultaneous agents for efficiency
    
    def spark_status(self) -> Dict[str, Any]:
        """Get comprehensive SPARK system status"""
        state = self.state_manager.read_state()
        phase_status = self.phase_manager.check_phase_progression()
        
        # Calculate token efficiency (should maintain 88.4%)
        token_usage = state.get("token_usage", 0)
        baseline_tokens = 44000  # SuperClaude baseline
        current_tokens = max(token_usage, 5100)  # SPARK average
        efficiency = round((1 - current_tokens / baseline_tokens) * 100, 1)
        
        return {
            "spark_version": "3.0",
            "system_status": "operational",
            "token_efficiency": f"{efficiency}%",
            "current_tokens": current_tokens,
            "token_savings": baseline_tokens - current_tokens,
            "active_personas": len(state.get("personas", [])),
            "workflow_progress": phase_status.get("progress", 0),
            "current_phase": phase_status.get("current_phase"),
            "quality_gates_status": {
                "passed": state.get("quality_gates", {}).get("passed", 0),
                "required": state.get("quality_gates", {}).get("required", 8)
            },
            "pipeline_active": bool(state.get("pipeline", {}).get("current_agent")),
            "last_updated": state.get("last_updated")
        }
    
    def emergency_reset(self) -> Dict[str, Any]:
        """Emergency reset of SPARK system"""
        print("🔥 Emergency Reset Initiated")
        
        # Clear current state
        success = self.state_manager.clear_state()
        
        if success:
            print("✅ SPARK system reset successfully")
            return {
                "status": "reset_complete",
                "message": "SPARK system has been reset to initial state",
                "next_step": "Run persona routing to restart workflow"
            }
        else:
            return {
                "status": "reset_failed",
                "message": "Failed to reset SPARK system state"
            }


def main():
    """CLI interface for integration commands"""
    if len(sys.argv) < 2:
        print("""
SPARK Integration Commands Usage:

python spark_integration_commands.py <command> [args...]

Commands:
  sijak <task> [agents...]           - Task Task Task Task → 시작! pattern  
  dongsi <task> [agents...]          - Task 동시 호출 pattern
  multi <task> <agent1> <agent2>...  - Explicit multi-agent simultaneous call
  relay <agent> <data>               - JSON context relay
  inho [type]                        - 2호 orchestration
  status                             - System status
  reset                              - Emergency reset

Jason's Parallel Execution Examples:
  python spark_integration_commands.py sijak "implement secure API"
  python spark_integration_commands.py sijak "create dashboard" implementer-spark designer-spark
  python spark_integration_commands.py multi "full-stack app" architect-spark implementer-spark designer-spark tester-spark
  python spark_integration_commands.py dongsi "user authentication" security-spark implementer-spark
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    spark = SparkIntegrationCommands()
    
    if command == "sijak":
        task = sys.argv[2] if len(sys.argv) > 2 else "default task"
        agents_override = sys.argv[3:] if len(sys.argv) > 3 else None
        result = spark.task_task_task_sijak(task, agents_override)
        print(json.dumps(result, indent=2))
    
    elif command == "dongsi":
        task = sys.argv[2] if len(sys.argv) > 2 else "default task"
        agents_list = sys.argv[3:] if len(sys.argv) > 3 else None
        result = spark.dongsi_hocul(task, None, agents_list)
        print(json.dumps(result, indent=2))
    
    elif command == "multi":
        if len(sys.argv) < 4:
            print("Usage: multi <task> <agent1> <agent2> [agent3...]")
            print("Example: multi 'build API' implementer-spark security-spark tester-spark")
            sys.exit(1)
        task = sys.argv[2]
        agents = sys.argv[3:]
        print(f"🚀 Multi-agent simultaneous execution: {', '.join(agents)}")
        result = spark.task_task_task_sijak(task, agents)
        print(json.dumps(result, indent=2))
    
    elif command == "relay":
        if len(sys.argv) < 4:
            print("Usage: relay <target_agent> <json_data>")
            sys.exit(1)
        agent = sys.argv[2]
        try:
            data = json.loads(sys.argv[3])
        except json.JSONDecodeError:
            data = {"message": sys.argv[3]}
        result = spark.json_context_relay(data, agent)
        print(json.dumps(result, indent=2))
    
    elif command == "inho":
        orch_type = sys.argv[2] if len(sys.argv) > 2 else "standard"
        result = spark.inho_orchestration(orch_type)
        print(json.dumps(result, indent=2))
    
    elif command == "status":
        result = spark.spark_status()
        print(json.dumps(result, indent=2))
    
    elif command == "reset":
        result = spark.emergency_reset()
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()