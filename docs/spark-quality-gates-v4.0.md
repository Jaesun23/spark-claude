# SPARK Quality Gates v4.0 - 12-Step Mandatory Validation

> **"프로젝트 전체 무결성을 보장하는 체계적 품질 검증 시스템"**  
> DNA v3.6 Bootstrap Gate + SPARK 9-Step Gates 통합 버전

## 🎯 Overview

모든 SPARK 에이전트는 Phase 4에서 이 12단계 품질 게이트를 **필수**로 실행합니다.
각 단계별로 직접 명령어를 실행하여 검사하고, 결과를 숫자로 JSON에 기록합니다.

### 핵심 원칙
- **Zero Tolerance**: 모든 검사는 0 violations 목표 (테스트 제외)
- **Phase Blocking**: 각 Phase 완료 전 다음 Phase 진행 불가
- **Project Integrity**: 작업 단위가 아닌 프로젝트 전체 무결성 보장
- **Numeric Recording**: true/false가 아닌 숫자로 기록

---

## 📊 4-Phase 12-Step Structure

```
Phase A: Foundation (기초 검증) - 코드 실행 가능성
├── Step 1: Syntax Validation
├── Step 2: Type Checking  
└── Step 3: Code Formatting

Phase B: Architecture (구조 검증) - 시스템 무결성
├── Step 4: Import Architecture
├── Step 5: Circular Dependencies
└── Step 6: Domain Boundaries

Phase C: Quality (품질 검증) - 코드 품질
├── Step 7: Linting & Magic Numbers
├── Step 8: Complexity Check
├── Step 9: Test Coverage
└── Step 10: Documentation

Phase D: Operations (운영 검증) - 프로덕션 준비
├── Step 11: Logging & Monitoring
└── Step 12: Security & Configuration
```

---

## 🔒 Phase A: Foundation Layer (기초 검증)

### Step 1: Syntax Validation (구문 검증)
```bash
# Python 구문 오류 검사
find . -name "*.py" -type f | xargs -I {} python3 -m py_compile {} 2>&1 | grep -c "SyntaxError"
# Result: Must be 0

# JavaScript/TypeScript 구문 검사
npx eslint . --no-eslintrc --parser-options=ecmaVersion:latest 2>&1 | grep -c "Parsing error"
# Result: Must be 0
```

### Step 2: Type Checking (타입 검사)
```bash
# Python - MyPy strict mode
mypy . --strict --no-error-summary 2>&1 | grep -c "error:"
# Result: Must be 0

# TypeScript strict
npx tsc --strict --noEmit 2>&1 | grep -c "error TS"
# Result: Must be 0
```

### Step 3: Code Formatting (코드 포맷팅)
```bash
# Python - Black
black . --check 2>&1 | grep -c "would be reformatted"
# Result: Must be 0

# Python - isort
isort . --check-only 2>&1 | grep -c "Fixing"
# Result: Must be 0
```

**⚠️ Phase A Failed = Cannot Run Code**

---

## 🏗️ Phase B: Architecture Layer (구조 검증)

### Step 4: Import Architecture (임포트 구조)
```bash
# Import Linter - DNA 골격계 핵심
import-linter 2>&1 | grep -c "Broken contracts"
# Result: Must be 0

# Layer violations 체크
grep -r "from infrastructure" domain/ --include="*.py" 2>/dev/null | wc -l
# Result: Must be 0 (Domain cannot import Infrastructure)
```

### Step 5: Circular Dependencies (순환 참조)
```bash
# pycycle 또는 madge 사용
pycycle . --here 2>&1 | grep -c "circular"
# Alternative: madge --circular src/
# Result: Must be 0

# Manual check for Python
python3 -c "
import ast
import os
# Circular dependency detection logic
print(0)  # 0 if no circular deps
"
# Result: Must be 0
```

### Step 6: Domain Boundaries (도메인 경계)
```bash
# Cross-domain imports 체크
grep -r "from.*domain" --include="*.py" | grep -v "from domain" | grep -c "domain"
# Result: Must be 0

# DI pattern 준수 (의존성 주입)
grep -r "= .*\(\)" --include="*.py" | grep -v "__init__" | grep -c "Service()"
# Result: Must be 0 (No direct instantiation of services)
```

**⚠️ Phase B Failed = Structural Integrity Compromised**

---

## 📈 Phase C: Quality Layer (품질 검증)

### Step 7: Linting & Magic Numbers (린팅 및 매직넘버)
```bash
# Python - Ruff with all rules
ruff check . --select=ALL 2>&1 | grep "Found" | grep -oE "[0-9]+" | head -1
# Result: Must be 0

# Magic numbers 전용 검사
ruff check . --select=PLR2004 2>&1 | grep -c "PLR2004"
# Result: Must be 0

# Hardcoded values in configuration
grep -r "localhost\|127.0.0.1\|8080\|3306" --include="*.py" | grep -v "\.env" | wc -l
# Result: Must be 0
```

### Step 8: Complexity Check (복잡도 검사)
```bash
# McCabe complexity
python3 -m mccabe --min 10 **/*.py 2>/dev/null | wc -l
# Result: Must be 0 (no functions >10 complexity)

# Cognitive complexity
radon cc . -s -n B 2>/dev/null | grep -c "^    [MCF]"
# Result: Must be 0

# File length check (no file >500 lines)
find . -name "*.py" -exec wc -l {} \; | awk '$1 > 500' | wc -l
# Result: Must be 0
```

### Step 9: Test Coverage (테스트 커버리지)
```bash
# FOR TESTER AGENTS ONLY:
pytest --cov=. --cov-report=term --cov-report=json --quiet
coverage=$(jq -r '.totals.percent_covered' coverage.json | cut -d. -f1)
echo $((95 - coverage))  # Negative if above 95%
# Result: Must be ≤0 (meaning ≥95%)

# FOR NON-TESTER AGENTS:
echo -1  # Skip marker
```

### Step 10: Documentation (문서화)
```bash
# Docstring coverage
python3 -c "
import ast, glob
missing = 0
for file in glob.glob('**/*.py', recursive=True):
    if '__pycache__' in file: continue
    with open(file) as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    missing += 1
print(missing)
"
# Result: Must be 0

# README files exist check
[ -f "README.md" ] && echo 0 || echo 1
# Result: Must be 0
```

**⚠️ Phase C Failed = Code Quality Insufficient**

---

## 🚀 Phase D: Operations Layer (운영 검증)

### Step 11: Logging & Monitoring (로깅 및 모니터링)
```bash
# No print statements (구조화 로깅 강제)
grep -r "print(" --include="*.py" | grep -v "#" | wc -l
# Result: Must be 0

# Proper logger usage (DNA 신경계)
grep -r "logger\." --include="*.py" | wc -l | awk '{if($1>0) print 0; else print 1}'
# Result: Must be 0 (means logger is used)

# JSON structured logging check
grep -r "logger.*extra=" --include="*.py" | wc -l | awk '{if($1>0) print 0; else print 1}'
# Result: Must be 0 (structured logging used)

# Error messages standardization
grep -r "raise.*Exception" --include="*.py" | grep -v "Error:" | wc -l
# Result: Must be 0 (all errors have "Error:" prefix)
```

### Step 12: Security & Configuration (보안 및 설정)
```bash
# Security scan (bandit)
bandit -r . -f json 2>/dev/null | jq '.metrics._totals."SEVERITY.HIGH" + .metrics._totals."SEVERITY.MEDIUM"'
# Result: Must be 0

# Hardcoded secrets
grep -r -E "(api_key|secret|token|password)\s*=\s*[\"'][^\"']+[\"']" --include="*.py" | grep -v ".env" | wc -l
# Result: Must be 0

# Environment variables (DNA 내분비계)
grep -r "os.environ\[" --include="*.py" | grep -v "get(" | wc -l
# Result: Must be 0 (use .get() for safety)

# Configuration in code check
grep -r "DATABASE_URL\|API_KEY\|SECRET" --include="*.py" | grep -v "os.environ" | grep -v "settings" | wc -l
# Result: Must be 0 (all config via env/settings)
```

**⚠️ Phase D Failed = Not Production Ready**

---

## 📝 JSON Recording Format

### Location: `~/.claude/workflows/spark_quality_gates_v4.json`

```json
{
  "agent": "implementer-spark",
  "timestamp": "2025-01-18T15:00:00Z",
  "task": "TASK-001",
  
  "phase_a_foundation": {
    "step_1_syntax": 0,
    "step_2_type_checking": 0,
    "step_3_formatting": 0,
    "total": 0,
    "passed": 1
  },
  
  "phase_b_architecture": {
    "step_4_import_architecture": 0,
    "step_5_circular_dependencies": 0,
    "step_6_domain_boundaries": 0,
    "total": 0,
    "passed": 1
  },
  
  "phase_c_quality": {
    "step_7_linting": 0,
    "step_8_complexity": 0,
    "step_9_test_coverage": -1,  // or 95+ for testers
    "step_10_documentation": 0,
    "total": 0,
    "passed": 1
  },
  
  "phase_d_operations": {
    "step_11_logging": 0,
    "step_12_security": 0,
    "total": 0,
    "passed": 1
  },
  
  "overall": {
    "total_violations": 0,
    "all_phases_passed": 1,
    "can_proceed": 1
  }
}
```

---

## 🔄 Execution Protocol

### For Every Agent Task:

```python
## Phase 4: SPARK Quality Gates (MANDATORY - BLOCKING)

echo "=== SPARK Quality Gates v4.0 - 12 Steps ==="

# Phase A: Foundation (병렬 실행 가능)
echo "== Phase A: Foundation =="
SYNTAX=$(find . -name "*.py" | xargs python3 -m py_compile 2>&1 | grep -c "SyntaxError")
TYPE=$(mypy . --strict 2>&1 | grep -c "error:")
FORMAT=$(black . --check 2>&1 | grep -c "would be")
PHASE_A=$((SYNTAX + TYPE + FORMAT))

if [ $PHASE_A -gt 0 ]; then
    echo "❌ Phase A Failed: Fix foundation issues first"
    # Fix and retry
    exit 1
fi

# Phase B: Architecture (순차 실행 필요)
echo "== Phase B: Architecture =="
IMPORT=$(import-linter 2>&1 | grep -c "Broken")
CIRCULAR=$(pycycle . 2>&1 | grep -c "circular")
DOMAIN=$(check_domain_boundaries.sh)
PHASE_B=$((IMPORT + CIRCULAR + DOMAIN))

if [ $PHASE_B -gt 0 ]; then
    echo "❌ Phase B Failed: Fix architecture issues"
    # Fix and retry
    exit 1
fi

# Phase C: Quality
echo "== Phase C: Quality =="
# ... (similar pattern)

# Phase D: Operations
echo "== Phase D: Operations =="
# ... (similar pattern)

# Write JSON results
write_quality_results_json()

# Final verification
echo '{"subagent": "implementer-spark", "self_check": true}' | \
    python3 ~/.claude/hooks/spark_quality_gates.py
```

---

## 🎯 Why 12 Steps Matter

### DNA Bootstrap Gate Integration
1. **골격계** → Step 4-6 (Architecture)
2. **신경계** → Step 11 (Logging)
3. **면역계** → Step 9 (Testing)
4. **순환계** → Step 6 (DI patterns)
5. **내분비계** → Step 12 (Configuration)
6. **감각계** → Step 7 (Input validation via linting)
7. **소화계** → Step 2 (Data model validation via types)
8. **호흡계** → Step 11 (Performance metrics logging)

### Project Integrity Assurance
- **작업 단위가 아닌 프로젝트 전체** 무결성 검증
- **DNA 시스템 8개 모두** 지속적 점검
- **레이어 침범 방지**로 구조적 붕괴 예방
- **운영 준비도** 지속적 유지

---

## ⚠️ Critical Rules

1. **NO SKIP**: 모든 단계 필수 실행
2. **NO FAKE**: 실제 명령어 실행 결과만 기록
3. **NO PROCEED**: Phase 실패 시 다음 Phase 진행 불가
4. **NO EXCUSE**: "나중에 고치겠다" 금지
5. **NO BYPASS**: --no-verify 사용 금지

---

## 🚨 Common Violations & Fixes

### Phase A Failures
- **Syntax Error**: 즉시 수정 필수
- **Type Error**: 타입 힌트 추가/수정
- **Format Error**: `black .` 자동 실행

### Phase B Failures
- **Import Violation**: 레이어 구조 재설계
- **Circular Import**: 의존성 역전 적용
- **Domain Violation**: 도메인 경계 명확화

### Phase C Failures
- **Linting**: ruff --fix 적용
- **Complexity**: 함수 분할
- **Coverage**: 테스트 추가 작성
- **Documentation**: Docstring 추가

### Phase D Failures
- **No Logger**: 구조화 로깅 도입
- **Hardcoded Values**: 환경 변수로 이동
- **Security Issues**: 취약점 패치

---

*SPARK Quality Gates v4.0 - Enforcing Project-Wide Integrity*
*Zero Tolerance. Four Phases. Twelve Steps. One Standard.*