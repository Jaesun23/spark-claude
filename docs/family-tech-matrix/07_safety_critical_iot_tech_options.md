# 안전-임계 IoT 패밀리 (A-B-A) - 기술 매트릭스

**작성일**: 2025-11-12  
**패밀리**: 안전-임계 IoT (A-B-A)  
**검증 사례**: SCADA (5-250ms), IoT 긴급 경보 (450ms), 산업 안전 시스템

---

## Part 1: 패밀리가 요구하는 시스템 구조 ⭐⭐⭐

### 1.1 A-B-A 특성이 강제하는 것

#### A (치명적 실패) → 안전 시스템 필수

**특성**:
- 실패 시 인명 손실, 재산 피해
- 산업 재해, 화재, 폭발 위험
- 긴급 대응 필수 (경보, 셧다운)
- 규제 준수 (SIL 2+, UL, IEC)

**강제되는 기술적 요구**:
```
✅ Fail-Safe 설계 (기본값 안전)
✅ 중복성 (Redundancy)
✅ 워치독 (Watchdog) 타이머
✅ 감사 로그 (Audit Trail)
✅ 긴급 셧다운 (Emergency Shutdown)
```

**검증 사례**:
- 산업 제어 시스템 (SCADA): 센서 고장 시 자동 정지
- 긴급 경보 (EAS): 10분 내 전국 경보, FEMA/FCC

---

#### B (반구조화 데이터) → 센서 융합 필수

**특성**:
- JSON, XML 센서 데이터
- 가변 스키마 (센서별 다른 필드)
- 시계열 데이터 (온도, 압력, 진동)
- 다중 센서 융합 (Sensor Fusion)

**강제되는 기술적 요구**:
```
✅ 유연한 스키마 (Flexible Schema)
✅ 시계열 DB (Time-Series DB)
✅ 센서 융합 알고리즘
✅ JSON/XML 파싱
✅ 동적 필드 처리
```

**검증 사례**:
- IoT 센서: 온도 + 습도 + 진동 + 가스 농도
- SCADA: PLCraw 데이터 + 알람 메시지 + 상태 정보

---

#### A (밀리초 응답) → 실시간 처리 필수

**특성**:
- SCADA: 5-250ms 응답
- 긴급 경보: 450ms 미만
- 산업 제어: 수 밀리초 루프
- Edge Computing 필수

**강제되는 기술적 요구**:
```
✅ Edge Computing (로컬 처리)
✅ 경량 프로토콜 (MQTT, CoAP)
✅ 비동기 처리
✅ 우선순위 큐
✅ 저지연 네트워크 (5G, LoRaWAN)
```

**검증 사례**:
- Uber GPS: 2-5초 위치 업데이트
- 제조 안전: 밀리초급 센서-액추에이터 루프

---

### 1.2 Bootstrap 필수 요소 (패밀리 강제)

A-B-A 패밀리는 다음 3가지 시스템 요소를 **반드시** 포함해야 합니다:

#### 1. IoT 메시징 (MQTT/AMQP) (필수!)
**역할**: 센서 데이터 수집, 명령 전송
**이유**: 반구조화(B) + 밀리초(A)
**선택지**: EMQX, AWS IoT Core, RabbitMQ

#### 2. 시계열 DB (필수!)
**역할**: 센서 데이터 저장, 이력 조회
**이유**: 반구조화(B) + 시계열
**선택지**: InfluxDB, TimescaleDB, DynamoDB

#### 3. Edge Computing (필수!)
**역할**: 로컬 실시간 처리, 긴급 대응
**이유**: 치명적(A) + 밀리초(A)
**선택지**: AWS IoT Greengrass, Azure IoT Edge, K3s

---

## Part 2: Bootstrap 요소별 기술 선택 ⭐⭐⭐

### 2.1 IoT 메시징 선택

**패밀리 요구**:
- 경량 프로토콜 (배터리 제약)
- QoS 보장 (메시지 손실 방지)
- 대규모 연결 (수만~수백만 센서)
- 낮은 레이턴시 (밀리초~초)

---

#### 옵션 1: EMQX (Enterprise)

**핵심 스펙**:
- **연결 처리량**: 500만+ 동시 연결
- **메시지 처리량**: 초당 100만+ 메시지
- **레이턴시**: 밀리초 미만 (단일 홉)
- **프로토콜**: MQTT 3.1/3.1.1/5.0, MQTT-SN, CoAP, LwM2M

**비용**:
- **오픈소스**: 무료 (EMQX Broker)
- **Enterprise**: $5,000~$20,000/년 (노드당)
- **클라우드**: $0.15~$0.30/million messages

**장점**:
- ⚡ 초대규모 확장 (500만+ 연결)
- 🔧 완벽한 MQTT 지원
- 📡 다중 프로토콜 (MQTT, CoAP, LwM2M)
- 💪 고가용성 (클러스터링)
- 🔐 TLS/SSL, 인증/권한

**단점**:
- 💰 Enterprise 고가
- 🧑‍💻 복잡한 운영 (클러스터)
- 📚 학습 곡선
- 🔧 튜닝 필요

**적합한 경우**:
- 산업 IoT (수만~수백만 센서)
- SCADA, 스마트 팩토리
- 높은 신뢰성 필수
- 예산 $20K~$100K /year

**검증 사례**: 중국 제조업, 스마트 시티 프로젝트

---

#### 옵션 2: AWS IoT Core

**핵심 스펙**:
- **연결 처리량**: 무제한 (자동 확장)
- **메시지 처리량**: 사용량 기반
- **레이턴시**: 수십~수백 밀리초
- **프로토콜**: MQTT, MQTT over WebSocket, HTTPS

**비용**:
- **연결 비용**: $0.08/million connection-minutes
- **메시지 비용**: $1/million messages (first 1B/월)
- **예상**: 월 $1,000~$10,000 (중규모)

**장점**:
- 🤖 완전 관리형 (운영 부담 없음)
- 🚀 무제한 확장
- 🔗 AWS 통합 (Lambda, S3, DynamoDB)
- 🔐 강력한 보안 (X.509 인증)
- 📊 내장 규칙 엔진

**단점**:
- 🔒 AWS 종속
- 💰 대규모 시 비용 급증
- 📊 제한적 프로토콜 (MQTT 중심)
- 🌐 글로벌 배포 복잡

**적합한 경우**:
- AWS 중심 조직
- 소규모~중규모 (수만~수십만 센서)
- 빠른 프로토타이핑
- 운영 부담 최소화

**검증 사례**: 스마트 홈, 소규모 공장 자동화

---

#### 옵션 3: RabbitMQ (MQTT 플러그인)

**핵심 스펙**:
- **연결 처리량**: 수만~수십만 연결
- **메시지 처리량**: 초당 3만 메시지
- **레이턴시**: 밀리초~초
- **프로토콜**: MQTT, AMQP, STOMP, HTTP

**비용**:
- **오픈소스**: 무료
- **Self-hosted**: 월 $200~$2,000 (VM 비용)
- **CloudAMQP**: $19~$1,199/월

**장점**:
- 💰 저렴한 비용
- 📚 성숙한 기술
- 🔧 간단한 운영
- 🔌 다양한 프로토콜
- 💪 메시지 라우팅 유연성

**단점**:
- 📉 제한적 확장 (수만 연결)
- ⚡ EMQX 대비 낮은 성능
- 🔧 MQTT 기능 제한 (플러그인)
- 📊 대규모 IoT 부적합

**적합한 경우**:
- 소규모 IoT (수천~수만 센서)
- 레거시 통합 (AMQP)
- 예산 $5K~$30K /year
- 간단한 아키텍처

**검증 사례**: 스타트업 IoT, 빌딩 자동화

---

#### IoT 메시징 비교표

| 항목 | EMQX | AWS IoT Core | RabbitMQ |
|------|------|--------------|----------|
| **연결 수** | 500만+ | 무제한 | 수만 |
| **메시지/초** | 100만+ | 사용량 기반 | ~3만 |
| **레이턴시** | <10ms | 수십~수백ms | 밀리초~초 |
| **비용** | $5K~$20K/년 | $1K~$10K/월 | $200~$2K/월 |
| **운영** | ⚙️⚙️⚙️ 높음 | ⚙️ 낮음 | ⚙️⚙️ 중간 |

**의사결정 가이드**:
```
센서 > 10만? → EMQX
  └─ NO
     ↓
AWS 중심? → AWS IoT Core
  └─ NO
     ↓
센서 < 5만? → RabbitMQ
  └─ NO → AWS IoT Core
```

---

### 2.2 시계열 DB 선택

**패밀리 요구**:
- 빠른 쓰기 (초당 수십만~수백만 포인트)
- 시간 기반 쿼리 최적화
- 압축 (저장 공간 절약)
- 다운샘플링 (Downsampling)

---

#### 옵션 1: InfluxDB (Enterprise)

**핵심 스펙**:
- **쓰기 처리량**: 초당 100만+ 포인트
- **압축**: 10:1 이상
- **레이턴시**: 밀리초 미만 (쓰기)
- **보존 정책**: 자동 다운샘플링

**비용**:
- **오픈소스**: 무료 (InfluxDB OSS)
- **Cloud**: $50~$500/월
- **Enterprise**: $10,000~$50,000/년

**장점**:
- ⚡ 초고속 쓰기
- 🔧 IoT 최적화 (Telegraf 통합)
- 📊 강력한 쿼리 (Flux, InfluxQL)
- 💾 효율적 압축
- 🕐 자동 다운샘플링

**단점**:
- 💰 Enterprise 고가
- 📊 제한적 분산 (클러스터링 Enterprise만)
- 🔧 메모리 사용량 높음
- 📈 대규모 확장 어려움

**적합한 경우**:
- IoT 센서 데이터 (초당 수십만 포인트)
- SCADA, 제조 라인
- 실시간 대시보드
- 예산 $10K~$100K /year

**검증 사례**: Cisco IoT, Salesforce 모니터링

---

#### 옵션 2: TimescaleDB (PostgreSQL 확장)

**핵심 스펙**:
- **쓰기 처리량**: 초당 10만 포인트
- **압축**: Native 압축 (7:1)
- **레이턴시**: <10ms (쓰기)
- **쿼리**: Full SQL 지원

**비용**:
- **오픈소스**: 무료
- **Timescale Cloud**: $50~$500/월
- **Enterprise**: $5,000~$20,000/년

**장점**:
- 🔍 Full SQL 지원
- 📊 복잡한 조인 가능
- 🛠️ PostgreSQL 생태계
- 💰 상대적 저렴
- 🔧 익숙한 운영

**단점**:
- ⚡ InfluxDB 대비 느림
- 📈 확장 제한 (vs 분산 DB)
- 💾 압축률 낮음
- 🔧 튜닝 필요

**적합한 경우**:
- SQL 필수 (복잡한 분석)
- PostgreSQL 팀 역량
- 중소규모 (초당 수만 포인트)
- 예산 $5K~$50K /year

**검증 사례**: 에너지 모니터링, 스마트 빌딩

---

#### 옵션 3: DynamoDB (AWS)

**핵심 스펙**:
- **쓰기 처리량**: 사용량 기반 (무제한)
- **레이턴시**: 단일 자릿수 밀리초
- **확장**: 자동 스케일링
- **TTL**: 자동 데이터 만료

**비용**:
- **On-Demand**: $1.25/million writes
- **Provisioned**: $0.00065/WCU/hour
- **예상**: 월 $500~$5,000

**장점**:
- 🤖 완전 관리형
- 🚀 무제한 확장
- 🔗 AWS 통합
- 💵 사용량 기반 과금
- 🕐 자동 TTL

**단점**:
- 🔒 AWS 종속
- 💰 대규모 시 비용 급증
- 📊 제한적 쿼리 (NoSQL)
- 🔧 시계열 최적화 부족

**적합한 경우**:
- AWS 중심
- 소규모~중규모
- 빠른 프로토타이핑
- 운영 부담 최소화

**검증 사례**: AWS IoT 사용자, 스타트업

---

#### 시계열 DB 비교표

| 항목 | InfluxDB | TimescaleDB | DynamoDB |
|------|----------|-------------|----------|
| **쓰기/초** | 100만+ | 10만 | 사용량 기반 |
| **SQL** | Flux/InfluxQL | ✅ Full SQL | ❌ NoSQL |
| **압축** | 10:1 | 7:1 | N/A |
| **비용** | $10K~$50K/년 | $5K~$20K/년 | $500~$5K/월 |
| **운영** | ⚙️⚙️ 중간 | ⚙️⚙️ 중간 | ⚙️ 낮음 |

**의사결정 가이드**:
```
쓰기 > 10만/초? → InfluxDB
  └─ NO
     ↓
SQL 필수? → TimescaleDB
  └─ NO
     ↓
AWS 중심? → DynamoDB
  └─ NO → InfluxDB
```

---

### 2.3 Edge Computing 선택

**패밀리 요구**:
- 로컬 실시간 처리 (밀리초)
- 오프라인 동작 (네트워크 단절 시)
- 경량 (저전력, 제한된 리소스)
- 클라우드 동기화

---

#### 옵션 1: AWS IoT Greengrass

**핵심 스펙**:
- **레이턴시**: 밀리초급 (로컬)
- **언어**: Python, Node.js, Java, C++
- **배포**: Over-the-Air (OTA)
- **오프라인**: 완전 지원

**비용**:
- **소프트웨어**: 무료
- **디바이스**: $10~$500 (하드웨어)
- **클라우드 연동**: AWS IoT Core 비용

**장점**:
- ⚡ 로컬 실시간 처리
- 🔗 AWS 완벽 통합
- 🤖 Lambda 로컬 실행
- 🔐 강력한 보안 (X.509)
- 📡 오프라인 동작

**단점**:
- 🔒 AWS 종속
- 💰 디바이스 비용 (ARM/x86)
- 🔧 복잡한 설정
- 📊 ML 추론 제한적

**적합한 경우**:
- AWS 중심 IoT
- 중간~고성능 Edge (Raspberry Pi 이상)
- 오프라인 필수
- 예산 $100~$500 per device

**검증 사례**: 석유/가스 리모트 모니터링, 스마트 빌딩

---

#### 옵션 2: Azure IoT Edge

**핵심 스펙**:
- **레이턴시**: 밀리초급 (로컬)
- **언어**: C#, Python, Node.js, Java, C
- **컨테이너**: Docker 기반
- **AI**: Azure ML 로컬 배포

**비용**:
- **소프트웨어**: 무료
- **디바이스**: $10~$500 (하드웨어)
- **클라우드 연동**: Azure IoT Hub 비용

**장점**:
- ⚡ 로컬 AI 추론 (ML 모델)
- 🐳 Docker 컨테이너 (표준)
- 🔗 Azure 통합
- 🔐 보안 모듈 (TPM)
- 📡 오프라인 동작

**단점**:
- 🔒 Azure 종속
- 💰 디바이스 비용
- 🧑‍💻 .NET 편향
- 📊 대규모 관리 복잡

**적합한 경우**:
- Azure 중심 조직
- AI/ML 추론 필요
- Docker 친숙
- 예산 $100~$500 per device

**검증 사례**: 제조업 품질 검사 (AI), 소매 매장 분석

---

#### 옵션 3: K3s (경량 Kubernetes)

**핵심 스펙**:
- **메모리**: 512MB RAM 이상
- **언어**: 모든 컨테이너화 앱
- **배포**: GitOps (Flux, ArgoCD)
- **클라우드**: 멀티 클라우드 지원

**비용**:
- **오픈소스**: 무료
- **디바이스**: $10~$200 (하드웨어)
- **관리**: Rancher (무료/Enterprise)

**장점**:
- 💰 완전 무료 (오픈소스)
- 🌐 멀티 클라우드 (AWS, Azure, GCP)
- 🔧 표준 Kubernetes API
- 🐳 모든 컨테이너 지원
- 📚 풍부한 생태계

**단점**:
- 🧑‍💻 Kubernetes 학습 곡선
- 🔧 직접 운영 필요
- 📊 클라우드 통합 별도 구현
- ⚠️ IoT 최적화 부족

**적합한 경우**:
- 멀티 클라우드 전략
- Kubernetes 팀 역량
- 예산 최소화
- 완전한 제어 필요

**검증 사례**: 엣지 AI 플랫폼, 스마트 시티 게이트웨이

---

#### Edge Computing 비교표

| 항목 | AWS Greengrass | Azure IoT Edge | K3s |
|------|----------------|----------------|-----|
| **레이턴시** | 밀리초 | 밀리초 | 밀리초 |
| **AI 추론** | 제한적 | ✅ Azure ML | ✅ 모든 프레임워크 |
| **오프라인** | ✅ | ✅ | ✅ |
| **비용** | AWS 연동 | Azure 연동 | 무료 |
| **운영** | ⚙️⚙️ 중간 | ⚙️⚙️ 중간 | ⚙️⚙️⚙️ 높음 |

**의사결정 가이드**:
```
AWS 중심? → AWS IoT Greengrass
  └─ NO
     ↓
AI 추론 필요? → Azure IoT Edge
  └─ NO
     ↓
멀티 클라우드? → K3s
  └─ NO → AWS IoT Greengrass
```

---

## Part 3: 도메인 선택 요소 (프로젝트별)

이 요소들은 **패밀리와 무관**하게 프로젝트 요구사항에 따라 선택합니다.

### 3.1 센서 하드웨어

**선택지**:
- **Raspberry Pi 4**: 범용, Linux, Python/C++
- **Arduino**: 저전력, 실시간, C/C++
- **ESP32**: WiFi/BLE, 초저전력, MicroPython
- **산업용 PLC**: Siemens, Allen-Bradley (규제 인증)

**선택 기준**:
- 처리 능력: 복잡한 센서 융합 → Raspberry Pi
- 저전력: 배터리 → Arduino, ESP32
- 산업 표준: 규제 준수 → PLC

**A-B-A 영향**: **큼** - 실시간 처리(A) + 센서 융합(B) 요구  
(Edge Computing 성능 결정)

---

### 3.2 통신 프로토콜

**선택지**:
- **WiFi**: 고대역폭, 짧은 거리, 실내
- **4G/5G**: 이동성, 넓은 범위, 고비용
- **LoRaWAN**: 초저전력, 장거리 (수 km), 저속 (50kbps)
- **Zigbee**: 저전력, 메쉬 네트워크, 짧은 거리

**선택 기준**:
- 레이턴시: 밀리초(A) → WiFi, 4G/5G
- 저전력: 배터리 수명 → LoRaWAN, Zigbee
- 이동성: 차량, 드론 → 4G/5G
- 범위: 공장/건물 → WiFi, Zigbee

**A-B-A 영향**: **매우 큼** - 밀리초(A) 달성 가능 여부  
(WiFi: 5-50ms, 4G: 50-100ms, LoRaWAN: 1-5초)

---

### 3.3 대시보드/시각화

**선택지**:
- **Grafana**: 오픈소스, 시계열, Prometheus 통합
- **Kibana**: Elasticsearch, 로그 중심
- **Power BI**: 엔터프라이즈, Microsoft 생태계
- **Custom Web**: React, D3.js (맞춤형)

**선택 기준**:
- 실시간 모니터링: Grafana (초 단위 갱신)
- 로그 분석: Kibana (ELK Stack)
- 비즈니스 리포트: Power BI (주간/월간)
- 특수 요구사항: Custom Web

**A-B-A 영향**: 최소 (패밀리 무관, 사용자 선호도)

---

### 3.4 클라우드 vs 온프레미스

**선택지**:
- **클라우드**: AWS IoT, Azure IoT (확장성, 관리 편의)
- **하이브리드**: Edge + 클라우드 (로컬 처리 + 중앙 집계)
- **온프레미스**: 완전 자체 호스팅 (데이터 주권, 규제)

**선택 기준**:
- 밀리초 응답(A): 하이브리드 또는 온프레미스 (네트워크 지연 회피)
- 규제: 데이터 주권, SIL 인증 → 온프레미스
- 확장성: 수십만 센서 → 클라우드

**A-B-A 영향**: **큼** - 치명적 실패(A) + 밀리초(A) 요구  
(클라우드 왕복 100-500ms → 로컬 처리 필수)

---

## Part 4: Stage 2 통합

### 4.1 Layer 3 제약 반영 예시

**시나리오**: 제조 공장 안전 시스템

**Layer 3 제약 발견**:
- 규제: SIL 2 인증 필수 (IEC 61508)
- 네트워크: 공장 WiFi 불안정 (패킷 손실 5%)
- 예산: $100K/년 (전체)
- 기존 시스템: Siemens PLC (Profinet)

**기술 선택 영향**:
```
IoT 메시징:
- EMQX (선호) → RabbitMQ
- 이유: 예산 제약, Profinet 연동

시계열 DB:
- InfluxDB (선호) → TimescaleDB
- 이유: SQL 필수 (규제 보고), 예산

Edge Computing:
- AWS Greengrass (불가능) → K3s
- 이유: 공장 내 온프레미스, 오프라인
```

---

### 4.2 충돌 해결 예시

**NFR 목표 vs Layer 3 제약**:

**충돌 1**: 밀리초 응답 A + WiFi 불안정
- **NFR**: 450ms 미만 경보 응답
- **제약**: 공장 WiFi 불안정 (패킷 손실 5%)
- **해결**: Edge Computing 필수 (로컬 처리) + 유선 백업
- **트레이드오프**:
  - ✅ 로컬 처리로 50ms 응답 달성 (WiFi 독립)
  - ✅ 네트워크 장애 시에도 작동
  - ⚠️ Edge 디바이스 비용 증가 ($200~$500/센서)
  - ⚠️ 유선 백업 설치 비용 ($50~$100/센서)
  - ⚠️ 유지보수 복잡도 증가 (센서별 업데이트)

---

**충돌 2**: 치명적 실패 A + 예산 제약
- **NFR**: SIL 2 인증 필수 (안전 규제)
- **제약**: 예산 $100K/년 (EMQX Enterprise, InfluxDB Enterprise 불가)
- **해결**: 오픈소스 스택 (RabbitMQ + TimescaleDB + K3s) + 외부 인증 비용
- **트레이드오프**:
  - ⚠️ 확장성 제한 (수만 센서까지, 수백만 불가)
  - ⚠️ 고가용성 구성 복잡 (직접 클러스터링)
  - ✅ 소프트웨어 비용 $50K/년 → $10K/년 (80% 절감)
  - ✅ SIL 2 인증 $30K (외부 인증 기관)
  - ✅ 총 예산 $40K/년 (목표 $100K 내)

---

**충돌 3**: 센서 융합 B + 레거시 PLC
- **NFR**: JSON 센서 데이터 (온도, 습도, 진동 융합)
- **제약**: Siemens PLC (Profinet 바이너리 프로토콜)
- **해결**: Edge Gateway 변환 (Profinet → MQTT/JSON)
- **트레이드오프**:
  - ⚠️ 레이턴시 추가 10-50ms (변환 오버헤드)
  - ⚠️ Gateway 단일 장애 지점 (SPOF)
  - ⚠️ Gateway 비용 $2,000~$5,000
  - ✅ 레거시 PLC 활용 (교체 불필요)
  - ✅ 표준 MQTT 인프라 구축
  - ✅ 향후 센서 추가 용이

**추가 해결**: Gateway 이중화 (Active-Standby)  
**추가 비용**: $3,000~$6,000 (Gateway 2대)

---

### 4.3 ADR 작성 준비

**선택한 기술 스택 정리**:
```
Bootstrap 필수:
✅ IoT 메시징: RabbitMQ (MQTT 플러그인)
✅ 시계열 DB: TimescaleDB
✅ Edge Computing: K3s (온프레미스)

도메인 선택:
✅ 센서: Raspberry Pi 4 + DHT22 + MCP3008
✅ 통신: WiFi (주) + 유선 Ethernet (백업)
✅ 대시보드: Grafana + Prometheus
```

**ADR 작성 대상**:
1. IoT 메시징 선택 (EMQX vs RabbitMQ)
2. 시계열 DB 선택 (InfluxDB vs TimescaleDB)
3. Edge Computing 전략 (Greengrass vs K3s)
4. 네트워크 이중화 방안 (WiFi + 유선)
5. SIL 2 인증 경로

---

## 📚 참고 자료

### IoT 메시징 벤치마크
- [EMQX Performance](https://www.emqx.com/en/products/emqx/performance)
- [AWS IoT Core Limits](https://docs.aws.amazon.com/general/latest/gr/iot-core.html)

### 시계열 DB 벤치마크
- [InfluxDB Performance](https://www.influxdata.com/influxdb-performance/)
- [TimescaleDB Benchmark](https://docs.timescale.com/timescaledb/latest/overview/how-it-works/)

### Edge Computing
- [AWS IoT Greengrass](https://aws.amazon.com/greengrass/)
- [Azure IoT Edge](https://azure.microsoft.com/en-us/products/iot-edge/)
- [K3s](https://k3s.io/)

### 산업 표준
- [IEC 61508: SIL](https://en.wikipedia.org/wiki/IEC_61508)
- [ISA-95: 제조 표준](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95)

### 검증 사례
- [IoT 긴급 경보 시스템](https://www.fcc.gov/emergency-alert-system-eas)
- [SCADA 시스템](https://en.wikipedia.org/wiki/SCADA)

---

**마지막 업데이트**: 2025-11-12  
**다음 검토**: 2026-02-12 (기술 스택 업데이트 반영)
