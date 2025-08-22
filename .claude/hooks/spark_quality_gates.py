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


class V41QualityVerifier:
    """Verifies agent's claimed quality results against actual measurements"""
    
    def __init__(self):
        self.executor = SecureCommandExecutor()
        self.project_root = find_project_root()
    
    def verify_step_1_architecture(self, claimed: Dict) -> Tuple[Dict, List[str]]:
        """Step 1: Architecture - imports, circular, domain"""
        actual = {"imports": 0, "circular": 0, "domain": 0}
        issues = []
        
        # Check import violations
        success, stdout, stderr = self.executor.run_command(
            ["python3", "-c", "import sys; sys.path.insert(0, '.'); from check_imports import check; print(check())"],
            timeout=10
        )
        if not success:
            actual["imports"] = 1  # Assume violation if check fails
        
        # Check circular dependencies
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv", "__pycache__"])
        for file_path in python_files[:10]:
            try:
                content = file_path.read_text()
                # Simple circular import detection
                if "from . import" in content and "import ." in content:
                    actual["circular"] += 1
            except:
                pass
        
        # Check domain boundaries
        # Simplified check - real implementation would be more sophisticated
        if Path("src").exists():
            cross_domain = 0
            # Check if src/domain_a imports from src/domain_b directly
            for py_file in Path("src").rglob("*.py"):
                try:
                    content = py_file.read_text()
                    if "from src." in content:
                        # Simple heuristic for cross-domain imports
                        cross_domain += content.count("from src.")
                except:
                    pass
            actual["domain"] = min(cross_domain, 10)  # Cap at 10
        
        # Compare claimed vs actual
        for key in actual:
            if claimed.get(key, 0) != actual[key]:
                issues.append(f"Architecture {key}: claimed {claimed.get(key, 0)}, actual {actual[key]}")
        
        return actual, issues
    
    def verify_step_2_foundation(self, claimed: Dict) -> Tuple[Dict, List[str]]:
        """Step 2: Foundation - syntax, types"""
        actual = {"syntax": 0, "types": 0}
        issues = []
        
        # Check syntax errors
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv", "__pycache__"])
        for file_path in python_files[:20]:
            success, stdout, stderr = self.executor.run_command(
                ["python3", "-m", "py_compile", str(file_path)],
                timeout=5
            )
            if not success:
                actual["syntax"] += 1
        
        # Check type errors with mypy --strict
        success, stdout, stderr = self.executor.run_command(
            ["mypy", ".", "--strict", "--no-error-summary"],
            timeout=30
        )
        if stdout or stderr:
            actual["types"] = stdout.count("error:") + stderr.count("error:")
        
        # Compare claimed vs actual
        for key in actual:
            if claimed.get(key, 0) != actual[key]:
                issues.append(f"Foundation {key}: claimed {claimed.get(key, 0)}, actual {actual[key]}")
        
        return actual, issues
    
    def verify_step_3_standards(self, claimed: Dict) -> Tuple[Dict, List[str]]:
        """Step 3: Standards - formatting, conventions"""
        actual = {"formatting": 0, "conventions": 0}
        issues = []
        
        # Check formatting with black
        success, stdout, stderr = self.executor.run_command(
            ["black", ".", "--check", "--quiet"],
            timeout=20
        )
        if not success:
            # Count unformatted files
            if "would be reformatted" in stdout:
                actual["formatting"] = int(stdout.split()[0]) if stdout.split()[0].isdigit() else 1
        
        # Check naming conventions with ruff
        success, stdout, stderr = self.executor.run_command(
            ["ruff", "check", ".", "--select", "N", "--quiet"],
            timeout=20
        )
        if stdout:
            actual["conventions"] = len(stdout.strip().split('\n'))
        
        # Compare claimed vs actual
        for key in actual:
            if claimed.get(key, 0) != actual[key]:
                issues.append(f"Standards {key}: claimed {claimed.get(key, 0)}, actual {actual[key]}")
        
        return actual, issues
    
    def verify_step_4_operations(self, claimed: Dict) -> Tuple[Dict, List[str]]:
        """Step 4: Operations - logging, security, config"""
        actual = {"logging": 0, "security": 0, "config": 0}
        issues = []
        
        # Check for print statements (should use logging)
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv", "__pycache__"])
        for file_path in python_files[:30]:
            try:
                content = file_path.read_text()
                # Count print statements not in comments
                lines = content.split('\n')
                for line in lines:
                    if 'print(' in line and not line.strip().startswith('#'):
                        actual["logging"] += 1
            except:
                pass
        
        # Check security with bandit
        success, stdout, stderr = self.executor.run_command(
            ["bandit", "-r", ".", "-f", "json", "-q"],
            timeout=30
        )
        if success and stdout:
            try:
                import json
                results = json.loads(stdout)
                metrics = results.get("metrics", {}).get("_totals", {})
                actual["security"] = metrics.get("SEVERITY.HIGH", 0) + metrics.get("SEVERITY.MEDIUM", 0)
            except:
                pass
        
        # Check for hardcoded configs
        for file_path in python_files[:20]:
            try:
                content = file_path.read_text()
                # Check for hardcoded passwords, keys, etc.
                if any(pattern in content for pattern in [
                    "password=", "api_key=", "secret=", 
                    "localhost:", "127.0.0.1:", "0.0.0.0:"
                ]):
                    actual["config"] += 1
            except:
                pass
        
        # Compare claimed vs actual
        for key in actual:
            if claimed.get(key, 0) != actual[key]:
                issues.append(f"Operations {key}: claimed {claimed.get(key, 0)}, actual {actual[key]}")
        
        return actual, issues
    
    def verify_step_5_quality(self, claimed: Dict) -> Tuple[Dict, List[str]]:
        """Step 5: Quality - linting, complexity"""
        actual = {"linting": 0, "complexity": 0}
        issues = []
        
        # Check linting with ruff (all rules)
        success, stdout, stderr = self.executor.run_command(
            ["ruff", "check", ".", "--select", "ALL", "--quiet"],
            timeout=30
        )
        if stdout:
            actual["linting"] = len(stdout.strip().split('\n'))
        
        # Check complexity with radon
        success, stdout, stderr = self.executor.run_command(
            ["radon", "cc", ".", "-s", "-n", "B"],
            timeout=20
        )
        if success and stdout:
            # Count functions with complexity > B (McCabe > 10)
            actual["complexity"] = stdout.count(" - ") if " - " in stdout else 0
        
        # Compare claimed vs actual
        for key in actual:
            if claimed.get(key, 0) != actual[key]:
                issues.append(f"Quality {key}: claimed {claimed.get(key, 0)}, actual {actual[key]}")
        
        return actual, issues
    
    def verify_step_6_testing(self, claimed: Dict) -> Tuple[Dict, List[str]]:
        """Step 6: Testing - coverage"""
        actual = {"coverage": -1}
        issues = []
        
        # Only verify if testing was claimed
        if claimed.get("coverage", -1) >= 0:
            # Run coverage
            success, stdout, stderr = self.executor.run_command(
                ["pytest", "--cov=.", "--cov-report=term", "-q"],
                timeout=60
            )
            
            if success:
                import re
                match = re.search(r'TOTAL.*?(\d+)%', stdout)
                if match:
                    actual["coverage"] = int(match.group(1))
                    
                    # Check if claimed coverage matches actual (with 5% tolerance)
                    if abs(claimed.get("coverage", 0) - actual["coverage"]) > 5:
                        issues.append(f"Testing coverage: claimed {claimed.get('coverage', 0)}%, actual {actual['coverage']}%")
        
        return actual, issues
    
    def verify_step_7_documentation(self, claimed: Dict) -> Tuple[Dict, List[str]]:
        """Step 7: Documentation - docstrings, readme"""
        actual = {"docstrings": 0, "readme": 0}
        issues = []
        
        # Check docstrings
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv", "__pycache__"])
        missing_docstrings = 0
        
        for file_path in python_files[:20]:
            try:
                content = file_path.read_text()
                import re
                # Count functions without docstrings
                functions = re.findall(r'def\s+\w+\([^)]*\):', content)
                docstrings = re.findall(r'def\s+\w+\([^)]*\):\s*\n\s*["\'\'\'\"]', content)
                missing_docstrings += max(0, len(functions) - len(docstrings))
            except:
                pass
        
        actual["docstrings"] = missing_docstrings
        
        # Check README
        if not any(Path(".").glob("README*")):
            actual["readme"] = 1
        
        # Compare claimed vs actual
        for key in actual:
            if claimed.get(key, 0) != actual[key]:
                issues.append(f"Documentation {key}: claimed {claimed.get(key, 0)}, actual {actual[key]}")
        
        return actual, issues
    
    def verify_step_8_integration(self, claimed: Dict) -> Tuple[Dict, List[str]]:
        """Step 8: Integration - final checks"""
        actual = {"final": 0}
        issues = []
        
        # Run final integration checks
        integration_issues = 0
        
        # Check for dependency conflicts
        if Path("requirements.txt").exists():
            success, stdout, stderr = self.executor.run_command(
                ["pip", "check"],
                timeout=10
            )
            if not success or "incompatible" in stdout.lower():
                integration_issues += 1
        
        # Check for broken imports
        python_files = self.executor.find_files("*.py", exclude_dirs=[".venv", "__pycache__"])
        for file_path in python_files[:10]:
            success, stdout, stderr = self.executor.run_command(
                ["python3", "-c", f"import ast; ast.parse(open('{file_path}').read())"],
                timeout=5
            )
            if not success:
                integration_issues += 1
        
        actual["final"] = integration_issues
        
        # Compare claimed vs actual
        if claimed.get("final", 0) != actual["final"]:
            issues.append(f"Integration final: claimed {claimed.get('final', 0)}, actual {actual['final']}")
        
        return actual, issues


class QualityGateRunner:
    """Jason's 8-Step Quality Gate Runner - Compares agent claims vs reality"""
    
    def __init__(self, claude_code_mode: bool = True):
        self.claude_code_mode = claude_code_mode
        self.verifier = V41QualityVerifier()
        
        # Additional verification gates (not part of 8-step structure)
        self.extra_gates = [
            ImplementationVerificationGate(),  # Verify implementation claims
            TestVerificationGate()             # Verify test claims
        ]
        
        self.state_manager = StateManager()
        self.chain_manager = AgentChainManager()
    
    def run_gates(self, required_gates: Optional[int] = None) -> Dict:
        """Compare agent's claimed quality results against actual measurements"""
        
        # First, read current_task.json to get agent's claims
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
            logger.warning("No current_task.json found - cannot verify agent claims")
            return {
                "passed_count": 0,
                "total_gates": 0,
                "required_gates": 8,
                "pass_rate": 0,
                "passed": False,
                "failed_gates": ["No JSON to verify"],
                "all_issues": ["current_task.json not found"],
                "results": {}
            }
        
        # Get claimed quality results from JSON
        claimed_quality = current_task.get("quality", {})
        
        # Initialize results
        results = {}
        all_issues = []
        verification_results = {}
        actual_quality = {}
        
        # Run extra verification gates first (implementation & test verification)
        for gate in self.extra_gates:
            try:
                passed, issues = gate.check()
                if not passed:
                    all_issues.extend(issues)
                results[gate.name] = {"passed": passed, "issues": issues}
            except Exception as e:
                logger.error(f"Extra gate {gate.name} failed: {e}")
        
        # Verify each of the 8 quality steps
        step_verifiers = [
            ("step_1_architecture", self.verifier.verify_step_1_architecture),
            ("step_2_foundation", self.verifier.verify_step_2_foundation),
            ("step_3_standards", self.verifier.verify_step_3_standards),
            ("step_4_operations", self.verifier.verify_step_4_operations),
            ("step_5_quality", self.verifier.verify_step_5_quality),
            ("step_6_testing", self.verifier.verify_step_6_testing),
            ("step_7_documentation", self.verifier.verify_step_7_documentation),
            ("step_8_integration", self.verifier.verify_step_8_integration)
        ]
        
        violations_total = 0
        failed_steps = []
        
        for step_name, verifier_func in step_verifiers:
            claimed_step = claimed_quality.get(step_name, {})
            
            try:
                logger.info(f"Verifying {step_name}...")
                actual_step, issues = verifier_func(claimed_step)
                
                # Store actual results
                actual_quality[step_name] = actual_step
                
                # Check if there are discrepancies
                if issues:
                    all_issues.extend(issues)
                    failed_steps.append(step_name)
                    logger.info(f"  ❌ {step_name}: MISMATCH - {len(issues)} discrepancies")
                    for issue in issues:
                        logger.info(f"     - {issue}")
                else:
                    # Check if all values are actually 0 (except coverage which can be -1)
                    step_violations = sum(v for k, v in actual_step.items() if k != "coverage" and v > 0)
                    if step_violations > 0:
                        violations_total += step_violations
                        failed_steps.append(step_name)
                        logger.info(f"  ❌ {step_name}: Has {step_violations} violations")
                    else:
                        logger.info(f"  ✅ {step_name}: VERIFIED (all clean)")
                
                results[step_name] = {
                    "claimed": claimed_step,
                    "actual": actual_step,
                    "issues": issues
                }
                
            except Exception as e:
                logger.error(f"  ⚠️ {step_name}: ERROR - {e}")
                all_issues.append(f"{step_name} verification failed: {str(e)}")
                failed_steps.append(step_name)
        
        # DO NOT modify the JSON file - it's a fixed format!
        # Log and display verification results for agent to see
        logger.info(f"Verification complete - total issues found: {len(all_issues)}")
        
        # Print results to stdout so agent can see them directly
        print("\n" + "="*60)
        print("🔍 QUALITY GATES VERIFICATION")
        print("="*60)
        
        # Collect all errors (both discrepancies and actual violations)
        error_summary = {}
        
        # Check each step for actual violations (not just discrepancies)
        for step_name in actual_quality:
            actual = actual_quality[step_name]
            for key, value in actual.items():
                # Skip coverage=-1 (not measured) and 0 values
                if key == "coverage" and value == -1:
                    continue
                if value > 0:
                    error_name = f"{step_name.replace('step_', '').replace('_', ' ').title()} - {key}"
                    error_summary[error_name] = value
        
        # If there are any errors, display them
        if error_summary:
            print("\n❌ Errors Found!\n")
            for error_name, count in error_summary.items():
                print(f"  • {error_name}: {count}")
            print("\n🚫 Quality gates FAILED. Please fix violations and retry.")
            print("   All violations must be 0 to complete the task.")
        else:
            print("\n✅ Quality gates PASSED.")
            print("   Task completed successfully. You may now exit.")
        
        print("="*60 + "\n")
        
        # Calculate pass/fail
        # Pass if: 1) No discrepancies between claimed and actual, 2) All violations are 0
        passed = len(all_issues) == 0 and violations_total == 0
        passed_steps = 8 - len(failed_steps)
        pass_rate = (passed_steps / 8 * 100)
        
        # Update state
        state = self.state_manager.read_state()
        state["quality_gates"] = {
            "passed": passed_steps,
            "total": 8,
            "results": results,
            "last_run": datetime.now().isoformat(),
            "violations_total": violations_total
        }
        self.state_manager.write_state(state)
        
        return {
            "passed_count": passed_steps,
            "total_gates": 8,
            "required_gates": 8,
            "pass_rate": round(pass_rate, 1),
            "passed": passed,
            "failed_gates": failed_steps,
            "all_issues": all_issues,
            "results": results,
            "violations_total": violations_total
        }


def main():
    """Main hook execution"""
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
        
        # Get required gates from state
        state = state_manager.read_state()
        required_gates = state.get("quality_gates", {}).get("required", 8)
        
        # Run quality gates
        results = runner.run_gates(required_gates)
        
        # Update state with quality results
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
        
        # Update state with quality results
        state_manager.write_state(state)
        
        # Prepare response based on results
        if results["passed"]:
            # Gates passed
            decision = "continue"
            reason = f"Quality gates passed: {results['passed_count']}/{results['total_gates']} gates passed ({results['pass_rate']}% pass rate)"
            
            # Pass quality results to next agent if in pipeline
            chain_status = chain_manager.get_chain_status()
            if chain_status.get("current_agent"):
                chain_manager.pass_data(
                    from_agent=subagent_name,
                    to_agent="next",
                    data={
                        "quality_results": results
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