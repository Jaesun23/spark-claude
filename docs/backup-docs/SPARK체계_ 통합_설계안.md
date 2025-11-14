# 🎯 SPARK 체계 통합 설계안

## CLAUDE.md, Agents, Commands의 역할 구분과 상호보완

### 📐 핵심 설계 원칙

1. #### Single Source of Truth
- 각 정보는 정확히 한 곳에만 존재
- 중복 = 불일치 가능성 = 제거 대상

2. #### Progressive Disclosure
- 2호: 가벼운 정보로 선택 (descriptions)
- 실행: 필요한 정보만 로드 (agent body, command)

3. #### Separation of Concerns
- CLAUDE.md: HOW (방법론)
- Agents: WHO & WHAT (정체성 & 작업)
- Commands: WHEN & ORDER (시점 & 순서)

4. #### Independence & Complementarity
- 각 요소는 독립적으로 작동 가능
- 함께 사용시 상호 보완



# 📋 Three-Layer Architecture

## LAYER 1: CLAUDE.md (2호의 Orchestration Manual)

### 목적: 2호가 에이전트를 "어떻게 사용하는가"

#### 포함할 내용:

✅ 2호 Identity & Relationships (유지)
✅ 2호의 4가지 역할 (Companion, Direct Worker, Team Leader, Quality Guardian)
✅ 작업 위임 결정 트리 (시간, 복잡도, 전문성 기준)
✅ Agent Portfolio - 간소화:
   **Core Specialists (6)**: analyzer, implementer, tester, documenter, designer, qc
   **Team Agents (15)**: 5 teams × 3 roles (parallel execution)

   See each agent's description for capabilities.

✅ Agent Delegation Protocol
   - Context 제공 방법
   - PROJECT_STANDARDS.md 참조 지시
   - 명확한 작업 명세 작성법

✅ State Management (JSON 파일 관리)
✅ Quality Verification (에이전트 완료 후 체크)
✅ 재시도 전략 (1-3차 실패 대응)
✅ Agent Chain Patterns (일반적 패턴)

#### 제거할 내용:

❌ 각 에이전트의 프로토콜 세부사항 (EVIDENCE-BEFORE-REPORT 등)
   → Agent description으로 이동

❌ 전문성 나열 (5-Phase Wave, file:line 등)
   → Agent description/body로 이동

❌ 사용시점 세부 설명
   → Agent description의 Triggering Conditions로 이동

#### 예시 - 개선 전후:

##### 개선 전:

**analyzer-spark** - Multi-dimensional system analysis

- 프로토콜: EVIDENCE-BEFORE-REPORT + PROJECT-CONTEXT-DISCOVERY
- 전문성: 5-Phase Wave, file:line 증거 수집, 12+ evidence items
- 사용시점: 시스템 분석, 성능 병목, 보안 감사, 기술 부채 평가

##### 개선 후:

```
## 🤖 SPARK Agent Portfolio

**Core Specialists (6)**: analyzer, implementer, tester, documenter, designer, qc
**Team Agents (15)**: 5 teams × 3 roles for parallel execution

Each agent's description contains detailed triggering conditions and capabilities.
```



## LAYER 2: Agent Definitions (전문가의 Identity)

목적: "나는 누구이고 무엇을 어떻게 하는가"

필수 구조:

Frontmatter (YAML)

---
name: agent-name                    # kebab-case, 고유

description: |                      # ⭐ 가장 중요! 2호가 언제 어떻게 이 에이전트를 사용할 것인지 지침이 됨
[한 줄 요약: What this agent does]

  **Triggering Conditions**:

  - [구체적 발동 조건 1 - specific keywords]
  - [구체적 발동 조건 2 - contexts]
  - [구체적 발동 조건 3 - scenarios]
  - [5-8개 조건]

  **Example Usage Scenarios**:

  <example>
  Context: [구체적 상황]
  user: "[사용자 발언]"
  assistant: "[2호 응답 및 Task 호출]"
  <agent_invocation>
  Task("agent-name", "specific task")
  </agent_invocation>
  </example>

  [3-4개 다양한 예시]

tools: [minimal set]                # 선택적
model: sonnet                       # 선택적
color: blue                         # 선택적

------

Body (7 Sections)

1. Opening Identity
   - "You are an elite [ROLE]..."
   - Core mission statement

2. Core Traits (≤5) or Responsibilities (5-8)
   - **Trait 1**: Description
   - **Trait 2**: Description
   - [Constitution: Traits 최대 5개]

3. Methodology (5-Phase 권장)
   - Phase 0/1: Understanding/Planning
   - Phase 1/2: Core Work
   - Phase 2/3: Verification
   - Phase 3/4: Quality/Documentation
   - Phase 4/5: Completion

4. Decision-Making Framework
   - 우선순위 규칙
   - 선택 기준
   - 모호함 처리 방법

5. Quality/Verification Checklist
   - [ ] Check 1
   - [ ] Check 2
   - [5-8개 항목]

6. Output Expectations (권장)
   - 산출물 형식
   - 템플릿 (선택적)

7. Final Statement
   - Commitment to excellence

------

Description 작성 가이드:
- "Use this agent when..." + "Triggering Conditions" + "Examples"
- 구체적 키워드 포함 (2호의 패턴 매칭용)
- 3-4개 현실적인 사용 시나리오
- "Use proactively" 문구 고려 (적극적 사용 유도)

---
## LAYER 3: Custom Commands (복잡한 워크플로우 레시피)

### 목적: 특정 multi-agent 워크플로우의 구체적 실행 지침

필수 구조:

Frontmatter

---
name: command-name
description: Command purpose
type: command
requires: [agent1, agent2, agent3]  # 선택적

------

Body

1. Purpose Statement
   - 이 커맨드의 목적과 가치

2. Decision Framework
   - 상황별 의사결정 기준
   - Quality vs Velocity balance
   - 우선순위 판단

3. Design Principles
   - Workflow 원칙
   - 품질 기준
   - 진행 규칙

4. Workflow Architecture
   - 시각적 흐름도
   - 에이전트 순서
   - 검증 지점

5. Execution Protocol ⭐
   - PHASE 1: [Agent] 호출
     * Task("agent", "task")
     * JSON 체크 조건
     * 성공 기준
     * 실패시 재시도
   - PHASE 2: [Agent] 호출
     * ...
   - PHASE N: 완료

6. Examples
   - 사용 예시
   - 기대 결과

------


Command가 필요한 경우:

- ✅ 2개 이상 에이전트 순차 실행
- ✅ Phase별 다른 검증 조건
- ✅ 복잡한 조건부 로직
- ✅ CLAUDE.md에 적기엔 너무 구체적인 내용

Command가 불필요한 경우:
- ❌ 단일 에이전트 호출 (직접 Task로 충분)
- ❌ 간단한 순차 작업 (2호가 판단 가능)

---
🔗 상호 작용 패턴

시나리오 1: 단순 작업

User: "파일 읽어줘"
2호: CLAUDE.md 참조 → Read 도구 직접 사용

시나리오 2: 단일 전문 작업

User: "시스템 성능 분석해줘"
2호:
  1. CLAUDE.md 참조 (delegation protocol)
  2. Agent descriptions 스캔 → analyzer-spark 매칭
  3. Task("analyzer-spark", "성능 분석")
Analyzer: Agent definition 로드 → 독립 실행

시나리오 3: 복잡한 워크플로우

User: "/spark-implement 새 기능"
2호:
  1. CLAUDE.md 참조 (general orchestration)
  2. spark-implement command 로드
  3. Command protocol 따라 실행:
     - Task("implementer-spark") → JSON verify
     - Task("tester-spark") → JSON verify
     - Task("documenter-spark") → JSON verify
     각 Agent: 독립적으로 실행

시나리오 4: 병렬 실행

User: "/multi-implement task1,task2,task3"
2호:
  1. CLAUDE.md 참조 (parallel protocol)
  2. multi-implement command (선택적)
  3. 동시에 Task 호출:
     - Task("team1-implementer-spark", task1)
     - Task("team2-implementer-spark", task2)
     - Task("team3-implementer-spark", task3)

---
✅ 검증 체크리스트

정보 중복 검증

Q: "이 정보가 두 곳 이상에 있는가?"
→ YES: Single Source of Truth 위반 → 통합
→ NO: 적절한 위치 확인

역할 경계 검증

CLAUDE.md 테스트:
- ✅ "이것이 2호의 orchestration 방법인가?" → 유지
- ❌ "이것이 에이전트 능력 설명인가?" → Agent로 이동

Agent Definition 테스트:
- ✅ "이것이 에이전트의 정체성/방법론인가?" → 유지
- ❌ "이것이 2호의 사용법인가?" → CLAUDE.md로 이동

Command 테스트:
- ✅ "복잡한 multi-step 워크플로우인가?" → 유지
- ❌ "단순한 단일 작업인가?" → 불필요, 삭제

독립성 검증

- ✅ 에이전트 definition만으로 작동 가능한가?
- ✅ CLAUDE.md 없이도 에이전트 호출 가능한가?
- ✅ Command 없이도 기본 작업 가능한가?

---
🚀 적용 로드맵

Phase 1: CLAUDE.md 간소화

1. Line 125-169 (Agent Registry) 간소화
2. 에이전트 세부사항 제거
3. 간단한 portfolio로 교체

Phase 2: Agent Descriptions 강화

1. 21개 모든 에이전트 description 재작성
2. Triggering Conditions 추가 (5-8개)
3. Example Scenarios 추가 (3-4개)

Phase 3: Agent Body 검증

1. 7-section 구조 확인
2. Traits ≤ 5 확인
3. 5-Phase methodology 확인

Phase 4: Commands 표준화

1. 기존 12개 commands 구조 검증
2. Execution Protocol 보강
3. 불필요한 commands 제거

---
