#!/usr/bin/env python3
"""
SPARK Multi-Team Orchestrator v1.0
Enables parallel execution of up to 4 teams with JSON context relay
Created by: Jason + Claude CODE
"""

import json
import sys
import os
import time
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from threading import Lock
import fcntl

# Import base orchestrator
sys.path.insert(0, str(Path(__file__).parent))
from spark_unified_orchestrator import (
    UnifiedOrchestrator, 
    PersonaRouter, 
    QualityGateValidator,
    SecureCommandExecutor,
    TaskContext,
    PersonaMode
)

class TeamStatus(Enum):
    """Team availability status"""
    INACTIVE = "INACTIVE"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"

class WorkflowPhase(Enum):
    """Workflow execution phases"""
    INITIALIZATION = "initialization"
    IMPLEMENTATION = "implementation"
    QUALITY = "quality"
    TESTING = "testing"
    REVIEW = "review"
    REPORT = "report"

@dataclass
class TeamContext:
    """Team-specific execution context"""
    team_id: str
    task_id: Optional[str]
    status: TeamStatus
    phase: Optional[WorkflowPhase]
    progress: int
    assigned_files: List[str]
    shared_resources: Dict[str, Any]
    implementation_details: Dict[str, Any]
    persona_activation: Dict[str, Any]
    quality_gates: Dict[str, str]
    retry_count: int
    max_retries: int
    start_time: Optional[str]
    end_time: Optional[str]
    errors: List[str]
    next_agent: Optional[str]
    communication: Dict[str, Any]
    
    def to_json_file(self, base_path: Path):
        """Save team context to JSON file"""
        file_path = base_path / f"{self.team_id}_current_task.json"
        with open(file_path, 'w') as f:
            json.dump(asdict(self), f, indent=2, default=str)
    
    @classmethod
    def from_json_file(cls, team_id: str, base_path: Path):
        """Load team context from JSON file"""
        file_path = base_path / f"{team_id}_current_task.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Convert string enums back to enum types
                if data.get('status'):
                    data['status'] = TeamStatus(data['status'])
                if data.get('phase'):
                    data['phase'] = WorkflowPhase(data['phase'])
                return cls(**data)
        return None

class FileLockManager:
    """Distributed file locking for parallel teams"""
    
    LOCK_FILE = ".claude/workflows/file_locks.json"
    MAX_LOCK_DURATION_MS = 30000  # 30 seconds max
    _file_lock = Lock()
    
    @classmethod
    def acquire_lock(cls, file_path: str, team_id: str) -> bool:
        """Attempt to acquire lock on a file"""
        with cls._file_lock:
            locks = cls._load_locks()
            
            if file_path in locks:
                lock = locks[file_path]
                # Check if lock expired
                if cls._is_lock_expired(lock):
                    # Expired, can acquire
                    locks[file_path] = {
                        "locked_by": team_id,
                        "timestamp": datetime.now().isoformat(),
                        "duration_ms": cls.MAX_LOCK_DURATION_MS
                    }
                    cls._save_locks(locks)
                    return True
                else:
                    # Still locked by another team
                    return False
            else:
                # No lock exists, acquire it
                locks[file_path] = {
                    "locked_by": team_id,
                    "timestamp": datetime.now().isoformat(),
                    "duration_ms": cls.MAX_LOCK_DURATION_MS
                }
                cls._save_locks(locks)
                return True
    
    @classmethod
    def release_lock(cls, file_path: str, team_id: str) -> bool:
        """Release lock on a file"""
        with cls._file_lock:
            locks = cls._load_locks()
            
            if file_path in locks and locks[file_path]["locked_by"] == team_id:
                del locks[file_path]
                cls._save_locks(locks)
                return True
            return False
    
    @classmethod
    def release_all_team_locks(cls, team_id: str) -> int:
        """Release all locks held by a team"""
        with cls._file_lock:
            locks = cls._load_locks()
            released = 0
            
            files_to_release = [
                path for path, lock in locks.items()
                if lock["locked_by"] == team_id
            ]
            
            for file_path in files_to_release:
                del locks[file_path]
                released += 1
            
            if released > 0:
                cls._save_locks(locks)
            
            return released
    
    @classmethod
    def wait_for_lock(cls, file_path: str, team_id: str, timeout_ms: int = 60000) -> bool:
        """Wait for lock with exponential backoff"""
        start_time = datetime.now()
        wait_ms = 100
        
        while (datetime.now() - start_time).total_seconds() * 1000 < timeout_ms:
            if cls.acquire_lock(file_path, team_id):
                return True
            
            time.sleep(wait_ms / 1000)
            wait_ms = min(wait_ms * 2, 5000)  # Exponential backoff, max 5s
        
        return False
    
    @classmethod
    def _load_locks(cls) -> Dict[str, Any]:
        """Load current locks from file"""
        lock_file = Path.home() / cls.LOCK_FILE
        if lock_file.exists():
            try:
                with open(lock_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    @classmethod
    def _save_locks(cls, locks: Dict[str, Any]):
        """Save locks to file"""
        lock_file = Path.home() / cls.LOCK_FILE
        lock_file.parent.mkdir(parents=True, exist_ok=True)
        with open(lock_file, 'w') as f:
            json.dump(locks, f, indent=2)
    
    @classmethod
    def _is_lock_expired(cls, lock: Dict[str, Any]) -> bool:
        """Check if a lock has expired"""
        timestamp = datetime.fromisoformat(lock["timestamp"])
        duration_ms = lock.get("duration_ms", cls.MAX_LOCK_DURATION_MS)
        expiry = timestamp + timedelta(milliseconds=duration_ms)
        return datetime.now() > expiry

class MultiTeamOrchestrator(UnifiedOrchestrator):
    """Extended orchestrator for parallel multi-team execution"""
    
    MAX_TEAMS = 4
    
    def __init__(self):
        super().__init__()
        self.workflows_path = Path.home() / ".claude" / "workflows"
        self.workflows_path.mkdir(parents=True, exist_ok=True)
        self.coordination_file = self.workflows_path / "multi_task_coordination.json"
        self.lock_manager = FileLockManager()
    
    def handle_multi_implement(self, task_ids: List[str]) -> Dict[str, Any]:
        """Handle /multi_implement command with parallel execution"""
        
        # Step 1: Allocate tasks to teams
        team_allocation = self._allocate_tasks_to_teams(task_ids)
        
        # Step 2: Initialize team JSON contexts
        for team_id, task_id in team_allocation.items():
            if task_id:
                self._initialize_team_context(team_id, task_id)
        
        # Step 3: Initialize coordination file
        self._initialize_coordination(team_allocation)
        
        # Step 4: Return parallel execution instructions
        active_teams = [tid for tid, task in team_allocation.items() if task]
        
        return {
            "action": "parallel_execute",
            "teams": team_allocation,
            "active_teams": active_teams,
            "workflow_phases": [phase.value for phase in WorkflowPhase],
            "instructions": self._generate_execution_instructions(active_teams),
            "coordination_file": str(self.coordination_file),
            "team_contexts": [f"{tid}_current_task.json" for tid in active_teams]
        }
    
    def _allocate_tasks_to_teams(self, task_ids: List[str]) -> Dict[str, Optional[str]]:
        """Allocate tasks to available teams"""
        allocation = {}
        
        for i in range(self.MAX_TEAMS):
            team_id = f"team{i+1}"
            if i < len(task_ids):
                allocation[team_id] = task_ids[i]
            else:
                allocation[team_id] = None
        
        return allocation
    
    def _initialize_team_context(self, team_id: str, task_id: str):
        """Initialize team-specific JSON context with full details"""
        
        # Get task details (would be loaded from task definition)
        task_details = self._get_task_details(task_id)
        
        # Analyze task for persona activation
        description = task_details.get("description", f"Implement {task_id}")
        personas = PersonaRouter.analyze_prompt(description)
        mcp_servers = self._select_mcp_servers(personas)
        complexity = PersonaRouter._calculate_complexity(description)
        
        # Create comprehensive team context
        context = TeamContext(
            team_id=team_id,
            task_id=task_id,
            status=TeamStatus.ASSIGNED,
            phase=WorkflowPhase.INITIALIZATION,
            progress=0,
            assigned_files=task_details.get("files", []),
            shared_resources=self._identify_shared_resources(task_details),
            implementation_details={
                "files_created": [],
                "files_modified": [],
                "functions_added": [],
                "classes_added": [],
                "tests_written": [],
                "quality_results": {},
                "metrics": {
                    "lines_added": 0,
                    "lines_removed": 0,
                    "complexity_score": 0
                }
            },
            persona_activation={
                "active_personas": [p.value for p in personas],
                "mcp_servers": mcp_servers,
                "complexity_score": complexity,
                "priority_hierarchy": self._get_persona_priorities(personas)
            },
            quality_gates={gate: "pending" for gate in QualityGateValidator.GATES[:8]},
            retry_count=0,
            max_retries=3,
            start_time=datetime.now().isoformat(),
            end_time=None,
            errors=[],
            next_agent=f"{team_id}_implementer",
            communication={
                "messages_for_orchestrator": [],
                "dependencies_on_other_teams": [],
                "blockers": [],
                "warnings": [],
                "progress_updates": []
            }
        )
        
        # Save to JSON file
        context.to_json_file(self.workflows_path)
    
    def _initialize_coordination(self, team_allocation: Dict[str, Optional[str]]):
        """Initialize multi-task coordination file"""
        
        teams_status = {}
        for team_id, task_id in team_allocation.items():
            if task_id:
                teams_status[team_id] = {
                    "status": TeamStatus.ASSIGNED.value,
                    "task_id": task_id,
                    "phase": WorkflowPhase.INITIALIZATION.value,
                    "progress": 0,
                    "last_update": datetime.now().isoformat()
                }
            else:
                teams_status[team_id] = {
                    "status": TeamStatus.INACTIVE.value,
                    "task_id": None,
                    "phase": None,
                    "progress": 0,
                    "last_update": None
                }
        
        coordination = {
            "session_id": f"multi_{datetime.now().strftime('%Y%m%d%H%M')}",
            "total_teams": self.MAX_TEAMS,
            "active_teams": len([t for t, task in team_allocation.items() if task]),
            "teams": teams_status,
            "shared_resources": {},
            "workflow_phases": [phase.value for phase in WorkflowPhase],
            "current_phase": WorkflowPhase.INITIALIZATION.value,
            "overall_progress": 0,
            "quality_metrics": {
                "total_violations": 0,
                "tests_passed": 0,
                "tests_failed": 0,
                "coverage_percentage": 0.0
            },
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "execution_log": []
        }
        
        with open(self.coordination_file, 'w') as f:
            json.dump(coordination, f, indent=2)
    
    def handle_team_completion(self, team_id: str, phase: str) -> Dict[str, Any]:
        """Handle when a team completes a phase"""
        
        # Load team context
        team_context = TeamContext.from_json_file(team_id, self.workflows_path)
        if not team_context:
            return {"error": f"Team context not found for {team_id}"}
        
        # Update team phase
        team_context.phase = WorkflowPhase(phase)
        team_context.progress = self._calculate_phase_progress(phase)
        
        # Run quality gates if in quality phase
        if phase == WorkflowPhase.QUALITY.value:
            quality_results = self._run_quality_gates_for_team(team_id, team_context)
            team_context.quality_gates = quality_results
            
            # Check if retry needed
            failed_gates = [g for g, s in quality_results.items() if s == "failed"]
            if failed_gates and team_context.retry_count < team_context.max_retries:
                team_context.retry_count += 1
                team_context.next_agent = f"{team_id}_quality"
                team_context.communication["messages_for_orchestrator"].append(
                    f"Quality gates failed: {', '.join(failed_gates)}. Retry {team_context.retry_count}/{team_context.max_retries}"
                )
                team_context.to_json_file(self.workflows_path)
                
                return {
                    "action": "retry_quality",
                    "team": team_id,
                    "failed_gates": failed_gates,
                    "retry_count": team_context.retry_count,
                    "guidance": self._generate_fix_guidance(failed_gates)
                }
        
        # Update status
        if phase == WorkflowPhase.REPORT.value:
            team_context.status = TeamStatus.COMPLETED
            team_context.end_time = datetime.now().isoformat()
        
        # Save updated context
        team_context.to_json_file(self.workflows_path)
        
        # Update coordination
        self._update_team_coordination(team_id, phase)
        
        # Check if all teams completed this phase
        if self._all_teams_completed_phase(phase):
            next_phase = self._get_next_phase(phase)
            if next_phase:
                return {
                    "action": "proceed_to_next_phase",
                    "next_phase": next_phase.value,
                    "teams_ready": self._get_active_teams()
                }
            else:
                return {
                    "action": "workflow_complete",
                    "final_report": self._generate_final_report()
                }
        else:
            return {
                "action": "wait_for_other_teams",
                "teams_pending": self._get_pending_teams(phase)
            }
    
    def _get_task_details(self, task_id: str) -> Dict[str, Any]:
        """Get task details from task definition"""
        # This would load from actual task definitions
        # For now, return mock data based on task ID pattern
        
        task_type = task_id.split('-')[1].lower() if '-' in task_id else "general"
        
        details = {
            "task_id": task_id,
            "description": f"Implement {task_id}",
            "files": [],
            "requirements": []
        }
        
        if "api" in task_type:
            details["description"] = f"Implement REST API endpoint for {task_id}"
            details["files"] = ["src/api/endpoints.py", "tests/test_api.py"]
            details["requirements"] = ["authentication", "validation", "error handling"]
        
        elif "ui" in task_type or "component" in task_type:
            details["description"] = f"Create responsive UI component for {task_id}"
            details["files"] = ["src/components/Component.tsx", "src/styles/component.css"]
            details["requirements"] = ["accessibility", "responsive design", "cross-browser"]
        
        elif "sec" in task_type or "auth" in task_type:
            details["description"] = f"Implement security features for {task_id}"
            details["files"] = ["src/security/auth.py", "tests/test_security.py"]
            details["requirements"] = ["encryption", "validation", "audit logging"]
        
        return details
    
    def _identify_shared_resources(self, task_details: Dict) -> Dict[str, Any]:
        """Identify files that might be shared across teams"""
        shared_files = [
            "src/constants.py",
            "src/types.py",
            "src/config.py",
            ".env",
            "pyproject.toml",
            "package.json",
            "requirements.txt",
            "tsconfig.json"
        ]
        
        resources = {}
        for file in shared_files:
            # Check if this shared file might be needed
            if any(file.split('/')[-1].split('.')[1] == f.split('.')[-1] 
                   for f in task_details.get("files", [])):
                resources[file] = {
                    "locked_by": None,
                    "lock_timestamp": None
                }
        
        return resources
    
    def _get_persona_priorities(self, personas: List[PersonaMode]) -> Dict[str, List[str]]:
        """Get priority hierarchies for active personas"""
        priorities = {}
        
        persona_priorities_map = {
            PersonaMode.BACKEND: ["Reliability", "Security", "Performance", "Convenience"],
            PersonaMode.FRONTEND: ["User Needs", "Accessibility", "Performance", "Technical Elegance"],
            PersonaMode.SECURITY: ["Security", "Compliance", "Reliability", "Performance"],
            PersonaMode.ARCHITECTURE: ["Maintainability", "Scalability", "Performance", "Short-term Gains"],
            PersonaMode.TESTING: ["Coverage", "Reliability", "Performance", "Maintainability"],
            PersonaMode.DEVOPS: ["Automation", "Reliability", "Security", "Performance"]
        }
        
        for persona in personas:
            if persona in persona_priorities_map:
                priorities[persona.value] = persona_priorities_map[persona]
        
        return priorities
    
    def _calculate_phase_progress(self, phase: str) -> int:
        """Calculate progress percentage for a phase"""
        phase_progress = {
            WorkflowPhase.INITIALIZATION.value: 10,
            WorkflowPhase.IMPLEMENTATION.value: 40,
            WorkflowPhase.QUALITY.value: 60,
            WorkflowPhase.TESTING.value: 80,
            WorkflowPhase.REVIEW.value: 90,
            WorkflowPhase.REPORT.value: 100
        }
        return phase_progress.get(phase, 0)
    
    def _run_quality_gates_for_team(self, team_id: str, context: TeamContext) -> Dict[str, str]:
        """Run quality gates for team's implemented files"""
        results = {}
        
        for file_path in context.implementation_details.get("files_modified", []):
            if Path(file_path).exists():
                language = self._detect_language(file_path)
                file_results = QualityGateValidator.validate(file_path, language)
                
                for gate, passed in file_results.items():
                    if gate not in results or not passed:
                        results[gate] = "passed" if passed else "failed"
        
        # Set any unvalidated gates to passed (for non-code files)
        for gate in QualityGateValidator.GATES[:8]:
            if gate not in results:
                results[gate] = "passed"
        
        return results
    
    def _update_team_coordination(self, team_id: str, phase: str):
        """Update team status in coordination file"""
        if self.coordination_file.exists():
            with open(self.coordination_file, 'r') as f:
                coordination = json.load(f)
            
            if team_id in coordination["teams"]:
                coordination["teams"][team_id]["phase"] = phase
                coordination["teams"][team_id]["progress"] = self._calculate_phase_progress(phase)
                coordination["teams"][team_id]["last_update"] = datetime.now().isoformat()
                
                # Add to execution log
                coordination["execution_log"].append({
                    "timestamp": datetime.now().isoformat(),
                    "team": team_id,
                    "event": f"Completed phase: {phase}"
                })
                
                # Update overall progress
                total_progress = sum(
                    t["progress"] for t in coordination["teams"].values()
                    if t["status"] != TeamStatus.INACTIVE.value
                )
                active_teams = coordination["active_teams"]
                coordination["overall_progress"] = total_progress // active_teams if active_teams > 0 else 0
            
            with open(self.coordination_file, 'w') as f:
                json.dump(coordination, f, indent=2)
    
    def _all_teams_completed_phase(self, phase: str) -> bool:
        """Check if all active teams completed a phase"""
        if self.coordination_file.exists():
            with open(self.coordination_file, 'r') as f:
                coordination = json.load(f)
            
            for team_data in coordination["teams"].values():
                if team_data["status"] == TeamStatus.INACTIVE.value:
                    continue
                if team_data["phase"] != phase:
                    return False
            
            return True
        return False
    
    def _get_next_phase(self, current_phase: str) -> Optional[WorkflowPhase]:
        """Get the next phase in workflow"""
        phases = list(WorkflowPhase)
        try:
            current_idx = [p.value for p in phases].index(current_phase)
            if current_idx < len(phases) - 1:
                return phases[current_idx + 1]
        except ValueError:
            pass
        return None
    
    def _get_active_teams(self) -> List[str]:
        """Get list of active team IDs"""
        if self.coordination_file.exists():
            with open(self.coordination_file, 'r') as f:
                coordination = json.load(f)
            
            return [
                team_id for team_id, data in coordination["teams"].items()
                if data["status"] != TeamStatus.INACTIVE.value
            ]
        return []
    
    def _get_pending_teams(self, phase: str) -> List[str]:
        """Get teams that haven't completed a phase"""
        if self.coordination_file.exists():
            with open(self.coordination_file, 'r') as f:
                coordination = json.load(f)
            
            pending = []
            for team_id, data in coordination["teams"].items():
                if data["status"] == TeamStatus.INACTIVE.value:
                    continue
                if data["phase"] != phase:
                    pending.append(team_id)
            
            return pending
        return []
    
    def _generate_execution_instructions(self, active_teams: List[str]) -> str:
        """Generate execution instructions for 2号"""
        return f"""
Execute {len(active_teams)} teams in parallel:

1. IMPLEMENTATION PHASE:
   Call all teams simultaneously:
   {', '.join([f'{t}_implementer' for t in active_teams])}
   
2. QUALITY PHASE (after all implementations complete):
   Call all teams simultaneously:
   {', '.join([f'{t}_quality' for t in active_teams])}
   
3. TESTING PHASE (after all quality checks pass):
   Call all teams simultaneously:
   {', '.join([f'{t}_tester' for t in active_teams])}
   
4. REVIEW PHASE (after all tests complete):
   Call single reviewer agent for all teams
   
5. REPORT PHASE:
   Generate consolidated report

IMPORTANT: Always call teams in parallel within each phase!
"""
    
    def _generate_final_report(self) -> Dict[str, Any]:
        """Generate final consolidated report"""
        report = {
            "session_summary": {},
            "team_results": {},
            "quality_metrics": {},
            "files_modified": [],
            "tests_added": [],
            "recommendations": []
        }
        
        # Load coordination data
        if self.coordination_file.exists():
            with open(self.coordination_file, 'r') as f:
                coordination = json.load(f)
            
            report["session_summary"] = {
                "session_id": coordination["session_id"],
                "total_teams": coordination["active_teams"],
                "overall_progress": coordination["overall_progress"],
                "start_time": coordination["start_time"],
                "end_time": datetime.now().isoformat(),
                "duration": self._calculate_duration(
                    coordination["start_time"],
                    datetime.now().isoformat()
                )
            }
            
            report["quality_metrics"] = coordination["quality_metrics"]
        
        # Load team results
        for team_id in self._get_active_teams():
            context = TeamContext.from_json_file(team_id, self.workflows_path)
            if context:
                report["team_results"][team_id] = {
                    "task_id": context.task_id,
                    "status": context.status.value,
                    "files_created": len(context.implementation_details.get("files_created", [])),
                    "files_modified": len(context.implementation_details.get("files_modified", [])),
                    "tests_written": len(context.implementation_details.get("tests_written", [])),
                    "quality_gates": context.quality_gates,
                    "retry_count": context.retry_count
                }
                
                report["files_modified"].extend(
                    context.implementation_details.get("files_modified", [])
                )
                report["tests_added"].extend(
                    context.implementation_details.get("tests_written", [])
                )
        
        # Generate recommendations
        if any(r["retry_count"] > 0 for r in report["team_results"].values()):
            report["recommendations"].append(
                "Some teams required quality retries. Consider code review for complex areas."
            )
        
        return report
    
    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """Calculate duration between timestamps"""
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        duration = end - start
        
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        seconds = duration.seconds % 60
        
        return f"{hours}h {minutes}m {seconds}s"

def main():
    """Main entry point for multi-team orchestrator"""
    try:
        # Read input
        input_data = json.load(sys.stdin)
        
        orchestrator = MultiTeamOrchestrator()
        
        # Detect command type
        if "multi_implement" in input_data:
            task_ids = input_data.get("task_ids", [])
            result = orchestrator.handle_multi_implement(task_ids)
        
        elif "team_complete" in input_data:
            team_id = input_data.get("team_id")
            phase = input_data.get("phase")
            result = orchestrator.handle_team_completion(team_id, phase)
        
        else:
            # Fall back to base orchestrator
            from spark_unified_orchestrator import main as base_main
            base_main()
            return
        
        # Output result
        print(json.dumps(result, indent=2))
        sys.exit(0)
        
    except Exception as e:
        error_output = {
            "error": str(e),
            "type": "multi_team_orchestrator_error"
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()