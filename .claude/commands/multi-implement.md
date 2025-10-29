---
name: multi-implement
description: Parallel implementation across multiple teams with coordination and integration management
type: command
requires: team1-implementer-spark, team2-implementer-spark, team3-implementer-spark, team4-implementer-spark
---

# /multi-implement - Parallel Team Implementation Command

**Purpose**: Parallel implementation is the art of orchestrating multiple teams to work in harmony, like conducting a symphony where every section contributes to a unified masterpiece.

## 🏗️ System Architecture Understanding (필독)

### 에이전트의 도구적 특성
- **에이전트 = 도구**: 2호가 사용하는 '도구' (cp, ls 명령어와 동일한 성격)
- **실행 중 2호 정지**: 에이전트 실행 중 2호는 suspended 상태
- **통신 불가능 (By Design)**: 에이전트 간, 에이전트-2호 간 통신 불가능
- **4개 모두 완료 대기**: 모든 에이전트 종료 후 2호 재활성화

### 병렬 실행의 전제 조건
**CRITICAL: 의존성 없는 작업만 병렬 실행 가능**

```python
# ✅ CORRECT: 의존성 없는 독립 작업들
tasks = [
    "Team1: 인증 모듈 구현",      # 독립적
    "Team2: 결제 모듈 구현",      # 독립적  
    "Team3: 알림 시스템 구현",    # 독립적
    "Team4: 로깅 시스템 구현"     # 독립적
]

# ❌ WRONG: 의존성 있는 작업들
tasks = [
    "Team1: API 엔드포인트 정의",
    "Team2: API 호출 구현",       # Team1 필요 ❌
    "Team3: API 테스트",          # Team1,2 필요 ❌
    "Team4: API 문서화"           # 모두 필요 ❌
]
```

### 체크리스트 기반 사전 조정
```
작업 흐름:
1. 청사진 작성 (전체 아키텍처 설계)
2. 작업 분해 (100+ 개별 작업으로 분해)
3. 체크리스트 작성 (작업별 완전한 명세서)
4. 의존성 분석 → 병렬 가능 그룹 선별
5. 병렬 실행 (충돌 없음이 사전 보장됨)
```

### 파일 락 시스템 (자동 관리)
- **자동 관리**: `.claude/hooks/file_lock_manager.py`가 처리
- **락 파일**: `.claude/workflows/file_locks.json`
- **자동 해제**: 30초 후 자동 해제
- **대상**: 주로 공통 상수 정의 파일

## Decision Framework (2호의 병렬 조정 판단)

2호가 다중팀 구현을 orchestrate할 때의 상황별 판단 기준:

### Team Coordination Balance (미묘한 조절이나 균형의 묘)

**상황별 조정 전략:**
- **High Interdependency**: 팀간 긴밀한 조정과 통합 검증 강화
- **Experienced Teams**: 팀 자율성 최대화, 최소한의 오버헤드  
- **Standard Cases**: 균형잡힌 조정으로 자율성과 통합 모두 확보

**구체적 조정 원칙:**
- 각 팀은 명확한 소유권과 결정권을 가짐
- 모든 팀이 같은 품질 기준과 사용자 경험 목표로 작업
- 팀 상호작용은 최소 오버헤드로 최대 가치 창출
- 성공은 개별 팀이 아닌 전체로 측정

### Parallel Implementation Philosophy

**병렬 작업 원칙:**
1. **Autonomous Teams**: 각 팀의 독립적 의사결정권 보장
2. **Shared Vision**: 공통 품질 및 사용자 경험 목표
3. **Smart Coordination**: 필요한 만큼만 조정, 과도한 마이크로매니징 방지
4. **Collective Success**: 전체 결과물의 통합성과 일관성 중시

## Design Principles (병렬 실행 설계 지침)

**Team Distribution:**
- 4개 팀 (team1, team2, team3, team4) 병렬 실행
- 각 팀은 독립적인 JSON 상태 파일 관리
- 공유 리소스에 대한 파일 락 메커니즘

**Quality Standards (전 팀 공통):**
- 팀별 Violations: 0
- 통합 충돌: 0
- 공유 리소스 위반: 0
- 모든 팀 완료: Required

## 📝 2호 Execution Protocol (병렬 orchestration)

### **WHEN RECEIVING /multi-implement COMMAND:**

**CRITICAL: 병렬 실행은 반드시 ONE MESSAGE에서 수행**

**PHASE 0: Pre-Parallel Validation (필수 사전 검증)**
```python
# 병렬 실행 전 필수 확인
def validate_parallel_eligibility(tasks):
    """의존성 체크 - 병렬 가능한지 확인"""
    for task in tasks:
        assert task.has_complete_checklist, f"{task} missing checklist!"
        assert task.dependencies == [], f"{task} has dependencies - cannot parallelize!"
        assert task.estimated_time_similar, "Unbalanced workload - adjust tasks"
    
    print("✅ All tasks are independent - safe for parallel execution")
    print("✅ Checklists complete - interfaces guaranteed to match")
    print("✅ Workload balanced - teams will finish around same time")
```

**PHASE 1: Parallel Team Launch**
```bash
# MUST be in SINGLE MESSAGE - 4 Task calls together:
1. Task("team1-implementer-spark", "Team1 task: [task1_description]")
   Task("team2-implementer-spark", "Team2 task: [task2_description]")  
   Task("team3-implementer-spark", "Team3 task: [task3_description]")
   Task("team4-implementer-spark", "Team4 task: [task4_description]")

2. Wait for ALL teams completion (parallel execution)
```

**PHASE 2: Individual Team Validation**
```bash
3. Check each team's JSON file:
   ✅ team1_current_task.json:
   - team_info.status == "COMPLETED" 
   - implementation.quality_score >= 95
   - testing.coverage >= 95
   - len(implementation.errors) == 0
   
   ✅ team2_current_task.json: [same criteria]
   ✅ team3_current_task.json: [same criteria]  
   ✅ team4_current_task.json: [same criteria]
   
   ❌ ANY TEAM FAILS → Retry only failed teams (max 2 retries per team)
```

**PHASE 3: Integration Validation**
```bash
4. Check file_locks.json for conflicts
5. Validate no shared resource violations
6. Run integration tests across all teams' outputs
   
   ✅ INTEGRATION PASS → Success report
   ❌ INTEGRATION FAIL → Coordinate conflict resolution
```

**SUCCESS REPORT:**
```
✅ Multi-Team Implementation Complete:
- Team 1: [files] files, [coverage]% coverage
- Team 2: [files] files, [coverage]% coverage  
- Team 3: [files] files, [coverage]% coverage
- Team 4: [files] files, [coverage]% coverage
- Integration: All teams integrated successfully
- Quality: 0 violations across all teams
```

**FAILURE HANDLING:**
- Individual team failure: Retry only that team
- Integration conflict: Coordinate resolution between affected teams  
- Shared resource violation: Implement file locking protocol
- Maximum 2 retries per issue, then abort with detailed report

⚡ **Core Principle**: 2호는 4개 팀을 병렬 관리하되 통합 품질을 보장합니다
