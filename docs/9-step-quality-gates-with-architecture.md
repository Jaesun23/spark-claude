# 9-Step Mandatory Quality Gates for SPARK v3.9

## 📋 Overview
All SPARK agents MUST execute these 9 quality gates in Phase 4. Results are recorded as numbers (0 = pass, >0 = violations count).

---

## 🔒 PHASE 4: MANDATORY QUALITY VALIDATION

### Step 1: Syntax Validation (구문 검증)
```bash
# Python files
python3 -m py_compile **/*.py 2>&1 | grep -c "SyntaxError"
# Result: Must be 0

# JavaScript/TypeScript files  
npx eslint . --no-eslintrc --parser-options=ecmaVersion:latest 2>&1 | grep -c "Parsing error"
# Result: Must be 0
```

### Step 2: Architecture & Structure Check (구조 검사) 🆕
```bash
# Layer violations (계층 침범)
import-linter --config .import-linter.ini 2>&1 | grep -c "Broken contracts"
# Result: Must be 0

# Circular imports (순환 임포트)
python3 -c "
import sys, importlib, pkgutil
circular = 0
# Check for circular imports logic here
print(circular)
"
# Alternative: pycycle or import-linter
# Result: Must be 0

# Domain boundary violations (도메인 경계 침범)
grep -r "from.*domain" --include="*.py" | grep -c "cross-domain"
# Result: Must be 0

# Structured logging check (구조화 로깅)
grep -r "print(" --include="*.py" | wc -l
# Result: Must be 0 (no print statements, only logger)

# Error message consistency (에러 메시지 일관성)
grep -r "raise.*Exception" --include="*.py" | grep -v "Error:" | wc -l
# Result: Must be 0 (all errors must have "Error:" prefix)
```

### Step 3: Type Checking - MyPy Strict (타입 검사)
```bash
# Python - STRICT mode mandatory
mypy . --strict --no-error-summary 2>&1 | grep -c "error:"
# Result: Must be 0

# TypeScript
npx tsc --strict --noEmit 2>&1 | grep -c "error TS"
# Result: Must be 0
```

### Step 4: Linting & Magic Numbers (린팅 및 매직넘버)
```bash
# Python - STRICT mode with magic number detection
ruff check . --select=ALL 2>&1 | grep "Found" | grep -oE "[0-9]+" | head -1
# Result: Must be 0

# Magic number specific check
ruff check . --select=PLR2004 2>&1 | grep -c "PLR2004"
# Result: Must be 0 (no magic numbers)

# JavaScript/TypeScript
npx eslint . --max-warnings 0 2>&1 | grep -oE "[0-9]+ problems" | grep -oE "[0-9]+" | head -1
# Result: Must be 0
```

### Step 5: Security Analysis (보안 분석)
```bash
# Python
bandit -r . -f json 2>/dev/null | jq '.metrics._totals."SEVERITY.HIGH" + .metrics._totals."SEVERITY.MEDIUM"'
# Result: Must be 0

# Secrets detection
grep -r -E "(api_key|secret|token|password)\s*=\s*[\"'][^\"']+[\"']" --include="*.py" --include="*.js" --include="*.ts" | wc -l
# Result: Must be 0
```

### Step 6: Test Coverage - CONDITIONAL (테스트 커버리지)
```bash
# FOR TESTER AGENTS ONLY (tester-spark, team1-4-tester-spark):
pytest --cov=. --cov-report=json --quiet
jq -r '.totals.percent_covered' coverage.json | cut -d. -f1
# Result: Must be ≥95

# FOR OTHER AGENTS: Skip this step (record as -1 in JSON)
```

### Step 7: Code Formatting (코드 포맷팅)
```bash
# Python - Black
black . --check 2>&1 | grep -c "would be reformatted"
# Result: Must be 0

# Python - isort
isort . --check-only 2>&1 | grep -c "Fixing"
# Result: Must be 0
```

### Step 8: Complexity Check (복잡도 검사)
```bash
# Python - McCabe complexity
python3 -m mccabe --min 10 **/*.py 2>/dev/null | wc -l
# Result: Must be 0 (no functions with complexity >10)

# Cyclomatic complexity
radon cc . -s -n B 2>/dev/null | grep -c "^    [MCF]"
# Result: Must be 0 (no blocks rated B or worse)
```

### Step 9: Documentation Check (문서화 검증)
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
    "step_2_architecture": 0,  // 🆕 구조 검사
    "step_3_type_checking": 0,
    "step_4_linting": 0,
    "step_5_security": 0,
    "step_6_test_coverage": -1,  // -1 for non-tester agents
    "step_7_formatting": 0,
    "step_8_complexity": 0,
    "step_9_documentation": 0
  },
  "architecture_details": {  // 🆕 구조 검사 상세
    "layer_violations": 0,
    "circular_imports": 0,
    "domain_violations": 0,
    "print_statements": 0,
    "inconsistent_errors": 0,
    "magic_numbers": 0
  },
  "total_violations": 0,
  "validation_passed": 1  // 1 = true, 0 = false
}
```

---

## 🏗️ Architecture Check Details (Step 2)

### Layer Architecture Rules
```python
# .import-linter.ini example
[importlinter]
root_packages = 
    core
    domain
    infrastructure
    presentation

[contract:layers]
type = layers
layers = 
    presentation
    domain
    infrastructure
    core
# presentation can import domain
# domain can import core
# infrastructure can import domain, core
# core imports nothing
```

### Structured Logging Pattern
```python
# ❌ BAD: Print statements
print(f"Processing {file}")

# ✅ GOOD: Structured logging
logger.info("Processing file", extra={"file": file, "action": "process"})
```

### Error Message Consistency
```python
# ❌ BAD: Inconsistent error
raise ValueError("invalid input")

# ✅ GOOD: Consistent format
raise ValueError("Error: Invalid input - expected string, got int")
```

### Magic Number Prevention
```python
# ❌ BAD: Magic numbers
if amount > 100:
    discount = amount * 0.9

# ✅ GOOD: Named constants
MAX_DISCOUNT_THRESHOLD = 100
DISCOUNT_RATE = 0.9

if amount > MAX_DISCOUNT_THRESHOLD:
    discount = amount * DISCOUNT_RATE
```

---

## 🔄 Execution Flow for 9 Steps

```python
## Phase 4: Internal Quality Validation (MANDATORY - BLOCKING)

echo "=== Phase 4: 9-Step Quality Validation ==="

# Step 1: Syntax
SYNTAX_ERRORS=$(python3 -m py_compile **/*.py 2>&1 | grep -c "SyntaxError")
echo "Step 1 - Syntax errors: $SYNTAX_ERRORS"
[[ $SYNTAX_ERRORS -gt 0 ]] && fix_syntax_errors()

# Step 2: Architecture (NEW!)
LAYER_VIOLATIONS=$(import-linter 2>&1 | grep -c "Broken")
CIRCULAR_IMPORTS=$(pycycle . 2>&1 | grep -c "circular")
PRINT_STATEMENTS=$(grep -r "print(" --include="*.py" | wc -l)
MAGIC_NUMBERS=$(ruff check . --select=PLR2004 2>&1 | grep -c "PLR2004")
ARCHITECTURE_TOTAL=$((LAYER_VIOLATIONS + CIRCULAR_IMPORTS + PRINT_STATEMENTS + MAGIC_NUMBERS))
echo "Step 2 - Architecture violations: $ARCHITECTURE_TOTAL"
[[ $ARCHITECTURE_TOTAL -gt 0 ]] && fix_architecture_issues()

# Step 3-9: Continue as before...
# ... (remaining steps)

# Write enhanced JSON
cat > ~/.claude/workflows/quality_gates_result.json << EOF
{
  "agent": "$(basename $0)",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "quality_gates": {
    "step_1_syntax": $SYNTAX_ERRORS,
    "step_2_architecture": $ARCHITECTURE_TOTAL,
    "step_3_type_checking": $TYPE_ERRORS,
    "step_4_linting": $LINT_ERRORS,
    "step_5_security": $SECURITY_ISSUES,
    "step_6_test_coverage": -1,
    "step_7_formatting": $FORMAT_ISSUES,
    "step_8_complexity": $COMPLEXITY_ISSUES,
    "step_9_documentation": $DOC_MISSING
  },
  "architecture_details": {
    "layer_violations": $LAYER_VIOLATIONS,
    "circular_imports": $CIRCULAR_IMPORTS,
    "domain_violations": 0,
    "print_statements": $PRINT_STATEMENTS,
    "inconsistent_errors": 0,
    "magic_numbers": $MAGIC_NUMBERS
  },
  "total_violations": $TOTAL_ALL,
  "validation_passed": $([[ $TOTAL_ALL -eq 0 ]] && echo 1 || echo 0)
}
EOF

# Final verification
python3 ~/.claude/hooks/spark_quality_gates.py
```

---

## ⚠️ Why Architecture Check Matters

### 레이어 침범 방지
- Presentation이 Infrastructure 직접 호출 ❌
- Domain이 Presentation 의존 ❌
- Core가 다른 레이어 의존 ❌

### 순환 임포트 방지
- A → B → C → A 순환 참조 ❌
- 컴파일 실패 및 런타임 오류 원인

### 구조화 로깅 강제
- print() 사용 금지
- logger만 사용 (JSON 형식 로깅)
- 프로덕션 로그 분석 가능

### 매직넘버 제거
- 하드코딩된 숫자 금지
- 상수로 정의 필수
- 코드 가독성 및 유지보수성 향상

---

## 🎯 Benefits of 9-Step Gates

1. **구조적 무결성**: 아키텍처 원칙 강제
2. **유지보수성**: 깨끗한 의존성 그래프
3. **디버깅 용이**: 구조화된 로깅
4. **가독성**: 매직넘버 없는 명확한 코드
5. **확장성**: 레이어 분리로 변경 용이

---

*SPARK v3.9 - Now with Architecture Enforcement*
*Zero tolerance. Clean architecture. No compromises.*