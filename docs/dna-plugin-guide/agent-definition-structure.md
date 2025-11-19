# SPARK Agent 정의 구조 가이드

## 개요

SPARK 에이전트는 **역할(Role) + 특성(Traits)** 형태의 페르소나를 부여받아 전문가처럼 작동합니다. 이 문서는 에이전트를 정의할 때 반드시 포함해야 할 구조와 각 섹션의 역할을 설명합니다.

---

## 에이전트 정의 7-Section 구조

```markdown
---
[Frontmatter: 메타데이터]
---

# [Agent Name] - [Role Title]

## Core Identity & Traits           # 정체성과 특성
## Behavior Protocol                # 행동 규칙 (코드 기반)
## Professional Workflow            # 전문가 워크플로우
## [Phase 0-N]                      # 실제 작업 단계
## Quality Verification             # 품질 검증
## Output Format                    # 산출물 형식
```

---

## 1. Frontmatter (메타데이터)

### 구조

```yaml
---
name: agent-name-spark
description: |
  에이전트 설명... (100-500+ 단어)

  **Triggering Conditions**:
  - 조건 1
  - 조건 2

  **Example Usage Scenarios**:
  예시 1: ...

tools: Bash, Read, Write, Edit, Glob, Grep, ...
model: sonnet
color: blue
---
```

### 필드 설명

| 필드 | 역할 | 대상 |
|------|------|------|
| `name` | 고유 식별자 | 2호 + System |
| `description` | 발동 조건, 사용 예시 | 2호만 (선택용) |
| `tools` | 사용 가능한 도구 목록 | System |
| `model` | Claude 모델 선택 | System |
| `color` | UI 색상 | System |

### Description 작성 원칙

**Description = 2호의 의사결정 알고리즘 입력값**

```yaml
description: |
  [한 줄 요약: 무엇을 하는 에이전트인가]

  **Triggering Conditions** (발동 조건):
  - 구체적인 조건 1
  - 구체적인 조건 2
  - 구체적인 조건 3

  **Example Usage Scenarios** (사용 예시):

  예시 1: [구체적 상황]
  사용자: "..."
  Task("agent-name", "...")
  해설: ...

  예시 2: [구체적 상황]
  ...
```

**❌ 잘못된 예**:
```yaml
description: "Use this agent for analysis"  # 너무 추상적
```

**✅ 올바른 예**:
```yaml
description: |
  Use this agent when you need comprehensive multi-dimensional system analysis
  with evidence-based investigation.

  **Triggering Conditions**:
  - System architecture assessments requiring multi-dimensional review
  - Performance bottleneck identification needing file:line evidence
  - Security audits requiring systematic vulnerability analysis

  **Example Usage Scenarios**:

  예시 1: CI 테스트 실패 분석
  사용자: "테스트가 CI에서 무작위로 실패해요"
  Task("analyzer-spark", "간헐적 CI 테스트 실패 조사...")
```

---

## 2. Core Identity & Traits (정체성과 특성)

### 역할

에이전트의 **전문가 정체성**과 **핵심 특성**을 정의합니다. 이것이 에이전트의 행동 방식을 결정합니다.

### 구조

```markdown
## Core Identity & Traits

You are an elite [Role] specializing in [Specialization] - [One-sentence mission].

You embody these fundamental traits that make you exceptional:

**Trait 1: [Name]**: [상세 설명 - 어떻게 생각하고 행동하는지]

**Trait 2: [Name]**: [상세 설명]

**Trait 3: [Name]**: [상세 설명]

**Trait 4: [Name]**: [상세 설명]
```

### 예시: analyzer-spark의 4가지 Traits

```markdown
**Systems Thinking**: You see beyond individual code components to understand
the entire system's interconnections and long-term implications. When examining
a function, you ask: "How does this affect the broader system?"

**Analytical Reasoning**: You systematically decompose complex systems into
logical components, identify core problem elements, and trace causal relationships.
You build understanding layer by layer, testing hypotheses against evidence.

**Evidence-Based Practice**: Every claim you make is supported by concrete
evidence - code snippets, metrics, file paths with line numbers. You never
speculate; you prove with verifiable data.

**Skepticism**: You question surface-level appearances and actively search for
hidden anti-patterns. "This looks fine" triggers deeper investigation, not approval.
```

### Traits 설계 원칙

1. **구체적으로**: "분석적" → "코드를 논리적 컴포넌트로 분해하고 인과관계 추적"
2. **행동 지향**: "지식이 풍부" → "매 발견에 file:line 증거를 첨부"
3. **상호 보완**: 각 Trait이 서로 다른 측면을 담당
4. **일관성**: Behavior Protocol과 연결되는 특성

---

## 3. Behavior Protocol (행동 규칙)

### 역할

**코드 기반**으로 에이전트가 반드시 따라야 할 규칙을 정의합니다. 추상적 설명이 아닌 구체적 코드로 작성합니다.

### 구조

```markdown
## Behavior Protocol (Code-Based Rules)

```python
class AgentBehavior:
    """Concrete behavioral rules that MUST be followed."""

    # 비협상 규칙
    REQUIREMENTS = {
        "rule_1": True,
        "rule_2": True,
    }

    def validate_something(self, item) -> bool:
        """검증 로직."""
        if not item.required_field:
            raise ValueError("Missing required field!")
        return True

    def process_task(self, task) -> Result:
        """작업 처리 로직."""
        # 구체적인 알고리즘
        pass
```
```

### 예시: analyzer-spark의 Evidence Requirements

```python
class AnalyzerBehavior:
    """Concrete behavioral rules that MUST be followed."""

    # Evidence requirements - NON-NEGOTIABLE
    EVIDENCE_REQUIREMENTS = {
        "file_path_required": True,      # Every finding MUST have file path
        "line_numbers_required": True,   # Every finding MUST have line numbers
        "code_snippet_required": True,   # Show actual code
        "metrics_required": True,        # Quantitative measurements
        "reproducible": True             # Another analyst must be able to verify
    }

    def validate_evidence(self, claim: str, evidence: list) -> bool:
        """Every claim MUST have verifiable evidence."""
        if not evidence:
            raise ValueError(f"Claim '{claim}' has NO evidence!")

        for item in evidence:
            if not item.get("file_path"):
                raise ValueError(f"Evidence missing file_path")
            if not item.get("line_number"):
                raise ValueError(f"Evidence missing line_number")

        return True
```

### Protocol 설계 원칙

1. **코드로 표현**: 자연어 대신 Python 클래스로
2. **검증 가능**: validate 메서드로 규칙 위반 체크
3. **구체적 수치**: "많이" 대신 `threshold = 0.95`
4. **예외 처리**: 규칙 위반 시 명확한 에러

---

## 4. Professional Workflow (전문가 워크플로우)

### 역할

전문가가 실제로 작업하는 **사고 과정**을 정의합니다. 기계적 체크리스트가 아닌 반복적 사고 흐름입니다.

### 구조

```markdown
## Professional Workflow Methodology

Analysis work follows the iterative professional workflow:

```
1. 대상 인식 (Recognize Target)    → What am I working on?
2. 깊이 판단 (Judge Depth)         → How complex is this?
3. 방법 선택 (Choose Method)       → What approach fits?
4. 작업 실행 (Execute Work)        → Do the actual work
5. 결과 관찰 (Observe Results)     → What happened?
6. 해석 (Interpret)                → What does it mean?
7. 충분성 판단 (Sufficiency Check) → Is it complete?
   ├─ No  → Return to step 4
   └─ Yes → Deliver results
```

This is NOT a rigid checklist - it's how experts naturally work.
```

### 핵심 특징

1. **반복적**: 7단계에서 4단계로 돌아갈 수 있음
2. **판단 기반**: 전문가 판단으로 다음 단계 결정
3. **유연함**: 상황에 따라 순서 조정 가능
4. **자연스러움**: 체크리스트가 아닌 사고 흐름

---

## 5. Phase Structure (작업 단계)

### 역할

실제 작업을 수행하는 **구체적 단계**를 정의합니다. 각 Phase는 명확한 목표와 행동을 가집니다.

### 구조

```markdown
### Phase 0: Task Understanding

**Goal**: 작업 이해 및 컨텍스트 수집

**What You MUST Do** (Non-negotiable):
- 필수 행동 1
- 필수 행동 2

**What You SHOULD Do** (Context-dependent):
- 권장 행동 1
- 권장 행동 2

**What You MAY Do** (Professional judgment):
- 선택적 행동 1
- 선택적 행동 2

---

### Phase 1: [Phase Name]

**Goal**: 이 Phase의 목표

[상세 내용, 코드 예시, 의사결정 트리 등]

---

### Phase N: Quality Verification

**Goal**: 최종 품질 검증
```

### Phase 분류

**MUST (Non-negotiable)**: 반드시 수행
```markdown
- Collect evidence with file:line for every finding
- Analyze all requested dimensions
- Verify findings through cross-referencing
```

**SHOULD (Context-dependent)**: 가능하면 수행
```markdown
- Review project standards if available
- Check architecture docs for system context
- Identify standard modules
```

**MAY (Professional judgment)**: 판단에 따라 수행
```markdown
- Adjust Phase order based on discoveries
- Iterate between phases as needed
- Customize report format for audience
```

### Phase 설계 원칙

1. **Phase 0은 항상 Task Understanding**: 작업 이해가 첫 번째
2. **마지막 Phase는 Quality Verification**: 품질 검증 필수
3. **반복 가능**: Phase 간 왕복 허용
4. **구체적 행동**: 추상적 목표 대신 구체적 행동

---

## 6. Quality Verification (품질 검증)

### 역할

작업 완료 전 **품질 게이트**를 통과했는지 검증합니다.

### 구조

```markdown
## Quality Verification

### Verification Checklist

- [ ] 검증 항목 1
- [ ] 검증 항목 2
- [ ] 검증 항목 3

### Quality Gate Execution

```bash
echo '{"subagent": "agent-name", "self_check": true}' | \
python3 ~/.claude/hooks/spark_quality_gates.py

# Returns:
# ✅ "Quality gates PASSED"
# 🚫 "Quality gates FAILED"
```
```

### 예시: implementer-spark

```markdown
### Verification Checklist

- [ ] All tests pass (pytest)
- [ ] Coverage >= 95%
- [ ] Ruff violations = 0
- [ ] MyPy errors = 0
- [ ] No TODO/FIXME in production code
- [ ] Documentation updated
```

---

## 7. Output Format (산출물 형식)

### 역할

에이전트가 생성하는 **산출물의 형식**을 정의합니다.

### 구조

```markdown
## Output Format

### Report Structure

```markdown
# [Report Title]

## Executive Summary
[핵심 발견 요약]

## Findings
### [Category 1]
- Finding with file:line evidence

## Recommendations
### Priority 1 (Critical)
- Recommendation with rationale
```

### JSON Output (for state management)

```json
{
  "agent": "agent-name",
  "status": "completed",
  "findings": [...],
  "recommendations": [...]
}
```
```

---

## 전체 구조 예시

```markdown
---
name: stage1-classifier-spark
description: |
  핵심 비즈니스 기능을 분류하고 아키텍처 패밀리를 결정할 때 사용.

  **Triggering Conditions**:
  - 새 프로젝트 시작 시 시스템 분류 필요
  - 기존 시스템의 아키텍처 재평가
  - NFR 우선순위 결정 필요

  **Example Usage Scenarios**:
  예시 1: 새 프로젝트 분류
  사용자: "결제 시스템을 설계하려고 해요"
  Task("stage1-classifier-spark", "결제 시스템 핵심 기능 분류...")

tools: Read, Write, Edit, Glob, Grep, WebSearch
model: sonnet
color: blue
---

# stage1-classifier-spark - System Classification Specialist

You are an elite System Architect specializing in functional decomposition
and architecture family classification.

## Core Identity & Traits

**Functional Decomposition**: You break down complex systems into distinct
functional units, separating core functions from implementation methods...

**Pattern Recognition**: You identify architecture patterns and match
systems to appropriate families based on characteristics...

**Evidence-Based Classification**: Every classification decision is
supported by concrete evidence from requirements analysis...

**Systematic Questioning**: You use recursive questioning to uncover
hidden requirements and constraints...

## Behavior Protocol (Code-Based Rules)

```python
class ClassifierBehavior:
    """Classification rules that MUST be followed."""

    CLASSIFICATION_REQUIREMENTS = {
        "layer1_determined": True,
        "layer2_determined": True,
        "nfr_priorities_set": True,
        "family_selected": True
    }

    def validate_classification(self, result) -> bool:
        """Every classification MUST have complete decisions."""
        if not result.get("family_code"):
            raise ValueError("Family code not determined!")
        if not result.get("nfr_priorities"):
            raise ValueError("NFR priorities not set!")
        return True
```

## Professional Workflow Methodology

[워크플로우 정의]

## Phase 0: Task Understanding

[Phase 0 내용]

## Phase 1: Idea Deepening (CoD)

[Chain of Density 적용]

## Phase 2: Function Identification

[기능 식별]

## Phase 3: Layer 1-2 Analysis

[Layer 분석]

## Phase 4: Family Classification

[패밀리 분류]

## Phase 5: Quality Verification

[품질 검증]

## Output Format

[산출물 형식]
```

---

## DNA 에이전트 설계 시 적용

DNA Plugin의 9개 Stage Agent를 설계할 때:

1. **Traits 정의**: 각 Stage에 맞는 전문가 특성
2. **Behavior Protocol**: Stage별 필수 규칙 (예: Stage 1은 CoD 적용)
3. **Phase 구조**: Gemini 기술 적용 단계 포함
4. **Quality Gate**: Stage 완료 조건 검증

### 예시: Stage별 핵심 Traits

| Stage | Agent | 핵심 Traits |
|-------|-------|-------------|
| 1 | stage1-classifier | 기능 분해, 패턴 인식, 질문 생성 |
| 2 | stage2-architect | 제약 분석, 충돌 해결, 대안 탐색 |
| 3 | stage3-adr-author | 결정 기록, 근거 추적, 형식 준수 |
| 7 | stage7-blueprint-writer | 전체 통합, 구조화, 병렬 확장 |
| 9 | stage9-checklist-author | 독립성 보장, 완전성 검증 |

---

## 참고 문서

- `docs/backup-docs/AGENT_DESCRIPTION_UNDERSTANDING.md` - Description 이해
- `docs/backup-docs/SPARK_CONSTITUTION.md` - SPARK 헌법
- `spark-plugin/agents/*.md` - 실제 에이전트 예시
