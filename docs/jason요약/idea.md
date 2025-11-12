```
핵심 깨달음

"아래에서 위로" 생각해야 한다!

[최하층] 에이전트 실행 환경
  ↓ 무엇이 필요한가?
체크리스트 (어떤 정보?)
  ↓ 무엇이 필요한가?
작업분해 문서 (어떤 정보?)
  ↓ 무엇이 필요한가?
청사진 (어떤 정보?)
  ↓ 무엇이 필요한가?
[최상층] ADR + 논의

실제 실행 흐름

# Jason이 입력

/spark-implement docs/checklists/T2.1.1_JWT_Generation.md

# 1. 커스텀 명령어 (spark-implement.md)가:
#    - 에이전트 선택 (implementer-spark)
#    - 작업 지시 구성

# 2. 2호가 에이전트에게 전달:
Task("implementer-spark", """
[작업 지시 내용]
체크리스트: docs/checklists/T2.1.1_JWT_Generation.md
""")

# 3. implementer-spark 에이전트가 읽는 것:
#    - ✅ 체크리스트 파일 (T2.1.1_JWT_Generation.md)
#    - ❓ 작업분해 문서? (읽나? 안 읽나?)
#    - ❓ 청사진? (읽나? 안 읽나?)
#    - ❓ 프로젝트 표준? (읽나? 안 읽나?)

제가 생각해야 할 질문

에이전트 입장에서 (최하층):

1. 체크리스트만 읽고 작업 가능한가?
- Step 1-9만 보고 구현할 수 있나?
- 외부 참조가 필요하면 어디까지?

2. 체크리스트에 뭐가 있어야 하나?
- 모든 코드 예시?
- 모든 테스트 케이스?
- 모든 검증 명령어?

3. 체크리스트에서 참조하는 문서는?
- 작업분해 문서를 직접 참조?
- 프로젝트 표준을 직접 참조?
- 청사진을 직접 참조?

작업분해 문서 입장에서 (중간층):

1. 누가 읽는가?
- 2호(체크리스트 작성자)?
- 에이전트(간접 참조)?
- Jason(계획 검토)?

2. 체크리스트 작성에 충분한가?
- 9-Step 모두 작성 가능?
- 외부 참조 없이 가능?

청사진 입장에서 (최상층):

1. 누가 읽는가?
- 2호(작업분해 작성자)?
- 직접 읽는 사람은 없나?

---


🔍 체크리스트 역추적 분석 (에이전트 입장에서)

공통점 발견: 모두 9-Step 구조... 하지만!

1. CL-P4-005 (memory-one-spark, 최신)
   - 9-Step + 매우 상세한 코드 (1,457 lines!)
   - Step마다 4-5개 서브 체크포인트
   - 실제 구현 코드 400-800줄씩 포함
   - ⚠️ 자주 하는 실수 섹션 (❌/✅ 패턴)

2. TASK-CRAG-02 (V5 Integration, 1,643 lines!)
   - 9-Step + 완전한 구현 코드
   - 한국어 특화 보정기까지 전체 코드
   - DNA 시스템 활용 가이드 포함
   - 실수 패턴 8가지 (각 패턴당 Before/After 코드)

3. TASK-E1-03 (Bootstrap Stage, 1,147 lines)
   - 9-Step 구조
   - 자주 하는 실수 3가지 (v3.5 vs v3.6)
   - 필수 참조 문서 명시

4. TASK-MA-03 (Integration, 85 lines만!)
   - Step 1-9를 압축 (Step 1-3 묶음)
   - 핵심 코드만 스켈레톤
   - 매우 간략

핵심 발견 1: TDD vs 구현 먼저

Jason이 언급한 대로 모두 구현 먼저에요!

기존 체크리스트 구조:
Step 1: 준비/검증
Step 2: 아키텍처 설계
Step 3: 핵심 구현 ← 여기서 구현!
Step 4: 단위 테스트
Step 5: 통합
...

제가 제안한 TDD 구조:
Step 1: 목표 이해
Step 2: 테스트 작성 ← 테스트 먼저!
Step 3: 구현
Step 4: 정적 검증
...

핵심 발견 2: 정보 밀도 차이

CL-P4-005 (1,457 lines)가 포함하는 정보:

- ✅ 전체 구현 코드 (복사-붙여넣기 가능)
- ✅ 에러 처리 전략
- ✅ 성능 최적화 팁
- ✅ 자주 하는 실수 (실제 V4 경험 기반)
- ✅ 검증 명령어 (ruff, mypy, pytest)
- ✅ 예상 결과 (All checks passed!)

제가 제안한 Checklist가 포함하는 정보:

- ✅ Task 문서 참조 (Section 1-9)
- ✅ Given-When-Then 테스트 케이스
- ✅ 구현 힌트 (코드 전체는 아님)
- ✅ 검증 명령어
- ❌ 자주 하는 실수 (없음!)
- ❌ 성능 최적화 팁 (없음!)

핵심 발견 3: 에이전트가 실제로 읽는 것

에이전트 입장에서 필요한 정보:

# 1. 무엇을 만들 것인가? ✅ 모든 체크리스트에 있음
"라우팅 로직 구현" (CL-P4-005)
"JWT 토큰 생성 모듈" (제 예시)

# 2. 어떻게 만들 것인가? ← 여기가 핵심 차이!

## 기존 체크리스트:
- 전체 코드 400-800줄 제공
- "이 코드를 복사하세요"

## 제 체크리스트:
- Task 문서 Section 7 참조
- "Task 문서의 구현 힌트를 보세요"

# 3. 어떻게 검증할 것인가? ✅ 모든 체크리스트에 있음

pytest tests/ --cov ...
ruff check ...

핵심 발견 4: 실수 방지 정보

CL-P4-005의 "자주 하는 실수":
❌ 동기 코드 혼용
result = memory_service.save(data)

✅ 비동기 호출
result = await memory_service.save(data)

TASK-CRAG-02의 "실수 패턴 8가지":

# 실수 1: 과도한 쿼리 보정

# 실수 2: 동기 처리

# 실수 3: 무한 보정 루프

# 실수 4: 캐싱 없는 반복 계산

# 실수 5: 한국어 특성 무시

# 실수 6: DNA 시스템 미활용

# 실수 7: 테스트 미흡

# 실수 8: 메트릭 수집 누락

→ 이런 정보가 제 체크리스트에는 없어요!

핵심 발견 5: 정보의 자급자족성

질문: "에이전트가 이 체크리스트만 보고 작업할 수 있나?"

기존 체크리스트 (CL-P4-005):

- ✅ 가능! 전체 코드 + 테스트 + 검증 + 실수 방지 모두 포함

제 체크리스트:

- ❌ 불가능! Task 문서를 계속 참조해야 함
- "Task Section 7 참조"
- "Task Section 2 표준 참조"

→ 이게 문제네요! Jason이 원한 "Necessary Information Only"는 체크리스트에도 적용되어야 하는데, 제 체크리스트는 Task 문서 의존도가 너무 높아요.


우리 방향이 맞다 - 체크리스트는 간결하게 (500-600 lines)
하지만 과거 문서에서 보완할 요소들을 찾아야 한다

---
🔍 과거 체크리스트에서 찾은 보완 요소들

제가 4개 체크리스트를 분석하면서 발견한, 우리 가이드에 추가해야 할 것들:

1. "자주 하는 실수" 섹션 (가장 중요!)

CL-P4-005에서 발견한 패턴:
## 자주 하는 실수

### 실수 1: 순환 참조
❌ Before:
from src.infrastructure.routing import RouteManager
# infrastructure → domain 순환 참조

✅ After:
from src.domain.routing.interfaces import IRouteManager
# 인터페이스 사용

### 실수 2: print() 사용
❌ Before:
print(f"Route registered: {path}")

✅ After:
logger.info("route_registered", path=path)

이게 왜 중요한가:
- Agent가 프로젝트별 제약을 스스로 알 수 없음
- 800 lines 전체 코드 없이도 핵심 가이드라인 제공
- "Necessary Information Only" 원칙에 완벽히 부합

---
2. 구현 힌트 코드 (20-30 lines 스켈레톤)

TASK-CRAG-02에서 발견한 패턴:
# Step 3: 구현
## 3.1 핵심 로직 스켈레톤
def correct_korean(text: str) -> str:
  """한글 교정 수행."""
  # 1. hanspell 라이브러리 사용
  spelled_sent = spell_checker.check(text)

  # 2. 교정 결과 추출
  corrected = spelled_sent.checked

  # 3. 로깅 (structlog 사용)
  logger.info("korean_corrected",
              original_length=len(text),
              corrected_length=len(corrected))

  return corrected

이게 왜 필요한가:
- 전체 코드 아니고 구조만 제시
- Agent가 채워 넣으면서 구현 (복붙 아님)
- 프로젝트 표준 준수 (structlog, 함수명 컨벤션 등)

---
3. 검증 예시 출력

TASK-E1-03에서 발견한 패턴:
# Step 4: 정적 검증
$ ruff check src/bootstrap/validator.py
All checks passed!

$ mypy src/bootstrap/validator.py
Success: no issues found in 1 source file

# 예상 출력을 명시해서 Agent가 "성공"을 판단할 수 있게

---
4. 난이도 및 예상 시간 (Task 문서에서 가져옴)

V5 UNIFIED_TASK_BREAKDOWN에서 발견:
난이도: MEDIUM
예상 시간: 2-3 hours
이유: PyJWT 사용 경험 있으면 EASY, 처음이면 MEDIUM

---
5. 구현 위치 명시

# 어디에 작성하나?
파일: src/auth/token_generator.py
클래스: TokenGenerator
메서드: generate_token(user_id: str) -> str

---
📝 보완된 체크리스트 템플릿 예시

우리 원래 구조 + 과거에서 찾은 요소들:

# Checklist: T2.1.1 - JWT 토큰 생성 구현

## Meta
- 난이도: MEDIUM
- 예상 시간: 2-3 hours
- 구현 위치: src/auth/token_generator.py

---

## Step 1: 목표 이해
**이 Task로 무엇을 만드나?**
- user_id를 받아 JWT access token을 생성하는 함수

**성공 기준:**
- ruff 0, mypy 0, coverage 95%+
- Token이 1시간 후 만료
- HS256 알고리즘 사용

---

## Step 2: 테스트 작성 (TDD)

### 2.1 Given-When-Then 케이스
```python
# tests/test_token_generator.py

def test_generate_token_success():
  """Given: 유효한 user_id
     When: generate_token 호출
     Then: JWT 토큰 반환, payload에 user_id와 exp 포함"""

def test_token_expires_in_1_hour():
  """Given: 생성된 토큰
     When: 토큰 디코드
     Then: exp가 현재 + 1시간"""

def test_invalid_secret_key():
  """Given: 잘못된 SECRET_KEY
     When: 토큰 검증
     Then: InvalidTokenError 발생"""

---
Step 3: 구현

3.1 함수 시그니처

from src.auth.interfaces import ITokenGenerator

class TokenGenerator(ITokenGenerator):
  def generate_token(self, user_id: str) -> str:
      """JWT access token 생성.

      Args:
          user_id: 사용자 ID

      Returns:
          JWT access token (str)

      Raises:
          TokenGenerationError: 토큰 생성 실패 시
      """

3.2 구현 힌트 (20-30 lines 스켈레톤)

from datetime import datetime, timedelta
import jwt
from src.common.config import config
from src.common.logging import logger

def generate_token(self, user_id: str) -> str:
  # 1. Payload 구성
  payload = {
      "user_id": user_id,
      "exp": datetime.utcnow() + timedelta(hours=1)
  }

  # 2. SECRET_KEY 가져오기
  secret_key = config.get_secret("JWT_SECRET_KEY")

  # 3. 토큰 생성
  token = jwt.encode(payload, secret_key, algorithm="HS256")

  # 4. 로깅
  logger.info("token_generated", user_id=user_id)

  return token

3.3 자주 하는 실수 ⚠️

실수 1: exp를 초 단위로 제공
❌ payload["exp"] = 3600  # 숫자로 주면 안 됨
✅ payload["exp"] = datetime.utcnow() + timedelta(hours=1)

실수 2: SECRET_KEY 하드코딩
❌ SECRET_KEY = "my-secret-key-123"
✅ secret_key = config.get_secret("JWT_SECRET_KEY")

실수 3: print() 사용
❌ print(f"Token generated for {user_id}")
✅ logger.info("token_generated", user_id=user_id)

---
Step 4: 정적 검증

# Ruff 검증
$ ruff check src/auth/token_generator.py
All checks passed!

# MyPy 검증
$ mypy src/auth/token_generator.py
Success: no issues found in 1 source file

예상 출력: 위와 동일해야 함. 에러 0개.

---
Step 5: 테스트 실행

$ pytest tests/test_token_generator.py -v --cov=src.auth.token_generator

Expected Output:
tests/test_token_generator.py::test_generate_token_success PASSED
tests/test_token_generator.py::test_token_expires_in_1_hour PASSED
tests/test_token_generator.py::test_invalid_secret_key PASSED

Coverage: 96%

---
Step 6-9: 리팩토링, 재테스트, 문서화, 커밋

(기존 템플릿과 동일)

---

## 📊 개선 효과

### Before (과거 방식):
✅ 자급자족 가능
❌ 1,400+ lines (800 lines 전체 코드 포함)
❌ 작업 중복 (코드 2번 작성)
❌ 상위 문서들도 비대화

### After (보완된 우리 방식):
✅ 자급자족 가능 (실수 패턴 + 힌트로 충분)
✅ 600-700 lines (적정 크기)
✅ Agent가 스스로 구현 (복붙 아님)
✅ "Necessary Information Only" 원칙 준수
✅ 프로젝트 제약사항 명확히 전달

---

Jason, 이제 **CHECKLIST_GUIDE.md를 이 방향으로 수정**하면 될까요?

추가할 주요 내용:
1. **"자주 하는 실수" 섹션 필수** (3-5개 패턴)
2. **구현 힌트는 20-30 lines 스켈레톤**
3. **검증 예시 출력 명시**
4. **구현 위치 명시** (파일, 클래스, 메서드)
5. **난이도 및 예상 시간** (Task 문서에서 가져옴)

이 방향으로 진행할까요? 🚀

> 자자! 우리는 에이전트에게 제공하는 문서와 정보들이 있어요. 지금 보완할 사항들과 겹칠 수 잇어요.
그걸 별도의 문서로 할 것이냐 아니면 체크리스트에 포함시킬 것이냐 하는 부분도 결정해야 해요.
기준문서가 너무 과하면 안 읽을 수도 있고, 그렇다고 체크리스트에 주저리주저리 써놓다고 그걸 다
지킨다고 볼 수도 없어요. 이해 하시죠?

이건 정보 설계 (Information Architecture) 문제네요!

---
🤔 핵심 딜레마

Option A: 별도 문서로 분리
├─ PROJECT_STANDARDS.md (800 lines)
├─ COMMON_MISTAKES.md (500 lines)
├─ CODING_CONVENTIONS.md (300 lines)
└─ Checklist (200 lines - 간결!)

문제:
❌ Agent가 5개 문서 왕복하며 읽어야 함
❌ "이 Task에 관련된" 부분만 찾기 어려움
❌ 기준문서 너무 길면 안 읽을 수도 있음

Option B: 체크리스트에 전부 포함
└─ Checklist (1,500 lines - 모든 것 포함)

문제:
❌ 너무 길어서 오히려 안 읽음
❌ 이 Task와 무관한 내용도 섞임
❌ "Necessary Information Only" 위반

---
💡 제가 생각하는 핵심 질문들

1️⃣ Agent는 언제 무엇을 읽는가?

# Agent의 실제 작업 흐름:
Phase 0: Task 시작 전
→ 뭘 읽나? 청사진? 작업분해? 체크리스트?

Phase 1: 구현 중
→ 막혔을 때 뭘 찾아보나?

Phase 2: 검증 중
→ 뭘 기준으로 "맞다/틀리다" 판단하나?

2️⃣ 정보의 "거리"가 중요한가?

가까움 (체크리스트 안):
- 읽을 확률: 95%
- 하지만 관련 없는 정보도 섞임

멀음 (별도 문서):
- 읽을 확률: 30%?
- 하지만 필요할 때만 정확히 참조

3️⃣ "반복되는 것" vs "Task별 다른 것"

모든 Task에 반복:
- print() 쓰지 마라
- structlog 써라
- ruff 0, mypy 0
→ 이건 별도 문서가 나을 수도?

Task마다 다름:
- "이 Task에서 자주 하는 실수 3가지"
- "이 함수의 시그니처"
- "이 모듈의 아키텍처 제약"
→ 이건 체크리스트에 포함되어야?

---
🔍 과거 문서들에서 발견한 힌트

CL-P4-005 (1,457 lines)

## Phase 0: 사전 확인
**필독 문서:**
- PROJECT_STANDARDS.md (Line 45-67만 읽기)
- ARCHITECTURE.md (Section 3.2만 읽기)

## Step 3: 구현
### 자주 하는 실수 (이 Task 한정)
실수 1: 순환 참조
실수 2: print() 사용
실수 3: ...

이 패턴의 의미:
- ✅ 범용 기준은 별도 문서 + Line 참조
- ✅ Task별 실수는 체크리스트 내부
- ✅ "필요한 부분만" 읽게 유도

---
💭 제안: 3-Layer Information Architecture

Layer 1: Universal Standards (별도 문서, 반복 참조)
├─ PROJECT_STANDARDS.md
│   ├─ 로깅: structlog 사용 (Line 12-25)
│   ├─ 설정: config.get_secret() 사용 (Line 30-45)
│   ├─ 에러: CustomError 상속 (Line 50-68)
│   └─ 테스트: pytest + Given-When-Then (Line 70-89)
│
├─ ARCHITECTURE.md
│   ├─ 계층 구조 (Line 10-35)
│   ├─ 의존성 규칙 (Line 40-58)
│   └─ 인터페이스 패턴 (Line 60-78)
│
└─ COMMON_MISTAKES.md
  ├─ print() 금지 → structlog
  ├─ SECRET_KEY 하드코딩 금지
  └─ 순환 참조 방지 패턴

↓ Agent가 Task 시작 전 한 번 읽음 (Phase 0)

Layer 2: Task-Specific Context (체크리스트 상단)
├─ 이 Task의 목표
├─ 이 Task의 입력/출력
├─ 이 Task의 완성 기준
├─ 읽어야 할 기준 문서 Line 참조
│   예: "PROJECT_STANDARDS.md Line 12-25, 30-45만"
└─ 이 Task의 난이도/예상시간

↓ Agent가 Task 이해하며 읽음 (Step 1)

Layer 3: Implementation Guide (체크리스트 본문)
├─ Step 2: 테스트 케이스 (Given-When-Then)
├─ Step 3: 구현
│   ├─ 함수 시그니처
│   ├─ 구현 힌트 스켈레톤 (20-30 lines)
│   └─ ⚠️ 이 Task에서 자주 하는 실수 3-5개
├─ Step 4-9: 검증, 리팩토링, 커밋

↓ Agent가 실제 구현하며 읽음

---
📝 구체적 예시

PROJECT_STANDARDS.md (별도 문서, 800 lines)

## 2. 로깅 표준 (Line 12-25)
- ❌ print() 사용 금지
- ✅ structlog 사용
- 형식: logger.info("event_name", key=value)

## 3. 설정 관리 (Line 30-45)
- ❌ 환경변수 직접 os.getenv()
- ✅ config.get_secret() 사용

## 4. 에러 처리 (Line 50-68)
...

Checklist: T2.1.1 (600 lines)

# Checklist: T2.1.1 - JWT 토큰 생성

## Phase 0: 사전 확인 ✋

**필독 문서 (정확히 이 부분만!):**
- `PROJECT_STANDARDS.md` Line 12-25 (로깅)
- `PROJECT_STANDARDS.md` Line 30-45 (설정)
- `ARCHITECTURE.md` Line 40-58 (의존성 규칙)

**왜 읽나?**
- 로깅: structlog 사용법
- 설정: SECRET_KEY 가져오는 법
- 의존성: infrastructure → domain 금지

---

## Step 1: 목표 이해
(Task별 내용)

## Step 2: 테스트 작성
(Task별 Given-When-Then)

## Step 3: 구현

### 3.1 함수 시그니처
(Task별 시그니처)

### 3.2 구현 힌트 (20-30 lines)
(Task별 스켈레톤)

### 3.3 ⚠️ 이 Task에서 자주 하는 실수

**실수 1: exp를 초 단위로 제공**
❌ payload["exp"] = 3600
✅ payload["exp"] = datetime.utcnow() + timedelta(hours=1)
→ 이건 JWT Task에만 해당

**실수 2: SECRET_KEY 하드코딩**
❌ SECRET_KEY = "abc123"
✅ secret_key = config.get_secret("JWT_SECRET_KEY")
→ 이건 PROJECT_STANDARDS에도 있지만,
 JWT 맥락에서 다시 강조

**실수 3: PyJWT encode 결과 타입 혼동**
❌ return jwt.encode(...)  # bytes 반환될 수도
✅ return jwt.encode(...).decode("utf-8")
→ 이건 JWT Task 특화 실수

---
🎯 이 설계의 장점

✅ 범용 기준: 별도 문서 (800 lines)
 - 하지만 "Line 12-25만 읽어라" 명시
 - Agent가 200K 토큰 중 50 lines만 집중

✅ Task별 맥락: 체크리스트 상단 (100 lines)
 - 이 Task 목표, 입력/출력, 완성 기준
 - 어느 기준 문서 어느 부분 읽을지

✅ Task별 가이드: 체크리스트 본문 (500 lines)
 - 구현 힌트 20-30 lines
 - 이 Task 특화 실수 3-5개
 - 범용 기준은 참조만, 중복 최소화

총합:
- 체크리스트: 600 lines (적정)
- 기준 문서: 별도 관리 (중복 없음)
- Agent 읽는 양: 50 + 100 + 500 = 650 lines
(전체 1,400 lines vs 과거 방식)

---
Jason, 이 3-Layer 구조가 우리가 찾던 균형점일까요?

핵심은:
1. 반복되는 범용 기준 → 별도 문서 + Line 참조
2. Task별 특화 내용 → 체크리스트 포함
3. "어디 읽을지" 명시 → Phase 0에서 정확한 Line 지정

이 방향으로 가도 될까요? 🤔
```

