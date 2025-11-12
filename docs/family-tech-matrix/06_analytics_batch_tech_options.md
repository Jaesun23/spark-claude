# 분석/배치 패밀리 (B-A-C) - 기술 매트릭스

**작성일**: 2025-11-12  
**패밀리**: 분석/배치 (B-A-C)  
**검증 사례**: Snowflake (8초 쿼리), Redshift, BigQuery, dbt

---

## Part 1: 패밀리가 요구하는 시스템 구조 ⭐⭐⭐

### 1.1 B-A-C 특성이 강제하는 것

#### B (점진적 실패) → 배치 재시도 필수

**특성**:
- 작업 실패 시 재시도
- 체크포인트 기반 복구
- 부분 성공 허용
- Idempotent 처리

**강제되는 기술적 요구**:
```
✅ 배치 스케줄러 (Airflow, dbt)
✅ 작업 재시도 메커니즘
✅ 데이터 리니지 추적
✅ 점진적 로드 (Incremental)
```

**검증 사례**:
- Snowflake: 작업 실패 시 자동 재시도, 체크포인트 복구
- dbt: Incremental 모델, 실패한 노드만 재실행

---

#### A (구조화 데이터) → 고정 스키마 필수

**특성**:
- 테이블 기반 구조
- 고정된 컬럼 정의
- SQL 쿼리 최적화
- ACID 트랜잭션 (배치 완료 시)

**강제되는 기술적 요구**:
```
✅ 관계형 스키마
✅ SQL 기반 변환
✅ 스키마 마이그레이션 도구
✅ 데이터 타입 검증
```

**검증 사례**:
- Snowflake: Zero-Copy Cloning, Time Travel (90일)
- Redshift: Columnar storage, Sort/Dist keys
- BigQuery: Nested/Repeated fields (STRUCT/ARRAY)

---

#### C (배치 처리) → ETL/ELT 파이프라인 필수

**특성**:
- 시간/일 단위 스케줄
- 대용량 데이터 처리
- 집계 및 변환
- 비실시간 (분~시간)

**강제되는 기술적 요구**:
```
✅ 배치 스케줄러
✅ 대용량 데이터 로더
✅ Materialized Views
✅ Query Result Caching
```

**검증 사례**:
- Snowflake: 8-12초 TPC-DS 쿼리 (벤치마크)
- Redshift: 8.24초 평균 쿼리, 82% 유휴 시간
- BigQuery: 11.18초 평균, 서버리스

---

### 1.2 Bootstrap 필수 요소 (패밀리 강제)

B-A-C 패밀리는 다음 3가지 시스템 요소를 **반드시** 포함해야 합니다:

#### 1. 데이터 웨어하우스 (필수!)
**역할**: 대용량 분석 쿼리, 집계, 저장
**이유**: 구조화 데이터(A) + 배치 처리(C)
**선택지**: Snowflake, Redshift, BigQuery

#### 2. ETL/ELT 도구 (필수!)
**역할**: 데이터 추출, 변환, 로드
**이유**: 배치 파이프라인(C) + 스케줄링
**선택지**: dbt, Airflow, Fivetran

#### 3. BI/시각화 (필수!)
**역할**: 대시보드, 리포트 생성
**이유**: 분석 결과 시각화
**선택지**: Tableau, Looker, Power BI

---

## Part 2: Bootstrap 요소별 기술 선택 ⭐⭐⭐

### 2.1 데이터 웨어하우스 선택

**패밀리 요구**:
- 대용량 SQL 쿼리 (수백 GB~PB)
- Columnar Storage (읽기 최적화)
- MPP (Massively Parallel Processing)
- 시간별/일별 배치 로드

---

#### 옵션 1: Snowflake

**핵심 스펙**:
- **쿼리 성능**: 8-12초 (TPC-DS 벤치마크)
- **처리량**: 수십 TB/일, PB급 스토리지
- **동시성**: 무제한 가상 웨어하우스
- **아키텍처**: Storage-Compute 분리, 3-Layer

**비용**:
- **Compute**: $2~$4/credit (웨어하우스 크기별)
- **Storage**: $23~$40/TB/월 (압축 후)
- **예상** (중규모): 월 $2,000~$10,000
- **대규모**: 월 $20,000~$100,000+

**장점**:
- ⚡ 최고 성능: 8초 TPC-DS
- 🔧 Zero-Copy Cloning: 개발/테스트 환경
- 📈 무제한 확장: 가상 웨어하우스 독립
- ⏱️ Time Travel: 90일 (Enterprise)
- 🌐 멀티 클라우드: AWS, Azure, GCP

**단점**:
- 💰 높은 비용: 크레딧 기반 과금
- 📊 러닝 커브: 최적화 복잡
- 🔒 클라우드 종속 (하지만 멀티)

**적합한 경우**:
- 대기업, 복잡한 분석
- 수십 TB~PB 데이터
- 멀티 팀 동시 작업
- 개발/스테이징 환경 필수

**검증 사례**: Instacart, Capital One, DoorDash

---

#### 옵션 2: AWS Redshift

**핵심 스펙**:
- **쿼리 성능**: 8.24초 평균 (벤치마크)
- **처리량**: 수 TB/일, PB급 확장
- **동시성**: WLM (Workload Management)
- **아키텍처**: MPP, Columnar, Sort/Dist Keys

**비용**:
- **RA3 (Storage-Compute 분리)**: $1.086~$13.04/node/hour
- **DC2 (Compute 최적화)**: $0.25~$4.80/node/hour
- **예상** (RA3.4xl, 2노드): 월 $1,600~$5,000
- **대규모** (10+ 노드): 월 $15,000~$50,000+

**장점**:
- 🔗 AWS 통합: S3, Lambda, Kinesis
- 💵 상대적 저렴: DC2 $0.25/시간부터
- 📊 성숙한 생태계: 다양한 커넥터
- ⚙️ WLM: 쿼리 우선순위 제어

**단점**:
- 🔒 AWS 종속
- 🔧 운영 복잡: 수동 튜닝 필요
- ⏱️ 동시성 제약: WLM 큐 관리
- 📉 유휴 비용: 82% 유휴 시간 (평균)

**적합한 경우**:
- AWS 중심 조직
- 수 TB~수십 TB 데이터
- 예측 가능한 워크로드
- SQL 최적화 역량 있음

**검증 사례**: Netflix, Lyft, McDonald's

---

#### 옵션 3: Google BigQuery

**핵심 스펙**:
- **쿼리 성능**: 11.18초 평균 (벤치마크)
- **처리량**: 수십 TB/일, PB급 스토리지
- **동시성**: 서버리스, 자동 확장
- **아키텍처**: Dremel, Columnar, Capacitor

**비용**:
- **On-Demand**: $6.25/TB (스캔된 데이터)
- **Flat-Rate**: $2,000~$10,000+/월 (slot 예약)
- **Storage**: $0.02/GB/월 (Active), $0.01 (Long-term)
- **예상** (On-Demand, 1TB/일): 월 $187

**장점**:
- 🚀 서버리스: 인프라 관리 불필요
- 💵 On-Demand: 사용한 만큼만
- 🔗 GCP 통합: Cloud Storage, Dataflow
- 📈 무제한 확장: 자동 슬롯 할당

**단점**:
- 🔒 GCP 종속
- 💰 대규모 시 비쌈: 쿼리 스캔량 기반
- 🔧 튜닝 제한: 서버리스라 제어 적음
- ⏱️ 스캔량 최적화 필요

**적합한 경우**:
- GCP 중심 조직
- 중소 규모, 비정기 쿼리
- 빠른 프로토타이핑
- 운영 부담 최소화

**검증 사례**: Spotify, Twitter, The New York Times

---

#### 데이터 웨어하우스 비교표

| 항목 | Snowflake | Redshift | BigQuery |
|------|-----------|----------|----------|
| **쿼리 성능** | 8-12초 | 8.24초 | 11.18초 |
| **처리량** | PB급 | PB급 | PB급 |
| **비용 (중규모)** | $2K~$10K/월 | $1.6K~$5K/월 | $187~$2K/월 |
| **운영** | ⚙️⚙️ 중간 | ⚙️⚙️⚙️ 높음 | ⚙️ 낮음 |
| **확장성** | 무제한 | 노드 추가 | 무제한 (서버리스) |
| **클라우드** | 멀티 | AWS | GCP |

**의사결정 가이드**:
```
데이터 > 100TB? → Snowflake
  └─ NO
     ↓
AWS 전용 OK? → Redshift
  └─ NO
     ↓
GCP 전용 OK? → BigQuery
  └─ NO → Snowflake (멀티 클라우드)
     ↓
운영 리소스 < 1명? → BigQuery
  └─ NO → Redshift or Snowflake
```

---

### 2.2 ETL/ELT 도구 선택

**패밀리 요구**:
- 배치 스케줄링 (cron, 이벤트 기반)
- 데이터 변환 (SQL, Python)
- 의존성 관리 (DAG)
- 재시도 및 모니터링

---

#### 옵션 1: dbt (Data Build Tool)

**핵심 스펙**:
- **변환 방식**: ELT (DW 내 SQL 변환)
- **배포**: Cloud ($50~$400+/월) or Core (오픈소스)
- **언어**: SQL + Jinja2
- **의존성**: DAG 자동 생성

**비용**:
- **dbt Core**: 무료 (오픈소스)
- **dbt Cloud Developer**: $50/seat/월
- **dbt Cloud Team**: $100+/seat/월
- **예상** (5명): 월 $250~$500

**장점**:
- 📊 SQL 중심: 데이터 분석가 친화적
- 🔧 Incremental 모델: 효율적 배치
- 📚 데이터 문서화: 자동 docs 생성
- 🧪 테스트: SQL 기반 데이터 품질 검증

**단점**:
- 🔧 오케스트레이션 제한: Airflow 필요 (대규모)
- 🐍 Python 제약: SQL 외 복잡 로직 어려움
- 📈 대규모 확장: 수천 모델 시 느림

**적합한 경우**:
- SQL 중심 팀
- 중소 규모 (수백 모델)
- Snowflake/Redshift/BigQuery 사용
- 데이터 분석가 주도 변환

**검증 사례**: GitLab, Zapier, JetBlue

---

#### 옵션 2: Apache Airflow

**핵심 스펙**:
- **변환 방식**: ETL/ELT 모두 지원
- **배포**: Self-hosted or Managed (MWAA)
- **언어**: Python (DAG 정의)
- **의존성**: 복잡한 DAG 지원

**비용**:
- **Self-hosted**: 월 $500~$2,000 (인프라)
- **AWS MWAA**: $0.49/hour (Environment) + $0.24/vCPU/hour
- **예상** (MWAA, 2 vCPU): 월 $700~$1,500
- **Google Cloud Composer**: 유사

**장점**:
- 🐍 Python 기반: 복잡한 로직 구현
- 🔧 유연성: 모든 데이터 소스 통합
- 📈 대규모 확장: 수천 작업 지원
- 📊 모니터링: UI + 알림

**단점**:
- 🧑‍💻 높은 러닝 커브: Python 필수
- 💰 운영 복잡: 워커 관리, 스케일링
- 🔧 설정 복잡: Executor, Queue 설정

**적합한 경우**:
- Python 팀
- 복잡한 파이프라인 (100+ 작업)
- 다양한 데이터 소스 통합
- 실시간 + 배치 혼합

**검증 사례**: Airbnb, Lyft, Reddit

---

#### 옵션 3: Fivetran

**핵심 스펙**:
- **변환 방식**: ELT (자동 커넥터)
- **배포**: Fully Managed (SaaS)
- **언어**: No-code (UI 설정)
- **커넥터**: 500+ 소스

**비용**:
- **Starter**: $120/월 (500K MAR)
- **Standard**: $180/월 (500K MAR)
- **Enterprise**: 맞춤형 가격
- **MAR**: Monthly Active Rows (변경된 행)
- **예상**: 월 $1,000~$10,000+

**장점**:
- 🚀 빠른 배포: 커넥터 클릭만
- 🤖 자동 스키마 변경 감지
- 🔗 500+ 커넥터: Salesforce, MySQL 등
- 💼 관리형: 유지보수 불필요

**단점**:
- 💰 높은 비용: MAR 기반 폭증 가능
- 🔧 커스터마이징 제한
- 🔒 벤더 종속

**적합한 경우**:
- No-code 선호
- 표준 SaaS 통합 (Salesforce 등)
- 빠른 MVP
- 운영 리소스 < 1명

**검증 사례**: DocuSign, Autodesk, Square

---

#### ETL/ELT 비교표

| 항목 | dbt | Airflow | Fivetran |
|------|-----|---------|----------|
| **언어** | SQL | Python | No-code |
| **비용** | $250~$500/월 | $700~$1.5K/월 | $1K~$10K/월 |
| **배포** | 수 시간 | 1~2주 | 수 시간 |
| **운영** | ⚙️ 낮음 | ⚙️⚙️⚙️ 높음 | ⚙️ 낮음 |
| **유연성** | SQL만 | 무제한 | 제한적 |

**의사결정 가이드**:
```
Python 팀? → Airflow
  └─ NO
     ↓
복잡한 로직 필요? → Airflow
  └─ NO
     ↓
표준 SaaS 통합? → Fivetran
  └─ NO → dbt
```

---

### 2.3 BI/시각화 선택

**패밀리 요구**:
- 대시보드 생성
- 드릴다운 분석
- 스케줄 리포트
- 공유 및 권한 관리

---

#### 옵션 1: Tableau

**핵심 스펙**:
- **배포**: Desktop, Server, Cloud
- **라이선스**: Creator, Explorer, Viewer
- **커넥터**: 100+ 데이터 소스

**비용**:
- **Creator**: $70/user/월
- **Explorer**: $42/user/월
- **Viewer**: $15/user/월
- **예상** (5 Creator, 20 Viewer): 월 $650

**장점**:
- 🎨 강력한 시각화
- 📊 드래그앤드롭: No-code
- 🔗 다양한 커넥터
- 📈 대규모 조직 지원

**단점**:
- 💰 높은 비용
- 🔧 서버 운영 필요 (온프렘)
- 📚 러닝 커브

**적합한 경우**:
- 대기업
- 복잡한 시각화
- 많은 Viewer

**검증 사례**: LinkedIn, Walmart, Verizon

---

#### 옵션 2: Google Looker

**핵심 스펙**:
- **배포**: Cloud only
- **모델링**: LookML (YAML 기반)
- **임베딩**: API 지원

**비용**:
- **Standard**: $5,000+/월 (10 users)
- **Enterprise**: 맞춤형
- **예상**: 월 $5,000~$20,000

**장점**:
- 🔗 GCP 통합
- 📊 LookML: 코드 기반 모델링
- 🔧 임베딩: 제품 통합

**단점**:
- 💰 매우 비쌈
- 🔒 GCP 종속
- 📚 LookML 러닝 커브

**적합한 경우**:
- GCP 중심
- 개발자 중심 팀
- 임베딩 필수

**검증 사례**: BuzzFeed, Warby Parker, Venmo

---

#### 옵션 3: Power BI

**핵심 스펙**:
- **배포**: Desktop, Service, Premium
- **라이선스**: Pro, Premium Per User

**비용**:
- **Pro**: $10/user/월
- **Premium Per User**: $20/user/월
- **예상** (20 users): 월 $200~$400

**장점**:
- 💵 저렴함
- 🔗 Microsoft 생태계
- 📊 Excel 친화적

**단점**:
- 🔒 Windows 권장
- 📉 복잡한 시각화 제약

**적합한 경우**:
- Microsoft 생태계
- 예산 제약
- Excel 중심 팀

**검증 사례**: Adobe, HP, Coca-Cola

---

#### BI 비교표

| 항목 | Tableau | Looker | Power BI |
|------|---------|--------|----------|
| **비용** | $650/월 | $5K+/월 | $200/월 |
| **시각화** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **러닝 커브** | 중간 | 높음 | 낮음 |

**의사결정 가이드**:
```
예산 > $5K/월? → Tableau or Looker
  └─ NO
     ↓
GCP 중심? → Looker
  └─ NO
     ↓
Microsoft 생태계? → Power BI
  └─ NO → Tableau
```

---

## Part 3: 도메인 선택 요소 (프로젝트별)

이 요소들은 **패밀리와 무관**하게 프로젝트 요구사항에 따라 선택합니다.

### 3.1 프론트엔드 프레임워크
- React, Vue, Angular (BI 임베딩 시)

### 3.2 백엔드 API
- REST API for 대시보드 데이터
- GraphQL for 복잡한 쿼리

### 3.3 인증/권한
- SSO, SAML (BI 통합)
- Row-Level Security (RLS)

### 3.4 모니터링
- Datadog, New Relic (파이프라인 모니터링)

---

## Part 4: Stage 2 통합

### 4.1 Layer 3 제약 반영 예시

**시나리오**: 금융 리포팅 시스템

**Layer 3 제약 발견**:
- 규제: SOX, GDPR 준수
- 비용: 쿼리 비용 제한 ($5K/월)
- 팀: SQL 중심 (Python 약함)

**기술 선택 영향**:
```
DW:
- BigQuery (선호) → Snowflake
- 이유: SOX 준수 인증, Time Travel

ETL:
- Airflow (선호) → dbt
- 이유: SQL 중심 팀

BI:
- Looker (선호) → Tableau
- 이유: 비용 ($650 vs $5K)
```

---

### 4.2 충돌 해결 예시

**NFR 목표 vs Layer 3 제약**:

**충돌 1**: 정확성 A + 비용 제약
- NFR: 100% 정확, 실시간 대시보드
- 제약: 쿼리 비용 $5K/월
- **해결**: Materialized Views + 1시간 새로고침

**충돌 2**: 속도 A + 팀 역량
- NFR: 초 단위 쿼리
- 제약: SQL만 가능 (Python 약함)
- **해결**: DW 내 최적화 (Clustering, Partitioning)

---

### 4.3 ADR 작성 준비

**선택한 기술 스택 정리**:
```
Bootstrap 필수:
✅ DW: Snowflake (SOX, Time Travel)
✅ ETL: dbt (SQL 중심)
✅ BI: Tableau (비용 효율)

도메인 선택:
✅ 인증: Okta SSO
✅ 모니터링: Datadog
```

**ADR 작성 대상**:
1. DW 선택 (Snowflake vs Redshift)
2. ETL 선택 (dbt vs Airflow)
3. BI 선택 (Tableau vs Looker)
4. 새로고침 주기 (1시간 vs 실시간)

---

**마지막 업데이트**: 2025-11-12  
**다음 검토**: 2026-02-12 (기술 스택 업데이트 반영)
