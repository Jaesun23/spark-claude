#!/usr/bin/env python3
"""
SPARK Pipeline Orchestrator
Enables multi-agent chaining with data passing and state management
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent))
from spark_core_utils import StateManager, AgentChainManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """Orchestrates multi-agent pipelines with data passing"""
    
    # Pre-defined pipeline templates
    PIPELINE_TEMPLATES = {
        "full-stack": {
            "description": "Complete full-stack development pipeline",
            "agents": ["architect-spark", "implementer-spark", "designer-spark", "tester-spark"],
            "data_flow": {
                "architect-spark": ["system_design", "api_contracts", "data_models"],
                "implementer-spark": ["backend_code", "api_endpoints", "services"],
                "designer-spark": ["ui_components", "styles", "interactions"],
                "tester-spark": ["test_results", "coverage", "performance"]
            }
        },
        "analyze-fix": {
            "description": "Analyze and fix code issues",
            "agents": ["analyzer-spark", "implementer-spark", "tester-spark"],
            "data_flow": {
                "analyzer-spark": ["issues", "recommendations", "complexity"],
                "implementer-spark": ["fixes", "refactoring", "improvements"],
                "tester-spark": ["validation", "regression", "quality"]
            }
        },
        "design-implement": {
            "description": "Design and implement features",
            "agents": ["designer-spark", "implementer-spark"],
            "data_flow": {
                "designer-spark": ["designs", "specifications", "mockups"],
                "implementer-spark": ["implementation", "integration"]
            }
        },
        "test-deploy": {
            "description": "Test and deploy pipeline",
            "agents": ["tester-spark", "devops-spark"],
            "data_flow": {
                "tester-spark": ["test_results", "quality_metrics"],
                "devops-spark": ["deployment", "monitoring"]
            }
        },
        "document-review": {
            "description": "Document and review code",
            "agents": ["documenter-spark", "reviewer-spark"],
            "data_flow": {
                "documenter-spark": ["documentation", "api_docs"],
                "reviewer-spark": ["review_feedback", "approval"]
            }
        }
    }
    
    def __init__(self):
        self.state_manager = StateManager()
        self.chain_manager = AgentChainManager()
    
    def start_pipeline(
        self,
        pipeline_name: str,
        custom_agents: Optional[List[str]] = None,
        initial_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Start a new pipeline execution"""
        
        # Get pipeline configuration
        if pipeline_name in self.PIPELINE_TEMPLATES:
            template = self.PIPELINE_TEMPLATES[pipeline_name]
            agents = custom_agents or template["agents"]
            description = template["description"]
        else:
            # Custom pipeline
            agents = custom_agents or []
            description = f"Custom pipeline: {pipeline_name}"
        
        if not agents:
            return {
                "success": False,
                "error": "No agents specified for pipeline"
            }
        
        # Generate pipeline ID
        pipeline_id = f"pipeline_{pipeline_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize pipeline in state
        state = self.state_manager.read_state()
        state["pipeline"] = {
            "id": pipeline_id,
            "name": pipeline_name,
            "description": description,
            "agents": agents,
            "current_index": 0,
            "current_agent": agents[0],
            "completed_agents": [],
            "data_passing": initial_data or {},
            "status": "running",
            "started_at": datetime.now().isoformat()
        }
        
        self.state_manager.write_state(state)
        
        logger.info(f"🚀 Pipeline started: {pipeline_name}")
        logger.info(f"   ID: {pipeline_id}")
        logger.info(f"   Agents: {' -> '.join(agents)}")
        
        return {
            "success": True,
            "pipeline_id": pipeline_id,
            "first_agent": agents[0],
            "total_agents": len(agents),
            "message": f"Pipeline '{pipeline_name}' started with {len(agents)} agents"
        }
    
    def advance_pipeline(
        self,
        completed_agent: str,
        output_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Advance pipeline to the next agent"""
        
        state = self.state_manager.read_state()
        pipeline = state.get("pipeline", {})
        
        if not pipeline or pipeline.get("status") != "running":
            return {
                "success": False,
                "error": "No active pipeline found"
            }
        
        # Verify the completed agent matches current
        if pipeline.get("current_agent") != completed_agent:
            return {
                "success": False,
                "error": f"Agent mismatch: expected {pipeline.get('current_agent')}, got {completed_agent}"
            }
        
        # Store output data if provided
        if output_data:
            data_key = f"{completed_agent}_output"
            pipeline["data_passing"][data_key] = {
                "agent": completed_agent,
                "data": output_data,
                "timestamp": datetime.now().isoformat()
            }
        
        # Mark current agent as completed
        pipeline["completed_agents"].append(completed_agent)
        
        # Advance to next agent
        current_index = pipeline.get("current_index", 0)
        agents = pipeline.get("agents", [])
        
        if current_index + 1 < len(agents):
            # Move to next agent
            pipeline["current_index"] = current_index + 1
            pipeline["current_agent"] = agents[current_index + 1]
            next_agent = agents[current_index + 1]
            
            # Pass data to next agent
            if output_data:
                self.chain_manager.pass_data(
                    from_agent=completed_agent,
                    to_agent=next_agent,
                    data=output_data
                )
            
            logger.info(f"✅ Agent completed: {completed_agent}")
            logger.info(f"🔄 Advancing to: {next_agent}")
            
            state["pipeline"] = pipeline
            self.state_manager.write_state(state)
            
            return {
                "success": True,
                "next_agent": next_agent,
                "progress": self._calculate_progress(pipeline),
                "message": f"Advanced pipeline to {next_agent}"
            }
        else:
            # Pipeline completed
            pipeline["status"] = "completed"
            pipeline["current_agent"] = None
            pipeline["completed_at"] = datetime.now().isoformat()
            
            state["pipeline"] = pipeline
            self.state_manager.write_state(state)
            
            logger.info(f"✅ Pipeline completed: {pipeline['name']}")
            logger.info(f"   Total agents: {len(agents)}")
            logger.info(f"   Duration: {self._calculate_duration(pipeline)}")
            
            return {
                "success": True,
                "completed": True,
                "total_agents": len(agents),
                "final_data": pipeline.get("data_passing", {}),
                "message": f"Pipeline '{pipeline['name']}' completed successfully"
            }
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        
        state = self.state_manager.read_state()
        pipeline = state.get("pipeline", {})
        
        if not pipeline:
            return {
                "active": False,
                "message": "No pipeline currently active"
            }
        
        return {
            "active": pipeline.get("status") == "running",
            "pipeline_id": pipeline.get("id"),
            "pipeline_name": pipeline.get("name"),
            "current_agent": pipeline.get("current_agent"),
            "completed_agents": pipeline.get("completed_agents", []),
            "remaining_agents": self._get_remaining_agents(pipeline),
            "progress": self._calculate_progress(pipeline),
            "data_keys": list(pipeline.get("data_passing", {}).keys()),
            "status": pipeline.get("status"),
            "started_at": pipeline.get("started_at"),
            "duration": self._calculate_duration(pipeline) if pipeline.get("status") == "running" else None
        }
    
    def get_agent_input_data(self, agent_name: str) -> Dict[str, Any]:
        """Get input data for a specific agent from previous agents"""
        
        state = self.state_manager.read_state()
        pipeline = state.get("pipeline", {})
        data_passing = pipeline.get("data_passing", {})
        
        # Collect all data targeted to this agent
        agent_data = {}
        for key, value in data_passing.items():
            if isinstance(value, dict):
                # Check if this data is meant for the current agent
                if "->"+agent_name in key or key.endswith("_output"):
                    source = value.get("agent", key.split("_")[0])
                    agent_data[source] = value.get("data", {})
        
        return agent_data
    
    def abort_pipeline(self, reason: str = "User requested abort") -> Dict[str, Any]:
        """Abort the current pipeline"""
        
        state = self.state_manager.read_state()
        pipeline = state.get("pipeline", {})
        
        if not pipeline or pipeline.get("status") != "running":
            return {
                "success": False,
                "error": "No active pipeline to abort"
            }
        
        pipeline["status"] = "aborted"
        pipeline["aborted_at"] = datetime.now().isoformat()
        pipeline["abort_reason"] = reason
        
        state["pipeline"] = pipeline
        self.state_manager.write_state(state)
        
        logger.info(f"⛔ Pipeline aborted: {pipeline['name']}")
        logger.info(f"   Reason: {reason}")
        
        return {
            "success": True,
            "pipeline_id": pipeline.get("id"),
            "completed_agents": pipeline.get("completed_agents", []),
            "message": f"Pipeline '{pipeline['name']}' aborted"
        }
    
    def _calculate_progress(self, pipeline: Dict[str, Any]) -> float:
        """Calculate pipeline progress percentage"""
        agents = pipeline.get("agents", [])
        completed = len(pipeline.get("completed_agents", []))
        
        if not agents:
            return 0.0
        return round((completed / len(agents)) * 100, 1)
    
    def _get_remaining_agents(self, pipeline: Dict[str, Any]) -> List[str]:
        """Get list of remaining agents"""
        agents = pipeline.get("agents", [])
        current_index = pipeline.get("current_index", 0)
        
        if current_index < len(agents):
            return agents[current_index + 1:]
        return []
    
    def _calculate_duration(self, pipeline: Dict[str, Any]) -> str:
        """Calculate pipeline duration"""
        started_at = pipeline.get("started_at")
        if not started_at:
            return "Unknown"
        
        try:
            start = datetime.fromisoformat(started_at)
            duration = datetime.now() - start
            
            # Format duration
            hours, remainder = divmod(duration.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            if hours > 0:
                return f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                return f"{minutes}m {seconds}s"
            else:
                return f"{seconds}s"
        except Exception:
            return "Unknown"


def main():
    """CLI interface for pipeline orchestrator"""
    
    orchestrator = PipelineOrchestrator()
    
    if len(sys.argv) < 2:
        print("Usage: spark_pipeline_orchestrator.py <command> [args]")
        print("Commands:")
        print("  start <pipeline_name> [agent1,agent2,...]")
        print("  advance <completed_agent>")
        print("  status")
        print("  abort [reason]")
        print("  templates")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "start":
        if len(sys.argv) < 3:
            print("Error: Pipeline name required")
            sys.exit(1)
        
        pipeline_name = sys.argv[2]
        custom_agents = sys.argv[3].split(",") if len(sys.argv) > 3 else None
        
        result = orchestrator.start_pipeline(pipeline_name, custom_agents)
        print(json.dumps(result, indent=2))
    
    elif command == "advance":
        if len(sys.argv) < 3:
            print("Error: Completed agent name required")
            sys.exit(1)
        
        completed_agent = sys.argv[2]
        result = orchestrator.advance_pipeline(completed_agent)
        print(json.dumps(result, indent=2))
    
    elif command == "status":
        result = orchestrator.get_pipeline_status()
        print(json.dumps(result, indent=2))
    
    elif command == "abort":
        reason = sys.argv[2] if len(sys.argv) > 2 else "User requested abort"
        result = orchestrator.abort_pipeline(reason)
        print(json.dumps(result, indent=2))
    
    elif command == "templates":
        print("Available Pipeline Templates:")
        for name, template in PipelineOrchestrator.PIPELINE_TEMPLATES.items():
            print(f"\n{name}:")
            print(f"  Description: {template['description']}")
            print(f"  Agents: {' -> '.join(template['agents'])}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()