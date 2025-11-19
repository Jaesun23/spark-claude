# DNA v4.0 에이전트 통합 프로세스 흐름도

**작성일**: 2025-11-19
**작성자**: Jason & Claude (2호)
**목적**: Gemini 검토를 위한 전체 프로세스 개요 및 에이전트 시스템 통합 설계

---

## 1. 개요: 왜 에이전트가 필요한가?

### 1.1 DNA v4.0의 핵심 문제

**컨텍스트 한계의 본질** (Jason's Insight):
- 트랜스포머 모델 구조 자체의 한계
- 토큰 간 관계가 길어지면 약해짐
- **많은 정보 ≠ 좋은 결과**
- 적당한 길이 + 적당한 수준 = 좋은 작업

**현재 DNA v4.0의 한계**:
1. **"무엇을 하라"는 있지만 "어떻게 하라"가 없음**
   - Stage마다 사람(Jason)과 AI가 즉흥적으로 해결
2. **Context Rot** (문맥 부패)
   - Stage 진행될수록 초기 결정사항(패밀리, NFR) 희석
3. **검증 메커니즘 부재**
   - "완성했다"의 기준 불명확
4. **순차 vs 병렬 불명확**
   - 어떤 작업이 병렬 가능한지 모름

### 1.2 해결 방향: 에이전트 시스템

**Gemini 연구 보고서에서 차용**:
- Skeleton-of-Thought (SoT): 병렬 확장 구조
- Chain of Density (CoD): 점진적 상세화
- Tree of Thoughts (ToT): 다중 경로 탐색
- Contradiction Detection: 자동 충돌 검증

**에이전트 = "어떻게"의 답**:
```
에이전트 정의 = 역할 + Traits + Behavior Protocol + Professional Workflow
```

---

## 2. 전체 프로세스 흐름도

### 2.1 High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     DNA v4.0 + Agent System                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Jason's Idea                                                   │
│      │                                                          │
│      ▼                                                          │
│  ┌─────────────────────────────────┐                           │
│  │  Phase 1: 아이디어 정제 (CoD)     │  Stage 1-2               │
│  │  - System Classifier Agent      │                           │
│  │  - Constraints Investigator     │                           │
│  └─────────────┬───────────────────┘                           │
│                │                                                │
│                ▼                                                │
│  ┌─────────────────────────────────┐                           │
│  │  Phase 2: 아키텍처 스켈레톤 (SoT+ToT) │  Stage 3-4          │
│  │  - Architecture Decision Maker   │                           │
│  │  - Blueprint Designer           │                           │
│  └─────────────┬───────────────────┘                           │
│                │                                                │
│                ▼                                                │
│  ┌─────────────────────────────────┐                           │
│  │  Phase 3: 환경 구축              │  Stage 5-6               │
│  │  - implementer-spark            │                           │
│  │  - documenter-spark             │                           │
│  └─────────────┬───────────────────┘                           │
│                │                                                │
│                ▼                                                │
│  ┌─────────────────────────────────┐                           │
│  │  Phase 4: 레고블럭 실행 (SoT)     │  Stage 7-9               │
│  │  - Blueprint → Breakdown        │                           │
│  │  - Checklist 작성               │                           │
│  └─────────────┬───────────────────┘                           │
│                │                                                │
│                ▼                                                │
│  ┌─────────────────────────────────┐                           │
│  │  Phase 5: 구현                   │  기존 SPARK 활용          │
│  │  - implementer-spark            │                           │
│  │  - tester-spark                 │                           │
│  │  - documenter-spark             │                           │
│  └─────────────────────────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 DNA v4.0 핵심과의 매핑

| Jason's 3단계 해결책 | Phase 매핑 | 에이전트 역할 |
|---------------------|-----------|-------------|
| **1. 단계적 정의** | Phase 1-2 | 패밀리, NFR, ADR 결정 |
| **2. 환경 강제** | Phase 3 | DNA 시스템, Standards, 자동화 |
| **3. 레고블럭 전략** | Phase 4-5 | 청사진 → 분해 → 체크리스트 → 구현 |

---

## 3. Phase별 상세 설계

### 3.1 Phase 1: 아이디어 정제 (Stage 1-2)

**적용 기법**: Chain of Density (CoD)

```
Iteration 1: 아이디어 스켈레톤 (핵심 기능만)
Iteration 2: Layer 1 질문 답변 추가
Iteration 3: NFR 우선순위 추가
Iteration 4: Layer 3 제약 추가
Iteration 5: 충돌 예측 및 해결
```

#### Stage 1: System Classifier Agent

| 항목 | 내용 |
|-----|-----|
| **역할** | 18가지 패밀리 중 결정 |
| **Traits** | Pattern Matching, Evidence-Based, Systematic Inquiry, Contextual Understanding |
| **입력** | Jason의 아이디어, 비즈니스 컨텍스트 |
| **출력** | 패밀리(A-A-B), Layer 1 분석, NFR 초안, 검증 사례 |
| **검증** | 모든 질문 답변됨, 검증 사례 2개 이상, 신뢰도 평가 |

#### Stage 2: Constraints Investigator Agent

| 항목 | 내용 |
|-----|-----|
| **역할** | Layer 3 환경 제약 조사 |
| **Traits** | Inquisitive, Constraint-Aware, Conflict Anticipation, Contextual Adaptation |
| **입력** | 패밀리, NFR 초안 |
| **출력** | 기술/팀/인프라 제약, 잠재적 충돌, 예비 해결안 |
| **검증** | 3개 카테고리 완료, 충돌 2개 이상 식별, 해결안 3가지 |

**Phase 1 결과물**:
- 고밀도 요구사항 명세서
- 패밀리 결정 (A-A-B 형식)
- NFR 우선순위 (정확성 > 속도 > 보안 > 비용)
- Layer 3 제약 목록
- 잠재적 충돌 및 해결안

---

### 3.2 Phase 2: 아키텍처 스켈레톤 (Stage 3-4)

**적용 기법**:
- Tree of Thoughts (ToT): ADR 3옵션 비교
- Skeleton-of-Thought (SoT): 청사진 목차 확정 후 병렬 확장

```
Step 1: Bootstrap 요소 목록 확정 (RDBMS, Cache, Messaging 등)
Step 2: 각 ADR 병렬 작성 (SoT)
        ├─ ADR-001 RDBMS (ToT: PostgreSQL vs MySQL vs Aurora)
        ├─ ADR-002 Cache (ToT: Redis vs Memcached vs ElastiCache)
        └─ ADR-003 Messaging (ToT: Kafka vs RabbitMQ vs SQS)
Step 3: ADR 간 충돌 검증 (GraphRAG)
Step 4: 청사진 스켈레톤 작성
```

#### Stage 3: Architecture Decision Maker Agent

| 항목 | 내용 |
|-----|-----|
| **역할** | Bootstrap ADR 작성 |
| **Traits** | Trade-off Reasoning, Systematic Comparison, Conflict Detection, Evidence-Based |
| **입력** | 패밀리, NFR, Layer 3 제약 |
| **출력** | Bootstrap ADR 세트 (5-7개), 충돌 해결됨 |
| **검증** | 모든 ADR 3옵션 비교, NFR+제약 반영, 충돌 해결, 예산 내 |

**ADR 작성 프로세스 (CoD 적용)**:
```
Iteration 1 (5분):  스켈레톤 (Context, Decision, Alternatives 목록)
Iteration 2 (10분): 옵션 비교 (스펙, 비용, 장단점)
Iteration 3 (10분): Rationale (NFR 관점, Layer 3 관점)
Iteration 4 (10분): Consequences (긍정/부정, 완화 전략)
Iteration 5 (15분): 충돌 검증 및 수정
```

#### Stage 4: Blueprint Designer Agent

| 항목 | 내용 |
|-----|-----|
| **역할** | Clean Architecture 청사진 작성 |
| **Traits** | Domain Modeling, Architectural Thinking, Mapping Ability, Dependency Awareness |
| **입력** | Bootstrap ADR, 도메인 요구사항 |
| **출력** | 도메인 분해, 4-Layer 설계, Bootstrap 매핑, API 설계 |
| **검증** | Dependency Rule 준수, Bootstrap 매핑 완료, API 일관성 |

**Phase 2 결과물**:
- Bootstrap ADR 세트 (5-7개)
- 청사진 스켈레톤 (목차)
- 도메인 모델 초안
- 4-Layer 구조 초안

---

### 3.3 Phase 3: 환경 구축 (Stage 5-6)

**핵심**: AI가 틀리고 싶어도 틀릴 수 없게!

```
환경 = Standards + 11 DNA Systems + 자동화 강제

├─ Standards (문서화된 규칙)
│   └─ "print() 사용 금지", "타입 힌트 필수" 등
│
├─ 11 DNA Systems (공용 모듈)
│   ├─ src/core/logging/ (structlog)
│   ├─ src/core/types/ (Pydantic)
│   ├─ src/core/config/ (Dynaconf)
│   └─ ... (11개)
│
└─ 자동화 강제
    ├─ Pre-commit hooks (ruff, mypy)
    ├─ CI/CD (pytest, coverage)
    └─ Import-linter (의존성 규칙)
```

#### Stage 5: DNA 시스템 구현
- **에이전트**: implementer-spark (기존)
- **작업**: 11개 공용 모듈 구현, Pre-commit hooks 설정

#### Stage 6: 프로젝트 표준
- **에이전트**: documenter-spark (기존)
- **작업**: Standards 문서화, import-linter 규칙 설정

**Phase 3 결과물**:
- 작동하는 DNA 시스템 (src/core/)
- PROJECT_STANDARDS.md
- 자동화된 Governance (환경)

---

### 3.4 Phase 4: 레고블럭 실행 (Stage 7-9)

**적용 기법**: Skeleton-of-Thought (SoT)

```
Step 1: 청사진 스켈레톤 완성 (Phase 2에서 시작)
Step 2: 각 섹션 병렬 확장 (SoT)
        ├─ Domain Layer 상세
        ├─ Application Layer 상세
        ├─ Infrastructure Layer 상세
        └─ Presentation Layer 상세
Step 3: 작업 분해 (독립 실행 가능 단위)
Step 4: 체크리스트 작성 (각 작업별)
```

#### Stage 7: 청사진 완성
- 환경(Stage 1-6)을 제외한 모든 것을 담음
- 컨텍스트가 온전할 때 최대한 상세히 작성

#### Stage 8: 작업 분해
- 독립 실행 가능한 레고블럭으로 나누기
- 각 작업 2-4시간 이내

#### Stage 9: 체크리스트
- 각 블럭별로 "그것만 보고 실행 가능"한 생명줄
- 나중의 2호/1호/에이전트를 위한 완전한 정보

**Phase 4 결과물**:
- 완전한 청사진 (환경 제외 모든 것)
- 레고블럭 작업 목록
- 각 블럭별 체크리스트

---

### 3.5 Phase 5: 구현 (기존 SPARK 활용)

```
체크리스트 1 → implementer-spark → tester-spark → documenter-spark
체크리스트 2 → implementer-spark → tester-spark → documenter-spark
...
모든 체크리스트 완료 = 프로젝트 완성
```

**Phase 5 결과물**:
- 완성된 프로젝트

---

## 4. Context Rot 방지 메커니즘

### 4.1 문제 정의

> "텍스트가 길어질수록 초기의 설정이나 요구사항이 후반부 생성에 미치는 영향력이 약화되고, 논리적 일관성이 무너지는 현상" - Gemini 보고서

**DNA v4.0에서의 증상**:
- Stage 1에서 결정한 패밀리가 Stage 3에서 무시됨
- NFR 우선순위가 ADR 작성 시 반영 안 됨
- Stage 간 모순 발생

### 4.2 해결 방안: 3중 방어

#### 방어 1: Context Summary (오케스트레이터 관리)

```json
{
  "project_id": "project_YYYYMMDD_HHMMSS",
  "core_decisions": {
    "family": "A-A-B",
    "nfr_priority": ["정확성", "속도", "보안", "비용"],
    "critical_constraints": [
      "ACID 필수",
      "예산 $500/월",
      "팀 Python 전문"
    ]
  },
  "stage_outputs": {
    "stage1": { "status": "completed", "file": "01C-01_family.md" },
    "stage2": { "status": "completed", "file": "02C-01_constraints.md" },
    "stage3": { "status": "in_progress", "file": "03A-*.md" }
  },
  "contradiction_log": []
}
```

#### 방어 2: Context Re-ranking (각 에이전트 호출 시)

```python
def call_agent(agent_name, task, context_summary):
    # 해당 Stage에 필요한 정보만 선별
    relevant_context = extract_relevant_context(task, context_summary)

    # 프롬프트 상단에 핵심 결정사항 배치
    prompt = f"""
    [CORE CONTEXT - 반드시 준수]
    - Family: {relevant_context['family']}
    - NFR Priority: {relevant_context['nfr_priority']}
    - Critical Constraints: {relevant_context['constraints']}

    위 결정사항을 반드시 준수하여 작업하세요.

    [TASK]
    {task}
    """

    return agent.execute(prompt)
```

#### 방어 3: Contradiction Detection (검증 단계)

```python
class ContradictionDetector:
    def check_consistency(self, stage_output, context_summary):
        """Stage 산출물이 핵심 결정사항과 일치하는지 검증"""

        contradictions = []

        # 패밀리 일치 검증
        if not self.family_consistent(stage_output, context_summary['family']):
            contradictions.append("Family mismatch detected")

        # NFR 반영 검증
        if not self.nfr_reflected(stage_output, context_summary['nfr_priority']):
            contradictions.append("NFR priority not reflected")

        # 제약 준수 검증
        if not self.constraints_respected(stage_output, context_summary['constraints']):
            contradictions.append("Constraint violation detected")

        return contradictions
```

### 4.3 실행 예시

**Stage 3 ADR 작성 시**:

```
1. 오케스트레이터가 Context Summary 로드
2. Architecture Decision Maker Agent 호출 시 Context Re-ranking:
   "[CORE CONTEXT] Family: A-A-B, NFR: 정확성>속도, Constraint: ACID 필수"
3. Agent가 ADR 작성
4. Contradiction Detector가 검증:
   - "RDBMS ADR에서 Eventual Consistency 선택함 → ACID 필수와 모순!"
5. Agent에게 수정 요청
6. 수정 후 재검증
7. 통과 시 다음 Stage
```

---

## 5. 오케스트레이터 역할 (2호/Main Claude)

### 5.1 핵심 책임

1. **전체 워크플로우 관리**
   - Phase/Stage 진행 상태 추적
   - 에이전트 호출 순서 결정

2. **Context Summary 관리**
   - 초기 결정사항 보존
   - Stage 간 데이터 전달

3. **검증 프로토콜 실행**
   - 에이전트 Self-Validation 결과 확인
   - Contradiction Detection 실행
   - 실패 시 재시도 (최대 3회)

4. **Jason과 상호작용**
   - 의사결정 요청 (충돌 해결 등)
   - 진행 상황 보고
   - 피드백 수렴

### 5.2 워크플로우 예시

```python
class DNAOrchestrator:
    def run_phase1(self, idea):
        """Phase 1: 아이디어 정제"""

        # Stage 1
        result1 = self.call_agent(
            "system-classifier-spark",
            f"Analyze: {idea}",
            context=None  # 첫 Stage
        )

        # 검증
        if not result1.self_validation_passed:
            result1 = self.retry(result1, max_attempts=3)

        # Context Summary 초기화
        self.context_summary = {
            "family": result1.family,
            "nfr_priority": result1.nfr_priority
        }

        # Stage 2
        result2 = self.call_agent(
            "constraints-investigator-spark",
            "Investigate constraints",
            context=self.context_summary
        )

        # Contradiction Detection
        contradictions = self.detect_contradictions(result2)
        if contradictions:
            result2 = self.resolve_contradictions(result2, contradictions)

        # Context Summary 업데이트
        self.context_summary.update({
            "constraints": result2.constraints,
            "conflicts": result2.conflicts
        })

        return self.context_summary
```

---

## 6. Gemini 검토 포인트

### 6.1 전체 구조

1. **Phase 구분이 적절한가?**
   - 5개 Phase로 나눈 것이 논리적인가?
   - Phase 간 의존성이 명확한가?

2. **기법 적용이 올바른가?**
   - SoT: 병렬 확장에 적절히 사용되었는가?
   - CoD: 점진적 상세화에 효과적인가?
   - ToT: 옵션 비교에 적합한가?

### 6.2 에이전트 설계

1. **Stage 1-4 에이전트의 Traits가 적절한가?**
   - 추가/수정/삭제할 Traits?
   - Traits 간 우선순위?

2. **Behavior Protocol이 검증 가능한가?**
   - Python 코드로 명시 가능한 규칙?
   - Self-Validation 체크리스트가 충분한가?

3. **Professional Workflow가 전문가의 자연스러운 흐름인가?**
   - Iteration Points가 적절한가?

### 6.3 Context Rot 방지

1. **3중 방어 메커니즘이 효과적인가?**
   - Context Summary 구조가 적절한가?
   - Context Re-ranking이 충분한가?
   - Contradiction Detection이 포괄적인가?

2. **다른 방지 메커니즘이 필요한가?**
   - Knowledge Graph 도입?
   - 요약 전략?

### 6.4 실용성

1. **산출물 품질이 실무 사용 가능한가?**
   - 각 Phase 결과물이 충분히 상세한가?
   - 누락/불필요한 정보가 있는가?

2. **소요 시간이 현실적인가?**
   - 병렬화 효과가 적절히 반영되었는가?

---

## 7. 다음 단계

### 7.1 Gemini 검토 후 작업

1. **에이전트 정의 확정**
   - Traits, Behavior Protocol, Workflow 최종화
   - `.claude/agents/` 에 에이전트 파일 작성

2. **오케스트레이터 구현**
   - Context Summary 관리 로직
   - Contradiction Detection 구현

3. **Custom Commands 작성**
   - `/dna-phase1`, `/dna-phase2` 등
   - 각 Phase를 실행하는 명령어

4. **통합 테스트**
   - 실제 프로젝트로 전체 프로세스 검증
   - Context Rot 방지 효과 측정

### 7.2 참조 문서

- `DNA_ALL_GUIDES_MERGED.md`: 현재 DNA v4.0 전체 가이드
- `Gemini_AI_장문작성_및_소프트웨어_개발방법론.md`: Gemini 연구 보고서

---

**작성자**: Jason & Claude (2호)
**날짜**: 2025-11-19
