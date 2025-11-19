# Claude Code 주요 기능 - DNA 방법론 적용 가이드

**작성일**: 2025-11-19
**목적**: Claude Code의 주요 기능을 DNA 방법론에 적용하기 위한 기술 문서
**출처**: Claude Code 공식 문서 (https://code.claude.com/docs)

---

## 1. 개요

### 1.1 Claude Code 주요 기능

| 기능 | 역할 | DNA 적용 |
|-----|-----|---------|
| **Subagents** | 전문화된 AI 어시스턴트 | Stage 1-4 에이전트 |
| **Slash Commands** | 커스텀 명령어 | Stage 진입점 |
| **Agent Skills** | 자동 발견되는 모듈 | Validator, Knowledge |
| **Hooks** | 이벤트 기반 스크립트 | 검증, Context 관리 |
| **MCP** | 외부 도구 연동 | 이미 활용 중 |

### 1.2 핵심 발견

1. **Subagent의 독립 컨텍스트** = Context Rot 방지의 핵심
2. **Skills의 자동 발견** = Executable Protocol 구현
3. **Hooks의 UserPromptSubmit** = Context Re-ranking
4. **파일 형식은 모두 Markdown** (.md)

---

## 2. Subagents

### 2.1 기본 정보

**저장 위치**:
- 프로젝트: `.claude/agents/*.md`
- 사용자: `~/.claude/agents/*.md`

**파일 구조**:
```markdown
---
name: subagent-name
description: 사용 시기 설명
tools: Read, Write, Grep, Glob  # 선택사항
model: sonnet  # 선택사항 (sonnet/opus/haiku/inherit)
skills: skill1, skill2  # 선택사항
---

System prompt 내용
(역할, 지침, 체크리스트, 제약사항)
```

### 2.2 핵심 특징

- **독립 컨텍스트**: 각 subagent는 별도의 컨텍스트 윈도우 → Context Rot 방지!
- **도구 제한**: `tools` 필드로 필요한 도구만 허용
- **자동 위임**: Claude가 description 기반으로 적절한 에이전트 선택
- **Resumable**: 이전 세션 재개 가능 (장기 분석에 유용)

### 2.3 DNA 적용

**Stage 1 에이전트 예시** (`system-classifier-spark.md`):

```markdown
---
name: system-classifier-spark
description: 시스템 특성을 분석하여 18가지 패밀리 중 하나로 분류합니다.
  아이디어나 비즈니스 요구사항을 분석할 때 사용합니다.
tools: Read, Write, WebSearch, Grep, Glob
model: sonnet
skills: architecture-patterns, verify-stage1
---

## Role
You are a System Classifier with the following traits:
- **Pattern Matching**: 18가지 패밀리 조합과 매칭
- **Evidence-Based**: 모든 주장에 검증 사례 필수
- **Ambiguity Intolerance**: 모호하면 반드시 되묻기
- **Benchmark Obsession**: 구체적 수치 요구

## Task
1. Layer 1 질문 (Q1, Q2, Q3) 분석
2. 18가지 조합 중 패턴 매칭
3. 검증 사례 2개 이상 인용
4. NFR 초안 도출

## Self-Validation Checklist
- [ ] L1-Q1, Q2, Q3 모두 답변됨
- [ ] 각 답변에 구체적 근거 있음 (3-5문장)
- [ ] 유사 사례 2개 이상 (회사명 + 시스템명 + 수치)
- [ ] 18가지 중 하나와 정확히 일치
- [ ] 신뢰도 평가 및 근거 명시

## Output Format
반드시 docs/context/stage1_output.json 형식으로 저장
```

### 2.4 호출 방법

**자동 위임**:
```
사용자: "주식 거래 플랫폼의 아키텍처 패밀리를 분류해줘"
→ Claude가 자동으로 system-classifier-spark 선택
```

**명시적 호출**:
```
사용자: "system-classifier-spark 에이전트로 이 아이디어를 분석해줘"
```

---

## 3. Slash Commands

### 3.1 기본 정보

**저장 위치**:
- 프로젝트: `.claude/commands/*.md`
- 사용자: `~/.claude/commands/*.md`

**파일 구조**:
```markdown
---
description: 명령어 설명
allowed-tools: Read, Write, Bash(git:*)
argument-hint: [인자1] [인자2]
model: claude-3-5-haiku-20241022
---

프롬프트 내용
```

### 3.2 핵심 기능

**변수**:
- `$ARGUMENTS`: 모든 인자
- `$1`, `$2`: 위치 기반 인자

**동적 콘텐츠**:
- `!command`: bash 명령 실행 및 출력 포함
- `@file`: 파일 내용 참조

### 3.3 DNA 적용

**Stage 1 명령어** (`stage1.md`):

```markdown
---
description: Stage 1 - 시스템 분류 및 패밀리 결정
allowed-tools: Read, Write, WebSearch, Grep, Glob
argument-hint: [아이디어 설명]
---

## Context Loading
현재 프로젝트 컨텍스트:
@docs/context/project_init.json

## Task
system-classifier-spark 에이전트를 사용하여 다음 아이디어를 분석합니다:

**아이디어**: $ARGUMENTS

## Expected Output
- 패밀리 결정 (A-A-B 형식)
- Layer 1 분석
- NFR 초안
- 검증 사례

결과는 docs/context/stage1_output.json에 저장합니다.
```

**사용**:
```bash
> /stage1 주식 거래 플랫폼을 만들고 싶습니다. 자동매매 기능이 핵심입니다.
```

---

## 4. Agent Skills

### 4.1 기본 정보

**저장 위치**:
- 프로젝트: `.claude/skills/skill-name/SKILL.md`
- 사용자: `~/.claude/skills/skill-name/SKILL.md`

**디렉토리 구조**:
```
skill-name/
├── SKILL.md          # 필수
├── reference.md      # 문서
├── scripts/          # 스크립트
│   └── validate.py
└── templates/        # 템플릿
    └── output.json
```

### 4.2 핵심 특징

- **자동 발견**: 사용자가 명시적으로 호출하지 않아도 Claude가 자동 선택
- **복잡한 워크플로우**: 여러 파일과 스크립트 포함 가능
- **도구 제한**: `allowed-tools` 필드로 접근 제어

### 4.3 DNA 적용

#### Validator Skill (Executable Protocol 구현)

**verify-stage1/SKILL.md**:
```markdown
---
name: verify-stage1
description: Stage 1 산출물의 필수 항목을 검증합니다.
  패밀리 결정, 검증 사례, NFR 초안이 모두 포함되었는지 확인합니다.
allowed-tools: Read, Bash
---

## Purpose
Stage 1 완료 전 자동으로 품질 검증

## Validation Script
@scripts/validate_stage1.py를 실행하여 검증

## Checklist
- 패밀리 코드 형식 (A-A-B)
- 검증 사례 개수 >= 2
- 레이턴시 수치 명시
- NFR 우선순위 포함
```

**verify-stage1/scripts/validate_stage1.py**:
```python
#!/usr/bin/env python3
import json
import sys

def validate_stage1_output(filepath):
    with open(filepath) as f:
        data = json.load(f)

    errors = []

    # 패밀리 코드 형식 검증
    family = data.get("family", "")
    if not re.match(r"^[ABC]-[ABC]-[ABC]$", family):
        errors.append("Invalid family code format")

    # 검증 사례 개수
    cases = data.get("validation_cases", [])
    if len(cases) < 2:
        errors.append(f"Need 2+ validation cases, got {len(cases)}")

    # 레이턴시 수치
    latency = data.get("layer1_analysis", {}).get("Q3_response_time")
    if not latency:
        errors.append("Missing latency specification")

    # NFR 우선순위
    nfr = data.get("nfr_priority", [])
    if len(nfr) < 3:
        errors.append("NFR priority incomplete")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("VALIDATION PASSED")
    sys.exit(0)

if __name__ == "__main__":
    validate_stage1_output(sys.argv[1])
```

#### Knowledge Skill

**architecture-patterns/SKILL.md**:
```markdown
---
name: architecture-patterns
description: 18가지 아키텍처 패밀리 패턴과 검증 사례를 제공합니다.
  시스템 분류나 아키텍처 결정 시 참조합니다.
allowed-tools: Read
---

## 18 Families
@patterns/18_families.md

## Validation Cases
@patterns/validation_cases.md

## Layer 1 Questions
@patterns/layer1_questions.md
```

---

## 5. Hooks

### 5.1 기본 정보

**설정 위치**: `settings.json`의 `hooks` 필드

**Hook 종류**:
| Hook | 실행 시점 | DNA 용도 |
|------|----------|---------|
| PreToolUse | 도구 실행 전 | 산출물 저장 전 검증 |
| PostToolUse | 도구 실행 후 | Context Summary 업데이트 |
| UserPromptSubmit | 사용자 입력 전 | Context Re-ranking |
| SessionStart | 세션 시작 | 환경변수 설정 |

### 5.2 설정 구조

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/validate_output.py",
            "timeout": 30
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/context_reranking.py"
          }
        ]
      }
    ]
  }
}
```

### 5.3 DNA 적용

#### Context Re-ranking Hook

**~/.claude/hooks/context_reranking.py**:
```python
#!/usr/bin/env python3
"""
UserPromptSubmit Hook: 현재 Stage에 필요한 컨텍스트만 주입
"""
import json
import sys
import os

def get_current_stage():
    """현재 작업 중인 Stage 확인"""
    context_dir = "docs/context"
    if os.path.exists(f"{context_dir}/stage3_output.json"):
        return 4
    elif os.path.exists(f"{context_dir}/stage2_output.json"):
        return 3
    elif os.path.exists(f"{context_dir}/stage1_output.json"):
        return 2
    return 1

def get_relevant_context(stage):
    """해당 Stage에 필요한 컨텍스트만 추출"""
    context = {}
    context_dir = "docs/context"

    # 핵심 결정사항 (모든 Stage에서 필요)
    if os.path.exists(f"{context_dir}/stage1_output.json"):
        with open(f"{context_dir}/stage1_output.json") as f:
            stage1 = json.load(f)
            context["family"] = stage1.get("family")
            context["nfr_priority"] = stage1.get("nfr_priority")

    # Stage별 추가 컨텍스트
    if stage >= 3 and os.path.exists(f"{context_dir}/stage2_output.json"):
        with open(f"{context_dir}/stage2_output.json") as f:
            stage2 = json.load(f)
            context["constraints"] = stage2.get("constraints")

    return context

def main():
    data = json.load(sys.stdin)

    stage = get_current_stage()
    context = get_relevant_context(stage)

    # 프롬프트에 컨텍스트 추가
    if context:
        context_str = json.dumps(context, indent=2, ensure_ascii=False)
        prefix = f"""[CORE CONTEXT - 반드시 준수]
{context_str}

위 결정사항을 반드시 준수하여 작업하세요.

---

"""
        # 원본 프롬프트에 컨텍스트 추가
        output = {
            "prompt": prefix + data.get("prompt", "")
        }
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
```

#### Post-Stage Hook (Context Summary 업데이트)

**~/.claude/hooks/update_context_summary.py**:
```python
#!/usr/bin/env python3
"""
PostToolUse Hook: Stage 완료 시 Context Summary 업데이트
"""
import json
import sys
import os
from datetime import datetime

def main():
    data = json.load(sys.stdin)

    # Write 도구로 stage output을 저장했는지 확인
    tool_name = data.get("tool_name")
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if tool_name == "Write" and "stage" in file_path and "_output.json" in file_path:
        # Context Summary 업데이트
        summary_path = "docs/context/context_summary.json"

        summary = {}
        if os.path.exists(summary_path):
            with open(summary_path) as f:
                summary = json.load(f)

        # Stage 번호 추출
        stage_num = file_path.split("stage")[1].split("_")[0]

        summary["last_updated"] = datetime.now().isoformat()
        summary["completed_stages"] = summary.get("completed_stages", [])
        if stage_num not in summary["completed_stages"]:
            summary["completed_stages"].append(stage_num)

        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(json.dumps({"message": f"Context summary updated for stage {stage_num}"}))

    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## 6. MCP (Model Context Protocol)

### 6.1 현재 활용

- **Context7**: 기술 문서 조회
- **Sequential-Thinking**: 복잡한 분석
- **Time**: 시간 관련 기능

### 6.2 DNA 확장 가능성

| MCP 서버 | 용도 |
|---------|------|
| PostgreSQL | Stage 결과 영구 저장 |
| GitHub | ADR을 이슈로 등록 |
| Notion | 문서 자동 생성 |

→ 현재는 파일 기반으로 충분, 필요 시 확장

---

## 7. DNA 방법론 통합 매핑

### 7.1 전체 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                   DNA + Claude Code                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  /stage1 "아이디어"                                  │
│      │                                              │
│      ▼                                              │
│  ┌─────────────────┐                               │
│  │ Slash Command   │ docs/context/*.json 로드       │
│  │ (stage1.md)     │                               │
│  └────────┬────────┘                               │
│           │                                        │
│           ▼                                        │
│  ┌─────────────────┐                               │
│  │ Subagent        │ 독립 컨텍스트로 시작            │
│  │ (classifier)    │ Traits + Behavior Protocol    │
│  └────────┬────────┘                               │
│           │                                        │
│           ▼                                        │
│  ┌─────────────────┐                               │
│  │ Skill           │ 자동 발견, 검증 실행            │
│  │ (verify-stage1) │ Pass/Fail 리턴                │
│  └────────┬────────┘                               │
│           │                                        │
│           ▼                                        │
│  ┌─────────────────┐                               │
│  │ Hook            │ Context Summary 업데이트       │
│  │ (PostToolUse)   │ 다음 Stage 준비               │
│  └─────────────────┘                               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 7.2 Context Rot 방지 3중 방어

| 방어선 | Claude Code 구현 | 역할 |
|-------|-----------------|------|
| **1. 독립 컨텍스트** | Subagent | 대화 히스토리 의존 제거 |
| **2. Context Re-ranking** | Hook (UserPromptSubmit) | 필요한 정보만 주입 |
| **3. 파일 기반 전달** | JSON 파일 + Hook | 구조화된 데이터만 전달 |

### 7.3 Gemini 인사이트 → Claude Code 매핑

| Gemini 인사이트 | Claude Code 구현 |
|----------------|------------------|
| Executable Protocol | **Skills** (Validator scripts) |
| 파일 기반 컨텍스트 전달 | **Hooks** + JSON files |
| Context Re-ranking | **Hook** (UserPromptSubmit) |
| 추가 Traits | **Subagent** System Prompt |
| 논리적 병렬화 | **Command** + **Subagent** |

---

## 8. 파일 구조 예시

```
.claude/
├── agents/
│   ├── system-classifier-spark.md       # Stage 1
│   ├── constraints-investigator-spark.md # Stage 2
│   ├── architecture-decision-maker-spark.md # Stage 3
│   └── blueprint-designer-spark.md      # Stage 4
│
├── commands/
│   ├── stage1.md
│   ├── stage2.md
│   ├── stage3.md
│   └── stage4.md
│
├── skills/
│   ├── verify-stage1/
│   │   ├── SKILL.md
│   │   └── scripts/validate_stage1.py
│   ├── verify-stage2/
│   ├── verify-stage3/
│   ├── architecture-patterns/
│   │   ├── SKILL.md
│   │   └── patterns/
│   │       ├── 18_families.md
│   │       └── validation_cases.md
│   └── bootstrap-knowledge/
│       ├── SKILL.md
│       └── knowledge/
│           ├── rdbms.md
│           ├── cache.md
│           └── messaging.md
│
└── hooks/ (스크립트)
    ├── context_reranking.py
    ├── update_context_summary.py
    └── validate_output.py

docs/
└── context/
    ├── project_init.json
    ├── stage1_output.json
    ├── stage2_output.json
    ├── stage3_output.json
    └── context_summary.json
```

---

## 9. 다음 단계

1. **Process Flow 업데이트**: 이 문서의 내용을 반영
2. **플로우 분할**: 집중 연구를 위한 레고블럭화
3. **프로토타입 구현**: Stage 1 에이전트부터 시작

---

**작성자**: Jason & Claude (2호)
**날짜**: 2025-11-19
