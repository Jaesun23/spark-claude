# SPARK 커맨드 설계 가이드
## 효과적인 커맨드 생성을 위한 상세 표준

**소속**: SPARK 헌법 v1.2
**핵심 문서**: 기본 원칙은 **1_CONSTITUTION_ko.md** 참조
**최종 업데이트**: 2025-10-30

이 가이드는 **Article III: 커맨드 설계 표준**을 상세 명세, 예시, 모범 사례로 확장합니다.

---

## 목차

1. [오케스트레이션 책임](#section-31-오케스트레이션-책임)
2. [검증 프로토콜](#section-32-검증-프로토콜)
3. [재시도 전략](#section-33-재시도-전략)
4. [멀티 세션 관리](#section-34-멀티-세션-관리)

---

## Section 3.1: 오케스트레이션 책임

### 지휘자 원칙

커맨드는 에이전트를 오케스트레이션하며, 작업을 수행하지 않음.

**핵심 비유**: 커맨드는 오케스트라를 이끄는 지휘자와 같음:
- 지휘자는 악기를 연주하지 않음 (에이전트가 작업 수행)
- 지휘자는 타이밍과 순서를 조율함 (오케스트레이션)
- 지휘자는 연주의 품질을 보장함 (검증)
- 지휘자는 발생하는 문제를 처리함 (재시도 로직)

### 커맨드 파일 구조

**표준 템플릿**:

```markdown
---
name: spark-design
description: 검증 및 멀티 세션 지원이 있는 시스템 아키텍처 설계
---

# /spark-design 커맨드

## 2号 오케스트레이션 프로토콜

### 1. 초기 평가
[기존 상태 확인, 재개 또는 새로 시작]

### 2. 에이전트 호출
[요구사항과 함께 designer-spark 호출]

### 3. 검증
[완료 기준에 대해 current_task.json 확인]

### 4. 재시도 로직
[검증 실패 시 피드백 제공하고 재시도]

### 5. 멀티 세션 관리
[필요시 세션 간 진행 추적]

### 6. 보고
[사용자에게 결과 알림]
```

### 필수 요소

모든 커맨드는 이 섹션들을 포함해야 함:

#### 1. 초기 평가

**목적**: 새 작업인지 계속인지 확인

**확인할 것**:
- 상태 파일이 존재하는가?
- 멀티 세션 계속인가?
- 재개할 부분 결과가 있는가?

**예시**:
```python
# 기존 상태 확인
state_file = "~/.claude/workflows/design_state.yaml"

if exists(state_file):
    print("📂 기존 작업 발견. 재개 중...")
    state = load_yaml(state_file)
    # 재개 로직
else:
    print("🆕 새 설계 작업 시작...")
    # 새 작업 로직
```

#### 2. 에이전트 호출

**목적**: 명확한 요구사항과 함께 적절한 에이전트 호출

**포함할 것**:
- 작업 설명
- 프로젝트 컨텍스트 (표준, 아키텍처 문서)
- 사용할 표준 모듈
- 예상 산출물
- 품질 요구사항

**예시**:
```python
Task("designer-spark", f"""
{feature_name}을 위한 RESTful API 설계.

📋 프로젝트 표준 (먼저 읽기):
- {PROJECT_ROOT}/PROJECT_STANDARDS.md
- {PROJECT_ROOT}/ARCHITECTURE.md

🏗️ 표준 모듈:
- common/errors/ → 에러 응답
- common/validation/ → 입력 검증

📦 예상 산출물:
- OpenAPI 명세
- 데이터 모델 다이어그램
- API 엔드포인트 문서

⚠️ 품질 요구사항:
- 모든 엔드포인트 문서화됨
- 에러 케이스 커버됨
- 검증 규칙 명시됨
""")
```

#### 3. 검증

**목적**: 에이전트가 실제로 작업을 성공적으로 완료했는지 검증

**확인할 것**:
- 상태 파일에 "completed" 상태 표시
- 품질 게이트 통과 (can_proceed == true)
- 위반 사항이 0
- 에이전트별 기준 충족

**예시**:
```python
def validate_completion():
    state = read_json("~/.claude/workflows/current_task.json")

    if state["state"]["status"] != "completed":
        return False, "에이전트가 완료하지 않음"

    if not state["quality"]["can_proceed"]:
        return False, "품질 게이트 실패"

    if state["quality"]["violations_total"] != 0:
        return False, f"{violations}개 위반 남음"

    return True, "성공"
```

#### 4. 재시도 로직

**목적**: 점점 구체적인 피드백으로 실패 처리

**전략**:
- 시도 1: 일반적 상기
- 시도 2: 구체적 이슈 나열
- 시도 3: 명시적 수정 지시
- 3회 후: 사용자에게 에스컬레이션

#### 5. 멀티 세션 관리 (해당하는 경우)

**목적**: 여러 세션에 걸친 큰 작업 지원

**추적할 것**:
- 완료된 세션 vs 계획된 세션
- 진행률 퍼센티지
- 누적 발견 사항
- 다음 세션 초점

#### 6. 사용자 소통

**목적**: 사용자에게 진행 상황 알림

**보고할 것**:
- 작업 시작
- 진행 업데이트
- 완료 상태
- 다음 단계 (멀티 세션인 경우)

### 금지된 내용

커맨드는 다음을 포함해서는 안 됨:

#### ❌ 에이전트 작업

```markdown
# ❌ 잘못됨 - 커맨드가 에이전트 작업 수행
def implement_feature():
    # 여기 코드 작성...
    code = generate_implementation()
    write_file("src/feature.py", code)
```

**왜 잘못됐나**: 이것은 implementer-spark의 일이지 커맨드의 일이 아님.

#### ❌ 에이전트 특성 정의

```markdown
# ❌ 잘못됨 - 에이전트 특성 정의
구현자로서 당신의 특성:
- 단순성 우선
- 구조적 무결성
```

**왜 잘못됐나**: 특성은 에이전트 정의에 속하지 커맨드에 속하지 않음.

#### ❌ 에이전트 Phase 로직

```markdown
# ❌ 잘못됨 - 에이전트 phase 중복
Phase 1: 증거 수집
Phase 2: 패턴 분석
Phase 3: 종합
```

**왜 잘못됐나**: Phase 로직은 에이전트에 속하고, 커맨드는 오케스트레이션만 함.

### 커맨드 예시

#### 예시 1: 단순 단일 에이전트 커맨드

```markdown
---
name: spark-analyze
description: 증거 수집이 있는 시스템 분석
---

# /spark-analyze 커맨드

## 1. 초기 평가

기존 분석 상태 확인.

## 2. 에이전트 호출

사용자 요구사항과 함께 analyzer-spark 호출:
- 프로젝트 컨텍스트 포함
- 분석 차원 지정
- 깊이와 범위 정의

## 3. 검증

검증:
- 분석 완료
- 증거 수집됨 (최소 12개 항목)
- 품질 게이트 통과

## 4. 재시도 로직

검증 실패 시:
- 시도 1: "증거 수집 완료"
- 시도 2: "다음에서 증거 누락: {dimensions}"
- 시도 3: "각 발견에 대해 file:line 수집"

## 5. 보고

표시:
- 증거 개수
- 분석된 차원
- 주요 발견 요약
```

#### 예시 2: 다중 에이전트 체인 커맨드

```markdown
---
name: spark-launch
description: 완전한 기능 출시 (설계 → 구현 → 테스트 → 문서화)
---

# /spark-launch 커맨드

## 1. 초기 평가

체인 진행 확인.

## 2. 에이전트 체인 호출

순서대로 실행:
1. designer-spark → 아키텍처
2. implementer-spark → 코드
3. tester-spark → 테스트
4. documenter-spark → 문서

각 에이전트 후 진행 전에 검증.

## 3. 체인 검증

각 에이전트 후:
- 완료 확인
- 품질 검증
- 산출물 확인

현재가 통과한 경우에만 다음 에이전트로 진행.

## 4. 체인 재시도 로직

에이전트 실패 시:
- 해당 특정 에이전트 재시도 (최대 3회)
- 여전히 실패 시 체인 일시 중지
- 어떤 에이전트가 실패했는지 사용자에게 보고

## 5. 보고

표시:
- 체인 진행 (4개 중 2개 에이전트 완료)
- 현재 에이전트 상태
- 전체 성공/실패
```

---

## Section 3.2: 검증 프로토콜

### 신뢰하되 검증하라 원칙

에이전트는 완료를 주장하고, 커맨드는 진실을 검증함.

**철학**: 에이전트는 신뢰할 만하지만 검증은 필수. 이것은 불신에 관한 것이 아니라 체계적 검증에 관한 것.

### 검증 체크리스트

**완전한 검증 함수**:

```python
def validate_agent_completion(agent_name: str) -> tuple[bool, str]:
    """
    에이전트가 실제로 작업을 성공적으로 완료했는지 검증.

    Returns:
        (success, message): 검증 통과 시 True, 설명과 함께
    """

    # 1. 상태 파일 읽기
    try:
        state = read_json("~/.claude/workflows/current_task.json")
    except FileNotFoundError:
        return False, "상태 파일 찾을 수 없음"

    # 2. 완료 상태 확인
    if state["state"]["status"] != "completed":
        status = state["state"]["status"]
        return False, f"상태가 '{status}'이며 'completed'가 아님"

    # 3. 품질 게이트 확인
    if not state["quality"]["can_proceed"]:
        return False, "품질 게이트 통과하지 않음"

    # 4. 위반 확인
    violations = state["quality"]["violations_total"]
    if violations != 0:
        return False, f"{violations}개 위반 남음"

    # 5. 에이전트별 검증
    if agent_name == "implementer-spark":
        # 테스트 결과 있어야 함
        coverage = state["quality"]["step_6_testing"]["coverage"]
        if coverage < 0.95:
            return False, f"커버리지 {coverage:.1%} < 95%"

        # 테스트 실패 0이어야 함
        if state["quality"]["step_6_testing"].get("failures", 0) != 0:
            return False, "테스트 실패 중"

    elif agent_name == "analyzer-spark":
        # 증거 있어야 함
        evidence_count = state.get("evidence_count", 0)
        if evidence_count < 8:
            return False, f"{evidence_count}개 증거만 (8개 이상 필요)"

    elif agent_name == "tester-spark":
        # 100% 테스트 통과율 있어야 함
        if state["quality"].get("test_pass_rate", 0) != 1.0:
            return False, "모든 테스트가 통과하지 않음"

    elif agent_name == "documenter-spark":
        # 100% API 커버리지 있어야 함
        if state["quality"].get("api_coverage", 0) != 1.0:
            return False, "모든 API가 문서화되지 않음"

    # 모든 확인 통과
    return True, "검증 성공"
```

### 검증 시행 규칙

**커맨드 필수**:
- 모든 에이전트 호출 후 검증
- 검증 실패 시 진행하지 않음
- 재시도 시도에 대해 구체적 피드백 제공
- 보편적 및 에이전트별 기준 모두 확인

**커맨드 금지**:
- "이번만" 검증 건너뛰기
- 부분 성공으로 진행
- 검증 없이 에이전트 주장 신뢰
- 품질 게이트 실패 무시

### 검증 에러 처리

**검증 실패 시**:

```python
success, message = validate_agent_completion(agent_name)

if not success:
    print(f"❌ 검증 실패: {message}")

    # 재시도 횟수 확인
    if retry_count < 3:
        # 피드백 제공하고 재시도
        feedback = generate_retry_feedback(message, retry_count)
        Task(agent_name, feedback)
        retry_count += 1
    else:
        # 사용자에게 에스컬레이션
        print(f"⚠️ 에이전트가 3회 시도 후 실패")
        print(f"마지막 에러: {message}")
        print(f"수동 개입 필요")
        return False
```

---

## Section 3.3: 재시도 전략

### 지속성 원칙

실패는 일시적, 성공은 필수.

**철학**: 대부분의 실패는 더 나은 피드백으로 수정 가능. 점진적 구체성을 가진 체계적 재시도는 보통 성공함.

### 재시도 결정 트리

**완전한 재시도 핸들러**:

```python
def handle_agent_failure(
    agent_name: str,
    attempt: int,
    max_attempts: int = 3
) -> bool:
    """
    학습을 통한 체계적 재시도.

    Args:
        agent_name: 실패한 에이전트 이름
        attempt: 현재 시도 번호 (0부터 시작)
        max_attempts: 허용되는 최대 재시도

    Returns:
        재시도해야 하면 True, 에스컬레이션해야 하면 False
    """

    if attempt >= max_attempts:
        report_failure_to_user(agent_name, attempt)
        return False

    # 실패 분석
    state = read_json("~/.claude/workflows/current_task.json")
    violations = state["quality"]["violations_total"]
    issues = identify_specific_issues(state)

    # 시도 번호에 따라 피드백 생성
    if attempt == 0:
        # 첫 재시도: 일반적 피드백
        feedback = f"""
        재시도 {max_attempts}회 중 1회

        이전 시도가 검증 실패.

        다음을 수행하세요:
        - 품질 요구사항 검토
        - 모든 위반 수정
        - 품질 확인 재실행
        - 모든 품질 게이트 통과 검증
        """

    elif attempt == 1:
        # 두 번째 재시도: 구체적 이슈
        feedback = f"""
        재시도 {max_attempts}회 중 2회

        이전 시도가 {violations}개 위반으로 실패:

        {format_issues_list(issues)}

        요구사항:
        - 각 이슈를 개별적으로 수정
        - 자동 스크립트 사용 안 함
        - 수동, 신중한 수정
        - 각 수정 후 검증
        """

    else:
        # 세 번째 재시도: 명시적 지시
        feedback = f"""
        재시도 {max_attempts}회 중 3회 - 최종 시도

        여전히 {violations}개 위반 남음.

        단계별 지시:
        1. 위반 읽기: {issues[0]}
        2. 근본 원인 이해
        3. 수동으로 수정 (자동 스크립트 사용 안 함)
        4. 품질 확인 실행
        5. 위반 사라진 것 검증
        6. 다음 위반 반복

        violations_total == 0이 될 때까지 완료 보고하지 마세요

        이것이 마지막 시도입니다. 제대로 수정할 시간을 가지세요.
        """

    # 피드백과 함께 재시도
    print(f"🔄 {agent_name} 재시도 중 ({max_attempts}회 중 {attempt + 1}회 시도)")
    Task(agent_name, feedback)
    return True
```

### 재시도 가이드라인

**점진적 피드백**:

| 시도 | 피드백 레벨 | 예시 |
|---------|----------------|---------|
| 1차 | 일반적 | "위반 수정하고 품질 확인 재실행" |
| 2차 | 구체적 | "이 5개 구체적 이슈 수정: [목록]" |
| 3차 | 명시적 | "Step 1: 45번 줄 수정. Step 2: 67번 줄 수정. ..." |

**진전 검증**:

각 재시도는 진전을 보여야 함:

```python
def verify_retry_progress(
    previous_violations: int,
    current_violations: int
) -> bool:
    """재시도가 진전을 만들었는지 검증."""

    if current_violations == 0:
        return True  # 성공!

    if current_violations < previous_violations:
        return True  # 진전 있음

    if current_violations >= previous_violations:
        return False  # 진전 없거나 악화
```

**진전 없는 예시**:

```
시도 1: 157개 위반
시도 2: 203개 위반 (악화 - 자동 스크립트가 더 많은 이슈 발생)
시도 3: 189개 위반 (여전히 진전 없음)
→ 사용자에게 에스컬레이션
```

**좋은 진전 예시**:

```
시도 1: 157개 위반 → 수동 수정
시도 2: 89개 위반 (진전 - 68개 수정)
시도 3: 0개 위반 (성공!)
```

### 에스컬레이션 프로토콜

**최대 시도 초과 후**:

```python
def report_failure_to_user(agent_name: str, attempts: int):
    """수동 개입을 위해 사용자에게 실패 보고."""

    state = read_json("~/.claude/workflows/current_task.json")
    violations = state["quality"]["violations_total"]

    print(f"""
    ⚠️ {agent_name}이(가) {attempts}회 시도 후 실패

    최종 상태:
    - 상태: {state['state']['status']}
    - 위반: {violations}
    - 진행 가능: {state['quality']['can_proceed']}

    남은 이슈:
    {format_remaining_issues(state)}

    수동 개입 필요:
    1. 상태 파일 검토: ~/.claude/workflows/current_task.json
    2. 구체적 위반 분석
    3. 수동으로 수정하거나 요구사항 조정
    4. 재시도하려면 커맨드 재실행

    가능한 행동:
    - 수동으로 이슈 수정하고 재시도
    - 품질 요구사항 조정
    - 에이전트 정의의 버그 보고
    - Jason에게 에스컬레이션
    """)
```

---

## Section 3.4: 멀티 세션 관리

### 연속성 원칙

큰 작업은 세션에 걸쳐 있으며, 상태는 지속되어야 함.

**사용 사례**:
- 대형 코드베이스 분석 (> 100K 토큰)
- 복잡한 다단계 구현
- 종합 문서화 프로젝트
- 며칠간의 기능 개발

### 멀티 세션 프로토콜

#### 상태 파일 구조

**위치**: `~/.claude/workflows/{agent}_state.yaml`

**구조**:

```yaml
# 멀티 세션 작업을 위한 상태 파일

analysis_id: "analyzer_20251028_143022"
version: "4.3"
sessions_planned: 3
sessions_completed: 1

progress:
  overall_percentage: 33
  components_completed: 12
  total_components: 36

last_session_summary: "Phase 1-2 완료: 156개 파일 발견, 89개 증거 항목 수집"

next_session:
  session: 2
  focus: "보안 및 성능 차원의 깊은 분석"
  priority: ["security_deep_dive", "performance_bottlenecks"]
  estimated_tokens: 45000

cumulative_findings:
  - category: "architecture"
    count: 23
    severity: "medium"
  - category: "performance"
    count: 15
    severity: "high"

key_findings:
  - "Critical: 15개 N+1 쿼리 패턴 발견"
  - "High: 8개 관리자 엔드포인트에 인증 없음"
  - "Medium: 23개 순환 import 감지"
```

#### 커맨드의 세션 관리

**완전한 멀티 세션 핸들러**:

```python
def manage_multi_session(
    agent_name: str,
    user_request: str,
    state_file: str
) -> str:
    """
    멀티 세션 계속 처리.

    Returns:
        사용자를 위한 상태 메시지
    """

    if exists(state_file):
        # 기존 작업 재개
        state = load_yaml(state_file)
        session = state['sessions_completed'] + 1
        total = state['sessions_planned']

        print(f"📂 {agent_name} 재개 중 (세션 {total}개 중 {session})")
        print(f"진행: {state['progress']['overall_percentage']}%")
        print(f"컴포넌트: {state['progress']['total_components']}개 중 {state['progress']['components_completed']}개")
        print(f"\n마지막 세션: {state['last_session_summary']}")
        print(f"다음 초점: {state['next_session']['focus']}")

        # 컨텍스트와 함께 계속
        Task(agent_name, f"""
        저장된 상태에서 계속:

        세션: {total}개 중 {session}
        상태 파일: {state_file}

        이전 진행:
        {state['last_session_summary']}

        누적 발견:
        {format_findings(state['cumulative_findings'])}

        이 세션 초점:
        {state['next_session']['focus']}

        우선순위:
        {format_list(state['next_session']['priority'])}

        중단했던 곳에서 계속하고 진행으로 상태 파일 업데이트.
        """)
    else:
        # 새 멀티 세션 작업
        print(f"🆕 새 {agent_name} 작업 시작")
        print(f"요청: {user_request}")

        Task(agent_name, f"""
        새 멀티 세션 작업:

        요청: {user_request}
        상태 파일: {state_file}

        한 세션에 너무 크면:
        1. 전체 범위 평가
        2. 세션 분해 계획
        3. 계획으로 상태 파일 생성
        4. 이 세션에서 가능한 것 완료
        5. 상태 파일에 진행 저장

        그렇지 않으면 이 세션에서 완료.
        """)

    # 완료 대기
    wait_for_agent_completion()

    # 더 많은 세션 필요한지 확인
    if exists(state_file):
        state = load_yaml(state_file)

        if state['sessions_completed'] < state['sessions_planned']:
            remaining = state['sessions_planned'] - state['sessions_completed']
            return f"""
            ⚠️ 멀티 세션 작업 진행 중

            완료된 세션: {state['sessions_planned']}개 중 {state['sessions_completed']}개
            진행: {state['progress']['overall_percentage']}%

            계속하려면:
            /{command_name} --continue

            예상 남은 세션: {remaining}
            """
        else:
            return """
            ✅ 모든 세션 완료!

            멀티 세션 작업이 성공적으로 완료됨.
            최종 보고서에서 누적 발견 검토.
            """
    else:
        return """
        ✅ 작업 완료!

        단일 세션에서 완료됨.
        """
```

#### 세션 계속

**사용자 경험**:

```bash
# 첫 세션
$ /spark-analyze large-codebase
📊 대형 코드베이스 분석 중...
⚠️ 멀티 세션 작업 필요 (3개 세션 예상)
세션 1/3 완료 (33% 진행)

계속하려면: /spark-analyze --continue

# 두 번째 세션
$ /spark-analyze --continue
📂 analyzer-spark 재개 중 (세션 2/3)
진행: 33%
마지막 세션: Phase 1-2 완료
...
세션 2/3 완료 (67% 진행)

계속하려면: /spark-analyze --continue

# 세 번째 세션
$ /spark-analyze --continue
📂 analyzer-spark 재개 중 (세션 3/3)
진행: 67%
...
✅ 모든 세션 완료!
```

#### 요구사항

멀티 세션 지원은 다음을 보장해야 함:

1. **상태 지속성**: 상태 파일이 세션 간에 유지됨
2. **진행 추적**: 완료 비율의 명확한 표시
3. **원활한 계속**: 사용자가 쉽게 재개 가능
4. **최종 종합**: 마지막 세션이 모든 이전 작업 통합
5. **정리**: 성공적 완료 후 상태 파일 삭제

#### 상태 파일 정리

```python
def cleanup_completed_state(state_file: str):
    """성공적 완료 후 상태 파일 제거."""

    if exists(state_file):
        state = load_yaml(state_file)

        if state['sessions_completed'] >= state['sessions_planned']:
            # 모든 세션 완료, 삭제 안전
            os.remove(state_file)
            print(f"🗑️ 상태 파일 정리됨: {state_file}")
```

---

## 요약

이 가이드는 효과적인 SPARK 커맨드 생성을 위한 상세 명세 제공:

1. **오케스트레이션**: 커맨드는 에이전트를 조율하며, 그들의 작업을 하지 않음
2. **검증**: 신뢰하되 검증 - 각 에이전트 후 체계적 검증
3. **재시도**: 3회 시도에 걸친 점진적 피드백
4. **멀티 세션**: 여러 세션에 걸친 큰 작업 지원

**핵심 원칙**: 커맨드는 지휘자이지 연주자가 아님. 오케스트라(에이전트)가 조화롭게 연주하도록 보장함.

---

**관련 문서**:
- **1_CONSTITUTION_ko.md** - 핵심 원칙
- **2_AGENT_DESIGN_GUIDE_ko.md** - 에이전트 설계 표준
- **4_INTEGRATION_GUIDE_ko.md** - 통합 표준
- **5_TEMPLATES_ko.md** - 빠른 시작 템플릿
