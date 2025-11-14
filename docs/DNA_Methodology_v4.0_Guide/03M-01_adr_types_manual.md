# Stage 3 Manual: ADR의 5가지 유형 상세 설명

> **목적**: ADR 5가지 유형의 상세 설명과 완전한 예시
> **버전**: v3.0 (2025-11-13, Stage 3 분리)
> **소요 시간**: 참고용 (Guide로 기본 작성 가능, Manual로 품질 향상)

---

## 📚 이 문서에 대해

**관계**:
- **Guide** (`03G-00_adr_guide.md`): ADR 기본 작성 방법
- **이 Manual**: 5가지 유형 상세 설명 + 완전한 예시 ADR
- **Manual 2** (`03M-02_adr_to_standards_manual.md`): ADR→Standards 변환 프로세스
- **Cases** (`03E-01_adr_examples_cases.md`): 실전 프로젝트 사례

**이 문서의 역할**:
- Guide의 섹션 2를 상세히 설명
- 각 유형별 완전한 예시 ADR 제공
- Compliance 전략 포함
- 실전 작성 팁 제공

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

### 2-6. 구현방법에서 ADR로 연결

구현방법 단계의 **4단계 (기술 옵션 탐색)**과 **5단계 (통합 설계)** 결과가 ADR의 입력이 됩니다.

이 섹션에서는 **[02-1_IMPLEMENTATION_CASES.md](./02-1_IMPLEMENTATION_CASES.md)**의 3가지 사례에서 핵심 ADR을 추출하여, 구체적인 변환 과정을 보여줍니다.

---

#### 📋 사례별 ADR 구성

**사례 1: 문서 자동생성** (결정론적 시스템)
- ADR-001: Milvus 벡터 DB 선정 (온프레미스 요구사항)
- ADR-002: Human-in-the-loop 승인 프로세스

**사례 2: AI 외부 메모리** (확률론적 시스템) - 🔥 충돌 해결!
- ADR-002: Kafka 기반 비동기식 데이터 수집 (충돌 패턴 해결)
- ADR-003: 멀티 테넌시 RLS 격리 전략

**사례 3: 채팅 애플리케이션** (실시간 시스템)
- ADR-001: WebSocket 기반 실시간 메시지 전송

---

### 사례 1: 문서 자동생성 (결정론적 시스템)

#### 배경: Layer 2 NFR 프로파일 (핵심정의에서)
```
L2-Q1 (핵심 품질): A (100% 정확성 최우선)
L2-Q2 (규모 특성): A (B2B - 10개 엔터프라이즈 고객사)
L2-Q3 (데이터 노출): A (절대 격리 - 온프레미스/VPC 필수)
L2-Q4 (데이터 최신성): C (배치 - 일 1회 업데이트)

충돌 패턴: ❌ 없음
```

#### ADR-001: Milvus 벡터 DB 선정 (온프레미스 배포)

**구현방법 4단계 → ADR 변환**

```markdown
[구현방법 문서에서 - 4단계: 기술 옵션 탐색]

**속성 요구사항**:
- 정확성: 100% (실패 = 치명적)
- 규모: 10개 고객사 (고객당 100만 문서)
- 데이터 격리: 절대 격리 (온프레미스/VPC)
- 동시 사용자: 10명

**제약 조건**:
- 온프레미스 배포 필수 (SaaS 벡터 DB 불가)
- GPU 리소스 없음 (CPU만)
- Python 생태계 선호

**옵션 1: Milvus (Self-hosted)**
- 장점: 온프레미스 배포 가능, CPU 지원, Python SDK
- 단점: 인프라 관리 부담
- NFR 충족: ✅ 모두 충족
- 비용: 인프라 $300/월

**옵션 2: Pinecone/Weaviate (SaaS)**
- 장점: 관리 편리
- 단점: ❌ 데이터 외부 노출 (온프레미스 불가)
- NFR 충족: ❌ 데이터 격리 미충족

**옵션 3: pgvector (PostgreSQL 확장)**
- 장점: 인프라 단순 (기존 PostgreSQL 활용)
- 단점: 성능 제한 (100만+ 문서 시)
- NFR 충족: ⚠️ 규모 이슈

**권장안: Milvus (Self-hosted)**
- 온프레미스 요구사항 충족
- 규모 지원 (수백만 문서)
```

↓ **변환** ↓

```markdown
# ADR-001: Milvus 벡터 DB 선정 (온프레미스 배포)

**Date**: 2025-01-10
**Status**: Accepted

## Context

법률 문서 자동생성 시스템은 과거 판례 검색을 위해 벡터 DB가 필요합니다.

**비기능 요구사항**:
- 정확성: 100% (검색 실패 = 잘못된 법률 문서 생성 = 치명적)
- 규모: 10개 고객사 (고객당 100만 문서)
- 데이터 격리: **절대 격리** (고객 데이터 외부 노출 금지)
- 동시 사용자: 10명 (B2B)

**제약 조건**:
- **온프레미스 배포 필수**: 금융/법률 규제로 SaaS 벡터 DB 사용 불가
- GPU 리소스 없음: CPU 기반 임베딩 및 검색
- Python 생태계: FastAPI + LangChain 스택

**고려된 옵션**:
1. Milvus (Self-hosted)
2. Pinecone/Weaviate (SaaS)
3. pgvector (PostgreSQL 확장)

## Decision

**Milvus 벡터 DB를 온프레미스 환경에 Self-hosted로 배포합니다.**

**배포 구성**:
- Milvus 2.3+ (Standalone mode)
- CPU 기반 벡터 검색 (GPU 불필요)
- MinIO for object storage
- etcd for metadata
- Docker Compose 배포

**선택 근거**:
- ✅ 온프레미스 배포 가능 (SaaS 아님)
- ✅ 규모 지원 (1천만+ 문서 검증됨)
- ✅ CPU 기반 검색 지원
- ✅ Python SDK + LangChain 통합
- ✅ 검증된 기술 (Airbnb, Nvidia 사용)

## Consequences

✅ **Easier**:
- 데이터 격리: 고객 VPC 내 완전 격리
- 규모 확장: 1천만+ 문서 처리 가능
- 통합: LangChain VectorStore 인터페이스

❌ **Harder**:
- 인프라 관리: Docker, MinIO, etcd 운영 부담
- 모니터링: Prometheus + Grafana 설정 필요
- 백업/복구: 수동 프로세스 필요
- 비용: 인프라 $300/월 (SaaS 대비 유사)

## Compliance

1. **Automated**: Docker Compose health check
   ```yaml
   # docker-compose.yml
   milvus:
     image: milvusdb/milvus:v2.3.0
     healthcheck:
       test: ["CMD", "curl", "-f", "http://localhost:9091/healthz"]
   ```

2. **Automated**: CI에서 Milvus 버전 검증
   ```python
   # tests/test_vector_db.py
   def test_milvus_version():
       assert milvus.__version__ >= "2.3.0"
   ```

3. **Semi-automated**: PR 체크리스트
   - [ ] 벡터 검색 코드가 Milvus SDK 사용하는가?
   - [ ] Pinecone/Weaviate 등 SaaS 벡터 DB 사용 금지

4. **Manual**: 분기별 인프라 리뷰
   - 백업/복구 프로세스 검증
   - 성능 모니터링 (latency, throughput)

## Notes

**배포 가이드**: `docs/deployment/milvus-setup.md`
**백업 전략**: 일 1회 MinIO 스냅샷
**모니터링**: Prometheus + Grafana dashboard
**참고자료**: https://milvus.io/docs

**예외 없음**: 모든 벡터 검색은 Milvus 사용
```

---

#### ADR-002: Human-in-the-loop 승인 프로세스

**구현방법 4단계 → ADR 변환**

```markdown
[구현방법 문서에서 - 4단계: 기술 옵션 탐색]

**속성 요구사항**:
- 정확성: 100% (법률 문서 오류 = 소송 리스크)
- 비용: 사람 검토 vs 완전 자동화 트레이드오프
- 규모: B2B (일 100건)

**제약 조건**:
- 법률 전문가 인건비 높음
- AI 100% 신뢰 불가 (Hallucination)

**옵션 1: Human-in-the-loop (사람 승인)**
- 장점: 100% 정확성 보장
- 단점: 비용 $50/건, 지연 4시간
- NFR 충족: ✅ 정확성 충족

**옵션 2: 완전 자동화 (사람 승인 없음)**
- 장점: 비용 $5/건, 지연 5분
- 단점: ❌ Hallucination 리스크
- NFR 충족: ❌ 정확성 미충족

**권장안: Human-in-the-loop**
- 정확성 > 비용/속도
- 법률 리스크 회피
```

↓ **변환** ↓

```markdown
# ADR-002: Human-in-the-loop 승인 프로세스

**Date**: 2025-01-11
**Status**: Accepted

## Context

AI가 생성한 법률 문서는 Hallucination 가능성이 있어 100% 신뢰할 수 없습니다.

**문제**:
- AI Hallucination: 존재하지 않는 판례 인용 가능
- 법률 리스크: 잘못된 문서 → 소송 패소 → 고객 손실
- 규제 요구사항: 법률 전문가 검토 필수 (일부 국가)

**제약 조건**:
- 법률 전문가 인건비: $100/시간
- B2B 규모: 일 100건
- 허용 지연: 최대 24시간

**고려된 옵션**:
1. Human-in-the-loop (전문가 승인 필수)
2. 완전 자동화 (승인 없음)

## Decision

**모든 AI 생성 문서는 법률 전문가의 승인을 필수로 합니다.**

**프로세스**:
1. AI가 문서 초안 생성 (5분)
2. 전문가 검토 대기열에 추가
3. 법률 전문가가 검토 및 수정 (평균 30분)
4. 승인 시 고객에게 전달
5. 거부 시 AI 재생성 + 재검토

**승인 기준**:
- 인용 판례 실존 여부 확인
- 법률 논리 일관성 검증
- 오타/문법 오류 수정

**선택 근거**:
- ✅ 100% 정확성 보장 (전문가 검증)
- ✅ 법률 리스크 회피 (소송 패소 방지)
- ✅ 규제 준수 (일부 국가 법률 요구사항)
- ❌ 비용: $50/건 (전문가 30분 = $50)
- ❌ 지연: 평균 4시간 (검토 대기 + 검토)

**Trade-off 승인**: B2B 고객은 24시간 이내 전달 허용, 비용은 고객사가 부담

## Consequences

✅ **Easier**:
- 100% 정확성 보장 (전문가 검증)
- 법률 리스크 최소화
- 고객 신뢰 증대

❌ **Harder**:
- 비용: $50/건 (완전 자동화 시 $5/건)
- 지연: 평균 4시간 (완전 자동화 시 5분)
- 운영: 전문가 스케줄 관리, 대기열 처리

## Compliance

1. **Automated**: 승인 없는 문서 전달 차단
   ```python
   # src/domain/document.py
   class Document:
       status: Literal["draft", "pending_review", "approved", "rejected"]

       def deliver_to_customer(self):
           if self.status != "approved":
               raise ValueError("❌ 승인되지 않은 문서는 전달 불가")
   ```

2. **Automated**: CI에서 승인 로직 테스트
   ```python
   # tests/test_document_approval.py
   def test_unapproved_document_cannot_be_delivered():
       doc = Document(status="draft")
       with pytest.raises(ValueError, match="승인되지 않은 문서"):
           doc.deliver_to_customer()
   ```

3. **Semi-automated**: PR 체크리스트
   - [ ] 모든 고객 전달 코드에 approval check 있는가?
   - [ ] 승인 우회 경로가 없는가?

4. **Manual**: 월 1회 승인 프로세스 감사
   - 승인 없이 전달된 문서 확인
   - 평균 검토 시간 모니터링

## Notes

**승인 대기열 구현**: `docs/approval-queue.md`
**전문가 가이드**: `docs/reviewer-guide.md`
**평균 검토 시간**: 30분 (목표: 20분)

**예외 없음**: 모든 문서는 승인 필수 (테스트 환경 제외)
```

---

### 사례 2: AI 외부 메모리 (확률론적 시스템) - 🔥 충돌 해결!

#### 배경: Layer 2 NFR 프로파일 + 충돌 패턴

```
L2-Q1 (핵심 품질): B (가장 빠름 - p99 < 500ms)
L2-Q2 (규모 특성): C (API - 수천 테넌트)
L2-Q3 (데이터 노출): B (암호화 - 멀티 테넌트 SaaS)
L2-Q4 (데이터 최신성): A (즉시 반영 - 수 초 이내)

🔥 충돌 패턴: L2-Q1 (속도) + L2-Q4 (즉시성) = 동기식 불가능!
→ 트레이드오프: "최종일관성(수 초 지연) 수용"
```

#### ADR-002: Kafka 기반 비동기식 데이터 수집 (충돌 해결)

**구현방법 4단계 → ADR 변환** (🔥 충돌 해결 중점!)

```markdown
[구현방법 문서에서 - 4단계: 기술 옵션 탐색]

**🔥 충돌 패턴 발견!**

**문제**: L2-Q1 (p99 < 500ms) + L2-Q4 (즉시 반영)

**동기식 API 시간 분석**:
1. 데이터 수신 (10ms)
2. 청킹 (50ms)
3. 임베딩 모델 호출 (OpenAI API, 200-400ms) 💥
4. 벡터 DB 저장 (50ms)
5. 200 OK 응답
총 시간: 310-510ms → p99 < 500ms **불가능**! ❌

**속성 요구사항**:
- API 응답: p99 < 500ms
- 데이터 최신성: 수 초 이내 (즉시)
- 규모: 수천 테넌트

**제약 조건**:
- 임베딩 외부 API 지연 통제 불가
- 배치 처리는 "즉시성" 미충족

**옵션 1: Kafka + 비동기 Workers ✅**
- 장점: API < 50ms (202 Accepted), 충돌 해결!
- 단점: 최종일관성 (수 초 지연)
- NFR 충족: ✅ 속도 충족, ⚠️ "즉시"를 "수 초"로 완화
- 비용: $800/월

**옵션 2: 동기식 처리 (충돌 미해결)**
- 장점: 진짜 즉시 반영
- 단점: ❌ p99 > 500ms (NFR 위반)
- NFR 충족: ❌ 속도 미충족

**권장안: Kafka + 비동기 Workers**
- 충돌 해결: 속도 + 즉시성 → 최종일관성으로 완화
- 대가: "즉시"를 "수 초"로 트레이드오프 (비즈니스 승인 필요)
```

↓ **변환** ↓

```markdown
# ADR-002: Kafka 기반 비동기식 데이터 수집 (충돌 패턴 해결)

**Date**: 2025-01-12
**Status**: Accepted

## Context

AI 외부 메모리 시스템은 사용자 데이터를 수집하여 벡터 DB에 저장합니다.

**🔥 충돌 패턴 발견!**

**Layer 2 NFR 충돌**:
- L2-Q1: B (가장 빠름 - p99 < 500ms)
- L2-Q4: A (즉시 반영 - 수 초 이내)
→ 동기식으로 양립 불가능!

**문제 분석** (동기식 API):
```
POST /api/v1/data (동기식)
├─ 1. 데이터 수신 (10ms)
├─ 2. 청킹 (50ms)
├─ 3. 임베딩 모델 호출 (200-400ms) 💥
│   └─ OpenAI API 외부 호출 (지연 통제 불가)
├─ 4. 벡터 DB 저장 (50ms)
└─ 5. 200 OK 응답

총 시간: 310-510ms
→ p99 < 500ms 불가능! ❌
```

**제약 조건**:
- 임베딩 API 지연: 200-400ms (외부 서비스, 통제 불가)
- 규모: 수천 테넌트 (초당 100+ 요청)
- 예산: 월 $1000 이내

**고려된 옵션**:
1. Kafka + 비동기 Workers (충돌 해결)
2. 동기식 처리 (충돌 미해결)

## Decision

**Kafka 기반 비동기 아키텍처를 채택하여 충돌 패턴을 해결합니다.**

**아키텍처**:
```
Client
  ↓ POST /api/v1/data
API (FastAPI)
  ↓ 202 Accepted (< 50ms) ✅
  ↓ Produce message
Kafka Topic: "data-ingestion"
  ↓ Consume
Worker Pool (3-5 workers)
  ↓ 청킹 + 임베딩 + 저장 (수 초)
Vector DB
```

**프로세스**:
1. API가 데이터 수신 (10ms)
2. Kafka에 메시지 produce (20ms)
3. **202 Accepted 즉시 응답** (< 50ms) ✅
4. Worker가 비동기 처리:
   - 청킹 (50ms)
   - 임베딩 (200-400ms)
   - 벡터 DB 저장 (50ms)
5. 총 처리 시간: 2-5초 (최종일관성)

**선택 근거**:
- ✅ 충돌 해결: 속도 (< 50ms) + 즉시성 (수 초) 양립
- ✅ NFR 충족: p99 < 50ms (목표 500ms 대비 10배 빠름!)
- ✅ 규모 확장: Worker 수평 확장 가능
- ❌ 대가: **최종일관성** (Eventually Consistent, 2-5초 지연)

**Trade-off 승인**:
- "즉시 반영"을 "수 초 이내 반영"으로 완화
- 비즈니스 승인: B2B SaaS 고객은 수 초 지연 허용

## Consequences

✅ **Easier**:
- **충돌 해결**: 속도 + 즉시성 양립 가능 (최종일관성으로)
- API 응답 속도: p99 < 50ms (목표 대비 10배 빠름)
- 수평 확장: Worker 추가로 처리량 증가
- 장애 격리: Worker 실패해도 API는 정상 응답
- 재시도: Kafka가 메시지 보존, Worker 재시도 가능

❌ **Harder**:
- **최종일관성**: 데이터 저장까지 2-5초 지연
- 인프라 복잡도: Kafka, Zookeeper, Worker 관리
- 디버깅: 비동기 처리 추적 어려움
- 비용: Kafka + Workers = $800/월 (동기식 대비 2배)

**최종일관성 시나리오**:
```
t=0초:   사용자가 데이터 업로드, API 202 Accepted
t=2-5초: Worker가 처리 완료, 벡터 DB 저장
t=5초:   사용자가 검색 시도
         → 2-5초 전 데이터는 검색 안 됨 (지연)
```

## Compliance

1. **Automated**: API 응답 시간 모니터링
   ```python
   # src/api/middleware.py
   @app.middleware("http")
   async def monitor_response_time(request, call_next):
       start = time.time()
       response = await call_next(request)
       duration = time.time() - start
       if duration > 0.5:  # 500ms
           logger.error("slow_api", path=request.url.path, duration=duration)
       return response
   ```

2. **Automated**: Kafka produce 실패 시 500 에러
   ```python
   # src/api/routes/data.py
   @app.post("/api/v1/data", status_code=202)
   async def ingest_data(data: DataRequest):
       try:
           await kafka_producer.produce("data-ingestion", data.json())
       except KafkaError:
           raise HTTPException(status_code=500, detail="Kafka produce 실패")
       return {"status": "accepted", "message": "처리 중"}
   ```

3. **Automated**: Worker health check (CI)
   ```python
   # tests/integration/test_kafka_worker.py
   @pytest.mark.integration
   async def test_worker_processes_message():
       # Kafka에 메시지 produce
       await producer.produce("data-ingestion", test_data)
       # 10초 대기 (Worker 처리)
       await asyncio.sleep(10)
       # 벡터 DB 확인
       result = await vector_db.search(test_data.query)
       assert result is not None
   ```

4. **Automated**: Prometheus 메트릭 수집
   ```python
   # Worker에서 메트릭 기록
   processing_duration.observe(duration)  # Worker 처리 시간
   kafka_lag.set(lag)  # Kafka consumer lag
   ```

5. **Semi-automated**: PR 체크리스트
   - [ ] 동기식 처리 코드 없는가? (임베딩 호출 시)
   - [ ] Kafka produce 실패 처리 있는가?
   - [ ] Worker 재시도 로직 구현되었는가?

6. **Manual**: 월 1회 아키텍처 리뷰
   - Kafka lag 모니터링 (< 10초 목표)
   - Worker 장애 빈도 확인
   - 최종일관성 지연 측정 (p99 < 5초)

## Notes

**Kafka 설정**: `docs/kafka-setup.md`
- Topic: data-ingestion (3 partitions, replication=2)
- Consumer group: vector-workers (3-5 workers)

**Worker 구현**: `docs/worker-implementation.md`
- 재시도: 최대 3회 (exponential backoff)
- Dead Letter Queue: 실패한 메시지 보존

**모니터링**:
- Grafana dashboard: API latency, Kafka lag, Worker throughput
- Alert: Kafka lag > 10초, Worker 장애율 > 5%

**최종일관성 완화 계획**:
- Phase 1: 수 초 지연 (현재)
- Phase 2: 밀리초 지연 (임베딩 모델 로컬 배포 시)

**예외 없음**: 모든 데이터 수집은 비동기 처리
```

---

#### ADR-003: 멀티 테넌시 RLS 격리 전략

**구현방법 4단계 → ADR 변환**

```markdown
[구현방법 문서에서 - 4단계: 기술 옵션 탐색]

**속성 요구사항**:
- 데이터 격리: 테넌트 간 완전 격리 (보안 최우선)
- 규모: 수천 테넌트
- 보안: L2-Q3 = B (암호화 - 멀티 테넌트 SaaS)

**제약 조건**:
- 물리적 DB 분리 불가 (수천 DB 운영 불가)
- 예산: 월 $1000 이내

**옵션 1: Row-Level Security (RLS)**
- 장점: DB 단일, 자동 격리, 비용 낮음
- 단점: PostgreSQL 특정, 복잡도
- NFR 충족: ✅ 모두 충족
- 비용: $600/월

**옵션 2: 물리적 DB 분리**
- 장점: 완전 격리
- 단점: ❌ 수천 DB 운영 불가, 비용 폭증
- NFR 충족: ⚠️ 비용/운영 이슈

**권장안: Row-Level Security (RLS)**
- 논리적 격리로 보안 충족
- 단일 DB로 운영 단순화
```

↓ **변환** ↓

```markdown
# ADR-003: 멀티 테넌시 RLS (Row-Level Security) 격리 전략

**Date**: 2025-01-13
**Status**: Accepted

## Context

AI 외부 메모리 SaaS는 수천 개의 테넌트(고객사) 데이터를 저장합니다.

**보안 요구사항**:
- **테넌트 간 완전 격리**: 테넌트 A가 테넌트 B 데이터 접근 절대 불가
- 암호화: 저장 시 암호화 (at-rest), 전송 시 암호화 (in-transit)
- 규모: 수천 테넌트 (현재 50개, 목표 1000+)

**제약 조건**:
- 물리적 DB 분리: 수천 개 DB 운영 불가 (비용, 관리 복잡도)
- 예산: 월 $1000 이내

**고려된 옵션**:
1. Row-Level Security (RLS) - 논리적 격리
2. 물리적 DB 분리 - 테넌트당 DB

## Decision

**PostgreSQL Row-Level Security (RLS)를 사용하여 논리적 테넌트 격리를 구현합니다.**

**아키텍처**:
```sql
-- 모든 테이블에 tenant_id 컬럼
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,  -- 테넌트 식별자
    content TEXT,
    created_at TIMESTAMP
);

-- RLS Policy: 현재 세션의 tenant_id와 일치하는 row만 조회
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON documents
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);

-- API에서 세션 설정
-- SET app.current_tenant_id = '<tenant-uuid>';
```

**프로세스**:
1. API 요청 시 JWT에서 tenant_id 추출
2. PostgreSQL 세션에 `app.current_tenant_id` 설정
3. 모든 쿼리는 자동으로 RLS Policy 적용
   - SELECT: 현재 tenant_id의 row만 반환
   - INSERT: tenant_id 자동 주입
   - UPDATE/DELETE: 현재 tenant_id의 row만 수정/삭제

**선택 근거**:
- ✅ 보안: DB 레벨 격리 (애플리케이션 버그로도 우회 불가)
- ✅ 운영: 단일 DB (수천 DB 관리 불필요)
- ✅ 비용: $600/월 (물리적 분리 대비 10배 절감)
- ✅ 성능: tenant_id 인덱스로 빠른 필터링

## Consequences

✅ **Easier**:
- **자동 격리**: 애플리케이션 코드에서 WHERE 절 누락해도 DB가 차단
- 운영 단순화: 단일 DB 백업/복구/마이그레이션
- 비용 절감: $600/월 (물리적 분리 시 $6000+/월)
- 성능: tenant_id 인덱스로 빠른 쿼리

❌ **Harder**:
- PostgreSQL 종속: RLS는 PostgreSQL 특정 기능
- 복잡도: RLS Policy 설정 및 테스트 필요
- 디버깅: RLS Policy 오류 시 원인 파악 어려움
- 세션 관리: 모든 API 요청마다 `SET app.current_tenant_id` 필수

**보안 시나리오**:
```python
# 공격 시나리오: 애플리케이션 버그로 tenant_id 체크 누락
query = "SELECT * FROM documents"  # WHERE tenant_id = ? 누락! 💥

# RLS가 없다면: 모든 테넌트 데이터 노출 ❌
# RLS가 있다면: 현재 세션의 tenant_id 데이터만 반환 ✅
```

## Compliance

1. **Automated**: RLS Policy 존재 확인 (CI)
   ```python
   # tests/test_rls.py
   def test_all_tables_have_rls():
       tables = ["documents", "embeddings", "metadata"]
       for table in tables:
           result = db.execute(f"SELECT relrowsecurity FROM pg_class WHERE relname='{table}'")
           assert result[0][0] is True, f"{table}에 RLS가 없습니다!"
   ```

2. **Automated**: tenant_id 누락 시 INSERT 실패 테스트
   ```python
   # tests/test_tenant_isolation.py
   def test_insert_without_tenant_id_fails():
       # app.current_tenant_id 설정 안 함
       with pytest.raises(DatabaseError):
           db.execute("INSERT INTO documents (content) VALUES ('test')")
   ```

3. **Automated**: 교차 테넌트 접근 차단 테스트
   ```python
   def test_cannot_access_other_tenant_data():
       # Tenant A로 세션 설정
       db.execute("SET app.current_tenant_id = 'tenant-a-uuid'")
       db.execute("INSERT INTO documents (content) VALUES ('A data')")

       # Tenant B로 세션 전환
       db.execute("SET app.current_tenant_id = 'tenant-b-uuid'")
       result = db.execute("SELECT * FROM documents")

       # Tenant B는 Tenant A 데이터 볼 수 없음
       assert len(result) == 0
   ```

4. **Automated**: Middleware에서 tenant_id 설정 강제
   ```python
   # src/api/middleware.py
   @app.middleware("http")
   async def set_tenant_context(request, call_next):
       tenant_id = extract_tenant_from_jwt(request.headers["Authorization"])
       if not tenant_id:
           raise HTTPException(status_code=401, detail="tenant_id 없음")

       # PostgreSQL 세션에 설정
       async with db.connection() as conn:
           await conn.execute(f"SET app.current_tenant_id = '{tenant_id}'")
           response = await call_next(request)
       return response
   ```

5. **Automated**: 모든 테이블에 tenant_id 컬럼 강제
   ```python
   # migrations/check_tenant_column.py
   def test_all_tables_have_tenant_id():
       tables = get_all_tables()
       for table in tables:
           columns = get_columns(table)
           assert "tenant_id" in columns, f"{table}에 tenant_id 컬럼 없음!"
   ```

6. **Semi-automated**: PR 체크리스트
   - [ ] 새 테이블에 tenant_id 컬럼 추가했는가?
   - [ ] RLS Policy 생성했는가?
   - [ ] 교차 테넌트 접근 테스트 작성했는가?

7. **Manual**: 분기별 보안 감사
   - RLS Policy 누락 테이블 확인
   - tenant_id 인덱스 성능 확인
   - 실제 교차 테넌트 접근 시도 (Penetration Test)

## Notes

**RLS 설정 가이드**: `docs/rls-setup.md`
**마이그레이션**: `docs/migration/add-tenant-id.md`
**성능 최적화**: 모든 테이블에 `(tenant_id, created_at)` 복합 인덱스

**보안 감사 도구**:
```bash
# RLS Policy 누락 테이블 찾기
SELECT relname FROM pg_class WHERE relkind='r' AND relrowsecurity=false;
```

**참고자료**:
- PostgreSQL RLS Docs: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- Multi-tenancy Patterns: https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/

**예외**:
- 테스트 DB: RLS 비활성화 (테스트 편의)
- Admin API: `app.current_tenant_id = 'admin'` (모든 테넌트 조회)
```

---

### 사례 3: 채팅 애플리케이션 (실시간 시스템)

#### 배경: Layer 2 NFR 프로파일
```
L2-Q1 (핵심 품질): B (가장 빠름 - p99 < 500ms)
L2-Q2 (규모 특성): B (B2C - 동시 1000명)
L2-Q3 (데이터 노출): C (공개 - 암호화 불필요)
L2-Q4 (데이터 최신성): A (즉시 반영 - 실시간)

충돌 패턴: ❌ 없음 (속도 + 즉시성 = WebSocket으로 양립)
```

#### ADR-001: WebSocket 기반 실시간 메시지 전송

**구현방법 4단계 → ADR 변환**

```markdown
[구현방법 문서에서 - 4단계: 기술 옵션 탐색]

**속성 요구사항**:
- 메시지 지연 < 500ms (99%ile)
- 동시 접속 1,000명
- 브라우저 호환성
- 방화벽 통과

**제약 조건**:
- Python/Flask 경험 풍부
- WebSocket 경험 없음 (학습 2주)
- 예산: 월 $500

**옵션 1: WebSocket**
- 장점: 양방향, 지연<100ms, 브라우저 표준
- 단점: 학습 2주, Stateful
- NFR 충족: ✅ 모두 충족
- 비용: $450/월

**옵션 2: Long Polling**
- 장점: HTTP 기반, 구현 단순
- 단점: 지연 1-2초, 부하 높음
- NFR 충족: ❌ 지연 미충족
- 비용: $500/월

**옵션 3: gRPC Streaming**
- 장점: 고성능, 지연<100ms
- 단점: 브라우저 제한, 학습 1개월+
- NFR 충족: ⚠️ 브라우저 이슈
- 비용: $400/월

**권장안: WebSocket (Socket.IO)**
- 모든 NFR 충족
- 예산 내
- 검증된 기술
```

↓ **변환** ↓

```markdown
# ADR-001: WebSocket 기반 실시간 메시지 전송

**Date**: 2025-01-08
**Status**: Accepted

## Context

채팅 애플리케이션은 실시간 양방향 통신을 필요로 합니다.

**비기능 요구사항**:
- 메시지 전송 지연 < 500ms (99 percentile)
- 동시 접속 1,000명 지원
- 브라우저 호환성 (웹 + 모바일)
- 방화벽 환경 지원

**제약 조건**:
- 팀: Python/Flask 경험 풍부, WebSocket 경험 없음
- 예산: 월 $500 이내
- 학습 시간: 최대 2주

**고려된 옵션**:
1. WebSocket (Socket.IO)
2. Long Polling
3. gRPC Streaming

## Decision

**WebSocket 기술을 사용하여 실시간 메시지 전송을 구현합니다.**
구체적으로 Flask-SocketIO 라이브러리를 사용합니다.

**아키텍처**:
```
Client (Web/Mobile)
  ↕ WebSocket (persistent connection)
Server (Flask-SocketIO)
  ↕ Redis Pub/Sub (수평 확장)
Server instances (3-5 nodes)
```

**선택 근거**:
- ✅ 모든 NFR 만족 (지연 < 100ms, 1000명 지원)
- ✅ 브라우저 표준 지원 + 자동 fallback (Long Polling)
- ✅ 예산 내 ($450/월 < $500/월)
- ✅ 학습 곡선 수용 가능 (2주)
- ✅ 검증된 기술 (Slack, Discord 사용)

## Consequences

✅ **Easier**:
- 낮은 지연 시간 (< 100ms vs Long Polling 1-2초)
- 효율적 리소스 사용 (persistent connection)
- 브라우저 호환성 자동 처리 (Socket.IO fallback)
- 양방향 통신 (서버 → 클라이언트 push 가능)

❌ **Harder**:
- 학습 필요 (2주 투자)
- **Stateful 서버**: 수평 확장 시 Redis Pub/Sub 필요
- 연결 관리 복잡도 증가 (reconnect, timeout)
- Debugging: WebSocket 트래픽 추적 어려움

## Compliance

1. **Automated**: CI에서 Flask-SocketIO 버전 검증
   ```python
   # tests/test_dependencies.py
   import flask_socketio
   def test_socketio_version():
       assert flask_socketio.__version__ >= "5.3.0"
   ```

2. **Automated**: WebSocket 연결 테스트
   ```python
   # tests/integration/test_websocket.py
   def test_websocket_connection():
       client = socketio.test_client(app)
       assert client.is_connected()
   ```

3. **Semi-automated**: PR 체크리스트
   - [ ] WebSocket 이외의 실시간 통신 방식 사용 여부 확인
   - [ ] Long Polling fallback 구현 확인

4. **Manual**: Architecture review
   - WebSocket vs REST API 경계 설계
   - 수평 확장 전략 (Redis Pub/Sub)

## Notes

**Flask-SocketIO 설정**: `docs/socketio-setup.md`
**수평 확장 가이드**: `docs/redis-pubsub.md`
**성능 벤치마크**: p99 < 80ms (1000 concurrent connections)

**참고자료**:
- Flask-SocketIO: https://flask-socketio.readthedocs.io/
- Socket.IO: https://socket.io/docs/

**예외 없음**: 모든 실시간 통신은 WebSocket 사용
```

---

#### 핵심 포인트: 구현방법 → ADR 변환 정리

**구현방법에서 제공하는 것**:
- ✅ Context: NFR, 제약 조건, 고려된 옵션
- ✅ Decision의 근거: 속성 충족도, 장단점 분석
- ✅ Consequences: 각 옵션의 장단점
- 🔥 **충돌 패턴 분석**: Layer 2 NFR 충돌 발견 및 해결 전략

**ADR에서 추가하는 것**:
- 공식 결정 선언
- **Compliance 메커니즘** (Automated/Semi-automated/Manual)
- Notes (마이그레이션 계획, 성능 벤치마크 등)

**중요**: 구현방법에서 이미 탐색이 완료되었으므로, ADR 작성은 **기록 작업**이 됩니다!

---

#### 🔥 충돌 패턴과 ADR의 관계

**사례 1 (문서 자동생성)**: 충돌 없음 → 간단한 ADR
- 온프레미스 요구사항 → Milvus 선택 (단순)
- 정확성 요구사항 → Human-in-the-loop (단순)

**사례 2 (AI 외부 메모리)**: 충돌 있음! → 복잡한 ADR 💥
- **충돌**: 속도 (p99 < 500ms) + 즉시성 (수 초) = 동기식 불가능
- **해결**: Kafka 비동기 아키텍처 + 최종일관성
- **ADR의 역할**: 충돌 해결 과정을 상세히 문서화
  - Context에 충돌 패턴 명시
  - Decision에 해결 전략 (비동기)
  - Consequences에 트레이드오프 (최종일관성)

**사례 3 (채팅앱)**: 충돌 없음 → 간단한 ADR
- 속도 + 즉시성 = WebSocket으로 양립 가능

**교훈**:
- 충돌이 있는 경우: ADR이 아키텍처를 결정하는 핵심 문서!
- 충돌이 없는 경우: ADR은 단순 기록 문서

---

