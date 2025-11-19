# 7개 핵심 아키텍처 패밀리

## 개요

DNA v4.0은 18개 조합을 7개 핵심 패밀리로 분류합니다. 이 분류는 1호의 철저한 프로덕션 사례 분석을 기반으로 검증되었습니다.

### Layer 1-2 분류 체계

**Layer 1 (데이터 일관성)**:
- A = Strong Consistency (ACID)
- B = Eventual Consistency

**Layer 2 (처리 패턴)**:
- A = Real-time / Synchronous
- B = Batch / Asynchronous
- C = Hybrid

---

## 7개 핵심 패밀리

### 1. 초고속 거래 시스템 (A-A-A)
**Ultra-Low Latency Trading**

- **특성**: Strong Consistency + Real-time + 최고 응답속도
- **NFR 우선순위**: Performance > Consistency > Availability
- **대표 사례**: HFT, 증권거래소, 파생상품 거래

**기술 스택**:
- DB: In-memory (Redis, Aerospike)
- Message: Kernel bypass (Aeron, DPDK)
- Language: C++, Rust

---

### 2. 트랜잭션/CRUD 시스템 (A-A-B)
**Transaction-Heavy Applications**

- **특성**: Strong Consistency + Real-time + 중간 처리량
- **NFR 우선순위**: Consistency > Reliability > Performance
- **대표 사례**: 은행 코어, ERP, 재고관리, 결제시스템

**기술 스택**:
- DB: PostgreSQL, Oracle, MySQL
- Cache: Redis (write-through)
- Framework: Spring Boot, Django

---

### 3. 협업/동기화 시스템 (B-A-A)
**Real-time Collaboration**

- **특성**: Eventual Consistency + Real-time + 동시편집
- **NFR 우선순위**: Availability > Latency > Consistency
- **대표 사례**: Google Docs, Figma, 화상회의, 멀티플레이어 게임

**기술 스택**:
- DB: CRDTs, MongoDB
- Sync: WebSocket, Operational Transform
- Infra: Edge computing

---

### 4. 검색/추천 시스템 (B-B-B)
**Search & Recommendation**

- **특성**: Eventual Consistency + Batch + 대용량
- **NFR 우선순위**: Scalability > Relevance > Freshness
- **대표 사례**: 검색엔진, 추천엔진, 광고시스템

**기술 스택**:
- Search: Elasticsearch, Solr
- ML: TensorFlow, PyTorch
- Pipeline: Spark, Flink

---

### 5. 실시간 스트리밍 시스템 (B-C-A)
**Real-time Streaming**

- **특성**: Eventual Consistency + Hybrid + 연속 데이터
- **NFR 우선순위**: Throughput > Latency > Durability
- **대표 사례**: IoT 플랫폼, 로그 분석, 실시간 대시보드

**기술 스택**:
- Stream: Kafka, Pulsar
- Processing: Flink, Spark Streaming
- Storage: ClickHouse, TimescaleDB

---

### 6. 분석/배치 시스템 (B-A-C)
**Analytics & Batch Processing**

- **특성**: Eventual Consistency + Real-time Query + Batch Load
- **NFR 우선순위**: Accuracy > Completeness > Timeliness
- **대표 사례**: DW, BI, 보고서 시스템, ETL

**기술 스택**:
- DW: Snowflake, BigQuery, Redshift
- ETL: Airflow, dbt
- Viz: Tableau, Looker

---

### 7. 안전-임계 IoT 시스템 (A-B-A)
**Safety-Critical IoT**

- **특성**: Strong Consistency + Async + 고신뢰성
- **NFR 우선순위**: Safety > Reliability > Performance
- **대표 사례**: 의료기기, 자율주행, 산업제어(SCADA)

**기술 스택**:
- Protocol: MQTT with QoS 2, OPC-UA
- Safety: Formal verification
- Redundancy: Active-active clustering

---

## 패밀리 선택 가이드

### Step 1: Layer 1 결정 (데이터 일관성)
```
금전/생명/법적 책임 관련? → A (Strong)
그 외? → B (Eventual)
```

### Step 2: Layer 2 결정 (처리 패턴)
```
즉각 응답 필수? → A (Real-time)
정기 처리 OK? → B (Batch)
둘 다 필요? → C (Hybrid)
```

### Step 3: NFR 우선순위로 최종 선택
```
같은 Layer 1-2 조합에서 NFR로 세부 구분
예: A-A지만 속도 vs 신뢰성 우선순위에 따라
    A-A-A (초고속) vs A-A-B (트랜잭션)
```

---

## 18개 조합과의 매핑

| 패밀리 | Layer 1-2 | 주요 NFR | 커버하는 조합 |
|--------|-----------|----------|---------------|
| 초고속 거래 | A-A-A | Performance | 1개 |
| 트랜잭션/CRUD | A-A-B | Consistency | 2-3개 |
| 협업/동기화 | B-A-A | Availability | 2개 |
| 검색/추천 | B-B-B | Scalability | 3-4개 |
| 실시간 스트리밍 | B-C-A | Throughput | 2-3개 |
| 분석/배치 | B-A-C | Accuracy | 2-3개 |
| 안전-임계 IoT | A-B-A | Safety | 2개 |

**참고**:
- 7개 패밀리로 18개 조합의 90% 이상 커버
- 나머지는 이 패밀리들의 변형으로 처리
- 새 프로젝트는 가장 가까운 패밀리에서 시작

---

## 검증 근거

이 분류는 1호의 체계적인 연구를 통해 검증되었습니다:

1. **프로덕션 사례 분석**: 각 패밀리별 실제 운영 시스템 확인
2. **기술 스택 검증**: 해당 분야에서 표준으로 사용되는 기술 매핑
3. **NFR 충돌 분석**: 각 패밀리 내에서 NFR 트레이드오프 확인
4. **실용성 검증**: 18개 → 7개 축소로 선택 복잡도 감소

**결론**: 7개 패밀리는 실무에서 충분히 구분 가능하며, 기술 선택을 효과적으로 가이드합니다.
