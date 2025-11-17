# 03G-00: ADR 작성 가이드 (Architecture Decision Records Guide)

**문서 버전**: 1.0
**작성일**: 2025-11-17
**대상**: DNA Methodology v4.0 Stage 3
**목적**: Architecture Decision Records (ADR) 작성 방법 및 5가지 카테고리별 템플릿 제공

---

## 📋 목차

- [Part 1: ADR이란 무엇인가](#part-1-adr이란-무엇인가)
- [Part 2: DNA v4.0 ADR 5 Categories](#part-2-dna-v40-adr-5-categories)
- [Part 3: ADR 작성 프로세스 (4 Steps)](#part-3-adr-작성-프로세스-4-steps)
- [Part 4: 실전 예시](#part-4-실전-예시)
- [Part 5: 엔터프라이즈 사례](#part-5-엔터프라이즈-사례)
- [Appendix: 템플릿 Quick Reference](#appendix-템플릿-quick-reference)

---

## Part 1: ADR이란 무엇인가

### 1.1 ADR의 정의

**Architecture Decision Record (ADR)**는 소프트웨어 아키텍처에서 중요한 결정을 기록하는 문서입니다.

**핵심 요소:**
- **What**: 무엇을 결정했는가
- **Why**: 왜 그 결정을 했는가
- **Alternatives**: 다른 선택지는 무엇이었는가
- **Consequences**: 이 결정의 영향은 무엇인가

### 1.2 왜 ADR이 필요한가?

**인간 협업 관점:**
- ✅ 의사결정 투명성 (왜 이렇게 설계했는지 추적)
- ✅ 지식 전달 (새로운 팀원의 빠른 온보딩)
- ✅ 일관성 유지 (같은 문제에 대해 다른 결정 방지)

**AI 협업 관점 (DNA v4.0 특화):**
- ✅ 컨텍스트 손실 방지 (AI는 200K 토큰 제약)
- ✅ 명시적 규칙 (AI는 암묵적 지식 이해 불가)
- ✅ 자동화 가능 (ADR → Standards → Enforcement 체인)

### 1.3 엔터프라이즈 vs DNA v4.0 ADR

#### 엔터프라이즈 접근 (Kubernetes, GitLab, Terraform)

**문서 형태**: KEP, Design Doc, Architecture Blueprints
- 거대한 통합 문서 (수천 줄)
- Motivation + Proposal + Alternatives를 한 문서에
- 인간 Code Review로 일관성 강제

**예: Kubernetes KEP-17**
```markdown
# KEP-17: Resource Versioning
## Motivation       ← DNA Stage 1-2 (왜 필요?)
## Proposal         ← DNA Stage 7 (어떻게 구현?)
## Alternatives     ← DNA Stage 2-3 (왜 이 방법?)
```

#### DNA v4.0 접근 (AI 협업 최적화)

**문서 형태**: 분리된 Stage별 문서
- Stage 3 ADR (결정만, 200-500줄)
- Stage 6 Standards (규칙)
- Stage 9 Governance (자동화)
- 명시적 Standards + 자동화로 일관성 강제

**핵심 차이:**

| 항목 | 엔터프라이즈 | DNA v4.0 |
|------|-------------|----------|
| **목적** | 인간 커뮤니케이션 | AI 협업 + 자동화 |
| **문서 크기** | 5,000+ 줄 통합 | 500줄 이하 분리 |
| **일관성 강제** | Code Review (인간) | Automation (AI) |
| **지식 형태** | 암묵적 OK | 명시적 필수 |

**Why DNA v4.0 방식?**
- AI = 200K 토큰 제약 → 큰 문서 처리 어려움
- AI = 컨텍스트 손실 → 명시적 규칙 필요
- AI = 반복 실수 → 자동화 강제 필수

---

## Part 2: DNA v4.0 ADR 5 Categories

### 2.1 5 Categories 개요

DNA v4.0은 ADR을 **목적별로 5가지 카테고리**로 분류합니다.

| Category | 개수 | 목적 | 예시 |
|----------|------|------|------|
| 1. External Constraint | 3-5개 | 변경 불가능한 외부 제약 | AWS Seoul Region 강제 |
| 2. Conflict Resolution | 2-3개 | NFR 간 충돌 해결 | 성능 vs 일관성 |
| 3. Technology Stack | 4-6개 | 기술/프레임워크 선택 | FastAPI vs Django |
| 4. Domain Technology | 2-4개 | 도메인 특화 설계 | Priority Queue Scheduler |
| 5. DNA System | 11개 | 전사 표준 시스템 | Structured Logging |

**총 ADR 개수**: 22-29개

**Why 카테고리 분리?**
- 각 카테고리는 **목적이 다름** → 템플릿 구조도 달라야 함
- External Constraint = 대안 없음 (선택지 1개)
- Technology Stack = 대안 비교 필수 (선택지 3-5개)

### 2.2 Category 1: External Constraint ADR

**목적**: 변경 불가능한 외부 요인 기록

**특징**:
- "어쩔 수 없는 선택" (No choice)
- 대안 섹션이 종종 비어있음
- 강제화 방안이 중요 (위반 시 법적/계약 문제)

**템플릿 구조**:
```markdown
# ADR-101: [제약 사항 제목]

## 1. 제약 사항 (Constraint)
- 무엇을 해야 하는가?

## 2. 제약의 출처 (Source of Constraint)
- 법률/규제/표준
- 고객사 요구사항
- API 제약

## 3. 결정 (Decision)
- 제약으로 인해 강제된 기술적 결정

## 4. 대안 (Alternatives Considered)
- 종종 "없음" 또는 "고려 불가"

## 5. 영향 및 파급 효과 (Consequences)
- 시스템에 미치는 영향

## 6. 강제화 방안 (Enforcement)
- IAM Policy, SCP, Policy-as-Code 등
```

**실제 예시**:

```markdown
# ADR-101: AWS 서울 리전 사용 강제

상태: Accepted
날짜: 2025-01-15
카테고리: 1. 외부 제약 (External Constraint)

## 1. 제약 사항 (Constraint)

모든 프로덕션 데이터는 대한민국 내에 위치해야 함.

## 2. 제약의 출처 (Source of Constraint)

- **법률**: 개인정보보호법 제28조의8 (국외 이전 제한)
- **고객사 요구**: XXX 은행 계약 조건 (국내 데이터 센터 필수)

## 3. 결정 (Decision)

AWS Seoul Region (ap-northeast-2)을 유일한 프로덕션 리전으로 사용한다.

## 4. 대안 (Alternatives Considered)

- **대안 1**: NHN Cloud, Naver Cloud (국내)
  - **기각 사유**: 기존 AWS 인프라 활용 위해 AWS 유지 결정
- **대안 2**: AWS Tokyo Region
  - **기각 불가**: 일본은 국외이므로 법률 위반

## 5. 영향 및 파급 효과 (Consequences)

- **긍정적**: 법률 준수, 고객 요구사항 충족
- **부정적**:
  - 타 리전의 신규 AWS 서비스 사용 불가
  - DR(재해 복구) 전략이 국내 타 리전으로 한정됨

## 6. 강제화 방안 (Enforcement)

- **IAM Policy**: SCP (Service Control Policies)로 타 리전 접근 차단
- **Terraform**:
  ```hcl
  terraform {
    required_providers {
      aws = {
        region = "ap-northeast-2"  # 하드코딩 강제
      }
    }
  }
  ```
- **CI/CD**: 배포 스크립트에서 region 검증
```

### 2.3 Category 2: Conflict Resolution ADR

**목적**: Stage 1-2에서 식별된 NFR 간 충돌 해결

**특징**:
- "어쩔 수 없는 타협" (Trade-off)
- 충돌하는 속성을 명시적으로 표현
- 트레이드오프 분석 필수

**템플릿 구조**:
```markdown
# ADR-201: [충돌 해결 제목]

## 1. 충돌하는 품질 속성 (Conflicting Attributes)
- 속성 A (주요 목표): ...
- 속성 B (희생 목표): ...

## 2. 배경 및 문제 (Context)
- 문제 상황 설명

## 3. 고려된 해결 옵션 (Options Considered)
### 옵션 1: Strong Consistency
- 장점/단점

### 옵션 2: Eventual Consistency
- 장점/단점

## 4. 결정 (Decision)
- 선택한 옵션 + 근거

## 5. 영향 및 파급 효과 (Consequences)
- 시스템/팀에 미치는 영향
```

**실제 예시**:

```markdown
# ADR-201: 검색 성능을 위한 최종 일관성 수용

상태: Accepted
날짜: 2025-01-20
카테고리: 2. 충돌 해결 (Conflict Resolution)

## 1. 충돌하는 품질 속성 (Conflicting Attributes)

- **속성 A (주요 목표)**: 검색 성능
  - NFR P-01: 검색 API 응답 시간 < 1초
- **속성 B (희생 목표)**: 데이터 일관성
  - NFR C-01: 상품 정보 변경 즉시 반영

## 2. 배경 및 문제 (Context)

상품 정보 변경 시, 즉각적인 검색 인덱스 갱신은 DB 트랜잭션과 묶여 성능 저하 유발.
- 현재: 동기식 갱신 → API 응답 5초 → P-01 실패

## 3. 고려된 해결 옵션 (Options Considered)

### 옵션 1: Strong Consistency (동기식 갱신)
- **설명**: 상품 DB 변경 트랜잭션 내에서 검색 인덱스 갱신
- **장점**: 데이터 즉시 일관성 보장
- **단점**: API 응답 시간 5초 이상, P-01 실패

### 옵션 2: Eventual Consistency (비동기식 갱신)
- **설명**: 상품 DB 변경 후 Kafka 이벤트 발행 → 워커가 인덱스 갱신
- **장점**: API 응답 시간 100ms 미만, P-01 충족
- **단점**: 최대 30초간 데이터 불일치, C-01 일부 희생

## 4. 결정 (Decision)

**옵션 2 (Eventual Consistency)를 채택한다.**

**근거**:
- 검색 성능(P-01)이 비즈니스 핵심 지표 (매출 직결)
- 30초 이내 데이터 불일치는 수용 가능한 트레이드오프
- 비즈니스 오너 승인 (2025-01-18 회의)

## 5. 영향 및 파급 효과 (Consequences)

- **긍정적**:
  - API 응답 시간 5초 → 100ms (50배 개선)
  - 사용자 경험 대폭 향상
- **부정적**:
  - 최대 30초 데이터 불일치 발생
  - 프론트엔드 팀: "정보 갱신 중..." UX 추가 필요
  - 모니터링: 이벤트 지연 알림 필요
```

### 2.4 Category 3: Technology Stack ADR

**목적**: 기술/프레임워크/라이브러리 선택 비교

**특징**:
- "최선의 선택" (Best choice)
- 정량적 비교표 필수
- 요구사항 기반 평가

**템플릿 구조**:
```markdown
# ADR-301: [기술 선택 제목]

## 1. 배경 및 문제 (Context)
- 해결하려는 문제

## 2. 요구사항 (Requirements)
- R-01: ...
- R-02: ...

## 3. 대안 비교 (Alternatives Comparison)
| 기준 | 옵션 1 | 옵션 2 | 옵션 3 |
|------|--------|--------|--------|
| R-01 | ✅ | 🔺 | ❌ |
| R-02 | ⭐ | ↓ | ↓ |

## 4. 결정 (Decision)
- 선택 + 근거

## 5. 영향 및 파급 효과 (Consequences)
- 긍정적/부정적 영향
```

**실제 예시**:

```markdown
# ADR-301: API 서버로 FastAPI 채택

상태: Accepted
날짜: 2025-01-25
카테고리: 3. 기술 스택 (Technology Stack)

## 1. 배경 및 문제 (Context)

실시간성이 중요한 B-C-A 패밀리 (Stage 1)의 API 서버가 필요하며,
Python 생태계를 활용해야 함 (ML 모델 통합).

## 2. 요구사항 (Requirements)

- R-01: 비동기(Async) 네이티브 지원
- R-02: 높은 성능 (1만 RPS 처리)
- R-03: 자동 API 문서 생성 (Swagger/OpenAPI)
- R-04: 빠른 개발 속도 (타입 힌트 지원)

## 3. 대안 비교 (Alternatives Comparison)

| 기준 | 옵션 1: FastAPI | 옵션 2: Django (DRF) | 옵션 3: Flask |
|------|----------------|---------------------|---------------|
| R-01: 비동기 지원 | ✅ (Native, ASGI) | 🔺 (부분적, ASGI 플러그인) | 🔺 (부분적, ASGI 플러그인) |
| R-02: 높은 성능 | ⭐ (매우 높음, 10K+ RPS) | ↓ (낮음, 2K RPS) | ↓ (낮음, 3K RPS) |
| R-03: API 문서 | ✅ (자동, Pydantic 기반) | ↓ (수동/추가 작업) | ↓ (수동/추가 작업) |
| R-04: 개발 속도 | ✅ (매우 빠름, 타입 강제) | ↓ (느림, 무거움) | ✅ (빠름, 경량) |
| 러닝 커브 | Medium | High | Low |
| 커뮤니티 | 중간 (성장 중) | 매우 큼 | 매우 큼 |

## 4. 결정 (Decision)

**FastAPI를 API 서버 기술 스택으로 채택한다.**

**근거**:
- 모든 요구사항 (R-01~R-04)을 가장 높은 수준으로 만족
- 비동기 네이티브 지원으로 B-C-A 패밀리 목표와 일치
- Pydantic 기반 타입 강제로 AI 협업 시 명시성 확보

## 5. 영향 및 파급 효과 (Consequences)

- **긍정적**:
  - 높은 성능 (10K+ RPS 처리 가능)
  - Pydantic 타입 강제로 안정성 증가
  - 자동 API 문서로 프론트엔드 협업 개선
- **부정적**:
  - Flask/Django 대비 커뮤니티 작음 (참고 자료 부족)
  - ASGI 서버 (Uvicorn) 학습 필요
  - 팀원 교육 2주 소요
```

### 2.5 Category 4: Domain Technology ADR

**목적**: 도메인 특화 설계/패턴 결정

**특징**:
- "문제 해결 필수" (Domain-specific)
- 자체 개발 아키텍처 패턴
- 아키텍처 스케치 포함

**템플릿 구조**:
```markdown
# ADR-401: [도메인 설계 제목]

## 1. 배경 및 문제 (Context)
- 비즈니스 문제

## 2. 결정 (Decision)
- 자체 설계 패턴

## 3. 아키텍처 설계 스케치 (Architecture Sketch)
- 다이어그램 또는 인터페이스 정의

## 4. 고려된 대안 (Alternatives Considered)
- 대안 1, 2, ...

## 5. 영향 및 파급 효과 (Consequences)
- 시스템 복잡도, 성능 등
```

**실제 예시**:

```markdown
# ADR-401: 주식 거래를 위한 우선순위 큐 스케줄러 설계

상태: Accepted
날짜: 2025-02-01
카테고리: 4. 도메인 기술 (Domain Technology)

## 1. 배경 및 문제 (Context)

주식 거래 시스템은 초당 20건의 API Rate Limit이 있으나,
100개의 조건을 감시해야 함.

**문제**:
- 모든 조건을 5초마다 폴링하면 (100/20) 중요 조건이 지연됨
- 중요 조건 (거래 임박)은 1초 내 감지 필요
- 비중요 조건은 10초 주기도 OK

## 2. 결정 (Decision)

**'가중치 기반 우선순위 큐 스케줄러 (Weighted Priority Queue Scheduler)'를
자체 설계하여 도입한다.**

**핵심 로직**:
- 모든 조건 (100개)을 큐에 넣되, '중요 조건'에 높은 가중치 부여
- API 호출 (초당 20건)을 우선순위에 따라 할당
- 중요 조건: 1초 주기, 비중요 조건: 10초 주기

## 3. 아키텍처 설계 스케치 (Architecture Sketch)

### 인터페이스 정의 (의사 코드)

```python
class PriorityScheduler:
    """가중치 기반 우선순위 큐 스케줄러"""

    def add_condition(
        self,
        condition_id: str,
        priority: int  # 1 (highest) ~ 10 (lowest)
    ) -> None:
        """조건 추가"""
        pass

    def get_next_task(self) -> ConditionTask:
        """다음 실행할 조건 반환 (가중치 기반)"""
        pass

    def update_priority(
        self,
        condition_id: str,
        new_priority: int
    ) -> None:
        """동적 우선순위 갱신 (거래 임박 시 1로 변경)"""
        pass
```

### 알고리즘

```
1. 초기화: 100개 조건을 priority 기준으로 heap에 삽입
2. 매 50ms마다 (초당 20건):
   - heap에서 우선순위 높은 조건 pop
   - API 호출 실행
   - 다음 실행 시각 계산 후 heap에 다시 삽입
3. 동적 우선순위 조정:
   - 거래 임박 감지 시 priority를 1로 변경
   - 거래 완료 시 priority를 5로 복원
```

### 아키텍처 다이어그램

```
┌─────────────────┐
│ 100 Conditions  │
│ (with priority) │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Priority Heap  │  ← 가중치 기반 정렬
└────────┬────────┘
         │
         ↓ (매 50ms)
┌─────────────────┐
│ get_next_task() │  ← 우선순위 높은 것 선택
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  API Call (20/s)│  ← Rate Limit 내에서 실행
└─────────────────┘
```

## 4. 고려된 대안 (Alternatives Considered)

### 대안 1: 단순 Round Robin 폴링
- **설명**: 100개 조건을 순차 폴링
- **기각 사유**: 5초 지연으로 '정확성 A' NFR (Stage 1) 위반

### 대안 2: 외부 솔루션 구매 (Quartz Scheduler 등)
- **설명**: 상용 스케줄러 도입
- **기각 사유**:
  - 비용 문제 (Stage 2 제약: 예산 부족)
  - API Rate Limit 환경에 맞는 솔루션 부재

## 5. 영향 및 파급 효과 (Consequences)

- **긍정적**:
  - Rate Limit 내에서 효율적 감시
  - 중요 조건: 1초 미만 감지 → '정확성 A' NFR 충족
  - 비중요 조건: 10초 주기 → 리소스 절약
- **부정적**:
  - 시스템 복잡도 증가 (자체 개발 스케줄러)
  - 테스트 난이도 상승 (우선순위 로직 검증 필요)
  - 유지보수 부담 (팀 내 전문성 필요)
```

### 2.6 Category 5: DNA System ADR

**목적**: 전사적 표준 시스템 (11개) 결정

**특징**:
- "자동 결정" (Pre-defined)
- DNA Systems 11개 중 하나
- Stage 6 Standards로 직접 연결

**템플릿 구조**:
```markdown
# ADR-001: [DNA System 제목]

## 1. 배경 및 문제 (Context)
- DNA System의 필요성

## 2. 요구사항 (Requirements)
- R-01, R-02, R-03

## 3. 대안 비교 (Alternatives Comparison)
- 옵션 1, 2

## 4. 결정 (Decision)
- 선택한 기술

## 5. 영향 및 파급 효과 (Consequences)
- 시스템 영향

## 6. 실행 및 강제화 (Enforcement)
- 연결된 표준: 06D-01
- 자동화: Pre-commit, ArchUnit
```

**실제 예시**:

```markdown
# ADR-001: 구조화된 로깅을 위한 Structlog 채택

상태: Accepted
날짜: 2025-01-10
카테고리: 5. DNA 시스템 (DNA System)

## 1. 배경 및 문제 (Context)

서비스가 분산됨에 따라 print()나 기본 logging 모듈로는
로그 추적(Traceability)이 불가능함.

**현재 문제**:
- 각 서비스마다 다른 로그 포맷 (Plain text, JSON 혼재)
- Request ID, User ID 등 Context 누락
- ELK 스택에서 로그 집계/분석 불가

## 2. 요구사항 (Requirements)

- R-01: 모든 로그는 JSON 형식이어야 함
- R-02: Request ID, User ID 등 Context 자동 주입 가능
- R-03: Python 표준 logging과 호환되어야 함
- R-04: 성능 영향 최소 (로깅으로 인한 지연 < 1ms)

## 3. 대안 비교 (Alternatives Comparison)

### 옵션 1: Structlog
- **장점**:
  - R-01, R-02, R-03, R-04 모두 충족
  - 유연한 설정 (Processor chain)
  - Context binding 지원
- **단점**:
  - 표준 라이브러리 아님 (외부 의존성)

### 옵션 2: 표준 logging + JSONFormatter
- **장점**:
  - 표준 라이브러리 (외부 의존성 없음)
- **단점**:
  - R-02 (Context 주입)가 매우 복잡함
  - Thread-local 직접 구현 필요

## 4. 결정 (Decision)

**모든 Python 기반 DNA 시스템의 로깅 표준으로 Structlog 라이브러리를 채택한다.**

**근거**:
- 모든 요구사항 (R-01~R-04) 충족
- Context binding으로 AI 협업 시 추적성 확보
- ELK 스택과 완벽 호환

## 5. 영향 및 파급 효과 (Consequences)

- **긍정적**:
  - 모든 로그가 일관된 JSON 형식
  - ELK에서 분석/알림 자동화 가능
  - Request/User 추적으로 디버깅 효율 10배 향상
- **부정적**:
  - 개발자들이 Structlog 사용법 학습 필요 (2일 소요)
  - 기존 코드 마이그레이션 (print → logger) 필요

## 6. 실행 및 강제화 (Enforcement)

### 연결된 표준
- **06D-01\_Project\_Standards.md**
  - Part 1, Mandatory-01: Logging 표준

### 자동화

**Pre-commit Hook** (`.pre-commit-config.yaml`):
```yaml
- repo: local
  hooks:
    - id: disallow-print
      name: "Disallow print()"
      entry: "print\\("
      language: pygrep
      types: [python]

    - id: disallow-stdlib-logging
      name: "Disallow 'import logging'"
      entry: "^import logging"
      language: pygrep
      types: [python]
```

**Architecture Test** (`tests/architecture/test_logging.py`):
```python
import pytest
from pathlib import Path

def test_no_print_in_src():
    """src/ 폴더에 print() 사용 금지"""
    src_files = Path("src").rglob("*.py")
    for file in src_files:
        content = file.read_text()
        assert "print(" not in content, f"{file} contains print()"

def test_no_stdlib_logging_import():
    """src/ 폴더에 import logging 금지"""
    src_files = Path("src").rglob("*.py")
    for file in src_files:
        content = file.read_text()
        assert "import logging" not in content, f"{file} imports logging"
```

**표준 사용 예시** (`src/core/logging/logger.py`):
```python
import structlog

def get_logger(name: str):
    """프로젝트 표준 logger 반환"""
    return structlog.get_logger(name)

# 사용
logger = get_logger(__name__)
logger.info("user_login", user_id=123, request_id="req-001")
# 출력: {"event": "user_login", "user_id": 123, "request_id": "req-001", ...}
```
```

---

## Part 3: ADR 작성 프로세스 (4 Steps)

### 3.1 전체 프로세스 개요

```
Step 1: Category 선택
   ↓
Step 2: Template 작성
   ↓
Step 3: Alternatives 비교
   ↓
Step 4: Enforcement 정의
   ↓
ADR 완성 → Stage 6 (Standards)로 연결
```

### 3.2 Step 1: Category 선택

**질문 트리**:

```
Q1: 이 결정이 외부에서 강제되었는가?
  YES → Category 1 (External Constraint)
  NO  → Q2

Q2: 이 결정이 NFR 간 충돌 해결인가?
  YES → Category 2 (Conflict Resolution)
  NO  → Q3

Q3: 이 결정이 기술/프레임워크 선택인가?
  YES → Category 3 (Technology Stack)
  NO  → Q4

Q4: 이 결정이 도메인 특화 설계인가?
  YES → Category 4 (Domain Technology)
  NO  → Q5

Q5: 이 결정이 DNA System 11개 중 하나인가?
  YES → Category 5 (DNA System)
  NO  → 재검토 (잘못된 ADR일 수 있음)
```

**카테고리별 개수 가이드**:

| Category | 목표 개수 | 허용 범위 |
|----------|----------|----------|
| 1. External Constraint | 4개 | 3-5개 |
| 2. Conflict Resolution | 2개 | 2-3개 |
| 3. Technology Stack | 5개 | 4-6개 |
| 4. Domain Technology | 3개 | 2-4개 |
| 5. DNA System | 11개 | 11개 (고정) |
| **Total** | **25개** | **22-29개** |

### 3.3 Step 2: Template 작성

**작성 순서** (카테고리 공통):

1. **Header 작성**
   ```markdown
   # ADR-XXX: [제목]

   상태: Proposed | Accepted | Deprecated | Superseded
   날짜: YYYY-MM-DD
   카테고리: [1-5 중 선택]
   ```

2. **필수 섹션 작성** (카테고리마다 다름)
   - Part 2.2~2.6의 템플릿 참조

3. **Markdown 규칙**
   - 헤더: `##` (2레벨부터)
   - 코드 블록: 언어 명시 (```python, ```yaml)
   - 표: GitHub Flavored Markdown
   - 이모지: ✅ ❌ 🔺 ⭐ ↓ 등 사용 OK

### 3.4 Step 3: Alternatives 비교

**비교 기준 선정**:

```
1. 요구사항 (Requirements) 도출
   - NFR에서 추출 (Stage 1)
   - 기술적 제약에서 추출 (Stage 2)

2. 비교 기준 정의
   - 정량적: 성능, 비용, 러닝 커브
   - 정성적: 커뮤니티, 유지보수성

3. 대안 평가
   - ✅ (충족), 🔺 (부분 충족), ❌ (미충족)
   - ⭐ (매우 높음), ↓ (낮음)
```

**비교표 작성 예시**:

```markdown
## 3. 대안 비교 (Alternatives Comparison)

| 기준 | 옵션 1 | 옵션 2 | 옵션 3 |
|------|--------|--------|--------|
| R-01: 비동기 지원 | ✅ Native | 🔺 플러그인 | ❌ 미지원 |
| R-02: 성능 | ⭐ 10K RPS | ↓ 2K RPS | ↓ 3K RPS |
| R-03: 문서화 | ✅ 자동 | ↓ 수동 | ↓ 수동 |
| 러닝 커브 | Medium | High | Low |
| 커뮤니티 | 중간 | 매우 큼 | 매우 큼 |
| 총점 | **9/10** | 5/10 | 6/10 |
```

### 3.5 Step 4: Enforcement 정의

**3단계 Enforcement**:

```
Phase 1: Static Analysis (개발 중)
  - Pre-commit hooks
  - Linters (ruff, mypy, eslint)
  - 즉시 피드백 (< 1초)

Phase 2: Architecture Tests (CI/CD)
  - ArchUnit (Java)
  - import-linter (Python)
  - PR 머지 전 검증

Phase 3: Runtime Validation (배포 전)
  - Fitness Functions
  - Integration tests
  - 배포 게이트
```

**Enforcement 섹션 작성 예시**:

```markdown
## 6. 강제화 방안 (Enforcement)

### Static Analysis (Pre-commit)
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: check-fastapi-usage
      name: "Ensure FastAPI import"
      entry: "from fastapi import"
      language: pygrep
      types: [python]
      files: ^src/api/
```

### Architecture Tests (CI/CD)
```python
# tests/architecture/test_api_framework.py
def test_api_routes_use_fastapi():
    """All API routes must use FastAPI"""
    api_files = Path("src/api").rglob("*.py")
    for file in api_files:
        content = file.read_text()
        if "@app.route" in content:  # Flask
            pytest.fail(f"{file} uses Flask, not FastAPI")
```

### Runtime Validation (Optional)
```python
# tests/fitness/test_api_performance.py
def test_api_response_time():
    """ADR-301: FastAPI must handle 10K RPS"""
    response = client.get("/api/health")
    assert response.elapsed.total_seconds() < 0.1
```
```

---

## Part 4: 실전 예시

### 4.1 Stock Trading Platform ADR 예시

**프로젝트**: 주식 자동 거래 시스템
**Stage 1 결과**: B-C-A 패밀리 (실시간 트랜잭션)
**Stage 2 결과**: 한국투자증권 API (초당 20건 제약)

**ADR 목록** (총 18개):

#### Category 1: External Constraint (3개)
- ADR-101: 한국투자증권 API 사용 강제
- ADR-102: 금융실명제 준수 (본인 계좌만 거래)
- ADR-103: 실시간 시세 API 제약 (초당 20건)

#### Category 2: Conflict Resolution (3개)
- ADR-201: 정확성 vs 비용 (WebSocket 포기, REST 폴링)
- ADR-202: 정확성 vs 성능 (하이브리드 아키텍처)
- ADR-203: 보안 vs 사용성 (토큰 자동 갱신)

#### Category 3: Technology Stack (5개)
- ADR-301: Python 3.11+ 선택
- ADR-302: FastAPI 채택
- ADR-303: SQLite → PostgreSQL 마이그레이션
- ADR-304: Pydantic v2 사용
- ADR-305: pytest 테스트 프레임워크

#### Category 4: Domain Technology (3개)
- ADR-401: 우선순위 큐 스케줄러 설계
- ADR-402: 조건 평가 엔진 아키텍처
- ADR-403: 거래 실행 재시도 전략

#### Category 5: DNA System (4개, 11개 중 일부만 사용)
- ADR-001: Structlog 로깅
- ADR-002: 표준 에러 핸들링
- ADR-003: Pydantic Settings 설정 관리
- ADR-004: pytest 테스트 표준

### 4.2 ADR 예시: ADR-201 (Conflict Resolution)

**전체 문서**: `docs/session-summaries/20251112_Phase2_복합시스템_도전.md` 참조

**요약**:
```markdown
# ADR-201: 정확성 vs 비용 - REST 폴링 방식 채택

## 충돌
- 정확성 A: 실시간 시세 필요
- 비용 B: WebSocket 비용 높음 (월 50만원)

## 결정
- REST 폴링 (5초 주기) 채택
- WebSocket 포기

## 근거
- 5초 지연 수용 가능 (Day Trading)
- 비용 절감 (월 0원)

## 영향
- 긍정: 비용 절감
- 부정: 5초 지연 (수용 가능)
```

---

## Part 5: 엔터프라이즈 사례

### 5.1 Kubernetes KEP (Kubernetes Enhancement Proposal)

**문서 형태**: KEP = Motivation + Proposal + Alternatives

**예: KEP-17 Resource Versioning**

```markdown
# KEP-17: Resource Versioning

## Motivation (왜 필요?)
- API 버전 관리 문제
- 하위 호환성 보장 필요

## Proposal (어떻게 구현?)
- v1alpha1, v1beta1, v1 단계 도입
- Conversion webhook 사용

## Alternatives (왜 이 방법?)
- 대안 1: 버저닝 없이 하나의 API
  - 기각: 하위 호환성 깨짐
- 대안 2: 별도 API 엔드포인트
  - 기각: 복잡도 증가
```

**DNA v4.0와 비교**:

| 요소 | KEP | DNA ADR |
|------|-----|---------|
| Motivation | ≈ Stage 1-2 | Context 섹션 |
| Proposal | ≈ Stage 7 | Decision 섹션 |
| Alternatives | ≈ Stage 2-3 | Alternatives 섹션 |
| Enforcement | ❌ 없음 | ✅ 필수 (Stage 6-9) |

**핵심 차이**: KEP는 "결정"만, DNA는 "결정 + 강제화"

### 5.2 GitLab Architecture Blueprints

**워크플로**: ADR → Issue → MR → Code Review → Merge

**예: Use lock_column for CI/CD Optimistic Locking**

```markdown
# ADR: Use lock_column for Optimistic Locking

## Context
- CI/CD 파이프라인 동시 실행 시 충돌

## Decision
- Rails의 lock_column 사용

## Consequences
- 동시성 문제 해결
- DB 컬럼 추가 필요
```

**특징**:
- ADR이 매우 구체적 (구현 방법까지 포함)
- 중간 문서 없음 (ADR → 직접 구현)
- Code Review로 일관성 강제

**DNA v4.0와 차이**:
- GitLab ADR ≈ DNA ADR + Standards 합침
- GitLab = 인간 Review, DNA = 자동화

### 5.3 Terraform Design Documents

**구분**: ADR vs Design Doc

- **ADR**: Decision 중심 (왜 이 기술?)
- **Design Doc**: Design 중심 (어떻게 구현?)

**예: Provider Plugin System Design Doc**

```markdown
# Design Doc: Provider Plugin System

## Abstract
- Terraform의 플러그인 아키텍처 설계

## Background
- 다양한 클라우드 지원 필요
- 핵심과 플러그인 분리

## Proposal
- Go Plugin 시스템 사용
- gRPC 통신

## Alternatives
- 대안 1: 모놀리식
- 대안 2: REST API
```

**DNA v4.0 매핑**:
- Terraform ADR ≈ DNA ADR (Stage 3)
- Terraform Design Doc ≈ DNA Blueprint (Stage 7)

---

## Appendix: 템플릿 Quick Reference

### A.1 템플릿 파일 위치

```
docs/
  adr/
    ADR-1XX_*.md         # Category 1: External Constraint
    ADR-2XX_*.md         # Category 2: Conflict Resolution
    ADR-3XX_*.md         # Category 3: Technology Stack
    ADR-4XX_*.md         # Category 4: Domain Technology
    dna-systems/
      ADR-001_*.md       # Category 5: DNA System (001-011)
      ADR-002_*.md
      ...
      ADR-011_*.md
```

### A.2 ADR 번호 체계

| Category | 번호 범위 | 예시 |
|----------|----------|------|
| 1. External Constraint | 101-199 | ADR-101, ADR-102, ... |
| 2. Conflict Resolution | 201-299 | ADR-201, ADR-202, ... |
| 3. Technology Stack | 301-399 | ADR-301, ADR-302, ... |
| 4. Domain Technology | 401-499 | ADR-401, ADR-402, ... |
| 5. DNA System | 001-011 | ADR-001, ADR-002, ..., ADR-011 |

### A.3 상태 (Status) 정의

| 상태 | 의미 | 사용 시점 |
|------|------|----------|
| Proposed | 제안됨 | 초안 작성, 리뷰 중 |
| Accepted | 승인됨 | 최종 결정, 구현 시작 |
| Deprecated | 폐기됨 | 더 이상 사용 안 함 |
| Superseded | 대체됨 | 새 ADR로 대체 (링크 필수) |

### A.4 체크리스트

**ADR 작성 완료 체크리스트**:

- [ ] Category 선택 (1-5 중 하나)
- [ ] ADR 번호 부여 (범위 확인)
- [ ] Header 작성 (상태, 날짜, 카테고리)
- [ ] 필수 섹션 작성 (카테고리별 템플릿)
- [ ] Alternatives 비교 (정량적 근거)
- [ ] Enforcement 정의 (Static/Arch/Runtime)
- [ ] 코드 예시 포함 (가능한 경우)
- [ ] 팀 리뷰 완료
- [ ] 상태를 'Accepted'로 변경
- [ ] Stage 6 (06D-01 Standards) 연결 (DNA System ADR만)

**ADR → Standards 변환 체크리스트** (DNA System ADR만):

- [ ] ADR에서 기술 결정 추출
- [ ] DO/DON'T 규칙 정의
- [ ] Pre-commit hook 작성
- [ ] Architecture test 작성
- [ ] 06D-01에 표준 추가
- [ ] 팀 교육 완료

---

## 🎯 다음 단계

**ADR 작성 완료 후**:

1. **Stage 6: Project Standards 작성**
   - 가이드: `06G-00_standards_guide.md` (작성 예정)
   - DNA System ADR (001-011)을 06D-01로 변환

2. **Stage 9: Governance 구현**
   - 가이드: `09G-00_governance_guide.md` (작성 예정)
   - Pre-commit hooks, ArchUnit tests, Fitness Functions

3. **Stage 7: Blueprint 작성**
   - ADR + Standards를 기반으로 구체적 설계

---

**작성일**: 2025-11-17
**작성자**: 2호 (with Jason)
**관련 문서**:
- `docs/CORE_METHODOLOGY.md` - DNA v4.0 전체 개요
- `docs/research/20251117_Gemini_미싱링크_분석결과.md` - ADR 분석 결과
- `docs/session-summaries/20251112_Phase2_복합시스템_도전.md` - Stock Trading 사례
