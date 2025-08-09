# 🚀 SPARK 올바른 구현 계획서 v3.0
## SuperClaude 100% 성능 재현을 위한 완전한 아키텍처 가이드

> **작성일**: 2025-08-09  
> **작성자**: Claude Code (2호)  
> **통합 내용**: 페르소나 시스템, 병렬 실행, Hook 정확성
> **목표**: SuperClaude 모든 기능 100% 재현 with 올바른 이해

---

## 📌 핵심 아키텍처 이해

### ✅ 올바른 아키텍처 (v3.0 최종)
- **사용자** → `자연어 요청` → **2호(Claude Code)** → `Task 도구` → **서브에이전트**
- 서브에이전트는 2호가 호출하는 전문가 도구
- 메인 에이전트(2호) 정지 → 서브에이전트 활성 → 완료 후 제어 복귀

## 🎯 **SPARK 분산 지능 아키텍처의 핵심 철학**

### 💡 **혁신적 역할 분담의 진실**

#### **2호(Claude Code) = 진정한 오케스트레이터** 🎼
```yaml
SuperClaude 모든 기능을 2호가 담당:
  🎭 사용자와 대화형 상호작용 (질문, 확인, 설명)
  🧠 컨텍스트 이해하고 의도 파악
  🎯 "어떤 전문가가 필요할까?" 지능적 판단
  🎨 "어떤 페르소나로 작동시킬까?" 결정 및 주입
  📦 "어떤 정보를 줘야 할까?" 컨텍스트 완벽 패키징
  📊 서브에이전트 결과 해석하고 사용자에게 명확히 설명
  🔄 추가 작업 필요시 다른 서브에이전트 연쇄 호출
```

#### **서브에이전트 = 고도화된 전문 도구** 🔧
```yaml
"One-shot completion tool"의 정체성:
  ⚡ 입력 받고 → 독립적 처리 → 완성된 출력 반환
  🎭 2호가 주입한 페르소나로 충실히 작동
  🚫 대화 불가 (2호 정지 상태)
  🚫 질문 불가 (추가 정보 요청 불가능)
  🚫 의도 해석 불가 (2호가 모든 해석 완료)
  ✅ 주어진 컨텍스트와 페르소나만으로 완벽 처리
  ✅ "원샷 완성형" 결과 제공
```

### 🔑 **페르소나 시스템 - AI 동기부여의 핵심**

#### **문제와 해결**
```yaml
초기 에이전트의 실패 원인:
  - 강력한 기준과 워크플로우 존재
  - 하지만 AI "지루함" 발생
  - 기계적 실행으로 품질 저하
  
SuperClaude의 천재적 해결책:
  - 작업(task)을 정체성(identity)으로 변환
  - 11개 페르소나로 AI에게 동기 부여
  - "복잡미묘함" 완전 보존 필수
```

#### **페르소나 주입 메커니즘**
```python
# 2호가 Task 호출 시
Task(
    subagent_type="implementer-spark",
    description="API implementation",
    prompt="""
[PERSONA: backend]
[PRIORITY: reliability > security > performance]
[QUALITY: strict]

구체적 작업: 사용자 인증 API 구현
위치: src/api/auth/
요구사항: JWT, rate limiting
"""
)

# 서브에이전트가 페르소나 수신
def activate_persona(prompt):
    if "[PERSONA: backend]" in prompt:
        # backend 페르소나로 변신
        self.identity = "신뢰성 엔지니어, API 전문가"
        self.priorities = ["reliability", "security", "performance"]
        self.approach = backend_specific_patterns
```

---

## 📋 목차

1. [페르소나 시스템 완전 가이드](#1-페르소나-시스템-완전-가이드)
2. [병렬 실행 시스템](#2-병렬-실행-시스템)
3. [Hook 시스템 정확한 구현](#3-hook-시스템-정확한-구현)
4. [서브에이전트 구현 표준](#4-서브에이전트-구현-표준)
5. [4단계 구현 로드맵](#5-4단계-구현-로드맵)
6. [검증 및 테스트 계획](#6-검증-및-테스트-계획)

---

## 1. 페르소나 시스템 완전 가이드

### 🎭 11개 SuperClaude 페르소나 완전 명세

#### 1.1 페르소나 정의 구조
```yaml
각 페르소나 필수 요소:
  identity: 정체성과 핵심 역할
  priorities: 우선순위 체계
  approach: 구체적 행동 패턴
  quality_standards: 품질 기준
  mcp_preferences: 선호 MCP 서버
```

#### 1.2 페르소나별 상세 정의

##### **Backend 페르소나**
```yaml
identity: "신뢰성 엔지니어, API 전문가, 데이터 무결성 수호자"
priorities: "reliability > security > performance > features"
approach:
  - 모든 엔드포인트에 철저한 에러 핸들링
  - 트랜잭션 보장 및 롤백 메커니즘
  - 상세한 로깅과 모니터링
quality_standards:
  - 99.9% uptime 목표
  - <200ms 응답 시간
  - ACID 준수
mcp_preferences: ["Context7", "Sequential"]
```

##### **Frontend 페르소나**
```yaml
identity: "UX 전문가, 접근성 옹호자, 성능 최적화 마스터"
priorities: "user_experience > accessibility > performance > aesthetics"
approach:
  - 모바일 우선 반응형 디자인
  - WCAG 2.1 AA 준수
  - 번들 크기 최적화
quality_standards:
  - Core Web Vitals 달성
  - 90% 이상 접근성 점수
  - <3초 초기 로드
mcp_preferences: ["Magic", "Playwright"]
```

##### **Security 페르소나**
```yaml
identity: "보안 전문가, 취약점 헌터, 제로 트러스트 설계자"
priorities: "security > compliance > reliability > convenience"
approach:
  - 모든 입력 검증 및 살균
  - 최소 권한 원칙
  - 암호화 우선
quality_standards:
  - OWASP Top 10 방어
  - 제로 취약점
  - 완전한 감사 로그
mcp_preferences: ["Sequential", "Context7"]
```

##### **Architect 페르소나**
```yaml
identity: "시스템 설계자, 장기 사고, 확장성 전문가"
priorities: "scalability > maintainability > performance > features"
approach:
  - 도메인 주도 설계
  - 마이크로서비스 패턴
  - 이벤트 기반 아키텍처
quality_standards:
  - 10x 성장 대응 가능
  - 명확한 경계와 계약
  - 기술 부채 최소화
mcp_preferences: ["Sequential", "Context7"]
```

[나머지 7개 페르소나도 동일한 구조로 정의...]

### 🔧 페르소나 매핑 규칙 (CLAUDE.md 추가용)

```markdown
## 서브에이전트 페르소나 자동 매핑

### 기본 매핑 규칙
- API, endpoint, service → [PERSONA: backend]
- component, UI, responsive → [PERSONA: frontend]
- auth, vulnerability, encryption → [PERSONA: security]
- architecture, design, scalability → [PERSONA: architect]
- test, coverage, validation → [PERSONA: qa]
- optimize, performance, bottleneck → [PERSONA: performance]

### 복합 페르소나 패턴
- "secure API" → backend + security
- "responsive dashboard" → frontend + performance
- "scalable architecture" → architect + performance

### Task 호출 템플릿
```
Task(subagent_type, f"""
[PERSONA: {primary}]
[SECONDARY: {secondary}]
[PRIORITY: {priorities}]
[QUALITY: strict]

{task_description}
""")
```
```

---

## 2. 병렬 실행 시스템

### ⚡ 병렬 Task 호출의 실제

#### 2.1 가능한 것과 제약
```yaml
가능한 것:
  ✅ Task 도구 동시 호출 (최대 4개)
  ✅ Hook으로 자동 팀 배분
  ✅ JSON 릴레이 통신
  ✅ Lock 메커니즘으로 충돌 방지
  
제약사항:
  ⚠️ 각 팀은 순차 작업 (Task A → Task B)
  ⚠️ 가장 느린 팀 기준으로 종료
  ⚠️ 중간 개입 불가능
  ⚠️ 2호는 모든 팀 완료까지 정지
```

#### 2.2 최적 작업 배분 전략
```python
def optimize_task_distribution(tasks):
    """각 팀의 총 작업 시간 균등화"""
    
    # 작업 시간 추정
    estimated_times = [estimate_time(task) for task in tasks]
    
    # 팀 배분 (예: 3개 팀)
    team1_tasks = []  # 목표: 20분
    team2_tasks = []  # 목표: 20분
    team3_tasks = []  # 목표: 20분
    
    # 균등 배분 알고리즘
    for task, time in sorted(zip(tasks, estimated_times), 
                            key=lambda x: x[1], reverse=True):
        # 가장 작업 시간이 적은 팀에 할당
        min_team = min([team1_tasks, team2_tasks, team3_tasks], 
                      key=lambda t: sum(t))
        min_team.append((task, time))
    
    return team1_tasks, team2_tasks, team3_tasks
```

#### 2.3 JSON 릴레이 시스템
```json
// team1_current_task.json
{
  "team_id": "team1",
  "tasks": ["TASK-API-01", "TASK-API-03"],
  "current_status": "in_progress",
  "persona": "backend",
  "completed": [],
  "quality_results": {},
  "locks_held": ["constants.py"],
  "estimated_completion": "20min"
}
```

#### 2.4 Lock 메커니즘
```python
# file_lock_manager.py 활용
class FileLockManager:
    def __init__(self):
        self.locks = {}
    
    def acquire_lock(self, file_path, team_id):
        if file_path not in self.locks:
            self.locks[file_path] = team_id
            return True
        return False
    
    def release_lock(self, file_path, team_id):
        if self.locks.get(file_path) == team_id:
            del self.locks[file_path]
            return True
        return False
```

---

## 3. Hook 시스템 정확한 구현

### 🪝 Anthropic 공식 Hook 이벤트 (8개)

#### 3.1 유효한 Hook 이벤트
```python
VALID_HOOK_EVENTS = [
    "PreToolUse",       # 도구 사용 전
    "PostToolUse",      # 도구 사용 후
    "UserPromptSubmit", # 사용자 입력 시
    "Stop",            # 세션 종료
    "SubagentStop",    # 서브에이전트 종료
    "PreCompact",      # 압축 전
    "SessionStart",    # 세션 시작
    "Notification"     # 알림
]

# ❌ 존재하지 않는 이벤트
# SubagentStart → PreToolUse 사용
```

#### 3.2 Hook 구현 예시

##### UserPromptSubmit - 페르소나 결정 및 라우팅
```python
#!/usr/bin/env python3
"""사용자 요청 시 페르소나 결정 및 서브에이전트 라우팅"""

import json
import sys

def determine_persona_and_route(prompt):
    """2호를 위한 페르소나 결정 및 라우팅 가이드"""
    
    # 키워드 기반 페르소나 매핑
    if any(kw in prompt for kw in ["API", "endpoint", "service"]):
        persona = "backend"
        agent = "implementer-spark"
    elif any(kw in prompt for kw in ["component", "UI", "responsive"]):
        persona = "frontend"
        agent = "implementer-spark"
    elif any(kw in prompt for kw in ["analyze", "review", "investigate"]):
        persona = "analyzer"
        agent = "analyzer-spark"
    else:
        persona = "generic"
        agent = "implementer-spark"
    
    # 복잡도 추정
    complexity = estimate_complexity(prompt)
    
    # 보조 페르소나 추가
    secondary = []
    if complexity > 0.7:
        secondary.append("architect")
    if "security" in prompt or "auth" in prompt:
        secondary.append("security")
    
    return {
        "primary_persona": persona,
        "secondary_personas": secondary,
        "recommended_agent": agent,
        "complexity": complexity
    }

def main():
    hook_data = json.load(sys.stdin)
    prompt = hook_data.get('prompt', '')
    
    routing = determine_persona_and_route(prompt)
    
    # 2호에게 전달할 컨텍스트
    response = {
        'continue': True,
        'additionalContext': {
            'spark_routing': routing,
            'suggested_task_call': f"""
Task("{routing['recommended_agent']}", \"\"\"
[PERSONA: {routing['primary_persona']}]
[SECONDARY: {', '.join(routing['secondary_personas'])}]
[COMPLEXITY: {routing['complexity']}]

{prompt}
\"\"\")
"""
        }
    }
    
    print(json.dumps(response))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

##### PreToolUse/PostToolUse - Task 추적 및 Lock 관리
```python
#!/usr/bin/env python3
"""Task 도구 호출 시 Lock 관리 및 JSON 생성"""

def handle_pre_tool_use(event):
    if event['tool_name'] == 'Task':
        # 병렬 호출 감지
        if is_parallel_call(event):
            # 팀별 JSON 생성
            create_team_json_files(event['parameters'])
            # Lock 초기화
            initialize_locks()

def handle_post_tool_use(event):
    if event['tool_name'] == 'Task':
        # 결과 수집
        collect_results_from_json()
        # Lock 해제
        release_all_locks()
```

---

## 4. 서브에이전트 구현 표준

### 📝 서브에이전트 필수 구조

```markdown
---
name: [agent-name]-spark
description: Use this agent when... [명확한 사용 조건]
tools: Read, Edit, Write, Bash, Grep, Glob, TodoWrite, mcp__sequential-thinking__sequentialthinking, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
model: opus
---

# 🎯 [Agent Name] SPARK Expert

## 중요: 서브에이전트 제약사항
- ❌ Task 도구 사용 불가 (다른 서브에이전트 호출 금지)
- ❌ 사용자 의도 해석 불가 (2호가 이미 완료)
- ✅ 2호가 주입한 페르소나로만 작동
- ✅ 주어진 컨텍스트로 완전한 결과 생성

## MANDATORY: 시작 프로토콜
```python
# 1. 페르소나 파싱 및 활성화
def parse_and_activate_persona(prompt):
    if "[PERSONA: backend]" in prompt:
        activate_backend_mode()
    elif "[PERSONA: frontend]" in prompt:
        activate_frontend_mode()
    # ... 다른 페르소나들
    
# 2. 팀 JSON 읽기 (병렬 실행 시)
if exists("team{N}_current_task.json"):
    team_data = read_json(f"team{N}_current_task.json")
    tasks = team_data['tasks']
    locks = team_data['locks_held']
```

## 페르소나별 행동 패턴
```python
def execute_with_persona():
    if self.persona == "backend":
        # Backend 특화 패턴
        - 모든 API에 에러 핸들링
        - 트랜잭션 보장
        - 성능 메트릭 추가
        
    elif self.persona == "frontend":
        # Frontend 특화 패턴
        - 접근성 검증
        - 반응형 디자인
        - 번들 최적화
```

## MANDATORY: 종료 프로토콜
```python
# 1. 품질 검증
quality_results = run_quality_gates()

# 2. 팀 JSON 업데이트 (병렬 실행 시)
if team_data:
    team_data['completed'].append(task_id)
    team_data['quality_results'] = quality_results
    write_json(f"team{N}_current_task.json", team_data)

# 3. Lock 해제
for lock in locks_held:
    release_lock(lock)

# 4. 결과 반환
return complete_results
```
```

### 🎯 서브에이전트별 페르소나 조합

| 서브에이전트 | 주 페르소나 | 보조 페르소나 (조건부) |
|-------------|-----------|---------------------|
| analyzer-spark | analyzer | architect(복잡도>0.7), security, performance |
| implementer-spark | backend/frontend | security, architect, performance |
| improver-spark | refactorer | performance, architect, qa |
| designer-spark | architect | frontend, backend |
| builder-spark | devops | frontend, backend |
| tester-spark | qa | frontend, backend, performance |
| documenter-spark | scribe | mentor |
| troubleshooter-spark | analyzer | qa, devops |

---

## 5. 4단계 구현 로드맵

### 📅 Phase 1: 기초 시스템 + 페르소나 철학 (Week 1)

#### Day 1-2: 페르소나 시스템 정립
```yaml
작업 내용:
  - 11개 페르소나 완전 명세 작성
  - 페르소나별 행동 패턴 정의
  - "복잡미묘함" 보존 원칙 문서화
  
산출물:
  - personas/backend.yaml
  - personas/frontend.yaml
  - ... (11개 파일)
  - CLAUDE.md에 매핑 규칙 추가
```

#### Day 3-4: Hook 시스템 구현
```yaml
작업 내용:
  - 8개 공식 Hook 이벤트 구현
  - UserPromptSubmit: 페르소나 결정
  - PreToolUse/PostToolUse: Task 추적
  - SubagentStop: 품질 검증
  
산출물:
  - hooks/spark_persona_router.py
  - hooks/spark_task_tracker.py
  - hooks/spark_quality_gates.py
```

#### Day 5-6: 통합 테스트
```yaml
테스트 시나리오:
  - 2호가 페르소나 정확히 주입하는지
  - 서브에이전트가 페르소나대로 작동하는지
  - "One-shot completion" 검증
  
검증 기준:
  - 페르소나 발화 정확도 >90%
  - 품질 게이트 통과율 >95%
```

### 📅 Phase 2: 핵심 서브에이전트 (Week 2)

```yaml
구현 우선순위:
  1. analyzer-spark (가장 빈번)
  2. implementer-spark (핵심 기능)  
  3. improver-spark (품질 향상)
  
각 에이전트 필수 요소:
  - 페르소나 수신 및 활성화
  - SuperClaude 복잡도 공식
  - MCP 서버 자동 선택
  - Jason's 8-step 품질 게이트
  - 병렬 도구 호출 최적화
```

### 📅 Phase 3: 전체 에이전트 완성 (Week 3)

```yaml
나머지 14개 에이전트:
  - designer, builder, tester
  - documenter, troubleshooter, estimator
  - explainer, gitter, cleaner
  - spawner, tasker, loader, indexer
  
병렬 실행 시스템:
  - multi-implement 명령어
  - 팀 배분 알고리즘
  - Lock 메커니즘
  - JSON 릴레이
```

### 📅 Phase 4: 최적화 및 검증 (Week 4)

```yaml
최적화:
  - 토큰 효율성 측정
  - 응답 시간 <200ms
  - 병렬 실행 효율 >60%
  
검증:
  - SuperClaude 기능 100% 재현
  - 페르소나 시스템 완전성
  - 품질 게이트 통과율 >98%
  - Jason 최종 승인
```

---

## 6. 검증 및 테스트 계획

### ✅ 핵심 검증 항목

#### 6.1 페르소나 시스템 검증
```python
def test_persona_injection():
    """2호의 페르소나 주입 정확도"""
    
    test_cases = [
        ("implement user API", "backend"),
        ("create React component", "frontend"),
        ("analyze security issues", "security"),
        ("design system architecture", "architect")
    ]
    
    for prompt, expected_persona in test_cases:
        # 2호가 결정한 페르소나
        actual_persona = determine_persona(prompt)
        assert actual_persona == expected_persona
        
        # 서브에이전트가 받은 페르소나
        task_prompt = create_task_prompt(prompt, actual_persona)
        assert f"[PERSONA: {expected_persona}]" in task_prompt
```

#### 6.2 병렬 실행 검증
```python
def test_parallel_execution():
    """병렬 Task 호출 및 균등 배분"""
    
    tasks = [
        ("Task A", 10),  # 10분
        ("Task B", 15),  # 15분
        ("Task C", 10),  # 10분
        ("Task D", 20),  # 20분
    ]
    
    # 최적 배분
    teams = optimize_distribution(tasks, num_teams=3)
    
    # 각 팀 작업 시간 확인
    team_times = [sum(t[1] for t in team) for team in teams]
    
    # 균등 배분 검증 (차이 <5분)
    assert max(team_times) - min(team_times) < 5
```

#### 6.3 품질 게이트 검증
```python
def test_quality_gates():
    """Jason's 8-step 품질 게이트"""
    
    gates = [
        "Syntax (0 errors)",
        "MyPy --strict (0 errors)",
        "Ruff (0 violations)",
        "Security (0 vulnerabilities)",
        "Coverage (≥95%)",
        "Performance (<200ms)",
        "Documentation (complete)",
        "Integration (working)"
    ]
    
    for gate in gates:
        result = run_quality_check(gate)
        assert result.passed, f"{gate} failed"
```

### 📊 성공 지표

```yaml
필수 달성:
  - 페르소나 정확도: >90%
  - SuperClaude 기능: 100% 재현
  - 품질 게이트: >98% 통과
  - 병렬 효율: >60%
  
성능 목표:
  - 응답 시간: <200ms
  - 토큰 효율: 최적화
  - 에러율: <2%
  
최종 검증:
  - Jason 승인: 필수
  - 사용자 경험: SuperClaude와 동일
```

---

## 📚 결론

### 🎯 v3.0 핵심 개선사항

1. **페르소나 시스템 완전 이해**
   - AI "지루함" 해결의 핵심
   - 2호가 페르소나 주입
   - 서브에이전트는 충실히 수행

2. **병렬 실행 정확한 이해**
   - Task 동시 호출 가능
   - 각 팀은 순차 작업
   - 균등 배분으로 효율 최대화

3. **Hook 시스템 정확성**
   - 8개 공식 이벤트만 사용
   - SubagentStart 없음 → PreToolUse
   - JSON 릴레이 통신

4. **구현 우선순위 재정립**
   - Phase 1: 페르소나 + Hook
   - Phase 2: 핵심 에이전트
   - Phase 3: 전체 완성
   - Phase 4: 최적화

### ✅ 이 계획서의 보장

- **SuperClaude 100% 재현**: 모든 기능 완벽 구현
- **올바른 아키텍처**: 2호 → Task → 서브에이전트
- **페르소나 시스템**: "복잡미묘함" 완전 보존
- **실용적 구현**: 검증된 방법론

이 v3.0 계획서는 우리의 모든 논의와 발견을 통합한 **완전한 구현 가이드**입니다.

---

*작성: Claude Code (2호)*  
*기반: 페르소나 철학 + 병렬 실행 이해 + Hook 정확성*  
*검증: 실제 구현 가능성 100%*