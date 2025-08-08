#!/usr/bin/env python3
"""
SPARK System Comprehensive Test Suite
Tests all critical fixes and validates system integrity
"""

import json
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Test results collector
test_results = {
    "timestamp": datetime.now().isoformat(),
    "tests_run": 0,
    "tests_passed": 0,
    "tests_failed": 0,
    "critical_issues": [],
    "warnings": [],
    "details": {}
}


def run_test(test_name: str, test_func):
    """Run a single test and collect results"""
    global test_results
    test_results["tests_run"] += 1
    
    print(f"\n🧪 Testing: {test_name}")
    print("-" * 40)
    
    try:
        success, message = test_func()
        if success:
            test_results["tests_passed"] += 1
            print(f"✅ PASSED: {message}")
            test_results["details"][test_name] = {"status": "passed", "message": message}
        else:
            test_results["tests_failed"] += 1
            print(f"❌ FAILED: {message}")
            test_results["details"][test_name] = {"status": "failed", "message": message}
            test_results["critical_issues"].append(f"{test_name}: {message}")
        return success
    except Exception as e:
        test_results["tests_failed"] += 1
        error_msg = f"Exception: {str(e)}"
        print(f"💥 ERROR: {error_msg}")
        test_results["details"][test_name] = {"status": "error", "message": error_msg}
        test_results["critical_issues"].append(f"{test_name}: {error_msg}")
        return False


def test_hook_json_compliance() -> Tuple[bool, str]:
    """Test that hooks output proper JSON"""
    hooks_dir = Path.home() / ".claude" / "hooks"
    
    # Test persona router
    router_path = hooks_dir / "spark_persona_router.py"
    if not router_path.exists():
        return False, "Persona router not found"
    
    test_input = json.dumps({"prompt": "implement API endpoint"})
    try:
        result = subprocess.run(
            ["python3", str(router_path)],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return False, f"Router exited with code {result.returncode}"
        
        # Check if output is valid JSON
        if result.stdout:
            output = json.loads(result.stdout)
            if "hookSpecificOutput" not in output:
                return False, "Missing hookSpecificOutput in router output"
            if "additionalContext" not in output["hookSpecificOutput"]:
                return False, "Missing additionalContext in hookSpecificOutput"
        else:
            # No output is valid if task doesn't trigger SPARK
            pass
        
        return True, "Hook outputs valid JSON structure"
        
    except json.JSONDecodeError:
        return False, "Hook output is not valid JSON"
    except Exception as e:
        return False, f"Hook test failed: {e}"


def test_secure_command_execution() -> Tuple[bool, str]:
    """Test secure command execution without shell=True"""
    hooks_dir = Path.home() / ".claude" / "hooks"
    
    # Check quality gates for shell=True usage
    quality_gates_path = hooks_dir / "spark_quality_gates.py"
    if quality_gates_path.exists():
        content = quality_gates_path.read_text()
        if "shell=True" in content:
            return False, "Quality gates still uses shell=True"
    
    # Test secure executor
    sys.path.insert(0, str(hooks_dir))
    try:
        from spark_core_utils import SecureCommandExecutor
        
        executor = SecureCommandExecutor()
        
        # Test basic command
        success, stdout, stderr = executor.run_command(["echo", "test"])
        if not success or stdout.strip() != "test":
            return False, "Secure command execution failed"
        
        # Test path sanitization
        malicious_path = "../../../etc/passwd"
        safe_path = executor.sanitize_path(malicious_path)
        if safe_path is not None:
            return False, "Path traversal not blocked"
        
        return True, "Secure command execution working correctly"
        
    except ImportError:
        return False, "Could not import SecureCommandExecutor"
    except Exception as e:
        return False, f"Security test failed: {e}"


def test_state_management() -> Tuple[bool, str]:
    """Test state management system"""
    hooks_dir = Path.home() / ".claude" / "hooks"
    sys.path.insert(0, str(hooks_dir))
    
    try:
        from spark_core_utils import StateManager
        
        manager = StateManager()
        
        # Test write
        test_data = {
            "test_id": "state_test",
            "value": 42,
            "timestamp": datetime.now().isoformat()
        }
        
        if not manager.write_state(test_data):
            return False, "Failed to write state"
        
        # Test read
        read_data = manager.read_state()
        if read_data.get("test_id") != "state_test":
            return False, "State read/write mismatch"
        
        # Test update
        if not manager.update_state({"updated": True}):
            return False, "Failed to update state"
        
        # Test file exists
        if not manager.state_file.exists():
            return False, "State file not created"
        
        # Clean up
        manager.clear_state()
        
        return True, "State management system working correctly"
        
    except ImportError:
        return False, "Could not import StateManager"
    except Exception as e:
        return False, f"State management test failed: {e}"


def test_agent_chaining() -> Tuple[bool, str]:
    """Test agent chaining and data passing"""
    hooks_dir = Path.home() / ".claude" / "hooks"
    sys.path.insert(0, str(hooks_dir))
    
    try:
        from spark_core_utils import AgentChainManager
        
        manager = AgentChainManager()
        
        # Start a chain
        if not manager.start_chain("test_chain", ["agent1", "agent2", "agent3"]):
            return False, "Failed to start chain"
        
        # Pass data between agents
        test_data = {"result": "success", "value": 100}
        if not manager.pass_data("agent1", "agent2", test_data):
            return False, "Failed to pass data between agents"
        
        # Get data for agent2
        agent2_data = manager.get_data("agent2")
        if "agent1" not in agent2_data:
            return False, "Agent2 did not receive data from agent1"
        
        # Advance chain
        next_agent = manager.advance_chain()
        if next_agent != "agent2":
            return False, f"Chain advancement failed, expected agent2, got {next_agent}"
        
        # Get status
        status = manager.get_chain_status()
        if status.get("progress") != 33.3:
            return False, f"Progress calculation incorrect: {status.get('progress')}"
        
        return True, "Agent chaining working correctly"
        
    except ImportError:
        return False, "Could not import AgentChainManager"
    except Exception as e:
        return False, f"Agent chaining test failed: {e}"


def test_pipeline_orchestration() -> Tuple[bool, str]:
    """Test pipeline orchestration"""
    hooks_dir = Path.home() / ".claude" / "hooks"
    orchestrator_path = hooks_dir / "spark_pipeline_orchestrator.py"
    
    if not orchestrator_path.exists():
        return False, "Pipeline orchestrator not found"
    
    sys.path.insert(0, str(hooks_dir))
    
    try:
        from spark_pipeline_orchestrator import PipelineOrchestrator
        
        orchestrator = PipelineOrchestrator()
        
        # Start a pipeline
        result = orchestrator.start_pipeline(
            "test_pipeline",
            custom_agents=["tester", "implementer"]
        )
        
        if not result.get("success"):
            return False, "Failed to start pipeline"
        
        # Get status
        status = orchestrator.get_pipeline_status()
        if not status.get("active"):
            return False, "Pipeline not active after start"
        
        # Advance pipeline
        advance_result = orchestrator.advance_pipeline(
            "tester",
            {"test_results": "all passed"}
        )
        
        if not advance_result.get("success"):
            return False, "Failed to advance pipeline"
        
        # Abort pipeline (cleanup)
        orchestrator.abort_pipeline("Test completed")
        
        return True, "Pipeline orchestration working correctly"
        
    except ImportError:
        return False, "Could not import PipelineOrchestrator"
    except Exception as e:
        return False, f"Pipeline test failed: {e}"


def test_quality_gates_integration() -> Tuple[bool, str]:
    """Test quality gates with new secure patterns"""
    hooks_dir = Path.home() / ".claude" / "hooks"
    
    # Create a temporary test directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test Python file
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("""
def hello():
    '''Say hello'''
    print("Hello, World!")

if __name__ == "__main__":
    hello()
""")
        
        # Run quality gates
        quality_gates_path = hooks_dir / "spark_quality_gates.py"
        if not quality_gates_path.exists():
            return False, "Quality gates not found"
        
        test_input = json.dumps({
            "subagent": "test",
            "cwd": tmpdir
        })
        
        try:
            result = subprocess.run(
                ["python3", str(quality_gates_path)],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=tmpdir
            )
            
            if result.returncode != 0:
                return False, f"Quality gates exited with code {result.returncode}"
            
            # Check output is valid JSON
            if result.stdout:
                output = json.loads(result.stdout)
                if "hookSpecificOutput" not in output:
                    return False, "Missing hookSpecificOutput in quality gates output"
                
                decision = output["hookSpecificOutput"].get("decision")
                if decision not in ["block", "continue"]:
                    return False, f"Invalid decision value: {decision}"
            
            return True, "Quality gates integration working"
            
        except json.JSONDecodeError:
            return False, "Quality gates output is not valid JSON"
        except Exception as e:
            return False, f"Quality gates test failed: {e}"


def test_hook_communication() -> Tuple[bool, str]:
    """Test hook-to-hook communication via state"""
    hooks_dir = Path.home() / ".claude" / "hooks"
    sys.path.insert(0, str(hooks_dir))
    
    try:
        from spark_core_utils import StateManager
        
        # Simulate persona router writing state
        manager1 = StateManager()
        router_data = {
            "task_id": "test_123",
            "personas": ["Backend Developer"],
            "agents": ["implementer-spark"],
            "complexity": 0.7
        }
        
        if not manager1.write_state(router_data):
            return False, "Router failed to write state"
        
        # Simulate quality gates reading state
        manager2 = StateManager()
        gates_data = manager2.read_state()
        
        if gates_data.get("task_id") != "test_123":
            return False, "Quality gates couldn't read router state"
        
        if gates_data.get("complexity") != 0.7:
            return False, "State data corrupted in transfer"
        
        # Clean up
        manager1.clear_state()
        
        return True, "Hook communication via state working"
        
    except Exception as e:
        return False, f"Hook communication test failed: {e}"


def test_error_handling() -> Tuple[bool, str]:
    """Test error handling and recovery"""
    hooks_dir = Path.home() / ".claude" / "hooks"
    sys.path.insert(0, str(hooks_dir))
    
    try:
        from spark_core_utils import SecureCommandExecutor, StateManager
        
        executor = SecureCommandExecutor()
        
        # Test command timeout
        success, stdout, stderr = executor.run_command(
            ["sleep", "10"],
            timeout=1
        )
        
        if success:
            return False, "Timeout not working"
        
        if "timed out" not in stderr:
            return False, "Timeout error message incorrect"
        
        # Test invalid command
        success, stdout, stderr = executor.run_command(
            ["nonexistent_command_xyz"]
        )
        
        if success:
            return False, "Invalid command not caught"
        
        # Test state recovery
        manager = StateManager()
        
        # Write corrupted JSON to state file
        manager.state_file.parent.mkdir(parents=True, exist_ok=True)
        manager.state_file.write_text("{ invalid json }")
        
        # Should return default state instead of crashing
        state = manager.read_state()
        if "version" not in state:
            return False, "State recovery failed"
        
        return True, "Error handling working correctly"
        
    except Exception as e:
        return False, f"Error handling test failed: {e}"


def run_all_tests():
    """Run all tests and generate report"""
    print("=" * 60)
    print("🚀 SPARK System Comprehensive Test Suite")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Hook JSON Compliance", test_hook_json_compliance),
        ("Secure Command Execution", test_secure_command_execution),
        ("State Management", test_state_management),
        ("Agent Chaining", test_agent_chaining),
        ("Pipeline Orchestration", test_pipeline_orchestration),
        ("Quality Gates Integration", test_quality_gates_integration),
        ("Hook Communication", test_hook_communication),
        ("Error Handling", test_error_handling)
    ]
    
    for test_name, test_func in tests:
        run_test(test_name, test_func)
    
    # Generate report
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    print(f"Tests Run: {test_results['tests_run']}")
    print(f"Tests Passed: {test_results['tests_passed']}")
    print(f"Tests Failed: {test_results['tests_failed']}")
    print(f"Success Rate: {(test_results['tests_passed'] / test_results['tests_run'] * 100):.1f}%")
    
    if test_results['critical_issues']:
        print(f"\n⚠️ Critical Issues Found ({len(test_results['critical_issues'])}):")
        for issue in test_results['critical_issues']:
            print(f"  - {issue}")
    
    if test_results['warnings']:
        print(f"\n⚠️ Warnings ({len(test_results['warnings'])}):")
        for warning in test_results['warnings']:
            print(f"  - {warning}")
    
    # Save detailed report
    report_path = Path.home() / ".claude" / "test_report.json"
    with open(report_path, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n📝 Detailed report saved to: {report_path}")
    
    # Exit code based on results
    if test_results['tests_failed'] == 0:
        print("\n✅ All tests passed! System is fully operational.")
        return 0
    else:
        print(f"\n❌ {test_results['tests_failed']} tests failed. Please review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())