# NFR (Non-Functional Requirements) 정의

## 핵심 NFR 속성

DNA v4.0에서 사용하는 8개 핵심 NFR 속성입니다.

---

### 1. Performance (성능)
**정의**: 시스템의 응답 시간과 처리 속도

**측정 지표**:
- Latency: p50, p95, p99 응답시간
- Throughput: TPS (Transactions Per Second)
- Resource efficiency: CPU/Memory 사용률

**수준 예시**:
- A (High): < 10ms p99
- B (Medium): 10-100ms p99
- C (Low): > 100ms p99

---

### 2. Consistency (일관성)
**정의**: 데이터 정확성과 동기화 수준

**유형**:
- Strong: ACID 트랜잭션, 즉시 일관성
- Eventual: 최종적 일관성, 일시적 불일치 허용
- Causal: 인과관계만 보장

**수준 예시**:
- A: Strong consistency (금융, 의료)
- B: Eventual consistency (SNS, 로그)

---

### 3. Availability (가용성)
**정의**: 시스템이 정상 작동하는 시간 비율

**측정 지표**:
- Uptime: 99.9% (3 nines), 99.99% (4 nines)
- MTBF: 평균 장애 간격
- MTTR: 평균 복구 시간

**수준 예시**:
- A: 99.99% (연간 52분 다운타임)
- B: 99.9% (연간 8.7시간)
- C: 99% (연간 3.65일)

---

### 4. Scalability (확장성)
**정의**: 부하 증가에 따른 확장 능력

**유형**:
- Horizontal: 노드 추가로 확장
- Vertical: 리소스 업그레이드로 확장

**측정 지표**:
- Linear scalability: 노드 2배 → 성능 2배
- Elasticity: 자동 확장/축소 속도

---

### 5. Reliability (신뢰성)
**정의**: 오류 없이 기능을 수행하는 능력

**측정 지표**:
- Error rate: 오류 발생 비율
- Data durability: 데이터 손실 확률
- Fault tolerance: 장애 내성

**수준 예시**:
- A: 11 nines durability (S3 수준)
- B: 99.99% durability

---

### 6. Security (보안)
**정의**: 데이터와 시스템 보호 수준

**영역**:
- Authentication: 사용자 인증
- Authorization: 권한 관리
- Encryption: 데이터 암호화
- Audit: 감사 로깅

**수준 예시**:
- A: 금융/의료 수준 (PCI-DSS, HIPAA)
- B: 일반 웹 서비스 수준

---

### 7. Maintainability (유지보수성)
**정의**: 시스템 수정과 확장의 용이성

**측정 지표**:
- Code complexity: 순환 복잡도
- Test coverage: 테스트 커버리지
- Documentation: 문서화 수준
- Deployment frequency: 배포 빈도

---

### 8. Observability (관측성)
**정의**: 시스템 내부 상태를 파악하는 능력

**3가지 기둥**:
- Logs: 이벤트 기록
- Metrics: 수치 데이터
- Traces: 요청 추적

---

## NFR 우선순위 매트릭스

### 패밀리별 NFR 우선순위

| 패밀리 | 1순위 | 2순위 | 3순위 |
|--------|-------|-------|-------|
| 초고속 거래 | Performance | Consistency | Availability |
| 트랜잭션/CRUD | Consistency | Reliability | Performance |
| 협업/동기화 | Availability | Performance | Consistency |
| 검색/추천 | Scalability | Performance | Availability |
| 실시간 스트리밍 | Performance | Scalability | Reliability |
| 분석/배치 | Reliability | Scalability | Performance |
| 안전-임계 IoT | Reliability | Security | Consistency |

---

## NFR 트레이드오프

### CAP 정리 기반
- CP (Consistency + Partition tolerance): 금융, 재고
- AP (Availability + Partition tolerance): SNS, 검색

### 일반적 트레이드오프
- Performance ↔ Consistency
- Availability ↔ Consistency
- Security ↔ Performance
- Maintainability ↔ Performance

---

## NFR 수치화 가이드

### 구체적 질문으로 수치화

**성능**:
- "최대 허용 응답시간은?" → 100ms
- "동시 사용자 수는?" → 10,000명

**가용성**:
- "다운타임 허용치는?" → 연간 1시간
- "복구 목표 시간은?" → 15분

**확장성**:
- "피크 대비 평상시 트래픽 비율?" → 10배
- "향후 3년 성장 예상치?" → 5배

이 수치들이 Stage 2에서 기술 선택의 근거가 됩니다.
