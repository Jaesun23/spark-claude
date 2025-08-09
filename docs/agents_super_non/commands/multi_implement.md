---
description: V5 병렬 체크리스트 구현 - 4팀 동시 실행으로 개발 속도 극대화
---

# Multi Implementation Command - Parallel Team Orchestration

## 🚀 당신(2호)이 실행해야 할 병렬 워크플로우

Jason이 `/multi_implement TASK-ID1 TASK-ID2 ...` 명령어를 입력하면, 당신은 **4개 팀의 총괄 지휘관**이 되어 병렬 실행을 조율합니다.

## 🎯 당신이 수행할 5단계 병렬 워크플로우

### 사전 확인: 훅 시스템 자동 처리 완료 검증
Jason이 `/multi_implement` 입력 시 multi_implement_scanner.py 훅이 자동으로:
- 각 TASK-ID를 Team1~4에 순차 할당 완료
- team1_current_task.json ~ team4_current_task.json에 DNA 리소스 스캔 완료
- multi_task_coordination.json에 팀 상태 기록 완료

**당신의 첫 번째 임무: 이 자동 처리가 성공했는지 확인**

### 1단계: 병렬 Implementation Phase
**당신이 Task 도구로 활성 팀들을 동시 호출:**

한 팀을 호출하고 기다렸다가 호출하면 대기상태에 들어가기 때문에 동시에 활성팀을 한 꺼번에 호출해야 함

multi_task_coordination.json에서 status="ASSIGNED"인 팀들만 골라서 동시에 Task 도구 호출:

```
description: "Team1 Implementation - [할당된 TASK-ID]"
prompt: "team1_current_task.json에서 할당받은 체크리스트 구현. DNA-First 방식으로 구현하되 다른 팀과 파일 충돌 없도록 주의."
subagent_type: "team1_implementer"

description: "Team2 Implementation - [할당된 TASK-ID]"
prompt: "team2_current_task.json에서 할당받은 체크리스트 구현. DNA-First 방식으로 구현하되 다른 팀과 파일 충돌 없도록 주의."
subagent_type: "team2_implementer"

description: "Team3 Implementation - [할당된 TASK-ID]"
prompt: "team3_current_task.json에서 할당받은 체크리스트 구현. DNA-First 방식으로 구현하되 다른 팀과 파일 충돌 없도록 주의."
subagent_type: "team3_implementer"

description: "Team4 Implementation - [할당된 TASK-ID]"
prompt: "team4_current_task.json에서 할당받은 체크리스트 구현. DNA-First 방식으로 구현하되 다른 팀과 파일 충돌 없도록 주의."
subagent_type: "team4_implementer"
```

**중요**: INACTIVE 상태인 팀은 호출하지 마세요.

### 2단계: 병렬 Quality Assurance Phase
**1단계 완료 후 구현 완료된 팀들의 품질 검사 동시 실행:**

```
description: "Team1 Quality Check"
prompt: "Team1이 구현한 코드의 품질 검사 수행. ruff, mypy, bandit 모든 위반사항을 0개까지 수정. team1_current_task.json의 quality 섹션 업데이트."
subagent_type: "team1_quality"

description: "Team2 Quality Check"
prompt: "Team2가 구현한 코드의 품질 검사 수행. ruff, mypy, bandit 모든 위반사항을 0개까지 수정. team2_current_task.json의 quality 섹션 업데이트."
subagent_type: "team2_quality"

description: "Team3 Quality Check"
prompt: "Team3이 구현한 코드의 품질 검사 수행. ruff, mypy, bandit 모든 위반사항을 0개까지 수정. team3_current_task.json의 quality 섹션 업데이트."
subagent_type: "team3_quality"

description: "Team4 Quality Check"
prompt: "Team4가 구현한 코드의 품질 검사 수행. ruff, mypy, bandit 모든 위반사항을 0개까지 수정. team4_current_task.json의 quality 섹션 업데이트."
subagent_type: "team4_quality"
```

### 3단계: 병렬 Testing Phase
**2단계 완료 후 품질 검사 통과한 팀들의 테스트 작성 동시 실행:**

```
description: "Team1 Comprehensive Testing"
prompt: "Team1 구현에 대한 포괄적 테스트 작성. 95% 커버리지 목표. team1_current_task.json에서 구현 내용 확인 후 단위/통합 테스트 작성."
subagent_type: "team1_tester"

description: "Team2 Comprehensive Testing"
prompt: "Team2 구현에 대한 포괄적 테스트 작성. 95% 커버리지 목표. team2_current_task.json에서 구현 내용 확인 후 단위/통합 테스트 작성."
subagent_type: "team2_tester"

description: "Team3 Comprehensive Testing"
prompt: "Team3 구현에 대한 포괄적 테스트 작성. 95% 커버리지 목표. team3_current_task.json에서 구현 내용 확인 후 단위/통합 테스트 작성."
subagent_type: "team3_tester"

description: "Team4 Comprehensive Testing"
prompt: "Team4 구현에 대한 포괄적 테스트 작성. 95% 커버리지 목표. team4_current_task.json에서 구현 내용 확인 후 단위/통합 테스트 작성."
subagent_type: "team4_tester"
```

### 4단계: 통합 Architecture Review
**3단계 완료 후 모든 팀 작업의 아키텍처 통합 검토:**

```
description: "Multi-Team Architecture Integration Review"
prompt: "모든 팀의 DNA 시스템 구현을 통합 아키텍처 관점에서 검토. DNA v3.5 준수, Clean Architecture 의존성 규칙, 시스템 간 충돌 여부, import-linter 통과 여부 검증."
subagent_type: "reviewer"
```

### 5단계: 통합 Final Report
**4단계 완료 후 전체 병렬 작업 결과 종합 보고:**

```
description: "Multi-Team Implementation Final Report"
prompt: "4팀 병렬 구현 결과 종합 보고서 생성. 각 팀별 성과 요약, 전체 진행률, 품질 지표 달성도, Stage 1 Bootstrap 진행 상황, 다음 우선순위 추천."
subagent_type: "reporter"
```

## 🏗️ 팀 구조 (4팀 고정)

### Team-specific Agents
- **team1_implementer**, **team1_quality**, **team1_tester**
- **team2_implementer**, **team2_quality**, **team2_tester**
- **team3_implementer**, **team3_quality**, **team3_tester**
- **team4_implementer**, **team4_quality**, **team4_tester**

### Shared Agents
- **reviewer**: 통합 아키텍처 검토
- **reporter**: 최종 통합 보고서

## 📁 파일 관리

### 팀별 작업 추적
```
.claude/workflows/team1_current_task.json
.claude/workflows/team2_current_task.json
.claude/workflows/team3_current_task.json
.claude/workflows/team4_current_task.json
.claude/workflows/multi_task_coordination.json  # 통합 조정
```

## 🚨 당신(2호)의 핵심 실행 지침

### ✅ 당신이 반드시 해야 할 일
1. **순차적 단계 실행**: 각 단계가 완료된 후에만 다음 단계 진행
2. **활성 팀만 호출**: multi_task_coordination.json에서 status="ASSIGNED"인 팀만 Task 호출
3. **동시 호출**: 같은 단계 내에서는 모든 활성 팀을 동시에 Task 도구로 호출
4. **완료 확인**: 각 단계 완료 후 결과를 확인하고 다음 단계로 진행

### ⚠️ 중요한 실행 원칙
- **한 번에 한 단계씩**: Implementation 완료 → Quality 완료 → Testing 완료 → Review → Report
- **INACTIVE 팀 제외**: status="INACTIVE"인 팀은 절대 호출하지 않음
- **충돌 방지**: 각 팀이 자신의 DNA 시스템 영역만 수정하도록 지시

## ⚠️ 공유 리소스 충돌 주의사항

모든 팀이 다음 파일들을 동시에 수정할 수 있으므로 **순차 처리**가 필요할 수 있습니다:
- `src/dna/endocrine/constants.py` - 모든 팀이 상수 추가
- `src/dna/skeletal/types.py` - 모든 팀이 타입 추가
- `.import-linter.toml` - 아키텍처 규칙

각 팀 에이전트에게 **"다른 팀과 파일 충돌하지 않도록 주의"**하라고 명시적으로 지시하세요.

## 📌 당신이 이 워크플로우를 실행할 조건

Jason이 `/multi_implement` 명령어와 함께 **2개 이상**의 TASK-ID를 입력했을 때만 이 병렬 워크플로우를 실행하세요.

**입력 패턴 인식:**
- `/multi_implement TASK-E1-01 TASK-N1-03` → 2개 팀 병렬 실행
- `/multi_implement TASK-S1-01 TASK-I1-01 TASK-D1-02` → 3개 팀 병렬 실행
- `/multi_implement TASK-S1-01 TASK-I1-01 TASK-D1-02 TASK-R1-01` → 4개 팀 병렬 실행

**주의:** 1개의 TASK-ID만 있다면 이 명령어가 아닌 `/implement` 워크플로우를 따르세요.

## 📈 예상 성과

이 병렬 워크플로우로 달성 가능한 성과:
- **개발 속도 2-4배 향상**: 팀 수에 비례한 속도 증가
- **품질 기준 동일 유지**: 각 팀이 개별적으로 0위반 달성
- **DNA 아키텍처 준수**: 팀별 DNA 시스템 전문화

## 📈 예상 효과

### 성능 향상:
- **최대 4배 속도**: 4개 작업 병렬 처리
- **효율적 리소스 사용**: 컨텍스트 제한 내에서 최적화
- **품질 보장**: 팀별 독립 검증 + 통합 검토

### 제한사항 관리:
- **컨텍스트 절약**: 4팀으로 제한하여 안정성 확보
- **충돌 최소화**: 독립적인 DNA 시스템 작업 권장

**이제 최대 4개의 대규모 구현 작업을 동시에 처리할 수 있습니다!** 🚀
