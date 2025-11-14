# Stage 5: DNA 시스템 구축 가이드

> **목적**: 11개 DNA 시스템 실제 구현 및 검증
> **버전**: v1.0 (2025-11-13)
> **소요 시간**: 4-8시간

---

## 🎯 이 Stage의 목표

**11개 DNA 시스템 실제 구축 및 동작 검증**

- DNA 구현 표준 작성: 통일성 규칙 정의
- 실제 구현: 체크리스트 따라 파일/코드 작성
- 통합 검증: Kent Beck 수준 (10/11개) 달성

---

## 📥 입력 문서 (Stage 4에서 받은 것)

### 필수
- **`04D-01_dna_blueprint.md`** (DNA 청사진)
  - 디렉토리 구조
  - 각 DNA 시스템별 파일 목록
  - 공개 인터페이스

- **`04T-01_dna_tasks.md`** (DNA 작업 분해)
  - 30-50개 하위 작업
  - 우선순위 (Phase 1/2)
  - 의존성

- **`04L-01_dna_checklist.md`** (DNA 체크리스트)
  - 통합 체크리스트 1개
  - 11개 섹션
  - 실행 명령어

### 참조
- **`DNA_Systems_11_Complete_Guide.md`**
- **`03A-001~011_*.md`** (DNA 시스템 ADR)

---

## 📋 작업 단계

### Step 1: DNA 구현 표준 작성 (1-2시간)

#### 1.1 파일 구조 규칙

**목표**: src/core/ 구조 통일

**작업**:
```markdown
# 05S-01_dna_standards.md 예시

## 1. 파일 구조 규칙

### 디렉토리 구조
```
src/core/           # DNA 시스템 공통 모듈
├── __init__.py     # 공개 API export
├── logger.py       # Observability (DNA 2)
├── error.py        # Error Handling (DNA 7)
├── config.py       # Configuration (DNA 6)
└── types.py        # Type definitions (DNA 1)

tests/core/         # DNA 시스템 테스트
├── __init__.py
├── test_logger.py
├── test_error.py
└── test_config.py
```

### 파일 네이밍
- 모듈 파일: snake_case (logger.py, error.py)
- 테스트 파일: test_*.py
- 설정 파일: 도구별 표준 (pyproject.toml, mypy.ini)
```

#### 1.2 네이밍 규칙

**목표**: 코드 일관성 확보

**작업**:
```markdown
## 2. 네이밍 규칙

### 클래스
- PascalCase
- 예: `AppConfig`, `CustomError`, `LoggerConfig`

### 함수
- snake_case
- 동사로 시작
- 예: `get_logger()`, `handle_error()`, `load_config()`

### 상수
- UPPER_SNAKE_CASE
- 예: `LOG_LEVEL`, `MAX_RETRIES`, `DEFAULT_TIMEOUT`

### 변수
- snake_case
- 명확한 이름
- 예: `user_id`, `error_message`, `config_path`

### Private
- 앞에 언더스코어 1개
- 예: `_internal_method()`, `_cache`
```

#### 1.3 Import 규칙

**목표**: 명확한 의존성 관리

**작업**:
```markdown
## 3. Import 규칙

### DNA 시스템 Import
- DNA 시스템은 항상 `src.core`에서 import
- 절대 경로 사용

```python
# ✅ 올바른 방법
from src.core.logger import get_logger
from src.core.error import AppError
from src.core.config import config

# ❌ 잘못된 방법
from core.logger import get_logger  # 상대 경로
from ..core.logger import get_logger  # 상대 import
```

### Import 순서
1. 표준 라이브러리
2. 서드파티 라이브러리
3. 로컬 모듈

```python
# 표준 라이브러리
import os
from typing import Optional

# 서드파티
import structlog
from pydantic import BaseModel

# 로컬
from src.core.logger import get_logger
from src.core.config import config
```
```

#### 1.4 테스트 규칙

**목표**: 95%+ 커버리지 달성

**작업**:
```markdown
## 4. 테스트 규칙

### 테스트 파일 위치
- DNA 시스템: `tests/core/test_*.py`
- 각 모듈당 1개 테스트 파일
- 예: `src/core/logger.py` → `tests/core/test_logger.py`

### 테스트 함수 네이밍
- `test_` 접두사 필수
- 기능을 명확히 설명
- 예: `test_get_logger_returns_configured_logger()`

### 테스트 구조 (Given-When-Then)
```python
def test_get_logger_with_name():
    # Given
    logger_name = "test.module"

    # When
    logger = get_logger(logger_name)

    # Then
    assert logger.name == logger_name
    assert isinstance(logger, structlog.BoundLogger)
```

### 커버리지 목표
- 단위 테스트: 95%+ 필수
- 각 DNA 시스템별 개별 확인
- 예외 경로도 테스트

```bash
# 커버리지 확인
pytest --cov=src/core --cov-report=term-missing tests/core/
```
```

#### 1.5 문서화 규칙

**목표**: 자기 설명적 코드

**작업**:
```markdown
## 5. 문서화 규칙

### Docstring 필수
- 모든 공개 함수/클래스
- Google 스타일

```python
def get_logger(name: str) -> structlog.BoundLogger:
    """구조화된 로거를 반환합니다.

    Args:
        name: 로거 이름 (일반적으로 __name__ 사용)

    Returns:
        설정된 structlog BoundLogger 인스턴스

    Example:
        ```python
        logger = get_logger(__name__)
        logger.info("message", user_id=123)
        ```
    """
    return structlog.get_logger(name)
```

### Type Hints 100%
- 모든 함수 인자와 반환값
- mypy strict mode 통과 필수

```python
# ✅ 올바른 방법
def process_data(data: dict[str, Any]) -> Result[Data, AppError]:
    ...

# ❌ 잘못된 방법
def process_data(data):  # 타입 없음
    ...
```

### 주석 최소화
- 코드로 설명
- 복잡한 로직만 주석
- "왜"를 설명 (무엇을 아님)
```

---

### Step 2: DNA 시스템 구현 (3-5시간)

#### 2.1 Phase 1: 기반 DNA 6개 구현

**목표**: 개발 환경 완성

**순서**:
1. Configuration System (6) 먼저 - 다른 DNA가 의존
2. Type System (1)
3. Observability System (2)
4. Testing System (3)
5. Code Quality System (4)
6. Architecture Enforcement (5)

**예시 - DNA 2: Observability System 구현**:

```python
# src/core/logger.py

"""구조화된 로깅 시스템 (DNA 2: Observability)"""

import structlog
from typing import Any

from src.core.config import config


def get_logger(name: str) -> structlog.BoundLogger:
    """구조화된 로거를 반환합니다.

    Args:
        name: 로거 이름 (일반적으로 __name__ 사용)

    Returns:
        설정된 structlog BoundLogger 인스턴스

    Example:
        ```python
        logger = get_logger(__name__)
        logger.info("user login", user_id=123, action="login")
        ```
    """
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

    return structlog.get_logger(name)


# 전역 로거 (편의성)
logger = get_logger(__name__)
```

**테스트**:
```python
# tests/core/test_logger.py

"""Observability System 테스트 (DNA 2)"""

import structlog
from src.core.logger import get_logger


def test_get_logger_returns_bound_logger():
    """get_logger가 structlog BoundLogger를 반환하는지 확인"""
    # Given
    logger_name = "test.module"

    # When
    logger = get_logger(logger_name)

    # Then
    assert isinstance(logger, structlog.BoundLogger)


def test_get_logger_with_different_names():
    """서로 다른 이름으로 로거를 생성할 수 있는지 확인"""
    # Given
    name1, name2 = "module1", "module2"

    # When
    logger1 = get_logger(name1)
    logger2 = get_logger(name2)

    # Then
    assert logger1.name == name1
    assert logger2.name == name2


def test_logger_info_logs_correctly(caplog):
    """로거가 info 레벨 로그를 올바르게 기록하는지 확인"""
    # Given
    logger = get_logger("test")
    message = "test message"

    # When
    logger.info(message, user_id=123)

    # Then
    assert message in caplog.text
    assert "user_id" in caplog.text
```

**체크리스트 체크**:
```markdown
### [x] DNA 2: Observability System
  - [x] structlog 추가 (`uv add structlog`)
  - [x] src/core/logger.py 작성
  - [x] get_logger() 구현
  - [x] tests/core/test_logger.py 작성 (3개 테스트)
  - [x] 테스트 실행 (`pytest tests/core/test_logger.py`)
  - [x] 커버리지 95%+ 확인
```

#### 2.2 Phase 2: 도메인 DNA 5개 구현

**목표**: 기능 구현 준비 완료

**순서**:
7. Error Handling System (7)
8. API System (9) - 프로젝트에 따라 순서 변경 가능
9. Data System (10)
10. Performance System (8)
11. Security System (11)

**예시 - DNA 7: Error Handling System 구현**:

```python
# src/core/error.py

"""에러 처리 시스템 (DNA 7: Error Handling)"""

from typing import TypeVar, Generic, Union
from dataclasses import dataclass


T = TypeVar('T')
E = TypeVar('E')


@dataclass
class Ok(Generic[T]):
    """성공 결과"""
    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value


@dataclass
class Err(Generic[E]):
    """에러 결과"""
    error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap(self) -> None:
        raise ValueError(f"Called unwrap on Err: {self.error}")


Result = Union[Ok[T], Err[E]]


class AppError(Exception):
    """애플리케이션 기본 에러"""

    def __init__(self, message: str, code: str = "UNKNOWN"):
        self.message = message
        self.code = code
        super().__init__(self.message)
```

---

### Step 3: 통합 검증 (1시간)

#### 3.1 전체 DNA 시스템 동작 확인

**목표**: 11개 DNA 모두 작동하는지 확인

**작업**:
```bash
# 1. Type System 검증
mypy src/

# 2. Code Quality 검증
ruff check src/
black --check src/

# 3. Testing System 검증
pytest tests/ --cov=src --cov-report=term-missing

# 4. Architecture Enforcement 검증
# (import-linter 등 실행)

# 5. 모든 DNA 통합 확인
pytest tests/core/  # 모든 DNA 테스트 실행
```

#### 3.2 Kent Beck 검증

**목표**: 10/11개 이상 달성

**작업**:
```markdown
# 05-검증보고서.md (선택적)

## DNA 시스템 검증 결과

| DNA               | 구현 완료 | 테스트 | 동작 확인 | 비고 |
| ----------------- | --------- | ------ | --------- | ---- |
| 1. Type           | ✅         | ✅      | ✅         | mypy strict 통과 |
| 2. Observability  | ✅         | ✅      | ✅         | structlog 설정 완료 |
| 3. Testing        | ✅         | ✅      | ✅         | pytest 95%+ 커버리지 |
| 4. Code Quality   | ✅         | ✅      | ✅         | ruff + black |
| 5. Architecture   | ✅         | ✅      | ✅         | import-linter |
| 6. Configuration  | ✅         | ✅      | ✅         | pydantic v2 |
| 7. Error Handling | ✅         | ✅      | ✅         | Result<T,E> 패턴 |
| 8. Performance    | ✅         | ✅      | ✅         | pytest-benchmark |
| 9. API            | ✅         | ✅      | ✅         | FastAPI |
| 10. Data          | ✅         | ✅      | ✅         | SQLAlchemy |
| 11. Security      | ✅         | ✅      | ✅         | bandit + safety |

**결과**: 11/11개 완성 ✅

## Kent Beck 검증
- Kent Beck BPlusTree: 10/11개 (Observability 최소)
- 우리 프로젝트: 11/11개 ✅
```

#### 3.3 품질 검사

**목표**: 0 violations

**작업**:
```bash
# Ruff 검사
ruff check src/ tests/
# Expected: All checks passed!

# Mypy 검사
mypy src/
# Expected: Success: no issues found

# 테스트 커버리지
pytest --cov=src --cov-report=term-missing --cov-fail-under=95
# Expected: Coverage >= 95%

# 보안 스캔
bandit -r src/
safety check
# Expected: No issues found
```

---

## 📤 출력 문서 (이 Stage에서 생성해야 할 것)

### 1. **`05S-01_dna_standards.md`** (DNA 구현 표준)

**내용**:
```markdown
# DNA 시스템 구현 표준

## 1. 파일 구조 규칙
[src/core/ 구조]

## 2. 네이밍 규칙
[클래스, 함수, 상수, 변수]

## 3. Import 규칙
[절대 경로, 순서]

## 4. 테스트 규칙
[95%+ 커버리지, Given-When-Then]

## 5. 문서화 규칙
[Docstring, Type Hints]

## 6. 예시 코드
[각 DNA 시스템별 템플릿]
```

---

### 2. **실제 구현 파일**

#### 설정 파일
- `pyproject.toml` (Type, Testing, Quality, Config)
- `.pre-commit-config.yaml` (Quality)
- `mypy.ini` (Type)
- `ruff.toml` (Quality)

#### DNA 시스템 코드
```
src/core/
├── __init__.py
├── logger.py      # DNA 2: Observability
├── error.py       # DNA 7: Error Handling
├── config.py      # DNA 6: Configuration
└── types.py       # DNA 1: Type definitions

tests/core/
├── __init__.py
├── test_logger.py
├── test_error.py
└── test_config.py
```

#### 기타
- `benchmarks/` (DNA 8: Performance)
- Security 스캔 설정 (DNA 11)

---

### 3. **검증 보고서** (선택적)

**내용**:
- 11개 DNA 시스템 검증 결과
- Kent Beck 비교
- 품질 검사 결과
- 커버리지 리포트

---

## 🔄 다음 Stage로 전달되는 것

**Stage 5 → Stage 6**:
- ✅ 완성된 DNA 시스템 (src/core/)
- ✅ DNA 구현 표준 (05S-01)
- ✅ 검증된 품질 (95%+ 커버리지, 0 violations)

**Stage 6에서 사용**:
- Project Standards에서 DNA 시스템 사용 강제
- "src.core에서 import 필수" 등 규칙 명시

**Stage 7에서 사용**:
- Blueprint에서 DNA 시스템 활용
- `from src.core.logger import get_logger` 등 명시

---

## ⚠️ 주의사항

### 1. TDD 기반 개발
- ❌ 코드 먼저 작성 후 테스트 X
- ✅ 테스트 먼저 작성 → 코드 구현 → 리팩토링

### 2. 한 번에 하나씩
- DNA 1개 완성 → 테스트 → 다음 DNA
- 체크리스트 하나씩 체크하며 진행

### 3. 품질 타협 금지
- 95%+ 커버리지 반드시 달성
- 0 violations 반드시 달성
- "나중에 고치자" 금지

### 4. 문서화 필수
- Docstring 없으면 미완성
- Type Hints 없으면 미완성
- 예시 코드 없으면 미완성

### 5. 실제 사용 확인
- 각 DNA 시스템을 간단한 예제로 테스트
- "만들기만 하고 안 써봄" 금지

---

## 📚 참고 자료

### 필수
- `04D-01_dna_blueprint.md` - 청사진 (파일 구조)
- `04T-01_dna_tasks.md` - 작업 분해
- `04L-01_dna_checklist.md` - 체크리스트
- `DNA_Systems_11_Complete_Guide.md` - 11개 DNA 상세

### 언어별 참고
- Python: pytest, mypy, ruff, structlog
- TypeScript: jest, prettier, eslint, winston
- Rust: cargo test, clippy, tracing
- Go: testing, golangci-lint, zap

---

## ✅ 완료 기준

이 Stage는 다음 조건을 모두 만족하면 완료:

- [ ] **05S-01_dna_standards.md** 작성 완료
  - [ ] 5개 규칙 섹션 모두 작성
  - [ ] 예시 코드 포함

- [ ] **11개 DNA 시스템 구현 완료**
  - [ ] Phase 1 (기반 6개) 완성
  - [ ] Phase 2 (도메인 5개) 완성
  - [ ] 모든 파일 구현 표준 준수

- [ ] **테스트 95%+ 커버리지**
  - [ ] 각 DNA별 테스트 작성
  - [ ] pytest --cov 실행
  - [ ] 커버리지 리포트 확인

- [ ] **품질 검사 0 violations**
  - [ ] ruff check 통과
  - [ ] mypy 통과
  - [ ] bandit 통과

- [ ] **Kent Beck 검증**
  - [ ] 10/11개 이상 달성
  - [ ] 검증 보고서 (선택)

- [ ] **04L-01 체크리스트 완료**
  - [ ] 모든 체크박스 체크
  - [ ] 전체 검증 완료

---

**마지막 업데이트**: 2025-11-13
**다음 검토**: Stage 6에서 DNA 시스템 사용 강제 확인
