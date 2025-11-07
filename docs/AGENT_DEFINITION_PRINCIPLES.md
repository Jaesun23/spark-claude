# Agent Definition Principles (에이전트 정의 원칙)

**작성일**: 2025-10-31
**기반 자료**:
- Anthropic 공식 블로그: "Effective Context Engineering for AI Agents"
- Anthropic 챗봇과의 대화 (공식 문서 기반)
- 자동 생성 에이전트 4개 패턴 분석
- SPARK Constitution v1.2

**핵심 원칙**: **페르소나(역할 + Traits)는 불변, 나머지는 Context Engineering**

---

## 🎯 핵심 조직 원칙 (Core Organizing Principle)

```typescript
// Jason's Key Insight
const AgentStructure = {
  INVARIANT: "Persona (Role + Traits, max 5)",  // 절대 변하지 않음
  VARIABLE: "Context Engineering (everything else)"  // 최적화 가능
};
```

**페르소나 = WHO the agent is** (불변)
- 역할 (Role)
- 핵심 특성 (Traits, 최대 5개)
- 전문성 (Expertise)
- 가치관 (Values)

**Context = HOW and WHEN** (context-engineered)
- Description (언제 사용하는가)
- Methodology (어떻게 작동하는가)
- Verification (무엇을 검증하는가)
- Output (무엇을 산출하는가)

---

## 📊 Complete Agent Definition Framework

### LAYER 1: FOUNDATION (불변 계층)

**목적**: 에이전트의 정체성과 핵심 가치를 정의

#### 1.1 Role Definition (역할 정의)
```markdown
You are an elite [ROLE] [specialization]...
```

**원칙**:
- "elite", "world-class", "foremost expert" 포지셔닝
- 명확한 역할 정의
- 전문 영역 명시

**예시**:
- "You are an elite Root Cause Analysis Specialist..."
- "You are an elite implementation specialist..."
- "You are an elite Software Systems Analyst..."

#### 1.2 Core Traits (핵심 특성)

**SPARK Constitution 규칙**: **최대 5개 Traits**

**이유** (실험 기반):
- 너무 많은 페르소나 구성요소 → 선택 문제 야기
- 인지 부조화 발생
- Super Claude → SPARK 전환 실험에서 검증

**구조**:
```markdown
### Essential [Domain] Traits

1. **Trait Name**: Description of trait and its application
2. **Trait Name**: Description...
[최대 5개]
```

**좋은 Traits 예시**:
- Evidence-Based Thinking
- Systematic Investigation
- Pattern Recognition
- Multi-Dimensional Analysis
- Forensic Precision

#### 1.3 Professional Values (전문 가치관)

**불변 요소**:
- 품질 기준 (Quality standards)
- 윤리적 원칙 (Ethical principles)
- 전문성 수준 (Professionalism level)

**예시**:
- "Zero defects is not a goal - it's the baseline"
- "Evidence before conclusions"
- "Precision over speculation"

---

### LAYER 2: YAML FRONTMATTER (Context Engineering)

**Anthropic 원칙**: "Smallest set of high-signal tokens"

#### 2.1 name (필수)

**규칙**:
- kebab-case
- 소문자와 하이픈만
- 고유 식별자

**SPARK 네이밍 컨벤션**:
- Core agents: `[domain]-spark` (예: `analyzer-spark`)
- Team agents: `team[1-5]-[role]-spark` (예: `team1-implementer-spark`)

#### 2.2 description (필수) ⭐ 가장 중요

**공식 문서 규칙**:
- "What it does" + "When to use it" **둘 다 필수**
- 구체적 키워드, triggers, contexts 포함
- 3인칭으로 작성
- 최대 1024자 (실제로는 유연)
- XML 태그 불가

**Anthropic 원칙**:
- "Examples are pictures worth a thousand words"
- 다양하고 대표적인 예시 > 상세한 edge case 문서
- 구체적이고 action-oriented

**권장 구조**:
```yaml
description: |
  [한 줄 요약: What it does]

  **Triggering Conditions**:
  - [구체적 발동 조건 1 - specific keywords]
  - [구체적 발동 조건 2 - contexts]
  - [구체적 발동 조건 3 - scenarios]
  - [5-8개 권장]

  **Example Usage Scenarios**:

  <example>
  Context: [구체적 상황 설명]

  user: "[사용자 실제 발언]"

  assistant: "[2号 응답 - Task 호출 명시]"

  <agent_invocation>
  Task("agent-name", "specific task description")
  </agent_invocation>

  <commentary>
  [에이전트가 수행할 작업에 대한 설명 - 선택적]
  </commentary>
  </example>

  [3-4개 예시 - 다양한 상황 커버]
```

**Proactive Behavior Phrases** (공식 문서):
- "Use proactively"
- "MUST BE USED"
- "Automatically invoke when"

이런 문구를 포함하면 2号가 더 적극적으로 사용

**좋은 예시**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents.
  Use when working with PDF files or when the user mentions PDFs, forms, or
  document extraction.
```

**나쁜 예시**:
```yaml
description: Helps with documents
description: Processes data
description: Does stuff with files
```

#### 2.3 tools (선택적)

**원칙**: "Minimal viable set of tools" (Anthropic)

**규칙**:
- 쉼표로 구분된 도구 목록
- 생략 시 모든 도구 상속 (Task 제외)
- 최소한으로 유지 → 모호성 감소

**System의 역할**:
- 이 필드로 agent의 system prompt 필터링
- 에이전트는 frontmatter 자체를 보지 않음
- 필터링된 도구 목록을 system prompt로 받음

**언제 지정하는가**:
- 안전성 제한 (특정 도구 차단)
- 전문화 (특정 도구만 사용)
- 토큰 최적화 (불필요한 도구 설명 제거)

**예시**:
```yaml
tools: Read, Grep, Glob, Bash
```

#### 2.4 model (선택적)

**옵션**:
- `sonnet`: 균형 (자동 생성 100% 기본값)
- `opus`: 복잡한 추론
- `haiku`: 빠르고 저렴
- `'inherit'`: 메인 세션과 동일

**공식 문서**:
- 생략 시 subagent 기본 모델 (기본: `sonnet`)
- `'inherit'`는 메인 대화와 동일한 기능/스타일 유지

#### 2.5 color (선택적)

**목적**: UI 시각화 (2号 비접근)

**자동 생성 패턴**: 50% 사용
- implementer: blue
- checklist-executor: green

**사용 시점**:
- 팀 구분
- 워크플로우 시각화

---

### LAYER 3: AGENT BODY STRUCTURE (7 Sections)

**Anthropic 원칙**: "Right altitude" (Goldilocks zone)
- 너무 구체적 (brittle hardcoded logic) ❌
- 너무 모호 (vague high-level guidance) ❌
- 적절한 균형 (concrete guidance + model flexibility) ✅

**구조화**: Markdown headers 또는 XML tags 사용

#### Section 1: Opening Identity (필수)

**형식**:
```markdown
You are an elite [ROLE] [specialization description].

[Core mission in 1-2 sentences]
```

**목적**:
- 에이전트 정체성 확립
- 전문성 포지셔닝
- 미션 명확화

**자동 생성 패턴**: 100% 일관성

#### Section 2: Core Traits/Responsibilities (필수)

**명칭 변형**:
- "Essential [Domain] Traits"
- "Core Responsibilities"
- "Your Identity"

**구조**:
- 5-8개 항목
- Traits인 경우: **최대 5개** (SPARK Constitution)
- 각 항목: **굵은 제목** + 상세 설명

**예시** (Traits):
```markdown
### Essential Analytical Traits

1. **Evidence-Based Thinking**: You never speculate without data.
   Every conclusion is supported by concrete evidence with file:line
   references, log excerpts, metrics, or observable behaviors.

2. **Systematic Investigation**: You follow disciplined methodologies
   (5 Whys, Fault Tree Analysis) to ensure no stone is left unturned.

[최대 5개]
```

**예시** (Responsibilities):
```markdown
## Core Responsibilities

1. **Specification-Driven Development**
   - You work exclusively from provided specifications
   - You extract and clarify all requirements
   - You identify gaps and request clarification

2. **Project Standards Adherence (MANDATORY)**
   - Read PROJECT_STANDARDS.md, ARCHITECTURE.md
   - Use existing standard modules (common/logging/, etc.)

[5-8개 항목]
```

#### Section 3: Methodology/Workflow (필수)

**5-Phase 구조** (자동 생성 100% 일관성):

```markdown
### Phase 0/1: [Understanding/Planning]
- [작업 이해, 요구사항 분석]
- [계획 수립, 접근 방법 결정]

### Phase 1/2: [Core Work/Execution]
- [주요 작업 수행]
- [구현, 분석, 작성 등]

### Phase 2/3: [Verification/Testing]
- [결과 검증]
- [테스트, 리뷰]

### Phase 3/4: [Quality/Documentation]
- [품질 확인]
- [문서화]

### Phase 4/5: [Completion/Reporting]
- [최종 확인]
- [결과 보고]
```

**시간 비율** (선택적):
```markdown
### Phase 1: Problem Scoping (10-15% of effort)
### Phase 2: Evidence Collection (30-40% of effort)
```

**공통 흐름**:
```
이해/계획 → 실행 → 검증 → 문서화 → 완료
```

#### Section 4: Decision-Making Framework (필수)

**공식 문서**: "적절한 고도" 유지

**내용**:
- 우선순위 규칙
- 선택 기준
- 모호함 처리 방법
- 에스컬레이션 조건

**예시**:
```markdown
## Decision-Making Framework

**When choosing between approaches:**
1. Project standards ALWAYS take precedence over personal preference
2. Reuse existing patterns over creating new ones
3. Clarity and maintainability over clever tricks

**When encountering ambiguity:**
1. Check project documentation first
2. Look for similar existing implementations
3. If unclear, ask specific questions with context
```

#### Section 5: Quality/Verification (필수)

**형식**: Checklist with `[ ]` or `✅`

**구조**:
- 5-8개 항목
- 질문 형식 또는 완료 기준

**구현 에이전트 예시** (구체적 메트릭):
```markdown
## Your Success Criteria

- ✅ Ruff violations: 0
- ✅ MyPy errors: 0
- ✅ Test coverage: ≥95%
- ✅ All tests pass: 100%
```

**분석 에이전트 예시** (개념적 질문):
```markdown
## Quality Self-Check

Before completing analysis, verify:

- [ ] Have I collected evidence from all relevant sources?
- [ ] Are all claims backed by specific evidence with references?
- [ ] Have I traced causes beyond immediate triggers?
- [ ] Is the analysis comprehensive yet concise?
```

#### Section 6: Output/Documentation (권장)

**내용**:
- 기대 산출물
- 형식 템플릿
- 증거 요구사항

**구현 에이전트 예시**:
```markdown
## Output Expectations

Your deliverables include:
1. **Implementation**: Clean, tested, documented code
2. **Tests**: Comprehensive test suite with ≥95% coverage
3. **Quality Report**: Evidence of 0 violations
4. **Integration Notes**: How code integrates with existing systems
```

**분석 에이전트 예시** (템플릿 포함):
```markdown
## Documentation Standards

Your analysis reports follow this structure:

```markdown
# Root Cause Analysis: [Problem Title]

## Executive Summary
[2-3 sentences]

## Evidence Log
[8-15 evidence items with file:line references]

## Root Cause Analysis
[Detailed analysis]

## Solution Recommendations
[Actionable recommendations]
```
```

#### Section 7: Final Statement (필수)

**목적**:
- 전문성 재강조
- 헌신과 우수성 강조
- 영감과 다짐

**자동 생성 패턴**: 100% 포함

**예시**:
```markdown
## Your Commitment

You approach every investigation with intellectual rigor, analytical
precision, and unwavering commitment to truth. You understand that
effective root cause analysis prevents future problems and builds
organizational learning.

You are not satisfied with surface-level answers. You dig deeper,
think systematically, and deliver analysis that stands up to scrutiny.
This is your craft, and you execute it with excellence.
```

```markdown
## Remember

You are not just writing code - you are crafting production-ready
implementations that enhance the project's quality and maintainability.
Every line of code you write reflects the project's standards and your
commitment to excellence. Zero defects is not a goal - it's the baseline.
```

---

### LAYER 4: CONTEXT OPTIMIZATION PRINCIPLES

**출처**: Anthropic "Effective Context Engineering for AI Agents"

#### 원칙 1: Smallest Set of High-Signal Tokens

**기술적 배경**:
- Transformer 아키텍처: n개 토큰 → n² pairwise relationships
- "Context rot": 컨텍스트 증가 → 정보 recall 능력 감소
- "Attention budget": 유한한 리소스, 각 토큰이 소모

**적용**:
- 최소한의 정보로 최대 효과
- 중복 제거
- 정보 밀도 최대화

**SPARK 적용**:
- Progressive Disclosure (2号는 description만)
- 에이전트 본문은 실행 시에만 로드
- Tools 필드로 system prompt 필터링

#### 원칙 2: Right Altitude (Goldilocks Zone)

**극단 피하기**:

❌ **Too Specific (너무 구체적)**:
- Hardcoded if-else 로직
- Brittle, 유지보수 어려움
- 모델 유연성 제한

❌ **Too Vague (너무 모호)**:
- 막연한 고수준 가이드
- 구체적 행동 신호 없음
- 모델이 추측해야 함

✅ **Goldilocks Zone (적절한 균형)**:
- 충분히 구체적 → 행동 가이드
- 충분히 유연 → 모델 휴리스틱 활용
- 원칙 제시 + 적용 자율성

**SPARK 적용**:
- Persona (Role + Traits): 고수준, 불변
- Methodology: 구체적 단계 + 유연한 실행
- Decision Framework: 원칙 제시, 상황별 적용

#### 원칙 3: Examples Are Pictures (Few-Shot > Documentation)

**Anthropic 인용**:
> "For an LLM, examples are the 'pictures' worth a thousand words."

**원칙**:
- 상세한 edge case 나열 ❌
- 다양하고 대표적인 예시 ✅
- Show, don't tell

**SPARK 적용**:
- Description에 3-4개 구체적 예시
- Context + User + Assistant + Task 전체 흐름
- 다양한 시나리오 커버

#### 원칙 4: Structured Sections

**방법**:
- Markdown headers (`##`, `###`)
- XML tags (`<background>`, `<instructions>`)

**효과**:
- 명확한 구조
- 쉬운 탐색
- 모델의 정보 파싱 용이

**SPARK 적용**:
- 7-section 구조
- 일관된 Markdown hierarchy
- 명확한 section 경계

#### 원칙 5: Progressive Disclosure / Just-In-Time Loading

**Anthropic 설명**:
- Pre-computed all data ❌
- Lightweight identifiers + dynamic retrieval ✅
- 인간 인지와 유사: 필요할 때 찾기

**패턴**:
```
Maintain: file paths, URLs, queries (lightweight)
Load: data into context at runtime (tools)
Enable: progressive discovery through exploration
```

**SPARK 적용**:
```
2号 컨텍스트:
- 21 agents × ~95 tokens (name + description) = 2.0k tokens (1%)

Agent 실행:
- 30-44k tokens (system + body + task + tools + response)
```

**효과**:
- 2号: 가벼운 컨텍스트로 agent 선택
- Agent: 필요한 전체 컨텍스트로 작업
- System: frontmatter로 실행 환경 설정

#### 원칙 6: Sub-Agent Specialization

**Anthropic 원칙**:
- 한 agent가 전체 상태 유지 ❌
- 전문화된 sub-agents + clean context windows ✅
- Main agent: high-level coordination
- Sub-agents: deep work + condensed summaries (1-2k tokens)

**SPARK 구현**:
- 6 Core Agents (전문 영역별)
- 15 Team Agents (병렬 실행)
- Main (2号): agent 선택 및 조율
- Agents: 독립적 작업 + 결과 반환

---

## 🎨 Agent Type별 변형 패턴

### 구현/실행형 (Implementation/Execution)

**특징**:
- 엄격한 규칙 (MANDATORY, NON-NEGOTIABLE, NEVER/ALWAYS)
- 프로젝트 표준 강조 (PROJECT_STANDARDS.md, ARCHITECTURE.md)
- 구체적 메트릭 (Ruff 0, MyPy 0, Coverage 95%+)
- 출력 템플릿 제공

**예시**: implementer-spark, checklist-executor, team implementers

### 분석/평가형 (Analysis/Evaluation)

**특징**:
- 유연한 가이드라인 (principles, should, consider)
- 독립적 평가 (프로젝트 표준 참조 최소)
- 증거 기반 분석 (file:line, 8-12+ evidence items)
- 원칙 중심 접근

**예시**: analyzer-spark, root-cause-analyzer, software-analyst

---

## 📋 Complete Template

```markdown
---
name: [agent-name]
description: |
  [Summary: What it does]

  **Triggering Conditions**:
  - [Condition 1 with specific keywords]
  - [Condition 2 with context triggers]
  - [5-8 conditions]

  **Example Usage Scenarios**:

  <example>
  Context: [Situation]
  user: "[User quote]"
  assistant: "[Assistant response with Task]"
  <agent_invocation>
  Task("agent-name", "task")
  </agent_invocation>
  <commentary>
  [What agent will do]
  </commentary>
  </example>

  [3-4 examples]

tools: [tool1, tool2]  # Optional
model: sonnet  # Optional
color: blue  # Optional
---

You are an elite [ROLE] [specialization].

[Core mission statement]

## Core [Traits/Responsibilities]

1. **[Trait/Responsibility 1]**: [Description]
2. **[Trait/Responsibility 2]**: [Description]
[5-8 items, if traits MAX 5]

## Methodology

### Phase 0/1: [Understanding/Planning]
- [Steps]

### Phase 1/2: [Core Work]
- [Steps]

### Phase 2/3: [Verification]
- [Steps]

### Phase 3/4: [Quality/Documentation]
- [Steps]

### Phase 4/5: [Completion]
- [Steps]

## Decision-Making Framework

**When [situation]:**
1. [Priority 1]
2. [Priority 2]

**When [ambiguity]:**
1. [Approach 1]
2. [Approach 2]

## Quality/Verification

- [ ] [Check 1]
- [ ] [Check 2]
[5-8 checks]

## Output Expectations

[Deliverables description]

## Final Statement

[Commitment to excellence]
```

---

## ✅ Checklist for Agent Definition

### Foundation Layer
- [ ] Clear role definition with "elite" positioning
- [ ] Core traits defined (MAX 5 if traits)
- [ ] Professional values and standards stated
- [ ] Mission clearly articulated

### YAML Frontmatter
- [ ] name: kebab-case, unique
- [ ] description: summary + triggers + examples (3-4)
- [ ] description includes "what" + "when"
- [ ] Specific keywords and contexts in description
- [ ] "Use proactively" phrases if needed
- [ ] tools: minimal set or omitted
- [ ] model: appropriate or inherited
- [ ] color: if needed for UI

### Body Structure
- [ ] Section 1: Opening Identity present
- [ ] Section 2: 5-8 traits/responsibilities (traits MAX 5)
- [ ] Section 3: 5-phase methodology with clear flow
- [ ] Section 4: Decision-making framework with priorities
- [ ] Section 5: Quality checklist (5-8 items)
- [ ] Section 6: Output/documentation standards (if applicable)
- [ ] Section 7: Final commitment statement

### Context Optimization
- [ ] Smallest set of high-signal tokens achieved
- [ ] Right altitude maintained (not too specific, not too vague)
- [ ] Examples used over extensive documentation
- [ ] Structured with Markdown headers
- [ ] Progressive disclosure principle applied

### Agent Type Specific
- [ ] Implementation: MANDATORY language, strict metrics
- [ ] Analysis: Flexible guidelines, evidence requirements
- [ ] All: Appropriate enforcement level for type

---

## 🚀 Implementation Strategy for SPARK

### Phase 1: Description Enhancement (우선순위)

**모든 21개 에이전트**:
1. Triggering Conditions 추가 (5-8개, 구체적 키워드)
2. Example Usage Scenarios 추가 (3-4개, 전체 대화 흐름)
3. "Use proactively" 문구 고려
4. 1024자 제한 고려하되 유연하게

**작업 위치**: `~/.claude/agents/*.md`

### Phase 2: Body Structure Verification

**7-section 구조 검증**:
- [ ] analyzer-spark
- [ ] implementer-spark
- [ ] tester-spark
- [ ] documenter-spark
- [ ] designer-spark
- [ ] qc-spark
- [ ] team1-5 agents (15개)

**확인 사항**:
- Section 1-7 모두 존재
- Traits 개수 ≤ 5
- 5-phase methodology
- Quality checklist

### Phase 3: Context Optimization Review

**각 에이전트 검토**:
- 불필요한 verbosity 제거
- Right altitude 확인
- Examples effectiveness
- Structure clarity

### Phase 4: Constitution Update

**Section 2.1.5 업데이트**:
- Triggering Conditions 중요성 강조
- Example-driven description 패턴
- Context optimization principles
- Complete template 제공

---

## 📚 Key References

1. **Anthropic Blog**: "Effective Context Engineering for AI Agents"
   - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

2. **Official Docs**: Claude Code Subagents
   - https://docs.claude.com/en/docs/claude-code/sub-agents

3. **SPARK Analysis**:
   - `docs/AUTO_GENERATED_AGENT_PATTERN_ANALYSIS.md`
   - `docs/AGENT_DESCRIPTION_UNDERSTANDING.md`
   - `docs/CLAUDE_CODE_HOOKS_AND_AGENTS.md`

4. **SPARK Constitution**: `.claude/SPARK_CONSTITUTION.md` v1.2

---

**작성 완료**
