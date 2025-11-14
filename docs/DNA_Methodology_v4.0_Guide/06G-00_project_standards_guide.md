# 프로젝트 표준 문서 작성 가이드

> **목적**: Stage 6 - ADR 결정을 실행 가능한 표준 규칙으로 변환하여 Agent가 따를 수 있는 구체적 가이드를 제공합니다.
>
> **버전**: v2.0 (2025-11-12)
> - v2.0: Stage 6 범위 명시, 입력/출력 문서 추가

---

## 📥 입력 문서 (Stage 3-5에서 받은 것)

Stage 6를 시작하기 전에 다음 문서를 읽어야 합니다:

#### 1. **모든 DNA 시스템 ADR** (필수)
**위치**: `docs/adr/DNA 시스템/03A-001_*.md` ~ `03A-015_*.md`
- 로깅, 에러 처리, 인증, 설정 등 공통 환경 결정
- **활용**: DNA 시스템 표준 규칙 작성

#### 2. **모든 Domain ADR** (필수)
**위치**: `docs/adr/domain/03A-101_*.md` ~ `03A-130_*.md`
- 기술 스택, 데이터 설계, API 설계 등 프로젝트 특화 결정
- **활용**: Domain 표준 규칙 작성

#### 3. **05S-01_dna_standards.md** (참고)
**위치**: `docs/stage5/05S-01_dna_standards.md` (Stage 5에서 작성됨)
- DNA 구현 표준 (파일 구조, 네이밍, Import 규칙, 테스트 규칙, 문서화 규칙)
- **활용**: DNA 시스템 사용 규칙 작성 시 참고

#### 4. **구현된 core/ 모듈** (참고)
**위치**: `src/core/` (Stage 5에서 구현됨)
- 실제 DNA 시스템 코드 (logger.py, error.py, config.py, types.py 등)
- **활용**: 실제 API 확인, 사용 예시 작성

---

## 📤 출력 문서 (이 Stage에서 생성해야 할 문서)

### 필수 문서

#### 1. **`06D-01_project_standards.md`** - 프로젝트 표준 (THE 산출물)
**내용**:
- ADR 결정을 실행 가능한 규칙으로 변환
- Agent가 직접 읽고 따를 수 있는 구체적 가이드
- Mandatory vs Optional 구분

**구조** (5개 섹션):
```markdown
# PROJECT STANDARDS

## 1. Naming Conventions
- File naming: snake_case, max 50 chars
- Variable naming: camelCase
- Class naming: PascalCase
- Examples: ✅ DO / ❌ DON'T

## 2. Code Organization
- Directory structure
- Module boundaries
- Import rules

## 3. Core Modules Usage
- Mandatory: MUST use core.logging
- Examples: ✅ DO / ❌ DON'T

## 4. Quality Standards
- Test coverage: 95%+ unit, 85%+ integration
- Linting: ruff, mypy
- Format: black

## 5. Development Workflow
- Git commit convention
- PR rules
- Review criteria
```

**예시**:
```markdown
## 3. Core Modules Usage

### 3.1 Logging (Mandatory)
**Rule**: MUST use `core.logging.get_logger()`

✅ **DO**:
```python
from core.logging import get_logger
logger = get_logger(__name__)
logger.info("Order created", order_id=order.id)
```

❌ **DON'T**:
```python
import logging  # FORBIDDEN!
logger = logging.getLogger(__name__)
```

**Enforcement**: Pre-commit hook blocks `import logging`
**Reference**: ADR-001 Logging Strategy
```

**특징**:
- ✅ DO / ❌ DON'T 예시 필수
- Enforcement 방법 명시
- ADR 참조 링크

---

## 🔄 다음 Stage로 전달되는 것

Stage 6 → Stage 7:
- ✅ 완성된 프로젝트 표준 문서
- ✅ Mandatory vs Optional 구분
- ✅ Agent가 따를 구체적 규칙
- ✅ Enforcement 방법

Stage 7 (Blueprint)에서는 이를 기반으로:
- 표준 규칙을 적용한 상세 청사진 작성
- 도메인별 구현 가이드에 표준 반영

---

## 목차

1. [프로젝트 표준이란](#1-프로젝트-표준이란)
2. [Mandatory vs Optional Standards](#2-mandatory-vs-optional-standards)
3. [Standards 파일 구조](#3-standards-파일-구조)
4. [ADR → Standards 변환 상세 절차](#4-adr--standards-변환-상세-절차)
5. [Individual Standard 작성하기](#5-individual-standard-작성하기)
6. [Progressive Accumulation 전략](#6-progressive-accumulation-전략)
7. [Standards 생명주기 관리](#7-standards-생명주기-관리)
8. [다음 단계 연결](#8-다음-단계-연결)

---

## 1. 프로젝트 표준이란

### 1-1. 정의

**Project Standards**는 ADR 결정을 구체적인 실행 규칙으로 변환한 문서입니다.

**핵심 개념**:
- **ADR = 결정 (What + Why)**
- **Standards = 실행 (How + Enforcement)**
- **Agent가 직접 읽고 따를 수 있는 수준의 구체성**

### 1-2. ADR vs Standards 비교

| 측면 | ADR | Standards |
|------|-----|-----------|
| **목적** | 아키텍처 결정 기록 | 실행 가이드 제공 |
| **내용** | Decision + Context + Rationale | Rules + Examples + Patterns |
| **독자** | 의사결정자 (Jason, 1호, 2호) | 개발자, Agent |
| **형식** | 서술형 (왜 이렇게 결정했나) | 명령형 (이렇게 하라) |
| **변경** | 불변 (Superseded로 대체) | 업데이트 가능 (패턴 추가) |
| **구조** | 7개 섹션 (flexible) | 5개 섹션 (fixed) |

### 1-3. 정보 흐름에서 Standards의 위치

```
ADR Documents (Decisions)
    ↓ Transformation
PROJECT_STANDARDS (Rules) ← 이 가이드!
    ↓ Applied to
BLUEPRINT (System Design)
    ↓ Broken down
TASK Documents (Work Units)
    ↓ Converted to
CHECKLIST (Agent Instructions)
    ↓ Execute
Agent Implementation
```

**Standards의 역할**:
- ✅ ADR 결정을 코드로 옮기는 **변환 계층**
- ✅ Blueprint 작성 시 **참조할 규칙 집합**
- ✅ Task/Checklist에 **인라인 복사될 내용**
- ✅ Quality Gates의 **검증 기준**

### 1-4. Jason의 방법론에서 Standards의 중요성

**Problem**: ADR만으로는 Agent가 실행 불가

```markdown
❌ ADR-015: "structlog를 사용하기로 결정"
   → Agent: "어떻게 사용하나요? import는? 형식은?"
```

**Solution**: Standards가 구체적 실행 규칙 제공

```markdown
✅ Standards/01_logging.md:
   - Import: `from structlog import get_logger`
   - Format: `logger.info("event_name", key=value)`
   - Forbidden: `print()`, `import logging`
   - Enforcement: pre-commit hook, ruff T201
   → Agent: 명확하게 따라 할 수 있음!
```

**핵심 인사이트**:
- Standards = "Blueprint를 작성하는 사람"이 따를 규칙
- Standards = "Checklist에 인라인 복사"될 내용
- Standards = "Quality Gates가 검증"할 기준

---

## 2. Mandatory vs Optional Standards

### 2-1. Mandatory Standards (필수 5개)

**모든 프로젝트에 필수적인 표준**:

#### 01. Logging (`01_logging.md`)
**Why Mandatory**: 프로덕션 디버깅, 모니터링, 감사 추적 필수

**출처 ADR 예시**:
- ADR-015: structlog 사용
- ADR-016: 로그 레벨 규칙
- ADR-017: 민감 정보 로깅 금지

**주요 내용**:
- Import 규칙
- Event 명명 규칙
- Context binding
- 금지 사항 (print, logging 모듈)
- Enforcement (pre-commit, ruff)

#### 02. Error Handling (`02_error_handling.md`)
**Why Mandatory**: 모든 코드는 에러를 다뤄야 함

**출처 ADR 예시**:
- ADR-020: Custom exception hierarchy
- ADR-021: 에러 로깅 규칙
- ADR-022: User-facing error messages

**주요 내용**:
- Exception 계층 구조
- 에러 발생 패턴 (raise vs return)
- 에러 로깅 규칙
- User-facing vs Internal errors
- Enforcement (mypy, pytest)

#### 03. Configuration (`03_configuration.md`)
**Why Mandatory**: 모든 프로젝트는 설정 관리 필요

**출처 ADR 예시**:
- ADR-025: pydantic-settings 사용
- ADR-026: .env 파일 규칙
- ADR-027: 시크릿 관리 (AWS Secrets Manager)

**주요 내용**:
- Settings class 패턴 (Pydantic)
- 환경별 설정 (.env.dev, .env.prod)
- 시크릿 관리
- 금지 사항 (하드코딩, git commit)
- Enforcement (pre-commit hook)

#### 04. Type Hints (`04_type_hints.md`)
**Why Mandatory**: 타입 안정성은 품질의 기본

**출처 ADR 예시**:
- ADR-030: 100% type hints coverage
- ADR-031: mypy strict mode
- ADR-032: Pydantic for DTOs

**주요 내용**:
- Type hint 규칙 (모든 함수, 클래스)
- Generic types (List, Dict, Optional)
- Pydantic models for data
- 금지 사항 (Any, type: ignore 남용)
- Enforcement (mypy strict)

#### 05. Testing (`05_testing.md`)
**Why Mandatory**: 테스트 없는 코드는 레거시

**출처 ADR 예시**:
- ADR-010: 95% coverage 필수
- ADR-035: pytest 사용
- ADR-036: Given-When-Then 패턴

**주요 내용**:
- Test 구조 (Given-When-Then)
- Fixture 사용법
- Mocking 규칙
- Coverage requirements (95% unit, 85% integration)
- Enforcement (pytest-cov, CI)

### 2-2. Optional Standards (프로젝트 필요에 따라)

#### 06. Database (`06_database.md`)
**When Needed**: DB를 사용하는 프로젝트

**출처 ADR 예시**:
- ADR-040: PostgreSQL 사용
- ADR-041: SQLAlchemy ORM
- ADR-042: Migration with Alembic

**주요 내용**:
- Connection management
- Repository pattern
- Migration 규칙
- Transaction 관리

#### 07. API (`07_api.md`)
**When Needed**: API를 제공하는 프로젝트

**출처 ADR 예시**:
- ADR-025: FastAPI + OpenAPI
- ADR-045: RESTful conventions
- ADR-046: Rate limiting

**주요 내용**:
- Endpoint naming
- HTTP methods, status codes
- Request/Response models (Pydantic)
- Error responses
- Enforcement (OpenAPI validation)

#### 08. Authentication (`08_authentication.md`)
**When Needed**: 사용자 인증이 필요한 프로젝트

**출처 ADR 예시**:
- ADR-050: JWT tokens
- ADR-051: OAuth2 + OIDC
- ADR-052: Session management

#### 09. Performance (`09_performance.md`)
**When Needed**: 성능 최적화가 필요한 프로젝트

**출처 ADR 예시**:
- ADR-055: Redis caching
- ADR-056: async/await 규칙
- ADR-057: DB query optimization

#### 10. Architecture (`10_architecture.md`)
**When Needed**: 복잡한 시스템 (Clean Architecture 등)

**출처 ADR 예시**:
- ADR-001: Clean Architecture
- ADR-002: DDD patterns
- ADR-003: Dependency injection

### 2-3. Universal Standards

#### 99. Common Mistakes (`99_common_mistakes.md`)
**항상 필요**: 모든 Task에 적용되는 범용 실수 집합

**출처**:
- 여러 ADR의 Consequences (harder)
- 과거 프로젝트 경험
- 코드 리뷰에서 발견된 패턴

**구조**:
```markdown
# 99. Common Mistakes

## Category: Imports
**Mistake 1: 상대 import 남용**
❌ from ..domain import User
✅ from src.domain import User

## Category: Error Handling
**Mistake 2: 빈 except**
❌ try: ... except: pass
✅ try: ... except SpecificError as e: logger.error(...)

## Category: Type Hints
**Mistake 3: Any 남용**
❌ def process(data: Any) -> Any
✅ def process(data: dict[str, int]) -> ProcessResult
```

### 2-4. Standards 우선순위

**프로젝트 시작 시** (Week 1):
1. ✅ Mandatory 5개 (01-05) - 즉시 작성
2. ✅ 99_common_mistakes.md - 초기 버전 작성

**필요 시점에 추가**:
- Week 2: API 개발 시작 → 07_api.md 작성
- Week 3: DB 연동 시작 → 06_database.md 작성
- Week 4: 인증 구현 → 08_authentication.md 작성

**나중에 추가** (최적화 단계):
- Month 2: 성능 이슈 발생 → 09_performance.md 작성
- Month 3: 아키텍처 정리 → 10_architecture.md 작성

---

## 3. Standards 파일 구조

### 3-1. 파일 분리 전략

**원칙**: 각 표준은 독립된 파일, 150-200 lines

**디렉토리 구조**:
```
PROJECT_STANDARDS/
├── 00_index.md (100 lines)        # 전체 인덱스, ADR 매핑
├── 01_logging.md (150 lines)      # Mandatory
├── 02_error_handling.md (180 lines)
├── 03_configuration.md (120 lines)
├── 04_type_hints.md (160 lines)
├── 05_testing.md (200 lines)
├── 06_database.md (180 lines)     # Optional
├── 07_api.md (200 lines)
├── 08_authentication.md (150 lines)
├── 09_performance.md (140 lines)
├── 10_architecture.md (220 lines)
└── 99_common_mistakes.md (200 lines)  # Universal
```

**파일 크기 기준**:
- ✅ 150-200 lines: 이상적
- ⚠️ 100-150 lines: 괜찮음 (간단한 표준)
- ⚠️ 200-250 lines: 괜찮음 (복잡한 표준)
- ❌ 250+ lines: 파일 분리 검토 (예: 07_api.md → 07_api_rest.md, 07_api_graphql.md)

### 3-2. Individual File 구조 (5개 섹션)

**모든 Standards 파일은 동일한 5개 섹션 구조**:

```markdown
# XX. [Standard Name]

> **출처**: ADR-XXX, ADR-YYY
> **업데이트**: YYYY-MM-DD

## 1. [Core Section 1] (Line 1-40)
핵심 규칙, import, 기본 패턴

## 2. [Core Section 2] (Line 41-80)
상세 규칙, 고급 패턴

## 3. [Core Section 3] (Line 81-120)
특수 케이스, 예외 처리

## 4. Common Mistakes (Line 121-160)
자주 하는 실수 (❌/✅ Before/After)

## 5. Enforcement (Line 161-200)
검증 메커니즘 (pre-commit, CI, Quality Gates)
```

**Line 범위 표시 이유**:
- Task 문서에서 정확히 참조: "01_logging.md Line 41-80"
- Agent가 읽을 범위 명확: 전체 150 lines가 아닌 40 lines만
- Progressive disclosure: 필요한 부분만

### 3-3. 00_index.md 구조

**목적**: ADR → Standards 매핑, 빠른 네비게이션

```markdown
# 00. Project Standards Index

> **Last Updated**: 2025-01-15
> **Project**: MyProject v1.0

## Standards Overview

### Mandatory Standards (5)
- ✅ 01_logging.md - Logging rules (structlog)
- ✅ 02_error_handling.md - Exception handling
- ✅ 03_configuration.md - Settings management
- ✅ 04_type_hints.md - Type safety
- ✅ 05_testing.md - Testing practices

### Optional Standards (5)
- ✅ 06_database.md - PostgreSQL + SQLAlchemy
- ✅ 07_api.md - FastAPI + OpenAPI
- ⏳ 08_authentication.md - (Planned Week 5)
- ⏳ 09_performance.md - (Planned Month 2)
- ⏳ 10_architecture.md - (Planned Month 3)

### Universal Standards
- ✅ 99_common_mistakes.md - Common pitfalls

---

## ADR → Standards Mapping

| ADR | 제목 | 생성 Standards | 날짜 |
|-----|------|----------------|------|
| ADR-001 | Clean Architecture | 10_architecture.md | 2025-01-05 |
| ADR-010 | 95% Coverage | 05_testing.md Section 4 | 2025-01-10 |
| ADR-015 | structlog 사용 | 01_logging.md 전체 | 2025-01-15 |
| ADR-020 | Domain → Infra 금지 | 10_architecture.md Section 2 | 2025-01-20 |
| ADR-025 | FastAPI + OpenAPI | 07_api.md 전체 | 2025-01-25 |

---

## When to Read Which Standard

**JWT 토큰 생성 구현 시**:
- 01_logging.md Line 31-60 (Event format)
- 02_error_handling.md Line 41-80 (Custom exceptions)
- 04_type_hints.md Line 81-120 (Pydantic models)
- 08_authentication.md Line 1-40 (JWT basics)

**API endpoint 추가 시**:
- 01_logging.md Line 61-90 (Request context)
- 07_api.md Line 1-120 (Endpoint, models, errors)
- 05_testing.md Line 81-120 (API testing)

**Database query 작성 시**:
- 06_database.md Line 1-80 (Repository pattern)
- 02_error_handling.md Line 81-120 (DB errors)
- 09_performance.md Line 41-80 (Query optimization)

---

## Cross-References

**01_logging.md references**:
- 02_error_handling.md: Exception 로깅 규칙
- 07_api.md: Request ID binding

**07_api.md references**:
- 01_logging.md: API 로깅
- 04_type_hints.md: Pydantic models
- 02_error_handling.md: Error responses
```

---

## 4. ADR → Standards 변환 상세 절차

### 4-1. 변환 절차 Overview

```
ADR Document
    ↓ Step 1: 섹션 매핑
Decision → Standards Sections 1-3
Compliance → Standards Section 5
Consequences (harder) → Standards Section 4
    ↓ Step 2: 형식 변환
서술형 (why) → 명령형 (how)
예시 추가 (Good/Bad)
Line 범위 할당
    ↓ Step 3: Enforcement 추가
Pre-commit hooks
CI pipeline
Quality Gates
    ↓ Output
Standards/XX_name.md (150-200 lines)
```

### 4-2. Step 1: ADR 섹션 → Standards 섹션 매핑

#### ADR Decision → Standards Sections 1-3

**ADR Decision 예시** (ADR-015):
```markdown
## Decision
모든 로깅은 structlog 사용.

Import:
```python
from structlog import get_logger
logger = get_logger()
```

Pattern:
```python
logger.info("event_name", key=value)
```

Forbidden:
- print()
- import logging
```

**→ Standards Section 1-3 변환**:

**Section 1: Import and Setup** (Line 1-40)
```markdown
## 1. Import and Setup (Line 1-40)

**Mandatory Import**:
```python
from structlog import get_logger
logger = get_logger()
```

**Configuration** (main.py 또는 settings.py):
```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)
```

**Forbidden Imports**:
❌ `import logging` - 표준 logging 모듈 사용 금지
❌ `from logging import getLogger` - 모든 logging 모듈 금지

**Why**: ELK stack 연동을 위해 structlog만 사용
```

**Section 2: Event Format** (Line 41-80)
```markdown
## 2. Event Format (Line 41-80)

**Pattern**: `logger.info("event_name", key=value)`

**Event Naming Rules**:
- snake_case 사용 (user_login, not UserLogin)
- 동사_명사 형태 (token_generated, order_created)
- 과거형 사용 안 함 (user_logged_in ❌)

**Good Examples**:
```python
✅ logger.info("user_login", user_id=user.id, ip=request.ip)
✅ logger.error("token_expired", token_id=token.jti, user_id=user.id)
✅ logger.warning("rate_limit_exceeded", user_id=user.id, limit=100)
```

**Bad Examples**:
```python
❌ logger.info(f"User {user.id} logged in")  # 문자열 포맷 사용
❌ logger.info("login")                       # Context 없음
❌ logger.info("User Login")                  # CamelCase
❌ print(f"User logged in: {user.id}")       # print 사용
```

**Why**:
- ELK stack은 key-value 필요 (문자열 파싱 불가)
- Request ID로 필터링 가능
- 성능 분석 (duration 자동 기록)
```

**Section 3: Context Binding** (Line 81-120)
```markdown
## 3. Context Binding (Line 81-120)

**Request ID Auto-binding** (FastAPI):
```python
from structlog import get_logger
import uuid

@app.middleware("http")
async def bind_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    logger = get_logger().bind(request_id=request_id)
    # request.state.logger = logger (store for later use)
    response = await call_next(request)
    return response
```

**User Context Binding**:
```python
logger = get_logger().bind(user_id=current_user.id)
logger.info("order_created", order_id=order.id)
# Output: {"event": "order_created", "order_id": 123, "user_id": 456, "request_id": "abc-123", ...}
```

**Exception Logging**:
```python
try:
    token = generate_token(user_id)
except TokenGenerationError as e:
    logger.error("token_generation_failed", user_id=user_id, exc_info=True)
    raise
```

**Why**: Context binding으로 모든 로그에 request_id, user_id 자동 포함
```

#### ADR Consequences (Harder) → Standards Section 4

**ADR Consequences 예시**:
```markdown
## Consequences
❌ **Harder**:
- 초기 설정 복잡도
- 팀 교육 필요 (structlog API)
- Migration 작업 (500+ print() 제거)
```

**→ Standards Section 4: Common Mistakes**:
```markdown
## 4. Common Mistakes (Line 121-160)

**Mistake 1: 문자열 포맷 사용**
```python
❌ Before: logger.info(f"Processing {count} items")
✅ After:  logger.info("processing_items", count=count)
```
**Why**: ELK stack은 key-value 필요, f-string은 파싱 불가
**출처**: ADR-015 Consequences (Migration 작업 중 발견)

**Mistake 2: print() 사용**
```python
❌ Before: print(f"User {user.id} logged in")
✅ After:  logger.info("user_login", user_id=user.id)
```
**Why**: print()는 파일 저장 안 됨, ELK 수집 불가
**출처**: ADR-015 Decision (print 금지)

**Mistake 3: 민감 정보 로깅**
```python
❌ Before: logger.info("auth", password=password, token=token)
✅ After:  logger.info("auth", user_id=user.id)
```
**Why**: 보안 이슈, GDPR 위반, 감사 실패
**출처**: 과거 프로젝트 보안 감사에서 발견

**Mistake 4: Exception 로깅 시 context 누락**
```python
❌ Before: logger.error("Error occurred")
✅ After:  logger.error("token_generation_failed", user_id=user.id, exc_info=True)
```
**Why**: 디버깅을 위한 context 필수, exc_info=True로 스택 트레이스 포함
```

#### ADR Compliance → Standards Section 5

**ADR Compliance 예시**:
```markdown
## Compliance
1. Automated: pre-commit hook (print 차단)
2. Automated: ruff T201
3. Semi-automated: PR 체크리스트
4. Manual: 민감 정보 로깅 리뷰
```

**→ Standards Section 5: Enforcement**:
```markdown
## 5. Enforcement (Line 161-200)

### 5-1. Pre-commit Hook

**설정** (`.pre-commit-config.yaml`):
```yaml
- repo: local
  hooks:
    - id: no-print
      name: Detect print()
      entry: python scripts/check_no_print.py
      language: python
      types: [python]
```

**스크립트** (`scripts/check_no_print.py`):
```python
import sys
import re

def check_file(filename):
    with open(filename) as f:
        content = f.read()
    if re.search(r'\bprint\s*\(', content):
        print(f"❌ {filename}: print() 사용 금지. logger.info() 사용.")
        return False
    return True

if __name__ == "__main__":
    files = sys.argv[1:]
    if not all(check_file(f) for f in files):
        sys.exit(1)
```

### 5-2. Ruff Configuration

**설정** (`pyproject.toml`):
```toml
[tool.ruff]
select = ["T201"]  # Detect print()

[tool.ruff.lint]
ignore = []
```

**실행**:
```bash
ruff check .
# Output: src/main.py:10:5: T201 `print` found
```

### 5-3. CI Pipeline

**GitHub Actions** (`.github/workflows/ci.yml`):
```yaml
name: CI
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: pip install ruff
      - name: Check print()
        run: ruff check .
```

### 5-4. Quality Gates (Phase 5B)

**Agent 자가 검증** (`~/.claude/hooks/spark_quality_gates.py`):
```python
def check_logging_standards():
    """Check logging standards compliance."""
    # Ruff check
    result = subprocess.run(["ruff", "check", "."], capture_output=True)
    if result.returncode != 0:
        return False, "Ruff violations (T201 print detected)"

    # Grep check (backup)
    result = subprocess.run(["grep", "-r", "print(", "src/"], capture_output=True)
    if result.returncode == 0:
        return False, "print() detected in src/"

    return True, "Logging standards OK"
```

### 5-5. PR Checklist

**PR Template** (`.github/pull_request_template.md`):
```markdown
## Logging Checklist
- [ ] print() 없음 (logger.info() 사용)
- [ ] logger.info("event", key=value) 형식 준수
- [ ] 민감 정보(password, token) 로깅 없음
- [ ] Exception 로깅 시 exc_info=True 포함
```

### 5-6. Manual Review (주 1회)

**리뷰 항목**:
1. 민감 정보 로깅 여부 (password, token, API key)
2. Event naming convention 준수 (snake_case, 동사_명사)
3. Context binding 적절성 (request_id, user_id)
4. 로그 레벨 적절성 (info vs warning vs error)

**리뷰 주기**: 매주 금요일 오후 2시
```

### 4-3. Step 2: 형식 변환 (서술형 → 명령형)

**ADR Decision (서술형)**:
```markdown
우리는 structlog를 사용하기로 결정했습니다.
이는 ELK stack과의 연동을 위해 JSON 포맷이 필요하기 때문입니다.
```

**→ Standards (명령형)**:
```markdown
**모든 로깅은 structlog 사용.**

```python
from structlog import get_logger
logger = get_logger()
logger.info("event_name", key=value)
```

**Why**: ELK stack 연동 (JSON 포맷 필요)
```

**변환 원칙**:
- ❌ "우리는 ~하기로 결정했습니다" (과거형, 설명)
- ✅ "~하라", "~사용", "~금지" (명령형, 직접적)
- ❌ "이는 ~때문입니다" (이유 중심)
- ✅ "**Why**: ~" (선택적 이유, 짧게)

### 4-4. Step 3: 예시 추가 (Good/Bad)

**ADR에는 예시가 적거나 없을 수 있음**:
```markdown
## Decision
logger.info("event_name", key=value) 형식 사용
```

**→ Standards에는 충분한 예시 필요**:
```markdown
**Good Examples**:
```python
✅ logger.info("user_login", user_id=user.id, ip=request.ip)
✅ logger.error("token_expired", token_id=token.jti, user_id=user.id)
✅ logger.warning("rate_limit_exceeded", user_id=user.id, limit=100)
```

**Bad Examples**:
```python
❌ logger.info(f"User {user.id} logged in")  # 문자열 포맷
❌ logger.info("login")                       # Context 없음
❌ logger.info("User Login")                  # CamelCase
```
```

**예시 작성 원칙**:
- Good 3개, Bad 3개 (최소)
- Bad는 실제로 하기 쉬운 실수
- 각 Bad에 주석으로 이유 설명
- Before/After 쌍으로 제시

### 4-5. Step 4: Line 범위 할당

**각 섹션에 Line 범위 명시**:
```markdown
## 1. Import and Setup (Line 1-40)
[40 lines of content]

## 2. Event Format (Line 41-80)
[40 lines of content]

## 3. Context Binding (Line 81-120)
[40 lines of content]

## 4. Common Mistakes (Line 121-160)
[40 lines of content]

## 5. Enforcement (Line 161-200)
[40 lines of content]
```

**Line 범위 계산**:
- 섹션당 평균 40 lines
- 복잡한 섹션 50-60 lines
- 간단한 섹션 30 lines
- 총합 150-200 lines

**Why Line 범위 필요**:
```markdown
Task 문서에서:
"이 Task에 필요한 Standards:
- 01_logging.md Line 41-80 (Event format만)
- 04_type_hints.md Line 81-120 (Pydantic models만)"

→ Agent는 전체 150 lines가 아닌 40 lines씩만 읽음!
```

---

## 5. Individual Standard 작성하기

### 5-1. 01_logging.md 완성 예시

**전체 구조** (150 lines):
```markdown
# 01. Logging Standards

> **출처**: ADR-015 (structlog 사용)
> **업데이트**: 2025-01-15

## 1. Import and Setup (Line 1-40)
[Mandatory import, configuration, forbidden]

## 2. Event Format (Line 41-80)
[Pattern, naming, good/bad examples]

## 3. Context Binding (Line 81-120)
[Request ID, user context, exception logging]

## 4. Common Mistakes (Line 121-160)
[4-5 mistakes with before/after]

## 5. Enforcement (Line 161-200)
[Pre-commit, ruff, CI, Quality Gates, PR checklist, manual review]
```

### 5-2. 07_api.md 작성 예시 (FastAPI)

**출처 ADR**:
- ADR-025: FastAPI + OpenAPI
- ADR-045: RESTful conventions
- ADR-046: Rate limiting

**Section 1: Endpoint Naming** (Line 1-50):
```markdown
## 1. Endpoint Naming (Line 1-50)

**Pattern**: `/api/v1/{resource}`

**Collection Endpoints**:
```python
@app.get("/api/v1/users")
async def list_users(
    skip: int = 0,
    limit: int = 100,
) -> List[UserResponse]:
    """List all users with pagination."""
    ...

@app.post("/api/v1/users")
async def create_user(user: UserCreateRequest) -> UserResponse:
    """Create a new user."""
    ...
```

**Item Endpoints**:
```python
@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: int) -> UserResponse:
    """Get user by ID."""
    ...

@app.patch("/api/v1/users/{user_id}")
async def update_user(
    user_id: int,
    update: UserUpdateRequest,
) -> UserResponse:
    """Update user (partial)."""
    ...

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: int) -> None:
    """Delete user."""
    ...
```

**Action Endpoints** (non-CRUD):
```python
@app.post("/api/v1/users/{user_id}/activate")
async def activate_user(user_id: int) -> UserResponse:
    """Activate user account."""
    ...

@app.post("/api/v1/users/{user_id}/send-email")
async def send_email(user_id: int, email: EmailRequest) -> None:
    """Send email to user."""
    ...
```

**Forbidden Patterns**:
❌ `/users` - API prefix 누락
❌ `/api/user` - 단수형 (복수형 사용!)
❌ `/api/v1/activate/{user_id}` - Action이 앞에 (뒤에!)
❌ `/api/v1/users/get` - GET 중복 (메서드로 충분)

**Why**: RESTful convention, OpenAPI 자동 생성 최적화
```

**Section 2: Request/Response Models** (Line 51-100):
```markdown
## 2. Request/Response Models (Line 51-100)

**모든 request/response는 Pydantic models 사용.**

**Request Models**:
```python
from pydantic import BaseModel, EmailStr, Field

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    name: str = Field(min_length=1, max_length=100)

class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    # password는 별도 endpoint (PATCH /users/{id}/password)
```

**Response Models**:
```python
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True  # SQLAlchemy ORM 지원
```

**Good Examples**:
```python
✅ class UserCreateRequest(BaseModel):
       email: EmailStr  # EmailStr로 validation
       password: str = Field(min_length=8)  # Field로 제약

✅ class UserResponse(BaseModel):
       id: int
       email: EmailStr
       # password 포함 안 함! (보안)
```

**Bad Examples**:
```python
❌ @app.post("/api/v1/users")
   async def create_user(email: str, password: str):  # dict 대신 개별 파라미터
       ...

❌ class UserResponse(BaseModel):
       password_hash: str  # 민감 정보 노출!

❌ async def get_user(user_id: int) -> dict:  # dict 대신 Pydantic model
```

**Why**: 자동 validation, OpenAPI schema 생성, Type safety
```

**Section 3: HTTP Status Codes** (Line 101-140):
```markdown
## 3. HTTP Status Codes (Line 101-140)

**Status Code Rules**:
- **200 OK**: GET, PATCH 성공
- **201 Created**: POST 성공 (생성)
- **204 No Content**: DELETE 성공
- **400 Bad Request**: Client error (validation)
- **401 Unauthorized**: 인증 실패
- **403 Forbidden**: 권한 없음
- **404 Not Found**: 리소스 없음
- **422 Unprocessable Entity**: Pydantic validation 실패
- **500 Internal Server Error**: Server error

**Good Examples**:
```python
✅ @app.post("/api/v1/users", status_code=201)  # 201 Created
   async def create_user(user: UserCreateRequest) -> UserResponse:
       ...

✅ @app.delete("/api/v1/users/{user_id}", status_code=204)
   async def delete_user(user_id: int) -> None:  # None = 204
       ...

✅ @app.get("/api/v1/users/{user_id}")
   async def get_user(user_id: int) -> UserResponse:
       user = await get_user_by_id(user_id)
       if not user:
           raise HTTPException(status_code=404, detail="User not found")
       return user
```

**Bad Examples**:
```python
❌ @app.post("/api/v1/users")  # status_code 누락 (200 리턴됨)
   async def create_user(...) -> UserResponse:

❌ @app.delete("/api/v1/users/{user_id}")
   async def delete_user(...) -> dict:
       return {"message": "Deleted"}  # 204 대신 200 + body

❌ @app.get("/api/v1/users/{user_id}")
   async def get_user(...) -> UserResponse | None:
       return None  # 404 대신 200 + null
```

**Why**: RESTful convention, Client가 status code로 결과 판단
```

**Section 4: Common Mistakes** (Line 141-180):
```markdown
## 4. Common Mistakes (Line 141-180)

**Mistake 1: dict 사용**
```python
❌ Before:
   @app.post("/api/v1/users")
   async def create_user(data: dict) -> dict:
       email = data["email"]  # KeyError 가능
       ...

✅ After:
   @app.post("/api/v1/users")
   async def create_user(user: UserCreateRequest) -> UserResponse:
       # Pydantic이 자동 validation
```

**Mistake 2: Response에 민감 정보 포함**
```python
❌ Before:
   class UserResponse(BaseModel):
       id: int
       email: EmailStr
       password_hash: str  # 노출됨!

✅ After:
   class UserResponse(BaseModel):
       id: int
       email: EmailStr
       # password 관련 필드 제외
```

**Mistake 3: Error 세부사항 노출**
```python
❌ Before:
   except Exception as e:
       raise HTTPException(500, detail=str(e))  # 스택 트레이스 노출

✅ After:
   except SpecificError as e:
       logger.error("user_creation_failed", exc_info=True)
       raise HTTPException(500, detail="Internal server error")
```

**Mistake 4: status_code 누락**
```python
❌ Before:
   @app.post("/api/v1/users")  # 200 리턴
   async def create_user(...):

✅ After:
   @app.post("/api/v1/users", status_code=201)
   async def create_user(...):
```
```

**Section 5: Enforcement** (Line 181-220):
```markdown
## 5. Enforcement (Line 181-220)

### 5-1. OpenAPI Schema Validation

**자동 생성**:
```python
# FastAPI가 자동으로 /docs endpoint 생성
# http://localhost:8000/docs
```

**Schema export**:
```bash
# OpenAPI spec export
python scripts/export_openapi.py > openapi.json
```

**Validation** (CI):
```yaml
# .github/workflows/ci.yml
- name: OpenAPI Schema Diff
  run: |
    python scripts/export_openapi.py > openapi_new.json
    openapi-diff openapi_old.json openapi_new.json
```

### 5-2. Pydantic Validation (Runtime)

**자동 검증** (FastAPI가 자동으로 실행):
```python
class UserCreateRequest(BaseModel):
    email: EmailStr  # 자동 email validation
    password: str = Field(min_length=8)  # 자동 length validation

# Client가 잘못된 요청 보내면:
# → 422 Unprocessable Entity (자동)
```

### 5-3. PR Checklist

```markdown
## API Checklist
- [ ] Endpoint naming: /api/v1/{resource}
- [ ] Pydantic models for request/response
- [ ] status_code 명시 (201 for POST, 204 for DELETE)
- [ ] 민감 정보(password) response에 없음
- [ ] Error는 HTTPException 사용
- [ ] OpenAPI docs 확인 (/docs)
```

### 5-4. Manual Review

**리뷰 항목**:
1. API 설계 일관성 (naming, status codes)
2. Pydantic model 적절성
3. 민감 정보 노출 여부
4. Error handling 적절성

**리뷰 주기**: 새 endpoint 추가 시 (PR에서)
```

---

## 6. Progressive Accumulation 전략

### 6-1. 프로젝트 시작 시 (Week 1)

**Mandatory 5개 작성**:
```
PROJECT_STANDARDS/
├── 00_index.md (50 lines) - 초기 버전
├── 01_logging.md (150 lines) - ADR-015
├── 02_error_handling.md (180 lines) - ADR-020, ADR-021
├── 03_configuration.md (120 lines) - ADR-025
├── 04_type_hints.md (160 lines) - ADR-030
├── 05_testing.md (200 lines) - ADR-010, ADR-035
└── 99_common_mistakes.md (100 lines) - 초기 버전 (10개 실수)
```

**작성 우선순위**:
1. 01_logging.md - 모든 코드에 필요
2. 04_type_hints.md - mypy 설정 전 필요
3. 02_error_handling.md - Exception 패턴 통일
4. 05_testing.md - TDD 시작 전 필요
5. 03_configuration.md - 설정 관리 통일

### 6-2. API 개발 시작 (Week 2-3)

**Optional 추가**:
```
PROJECT_STANDARDS/
├── [기존 Mandatory 5개]
├── 07_api.md (200 lines) - NEW! ADR-025, ADR-045
└── 99_common_mistakes.md (150 lines) - 업데이트 (API 실수 추가)
```

**00_index.md 업데이트**:
```markdown
## Optional Standards (1)
- ✅ 07_api.md - FastAPI + OpenAPI (Added 2025-01-20)

## ADR → Standards Mapping
| ADR-025 | FastAPI + OpenAPI | 07_api.md 전체 | 2025-01-20 |
```

### 6-3. DB 연동 시작 (Week 3-4)

**Optional 추가**:
```
PROJECT_STANDARDS/
├── [기존 Mandatory 5개 + 07_api.md]
├── 06_database.md (180 lines) - NEW! ADR-040, ADR-041, ADR-042
└── 99_common_mistakes.md (180 lines) - 업데이트 (DB 실수 추가)
```

### 6-4. 인증 구현 (Week 4-5)

```
PROJECT_STANDARDS/
├── [기존 6개]
├── 08_authentication.md (150 lines) - NEW! ADR-050, ADR-051
└── 99_common_mistakes.md (200 lines) - 최종 (50개 실수)
```

### 6-5. Progressive Accumulation 원칙

**원칙 1: 필요한 시점에 추가**
- ❌ 프로젝트 시작 시 10개 파일 모두 작성
- ✅ Week 1: Mandatory 5개
- ✅ Week 2-3: API 시작하면 07_api.md
- ✅ Week 3-4: DB 시작하면 06_database.md

**원칙 2: 버전 관리**
```bash
# Week 1: Mandatory 5개
git tag standards-v1.0

# Week 2: API 추가
git tag standards-v1.1

# Week 4: DB + Auth 추가
git tag standards-v2.0
```

**원칙 3: 99_common_mistakes.md는 지속 업데이트**
- Week 1: 10개 실수
- Week 2: 20개 (API 실수 추가)
- Week 4: 30개 (DB 실수 추가)
- Month 2: 50개 (최종)

---

## 7. Standards 생명주기 관리

### 7-1. Standards 업데이트 트리거

**Trigger 1: ADR Accepted**
→ 새 Standard 파일 생성 또는 기존 파일에 Section 추가

**Trigger 2: ADR Superseded**
→ Standard 업데이트 (Before/After 표시)

**Trigger 3: 코드 리뷰에서 새로운 패턴 발견**
→ 99_common_mistakes.md 업데이트

**Trigger 4: 버그 발생**
→ Common Mistakes에 추가

### 7-2. ADR Accepted → Standards 생성

**Example**: ADR-055 (Redis caching) 승인

**Step 1**: 09_performance.md 생성
```markdown
# 09. Performance Standards

> **출처**: ADR-055 (Redis caching)
> **업데이트**: 2025-02-01

## 1. Caching Strategy (Line 1-40)
[Redis caching 규칙]

## 2. Cache Keys (Line 41-80)
[Key naming, TTL]

## 3. Cache Invalidation (Line 81-120)
[Invalidation 패턴]

## 4. Common Mistakes (Line 121-160)
[Caching 실수]

## 5. Enforcement (Line 161-200)
[Cache hit rate monitoring]
```

**Step 2**: 00_index.md 업데이트
```markdown
## Optional Standards (6)
- ✅ 09_performance.md - Redis caching (Added 2025-02-01)

## ADR → Standards Mapping
| ADR-055 | Redis caching | 09_performance.md | 2025-02-01 |
```

### 7-3. ADR Superseded → Standards 업데이트

**Example**: ADR-015 (structlog) → ADR-065 (Python logging)

**Step 1**: 01_logging.md 업데이트
```markdown
# 01. Logging Standards

> **출처**: ADR-065 (Python logging + JSON)
> **이전**: ADR-015 (structlog) - Superseded 2025-03-01

## Before/After (Migration Guide)

**Before** (ADR-015):
```python
from structlog import get_logger
logger = get_logger()
logger.info("user_login", user_id=user.id)
```

**After** (ADR-065):
```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)
logger.info("user_login", extra={"user_id": user.id})
```

[나머지 섹션은 ADR-065 기준으로 업데이트]
```

**Step 2**: 00_index.md 업데이트
```markdown
| ADR-065 | Python logging | 01_logging.md 전체 (업데이트) | 2025-03-01 |
| ~~ADR-015~~ | ~~structlog~~ | ~~Superseded by ADR-065~~ | ~~2025-01-15~~ |
```

### 7-4. 새로운 패턴 발견 → 99_common_mistakes.md 업데이트

**Trigger**: 코드 리뷰에서 동일한 실수 3번 발견

**Step 1**: 실수 분석
```
User A: async 함수에서 sync DB 호출 → 블로킹
User B: 동일한 실수
User C: 동일한 실수
→ Common mistake!
```

**Step 2**: 99_common_mistakes.md에 추가
```markdown
# 99. Common Mistakes

## Category: Async/Await

**Mistake 15: async 함수에서 sync DB 호출** (Added 2025-02-15)
```python
❌ Before:
   async def get_user(user_id: int):
       user = session.query(User).filter_by(id=user_id).first()  # Blocking!
       return user

✅ After:
   async def get_user(user_id: int):
       async with async_session() as session:
           result = await session.execute(select(User).filter_by(id=user_id))
           return result.scalar_one_or_none()
```
**Why**: sync DB 호출은 event loop 블로킹
**출처**: 코드 리뷰 3건 (2025-02-10 ~ 2025-02-15)
```

---

## 8. 다음 단계 연결

### 8-1. 문서 흐름에서 Standards의 위치

```
ADR_GUIDE.md
    ↓ 결정 기록
Individual ADR documents
    ↓ 변환 (이 가이드!)
PROJECT_STANDARDS_GUIDE.md (이 문서)
    ↓ 표준 규칙
PROJECT_STANDARDS/ directory
    ↓ 적용
BLUEPRINT_GUIDE.md ← 다음 단계!
    ↓
TASK_BREAKDOWN_GUIDE.md
    ↓
CHECKLIST_GUIDE.md
```

### 8-2. 다음 단계: BLUEPRINT_GUIDE.md

**다음 가이드에서 배울 내용**:
1. ADR + Standards를 사용하여 Blueprint 작성
2. 기능 단위 명세 (30-50 lines per feature)
3. Level 3 구현 힌트 (40 lines 스켈레톤)
4. Blueprint 파일 분리 (500 lines per system)
5. Blueprint → Task 연결

**지금 PROJECT_STANDARDS_GUIDE.md에서 배운 것**:
- ✅ ADR → Standards 변환 절차
- ✅ Mandatory 5개 vs Optional standards
- ✅ Standards 파일 구조 (5개 섹션, Line 범위)
- ✅ Progressive accumulation 전략
- ✅ Standards 생명주기 관리

**Standards가 Blueprint에 어떻게 사용되나**:

**Blueprint 작성 시**:
```markdown
# blueprints/01_auth_system.md

## 2.1 JWT 토큰 생성 (Line 51-100)

**프로젝트 표준 적용**:
- 01_logging.md Line 31-60: Event format
- 02_error_handling.md Line 41-80: TokenGenerationError
- 04_type_hints.md Line 81-120: Pydantic for payload

**구현 힌트** (Level 3 스켈레톤):
```python
# 01_logging.md Line 31-60 적용
from structlog import get_logger
logger = get_logger()

# 04_type_hints.md Line 81-120 적용
from pydantic import BaseModel
class TokenPayload(BaseModel):
    user_id: int
    exp: datetime

def create_token(user_id: int) -> str:
    payload = TokenPayload(user_id=user_id, exp=...)
    secret_key = config.get_secret("JWT_SECRET_KEY")
    token = jwt.encode(payload.dict(), secret_key, algorithm="HS256")
    logger.info("token_generated", user_id=user_id)  # 01_logging.md
    return token
```

→ Blueprint는 Standards를 참조하여 작성됨!
```

**다음 가이드로 이동**: `BLUEPRINT_GUIDE.md`

---

## 부록: Quick Reference

### Standards 파일 템플릿

```markdown
# XX. [Standard Name]

> **출처**: ADR-XXX, ADR-YYY
> **업데이트**: YYYY-MM-DD

## 1. [Core Section 1] (Line 1-40)
**Mandatory**: [필수 import, 기본 패턴]

**Good Examples**:
```python
✅ [예시 코드]
```

**Bad Examples**:
```python
❌ [나쁜 예시]
```

**Forbidden**:
❌ [금지 사항]

**Why**: [이유]

---

## 2. [Core Section 2] (Line 41-80)
[상세 규칙, 고급 패턴]

---

## 3. [Core Section 3] (Line 81-120)
[특수 케이스, 예외 처리]

---

## 4. Common Mistakes (Line 121-160)

**Mistake 1: [실수 제목]**
```python
❌ Before: [나쁜 코드]
✅ After:  [좋은 코드]
```
**Why**: [이유]
**출처**: [ADR 또는 코드 리뷰]

[3-4개 더...]

---

## 5. Enforcement (Line 161-200)

### 5-1. Pre-commit Hook
[설정, 스크립트]

### 5-2. Ruff/Mypy Configuration
[pyproject.toml 설정]

### 5-3. CI Pipeline
[GitHub Actions]

### 5-4. Quality Gates
[Phase 5B 검증]

### 5-5. PR Checklist
[체크리스트 항목]

### 5-6. Manual Review
[리뷰 항목, 주기]
```

### ADR → Standards 체크리스트

ADR을 Standards로 변환할 때:

- [ ] Decision → Sections 1-3 매핑 완료
- [ ] Compliance → Section 5 매핑 완료
- [ ] Consequences (harder) → Section 4 매핑 완료
- [ ] 서술형 → 명령형 변환 완료
- [ ] Good/Bad 예시 각 3개 이상
- [ ] Line 범위 할당 (각 섹션 30-50 lines)
- [ ] 총 길이 150-200 lines
- [ ] Pre-commit hook 추가
- [ ] CI pipeline 추가
- [ ] Quality Gates 연결
- [ ] 00_index.md 업데이트

**모두 ✅면 완성!**

---

**이 가이드 완료!** 다음: `BLUEPRINT_GUIDE.md`
