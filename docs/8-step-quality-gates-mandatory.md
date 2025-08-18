# 8-Step Mandatory Quality Gates for All SPARK Agents

## 📋 Overview
All SPARK agents MUST execute these 8 quality gates in Phase 4. Results are recorded as numbers (0 = pass, >0 = violations count).

---

## 🔒 PHASE 4: MANDATORY QUALITY VALIDATION

### Step 1: Syntax Validation
```bash
# Python files
python3 -m py_compile **/*.py 2>&1 | grep -c "SyntaxError"
# Result: Must be 0

# JavaScript/TypeScript files  
npx eslint . --no-eslintrc --parser-options=ecmaVersion:latest 2>&1 | grep -c "Parsing error"
# Result: Must be 0
```

### Step 2: Type Checking (MyPy Strict)
```bash
# Python - STRICT mode mandatory
mypy . --strict --no-error-summary 2>&1 | grep -c "error:"
# Result: Must be 0

# TypeScript
npx tsc --strict --noEmit 2>&1 | grep -c "error TS"
# Result: Must be 0
```

### Step 3: Linting (Ruff Strict)
```bash
# Python - STRICT mode mandatory
ruff check . --select ALL 2>&1 | grep "Found" | grep -oE "[0-9]+" | head -1
# Result: Must be 0

# JavaScript/TypeScript
npx eslint . --max-warnings 0 2>&1 | grep -oE "[0-9]+ problems" | grep -oE "[0-9]+" | head -1
# Result: Must be 0
```

### Step 4: Security Analysis
```bash
# Python
bandit -r . -f json 2>/dev/null | jq '.metrics._totals."SEVERITY.HIGH" + .metrics._totals."SEVERITY.MEDIUM"'
# Result: Must be 0

# Secrets detection
grep -r -E "(api_key|secret|token|password)\s*=\s*[\"'][^\"']+[\"']" --include="*.py" --include="*.js" --include="*.ts" | wc -l
# Result: Must be 0
```

### Step 5: Test Coverage (CONDITIONAL)
```bash
# FOR TESTER AGENTS ONLY (tester-spark, team1-4-tester-spark):
pytest --cov=. --cov-report=json --quiet
jq -r '.totals.percent_covered' coverage.json | cut -d. -f1
# Result: Must be ≥95

# FOR OTHER AGENTS: Skip this step (record as -1 in JSON)
```

### Step 6: Code Formatting
```bash
# Python - Black
black . --check 2>&1 | grep -c "would be reformatted"
# Result: Must be 0

# Python - isort
isort . --check-only 2>&1 | grep -c "Fixing"
# Result: Must be 0
```

### Step 7: Complexity Check
```bash
# Python - McCabe complexity
python3 -m mccabe --min 10 **/*.py 2>/dev/null | wc -l
# Result: Must be 0 (no functions with complexity >10)

# Cyclomatic complexity
radon cc . -s -n B 2>/dev/null | grep -c "^    [MCF]"
# Result: Must be 0 (no blocks rated B or worse)
```

### Step 8: Documentation Check
```bash
# Python - Docstring coverage
python3 -c "
import ast, glob, sys
missing = 0
for file in glob.glob('**/*.py', recursive=True):
    with open(file) as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    missing += 1
print(missing)
"
# Result: Must be 0
```

---

## 📝 JSON Recording Format

### Location: `~/.claude/workflows/quality_gates_result.json`

```json
{
  "agent": "implementer-spark",
  "timestamp": "2025-01-18T14:30:00Z",
  "task": "TASK-001",
  "quality_gates": {
    "step_1_syntax": 0,
    "step_2_type_checking": 0,
    "step_3_linting": 0,
    "step_4_security": 0,
    "step_5_test_coverage": -1,  // -1 for non-tester agents
    "step_6_formatting": 0,
    "step_7_complexity": 0,
    "step_8_documentation": 0
  },
  "total_violations": 0,
  "validation_passed": 1  // 1 = true, 0 = false
}
```

---

## 🔄 Execution Flow

### For Each Agent:

```python
## Phase 4: Internal Quality Validation (MANDATORY - BLOCKING)

1. Execute each quality gate command directly
2. If violations > 0:
   - Fix the issues
   - Re-run that specific gate
   - Maximum 3 attempts per gate
3. Record results in JSON (numbers only)
4. After all gates complete, run verification:
   ```bash
   echo '{"subagent": "[agent-name]", "self_check": true}' | \
       python3 ~/.claude/hooks/spark_quality_gates.py
   ```
5. Compare script results with JSON:
   - If mismatch: Re-run failed gates
   - If match and all 0: Proceed to Phase 5
   - If not all 0: BLOCKED - cannot proceed

### CRITICAL: Cannot proceed to Phase 5 until:
- All applicable gates show 0 violations
- JSON file is written with results
- Verification script confirms results
```

---

## 🎯 Agent-Specific Rules

### Implementer Agents (implementer-spark, team1-4-implementer-spark)
- **Skip Step 5** (Test Coverage) - Record as -1
- Focus on code quality, not test writing
- Handoff to tester for coverage

### Tester Agents (tester-spark, team1-4-tester-spark)
- **Step 5 is MANDATORY** - Must achieve ≥95%
- Write tests until coverage met
- Cannot complete without 95% coverage

### Documenter Agents
- **Skip Step 5** (Test Coverage) - Record as -1
- **Step 8 extra strict** - Every public API must be documented

### All Other Agents
- **Skip Step 5** (Test Coverage) - Record as -1
- All other gates mandatory with 0 tolerance

---

## ⚠️ Enforcement Mechanism

```markdown
### In every agent's Phase 4 section:

**⚠️ MANDATORY QUALITY GATES - BLOCKING**
You MUST complete all 8 quality gates with 0 violations before proceeding.
This is NOT optional. Phase 5 is BLOCKED until all gates pass.

1. Run each gate command directly
2. Fix any violations immediately  
3. Record results in JSON (numbers only)
4. Verify with quality gates script
5. CANNOT PROCEED if any gate > 0 (except test coverage for non-testers)
```

---

## 🚨 Common Mistakes to Avoid

1. **DO NOT** skip gates thinking they're optional
2. **DO NOT** proceed with violations > 0
3. **DO NOT** fake JSON numbers - script will verify
4. **DO NOT** use "true/false" - use numbers only
5. **DO NOT** forget to run verification script

---

## 📊 Example Implementation in Agent

```bash
# Phase 4 execution example
echo "=== Phase 4: Mandatory Quality Validation ==="

# Step 1: Syntax
SYNTAX_ERRORS=$(python3 -m py_compile **/*.py 2>&1 | grep -c "SyntaxError")
echo "Syntax errors: $SYNTAX_ERRORS"
if [ $SYNTAX_ERRORS -gt 0 ]; then
    # Fix syntax errors
    # Re-run check
fi

# Step 2: Type checking
TYPE_ERRORS=$(mypy . --strict --no-error-summary 2>&1 | grep -c "error:")
echo "Type errors: $TYPE_ERRORS"
if [ $TYPE_ERRORS -gt 0 ]; then
    # Fix type errors
    # Re-run check
fi

# ... continue for all 8 steps ...

# Write JSON
cat > ~/.claude/workflows/quality_gates_result.json << EOF
{
  "agent": "$(basename $0)",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "quality_gates": {
    "step_1_syntax": $SYNTAX_ERRORS,
    "step_2_type_checking": $TYPE_ERRORS,
    "step_3_linting": $LINT_ERRORS,
    "step_4_security": $SECURITY_ISSUES,
    "step_5_test_coverage": -1,
    "step_6_formatting": $FORMAT_ISSUES,
    "step_7_complexity": $COMPLEXITY_ISSUES,
    "step_8_documentation": $DOC_MISSING
  },
  "total_violations": $((SYNTAX_ERRORS + TYPE_ERRORS + LINT_ERRORS + SECURITY_ISSUES + FORMAT_ISSUES + COMPLEXITY_ISSUES + DOC_MISSING)),
  "validation_passed": $([[ $TOTAL -eq 0 ]] && echo 1 || echo 0)
}
EOF

# Verify
python3 ~/.claude/hooks/spark_quality_gates.py
```

---

*This is the mandatory quality standard for SPARK v3.8+*
*Zero tolerance. No exceptions. No negotiations.*