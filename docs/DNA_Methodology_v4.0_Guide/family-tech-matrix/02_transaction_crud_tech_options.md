# 트랜잭션/CRUD 패밀리 (A-A-B) - 기술 매트릭스

**작성일**: 2024-11-12  
**패밀리**: 트랜잭션/CRUD (A-A-B)  
**검증 사례**: Amazon 주문 시스템, Booking.com 예약, Stripe 결제, SAP ERP

---

## Part 1: 패밀리가 요구하는 시스템 구조 ⭐⭐⭐

### 1.1 A-A-B 특성이 강제하는 것

#### A (치명적 실패) → ACID 트랜잭션 필수

**특성**:
- 부분 성공 불가 (All-or-Nothing)
- 실패 = 재정 손실, 재고 불일치, 규제 위반
- 완전 롤백 메커니즘 필수
- 감사 추적 (Audit Trail) 의무

**강제되는 기술적 요구**:
```
✅ ACID 트랜잭션 DB 필수
✅ 격리 수준 제어 (Isolation Level)
✅ 분산 트랜잭션 조율 (2PC, Saga)
✅ 롤백 & 복구 메커니즘
✅ 데이터 무결성 제약
```

**검증 사례**:
- Amazon: 주문-재고-결제 트랜잭션, 실패 시 전체 롤백, 연간 수십억 건 처리
- Stripe: 결제 100% 정확성, PCI DSS 준수, 이중 청구 방지
- Booking.com: 객실 예약 트랜잭션, 초과 예약 방지

---

#### A (구조화 데이터) → 관계형 스키마 필수

**특성**:
- 명확한 엔티티 관계 (Order ↔ Customer ↔ Product)
- 참조 무결성 (Foreign Key Constraints)
- 복잡한 JOIN 쿼리 빈번
- 정규화된 스키마 설계

**강제되는 기술적 요구**:
```
✅ 관계형 데이터베이스 (RDBMS)
✅ 외래 키 제약 조건
✅ 스키마 마이그레이션 도구
✅ 인덱싱 전략
✅ 쿼리 최적화
```

**검증 사례**:
- Booking.com: 객실-호텔-예약-고객 복잡한 관계, 수백 개 테이블 JOIN
- SAP ERP: 수천 개 테이블 간 참조 무결성, 30년+ 스키마 진화

---

#### B (수초 응답) → 읽기 최적화 전략 필수

**특성**:
- 200ms~3초 응답 목표 (사용자 경험)
- 읽기 : 쓰기 = 90:10 (읽기 중심)
- 밀리초급 불필요 (A-A-A와 차이)
- 3초+ 지연 시 57% 사용자 이탈

**강제되는 기술적 요구**:
```
✅ 캐시 레이어 (Redis, Memcached)
✅ 읽기 복제본 (Read Replicas)
✅ 인덱스 전략 (B-tree, Hash)
✅ 쿼리 최적화 & 모니터링
✅ Connection Pooling
```

**검증 사례**:
- Amazon: 100ms 지연 = 매출 1% 손실 ($1.6B/년 추정)
- 산업 평균: 47% 사용자가 2초 내 로딩 기대, 3초+ 시 이탈

---

### 1.2 이 패밀리에 필요한 DNA 시스템 및 메인 서비스

#### DNA 11개 시스템 중 필요한 것

A-A-B 패밀리는 다음 DNA 시스템이 필요합니다:

| DNA 시스템 | 중요도 | 이유 |
|-----------|-------|------|
| 1. Testing | ✅ 필수 | 트랜잭션 로직 검증 |
| 2. Code Quality | ✅ 필수 | 비즈니스 로직 품질 |
| 3. Architecture | ✅ 필수 | 도메인 모듈 분리 |
| 4. Type System | ✅ 필수 | 엔티티 타입 안전성 |
| 5. **Error Handling** | **⭐⭐⭐ 매우 중요** | **트랜잭션 롤백, 보상 트랜잭션** |
| 6. Configuration | ✅ 필수 | DB 연결, 트랜잭션 타임아웃 |
| 7. **Identity & Access** | **⭐⭐⭐ 매우 중요** | **사용자 인증, RBAC, 감사 로그** |
| 8. Observability | ✅ 필수 | 쿼리 성능, 트랜잭션 추적 |
| 9. **API Gateway** | **⭐⭐⭐ 매우 중요** | **Rate Limiting, 인증, 버전 관리** |
| 10. **Resilience** | **⭐⭐⭐ 매우 중요** | **Circuit Breaker, 재시도, 타임아웃** |
| 11. Performance | ✅ 필수 | 쿼리 최적화, 인덱싱 |

**특별히 중요한 DNA 시스템 (⭐⭐⭐)**:
- **Identity & Access**: 사용자 인증 실패 = 보안 침해, RBAC 없으면 권한 관리 불가
- **API Gateway**: Rate limiting 없으면 DDoS 공격, 버전 관리 없으면 배포 중단
- **Error Handling**: 트랜잭션 롤백 실패 = 데이터 불일치, 보상 트랜잭션 필수
- **Resilience**: 외부 API 장애 시 전체 시스템 다운 방지

→ **Part 2.5에서 이 4가지 중 3가지 DNA 시스템의 기술 옵션을 다룹니다.**

#### 메인 서비스 필수 요소 (패밀리 강제)

A-A-B 패밀리는 다음 3가지 메인 서비스 기술을 **반드시** 포함해야 합니다:

#### 1. 관계형 데이터베이스 (필수!)
**역할**: ACID 트랜잭션, 참조 무결성, 복잡한 쿼리
**이유**: 치명적 실패(A) + 구조화 데이터(A)
**선택지**: PostgreSQL, MySQL, CockroachDB

#### 2. 캐시 레이어 (필수!)
**역할**: 읽기 성능 최적화 (<200ms)
**이유**: 수초 응답(B) + 높은 읽기 비율 (90%+)
**선택지**: Redis, Memcached

#### 3. 메시징 시스템 (강력 권장)
**역할**: 비동기 작업, 서비스 분리, 확장성
**이유**: 마이크로서비스 아키텍처, 이벤트 기반 통신
**선택지**: RabbitMQ, Kafka, AWS SQS

---

## Part 2: 메인 서비스 기술 선택 ⭐⭐⭐

### 2.1 관계형 데이터베이스 선택

**패밀리 요구**:
- ACID 트랜잭션 보장
- Serializable 격리 수준 지원
- 참조 무결성 제약
- 복잡한 JOIN 쿼리 성능
- 읽기/쓰기 확장성

---

#### 옵션 1: PostgreSQL

**핵심 스펙**:
- **읽기**: 50,000~100,000 QPS (최적화 시)
- **쓰기**: 15,000~30,000 TPS (SSD 기준)
- **트랜잭션 격리**: Serializable 완벽 지원
- **동시 연결**: 100~500 (PgBouncer로 10,000+)
- **데이터 크기**: 수백 TB (단일 인스턴스)

**비용**:
- **Self-hosted**: $0 (오픈소스)
- **AWS RDS**: $0.115/hour (db.t3.medium), 월 ~$84
- **Managed (Supabase)**: $25/월 (Hobby), $599/월 (Pro)
- **Enterprise**: $500~$5,000/월 (규모별)

**장점**:
- ⚡ 고급 ACID 지원: Serializable 격리 수준 완벽 구현
- 🔧 JSON/JSONB: 하이브리드 데이터 유연성
- 📈 성숙한 확장: 읽기 복제본, 파티셔닝, 샤딩
- 🌐 20년+ 검증: 엔터프라이즈급 안정성
- 🛠️ 풍부한 생태계: 마이그레이션, 모니터링 도구

**단점**:
- 🔧 복잡한 튜닝: 수백 개 설정 파라미터
- 📚 학습 곡선: 고급 기능 숙달 시간 필요
- 💰 고급 기능 비용: Replication, Clustering

**적합한 경우**:
- 복잡한 비즈니스 로직 (수십~수백 개 테이블)
- JSON과 관계형 혼합 데이터
- 장기 프로젝트 (10년+ 지원)
- 엔터프라이즈급 안정성 필요
- Serializable 트랜잭션 필수

**검증 사례**: Instagram (수십억 행), Discord (초당 120만 메시지), Stripe, Apple

---

#### 옵션 2: MySQL

**핵심 스펙**:
- **읽기**: 60,000~120,000 QPS (MyISAM, 단순 쿼리)
- **쓰기**: 10,000~20,000 TPS (InnoDB)
- **트랜잭션 격리**: Read Committed (기본), Serializable (제한)
- **동시 연결**: 100~300
- **데이터 크기**: 수십 TB (권장)

**비용**:
- **Self-hosted**: $0 (오픈소스)
- **AWS RDS**: $0.102/hour (db.t3.medium), 월 ~$74
- **Managed (PlanetScale)**: $15/월 (Scaler), $39/월 (Scaler Pro)
- **Enterprise**: $300~$3,000/월

**장점**:
- 📚 성숙도: LAMP 스택, 30년 역사
- 🔧 단순 설정: PostgreSQL 대비 쉬운 초기 설정
- 💰 저렴한 호스팅: 공유 호스팅 옵션 다수
- ⚡ 읽기 최적화: 단순 쿼리 고속 처리
- 🌐 광범위 채택: WordPress, Drupal 기본

**단점**:
- 🔒 제한적 트랜잭션: Serializable 성능 이슈
- 📊 약한 JSON 지원: PostgreSQL JSONB 대비 부족
- 🔧 고급 인덱스 부족: 부분 인덱스, 함수 인덱스 제한

**적합한 경우**:
- 읽기 중심 워크로드 (90%+ SELECT)
- 단순한 스키마 (수십 개 테이블)
- 예산 제약 (<$100/월)
- 팀이 MySQL 경험 풍부
- Read Committed 충분

**검증 사례**: Facebook (초기), WordPress (3천만 사이트), Shopify, GitHub (초기)

---

#### 옵션 3: CockroachDB

**핵심 스펙**:
- **읽기**: 30,000~50,000 QPS (단일 리전)
- **쓰기**: 10,000~15,000 TPS (다중 리전 시 감소)
- **트랜잭션 격리**: Serializable (분산 환경)
- **레이턴시**: +10~50ms (리전 간 증가)
- **데이터 크기**: PB급 (자동 샤딩)

**비용**:
- **Serverless**: $1 per 1M Request Units, 월 ~$50 (소규모)
- **Dedicated**: $0.50/vCPU/hour, 월 ~$360 (3노드 최소)
- **Enterprise**: $1,000~$10,000/월 (규모별)

**장점**:
- 🌐 전역 분산 ACID: 다중 리전 Serializable 트랜잭션
- 📈 자동 샤딩: 무한 수평 확장
- 🔄 PostgreSQL 호환: 기존 쿼리 재사용
- ☁️ 클라우드 네이티브: Kubernetes 친화적
- 🛡️ 내장 복제: 자동 failover

**단점**:
- 💰 높은 비용: PostgreSQL 대비 3~5배
- ⏱️ 레이턴시 증가: 분산 합의 오버헤드
- 🔧 운영 복잡도: 분산 시스템 전문 지식
- 📊 제한적 생태계: PostgreSQL 대비 도구 부족

**적합한 경우**:
- 글로벌 분산 필수 (다중 리전)
- 무한 확장 필요 (PB급 데이터)
- 지역 간 트랜잭션 빈번
- 예산 여유 ($500+/월)
- 클라우드 네이티브 환경

**검증 사례**: Bose, Lush Cosmetics, SpaceX Starlink, Hard Rock Digital

---

#### 데이터베이스 비교표

| 항목 | PostgreSQL | MySQL | CockroachDB |
|------|-----------|-------|-------------|
| **읽기 QPS** | 50K~100K | 60K~120K | 30K~50K |
| **쓰기 TPS** | 15K~30K | 10K~20K | 10K~15K |
| **격리 수준** | ⭐⭐⭐ Serializable | ⭐⭐ Read Committed | ⭐⭐⭐ Serializable (분산) |
| **비용 (중규모)** | $100~$300/월 | $80~$250/월 | $360~$1K/월 |
| **JSON 지원** | ⭐⭐⭐ 우수 | ⭐⭐ 보통 | ⭐⭐⭐ 우수 |
| **다중 리전** | 복제본 | 복제본 | ⭐⭐⭐ 네이티브 |
| **확장성** | 읽기 복제본 | 읽기 복제본 | 수평 자동 |
| **생태계** | ⭐⭐⭐ 풍부 | ⭐⭐⭐ 풍부 | ⭐⭐ 성장 중 |

**의사결정 가이드**:
```
글로벌 다중 리전 필수? → CockroachDB
  └─ NO
     ↓
Serializable 트랜잭션 필수?
  ├─ YES → PostgreSQL
  └─ NO
     ↓
예산 < $100/월?
  ├─ YES
  │  ├─ 복잡한 쿼리? → PostgreSQL (Managed)
  │  └─ 읽기 중심? → MySQL
  │
  └─ NO → PostgreSQL (장기 투자)
```

---

### 2.2 캐시 레이어 선택

**패밀리 요구**:
- 읽기 레이턴시 <10ms
- 높은 처리량 (100K+ ops/sec)
- TTL 관리
- 세션 저장 지원

---

#### 옵션 1: Redis

**핵심 스펙**:
- **레이턴시**: 0.15ms (GET, p99)
- **처리량**: 100,000~200,000 ops/sec (단일 인스턴스)
- **자료구조**: String, Hash, List, Set, Sorted Set, Stream, HyperLogLog
- **영속성**: RDB 스냅샷, AOF (Append-Only File)
- **메모리**: 1GB~수백 GB

**비용**:
- **Self-hosted**: $0 (오픈소스)
- **AWS ElastiCache**: $0.034/hour (cache.t3.micro), 월 ~$25
- **Redis Cloud**: $7/월 (250MB), $200/월 (10GB)
- **Enterprise**: $500~$5,000/월 (HA, 다중 리전)

**장점**:
- ⚡ 초고속: 0.15ms 평균 레이턴시
- 🔧 다양한 자료구조: 복잡한 캐싱 패턴 지원
- 📡 Pub/Sub: 실시간 알림 가능
- 💾 영속성: 재시작 후 데이터 복구
- 🌐 풍부한 클라이언트: 모든 주요 언어 지원

**단점**:
- 💰 메모리 기반: 디스크 대비 비쌈 (GB당)
- 🔧 단일 스레드: CPU 코어 1개만 활용
- 🛠️ 운영 복잡도: 클러스터링, 샤딩 수동 관리

**적합한 경우**:
- 세션 관리 필수
- API 응답 캐싱
- Rate Limiting
- Leaderboards, Counters
- Pub/Sub 필요
- 복잡한 자료구조 활용

**검증 사례**: Twitter (120만 TPS), GitHub, Stack Overflow, Pinterest

---

#### 옵션 2: Memcached

**핵심 스펙**:
- **레이턴시**: <0.1ms (마이크로초급)
- **처리량**: 120,000+ ops/sec
- **자료구조**: Key-Value만
- **영속성**: 없음 (휘발성)
- **메모리**: 1GB~수백 GB

**비용**:
- **Self-hosted**: $0 (오픈소스)
- **AWS ElastiCache**: $0.017/hour (cache.t3.micro), 월 ~$12
- **월 예상**: $30~$500

**장점**:
- 💰 Redis 대비 50% 저렴
- ⚡ 극도로 빠름: 마이크로초 레이턴시
- 🔧 멀티스레드: CPU 코어 활용 우수
- 🛠️ 단순함: 설정 & 운영 간단

**단점**:
- 📊 단순 자료구조: Key-Value만 지원
- 💾 영속성 없음: 재시작 시 데이터 손실
- 📡 Pub/Sub 없음: 이벤트 알림 불가
- 🔒 제한적 고급 기능: 트랜잭션, Lua 스크립트 없음

**적합한 경우**:
- 단순 Key-Value 캐싱만
- 예산 최소화 (<$50/월)
- 높은 동시성 필요 (멀티스레드)
- 영속성 불필요
- Facebook, Twitter 초기 규모

**검증 사례**: Facebook (역사적), Wikipedia, YouTube (콘텐츠 캐싱)

---

#### 캐시 비교표

| 항목 | Redis | Memcached |
|------|-------|-----------|
| **레이턴시** | 0.15ms | <0.1ms |
| **자료구조** | ⭐⭐⭐ 다양 | Key-Value만 |
| **영속성** | ⭐⭐ 옵션 있음 | ❌ 없음 |
| **비용** | 중간 | ⭐⭐⭐ 낮음 (50% 저렴) |
| **Pub/Sub** | ✅ | ❌ |
| **멀티스레드** | ❌ (단일) | ⭐⭐⭐ 우수 |
| **운영 복잡도** | 중간 | ⭐⭐⭐ 낮음 |

**의사결정 가이드**:
```
세션 관리 필요? → Redis
  └─ NO
     ↓
Pub/Sub 필요? → Redis
  └─ NO
     ↓
복잡한 자료구조? → Redis
  └─ NO
     ↓
예산 < $30/월? → Memcached
  └─ NO → Redis (범용)
```

---

### 2.3 메시징 시스템 선택

**패밀리 요구**:
- 비동기 작업 처리
- 서비스 간 분리
- At-Least-Once 전달 보장
- Task Queue 기능

---

#### 옵션 1: RabbitMQ

**핵심 스펙**:
- **처리량**: 10,000~50,000 msg/sec (단일 노드)
- **레이턴시**: 1~10ms (p99)
- **메시지 크기**: <128KB 권장, 512MB 최대
- **보장**: At-Least-Once, Persistent Queue
- **프로토콜**: AMQP 0-9-1

**비용**:
- **Self-hosted**: $0 (오픈소스)
- **CloudAMQP**: $13/월 (Tiger, 1M msg/월), $40/월 (Panda)
- **AWS AmazonMQ**: $0.50/hour (~$360/월, 3노드)
- **Enterprise**: $500~$3,000/월

**장점**:
- 📚 성숙도: 15년+ 검증, 엔터프라이즈급
- 🔧 유연한 라우팅: Exchange (Direct, Topic, Fanout, Headers)
- 💾 메시지 영속성: 디스크 저장 지원
- 🛠️ 관리 UI: 웹 기반 모니터링 & 관리
- 🌐 다양한 클라이언트: 모든 주요 언어

**단점**:
- 📉 제한적 확장: 클러스터링 복잡
- ⏱️ 부하 시 레이턴시: 큐 깊이 증가 시 성능 저하
- 🔧 운영 복잡도: 클러스터, Federation 수동 관리

**적합한 경우**:
- 전통적 메시징 패턴 (Queue, Pub/Sub)
- 복잡한 라우팅 규칙
- 메시지 영속성 필수
- 중소 규모 (초당 5만 미만)
- 예산 $50~$500/월

**검증 사례**: T-Mobile, Heroku, BBC, Reddit, Trivago

---

#### 옵션 2: Apache Kafka

**핵심 스펙**:
- **처리량**: 200K~2M msg/sec (클러스터)
- **레이턴시**: p99.9 <10ms
- **메시지 크기**: 1MB 기본, 10MB+ 설정 가능
- **보장**: At-Least-Once 기본, Exactly-Once 선택
- **보관**: 일~월 단위 (설정 가능)

**비용**:
- **Self-hosted**: $2,000~$10,000+/월 (3노드)
- **AWS MSK**: $0.21~$0.84/hour per vCPU, $3,000~$10,000/월
- **Confluent Cloud**: $5,000~$20,000/월 (eCKU 기반)

**장점**:
- ⚡ 초고속: 수백만 msg/sec
- 📈 무제한 확장: 파티션 추가로 선형 확장
- 💾 장기 보관: 이벤트 재생 가능
- 🔧 이벤트 소싱: 불변 로그 기반 아키텍처
- 🌐 풍부한 생태계: Kafka Connect, Kafka Streams

**단점**:
- 💰 높은 비용: RabbitMQ 대비 10배+
- 🧑‍💻 전문 인력: Kafka 전문가 필수
- ⏱️ 배포 시간: 1~4주 (self-hosted)
- 🔧 운영 복잡도: ZooKeeper, Replication 관리

**적합한 경우**:
- 초대규모 (초당 10만+ 메시지)
- 이벤트 소싱 아키텍처
- 장기 이벤트 재생 필요
- 대기업, 미션 크리티컬
- 예산 $5K+/월

**검증 사례**: LinkedIn, Netflix, Uber, Airbnb, Spotify

---

#### 옵션 3: AWS SQS

**핵심 스펙**:
- **처리량**: 3,000 msg/sec (Standard), 300 msg/sec (FIFO)
- **레이턴시**: 수십 ms
- **메시지 크기**: 256KB 최대
- **보장**: At-Least-Once (Standard), Exactly-Once (FIFO)
- **보관**: 최대 14일

**비용**:
- **Standard**: $0.40 per 1M requests
- **FIFO**: $0.50 per 1M requests
- **월 예상** (100만 msg): $40~$500

**장점**:
- 🤖 완전 관리형: 운영 부담 제로
- 💵 사용량 기반 과금: 예측 가능
- 🔗 AWS 통합: Lambda, EC2, ECS 쉬운 연동
- 📈 자동 확장: 무제한 처리량 (Standard)
- 🛡️ 높은 가용성: 99.9% SLA

**단점**:
- 🔒 AWS 종속: 멀티 클라우드 불가
- ⏱️ 제한적 처리량: FIFO 300 msg/sec
- 📊 단순 기능: Exchange, Routing 없음
- 💰 대규모 비용: 수억 메시지 시 급증

**적합한 경우**:
- AWS 중심 인프라
- 운영 간소화 최우선
- 중소 규모 (초당 3천 미만)
- 빠른 MVP 출시
- 예산 유연성

**검증 사례**: NASA JPL, Capital One, Change.org, BMW

---

#### 메시징 시스템 비교표

| 항목 | RabbitMQ | Kafka | AWS SQS |
|------|----------|-------|---------|
| **처리량** | 10K~50K/s | 200K~2M/s | 3K/s (Standard) |
| **레이턴시** | 1~10ms | <10ms | 수십 ms |
| **비용 (중규모)** | $50~$500/월 | $3K~$10K/월 | $40~$500/월 |
| **배포** | 1~3일 | 1~4주 | 즉시 |
| **운영** | ⚙️⚙️ 중간 | ⚙️⚙️⚙️ 높음 | ⚙️ 낮음 (관리형) |
| **메시지 보관** | 단기 | 일~월 | 최대 14일 |
| **확장성** | 제한적 | 무제한 | 자동 |
| **라우팅** | ⭐⭐⭐ 풍부 | Topic 기반 | 단순 |

**의사결정 가이드**:
```
처리량 > 10만/s? → Kafka
  └─ NO
     ↓
AWS 전용 OK? → SQS
  └─ NO → RabbitMQ
     ↓
운영 간소화 최우선? → SQS
  └─ NO
     ↓
복잡한 라우팅? → RabbitMQ
  └─ NO → SQS
```

---

## Part 2.5: 중요 DNA 시스템 기술 선택 🆕

이 섹션에서는 A-A-B 패밀리에서 **⭐⭐⭐ 매우 중요한 DNA 시스템 3가지**의 기술 옵션을 다룹니다.

### 2.5.1 Identity & Access (DNA #7) - 사용자 인증 및 권한 관리 ⭐⭐⭐

**패밀리 요구**:
- 사용자 인증 (OAuth2, OpenID Connect, SAML)
- RBAC (Role-Based Access Control) - 세밀한 권한 관리
- MFA (Multi-Factor Authentication) - 보안 강화
- 감사 로그 (Audit Trail) - 규제 준수
- 세션 관리 - 수초 응답 시간 유지

---

#### 옵션 1: Auth0

**핵심 스펙**:
- **처리량**: 100억+ 인증/월 (전역 처리)
- **레이턴시**: <50ms (글로벌 CDN)
- **가용성**: 99.99% SLA (Enterprise)
- **비용**: Free (25K MAU), Essentials $32/월 (500 MAU), Professional $220/월 (1K MAU), Enterprise $2,500/월

**장점**:
- 완전 관리형 (Managed SaaS), 운영 부담 제로
- 25K MAU까지 무료 (소규모 프로젝트 이상적)
- Universal Login, Passwordless, Social Login 즉시 사용
- 즉시 배포 가능 (5분 설정)
- 풍부한 SDK (React, Vue, Node.js, Python, Java 등)
- MFA, Bot Detection, Brute-Force Protection 내장
- 규제 준수 (GDPR, SOC2, ISO27001)

**단점**:
- MAU 제한으로 대규모 시 비용 급증 (10K MAU = $1,250~$1,595/월)
- 벤더 락인 (Okta 인수 후 가격 변동 우려)
- Enterprise 기능 (로그 내보내기, 고급 보안) 고가
- 커스터마이징 제한 (Rules/Actions로 일부 해결)

**적합한 경우**:
- 빠른 프로덕션 배포 (1주 이내)
- 운영 인력 부족 (DevOps 최소화)
- B2C 애플리케이션 (소셜 로그인 필수)
- 스타트업 (25K MAU 무료 활용)
- 규제 준수 필수 (HIPAA, PCI DSS)

**검증 사례**: Atlassian, Mozilla, Mazda, Schneider Electric

---

#### 옵션 2: AWS Cognito

**핵심 스펙**:
- **처리량**: 수백만 MAU 지원 (자동 스케일)
- **레이턴시**: <10ms (단일 리전)
- **가용성**: 99.9% SLA
- **비용**: Lite $0.0055/MAU (10K 무료), Essentials $0.015/MAU (10K 무료), Plus $0.02/MAU

**장점**:
- AWS 네이티브 통합 (Lambda, API Gateway, DynamoDB)
- 10K MAU 무료 (Lite, Essentials), 추가 비용 낮음
- 서버리스, 완전 관리형
- Cognito Identity Pools로 AWS 리소스 직접 접근
- IAM 통합 보안
- 예측 가능한 가격 (MAU 기반)

**단점**:
- AWS 벤더 락인 (멀티 클라우드 불가)
- UI/UX 제한적 (Hosted UI 커스터마이징 어려움)
- 문서 복잡함 (User Pools vs Identity Pools 혼란)
- Advanced Security Features 추가 비용 ($0.05/MAU)
- 크로스 리전 복제 미지원 (많은 사용자 요청 중)

**적합한 경우**:
- AWS 중심 인프라 (Lambda, API Gateway 사용)
- 서버리스 아키텍처
- 중간 규모 (10K~100K MAU)
- 예산 민감 (10K 무료 활용)
- 빠른 MVP 출시

**검증 사례**: 수많은 AWS 고객 (공개 사례 적음)

---

#### 옵션 3: Keycloak (Self-hosted / Managed)

**핵심 스펙**:
- **처리량**: 수만~수십만 MAU (클러스터 크기에 따라)
- **레이턴시**: <100ms (Self-hosted)
- **가용성**: 99.9%+ (HA 클러스터)
- **비용**: $0 (오픈소스) + 인프라 $510~$1,250/월 (Self-hosted), Managed $200~$1,000/월

**장점**:
- 완전한 커스터마이징 (소스 코드 접근)
- MAU 무제한 (인프라 비용만)
- 벤더 락인 없음 (온프레미스, 멀티 클라우드)
- 표준 프로토콜 (OIDC, OAuth2, SAML) 완벽 지원
- Active Directory, LDAP 통합
- Red Hat 상용 지원 가능 (Red Hat SSO)

**단점**:
- 높은 운영 부담 (HA 클러스터, DB, 모니터링)
- 배포 복잡도 (2~6개월 소요)
- 전문 인력 필요 (IAM 엔지니어 1~2명)
- 인프라 비용 (3×4 vCPU VM + 2×2 vCPU VM = $910/월)
- 유지보수 비용 (주 3시간 = $360/월)
- 러닝 커브 높음

**적합한 경우**:
- 대규모 사용자 (100K+ MAU, MAU 당 비용 회피)
- 온프레미스 필수 (금융, 정부, 의료)
- 완전한 제어 필요 (커스텀 인증 흐름)
- 장기 프로젝트 (5년+)
- 운영 역량 있는 팀

**검증 사례**: Red Hat, Cisco, CERN, 유럽 정부 기관

---

**의사결정 플로우차트**:
```
AWS 올인 환경?
├─ YES → 예산 < $500/월?
│   ├─ YES → AWS Cognito (옵션 2)
│   └─ NO → Auth0 (옵션 1)
└─ NO → MAU > 100K?
    ├─ YES → 운영 역량 있나?
    │   ├─ YES → Keycloak (옵션 3)
    │   └─ NO → Auth0 Enterprise (옵션 1)
    └─ NO → 빠른 배포 필요?
        ├─ YES → Auth0 (옵션 1)
        └─ NO → Keycloak Managed (옵션 3)
```

---

## Part 3: 도메인 선택 요소 (프로젝트별)

이 요소들은 **패밀리와 무관**하게 프로젝트 요구사항에 따라 선택합니다.

### 3.1 프론트엔드 프레임워크
- React, Vue, Angular, Svelte
- (패밀리 영향 없음, 팀 선호도 & 프로젝트 요구사항)

### 3.2 백엔드 언어/프레임워크
- Node.js (Express, NestJS), Python (FastAPI, Django), Java (Spring Boot), Go, C# (.NET)
- (패밀리 영향 적음, 팀 역량 & 성능 요구사항 우선)

### 3.3 인증/권한
- Auth0, AWS Cognito, Keycloak, Firebase Auth
- (패밀리 무관, 보안 요구사항 & 예산)

### 3.4 모니터링/로깅
- Prometheus + Grafana, ELK Stack, Datadog, New Relic, CloudWatch
- (패밀리 무관, 운영 선호도 & 예산)

### 3.5 ORM/쿼리 빌더
- TypeORM, Prisma, Sequelize (Node.js), SQLAlchemy (Python), JPA/Hibernate (Java)
- (DB 선택에 영향받음, 언어별 생태계)

---

## Part 4: Stage 2 통합

### 4.1 Layer 3 제약 반영 예시

**시나리오**: 전자상거래 주문 시스템

**Layer 3 제약 발견**:
- **팀 역량**: Python 팀 (Java 경험 부족)
- **인프라**: AWS 전용, 온프레미스 불가
- **예산**: 월 $500 이하
- **규정**: PCI DSS 준수 (결제 정보)

**기술 선택 영향**:
```
데이터베이스:
- CockroachDB (선호) → PostgreSQL RDS
- 이유: 예산 제약 ($360 vs $100), 다중 리전 불필요

캐시:
- Redis 유지
- 이유: 세션 관리 필수, PCI DSS 암호화 지원

메시징:
- Kafka (선호) → AWS SQS
- 이유: 예산 & 운영 간소화, AWS 전용 인프라
```

**재설계된 아키텍처**:
```
Frontend (React) → API Gateway
                      ↓
              Lambda (Python)
                      ↓
    PostgreSQL RDS + Redis ElastiCache + SQS
```

---

### 4.2 충돌 해결 예시

**NFR 목표 vs Layer 3 제약**:

**충돌 1**: 100% 정확성 A + 예산 $500/월
- **NFR**: Serializable 트랜잭션, 다중 리전
- **제약**: 예산 부족 (CockroachDB $360 최소)
- **해결**: PostgreSQL Serializable + 읽기 복제본 ($150/월)
  - 트레이드오프: 다중 리전 포기, 단일 리전 HA

**충돌 2**: 200ms 응답 A + Python 팀
- **NFR**: 캐싱, 읽기 복제본, 인덱싱
- **제약**: Python ORM 성능 (vs Java/Go)
- **해결**: Redis 적극 활용 + Async Python (FastAPI)
  - 읽기 90% 캐시 Hit, DB 부하 10%로 감소

**충돌 3**: 확장성 B + 메시징 경험 없음
- **NFR**: 비동기 처리, 서비스 분리
- **제약**: RabbitMQ/Kafka 학습 시간 부족
- **해결**: AWS SQS + Lambda (관리형)
  - 트레이드오프: AWS 종속, 처리량 제한 (3K/s)

---

### 4.3 ADR 작성 준비

**선택한 기술 스택 정리**:
```
Bootstrap 필수:
✅ DB: PostgreSQL RDS (db.t3.medium)
✅ 캐시: Redis ElastiCache (cache.t3.medium)
✅ 메시징: AWS SQS (Standard)

도메인 선택:
✅ 백엔드: Python 3.12 + FastAPI
✅ ORM: SQLAlchemy + Alembic
✅ 프론트엔드: React 18 + TypeScript
✅ 인증: AWS Cognito
✅ 모니터링: CloudWatch + Grafana
```

**ADR 작성 대상**:
1. **ADR-001**: PostgreSQL vs CockroachDB 선택 (예산 제약)
2. **ADR-002**: AWS SQS vs RabbitMQ 선택 (운영 간소화)
3. **ADR-003**: Redis 캐싱 전략 (Cache-Aside vs Write-Through)
4. **ADR-004**: Read Replicas 구성 (읽기 부하 분산)
5. **ADR-005**: Serializable 격리 수준 적용 범위 (성능 vs 정확성)

**각 ADR 포함 내용**:
- Context: 비즈니스 요구사항 & Layer 3 제약
- Decision: 선택한 기술 & 이유
- Consequences: 장단점, 트레이드오프
- Alternatives: 고려했던 다른 옵션

---

## 📚 참고 자료

### 벤치마크
- [PostgreSQL Performance Tuning](https://www.postgresql.org/docs/current/performance-tips.html)
- [MySQL Performance Documentation](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [Redis Benchmarks](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/)
- [RabbitMQ Performance Measurements](https://www.rabbitmq.com/blog/2012/04/25/rabbitmq-performance-measurements-part-2)

### 비용 계산기
- [AWS Pricing Calculator](https://calculator.aws.amazon.com/)
- [PlanetScale Pricing](https://planetscale.com/pricing)
- [Supabase Pricing](https://supabase.com/pricing)
- [Redis Cloud Pricing](https://redis.io/pricing/)

### 공식 문서
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [CockroachDB Documentation](https://www.cockroachlabs.com/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [AWS SQS Documentation](https://docs.aws.amazon.com/sqs/)

### 검증 사례
- Amazon: [Amazon's Architecture](https://aws.amazon.com/architecture/)
- Stripe: [Stripe Engineering Blog](https://stripe.com/blog/engineering)
- Booking.com: [Booking.com Tech Blog](https://blog.booking.com/)
- Instagram: [Instagram Engineering Blog](https://instagram-engineering.com/)

---

**마지막 업데이트**: 2024-11-12  
**다음 검토**: 2025-02-12 (기술 스택 업데이트 반영)


### 2.5.2 API Gateway (DNA #9) - 라우팅 및 Rate Limiting ⭐⭐⭐

**패밀리 요구**:
- Rate Limiting - DDoS 방지, 서비스 보호
- 인증/권한 통합 - Identity 시스템과 연동
- API 버전 관리 - 배포 중단 없는 업그레이드
- 로드 밸런싱 - 트래픽 분산
- 모니터링 & 로깅 - 성능 추적, 디버깅

---

#### 옵션 1: Kong API Gateway

**핵심 스펙**:
- **처리량**: 100,000+ RPS (단일 노드)
- **레이턴시**: p99 <10ms (프록시 오버헤드)
- **Rate Limiting**: 초당 요청, 분당, 시간당 제한 가능
- **플러그인**: 50+ 공식 플러그인, 커스텀 Lua 플러그인
- **가용성**: 99.99% (클러스터 모드)

**비용**:
- **Kong Gateway OSS**: $0 (오픈소스)
- **Kong Konnect Free**: $0 (10 서비스)
- **Kong Konnect Plus**: $249/월 (무제한 서비스)
- **Kong Konnect Enterprise**: $2,500+/월 (고급 보안, 지원)
- **Self-hosted 인프라**: $200~$600/월 (3노드 HA)

**장점**:
- 고성능 (Nginx 기반, LuaJIT)
- 풍부한 플러그인 생태계 (인증, Rate Limiting, Transformation)
- Kubernetes 네이티브 (Kong Ingress Controller)
- 활발한 커뮤니티, 15년+ 검증
- Declarative 설정 (YAML/JSON)
- 멀티 프로토콜 (HTTP, gRPC, WebSocket, TCP/UDP)
- DB-less 모드 지원 (설정 파일 기반)

**단점**:
- Lua 학습 필요 (커스텀 플러그인 시)
- Enterprise 기능 고가 (RBAC, 분석)
- 클러스터 설정 복잡도 (PostgreSQL/Cassandra 필요)
- 메모리 사용량 높음 (150~300MB per 인스턴스)

**적합한 경우**:
- Kubernetes 환경 (Ingress Controller)
- 고성능 필수 (100K+ RPS)
- 플러그인 확장성 필요
- 오픈소스 우선 (벤더 락인 회피)
- 장기 프로젝트 (5년+)

**검증 사례**: NASA, Cisco, Samsung, Yahoo, T-Mobile

---

#### 옵션 2: AWS API Gateway

**핵심 스펙**:
- **처리량**: 10,000 RPS (기본), Throttling 설정 가능
- **레이턴시**: <50ms (통합 지연 포함)
- **Rate Limiting**: 계정당, API당, 메서드당 설정
- **통합**: Lambda, EC2, HTTP 엔드포인트
- **가용성**: 99.95% SLA (REST API), 99.99% (HTTP API)

**비용**:
- **HTTP API**: $1.00 per 1M requests
- **REST API**: $3.50 per 1M requests
- **WebSocket API**: $1.00 per 1M messages
- **월 예상** (100만 요청): $1~$3.50
- **추가 비용**: 데이터 전송, CloudWatch 로그

**장점**:
- 완전 관리형 (운영 부담 제로)
- AWS 네이티브 통합 (Lambda, Cognito, IAM)
- 자동 스케일링 (무제한 트래픽)
- 빠른 배포 (5~10분 설정)
- 저렴한 비용 (HTTP API $1/1M 요청)
- API Keys, Usage Plans 내장
- OpenAPI 스펙 지원

**단점**:
- AWS 벤더 락인 (멀티 클라우드 불가)
- 10K RPS 초과 시 AWS 지원팀 요청 필요
- 고급 Rate Limiting 제한적 (IP 기반만)
- WebSocket 30분 연결 제한
- 복잡한 변환 로직 어려움
- Latency 증가 가능 (통합 오버헤드)

**적합한 경우**:
- AWS 중심 인프라
- 서버리스 아키텍처 (Lambda)
- 빠른 MVP 출시 (1주 이내)
- 운영 최소화 우선
- 중소 규모 (10K RPS 이하)

**검증 사례**: Expedia, Coca-Cola, Change.org (공식 사례 다수)

---

#### 옵션 3: Traefik

**핵심 스펙**:
- **처리량**: 50,000~80,000 RPS (단일 노드)
- **레이턴시**: p99 <5ms (매우 낮은 오버헤드)
- **Rate Limiting**: 평균 요청률, 버스트 제한
- **자동 발견**: Docker, Kubernetes, Consul 자동 감지
- **가용성**: 99.9%+ (HA 구성 시)

**비용**:
- **Traefik OSS**: $0 (오픈소스)
- **Traefik Enterprise**: $2,000~$10,000/년 (클러스터당)
- **Self-hosted 인프라**: $100~$400/월 (2~3노드)

**장점**:
- 클라우드 네이티브 (Kubernetes, Docker 자동 발견)
- 자동 HTTPS (Let's Encrypt)
- 실시간 설정 업데이트 (재시작 불필요)
- 매우 가벼움 (50MB 메모리)
- Go 기반 (단일 바이너리, 배포 간편)
- 직관적 웹 UI (Traefik Dashboard)
- 멀티 프로토콜 (HTTP, gRPC, TCP, UDP)

**단점**:
- 플러그인 생태계 작음 (Kong 대비)
- 문서 분산 (v1, v2, v3 차이)
- Enterprise 기능 제한적 (Rate Limiting은 Enterprise만)
- 커뮤니티 작음 (Kong 대비)
- 고급 Rate Limiting 부족 (Redis 기반 분산 X)

**적합한 경우**:
- Kubernetes/Docker 환경
- 마이크로서비스 아키텍처
- 가벼운 게이트웨이 선호
- 자동 발견 필수
- 예산 최소화 (<$500/월)

**검증 사례**: Zed, Containous, 수많은 K8s 프로젝트

---

#### API Gateway 비교표

| 항목 | Kong | AWS API Gateway | Traefik |
|------|------|-----------------|---------|
| **처리량** | 100K+ RPS | 10K RPS (기본) | 50K~80K RPS |
| **레이턴시** | <10ms | <50ms | <5ms |
| **비용 (중규모)** | $200~$600/월 | $100~$500/월 | $100~$400/월 |
| **Rate Limiting** | ⭐⭐⭐ 고급 | ⭐⭐ 기본 | ⭐⭐ 기본 |
| **플러그인** | ⭐⭐⭐ 풍부 | AWS 통합 | ⭐⭐ 제한적 |
| **K8s 통합** | ⭐⭐⭐ 네이티브 | 가능 | ⭐⭐⭐ 네이티브 |
| **운영** | ⚙️⚙️ 중간 | ⚙️ 낮음 (관리형) | ⚙️⚙️ 중간 |
| **벤더 락인** | ❌ 없음 | ⚠️ AWS | ❌ 없음 |

**의사결정 플로우차트**:
```
AWS 올인 환경?
├─ YES → 서버리스 (Lambda)?
│   ├─ YES → AWS API Gateway (옵션 2)
│   └─ NO → Kong (옵션 1)
└─ NO → Kubernetes 환경?
    ├─ YES → 예산 < $500/월?
    │   ├─ YES → Traefik (옵션 3)
    │   └─ NO → 처리량 > 80K RPS?
    │       ├─ YES → Kong (옵션 1)
    │       └─ NO → Traefik (옵션 3)
    └─ NO → 플러그인 필수?
        ├─ YES → Kong (옵션 1)
        └─ NO → Traefik (옵션 3)
```

---

### 2.5.3 Error Handling (DNA #5) - 트랜잭션 롤백 및 보상 ⭐⭐⭐

**패밀리 요구**:
- 트랜잭션 롤백 메커니즘 - 전체 작업 취소
- 보상 트랜잭션 (Compensating Transaction) - 분산 트랜잭션 실패 복구
- 3-Level 에러 전략 - Domain, Application, Infrastructure 구분
- Context 전파 - 에러 원인 추적
- 타입 안전성 - 컴파일 타임 검증 (선택적)

---

#### 옵션 1: Custom Error Types (언어 표준)

**핵심 스펙**:
- **타입 안전성**: TypeScript/Rust에서 완벽한 타입 체킹
- **성능**: 제로 오버헤드 (런타임 비용 없음)
- **유연성**: 프로젝트 요구사항에 정확히 맞춤
- **학습 곡선**: 중간 (타입 시스템 이해 필요)

**비용**:
- $0 (언어 표준 기능)

**장점**:
- 완전한 제어 (에러 구조, 메시지 형식)
- 타입 안전성 (컴파일 타임 검증)
- 도메인 특화 에러 (비즈니스 로직 반영)
- 제로 의존성 (외부 라이브러리 불필요)
- 성능 최적화 가능
- IDE 자동완성 지원
- 디버깅 용이 (명확한 에러 타입)

**단점**:
- 보일러플레이트 코드 많음
- 각 에러마다 타입 정의 필요
- 팀 컨벤션 통일 어려움
- 에러 변환 수동 구현
- Backtrace 수동 관리

**적합한 경우**:
- 복잡한 도메인 로직 (수십 개 에러 타입)
- 타입 안전성 최우선
- 외부 의존성 최소화
- 팀 역량 높음 (타입 시스템 숙달)
- 장기 프로젝트 (유지보수 고려)

**검증 사례**: 대부분의 TypeScript/Rust 엔터프라이즈 프로젝트

**예시 (TypeScript)**:
```typescript
// 도메인별 에러 정의
class OrderError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: unknown
  ) {
    super(message);
    this.name = 'OrderError';
  }
}

class PaymentError extends Error {
  constructor(
    message: string,
    public transactionId: string,
    public amount: number
  ) {
    super(message);
    this.name = 'PaymentError';
  }
}

// 사용 예시
async function createOrder(data: OrderData): Promise<Order> {
  if (!data.items.length) {
    throw new OrderError('Empty order', 'ORDER_EMPTY');
  }
  
  try {
    const payment = await processPayment(data);
    return await saveOrder(data, payment);
  } catch (e) {
    if (e instanceof PaymentError) {
      // 보상 트랜잭션: 재고 복구
      await restoreInventory(data.items);
      throw new OrderError(
        'Payment failed',
        'PAYMENT_FAILED',
        { transactionId: e.transactionId }
      );
    }
    throw e;
  }
}
```

---

#### 옵션 2: thiserror (Rust 전용)

**핵심 스펙**:
- **타입 안전성**: 완벽한 컴파일 타임 검증
- **성능**: Zero-cost abstraction
- **derive 매크로**: 자동 Error trait 구현
- **Backtrace**: 자동 캡처 (nightly)

**비용**:
- $0 (오픈소스)

**장점**:
- 간결한 코드 (#[derive(Error)] 한 줄)
- 자동 Display 구현 (포맷 문자열)
- 자동 From 구현 (#[from] 속성)
- Backtrace 자동 전파
- 타입 안전성 (Result<T, E>)
- 제로 런타임 오버헤드
- IDE 자동완성 우수

**단점**:
- Rust 전용 (다른 언어 불가)
- nightly 컴파일러 필요 (Backtrace 기능)
- derive 매크로 학습 필요
- 복잡한 에러 계층 시 코드 길어짐

**적합한 경우**:
- Rust 프로젝트
- 타입 안전성 최우선
- 보일러플레이트 최소화
- 고성능 필수 (금융, 실시간)
- 팀이 Rust 숙련

**검증 사례**: Tokio, Serde, Actix, rust-analyzer

**예시 (Rust)**:
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum OrderError {
    #[error("order is empty")]
    EmptyOrder,
    
    #[error("payment failed: {transaction_id}")]
    PaymentFailed {
        transaction_id: String,
        #[from]
        source: PaymentError,
    },
    
    #[error("inventory insufficient for item {item_id}")]
    InsufficientInventory {
        item_id: String,
        required: u32,
        available: u32,
    },
}

#[derive(Error, Debug)]
#[error("payment error: {message}")]
pub struct PaymentError {
    message: String,
    amount: f64,
}

// 사용 예시
async fn create_order(data: OrderData) -> Result<Order, OrderError> {
    if data.items.is_empty() {
        return Err(OrderError::EmptyOrder);
    }
    
    let payment = process_payment(&data)
        .await?; // PaymentError 자동 변환 (From impl)
    
    save_order(data, payment).await
}
```

---

#### 옵션 3: anyhow (Rust 전용)

**핵심 스펙**:
- **유연성**: 모든 에러 타입 수용
- **Context**: 에러 체인, 메시지 추가
- **Backtrace**: 자동 캡처
- **간편함**: 빠른 프로토타이핑

**비용**:
- $0 (오픈소스)

**장점**:
- 극도로 간단 (anyhow::Result<T> 만으로 충분)
- Context 체이닝 (.context() 메서드)
- Downcast 지원 (특정 에러 타입 검사)
- Backtrace 자동 포함
- ? 연산자 편리 (모든 에러 자동 전파)
- 빠른 프로토타이핑
- 학습 곡선 낮음

**단점**:
- 타입 안전성 약함 (anyhow::Error는 trait object)
- 라이브러리에 부적합 (API 경계에서 타입 정보 손실)
- 에러 타입 구별 어려움 (Downcast 필요)
- 애플리케이션 전용 (라이브러리는 thiserror 권장)

**적합한 경우**:
- 빠른 프로토타이핑 (MVP, POC)
- 애플리케이션 코드 (라이브러리 아님)
- 간편함 최우선
- 에러 타입 구별 불필요
- 팀이 Rust 초보

**검증 사례**: 많은 Rust CLI 도구, 애플리케이션

**예시 (Rust)**:
```rust
use anyhow::{Context, Result, bail};

async fn create_order(data: OrderData) -> Result<Order> {
    if data.items.is_empty() {
        bail!("Order cannot be empty");
    }
    
    let payment = process_payment(&data)
        .await
        .context("Failed to process payment")?;
    
    save_order(data, payment)
        .await
        .with_context(|| {
            format!("Failed to save order for user {}", data.user_id)
        })
}

// 에러 핸들링
match create_order(data).await {
    Ok(order) => println!("Order created: {}", order.id),
    Err(e) => {
        eprintln!("Error: {:?}", e);
        // 에러 체인 출력
        for cause in e.chain() {
            eprintln!("  Caused by: {}", cause);
        }
    }
}
```

---

#### Error Handling 비교표

| 항목 | Custom Types | thiserror | anyhow |
|------|--------------|-----------|--------|
| **타입 안전성** | ⭐⭐⭐ 완벽 | ⭐⭐⭐ 완벽 | ⭐⭐ 약함 |
| **보일러플레이트** | ⚠️ 많음 | ⭐⭐⭐ 적음 | ⭐⭐⭐ 최소 |
| **학습 곡선** | 중간 | 중간 | ⭐⭐⭐ 낮음 |
| **성능** | ⭐⭐⭐ 최고 | ⭐⭐⭐ 최고 | ⭐⭐ 약간 오버헤드 |
| **Backtrace** | 수동 | ⭐⭐⭐ 자동 | ⭐⭐⭐ 자동 |
| **Context 전파** | 수동 | 수동 | ⭐⭐⭐ 자동 |
| **라이브러리 적합** | ⭐⭐⭐ 우수 | ⭐⭐⭐ 우수 | ❌ 부적합 |
| **언어 지원** | 모든 언어 | Rust만 | Rust만 |

**의사결정 플로우차트 (Rust 프로젝트)**:
```
라이브러리 개발?
├─ YES → thiserror (옵션 2)
└─ NO → 빠른 프로토타이핑?
    ├─ YES → anyhow (옵션 3)
    └─ NO → 복잡한 에러 계층?
        ├─ YES → 타입 안전성 필수?
        │   ├─ YES → thiserror (옵션 2)
        │   └─ NO → anyhow (옵션 3)
        └─ NO → 간편함 우선?
            ├─ YES → anyhow (옵션 3)
            └─ NO → thiserror (옵션 2)
```

**의사결정 플로우차트 (TypeScript/JavaScript)**:
```
Custom Error Types (옵션 1) 사용
- 표준 Error 클래스 확장
- 도메인별 에러 클래스 정의
- Result<T, E> 패턴 고려 (ts-results 라이브러리)
```

---

