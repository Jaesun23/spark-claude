# DNA Stage별 실행 가이드

## 개요

이 가이드는 각 Stage에서 **무엇을 달성해야 하는지**, **어떤 기술을 적용해야 하는지**, **어떤 문서를 참고해야 하는지**를 명확히 정의합니다. Gemini 연구의 4-Phase 프로세스를 기반으로 합니다.

### 작업 위치
**모든 작업은 프로젝트 내에서 진행합니다.**
- 작업 경로: `/Users/jason/Projects/spark-claude/skills/dna-methodology/`
- 완료 후 배포: `~/.claude/skills/`

---

## Gemini 4-Phase와 DNA 9-Stage 매핑

| Gemini Phase | DNA Stage | 핵심 목표 |
|--------------|-----------|-----------|
| **Phase 1: 아이디어 정제** | Stage 1-2 | 추상 → 구체, 제약 파악 |
| **Phase 2: 스켈레톤 수립** | Stage 3-6 | 환경 구축, 표준화 |
| **Phase 3: 병렬 확장** | Stage 7-8 | 청사진 작성, 작업 분해 |
| **Phase 4: 정합성 검증** | Stage 9 | 무결성 검증, 체크리스트 |

---

## Stage 1: Core Definition (핵심 정의)

### 목표
추상적 아이디어를 **고밀도 요구사항**으로 변환하고 **아키텍처 패밀리** 결정

### 적용 기술

#### 1. Chain of Density (CoD)
**목적**: 정보 밀도를 단계적으로 증가

**프로세스**:
1. 사용자 아이디어를 1-2문장으로 요약
2. 누락된 핵심 Entity 식별
3. Entity 통합 + 불필요한 수사 제거
4. 3-5회 반복
5. 최종 고밀도 SRS 완성

**예시**:
```
Round 1: "결제 시스템을 만들고 싶어"
Round 2: "카드/계좌이체 지원하는 결제 시스템"
Round 3: "PG사 연동 카드/계좌이체, 월 100만 건 처리,
         p99 응답시간 500ms, PCI-DSS 준수"
```

#### 2. 재귀적 질문 생성
**목적**: 정보 부족 영역 자동 탐지 및 구체화

**프로세스**:
1. 정보 부족 영역 식별
2. 구체화 질문 생성:
   - "핵심 기능은 무엇인가요?"
   - "대상 사용자는 누구인가요?"
   - "플랫폼/환경은?"
3. 답변 수집
4. 불충분하면 추가 질문 재귀

### 작업 내용

#### A. Layer 1-2 분석
**Layer 1 질문** (데이터 일관성):
- 금전/생명/법적 책임이 관련되는가?
- 데이터 손실이 치명적인가?
- → A (Strong) or B (Eventual)

**Layer 2 질문** (처리 패턴):
- 즉각 응답이 필수인가?
- 배치 처리가 가능한가?
- → A (Real-time), B (Batch), C (Hybrid)

#### B. NFR 프로파일 결정
- Performance: p99 응답시간, TPS
- Availability: 목표 uptime
- Consistency: 허용 불일치 범위
- 우선순위 결정: 1순위, 2순위, 3순위

#### C. 패밀리 분류
7개 패밀리 중 매칭:
1. 초고속 거래 (A-A-A)
2. 트랜잭션/CRUD (A-A-B)
3. 협업/동기화 (B-A-A)
4. 검색/추천 (B-B-B)
5. 실시간 스트리밍 (B-C-A)
6. 분석/배치 (B-A-C)
7. 안전-임계 IoT (A-B-A)

### 참고 문서

**Skills References**:
- `references/core/families.md` - 7개 패밀리 정의
- `references/core/nfr-definitions.md` - NFR 속성 정의

**DNA Methodology v4.0 Guide**:
- `01G-00_core_definition_guide.md` - 전체 가이드
- `01M-01_layer1_manual.md` - Layer 1 상세
- `01M-02_layer2_manual.md` - Layer 2 상세

### 산출물

| 파일 | 내용 |
|------|------|
| `01F-01_core_functions.md` | 핵심 기능 목록 |
| `01C-01_family_classification.md` | 패밀리 분류 결과 |
| `stage1_output.json` | 구조화된 산출물 |

### 완료 기준

- [ ] CoD로 고밀도 SRS 생성 (Entity 5개 이상)
- [ ] Layer 1-2 결정에 명확한 근거 있음
- [ ] NFR 우선순위 3개 결정됨
- [ ] 7개 패밀리 중 하나로 분류됨
- [ ] 핵심 기능이 구현방식과 분리됨

---

## Stage 2: Structure Design (구조 설계)

### 목표
**Layer 3 환경 제약**을 조사하고 **충돌 패턴**을 식별하여 해결

### 적용 기술

#### Tree of Thoughts (ToT)
**목적**: 아키텍처 대안 탐색 및 최적안 선택

**프로세스**:
1. 문제를 중간 단계로 분해
2. 각 단계에서 3+ 후보 생성
3. 각 후보 자체 평가 (확장성, 비용, 복잡도)
4. BFS/DFS로 최적 경로 탐색
5. 막다른 길에서 백트래킹

**예시**:
```
결정: 메시지 큐 선택
├─ Kafka: 처리량 ★★★, 지연 ★★☆, 운영 ★★★
├─ RabbitMQ: 처리량 ★★☆, 지연 ★★★, 운영 ★★☆
└─ Redis Pub/Sub: 처리량 ★★☆, 지연 ★★★, 운영 ★☆☆
    → 요구사항: 처리량 > 지연 → Kafka 선택
```

### 작업 내용

#### A. Layer 3 환경 제약 조사
5가지 제약 영역:
1. **기술 제약**: 기존 스택, 라이선스
2. **팀 제약**: 기술 역량, 인원수
3. **인프라 제약**: 클라우드/온프렘, 예산
4. **외부 제약**: API, 규제, 보안
5. **시간 제약**: 데드라인, 마일스톤

#### B. 충돌 패턴 식별
**일반적 충돌**:
- Performance vs Consistency
- 팀 역량 vs 기술 선택
- 예산 vs 확장성

**식별 방법**:
1. Layer 1-2 결정과 Layer 3 제약 교차
2. 상충되는 요구사항 식별
3. 우선순위에 따른 트레이드오프

#### C. 5단계 구현방법 결정
1. **기능** 정의 (Stage 1에서)
2. **속성** 수치화 (NFR 구체적 값)
3. **제약** 반영 (Layer 3)
4. **기술** 선택 (ToT로 평가)
5. **설계** 결정 (ADR로 문서화)

### 참고 문서

**Skills References**:
- `references/core/families.md` - 패밀리별 기술 스택 힌트
- `references/stage2/layer3-questions.md` - Layer 3 질문

**DNA Methodology v4.0 Guide**:
- `02G-00_environment_constraints_guide.md` - 전체 가이드
- `02M-01_environment_constraints_manual.md` - 상세 해설
- `02E-01_stock_trading_case.md` - 주식 거래 사례

### 산출물

| 파일 | 내용 |
|------|------|
| `02C-01_layer3_constraints.md` | 5가지 제약 목록 |
| `02C-02_conflicts_analysis.md` | 충돌 패턴 분석 |
| `02D-01_tech_candidates.md` | 기술 후보 및 평가 |
| `stage2_output.json` | 구조화된 산출물 |

### 완료 기준

- [ ] 5가지 제약 영역 모두 조사됨
- [ ] 3개 이상 충돌 패턴 식별됨
- [ ] 각 충돌에 해결 방안 제시됨
- [ ] ToT로 기술 대안 평가됨
- [ ] 5단계 구현방법 결정됨

---

## Stage 3: Architecture Decision Records (ADR)

### 목표
모든 아키텍처 결정을 **ADR로 문서화**하고 추적 가능하게 만들기

### 적용 기술

#### SOP 기반 템플릿
**목적**: 일관된 형식으로 결정 기록

**ADR 템플릿**:
```markdown
# ADR-NNN: [결정 제목]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
왜 이 결정이 필요한가?

## Decision
무엇을 결정했는가?

## Consequences
### Positive
- 장점 1
- 장점 2

### Negative
- 단점 1

### Risks
- 리스크 1

## Alternatives Considered
1. 대안 A: 이유로 기각
2. 대안 B: 이유로 기각

## References
- [관련 문서]
```

### 작업 내용

#### A. ADR 분류 (5 Categories)
1. **Bootstrap ADR** (001-099): DB, Cache, Messaging 등 인프라
2. **Domain ADR** (100-199): 비즈니스 로직 결정
3. **Integration ADR** (200-299): 외부 시스템 연동
4. **Security ADR** (300-399): 보안 관련 결정
5. **Operational ADR** (400-499): 운영/모니터링

#### B. Stage 2 → ADR 매핑
- 기술 제약 → Bootstrap ADR
- 외부 제약 → Integration ADR
- 보안 요구 → Security ADR
- 충돌 해결 → 해당 카테고리 ADR

#### C. ADR 작성 원칙
- **제약에 의한 결정도 ADR**: 선택지가 1개여도 기록
- **대안 명시**: 왜 다른 것을 선택하지 않았는지
- **결과 예측**: 긍정/부정/리스크

### 참고 문서

**Skills References**:
- `references/stage3/adr-template.md` - ADR 템플릿
- `references/stage3/adr-categories.md` - 5가지 카테고리

**DNA Methodology v4.0 Guide**:
- `03G-00_adr_guide.md` - 전체 가이드
- `03M-01_adr_types_manual.md` - ADR 유형
- `03M-02_adr_to_standards_manual.md` - ADR → Standards 변환
- `03E-02_kent_beck_bplustree_case.md` - 실제 사례

### 산출물

| 파일 | 내용 |
|------|------|
| `03A-001_database.md` | DB 선택 ADR |
| `03A-002_cache.md` | 캐시 전략 ADR |
| `03A-101_domain_*.md` | 도메인 ADR들 |
| `stage3_output.json` | 구조화된 산출물 |

### 완료 기준

- [ ] Bootstrap ADR 최소 5개 작성
- [ ] 모든 Stage 2 결정이 ADR로 문서화됨
- [ ] 각 ADR에 대안과 결과가 명시됨
- [ ] ADR 간 참조가 연결됨

---

## Stage 4-6: DNA System Planning & Implementation

### 목표
**11개 DNA 시스템**을 계획하고 구현하여 **환경 강제** 기반 마련

### Stage 4: DNA System Planning

11개 DNA 시스템 스펙 정의:
1. Logging (structlog)
2. Config Management
3. Error Handling
4. Type System (Pydantic)
5. Database Access
6. Caching
7. Messaging
8. Authentication
9. Monitoring
10. Testing Infrastructure
11. Documentation

### Stage 5: DNA System Implementation

각 시스템의:
- 인터페이스 정의
- 기본 구현
- 테스트 코드
- 사용 예시

### Stage 6: Project Standards

#### ADR → DO/DON'T 변환
```
ADR-001: structlog 사용
    ↓
DO: from common.logging import logger
DON'T: import logging / print()
```

#### 자동화 설정
- Pre-commit hooks
- CI/CD 파이프라인
- Import-linter 규칙

### 참고 문서

**DNA Methodology v4.0 Guide**:
- `04G-00_dna_planning_guide.md`
- `05G-00_dna_implementation_guide.md`
- `06G-00_project_standards_guide.md`
- `DNA_Systems_11_Complete_Guide.md`

### 산출물

| Stage | 파일 | 내용 |
|-------|------|------|
| 4 | `04S-01_dna_system_spec.md` | 11개 시스템 스펙 |
| 5 | `src/core/*/` | 구현된 DNA 시스템 |
| 6 | `PROJECT_STANDARDS.md` | DO/DON'T 규칙 |
| 6 | `.pre-commit-config.yaml` | 자동화 설정 |

### 완료 기준

- [ ] 11개 DNA 시스템 스펙 완성
- [ ] 핵심 시스템 (Logging, Config, Error) 구현
- [ ] PROJECT_STANDARDS.md 완성
- [ ] Pre-commit hooks 설정됨
- [ ] CI/CD 파이프라인 구성됨

---

## Stage 7: Blueprint (청사진)

### 목표
환경(Stage 1-6)이 완성된 후 **전체 설계도**를 작성

### 적용 기술

#### 1. Skeleton-of-Thought (SoT)
**목적**: 구조 먼저 확정, 세부사항 나중

**프로세스**:
1. 청사진 목차(스켈레톤) 생성
2. 각 섹션의 핵심 포인트만 정의
3. 구조 확정 후 상세 확장
4. 독립 섹션은 병렬 처리

**청사진 스켈레톤**:
```
1. Executive Summary
2. System Overview
3. Domain Model
4. API Design
5. Data Architecture
6. Infrastructure
7. Security
8. Monitoring
```

#### 2. Context Re-ranking
**목적**: 컨텍스트 부패 방지

**프로세스**:
각 섹션 작성 시:
1. 전체 문서 입력 X
2. 해당 섹션 관련 정보만 검색
3. 검색 결과를 프롬프트 상단 배치

**예시**:
```
Section "API Design" 작성 시:
- stage1: 핵심 기능 목록
- stage3: API 관련 ADR만
- stage6: API 관련 Standards만
→ 이것들만 로드
```

#### 3. 병렬 확장
**독립 섹션** (병렬 가능):
- Domain Model
- Infrastructure

**의존 섹션** (순차 필요):
- API Design → Security (인증 의존)
- Executive Summary (마지막)

### 작업 내용

#### A. C4 Model 생성
- Level 1: Context Diagram
- Level 2: Container Diagram
- 텍스트(Mermaid) 형태로 포함

#### B. 청사진 섹션별 내용

**Executive Summary**:
- 프로젝트 개요
- 핵심 결정사항
- 기술 스택 요약

**Domain Model**:
- 엔티티 정의
- 관계 다이어그램
- 비즈니스 규칙

**API Design**:
- 엔드포인트 목록
- Request/Response 스키마
- 인증/인가

**Data Architecture**:
- DB 스키마
- 캐싱 전략
- 데이터 흐름

### 참고 문서

**Skills References**:
- `references/core/gemini-techniques.md` - SoT, Re-ranking
- `references/stage7/blueprint-guide.md`

**DNA Methodology v4.0 Guide**:
- `07G-00_blueprint_guide.md`

**이전 Stage 산출물**:
- `stage1_output.json` - 패밀리, NFR
- `stage2_output.json` - 제약, 기술
- `stage3_output.json` - ADR 목록
- `PROJECT_STANDARDS.md`

### 산출물

| 파일 | 내용 |
|------|------|
| `07B-01_blueprint.md` | 완전한 청사진 |
| `stage7_output.json` | 구조화된 산출물 |

### 완료 기준

- [ ] SoT로 스켈레톤 먼저 생성됨
- [ ] 모든 섹션이 Re-ranking으로 작성됨
- [ ] C4 Level 1-2 다이어그램 포함
- [ ] ADR/Standards와 정합성 확인
- [ ] 독립 구현 가능한 수준의 상세도

---

## Stage 8: Task Breakdown (작업 분해)

### 목표
청사진을 **독립 실행 가능한 레고블럭**으로 분해

### 작업 내용

#### A. 원자 단위 분해
각 작업이:
- 2-4시간 내 완료 가능
- 독립적으로 실행 가능
- TODO, pass 없이 완전
- 검증 가능한 산출물

#### B. 의존성 그래프
```
Task 1 (DB 스키마)
    ↓
Task 2 (Repository 구현) ← Task 3 (API 인터페이스)
    ↓                         ↓
Task 4 (Service 레이어) ───────┘
    ↓
Task 5 (Integration Test)
```

#### C. 작업 메타데이터
각 작업에:
- 예상 시간
- 필요 컨텍스트
- 의존 작업
- 산출물

### 참고 문서

**DNA Methodology v4.0 Guide**:
- `08G-00_task_breakdown_guide.md`

### 산출물

| 파일 | 내용 |
|------|------|
| `08T-01_tasks.md` | 작업 목록 |
| `08T-02_dependency_graph.md` | 의존성 그래프 |
| `stage8_output.json` | 구조화된 산출물 |

### 완료 기준

- [ ] 모든 작업이 2-4시간 단위
- [ ] 의존성 그래프 완성
- [ ] 순환 의존 없음
- [ ] 각 작업에 명확한 산출물

---

## Stage 9: Checklist (체크리스트)

### 목표
각 작업별로 **독립 실행 가능한 9-Step 체크리스트** 작성

### 적용 기술

#### Knowledge Graph 기반 검증
**목적**: 문서 간 모순 자동 탐지

**프로세스**:
1. 모든 산출물에서 Entity 추출
   - 테이블명, API 경로, 변수명, 타입
2. Entity 간 관계 그래프 구축
3. 규칙 기반 모순 탐지:
   - 미정의 참조
   - 순환 의존
   - 타입 불일치
   - 네이밍 충돌

**예시**:
```
[탐지됨]
- API /users/{id}가 User.id 참조
- 그러나 User 엔티티에 id 필드 없음
→ 권장: User 엔티티에 id 필드 추가
```

### 작업 내용

#### A. 9-Step 체크리스트 템플릿

```markdown
# Task: [작업명]

## Step 1: Context Loading
- [ ] 필요한 파일 로드
- [ ] 이전 산출물 확인

## Step 2: Prerequisites Check
- [ ] 의존 작업 완료 확인
- [ ] 필요 모듈 존재 확인

## Step 3: Interface Definition
- [ ] 입출력 정의
- [ ] 타입 명시

## Step 4: Implementation
- [ ] 핵심 로직 구현
- [ ] DNA 시스템 활용

## Step 5: Error Handling
- [ ] 예외 처리
- [ ] 에러 메시지

## Step 6: Testing
- [ ] 단위 테스트
- [ ] 엣지 케이스

## Step 7: Documentation
- [ ] 주석/Docstring
- [ ] 사용 예시

## Step 8: Integration
- [ ] 다른 모듈과 연결
- [ ] 통합 테스트

## Step 9: Quality Verification
- [ ] Ruff 통과
- [ ] MyPy 통과
- [ ] 커버리지 95%+
```

#### B. 작업별 컨텍스트 명시
각 체크리스트에:
- 필요한 파일 목록
- 참조할 ADR
- 준수할 Standards
- 사용할 DNA 시스템

### 참고 문서

**Skills References**:
- `references/core/gemini-techniques.md` - Knowledge Graph
- `references/stage9/checklist-guide.md`

**DNA Methodology v4.0 Guide**:
- `09G-00_checklist_guide.md`

### 산출물

| 파일 | 내용 |
|------|------|
| `09L-001_task1_checklist.md` | Task 1 체크리스트 |
| `09L-002_task2_checklist.md` | Task 2 체크리스트 |
| `...` | 모든 Task의 체크리스트 |
| `stage9_output.json` | 구조화된 산출물 |

### 완료 기준

- [ ] 모든 Task에 9-Step 체크리스트 있음
- [ ] 각 체크리스트가 독립 실행 가능
- [ ] Knowledge Graph로 모순 검증 완료
- [ ] 모든 체크리스트 완료 = 프로젝트 완성

---

## 전체 검증: /audit

### 목표
전체 DNA 프로젝트의 **무결성 검증**

### 검증 항목

1. **Stage 완료 검증**
   - 모든 Stage 산출물 존재
   - JSON 스키마 유효성

2. **Stage 간 정합성**
   - Stage 1 패밀리 → Stage 2 기술 선택 일치
   - Stage 2 결정 → Stage 3 ADR 존재
   - Stage 3 ADR → Stage 6 Standards 반영

3. **청사진 무결성**
   - ADR과 청사진 내용 일치
   - Standards와 청사진 충돌 없음

4. **Knowledge Graph 검증**
   - 전체 Entity 그래프
   - 모순 탐지
   - 수정 제안

### 산출물

- `audit_report.md`: 전체 감사 리포트
- 문제점 목록
- 수정 제안

---

## 요약: 핵심 기술 적용 위치

| 기술 | Stage | 목적 |
|------|-------|------|
| **CoD** | 1 | 아이디어 밀도 증가 |
| **재귀적 질문** | 1 | 정보 부족 탐지 |
| **ToT** | 2 | 아키텍처 대안 탐색 |
| **SOP 템플릿** | 3 | ADR 표준화 |
| **SoT** | 7 | 청사진 구조화 |
| **Context Re-ranking** | 7 | 컨텍스트 관리 |
| **병렬 확장** | 7-8 | 속도 향상 |
| **Knowledge Graph** | 9 | 모순 탐지 |

이 가이드를 따르면 각 Stage에서 **무엇을**, **어떻게**, **왜** 해야 하는지 명확합니다.
