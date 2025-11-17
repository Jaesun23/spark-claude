# 06G-00: Project Standards 작성 가이드 (ADR → Standards Transformation Guide)

**문서 버전**: 1.0
**작성일**: 2025-11-17
**대상**: DNA Methodology v4.0 Stage 6
**목적**: ADR 결정을 실행 가능한 Project Standards로 변환하는 방법 제공

---

## 📋 목차

- [Part 1: Project Standards란 무엇인가](#part-1-project-standards란-무엇인가)
- [Part 2: ADR → Standards 변환 프로세스 (4 Steps)](#part-2-adr--standards-변환-프로세스-4-steps)
- [Part 3: 06D-01 템플릿 및 구조](#part-3-06d-01-템플릿-및-구조)
- [Part 4: Enforcement 구현 (3 Phases)](#part-4-enforcement-구현-3-phases)
- [Part 5: 실전 예시](#part-5-실전-예시)
- [Appendix: Enforcement 코드 예시](#appendix-enforcement-코드-예시)

---

## Part 1: Project Standards란 무엇인가

### 1.1 Project Standards의 정의

**Project Standards**는 ADR의 "결정"을 개발자가 즉시 따를 수 있는 **실행 가능한 규칙**으로 변환한 문서입니다.

**핵심 차이**:

| ADR (Stage 3) | Project Standards (Stage 6) |
|---------------|----------------------------|
| **What + Why** | **How** |
| "Structlog를 사용한다" | "✅ DO: from structlog import get_logger" |
| "print() 금지" | "❌ DON'T: print('message')" |
| 결정의 기록 | 실행의 규칙 |
| 추상적 | 구체적 |

**Project Standards = ADR + DO/DON'T + Automation**

### 1.2 왜 Project Standards가 필요한가?

**문제**: ADR만으로는 일관성 강제 불가능

```markdown
# ADR-001: Structlog 채택
## 결정
모든 로깅은 Structlog를 사용한다.
```

**이 ADR만으로는:**
- ❌ 개발자가 print() 사용 가능 (ADR 위반)
- ❌ import logging 사용 가능 (ADR 위반)
- ❌ 위반 여부를 수동으로 확인해야 함 (Code Review)

**해결책**: Project Standards + Automation

```markdown
# 06D-01: Project Standards
## 표준 01: 로깅

✅ DO: from structlog import get_logger
❌ DON'T: print("message")
❌ DON'T: import logging

## Enforcement (자동화)
- Pre-commit: print() 감지 시 커밋 실패
- ArchUnit: import logging 감지 시 빌드 실패
```

**결과**:
- ✅ 개발자가 print() 사용 시 즉시 차단 (커밋 전)
- ✅ Code Review 부담 감소 (자동화가 검증)
- ✅ AI 협업 시 명시적 규칙 제공

### 1.3 DNA v4.0의 미싱 링크

**엔터프라이즈는 왜 Standards가 없는가?**

엔터프라이즈 (인간 협업):
```
ADR (결정)
  ↓
Code Review (인간이 검증)
  ↓
암묵적 지식으로 일관성 유지
```

DNA v4.0 (AI 협업):
```
ADR (결정)
  ↓
Standards (명시적 규칙) ← 미싱 링크!
  ↓
Governance (자동화 강제)
  ↓
Blueprint (설계)
```

**핵심 차이**:
- 인간 = 암묵적 지식 OK, 무제한 컨텍스트
- AI = 명시적 규칙 필수, 200K 토큰 제약

**따라서**: DNA v4.0는 Standards를 **명시적 문서**로 작성!

### 1.4 4대 구성요소에서 Standards의 위치

```
┌──────────────────────────────────────────────┐
│ 1. 성문화된 결정 (ADR) - Stage 3             │
│    Why + What                                │
└────────────────┬─────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────┐
│ 2. 재사용 가능한 컴포넌트 (DNA Systems)       │
│    Tools (src/core/)                         │
└────────────────┬─────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────┐
│ 3. 의무적 규칙 집합 (Standards) - Stage 6 ← │
│    DO/DON'T Rulebook                         │
└────────────────┬─────────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────────┐
│ 4. 자동화된 거버넌스 (Enforcement) - Stage 9 │
│    Police (pre-commit, ArchUnit, Fitness)    │
└──────────────────────────────────────────────┘
```

**Standards = ADR (결정)과 Governance (자동화)를 연결하는 다리!**

---

## Part 2: ADR → Standards 변환 프로세스 (4 Steps)

### 2.1 전체 프로세스 개요

```
Step 1: ADR 결정 추출
  ↓
Step 2: DO/DON'T 규칙 정의
  ↓
Step 3: 자동화 코드 작성
  ↓
Step 4: 검증 테스트 작성
  ↓
06D-01 Standards 완성
```

### 2.2 Step 1: ADR 결정 추출

**목적**: ADR에서 "실행 가능한 결정" 식별

**Input**: ADR-001 Structlog 채택 (Category 5: DNA System)

```markdown
# ADR-001: 구조화된 로깅을 위한 Structlog 채택

## 결정 (Decision)
모든 Python 기반 DNA 시스템의 로깅 표준으로 Structlog 라이브러리를 채택한다.

## 요구사항 (Requirements)
- R-01: 모든 로그는 JSON 형식이어야 함
- R-02: Request ID, User ID 등 Context 자동 주입 가능
- R-03: Python 표준 logging과 호환

## 강제화 방안 (Enforcement)
- Pre-commit: print(), import logging 금지
```

**Output**: 추출된 기술 결정

```
1. "Structlog 사용"
2. "JSON 형식 로깅"
3. "Context 자동 주입"
4. "print() 금지"
5. "import logging 금지"
```

**추출 기준**:
- ✅ 구체적 행동 (Use X, Don't use Y)
- ✅ 검증 가능 (코드로 검증 가능)
- ❌ 추상적 목표 ("좋은 로그를 작성한다" - 검증 불가)

### 2.3 Step 2: DO/DON'T 규칙 정의

**목적**: 추상적 결정을 구체적 실행 규칙으로 변환

**변환 표**:

| ADR 결정 (추상적) | → | Standards 규칙 (구체적) |
|-------------------|---|------------------------|
| "Structlog 사용" | → | ✅ DO: `from structlog import get_logger` |
| "JSON 형식" | → | ✅ DO: `logger.info("event", key="value")` |
| (위 규칙 위반) | → | ❌ DON'T: `logger.info(f"msg {var}")` (JSON 깨짐) |
| "print() 금지" | → | ❌ DON'T: `print("message")` |
| "import logging 금지" | → | ❌ DON'T: `import logging` |

**DO/DON'T 작성 원칙**:

1. **구체성**: 코드 예시 포함
   - ❌ "로거를 사용하라"
   - ✅ "from structlog import get_logger"

2. **검증 가능성**: 자동화 가능한 규칙
   - ❌ "좋은 로그 메시지를 작성하라" (주관적)
   - ✅ "print() 사용 금지" (pygrep으로 검증 가능)

3. **짝**: DO와 DON'T를 함께
   - ✅ DO: `logger.info("event", user_id=123)`
   - ❌ DON'T: `print(f"User {uid} logged in")`

**실제 예시**:

```markdown
## 표준 01: 로깅 (Logging)

### 규칙 (Rules)

| ✅ DO (해야 할 일) | ❌ DON'T (하지 말아야 할 일) |
|-------------------|----------------------------|
| `from structlog import get_logger` | `import logging` |
| `logger = get_logger(__name__)` | `logger = logging.getLogger(__name__)` |
| `logger.info("user_login", user_id=123)` | `logger.info(f"User {uid} logged in")` |
| `logger.error("error_event", exc_info=True)` | `print(f"Error: {e}")` |
```

### 2.4 Step 3: 자동화 코드 작성

**목적**: DO/DON'T 규칙을 자동으로 검증하는 코드 작성

**3단계 자동화**:

```
Phase 1: Static Analysis (개발 중)
  - Pre-commit hooks
  - 즉시 피드백 (< 1초)

Phase 2: Architecture Tests (CI/CD)
  - ArchUnit, import-linter
  - PR 머지 전 검증

Phase 3: Runtime Validation (배포 전)
  - Fitness Functions
  - 배포 게이트
```

**Step 3a: Pre-commit Hook 작성**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      # 표준 01: print() 사용 금지
      - id: disallow-print
        name: "Disallow print()"
        entry: "print\\("  # 정규식
        language: pygrep
        types: [python]
        description: "Prohibited: 'print()'. Use 'logger' from DNA System 01."

      # 표준 01: 표준 logging 모듈 임포트 금지
      - id: disallow-stdlib-logging
        name: "Disallow 'import logging'"
        entry: "^import logging"  # 라인 시작
        language: pygrep
        types: [python]
        description: "Prohibited: 'import logging'. Use 'structlog'."
```

**Step 3b: Architecture Test 작성**

```python
# tests/architecture/test_logging.py
import pytest
from pathlib import Path

def test_no_print_in_src():
    """표준 01: src/ 폴더에 print() 사용 금지"""
    src_files = Path("src").rglob("*.py")
    violations = []

    for file in src_files:
        content = file.read_text()
        if "print(" in content:
            violations.append(str(file))

    assert not violations, f"print() found in: {violations}"


def test_no_stdlib_logging_import():
    """표준 01: src/ 폴더에 import logging 금지"""
    src_files = Path("src").rglob("*.py")
    violations = []

    for file in src_files:
        content = file.read_text()
        if "import logging" in content:
            violations.append(str(file))

    assert not violations, f"import logging found in: {violations}"
```

**Step 3c: Fitness Function (선택적)**

```python
# tests/fitness/test_logging_format.py
import pytest
import json

def test_logs_are_json_format():
    """표준 01: 모든 로그는 JSON 형식이어야 함"""
    # 로그 파일 읽기 (테스트 환경)
    with open("logs/test.log") as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                assert "event" in log_entry
                assert "timestamp" in log_entry
            except json.JSONDecodeError:
                pytest.fail(f"Non-JSON log found: {line}")
```

### 2.5 Step 4: 검증 테스트 작성

**목적**: Enforcement가 실제로 작동하는지 검증

**테스트 전략**:

```python
# tests/test_enforcement.py

def test_pre_commit_blocks_print():
    """Pre-commit이 print()를 차단하는지 검증"""
    # 1. print() 포함 파일 생성
    test_file = "src/test_violation.py"
    with open(test_file, "w") as f:
        f.write("print('hello')\n")

    # 2. pre-commit 실행
    result = subprocess.run(
        ["pre-commit", "run", "--files", test_file],
        capture_output=True
    )

    # 3. 실패해야 함
    assert result.returncode != 0
    assert "disallow-print" in result.stdout.decode()

    # 4. 파일 삭제
    os.remove(test_file)


def test_architecture_test_detects_logging_import():
    """Architecture test가 import logging을 감지하는지 검증"""
    # 1. import logging 포함 파일 생성
    test_file = "src/test_violation2.py"
    with open(test_file, "w") as f:
        f.write("import logging\n")

    # 2. Architecture test 실행
    result = subprocess.run(
        ["pytest", "tests/architecture/test_logging.py"],
        capture_output=True
    )

    # 3. 실패해야 함
    assert result.returncode != 0
    assert "import logging found" in result.stdout.decode()

    # 4. 파일 삭제
    os.remove(test_file)
```

---

## Part 3: 06D-01 템플릿 및 구조

### 3.1 06D-01 파일 구조

```markdown
# 06D-01: [Project Name] 프로젝트 표준

버전: 1.0
최종 수정: YYYY-MM-DD
ADR 참조: ADR-001, ADR-002, ADR-003, ADR-301

---

## Part 1: Mandatory Standards (필수 5대 표준)

### 1.1 표준 01: 로깅 (Logging)
- ADR 근거
- 규칙 (DO/DON'T)
- 강제화 (Enforcement)

### 1.2 표준 02: 에러 핸들링 (Error Handling)
[동일 구조]

### 1.3 표준 03: 설정 관리 (Configuration)
[동일 구조]

### 1.4 표준 04: 데이터베이스 접근 (Database Access)
[동일 구조]

### 1.5 표준 05: 테스팅 (Testing)
[동일 구조]

---

## Part 2: Domain-Specific Standards (도메인 특화 표준)

### 2.1 표준 06: API 설계 (API Design)
[프로젝트별 추가]

### 2.2 표준 07: ...
[프로젝트별 추가]

---

## Part 3: Enforcement Code (자동화 코드)

### 3.1 Pre-commit Configuration
[.pre-commit-config.yaml]

### 3.2 Architecture Tests
[tests/architecture/*.py]

### 3.3 Fitness Functions
[tests/fitness/*.py]
```

### 3.2 Mandatory 5 Standards (필수)

**DNA v4.0의 5가지 필수 표준**:

| 표준 | DNA System ADR | 목적 |
|------|----------------|------|
| 01. 로깅 | ADR-001 | 구조화된 JSON 로깅 |
| 02. 에러 핸들링 | ADR-002 | 표준화된 예외 처리 |
| 03. 설정 관리 | ADR-003 | 환경별 설정 관리 |
| 04. 데이터베이스 접근 | ADR-004 | DB 접근 패턴 통일 |
| 05. 테스팅 | ADR-005 | 테스트 작성 규칙 |

**Why 5개 필수?**
- DNA Systems 11개 중 **모든 프로젝트에 공통** 적용되는 것들
- 나머지 6개 (006-011)는 선택적 (프로젝트별)

### 3.3 표준 01: 로깅 (Logging) - 완전한 예시

```markdown
### 1.1 표준 01: 로깅 (Logging)

#### ADR 근거
- **ADR-001**: Structured Logging (Structlog 채택)
- **목적**: 분산 시스템에서 로그 추적 및 ELK 스택 통합

#### 규칙 (Rules)

| ✅ DO (해야 할 일) | ❌ DON'T (하지 말아야 할 일) |
|-------------------|----------------------------|
| `from structlog import get_logger` | `import logging` |
| `logger = get_logger(__name__)` | `logger = logging.getLogger(__name__)` |
| `logger.info("user_login", user_id=123, request_id="req-001")` | `logger.info(f"User {uid} logged in")` |
| `logger.error("api_error", exc_info=True, status_code=500)` | `print(f"Error: {e}")` |
| Context 자동 주입 (Request ID, User ID) | Hard-coded context 값 |

#### 표준 사용 예시

```python
# ✅ CORRECT: DNA System 01 사용
from src.core.logging import get_logger

logger = get_logger(__name__)

def create_user(user_id: int, username: str):
    logger.info(
        "user_created",
        user_id=user_id,
        username=username,
        action="create"
    )
    # 출력: {"event": "user_created", "user_id": 123, "username": "jason", ...}
```

```python
# ❌ INCORRECT: print() 사용
def create_user(user_id: int, username: str):
    print(f"User {username} created")  # 커밋 실패!
```

```python
# ❌ INCORRECT: 표준 logging 사용
import logging  # 커밋 실패!

logger = logging.getLogger(__name__)

def create_user(user_id: int, username: str):
    logger.info(f"User {username} created")
```

#### 강제화 (Enforcement)

**정적 분석 (Static Analysis) - Pre-commit**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: disallow-print
        name: "Disallow print()"
        entry: "print\\("
        language: pygrep
        types: [python]
        files: ^src/
        description: "Use logger from src.core.logging"

      - id: disallow-stdlib-logging
        name: "Disallow 'import logging'"
        entry: "^import logging"
        language: pygrep
        types: [python]
        files: ^src/
        description: "Use structlog from DNA System 01"
```

**아키텍처 테스트 (Architecture Tests) - CI/CD**

```python
# tests/architecture/test_logging_standard.py
import pytest
from pathlib import Path

def test_no_print_statements_in_src():
    """표준 01: src/ 폴더에 print() 사용 금지"""
    src_files = list(Path("src").rglob("*.py"))
    violations = []

    for file in src_files:
        content = file.read_text()
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if "print(" in line and not line.strip().startswith("#"):
                violations.append(f"{file}:{i}")

    assert not violations, (
        f"Found {len(violations)} print() violations:\n"
        + "\n".join(violations[:10])  # 처음 10개만 표시
    )


def test_no_stdlib_logging_imports():
    """표준 01: src/ 폴더에 import logging 금지"""
    src_files = list(Path("src").rglob("*.py"))
    violations = []

    for file in src_files:
        content = file.read_text()
        if "import logging" in content or "from logging import" in content:
            violations.append(str(file))

    assert not violations, (
        f"Found stdlib logging imports in:\n"
        + "\n".join(violations)
    )


def test_all_modules_use_structlog():
    """표준 01: 모든 모듈은 structlog 사용"""
    src_files = list(Path("src").rglob("*.py"))

    # logger = get_logger(__name__) 패턴 확인
    for file in src_files:
        if file.name == "__init__.py":
            continue

        content = file.read_text()

        # 로거 사용하는 파일만 검증
        if "logger." in content:
            assert "from src.core.logging import get_logger" in content, (
                f"{file} uses logger but doesn't import from DNA System 01"
            )
```

**런타임 검증 (Runtime Validation) - 선택적**

```python
# tests/fitness/test_log_format.py
import pytest
import json
from pathlib import Path

def test_all_logs_are_valid_json():
    """표준 01: 모든 로그는 유효한 JSON이어야 함"""
    log_file = Path("logs/test.log")

    if not log_file.exists():
        pytest.skip("No log file found")

    with open(log_file) as f:
        for i, line in enumerate(f, 1):
            try:
                log_entry = json.loads(line)

                # 필수 필드 검증
                assert "event" in log_entry, f"Line {i}: missing 'event'"
                assert "timestamp" in log_entry, f"Line {i}: missing 'timestamp'"

            except json.JSONDecodeError as e:
                pytest.fail(f"Line {i}: Invalid JSON - {e}\n{line}")
```
```

### 3.4 표준 02: 에러 핸들링 (Error Handling) - 완전한 예시

```markdown
### 1.2 표준 02: 에러 핸들링 (Error Handling)

#### ADR 근거
- **ADR-002**: Error Handling Standard
- **목적**: 일관된 예외 처리 및 RFC 7807 준수

#### 규칙 (Rules)

| ✅ DO (해야 할 일) | ❌ DON'T (하지 말아야 할 일) |
|-------------------|----------------------------|
| `class UserNotFound(BaseProjectException):` | `raise Exception("User not found")` |
| `except SpecificError as e: logger.error(...)` | `except Exception: pass` (예외 무시) |
| `raise HTTPException(404, detail="...")` | `raise Exception("error")` (컨텍스트 없음) |
| RFC 7807 포맷 반환 | Raw 에러 메시지 반환 |

#### 표준 사용 예시

```python
# ✅ CORRECT: BaseProjectException 상속
from src.core.errors import BaseProjectException

class UserNotFoundError(BaseProjectException):
    """사용자를 찾을 수 없음"""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")


def get_user(user_id: int):
    user = db.get(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user
```

```python
# ❌ INCORRECT: Generic Exception
def get_user(user_id: int):
    user = db.get(user_id)
    if not user:
        raise Exception("User not found")  # 빌드 실패!
    return user
```

```python
# ❌ INCORRECT: 예외 무시
try:
    result = risky_operation()
except Exception:
    pass  # 빌드 실패!
```

#### 강제화 (Enforcement)

**정적 분석 (Static Analysis) - Ruff**

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.4.4
  hooks:
    - id: ruff
      args:
        - --select=BLE  # Blind except (except:)
        - --select=TRY  # Try/except patterns
```

**아키텍처 테스트 (Architecture Tests)**

```python
# tests/architecture/test_error_handling.py
import ast
import pytest
from pathlib import Path

def test_no_generic_exception_raise():
    """표준 02: Exception을 직접 raise 금지"""
    src_files = list(Path("src").rglob("*.py"))
    violations = []

    for file in src_files:
        tree = ast.parse(file.read_text())

        for node in ast.walk(tree):
            if isinstance(node, ast.Raise):
                if isinstance(node.exc, ast.Call):
                    if isinstance(node.exc.func, ast.Name):
                        if node.exc.func.id == "Exception":
                            violations.append(
                                f"{file}:{node.lineno}"
                            )

    assert not violations, (
        f"Found {len(violations)} generic Exception raises:\n"
        + "\n".join(violations)
    )


def test_all_exceptions_inherit_from_base():
    """표준 02: 모든 예외는 BaseProjectException 상속"""
    # src/domain/errors.py 검증
    errors_file = Path("src/domain/errors.py")

    if not errors_file.exists():
        pytest.skip("No domain errors file")

    tree = ast.parse(errors_file.read_text())

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if node.name.endswith("Error") or node.name.endswith("Exception"):
                # BaseProjectException 상속 확인
                has_base = any(
                    isinstance(base, ast.Name) and
                    base.id == "BaseProjectException"
                    for base in node.bases
                )

                assert has_base, (
                    f"{node.name} must inherit from BaseProjectException"
                )
```
```

---

## Part 4: Enforcement 구현 (3 Phases)

### 4.1 3-Phase 자동화 성숙도 모델

**목표**: 비용 효율적인 순서로 자동화 구현

```
┌─────────────────────────────────────────────────────┐
│ Phase 1: Static Analysis (Day 1)                    │
│ - Pre-commit hooks                                  │
│ - Linters (Ruff, ESLint)                           │
│ - 즉시 피드백 (< 1초)                               │
│ - 비용: 낮음, 효과: 높음                            │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ Phase 2: Architecture Tests (Week 2)                │
│ - ArchUnit, import-linter                          │
│ - CI/CD 파이프라인                                  │
│ - 비용: 중간, 효과: 높음                            │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ Phase 3: Runtime Validation (Month 1+)              │
│ - Fitness Functions, Policy-as-Code                │
│ - 배포 게이트                                       │
│ - 비용: 높음, 효과: 중간                            │
└─────────────────────────────────────────────────────┘
```

### 4.2 Phase 1: Static Analysis (Day 1)

**목표**: 개발자 PC에서 즉시 피드백

**우선순위**:
1. ⭐⭐⭐ 코드 포맷팅 (Black, Prettier)
2. ⭐⭐⭐ 명백한 위반 (print(), import logging)
3. ⭐⭐ 타입 힌트 (mypy, pyright)

**구현**:

```yaml
# .pre-commit-config.yaml
repos:
  # 1. 코드 포맷팅 (최우선)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # 2. DNA 표준 강제화 (로컬)
  - repo: local
    hooks:
      - id: disallow-print
        name: "표준 01: print() 금지"
        entry: "print\\("
        language: pygrep
        types: [python]
        files: ^src/

      - id: disallow-stdlib-logging
        name: "표준 01: import logging 금지"
        entry: "^import logging"
        language: pygrep
        types: [python]
        files: ^src/

  # 3. 타입 힌트 (선택적)
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

**설치 및 실행**:

```bash
# 1. pre-commit 설치
pip install pre-commit

# 2. Git hooks 등록
pre-commit install

# 3. 모든 파일에 실행 (최초 1회)
pre-commit run --all-files

# 4. 이후 자동 실행 (git commit 시)
git commit -m "feat: add user api"
# → pre-commit이 자동으로 실행되어 위반 사항 차단
```

### 4.3 Phase 2: Architecture Tests (Week 2)

**목표**: CI/CD에서 아키텍처 규칙 검증

**우선순위**:
1. ⭐⭐⭐ Layer 의존성 (Domain → Infrastructure 금지)
2. ⭐⭐ DNA System 사용 (import logging 금지)
3. ⭐⭐ 순환 의존성 방지

**Python: import-linter**

```toml
# .importlinter
[importlinter]
root_package = src

[importlinter:contract:layers]
name = Layered Architecture
type = layers
layers =
    api
    domain
    infrastructure

[importlinter:contract:no-stdlib-logging]
name = No stdlib logging
type = forbidden
source_modules =
    src
forbidden_modules =
    logging
```

**Java: ArchUnit**

```java
// tests/architecture/ArchitectureTest.java
import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
import static com.tngtech.archunit.library.Architectures.layeredArchitecture;

class ArchitectureTest {

    private final JavaClasses classes = new ClassFileImporter()
        .importPackages("com.myproject");

    @Test
    void layered_architecture_is_respected() {
        ArchRule rule = layeredArchitecture()
            .layer("API").definedBy("..api..")
            .layer("Domain").definedBy("..domain..")
            .layer("Infrastructure").definedBy("..infrastructure..")

            .whereLayer("API").mayNotBeAccessedByAnyLayer()
            .whereLayer("Domain").mayOnlyBeAccessedByLayers("API")
            .whereLayer("Infrastructure").mayOnlyBeAccessedByLayers("API", "Domain");

        rule.check(classes);
    }

    @Test
    void domain_should_not_depend_on_infrastructure() {
        ArchRule rule = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAPackage("..infrastructure..");

        rule.check(classes);
    }
}
```

**CI/CD 통합 (GitHub Actions)**:

```yaml
# .github/workflows/quality.yml
name: Quality Gates

on: [push, pull_request]

jobs:
  architecture-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install import-linter

      - name: Run architecture tests
        run: |
          pytest tests/architecture/
          import-linter
```

### 4.4 Phase 3: Runtime Validation (Month 1+)

**목표**: NFR 및 Policy-as-Code 검증

**우선순위**:
1. ⭐⭐ NFR 검증 (API 응답 시간, DB 쿼리 성능)
2. ⭐⭐ 보안 정책 (AWS Region, IAM Policy)
3. ⭐ 인프라 제약 (Terraform Sentinel, OPA)

**Fitness Functions (pytest)**:

```python
# tests/fitness/test_nfr_performance.py
import pytest
import requests
import time

def test_api_response_time_under_200ms():
    """NFR P-01: API 응답 시간 < 200ms (P95)"""
    response_times = []

    for _ in range(100):
        start = time.time()
        response = requests.get("http://localhost:8000/api/users")
        elapsed = time.time() - start
        response_times.append(elapsed)

    # P95 계산
    p95 = sorted(response_times)[94]

    assert response.status_code == 200
    assert p95 < 0.2, f"P95 response time {p95:.3f}s exceeds 200ms"


def test_database_query_performance():
    """NFR P-02: DB 쿼리 < 500ms"""
    from src.infrastructure.database import db

    start = time.time()
    results = db.query("SELECT * FROM users LIMIT 1000")
    elapsed = time.time() - start

    assert elapsed < 0.5, f"Query took {elapsed:.3f}s (> 500ms)"
```

**Policy-as-Code (Terraform Sentinel)**:

```hcl
# policies/aws-region-restriction.sentinel
import "tfplan/v2" as tfplan

# 모든 AWS 리소스는 ap-northeast-2 (Seoul) 리전만 허용
main = rule {
    all tfplan.resource_changes as _, rc {
        rc.provider_name is "registry.terraform.io/hashicorp/aws"

        implies rc.change.after.region is "ap-northeast-2"
    }
}
```

---

## Part 5: 실전 예시

### 5.1 Stock Trading Platform Standards

**프로젝트**: 주식 자동 거래 시스템
**ADR 개수**: 18개
**Standards 개수**: 8개 (Mandatory 5 + Domain 3)

#### 06D-01: Stock Trading Project Standards

```markdown
# 06D-01: Stock Trading 프로젝트 표준

버전: 1.0
최종 수정: 2025-02-15
ADR 참조: ADR-001, ADR-002, ADR-003, ADR-301, ADR-302

---

## Part 1: Mandatory Standards (필수 5대 표준)

### 1.1 표준 01: 로깅 (Logging)
- ADR 근거: ADR-001 (Structlog)
- [Part 3.3 참조]

### 1.2 표준 02: 에러 핸들링 (Error Handling)
- ADR 근거: ADR-002
- [Part 3.4 참조]

### 1.3 표준 03: 설정 관리 (Configuration)
- ADR 근거: ADR-003 (Pydantic Settings)
- [생략]

### 1.4 표준 04: 데이터베이스 접근 (Database Access)
- ADR 근거: ADR-004 (SQLAlchemy ORM)
- [생략]

### 1.5 표준 05: 테스팅 (Testing)
- ADR 근거: ADR-005 (pytest)
- [생략]

---

## Part 2: Domain-Specific Standards (도메인 특화 3개)

### 2.1 표준 06: API 설계 (API Design)

#### ADR 근거
- ADR-301: FastAPI 채택
- ADR-305: RESTful API 원칙

#### 규칙 (Rules)

| ✅ DO | ❌ DON'T |
|-------|----------|
| `GET /v1/users/{user_id}` (경로 파라미터) | `GET /v1/getUser?id={id}` (쿼리) |
| `class UserResponse(BaseModel):` (Pydantic 모델) | `return {"id": 1}` (Raw dict) |
| `404 Not Found` 반환 | `200 OK + {"error": "..."}` |
| `POST /v1/users` (자원 생성) | `POST /v1/createUser` (동사) |

#### 강제화

```python
# tests/architecture/test_api_design.py
def test_all_routes_use_pydantic_models():
    """표준 06: 모든 API는 Pydantic 모델 사용"""
    from src.api import app

    for route in app.routes:
        if hasattr(route, "response_model"):
            assert route.response_model is not None, (
                f"{route.path} has no response_model"
            )
```

### 2.2 표준 07: 한국투자증권 API 사용 (KIS API)

#### ADR 근거
- ADR-101: 한국투자증권 API 사용 강제 (External Constraint)
- ADR-103: Rate Limit 준수 (초당 20건)

#### 규칙 (Rules)

| ✅ DO | ❌ DON'T |
|-------|----------|
| `from src.infrastructure.kis import KISClient` | 직접 requests 사용 |
| Rate Limiter 통과 후 API 호출 | 직접 API 호출 (Rate Limit 위반) |
| 토큰 자동 갱신 사용 | 수동 토큰 관리 |

#### 강제화

```python
# tests/architecture/test_kis_api.py
def test_no_direct_kis_api_calls():
    """표준 07: KIS API는 KISClient를 통해서만 호출"""
    src_files = list(Path("src/domain").rglob("*.py"))

    for file in src_files:
        content = file.read_text()

        # 직접 requests 사용 금지
        if "requests.get" in content or "requests.post" in content:
            # KIS API URL 패턴
            if "openapi.koreainvestment.com" in content:
                pytest.fail(
                    f"{file} calls KIS API directly. "
                    "Use KISClient from src.infrastructure.kis"
                )
```

### 2.3 표준 08: 거래 조건 검증 (Trading Conditions)

#### ADR 근거
- ADR-401: Priority Queue Scheduler (Domain Technology)

#### 규칙 (Rules)

| ✅ DO | ❌ DON'T |
|-------|----------|
| 모든 조건은 Scheduler에 등록 | 직접 폴링 루프 작성 |
| 우선순위 1-10 명시 | 우선순위 없이 등록 |
| 조건 평가 결과 로깅 | 조건 평가 결과 무시 |

---

## Part 3: Enforcement Code

### 3.1 Pre-commit Configuration

[Part 4.2 참조]

### 3.2 Architecture Tests

```python
# tests/architecture/test_all_standards.py
import pytest
from pathlib import Path

class TestMandatoryStandards:
    """필수 5대 표준 검증"""

    def test_standard_01_logging(self):
        """표준 01: 로깅"""
        # [Part 3.3 참조]

    def test_standard_02_error_handling(self):
        """표준 02: 에러 핸들링"""
        # [Part 3.4 참조]

    # ... 3, 4, 5


class TestDomainStandards:
    """도메인 특화 표준 검증"""

    def test_standard_06_api_design(self):
        """표준 06: API 설계"""
        # [위 참조]

    def test_standard_07_kis_api_usage(self):
        """표준 07: KIS API 사용"""
        # [위 참조]
```

### 3.3 CI/CD Integration

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on: [push, pull_request]

jobs:
  standards-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run architecture tests
        run: |
          pytest tests/architecture/ -v

      - name: Verify no violations
        run: |
          pytest tests/architecture/ --tb=short
          # 실패 시 PR 머지 차단
```
```

---

## Appendix: Enforcement 코드 예시

### A.1 Pre-commit Hook 전체 예시

```yaml
# .pre-commit-config.yaml
repos:
  # 기본 hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace

  # Ruff: Python Linter & Formatter
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # DNA v4.0 Standards
  - repo: local
    hooks:
      # 표준 01: 로깅
      - id: disallow-print
        name: "표준 01: print() 금지"
        entry: "print\\("
        language: pygrep
        types: [python]
        files: ^src/
        description: "Use logger from src.core.logging"

      - id: disallow-stdlib-logging
        name: "표준 01: import logging 금지"
        entry: "^import logging"
        language: pygrep
        types: [python]
        files: ^src/
        description: "Use structlog from DNA System 01"

      # 표준 02: 에러 핸들링
      - id: no-generic-exception
        name: "표준 02: Generic Exception 금지"
        entry: "raise Exception\\("
        language: pygrep
        types: [python]
        files: ^src/
        description: "Use BaseProjectException"

      # 표준 07: KIS API (Stock Trading 특화)
      - id: no-direct-kis-api
        name: "표준 07: 직접 KIS API 호출 금지"
        entry: "openapi\\.koreainvestment\\.com"
        language: pygrep
        types: [python]
        files: ^src/domain/
        description: "Use KISClient from infrastructure"
```

### A.2 Architecture Test 전체 예시

```python
# tests/architecture/test_dna_standards.py
"""
DNA v4.0 Project Standards 검증

이 테스트는 06D-01에 정의된 모든 표준이 준수되는지 검증합니다.
"""
import ast
import pytest
from pathlib import Path
from typing import List


class TestMandatoryStandards:
    """필수 5대 표준 검증"""

    @pytest.fixture
    def src_files(self) -> List[Path]:
        """src/ 폴더의 모든 Python 파일"""
        return list(Path("src").rglob("*.py"))

    def test_standard_01_no_print_statements(self, src_files):
        """표준 01: print() 사용 금지"""
        violations = []

        for file in src_files:
            content = file.read_text()
            lines = content.split("\n")

            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                # 주석 제외
                if stripped.startswith("#"):
                    continue

                if "print(" in line:
                    violations.append(f"{file}:{i}")

        assert not violations, (
            f"Found {len(violations)} print() violations:\n"
            + "\n".join(violations[:10])
        )

    def test_standard_01_no_stdlib_logging(self, src_files):
        """표준 01: import logging 금지"""
        violations = []

        for file in src_files:
            content = file.read_text()

            if "import logging" in content or "from logging import" in content:
                violations.append(str(file))

        assert not violations, (
            f"Found stdlib logging in:\n" + "\n".join(violations)
        )

    def test_standard_02_no_generic_exception_raise(self, src_files):
        """표준 02: Exception을 직접 raise 금지"""
        violations = []

        for file in src_files:
            try:
                tree = ast.parse(file.read_text())
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Raise):
                    if isinstance(node.exc, ast.Call):
                        if isinstance(node.exc.func, ast.Name):
                            if node.exc.func.id == "Exception":
                                violations.append(f"{file}:{node.lineno}")

        assert not violations, (
            f"Found {len(violations)} generic Exception raises:\n"
            + "\n".join(violations)
        )

    def test_standard_02_all_exceptions_inherit_base(self):
        """표준 02: 모든 예외는 BaseProjectException 상속"""
        errors_file = Path("src/domain/errors.py")

        if not errors_file.exists():
            pytest.skip("No domain errors file")

        tree = ast.parse(errors_file.read_text())
        violations = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Error/Exception으로 끝나는 클래스만 검증
                if node.name.endswith(("Error", "Exception")):
                    has_base = any(
                        isinstance(base, ast.Name) and
                        base.id == "BaseProjectException"
                        for base in node.bases
                    )

                    if not has_base:
                        violations.append(node.name)

        assert not violations, (
            f"These exceptions don't inherit BaseProjectException:\n"
            + "\n".join(violations)
        )


class TestLayeredArchitecture:
    """아키텍처 Layer 검증"""

    def test_domain_does_not_import_infrastructure(self):
        """Domain 레이어는 Infrastructure 레이어 임포트 금지"""
        domain_files = list(Path("src/domain").rglob("*.py"))
        violations = []

        for file in domain_files:
            content = file.read_text()

            if "from src.infrastructure" in content:
                violations.append(str(file))
            elif "import src.infrastructure" in content:
                violations.append(str(file))

        assert not violations, (
            f"Domain imports Infrastructure in:\n"
            + "\n".join(violations)
        )

    def test_no_circular_dependencies(self):
        """순환 의존성 금지"""
        # import-linter로 검증 (별도 실행)
        pytest.skip("Use import-linter in CI/CD")


class TestDomainSpecificStandards:
    """도메인 특화 표준 검증"""

    def test_api_routes_use_pydantic_models(self):
        """표준 06: 모든 API는 Pydantic 모델 사용"""
        api_files = list(Path("src/api/routes").rglob("*.py"))

        for file in api_files:
            content = file.read_text()

            # FastAPI route decorator 찾기
            if "@router." in content or "@app." in content:
                # Pydantic import 확인
                assert "from pydantic import" in content or "BaseModel" in content, (
                    f"{file} has API routes but no Pydantic models"
                )
```

### A.3 Fitness Function 예시

```python
# tests/fitness/test_performance_nfr.py
"""
NFR 성능 요구사항 검증 (Fitness Functions)

ADR-201: 검색 성능 vs 일관성 트레이드오프
- NFR P-01: API 응답 시간 < 1초 (P95)
"""
import pytest
import requests
import time
import statistics

@pytest.mark.fitness
def test_api_p95_response_time_under_1_second():
    """NFR P-01: API P95 응답 시간 < 1초"""
    # 100회 요청
    response_times = []

    for _ in range(100):
        start = time.time()
        response = requests.get("http://localhost:8000/api/search?q=test")
        elapsed = time.time() - start

        assert response.status_code == 200
        response_times.append(elapsed)

    # P95 계산
    p95 = statistics.quantiles(response_times, n=20)[18]  # 95th percentile

    assert p95 < 1.0, (
        f"P95 response time {p95:.3f}s exceeds 1 second\n"
        f"Mean: {statistics.mean(response_times):.3f}s\n"
        f"Max: {max(response_times):.3f}s"
    )


@pytest.mark.fitness
def test_database_query_performance():
    """NFR P-02: DB 쿼리 < 500ms"""
    from src.infrastructure.database import db

    start = time.time()
    results = db.query("SELECT * FROM users WHERE active = true LIMIT 1000")
    elapsed = time.time() - start

    assert elapsed < 0.5, f"Query took {elapsed:.3f}s (> 500ms)"
    assert len(results) > 0, "No results returned"
```

---

## 🎯 다음 단계

**Standards 작성 완료 후**:

1. **Stage 9: Governance 구현**
   - 가이드: `09G-00_governance_guide.md` (다음 작성 예정)
   - Pre-commit hooks 실제 설치
   - CI/CD 파이프라인 구축

2. **Stage 7: Blueprint 작성**
   - Standards를 기반으로 구체적 설계
   - API 스펙, DB 스키마, 배포 전략

3. **Stage 8: Implementation**
   - Blueprint → 실제 코드
   - Standards 자동 검증

---

**작성일**: 2025-11-17
**작성자**: 2호 (with Jason)
**관련 문서**:
- `docs/03G-00_adr_guide.md` - ADR 작성 가이드
- `docs/09G-00_governance_guide.md` - Governance 구현 가이드 (작성 예정)
- `docs/research/20251117_Gemini_미싱링크_분석결과.md` - 미싱 링크 분석
