#!/usr/bin/env python3
"""
SPARK Quality Gates Hook (SubagentStop)
Universal quality validation for any project - no project dependencies
"""

import json
import logging
import re
import subprocess
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler(sys.stderr)])
logger = logging.getLogger(__name__)


def run_command(cmd: str, check: bool = False) -> tuple[bool, str, str]:
    """Run a command and return (success, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def check_syntax_validation() -> tuple[bool, list]:
    """Check for basic syntax errors in common file types"""
    issues = []
    
    # Python files
    success, stdout, stderr = run_command("find . -name '*.py' -not -path './.venv/*' -not -path './.*' | head -10 | xargs -I {} python3 -m py_compile {}")
    if not success and stderr:
        issues.append(f"Python syntax errors: {stderr}")
    
    # JavaScript/TypeScript files  
    success, stdout, stderr = run_command("find . -name '*.js' -o -name '*.ts' -not -path './node_modules/*' | head -5")
    # Note: Basic check, would need proper JS parser for full validation
    
    return len(issues) == 0, issues


def check_linting() -> tuple[bool, list]:
    """Check common linting tools"""
    issues = []
    
    # Python - Ruff
    if Path("pyproject.toml").exists() or any(Path(".").glob("*.py")):
        success, stdout, stderr = run_command("ruff check . --quiet")
        if not success:
            issues.append("Ruff linting violations found")
    
    # JavaScript/TypeScript - ESLint
    if Path("eslint.config.js").exists() or Path(".eslintrc.js").exists():
        success, stdout, stderr = run_command("npx eslint . --quiet --max-warnings 0")
        if not success:
            issues.append("ESLint violations found")
    
    # Go
    if any(Path(".").glob("*.go")):
        success, stdout, stderr = run_command("golint ./...")
        if not success and stderr:
            issues.append("Go lint issues found")
    
    return len(issues) == 0, issues


def check_type_validation() -> tuple[bool, list]:
    """Check type checking tools"""
    issues = []
    
    # Python - MyPy
    if Path("pyproject.toml").exists() or any(Path(".").glob("*.py")):
        success, stdout, stderr = run_command("mypy . --ignore-missing-imports --no-error-summary")
        if not success and "error:" in stderr:
            issues.append("MyPy type checking errors found")
    
    # TypeScript
    if Path("tsconfig.json").exists():
        success, stdout, stderr = run_command("npx tsc --noEmit")
        if not success:
            issues.append("TypeScript type checking errors found")
    
    return len(issues) == 0, issues


def check_security_basic() -> tuple[bool, list]:
    """Basic security checks"""
    issues = []
    
    # Check for common secret patterns in recently modified files
    success, stdout, stderr = run_command("git diff --name-only HEAD~1 2>/dev/null | head -10 | xargs grep -l -E '(password|secret|key)\\s*[=:]' 2>/dev/null")
    if success and stdout.strip():
        issues.append("Potential secrets found in recent changes")
    
    # Python - Bandit
    if any(Path(".").glob("*.py")):
        success, stdout, stderr = run_command("bandit -r . -f json -q -x './.venv/*' 2>/dev/null")
        if success and stdout:
            try:
                results = json.loads(stdout)
                if results.get("results"):
                    issues.append("Security issues found by Bandit")
            except:
                pass
    
    return len(issues) == 0, issues


def check_documentation() -> tuple[bool, list]:
    """Check for basic documentation"""
    issues = []
    
    # Check if Python functions have docstrings
    success, stdout, stderr = run_command("find . -name '*.py' -not -path './.venv/*' | head -5 | xargs grep -L 'def.*:.*\"\"\"' 2>/dev/null")
    if success and stdout.strip():
        issues.append("Some Python functions missing docstrings")
    
    # Check for README
    if not any(Path(".").glob("README*")):
        issues.append("No README file found")
    
    return len(issues) == 0, issues


def run_quality_gates() -> dict:
    """Run all quality gates and return results"""
    
    gates = {
        "syntax_validation": check_syntax_validation,
        "linting": check_linting,
        "type_checking": check_type_validation,
        "security": check_security_basic,
        "documentation": check_documentation,
    }
    
    results = {}
    total_passed = 0
    total_gates = len(gates)
    
    for gate_name, gate_func in gates.items():
        try:
            passed, issues = gate_func()
            results[gate_name] = {
                "passed": passed,
                "issues": issues
            }
            if passed:
                total_passed += 1
            logger.info(f"{'✅' if passed else '❌'} {gate_name}: {'PASS' if passed else f'FAIL ({len(issues)} issues)'}")
        except Exception as e:
            results[gate_name] = {
                "passed": False,
                "issues": [f"Gate execution failed: {e}"]
            }
            logger.error(f"❌ {gate_name}: ERROR - {e}")
    
    return {
        "gates_passed": total_passed,
        "total_gates": total_gates,
        "pass_rate": round(total_passed / total_gates * 100, 1),
        "results": results,
        "overall_pass": total_passed >= int(total_gates * 0.8)  # 80% threshold
    }


def main():
    """Main hook execution"""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
        
        # Check if we should run quality gates
        # Only run for implementation-related subagents
        cwd = input_data.get("cwd", "")
        
        logger.info("🛡️  Running SPARK Quality Gates...")
        
        # Run quality gates
        gate_results = run_quality_gates()
        
        # Determine action based on results
        if gate_results["overall_pass"]:
            # Quality gates passed - continue normally
            logger.info(f"✅ Quality Gates PASSED: {gate_results['gates_passed']}/{gate_results['total_gates']} ({gate_results['pass_rate']}%)")
            
            # Output success context
            context = f"""✅ **SPARK Quality Gates PASSED** ({gate_results['pass_rate']}%)

**Gates Passed**: {gate_results['gates_passed']}/{gate_results['total_gates']}
**Status**: Ready for next phase or completion

The code meets SPARK quality standards. You may proceed with confidence."""
            
            print(context)
            sys.exit(0)
            
        else:
            # Quality gates failed - provide feedback to continue improvements
            failed_gates = []
            for gate_name, result in gate_results["results"].items():
                if not result["passed"]:
                    failed_gates.append(f"{gate_name}: {', '.join(result['issues'])}")
            
            logger.info(f"❌ Quality Gates FAILED: {gate_results['gates_passed']}/{gate_results['total_gates']} ({gate_results['pass_rate']}%)")
            
            # Use JSON output to provide feedback to the subagent
            feedback = {
                "decision": "block",
                "reason": f"""❌ **SPARK Quality Gates FAILED** ({gate_results['pass_rate']}%)

**Failed Gates**: {gate_results['total_gates'] - gate_results['gates_passed']}/{gate_results['total_gates']}

**Issues to fix:**
{chr(10).join(f'• {issue}' for issue in failed_gates)}

Please fix these issues before proceeding. Focus on the failing quality gates and rerun your implementation."""
            }
            
            print(json.dumps(feedback))
            sys.exit(0)
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON input: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Hook execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
