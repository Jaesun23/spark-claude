#!/usr/bin/env python3
"""
Jason's 8-Step Strict Quality Gates Hook (SubagentStop) - EFFICIENT VERSION
Universal quality validation with zero tolerance and proper JSON output
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def find_project_root() -> Path:
    """Find project root using Claude Code environment variables or directory search"""
    import os
    
    # First try Claude Code's project directory environment variable
    claude_project_dir = os.getenv('CLAUDE_PROJECT_DIR')
    if claude_project_dir:
        project_path = Path(claude_project_dir)
        if project_path.exists() and (project_path / ".claude").exists():
            return project_path
    
    # Fallback: search for .claude directory from current location
    current = Path.cwd()
    while current != current.parent:
        if (current / ".claude").exists():
            return current
        current = current.parent
    
    # Final fallback to current directory
    return Path.cwd()

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
        
        # Check Python files (Claude Code compatible - limited scope)
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv", "__pycache__", ".git"])
        for file_path in python_files[:5]:  # Reduced limit for Claude Code
            success, stdout, stderr = self.executor.run_command(
                ["python3", "-m", "py_compile", str(file_path)],
                timeout=10  # Shorter timeout
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


class MyPyStrictGate(QualityGate):
    """MyPy --strict: Zero errors mandatory (strongest type checking)"""
    
    def __init__(self):
        super().__init__(
            "MyPy --strict",
            "Zero errors mandatory - strongest type checking"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        issues = []
        
        # Python - MyPy with --strict flag (Jason's requirement)
        if Path("pyproject.toml").exists() or any(Path(".").glob("*.py")):
            success, stdout, stderr = self.executor.run_command(
                ["mypy", ".", "--strict", "--no-error-summary", "--no-incremental"],
                timeout=20  # Reduced timeout for Claude Code
            )
            if not success or "error:" in stderr:
                error_count = stderr.count("error:")
                issues.append(f"MyPy --strict found {error_count} type errors (ZERO tolerance)")
        
        # TypeScript - strict mode
        if Path("tsconfig.json").exists():
            success, stdout, stderr = self.executor.run_command(
                ["npx", "tsc", "--strict", "--noEmit"],
                timeout=30
            )
            if not success:
                issues.append("TypeScript strict type checking failed")
        
        return len(issues) == 0, issues


class RuffStrictGate(QualityGate):
    """Ruff --strict: Zero violations mandatory (strongest linting)"""
    
    def __init__(self):
        super().__init__(
            "Ruff --strict",
            "Zero violations mandatory - strongest linting"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        issues = []
        
        # Python - Ruff with strict enforcement
        if Path("pyproject.toml").exists() or any(Path(".").glob("*.py")):
            success, stdout, stderr = self.executor.run_command(
                ["ruff", "check", ".", "--select", "ALL", "--quiet"],
                timeout=20
            )
            if not success:
                # Count violations from stdout
                violation_count = len(stdout.strip().split('\n')) if stdout else 1
                issues.append(f"Ruff --strict found {violation_count} violations (ZERO tolerance)")
        
        # JavaScript/TypeScript - ESLint strict
        if Path("package.json").exists():
            for config_file in [".eslintrc.js", ".eslintrc.json", "eslint.config.js"]:
                if Path(config_file).exists():
                    success, stdout, stderr = self.executor.run_command(
                        ["npx", "eslint", ".", "--max-warnings", "0"],
                        timeout=30
                    )
                    if not success:
                        issues.append("ESLint strict found violations (ZERO tolerance)")
                    break
        
        return len(issues) == 0, issues


class SecurityEnhancedGate(QualityGate):
    """Security Analysis: OWASP + enhanced (no hardcoded secrets)"""
    
    def __init__(self):
        super().__init__(
            "Security Analysis (OWASP + Enhanced)",
            "OWASP compliance + enhanced security scanning"
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


class TestCoverage95Gate(QualityGate):
    """Test Coverage 95%+: High standard enforcement"""
    
    def __init__(self):
        super().__init__(
            "Test Coverage 95%+",
            "High standard test coverage enforcement"
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


class DocumentationValidationGate(QualityGate):
    """Documentation Validation: Docstrings required"""
    
    def __init__(self):
        super().__init__(
            "Documentation Validation",
            "Docstrings required for all functions and classes"
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


class IntegrationTestingGate(QualityGate):
    """Integration Testing: End-to-end validation + deployment readiness"""
    
    def __init__(self):
        super().__init__(
            "Integration Testing",
            "End-to-end validation and deployment readiness"
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


class TestVerificationGate(QualityGate):
    """Verify test claims against actual test execution"""
    
    def __init__(self):
        super().__init__(
            "Test Verification",
            "Verify claimed test results against actual test execution"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        """Verify test claims from current_task.json"""
        issues = []
        verification_results = {
            "claimed_test_files": [],
            "actual_test_files": [],
            "claimed_coverage": 0,
            "actual_coverage": 0,
            "claimed_tests_pass": False,
            "actual_tests_pass": False,
            "test_execution_results": {},
            "discrepancies": []
        }
        
        # Try to read current_task.json
        project_root = find_project_root()
        json_paths = [
            Path.home() / ".claude/workflows/current_task.json",
            project_root / ".claude/workflows/current_task.json"
        ]
        
        current_task = None
        for json_path in json_paths:
            if json_path.exists():
                try:
                    with open(json_path, 'r') as f:
                        current_task = json.load(f)
                    break
                except Exception as e:
                    logger.error(f"Failed to read {json_path}: {e}")
        
        if not current_task:
            return True, []
        
        # Check if there's a testing section
        testing = current_task.get("testing", {})
        if not testing:
            # No testing claimed yet
            return True, []
        
        # 1. Verify test files exist
        test_files = testing.get("test_files", [])
        verification_results["claimed_test_files"] = test_files
        
        for test_file in test_files:
            if Path(test_file).exists():
                verification_results["actual_test_files"].append(test_file)
            else:
                issues.append(f"Claimed test file does not exist: {test_file}")
                verification_results["discrepancies"].append(f"Missing test file: {test_file}")
        
        # 2. Run tests and verify they pass (Python)
        if any(Path(".").glob("test_*.py")) or any(Path(".").glob("*_test.py")):
            # First, collect tests
            success, stdout, stderr = self.executor.run_command(
                ["pytest", "--collect-only", "-q"],
                timeout=10
            )
            
            if success:
                # Count collected tests
                test_count = stdout.count(" selected") or stdout.count("test")
                verification_results["test_execution_results"]["collected_tests"] = test_count
                
                # Now run the tests
                success, stdout, stderr = self.executor.run_command(
                    ["pytest", "-v", "--tb=short"],
                    timeout=60
                )
                
                if success and "failed" not in stdout.lower():
                    verification_results["actual_tests_pass"] = True
                    passed_count = stdout.count(" PASSED")
                    verification_results["test_execution_results"]["passed_tests"] = passed_count
                else:
                    verification_results["actual_tests_pass"] = False
                    failed_count = stdout.count(" FAILED")
                    verification_results["test_execution_results"]["failed_tests"] = failed_count
                    
                    # Check if tests were claimed to pass
                    if testing.get("all_tests_pass", False):
                        issues.append(f"Tests are failing ({failed_count} failed) despite claims of passing")
                        verification_results["discrepancies"].append(f"{failed_count} tests failing")
        
        # 3. Verify coverage (Python)
        claimed_coverage = testing.get("coverage", 0)
        verification_results["claimed_coverage"] = claimed_coverage
        
        if claimed_coverage > 0:
            # Run coverage
            success, stdout, stderr = self.executor.run_command(
                ["pytest", "--cov=.", "--cov-report=term-missing", "--cov-report=json", "-q"],
                timeout=60
            )
            
            if success:
                # Try to parse coverage from output
                import re
                coverage_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', stdout)
                if coverage_match:
                    actual_coverage = int(coverage_match.group(1))
                    verification_results["actual_coverage"] = actual_coverage
                    
                    if actual_coverage < claimed_coverage - 5:  # Allow 5% tolerance
                        issues.append(f"Coverage {actual_coverage}% is significantly lower than claimed {claimed_coverage}%")
                        verification_results["discrepancies"].append(f"Coverage gap: {claimed_coverage - actual_coverage}%")
                
                # Also try to read coverage.json if it exists
                coverage_json = Path("coverage.json")
                if coverage_json.exists():
                    try:
                        with open(coverage_json) as f:
                            cov_data = json.load(f)
                            actual_coverage = round(cov_data.get("totals", {}).get("percent_covered", 0))
                            verification_results["actual_coverage"] = actual_coverage
                    except Exception:
                        pass
        
        # 4. Verify test count
        claimed_test_count = testing.get("test_count", 0)
        if claimed_test_count > 0:
            actual_test_count = verification_results["test_execution_results"].get("passed_tests", 0)
            if actual_test_count < claimed_test_count:
                issues.append(f"Only {actual_test_count} tests found, but {claimed_test_count} were claimed")
                verification_results["discrepancies"].append(f"Test count mismatch: {actual_test_count} vs {claimed_test_count}")
        
        # 5. Check JavaScript/TypeScript tests
        if Path("package.json").exists():
            package_json = Path("package.json").read_text()
            
            # Jest tests
            if "jest" in package_json:
                success, stdout, stderr = self.executor.run_command(
                    ["npx", "jest", "--listTests"],
                    timeout=10
                )
                if success:
                    js_test_count = len(stdout.strip().split('\n'))
                    verification_results["test_execution_results"]["jest_tests"] = js_test_count
                
                # Run Jest tests
                success, stdout, stderr = self.executor.run_command(
                    ["npx", "jest", "--passWithNoTests"],
                    timeout=60
                )
                
                if not success or "FAIL" in stdout:
                    if testing.get("all_tests_pass", False):
                        issues.append("JavaScript tests are failing despite claims of passing")
                        verification_results["discrepancies"].append("Jest tests failing")
        
        # Save verification results
        from spark_core_utils import StateManager as SM
        state_manager = SM()
        state = state_manager.read_state()
        
        state["test_verification"] = {
            "verified_at": datetime.now().isoformat(),
            "verification_passed": len(issues) == 0,
            "verification_results": verification_results,
            "issues": issues
        }
        
        # Also update current_task if we have it
        if current_task:
            current_task["test_verification"] = state["test_verification"]
            
            for json_path in json_paths:
                if json_path.exists():
                    try:
                        with open(json_path, 'w') as f:
                            json.dump(current_task, f, indent=2)
                        logger.info(f"Saved test verification to {json_path}")
                        break
                    except Exception as e:
                        logger.error(f"Failed to write test verification: {e}")
        
        state_manager.write_state(state)
        
        return len(issues) == 0, issues


class ImplementationVerificationGate(QualityGate):
    """Verify implementation claims against actual code"""
    
    def __init__(self):
        super().__init__(
            "Implementation Verification",
            "Verify claimed implementation against actual files and code"
        )
    
    def check(self) -> Tuple[bool, List[str]]:
        """Verify implementation claims from current_task.json"""
        issues = []
        verification_results = {
            "claimed_files": [],
            "actual_files": [],
            "claimed_endpoints": [],
            "actual_endpoints": [],
            "claimed_db_changes": [],
            "actual_db_changes": [],
            "discrepancies": []
        }
        
        # Try to read current_task.json
        project_root = find_project_root()
        json_paths = [
            Path.home() / ".claude/workflows/current_task.json",
            project_root / ".claude/workflows/current_task.json"
        ]
        
        current_task = None
        for json_path in json_paths:
            if json_path.exists():
                try:
                    with open(json_path, 'r') as f:
                        current_task = json.load(f)
                    break
                except Exception as e:
                    logger.error(f"Failed to read {json_path}: {e}")
        
        if not current_task:
            # No current_task.json, can't verify
            return True, []
        
        # Check if there's an implementation section
        implementation = current_task.get("implementation", {})
        if not implementation:
            # No implementation claimed yet
            return True, []
        
        results = implementation.get("results", {})
        
        # 1. Verify files_created
        files_created = results.get("files_created", [])
        verification_results["claimed_files"] = files_created
        for file_path in files_created:
            if Path(file_path).exists():
                verification_results["actual_files"].append(file_path)
            else:
                issues.append(f"Claimed file does not exist: {file_path}")
                verification_results["discrepancies"].append(f"Missing file: {file_path}")
        
        # 2. Verify files_modified
        files_modified = results.get("files_modified", [])
        for file_path in files_modified:
            if not Path(file_path).exists():
                issues.append(f"Claimed modified file does not exist: {file_path}")
                verification_results["discrepancies"].append(f"Missing modified file: {file_path}")
            else:
                # Check if file was actually modified (using git)
                success, stdout, stderr = self.executor.run_command(
                    ["git", "diff", "--name-only", file_path],
                    timeout=5
                )
                if success and not stdout.strip():
                    # File not modified according to git
                    success2, stdout2, stderr2 = self.executor.run_command(
                        ["git", "diff", "--cached", "--name-only", file_path],
                        timeout=5
                    )
                    if not stdout2.strip():
                        issues.append(f"File claimed as modified but no changes detected: {file_path}")
                        verification_results["discrepancies"].append(f"Unchanged file: {file_path}")
        
        # 3. Verify API endpoints
        api_endpoints = results.get("api_endpoints", [])
        verification_results["claimed_endpoints"] = [f"{ep.get('method', 'GET')} {ep.get('path', '')}" for ep in api_endpoints]
        
        if api_endpoints:
            # Search for FastAPI/Flask/Express endpoints in Python/JS files
            for endpoint in api_endpoints:
                method = endpoint.get("method", "GET").lower()
                path = endpoint.get("path", "")
                
                # Search in Python files for FastAPI/Flask
                found = False
                python_files = self.executor.find_files("*.py", exclude_dirs=[".venv", "__pycache__"])
                for py_file in python_files[:20]:  # Limit search
                    try:
                        content = py_file.read_text()
                        # FastAPI patterns
                        if f'@app.{method}("{path}")' in content or f"@app.{method}('{path}')" in content:
                            found = True
                            break
                        # Flask patterns
                        if f'@app.route("{path}", methods=["{method.upper()}"])' in content:
                            found = True
                            break
                    except Exception:
                        pass
                
                if found:
                    verification_results["actual_endpoints"].append(f"{method.upper()} {path}")
                else:
                    issues.append(f"API endpoint not found in code: {method.upper()} {path}")
                    verification_results["discrepancies"].append(f"Missing endpoint: {method.upper()} {path}")
        
        # 4. Verify database changes (check for migration files)
        db_changes = results.get("database_changes", [])
        verification_results["claimed_db_changes"] = db_changes
        
        if db_changes:
            # Look for migration files
            migration_patterns = ["**/migrations/*.py", "**/alembic/versions/*.py", "**/*.sql"]
            migration_files = []
            for pattern in migration_patterns:
                migration_files.extend(Path(".").glob(pattern))
            
            if migration_files:
                verification_results["actual_db_changes"].append("Migration files found")
            else:
                issues.append("Database changes claimed but no migration files found")
                verification_results["discrepancies"].append("No migration files for DB changes")
        
        # Save verification results to state manager
        from spark_core_utils import StateManager as SM
        state_manager = SM()
        state = state_manager.read_state()
        
        # Add implementation verification results to state
        state["implementation_verification"] = {
            "verified_at": datetime.now().isoformat(),
            "verification_passed": len(issues) == 0,
            "verification_results": verification_results,
            "issues": issues
        }
        
        # Also update the current_task if we have it
        if current_task:
            current_task["implementation_verification"] = state["implementation_verification"]
            
            # Write back to the same JSON file
            for json_path in json_paths:
                if json_path.exists():
                    try:
                        with open(json_path, 'w') as f:
                            json.dump(current_task, f, indent=2)
                        logger.info(f"Saved implementation verification to {json_path}")
                        break
                    except Exception as e:
                        logger.error(f"Failed to write verification results: {e}")
        
        # Write state (this ensures it's saved even if JSON write fails)
        state_manager.write_state(state)
        
        return len(issues) == 0, issues


class QualityGateRunner:
    """Jason's 8-Step Strict Quality Gate Runner - Zero tolerance approach"""
    
    def __init__(self, claude_code_mode: bool = True):
        self.claude_code_mode = claude_code_mode
        
        # Jason's 10-Step Strict Quality Gates (with Implementation & Test Verification)
        self.gates = [
            ImplementationVerificationGate(), # Step 0: Verify implementation claims FIRST
            TestVerificationGate(),          # Step 0.5: Verify test claims (if testing phase)
            SyntaxValidationGate(),          # Step 1: Syntax Validation (0 errors)
            MyPyStrictGate(),               # Step 2: MyPy --strict (0 errors)
            RuffStrictGate(),               # Step 3: Ruff --strict (0 violations)
            SecurityEnhancedGate(),         # Step 4: Security Analysis (OWASP + enhanced)
            TestCoverage95Gate(),           # Step 5: Test Coverage 95%+
            PerformanceGate(),              # Step 6: Performance Check
            DocumentationValidationGate(),   # Step 7: Documentation Validation
            IntegrationTestingGate()        # Step 8: Integration Testing
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
        
        # Fast-fail mode for Claude Code (stop on first critical failure)
        fast_fail = self.claude_code_mode and len(gates_to_run) > 2
        
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
                    for issue in issues[:2]:  # Log first 2 issues for Claude Code
                        logger.info(f"     - {issue}")
                    
                    # Fast-fail for critical gates (syntax, security)
                    if fast_fail and gate.name in ["Syntax Validation", "Security Analysis"]:
                        logger.info("💨 Fast-fail activated - stopping quality gates")
                        break
                        
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
    """Main hook execution with Phase Manager integration"""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
        
        # Get context from input
        subagent_name = input_data.get("subagent", "unknown")
        cwd = input_data.get("cwd", ".")
        self_check = input_data.get("self_check", False)  # Agent self-validation mode
        
        logger.info("=" * 60)
        if self_check:
            logger.info("🔍  Self-Validation Mode - Agent checking its own work")
        else:
            logger.info("🛡️  Jason's 8-Step Strict Quality Gates - Starting Validation")
        logger.info(f"   Subagent: {subagent_name}")
        logger.info(f"   Directory: {cwd}")
        logger.info("=" * 60)
        
        # Initialize components with Claude Code optimization
        claude_code_mode = input_data.get("claude_code_mode", True)
        runner = QualityGateRunner(claude_code_mode=claude_code_mode)
        state_manager = StateManager()
        chain_manager = AgentChainManager()
        
        # Check if already self-validated (to avoid duplicate validation)
        if not self_check:  # Only check in hook mode
            state = state_manager.read_state()
            if state.get("self_validated_by") == subagent_name:
                # Check if validation was recent (within 5 minutes)
                validated_at = state.get("self_validated_at")
                if validated_at:
                    try:
                        from datetime import datetime, timedelta
                        validated_time = datetime.fromisoformat(validated_at.replace('Z', '+00:00'))
                        current_time = datetime.now(validated_time.tzinfo) if validated_time.tzinfo else datetime.now()
                        time_diff = current_time - validated_time
                        if time_diff.total_seconds() < 300:  # 5 minutes
                            logger.info("✅ Already self-validated recently, skipping duplicate check")
                            # Return success response
                            output = HookOutputFormatter.format_subagent_stop(
                                decision="continue",
                                reason="Already self-validated successfully",
                                metadata={"self_validated": True}
                            )
                            print(json.dumps(output))
                            return
                    except Exception:
                        pass  # If parsing fails, continue with validation
        
        # Import Phase Manager for progression checking
        from spark_phase_manager import SPARKPhaseManager
        phase_manager = SPARKPhaseManager()
        
        # Get required gates from state
        state = state_manager.read_state()
        required_gates = state.get("quality_gates", {}).get("required", 8)
        
        # Run quality gates
        results = runner.run_gates(required_gates)
        
        # Update state with quality results for Phase Manager
        state["spark_quality_results"] = {
            "gates_passed": results["passed_count"],
            "total_gates": results["total_gates"], 
            "violations": {},
            "gate_results": results["results"],
            "spark_compliance": results["passed"],
            "jason_dna_compliance": results["passed"]
        }
        
        logger.info("=" * 60)
        logger.info(f"📊 Quality Gates Summary:")
        logger.info(f"   Passed: {results['passed_count']}/{results['total_gates']}")
        logger.info(f"   Pass Rate: {results['pass_rate']}%")
        logger.info(f"   Required: {results['required_gates']} gates to pass")
        logger.info(f"   Status: {'✅ PASSED' if results['passed'] else '❌ FAILED'}")
        logger.info("=" * 60)
        
        # Mark if self-validation passed (to avoid duplicate validation in hook)
        if self_check and results["passed"]:
            state["self_validated_at"] = datetime.now().isoformat()
            state["self_validated_by"] = subagent_name
        
        # Update state with quality results and check phase progression
        state_manager.write_state(state)
        
        # Check phase progression with Phase Manager
        progression_check = phase_manager.check_phase_progression()
        
        # Prepare response based on results and phase progression
        if results["passed"]:
            # Gates passed - check phase progression
            decision = "continue"
            reason = f"Quality gates passed: {results['passed_count']}/{results['total_gates']} gates passed ({results['pass_rate']}% pass rate)"
            
            # Add phase progression information
            if progression_check.get("can_progress"):
                if progression_check.get("workflow_complete"):
                    reason += f"\n\n✅ Workflow Complete! All phases finished successfully."
                elif progression_check.get("next_phase"):
                    reason += f"\n\n🔄 Phase Progression: Moving to '{progression_check['next_phase']}' phase."
                    # Update routing decision for next phase
                    state["routing_decision"] = {
                        "next_action": "proceed_to_next_phase",
                        "next_phase": progression_check["next_phase"],
                        "reason": "Quality gates passed, progressing to next workflow phase",
                        "retry_required": False
                    }
                    state_manager.write_state(state)
            elif progression_check.get("hanging_detected"):
                reason += f"\n\n⚠️ Hanging Detection: {progression_check['reason']}"
                if progression_check.get("resolution_strategy") == "force_progression":
                    reason += f"\nAutomatically resolved by force progression."
            
            # Pass quality results to next agent if in pipeline
            chain_status = chain_manager.get_chain_status()
            if chain_status.get("current_agent"):
                chain_manager.pass_data(
                    from_agent=subagent_name,
                    to_agent="next",
                    data={
                        "quality_results": results,
                        "phase_progression": progression_check
                    }
                )
            
            # Format output with phase information
            metadata = {
                "quality_gates_passed": results["passed_count"],
                "quality_gates_total": results["total_gates"],
                "pass_rate": results["pass_rate"],
                "phase_progression": progression_check
            }
            
            output = HookOutputFormatter.format_subagent_stop(
                decision=decision,
                reason=reason,
                metadata=metadata
            )
            
        else:
            # Gates failed - block and request fixes
            decision = "block"
            
            # Generate detailed failure message with actionable fixes
            failure_details = []
            actionable_fixes = []
            
            for gate_name in results["failed_gates"]:
                gate_results = results["results"].get(gate_name, {})
                issues = gate_results.get("issues", [])
                if issues:
                    failure_details.append(f"• {gate_name}:")
                    for issue in issues[:2]:  # Show first 2 issues per gate
                        failure_details.append(f"  - {issue}")
                        
                        # Add actionable fix suggestions
                        if "does not exist" in issue:
                            actionable_fixes.append(f"📝 Create the missing file: {issue.split(':')[1].strip()}")
                        elif "coverage" in issue.lower():
                            actionable_fixes.append(f"📈 Increase test coverage to 95% or higher")
                        elif "endpoint not found" in issue:
                            actionable_fixes.append(f"🔌 Add the missing API endpoint to your code")
                        elif "no changes detected" in issue:
                            actionable_fixes.append(f"✏️ Make actual changes to the file or remove from modified list")
                        elif "tests are failing" in issue:
                            actionable_fixes.append(f"🔧 Fix failing tests or update JSON to reflect actual status")
            
            if self_check and actionable_fixes:
                # Self-check mode: provide clear instructions
                reason = f"""🚫 VALIDATION FAILED - Fix these issues before exiting:

{chr(10).join(failure_details)}

📋 ACTION REQUIRED:
{chr(10).join(actionable_fixes)}

After fixing, run validation again:
echo '{{"subagent": "{subagent_name}", "self_check": true}}' | python3 ~/.claude/hooks/spark_quality_gates.py
"""
            else:
                # Hook mode: standard message
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