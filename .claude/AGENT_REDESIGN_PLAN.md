# SPARK Agent Redesign Plan v2.0

**날짜**: 2025-10-29
**작성자**: 2호 (Claude Code)
**목적**: 5개 Core Agents 재설계를 통한 SPARK v4.3 시스템 정제
**기반**: Constitution v1.1 원칙 + analyzer-spark v2.0 성공 패턴

---

## 📋 목차

1. [핵심 발견: 전문가 에이전트란 무엇인가?](#1-핵심-발견-전문가-에이전트란-무엇인가)
2. [역할 분담: Three-Layer Architecture](#2-역할-분담-three-layer-architecture)
3. [현황 분석](#3-현황-분석)
4. [재설계 전략](#4-재설계-전략)
5. [작업 계획](#5-작업-계획)

---

## 1. 핵심 발견: 전문가 에이전트란 무엇인가?

### 1.1 전문가의 정의

각 에이전트는 **특정 분야의 전문가**로 정의됩니다:

| 에이전트 | 분야 전문가 | 핵심 작업 |
|---------|------------|----------|
| **analyzer-spark** | 시스템 분석 | 코드베이스 다각도 분석, 문제점/개선점 발견 |
| **implementer-spark** | 소프트웨어 구현 | 요구사항을 견고한 코드로 전환 + 테스트 |
| **tester-spark** | 소프트웨어 테스팅 | 95%+ 커버리지, 모든 엣지케이스 검증 |
| **designer-spark** | 시스템 아키텍처 | 확장 가능, 안전, 비즈니스 만족 설계 |
| **documenter-spark** | 기술 문서화 | 다양한 청중을 위한 명확하고 완전한 문서 |
| **qc-spark** | 품질 관리 | 품질 위반사항 체계적 발견 및 제거 |

### 1.2 전문가의 작업 흐름

**Jason의 분석 프로세스** (2025-10-28 대화):
> "저라면 분석 대상을 인식하고, 어느 정도의 분석이 이루어져야 할 지 판단하고, 어떤 분석방법을 쓸지 고민할거에요. 그게 정해지면 분석방법에 따른 작업을 하고, 결과를 보며, 결과를 해석 할 거에요. **그걸 충분한 답이 나올때까지 반복**한 후에..."

**일반화된 전문가의 작업 흐름**:
```
1. 대상 인식     → 무엇을 다루는가?
2. 깊이 판단     → 어느 수준까지?
3. 방법 선택     → 어떻게 접근할까?
4. 작업 실행     → 방법론에 따라 수행
5. 결과 관찰     → 무엇이 나왔나?
6. 해석          → 의미는 무엇인가?
7. 충분성 판단   → 더 필요한가?
   ├─ Yes → 4번으로 (반복)
   └─ No  → 보고
```

**핵심**: 전문가는 **기계적이 아니라 적응적**이다. 고정된 체크리스트가 아니라 **professional judgment**로 작업한다.

### 1.3 Common Protocol vs Task-Specific

#### Common Protocol (에이전트 정의에 포함)

**수정된 표현**:
- ❌ "모든 분석 작업에 적용되는 보편적 프로토콜"
- ✅ **"분석(구현/테스트/설계/문서화/QC)의 전문가들이 공통적으로 가지고 있는 프로토콜"**

**의미**:
- 각 분야마다 다르지만, **그 분야 내에서는 공통적**
- Proven methodology, field-specific best practice
- Community of practice의 shared knowledge

**분야별 공통 프로토콜 예시**:
- **분석 전문가들**: Evidence-based practice, Systematic scanning, Pattern recognition, Risk assessment
- **구현 전문가들**: Foundation-first approach, TDD, Incremental development, Structural integrity
- **테스트 전문가들**: Test pyramid (70/20/10), Coverage-driven, Edge case focus, Skepticism
- **설계 전문가들**: User-centric design, Scalability-first, Long-term thinking, Risk mitigation
- **문서화 전문가들**: Audience analysis, Progressive disclosure, Example-driven, Empathy
- **QC 전문가들**: Zero tolerance, Systematic inspection, Manual precision, Persistence

#### Task-Specific Instructions (2호가 제공)

**각 작업마다 2호가 지시하는 특성**:
- **범위** (scope): 어디까지 다룰 것인가?
- **깊이** (depth): 얼마나 깊이?
- **시간** (time): 제약사항?
- **초점** (focus): 특히 중요한 것?
- **우선순위** (priority): 무엇을 먼저?
- **제약사항** (constraints): 기술스택, 리소스 등
- **맥락** (context): 왜 이 작업? 이전 단계는?

**실제 예시** (analyzer-spark on code-laundry, 2025-10-28):
```
Task("analyzer-spark", """
작업: 코드베이스 품질 분석
대상: /Users/jason/Projects/code-laundry
시간: 15분 이내
깊이: 표면적 스캔 (구조, 설정, 명백한 문제)
초점: Python 중심 (다른 언어는 간단히)
결과: 3-5개 대표 예시 + 우선순위
""")
```

**전문가의 해석**:
- "15분" → 깊이 들어가지 말고 빠르게 스캔
- "표면적" → 파일 구조, 설정 파일, 명백한 문제 중심
- "Python 중심" → .py 파일 우선, 다른 언어는 간단히
- "3-5개 예시" → 모든 문제 나열 말고 대표적인 것만

**그리고 전문가는 미처 고려 못한 것도 알아서**:
- TODO 항목 53개 발견 (지시에 없었지만 중요)
- Architecture 문제 지적
- 우선순위 P1/P2/P3로 분류

→ 이게 **진짜 전문가**!

### 1.4 전문가에게 필요한 Traits

**Traits의 역할** (Constitution v1.1 Section 2.5):
> Traits create cognitive immersion for natural professional judgment
> - NOT for decoration
> - FOR enabling natural professional behavior

**각 에이전트별 핵심 Traits**:

**analyzer-spark**:
- Systems Thinking: 개별 컴포넌트가 아니라 전체 시스템 이해
- Evidence-Based Practice: 모든 주장에 file:line 증거
- Skepticism: "버그가 있다"고 가정
- Pattern Recognition: 반복 패턴 발견

**implementer-spark**:
- Systematic Execution: 방법론적 접근
- Simplicity-First: 단순하고 명확한 솔루션
- Attention to Detail: 엣지케이스, 에러 처리
- Structural Integrity: 아키텍처 준수

**tester-spark**:
- Attention to Detail: 미묘한 버그 발견
- Analytical Reasoning: 체계적 분해
- Systematic Execution: Test pyramid 준수
- Skepticism: 버그 존재 가정

**designer-spark**:
- Long-Term Thinking: 3-5년 진화 고려
- Abstraction Ability: 복잡함을 단순 모델로
- Systems Thinking: 전체 최적화
- User-Centric: 사용자 경험 우선
- Risk Assessment: 위험 사전 식별

**documenter-spark**:
- Clear Communication: 복잡한 개념을 명확하게
- Knowledge Structuring: 논리적 정보 구조
- User-Centric: 독자 관점
- Empathy: 초보자와 전문가 모두 배려

**qc-spark**:
- Zero Tolerance: 모든 위반 제거
- Systematic Methodology: 5-phase 체계적 검사
- Manual Precision: 자동화 금지, 수작업
- Persistence: "따박따박 꾸역꾸역" 끝까지

**핵심**: Traits는 "무엇을 하는가"가 아니라 **"어떻게 생각하는가"**를 정의한다.

### 1.5 반드시 지켜야 할 규칙 (Rules)

**각 에이전트별 절대 규칙**:

**analyzer-spark**:
- ✅ MUST: file:line 형식 증거 (12+ items)
- ✅ MUST: EVIDENCE-BEFORE-REPORT
- ❌ NEVER: 증거 없는 주장

**implementer-spark**:
- ✅ MUST: Phase 4에서 pytest 실행 (TEST-BEFORE-REPORT)
- ✅ MUST: Ruff 0, MyPy 0, Coverage 95%+
- ❌ NEVER: 자동화 스크립트 (sed, awk, --fix)로 대량 수정
- ❌ NEVER: 테스트 없이 "완료" 보고

**tester-spark**:
- ✅ MUST: 95% unit, 85% integration coverage
- ✅ MUST: 실제 pytest 실행 (TEST-EXECUTION-BEFORE-REPORT)
- ✅ MUST: Test pyramid (70/20/10)
- ❌ NEVER: 테스트 작성만 하고 실행 안 함

**designer-spark**:
- ✅ MUST: 확장성, 보안, 성능 고려
- ✅ MUST: Validation criteria 충족
- ❌ NEVER: Vendor lock-in

**documenter-spark**:
- ✅ MUST: 100% API coverage
- ✅ MUST: 예시 코드가 실제 작동 (VALIDATION-BEFORE-REPORT)
- ❌ NEVER: 검증 안 된 예시 코드

**qc-spark**:
- ✅ MUST: Violations = 0 달성
- ✅ MUST: Manual fix only (하나씩)
- ❌ NEVER: 자동화 스크립트

**공통 규칙**:
1. Quality gates MUST pass
2. Evidence/Test/Validation BEFORE report
3. NEVER automated bulk fixes
4. Zero tolerance for violations

### 1.6 전문가에게 추가로 필요한 것

1. **Communication skill**: 결과를 명확하게 보고
2. **Tool knowledge**: 자기 분야 도구 숙지
3. **Quality awareness**: 품질 기준 인지
4. **Collaboration awareness**: 다른 전문가와 협업
5. **Self-validation**: 자기 작업 검증
6. **Escalation judgment**: 언제 에스컬레이션할지
7. **Context understanding**: 2호의 지시 해석
8. **Proactive thinking**: 지시에 없어도 중요하면 포함

**핵심**: 전문가는 **독립적으로 작업하지만 전체 시스템의 일부**임을 안다.

---

## 2. 역할 분담: Three-Layer Architecture

### 2.1 시스템 구조

```
┌──────────────────────────────────────────────────┐
│        SPARK Constitution v1.1 (원칙)            │
│  - Phase flexibility                             │
│  - Common protocol vs task-specific              │
│  - Traits drive behavior                         │
│  - Professional judgment over checklists         │
└──────────────────────────────────────────────────┘
                        │
                모든 것이 따름
                        ▼
┌──────────────────────────────────────────────────┐
│           CLAUDE.md (2호의 가이드북)              │
│  - Agent catalog (21 agents)                     │
│  - ⭐ Orchestration guide (강화 필요!)            │
│  - ⭐ Information passing (추가 필요!)            │
│  - ⭐ State management (추가 필요!)               │
│  - ⭐ Context continuity (추가 필요!)             │
└──────────────────────────────────────────────────┘
              │                          │
          참조 │                          │ 참조
              ▼                          ▼
┌──────────────────────┐      ┌──────────────────────┐
│  Agent Definitions   │      │  Custom Commands     │
│   (전문가의 정체성)   │      │    (보조 도구)        │
│                      │      │                      │
│  - Traits            │      │  - Pre-check         │
│  - Common protocol   │      │  - Execution guide   │
│  - Methodology       │      │  - Post-validate     │
│  - Rules             │      │  - State update      │
└──────────────────────┘      └──────────────────────┘
              │                          │
           실행 │                          │ 실행 보조
              └─────────┬────────────────┘
                        ▼
                  ┌──────────┐
                  │   2호    │
                  │(Director)│
                  └──────────┘
                        │
                   결과 보고
                        ▼
                     Jason
```

### 2.2 Layer 1: Agent Definitions (전문가의 정체성)

**파일 위치**: `.claude/agents/xxx-spark.md`

**포함할 내용**:
```markdown
# Frontmatter
- name, description, tools, model, color

## Core Identity & Traits (Natural Language Persona)
- 그 분야 전문가의 사고방식 (4-5 traits)
- 왜 이런 traits를 가지는가?
- Traits가 어떻게 행동을 유도하는가?

## Behavior Protocol (Code-Based Rules)
- 반드시 지켜야 할 규칙 (MUST, NEVER)
- 품질 기준 (Coverage targets, Validation criteria)
- Escalation rules (언제 더 높은 수준으로?)
- Tool usage (언제 어떤 도구?)

## Professional Methodology
- Phase 0: Task Understanding
  - "2호 provides task-specific guidance" 명시
  - 범위, 깊이, 우선순위 해석 방법
- Phase 1-N: Domain work (flexible, not fixed at 5)
  - Iteration expected
  - Professional judgment
  - "Sufficient" not "complete"
- Phase N+1: Quality Validation
  - Self-check
  - Quality gates call (간단히)

## Communication Protocol
- 어떤 형식으로 보고?
- 필수 증거/데이터
- 다음 전문가에게 넘길 것
```

**제외할 내용** (중요!):
- ❌ 2호 orchestration 로직 (designer-spark Lines 637-830 같은 것)
- ❌ Multi-session 구체적 구현 (principle만 언급)
- ❌ 교육적 예시 과다 (PROTOCOL sections 200+ lines)
- ❌ Template 전체 (간단한 예시만)
- ❌ Phase 5B의 quality gates 실행 상세 (호출만)

**목표 라인 수**: ~400-600 lines (전문성 유지하면서 간결)

**성공 사례**: analyzer-spark v2.0
- Before: 1,290 lines (bloated)
- After: 500 lines (focused)
- 61% 감소, but 전문성은 더 강화됨!

### 2.3 Layer 2: CLAUDE.md (2호의 가이드북)

**파일 위치**: `CLAUDE.md` (프로젝트 루트)

**현재 내용** (~400 lines):
- ✅ Project overview (SPARK v4.3)
- ✅ Core commands
- ✅ Architecture & Execution Flow
- ✅ Token Management
- ✅ JSON State Management
- ✅ Agent Specialization

**추가/강화 필요**:

#### 2.3.1 Information Passing to Agents (NEW!)

```markdown
## 2호 Orchestration Guide

### Information Passing to Agents

에이전트에게 정보를 전달하는 표준 형식:

\`\`\`python
Task("agent-name", f"""
작업: {clear_objective}
대상: {target_scope}
제약사항:
  - 시간: {time_constraint}
  - 깊이: {depth_level}
  - 기술스택: {tech_stack}
초점: {focus_areas}
우선순위: {priorities}
맥락: {previous_phase_summary}
""")
\`\`\`

**필수 정보**:
1. 작업 목표 (what)
2. 작업 범위 (where)
3. 제약사항 (constraints)
4. 초점 (focus)
5. 결과 형식 (expected output)
6. 맥락 (context from previous phases)
```

#### 2.3.2 State Management Protocol (NEW!)

```markdown
### State Management Protocol

**프로젝트 상태 추적**:
- `~/.claude/workflows/project_state.yaml`: 전체 프로젝트 진행
- `.claude/artifacts/phase_{name}/`: 각 Phase 산출물
- `.claude/decision_log.md`: 주요 결정 기록
- `~/.claude/workflows/current_task.json`: 현재 작업 상태

**2호의 책임**:
1. 각 에이전트 작업 전: 관련 맥락 로드
2. 각 에이전트 작업 후: 결과 기록
3. 프로젝트 전체 흐름 관리
```

#### 2.3.3 Quality Verification Checklist (NEW!)

```markdown
### Quality Verification Checklist

에이전트 완료 후 2호가 반드시 확인:

\`\`\`python
import json
workflow_dir = os.path.expanduser("~/.claude/workflows")
task_file = os.path.join(workflow_dir, "current_task.json")

with open(task_file, 'r') as f:
    state = json.load(f)

# ✅ 모든 조건 확인
assert state["quality"]["violations_total"] == 0
assert state["quality"]["can_proceed"] == True
assert state["state"]["status"] == "completed"

# Phase-specific checks
if agent == "implementer-spark":
    assert state["tests"]["passed"] > 0
    assert state["tests"]["failed"] == 0
elif agent == "tester-spark":
    assert state["coverage"]["unit"] >= 0.95
    assert state["coverage"]["integration"] >= 0.85
# ... (에이전트별 추가 검증)
\`\`\`
```

#### 2.3.4 Context Continuity (NEW!)

```markdown
### Context Continuity

**새 세션 시작 시**:
1. Load `project_state.yaml`
2. Read recent `decision_log.md` entries
3. Load relevant artifacts from previous phases
4. Summarize context for next agent

**예시**:
\`\`\`python
# Session 2 시작
project_state = load_yaml("~/.claude/workflows/project_state.yaml")

if project_state["last_phase"] == "analysis":
    analysis_results = load_artifact("phase_analysis/analysis_report.md")

    Task("designer-spark", f"""
    작업: {feature_name} 시스템 설계
    분석 결과 요약: {summarize(analysis_results)}
    주요 발견: {analysis_results["key_findings"]}
    제약사항: {analysis_results["constraints"]}
    """)
\`\`\`
```

#### 2.3.5 Agent Chain Patterns (NEW!)

```markdown
### Agent Chain Patterns

**Analysis → Design**:
- 분석 결과 요약 전달
- 발견된 제약사항 명시
- 우선순위 반영

**Design → Implementation**:
- 설계 문서 경로 제공
- 아키텍처 제약사항
- API 명세 참조

**Implementation → Testing**:
- 구현된 코드 위치
- 변경된 파일 목록
- 테스트해야 할 시나리오

**Testing → Documentation**:
- 테스트 결과 (pass count, coverage)
- 발견된 엣지케이스
- API 사용 예시
```

### 2.4 Layer 3: Custom Commands (보조 도구)

**파일 위치**: `.claude/commands/spark-*.md`

**현재 상태**: 단순히 에이전트 체인만 정의
```markdown
1. Task("implementer-spark", user_request)
2. Wait
3. Validate
```

**개선된 구조**:

```markdown
# /spark-implement - Feature Implementation Pipeline

## Purpose
체계적인 feature 구현 (implementer → tester → documenter chain)

## Pre-execution Checklist (2호가 준비할 것)
1. [ ] 요구사항 명확화:
   - What: 무엇을 구현?
   - Why: 왜 필요?
   - Constraints: 기술스택, 시간, 리소스

2. [ ] 이전 맥락 로드:
   - 관련 분석 결과
   - 설계 문서

3. [ ] `current_task.json` 초기화

## Phase 1: Implementation

\`\`\`python
Task("implementer-spark", f"""
작업: {feature_name} 구현
요구사항: {detailed_requirements}
제약사항:
  - 기술스택: {tech_stack}
  - 아키텍처: {architecture_constraints}
우선순위: {priority_order}
설계 참조: {design_doc_path}
""")
\`\`\`

### Validation (2호가 확인):
- [ ] `state.status == "completed"`
- [ ] `quality.violations_total == 0`
- [ ] Tests executed and passed
- [ ] Implementation artifacts saved

## Phase 2: Testing
[Similar structure]

## Phase 3: Documentation
[Similar structure]

## Post-execution (2호가 기록)
1. Update `project_state.yaml`
2. Record in `decision_log.md`
3. Archive artifacts
4. Report to Jason
```

**커스텀 명령어의 역할**:
- ❌ NOT: 필수 경로 (2호가 직접 호출도 가능)
- ✅ YES: 자주 쓰는 패턴의 단축키
- ✅ YES: 2호를 위한 체크리스트
- ✅ YES: 작업 효율성 향상
- ✅ YES: Orchestration 보조

---

## 3. 현황 분석

### 3.1 에이전트별 현황

| 에이전트 | 라인 수 | 주요 문제 | 우선순위 |
|---------|---------|----------|---------|
| **designer-spark** | 829 | ⚠️ **치명적**: 2호 orchestration 193 lines (Lines 637-830) | 🔴 1순위 |
| **documenter-spark** | 975 | 가장 큼, VALIDATION protocol 예상 | 🟡 2순위 |
| **implementer-spark** | 808 | Multi-session 106 lines, TEST protocol 188 lines | 🟢 3순위 |
| **tester-spark** | 847 | Multi-session 32 lines, TEST-EXECUTION protocol 258 lines | 🟢 4순위 |
| **qc-spark** | 429 | 큰 문제 없음, 이미 간결 | 🟢 5순위 |
| **합계** | **3,888** | | |

### 3.2 공통 문제점

#### 문제 1: Multi-Session 구현 상세 (100+ lines)
**문제**: 모든 에이전트에 구체적 구현 코드
- implementer-spark: Lines 139-244 (106 lines)
- tester-spark: Lines 89-120 (32 lines)
- designer-spark: Lines 157-186 (30 lines)

**해결**: Principle만 언급 (analyzer-spark 패턴)
```markdown
## Multi-Session Capability

For large-scale analysis that may span multiple sessions:
- Can break work into logical phases
- Saves progress to state file
- Resumes from saved state
- Accumulates findings progressively

(구체적 구현 제거)
```

#### 문제 2: PROTOCOL Sections (150-250 lines)
**문제**: 교육적 예시가 너무 많음
- implementer-spark: TEST-BEFORE-REPORT (188 lines)
- tester-spark: TEST-EXECUTION-BEFORE-REPORT (258 lines)
- documenter-spark: VALIDATION-BEFORE-REPORT (예상 200+ lines)

**해결**: 핵심만, 예시 최소화
```markdown
## TEST-BEFORE-REPORT Protocol

**Rule**: Cannot report "complete" without test execution evidence.

**Required Evidence**:
- Test results: X/X passed
- Coverage: Unit X%, Integration X%
- Quality: Ruff 0, MyPy 0

(Bad/Good examples 제거, 핵심만)
```

#### 문제 3: Phase 5B Quality Gates 실행 로직
**문제**: Orchestration 로직 (2호가 할 일)
- 모든 에이전트에 40-70 lines의 실행 상세

**해결**: 간단히 호출만
```python
def phase_5b_quality_gates():
    """Execute quality gates - MUST pass."""
    result = subprocess.run([
        "python3", "~/.claude/hooks/spark_quality_gates.py"
    ], ...)

    if "Quality gates PASSED" in result.stdout:
        return True
    else:
        # Fix issues and retry
        return phase_5b_quality_gates()
```

#### 문제 4: 2호 지시사항 (designer-spark만!)
**문제**: Lines 637-830 (193 lines) - 완전히 잘못된 위치!
```markdown
## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-design COMMAND:**
[193 lines of orchestration logic]
```

**해결**: **완전 삭제**, CLAUDE.md로 이동

### 3.3 성공 사례: analyzer-spark v2.0

**Before** (2025-10-27):
- 1,290 lines
- Multi-session 구현 상세 (481 lines)
- EVIDENCE-BEFORE-REPORT protocol (196 lines)
- Educational content (119 lines)

**After** (2025-10-28):
- 500 lines (61% 감소)
- Multi-session principle만 (60 lines)
- EVIDENCE protocol 핵심만
- Educational content 제거

**결과**:
- ✅ 더 명확한 전문가 정체성
- ✅ 실전 테스트 성공 (code-laundry)
- ✅ Task-specific instructions 잘 해석
- ✅ Proactive thinking (TODO 53개 발견)

---

## 4. 재설계 전략

### 4.1 우선순위별 작업 계획

#### 🔴 우선순위 1: designer-spark (가장 심각)

**현재**: 829 lines
**목표**: ~500 lines

**삭제할 내용**:
- Lines 637-830 (193 lines): **2호 orchestration 로직 완전 삭제**
  - "2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL"
  - Multi-session orchestration for 2호
  - Validation enforcement code for 2호
  - Design validation requirements
  - All 2호 instructions

**간소화할 내용**:
- Lines 157-186 (30 lines): Token safety protocol → principle만
- Lines 462-538 (77 lines): Phase 5B quality gates → 간단히
- Lines 540-590 (51 lines): Documentation template → 제거

**유지할 내용**:
- Core Identity & Traits (강력함)
- Behavior Protocol (good)
- Professional methodology (Phases)

#### 🟡 우선순위 2: documenter-spark (가장 큼)

**현재**: 975 lines
**목표**: ~600 lines

**예상 문제**:
- VALIDATION-BEFORE-REPORT protocol (250+ lines 예상)
- Multi-session support
- Audience adaptation 상세 구현

**작업**:
1. 파일 전체 읽기
2. analyzer-spark 패턴 적용
3. VALIDATION protocol 핵심만

#### 🟢 우선순위 3: implementer-spark

**현재**: 808 lines
**목표**: ~500 lines

**삭제/간소화**:
- Lines 139-244 (106 lines): Multi-session → principle만
- Lines 620-808 (188 lines): TEST-BEFORE-REPORT → 핵심만
- Lines 41-123 (83 lines): FORBIDDEN patterns → 핵심 3-4개만

**강화**:
- Traits 더 명확히
- Professional judgment 강조

#### 🟢 우선순위 4: tester-spark

**현재**: 847 lines
**목표**: ~500 lines

**삭제/간소화**:
- Lines 89-120 (32 lines): Multi-session → principle만
- Lines 591-848 (258 lines): TEST-EXECUTION protocol → 핵심만
- Lines 450-562 (113 lines): Critical rules, protocols → 간소화

#### 🟢 우선순위 5: qc-spark (양호)

**현재**: 429 lines
**목표**: ~450 lines (큰 변경 없음)

**작업**:
- Constitution v1.1 원칙 적용 (flexible phases)
- 이미 간결하므로 큰 수정 불필요

### 4.2 공통 재설계 패턴

**모든 에이전트에 적용**:

1. **Multi-Session**: Principle만, 구체적 구현 제거
2. **PROTOCOL Sections**: 핵심만, 예시 최소화
3. **Phase 5B**: 간단히 호출만
4. **Educational Content**: 제거
5. **Templates**: 간단한 예시만
6. **Flexible Phases**: "Phase count is flexible" 명시
7. **Iteration**: "Iteration expected" 명시
8. **Professional Judgment**: "Professional judgment over checklists" 강조
9. **Task-Specific**: "2호 provides task-specific guidance" Phase 0에 명시

### 4.3 에이전트 정의 표준 구조

```markdown
---
name: xxx-spark
description: [50-100 words]
tools: [relevant tools]
model: sonnet
color: [color]
---

# Introduction
[2-3 sentences about this professional's role]

## Core Identity & Traits (Natural Language Persona)

[4-5 traits with rich descriptions]

**Trait 1:** [How this shapes behavior...]

**Trait 2:** [How this drives decisions...]

## Behavior Protocol (Code-Based Rules)

\`\`\`python
class AgentBehavior:
    """Concrete rules that MUST be followed."""

    # Quality requirements
    QUALITY_REQUIREMENTS = {...}

    # Validation criteria
    VALIDATION_CRITERIA = {...}

    # Critical rules
    def must_do(self):
        # ...

    def never_do(self):
        # ...
\`\`\`

## Professional Methodology

### Phase 0: Task Understanding
**Key Principle**: 2호 will provide task-specific guidance on scope,
depth, priorities, and constraints. Interpret these thoughtfully.

### Phase 1-N: Domain Work
[Flexible, not fixed at 5]
**Iteration**: Expected to cycle between phases as understanding deepens.
**Judgment**: Work until "sufficient", not "complete".

### Phase N+1: Quality Validation
- Self-check against quality requirements
- Execute quality gates (call only, not implement)
- Record results

## Communication Protocol

[How to report results]
[Required evidence format]
[What to hand off to next professional]

## Multi-Session Capability (Optional)

For large-scale work:
- Can break into logical phases
- Saves progress
- Resumes from state
(No detailed implementation)

---

Remember: You are defined by your traits. These drive your professional
judgment and natural behavior. The behavior protocol isn't optional -
it's mandatory. Quality isn't negotiable - it's the minimum standard.
```

**목표 라인 수**: 400-600 lines

---

## 5. 작업 계획

### 5.1 작업 방식

**옵션 A: 순차적 (안전)**
```
designer → test → documenter → test → implementer → test → ...
```
- 장점: 매 단계 검증, 안전
- 단점: 시간 더 걸림

**옵션 B: 일괄 재설계 후 테스트 (효율적)** ⭐ 추천
```
5개 모두 재설계 → 통합 테스트 → 수정 → 최종 커밋
```
- 장점: 빠름, 일관성
- 단점: 문제 발견 시 여러 개 동시 수정

**추천 이유**:
- analyzer-spark로 패턴 확립됨
- 문제점 명확히 파악됨
- 일관성 있게 적용 가능

### 5.2 작업 순서

```
1. designer-spark 재설계 (2호 로직 193 lines 삭제!)
   └─ 가장 심각한 문제 우선 해결

2. documenter-spark 재설계 (가장 큼)
   └─ analyzer 패턴 적용

3. implementer-spark 재설계
   └─ TEST-BEFORE-REPORT 간소화

4. tester-spark 재설계
   └─ TEST-EXECUTION protocol 간소화

5. qc-spark 재설계
   └─ Constitution 원칙 적용

6. 통합 테스트
   ├─ 각 에이전트 실전 테스트
   └─ 에이전트 체인 테스트 (/spark-implement)

7. CLAUDE.md 강화
   ├─ Orchestration guide 추가
   ├─ Information passing 추가
   ├─ State management 추가
   └─ Context continuity 추가

8. 커스텀 명령어 개선 (선택적)
   └─ 보조 기능 강화

9. 최종 검증 및 커밋
```

### 5.3 검증 기준

**각 에이전트별**:
1. ✅ Traits가 명확하고 행동을 유도하는가?
2. ✅ Common protocol이 명확한가?
3. ✅ Rules가 구체적인가?
4. ✅ Phase가 flexible한가? (not fixed at 5)
5. ✅ Iteration이 허용되는가?
6. ✅ Professional judgment 강조되는가?
7. ✅ "2호 provides task-specific" 명시되는가?
8. ✅ 2호 orchestration 로직 없는가?
9. ✅ Multi-session principle만 있는가?
10. ✅ 목표 라인 수 달성? (400-600 lines)

**통합 테스트**:
1. ✅ 실제 프로젝트에서 작동하는가?
2. ✅ Task-specific instructions 잘 해석하는가?
3. ✅ Proactive thinking 보이는가?
4. ✅ Quality gates 통과하는가?
5. ✅ 에이전트 체인이 작동하는가?

### 5.4 예상 결과

| 지표 | 현재 | 목표 | 개선 |
|------|------|------|------|
| **전체 라인 수** | 3,888 | ~2,550 | -34% |
| **토큰 소비** | ~15K | ~10K | -33% |
| **평균 라인/에이전트** | 778 | ~510 | -34% |
| **Multi-session** | 구현 상세 | Principle만 | 명확화 |
| **Orchestration** | Agent 안에 | CLAUDE.md로 | 분리 |
| **Phase 유연성** | 고정 5-Phase | 유연 적응 | 개선 |
| **전문성** | 혼재 | 명확 | 강화 |

**핵심**: 라인 수 감소는 **부수적 결과**. 진짜 목표는 **"전문가 수준"** 달성.

### 5.5 완료 기준

**개별 에이전트**:
- [ ] Constitution v1.1 원칙 모두 적용
- [ ] 2호 orchestration 로직 제거
- [ ] Multi-session principle만
- [ ] PROTOCOL 핵심만
- [ ] 목표 라인 수 달성
- [ ] 실전 테스트 통과

**전체 시스템**:
- [ ] 5개 에이전트 모두 재설계 완료
- [ ] CLAUDE.md 강화 완료
- [ ] 통합 테스트 통과
- [ ] Git commit & push
- [ ] Constitution v1.1 + Redesign Plan 문서화

---

## 6. 결론

### 6.1 핵심 발견 요약

1. **전문가의 본질**: 특정 분야에서 공통 프로토콜을 가진 전문가
2. **Common vs Task-Specific**: 에이전트는 공통, 2호는 특성
3. **Flexible Workflow**: Phase 고정 아님, 적응적
4. **Professional Judgment**: 체크리스트 아닌 판단
5. **Traits Drive Behavior**: 장식 아닌 행동 원동력
6. **Three-Layer Clear**: Agent / CLAUDE.md / Commands 역할 명확
7. **Not Complex, Clear**: 복잡한 게 아니라 명확함

### 6.2 기대 효과

**단기 효과**:
- 34% 토큰 절감
- 에이전트 정체성 명확화
- 2호 orchestration 가이드 확보

**장기 효과**:
- 새 에이전트 추가 용이
- 전문성 지속적 개선
- 프로젝트 맥락 유지
- 품질 일관성 보장

### 6.3 다음 단계

1. Jason 승인 받기
2. 재설계 시작 (designer-spark부터)
3. 각 단계마다 검증
4. 최종 통합 테스트
5. 문서화 및 커밋

---

**문서 버전**: v2.0
**최종 수정**: 2025-10-29
**상태**: Jason 검토 대기 중
