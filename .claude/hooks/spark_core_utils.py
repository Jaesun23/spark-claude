#!/usr/bin/env python3
"""
SPARK Core Utilities Module
Provides secure command execution, state management, and JSON compliance
"""

import json
import logging
import os
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Set up logging to stderr to avoid contaminating stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)


class SecureCommandExecutor:
    """Secure command execution without shell injection risks"""
    
    @staticmethod
    def sanitize_path(path: str) -> Optional[Path]:
        """Sanitize and validate file paths to prevent traversal attacks"""
        try:
            # Resolve to absolute path and check it exists
            resolved = Path(path).resolve()
            
            # Prevent access outside allowed directories
            allowed_dirs = [
                Path.cwd(),
                Path.home() / ".claude",
                Path("/tmp"),
                Path("/var/folders")  # macOS temp directories
            ]
            
            # Check if path is within allowed directories
            is_allowed = any(
                str(resolved).startswith(str(allowed_dir))
                for allowed_dir in allowed_dirs
            )
            
            if not is_allowed:
                logger.error(f"Path traversal attempt blocked: {path}")
                return None
                
            return resolved
            
        except Exception as e:
            logger.error(f"Invalid path: {path} - {e}")
            return None
    
    @staticmethod
    def run_command(
        command: List[str],
        timeout: int = 30,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None
    ) -> Tuple[bool, str, str]:
        """
        Execute command safely without shell=True
        
        Args:
            command: Command as list of arguments
            timeout: Command timeout in seconds
            cwd: Working directory (will be validated)
            env: Environment variables
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            # Validate working directory if provided
            if cwd:
                safe_cwd = SecureCommandExecutor.sanitize_path(cwd)
                if not safe_cwd or not safe_cwd.is_dir():
                    return False, "", f"Invalid working directory: {cwd}"
                cwd = str(safe_cwd)
            
            # Merge environment variables
            run_env = os.environ.copy()
            if env:
                run_env.update(env)
            
            # Execute command safely
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env=run_env,
                shell=False  # NEVER use shell=True
            )
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            return False, "", f"Command timed out after {timeout} seconds"
        except FileNotFoundError:
            return False, "", f"Command not found: {command[0]}"
        except Exception as e:
            return False, "", f"Command execution failed: {e}"
    
    @staticmethod
    def find_files(
        pattern: str,
        directory: str = ".",
        exclude_dirs: Optional[List[str]] = None
    ) -> List[Path]:
        """Safely find files matching pattern"""
        try:
            safe_dir = SecureCommandExecutor.sanitize_path(directory)
            if not safe_dir:
                return []
            
            exclude_dirs = exclude_dirs or [".venv", "node_modules", ".git", "__pycache__"]
            
            # Use pathlib for safe file discovery
            results = []
            for path in safe_dir.rglob(pattern):
                # Check exclusions
                if any(excluded in str(path) for excluded in exclude_dirs):
                    continue
                results.append(path)
                
            return results[:100]  # Limit results to prevent DoS
            
        except Exception as e:
            logger.error(f"File search failed: {e}")
            return []


class StateManager:
    """Manages persistent state for SPARK workflows"""
    
    def __init__(self):
        self.state_dir = Path.home() / ".claude" / "workflows"
        self.state_file = self.state_dir / "current_task.json"
        self._ensure_state_dir()
    
    def _ensure_state_dir(self):
        """Ensure state directory exists"""
        try:
            self.state_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create state directory: {e}")
    
    def read_state(self) -> Dict[str, Any]:
        """Read current task state"""
        try:
            if self.state_file.exists():
                with self.state_file.open('r') as f:
                    return json.load(f)
            return self._default_state()
        except Exception as e:
            logger.error(f"Failed to read state: {e}")
            return self._default_state()
    
    def write_state(self, state: Dict[str, Any]) -> bool:
        """Write task state atomically"""
        try:
            # Add metadata
            state["last_updated"] = datetime.now().isoformat()
            state["version"] = "1.0.0"
            
            # Write to temp file first (atomic operation)
            temp_file = self.state_file.with_suffix('.tmp')
            with temp_file.open('w') as f:
                json.dump(state, f, indent=2)
            
            # Atomic rename
            temp_file.replace(self.state_file)
            return True
            
        except Exception as e:
            logger.error(f"Failed to write state: {e}")
            return False
    
    def update_state(self, updates: Dict[str, Any]) -> bool:
        """Update specific state fields"""
        try:
            current = self.read_state()
            current.update(updates)
            return self.write_state(current)
        except Exception as e:
            logger.error(f"Failed to update state: {e}")
            return False
    
    def clear_state(self) -> bool:
        """Clear current task state"""
        try:
            if self.state_file.exists():
                self.state_file.unlink()
            return True
        except Exception as e:
            logger.error(f"Failed to clear state: {e}")
            return False
    
    def _default_state(self) -> Dict[str, Any]:
        """Default state structure"""
        return {
            "task_id": None,
            "personas": [],
            "agents": [],
            "complexity": 0.0,
            "quality_gates": {
                "required": 8,
                "passed": 0,
                "results": {}
            },
            "pipeline": {
                "current_agent": None,
                "completed_agents": [],
                "data_passing": {}
            },
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "version": "1.0.0"
        }


class HookOutputFormatter:
    """Formats hook outputs according to Anthropic specifications"""
    
    @staticmethod
    def format_user_prompt_submit(
        additional_context: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Format UserPromptSubmit hook output
        
        The hook should output JSON with hookSpecificOutput containing additionalContext
        """
        output = {
            "hookSpecificOutput": {
                "additionalContext": additional_context
            }
        }
        
        if metadata:
            output["metadata"] = metadata
            
        return json.dumps(output)
    
    @staticmethod
    def format_subagent_stop(
        decision: str,
        reason: str,
        retry_prompt: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Format SubagentStop hook output
        
        decision: "block" or "continue"
        reason: Explanation for the decision
        retry_prompt: Optional prompt for retry (only when blocking)
        """
        output = {
            "hookSpecificOutput": {
                "decision": decision,
                "reason": reason
            }
        }
        
        if decision == "block" and retry_prompt:
            output["hookSpecificOutput"]["retryPrompt"] = retry_prompt
            
        if metadata:
            output["metadata"] = metadata
            
        return json.dumps(output)
    
    @staticmethod
    def format_agent_stop(
        should_stop: bool,
        reason: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Format AgentStop hook output
        
        should_stop: Whether to stop the agent
        reason: Optional explanation
        """
        output = {
            "hookSpecificOutput": {
                "shouldStop": should_stop
            }
        }
        
        if reason:
            output["hookSpecificOutput"]["reason"] = reason
            
        if metadata:
            output["metadata"] = metadata
            
        return json.dumps(output)


class AgentChainManager:
    """Manages data passing between agents in pipelines"""
    
    def __init__(self):
        self.state_manager = StateManager()
    
    def start_chain(self, chain_id: str, agents: List[str]) -> bool:
        """Initialize a new agent chain"""
        try:
            state = self.state_manager.read_state()
            state["pipeline"] = {
                "chain_id": chain_id,
                "agents": agents,
                "current_index": 0,
                "current_agent": agents[0] if agents else None,
                "completed_agents": [],
                "data_passing": {},
                "started_at": datetime.now().isoformat()
            }
            return self.state_manager.write_state(state)
        except Exception as e:
            logger.error(f"Failed to start chain: {e}")
            return False
    
    def pass_data(self, from_agent: str, to_agent: str, data: Dict[str, Any]) -> bool:
        """Pass data from one agent to another"""
        try:
            state = self.state_manager.read_state()
            if "pipeline" not in state:
                state["pipeline"] = {"data_passing": {}}
                
            # Store data with source and target
            data_key = f"{from_agent}->{to_agent}"
            state["pipeline"]["data_passing"][data_key] = {
                "from": from_agent,
                "to": to_agent,
                "data": data,
                "timestamp": datetime.now().isoformat()
            }
            
            return self.state_manager.write_state(state)
        except Exception as e:
            logger.error(f"Failed to pass data: {e}")
            return False
    
    def get_data(self, for_agent: str) -> Dict[str, Any]:
        """Get data passed to an agent"""
        try:
            state = self.state_manager.read_state()
            if "pipeline" not in state:
                return {}
                
            # Find all data targeted to this agent
            agent_data = {}
            for key, value in state["pipeline"].get("data_passing", {}).items():
                if value.get("to") == for_agent:
                    from_agent = value.get("from", "unknown")
                    agent_data[from_agent] = value.get("data", {})
                    
            return agent_data
        except Exception as e:
            logger.error(f"Failed to get data: {e}")
            return {}
    
    def advance_chain(self) -> Optional[str]:
        """Move to the next agent in the chain"""
        try:
            state = self.state_manager.read_state()
            pipeline = state.get("pipeline", {})
            
            agents = pipeline.get("agents", [])
            current_index = pipeline.get("current_index", 0)
            
            # Mark current agent as completed
            if pipeline.get("current_agent"):
                completed = pipeline.get("completed_agents", [])
                completed.append(pipeline["current_agent"])
                pipeline["completed_agents"] = completed
            
            # Move to next agent
            next_index = current_index + 1
            if next_index < len(agents):
                pipeline["current_index"] = next_index
                pipeline["current_agent"] = agents[next_index]
                self.state_manager.write_state(state)
                return agents[next_index]
            else:
                # Chain completed
                pipeline["current_agent"] = None
                pipeline["completed_at"] = datetime.now().isoformat()
                self.state_manager.write_state(state)
                return None
                
        except Exception as e:
            logger.error(f"Failed to advance chain: {e}")
            return None
    
    def get_chain_status(self) -> Dict[str, Any]:
        """Get current chain status"""
        try:
            state = self.state_manager.read_state()
            pipeline = state.get("pipeline", {})
            
            return {
                "chain_id": pipeline.get("chain_id"),
                "current_agent": pipeline.get("current_agent"),
                "completed_agents": pipeline.get("completed_agents", []),
                "remaining_agents": self._get_remaining_agents(pipeline),
                "progress": self._calculate_progress(pipeline),
                "data_passed": len(pipeline.get("data_passing", {}))
            }
        except Exception as e:
            logger.error(f"Failed to get chain status: {e}")
            return {}
    
    def _get_remaining_agents(self, pipeline: Dict[str, Any]) -> List[str]:
        """Get list of remaining agents"""
        agents = pipeline.get("agents", [])
        current_index = pipeline.get("current_index", 0)
        return agents[current_index + 1:] if current_index < len(agents) else []
    
    def _calculate_progress(self, pipeline: Dict[str, Any]) -> float:
        """Calculate chain progress percentage"""
        agents = pipeline.get("agents", [])
        completed = len(pipeline.get("completed_agents", []))
        
        if not agents:
            return 0.0
        return round((completed / len(agents)) * 100, 1)


# Export all utilities
__all__ = [
    'SecureCommandExecutor',
    'StateManager', 
    'HookOutputFormatter',
    'AgentChainManager'
]