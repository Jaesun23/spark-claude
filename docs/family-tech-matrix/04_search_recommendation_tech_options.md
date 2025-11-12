# 검색/추천 패밀리 (B-B-B) - 기술 매트릭스

**작성일**: 2025-11-12  
**패밀리**: 검색/추천 (B-B-B)  
**검증 사례**: Elasticsearch (Zillow), Vector DB (RAG 앱), 추천 엔진

---

## Part 1: 패밀리가 요구하는 시스템 구조 ⭐⭐⭐

### 1.1 B-B-B 특성이 강제하는 것

#### B (점진적 실패) → 점진적 품질 저하 허용

**특성**:
- 일부 결과 누락 허용 (전부 또는 전무가 아님)
- 관련성 점수 기반 순위
- 타임아웃 시 부분 결과 반환
- Eventual consistency

**강제되는 기술적 요구**:
```
✅ Circuit breaker, fallback 메커니즘
✅ 관련성 스코어링 (relevance scoring)
✅ 타임아웃 처리
✅ 캐시 레이어 (구형 결과 반환)
```

**검증 사례**:
- Elasticsearch: 검색 스레드 풀 거부 시 에러, 하지만 시스템 계속 작동
- Zillow 추천: 실시간 추천 실패 시 캐시된 추천 반환

---

#### B (반구조화 데이터) → 유연한 스키마 필수

**특성**:
- JSON 문서, 다양한 필드 구조
- 동적 필드 추가/제거
- 중첩 객체, 배열
- 스키마 진화

**강제되는 기술적 요구**:
```
✅ Document store (JSON 네이티브)
✅ 동적 매핑 (dynamic mapping)
✅ Sparse vectors (희소 벡터)
✅ 유연한 인덱싱
```

**검증 사례**:
- Elasticsearch: 상품 카탈로그, 각 상품마다 다른 속성 (전자제품 vs 의류)
- Vector DB: 다양한 길이의 텍스트 임베딩

---

#### B (수초 응답) → 빠른 검색 필수

**특성**:
- 50ms~10초 (단순→복잡 쿼리)
- 사용자 대기 가능 범위
- 관련성 우선, 속도 차선
- 병렬 쿼리 최적화

**강제되는 기술적 요구**:
```
✅ 역인덱스 (inverted index)
✅ 샤딩, 파티셔닝
✅ 쿼리 캐싱
✅ 인메모리 구조
```

**검증 사례**:
- Elasticsearch: 50-100ms 단순 쿼리, 100ms-10초 복잡 집계
- Zillow: 100ms 미만 실시간 추천, 11.5-25.6% 레이턴시 감소

---

### 1.2 Bootstrap 필수 요소 (패밀리 강제)

B-B-B 패밀리는 다음 3가지 시스템 요소를 **반드시** 포함해야 합니다:

#### 1. 검색 엔진 (필수!)
**역할**: Full-text search, 관련성 스코어링
**이유**: 반구조화 데이터(B) + 빠른 검색(B)
**선택지**: Elasticsearch, Typesense, Meilisearch

#### 2. Vector DB (AI/RAG 시 필수, 아니면 불필요)
**역할**: 의미적 검색 (semantic search)
**이유**: 반구조화(B) + 의미 기반 관련성
**선택지**: Pinecone, Weaviate, pgvector
**주의**: Keyword 검색만 하면 불필요

#### 3. 캐시 레이어 (필수!)
**역할**: 핫 쿼리 결과 캐싱
**이유**: 수초 응답(B) + 점진적 실패(B)
**선택지**: Redis, Memcached

---

## Part 2: Bootstrap 요소별 기술 선택 ⭐⭐⭐

### 2.1 검색 엔진 선택

**패밀리 요구**:
- Full-text search
- 관련성 스코어링
- 동적 필드 매핑
- 빠른 인덱싱

---

#### 옵션 1: Elasticsearch

**핵심 스펙**:
- **쿼리 속도**: 50-100ms (단순), 100ms-10초+ (복잡 집계)
- **인덱싱**: 초당 1만~10만 문서
- **처리량**: 초당 1만~10만 쿼리
- **확장**: 수평 확장 (샤딩)

**비용**:
- **Self-hosted**: 월 $25~$500 (소규모), $2,000~$7,000 (대규모)
- **Elastic Cloud**: 월 $95~$175 (Standard~Enterprise)
- **AWS OpenSearch**: 월 $500~$5,000

**장점**:
- 🔍 강력한 Full-text search, 다국어 지원
- 📊 복잡한 집계 (aggregations) 가능
- 🌐 풍부한 생태계, Kibana 시각화
- 🔧 유연한 쿼리 DSL, 필터링

**단점**:
- 💰 높은 비용 (대규모 시)
- 🔧 복잡한 설정, 튜닝 필요
- 💾 메모리 많이 사용
- 📈 클러스터 관리 부담

**적합한 경우**:
- 대기업, 복잡한 검색 요구
- 대용량 데이터 (TB급)
- 로그 분석, 모니터링
- 다국어, 지리 검색

**검증 사례**: Zillow (11.5-25.6% 레이턴시 감소), Uber, GitHub

---

#### 옵션 2: Typesense

**핵심 스펙**:
- **쿼리 속도**: <50ms (p99)
- **인덱싱**: 초당 1만~5만 문서
- **처리량**: 초당 5만~20만 쿼리
- **메모리**: Elasticsearch 대비 50% 절감

**비용**:
- **Self-hosted**: 월 $50~$300
- **Typesense Cloud**: 월 $29~$299 (사용량 기반)

**장점**:
- ⚡ 극도로 빠름, 메모리 효율
- 💰 저렴한 비용
- 🔧 간단한 설정, RESTful API
- 🔥 Typo tolerance (오타 허용)

**단점**:
- 📊 제한적 집계 (Elasticsearch 대비)
- 📦 작은 생태계, 커뮤니티
- 🔧 고급 기능 부족 (ML, 파이프라인)
- 📈 대규모 확장 제한

**적합한 경우**:
- 스타트업, MVP
- e-commerce 검색
- 예산 <$500/월
- 단순한 검색 요구

**검증 사례**: 여러 스타트업, e-commerce 사이트

---

#### 옵션 3: Meilisearch

**핵심 스펙**:
- **쿼리 속도**: <20ms (p99)
- **인덱싱**: 초당 5,000~20,000 문서
- **처리량**: 초당 1만~5만 쿼리
- **특징**: Search-as-you-type 최적화

**비용**:
- **Self-hosted**: 월 $30~$200
- **Meilisearch Cloud**: 월 $15~$500

**장점**:
- ⚡ 초고속, Instant search
- 🎯 Search-as-you-type 우수
- 🔧 간단한 API, 개발자 친화
- 💰 매우 저렴

**단점**:
- 📊 집계 없음
- 📈 대규모 데이터 제한 (GB급)
- 🔧 고급 쿼리 부족
- 🌐 작은 생태계

**적합한 경우**:
- 문서 검색, 웹사이트 검색
- 소규모 (GB급 데이터)
- Instant search UX 필수
- 최소 비용

**검증 사례**: 여러 문서 사이트, 소규모 앱

---

#### 검색 엔진 비교표

| 항목 | Elasticsearch | Typesense | Meilisearch |
|------|--------------|-----------|-------------|
| **쿼리 속도** | 50-100ms | <50ms | <20ms |
| **인덱싱** | 10K~100K/s | 10K~50K/s | 5K~20K/s |
| **비용** | $500~$7K/월 | $50~$300/월 | $30~$200/월 |
| **집계** | 강력 | 제한적 | 없음 |
| **확장성** | 무제한 | 중간 | 제한적 |
| **복잡도** | ⚙️⚙️⚙️ 높음 | ⚙️⚙️ 중간 | ⚙️ 낮음 |

**의사결정 가이드**:
```
데이터 > TB급? → Elasticsearch
  └─ NO
     ↓
복잡한 집계 필요? → Elasticsearch
  └─ NO
     ↓
Instant search 필수? → Meilisearch
  └─ NO
     ↓
예산 <$500/월? → Typesense
  └─ NO → Elasticsearch
```

---

### 2.2 Vector DB 선택 (AI/RAG 앱만 해당)

**패밀리 요구**:
- 의미적 검색 (semantic search)
- 고차원 벡터 저장 (768~1536 차원)
- K-NN 검색 (<100ms)
- 메타데이터 필터링

---

#### 옵션 1: Pinecone

**핵심 스펙**:
- **쿼리 속도**: p50 <10ms, p99 <50ms
- **처리량**: 초당 10만+ 쿼리
- **확장**: 억 단위 벡터 지원
- **인덱싱**: 초당 1만+ 벡터

**비용**:
- **Serverless**: 월 $50 최소 (pay-as-you-go)
- **Standard**: 월 $40~$200 (소중형)
- **Enterprise**: 월 $500~$2,000+

**장점**:
- ⚡ 극도로 빠름, 일관된 성능
- 🤖 완전 관리형, 자동 스케일링
- 🔧 간단한 API, SDK 풍부
- 🔒 SOC 2, HIPAA 인증

**단점**:
- 💰 높은 비용 (대규모 시)
- 🔒 벤더 종속
- 📊 제한적 쿼리 (K-NN 중심)
- 🔧 커스터마이징 제한

**적합한 경우**:
- 프로덕션 RAG 앱
- 빠른 배포, 운영 최소화
- 억 단위 벡터
- 예산 $200~$2,000/월

**검증 사례**: 다수 RAG 앱, LLM 기반 서비스

---

#### 옵션 2: Weaviate

**핵심 스펙**:
- **쿼리 속도**: p99 <50ms
- **처리량**: 초당 5만~10만 쿼리
- **확장**: 억 단위 벡터 지원
- **특징**: Hybrid search (Vector + BM25)

**비용**:
- **Self-hosted**: 무료 (오픈소스)
- **Serverless**: 월 $25~$153 (사용량 기반)
- **Classic**: $0.05/백만 차원

**장점**:
- 🔓 오픈소스, Self-host 가능
- 🔧 Hybrid search, GraphQL
- 🌐 Multi-modal (텍스트, 이미지)
- 💰 저렴한 비용

**단점**:
- ⏱️ Pinecone 대비 약간 느림
- 🔧 Self-host 시 운영 부담
- 📦 생태계 작음 (Pinecone 대비)
- 🔧 복잡한 설정 (고급 기능)

**적합한 경우**:
- Hybrid search 필요
- Self-host 선호
- Multi-modal 데이터
- 예산 <$200/월

**검증 사례**: 여러 RAG 앱, 지식 그래프

---

#### 옵션 3: pgvector (PostgreSQL 확장)

**핵심 스펙**:
- **쿼리 속도**: 10-100ms (데이터 규모 의존)
- **처리량**: 초당 1만~5만 쿼리
- **확장**: 백만 단위 벡터 권장
- **특징**: PostgreSQL 네이티브

**비용**:
- **Self-hosted**: 월 $50~$500 (PostgreSQL 비용)
- **Supabase**: 월 $25~$599
- **AWS RDS**: 월 $70~$2,000

**장점**:
- 🔧 PostgreSQL 통합, SQL 사용
- 💰 저렴한 비용
- 🔒 트랜잭션 보장 (ACID)
- 📦 기존 인프라 활용

**단점**:
- ⏱️ 전용 Vector DB 대비 느림
- 📈 대규모 확장 제한 (백만 단위)
- 🔧 튜닝 필요 (인덱스, 쿼리)
- 💾 메모리 사용 높음

**적합한 경우**:
- PostgreSQL 이미 사용 중
- 소중형 (백만 단위 벡터)
- SQL + Vector 통합
- 예산 <$500/월

**검증 사례**: 여러 스타트업, 프로토타입

---

#### Vector DB 비교표

| 항목 | Pinecone | Weaviate | pgvector |
|------|----------|----------|----------|
| **쿼리 속도** | <10ms (p50) | <50ms (p99) | 10-100ms |
| **처리량** | 100K+/s | 50K~100K/s | 10K~50K/s |
| **확장** | 억 단위 | 억 단위 | 백만 단위 |
| **비용** | $50~$2K/월 | $25~$153/월 | $50~$500/월 |
| **운영** | ⚙️ 낮음 | ⚙️⚙️ 중간 | ⚙️⚙️ 중간 |

**의사결정 가이드**:
```
벡터 > 1억? → Pinecone or Weaviate
  └─ NO
     ↓
PostgreSQL 사용 중? → pgvector
  └─ NO
     ↓
Hybrid search 필요? → Weaviate
  └─ NO
     ↓
완전 관리형 필요? → Pinecone
  └─ NO → Weaviate (self-host)
```

---

### 2.3 캐시 레이어 선택

**패밀리 요구**:
- 핫 쿼리 결과 캐싱
- 밀리초 미만 응답
- TTL 관리
- 높은 처리량

---

#### 옵션 1: Redis

**핵심 스펙**:
- **레이턴시**: 0.15ms (GET)
- **처리량**: 초당 120만 트랜잭션
- **자료구조**: String, Hash, Sorted Set
- **특징**: TTL, Pub/Sub

**비용**:
- **Self-hosted**: 월 $50~$500
- **AWS ElastiCache**: 월 $50~$1,000
- **Redis Cloud**: 월 $30~$2,000

**장점**:
- ⚡ 초고속, 다양한 자료구조
- 🔧 TTL 자동 만료
- 🔔 Pub/Sub (캐시 무효화)
- 📦 풍부한 클라이언트

**단점**:
- 💰 메모리 기반, 비용 높음
- 🔧 단일 스레드
- 📈 클러스터 설정 복잡

**적합한 경우**:
- 대부분의 검색 시스템
- 복잡한 캐시 로직
- Pub/Sub 필요
- 쿼리 결과 캐싱

**검증 사례**: Zillow, GitHub, Uber

---

#### 옵션 2: Memcached

**핵심 스펙**:
- **레이턴시**: <0.1ms
- **처리량**: 초당 100만+ operations
- **자료구조**: Key-Value만
- **특징**: 멀티 스레드

**비용**:
- **Self-hosted**: 월 $30~$300
- **AWS ElastiCache**: 월 $30~$500

**장점**:
- ⚡ 극도로 빠름
- 💰 저렴한 비용
- 🔧 멀티 스레드, CPU 효율
- 📉 낮은 메모리 오버헤드

**단점**:
- 📊 단순한 자료구조
- 🚫 TTL 정밀도 낮음
- 💾 지속성 없음

**적합한 경우**:
- 단순 캐싱만
- 최소 비용
- 초고속 필수
- 복잡한 자료구조 불필요

---

#### 캐시 비교표

| 항목 | Redis | Memcached |
|------|-------|-----------|
| **레이턴시** | 0.15ms | <0.1ms |
| **자료구조** | 다양 | Key-Value |
| **TTL** | 정밀 | 제한적 |
| **비용** | 중간 | 낮음 |

**의사결정 가이드**:
```
복잡한 자료구조? → Redis
  └─ NO
     ↓
정밀한 TTL? → Redis
  └─ NO → Memcached
```

---

## Part 3: 도메인 선택 요소 (프로젝트별)

이 요소들은 **패밀리와 무관**하게 프로젝트 요구사항에 따라 선택합니다.

### 3.1 프론트엔드 프레임워크
- **선택 기준**: 팀 역량, 생태계, 프로젝트 규모
- **옵션**: React (대형, 풍부한 생태계), Vue (중소형, 학습 곡선 낮음), Svelte (경량, 빠른 성능)
- **패밀리 무관**: C-B-B는 프론트엔드 선택에 영향 없음

### 3.2 백엔드 언어/프레임워크
- **선택 기준**: 팀 역량, 검색 엔진 클라이언트 지원
- **옵션**: Node.js (Elasticsearch 클라이언트 우수), Python (ML/AI 통합), Go (성능 중시)
- **고려사항**: 검색 엔진 SDK 품질 확인 필요

### 3.3 인증/권한
- **선택 기준**: 보안 요구사항, 규제 준수
- **옵션**: Auth0 (엔터프라이즈), Clerk (개발자 친화), Firebase Auth (간편)
- **검색 연동**: 사용자별 검색 결과 필터링 고려

### 3.4 Embedding 모델 (AI/RAG 시)
- **선택 기준**: 정확도, 비용, 레이턴시
- **옵션**: OpenAI Ada-002 (높은 품질, $0.0001/1K tokens), Cohere (다국어), Sentence Transformers (무료, self-host)
- **Vector DB 연동**: 차원 수 호환성 확인 (768, 1536 등)

---

## Part 4: Stage 2 통합

### 4.1 Layer 3 제약 반영 예시

**시나리오**: e-commerce 검색 플랫폼

**Layer 3 제약 발견**:
- 규제: GDPR, 유럽 데이터 저장
- 팀: Python 경험, Go 없음
- 인프라: AWS 중심
- 비용: 초기 예산 $1,000/월

**기술 선택 영향**:
```
검색 엔진:
- Elasticsearch (선호) → Typesense
- 이유: 비용 절감 ($7K → $300/월)

Vector DB:
- Pinecone (선호) → Weaviate (self-host)
- 이유: GDPR 준수, 유럽 서버 필요

캐시:
- Redis 유지
- 이유: TTL, 쿼리 결과 캐싱 필수
```

---

### 4.2 충돌 해결 예시

**NFR 목표 vs Layer 3 제약**:

**충돌 1**: 속도 A + 예산 제한
- NFR: <50ms 검색
- 제약: 예산 $1,000/월
- **해결**: Typesense ($300) + 적극적 캐싱
  - **트레이드오프**: 복잡한 집계 불가 (Elasticsearch 대비), 대규모 확장 제한

**충돌 2**: 관련성 A + 개발 기간
- NFR: AI 의미적 검색
- 제약: 3개월 출시
- **해결**: Pinecone (관리형) 대신 pgvector (간단)
  - **트레이드오프**: 성능 낮음 (<10ms → 10-100ms), 백만 단위 벡터로 제한

---

### 4.3 ADR 작성 준비

**선택한 기술 스택 정리**:
```
Bootstrap 필수:
✅ 검색: Typesense (AWS EC2)
✅ Vector DB: pgvector (AWS RDS PostgreSQL)
✅ 캐시: Redis (AWS ElastiCache)

도메인 선택:
✅ 백엔드: Python + FastAPI
✅ 프론트엔드: React
✅ 인증: Auth0
✅ Embedding: OpenAI Ada-002
```

**ADR 작성 대상**:

Bootstrap ADR:
1. Typesense 선택 (Elasticsearch, Meilisearch 대비)
2. pgvector 선택 (Pinecone, Weaviate 대비)
3. Redis 선택 (Memcached 대비)

도메인 ADR:
4. FastAPI 선택 (Django 대비)
5. React 선택 (Vue 대비)
6. OpenAI Ada-002 선택 (Cohere 대비)

---

## 📚 참고 자료

### 벤치마크
- [Elasticsearch Performance Tuning](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-search-speed.html)
- [Typesense vs Elasticsearch Benchmark](https://typesense.org/docs/guide/performance.html)
- [Pinecone Performance Benchmarks](https://www.pinecone.io/learn/series/performance/)

### 비용 계산기
- [Elasticsearch Pricing](https://www.elastic.co/pricing/)
- [Typesense Cloud Pricing](https://cloud.typesense.org/pricing)
- [Pinecone Pricing Calculator](https://www.pinecone.io/pricing/)
- [Weaviate Pricing](https://weaviate.io/pricing)

### 공식 문서
- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Typesense Documentation](https://typesense.org/docs/)
- [Meilisearch Documentation](https://www.meilisearch.com/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [pgvector Documentation](https://github.com/pgvector/pgvector)

### 검증 사례
- Zillow: [Elasticsearch 레이턴시 개선](https://www.elastic.co/customers/zillow)
- RAG Apps: [Vector DB 벤치마크](https://www.pinecone.io/learn/vector-database-benchmark/)
- e-commerce: [Typesense 사례](https://typesense.org/showcase/)

---

**마지막 업데이트**: 2025-11-12  
**다음 검토**: 2026-02-12 (기술 스택 업데이트 반영)
