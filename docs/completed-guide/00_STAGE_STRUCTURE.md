# DNA 방법론 Stage 구조 기준서

> **목적**: 아이디어부터 구현까지 9개 Stage의 목적, 범위, 산출물을 명확히 정의
>
> **버전**: v1.0 (2025-11-12)
> **기반**: Phase 2 실전 검증 (주식 거래 플랫폼)

---

## 🎯 전체 흐름 개요

```
아이디어 → 실현 가능한 소프트웨어

Stage 1: 패밀리 구분과 핵심기능 파악 (큰 방향)
   ↓
Stage 2: 구조설계 (결정 요소 파악)
   ↓
Stage 3: ADR 문서화 (결정)
   ↓
Stage 4: Bootstrap 계획 (공통 환경)
   ↓
Stage 5: Bootstrap 실행 (DNA 기본시스템)
   ↓
Stage 6: Project Standards (규칙)
   ↓
Stage 7: Project Blueprint (상세 청사진)
   ↓
Stage 8: Task Breakdown (작업 분할)
   ↓
Stage 9: Checklist (작업별 체크리스트)
   ↓
구현 (TDD 9-Step)
```

---

## Stage 1: 패밀리 구분과 핵심기능 파악

### 목적
- **큰 방향과 큰 틀만 잡기**
- 시스템의 본질적 특성 파악
- 필수 기술 방향 자동 결정

### 범위
1. **Part 0: 핵심 기능 파악**
   - 이 시스템의 존재 이유는?
   - 구현 방식이 아닌 비즈니스 목적으로 구분
   - 예: "거래" (O) vs "수동 거래 + 자동 거래" (X)

2. **Layer 1: 아키텍처 패밀리 식별**
   - L1-Q1: 실패 파급력 (A/B/C)
   - L1-Q2: 정보 형태 (A/B/C)
   - L1-Q3: 응답 시점 (A/B/C)
   - 결과: 패밀리 패턴 (예: A-C-A)

3. **Layer 2: NFR 우선순위**
   - L2-Q1: 핵심 품질 (A/B/C)
   - L2-Q2: 규모 (A/B/C)
   - L2-Q3: 데이터 노출 (A/B/C)
   - L2-Q4: 데이터 최신성 (A/B/C)
   - 결과: NFR 프로파일 (예: A-B-B-A)

### 산출물
- **패밀리 결정**: A-C-A (실시간 트랜잭션)
- **핵심 기능**: 거래
- **필수 기술 방향**:
  - ✅ 실시간 통신 필수 (WebSocket 계열)
  - ✅ 숫자 데이터 처리 (시계열 DB 고려)
  - ✅ 정확성 보장 (ACID 또는 강력한 일관성)
- **기술 후보군**:
  - WebSocket, FastAPI, Redis, PostgreSQL 계열

### 제외 사항
- ❌ 구체적 기술 스택 선택 (Stage 2에서)
- ❌ 외부 제약 조사 (Stage 2에서)
- ❌ 아키텍처 다이어그램 (Stage 2에서)

### 관련 문서
- `01_CORE_DEFINITION_GUIDE.md`
- `01-1_CORE_DEFINITION_MANUAL_Part1.md`
- `01-2_CORE_DEFINITION_MANUAL_Part2.md`

---

## Stage 2: 구조설계

### 목적
- **결정해야 할 요소 목록 만들기**
- 내부 자원과 외부 제약/기회 파악
- 구체적 설계 (청사진 수준)

### 범위
1. **Part 1: Layer 3 - 환경 제약 조사**
   - L3-Q1: 기술 스택 제약 (외부 조사 필수!)
     - 외부 API/서비스 비교 (예: 증권사 6개)
     - 법적 규제 조사
     - 개인정보보호 조사
   - L3-Q2: 팀 역량
   - L3-Q3: 배포 환경

2. **Part 2: 충돌 패턴 발견**
   - Layer 2 NFR vs Layer 3 제약 충돌
   - 충돌 매트릭스 작성
   - 트레이드오프 옵션 정리

3. **Part 3: 5단계 구현방법**
   - 1단계: 기능 분해
   - 2단계: 속성 질문 (NFR → 구체적 수치)
   - 3단계: 제약조건
   - 4단계: 기술 옵션 비교
   - 5단계: 통합 설계
     - 아키텍처 다이어그램
     - 데이터 스키마 v1.0
     - API 설계 v1.0

### 산출물
- **제약 목록**:
  - 외부: 한국투자증권 API (20건/초, WebSocket 41개)
  - 내부: 팀 역량, 비용 제약
- **충돌 목록**:
  - #1: 정확성 A vs API 20건/초
  - #2: 즉시성 A vs WebSocket 41개
  - #3: 모의 검증 vs 실전 차이
- **기술 스택 (확정)**:
  - 백엔드: FastAPI (Python)
  - 실시간: WebSocket
  - Queue: Redis + Bull/Celery
  - DB: PostgreSQL
  - 캐시: Redis
  - 프론트: Next.js + React
- **아키텍처 다이어그램**
- **데이터 스키마 v1.0**
- **API 설계 v1.0**
- **ADR 작성 대상 목록** (18개)

### 제외 사항
- ❌ ADR 작성 (Stage 3에서)
- ❌ Bootstrap 설계 (Stage 4에서)
- ❌ 도메인별 상세 설계 (Stage 7에서)

### 관련 문서
- `02_STRUCTURE_DESIGN_GUIDE.md` (새로 작성 예정)
- `02-1_STRUCTURE_DESIGN_MANUAL.md` (새로 작성 예정)

---

## Stage 3: 결정 문서화 (ADR)

### 목적
- **모든 아키텍처 결정을 문서화**
- "왜?"에 대한 근거 명확히
- 시스템 강제(System Enforcement) 기반 마련

### 범위
1. **Bootstrap ADR 작성**
   - 전 프로젝트 공통 요소
   - common/ 모듈 관련 결정
   - 예: 로깅, 에러 처리, 인증, 설정 관리

2. **도메인 ADR 작성**
   - 프로젝트 특화 요소
   - 예: 한국투자증권 선택, 하이브리드 전략, Redis Queue

3. **ADR 작성 원칙**
   - 하나의 ADR = 하나의 결정
   - 너무나 당연한 요소도 모두 작성
   - 제약도 ADR이다 (선택지 1개여도 기록)

### 산출물
- **Bootstrap ADR** (예상 10-15개)
  - 로깅 전략
  - 에러 처리 표준
  - 인증/인가 방식
  - 설정 관리 방법
  - 환경 변수 관리
  - ...

- **도메인 ADR** (예상 15-20개)
  - 외부 제약 관련 (예: 한국투자증권 선택)
  - 충돌 해결 관련 (예: 하이브리드 전략)
  - 기술 스택 관련 (예: FastAPI 선택)
  - 데이터 설계 관련
  - API 설계 관련
  - ...

### 제외 사항
- ❌ 구현 (Stage 5, 9에서)
- ❌ 테스트 코드 (Stage 9에서)

### 관련 문서
- `03_ADR_GUIDE.md`
- `03-1_ADR_MANUAL.md` (작성 예정)

---

## Stage 4: Bootstrap 계획

### 목적
- **전 프로젝트 공통 환경 구축 계획**
- DNA 기본시스템 청사진 작성

### 범위
1. **common/ 모듈 설계**
   - Bootstrap ADR 기반
   - 로깅, 에러, 설정, 인증 등 공통 모듈

2. **DNA 기본시스템 청사진**
   - 디렉토리 구조
   - 공통 모듈 인터페이스
   - 사용 방법

3. **작업 분해**
   - Bootstrap 체크리스트 작성
   - 우선순위 결정

### 산출물
- **DNA 기본시스템 청사진**
- **common/ 모듈 목록**
- **Bootstrap 체크리스트**

### 관련 문서
- `04_BOOTSTRAP_PLAN_GUIDE.md` (작성 예정)

---

## Stage 5: Bootstrap 실행

### 목적
- **DNA 기본시스템 구현**
- 공통 모듈 작동 점검

### 범위
1. **공통 모듈 구현**
   - TDD 9-Step 기반 구현
   - 단위 테스트 95%+ 커버리지

2. **통합 테스트**
   - 공통 모듈 간 통합 확인

3. **문서화**
   - 각 모듈 사용법
   - 예제 코드

### 산출물
- **구현된 common/ 모듈**
- **테스트 코드**
- **모듈 사용 문서**

### 관련 문서
- `05_BOOTSTRAP_EXECUTION_GUIDE.md` (작성 예정)

---

## Stage 6: Project Standards 작성

### 목적
- **프로젝트 종료 시까지 지켜야 할 규칙 정의**
- 일관성 보장

### 범위
1. **코딩 스타일**
   - Naming conventions
   - File organization
   - Code formatting

2. **로깅 표준**
   - Log levels
   - Log format
   - Log rotation

3. **에러 처리 표준**
   - Error types
   - Error messages
   - Error propagation

4. **설정 관리 표준**
   - Environment variables
   - Config files
   - Secrets management

5. **기타 룰**
   - Git commit convention
   - PR 규칙
   - Review 기준

6. **공통 모듈 사용 강제**
   - common/ 모듈 필수 사용
   - 직접 구현 금지 항목

### 산출물
- **PROJECT_STANDARDS.md**

### 관련 문서
- `04_PROJECT_STANDARDS_GUIDE.md` (기존)

---

## Stage 7: Project Blueprint 작성

### 목적
- **초상세 프로젝트 전체 청사진**
- 도메인별 구현 가이드

### 범위
1. **아키텍처 구조**
   - 전체 시스템 아키텍처
   - 레이어별 구조
   - 컴포넌트 다이어그램

2. **도메인 구조**
   - 도메인 모델
   - 도메인별 경계
   - 도메인 간 관계

3. **전체 시스템 다이어그램**
   - 시스템 컨텍스트
   - 컨테이너 다이어그램
   - 컴포넌트 다이어그램
   - 시퀀스 다이어그램

4. **도메인별 다이어그램**
   - 각 도메인의 상세 설계
   - 데이터 흐름
   - API 엔드포인트

5. **도메인별 구현 가이드**
   - 구현해야 할 기능 목록
   - 기술 스택 활용 방법
   - 최신 기술/기법 적용 방안

### 산출물
- **PROJECT_BLUEPRINT.md** (초상세)
- **아키텍처 다이어그램** (여러 레벨)
- **도메인별 구현 가이드**

### 관련 문서
- `05_BLUEPRINT_GUIDE.md` (기존)

---

## Stage 8: Task Breakdown 문서 작성

### 목적
- **AI가 집중해서 완전하게 구현할 크기로 작업 분할**

### 범위
1. **작업 분할 기준**
   - 1개 작업 = 1개 파일 또는 1개 기능
   - 4시간 이내 완료 가능 크기
   - 독립적으로 테스트 가능

2. **작업 목록 작성**
   - 도메인별 작업 분할
   - 우선순위 결정
   - 의존성 파악

3. **작업별 설명**
   - 목표
   - 입력/출력
   - 제약 조건
   - 참고 자료

### 산출물
- **TASK_BREAKDOWN.md**
- **작업별 상세 설명**

### 관련 문서
- `06_TASK_BREAKDOWN_GUIDE.md` (기존)

---

## Stage 9: 작업별 Checklist 작성

### 목적
- **TDD 기반 9-Step Checklist**
- 모든 기능 구현, 0 violations, 95%+ coverage 보장

### 범위
**TDD 9-Step Checklist**:
1. **목표 이해**
   - 요구사항 명확히
   - 성공 기준 정의

2. **테스트 작성**
   - 단위 테스트 먼저
   - 실패하는 테스트 확인

3. **구현**
   - 테스트 통과하는 최소 코드
   - 점진적 개선

4. **정적 검증**
   - Ruff, Mypy 실행
   - 0 violations 확인

5. **단위 테스트 실행**
   - Pytest 실행
   - 95%+ 커버리지 확인

6. **리팩토링**
   - 코드 정리
   - 중복 제거

7. **종합 테스트**
   - 통합 테스트
   - E2E 테스트

8. **문서화**
   - Docstring
   - README 업데이트

9. **커밋**
   - Git commit
   - PR 생성

### 산출물
- **작업별 체크리스트 문서**
- **테스트 템플릿**

### 관련 문서
- `07_CHECKLIST_GUIDE.md` (기존)

---

## 📊 Stage 간 관계

```
Stage 1 (패밀리+핵심기능)
   ↓ 필수 기술 방향, 기술 후보군
Stage 2 (구조설계)
   ↓ ADR 작성 대상 목록, 기술 스택 확정
Stage 3 (ADR)
   ↓ Bootstrap ADR, 도메인 ADR
Stage 4 (Bootstrap 계획)
   ↓ DNA 기본시스템 청사진
Stage 5 (Bootstrap 실행)
   ↓ 구현된 공통 모듈
Stage 6 (Standards)
   ↓ 프로젝트 규칙
Stage 7 (Blueprint)
   ↓ 초상세 청사진
Stage 8 (Task Breakdown)
   ↓ 작업 목록
Stage 9 (Checklist)
   ↓ 작업별 체크리스트
구현 (TDD 9-Step)
```

---

## 🎯 각 Stage의 핵심 원칙

### Stage 1: 큰 방향만
- ✅ 패밀리 결정 → 필수 기술 방향 자동 결정
- ✅ 핵심 기능 파악 → 구현 후보군 결정
- ❌ 구체적 기술 선택 금지

### Stage 2: 구체적 설계
- ✅ 외부 제약 조사 (실제 API, 법규 확인)
- ✅ 충돌 발견 → 트레이드오프 정리
- ✅ 기술 스택 확정 → 아키텍처 다이어그램

### Stage 3: 모든 결정 문서화
- ✅ 너무 당연한 것도 ADR 작성
- ✅ 제약도 ADR (선택지 1개여도)
- ✅ Bootstrap vs 도메인 구분

### Stage 4-9: 체계적 구현 준비
- ✅ 공통 환경 먼저 (Bootstrap)
- ✅ 규칙 정의 (Standards)
- ✅ 상세 설계 (Blueprint)
- ✅ 작업 분할 → 체크리스트 → 구현

---

## 📝 문서 명명 규칙

```
00_STAGE_STRUCTURE.md (이 문서)
01_CORE_DEFINITION_GUIDE.md (Stage 1)
01-1_CORE_DEFINITION_MANUAL_Part1.md
01-2_CORE_DEFINITION_MANUAL_Part2.md
02_STRUCTURE_DESIGN_GUIDE.md (Stage 2)
02-1_STRUCTURE_DESIGN_MANUAL.md
03_ADR_GUIDE.md (Stage 3)
03-1_ADR_MANUAL.md
04_BOOTSTRAP_PLAN_GUIDE.md (Stage 4)
05_BOOTSTRAP_EXECUTION_GUIDE.md (Stage 5)
04_PROJECT_STANDARDS_GUIDE.md (Stage 6)
05_BLUEPRINT_GUIDE.md (Stage 7)
06_TASK_BREAKDOWN_GUIDE.md (Stage 8)
07_CHECKLIST_GUIDE.md (Stage 9)
```

---

## 🔄 현재 작업 상태 (2025-11-12)

- ✅ **Stage 1**: 01_CORE_DEFINITION 완성
  - Part 0, Layer 1-2 완료
  - A-C-A 패밀리 발견 반영

- 🔄 **Stage 2**: 02_STRUCTURE_DESIGN 작성 필요
  - 기존 02_ARCHITECTURE_DECISION + 02_IMPLEMENTATION_APPROACH 통합
  - Layer 3 + 충돌 + 5단계 통합

- ✅ **Stage 3**: 03_ADR 기존 문서 검토 필요
  - Bootstrap vs 도메인 구분 추가

- ⏸️ **Stage 4-9**: 향후 작업

---

**버전 이력**:
- v1.0 (2025-11-12): 초기 작성 (Phase 2 실전 검증 기반)
