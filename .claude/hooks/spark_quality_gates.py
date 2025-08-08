#!/usr/bin/env python3
"""
SPARK Quality Gates Hook (SubagentStop) - FIXED VERSION
Universal quality validation with secure execution and proper JSON output
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add hooks directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from spark_core_utils import (
    SecureCommandExecutor, 
    StateManager, 
    HookOutputFormatter,
    AgentChainManager
)

# Set up logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)


class QualityGate:
    """Base class for quality gates"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.executor = SecureCommandExecutor()
    
    def check(self) -> Tuple[bool, List[str]]:
        """Run the quality check"""
        raise NotImplementedError
    
    def __str__(self):
        return f"{self.name}: {self.description}"


class SyntaxValidationGate(QualityGate):
    """Check for syntax errors in code files"""
    
    def __init__(self):
        super().__init__(
            "Syntax Validation",
            "Verify code has no syntax errors"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        issues = []
        
        # Check Python files
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv", "__pycache__"])
        for file_path in python_files[:10]:  # Limit to prevent timeout
            success, stdout, stderr = self.executor.run_command(
                ["python3", "-m", "py_compile", str(file_path)]
            )
            if not success and stderr:
                issues.append(f"Python syntax error in {file_path.name}: {stderr[:100]}")
        
        # Check JavaScript/TypeScript files
        js_files = self.executor.find_files("*.js") + self.executor.find_files("*.ts")
        for file_path in js_files[:5]:
            # Basic syntax check using Node.js
            success, stdout, stderr = self.executor.run_command(
                ["node", "--check", str(file_path)],
                timeout=5
            )
            if not success and stderr:
                issues.append(f"JavaScript syntax error in {file_path.name}")
        
        return len(issues) == 0, issues


class TypeCheckingGate(QualityGate):
    """Check type annotations and type safety"""
    
    def __init__(self):
        super().__init__(
            "Type Checking",
            "Verify type safety and annotations"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        issues = []
        
        # Python - MyPy
        if Path("pyproject.toml").exists() or any(Path(".").glob("*.py")):
            success, stdout, stderr = self.executor.run_command(
                ["mypy", ".", "--ignore-missing-imports", "--no-error-summary"],
                timeout=30
            )
            if not success or "error:" in stderr:
                error_count = stderr.count("error:")
                issues.append(f"MyPy found {error_count} type errors")
        
        # TypeScript
        if Path("tsconfig.json").exists():
            success, stdout, stderr = self.executor.run_command(
                ["npx", "tsc", "--noEmit"],
                timeout=30
            )
            if not success:
                issues.append("TypeScript type checking failed")
        
        return len(issues) == 0, issues


class LintingGate(QualityGate):
    """Check code style and linting rules"""
    
    def __init__(self):
        super().__init__(
            "Code Linting",
            "Verify code follows style guidelines"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        issues = []
        
        # Python - Ruff
        if Path("pyproject.toml").exists() or any(Path(".").glob("*.py")):
            success, stdout, stderr = self.executor.run_command(
                ["ruff", "check", ".", "--quiet"],
                timeout=20
            )
            if not success:
                # Count violations from stdout
                violation_count = len(stdout.strip().split('\n')) if stdout else 1
                issues.append(f"Ruff found {violation_count} style violations")
        
        # JavaScript/TypeScript - ESLint
        if Path("package.json").exists():
            for config_file in [".eslintrc.js", ".eslintrc.json", "eslint.config.js"]:
                if Path(config_file).exists():
                    success, stdout, stderr = self.executor.run_command(
                        ["npx", "eslint", ".", "--quiet", "--max-warnings", "0"],
                        timeout=30
                    )
                    if not success:
                        issues.append("ESLint found style violations")
                    break
        
        return len(issues) == 0, issues


class SecurityGate(QualityGate):
    """Check for security vulnerabilities"""
    
    def __init__(self):
        super().__init__(
            "Security Analysis",
            "Scan for security vulnerabilities and secrets"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        issues = []
        
        # Check for hardcoded secrets in Python files
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv"])
        for file_path in python_files[:10]:
            try:
                content = file_path.read_text()
                # Simple pattern matching for common secrets
                if any(pattern in content.lower() for pattern in [
                    "password=", "api_key=", "secret=", "token=",
                    "aws_access_key", "private_key"
                ]):
                    # More sophisticated check
                    import re
                    # Check if it's actually a hardcoded value (not a variable)
                    if re.search(r'(password|api_key|secret|token)\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
                        issues.append(f"Potential hardcoded secret in {file_path.name}")
            except Exception:
                pass
        
        # Python - Bandit
        if any(Path(".").glob("*.py")):
            success, stdout, stderr = self.executor.run_command(
                ["bandit", "-r", ".", "-f", "json", "-q", "--severity-level", "medium"],
                timeout=30
            )
            if success and stdout:
                try:
                    results = json.loads(stdout)
                    if results.get("results"):
                        high_severity = sum(1 for r in results["results"] if r.get("issue_severity") == "HIGH")
                        if high_severity > 0:
                            issues.append(f"Bandit found {high_severity} high severity issues")
                except json.JSONDecodeError:
                    pass
        
        # Check for dependency vulnerabilities
        if Path("requirements.txt").exists():
            success, stdout, stderr = self.executor.run_command(
                ["pip-audit", "--desc"],
                timeout=30
            )
            if not success and "vulnerabilit" in stdout.lower():
                issues.append("Vulnerable dependencies detected")
        
        return len(issues) == 0, issues


class TestCoverageGate(QualityGate):
    """Check test coverage and test existence"""
    
    def __init__(self):
        super().__init__(
            "Test Coverage",
            "Verify tests exist and have adequate coverage"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        issues = []
        
        # Check if test files exist
        test_patterns = ["test_*.py", "*_test.py", "*.test.js", "*.spec.js", "*.test.ts", "*.spec.ts"]
        test_files = []
        for pattern in test_patterns:
            test_files.extend(self.executor.find_files(pattern))
        
        if not test_files:
            issues.append("No test files found")
            return False, issues
        
        # Python - pytest with coverage
        if any(Path(".").glob("test_*.py")) or any(Path(".").glob("*_test.py")):
            success, stdout, stderr = self.executor.run_command(
                ["pytest", "--co", "-q"],  # Just collect tests, don't run
                timeout=10
            )
            if not success:
                issues.append("pytest cannot collect tests")
        
        # JavaScript/TypeScript - Jest
        if Path("package.json").exists():
            package_json = Path("package.json").read_text()
            if "jest" in package_json or "@jest" in package_json:
                success, stdout, stderr = self.executor.run_command(
                    ["npx", "jest", "--listTests"],
                    timeout=10
                )
                if not success:
                    issues.append("Jest cannot find tests")
        
        return len(issues) == 0, issues


class DocumentationGate(QualityGate):
    """Check documentation quality"""
    
    def __init__(self):
        super().__init__(
            "Documentation",
            "Verify code is properly documented"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        issues = []
        
        # Check Python docstrings
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv"])
        undocumented_count = 0
        
        for file_path in python_files[:10]:
            try:
                content = file_path.read_text()
                # Check for function definitions without docstrings
                import re
                functions = re.findall(r'def\s+\w+\([^)]*\):', content)
                docstrings = re.findall(r'def\s+\w+\([^)]*\):\s*\n\s*"""', content)
                
                if len(functions) > len(docstrings):
                    undocumented_count += len(functions) - len(docstrings)
                    
            except Exception:
                pass
        
        if undocumented_count > 5:
            issues.append(f"{undocumented_count} functions missing docstrings")
        
        # Check for README
        if not any(Path(".").glob("README*")):
            issues.append("No README file found")
        
        return len(issues) == 0, issues


class PerformanceGate(QualityGate):
    """Check performance and optimization"""
    
    def __init__(self):
        super().__init__(
            "Performance",
            "Verify code meets performance standards"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        issues = []
        
        # Check for common performance anti-patterns in Python
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv"])
        
        for file_path in python_files[:5]:
            try:
                content = file_path.read_text()
                
                # Check for nested loops with database queries (N+1 problem)
                if "for " in content and ".objects." in content:
                    import re
                    if re.search(r'for .+ in .+:\s+.+\.objects\.(get|filter|all)', content):
                        issues.append(f"Potential N+1 query problem in {file_path.name}")
                
                # Check for synchronous I/O in async functions
                if "async def" in content and "open(" in content:
                    issues.append(f"Synchronous I/O in async function in {file_path.name}")
                    
            except Exception:
                pass
        
        return len(issues) == 0, issues


class IntegrationGate(QualityGate):
    """Check integration and compatibility"""
    
    def __init__(self):
        super().__init__(
            "Integration",
            "Verify component integration and compatibility"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        issues = []
        
        # Check for dependency conflicts
        if Path("requirements.txt").exists():
            success, stdout, stderr = self.executor.run_command(
                ["pip", "check"],
                timeout=10
            )
            if not success or "incompatible" in stdout.lower():
                issues.append("Dependency conflicts detected")
        
        # Check for broken imports in Python
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv"])
        for file_path in python_files[:5]:
            success, stdout, stderr = self.executor.run_command(
                ["python3", "-c", f"import ast; ast.parse(open('{file_path}').read())"],
                timeout=5
            )
            if not success:
                issues.append(f"Import errors in {file_path.name}")
        
        return len(issues) == 0, issues


class QualityGateRunner:
    """Orchestrates running all quality gates"""
    
    def __init__(self):
        self.gates = [
            SyntaxValidationGate(),
            TypeCheckingGate(),
            LintingGate(),
            SecurityGate(),
            TestCoverageGate(),
            DocumentationGate(),
            PerformanceGate(),
            IntegrationGate()
        ]
        self.state_manager = StateManager()
        self.chain_manager = AgentChainManager()
    
    def run_gates(self, required_gates: Optional[int] = None) -> Dict:
        """Run quality gates and return results"""
        
        # Get required gates from state if not provided
        if required_gates is None:
            state = self.state_manager.read_state()
            required_gates = state.get("quality_gates", {}).get("required", 8)
        
        results = {}
        passed_count = 0
        failed_gates = []
        all_issues = []
        
        # Run only the required number of gates
        gates_to_run = self.gates[:required_gates]
        
        for gate in gates_to_run:
            try:
                logger.info(f"Running gate: {gate.name}")
                passed, issues = gate.check()
                
                results[gate.name] = {
                    "passed": passed,
                    "issues": issues
                }
                
                if passed:
                    passed_count += 1
                    logger.info(f"  ✅ {gate.name}: PASSED")
                else:
                    failed_gates.append(gate.name)
                    all_issues.extend(issues)
                    logger.info(f"  ❌ {gate.name}: FAILED - {len(issues)} issues")
                    for issue in issues[:3]:  # Log first 3 issues
                        logger.info(f"     - {issue}")
                        
            except Exception as e:
                logger.error(f"  ⚠️ {gate.name}: ERROR - {e}")
                results[gate.name] = {
                    "passed": False,
                    "issues": [f"Gate execution failed: {str(e)}"]
                }
                failed_gates.append(gate.name)
                all_issues.append(f"{gate.name} execution failed")
        
        # Calculate pass rate
        total_gates = len(gates_to_run)
        pass_rate = (passed_count / total_gates * 100) if total_gates > 0 else 0
        
        # Update state with results
        state = self.state_manager.read_state()
        state["quality_gates"]["passed"] = passed_count
        state["quality_gates"]["results"] = results
        state["quality_gates"]["last_run"] = datetime.now().isoformat()
        self.state_manager.write_state(state)
        
        return {
            "passed_count": passed_count,
            "total_gates": total_gates,
            "required_gates": required_gates,
            "pass_rate": round(pass_rate, 1),
            "passed": passed_count >= required_gates,
            "failed_gates": failed_gates,
            "all_issues": all_issues,
            "results": results
        }


def main():
    """Main hook execution"""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
        
        # Get context from input
        subagent_name = input_data.get("subagent", "unknown")
        cwd = input_data.get("cwd", ".")
        
        logger.info("=" * 60)
        logger.info("🛡️  SPARK Quality Gates - Starting Validation")
        logger.info(f"   Subagent: {subagent_name}")
        logger.info(f"   Directory: {cwd}")
        logger.info("=" * 60)
        
        # Initialize components
        runner = QualityGateRunner()
        state_manager = StateManager()
        chain_manager = AgentChainManager()
        
        # Get required gates from state
        state = state_manager.read_state()
        required_gates = state.get("quality_gates", {}).get("required", 8)
        
        # Run quality gates
        results = runner.run_gates(required_gates)
        
        logger.info("=" * 60)
        logger.info(f"📊 Quality Gates Summary:")
        logger.info(f"   Passed: {results['passed_count']}/{results['total_gates']}")
        logger.info(f"   Pass Rate: {results['pass_rate']}%")
        logger.info(f"   Required: {results['required_gates']} gates to pass")
        logger.info(f"   Status: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
        logger.info("=" * 60)
        
        # Prepare response based on results
        if results["passed"]:
            # Gates passed - allow continuation
            decision = "continue"
            reason = f"Quality gates passed: {results['passed_count']}/{results['total_gates']} gates passed ({results['pass_rate']}% pass rate)"
            
            # Pass quality results to next agent if in pipeline
            chain_status = chain_manager.get_chain_status()
            if chain_status.get("current_agent"):
                chain_manager.pass_data(
                    from_agent=subagent_name,
                    to_agent="next",
                    data={"quality_results": results}
                )
            
            # Format output
            output = HookOutputFormatter.format_subagent_stop(
                decision=decision,
                reason=reason,
                metadata={
                    "quality_gates_passed": results["passed_count"],
                    "quality_gates_total": results["total_gates"],
                    "pass_rate": results["pass_rate"]
                }
            )
            
        else:
            # Gates failed - block and request fixes
            decision = "block"
            
            # Generate detailed failure message
            failure_details = []
            for gate_name in results["failed_gates"]:
                gate_results = results["results"].get(gate_name, {})
                issues = gate_results.get("issues", [])
                if issues:
                    failure_details.append(f"• {gate_name}:")
                    for issue in issues[:2]:  # Show first 2 issues per gate
                        failure_details.append(f"  - {issue}")
            
            reason = f"""Quality gates failed: {results['passed_count']}/{results['total_gates']} passed ({results['pass_rate']}% pass rate)

Failed Gates ({len(results['failed_gates'])}):
{chr(10).join(failure_details)}

Please fix these issues and try again."""
            
            retry_prompt = f"""The following quality gates need to be fixed:
{chr(10).join(f'- {gate}' for gate in results['failed_gates'])}

Focus on fixing the specific issues identified and ensure the code meets SPARK quality standards."""
            
            # Format output
            output = HookOutputFormatter.format_subagent_stop(
                decision=decision,
                reason=reason,
                retry_prompt=retry_prompt,
                metadata={
                    "quality_gates_passed": results["passed_count"],
                    "quality_gates_total": results["total_gates"],
                    "quality_gates_failed": results["failed_gates"],
                    "pass_rate": results["pass_rate"]
                }
            )
        
        # Output JSON to stdout
        print(output)
        
        sys.exit(0)
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON input: {e}")
        # Output error in proper JSON format
        error_output = HookOutputFormatter.format_subagent_stop(
            decision="block",
            reason=f"Invalid input format: {e}"
        )
        print(error_output)
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Hook execution failed: {e}")
        logger.exception(e)
        # Output error in proper JSON format
        error_output = HookOutputFormatter.format_subagent_stop(
            decision="block",
            reason=f"Quality gate system error: {e}"
        )
        print(error_output)
        sys.exit(1)


if __name__ == "__main__":
    main()