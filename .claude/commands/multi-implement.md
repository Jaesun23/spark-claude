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

### **CRITICAL: JSON 파일 역할 이해**
```typescript
// ⚠️ 중요: 에이전트는 JSON을 READ & WRITE 모두 수행!
// 2호가 초기 구조 생성 → 에이전트가 결과 업데이트 → 2호가 검증

// team1_current_task.json (에이전트가 업데이트)
{
  "task_id": "AKL-02",
  "checklist_path": "/docs/blueprints/checklists/...",  // 2호가 설정
  "status": "in_progress",  // 에이전트가 업데이트
  "results": { ... },  // 에이전트가 작성
  "quality": {
    "violations": 0,  // 에이전트가 계산
    "can_proceed": true  // 에이전트가 판단
  }
}
```

### **팀 할당 원칙 (5개 팀 사용 가능)**
- 작업 수 ≤ 5: 작업 수만큼 팀 사용 (2개 작업 = team1, team2만)
- 작업 수 > 5: 5개 팀 순환 사용 후 재할당
- 빈 팀은 호출하지 않음 (불필요한 리소스 낭비 방지)

### **체크리스트 전달 템플릿**
```python
# 체크리스트는 완전한 작업 명세서 - 반드시 경로와 준수 지시 포함
Task("team1-implementer-spark", f"""
작업: {task_name}
체크리스트 위치: {checklist_path}

필수 준수사항:
1. 체크리스트의 9단계를 완전히 따를 것
2. ShellCheck 0 violations 달성 (SC1091, SC2154 제외)
3. 결과를 team1_current_task.json에 기록
4. 품질 기준 미달 시 스스로 수정 후 재검증

{additional_emphasis}  # 2호가 판단하여 추가 강조
""")
```

### **WHEN RECEIVING /multi-implement COMMAND:**

**PHASE 0: Pre-Parallel Setup (필수 사전 준비)**
```python
# 1. 체크리스트 파일 존재 확인
for checklist in checklists:
    assert os.path.exists(checklist), f"Missing: {checklist}"

# 2. 팀별 JSON 초기 구조 생성
for i, task in enumerate(tasks[:5]):  # 최대 5팀
    create_team_json(f"team{i+1}_current_task.json", {
        "task_id": task.id,
        "checklist_path": task.checklist,
        "status": "pending"
    })

# 3. 의존성 검증 (병렬 가능 확인)
validate_no_dependencies(tasks)
```

**PHASE 1: Implementation (병렬 구현)**
```bash
# MUST be in SINGLE MESSAGE - 모든 Task 호출을 한번에:
# 작업 수에 따라 팀 수 조정 (2개 작업 = 2팀만 사용)
Task("team1-implementer-spark", "작업1 + 체크리스트1 경로 + 품질기준")
Task("team2-implementer-spark", "작업2 + 체크리스트2 경로 + 품질기준")
# Task("team3-implementer-spark", ...) # 작업이 3개 이상일 때만
# Task("team4-implementer-spark", ...) # 작업이 4개 이상일 때만
# Task("team5-implementer-spark", ...) # 작업이 5개일 때만

# Wait for ALL teams completion
```

**PHASE 1.5: Implementation Quality Gate**
```python
# 각 팀의 구현 품질 검증
for team in active_teams:
    json_data = read_json(f"{team}_current_task.json")
    if json_data.quality.violations > 0:
        # 즉시 재작업 지시 (특히 ShellCheck)
        Task(f"{team}-implementer-spark", """
        ShellCheck violations 발견! 반드시 수정:
        - 현재 violations: {violations}
        - 목표: 0 violations
        재작업 후 JSON 업데이트
        """)
```

**PHASE 2: Testing (병렬 테스트)**
```bash
# 구현 품질 통과 후에만 진행
Task("team1-tester-spark", "작업1 테스트 - 95% coverage 필수")
Task("team2-tester-spark", "작업2 테스트 - 95% coverage 필수")
# ... (활성 팀 수만큼)

# Wait for ALL teams completion
```

**PHASE 3: Documentation (병렬 문서화)**
```bash
# 테스트 통과 후에만 진행
Task("team1-documenter-spark", "작업1 문서화 - API/사용자/개발자 문서")
Task("team2-documenter-spark", "작업2 문서화 - API/사용자/개발자 문서")
# ... (활성 팀 수만큼)

# Wait for ALL teams completion
```

**PHASE 4: Final Integration Validation**
```python
# 모든 팀 JSON 검증
results = []
for team in active_teams:
    json_data = read_json(f"{team}_current_task.json")
    assert json_data.status == "completed"
    assert json_data.quality.violations == 0
    assert json_data.quality.can_proceed == True
    results.append(json_data.results)

# 통합 충돌 검사
check_no_conflicts(results)
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
