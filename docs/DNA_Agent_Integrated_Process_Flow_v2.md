# DNA v4.0 에이전트 통합 프로세스 흐름도 v2

**작성일**: 2025-11-19
**작성자**: Jason & Claude (2호)
**버전**: 2.0 (Claude Code 기능 + Gemini 인사이트 반영)

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
2. **Context Rot** (문맥 부패)
3. **검증 메커니즘 부재**
4. **순차 vs 병렬 불명확**

### 1.2 해결 방향: 에이전트 시스템 + Claude Code

**Gemini 연구 보고서에서 차용**:
- Skeleton-of-Thought (SoT): 병렬 확장 구조
- Chain of Density (CoD): 점진적 상세화
- Tree of Thoughts (ToT): 다중 경로 탐색
- **Executable Protocol**: 규칙을 읽는 게 아니라 실행

**Claude Code로 구현**:
- **Subagents**: Stage별 전문화된 에이전트 (.md)
- **Slash Commands**: Stage 진입점 (/stage1)
- **Agent Skills**: Validator, Knowledge (자동 발견)
- **Hooks**: Context 관리, 검증 (자동 실행)

**에이전트 정의**:
```
에이전트 = 역할 + Traits + Behavior Protocol + Professional Workflow
         → Subagent (.md) + Skill (Validator) + Hook (Context)
```

---

## 2. 전체 프로세스 흐름도

### 2.1 High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              DNA v4.0 + Agent System + Claude Code              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Jason: /stage1 "주식 거래 플랫폼"                               │
│      │                                                          │
│      ▼                                                          │
│  ┌─────────────────────────────────┐                           │
│  │  Phase 1: 아이디어 정제 (CoD)     │  Stage 1-2               │
│  │  /stage1, /stage2               │                           │
│  │  system-classifier-spark        │                           │
│  │  constraints-investigator-spark │                           │
│  └─────────────┬───────────────────┘                           │
│                │                                                │
│                ▼                                                │
│  ┌─────────────────────────────────┐                           │
│  │  Phase 2: 아키텍처 스켈레톤       │  Stage 3-4               │
│  │  /stage3, /stage4               │                           │
│  │  architecture-decision-maker    │                           │
│  │  blueprint-designer-spark       │                           │
│  └─────────────┬───────────────────┘                           │
│                │                                                │
│                ▼                                                │
│  ┌─────────────────────────────────┐                           │
│  │  Phase 3: 환경 구축              │  Stage 5-6               │
│  │  기존 SPARK 에이전트 활용         │                           │
│  └─────────────┬───────────────────┘                           │
│                │                                                │
│                ▼                                                │
│  ┌─────────────────────────────────┐                           │
│  │  Phase 4-5: 레고블럭 + 구현       │  Stage 7-9               │
│  │  기존 SPARK 에이전트 활용         │                           │
│  └─────────────────────────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Claude Code 기능 매핑

| Claude Code 기능 | DNA 용도 | 파일 위치 |
|-----------------|---------|----------|
| **Subagents** | Stage 1-4 전문 에이전트 | `.claude/agents/*.md` |
| **Slash Commands** | Stage 진입점 | `.claude/commands/stage*.md` |
| **Agent Skills** | Validator + Knowledge | `.claude/skills/*/SKILL.md` |
| **Hooks** | Context 관리 + 검증 | `settings.json` |
| **MCP** | Context7, Sequential-Thinking | 이미 활용 중 |

### 2.3 실행 흐름 상세

```
사용자: /stage1 "주식 거래 플랫폼"
   │
   ▼
┌─────────────────────────────────────┐
│ 1. Slash Command (stage1.md)       │
│    - docs/context/*.json 참조       │
│    - 에이전트 호출 지시              │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ 2. Hook (UserPromptSubmit)         │
│    - Context Re-ranking            │
│    - 핵심 결정사항 프롬프트 상단 주입  │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ 3. Subagent (system-classifier)    │
│    - 독립 컨텍스트 시작              │
│    - Traits 기반 작업               │
│    - 산출물 작성                    │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ 4. Skill (verify-stage1) - 자동발견 │
│    - validate_stage1.py 실행        │
│    - Pass/Fail 리턴                 │
│    - Fail 시 수정 루프              │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ 5. Hook (PostToolUse - Write)      │
│    - stage1_output.json 저장        │
│    - context_summary.json 업데이트  │
└─────────────────────────────────────┘
```

---

## 3. Phase별 상세 설계

### 3.1 Phase 1: 아이디어 정제 (Stage 1-2)

**적용 기법**: Chain of Density (CoD)

#### Stage 1: System Classifier Agent

| 항목 | 내용 |
|-----|-----|
| **역할** | 18가지 패밀리 중 결정 |
| **Traits** | Pattern Matching, Evidence-Based, **Ambiguity Intolerance**, **Benchmark Obsession** |
| **입력** | Jason의 아이디어, 비즈니스 컨텍스트 |
| **출력** | 패밀리(A-A-B), Layer 1 분석, NFR 초안, 검증 사례 |
| **검증** | 모든 질문 답변됨, 검증 사례 2개 이상, 신뢰도 평가 |

**Claude Code 구현**:
- **Subagent**: `.claude/agents/system-classifier-spark.md`
- **Command**: `.claude/commands/stage1.md`
- **Skill**: `.claude/skills/verify-stage1/SKILL.md`
- **Output**: `docs/context/stage1_output.json`

**추가 Traits (Gemini 인사이트)**:
- **Ambiguity Intolerance**: 모호하면 반드시 되묻기
  - 예: "트래픽이 1만인가요 100만인가요?"
- **Benchmark Obsession**: 구체적 수치 요구
  - 예: "Netflix는 2016년 자료에 따르면..."

#### Stage 2: Constraints Investigator Agent

| 항목 | 내용 |
|-----|-----|
| **역할** | Layer 3 환경 제약 조사 |
| **Traits** | Inquisitive, Constraint-Aware, Conflict Anticipation |
| **입력** | 패밀리, NFR 초안 |
| **출력** | 기술/팀/인프라 제약, 잠재적 충돌, 해결안 |

**Claude Code 구현**:
- **Subagent**: `.claude/agents/constraints-investigator-spark.md`
- **Command**: `.claude/commands/stage2.md`
- **Skill**: `.claude/skills/verify-stage2/SKILL.md`
- **Output**: `docs/context/stage2_output.json`

---

### 3.2 Phase 2: 아키텍처 스켈레톤 (Stage 3-4)

**적용 기법**:
- Tree of Thoughts (ToT): ADR 3옵션 비교
- Skeleton-of-Thought (SoT): 논리적 병렬화
- **3-Turn 대화** (Gemini): 초안 → 반론 → 재작성

#### Stage 3: Architecture Decision Maker Agent

| 항목 | 내용 |
|-----|-----|
| **역할** | Bootstrap ADR 작성 |
| **Traits** | Trade-off Reasoning, **Devil's Advocate**, Evidence-Based |
| **입력** | 패밀리, NFR, Layer 3 제약 |
| **출력** | Bootstrap ADR 세트 (5-7개), 충돌 해결됨 |

**추가 Trait (Gemini 인사이트)**:
- **Devil's Advocate**: 자신의 선택 공격
  - 예: "Redis가 빠르지만, 데이터 유실 시 복구 시나리오는?"

**논리적 병렬화 (SoT)**:
```
Step 1: ADR_SKELETON.md 작성 (5개 ADR 목록 + 핵심 결정)
Step 2: 각 ADR을 독립적으로 상세화 (이전 ADR 컨텍스트 오염 없이)
```

**3-Turn 대화 (CoD)**:
```
Turn 1: 초안 작성
Turn 2: Devil's Advocate로 반론 제기
Turn 3: 반론 반영하여 재작성
```

**Claude Code 구현**:
- **Subagent**: `.claude/agents/architecture-decision-maker-spark.md`
- **Command**: `.claude/commands/stage3.md`
- **Skill**: `.claude/skills/verify-stage3/SKILL.md`
- **Knowledge Skill**: `.claude/skills/bootstrap-knowledge/SKILL.md`

#### Stage 4: Blueprint Designer Agent

| 항목 | 내용 |
|-----|-----|
| **역할** | Clean Architecture 청사진 작성 |
| **Traits** | Domain Modeling, Architectural Thinking, Dependency Awareness |
| **입력** | Bootstrap ADR, 도메인 요구사항 |
| **출력** | 도메인 분해, 4-Layer 설계, API 설계 |

**Claude Code 구현**:
- **Subagent**: `.claude/agents/blueprint-designer-spark.md`
- **Command**: `.claude/commands/stage4.md`
- **Skill**: `.claude/skills/verify-stage4/SKILL.md`

---

### 3.3 Phase 3-5: 환경 구축 + 레고블럭 + 구현

기존 SPARK 에이전트 활용 (implementer-spark, tester-spark, documenter-spark)

**핵심**: AI가 틀리고 싶어도 틀릴 수 없게!

```
환경 = Standards + 11 DNA Systems + 자동화 강제
```

---

## 4. Context Rot 방지: Claude Code 구현

### 4.1 3중 방어 메커니즘

| 방어선 | Claude Code 구현 | 역할 |
|-------|-----------------|------|
| **1. 독립 컨텍스트** | Subagent | 대화 히스토리 의존 제거 |
| **2. Context Re-ranking** | Hook (UserPromptSubmit) | 필요한 정보만 주입 |
| **3. 파일 기반 전달** | Hook (PostToolUse) + JSON | 구조화된 데이터만 전달 |

### 4.2 방어 1: Subagent 독립 컨텍스트

**핵심**: 각 Subagent는 별도의 컨텍스트 윈도우를 가짐

```
Stage 1 → 새 컨텍스트 시작 (대화 히스토리 없음)
Stage 2 → 새 컨텍스트 시작 (stage1_output.json만 로드)
Stage 3 → 새 컨텍스트 시작 (stage1, stage2 output만 로드)
```

**효과**: 이전 Stage의 불필요한 대화가 현재 작업을 오염시키지 않음

### 4.3 방어 2: UserPromptSubmit Hook

**역할**: 사용자 입력 전에 Context Re-ranking 자동 실행

```python
# ~/.claude/hooks/context_reranking.py
def main():
    stage = get_current_stage()
    context = get_relevant_context(stage)

    prefix = f"""[CORE CONTEXT - 반드시 준수]
Family: {context['family']}
NFR: {context['nfr_priority']}
Constraints: {context['constraints']}

위 결정사항을 반드시 준수하여 작업하세요.
---
"""
    output = {"prompt": prefix + original_prompt}
    print(json.dumps(output))
```

**설정** (settings.json):
```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/context_reranking.py"
      }]
    }]
  }
}
```

### 4.4 방어 3: PostToolUse Hook + JSON

**역할**: 산출물 저장 시 Context Summary 자동 업데이트

```python
# ~/.claude/hooks/update_context_summary.py
def main():
    if tool_name == "Write" and "stage" in file_path:
        # context_summary.json 업데이트
        summary["completed_stages"].append(stage_num)
        # 다음 Stage 입력 준비
```

**파일 구조**:
```
docs/context/
├── project_init.json      # 초기 설정
├── stage1_output.json     # Stage 1 결과
├── stage2_output.json     # Stage 2 결과
├── stage3_output.json     # Stage 3 결과
└── context_summary.json   # 전체 요약
```

### 4.5 Executable Protocol (Gemini 인사이트)

**원칙**: AI가 규칙을 "읽는" 게 아니라 "실행"하게!

**구현**: Validator Skill

```python
# .claude/skills/verify-stage1/scripts/validate_stage1.py
def validate(filepath):
    errors = []

    # 패밀리 코드 형식
    if not re.match(r"^[ABC]-[ABC]-[ABC]$", family):
        errors.append("Invalid family code")

    # 검증 사례 개수
    if len(cases) < 2:
        errors.append("Need 2+ validation cases")

    if errors:
        sys.exit(1)  # Fail → 수정 루프
    sys.exit(0)      # Pass
```

**효과**: Self-Validation 체크리스트가 실제로 검증됨

---

## 5. Gemini 인사이트 반영 요약

### 5.1 채택한 인사이트

| 인사이트 | Claude Code 구현 | 효과 |
|---------|-----------------|------|
| **Executable Protocol** | Skills (Validator) | 규칙 강제 |
| **파일 기반 컨텍스트** | Hooks + JSON | Context Rot 방지 |
| **Context Re-ranking** | UserPromptSubmit Hook | 필요한 정보만 주입 |
| **Ambiguity Intolerance** | Subagent Traits | 모호함 제거 |
| **Devil's Advocate** | Subagent Traits | 품질 향상 |
| **Benchmark Obsession** | Subagent Traits | 증거 기반 |
| **3-Turn 대화** | ADR 작성 프로세스 | 점진적 개선 |

### 5.2 보류한 항목

| 항목 | 이유 |
|-----|-----|
| 에이전트 파일 형식 (.json) | 실제는 .md |
| Skills/Hooks 구조 세부사항 | 실제와 다름 |

→ Gemini가 Claude Code 문서 숙지 후 재검토

---

## 6. 파일 구조

```
.claude/
├── agents/
│   ├── system-classifier-spark.md       # Stage 1
│   ├── constraints-investigator-spark.md # Stage 2
│   ├── architecture-decision-maker-spark.md # Stage 3
│   └── blueprint-designer-spark.md      # Stage 4
│
├── commands/
│   ├── stage1.md    # /stage1 명령어
│   ├── stage2.md    # /stage2 명령어
│   ├── stage3.md    # /stage3 명령어
│   └── stage4.md    # /stage4 명령어
│
├── skills/
│   ├── verify-stage1/
│   │   ├── SKILL.md
│   │   └── scripts/validate_stage1.py
│   ├── verify-stage2/
│   ├── verify-stage3/
│   ├── verify-stage4/
│   ├── architecture-patterns/    # 18가지 패밀리 지식
│   │   ├── SKILL.md
│   │   └── patterns/
│   └── bootstrap-knowledge/      # 기술 스택 지식
│       ├── SKILL.md
│       └── knowledge/
│
└── hooks/ (스크립트, settings.json에서 참조)
    ├── context_reranking.py
    └── update_context_summary.py

docs/
└── context/
    ├── project_init.json
    ├── stage1_output.json
    ├── stage2_output.json
    ├── stage3_output.json
    └── context_summary.json
```

---

## 7. 다음 단계: 집중 연구 계획

### 7.1 연구 계획 개요

전체 플로우를 독립 실행 가능한 레고블럭 단위로 분할:

| 세션 | 범위 | 예상 시간 | 의존성 |
|-----|-----|----------|-------|
| **세션 0** | Context 관리 시스템 | 2-3시간 | 없음 (기반) |
| **세션 1** | Stage 1 에이전트 | 3-4시간 | 세션 0 |
| **세션 2** | Stage 2 에이전트 | 2-3시간 | 세션 0, 1 |
| **세션 3** | Stage 3 에이전트 | 4시간 | 세션 0, 1, 2 |
| **세션 4** | Stage 4 에이전트 | 3시간 | 세션 0, 1-3 |
| **세션 5** | 통합 테스트 및 검증 | 3-4시간 | 세션 0-4 |

**총 예상 시간**: 17-21시간 (3일)

### 7.2 상세 연구 계획

각 세션별 상세 체크리스트, 산출물, 검증 기준은 다음 문서를 참조:

> **`docs/research/DNA_Agent_Research_Plan.md`**

### 7.3 실행 원칙

**DNA v4.0 레고블럭 전략 적용**:
- 각 세션이 독립 실행 가능
- 그 세션 문서만 보고 작업 완료 가능
- Context Rot 방지: 필요한 정보만 로드

---

## 8. 참조 문서

- `20251119_Claude_Code_Features_for_DNA.md`: Claude Code 주요 기능 상세
- `20251119_Gemini_Agent_Design_Insights.md`: Gemini 인사이트 정리
- `DNA_Agent_System_Design_for_Gemini_Review.md`: 1호 의견 (세부 질문)
- `DNA_ALL_GUIDES_MERGED.md`: 현재 DNA v4.0 전체 가이드

---

**작성자**: Jason & Claude (2호)
**날짜**: 2025-11-19
**버전**: 2.0
