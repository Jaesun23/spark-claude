---
description: V5 체크리스트 자동 구현 - 지능적 조건부 워크플로우
---

# V5 Implementation Command - Intelligent Orchestration

## 📌 2호를 위한 핵심 지침

**당신(2호)은 이제 지능적 오케스트레이터입니다!**

1. **매 서브에이전트 완료 후 반드시 할 일:**
   - Read 도구로 `.claude/workflows/current_task.json` 읽기
   - `routing_decision["next_action"]` 값 확인
   - 그 값에 따라 다음 에이전트 호출 또는 워크플로우 종료

2. **절대 규칙:**
   - routing_decision을 무시하고 임의로 다음 단계 진행 금지
   - 항상 current_task.json이 지시하는 대로만 행동
   - SubagentStop hook이 routing을 결정, 2호는 실행만

## 🚀 개선된 자동화 워크플로우

이제 당신(2호)은 단순한 순차 실행이 아닌 **지능적 오케스트레이터** 역할을 합니다.
Quality 결과에 따라 조건부로 흐름을 제어하여 **오류 0개**를 목표로 합니다.

## 📊 워크플로우 다이어그램

```
┌─────────────┐
│ Implementer │ ←────┐
└──────┬──────┘      │
       ↓             │
┌─────────────┐      │ (오류 발견 시)
│  Quality#1  │ ─────┘
└──────┬──────┘
       ↓ (통과 시)
┌─────────────┐
│   Tester    │ ←────┐
└──────┬──────┘      │
       ↓             │
┌─────────────┐      │ (테스트 오류 시)
│  Quality#2  │ ─────┘
└──────┬──────┘
       ↓ (통과 시)
┌─────────────┐
│  Reviewer   │
└──────┬──────┘
       ↓
┌─────────────┐
│  Reporter   │
└─────────────┘
```

## 🎯 2호의 오케스트레이터 역할

### 핵심: SubagentStop Hook을 통한 제어권 회복
2호는 각 서브에이전트가 완료될 때마다 `SubagentStop` hook을 통해 제어권을 되찾고,
`current_task.json`의 `routing_decision`을 읽어 다음 행동을 결정합니다.

### 1단계: 초기화 및 DNA 리소스 스캔
**2호가 직접 수행:**
1. 체크리스트 파일 읽기: `$ARGUMENTS`
2. Task ID 추출 (예: TASK-N1-01)
3. current_task.json 초기화 (새 구조 사용)
4. DNA 리소스 스캔하여 사용 가능한 상수/타입 파악

### 2단계: Implementer 호출
**2호의 Task 도구 호출:**
```python
Task(
    description="V5 Implementation - $ARGUMENTS",
    prompt="Implement $ARGUMENTS. Read current_task.json for context and DNA resources.",
    subagent_type="implementer"
)
```

**SubagentStop 후 2호가 해야 할 행동:**
1. Read 도구로 `current_task.json` 읽기
2. `routing_decision` 필드 확인
3. `next_action` 값에 따라 행동:
   - `"quality_check_1"` → 3단계로 진행 (Quality 호출)
   - `"retry_implementer"` → 2단계 반복 (fix_suggestions 포함)
   - `"escalate"` → 수동 개입 요청 메시지 출력

### 3단계: Quality Check #1
**조건: routing_decision["next_action"]이 "quality_check_1"일 때만 실행**
```python
Task(
    description="Quality Check Post-Implementation",
    prompt="Check implementation quality. Update quality_metrics in current_task.json.",
    subagent_type="quality"
)
```

**SubagentStop 후 2호가 해야 할 행동:**
1. Read 도구로 `current_task.json` 다시 읽기
2. `routing_decision` 필드 확인
3. `next_action` 값에 따라 행동:
   - `"retry_implementer"` → 2단계로 돌아가기 (fix_suggestions 읽어서 전달)
   - `"proceed_to_tester"` → 5단계로 진행 (Tester 호출)
   - `"escalate"` → 최대 반복 도달 메시지 출력

### 4단계: 조건부 라우팅 (2호의 핵심 역할)
**2호는 항상 current_task.json의 routing_decision을 따름:**
```python
# 2호가 실제로 해야 할 코드
import json

# 1. current_task.json 읽기
with open('.claude/workflows/current_task.json', 'r') as f:
    task_data = json.load(f)
    
routing = task_data["routing_decision"]
next_action = routing["next_action"]

# 2. next_action에 따라 다음 에이전트 호출
if next_action == "retry_implementer":
    # fix_suggestions 읽어서 전달
    fixes = task_data["fix_management"]["fix_suggestions"]
    Task(
        description=f"Fix {len(fixes)} violations",
        prompt=f"Fix these issues from current_task.json: {fixes}",
        subagent_type="implementer"
    )
elif next_action == "proceed_to_tester":
    # Tester 호출
    Task(
        description="Write tests with 95% coverage",
        prompt="Write comprehensive tests. Check current_task.json for implementation details.",
        subagent_type="tester"
    )
```
### 5단계: Tester 실행
**조건: routing_decision["next_action"]이 "proceed_to_tester"일 때만 실행**
```python
Task(
    description="Write Tests - $ARGUMENTS",
    prompt="Write comprehensive tests. Target 95% coverage. Check current_task.json for implementation details.",
    subagent_type="tester"
)
```

**SubagentStop 후 2호가 해야 할 행동:**
1. Read 도구로 `current_task.json` 읽기
2. `routing_decision["next_action"]` 확인
3. 일반적으로 `"quality_check_2"`로 설정되어 있으므로 6단계로 진행

### 6단계: Quality Check #2
**조건: routing_decision["next_action"]이 "quality_check_2"일 때 실행**
```python
Task(
    description="Quality Check Post-Test",
    prompt="Validate test quality and coverage. Update quality_metrics.testing in current_task.json.",
    subagent_type="quality"
)
```

**SubagentStop 후 2호가 해야 할 행동:**
1. Read 도구로 `current_task.json` 읽기
2. `routing_decision["next_action"]` 확인
3. 값에 따라 행동:
   - `"retry_tester"` → 5단계로 돌아가기 (테스트 개선 요청)
   - `"proceed_to_reviewer"` → 7단계로 진행 (Reviewer 호출)
   - `"proceed_with_warnings"` → 경고 메시지 출력 후 7단계로 진행

### 7단계: Reviewer 실행
**조건: routing_decision["next_action"]이 "proceed_to_reviewer"일 때만 실행**
```python
Task(
    description="Architecture Review - $ARGUMENTS",
    prompt="Review DNA v3.6 compliance. Check for architectural violations.",
    subagent_type="reviewer"
)
```

**SubagentStop 후 2호가 해야 할 행동:**
1. Read 도구로 `current_task.json` 읽기
2. `routing_decision["next_action"]` 확인
3. 일반적으로 `"proceed_to_reporter"`로 설정되므로 8단계로 진행

### 8단계: Reporter 실행
**조건: routing_decision["next_action"]이 "proceed_to_reporter"일 때만 실행**
```python
Task(
    description="Final Report - $ARGUMENTS",
    prompt="Generate comprehensive report with metrics and actionable insights.",
    subagent_type="reporter"
)
```

**SubagentStop 후 2호가 해야 할 행동:**
1. Read 도구로 `current_task.json` 최종 확인
2. `routing_decision["next_action"]`이 `"workflow_complete"`인지 확인
3. 워크플로우 완료 메시지 출력: "✅ 워크플로우 완료! 최종 보고서는 current_task.json 참조"

## 🔧 current_task.json 구조 확장

```json
{
  "task_id": "TASK-XX-XX",
  "iteration_count": 1,
  "max_iterations": 3,
  "current_phase": "quality_check_1",

  "dna_resources": {
    "target_system": "nervous",
    "available_constants": ["LOG_LEVEL", "LOG_FORMAT", ...],
    "available_types": ["LogContext", "LogLevel", ...],
    "required_imports": [
      "from src.dna.nervous.logger import get_logger",
      "from src.dna.endocrine.constants import LOG_LEVEL"
    ]
  },

  "quality_gates": {
    "ruff_violations": 0,
    "mypy_errors": 0,
    "bandit_issues": 0,
    "coverage": 98.5,
    "magic_numbers": 0,
    "any_types": 0,
    "missing_dna_imports": 0
  },

  "fix_suggestions": [
    {
      "type": "magic_number",
      "location": "line 45",
      "current": "timeout = 30",
      "suggested": "timeout = HEALTH_CHECK_TIMEOUT",
      "dna_import": "from src.dna.endocrine.constants import HEALTH_CHECK_TIMEOUT"
    }
  ],

  "implementation_history": [
    {
      "iteration": 1,
      "timestamp": "2025-08-05T10:00:00Z",
      "issues_found": 15,
      "issues_fixed": 0
    },
    {
      "iteration": 2,
      "timestamp": "2025-08-05T10:30:00Z",
      "issues_found": 3,
      "issues_fixed": 12
    }
  ]
}
```

## 🎮 2호의 오케스트레이션 규칙

### 핵심 원칙
1. **SubagentStop Hook 의존**: 각 서브에이전트 완료 시 hook이 routing_decision 업데이트
2. **routing_decision 절대 준수**: 2호는 항상 current_task.json의 routing_decision을 따름
3. **서브에이전트는 독립적**: 서로 소통 불가, JSON이 유일한 소통 채널
4. **2호만이 흐름 제어**: 조건부 판단과 다음 에이전트 호출은 2호의 책임

### 실행 시 2호의 구체적 행동 코드
```python
# 2호가 실제로 실행해야 할 코드
import json

# 초기화
current_phase = "implementation"
workflow_complete = False

while not workflow_complete:
    # 1. 현재 phase에 따라 Task 도구 호출
    if current_phase == "implementation":
        Task(
            description="V5 Implementation",
            prompt="Implement task. Check current_task.json",
            subagent_type="implementer"
        )
    
    # 2. SubagentStop hook이 자동 실행됨 (2호는 대기)
    # Hook이 current_task.json의 routing_decision 업데이트
    
    # 3. 2호가 제어권 회복 후 JSON 읽기
    with open('.claude/workflows/current_task.json', 'r') as f:
        task_data = json.load(f)
    
    # 4. routing_decision 확인하고 다음 행동 결정
    next_action = task_data["routing_decision"]["next_action"]
    
    if next_action == "workflow_complete":
        print("✅ 워크플로우 완료!")
        workflow_complete = True
    elif next_action == "escalate":
        print("⚠️ 수동 개입 필요:", task_data["routing_decision"]["reason"])
        break
    elif next_action == "retry_implementer":
        # 2단계로 다시
        current_phase = "implementation"
    elif next_action == "quality_check_1":
        # Quality 호출
        Task(
            description="Quality Check #1",
            prompt="Check quality",
            subagent_type="quality"
        )
    # ... 각 next_action에 대한 처리
```

## 🚨 중요 지침

1. **Hook 시스템 필수**: SubagentStop hook이 없으면 조건부 워크플로우 불가능
2. **JSON 상태 관리**: current_task.json이 워크플로우의 단일 진실 소스
3. **반복 제한 준수**: 최대 3회 반복으로 무한 루프 방지
4. **품질 우선**: 품질 기준 미충족 시 다음 단계 진행 불가
5. **DNA 사용 강제**: magic_numbers와 any_types는 반드시 0

## 📈 예상 결과

이 지능적 오케스트레이션을 통해:
- **285개 오류 → 0개** 목표
- DNA 시스템 활용률 **100%** 달성
- 자동 품질 보장 시스템 구축
- 수동 개입 최소화
- 일관된 고품질 코드 생산

2호는 이제 **SubagentStop Hook과 협력하는 지능적 오케스트레이터**입니다!
