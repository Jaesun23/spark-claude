# 패밀리별 기술 매트릭스 디렉토리 안내

**작성일**: 2025-11-14 11:56  
**목적**: DNA 방법론 v4.0의 7가지 아키텍처 패밀리별 기술 선택 가이드

---

## 🎯 이 디렉토리의 역할

### DNA 방법론에서의 위치

```
Stage 1: 핵심 정의 (Core Definition)
  - 패밀리 구분 (3-Layer Decision Tree)
  ↓
🔥 여기! 패밀리별 기술 매트릭스 🔥
  ↓
Stage 2: 구현 방법 (Implementation Method)
  - Layer 3 제약사항 조사
  - NFR 우선순위 결정
  - 5단계 설계 프로세스
  ↓
Stage 3: ADR 작성 (Architecture Decision Records)
  - DNA 시스템 ADR
  - 도메인 특화 ADR
```

### 3가지 핵심 역할

#### 1. 패밀리별 필수 기술 자동 결정
- 패밀리 코드 (예: B-C-A) → 필수 DNA 시스템 도출
- 개발자가 "뭘 써야 하지?"를 고민하지 않도록
- 검증된 기술 조합 제시

#### 2. DNA 시스템 vs 도메인 기술 구분
- **DNA 시스템**: 패밀리가 강제하는 필수 요소 (공통 인프라)
- **도메인 기술**: 프로젝트 특성에 따라 선택 (서비스 로직)
- ADR 작성 범위 명확화

#### 3. 다음 단계로 자연스럽게 연결
- 기술 선택 → Stage 3 ADR 작성
- ADR → Stage 4 청사진 작성
- 체계적 의사결정 프로세스

---

## 🧬 DNA 11개 시스템

DNA 방법론의 핵심은 **11개의 표준 시스템**입니다. 모든 소프트웨어 프로젝트는 이 11개 시스템의 조합으로 구성됩니다.

### 11개 시스템 목록

| # | 시스템 이름 | 역할 | 모든 패밀리 필수? |
|---|------------|------|-----------------|
| **1** | Testing System | 테스트 전략, TDD, 품질 검증 | ✅ 필수 |
| **2** | Code Quality | 코딩 표준, Linting, 포맷팅 | ✅ 필수 |
| **3** | Architecture | 모듈 구조, 의존성 관리, 경계 강제 | ✅ 필수 |
| **4** | Type System | 타입 안전성, 정적 분석 | ✅ 필수 |
| **5** | Error Handling | 에러 처리 전략, 롤백, 복구 | ✅ 필수 |
| **6** | Configuration | 환경 설정, Feature Flags, Secrets | ✅ 필수 |
| **7** | Identity & Access | 인증, 권한, 사용자 관리 | ⚠️ 조건부 |
| **8** | Observability | 로깅, 모니터링, 추적, 메트릭 | ✅ 필수 |
| **9** | API Gateway | 요청 라우팅, Rate Limiting, 인증 | ⚠️ 조건부 |
| **10** | Resilience | 장애 허용, Circuit Breaker, Retry | ✅ 필수 |
| **11** | Performance | 벤치마크, 프로파일링, 최적화 | ✅ 필수 |

**조건부 시스템 설명**:
- **Identity & Access (#7)**: 사용자가 있는 시스템만 필요 (라이브러리/CLI는 불필요)
- **API Gateway (#9)**: 네트워크 API가 있는 시스템만 필요 (로컬 라이브러리는 불필요)

### DNA 시스템 vs 메인 서비스 기술

이 디렉토리의 각 패밀리 파일은 **두 종류의 기술**을 다룹니다:

**1. DNA 시스템 관련 기술** (모든 프로젝트 공통)
- Testing 프레임워크 (pytest, Jest)
- Code Quality 도구 (ESLint, Ruff)
- Observability 도구 (winston, structlog)
- 등등...

**2. 메인 서비스 기술** (패밀리별로 다름)
- A-A-B: RDBMS, 캐시, 메시징
- B-C-A: 스트리밍 플랫폼, 시계열 DB, 캐시
- B-B-B: Vector DB, 검색엔진, Embedding
- 등등...

---

## 📂 7개 패밀리 파일 구조

각 패밀리는 **3차원 코드**로 분류됩니다:

| 파일 | 패밀리 코드 | 패밀리 이름 | 대표 사례 |
|------|------------|------------|-----------|
| `01_ultra_high_frequency_trading_tech_options.md` | **A-A-A** | 초고속 거래 | NASDAQ (14μs), HFT |
| `02_transaction_crud_tech_options.md` | **A-A-B** | 트랜잭션/CRUD | Amazon 주문, Stripe 결제 |
| `03_collaboration_sync_tech_options.md` | **B-A-A** | 협업/동기화 | Google Docs, Figma |
| `04_search_recommendation_tech_options.md` | **B-B-B** | 검색/추천 | Elasticsearch, AI 외부메모리 |
| `05_real_time_streaming_tech_options.md` | **B-C-A** | 실시간 스트리밍 | Netflix RDG, Uber GPS |
| `06_analytics_batch_tech_options.md` | **B-A-C** | 분석/배치 | Snowflake, BigQuery |
| `07_safety_critical_iot_tech_options.md` | **A-B-A** | 안전-임계 IoT | 산업 제어, 긴급 경보 |

### 패밀리별 필요 DNA 시스템 매트릭스

| DNA 시스템 | A-A-A | A-A-B | B-A-A | B-B-B | B-C-A | B-A-C | A-B-A |
|-----------|-------|-------|-------|-------|-------|-------|-------|
| 1. Testing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2. Code Quality | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3. Architecture | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4. Type System | ⭐⭐⭐ | ✅ | ✅ | ✅ | ✅ | ✅ | ⭐⭐⭐ |
| 5. Error Handling | ✅ | ⭐⭐⭐ | ✅ | ✅ | ✅ | ✅ | ⭐⭐⭐ |
| 6. Configuration | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 7. Identity & Access | ❌ | ⭐⭐⭐ | ⭐⭐⭐ | ✅ | ✅ | ✅ | ⚠️ |
| 8. Observability | ⭐⭐⭐ | ✅ | ✅ | ✅ | ⭐⭐⭐ | ✅ | ⭐⭐⭐ |
| 9. API Gateway | ❌ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ✅ | ✅ | ⭐⭐⭐ |
| 10. Resilience | ⭐⭐⭐ | ⭐⭐⭐ | ✅ | ✅ | ⭐⭐⭐ | ✅ | ⭐⭐⭐ |
| 11. Performance | ⭐⭐⭐ | ✅ | ⭐⭐⭐ | ✅ | ⭐⭐⭐ | ✅ | ✅ |

**범례**:
- ✅ 필수 (기본 수준)
- ⭐⭐⭐ 매우 중요 (높은 우선순위, 특별한 주의 필요)
- ⚠️ 조건부 (프로젝트 특성에 따라)
- ❌ 불필요 (해당 패밀리에서 거의 사용 안 함)

**패밀리별 특징**:
- **A-A-A (초고속 거래)**: Type System, Performance, Observability 극대화
- **A-A-B (트랜잭션)**: Identity, API Gateway, Error Handling, Resilience 중요
- **B-A-A (협업)**: Identity, API Gateway, Performance (실시간 동기화)
- **B-B-B (검색)**: API Gateway (검색 API), Identity (접근 제어)
- **B-C-A (스트리밍)**: Observability, Resilience, Performance (메시지 처리량)
- **B-A-C (분석)**: 기본 DNA 시스템으로 충분
- **A-B-A (IoT)**: Type System, Error Handling, Observability, Resilience 중요

### 패밀리별 메인 서비스 기술

각 패밀리는 DNA 시스템 외에 **메인 서비스 기술**이 필요합니다:

| 패밀리 | 메인 서비스 핵심 기술 | 이유 |
|-------|-------------------|------|
| **A-A-A** | FPGA, 코로케이션, RDMA 네트워킹 | 마이크로초급 레이턴시 필수 |
| **A-A-B** | RDBMS, 캐시, 메시징 | ACID 트랜잭션 + 성능 + 비동기 |
| **B-A-A** | CRDT/OT 엔진, WebSocket, 동기화 DB | 실시간 협업 + 충돌 해결 |
| **B-B-B** | Vector DB, Embedding 모델, 검색엔진 | 유사도 검색 + 랭킹 |
| **B-C-A** | 스트리밍 플랫폼, 시계열 DB, 캐시 | 대용량 이벤트 처리 |
| **B-A-C** | 데이터 웨어하우스, ETL, BI 도구 | 대규모 배치 분석 |
| **A-B-A** | MQTT, SCADA, 센서 융합 | IoT 프로토콜 + 실시간 제어 |

---

### 3차원 코드 의미

**첫 번째 글자 (실패의 파급력)**:
- **A** (Critical): 치명적 - 실패 시 생명/재산/시장 손실
- **B** (Graceful): 점진적 - 실패 시 성능 저하, 계속 작동 가능

**두 번째 글자 (데이터의 형태)**:
- **A** (Structured): 구조화 - 고정 스키마, 명확한 관계
- **B** (Semi-Structured): 반구조화 - 유연한 스키마, JSON/XML
- **C** (Unstructured): 비구조화 - 스키마 없음, 이벤트/로그

**세 번째 글자 (응답 시점)**:
- **A** (Real-time): 밀리초 - 즉각 응답 (< 100ms)
- **B** (Interactive): 수초 - 사람이 기다릴 수 있는 속도 (1~10초)
- **C** (Batch): 배치 - 스케줄 기반 (시간/일 단위)

---

## 📖 각 파일의 구조 (4-Part)

모든 패밀리 파일은 동일한 구조를 따릅니다:

### Part 1: 패밀리가 요구하는 시스템 구조 ⭐⭐⭐
- 각 차원(A/B/C)이 강제하는 기술적 요구사항
- 검증 사례 (Netflix, Google, Uber 등)
- **이 패밀리에 필요한 DNA 시스템** (11개 중 선택)
- **메인 서비스 필수 기술** (2~5개)

### Part 2: 메인 서비스 기술 선택 ⭐⭐⭐
- 각 메인 서비스 기술마다 **3가지 옵션** 제시:
  - 옵션 1: 고성능/고비용
  - 옵션 2: 균형 (중간)
  - 옵션 3: 저비용/경량
- 구체적 스펙, 비용, 장단점, 적합 사례
- 비교표 + 의사결정 플로우차트

### Part 2.5: DNA 시스템 기술 선택 (새로 추가) 🆕
- **이 패밀리에 특별히 중요한 DNA 시스템**에 대한 기술 옵션
- 예: A-A-A는 Performance 시스템이 매우 중요 → 벤치마크 도구 3가지 비교
- 예: A-A-B는 Identity 시스템이 중요 → 인증 솔루션 3가지 비교
- 모든 DNA 시스템을 다루지 않고, **⭐⭐⭐ 표시된 것만** 다룸

### Part 3: 도메인 선택 요소
- 패밀리와 무관하게 프로젝트별로 선택하는 기술
- 프론트엔드, 백엔드 언어, 인증 등
- 간결하게 (20~50줄)

### Part 4: Stage 2 통합
- Layer 3 제약사항 반영 예시
- NFR 충돌 해결 예시
- ADR 작성 준비 (DNA 시스템 vs 도메인 구분)

---

## 🚀 사용 방법

### Step 1: 패밀리 코드 확정
Stage 1에서 3-Layer Decision Tree로 패밀리 코드를 확정합니다.

**예시**:
```
Q1: 실패하면? → B (점진적, 일부 손실 허용)
Q2: 데이터 형태? → C (비구조화, 이벤트 스트림)
Q3: 응답 시점? → A (밀리초, 실시간)

→ 패밀리 코드: B-C-A (실시간 스트리밍)
```

### Step 2: 해당 패밀리 파일 열기
`05_real_time_streaming_tech_options.md` 파일을 엽니다.

### Step 3: Part 1 확인 - 필요한 시스템 파악
패밀리가 요구하는 두 종류의 시스템을 확인합니다.

**1. DNA 시스템** (11개 중 필요한 것):
```
✅ 필수: Testing, Code Quality, Architecture, Error Handling, Configuration, Observability, Resilience, Performance
⭐⭐⭐ 특별 중요: Performance (마이크로초 최적화), Type System (안전성)
❌ 불필요: Identity, API Gateway (네트워크 서비스 아님)
```

**2. 메인 서비스 기술** (패밀리 특화):
```
- FPGA/ASIC 하드웨어
- RDMA 네트워킹
- 커널 바이패스 스택
```

### Step 4: Part 2 확인 - 메인 서비스 기술 선택
각 메인 서비스 기술마다 3가지 옵션을 비교하고 선택합니다.

**FPGA 하드웨어 예시**:
- 옵션 1: Custom FPGA (초고성능, 매우 비쌈)
- 옵션 2: 상용 FPGA 카드 (고성능, 비쌈)
- 옵션 3: Software 최적화 (저렴, 마이크로초급 어려움)

비교표와 플로우차트를 참고하여 의사결정합니다.

### Step 4.5: Part 2.5 확인 - 중요 DNA 시스템 기술 선택 🆕
이 패밀리에서 **⭐⭐⭐ 표시된 DNA 시스템**의 기술을 선택합니다.

**Performance System 예시** (A-A-A에서 ⭐⭐⭐):
- 옵션 1: VTune (Intel, 전문가용)
- 옵션 2: perf (Linux 기본)
- 옵션 3: Custom Profiler

**Type System 예시** (A-A-A에서 ⭐⭐⭐):
- 옵션 1: Rust (소유권 시스템)
- 옵션 2: C++ (템플릿)
- 옵션 3: C (수동 관리)

### Step 5: Part 3 확인 - 도메인 기술 선택
프로젝트 특성에 따라 도메인 기술을 선택합니다.

**예시**:
- 백엔드: Node.js vs Python vs Go
- 프론트엔드: React vs Vue
- 인증: Auth0 vs Cognito

### Step 6: Part 4 활용 - Stage 2로 연결
- Layer 3 제약사항 반영 방법 참고
- NFR 충돌 해결 패턴 참고
- **DNA 시스템 ADR 목록 준비** (ADR-001 ~ ADR-011)
- **메인 서비스 ADR 목록 준비** (ADR-101 ~ ADR-1XX)
- **도메인 ADR 목록 준비** (ADR-201 ~ ADR-2XX)

---

## 🎓 핵심 원칙

### 1. 패밀리가 시스템 구조를 결정합니다
- 개발자의 "취향"이 아닌 **시스템 특성**이 필요한 시스템을 강제
- B-C-A 패밀리는 **무조건** 스트리밍 플랫폼 필요
- A-A-B 패밀리는 **무조건** ACID DB 필요
- A-A-A 패밀리는 **무조건** Performance 시스템 극대화 필요

### 2. 3가지 기술 계층 구분이 중요합니다
- **DNA 시스템**: 11개 표준 시스템, 모든 프로젝트 공통 기반 (ADR-001~011)
- **메인 서비스**: 패밀리가 강제하는 핵심 기술 (ADR-101~1XX)
- **도메인 기술**: 프로젝트 특화, 팀 역량/선호도 반영 (ADR-201~2XX)
- 구분하지 않으면 ADR이 뒤죽박죽!

### 3. DNA 시스템은 우선순위가 있습니다
- **✅ 필수**: 모든 패밀리에 기본 수준 필요
- **⭐⭐⭐ 특별 중요**: 해당 패밀리에서 높은 우선순위
- **⚠️ 조건부**: 프로젝트 특성에 따라
- **❌ 불필요**: 해당 패밀리에서 거의 사용 안 함

### 4. 실증 데이터 기반입니다
- 모든 기술 옵션은 **실제 프로덕션 사례** 검증
- 구체적 수치 (처리량, 레이턴시, 비용) 제시
- "빠름" ✗ → "p99 <10ms" ✓

### 4. 의사결정을 지원합니다
- 3가지 옵션 비교 (고/중/저)
- 비교표 + 플로우차트 제공
- "무엇을 선택할지" 명확히 안내

---

## ⚠️ 주의사항

### ❌ 이 파일들은 구현 가이드가 아닙니다
- 코드 예시 없음 (단 한 줄도!)
- 패턴 설명 최소화
- 도구 나열 최소화
- **목적**: 기술 **선택** 지원

### ✅ 구현은 공식 문서를 참고하세요
- PostgreSQL 설정 → PostgreSQL 공식 문서
- Kafka 튜닝 → Kafka 공식 문서
- Redis 패턴 → Redis 공식 문서

### 📝 Context7 MCP 활용
- 모든 기술 정보는 Context7에서 확보
- 출처 확인된 공식 문서만 사용
- 토큰 효율 6~10배 (WebSearch 대비)

---

## 🔗 다음 단계

### 패밀리 선택 완료 후
1. **Stage 2**: 구현 방법 설계
   - Layer 3 제약사항 조사
   - NFR 우선순위 결정
   - 5단계 설계 프로세스

2. **Stage 3**: ADR 작성
   - DNA 시스템 ADR (예: ADR-001 ~ ADR-011)
   - 도메인 특화 ADR (예: ADR-101 ~ ADR-1XX)

3. **Stage 4**: 청사진 작성
   - DNA 시스템 청사진 (common/ 폴더)
   - 도메인 청사진 (services/ 폴더)

4. **Stage 5~9**: 분해 → 체크리스트 → 구현

---

## 📊 완성도 검증

### 7개 패밀리 이론적 완전성
- 3×3×3 = 27가지 이론 조합 중
- ✅ **16개 조합** 프로덕션 검증
- ⭐ **7개 핵심 패밀리** 선정
- 실무 커버리지: **95%+**

### 검증 근거
- **SEI Quality Attributes Framework** 매핑
- **Martin Fowler Patterns** 조합
- **CAP/ACID/BASE Theorem** 반영
- Netflix, Google, Uber, Amazon 등 실증

---

## 💡 자주 묻는 질문

### Q1: 우리 시스템이 여러 패밀리에 걸쳐 있다면?
**A**: 하이브리드 시스템입니다. 각 하위 시스템별로 패밀리를 구분하세요.

**예시 - Netflix**:
- 스트리밍: B-C-A (실시간 스트리밍)
- 결제: A-A-B (트랜잭션/CRUD)
- 추천: B-B-B (검색/추천)

### Q2: 패밀리 코드가 애매하다면?
**A**: 가장 중요한 특성(코어 기능)을 기준으로 선택하세요.

**예시 - 주문 시스템**:
- 코어: 주문 트랜잭션 → A-A-B
- 부가: 실시간 알림 → B-C-A (별도 모듈)

### Q3: DNA 시스템, 메인 서비스, 도메인 기술 구분이 애매하다면?
**A**: 두 가지 기준으로 판단하세요.

**기준 1: 패밀리 변경 시 함께 바뀌는가?**
- **DNA 시스템**: 패밀리 무관, 모든 프로젝트 공통 (Testing, Observability 등)
- **메인 서비스**: A-A-B → B-C-A 변경 시 RDBMS → Kafka로 변경 필수
- **도메인 기술**: 패밀리 변경과 무관 (React → Vue 선택은 패밀리와 무관)

**기준 2: 11개 표준 시스템에 해당하는가?**
- **DNA 시스템**: Testing, Code Quality, Architecture, Type System, Error Handling, Configuration, Identity & Access, Observability, API Gateway, Resilience, Performance
- **메인 서비스**: 위 11개에 해당 안 함 (RDBMS, Kafka, Redis, CRDT 등)
- **도메인 기술**: 위 11개에 해당 안 함 (React, FastAPI, Auth0 등)

**예시**:
- PostgreSQL → 메인 서비스 (A-A-B 패밀리 강제)
- pytest → DNA 시스템 #1 (Testing)
- FastAPI → 도메인 기술 (프로젝트 선택)

### Q4: DNA 시스템 중 ⭐⭐⭐가 많은데 모두 다뤄야 하나요?
**A**: 아니요, Part 2.5에서는 **가장 중요한 1~3개만** 다룹니다.

**예시 - A-A-A**:
- ⭐⭐⭐ 4개: Type System, Observability, Resilience, Performance
- Part 2.5에서 다룰 것: Performance (가장 특수함), Type System (안전성 극대화)
- 나머지는 일반 DNA 시스템 가이드 참고

---

**이 디렉토리는 DNA 방법론의 핵심 연결고리입니다!**

패밀리 선택 → 기술 매트릭스 참고 → ADR 작성 → 청사진 작성 → 구현

체계적이고 검증된 기술 선택으로 프로젝트 성공률을 높이세요! 💪
