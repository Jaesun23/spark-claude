# ADR (Architecture Decision Records) 작성 가이드

> **목적**: 아키텍처 결정을 문서화하고 시스템 강제(System Enforcement)로 전환하는 방법을 정의합니다.

---

## 목차

1. [ADR이란 무엇인가](#1-adr이란-무엇인가)
2. [ADR의 5가지 유형](#2-adr의-5가지-유형)
3. [ADR 7개 섹션 템플릿](#3-adr-7개-섹션-템플릿)
4. [좋은 ADR 작성하기](#4-좋은-adr-작성하기)
5. [ADR → Standards 변환 프로세스](#5-adr--standards-변환-프로세스)
6. [ADR 생명주기 관리](#6-adr-생명주기-관리)
7. [다음 단계 연결](#7-다음-단계-연결)

---

## 1. ADR이란 무엇인가

### 1-1. 정의

**Architecture Decision Record (ADR)**는 프로젝트의 중요한 아키텍처 결정을 문서화하는 짧은 문서입니다.

**핵심 개념**:
- **단일 결정**: 하나의 ADR = 하나의 아키텍처 결정
- **결정 + 근거**: "무엇을" + "왜" 선택했는지
- **불변성**: 한번 작성된 ADR은 수정하지 않음 (Superseded로 대체)
- **시스템 강제**: Compliance 섹션을 통해 결정이 실제로 지켜지도록 강제

### 1-2. Jason의 방법론에서 ADR의 위치

```
[Human-Driven Stages - SPARK Cannot Help]
Architecture Decisions → ADR Documents → Blueprint
    ↑
Jason + 1호/2호 conversations
    ↓
----------------------------------------------------------← SPARK STARTS HERE
[SPARK-Enabled Stages - Systematic Enforcement]
Standards → Task Breakdown → Checklists → Implementation
```

**ADR의 역할**:
- ❌ ADR은 SPARK가 자동으로 생성할 수 없음 (너무 많은 맥락, 판단 필요)
- ✅ ADR은 사람(Jason + 1호/2호)의 협업으로 작성
- ✅ ADR은 Standards 문서의 입력이 됨
- ✅ ADR의 Compliance는 Quality Gates로 연결됨

### 1-3. 왜 ADR이 필요한가?

**Problem**: "가이드라인"은 AI가 무시하거나 잊어버림

```markdown
❌ "좋은 로깅 관행을 따르세요"
❌ "표준 도구를 사용하세요"
❌ "print()를 사용하지 마세요"
```

**Solution**: ADR + Compliance = 시스템 강제

```python
# ADR-015: structlog 사용 (Decision)
# Compliance:
if "print(" in code:
    BLOCK "❌ print() 금지. structlog 사용."

if "import logging" in code:
    BLOCK "❌ logging 모듈 금지. structlog 사용."
```

**핵심 인사이트**:
- ADR = 결정 문서 (What + Why)
- Standards = 실행 규칙 (How + Enforcement)
- Quality Gates = 자동 검증 (Blocking + Validation)

---

## 2. ADR의 5가지 유형

ADR은 결정의 성격에 따라 5가지 유형으로 분류됩니다.

### 2-1. Type 1: Structure (구조 결정)

**정의**: 시스템 조직 방식, 아키텍처 패턴에 대한 결정

**예시**:
- Clean Architecture 사용
- Microservices vs Monolith
- Domain-Driven Design 적용
- Layer 분리 규칙 (Domain → Infrastructure 의존 금지)

**생성되는 Standards**:
- `10_architecture.md` - 전체 구조 규칙
- `11_dependencies.md` - 의존성 규칙

**Compliance 전략**:
- ✅ **Automated**: import-linter로 의존성 방향 검증
- ✅ **Automated**: pre-commit hook으로 위반 차단
- ⚠️ **Semi-automated**: Architecture review checklist

**예시 ADR**:
```markdown
# ADR-001: Clean Architecture 적용

## Context
현재 코드가 Infrastructure(DB, API)와 Business Logic이 섞여 있어:
- 테스트가 어려움 (DB 없이 비즈니스 로직 테스트 불가)
- 변경이 어려움 (PostgreSQL → MongoDB 전환 시 비즈니스 코드 수정)
- 재사용이 어려움 (CLI, API 동시 제공 불가)

## Decision
Clean Architecture를 적용하여 계층을 분리:
- Domain: 비즈니스 규칙 (외부 의존 없음)
- Use Case: 애플리케이션 로직
- Interface Adapters: API, CLI
- Infrastructure: DB, 외부 서비스

**의존성 규칙**: 외부 계층 → 내부 계층 (Domain은 아무것도 의존 안 함)

## Consequences
✅ **Easier**:
- 비즈니스 로직 단위 테스트 (Mock 불필요)
- Infrastructure 교체 (PostgreSQL → MongoDB)
- 다중 Interface (CLI + API 동시 제공)

❌ **Harder**:
- 초기 설정 복잡도 증가
- 파일 개수 증가
- 팀 교육 필요

## Compliance
1. **Automated**: import-linter 설정
   ```toml
   [[tool.importlinter.contracts]]
   name = "Domain은 Infrastructure를 import 금지"
   type = "forbidden"
   source_modules = ["src.domain"]
   forbidden_modules = ["src.infrastructure"]
   ```
2. **Automated**: pre-commit hook에서 import-linter 실행
3. **Semi-automated**: PR 리뷰 체크리스트 (architecture 섹션)

## Notes
- 마이그레이션 가이드: `docs/clean-architecture-migration.md`
- 팀 교육: Week 2 세션 예정
- 참고: Uncle Bob's Clean Architecture (2017)
```

### 2-2. Type 2: Nonfunctional Characteristics (품질 속성 결정)

**정의**: 성능, 확장성, 보안, 테스트 커버리지 등 품질 요구사항에 대한 결정

**예시**:
- 테스트 커버리지 95% 이상 필수
- API 응답 시간 200ms 이하
- 모든 API는 rate limiting 적용
- 모든 에러는 구조화된 로깅

**생성되는 Standards**:
- `05_testing.md` Section 4 - Coverage requirements
- `09_performance.md` - Performance benchmarks
- `08_security.md` - Security requirements

**Compliance 전략**:
- ✅ **Automated**: pytest-cov가 95% 미만이면 CI 실패
- ✅ **Automated**: Quality Gates가 커버리지 체크 후 blocking
- ⚠️ **Semi-automated**: Performance test in CI

**예시 ADR**:
```markdown
# ADR-010: 테스트 커버리지 95% 이상 필수

## Context
과거 프로젝트 5개 실패 분석 결과:
- 테스트 없는 코드 → 리팩토링 시 regression
- 커버리지 60% → 핵심 로직 35% 미테스트
- 배포 후 버그 발견 → 고객 신뢰 손실

## Decision
**모든 Python 코드는 95% 이상 테스트 커버리지 필수.**

- Unit test: 95% 이상
- Integration test: 85% 이상
- 커버리지 미달 시 CI 실패 (merge 불가)

**예외**:
- `__main__.py` (CLI entry point)
- Type stub files (`.pyi`)
- 마이그레이션 스크립트 (일회성)

## Consequences
✅ **Easier**:
- 리팩토링 안전성 (regression 조기 발견)
- 버그 조기 발견 (배포 전)
- 코드 품질 향상 (테스트 가능한 설계)

❌ **Harder**:
- 개발 초기 속도 느림 (테스트 작성 시간)
- 복잡한 로직 테스트 작성 어려움
- Mock/Fixture 설정 복잡도

## Compliance
1. **Automated**: pytest.ini 설정
   ```ini
   [pytest]
   addopts = --cov=src --cov-fail-under=95
   ```
2. **Automated**: CI pipeline에서 pytest-cov 실행
   ```yaml
   - name: Test
     run: pytest --cov=src --cov-fail-under=95
   ```
3. **Automated**: Quality Gates (Phase 5B)
   ```python
   coverage_result = subprocess.run(["pytest", "--cov=src", ...])
   if coverage < 95:
       BLOCK "❌ Coverage 95% 미만. merge 불가."
   ```
4. **Semi-automated**: PR 리뷰 체크리스트

## Notes
- Coverage 측정: pytest-cov (branch coverage)
- 예외 신청: Architecture review 필요
- 마이그레이션: 기존 코드 4주 내 95% 달성
```

### 2-3. Type 3: Dependency (의존성 결정)

**정의**: 외부 라이브러리, 프레임워크, 서비스 선택에 대한 결정

**예시**:
- structlog 사용 (logging 대신)
- FastAPI 사용 (Flask 대신)
- PostgreSQL 사용 (MySQL 대신)
- Pydantic for validation

**생성되는 Standards**:
- `01_logging.md` - structlog 사용법
- `07_api.md` - FastAPI 패턴
- `06_database.md` - PostgreSQL 패턴

**Compliance 전략**:
- ✅ **Automated**: pre-commit hook으로 금지된 import 차단
- ✅ **Automated**: ruff로 특정 패턴 검사
- ⚠️ **Manual**: 코드 리뷰

**예시 ADR**:
```markdown
# ADR-015: structlog 사용 (표준 logging 모듈 금지)

## Context
현재 print() 디버깅과 표준 logging 모듈 혼용:
- print() → 프로덕션에 남아있음
- logging.info(f"User {id}") → 문자열 포맷, 파싱 불가
- ELK stack 연동 불가 (key-value 형식 필요)
- Request ID correlation 불가

## Decision
**모든 로깅은 structlog 사용, print()와 logging 모듈 금지.**

```python
from structlog import get_logger
logger = get_logger()

# Good
logger.info("user_login", user_id=user.id, ip=request.ip)
logger.error("token_expired", token_id=token.jti, user_id=user.id)

# Forbidden
print(f"User {user.id} logged in")  # ❌
logging.info("User login")           # ❌
```

**설정**:
- JSON output (프로덕션)
- Pretty printing (개발 환경)
- Request ID auto-binding

## Consequences
✅ **Easier**:
- 로그 분석 (ELK stack 연동)
- 프로덕션 디버깅 (Request ID로 추적)
- 성능 측정 (duration 자동 기록)

❌ **Harder**:
- 초기 설정 복잡도
- 팀 교육 필요 (structlog API)
- Migration 작업 (기존 print() 제거)

## Compliance
1. **Automated**: pre-commit hook
   ```python
   # .pre-commit-config.yaml에서 실행
   if "print(" in python_code:
       return "❌ print() 금지. logger.info() 사용."
   if "import logging" in python_code:
       return "❌ logging 모듈 금지. structlog 사용."
   ```
2. **Automated**: ruff rule T201 (print 검출)
   ```toml
   [tool.ruff]
   select = ["T201"]  # Detect print()
   ```
3. **Automated**: mypy plugin (structlog type stubs)
4. **Semi-automated**: PR 체크리스트

## Notes
- Migration guide: `docs/logging-migration.md`
- structlog docs: https://www.structlog.org/
- 팀 교육: Week 3 세션
- 예외: 스크립트의 사용자 출력은 print() 허용 (main 함수만)
```

### 2-4. Type 4: Interface (인터페이스 결정)

**정의**: API 설계, 모듈 간 계약, 외부 연동 방식에 대한 결정

**예시**:
- RESTful API with OpenAPI
- GraphQL vs REST
- gRPC for microservices
- Event-driven architecture (Kafka)

**생성되는 Standards**:
- `07_api.md` - API endpoint 패턴
- `12_events.md` - Event schema

**Compliance 전략**:
- ✅ **Automated**: OpenAPI schema validation
- ✅ **Automated**: Pydantic model validation
- ⚠️ **Semi-automated**: API contract testing

**예시 ADR**:
```markdown
# ADR-025: RESTful API with FastAPI + OpenAPI

## Context
여러 클라이언트(Web, Mobile, CLI)에서 동일한 기능 사용:
- API 필요성: Web/Mobile에서 호출
- 명확한 계약: Frontend/Backend 팀 분리
- 문서 자동화: OpenAPI spec으로 자동 생성

## Decision
**FastAPI로 RESTful JSON API 구축, OpenAPI 자동 생성.**

**API 규칙**:
1. **Endpoint 네이밍**: `/api/v1/{resource}`
   - Collection: `GET /api/v1/users`
   - Item: `GET /api/v1/users/{user_id}`
   - Action: `POST /api/v1/users/{user_id}/activate`

2. **HTTP 메서드**:
   - GET: 조회
   - POST: 생성
   - PATCH: 부분 수정
   - DELETE: 삭제

3. **Status codes**:
   - 200: 성공 (GET, PATCH)
   - 201: 생성 성공 (POST)
   - 204: 삭제 성공 (DELETE)
   - 400: Client error
   - 401: Unauthorized
   - 404: Not found
   - 500: Server error

4. **Request/Response**: Pydantic models (자동 validation)

## Consequences
✅ **Easier**:
- Frontend/Backend 독립 개발 (OpenAPI contract)
- 자동 문서 (`/docs` endpoint)
- Type safety (Pydantic validation)

❌ **Harder**:
- FastAPI 학습 곡선
- Pydantic model 작성 시간

## Compliance
1. **Automated**: Pydantic validation (런타임)
   ```python
   class UserCreateRequest(BaseModel):
       email: EmailStr
       password: str = Field(min_length=8)

   # 자동 검증, 400 error 리턴
   ```
2. **Automated**: OpenAPI schema validation (CI)
   ```bash
   # OpenAPI spec 변경 감지
   openapi-diff old.json new.json
   ```
3. **Semi-automated**: Contract testing (Pact)
4. **Manual**: API design review

## Notes
- FastAPI docs: https://fastapi.tiangolo.com/
- OpenAPI 3.1 spec
- 버전 관리: `/api/v1`, `/api/v2` (breaking changes 시)
```

### 2-5. Type 5: Construction Technique (구현 기법 결정)

**정의**: 코드 작성 방식, 패턴, 기법에 대한 결정

**예시**:
- Pydantic for all DTOs
- async/await for I/O operations
- Repository pattern for database
- Factory pattern for object creation

**생성되는 Standards**:
- `04_type_hints.md` Section 3 - Pydantic usage
- `06_database.md` Section 2 - Repository pattern
- `09_performance.md` - Async patterns

**Compliance 전략**:
- ✅ **Automated**: mypy strict mode로 type 검증
- ⚠️ **Semi-automated**: Code review checklist
- ⚠️ **Manual**: Architecture review

**예시 ADR**:
```markdown
# ADR-030: Pydantic for All DTOs and Configuration

## Context
현재 데이터 전달 객체(DTO)와 설정 관리 문제:
- dict 남용 → 타입 안정성 없음
- JSON 파싱 시 validation 없음
- API request/response 구조 불명확
- 설정 파일 오류 런타임에 발견

## Decision
**모든 DTO와 설정은 Pydantic BaseModel 사용.**

**적용 범위**:
1. API request/response models
2. Database models (SQLAlchemy + Pydantic hybrid)
3. Configuration (pydantic-settings)
4. Event schemas
5. 외부 API 응답 파싱

**금지**:
- ❌ dict로 데이터 전달 (type unsafe)
- ❌ dataclass (validation 없음)
- ❌ 수동 JSON validation

## Consequences
✅ **Easier**:
- 자동 validation (런타임 type checking)
- JSON ↔ Python 자동 변환
- OpenAPI schema 자동 생성
- 설정 오류 즉시 발견

❌ **Harder**:
- Pydantic 학습 필요
- Model 작성 시간 증가
- 복잡한 validation logic 작성

## Compliance
1. **Automated**: mypy strict mode
   ```toml
   [tool.mypy]
   strict = true
   plugins = ["pydantic.mypy"]
   ```
2. **Automated**: ruff rule (dict 타입 힌트 누락 감지)
3. **Semi-automated**: PR 체크리스트
   - [ ] 모든 DTO가 Pydantic model인가?
   - [ ] Validation logic이 model에 있는가?
4. **Manual**: Architecture review (복잡한 경우)

## Notes
- Pydantic v2 사용 (성능 개선)
- Migration: 기존 dict → Pydantic (2주 계획)
- 성능: Pydantic v2는 dataclass보다 빠름
```

---

## 3. ADR 7개 섹션 템플릿

Jason의 ADR 템플릿은 Michael Nygard의 기본 템플릿에 **Compliance**와 **Notes** 섹션을 추가한 확장 버전입니다.

### 3-1. 기본 구조

```markdown
# ADR-XXX: [간결한 제목]

## 1. Title
ADR 번호와 명확한 제목

## 2. Date
작성일 (YYYY-MM-DD)

## 3. Status
Proposed | Accepted | Rejected | Deprecated | Superseded

## 4. Context
이 결정을 내리게 된 배경, 문제, 제약사항

## 5. Decision
우리가 선택한 것, 구체적인 규칙/패턴

## 6. Consequences
이 결정으로 인해 더 쉬워지는 것 / 더 어려워지는 것

## 7. Compliance (Jason's Extension)
이 결정이 실제로 지켜지도록 하는 검증 메커니즘
- Automated: 자동 검증 (CI, pre-commit, Quality Gates)
- Semi-automated: 반자동 검증 (체크리스트, contract testing)
- Manual: 수동 검증 (architecture review, 코드 리뷰)

## 8. Notes (Jason's Extension)
추가 참고사항, 마이그레이션 가이드, 관련 문서
```

### 3-2. 각 섹션 작성 가이드

#### Section 1-2: Title + Date

**Format**:
```markdown
# ADR-015: Use structlog for Structured Logging

**Date**: 2025-01-15
**Status**: Accepted
```

**Guidelines**:
- 번호: 3자리 (ADR-001, ADR-015, ADR-123)
- 제목: 명령문 형태 ("Use X", "Apply Y", "Adopt Z")
- 간결하게 (5-10 단어)

#### Section 3: Status

**5가지 상태**:

1. **Proposed**: 제안됨, 아직 결정 안 됨
   - Standards 생성 ❌
   - 참고용으로만 보관

2. **Accepted**: 승인됨, 적용 시작
   - Standards 생성 ✅
   - Compliance 메커니즘 적용

3. **Rejected**: 거부됨
   - Standards 생성 ❌
   - 왜 거부했는지 Notes에 기록

4. **Deprecated**: 더 이상 사용 안 함
   - Standards에 "Deprecated" 표시
   - 마이그레이션 가이드 제공

5. **Superseded**: 다른 ADR로 대체됨
   - `Superseded by ADR-045` 표시
   - Standards 업데이트 (Before/After 표시)

#### Section 4: Context

**무엇을 작성하나**:
- 현재 문제점
- 제약사항 (기술, 비용, 시간)
- 대안 검토 결과

**Good Example**:
```markdown
## Context
현재 로깅 문제점:
1. print() 디버깅이 프로덕션에 남아있음
2. logging.info(f"...") → 문자열 포맷, ELK 파싱 불가
3. Request ID correlation 불가 → 분산 추적 어려움

제약사항:
- ELK stack 이미 구축됨 (JSON 로그 필요)
- 기존 코드 500+ print() 존재 (마이그레이션 필요)

검토한 대안:
1. 표준 logging + formatter → ELK 연동 가능하나 Request ID binding 어려움
2. structlog → ELK 연동 + Request ID binding 모두 가능
3. loguru → 좋지만 structlog보다 생태계 작음
```

**Bad Example** (너무 짧음):
```markdown
## Context
로깅이 필요함.
```

#### Section 5: Decision

**무엇을 작성하나**:
- 구체적인 선택 (라이브러리 이름, 버전, 패턴)
- 적용 범위
- 금지 사항

**Good Example**:
```markdown
## Decision
**모든 로깅은 structlog 사용, print()와 logging 모듈 금지.**

설정:
- JSON output (프로덕션)
- Pretty printing (개발)
- Auto-binding: request_id, user_id

패턴:
```python
from structlog import get_logger
logger = get_logger()
logger.info("event_name", key=value)
```

금지:
- ❌ print()
- ❌ import logging
- ❌ logger.info(f"...") (문자열 포맷)
```

**Bad Example** (추상적):
```markdown
## Decision
좋은 로깅 도구를 사용한다.
```

#### Section 6: Consequences

**무엇을 작성하나**:
- ✅ 더 쉬워지는 것 (benefits)
- ❌ 더 어려워지는 것 (trade-offs)

**Good Example**:
```markdown
## Consequences

✅ **Easier**:
- 로그 분석: ELK stack에서 `user_id:123` 필터링
- 프로덕션 디버깅: Request ID로 전체 흐름 추적
- 성능 측정: duration 자동 기록

❌ **Harder**:
- 초기 설정: structlog 설정 파일 작성
- 팀 교육: 1-2주 학습 곡선
- 마이그레이션: 500+ print() 제거 (4주 소요 예상)
```

**Key Point**: 장점만 나열하지 말고, trade-off를 정직하게 기록!

#### Section 7: Compliance (핵심 섹션!)

**무엇을 작성하나**:
- 이 결정이 실제로 지켜지도록 하는 **시스템 강제 메커니즘**
- 3가지 수준: Automated, Semi-automated, Manual

**Compliance 3가지 수준**:

1. **Automated** (자동 검증, 차단):
   - pre-commit hook으로 print() 차단
   - CI에서 ruff/mypy 실행 (실패 시 merge 불가)
   - Quality Gates (Phase 5B) blocking

2. **Semi-automated** (반자동 검증):
   - PR 체크리스트 (사람이 확인, 도구 지원)
   - Contract testing (Pact)
   - OpenAPI schema diff

3. **Manual** (수동 검증):
   - Architecture review
   - 코드 리뷰 (복잡한 패턴)
   - 주기적 감사

**Good Example** (3가지 수준 모두 포함):
```markdown
## Compliance

1. **Automated**: pre-commit hook
   ```python
   # .pre-commit-config.yaml
   - repo: local
     hooks:
       - id: no-print
         name: Detect print()
         entry: python scripts/check_no_print.py
         language: python
         types: [python]

   # scripts/check_no_print.py
   if "print(" in content:
       sys.exit("❌ print() 금지. logger.info() 사용.")
   ```

2. **Automated**: ruff T201
   ```toml
   [tool.ruff]
   select = ["T201"]  # Detect print()
   ```

3. **Automated**: Quality Gates (Phase 5B)
   ```python
   # ~/.claude/hooks/spark_quality_gates.py
   ruff_result = subprocess.run(["ruff", "check", "."])
   if ruff_result.returncode != 0:
       return "🚫 Quality gates FAILED"
   ```

4. **Semi-automated**: PR 체크리스트
   - [ ] 모든 print()가 logger.info()로 변경되었나?
   - [ ] structlog import가 사용되었나?

5. **Manual**: 코드 리뷰
   - 복잡한 로깅 로직 리뷰
   - 민감 정보 로깅 여부 확인
```

**Bad Example** (검증 방법 없음):
```markdown
## Compliance
개발자들이 이 규칙을 따를 것으로 기대한다.
```

**Key Insight**:
- **Compliance 섹션 = ADR과 Quality Gates의 연결고리**
- Compliance에 명시된 것 = Standards로 변환됨
- Compliance 없는 ADR = 그냥 "가이드라인" (무시됨)

#### Section 8: Notes

**무엇을 작성하나**:
- 마이그레이션 가이드 링크
- 관련 문서, 참고자료
- 팀 교육 계획
- 예외 사항

**Example**:
```markdown
## Notes

**마이그레이션**:
- 가이드: `docs/logging-migration.md`
- 일정: 4주 (Week 3-6)
- 우선순위: 프로덕션 코드 먼저, 테스트 코드 나중

**교육**:
- Week 3: structlog 기본 세션 (2시간)
- Week 4: ELK 연동 세션 (1시간)

**참고자료**:
- structlog docs: https://www.structlog.org/
- ELK integration: `docs/elk-integration.md`

**예외**:
- CLI 스크립트의 사용자 출력: print() 허용
- 마이그레이션 스크립트: 일회성이므로 예외
```

---

## 4. 좋은 ADR 작성하기

### 4-1. Good ADR의 특징

✅ **구체적**: "좋은 로깅" ❌ → "structlog 사용" ✅
✅ **검증 가능**: Compliance 섹션에 자동 검증 방법
✅ **실행 가능**: Standards로 변환 가능
✅ **정직함**: Trade-off를 숨기지 않음

### 4-2. Bad ADR 예시

```markdown
# ADR-010: Use Good Coding Practices

**Date**: 2025-01-10
**Status**: Accepted

## Context
We need to write good code.

## Decision
We will follow good coding practices.

## Consequences
Code will be better.

## Compliance
Developers will follow the guidelines.
```

**문제점**:
1. ❌ "Good coding practices" - 추상적, 측정 불가
2. ❌ Context가 문제를 설명하지 않음
3. ❌ Decision이 구체적 액션이 아님
4. ❌ Consequences가 trade-off를 보여주지 않음
5. ❌ Compliance에 검증 방법 없음 (그냥 "기대")

**Result**: Standards로 변환 불가능, 그냥 무시됨

### 4-3. Good ADR 예시

```markdown
# ADR-020: Enforce Domain → Infrastructure Dependency Rule

**Date**: 2025-01-20
**Status**: Accepted

## Context
현재 Domain 계층이 Infrastructure를 직접 import:
```python
# src/domain/user.py (문제!)
from src.infrastructure.database import UserRepository  # ❌

class User:
    def save(self):
        repo = UserRepository()
        repo.save(self)
```

문제점:
- Domain 로직 테스트 시 DB 필요 (느림, 복잡)
- Infrastructure 변경 시 Domain 수정 (결합도 높음)
- Clean Architecture 위반

## Decision
**Domain은 Infrastructure를 절대 import 금지.**

대신:
1. Domain에서 Interface(Protocol) 정의
2. Infrastructure에서 Interface 구현
3. Use Case에서 의존성 주입

```python
# src/domain/user.py (수정)
from typing import Protocol

class UserRepositoryProtocol(Protocol):
    def save(self, user: "User") -> None: ...

class User:
    def save(self, repo: UserRepositoryProtocol):
        repo.save(self)

# src/infrastructure/database/user_repository.py
from src.domain.user import UserRepositoryProtocol

class UserRepository(UserRepositoryProtocol):
    def save(self, user: User) -> None:
        # DB 저장 로직
```

## Consequences

✅ **Easier**:
- Domain 단위 테스트 (Mock repository 사용)
- Infrastructure 교체 (PostgreSQL → MongoDB)
- 여러 구현 공존 (MemoryRepository, FileRepository)

❌ **Harder**:
- 초기 설정: Protocol 정의, DI 설정
- 파일 개수 증가 (interface + implementation)
- 팀 교육: Protocol, DI 개념

## Compliance

1. **Automated**: import-linter
   ```toml
   # pyproject.toml
   [[tool.importlinter.contracts]]
   name = "Domain은 Infrastructure import 금지"
   type = "forbidden"
   source_modules = ["src.domain"]
   forbidden_modules = ["src.infrastructure"]
   ```

2. **Automated**: pre-commit hook
   ```yaml
   # .pre-commit-config.yaml
   - repo: https://github.com/seddonym/import-linter
     hooks:
       - id: import-linter
   ```

3. **Automated**: CI pipeline
   ```yaml
   # .github/workflows/ci.yml
   - name: Check Dependencies
     run: lint-imports
   ```

4. **Semi-automated**: PR 체크리스트
   - [ ] Domain 코드에 Infrastructure import 없는가?
   - [ ] Protocol이 올바르게 정의되었는가?

5. **Manual**: Architecture review (주 1회)
   - 복잡한 의존성 패턴 검토

## Notes

**마이그레이션**:
- 가이드: `docs/architecture/dependency-injection.md`
- 일정: 6주 (Week 4-9)
- 우선순위: User, Auth 모듈 먼저

**교육**:
- Week 4: Clean Architecture 세션
- Week 5: Protocol과 DI 세션
- Week 6: Hands-on workshop

**참고자료**:
- Uncle Bob's Clean Architecture
- import-linter docs: https://import-linter.readthedocs.io/

**예외 없음**: 모든 Domain 코드에 적용
```

**왜 Good인가**:
1. ✅ Context가 구체적 코드 예시로 문제 설명
2. ✅ Decision이 Before/After 코드로 명확
3. ✅ Consequences가 정직한 trade-off
4. ✅ Compliance에 5가지 검증 메커니즘 (자동 3개, 반자동 1개, 수동 1개)
5. ✅ Notes에 마이그레이션 계획, 교육 일정

**Result**: Standards/10_architecture.md Section 2로 변환 가능!

### 4-4. Compliance 작성 전략

**원칙**: Automated > Semi-automated > Manual 순서로 선호

**Step 1: Automated부터 찾기**
- 이 규칙을 자동으로 검증할 도구가 있나?
  - Linter (ruff, pylint)
  - Type checker (mypy)
  - Import checker (import-linter)
  - Security scanner (bandit)
  - Coverage tool (pytest-cov)

**Step 2: Pre-commit hook 추가**
- 자동 도구를 pre-commit에 연결
- 위반 시 commit 차단

**Step 3: CI pipeline 추가**
- Pre-commit 통과해도 CI에서 재검증
- Merge 전 마지막 방어선

**Step 4: Quality Gates 연결**
- Phase 5B에서 최종 검증
- `spark_quality_gates.py`에서 blocking

**Step 5: Semi-automated 추가**
- 자동화 어려운 부분 → 체크리스트
- PR template에 포함

**Step 6: Manual 최소화**
- 정말 사람 판단 필요한 것만
- 주기적 리뷰 (주 1회, 월 1회)

**예시 적용**:
```markdown
ADR-015: structlog 사용

Compliance:
1. ✅ Automated: ruff T201 (print 검출)
2. ✅ Automated: pre-commit hook (import logging 차단)
3. ✅ Automated: CI (ruff 실행)
4. ✅ Automated: Quality Gates (Phase 5B)
5. ⚠️ Semi-automated: PR 체크리스트 (logger.info 형식 확인)
6. ⚠️ Manual: 민감 정보 로깅 여부 리뷰 (주 1회)

→ 자동 4개, 반자동 1개, 수동 1개 = 균형!
```

---

## 5. ADR → Standards 변환 프로세스

### 5-1. 변환의 핵심 원칙

**ADR vs Standards 차이**:

| 측면 | ADR | Standards |
|------|-----|-----------|
| 목적 | 결정 기록 | 실행 가이드 |
| 내용 | What + Why | How + Enforcement |
| 형식 | Decision + Context | Rules + Examples |
| 독자 | 의사결정자 | 개발자 (Agent) |
| 변경 | 불변 (Superseded) | 업데이트 가능 |

**변환 원칙**:
1. ADR Decision → Standard Rules
2. ADR Compliance → Standard Enforcement
3. ADR Consequences (harder) → Standard Common Mistakes
4. ADR 예시 코드 → Standard Good/Bad Examples

### 5-2. 변환 Step-by-Step (예시: structlog)

#### Step 1: ADR Decision → Standard Sections

**ADR-015 Decision**:
```markdown
## Decision
모든 로깅은 structlog 사용, print()와 logging 모듈 금지.

패턴:
```python
from structlog import get_logger
logger = get_logger()
logger.info("event_name", key=value)
```

금지:
- print()
- import logging
```

**→ Standards/01_logging.md Section 1, 2**:
```markdown
# 01. Logging Standards

## 1. Import and Setup (Line 1-30)

**Mandatory Import**:
```python
from structlog import get_logger
logger = get_logger()
```

**Forbidden**:
❌ `import logging`
❌ `print()` for debugging

**Enforcement**: pre-commit hook, ruff T201

## 2. Event Format (Line 31-60)

**Pattern**: `logger.info("event_name", key=value)`

**Good Examples**:
✅ `logger.info("user_login", user_id=user.id, ip=request.ip)`

**Bad Examples**:
❌ `logger.info(f"User {user.id} logged in")` - No structure
```

#### Step 2: ADR Compliance → Standard Enforcement

**ADR-015 Compliance**:
```markdown
## Compliance
1. Automated: pre-commit hook (print 차단)
2. Automated: ruff T201
3. Semi-automated: PR 체크리스트
```

**→ Standards/01_logging.md Section 5**:
```markdown
## 5. Enforcement (Line 121-150)

**Pre-commit Hook**:
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: no-print
      entry: python scripts/check_no_print.py
```

**Ruff Configuration**:
```toml
[tool.ruff]
select = ["T201"]  # Detect print()
```

**Quality Gates** (Phase 5B):
```python
ruff_result = subprocess.run(["ruff", "check", "."])
if ruff_result.returncode != 0:
    BLOCK
```

**PR Checklist**:
- [ ] print() 없음
- [ ] logger.info("event", key=value) 형식
```

#### Step 3: ADR Consequences → Standard Common Mistakes

**ADR-015 Consequences (Harder)**:
```markdown
❌ Harder:
- 초기 설정 복잡도
- 팀 교육 필요
- Migration 작업
```

**→ Standards/01_logging.md Section 4**:
```markdown
## 4. Common Mistakes (Line 91-120)

**Mistake 1: 문자열 포맷 사용**
❌ Before: `logger.info(f"Processing {count} items")`
✅ After: `logger.info("processing_items", count=count)`

**Why**: ELK stack은 key-value 필요

**Mistake 2: 민감 정보 로깅**
❌ `logger.info("auth", password=password)`
✅ `logger.info("auth", user_id=user.id)`

**Why**: 보안 이슈, GDPR 위반
```

#### Step 4: 완성된 Standard 파일

**Standards/01_logging.md** (150 lines):
```markdown
# 01. Logging Standards

> **출처**: ADR-015 (structlog 사용)
> **업데이트**: 2025-01-15

## 1. Import and Setup (Line 1-30)

**Mandatory Import**:
```python
from structlog import get_logger
logger = get_logger()
```

**Configuration** (프로덕션):
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

**Configuration** (개발):
```python
structlog.configure(
    processors=[
        structlog.dev.ConsoleRenderer(),
    ],
)
```

**Forbidden**:
❌ `import logging` - 표준 logging 모듈 금지
❌ `print()` - 디버깅용 print 금지

**Enforcement**: pre-commit hook, ruff T201

---

## 2. Event Format (Line 31-60)

**Pattern**: `logger.info("event_name", key=value)`

**Event Naming**:
- snake_case 사용
- 동사_명사 형태 (`user_login`, `token_generated`)
- 과거형 아님 (`user_logged_in` ❌)

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

---

## 3. Context Binding (Line 61-90)

**Request ID Auto-binding**:
```python
from structlog import get_logger, BoundLogger

# FastAPI middleware
@app.middleware("http")
async def bind_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    logger = get_logger().bind(request_id=request_id)
    # ... call_next
```

**User Context Binding**:
```python
logger = get_logger().bind(user_id=current_user.id)
logger.info("order_created", order_id=order.id)
# Output: {"event": "order_created", "order_id": 123, "user_id": 456, ...}
```

---

## 4. Common Mistakes (Line 91-120)

**Mistake 1: 문자열 포맷 사용**
```python
❌ Before: logger.info(f"Processing {count} items")
✅ After:  logger.info("processing_items", count=count)
```
**Why**: ELK stack은 key-value 필요, 문자열 파싱 불가

**Mistake 2: 민감 정보 로깅**
```python
❌ logger.info("auth", password=password)
✅ logger.info("auth", user_id=user.id)
```
**Why**: 보안 이슈, GDPR 위반

**Mistake 3: Exception 로깅 시 context 누락**
```python
❌ logger.error("Error occurred")
✅ logger.error("token_generation_failed", user_id=user.id, exc_info=True)
```
**Why**: 디버깅을 위한 context 필요

---

## 5. Enforcement (Line 121-150)

**Pre-commit Hook**:
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: no-print
      name: Detect print()
      entry: python scripts/check_no_print.py
      language: python
      types: [python]
```

**Ruff Configuration**:
```toml
[tool.ruff]
select = ["T201"]  # Detect print()
```

**Quality Gates** (Phase 5B):
```python
# ~/.claude/hooks/spark_quality_gates.py
ruff_result = subprocess.run(["ruff", "check", "."])
if ruff_result.returncode != 0:
    return "🚫 Quality gates FAILED"
```

**PR Checklist**:
- [ ] print() 없음
- [ ] logger.info("event", key=value) 형식
- [ ] 민감 정보(password, token) 로깅 없음
- [ ] Exception 로깅 시 exc_info=True 포함

**Manual Review** (주 1회):
- 민감 정보 로깅 여부
- Event naming convention 준수 여부
```

### 5-3. 변환 예시 2: FastAPI (부분 변환)

**ADR-025: FastAPI with OpenAPI** → **Standards/07_api.md**

#### ADR Decision (일부):
```markdown
## Decision
FastAPI로 RESTful JSON API 구축.

Endpoint 네이밍:
- Collection: GET /api/v1/users
- Item: GET /api/v1/users/{user_id}
```

#### Standards 변환:
```markdown
# 07. API Standards

> **출처**: ADR-025 (FastAPI with OpenAPI)

## 1. Endpoint Naming (Line 1-40)

**Pattern**: `/api/v1/{resource}`

**Collection endpoints**:
```python
@app.get("/api/v1/users")
async def list_users() -> List[UserResponse]:
    ...

@app.post("/api/v1/users")
async def create_user(user: UserCreateRequest) -> UserResponse:
    ...
```

**Item endpoints**:
```python
@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: int) -> UserResponse:
    ...

@app.patch("/api/v1/users/{user_id}")
async def update_user(user_id: int, update: UserUpdateRequest) -> UserResponse:
    ...
```

**Action endpoints** (non-CRUD):
```python
@app.post("/api/v1/users/{user_id}/activate")
async def activate_user(user_id: int) -> UserResponse:
    ...
```

**Forbidden**:
❌ `/users` - API prefix 누락
❌ `/api/user` - 단수형 (복수형 사용!)
❌ `/api/v1/users/activate/{user_id}` - Action이 앞에 (뒤에!)
```

### 5-4. 변환 예시 3: Test Coverage (부분 업데이트)

**ADR-010: 95% Coverage** → **Standards/05_testing.md Section 4**

#### ADR Decision:
```markdown
## Decision
모든 Python 코드는 95% 이상 테스트 커버리지 필수.
- Unit test: 95% 이상
- Integration test: 85% 이상
```

#### Standards 변환 (기존 파일에 Section 추가):
```markdown
# 05. Testing Standards

> **출처**: ADR-005 (pytest), ADR-010 (95% coverage)

## 1. Test Framework (Line 1-40)
[기존 내용]

## 2. Test Structure (Line 41-80)
[기존 내용]

## 3. Fixtures (Line 81-120)
[기존 내용]

## 4. Coverage Requirements (Line 121-160) ← NEW!

> **출처**: ADR-010

**Mandatory Coverage**:
- Unit tests: **95% 이상**
- Integration tests: **85% 이상**

**Configuration**:
```ini
# pytest.ini
[pytest]
addopts = --cov=src --cov-fail-under=95 --cov-report=html
```

**CI Enforcement**:
```yaml
# .github/workflows/ci.yml
- name: Test with Coverage
  run: pytest --cov=src --cov-fail-under=95
```

**예외**:
- `__main__.py` (entry point)
- `*.pyi` (type stubs)
- Migration scripts (일회성)

**Coverage 측정**:
```bash
pytest --cov=src --cov-report=term-missing
```

**Enforcement**:
1. CI 실패 시 merge 불가
2. Quality Gates (Phase 5B) blocking
3. PR 체크리스트
```

---

## 6. ADR 생명주기 관리

### 6-1. Status 변경 흐름

```
Proposed → Accepted → Deprecated/Superseded
    ↓           ↓              ↓
  보관        Standards    Standards
  (참고)        생성          업데이트
```

### 6-2. Proposed → Accepted

**Trigger**: 팀 회의에서 승인

**Actions**:
1. ADR status 변경: `Proposed` → `Accepted`
2. Standards 생성:
   - ADR Decision → Standards rules
   - ADR Compliance → Standards enforcement
3. `00_index.md` 업데이트:
   ```markdown
   ## Standards 출처
   - 01_logging.md ← ADR-015
   - 05_testing.md Section 4 ← ADR-010
   ```

**Example**:
```markdown
# ADR-015 변경
- **Status**: Proposed ~~Accepted~~
+ **Status**: Accepted
  **Date Accepted**: 2025-01-15
```

### 6-3. Accepted → Deprecated

**Trigger**: 더 이상 사용하지 않기로 결정

**Actions**:
1. ADR status 변경: `Accepted` → `Deprecated`
2. Standards에 Deprecated 표시:
   ```markdown
   # 01. Logging Standards

   > **⚠️ DEPRECATED**: 이 표준은 deprecated됩니다.
   > **Deprecated Date**: 2025-06-01
   > **Reason**: ADR-015 deprecated (ADR-045로 대체)
   > **Migration**: docs/migration/logging-v2.md
   ```
3. 마이그레이션 가이드 작성

**Example**:
```markdown
# ADR-015 변경 (structlog → 다른 도구로 변경)
  **Status**: Accepted ~~Deprecated~~
+ **Status**: Deprecated
+ **Deprecated Date**: 2025-06-01
+ **Reason**: Performance issues in production
```

**Standards 변경**:
```markdown
# 01. Logging Standards

> **⚠️ DEPRECATED**: 2025-06-01
> **출처**: ADR-015 (Deprecated)
> **대체**: ADR-045 (New logging solution)
> **마이그레이션**: docs/migration/logging-v2.md

[기존 내용은 남겨둠 - 레거시 코드 참고용]
```

### 6-4. Accepted → Superseded

**Trigger**: 더 나은 방법으로 대체

**Actions**:
1. 새 ADR 작성 (ADR-045)
2. 구 ADR status 변경: `Accepted` → `Superseded by ADR-045`
3. Standards 업데이트:
   - Before/After 섹션 추가
   - 마이그레이션 가이드 추가

**Example**:

**ADR-015 변경**:
```markdown
# ADR-015: Use structlog for Logging

- **Status**: Accepted ~~Superseded by ADR-045~~
+ **Status**: Superseded by ADR-045
+ **Superseded Date**: 2025-06-01
```

**ADR-045 작성** (새 ADR):
```markdown
# ADR-045: Use Python logging with JSON Formatter

**Status**: Accepted
**Date**: 2025-06-01
**Supersedes**: ADR-015

## Context
structlog 성능 문제 (대용량 로그 처리 시 병목):
- 초당 10K+ events → 50% CPU 사용
- GIL 경합 (Python logging은 C로 구현)

## Decision
표준 logging 모듈 + JSON formatter 사용.
[...]
```

**Standards 업데이트** (01_logging.md):
```markdown
# 01. Logging Standards

> **출처**: ADR-045 (Python logging + JSON)
> **이전**: ADR-015 (structlog) - Superseded 2025-06-01

## Before/After (Migration Guide)

**Before** (ADR-015, structlog):
```python
from structlog import get_logger
logger = get_logger()
logger.info("user_login", user_id=user.id)
```

**After** (ADR-045, logging + JSON):
```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)
logger.info("user_login", extra={"user_id": user.id})
```

**마이그레이션**: docs/migration/structlog-to-logging.md

---

## 1. Import and Setup (Line 1-30) ← UPDATED!

**Mandatory Import**:
```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)
```

[나머지 업데이트된 내용...]
```

### 6-5. Rejected ADR

**Trigger**: 제안이 거부됨

**Actions**:
1. ADR status 변경: `Proposed` → `Rejected`
2. Notes에 거부 이유 상세 기록
3. Standards 생성 ❌ (거부되었으므로)

**Example**:
```markdown
# ADR-018: Use loguru for Logging

**Status**: Rejected
**Date Proposed**: 2025-01-10
**Date Rejected**: 2025-01-15

## Context
structlog 대안으로 loguru 검토.

## Decision
loguru 사용 제안.

## Why Rejected
1. 생태계가 작음 (structlog 대비)
2. 팀이 이미 structlog 학습 완료
3. 마이그레이션 비용이 이득보다 큼

## Notes
- 논의 내용: `docs/meetings/2025-01-15-logging.md`
- 대신 ADR-015 (structlog) 승인
```

---

## 7. 다음 단계 연결

### 7-1. 문서 흐름에서 ADR의 위치

```
ADR_GUIDE.md (이 문서)
    ↓ 작성 방법 학습
Individual ADR documents (ADR-001, ADR-015, ...)
    ↓ Accepted ADRs
PROJECT_STANDARDS_GUIDE.md ← 다음 단계!
    ↓ 변환 방법 학습
PROJECT_STANDARDS/ directory (01_logging.md, 07_api.md, ...)
    ↓ 적용
BLUEPRINT_GUIDE.md
    ↓
TASK_BREAKDOWN_GUIDE.md
    ↓
CHECKLIST_GUIDE.md
```

### 7-2. 다음 단계: PROJECT_STANDARDS_GUIDE.md

**다음 가이드에서 배울 내용**:
1. Standards 파일 구조 (5개 섹션, Line 범위)
2. Mandatory 5 standards vs Optional standards
3. 파일 분리 전략 (150-200 lines per file)
4. Progressive accumulation (프로젝트 초기 vs 중후반)
5. ADR → Standards 상세 변환 절차
6. Standards → Blueprint 연결

**지금 ADR_GUIDE.md에서 배운 것**:
- ✅ ADR 5가지 유형
- ✅ ADR 7개 섹션 (특히 Compliance!)
- ✅ Good vs Bad ADR
- ✅ ADR → Standards 변환 개념

**다음 가이드로 이동**: `PROJECT_STANDARDS_GUIDE.md`

---

## 부록: Quick Reference

### ADR 템플릿 (Copy-Paste)

```markdown
# ADR-XXX: [Title]

**Date**: YYYY-MM-DD
**Status**: Proposed

## Context
[현재 문제점, 제약사항, 검토한 대안]

## Decision
[구체적인 선택, 적용 범위, 금지 사항]

## Consequences
✅ **Easier**:
- [이점 1]
- [이점 2]

❌ **Harder**:
- [Trade-off 1]
- [Trade-off 2]

## Compliance
1. **Automated**: [도구, hook, CI]
2. **Semi-automated**: [체크리스트, contract test]
3. **Manual**: [리뷰, 감사]

## Notes
[마이그레이션 가이드, 교육 계획, 참고자료, 예외사항]
```

### Compliance 체크리스트

작성한 ADR의 Compliance 섹션을 검증:

- [ ] Automated 검증이 최소 1개 이상 있는가?
- [ ] Pre-commit hook에 연결되어 있는가?
- [ ] CI pipeline에서 검증하는가?
- [ ] Quality Gates (Phase 5B)와 연결되어 있는가?
- [ ] Semi-automated 체크리스트가 구체적인가?
- [ ] Manual 검증의 주기가 명시되어 있는가?

**모두 ✅면 좋은 ADR!**

---

**이 가이드 완료!** 다음: `PROJECT_STANDARDS_GUIDE.md`
