# 실시간 스트리밍 패밀리 (B-C-A) - 기술 매트릭스

**작성일**: 2024-11-12  
**패밀리**: 실시간 스트리밍 (B-C-A)  
**검증 사례**: Netflix RDG (100만 msg/s), Uber GPS, Twitter 타임라인

---

## Part 1: 패밀리가 요구하는 시스템 구조 ⭐⭐⭐

### 1.1 B-C-A 특성이 강제하는 것

#### B (점진적 실패) → 이벤트 스트리밍 필수

**특성**:
- 일부 메시지 손실 허용
- 버퍼링 및 재시도 메커니즘
- 최종 일관성 (Eventual Consistency)
- At-least-once 전달 보장

**강제되는 기술적 요구**:
```
✅ 메시지 큐/스트림 플랫폼 필수
✅ 이벤트 재생(replay) 기능
✅ Dead Letter Queue (DLQ)
✅ 체크포인트/오프셋 관리
```

**검증 사례**:
- Netflix: Kafka at-least-once, 메시지 재생으로 장애 복구
- Uber: GPS 데이터 일시 손실 허용, 보간(interpolation)으로 복구

---

#### C (비구조화 데이터) → 유연한 스키마 필수

**특성**:
- 이벤트 스트림, 시계열 데이터
- JSON, Protobuf 같은 유연한 포맷
- 스키마 진화 (Schema Evolution)
- 가변 필드 구조

**강제되는 기술적 요구**:
```
✅ NoSQL 또는 시계열 DB
✅ Schema Registry (선택)
✅ JSON/Protobuf 직렬화
✅ 동적 필드 처리
```

**검증 사례**:
- Twitter: 트윗 이벤트의 가변 메타데이터 (리트윗, 인용, 미디어)
- IoT: 센서별 다른 데이터 구조 (온도, 습도, 진동 등)

---

#### A (밀리초~수초 응답) → 저지연 아키텍처 필수

**특성**:
- p99 < 5초 목표
- 실시간 느낌 제공
- 고처리량 요구
- 수평 확장 가능

**강제되는 기술적 요구**:
```
✅ 파티셔닝 (병렬 처리)
✅ 인메모리 캐시
✅ 비동기 처리
✅ 수평 확장 아키텍처
```

**검증 사례**:
- Uber GPS: 2-5초 위치 업데이트, 초당 100만 쿼리
- Netflix: 5초 미만 추천 업데이트

---

### 1.2 Bootstrap 필수 요소 (패밀리 강제)

B-C-A 패밀리는 다음 3가지 시스템 요소를 **반드시** 포함해야 합니다:

#### 1. 스트리밍 플랫폼 (필수!)
**역할**: 이벤트 수집, 파티셔닝, 전달
**이유**: 점진적 실패(B) + 연속 스트림(C)
**선택지**: Kafka, Kinesis, RabbitMQ

#### 2. 시계열 DB (필수!)
**역할**: 이벤트 저장, 시간 순 조회
**이유**: 비구조화 데이터(C) + 빠른 쓰기(A)
**선택지**: Cassandra, DynamoDB, TimescaleDB

#### 3. 캐시 레이어 (필수!)
**역할**: 핫 데이터 빠른 조회
**이유**: 밀리초 응답(A)
**선택지**: Redis, Memcached

---

## Part 2: Bootstrap 요소별 기술 선택 ⭐⭐⭐

### 2.1 스트리밍 플랫폼 선택

**패밀리 요구**:
- 연속 이벤트 처리
- 파티션 기반 병렬 처리
- At-least-once 전달
- 이벤트 재생 가능

---

#### 옵션 1: Apache Kafka + Flink

**핵심 스펙**:
- **처리량**: 초당 200K~2M 메시지
- **레이턴시**: p99.9 <10ms
- **Peak throughput**: 605 MB/sec (managed cloud)
- **보장**: At-least-once 기본, exactly-once 선택 가능

**아키텍처**:
```
Producer → Kafka (Partitioned Topics)
           ↓
        Flink (Stream Processing)
           ↓
    Cassandra/ScyllaDB + Redis
```

**비용**:
- **Self-hosted**: 월 $2,000~$10,000+ (3노드 클러스터)
- **AWS MSK**: $0.21~$0.84/hour per vCPU, 예상 $3,000~$10,000/월
- **Confluent Cloud**: eCKU 기반, 예상 $5,000~$20,000/월

**배포 & 운영**:
- 배포 시간: 1~4주 (self-hosted), 1~3일 (MSK)
- 운영 복잡도: ⚙️⚙️⚙️ 높음
- 필요 역량: Kafka 전문가, Java/Scala, ZooKeeper

**장점**:
- ⚡ 최고 성능: 처리량 & 레이턴시
- 🔧 완벽한 제어: 세밀한 튜닝
- 🌐 풍부한 생태계: 검증된 커넥터
- 📈 무제한 확장

**단점**:
- 💰 높은 총비용
- 🧑‍💻 전문 인력 필수
- ⏱️ 긴 배포 시간
- 🔧 복잡한 운영

**적합한 경우**:
- 대기업, 미션 크리티컬
- 초당 100만+ 메시지
- 전담 DevOps 팀
- 멀티 클라우드/온프레미스

**검증 사례**: Netflix RDG (100만 msg/s), LinkedIn, Uber

---

#### 옵션 2: AWS Kinesis + Lambda

**핵심 스펙**:
- **처리량**: 1 MB/sec per shard (input), 2 MB/sec (output)
- **레이턴시**: p99 <1초
- **Capacity**: 1,000 PUT records/sec per shard
- **확장**: Shard 추가로 수평 확장

**아키텍처**:
```
Producer → Kinesis Data Streams (Shards)
           ↓
        Lambda (Serverless Processing)
           ↓
    DynamoDB + DAX Cache
```

**비용**:
- **Provisioned**: $0.015/shard/hour (~$11/shard/월)
- **On-Demand**: $0.0134/GB + $0.015/shard-hour
- **예상** (10 shards): 월 $500~$2,000

**배포 & 운영**:
- 배포 시간: 수 시간~1일
- 운영 복잡도: ⚙️ 낮음
- 필요 역량: AWS 기본, Lambda 경험

**장점**:
- 🚀 빠른 배포: 몇 시간 내 production
- 🤖 완전 관리형: 자동 스케일링
- 💵 예측 가능한 비용
- 🔗 AWS 통합: Lambda, S3, DynamoDB

**단점**:
- 🔒 AWS 종속
- ⚡ 성능 제한: Kafka 대비 낮음
- 🔧 튜닝 제한
- 📊 대규모는 비용 급증

**적합한 경우**:
- AWS 중심 조직
- 초당 1만~50만 메시지
- 제한된 DevOps 리소스
- 빠른 MVP/출시

**검증 사례**: Amazon 내부, Sonos, 중소기업

---

#### 옵션 3: RabbitMQ + 자체 처리

**핵심 스펙**:
- **처리량**: 초당 ~3만 메시지
- **레이턴시**: 30K msg/s까지 낮음, 초과 시 급증
- **메모리**: 메시지 큐잉, 지속 스토리지 아님

**아키텍처**:
```
Producer → RabbitMQ (Queues/Exchanges)
           ↓
    Custom Workers (Node.js/Python)
           ↓
    PostgreSQL + Redis
```

**비용**:
- **Self-hosted**: 월 $100~$500 (t3.medium~m5.large)
- **Amazon MQ**: ~$703/월 (3-node mq.m5.large)

**배포 & 운영**:
- 배포 시간: 1~3일
- 운영 복잡도: ⚙️⚙️ 중간
- 필요 역량: AMQP 이해, 기본 DevOps

**장점**:
- 💰 저렴한 비용
- 📚 성숙한 기술
- 🛠️ 간단한 운영
- 🔌 다양한 프로토콜 지원

**단점**:
- 📉 낮은 처리량
- ⏱️ 부하 시 레이턴시 증가
- 💾 단기 보관
- 🚫 확장 어려움

**적합한 경우**:
- 스타트업, MVP
- 초당 1만 미만 메시지
- 예산 $1,000/month 이하
- 전통적 메시징 패턴

---

#### 스트리밍 플랫폼 비교표

| 항목 | Kafka + Flink | Kinesis + Lambda | RabbitMQ |
|------|--------------|------------------|----------|
| **처리량** | 200K~2M/s | 50K~500K/s | ~30K/s |
| **레이턴시** | p99.9 <10ms | p99 <1s | 낮음 (저부하) |
| **비용 (중규모)** | $5K~$20K/월 | $500~$2K/월 | $200~$1.5K/월 |
| **배포** | 1~4주 | 수시간~1일 | 1~3일 |
| **운영** | ⚙️⚙️⚙️ 높음 | ⚙️ 낮음 | ⚙️⚙️ 중간 |
| **확장성** | 무제한 | Shard 제한 | 제한적 |
| **클라우드** | 멀티/온프렘 | AWS 전용 | 자유 |

**의사결정 가이드**:
```
처리량 > 100만/s? → Kafka
  └─ NO
     ↓
AWS 전용 OK? → Kinesis
  └─ NO → Kafka (self-hosted)
     ↓
처리량 > 5만/s? → Kinesis
  └─ NO
     ↓
예산 < $1K/월? → RabbitMQ
  └─ NO → Kinesis
```

---

### 2.2 시계열 DB 선택

**패밀리 요구**:
- 빠른 쓰기 성능 (초당 수만~수십만 건)
- 시간 순 조회 최적화
- 파티션/샤딩 지원
- 유연한 스키마 (JSON, Key-Value)

---

#### 옵션 1: Apache Cassandra / ScyllaDB

**핵심 스펙**:
- **쓰기 처리량**: 초당 100만+ 쓰기
- **레이턴시**: p99 <10ms (쓰기)
- **확장**: 선형 수평 확장
- **일관성**: Tunable (Quorum 권장)

**아키텍처**:
- Masterless, Peer-to-Peer
- 파티션 키 기반 분산
- Compaction 전략 (Time-Window)

**비용**:
- **Self-hosted**: 월 $1,000~$5,000 (3노드)
- **ScyllaDB Cloud**: 월 $500~$3,000
- **AWS Keyspaces**: 사용량 기반

**장점**:
- ⚡ 초고속 쓰기
- 📈 선형 확장
- 🌐 멀티 데이터센터 복제
- 💪 고가용성 (P2P)

**단점**:
- 🔧 복잡한 데이터 모델링
- 📊 제한적 쿼리 (No JOIN)
- 🧑‍💻 전문 지식 필요
- 💰 높은 리소스 사용

**적합한 경우**:
- 초고속 쓰기 (100만+ writes/sec)
- 시계열 데이터 (센서, 로그)
- 멀티 리전 배포
- Netflix, Uber 규모

**검증 사례**: Netflix (5M+ writes/sec), Uber, Discord

---

#### 옵션 2: AWS DynamoDB

**핵심 스펙**:
- **쓰기 처리량**: RCU/WCU 기반 확장
- **레이턴시**: p99 <10ms (single-digit ms)
- **확장**: 자동 스케일링
- **일관성**: Eventually consistent 기본

**아키텍처**:
- Managed NoSQL
- 파티션 키 + 정렬 키
- DynamoDB Streams (CDC)

**비용**:
- **On-Demand**: $1.25/million writes
- **Provisioned**: $0.00065/WCU/hour
- **예상**: 월 $500~$5,000

**장점**:
- 🤖 완전 관리형
- 🚀 빠른 배포
- 🔗 AWS 통합 (Lambda, Kinesis)
- 💵 사용량 기반 과금

**단점**:
- 🔒 AWS 종속
- 💰 대규모 시 비싸짐
- 📊 제한적 쿼리
- 🔧 핫 파티션 주의

**적합한 경우**:
- AWS 중심
- 중간 규모 (초당 1만~10만)
- 빠른 프로토타이핑
- 운영 부담 최소화

---

#### 옵션 3: TimescaleDB (PostgreSQL 확장)

**핵심 스펙**:
- **쓰기 처리량**: 초당 10만 건
- **레이턴시**: <10ms (쓰기)
- **확장**: Hypertable 파티셔닝
- **쿼리**: Full SQL 지원

**아키텍처**:
- PostgreSQL 기반
- 자동 시간 기반 파티셔닝
- 압축 (10:1 비율)

**비용**:
- **Self-hosted**: 월 $200~$2,000
- **Timescale Cloud**: 사용량 기반

**장점**:
- 🔍 Full SQL 지원
- 📊 복잡한 쿼리 가능
- 🛠️ 익숙한 PostgreSQL
- 💰 상대적 저렴

**단점**:
- ⚡ 쓰기 성능 한계 (vs Cassandra)
- 📈 확장 제한
- 🔧 Cassandra보다 운영 쉬움

**적합한 경우**:
- SQL 필수
- 중소 규모 (초당 ~10만)
- 복잡한 분석 쿼리
- PostgreSQL 팀 역량

---

#### 시계열 DB 비교표

| 항목 | Cassandra/ScyllaDB | DynamoDB | TimescaleDB |
|------|-------------------|----------|-------------|
| **쓰기 처리량** | 1M+/s | 100K~500K/s | ~100K/s |
| **쿼리 기능** | 제한적 | 제한적 | Full SQL |
| **확장성** | 선형 | 자동 | 제한적 |
| **비용** | $1K~$5K/월 | $500~$5K/월 | $200~$2K/월 |
| **운영** | ⚙️⚙️⚙️ 높음 | ⚙️ 낮음 | ⚙️⚙️ 중간 |

**의사결정 가이드**:
```
쓰기 > 100만/s? → Cassandra
  └─ NO
     ↓
AWS 전용 + 관리형? → DynamoDB
  └─ NO
     ↓
복잡한 SQL 필요? → TimescaleDB
  └─ NO → DynamoDB
```

---

### 2.3 캐시 레이어 선택

**패밀리 요구**:
- 밀리초 미만 응답
- 핫 데이터 빠른 조회
- 높은 처리량

---

#### 옵션 1: Redis

**핵심 스펙**:
- **레이턴시**: 0.15ms (GET)
- **처리량**: 초당 120만 트랜잭션
- **자료구조**: String, Hash, List, Set, Sorted Set, Stream

**비용**:
- **Self-hosted**: 월 $100~$500
- **AWS ElastiCache**: 월 $50~$1,000

**장점**:
- ⚡ 초고속
- 🔧 다양한 자료구조
- 📡 Pub/Sub 지원
- 💾 지속성 옵션 (AOF, RDB)

**단점**:
- 💰 메모리 기반 (비쌈)
- 🔧 단일 스레드

**적합한 경우**:
- 대부분의 스트리밍 시스템
- 복잡한 캐시 로직
- Pub/Sub 필요

---

#### 옵션 2: Memcached

**핵심 스펙**:
- **레이턴시**: 마이크로초
- **처리량**: 초당 100만+ operations
- **자료구조**: Key-Value만

**비용**:
- **Self-hosted**: 월 $50~$300
- **AWS ElastiCache**: 월 $30~$500

**장점**:
- ⚡ 극도로 빠름
- 💰 더 저렴
- 🔧 단순함

**단점**:
- 📊 단순한 자료구조
- 💾 지속성 없음

**적합한 경우**:
- 단순 캐싱만
- 최소 비용
- 초고속 필수

---

#### 캐시 비교표

| 항목 | Redis | Memcached |
|------|-------|-----------|
| **레이턴시** | 0.15ms | <0.1ms |
| **자료구조** | 다양 | Key-Value |
| **지속성** | 옵션 있음 | 없음 |
| **비용** | 중간 | 낮음 |

**의사결정 가이드**:
```
복잡한 자료구조 필요? → Redis
  └─ NO
     ↓
Pub/Sub 필요? → Redis
  └─ NO → Memcached
```

---

## Part 3: 도메인 선택 요소 (프로젝트별)

이 요소들은 **패밀리와 무관**하게 프로젝트 요구사항에 따라 선택합니다.

### 3.1 프론트엔드 프레임워크
- React, Vue, Angular, Svelte
- (패밀리 영향 없음, 프로젝트 선호도)

### 3.2 백엔드 언어/프레임워크
- Node.js (Express, NestJS)
- Python (FastAPI, Django)
- Java (Spring Boot)
- Go
- (패밀리 영향 적음, 팀 역량 우선)

### 3.3 인증/권한
- Auth0, Cognito, Keycloak
- (패밀리 무관, 보안 요구사항)

### 3.4 모니터링/로깅
- Prometheus + Grafana
- ELK Stack
- Datadog, New Relic
- (패밀리 무관, 운영 선호도)

---

## Part 4: Stage 2 통합

### 4.1 Layer 3 제약 반영 예시

**시나리오**: 주식 거래 플랫폼

**Layer 3 제약 발견**:
- 증권사 API: 초당 20건 제한
- OS: Windows 전용 (일부 증권사)
- 비용: API 호출당 과금

**기술 선택 영향**:
```
스트리밍 플랫폼:
- Kafka (선호) → RabbitMQ (Windows 호환성)
- 이유: 일부 증권사 Windows DLL 제약

시계열 DB:
- Cassandra (선호) → PostgreSQL + TimescaleDB
- 이유: API 호출 제한으로 대용량 불필요

캐시:
- Redis 유지
- 이유: API 호출 최소화 필수
```

---

### 4.2 충돌 해결 예시

**NFR 목표 vs Layer 3 제약**:

**충돌 1**: 정확성 A + API 20건/초
- NFR: 100% 정확, 즉시 감지
- 제약: API 호출 제한
- **해결**: 우선순위 종목 + 폴링 주기 조정

**충돌 2**: 즉시성 A + API 지연
- NFR: 밀리초 응답
- 제약: API 응답 100ms
- **해결**: 적극적 캐싱 + WebSocket 활용

---

### 4.3 ADR 작성 준비

**선택한 기술 스택 정리**:
```
Bootstrap 필수:
✅ 스트리밍: RabbitMQ (Layer 3 제약)
✅ DB: PostgreSQL + TimescaleDB
✅ 캐시: Redis

도메인 선택:
✅ 백엔드: Node.js + TypeScript
✅ 프론트엔드: React
✅ 인증: JWT (자체 구현)
```

**ADR 작성 대상**:
1. 스트리밍 플랫폼 선택 (Kafka vs RabbitMQ)
2. DB 선택 (Cassandra vs TimescaleDB)
3. 캐시 전략
4. 증권사 API 통합 방식

---

## 📚 참고 자료

### 벤치마크
- [Confluent: Kafka vs Pulsar vs RabbitMQ (2020)](https://www.confluent.io/blog/kafka-fastest-messaging-system/)
- [OpenMessaging Benchmark Framework](https://openmessaging.cloud/docs/benchmarks/)
- Netflix Tech Blog: RDG 아키텍처

### 비용 계산기
- [AWS Kinesis Pricing](https://aws.amazon.com/kinesis/data-streams/pricing/)
- [AWS MSK Pricing](https://aws.amazon.com/msk/pricing/)
- [Confluent Cloud Pricing](https://www.confluent.io/confluent-cloud/pricing/)

### 공식 문서
- [Apache Kafka](https://kafka.apache.org/documentation/)
- [AWS Kinesis Developer Guide](https://docs.aws.amazon.com/kinesis/)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Cassandra Documentation](https://cassandra.apache.org/doc/)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)
- [TimescaleDB Documentation](https://docs.timescale.com/)
- [Redis Documentation](https://redis.io/documentation)

### 검증 사례
- Netflix: [Building Netflix's Distributed Tracing Infrastructure](https://netflixtechblog.com/)
- Uber: [Real-Time Data Infrastructure at Uber](https://eng.uber.com/)
- Twitter: [The Infrastructure Behind Twitter](https://blog.twitter.com/engineering/)

---

**마지막 업데이트**: 2024-11-12  
**다음 검토**: 2025-02-12 (기술 스택 업데이트 반영)
