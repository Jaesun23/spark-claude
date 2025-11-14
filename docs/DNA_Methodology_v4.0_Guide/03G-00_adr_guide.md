# ADR (Architecture Decision Records) 작성 가이드

> **목적**: Stage 3 - 모든 아키텍처 결정을 문서화하고 시스템 강제(System Enforcement)로 전환
>
> **버전**: v3.0 (2025-11-13, Stage 3 분리)
> - v3.0: Guide/Manual/Cases 분리로 간결성 확보
> - v2.0: Stage 3 범위 명시 (DNA 시스템 vs 도메인 ADR 구분)
> - v1.0: ADR 작성 방법론 확립

---

## 📚 이 가이드의 구성

- **이 문서** (Guide): ADR 작성 방법 + 템플릿
- **상세 설명** (Manual):
  - `03M-01_adr_types_manual.md` - 5가지 유형 상세
  - `03M-02_adr_to_standards_manual.md` - 변환 프로세스
- **실전 사례** (Cases):
  - `IMPLEMENTATION_CASES.md` - 프로젝트 사례
  - `03M-01_adr_types_manual.md` 섹션 2-6 - 구현방법→ADR 변환 사례

---

---

## 📚 이 가이드의 구성

- **이 문서** (Guide): ADR 작성 방법 + 템플릿
- **사례집** (Cases): 실전 ADR 예시 → `IMPLEMENTATION_CASES.md`

---

## 📥 입력 문서 (Stage 2에서 받은 것)

Stage 3를 시작하기 전에 다음 문서를 읽어야 합니다:

#### 1. **`02D-01_tech_stack_decision.md`** (필수)
- 확정된 DNA 시스템 기술 스택
- 확정된 Domain 기술 스택
- **활용**: ADR 작성 대상 파악

#### 2. **`02C-01_layer3_constraints.md`** (필수)
- 외부 제약 조사 결과
- **활용**: 제약에 의한 결정 ADR 작성

#### 3. **`02C-02_conflicts_analysis.md`** (필수)
- 충돌 패턴 및 해결 방안
- **활용**: 충돌 해결 ADR 작성

#### 4. **`02L-01_adr_list.md`** (필수)
- 작성할 ADR 목록 (18-25개)
- 우선순위
- **활용**: ADR 작성 계획

#### 5. **`02S-02_data_schema_v1.md`**, **`02S-03_api_design_v1.md`** (필수)
- 데이터 스키마 및 API 설계
- **활용**: 설계 결정 ADR 작성

#### 6. **Stage 1 모든 산출물** (참고)
- 패밀리, NFR, 핵심 기능
- **활용**: 결정의 근거

---

## 📤 출력 문서 (이 Stage에서 생성해야 할 문서)

### 필수 문서

#### DNA 시스템 ADR (001-099)
**위치**: `docs/adr/dna-systems/`

**DNA 시스템 ADR 목록** (전 프로젝트 공통 요소):

1. **`03A-001_logging_strategy.md`**
   - 로깅 레벨, 포맷, 저장소
   - 예: Structured logging with JSON format

2. **`03A-002_error_handling_standard.md`**
   - 에러 타입, 메시지 형식, 전파 방식
   - 예: Custom exception hierarchy

3. **`03A-003_authentication_method.md`**
   - 인증 방식 (JWT, OAuth, Session 등)
   - 예: JWT with RS256

4. **`03A-004_configuration_management.md`**
   - 환경 변수, 설정 파일 관리
   - 예: Pydantic Settings

5. **`03A-005_database_connection_pooling.md`**
   - Connection pool 설정
   - 예: SQLAlchemy pool size

6. **`03A-006_caching_strategy.md`**
   - 캐시 레이어 설계
   - 예: Redis cache-aside pattern

7. **`03A-007_api_versioning.md`**
   - API 버전 관리 방식
   - 예: URL path versioning (/v1/)

8. **`03A-008_cors_policy.md`**
   - CORS 설정
   - 예: Origin whitelist

9. **`03A-009_rate_limiting.md`**
   - API 요청 제한
   - 예: Token bucket algorithm

10. **`03A-010_monitoring_observability.md`**
    - 모니터링 및 메트릭 수집
    - 예: Prometheus + Grafana

... (총 10-15개)

---

#### Domain ADR (100-999)
**위치**: `docs/adr/domain/`

**Domain ADR 목록** (프로젝트 특화 요소):

##### 외부 제약 관련 (101-105)
1. **`03A-101_kis_api_selection.md`**
   - 한국투자증권 API 선택
   - 대안: 키움증권, eBest
   - 근거: Layer 3 조사 결과

2. **`03A-102_api_rate_limit_handling.md`**
   - 20건/초 제한 대응
   - 해결: Queue + throttling

##### 충돌 해결 관련 (106-110)
3. **`03A-106_hybrid_order_strategy.md`**
   - REST + WebSocket 하이브리드
   - 충돌: 정확성 A + API 제한
   - 해결: WebSocket으로 실시간 체결, REST로 주문

4. **`03A-107_websocket_channel_management.md`**
   - 41개 채널 관리 방식
   - 충돌: 즉시성 A + 채널 제한

##### 기술 스택 관련 (111-115)
5. **`03A-111_fastapi_selection.md`**
   - FastAPI 선택
   - 대안: Django, Flask
   - 근거: 비동기, 성능, 타입 안전성

6. **`03A-112_postgresql_selection.md`**
   - PostgreSQL 선택
   - 대안: MySQL, CockroachDB
   - 근거: ACID, JSON 지원

7. **`03A-113_redis_usage.md`**
   - Redis 사용 범위
   - 캐시 + Queue + Pub/Sub

8. **`03A-114_nextjs_react_selection.md`**
   - Next.js + React 선택
   - 대안: Vue, Svelte
   - 근거: SSR, 생태계

##### 데이터 설계 관련 (116-120)
9. **`03A-116_order_schema_design.md`**
   - 주문 테이블 스키마
   - UUID vs SERIAL, status enum

10. **`03A-117_price_data_storage.md`**
    - 실시간 가격 데이터 저장
    - TimescaleDB vs Redis

11. **`03A-118_user_portfolio_model.md`**
    - 포트폴리오 데이터 모델

##### API 설계 관련 (121-125)
12. **`03A-121_rest_api_design.md`**
    - REST API 엔드포인트 설계
    - RESTful 원칙 적용

13. **`03A-122_websocket_protocol.md`**
    - WebSocket 메시지 프로토콜
    - JSON format, subscription model

14. **`03A-123_error_response_format.md`**
    - API 에러 응답 표준
    - RFC 7807 Problem Details

##### 품질/보안 관련 (126-130)
15. **`03A-126_input_validation.md`**
    - 입력 검증 전략
    - Pydantic models

16. **`03A-127_security_headers.md`**
    - 보안 헤더 설정
    - HSTS, CSP, X-Frame-Options

... (총 15-20개)

---

### ADR 템플릿

모든 ADR은 다음 형식을 따라야 합니다:

```markdown
# ADR-XXX: {Decision Title}

**상태**: Accepted | Proposed | Deprecated
**작성일**: YYYY-MM-DD
**결정자**: {Team/Person}
**태그**: #{dna-systems|domain}, #{tech-stack|data|api|...}

---

## Context (배경)

왜 이 결정이 필요한가?
- 문제 상황
- 제약 조건
- 요구사항

## Decision (결정)

무엇을 선택했는가?
- 선택한 옵션
- 핵심 이유 (간결하게)

## Alternatives (대안)

고려했던 다른 옵션들:
1. **Option A**: ...
   - 장점: ...
   - 단점: ...
   - 거부 이유: ...

2. **Option B**: ...

## Consequences (결과)

이 결정의 영향:
- ✅ 긍정적 영향
- ⚠️ 트레이드오프
- ❌ 부정적 영향
- 🔄 후속 조치 필요

## References (참고)

- Stage 2 문서: {파일명}
- 외부 링크: {URL}
- 관련 ADR: ADR-XXX
```

---

### ADR 작성 우선순위

1. **Phase 1**: 외부 제약 ADR (101-105)
   - 가장 먼저 작성 (변경 불가능)

2. **Phase 2**: 충돌 해결 ADR (106-110)
   - 외부 제약 기반 해결책

3. **Phase 3**: 핵심 기술 스택 ADR (111-115)
   - DNA 시스템 + Domain 주요 기술

4. **Phase 4**: 설계 ADR (116-125)
   - 데이터, API 설계

5. **Phase 5**: DNA 시스템 ADR (001-015)
   - 공통 환경 요소

6. **Phase 6**: 품질/보안 ADR (126-130)
   - 마지막 (다른 ADR 참조)

---

## 🔄 다음 Stage로 전달되는 것

Stage 3 → Stage 4:
- ✅ 완성된 DNA 시스템 ADR (10-15개)
- ✅ 완성된 Domain ADR (15-20개)
- ✅ 모든 아키텍처 결정의 근거 문서화

Stage 4에서는 이를 기반으로:
- DNA 시스템 ADR을 바탕으로 DNA 기본시스템 청사진 작성
- core/ 모듈 설계

---

## 📍 전체 프로세스에서의 위치

```
전체 프로세스:
Stage 0: 아이디어
Stage 1: 패밀리 구분 (01G-00_core_definition_guide.md) ✅
Stage 2: 구조설계 (02G-00_structure_design_guide.md) ✅
Stage 3: ADR 문서화 ← 이 가이드 ⭐
Stage 4-5: DNA 시스템 계획 및 실행
Stage 6-9: Standards → Blueprint → 분해 → 구현
```

---

## Stage 2에서 받은 입력

Stage 2 완료 후 확정된 것:
- ✅ **외부 제약** (API, 규제, 배포환경)
- ✅ **충돌 패턴** (NFR vs 제약)
- ✅ **기술 스택** (언어, DB, 프레임워크)
- ✅ **아키텍처** (구조, 통신, 배포)

Stage 3의 목표:
- 🔄 **DNA 시스템 ADR 작성** (전 프로젝트 공통)
- 🔄 **도메인 ADR 작성** (프로젝트 특화)
- 🔄 **ADR 원칙 적용** (제약도 ADR이다!)

---

## DNA 시스템 ADR vs 도메인 ADR ⭐

> **⚠️ TODO (2025-11-12)**:
> - 1호가 추가 패밀리 발견 및 명확한 구분 방법 확립
> - DNA 시스템 ADR 정의 수정 필요:
>   - 현재: core/ 공통 요소 (잘못된 이해)
>   - 올바름: 패밀리가 정한 시스템 구조에서 나오는 요소
> - 패밀리별 DNA 시스템 요소 목록 추가 예정

---

### ADR 작성 로직 (올바른 흐름)

```
1. 패밀리 결정 (Stage 1)
   ↓
2. 패밀리 → 시스템 구조 자동 결정
   ↓
3. 시스템 구조에서 DNA 시스템 vs 도메인 요소 구분
   - DNA 시스템: 구조가 강제하는 요소
   - 도메인: 프로젝트 특화 요소
   ↓
4. 도메인 특성 검토 → 추가 DNA 시스템 요소 발견
   ↓
5. DNA 시스템 ADR + 도메인 ADR 작성
```

---

### DNA 시스템 ADR (시스템 구조 기반)

**정의**: 패밀리가 결정한 시스템 구조에서 자동으로 도출되는 요소

**예시** (TODO: 패밀리별 상세 목록 추가 예정):
- A-A-A (CRUD/트랜잭션):
  - RDBMS 필수
  - ACID 트랜잭션 필수
  - ORM 필수
  - ...

- A-C-A (실시간 트랜잭션):
  - RDBMS + WebSocket 필수
  - 메시지 큐 필수
  - 캐시 필수
  - ...

**특징**:
- 패밀리가 정하면 자동으로 결정됨
- 도메인과 무관하게 필수
- 시스템 구조의 필수 구성 요소

---

### 도메인 ADR (프로젝트 특화)

**정의**: 특정 프로젝트만의 고유한 결정

**주식 거래 플랫폼 예시**:
- **ADR-101**: 한국투자증권 선택 (vs 키움, 이베스트)
- **ADR-102**: 하이브리드 아키텍처 (WebSocket + Polling)
- **ADR-103**: FastAPI 선택 (Python 프레임워크)
- **ADR-104**: PostgreSQL + Redis (구체적 DB 선택)
- **ADR-105**: Human-in-the-loop 주문 검증

**특징**:
- 프로젝트별 요구사항 반영
- DNA 시스템이 정한 범주 내에서 구체적 선택
- 도메인 제약 조건 반영

---

### ADR 번호 체계

```
DNA 시스템 ADR: 001-099
- 패밀리별 필수 구조 요소
- 시스템 구조가 강제하는 결정

도메인 ADR: 100+
- 프로젝트별로 100번대부터 시작
- DNA 시스템 범주 내 구체적 선택
```

---

## 목차

0. [DNA 시스템 vs 도메인 ADR](#dna-시스템-adr-vs-도메인-adr-) ⭐
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

#### 전체 흐름 (Amazon 3단계 방법론)

```
[Human-Driven Stages - SPARK Cannot Help]

핵심정의 (Core Definition)
  = Amazon 1단계: Identify Use Cases
  = "무엇을" (What) & "왜" (Why)
    ↓
구현방법 (Implementation Approach)
  = Amazon 2단계: Specify Concrete Requirements
  = "어떻게" (How)
  = 5단계 프로세스:
    1. 기능 분해
    2. 속성 질문 ⭐ (성능/품질/환경)
    3. 제약조건 파악
    4. 기술 옵션 탐색 (옵션 3개 비교)
    5. 통합 설계 (아키텍처, Schema, API)
    ↓
ADR (Architecture Decision Records) ← 여기!
  = Amazon 3단계: Select Tools & Infrastructure
  = "무엇을 선택" (Which) & "왜" (Why)
  = 구현방법의 탐색 과정을 **기록**
    ↓
Blueprint (구체적 설계)
  = 최종 구현 청사진

----------------------------------------------------------← SPARK STARTS HERE
[SPARK-Enabled Stages - Systematic Enforcement]
Standards → Task Breakdown → Checklists → Implementation
```

**중요한 순서**:
```
❌ 잘못된 순서: 핵심정의 → ADR (기술 먼저)
   "채팅 필요" → "Redis 쓰자"
   → 왜? (근거 없음)

✅ 올바른 순서: 핵심정의 → 구현방법 → ADR
   "채팅 필요"
   → "500ms, 1000명 동시 접속" (속성 질문)
   → WebSocket vs Long Polling vs gRPC (옵션 비교)
   → "WebSocket 선택" (근거: 모든 NFR 충족)
   → ADR 작성 (결정 기록)
```

**ADR의 역할**:
- ❌ ADR은 SPARK가 자동으로 생성할 수 없음 (너무 많은 맥락, 판단 필요)
- ❌ ADR은 탐색 도구가 아님 (구현방법에서 탐색 완료)
- ✅ ADR은 구현방법의 탐색 결과를 **기록**
- ✅ ADR은 사람(Jason + 1호/2호)의 협업으로 작성
- ✅ ADR은 Standards 문서의 입력이 됨
- ✅ ADR의 Compliance는 Quality Gates로 연결됨

**핵심 원칙** (One Medical의 Double-Diamond):
> 제안(Proposal) → 결정(Decision) → ADR
>
> - 제안 = 구현방법의 기술 옵션 탐색
> - 결정 = 권장안 선택
> - ADR = 최종 결정 기록

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

ADR은 결정의 성격에 따라 5가지 유형으로 분류됩니다:

### 2-1. Type 1: Structure (구조 결정)
**정의**: 시스템 조직 방식, 아키텍처 패턴에 대한 결정

**예시**:
- Clean Architecture 사용
- Microservices vs Monolith
- Domain-Driven Design 적용

**생성되는 Standards**: `10_architecture.md`, `11_dependencies.md`

### 2-2. Type 2: Nonfunctional Characteristics (품질 속성 결정)
**정의**: 성능, 확장성, 보안, 테스트 커버리지 등 품질 요구사항

**예시**:
- 테스트 커버리지 95% 이상 필수
- API 응답 시간 200ms 이하
- 모든 API는 rate limiting 적용

**생성되는 Standards**: `05_testing.md`, `09_performance.md`, `08_security.md`

### 2-3. Type 3: Dependency (의존성 결정)
**정의**: 외부 라이브러리, 프레임워크, 서비스 선택

**예시**:
- structlog 사용 (logging 대신)
- FastAPI 사용 (Flask 대신)
- PostgreSQL 사용 (MySQL 대신)

**생성되는 Standards**: `01_logging.md`, `07_api.md`, `06_database.md`

### 2-4. Type 4: Interface (인터페이스 결정)
**정의**: API 설계, 모듈 간 계약, 외부 연동 방식

**예시**:
- RESTful API with OpenAPI
- GraphQL vs REST
- gRPC for microservices

**생성되는 Standards**: `07_api.md`, `12_events.md`

### 2-5. Type 5: Construction Technique (구현 기법 결정)
**정의**: 코드 작성 방식, 패턴, 기법

**예시**:
- Pydantic for all DTOs
- async/await for I/O operations
- Repository pattern for database

**생성되는 Standards**: `04_type_hints.md`, `06_database.md`, `09_performance.md`

---

**상세 설명**: 각 유형의 완전한 예시 ADR과 Compliance 전략은 `03M-01_adr_types_manual.md` 참고

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

ADR 작성 후 Standards 문서로 변환하여 Quality Gates에 연결합니다.

### 5-1. 변환 원칙

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

### 5-2. 변환 절차

**Step 1**: ADR Decision → Standard Sections
- Decision 내용을 규칙으로 변환
- 패턴, 금지사항을 명시

**Step 2**: ADR Compliance → Standard Enforcement
- Automated: pre-commit hook, CI, Quality Gates
- Semi-automated: PR 체크리스트
- Manual: Architecture review

**Step 3**: ADR Consequences → Standard Common Mistakes
- "Harder" 항목을 실수 사례로 변환
- Before/After 예시 제공

**Step 4**: Standards 파일 완성
- 150줄 내외
- 5개 섹션: Import, Pattern, Context, Mistakes, Enforcement

---

**상세 프로세스**: 완전한 변환 예시(structlog, API, Testing)는 `03M-02_adr_to_standards_manual.md` 참고

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
