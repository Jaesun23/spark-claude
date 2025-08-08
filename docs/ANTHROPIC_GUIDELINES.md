# 📘 Anthropic Claude Code 가이드라인 핵심 요약

> **Claude Code Hooks, Slash Commands, Subagents 구현을 위한 필수 가이드라인**
> 
> *이 문서는 Anthropic 공식 문서를 기반으로 작성되었으며, 모든 SPARK 시스템 구현 시 반드시 준수해야 합니다.*

## 🎯 목적
- Hook, Slash Commands, Subagents 구현 시 Anthropic 표준 준수
- 존재하지 않는 기능 사용으로 인한 오류 방지
- 올바른 JSON 형식과 Exit Code 사용 보장
- 보안 모범 사례 적용

---

## 📌 Hook System 핵심 가이드라인

### ✅ 존재하는 Hook 이벤트 (7개만)
```json
{
  "hooks": {
    "PreToolUse": [...],        // 도구 실행 전
    "PostToolUse": [...],       // 도구 실행 후  
    "UserPromptSubmit": [...],  // 사용자 프롬프트 제출 시
    "Stop": [...],              // Claude 응답 완료 직전
    "SubagentStop": [...],      // 서브에이전트 응답 완료 직전
    "PreCompact": [...],        // 대화 압축 전
    "SessionStart": [...],      // 세션 시작/재개 시
    "Notification": [...]       // 알림 전송 시
  }
}
```

### ❌ 존재하지 않는 Hook 이벤트 (절대 사용 금지)
- `subagentStart` ❌
- `toolUse` ❌ 
- `userPromptComplete` ❌
- `assistantResponse` ❌
- `lifecycleStart` ❌
- `taskComplete` ❌

### 🏗️ 올바른 Hook 구조
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",  // PreToolUse, PostToolUse, PreCompact만 해당
        "description": "Hook 설명",  // 선택사항
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script1.py",
            "timeout": 60  // 선택사항, 기본값 60초
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script2.py"
            // 같은 훅 안에 여러 커맨드 가능
          }
        ]
      },
      {
        "description": "추가 검증 레이어",  // 같은 이벤트에 여러 훅 가능
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script3.py"
          }
        ]
      }
    ]
  }
}
```

### 📊 Hook Exit Code 동작
| Exit Code | 동작 |
|-----------|------|
| **0** | 성공. stdout은 transcript 모드에서 표시 (UserPromptSubmit, SessionStart는 context에 추가) |
| **2** | 차단. stderr를 Claude에게 전달하여 자동 처리 |
| **기타** | 비차단 오류. stderr를 사용자에게만 표시하고 계속 진행 |

### 🔧 Hook별 Exit Code 2 동작
| Hook Event | Exit Code 2 동작 |
|------------|------------------|
| `PreToolUse` | 도구 호출 차단, stderr를 Claude에게 표시 |
| `PostToolUse` | stderr를 Claude에게 표시 (도구는 이미 실행됨) |
| `UserPromptSubmit` | 프롬프트 처리 차단, 프롬프트 삭제, stderr를 사용자에게만 표시 |
| `Stop` | 중단 차단, stderr를 Claude에게 표시 |
| `SubagentStop` | 중단 차단, stderr를 서브에이전트에게 표시 |
| `PreCompact` | 압축 차단 |
| `SessionStart` | 영향 없음, stderr를 사용자에게만 표시 |
| `Notification` | 영향 없음, stderr를 사용자에게만 표시 |

### 📋 고급 JSON 출력 형식

#### 공통 JSON 필드
```json
{
  "continue": true,           // Claude 계속 실행 여부 (기본: true)
  "stopReason": "문자열",     // continue가 false일 때 사용자에게 표시
  "suppressOutput": true      // stdout을 transcript에서 숨김 (기본: false)
}
```

#### PreToolUse 전용 필드
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "결정 이유 (사용자에게 표시)"
  }
}
```

#### UserPromptSubmit 전용 필드
```json
{
  "decision": "block" | undefined,
  "reason": "차단 이유",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit", 
    "additionalContext": "추가할 컨텍스트"
  }
}
```

#### SubagentStop 전용 필드
```json
{
  "decision": "block" | undefined,
  "reason": "계속해야 하는 이유 (필수)"
}
```

---

## 🚀 Slash Commands 핵심 가이드라인

### 📁 파일 위치 및 우선순위
1. **프로젝트 명령어**: `.claude/commands/` (높은 우선순위)
2. **사용자 명령어**: `~/.claude/commands/` (낮은 우선순위)

### 📝 올바른 파일 구조
```markdown
---
allowed-tools: Tool1, Tool2, Tool3
argument-hint: [arg1] [arg2]
description: 명령어 설명
model: sonnet
---

# 명령어 내용

$ARGUMENTS 플레이스홀더 사용 가능

## Bash 명령어 실행 (선택사항)
- Current status: !`git status`
- File contents: @src/file.js
```

### 🔑 Frontmatter 필드
| 필드 | 필수 | 설명 |
|------|------|------|
| `allowed-tools` | 아니오 | 사용 가능한 도구 목록 (없으면 상속) |
| `argument-hint` | 아니오 | 자동완성을 위한 인수 힌트 |
| `description` | 아니오 | 명령어 설명 (없으면 첫 줄 사용) |
| `model` | 아니오 | 사용할 모델 (없으면 상속) |

### ⚠️ 중요 규칙
- **파일명 = 명령어명**: `optimize.md` → `/optimize`
- **네임스페이싱**: `frontend/component.md` → `/frontend:component`
- **인수 전달**: `$ARGUMENTS` 플레이스홀더 사용
- **Bash 실행**: `!` 접두사로 명령어 실행 (allowed-tools에 Bash 필요)
- **파일 참조**: `@` 접두사로 파일 내용 포함

---

## 🤖 Subagents 핵심 가이드라인

### 📁 파일 위치 및 우선순위
1. **프로젝트 서브에이전트**: `.claude/agents/` (높은 우선순위)
2. **사용자 서브에이전트**: `~/.claude/agents/` (낮은 우선순위)

### 📝 올바른 YAML Frontmatter
```markdown
---
name: agent-name-in-kebab-case
description: 에이전트가 언제 사용되어야 하는지 설명
tools: Tool1, Tool2, Tool3  # 선택사항 - 없으면 모든 도구 상속
---

에이전트의 시스템 프롬프트가 여기에 작성됩니다.
역할, 능력, 문제 해결 접근법을 명확히 정의하세요.

구체적인 지시사항, 모범 사례, 제약사항을 포함하세요.
```

### 📋 필수 필드
| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | ✅ | 소문자+하이픈 형식의 고유 식별자 |
| `description` | ✅ | 에이전트 목적과 사용 시점 설명 |
| `tools` | ❌ | 특정 도구만 허용 (없으면 모든 도구 상속) |

### 🎯 Description 작성 팁
- **구체적으로**: "코드 리뷰 전문가" ❌ → "코드 작성/수정 후 PROACTIVELY 품질, 보안, 유지보수성 검토" ✅
- **사용 시점 명시**: "Use PROACTIVELY when...", "MUST BE USED for..."
- **키워드 포함**: 자동 위임을 위한 관련 키워드 포함

### 🛠️ 도구 권한 설정
```yaml
# 모든 도구 상속 (권장)
tools: # 필드 생략

# 특정 도구만 허용
tools: Read, Edit, Bash, Grep

# MCP 도구 포함 (자동 상속됨)
# tools 필드 생략 시 MCP 도구도 자동 포함
```

### 🔄 **서브에이전트 실행 시 중요한 동작 원리**

#### ⚠️ 메인 에이전트 정지 상태
```
메인 에이전트가 서브에이전트 호출 시:
┌─────────────────┐
│ Main Agent      │ ─── 서브에이전트 호출
│ (정지 상태 🛑)   │     ↓
└─────────────────┘   ┌─────────────────┐
                      │ Subagent        │ ← 활성 상태 ▶️
                      │ (작업 수행 중)   │
                      └─────────────────┘
```

**핵심 규칙**:
- **메인 에이전트는 서브에이전트 호출 즉시 정지** 🛑
- **서브에이전트만 활성 상태로 작업 수행** ▶️
- **서브에이전트 완료 후 메인 에이전트로 제어 복귀** 🔄
- **동시 실행 불가**: 한 번에 하나의 에이전트만 활성

#### 📝 올바른 서브에이전트 위임 패턴
```bash
# ✅ 올바른 패턴
"I'll use the Task tool to delegate this to implementer-spark"
→ 메인 에이전트 정지, implementer-spark 활성화

# ❌ 잘못된 패턴  
"I'll help implement this myself while also using implementer-spark"
→ 불가능! 메인 에이전트는 정지 상태가 됨
```

#### 🎯 위임 시 고려사항
1. **완전한 컨텍스트 전달**: 서브에이전트가 독립적으로 작업 가능하도록
2. **명확한 작업 범위**: 서브에이전트가 무엇을 해야 하는지 정확히 명시
3. **필요한 정보 모두 제공**: 메인 에이전트와 소통 불가하므로 사전에 모든 정보 제공
4. **결과 처리 계획**: 서브에이전트 완료 후 어떻게 결과를 처리할지 미리 계획

### ⚡ **도구 동시 호출 및 병렬 처리**

#### 🚀 도구 동시 호출 제한
```yaml
일반 Claude Code:
  - 동시 도구 호출: 최대 8개 (실제 테스트 결과)
  
서브에이전트:
  - 동시 도구 호출: 최대 10개 (공식 문서 기준)
  
⚠️ 중요: "진짜 동시" 호출이어야 함!
```

#### 📋 올바른 동시 호출 패턴
```xml
<!-- ✅ 올바른 동시 호출 (단일 응답에서 모두 호출) -->
<function_calls>
<invoke name="Read">
<parameter name="file_path">file1.py</parameter>
</invoke>
<invoke name="Read">
<parameter name="file_path">file2.py</parameter>
</invoke>
<invoke name="Grep">
<parameter name="pattern">function</parameter>
</invoke>
<invoke name="Bash">
<parameter name="command">git status</parameter>
</invoke>
</function_calls>

<!-- ❌ 잘못된 순차 호출 (여러 응답으로 나누어 호출) -->
첫 번째 응답:
<function_calls>
<invoke name="Read">
<parameter name="file_path">file1.py</parameter>
</invoke>
</function_calls>

두 번째 응답:
<function_calls>
<invoke name="Read">
<parameter name="file_path">file2.py</parameter>
</invoke>
</function_calls>
```

#### 🚀 병렬 작업 진행 (실제 검증됨)
```yaml
병렬 작업 테스트 결과 (Jason 검증):
  - 4개 작업 동시 병렬 처리: ✅ 성공
  - git status, git diff, 파일 읽기, 검색 등 동시 실행
  - 각 작업이 독립적으로 완료되어 결과 반환

효율성 향상:
  - 순차 처리 대비 75% 시간 절약
  - I/O 대기 시간 최적화
  - SPARK 시스템 핵심 성능 최적화 기능
```

#### 💡 동시 호출 최적화 팁
```python
# ✅ 독립적 작업들을 묶어서 동시 호출
병렬 가능한 작업들:
  - 여러 파일 읽기 (Read)
  - 여러 디렉토리 검색 (Grep, Glob)
  - 독립적인 bash 명령어들
  - git 상태 확인 작업들

# ❌ 의존성이 있는 작업들은 순차 처리
순차 처리 필요한 작업들:
  - 파일 읽기 → 편집 → 저장
  - git add → git commit → git push
  - 테스트 실행 → 결과 분석 → 보고서 생성
```

#### 🎯 SPARK 에이전트별 최적화
```yaml
Implementer-Spark:
  - 분석 단계: Read + Grep + Glob 동시 호출 (최대 8개)
  - 구현 단계: 독립적 파일들 동시 편집
  - 검증 단계: 테스트 + 린트 + 타입체크 병렬 실행

Analyzer-Spark:
  - 다중 파일 동시 분석
  - 여러 검색 패턴 병렬 실행
  - 메트릭스 수집 작업 동시 진행

Tester-Spark:
  - 여러 테스트 파일 동시 생성
  - 병렬 테스트 실행
  - 커버리지 + 린트 + 보안 검사 동시 실행
```

---

## 🔒 보안 모범 사례

### ✅ 필수 준수사항
- **절대 경로 사용**: `~/scripts/check.sh` ✅, `check.sh` ❌
- **sudo 사용 금지**: Hook은 사용자 권한으로만 실행
- **민감한 파일 패턴 주의**: `.env`, `.ssh/*`, `secrets.*` 등
- **입력 경로 검증**: `../` 경로 거부, 예상 형식 확인
- **변수 인용**: `"$VAR"` 사용으로 인젝션 방지
- **오류 검사 유지**: `set +e` 피하기

### 🚫 위험한 패턴 (차단 필요)
```python
# Hook에서 위험한 명령어 차단 예제
dangerous_patterns = [
    'rm -rf /', 'dd if=', ':(){ :|:& };:',
    '> /dev/sda', 'mkfs.', 'format ',
    '; rm ', '&& rm ', '| rm ',
    'eval(', 'exec(', '__import__',
    'curl ... | sh', '| bash'
]
```

### 🛡️ 안전한 Hook 작성 템플릿
```python
#!/usr/bin/env python3
import json
import sys
import os

def main():
    try:
        # stdin에서 JSON 입력 받기
        input_data = json.load(sys.stdin)
        
        # 입력 검증
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        
        # 비즈니스 로직 처리
        result = process_hook(input_data)
        
        # JSON 출력 (선택사항)
        if result:
            print(json.dumps(result))
        
        sys.exit(0)
        
    except Exception as e:
        # 오류 처리
        print(f"Hook error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 📊 SPARK 시스템 적용 원칙

### 🎯 Hook 사용 가이드라인
```json
{
  "hooks": {
    "userPromptSubmit": [
      {
        "description": "SPARK Persona Router - Task routing and persona activation",
        "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/spark_persona_router.py"}]
      }
    ],
    "subagentStop": [
      {
        "description": "SPARK Quality Gates - Multi-point validation with retry",
        "hooks": [{"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/spark_quality_gates.py"}]
      }
    ]
  }
}
```

### 🚀 명령어 구조 원칙
- **명확한 단계 정의**: Phase 1, Phase 2, Phase 3...
- **진행 조건 명시**: "Phase X → Phase Y 진행 조건"
- **Hook 신호 확인**: "SubagentStop hook이 'continue' 신호 반환"
- **실패 조건 정의**: 재시도 vs 중단 기준 명확화

### 🤖 Subagent 설계 원칙
- **단일 책임**: 하나의 명확한 역할만 담당
- **상세한 프롬프트**: 구체적인 지시사항과 예제 포함
- **도구 권한 최소화**: 필요한 도구만 허용
- **버전 관리**: 프로젝트 subagent는 Git에 포함

---

## 🚨 절대 금지사항

### ❌ Hook 관련
- 존재하지 않는 hook 이벤트 사용
- 모든 hook에서 같은 스크립트 호출
- Exit code 의미 무시
- JSON 형식 오류

### ❌ Commands 관련
- Task 도구 직접 호출 지시
- 진행 조건 없는 multi-phase 명령어
- Frontmatter 필드 오타
- 보안 검증 없는 Bash 실행

### ❌ Subagents 관련
- 필수 필드 누락 (name, description)
- 모호한 description
- 과도한 권한 부여
- YAML 문법 오류

---

## 📚 참고 자료

### 공식 문서
- [Hook Guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)
- [Hooks Reference](https://docs.anthropic.com/en/docs/claude-code/hooks-reference)
- [Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Subagents](https://docs.anthropic.com/en/docs/claude-code/subagents)

### 환경 변수
- `$CLAUDE_PROJECT_DIR`: 프로젝트 루트 디렉토리 절대 경로

### 디버깅
```bash
# Hook 실행 상세 정보 확인
claude --debug

# Hook 상태 확인  
/hooks

# 설정 검증
/config
```

---

## ✅ 체크리스트

### Hook 구현 시
- [ ] 존재하는 Hook 이벤트만 사용
- [ ] 올바른 JSON 구조 적용
- [ ] Exit code 의미 준수
- [ ] 보안 검증 포함
- [ ] 에러 처리 구현

### Command 구현 시
- [ ] 올바른 Frontmatter 사용
- [ ] 진행 조건 명시 (multi-phase인 경우)
- [ ] $ARGUMENTS 올바른 사용
- [ ] 보안 고려 (Bash 사용 시)

### Subagent 구현 시
- [ ] 필수 필드 모두 포함
- [ ] 구체적인 description 작성
- [ ] 적절한 도구 권한 설정
- [ ] 상세한 시스템 프롬프트 작성

---

*이 가이드라인을 준수하여 안정적이고 효율적인 SPARK 시스템을 구축하세요.*