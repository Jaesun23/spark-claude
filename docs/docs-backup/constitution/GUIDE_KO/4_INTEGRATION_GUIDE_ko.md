# SPARK 통합 가이드
## 에이전트-커맨드 통합을 위한 상세 표준

**소속**: SPARK 헌법 v1.2
**핵심 문서**: 기본 원칙은 **1_CONSTITUTION_ko.md** 참조
**최종 업데이트**: 2025-10-30

이 가이드는 **Article IV: 통합 표준**을 상세 명세, 예시, 모범 사례로 확장합니다.

---

## 목차

1. [에이전트 격리 모델](#section-40-에이전트-격리-모델)
2. [JSON 상태 관리](#section-41-json-상태-관리)
3. [에이전트별 증거 요구사항](#section-42-에이전트별-증거-요구사항)
4. [완료 기준](#section-43-완료-기준)

---

## Section 4.0: 에이전트 격리 모델

### 근본적 아키텍처 제약

**핵심 현실**: 에이전트는 2号의 Task 도구로 생성되는 격리된 세션이다. 이 격리는 설계 선택이 아니라 전체 SPARK 아키텍처를 주도하는 기술적 제약이다.

### 기술적 특성

**1. 세션 격리**
- 각 에이전트는 완전히 분리된 실행 컨텍스트에서 실행
- 2号가 `Task("agent-name", "task description")` 호출 시 에이전트 생성
- 2号는 에이전트 완료까지 **차단**(일시정지) 상태
- 에이전트는 2号에게 단일 최종 메시지 반환 후 종료
- 에이전트의 모든 메모리와 컨텍스트는 종료 시 파괴됨

**2. 도구 접근 제한**
- 에이전트는 Task를 제외한 모든 도구에 접근 가능
- 서브에이전트 생성 또는 다른 에이전트 호출 불가
- 실행 중 2号와 통신 불가
- 다른 에이전트와 통신 불가

**3. 실행 흐름**
```
2号 활성 → Task("agent-A") → 2号 일시정지
                                에이전트 A 생성
                                에이전트 A 실행 (격리)
                                에이전트 A JSON 작성
                                에이전트 A 메시지 반환
                                에이전트 A 종료
2号 재개 ← 에이전트 A 메시지 ← 에이전트 A 완료
2号 JSON 상태 읽기
2号 활성 → Task("agent-B") → [순환 반복]
```

### 아키텍처적 함의

이 격리 제약이 특정 설계 결정을 **강제**한다:

#### 1. 유일한 통신 채널로서의 JSON

**문제**: 에이전트가 실행 중 2号나 다른 에이전트와 통신 불가능.

**해결책**: JSON 상태 파일이 유일한 세션 간 통신 메커니즘이 됨.

```
에이전트 → JSON 작성 → 에이전트 종료 → 2号 JSON 읽기
```

**파일 구조**:
- `current_task.json`: 단일 에이전트 실행 상태
- `team[1-5]_current_task.json`: 병렬 에이전트 실행 상태

**데이터 흐름**:
- 에이전트 → JSON: 결과, 증거, 품질 메트릭
- 2号 → JSON: 초기 작업 컨텍스트 (드물게 필요)
- 다음 에이전트 → JSON: 이전 에이전트 결과 읽기 (2号 경유)

#### 2. 필수 오케스트레이터로서의 2号

**문제**: 에이전트가 다른 에이전트를 호출할 수 없음.

**해결책**: 2号가 모든 다중 에이전트 워크플로우를 반드시 조율해야 함.

**패턴**:
```
사용자 요청 → 2号 분석 → 에이전트 시퀀스 결정
2号 → 에이전트 A → 완료 → 2号 검증 → 에이전트 B → 완료 → 2号
```

**커맨드가 존재하는 이유**:
- 2号가 모든 오케스트레이션 프로토콜을 암기할 수 없음
- 커맨드가 사전 정의된 다중 에이전트 시퀀스 제공
- 커맨드가 검증 및 재시도 로직 인코딩
- 예시: `/spark-implement`는 analyze → design → implement → test → document 조율

#### 3. 종료 전 증거 수집

**문제**: 에이전트 종료 후 2号가 주장 검증 불가능.

**해결책**: 에이전트가 완료 **전에** 증거(file:line 참조) 수집 필수.

**시행**:
- EVIDENCE-BEFORE-REPORT 프로토콜
- 최소 증거 개수 (analyzer: 12+, implementer: 테스트 결과)
- JSON에 모든 검증 데이터 포함 필수
- 품질 게이트가 증거 존재 검증

#### 4. 토큰 효율을 위한 계층 분리

**문제**: 각 에이전트가 파일 내용을 컨텍스트로 로드. 불필요한 파일 로딩은 토큰 낭비.

**해결책**: 엄격한 분리—에이전트는 필요한 것만 로드.

**계층 격리**:
- Layer 1 (CLAUDE.md): 2号만—에이전트는 로드 안 함
- Layer 2 (Commands): 2号만—에이전트는 로드 안 함
- Layer 3 (Agents): 특정 에이전트만—다른 에이전트는 로드 안 함

**토큰 절약**:
- 에이전트가 2号의 오케스트레이션 로직 로드 안 함 (~800줄 절약)
- 에이전트가 다른 에이전트 정의 로드 안 함 (~6,000줄 절약, 6개 에이전트)
- 자신의 traits + protocol만 로드 (~500줄)
- 에이전트 호출당 90%+ 토큰 감소

### 격리로 방지되는 안티패턴

**1. 무한 재귀**
- ❌ 불가능: 에이전트가 Task 호출 불가 → 에이전트 생성 불가 → 재귀 없음

**2. 역할 혼란**
- ❌ 불가능: 2号만 오케스트레이션 가능 → 명확한 책임 경계

**3. 상태 오염**
- ❌ 불가능: 각 세션 완전 격리 → 공유 상태 없음 → 오염 없음

**4. 토큰 폭발**
- ❌ 방지됨: 공유 컨텍스트 없음 → 각 세션 최소화 → 예측 가능한 토큰 사용

### 설계의 우아함: 제약이 해결책을 창조

**핵심 통찰**: 전체 SPARK 아키텍처(JSON 통신, 3계층 분리, 커맨드, 증거 프로토콜)는 임의적이지 않다—에이전트 격리라는 단일 제약에 대한 **불가피한 논리적 해결책**이다.

**아키텍처 도출**:
```
근본 제약: 에이전트 격리
    ↓
파생 제약: 에이전트 간 통신 불가
    ↓
해결책 1: 통신 채널로서의 JSON
    ↓
파생 제약: 2号가 조율 필수
    ↓
해결책 2: 오케스트레이션을 인코딩하는 커맨드
    ↓
파생 제약: 종료 후 검증 불가능
    ↓
해결책 3: 완료 전 증거 수집
    ↓
최적화 기회: 토큰 효율성
    ↓
해결책 4: 3계층 분리 (필요한 것만 로드)
```

이것은 **제약 주도 설계**의 정수—아키텍처는 선택된 것이 아니라 필연적인 것이다.

---

## Section 4.1: JSON 상태 관리

### 통신 프로토콜

에이전트는 직접 메시지 전달이 아니라 구조화된 상태 파일을 통해 소통함.

**철학**: 상태 파일이 제공하는 것:
- **지속성**: 에이전트 완료 후에도 유지됨
- **투명성**: 2号가 진행 상황 검사 가능
- **검증**: 커맨드가 주장 검증 가능
- **디버깅**: 실패 상태가 에러 정보 보존

### 상태 파일 위치

```
~/.claude/workflows/current_task.json         # 메인 작업 상태
~/.claude/workflows/team1_current_task.json   # 팀 1 병렬 작업
~/.claude/workflows/team2_current_task.json   # 팀 2 병렬 작업
~/.claude/workflows/team3_current_task.json   # 팀 3 병렬 작업
~/.claude/workflows/team4_current_task.json   # 팀 4 병렬 작업
~/.claude/workflows/team5_current_task.json   # 팀 5 병렬 작업
```

**파일 구조**:
- **current_task.json**: 단일 에이전트 또는 순차 에이전트 체인
- **team{N}_current_task.json**: 병렬 실행 (multi-implement)
- 각 팀은 병렬 작업을 위한 독립 상태 보유

### 표준 상태 구조

**완전한 구조**:

```json
{
  "id": "spark_20251030_143022",
  "version": "4.3",
  "agent": "implementer-spark",
  "task_description": "사용자 인증 API 구현",
  "state": {
    "status": "completed",
    "phase": 5,
    "started_at": "2025-10-30T14:30:22Z",
    "completed_at": "2025-10-30T15:45:18Z"
  },
  "quality": {
    "step_1_architecture": {
      "imports": 0,
      "circular": 0
    },
    "step_2_foundation": {
      "syntax": 0,
      "types": 0
    },
    "step_3_standards": {
      "formatting": 0,
      "conventions": 0
    },
    "step_4_operations": {
      "logging": 0,
      "security": 0
    },
    "step_5_quality": {
      "linting": 0,
      "complexity": 0
    },
    "step_6_testing": {
      "coverage": 0.97,
      "tests_total": 45,
      "tests_passed": 45,
      "tests_failed": 0
    },
    "step_7_documentation": {
      "docstrings": 0,
      "readme": 0
    },
    "step_8_integration": {
      "final": 0
    },
    "violations_total": 0,
    "can_proceed": true
  },
  "evidence": {
    "files_created": [
      "src/auth/api.py",
      "src/auth/models.py",
      "tests/test_auth_api.py"
    ],
    "tests_executed": true,
    "coverage_report": "htmlcov/index.html"
  }
}
```

### 상태 필드 정의

#### 최상위 필드

| 필드 | 타입 | 필수 | 설명 |
|-------|------|----------|-------------|
| `id` | string | Yes | 고유 식별자: `spark_YYYYMMDD_HHMMSS` |
| `version` | string | Yes | SPARK 버전: `"4.3"` |
| `agent` | string | Yes | 에이전트 이름: `"implementer-spark"` |
| `task_description` | string | No | 간단한 작업 설명 |

#### State 객체

| 필드 | 타입 | 필수 | 값 | 설명 |
|-------|------|----------|--------|-------------|
| `status` | string | Yes | `pending`, `running`, `completed`, `failed` | 현재 실행 상태 |
| `phase` | number | Yes | 0-6 | 현재 phase 번호 |
| `started_at` | string | Yes | ISO8601 | 작업 시작 타임스탬프 |
| `completed_at` | string | No | ISO8601 | 작업 완료 타임스탬프 |

#### Quality 객체

**구조**: 구현 단계별로 구성된 품질 메트릭

각 단계는 특정 메트릭을 가짐:

**Step 1: Architecture**
```json
"step_1_architecture": {
  "imports": 0,        // Import 위반
  "circular": 0        // 순환 의존성 위반
}
```

**Step 2: Foundation**
```json
"step_2_foundation": {
  "syntax": 0,         // 구문 에러
  "types": 0           // 타입 에러
}
```

**Step 3: Standards**
```json
"step_3_standards": {
  "formatting": 0,     // 포맷팅 위반
  "conventions": 0     // 명명 규칙 위반
}
```

**Step 4: Operations**
```json
"step_4_operations": {
  "logging": 0,        // 로깅 표준 위반
  "security": 0        // 보안 이슈
}
```

**Step 5: Quality**
```json
"step_5_quality": {
  "linting": 0,        // 린팅 위반 (ruff)
  "complexity": 0      // 복잡도 위반
}
```

**Step 6: Testing** (implementer/tester에 중요)
```json
"step_6_testing": {
  "coverage": 0.95,    // 커버리지 비율 (0.0-1.0)
  "tests_total": 45,   // 총 테스트 개수
  "tests_passed": 45,  // 통과한 테스트 개수
  "tests_failed": 0    // 실패한 테스트 개수 (반드시 0)
}
```

**Step 7: Documentation**
```json
"step_7_documentation": {
  "docstrings": 0,     // 누락된 docstring 위반
  "readme": 0          // README 이슈
}
```

**Step 8: Integration**
```json
"step_8_integration": {
  "final": 0           // 최종 통합 위반
}
```

**전체 품질**
```json
"violations_total": 0,    // 모든 위반의 합 (반드시 0)
"can_proceed": true       // 작업 진행 가능 여부 (반드시 true)
```

### 에이전트 책임

#### Phase 0: 상태 읽기

```python
def phase_0_read_state(self):
    """기존 상태 읽기 또는 새로 생성."""

    state_file = "~/.claude/workflows/current_task.json"

    if exists(state_file):
        # 기존 상태 읽기
        self.state = read_json(state_file)

        # 계속인지 재시도인지 확인
        if self.state["state"]["status"] == "failed":
            print("실패한 작업 재시도 중...")
        elif self.state["state"]["status"] == "running":
            print("중단된 작업 계속 중...")
    else:
        # 새 상태 생성
        self.state = {
            "id": f"spark_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "version": "4.3",
            "agent": self.agent_name,
            "state": {
                "status": "running",
                "phase": 0,
                "started_at": datetime.now().isoformat()
            },
            "quality": self._init_quality_metrics()
        }
```

#### 실행 중: 상태 업데이트

```python
def update_phase(self, phase: int):
    """상태에서 현재 phase 업데이트."""

    self.state["state"]["phase"] = phase
    write_json("~/.claude/workflows/current_task.json", self.state)

def record_violation(self, step: str, violation_type: str, count: int):
    """품질 위반 기록."""

    self.state["quality"][step][violation_type] = count
    self._recalculate_total_violations()
    write_json("~/.claude/workflows/current_task.json", self.state)
```

#### Phase 5A: 최종 상태 작성

```python
def phase_5a_record_metrics(self):
    """최종 품질 메트릭 기록."""

    # 모든 품질 확인 실행
    ruff_violations = self.run_ruff_check()
    mypy_violations = self.run_mypy_check()
    test_results = self.run_pytest()

    # 상태에 기록
    self.state["quality"]["step_5_quality"]["linting"] = ruff_violations
    self.state["quality"]["step_2_foundation"]["types"] = mypy_violations
    self.state["quality"]["step_6_testing"] = {
        "coverage": test_results["coverage"],
        "tests_total": test_results["total"],
        "tests_passed": test_results["passed"],
        "tests_failed": test_results["failed"]
    }

    # 총 위반 계산
    self._recalculate_total_violations()

    # can_proceed 플래그 설정
    self.state["quality"]["can_proceed"] = (
        self.state["quality"]["violations_total"] == 0
    )

    # 완료 표시
    self.state["state"]["status"] = "completed"
    self.state["state"]["completed_at"] = datetime.now().isoformat()

    # 최종 상태 작성
    write_json("~/.claude/workflows/current_task.json", self.state)
```

#### Phase 5B: 품질 게이트 확인

에이전트는 Phase 5B에서 상태를 수정하지 않음 - 통과하는지만 검증.

### 2号 책임

#### 에이전트 호출 전: 상태 초기화

```python
def initialize_agent_state(agent_name: str, task_description: str):
    """에이전트 호출 전 상태 초기화."""

    state = {
        "id": f"spark_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "version": "4.3",
        "agent": agent_name,
        "task_description": task_description,
        "state": {
            "status": "pending",
            "phase": 0,
            "started_at": datetime.now().isoformat()
        },
        "quality": init_quality_structure()
    }

    write_json("~/.claude/workflows/current_task.json", state)
```

#### 에이전트 완료 후: 상태 검증

```python
def validate_agent_state(agent_name: str) -> tuple[bool, str]:
    """완료 후 에이전트 상태 검증."""

    state = read_json("~/.claude/workflows/current_task.json")

    # 보편적 확인
    if state["state"]["status"] != "completed":
        return False, f"상태가 {state['state']['status']}임"

    if state["quality"]["violations_total"] != 0:
        return False, f"{state['quality']['violations_total']}개 위반"

    if not state["quality"]["can_proceed"]:
        return False, "can_proceed가 false임"

    # 에이전트별 확인
    if agent_name == "implementer-spark":
        coverage = state["quality"]["step_6_testing"]["coverage"]
        if coverage < 0.95:
            return False, f"커버리지 {coverage:.1%} < 95%"

    return True, "성공"
```

#### 성공적인 워크플로우 후: 상태 삭제

```python
def cleanup_state():
    """성공적 완료 후 상태 삭제."""

    state_file = "~/.claude/workflows/current_task.json"

    if exists(state_file):
        state = read_json(state_file)

        if state["state"]["status"] == "completed" and \
           state["quality"]["violations_total"] == 0:
            os.remove(state_file)
            print("✅ 상태 정리됨")
```

### 상태 전환

**유효한 상태 전환**:

```
pending → running → completed ✅
pending → running → failed ❌
failed → running (재시도) → completed ✅
running → failed ❌
```

**무효한 전환**:

```
pending → completed ❌ (running을 거쳐야 함)
failed → completed ❌ (running을 통해 재시도해야 함)
completed → running ❌ (completed는 종료 상태)
```

### 상태 파일 예시

#### 예시 1: 성공한 Implementer

```json
{
  "id": "spark_20251030_143022",
  "version": "4.3",
  "agent": "implementer-spark",
  "task_description": "사용자 로그인 엔드포인트 구현",
  "state": {
    "status": "completed",
    "phase": 5,
    "started_at": "2025-10-30T14:30:22Z",
    "completed_at": "2025-10-30T15:45:18Z"
  },
  "quality": {
    "step_1_architecture": { "imports": 0, "circular": 0 },
    "step_2_foundation": { "syntax": 0, "types": 0 },
    "step_3_standards": { "formatting": 0, "conventions": 0 },
    "step_4_operations": { "logging": 0, "security": 0 },
    "step_5_quality": { "linting": 0, "complexity": 0 },
    "step_6_testing": {
      "coverage": 0.98,
      "tests_total": 23,
      "tests_passed": 23,
      "tests_failed": 0
    },
    "step_7_documentation": { "docstrings": 0, "readme": 0 },
    "step_8_integration": { "final": 0 },
    "violations_total": 0,
    "can_proceed": true
  },
  "evidence": {
    "files_created": ["src/auth/login.py", "tests/test_login.py"],
    "coverage_report": "htmlcov/index.html"
  }
}
```

#### 예시 2: 위반으로 실패

```json
{
  "id": "spark_20251030_160000",
  "version": "4.3",
  "agent": "implementer-spark",
  "state": {
    "status": "failed",
    "phase": 5,
    "started_at": "2025-10-30T16:00:00Z",
    "completed_at": "2025-10-30T16:30:00Z"
  },
  "quality": {
    "step_1_architecture": { "imports": 0, "circular": 0 },
    "step_2_foundation": { "syntax": 0, "types": 5 },
    "step_3_standards": { "formatting": 12, "conventions": 3 },
    "step_4_operations": { "logging": 0, "security": 0 },
    "step_5_quality": { "linting": 23, "complexity": 0 },
    "step_6_testing": {
      "coverage": 0.87,
      "tests_total": 15,
      "tests_passed": 13,
      "tests_failed": 2
    },
    "step_7_documentation": { "docstrings": 8, "readme": 0 },
    "step_8_integration": { "final": 0 },
    "violations_total": 51,
    "can_proceed": false
  },
  "error_details": {
    "type_errors": ["src/auth/login.py:45: 타입 주석 누락"],
    "linting_errors": ["F841: 지역 변수 'unused' 할당되었으나 사용 안 됨"],
    "test_failures": ["test_invalid_credentials 실패"]
  }
}
```

### Section 4.1.5: Hooks - 자동화된 검증 (실험적)

⚠️ **실험적 기능**: Hooks는 강력하지만 광범위한 테스트와 신중한 설계가 필요합니다. SPARK은 hooks를 실험했으나 프로덕션 수준의 통합을 달성하지 못했습니다. 주의해서 사용하고 철저히 테스트하세요.

#### 개요

**Hooks**는 특정 Claude Code 라이프사이클 이벤트에서 투명하게 실행되는 자동화된 셸 스크립트로, 에이전트나 2号의 인지 없이 검증, 컨텍스트 주입, 워크플로우 자동화를 가능하게 합니다.

**핵심 특성**: Hooks는 **보이지 않게** 실행됩니다—에이전트와 2号는 hooks가 실행되었다는 것을 알지 못합니다. 이것은 백그라운드 프로세싱이 아닙니다; hooks는 이벤트를 가로채고 제어가 반환되기 전에 실행됩니다.

#### Hooks의 작동 방식

**실행 흐름**:
```
이벤트 발생 (예: Tool 사용, Prompt 제출)
  → Hook 자동 트리거
  → Hook은 stdin으로 JSON 입력 수신
  → Hook은 셸 명령 실행
  → Hook은 Exit Code + 선택적 JSON 출력 반환
  → 제어가 에이전트/2号에게 반환 (hook 실행을 모름)
```

**통신**:
- **입력**: `stdin`을 통한 JSON (세션 데이터, 이벤트 데이터, 도구 파라미터)
- **출력**: Exit code (0 = 성공, 2 = 차단 에러, 기타 = 비차단 에러)
- **선택적**: 고급 제어를 위한 `stdout` JSON

#### 주요 Hook 타입

**도구 관련 Hooks**:

1. **PreToolUse**
   - **트리거**: 에이전트가 도구 파라미터 생성 후, 실행 전
   - **목적**: 도구 호출 검증, 수정, 차단
   - **예시**: 위험한 Bash 명령 차단, 파일 경로 검증, 표준 강제
   - **Matchers 지원**: 특정 도구 타겟 (`Bash`, `Write`, `Edit` 등)

2. **PostToolUse**
   - **트리거**: 도구 성공적 완료 후
   - **목적**: 결과에 반응, 작업 로그, 후속 작업 트리거
   - **접근**: 도구 입력과 도구 출력 모두
   - **예시**: Write 후 코드 자동 포맷, Edit 후 테스트 실행

**이벤트 Hooks**:

3. **UserPromptSubmit**
   - **트리거**: 사용자 프롬프트 제출 시 (Claude 처리 전)
   - **목적**: 컨텍스트 주입, 요청 검증, 표준 로드
   - **컨텍스트 주입**: Hook stdout이 Claude 컨텍스트에 추가됨
   - **예시**: 모든 요청 전 PROJECT_STANDARDS.md 로드

4. **SessionStart/SessionEnd**
   - **트리거**: 세션 초기화/종료
   - **목적**: 환경 설정, 정리 작업
   - **예시**: 가상환경 활성화, 세션 로그 저장

5. **Stop/SubagentStop**
   - **트리거**: 에이전트 응답 완료 시
   - **목적**: 완료 전 개입, 정리
   - **예시**: 최종 상태 검증, 아티팩트 저장

#### 설정

**위치**: `.claude/settings.json`, `.claude/settings.local.json`, 또는 `~/.claude/settings.json`

**구조**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validate_bash.py",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/quality_check.py"
          }
        ]
      }
    ]
  }
}
```

**필드**:
- **matcher**: 도구 이름을 위한 정규식 패턴 (대소문자 구분). 모든 도구는 `*` 또는 `""` 사용
- **command**: 셸 명령 또는 스크립트 경로. 프로젝트 상대 경로는 `$CLAUDE_PROJECT_DIR` 사용
- **timeout**: 초 단위 (기본값 60)

#### SPARK 실험: Quality Gates

**목표**: PostToolUse hooks를 사용하여 에이전트 주장을 자동으로 검증.

**접근 방법**:
```python
# spark_quality_gates.py (실험적)
import json
import sys

# 에이전트가 작성한 JSON 상태 읽기
state = json.load(sys.stdin)

# 에이전트 주장: "violations_total": 0
claimed_violations = state.get("quality", {}).get("violations_total", 0)

# 실제로 ruff 실행하여 검증
import subprocess
result = subprocess.run(["ruff", "check", "."], capture_output=True)
actual_violations = len(result.stdout.decode().splitlines())

if claimed_violations != actual_violations:
    print(f"VIOLATION: 에이전트가 {claimed_violations}개 주장했으나 {actual_violations}개 발견", file=sys.stderr)
    sys.exit(2)  # 완료 차단

sys.exit(0)  # 완료 허용
```

**설정**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/spark_quality_gates.py"
          }
        ]
      }
    ]
  }
}
```

**결과**: 혼재. Hooks는 올바르게 트리거되었으나:
- 타이밍 이슈 (hook이 에이전트가 모든 파일 쓰기를 완료하기 전에 실행됨)
- 컨텍스트 가용성 (hook이 전체 JSON 상태에 접근 필요)
- 에러 처리 (차단 에러가 때때로 올바르게 표시되지 않음)

**상태**: 프로덕션 사용 전 **추가 연구 및 테스트 필요**.

#### Hook 입출력

**입력 구조** (모든 hooks 수신):
```json
{
  "session_id": "unique_identifier",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/working/directory",
  "hook_event_name": "PreToolUse|PostToolUse|etc",
  "tool_name": "Bash",  // 도구 hooks용
  "tool_input": {...},   // 도구 hooks용
  "tool_output": {...}   // PostToolUse만
}
```

**출력 옵션**:

1. **단순 Exit Codes**:
   - `0`: 성공 (stdout이 transcript에 표시되거나 컨텍스트로 추가됨)
   - `2`: 차단 에러 (stderr이 Claude에게 전달되어 처리)
   - 기타: 비차단 에러 (stderr이 사용자에게 표시됨)

2. **고급 JSON 출력**:
```json
{
  "continue": true,
  "decision": "allow|deny|block",
  "additionalContext": "주입할 문자열"
}
```

#### 보안 경고

⚠️ **중요**: Hooks는 전체 사용자 권한으로 임의의 셸 명령을 자동으로 실행합니다.

**위험**:
- 접근 가능한 모든 파일 수정/삭제 가능
- 임의 코드 실행 가능
- 민감한 데이터 접근 가능
- 샌드박싱이나 격리 없음

**모범 사례**:
1. **모든 입력 검증**: JSON 데이터 정제, 경로 순회(`..`) 확인
2. **변수 인용**: 셸에서 항상 `"$VAR"` 구문 사용
3. **절대 경로 사용**: 스크립트와 중요 파일용
4. **철저한 테스트**: 프로덕션 전 안전한 환경에서
5. **민감한 파일 건너뛰기**: `.env`, `.git/`, 자격증명
6. **범위 제한**: Matchers를 사용하여 특정 도구만 타겟

#### 현재 권장사항

**프로덕션 사용**:
- **DO**: 컨텍스트 주입을 위한 UserPromptSubmit hooks 사용 (검증된 신뢰성)
- **DO**: 환경 설정을 위한 SessionStart hooks 사용 (검증된 신뢰성)
- **주의**: 검증을 위한 PreToolUse hooks 사용 (먼저 광범위하게 테스트)
- **주의**: 단순 로깅을 위한 PostToolUse hooks 사용 (타이밍 이슈 가능)
- **회피**: 품질 게이트를 위한 복잡한 PostToolUse hooks (SPARK 실험 결과 불확실)

**실험용**:
- 모든 hook 동작을 신중하게 문서화
- 격리된 환경에서 테스트
- 대체 메커니즘 유지
- SPARK 커뮤니티와 결과 공유

**SPARK 프로젝트용**:
- Quality gates 접근 방식은 유망하나 정제 필요
- 대안적 검증 메커니즘 고려 (2号 주도 검사)
- 모든 실험 결과 문서화
- 발견에 기반한 반복

#### 완전한 참조

**상세 문서**: `docs/CLAUDE_CODE_HOOKS_AND_AGENTS.md` 참조:
- 완전한 hook 타입 참조
- 모든 설정 옵션
- 고급 예시
- MCP 도구 통합
- 플러그인 hook 지원

**공식 Anthropic 문서**: [https://docs.claude.com/en/docs/claude-code/hooks](https://docs.claude.com/en/docs/claude-code/hooks)

---

## Section 4.2: 에이전트별 증거 요구사항

### 증명 원칙

다른 에이전트 유형은 다른 형태의 증거를 요구하지만, 모두 증명이 필요함.

### Analyzer 증거 요구사항

**최소 요구사항**:
- **증거 항목**: 분석된 모든 차원에서 최소 8-12개
- **형식**: 모든 발견에 대해 `file_path:line_number`
- **내용**: 각 증거 항목에 대해 코드 스니펫 또는 메트릭
- **검증**: Phase 3 전에 증거 검증 통과해야 함

**증거 항목 구조**:

```python
evidence_item = {
    "file_path": "src/api/handler.py",
    "line_number": 145,
    "code": "api_key = os.getenv('KEY')",  # 또는
    "metric": {"response_time": "2.5s"},
    "category": "security",
    "severity": "high",
    "description": "하드코딩된 API 키 발견"
}
```

**완전한 증거 수집**:

```json
{
  "evidence_count": 26,
  "dimensions_analyzed": ["performance", "security", "architecture"],
  "evidence_items": [
    {
      "file_path": "src/api/users.py",
      "line_number": 45,
      "code": "users = db.query('SELECT * FROM users')",
      "category": "performance",
      "severity": "high",
      "description": "N+1 쿼리 패턴"
    },
    {
      "file_path": "src/auth/login.py",
      "line_number": 78,
      "code": "@app.post('/login')",
      "category": "security",
      "severity": "critical",
      "description": "로그인 엔드포인트에 인증 없음"
    }
    // ... 24개 더
  ]
}
```

**검증**:

```python
def validate_analyzer_evidence(state: dict) -> bool:
    """분석가가 충분한 증거를 수집했는지 검증."""

    evidence = state.get("evidence", {})

    # 최소 개수 확인
    if evidence.get("evidence_count", 0) < 8:
        return False

    # 각 항목에 file:line 있는지 확인
    for item in evidence.get("evidence_items", []):
        if not item.get("file_path") or not item.get("line_number"):
            return False

    # 분석된 차원 확인
    if not evidence.get("dimensions_analyzed"):
        return False

    return True
```

### Implementer 증거 요구사항

**최소 요구사항**:
- **테스트 실행**: pytest가 실행되고 출력이 캡처되어야 함
- **품질 메트릭**: Ruff, MyPy 전/후 개수
- **커버리지**: 파일별 비율, 전체 >= 95%
- **테스트 결과**: 모든 테스트 통과해야 함 (failures == 0)

**증거 구조**:

```json
{
  "files_created": [
    "src/auth/api.py",
    "src/auth/models.py",
    "tests/test_auth_api.py"
  ],
  "files_modified": [
    "src/main.py"
  ],
  "test_execution": {
    "command": "pytest tests/test_auth_api.py -v --cov=src/auth",
    "output": "===== test session starts =====\n...",
    "total": 23,
    "passed": 23,
    "failed": 0,
    "duration": "2.45s"
  },
  "coverage": {
    "overall": 0.98,
    "files": {
      "src/auth/api.py": 1.0,
      "src/auth/models.py": 0.96
    }
  },
  "quality_before": {
    "ruff": 45,
    "mypy": 12
  },
  "quality_after": {
    "ruff": 0,
    "mypy": 0
  }
}
```

**검증**:

```python
def validate_implementer_evidence(state: dict) -> bool:
    """구현자가 실행 증명을 제공했는지 검증."""

    quality = state["quality"]

    # 테스트 실행 확인
    if quality["step_6_testing"]["tests_total"] == 0:
        return False

    # 모든 테스트 통과 확인
    if quality["step_6_testing"]["tests_failed"] != 0:
        return False

    # 커버리지 확인
    if quality["step_6_testing"]["coverage"] < 0.95:
        return False

    # 품질 메트릭 확인
    if quality["violations_total"] != 0:
        return False

    return True
```

### Tester 증거 요구사항

**최소 요구사항**:
- **테스트 실행 로그**: 전체 pytest 출력
- **커버리지 보고서**: 파일별 비율
- **테스트 파일 경로**: 테스트 개수와 함께 모든 테스트 파일 목록
- **통과율**: 100% (test_pass_rate == 1.0)

**증거 구조**:

```json
{
  "test_files": [
    {
      "path": "tests/test_auth_api.py",
      "tests": 23,
      "passed": 23,
      "failed": 0
    },
    {
      "path": "tests/test_auth_models.py",
      "tests": 15,
      "passed": 15,
      "failed": 0
    }
  ],
  "coverage": {
    "unit": 0.97,
    "integration": 0.89,
    "overall": 0.95,
    "files": {
      "src/auth/api.py": 1.0,
      "src/auth/models.py": 0.96,
      "src/auth/utils.py": 0.92
    }
  },
  "execution_log": "pytest 출력...",
  "test_pass_rate": 1.0,
  "tests_total": 38,
  "tests_passed": 38,
  "tests_failed": 0
}
```

**검증**:

```python
def validate_tester_evidence(state: dict) -> bool:
    """테스터가 테스트를 제대로 실행했는지 검증."""

    evidence = state.get("evidence", {})

    # 100% 통과율 확인
    if evidence.get("test_pass_rate") != 1.0:
        return False

    # 테스트 실행 확인
    if evidence.get("tests_total", 0) == 0:
        return False

    # 커버리지 목표 확인
    coverage = evidence.get("coverage", {})
    if coverage.get("unit", 0) < 0.95:
        return False
    if coverage.get("integration", 0) < 0.85:
        return False

    return True
```

### Designer 증거 요구사항

**최소 요구사항**:
- **아키텍처 다이어그램**: 이미지 파일 또는 ASCII 다이어그램
- **API 명세**: OpenAPI 3.0 또는 GraphQL 스키마
- **데이터 모델**: ERD 또는 데이터베이스 스키마
- **기술 스택**: 근거와 함께 결정사항

**증거 구조**:

```json
{
  "artifacts": {
    "architecture_diagram": "docs/architecture.png",
    "api_spec": "docs/openapi.yaml",
    "data_model": "docs/erd.png",
    "tech_stack": "docs/tech_decisions.md"
  },
  "api_endpoints": 15,
  "data_entities": 8,
  "design_decisions": [
    {
      "area": "인증",
      "decision": "JWT with refresh tokens",
      "rationale": "상태 비저장, 확장 가능, 업계 표준"
    }
  ],
  "validation": {
    "api_completeness": 1.0,
    "model_coverage": 1.0,
    "documentation_complete": true
  }
}
```

**검증**:

```python
def validate_designer_evidence(state: dict) -> bool:
    """설계자가 필요한 산출물을 생성했는지 검증."""

    evidence = state.get("evidence", {})
    artifacts = evidence.get("artifacts", {})

    # 필수 산출물 존재 확인
    required = ["architecture_diagram", "api_spec", "data_model"]
    for artifact in required:
        if not artifacts.get(artifact):
            return False

    # 검증 메트릭 확인
    validation = evidence.get("validation", {})
    if validation.get("api_completeness", 0) != 1.0:
        return False

    return True
```

### Documenter 증거 요구사항

**최소 요구사항**:
- **문서 파일**: 생성/업데이트된 파일 목록
- **예제 코드 검증**: 모든 예제가 성공적으로 실행되어야 함
- **API 커버리지**: 공개 API의 100% 문서화
- **완전성**: 매개변수, 반환값, 에러 모두 문서화

**증거 구조**:

```json
{
  "files_created": [
    "docs/api/authentication.md",
    "docs/api/users.md",
    "docs/guides/quick_start.md"
  ],
  "api_coverage": {
    "total_apis": 45,
    "documented": 45,
    "percentage": 1.0
  },
  "example_validation": {
    "total_examples": 23,
    "executed": 23,
    "passed": 23,
    "failed": 0
  },
  "completeness": {
    "parameters": 1.0,
    "returns": 1.0,
    "errors": 1.0,
    "examples": 1.0
  }
}
```

**검증**:

```python
def validate_documenter_evidence(state: dict) -> bool:
    """문서작성자가 문서화를 완료했는지 검증."""

    evidence = state.get("evidence", {})

    # API 커버리지 확인
    coverage = evidence.get("api_coverage", {})
    if coverage.get("percentage", 0) != 1.0:
        return False

    # 예제 검증 확인
    examples = evidence.get("example_validation", {})
    if examples.get("failed", 0) != 0:
        return False

    # 완전성 확인
    completeness = evidence.get("completeness", {})
    for aspect in ["parameters", "returns", "errors"]:
        if completeness.get(aspect, 0) != 1.0:
            return False

    return True
```

---

## Section 4.3: 완료 기준

### 보편적 기준 (모든 에이전트)

**기본 함수**:

```python
def is_agent_complete(state: dict) -> bool:
    """
    모든 에이전트에 대한 보편적 완료 확인.

    모든 기준이 충족된 경우에만 True 반환.
    """
    return (
        state["state"]["status"] == "completed" and
        state["quality"]["violations_total"] == 0 and
        state["quality"]["can_proceed"] == True
    )
```

**설명**:
- `status == "completed"`: 에이전트가 작업을 완료로 표시
- `violations_total == 0`: 품질 위반 0개
- `can_proceed == True`: 품질 게이트 통과

**세 가지 모두 참이어야 함.** 하나라도 거짓이면 에이전트가 완료되지 않은 것.

### 에이전트별 기준

각 에이전트 유형은 보편적 기준을 넘어서는 추가 요구사항을 가짐.

#### Implementer 완료

```python
def is_implementer_complete(state: dict) -> bool:
    """Implementer별 완료 기준."""

    # 보편적 확인
    if not is_agent_complete(state):
        return False

    quality = state["quality"]

    # 테스트 커버리지 >= 95%
    coverage = quality["step_6_testing"]["coverage"]
    if coverage < 0.95:
        return False

    # 모든 테스트 통과
    if quality["step_6_testing"]["tests_failed"] != 0:
        return False

    # 최소한 일부 테스트 존재
    if quality["step_6_testing"]["tests_total"] == 0:
        return False

    return True
```

**요구사항**:
- ✅ 보편적 기준 충족
- ✅ 커버리지 >= 95%
- ✅ 테스트 실패 0개
- ✅ 최소 1개 테스트 존재

#### Analyzer 완료

```python
def is_analyzer_complete(state: dict) -> bool:
    """Analyzer별 완료 기준."""

    # 보편적 확인
    if not is_agent_complete(state):
        return False

    evidence = state.get("evidence", {})

    # 최소 증거 개수
    if evidence.get("evidence_count", 0) < 8:
        return False

    # 모든 요청된 차원 분석됨
    dimensions_requested = state.get("dimensions_requested", [])
    dimensions_analyzed = evidence.get("dimensions_analyzed", [])

    if not all(dim in dimensions_analyzed for dim in dimensions_requested):
        return False

    return True
```

**요구사항**:
- ✅ 보편적 기준 충족
- ✅ 최소 8개 증거 항목
- ✅ 모든 요청된 차원 분석됨

#### Tester 완료

```python
def is_tester_complete(state: dict) -> bool:
    """Tester별 완료 기준."""

    # 보편적 확인
    if not is_agent_complete(state):
        return False

    evidence = state.get("evidence", {})

    # 100% 테스트 통과율
    if evidence.get("test_pass_rate", 0) != 1.0:
        return False

    # 커버리지 목표 충족
    coverage = evidence.get("coverage", {})
    if coverage.get("unit", 0) < 0.95:
        return False
    if coverage.get("integration", 0) < 0.85:
        return False

    return True
```

**요구사항**:
- ✅ 보편적 기준 충족
- ✅ 100% 테스트 통과율
- ✅ 단위 커버리지 >= 95%
- ✅ 통합 커버리지 >= 85%

#### Designer 완료

```python
def is_designer_complete(state: dict) -> bool:
    """Designer별 완료 기준."""

    # 보편적 확인
    if not is_agent_complete(state):
        return False

    evidence = state.get("evidence", {})
    validation = evidence.get("validation", {})

    # 모든 설계 phase 완료
    if not validation.get("all_phases_complete", False):
        return False

    # 검증 기준 충족
    if validation.get("api_completeness", 0) != 1.0:
        return False

    if validation.get("model_coverage", 0) != 1.0:
        return False

    return True
```

**요구사항**:
- ✅ 보편적 기준 충족
- ✅ 모든 설계 phase 완료
- ✅ 100% API 완전성
- ✅ 100% 모델 커버리지

#### Documenter 완료

```python
def is_documenter_complete(state: dict) -> bool:
    """Documenter별 완료 기준."""

    # 보편적 확인
    if not is_agent_complete(state):
        return False

    evidence = state.get("evidence", {})

    # 100% API 커버리지
    api_coverage = evidence.get("api_coverage", {})
    if api_coverage.get("percentage", 0) != 1.0:
        return False

    # 모든 예제 검증됨
    examples = evidence.get("example_validation", {})
    if examples.get("failed", 0) != 0:
        return False

    # 완전성 확인
    completeness = evidence.get("completeness", {})
    for aspect in ["parameters", "returns", "errors"]:
        if completeness.get(aspect, 0) != 1.0:
            return False

    return True
```

**요구사항**:
- ✅ 보편적 기준 충족
- ✅ 100% API 커버리지
- ✅ 모든 예제 성공적으로 실행
- ✅ 완전한 문서화 (매개변수, 반환값, 에러)

### 완료 검증 워크플로우

**완전한 검증 함수**:

```python
def verify_agent_completion(agent_name: str) -> tuple[bool, str]:
    """
    종합적 완료 검증.

    Returns:
        (success, message): 완료되면 True, 설명과 함께
    """

    # 상태 읽기
    try:
        state = read_json("~/.claude/workflows/current_task.json")
    except FileNotFoundError:
        return False, "상태 파일 찾을 수 없음"

    # 보편적 확인
    if not is_agent_complete(state):
        status = state["state"]["status"]
        violations = state["quality"]["violations_total"]
        can_proceed = state["quality"]["can_proceed"]

        if status != "completed":
            return False, f"상태: {status} (완료 아님)"
        if violations != 0:
            return False, f"{violations}개 위반 남음"
        if not can_proceed:
            return False, "품질 게이트 실패"

    # 에이전트별 확인
    if agent_name == "implementer-spark":
        success, msg = verify_implementer_specific(state)
        if not success:
            return False, f"Implementer: {msg}"

    elif agent_name == "analyzer-spark":
        success, msg = verify_analyzer_specific(state)
        if not success:
            return False, f"Analyzer: {msg}"

    elif agent_name == "tester-spark":
        success, msg = verify_tester_specific(state)
        if not success:
            return False, f"Tester: {msg}"

    elif agent_name == "designer-spark":
        success, msg = verify_designer_specific(state)
        if not success:
            return False, f"Designer: {msg}"

    elif agent_name == "documenter-spark":
        success, msg = verify_documenter_specific(state)
        if not success:
            return False, f"Documenter: {msg}"

    # 모든 확인 통과
    return True, "에이전트가 성공적으로 완료됨"
```

---

## 요약

이 가이드는 SPARK 통합을 위한 상세 명세 제공:

1. **JSON 상태 관리**: 상태 파일을 통한 구조화된 통신
2. **증거 요구사항**: 에이전트별 증명 요구사항
3. **완료 기준**: 보편적 + 에이전트별 검증

**핵심 원칙**: 증거는 필수. 증명 없는 주장은 무가치. 상태 파일은 에이전트와 커맨드 간에 투명하고 검증 가능한 통신 제공.

---

**관련 문서**:
- **1_CONSTITUTION_ko.md** - 핵심 원칙
- **2_AGENT_DESIGN_GUIDE_ko.md** - 에이전트 설계 표준
- **3_COMMAND_DESIGN_GUIDE_ko.md** - 커맨드 오케스트레이션
- **5_TEMPLATES_ko.md** - 빠른 시작 템플릿
