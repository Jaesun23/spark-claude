# 구현 사례집 (Implementation Cases)

> **목적**: Stage 1-3 전체 흐름을 실전 사례로 보여주기
>
> **버전**: v1.0 (2025-11-12)
> - v1.0: 4개 사례 (A-A-A, C-B-B, B-A-A, A-C-A)

---

## 📚 이 문서의 구성

각 사례는 다음 흐름을 따릅니다:

```
Stage 1: 패밀리 구분
├─ Part 0: 핵심 기능 파악
├─ Layer 1: 패밀리 결정 (A-B-C 패턴)
└─ Layer 2: NFR 우선순위

Stage 2: 구조설계
├─ Layer 3: 환경 제약 조사
├─ 충돌 패턴 발견
└─ 5단계 구현방법

Stage 3: ADR 문서화
├─ DNA 시스템 ADR 목록
└─ 도메인 ADR 목록
```

---

## 사례 목록

1. [Case 1: AI 외부메모리 (A-A-A)](#case-1-ai-외부메모리-a-a-a) - CRUD/트랜잭션
2. [Case 2: BioNeX (C-B-B)](#case-2-bionex-c-b-b) - 검색/추천
3. [Case 3: BlueprintAI (B-A-A)](#case-3-blueprintai-b-a-a) - 협업/동기화
4. [Case 4: 주식 거래 플랫폼 (A-C-A)](#case-4-주식-거래-플랫폼-a-c-a) ⭐ - 실시간 트랜잭션

---

## Case 1: AI 외부메모리 (A-A-A)

### 시스템 개요

**목적**: Gemini AI에게 영구 메모리 제공 (CREATE, READ, UPDATE, DELETE)

**핵심 기능**: 메모리 CRUD
- 생성: AI가 대화에서 얻은 정보를 저장
- 읽기: AI가 필요할 때 과거 정보 검색
- 수정: 정보 업데이트
- 삭제: 불필요한 정보 제거

---

### Stage 1: 패밀리 구분

#### Part 0: 핵심 기능 파악

**Q0-1: 존재 이유**
```
핵심 기능: 메모리 CRUD (하나!)
구현 방식:
- CREATE: POST /memories
- READ: GET /memories
- UPDATE: PUT /memories/{id}
- DELETE: DELETE /memories/{id}

⚠️ 주의: CRUD가 4개 기능 아님, 1개 기능의 4가지 작업!
```

**Q0-2: 실패 영향**
```
CREATE 실패: 정보 저장 안 됨 → AI가 까먹음
READ 실패: 정보 못 가져옴 → AI가 모름
UPDATE 실패: 잘못된 정보 유지 → AI가 착각
DELETE 실패: 불필요한 정보 남음 → 혼란

→ 모두 동일한 영향: 데이터 손실/오류
→ 치명도: A (데이터 정확성 필수)
```

---

#### Layer 1: 패밀리 결정

**L1-Q1: 실패 파급력**
```
선택: A (치명적)
이유: 메모리 데이터 손실 = AI 기능 상실
```

**L1-Q2: 정보 형태**
```
선택: A (구조화)
이유: JSON 형식, 스키마 정의됨
{
  "id": "uuid",
  "content": "Jason prefers Python",
  "timestamp": "2025-11-12",
  "tags": ["preference", "programming"]
}
```

**L1-Q3: 응답 시점**
```
선택: A (즉각)
이유: AI가 대화 중 즉시 저장/조회
```

**→ 패밀리: A-A-A (CRUD/트랜잭션)**

---

#### Layer 2: NFR 우선순위

**L2-Q1: 핵심 품질**
```
선택: A (정확성 100%)
이유: 메모리 오류 = AI 오작동
```

**L2-Q2: 규모**
```
선택: A (소규모)
이유: 개인 사용 (1명), 메모리 수천 개
```

**L2-Q3: 데이터 노출**
```
선택: B (민감)
이유: 개인 대화 내용, 암호화 권장
```

**L2-Q4: 최신성**
```
선택: A (즉시)
이유: 저장 즉시 다음 대화에서 사용
```

**NFR 프로파일: A-A-B-A**

---

### Stage 2: 구조설계

#### Layer 3: 환경 제약

**L3-Q1: 외부 API/서비스**
```
없음 - 자체 구축
```

**L3-Q2: 보안/컴플라이언스**
```
개인 사용:
- API 키 환경변수
- HTTPS 권장
- 백업 권장
```

**L3-Q3: 배포 환경**
```
선택: 클라우드 (AWS, GCP)
이유: 24/7 가용성, AI가 언제든 접근
```

---

#### 충돌 패턴

**충돌 매트릭스**:
```
| Layer 2 NFR | Layer 3 제약 | 충돌? | 영향 |
|-------------|--------------|-------|------|
| 정확성 A | 자체 구축 | ❌ | RDBMS로 해결 |
| 규모 A | 개인 사용 | ❌ | 단일 서버 충분 |
| 보안 B | 클라우드 | ❌ | TLS 기본 제공 |
| 즉시성 A | 클라우드 | ❌ | API < 100ms |
```

**→ 충돌 없음! 단순 CRUD 시스템**

---

#### 5단계 구현방법

**Step 4: 기술 스택**
```
Backend:
- Python 3.11+
- FastAPI (REST API)
- PostgreSQL (ACID)
- SQLAlchemy (ORM)

Deployment:
- Docker
- AWS ECS / GCP Cloud Run
```

**Step 5: 아키텍처**
```
시스템 구조: 모놀리식 (단순 CRUD)
통신 패턴: REST API
데이터베이스: PostgreSQL (ACID 보장)
배포: 컨테이너 (Docker)
```

---

### Stage 3: ADR 목록

#### DNA 시스템 ADR (A-A-A 패밀리)
```
ADR-001: PostgreSQL 사용 (RDBMS 필수)
ADR-002: ACID 트랜잭션 필수
ADR-003: SQLAlchemy ORM 사용
ADR-004: REST API 표준
```

#### 도메인 ADR
```
ADR-101: FastAPI 선택 (vs Flask, Django)
ADR-102: PostgreSQL 14+ 사용
ADR-103: UUID primary key 사용
ADR-104: AWS ECS 배포
```

---

## Case 2: BioNeX (C-B-B)

### 시스템 개요

**목적**: 생명과학 논문 AI 검색 및 추천

**핵심 기능**: 의미 기반 검색
- 자연어 질문 → 관련 논문 찾기
- 논문 내용 이해 → 비슷한 논문 추천

---

### Stage 1: 패밀리 구분

#### Part 0: 핵심 기능

**Q0-1: 존재 이유**
```
핵심 기능: 검색 (하나!)
구현 방식:
- 키워드 검색
- 의미 검색 (Vector)
- 필터링 (저자, 연도)

❌ 잘못: 키워드 검색 + 의미 검색 = 2개 기능
✅ 올바름: 검색 = 1개 기능, 여러 방식
```

**Q0-2: 실패 영향**
```
검색 실패: 논문 못 찾음 → 불편
검색 품질 낮음: 관련 없는 결과 → 불편

→ 데이터 손실 아님, 점진적 품질 저하
→ 치명도: C (관련성)
```

---

#### Layer 1: 패밀리

**L1-Q1: 실패 파급력**
```
선택: C (점진적 저하)
이유: 검색 결과 없어도 시스템 동작, 품질만 낮음
```

**L1-Q2: 정보 형태**
```
선택: B (비구조화)
이유: 논문 텍스트, 초록, 자연어
```

**L1-Q3: 응답 시점**
```
선택: B (조회 후)
이유: 검색 쿼리 → 1-3초 대기 OK
```

**→ 패밀리: C-B-B (검색/추천)**

---

#### Layer 2: NFR

**NFR 프로파일: C-B-B-B**
```
L2-Q1: C (관련성) - 의미 이해 중요
L2-Q2: B (중규모) - 연구자 수백 명
L2-Q3: B (민감) - 논문 접근 권한
L2-Q4: B (준실시간) - 일일 업데이트
```

---

### Stage 2: 구조설계

#### 충돌 패턴

```
| Layer 2 NFR | Layer 3 제약 | 충돌? | 영향 |
|-------------|--------------|-------|------|
| 관련성 C | 임베딩 비용 | ✅ | OpenAI API 비용 높음 |
| 규모 B | Vector DB | ⚠️ | 논문 10만 편 시 확장 |
```

**트레이드오프**:
- 옵션 1: OpenAI Embedding (비용 높음, 품질 좋음)
- 옵션 2: Self-hosted (비용 낮음, 품질 낮음)
- 선택: OpenAI (관련성 우선)

---

#### 기술 스택

```
Backend: Python + FastAPI
Vector DB: Milvus / Pinecone
Embedding: OpenAI text-embedding-3-large
Search: Elasticsearch (hybrid search)
```

---

### Stage 3: ADR 목록

#### DNA 시스템 ADR (C-B-B)
```
ADR-001: Vector DB 필수
ADR-002: Embedding Model 필수
ADR-003: Hybrid Search (Vector + Keyword)
```

#### 도메인 ADR
```
ADR-101: OpenAI Embedding 선택 (vs self-hosted)
ADR-102: Milvus 선택 (vs Pinecone)
ADR-103: Elasticsearch 병행 (키워드)
```

---

## Case 3: BlueprintAI (B-A-A)

### 시스템 개요

**목적**: 실시간 협업 다이어그램 편집 (Google Docs 스타일)

**핵심 기능**: 협업 편집
- 여러 사용자 동시 편집
- 실시간 동기화
- 충돌 해결

---

### Stage 1: 패밀리

**Layer 1: B-A-A**
```
L1-Q1: B (중단·재시도) - 일시 연결 끊김 OK
L1-Q2: A (구조화) - 다이어그램 JSON
L1-Q3: A (즉각) - 실시간 동기화
```

**Layer 2: B-B-B-A**
```
L2-Q1: B (속도) - 부드러운 UX
L2-Q2: B (중규모) - 팀 수십 명
L2-Q3: B (민감) - 프로젝트 정보
L2-Q4: A (즉시) - 실시간 변경 반영
```

**→ 패밀리: B-A-A (협업/동기화)**

---

### Stage 2: 구조설계

#### 충돌 패턴

```
| Layer 2 NFR | Layer 3 제약 | 충돌? | 영향 |
|-------------|--------------|-------|------|
| 속도 B | 동기화 오버헤드 | ✅ | OT/CRDT 복잡도 |
| 즉시성 A | WebSocket 연결 | ⚠️ | 재연결 처리 |
```

**해결 전략**:
- CRDT (Conflict-free Replicated Data Type)
- WebSocket + Fallback (Long Polling)

---

#### 기술 스택

```
Frontend: React + Yjs (CRDT)
Backend: Node.js + WebSocket
Database: PostgreSQL (document state)
Real-time: y-websocket provider
```

---

### Stage 3: ADR

#### DNA 시스템 ADR (B-A-A)
```
ADR-001: CRDT 알고리즘 필수
ADR-002: WebSocket 필수
ADR-003: 재연결 로직 필수
```

#### 도메인 ADR
```
ADR-101: Yjs 선택 (vs Automerge)
ADR-102: PostgreSQL 선택
ADR-103: y-websocket 선택
```

---

## Case 4: 주식 거래 플랫폼 (A-C-A) ⭐

### 시스템 개요

**목적**: 개인 투자자를 위한 주식 자동/수동 거래 플랫폼

**핵심 기능**: 거래 (Trading)
- 구현 방식 A: 수동 거래 (사용자 클릭)
- 구현 방식 B: 자동 거래 (조건 충족 시)
  - 전략 1: 지정가 도달 → 매수
  - 전략 2: % 변동 감지 → 매도
  - 전략 3: 정기 매수 (적립식)

**부가 기능**: 실시간 호가 스트리밍

---

### Stage 1: 패밀리 구분

#### Part 0: 핵심 기능 파악 ⭐

**Q0-1: 존재 이유**
```
❌ 잘못된 구분:
- 수동 거래 (핵심 기능 1)
- 자동 거래 (핵심 기능 2)

✅ 올바른 구분:
- 거래 (핵심 기능 하나!)
  ├─ 구현 방식 A: 수동 (클릭)
  └─ 구현 방식 B: 자동 (조건)
```

**핵심 인사이트** (Jason):
> "'자동'에 의미를 두면 안되고 '거래'가 핵심이에요.
> 실패 = 금전 손실이 구현 방식과 무관하다는 게 증거죠."

**Q0-2: 실패 영향**
```
수동 거래 실패: 클릭했는데 안 됨 → 금전 손실
자동 거래 실패: 조건 충족했는데 안 됨 → 금전 손실

→ 구현 방식 무관, 동일한 치명도!
→ "거래" 1개가 핵심 기능 맞음 ✅
```

---

#### Layer 1: 패밀리 결정

**L1-Q1: 실패 파급력**
```
선택: A (치명적)
이유:
- 거래 요청 실패 → 금전 손실
- 조건 감지 오류 → 기회 상실 → 금전 손실
- 체결 실패 → 금전 손실
```

**L1-Q2: 정보 형태**
```
선택: C (숫자·분석)
이유:
- 주가, 호가, 거래량 = 시계열 데이터
- % 변동 계산, 이동평균
- 조건 비교 (지정가 도달 여부)
```

**L1-Q3: 응답 시점**
```
선택: A (즉각)
이유:
- 거래 요청 → 즉시 체결 (<100ms)
- 가격 변동 → 즉시 감지 (초 단위)
- 체결 완료 → 즉시 알림
```

**→ 패밀리: A-C-A** 💥

**🔥 중요 발견: 새로운 패밀리!**
```
기존 5개 패밀리:
1. A-A-A (CRUD/트랜잭션)
2. C-B-B (검색/추천)
3. B-C-A (실시간 스트리밍)
4. B-A-A (협업/동기화)
5. C-C-C (분석/배치)

새 패밀리:
6. A-C-A (실시간 트랜잭션) ⭐
   - 특성: 정확성 + 숫자 데이터 + 즉시성
   - 예시: 금융 거래, IoT 제어, 자동화 시스템
```

---

#### Layer 2: NFR 우선순위

**L2-Q1: 핵심 품질**
```
선택: A (정확성 100%)
이유:
- 조건 감지 오류 = 금전 손실
- "70,000원 도달" 놓치면 안 됨
```

**L2-Q2: 규모**
```
선택: B (중규모)
이유: 개인용 시작 → 추후 서비스화 대비
```

**L2-Q3: 데이터 노출**
```
선택: B (민감)
이유:
- 개인 투자 내역
- 금융위원회 규제
```

**L2-Q4: 최신성**
```
선택: A (즉시)
이유:
- 호가 변동 즉시 반영
- 조건 감지 즉시 체결
```

**NFR 프로파일: A-B-B-A**

---

### Stage 2: 구조설계

#### Layer 3: 환경 제약 조사

**L3-Q1: 외부 API 비교** (필수!)

**비교표** (증권사 6개 비교):
```
| 증권사 | Rate Limit | API 방식 | OS 제약 | 개인 사용 | 평가 |
|--------|------------|----------|---------|-----------|------|
| 한국투자증권 | 20건/초 | REST+WS | 크로스 | ✅ 무료 | ⭐⭐⭐ |
| 키움증권 | 5건/초 | COM/DLL | Windows | ✅ 무료 | ⭐⭐ |
| 이베스트 | 10건/초 | REST+WS | 크로스 | ✅ 무료 | ⭐⭐ |
| 삼성증권 | - | - | - | ❌ 불가 | ❌ |
| NH투자증권 | 10건/초 | REST | 크로스 | ✅ 무료 | ⭐⭐ |
| 미래에셋 | - | - | - | ⚠️ 제한 | ⭐ |
```

**선택 과정**:
```
1차 필터: 개인 사용 가능? (4개 남음)
2차 필터: 플랫폼 제약? (크로스 플랫폼 3개)
3차 비교: Rate Limit (한투 20 > 이베 10 > NH 10)

→ 선택: 한국투자증권 ✅
```

**🔥 핵심 통찰**:
> "증권사 선택 = 아키텍처 결정!"
>
> - Rate Limit 20건/초 → 관리 전략 필요
> - REST + WebSocket → 하이브리드 가능
> - 크로스 플랫폼 → Docker, Cloud 가능

**L3-Q2: 보안/컴플라이언스**

**개인 개발자 vs 증권사 구분** (Jason 지적!):
```
증권사의 의무 (우리와 무관):
- 거래 기록 10년 보관
- KYC 정보 관리
- 금융위원회 규제 준수

개인 개발자의 의무 (우리가 해야 함):
✅ API 키 안전 저장 (.env, Secret Manager)
✅ HTTPS 통신 (증권사 API 기본)
✅ 거래 로그 (자체 감사용)
```

**L3-Q3: 배포 환경**
```
선택: 클라우드 (AWS, GCP)
이유:
- 24/7 가동 필요 (자동 거래)
- Docker 지원
- Linux 가능 (한투 API 크로스)
```

---

#### 충돌 패턴 발견

**충돌 매트릭스**:
```
| Layer 2 NFR | Layer 3 제약 | 충돌? | 영향 |
|-------------|--------------|-------|------|
| 정확성 A | API 20건/초 | ✅ | 모든 조건 실시간 감지 불가 |
| 즉시성 A | API 20건/초 | ✅ | 50개 종목 동시 모니터링 불가 |
| 보안 B | HTTPS 기본 | ❌ | 충돌 없음 |
| 규모 B | WebSocket 41건 | ⚠️ | 서비스화 시 재검토 |
```

**충돌 1: 정확성 A + 즉시성 A vs Rate Limit**
```
문제:
- 100% 정확 + 초 단위 감지
- 관심 종목 50개 × 1초마다 = 50건
- Rate Limit 20건/초 → 불가능!

트레이드오프 옵션:
1. 정확성 우선: 20개만 실시간, 나머지 폴링
2. 즉시성 우선: 50개 전부, 2.5초마다 확인
3. 균형: 핵심 20개 실시간, 나머지 5초 주기

선택: 옵션 3 (균형) ✅
이유: 사용자 우선순위 설정 기능
```

---

#### 5단계 구현방법

**Step 1: 속성 질문**
```
성능:
- 거래 요청 응답 시간: < 100ms
- 조건 감지 주기: 1초 (우선순위) / 5초 (일반)
- 동시 모니터링 종목: 50개

가용성:
- 다운타임: < 0.1% (99.9%)
- 자동 재연결: 필수

확장성:
- 사용자: 1명 → 100명 (단계적)
- 종목: 50개 → 200개
```

**Step 4: 기술 스택**
```
Backend:
- Python 3.11+
- FastAPI (REST API)
- asyncio + WebSocket
- PostgreSQL (거래 기록)
- Redis (Queue + 캐시)

Integration:
- 한국투자증권 OpenAPI
- WebSocket (실시간 호가)
- REST (거래 요청)

Deployment:
- Docker
- AWS ECS
- RDS (PostgreSQL)
- ElastiCache (Redis)
```

**Step 5: 아키텍처**
```
시스템 구조: 하이브리드

통신 패턴:
- WebSocket: 실시간 호가 (우선순위 종목)
- Polling: 주기적 확인 (일반 종목)
- REST: 거래 요청 (Rate Limit 관리)

상태 관리:
- Stateful: WebSocket 연결 유지
- Redis Queue: 거래 요청 순서 보장

배포 전략:
- 컨테이너: Docker
- 오케스트레이션: ECS
- 스케일링: 수평 확장 대비
```

---

### Stage 3: ADR 문서화

#### DNA 시스템 ADR (A-C-A 패밀리)

**패밀리가 강제하는 필수 요소**:
```
ADR-001: RDBMS 필수 (트랜잭션 보장)
- PostgreSQL 14+
- ACID 트랜잭션
- 이유: 거래 정확성 A 요구

ADR-002: 실시간 통신 필수
- WebSocket 또는 Server-Sent Events
- 이유: 즉시성 A 요구

ADR-003: 메시지 큐 필수
- Redis Queue, RabbitMQ, Kafka 중 택 1
- 이유: 이벤트 순서 보장, Rate Limit 관리

ADR-004: 캐시 필수
- Redis 또는 Memcached
- 이유: 실시간 성능 + 정확성 균형

ADR-005: 하이브리드 아키텍처
- 실시간 + 배치 혼합
- 이유: A-C-A 패밀리 특성 (트랜잭션 + 분석)
```

---

#### 도메인 ADR (주식 거래 특화)

**외부 제약 관련**:
```
ADR-101: 한국투자증권 OpenAPI 선택
- Context: 6개 증권사 비교
- Decision: 한국투자증권
- Reason:
  - Rate Limit 20건/초 (최고)
  - REST + WebSocket (유연)
  - 크로스 플랫폼 (클라우드 배포 가능)
- Consequences:
  ✅ 높은 처리량
  ✅ 유연한 아키텍처
  ❌ API 변경 시 종속성

ADR-102: 하이브리드 전략 (WebSocket + Polling)
- Context: Rate Limit vs 즉시성 충돌
- Decision: 우선순위별 이원화
  - 핵심 20개: WebSocket (1초)
  - 나머지: Polling (5초)
- Reason: 정확성 + 즉시성 균형
- Consequences:
  ✅ 중요 종목 실시간
  ✅ Rate Limit 준수
  ❌ 복잡도 증가
```

**기술 스택**:
```
ADR-103: FastAPI 선택
- Context: Python 프레임워크
- Decision: FastAPI (vs Flask, Django)
- Reason:
  - asyncio 네이티브 (WebSocket)
  - 타입 검증 (Pydantic)
  - 자동 문서화
- Compliance:
  - 모든 엔드포인트 async def
  - Pydantic 모델 필수

ADR-104: PostgreSQL + Redis
- Context: 데이터 저장 + 큐
- Decision:
  - PostgreSQL: 거래 기록, 사용자 정보
  - Redis: Queue, 캐시, WebSocket 세션
- Reason:
  - PostgreSQL: ACID 보장
  - Redis: 빠른 캐시 + 큐
```

**품질 보장**:
```
ADR-105: Human-in-the-loop 주문 검증
- Context: 자동 거래 오작동 방지
- Decision: 실제 체결 전 사용자 확인
- Reason:
  - 조건 감지 버그 → 금전 손실 방지
  - 사용자 최종 결정권
- Implementation:
  - 조건 충족 → 알림 전송
  - 사용자 승인 → 실제 체결
  - 타임아웃: 30초

ADR-106: 거래 로그 영구 보관
- Context: 감사 추적, 버그 디버깅
- Decision: 모든 거래 PostgreSQL 저장
- Columns:
  - timestamp, stock_code, action
  - price, quantity, condition
  - execution_status, api_response
- Retention: 무제한 (세금 신고용)
```

---

### 핵심 교훈

#### 1. 핵심 기능 구분이 출발점

```
❌ 잘못된 구분: 수동 거래 + 자동 거래 = 2개
   → Layer 1 답변 혼란
   → "어느 기능 기준으로 답하나?"

✅ 올바른 구분: 거래 = 1개, 수동/자동 = 구현 방식
   → Layer 1 일관된 답변
   → 통합 아키텍처 가능
```

#### 2. Layer 3 조사가 필수

```
외부 API 비교 없이는 설계 불가능!
- 증권사 선택 = 아키텍처 80% 결정
- Rate Limit = 전체 설계 제약
- OS 제약 = 배포 전략 결정
```

#### 3. 충돌은 정상이다

```
정확성 A + 즉시성 A + Rate Limit
→ 당연히 충돌!

중요한 것:
✅ 충돌을 조기 발견
✅ 트레이드오프 의식적 결정
✅ ADR로 근거 기록
```

#### 4. 새 패밀리 발견!

```
A-C-A = 실시간 트랜잭션
- 금융 거래, IoT 제어, 자동화 시스템
- 특성: 정확 + 빠름 + 숫자 데이터

→ 6번째 패밀리 확정!
```

---

## 다음 단계

**사례집 완료 후**:
1. 패밀리별 DNA 시스템 요소 목록 정리
2. 패밀리 6개 → Guide에 반영
3. Manual에 패밀리별 상세 설명 추가

---

**버전 이력**:
- v1.0 (2025-11-12): 4개 사례 작성 (A-A-A, C-B-B, B-A-A, A-C-A)
