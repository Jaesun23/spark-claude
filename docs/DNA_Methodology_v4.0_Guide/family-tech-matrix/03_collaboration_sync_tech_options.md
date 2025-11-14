# 협업/동기화 패밀리 (B-A-A) - 기술 매트릭스

**작성일**: 2025-11-12  
**패밀리**: 협업/동기화 (B-A-A)  
**검증 사례**: Google Docs (OT), Figma (CRDT), Notion (블록 편집)

---

## Part 1: 패밀리가 요구하는 시스템 구조 ⭐⭐⭐

### 1.1 B-A-A 특성이 강제하는 것

#### B (점진적 실패) → 최종 일관성 필수

**특성**:
- 일부 사용자가 일시적으로 구형 데이터 표시 허용
- 낙관적 업데이트 (Optimistic UI)
- 충돌 자동 해결 또는 수동 병합
- Eventual Consistency

**강제되는 기술적 요구**:
```
✅ 충돌 해결 메커니즘 (CRDT, OT, Last-Write-Wins)
✅ 버전 관리 시스템
✅ 동기화 프로토콜
✅ 오프라인 편집 지원
```

**검증 사례**:
- Google Docs: Operational Transformation, 200ms 네트워크 지연 허용
- Notion: 블록 기반 최종 일관성, 낙관적 업데이트

---

#### A (구조화 데이터) → 스키마 기반 DB 필수

**특성**:
- 문서, 텍스트, 구조화된 블록
- 고정 스키마 또는 반구조화 JSON
- 트랜잭션 보장 (일부)
- 관계형 쿼리

**강제되는 기술적 요구**:
```
✅ RDBMS (PostgreSQL, MySQL)
✅ Document versioning
✅ Foreign key constraints
✅ ACID 트랜잭션 (선택적)
```

**검증 사례**:
- Notion: 블록 기반 구조, PostgreSQL 백엔드
- Figma: 파일 메타데이터 RDBMS 저장, 디자인 변경은 별도 처리

---

#### A (밀리초~초 응답) → 실시간 통신 필수

**특성**:
- 0~200ms 체감 지연 (사용자 느낌)
- 양방향 실시간 통신
- 다중 사용자 동시 작업
- 변경 사항 즉시 전파

**강제되는 기술적 요구**:
```
✅ WebSocket 또는 유사 기술
✅ Pub/Sub 메커니즘
✅ 사용자 프레즌스 추적
✅ 인메모리 캐시
```

**검증 사례**:
- Figma: WebSocket 기반, 문서당 별도 프로세스, 밀리초급 응답
- Linear: 실시간 이슈 업데이트, 다중 사용자 동시 편집

---

### 1.2 Bootstrap 필수 요소 (패밀리 강제)

B-A-A 패밀리는 다음 4가지 시스템 요소를 **반드시** 포함해야 합니다:

#### 1. RDBMS (필수!)
**역할**: 권위 있는 상태 저장, 메타데이터 관리
**이유**: 구조화 데이터(A) + 트랜잭션 보장
**선택지**: PostgreSQL, MySQL, CockroachDB

#### 2. WebSocket/실시간 통신 (필수!)
**역할**: 양방향 실시간 데이터 전송
**이유**: 밀리초 응답(A) + 다중 사용자 동시 작업
**선택지**: Socket.io, Native WebSocket, Server-Sent Events

#### 3. 동기화 엔진 (필수!)
**역할**: 충돌 해결, 상태 병합
**이유**: 점진적 실패(B) + 최종 일관성
**선택지**: Yjs, Automerge, 자체 구현(OT/CRDT)

#### 4. 캐시 레이어 (필수!)
**역할**: 빠른 읽기, 사용자 프레즌스 추적
**이유**: 밀리초 응답(A)
**선택지**: Redis, Memcached

---

## Part 2: Bootstrap 요소별 기술 선택 ⭐⭐⭐

### 2.1 RDBMS 선택

**패밀리 요구**:
- 권위 있는 상태 저장
- 버전 히스토리 관리
- 메타데이터 쿼리
- 트랜잭션 보장

---

#### 옵션 1: PostgreSQL

**핵심 스펙**:
- **처리량**: 초당 1만~10만 트랜잭션 (pgbench 기준)
- **레이턴시**: 평균 15ms (TPC-B 벤치마크)
- **동시 접속**: 100~1000 커넥션 (connection pooling)
- **스토리지**: TB급 문서, JSON 네이티브 지원

**비용**:
- **Self-hosted**: 월 $100~$1,000 (t3.medium~m5.xlarge)
- **AWS RDS**: 월 $70~$2,000 (db.t3.medium~db.r5.xlarge)
- **Azure Database**: 월 $60~$1,800

**장점**:
- 🔧 Full SQL 지원, 복잡한 쿼리 가능
- 📦 JSON/JSONB 네이티브, 반구조화 데이터 유연
- 🔒 ACID 트랜잭션, 데이터 무결성
- 🌐 풍부한 생태계, 검증된 안정성

**단점**:
- 📈 수직 확장 중심, 수평 확장 어려움
- 💰 관리형 서비스 비용 높음
- 🔧 세밀한 튜닝 필요 (인덱스, 쿼리 최적화)

**적합한 경우**:
- 중대형 프로젝트 (1,000+ 동시 사용자)
- 복잡한 쿼리 필요 (보고서, 분석)
- JSON 문서 + 관계형 혼합
- ACID 보장 필수

**검증 사례**: Notion, Linear, Dropbox Paper

---

#### 옵션 2: MySQL

**핵심 스펙**:
- **처리량**: 초당 5,000~50,000 트랜잭션
- **레이턴시**: 평균 10~20ms
- **동시 접속**: 100~500 커넥션 권장
- **스토리지**: TB급, InnoDB 엔진

**비용**:
- **Self-hosted**: 월 $50~$800
- **AWS RDS**: 월 $50~$1,500
- **Google Cloud SQL**: 월 $40~$1,200

**장점**:
- 💰 저렴한 비용, 널리 사용됨
- 🚀 빠른 읽기 성능 (InnoDB)
- 🔧 간단한 설정, 낮은 학습 곡선
- 📚 방대한 커뮤니티, 레퍼런스

**단점**:
- 📊 PostgreSQL 대비 부족한 기능 (JSON, Full-text)
- 🔒 트랜잭션 처리 제한적
- 📈 대규모 확장 어려움

**적합한 경우**:
- 소중형 프로젝트 (100~1,000 사용자)
- 예산 $500/월 이하
- 단순한 스키마
- 빠른 MVP 출시

**검증 사례**: Basecamp, GitHub (초기), WordPress 기반 협업 도구

---

#### 옵션 3: CockroachDB

**핵심 스펙**:
- **처리량**: 초당 10만+ 트랜잭션 (분산 환경)
- **레이턴시**: 평균 10~50ms (지역 간 100ms+)
- **확장**: 선형 수평 확장
- **가용성**: 99.99% (멀티 리전)

**비용**:
- **Serverless**: $1/GB 저장, $0.50/10M RU
- **Dedicated**: 월 $295~$5,000+
- **Self-hosted**: 월 $500~$3,000 (3노드 클러스터)

**장점**:
- 📈 무제한 수평 확장
- 🌍 멀티 리전, 지리적 분산
- 🔒 강한 일관성 + 고가용성
- 🔄 PostgreSQL 호환 (95%)

**단점**:
- 💰 높은 비용 (대규모 시)
- ⏱️ 지역 간 레이턴시 증가
- 🔧 복잡한 운영 (분산 시스템)
- 🆕 상대적 신생, 생태계 작음

**적합한 경우**:
- 글로벌 서비스 (멀티 리전 필수)
- 무제한 확장 필요
- 고가용성 99.99%+ 요구
- 예산 $5,000/월+ 가능

**검증 사례**: Figma (부분적), LaunchDarkly

---

#### RDBMS 비교표

| 항목 | PostgreSQL | MySQL | CockroachDB |
|------|-----------|-------|-------------|
| **처리량** | 10K~100K/s | 5K~50K/s | 100K+/s |
| **레이턴시** | 15ms | 10~20ms | 10~50ms |
| **확장** | 수직 | 수직 | 수평 |
| **비용** | $100~$2K/월 | $50~$1.5K/월 | $500~$5K/월 |
| **운영** | ⚙️⚙️ 중간 | ⚙️ 낮음 | ⚙️⚙️⚙️ 높음 |
| **JSON 지원** | JSONB (우수) | JSON (제한) | JSONB (우수) |

**의사결정 가이드**:
```
글로벌 멀티 리전? → CockroachDB
  └─ NO
     ↓
복잡한 쿼리/JSON 많음? → PostgreSQL
  └─ NO
     ↓
예산 <$500/월? → MySQL
  └─ NO → PostgreSQL
```

---

### 2.2 WebSocket/실시간 통신 선택

**패밀리 요구**:
- 양방향 실시간 통신
- 다중 사용자 지원
- 낮은 레이턴시 (<100ms)
- 자동 재연결

---

#### 옵션 1: Socket.io

**핵심 스펙**:
- **레이턴시**: 50~150ms (네트워크 포함)
- **동시 접속**: 1만~10만 (단일 서버)
- **fallback**: HTTP Long-polling 자동
- **처리량**: 초당 10만+ 메시지

**비용**:
- **Self-hosted**: 월 $100~$1,000 (t3.medium~m5.xlarge)
- **Heroku**: 월 $25~$500 (Dyno)
- **DigitalOcean**: 월 $12~$160

**장점**:
- 🚀 자동 재연결, Fallback 내장
- 🔧 Room, Namespace 기능 내장
- 📦 풍부한 에코시스템, 클라이언트 라이브러리
- 🔗 Broadcasting, Acknowledgements 간편

**단점**:
- 💰 메모리 사용 높음 (연결당 ~100KB)
- 📈 대규모는 Redis Adapter 필요
- ⚡ native WebSocket 대비 약간 느림
- 🔧 프로토콜 오버헤드

**적합한 경우**:
- 중소 규모 (1,000~10,000 동시 접속)
- 빠른 개발 우선
- Fallback 필수 (방화벽 환경)
- Room 기능 활용

**검증 사례**: Figma (초기), Slack (초기), 다수 스타트업

---

#### 옵션 2: Native WebSocket

**핵심 스펙**:
- **레이턴시**: 10~50ms (네트워크 포함)
- **동시 접속**: 5만~20만 (단일 서버)
- **처리량**: 초당 50만+ 메시지
- **메모리**: 연결당 ~10KB

**비용**:
- **Self-hosted**: 월 $50~$800 (경량)
- **AWS ELB**: 월 $20~$300 (트래픽 기반)
- **Nginx**: 월 $30~$500 (프록시)

**장점**:
- ⚡ 최고 성능, 최소 오버헤드
- 💰 낮은 메모리 사용
- 🔧 완전한 제어, 커스터마이징 가능
- 📡 표준 프로토콜, 브라우저 네이티브

**단점**:
- 🔨 Room, Broadcasting 직접 구현
- 🔄 재연결 로직 수동 구현
- 📦 생태계 작음, 보일러플레이트 많음
- 🚫 Fallback 없음

**적합한 경우**:
- 대규모 (10,000+ 동시 접속)
- 최고 성능 필수
- 커스텀 프로토콜 필요
- 직접 제어 선호

**검증 사례**: Google Docs (WebSocket + 자체 프로토콜), Figma (현재)

---

#### 옵션 3: Server-Sent Events (SSE)

**핵심 스펙**:
- **레이턴시**: 50~200ms
- **동시 접속**: 1만~5만 (단일 서버)
- **방향**: 서버 → 클라이언트 단방향
- **Fallback**: HTTP 기반, 방화벽 통과 용이

**비용**:
- **Self-hosted**: 월 $50~$500
- **Cloudflare Workers**: 월 $5~$50 (100K 요청)
- **Vercel**: 월 $20~$300

**장점**:
- 🔥 단순함, HTTP 기반
- 🔓 방화벽 통과 용이
- 🔄 자동 재연결 내장
- 💰 저렴한 비용

**단점**:
- 🚫 단방향 (서버 → 클라이언트만)
- 📈 제한된 확장성
- 🔧 클라이언트 → 서버는 HTTP POST
- ⏱️ 상대적 높은 레이턴시

**적합한 경우**:
- 단방향 업데이트만 (알림, 피드)
- 소규모 (100~1,000 사용자)
- 방화벽 제약 심함
- 단순한 아키텍처 선호

**검증 사례**: GitHub (알림), Linear (일부 업데이트)

---

#### WebSocket 비교표

| 항목 | Socket.io | Native WebSocket | SSE |
|------|----------|------------------|-----|
| **레이턴시** | 50~150ms | 10~50ms | 50~200ms |
| **동시 접속** | 10K~100K | 50K~200K | 10K~50K |
| **방향** | 양방향 | 양방향 | 단방향 |
| **비용** | $100~$1K/월 | $50~$800/월 | $50~$500/월 |
| **복잡도** | ⚙️ 낮음 | ⚙️⚙️⚙️ 높음 | ⚙️ 낮음 |

**의사결정 가이드**:
```
양방향 필수? 
  └─ NO → SSE
  └─ YES
     ↓
동시 접속 > 10,000? → Native WebSocket
  └─ NO
     ↓
빠른 개발 우선? → Socket.io
  └─ NO → Native WebSocket
```

---

### 2.3 동기화 엔진 선택

**패밀리 요구**:
- 충돌 자동 해결
- 오프라인 편집 지원
- 버전 관리
- 효율적 델타 동기화

---

#### 옵션 1: Yjs (CRDT)

**핵심 스펙**:
- **동기화 방식**: CRDT (Conflict-free Replicated Data Types)
- **레이턴시**: <10ms (로컬 병합)
- **네트워크**: Binary encoding, 효율적 델타
- **자료구조**: Text, Map, Array, XML

**비용**:
- **오픈소스**: 무료
- **Hocuspocus (서버)**: Self-hosted, 월 $50~$500
- **Y-Sweet (관리형)**: 월 $100~$2,000

**장점**:
- ⚡ 수학적으로 보장된 수렴
- 🔄 오프라인 편집 완벽 지원
- 📦 풍부한 자료구조, 확장 가능
- 🔧 Provider 다양 (WebSocket, WebRTC, IndexedDB)

**단점**:
- 📚 학습 곡선, CRDT 이해 필요
- 💾 메모리 사용 높음 (히스토리 보관)
- 🔧 복잡한 충돌 시나리오 예측 어려움
- 🚫 의미 보존 제한 (텍스트 편집 외)

**적합한 경우**:
- 텍스트 편집 중심 (문서, 코드)
- 오프라인 필수
- 자동 충돌 해결 우선
- 대규모 동시 편집

**검증 사례**: Notion (블록), CodeMirror, ProseMirror 통합

---

#### 옵션 2: Automerge (CRDT)

**핵심 스펙**:
- **동기화 방식**: CRDT (JSON-like)
- **레이턴시**: <20ms (로컬 병합)
- **네트워크**: Columnar encoding, 압축
- **자료구조**: JSON 호환 (Object, Array, Text)

**비용**:
- **오픈소스**: 무료
- **Automerge-Repo (서버)**: Self-hosted, 월 $50~$300

**장점**:
- 📄 JSON 친화적, 익숙한 API
- 🔒 강한 일관성, 수학적 보장
- 🔧 Time-travel, 버전 히스토리
- 🌐 P2P 동기화 지원

**단점**:
- ⏱️ 상대적 느림 (Yjs 대비)
- 💾 높은 메모리 사용 (전체 히스토리)
- 📦 생태계 작음, 커뮤니티 작음
- 🆕 상대적 신생, 프로덕션 사례 적음

**적합한 경우**:
- JSON 문서 중심 (설정, 메타데이터)
- Time-travel 필요
- P2P 아키텍처
- 강한 일관성 보장

**검증 사례**: Actual Budget, Pushpin, 일부 분산 앱

---

#### 옵션 3: 자체 구현 (OT/Last-Write-Wins)

**핵심 스펙**:
- **동기화 방식**: Operational Transformation 또는 LWW
- **레이턴시**: <5ms (로컬 적용)
- **네트워크**: 커스텀 프로토콜
- **복잡도**: 높음, 직접 구현

**비용**:
- **개발 비용**: 1~6개월 (엔지니어 투입)
- **운영 비용**: 월 $50~$500 (서버)

**장점**:
- 🎯 완전한 제어, 도메인 최적화
- ⚡ 최고 성능 가능 (최적화 시)
- 💰 라이선스 비용 없음
- 🔧 커스텀 충돌 전략

**단점**:
- 🔨 높은 개발 비용, 유지보수 부담
- 🐛 버그 위험, 엣지 케이스 많음
- 📚 전문 지식 필요 (OT, CRDT)
- ⏱️ 긴 개발 시간 (1~6개월)

**적합한 경우**:
- 특수 요구사항 (CRDT로 불가능)
- 장기 프로젝트, 전담 팀
- 레거시 시스템 통합
- 특정 도메인 로직

**검증 사례**: Google Docs (OT), Figma (LWW + 중앙 서버)

---

#### 동기화 엔진 비교표

| 항목 | Yjs | Automerge | 자체 구현 |
|------|-----|-----------|----------|
| **병합 속도** | <10ms | <20ms | <5ms (최적화 시) |
| **메모리** | 높음 | 매우 높음 | 낮음~중간 |
| **충돌 해결** | 자동 (CRDT) | 자동 (CRDT) | 수동/커스텀 |
| **개발 비용** | 낮음 | 낮음 | 매우 높음 |
| **생태계** | 풍부 | 작음 | 없음 |

**의사결정 가이드**:
```
텍스트 편집 중심? → Yjs
  └─ NO
     ↓
JSON 문서 + Time-travel? → Automerge
  └─ NO
     ↓
특수 요구사항 + 전담 팀? → 자체 구현
  └─ NO → Yjs (범용)
```

---

### 2.4 캐시 레이어 선택

**패밀리 요구**:
- 밀리초 미만 응답
- 사용자 프레즌스 추적
- 세션 관리
- Pub/Sub

---

#### 옵션 1: Redis

**핵심 스펙**:
- **레이턴시**: 0.15ms (GET)
- **처리량**: 초당 120만 트랜잭션
- **자료구조**: String, Hash, List, Set, Sorted Set (5가지)
- **기능**: Pub/Sub, 지속성 (AOF, RDB)

**비용**:
- **Self-hosted**: 월 $50~$500
- **AWS ElastiCache**: 월 $50~$1,000
- **Redis Cloud**: 월 $30~$2,000

**장점**:
- ⚡ 초고속, 다양한 자료구조
- 🔔 Pub/Sub 내장, Broadcasting 용이
- 💾 지속성 옵션, 데이터 손실 방지
- 📦 풍부한 클라이언트 라이브러리

**단점**:
- 💰 메모리 기반, 비용 높음
- 🔧 단일 스레드, CPU 1코어만 사용
- 📈 클러스터 설정 복잡 (대규모 시)

**적합한 경우**:
- 대부분의 협업 시스템
- Pub/Sub 필요
- 복잡한 캐시 로직
- 사용자 프레즌스 추적

**검증 사례**: GitHub, Figma, Linear

---

#### 옵션 2: Memcached

**핵심 스펙**:
- **레이턴시**: <0.1ms
- **처리량**: 초당 100만+ operations
- **자료구조**: Key-Value만
- **멀티 스레드**: CPU 멀티코어 활용

**비용**:
- **Self-hosted**: 월 $30~$300
- **AWS ElastiCache**: 월 $30~$500

**장점**:
- ⚡ 극도로 빠름, 단순함
- 💰 저렴한 비용
- 🔧 멀티 스레드, CPU 효율
- 📉 낮은 메모리 오버헤드

**단점**:
- 📊 단순한 자료구조 (Key-Value만)
- 🚫 Pub/Sub 없음
- 💾 지속성 없음, 재시작 시 데이터 손실

**적합한 경우**:
- 단순 캐싱만
- 최소 비용
- 초고속 필수
- Pub/Sub 불필요

---

#### 캐시 비교표

| 항목 | Redis | Memcached |
|------|-------|-----------|
| **레이턴시** | 0.15ms | <0.1ms |
| **자료구조** | 다양 | Key-Value |
| **Pub/Sub** | 있음 | 없음 |
| **비용** | 중간 | 낮음 |

**의사결정 가이드**:
```
Pub/Sub 필요? → Redis
  └─ NO
     ↓
복잡한 자료구조? → Redis
  └─ NO → Memcached
```

---

## Part 3: 도메인 선택 요소 (프로젝트별)

이 요소들은 **패밀리와 무관**하게 프로젝트 요구사항에 따라 선택합니다.

### 3.1 프론트엔드 프레임워크
- React, Vue, Svelte, Solid (패밀리 영향 없음, 프로젝트 선호도)

### 3.2 백엔드 언어/프레임워크
- Node.js (Express, NestJS, Fastify)
- Python (FastAPI, Django)
- Go (Gin, Echo)
(패밀리 영향 적음, 팀 역량 우선)

### 3.3 인증/권한
- Auth0, Clerk, Supabase Auth, Firebase Auth
(패밀리 무관, 보안 요구사항)

### 3.4 모니터링/로깅
- Prometheus + Grafana, Datadog, New Relic
(패밀리 무관, 운영 선호도)

---

## Part 4: Stage 2 통합

### 4.1 Layer 3 제약 반영 예시

**시나리오**: 디자인 협업 도구

**Layer 3 제약 발견**:
- 규제: GDPR, 유럽 데이터 저장 의무
- 팀: Node.js 경험, Python 없음
- 인프라: AWS 중심, 멀티 리전 불필요
- 비용: 초기 예산 $2,000/월

**기술 선택 영향**:
```
RDBMS:
- CockroachDB (선호) → PostgreSQL
- 이유: 멀티 리전 불필요, 비용 절감 ($5K → $2K/월)

동기화:
- 자체 구현 (선호) → Yjs
- 이유: 개발 기간 단축 (6개월 → 1주), 검증된 CRDT
```

---

### 4.2 충돌 해결 예시

**NFR 목표 vs Layer 3 제약**:

**충돌 1**: 글로벌 확장 A + 예산 제한
- NFR: 멀티 리전, 99.99% 가용성
- 제약: 예산 $2,000/월
- **해결**: PostgreSQL + Read Replica (리전별)
  - 트레이드오프: 단일 리전 쓰기, 99.9% SLA (99.99% 포기)

**충돌 2**: 오프라인 필수 A + 개발 기간
- NFR: 오프라인 편집, CRDT 자동 병합
- 제약: 3개월 출시
- **해결**: Yjs 도입 (자체 구현 포기)
  - 트레이드오프: 커스텀 충돌 전략 불가, 라이브러리 의존성

---

### 4.3 ADR 작성 준비

**선택한 기술 스택 정리**:
```
Bootstrap 필수:
✅ RDBMS: PostgreSQL (AWS RDS)
✅ WebSocket: Socket.io
✅ 동기화: Yjs
✅ 캐시: Redis (AWS ElastiCache)

도메인 선택:
✅ 백엔드: Node.js + NestJS
✅ 프론트엔드: React + TypeScript
✅ 인증: Clerk
✅ 모니터링: Datadog
```

**ADR 작성 대상**:

Bootstrap ADR:
1. PostgreSQL 선택 (MySQL, CockroachDB 대비)
2. Socket.io 선택 (Native WebSocket 대비)
3. Yjs 선택 (Automerge, 자체 구현 대비)
4. Redis 선택 (Memcached 대비)

도메인 ADR:
5. NestJS 선택 (Express 대비)
6. React 선택 (Vue, Svelte 대비)
7. Clerk 선택 (Auth0 대비)

---

## 📚 참고 자료

### 벤치마크
- [PostgreSQL pgbench 공식 문서](https://www.postgresql.org/docs/current/pgbench.html)
- [Socket.io Performance Tuning](https://socket.io/docs/v4/performance-tuning/)
- [Yjs Performance Benchmarks](https://github.com/yjs/yjs#benchmarks)

### 비용 계산기
- [AWS RDS Pricing](https://aws.amazon.com/rds/postgresql/pricing/)
- [CockroachDB Pricing](https://www.cockroachlabs.com/pricing/)
- [AWS ElastiCache Pricing](https://aws.amazon.com/elasticache/pricing/)

### 공식 문서
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [CockroachDB Documentation](https://www.cockroachlabs.com/docs/)
- [Socket.io Documentation](https://socket.io/docs/)
- [Yjs Documentation](https://docs.yjs.dev/)
- [Automerge Documentation](https://automerge.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

### 검증 사례
- Figma: [Rust + WebSocket 아키텍처](https://www.figma.com/blog/)
- Google Docs: [Operational Transformation](https://googledocs.blogspot.com/)
- Notion: [블록 기반 편집](https://www.notion.so/blog/)

---

**마지막 업데이트**: 2025-11-12  
**다음 검토**: 2026-02-12 (기술 스택 업데이트 반영)
