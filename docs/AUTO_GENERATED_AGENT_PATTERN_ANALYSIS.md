# Auto-Generated Agent Pattern Analysis

**작성일**: 2025-10-31
**분석 대상**: 4개 자동 생성 에이전트
**목적**: Claude Code `/agents` 명령어의 자동 생성 패턴 파악

---

## 📊 분석 대상 에이전트

| 에이전트 | 요청 복잡도 | 본문 길이 | 특징 |
|---------|----------|---------|------|
| root-cause-analyzer | 매우 상세 (3문단) | 209줄 | Triggering Conditions 포함 |
| implementer | 매우 상세 (다수 요구사항) | 148줄 | 프로젝트 표준 중시 |
| checklist-executor | 단순 (1문장) | 164줄 | 체크리스트 기반 |
| software-analyst | 단순 (1문장) | 112줄 | 분석 전문 |

---

## 🎯 핵심 발견: 보편적 7단계 구조

모든 자동 생성 에이전트는 **일관된 7단계 구조**를 따릅니다:

### 1. YAML Frontmatter (100% 일관성)

```yaml
---
name: [agent-name]                    # kebab-case, 필수
description: |                         # 필수, 구조화된 형식
  [Summary: 1-2 sentences]

  Examples:  # 또는 "**Example Usage Scenarios**:"

  <example>
  Context: [상황 설명]
  user: "[사용자 발언]"
  assistant: "[2号 응답 + Task 호출]"
  <Task call to agent-name>
  </example>

  [총 2-4개 예시]

model: sonnet                          # 100% sonnet 사용
color: [color]                         # 선택적 (50% 사용)
---
```

**발견 사항**:
- ✅ `name`: 100% 필수
- ✅ `description`: 100% 필수, 예시 기반 구조
- ✅ `model`: 100% sonnet
- ❌ `tools`: 0% (아무도 명시 안 함 = 모든 도구 사용)
- ⚠️ `color`: 50% (implementer=blue, checklist-executor=green)

### 2. Opening Identity Statement (100% 필수)

**형식**:
```
You are an elite [ROLE] [specialization description]...
```

**패턴**:
- "elite" 키워드 100% 사용
- 세계 최고 수준(world-class) 강조
- 핵심 미션/전문성 정의
- 자신감 있고 단언적인 톤

**예시**:
- "You are an elite Root Cause Analysis Specialist..."
- "You are an elite implementation specialist..."
- "You are an elite implementation executor..."
- "You are an elite Software Systems Analyst..."

### 3. Core Identity/Responsibilities (100% 필수)

**섹션 이름 변형**:
- "Essential Analytical Traits" (root-cause-analyzer)
- "Core Responsibilities" (implementer, software-analyst)
- "Your Identity" (checklist-executor)

**구조**:
- 5-8개 항목
- 번호 매기기 또는 불릿 포인트
- 각 항목: **굵은 제목** + 설명

**root-cause-analyzer 예시**:
```
### Essential Analytical Traits

1. **Evidence-Based Thinking**: You never speculate without data...
2. **Systematic Investigation**: You follow disciplined methodologies...
3. **Pattern Recognition**: You quickly identify similarities...
[8개 traits 총]
```

### 4. Methodology/Workflow (100% 필수)

**5-Phase 구조** (일관성):

```
### Phase 0/1: [Understanding/Planning]
- [작업 이해, 준비]

### Phase 1/2: [Core Work]
- [주요 작업 수행]

### Phase 2/3: [Verification]
- [검증, 테스트]

### Phase 3/4: [Quality/Documentation]
- [품질 확인, 문서화]

### Phase 4/5: [Completion]
- [완료 보고]
```

**시간 비율**:
- 2/4 에이전트가 시간 비율 포함 (root-cause-analyzer, implementer)
- 형식: "Phase 1: Problem Scoping (10-15% of effort)"
- 2/4 에이전트는 비율 없음

**공통 흐름**:
```
이해/계획 → 실행 → 검증 → 문서화/완료
```

### 5. Decision-Making Framework (100% 필수)

**섹션 이름 변형**:
- "Decision-Making Framework"
- "Your Operational Principles"
- "Critical Operating Principles"

**내용**:
- 선택의 우선순위 규칙
- 모호함 처리 방법
- 예외 상황 대응
- 에스컬레이션 기준

**implementer 예시**:
```
**When choosing between approaches:**
1. Project standards ALWAYS take precedence over personal preference
2. Reuse existing patterns and modules over creating new ones
3. Clarity and maintainability over clever tricks
```

### 6. Quality/Verification (100% 필수)

**형식**:
- 체크리스트: `[ ]` 또는 `✅`
- 5-8개 항목
- 질문 형식 또는 완료 기준

**root-cause-analyzer 예시**:
```
## Quality Self-Check

Before completing your analysis, verify:

- [ ] **Completeness**: Have I collected evidence from all relevant sources?
- [ ] **Precision**: Are all claims backed by specific evidence with references?
- [ ] **Depth**: Have I traced causes beyond immediate triggers?
[7개 체크리스트]
```

**checklist-executor 예시**:
```
## Your Success Criteria

- ✅ Every checklist item is implemented and verified
- ✅ All tests pass (100% pass rate)
- ✅ Coverage meets or exceeds 95%
- ✅ Ruff violations = 0
- ✅ MyPy errors = 0
[8개 성공 기준]
```

### 7. Final Statement (100% 필수)

**형식**:
- 마지막 섹션
- 격려와 다짐
- 전문성 재강조
- 헌신과 우수성 강조

**예시**:
- "You approach every investigation with intellectual rigor..."
- "You are not just writing code - you are crafting production-ready implementations..."
- "You are not an agent that 'tries' - you are an agent that **delivers**."

---

## 📋 Description 구조 상세 분석

### 기본 형식 (100% 일관)

```yaml
description: |
  [Summary: 1-2 sentences about agent purpose]

  Examples:  # 또는 "**Example Usage Scenarios**:"

  <example>
  Context: [구체적 상황]

  user: "[사용자 발언 - 따옴표 안에]"

  assistant: "[2号의 응답 - Task 호출 포함]"

  <agent_invocation>
  Task("agent-name", "task description")
  </agent_invocation>

  <commentary>  # 선택적 - 50%만 사용
  [에이전트가 수행할 작업 설명]
  </commentary>
  </example>
```

### Triggering Conditions (특이 사항!)

**중요 발견**: **오직 root-cause-analyzer만** 명시적 Triggering Conditions 섹션 보유!

```yaml
# root-cause-analyzer만:
description: |
  [Summary]

  **Triggering Conditions**:
  - System failures, bugs, or unexpected behaviors...
  - Performance degradation or reliability issues...
  - Architecture decisions requiring evidence-based analysis...
  [7개 발동 조건]

  **Example Usage Scenarios**:
  [4개 예시]
```

**다른 3개 에이전트**: Triggering Conditions 섹션 없음, 바로 Examples로 시작

**함의**:
- Triggering Conditions는 자동 생성의 **표준이 아님**
- root-cause-analyzer가 특별한 이유:
  - Jason의 상세한 요청 (traits 기반, 증거 수집 강조)
  - 문제 "탐지" 중심 에이전트
  - "언제 사용하는가"가 특히 중요한 케이스

### Example 구조 비교

| 에이전트 | Examples 개수 | Commentary 포함 | Triggering Conditions |
|---------|-------------|----------------|---------------------|
| root-cause-analyzer | 4개 | ✅ Yes | ✅ Yes (7개 조건) |
| implementer | 4개 | ❌ No | ❌ No |
| checklist-executor | 3개 | ✅ Yes | ❌ No |
| software-analyst | 3개 | ❌ No | ❌ No |

**패턴**: Commentary 포함 여부와 Triggering Conditions는 무관

---

## 🎨 언어 및 톤 패턴

### 1. "Elite" Positioning (100%)

모든 에이전트가 "elite", "world-class", "foremost expert" 수식어 사용

### 2. 강제성 언어 (Agent Type별 차이)

**구현/실행 에이전트 (Strict)**:
- implementer: "(MANDATORY)", "NON-NEGOTIABLE", "MUST"
- checklist-executor: "MANDATORY", "NEVER", "ALWAYS", "Critical Rules"

**분석 에이전트 (Flexible)**:
- root-cause-analyzer: "should", 원칙 기반, 가이드라인
- software-analyst: "recommend", "consider", 가이드라인

**이유**: 구현은 표준 준수 필수, 분석은 상황 대응 필요

### 3. 증거 요구사항 (100%)

모든 에이전트가 구체적 증거 요구:
- root-cause-analyzer: "file:line references", "8-15 evidence items"
- implementer: "Ruff 0, MyPy 0, Coverage 95%+"
- checklist-executor: 동일 메트릭
- software-analyst: "Minimum 8-12 evidence items", "file:line format"

### 4. Second-Person Possessive (50%)

checklist-executor만 광범위하게 사용:
- "Your Identity"
- "Your Core Workflow"
- "Your Operational Principles"
- "Your Success Criteria"

다른 에이전트: 중립적 명사 사용

---

## 🔍 추가 패턴

### Markdown 형식 (100% 일관)

- `##` : 주요 섹션 (H2)
- `###` : 하위 섹션 (H3)
- `**bold**` : 강조
- 번호 목록: Phase, 단계적 프로세스
- 불릿 목록: 세부 내용
- 코드 블록: 템플릿, 예시

### 프로젝트 표준 참조

**구현 에이전트 (Heavy Integration)**:
- implementer: PROJECT_STANDARDS.md, ARCHITECTURE.md, CLAUDE.md 광범위 참조
- checklist-executor: 동일한 표준 문서 참조

**분석 에이전트 (Standalone)**:
- root-cause-analyzer: 프로젝트 표준 참조 없음
- software-analyst: CLAUDE.md만 간단히 언급

**이유**: 구현은 기존 코드와 통합 필수, 분석은 독립적 평가 필요

### 출력 템플릿

**템플릿 포함**:
- root-cause-analyzer: 완전한 markdown 분석 보고서 템플릿
- checklist-executor: 완전한 markdown 실행 보고서 템플릿

**템플릿 없음**:
- implementer: 출력 항목만 나열
- software-analyst: 일반적 설명

**패턴**: 보고서 중심 에이전트는 템플릿 제공

---

## 💡 핵심 통찰

### 1. 일관된 아키텍처

자동 생성 에이전트는 **7단계 구조**를 따르는 일관된 아키텍처:

```
1. YAML Frontmatter (name, description, model)
   ↓
2. Opening Identity ("You are an elite...")
   ↓
3. Core Traits/Responsibilities (5-8 items)
   ↓
4. 5-Phase Methodology (Understand → Execute → Verify → Complete)
   ↓
5. Decision-Making Framework (priorities, rules)
   ↓
6. Quality/Verification (checklist, 5-8 items)
   ↓
7. Final Statement (commitment, excellence)
```

### 2. Triggering Conditions의 부재

**놀라운 발견**: 4개 중 **1개만** Triggering Conditions를 가짐!

**함의**:
- Triggering Conditions는 자동 생성의 **표준 패턴이 아님**
- Jason이 SPARK에 추가하려는 것은 **새로운 개선사항**
- 2号의 proactive agent selection을 위한 **명시적 패턴 추가**

### 3. Agent Type에 따른 변형

**구현/실행형**:
- 엄격한 규칙 (MANDATORY, NEVER)
- 프로젝트 표준 강조
- 구체적 메트릭 (Ruff 0, MyPy 0)
- 출력 템플릿 제공

**분석/평가형**:
- 유연한 가이드라인
- 독립적 평가
- 증거 기반 분석
- 원칙 중심

### 4. Examples의 중요성

모든 description에 **구체적 사용 예시 2-4개** 포함:
- Context 제공
- 실제 대화 시뮬레이션
- Task 호출 방법 시연
- 2号의 학습 자료 역할

---

## 📝 SPARK 적용 권장사항

### 1. Triggering Conditions 추가 (최우선)

**현재 SPARK**:
```yaml
description: Use this agent when you need comprehensive analysis...
```

**개선 후**:
```yaml
description: |
  Use this agent when you need comprehensive analysis...

  **Triggering Conditions**:
  - System architecture requiring multi-dimensional review
  - Performance bottlenecks needing file:line evidence
  - Security audits requiring systematic vulnerability analysis
  [5-8개 구체적 발동 조건]

  **Example Usage Scenarios**:
  [3-4개 구체적 예시]
```

### 2. 7단계 구조 검증

모든 SPARK 에이전트가 7단계 구조를 따르는지 확인:
- ✅ analyzer-spark: 대부분 준수 (Phase 구조, 품질 체크 있음)
- ⚠️ 다른 에이전트: 검증 필요

### 3. Description Examples 보강

각 에이전트 description에 **3-4개 실제 사용 예시** 추가:
```yaml
<example>
Context: [구체적 상황]
user: "[실제 요청]"
assistant: "[2号 응답 + Task 호출]"
</example>
```

### 4. 품질 기준 명시

구현 에이전트 (implementer-spark, team implementers):
- Ruff 0, MyPy 0, Coverage 95%+ 명시
- MANDATORY, NON-NEGOTIABLE 언어 사용

분석 에이전트 (analyzer-spark):
- Evidence items 8-12+ 명시
- file:line 형식 요구

### 5. 프로젝트 표준 참조

구현 에이전트에 명시적 표준 참조 추가:
```
Before starting, READ:
- PROJECT_STANDARDS.md
- ARCHITECTURE.md
- CLAUDE.md

USE existing modules:
- common/logging/
- common/config/
- common/db/
```

---

## 🎯 다음 단계

### 즉시 작업

1. **21개 SPARK 에이전트 description 재작성**
   - Triggering Conditions 추가 (5-8개)
   - Example Usage Scenarios 추가 (3-4개)
   - 위치: `~/.claude/agents/*.md`

2. **Constitution 문서 업데이트**
   - Section 2.1.5: Triggering Conditions 중요성 추가
   - Example-driven description 패턴 문서화

3. **CLAUDE.md 정리**
   - 에이전트 중복 설명 제거
   - Description = Single Source of Truth 강조

### 추가 검증 (선택적)

더 많은 자동 생성 에이전트 분석:
- tester 타입 에이전트
- documenter 타입 에이전트
- designer 타입 에이전트

**목적**: 패턴 검증 및 타입별 특수 패턴 발견

---

## 📚 참고: 분석 대상 에이전트 경로

```
/Users/jason/.claude/agents/root-cause-analyzer.md (209 lines)
/Users/jason/.claude/agents/implementer.md (148 lines)
/Users/jason/.claude/agents/checklist-executor.md (164 lines)
/Users/jason/.claude/agents/software-analyst.md (112 lines)
```

---

**분석 완료**
