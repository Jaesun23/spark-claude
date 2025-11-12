# Checklist 작성 가이드

> **목적**: Stage 9 - TDD 기반 9-Step Checklist로 모든 기능 구현, 0 violations, 95%+ coverage 보장
>
> **버전**: v2.0 (2025-11-12)
> - v2.0: Stage 9 범위 명시, 입력/출력 문서 추가

---

## 📥 입력 문서 (Stage 8에서 받은 것)

#### 1. **`08T-01_task_breakdown.md`** (필수)
- 작업 목록 (Task 001~N)
- **활용**: 각 Task마다 Checklist 생성

#### 2. **`06D-01_project_standards.md`** (참고)
- 프로젝트 표준
- **활용**: Checklist에 표준 반영

---

## 📤 출력 문서 (이 Stage에서 생성해야 할 문서)

### 필수 문서

각 Task마다 1개씩 Checklist 생성:

#### 1. **`09L-01_task_001_checklist.md`**
#### 2. **`09L-02_task_002_checklist.md`**
#### 3. **`09L-03_task_003_checklist.md`**
...

**내용** (TDD 9-Step):
```markdown
# Task 001 Checklist: Order Entity 구현

## Step 1: 목표 이해 ✅
- [ ] Task 문서 읽기 (08T-01 Task 001)
- [ ] ADR-116 읽기
- [ ] 표준 확인 (Naming, Validation)
- [ ] 성공 기준 명확히

## Step 2: 테스트 작성 ✅
- [ ] `tests/test_order_entity.py` 생성
- [ ] 실패하는 테스트 작성
- [ ] pytest 실행 → RED 확인

## Step 3: 구현 ✅
- [ ] `src/domains/order/models.py` 생성
- [ ] Order 클래스 작성
- [ ] pytest 실행 → GREEN 확인

## Step 4: 정적 검증 ✅
- [ ] ruff check . (0 violations)
- [ ] mypy . (0 errors)

## Step 5: 단위 테스트 실행 ✅
- [ ] pytest tests/test_order_entity.py
- [ ] coverage report (95%+)

## Step 6: 리팩토링 ✅
- [ ] 중복 코드 제거
- [ ] 명명 개선
- [ ] 테스트 재실행

## Step 7: 종합 테스트 ✅
- [ ] 통합 테스트 (필요시)
- [ ] E2E 테스트 (필요시)

## Step 8: 문서화 ✅
- [ ] Docstring 작성
- [ ] README 업데이트 (필요시)

## Step 9: 커밋 ✅
- [ ] git add .
- [ ] git commit -m "..."
- [ ] PR 생성 (필요시)
```

**특징**:
- AI가 체크박스 하나씩 완료
- 0 violations 보장
- 95%+ coverage 보장

---

## 🔄 다음 Stage로 전달되는 것

Stage 9 → 구현:
- ✅ 작업별 체크리스트
- ✅ TDD 9-Step 실행 가이드
- ✅ 품질 보장 메커니즘

구현 단계에서는:
- Checklist를 따라 단계별 구현
- 모든 검증 통과 확인
- 완성된 코드 + 테스트 + 문서

---

## 1. 개요

### 목적
**Task 문서 (100줄) → 9-Step Checklist (실행 가능한 작업 지시서)**

Task 문서는 "무엇을" 만들지 정의하고, Checklist는 "어떻게" 만들지 실행 단계를 제공합니다.

### Checklist의 역할
```
Task 문서 (설계도)
    ↓
Checklist (작업 지시서)
    ↓
AI 에이전트 실행 (구현)
    ↓
완성된 코드 + 테스트 + 문서
```

### 완성 기준
- ✅ **실행 가능성**: AI가 이 Checklist만으로 Task를 완수할 수 있어야 함
- ✅ **자급자족성**: Task 문서 + Checklist만 있으면 Blueprint 없이도 작업 가능
- ✅ **검증 가능성**: 각 Step의 완료 여부를 명확히 확인 가능

---

## 2. 정보 밀도 균형점 ⚖️

### 2-1. 왜 500 lines인가?

**너무 많으면 (1,400+ lines)**:
```markdown
❌ 전체 구현 코드 400 lines 포함
❌ 전체 테스트 코드 200 lines 포함
❌ 모든 에러 처리, 엣지 케이스 포함
→ Agent가 읽기 부담스러움
→ 복붙만 하게 되어 TDD 불가능
```

**너무 적으면 (200 lines)**:
```markdown
❌ "Task 문서 Section 7 참조하세요"
❌ "PROJECT_STANDARDS.md 읽어보세요"
→ Agent가 문서 왕복하며 읽어야 함
→ 집중력 분산, 비효율적
```

**균형점 (500 lines)**: ✅
```markdown
✅ 구현 스켈레톤 (40 lines) - 핵심 로직 구조만
✅ 테스트 스켈레톤 (30 lines/케이스) - Given-When-Then + 기본 assert
✅ 자주 하는 실수 (15 lines/패턴) - ❌/✅ Before/After
✅ 프로젝트 표준 인라인 (30 lines) - 이 Task 관련만
→ Agent가 체크리스트만 보고 작업 완료
→ 스켈레톤이라 Agent가 채우며 TDD 가능
```

---

### 2-2. 구현 코드는 얼마나?

**Level 1: 인터페이스 계약** (20 lines) - **필수**
```python
def create_token(user_id: str) -> str:
    """JWT 액세스 토큰 생성.

    Args:
        user_id: 사용자 ID
    Returns:
        JWT 토큰 (1시간 유효)
    Raises:
        ValueError: user_id 빈 문자열
    """
```
→ "무엇을" 만들지 정의. Agent가 추측 불가능.

**Level 2: 아키텍처 제약** (10 lines) - **필수**
```python
# PyJWT 라이브러리 사용
# HS256 알고리즘만
# config.get_secret("JWT_SECRET_KEY") 사용
# structlog로 로깅
```
→ 프로젝트별 제약. Agent가 추측하면 틀림.

**Level 3: 구현 스켈레톤** (40 lines) - **균형점!** ✅
```python
def create_token(user_id: str) -> str:
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1)}
    secret_key = config.get_secret("JWT_SECRET_KEY")
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    logger.info("token_generated", user_id=user_id)
    return token
```
→ 핵심 로직 구조만. Agent가 에러 처리, validation 추가.

**Level 4: 전체 구현** (200+ lines) - **과함!** ❌
```python
def create_token(user_id: str) -> str:
    try:
        if not user_id:
            raise ValueError("user_id cannot be empty")
        if not isinstance(user_id, str):
            raise TypeError("user_id must be string")
        # ... 100+ lines of error handling
        # ... 50+ lines of edge case handling
    except Exception as e:
        logger.exception("unexpected_error")
        raise
```
→ 모든 엣지 케이스 포함. Agent가 복붙만 함. TDD 불가능.

**선택: Level 3 (스켈레톤)** - 이유:
- Agent가 스스로 채우며 구현 (학습 효과)
- TDD 가능 (테스트 실패 → 수정 → 통과 반복)
- "Necessary Information Only" 원칙 준수

---

### 2-3. 테스트 코드는 얼마나?

**Level 1: Given-When-Then 시나리오만** (10 lines) - **불충분** ❌
```python
def test_create_token_success():
    """Given: 유효한 user_id
       When: create_token 호출
       Then: JWT 토큰 반환"""
```
→ 구체적인 assert 없음. Agent가 어떻게 검증할지 모름.

**Level 2: 테스트 스켈레톤** (30 lines) - **균형점!** ✅
```python
def test_create_token_success():
    """Given: 유효한 user_id
       When: create_token 호출
       Then: JWT 토큰 반환"""
    # Given
    user_id = "test-user-123"
    generator = TokenGenerator()

    # When
    token = generator.create_token(user_id)

    # Then
    assert isinstance(token, str)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    assert decoded["user_id"] == user_id
    # Agent가 exp 검증 등 추가
```
→ 기본 assert 구조 제공. Agent가 세밀한 검증 추가.

**Level 3: 완전한 테스트** (100+ lines) - **과함!** ❌
```python
def test_create_token_success():
    # ... 50 lines of setup
    # ... 30 lines of execution
    # ... 20 lines of verification
```
→ 모든 검증 포함. Agent가 복붙만 함.

**선택: Level 2 (스켈레톤)** - 이유:
- Given-When-Then 구조 명확
- 기본 assert로 방향 제시
- Agent가 세밀한 검증 추가 (TDD)

---

### 2-4. 자주 하는 실수는?

**Level 1: 항목만 나열** (5 lines) - **불충분** ❌
```
실수 1: exp를 초 단위로 제공
실수 2: SECRET_KEY 하드코딩
```
→ 뭐가 잘못됐는지만. 어떻게 고쳐야 할지 모름.

**Level 2: ❌/✅ Before/After** (15 lines) - **균형점!** ✅
```python
실수 1: exp를 초 단위로 제공
❌ payload["exp"] = 3600
✅ payload["exp"] = datetime.utcnow() + timedelta(hours=1)

실수 2: SECRET_KEY 하드코딩
❌ SECRET_KEY = "my-secret-123"
✅ secret_key = config.get_secret("JWT_SECRET_KEY")
```
→ 명확한 대비. Agent가 즉시 이해.

**Level 3: 이유 + 디버깅** (30+ lines) - **과함!** ❌
```
실수 1: exp를 초 단위로 제공

❌ 잘못된 코드: ...
왜 잘못됐나? ...
어떻게 발견하나? ...
✅ 올바른 코드: ...
추가 고려사항: ...
```
→ 너무 장황. Agent가 읽기 부담.

**선택: Level 2 (Before/After)** - 이유:
- 3-5 lines로 간결
- 즉시 비교 가능
- 패턴 명확

---

### 2-5. 프로젝트 표준은 어떻게?

**Option 1: 범용 문서 참조** ❌
```markdown
## Step 3: 구현
**프로젝트 표준**: PROJECT_STANDARDS.md 참조하세요
```
→ Agent가 800 lines 문서를 언제 읽나?

**Option 2: 인라인 복사** ✅ (균형점!)
```markdown
## Step 3: 구현

### 3.1 이 Task의 프로젝트 표준

#### 로깅 (PROJECT_STANDARDS.md Line 12-25)
- logger.info("event_name", key=value) 형식
- print() 금지
- 모든 주요 작업 로깅

#### 설정 (PROJECT_STANDARDS.md Line 30-45)
- config.get_secret("KEY_NAME") 사용
- 하드코딩 금지
- 환경변수로 관리

#### 에러 (PROJECT_STANDARDS.md Line 50-68)
- CustomError 상속
- structlog로 로깅
- 사용자에게 명확한 메시지
```
→ 체크리스트에 인라인. Agent가 왕복 불필요.
→ Line 참조 유지 (추적 가능성)
→ "이 Task 관련" 부분만 (Necessary Information Only)

**선택: Option 2 (인라인)** - 이유:
- 체크리스트만으로 자급자족
- 다른 문서 참조 불필요
- 30 lines 정도로 적정

---

### 2-6. 체크리스트 크기 계산

```
Step 1: 목표 이해 (50 lines)
  - Task 목표, 입출력, 성공 기준

Step 2: 테스트 작성 (100 lines)
  - Given-When-Then 시나리오 3-5개
  - 테스트 스켈레톤 (각 20-30 lines)

Step 3: 구현 (200 lines) ← 가장 많음
  - 3.1 프로젝트 표준 인라인 (30)
  - 3.2 함수 시그니처 (20)
  - 3.3 구현 스켈레톤 (40)
  - 3.4 자주 하는 실수 (60)
  - 3.5 구현 위치 (10)

Step 4: 정적 검증 (30 lines)
  - ruff, mypy, import-linter 명령어
  - 예상 출력

Step 5: 테스트 실행 (40 lines)
  - pytest + coverage 명령어
  - 예상 출력

Step 6-9: 리팩토링/재테스트/문서화/커밋 (80 lines)

총합: 50 + 100 + 200 + 30 + 40 + 80 = 500 lines
```

---

### 2-7. 파일 분리와 Line 참조

**큰 문서 = 문제 아님!**

```markdown
# 청사진이 5,000 lines? 괜찮아!

blueprints/
├── 01_auth_system.md (500 lines)
├── 02_payment_system.md (600 lines)
├── 03_notification_system.md (450 lines)
...

# Task 작성 시:
청사진 참조: blueprints/01_auth_system.md Line 145-178
→ 500 lines 문서의 33 lines만 읽으면 됨!

# Checklist 작성 시:
그 33 lines를 인라인으로 복사
→ Agent는 체크리스트만 읽음!
```

**PROJECT_STANDARDS.md가 800 lines? 괜찮아!**

```markdown
standards/
├── 01_logging.md (150 lines)
├── 02_configuration.md (120 lines)
├── 03_error_handling.md (180 lines)
├── 04_database.md (200 lines)
...

# Task 작성 시:
표준 참조: standards/01_logging.md Line 12-25
→ 150 lines 문서의 13 lines만!

# Checklist 작성 시:
그 13 lines를 Step 3.1에 인라인
→ Agent는 체크리스트만 읽음!
```

**핵심**:
- 큰 문서는 파일로 분리 (각 200-500 lines)
- Line 참조로 정확한 부분만 지정
- 체크리스트에 인라인 복사
- Agent는 최종적으로 체크리스트 500 lines만 읽음

---

## 3. 9-Step 구조 이해

### 전체 흐름
```
┌─────────────────────────────────────────────┐
│ Phase 1: 이해 + 테스트 설계 (Step 1-2)          │
│ - 목표 명확화                                  │
│ - 테스트 케이스 작성 (TDD)                      │
├─────────────────────────────────────────────┤
│ Phase 2: 구현 + 1차 검증 (Step 3-4)            │
│ - 핵심 로직 구현                               │
│ - 정적 검증 (ruff, mypy, import-linter)       │
├─────────────────────────────────────────────┤
│ Phase 3: 테스트 + 품질 개선 (Step 5-7)          │
│ - 테스트 실행 (pytest 95%+ coverage)          │
│ - 리팩토링                                    │
│ - 재테스트                                    │
├─────────────────────────────────────────────┤
│ Phase 4: 문서화 + 제출 (Step 8-9)             │
│ - Docstring + 사용 예시                       │
│ - Git commit                                │
└─────────────────────────────────────────────┘
```

### 핵심 원칙

**TDD (Test-Driven Development)**
- Step 2에서 테스트 먼저 작성
- Step 3에서 구현
- Step 5에서 테스트 실행

**Zero-Tolerance Quality**
- Step 4: ruff 0, mypy 0, import-linter 0
- Step 5: pytest 95%+ coverage
- Step 6-7: 품질 개선 + 재검증

**Documentation First**
- Step 8: Docstring (Google 스타일)
- 사용 예시 코드 포함

---

## 3. 9-Step 상세 가이드

### Step 1: 목표 이해

**질문**: "이 Task로 무엇을 만들 것인가?"

**산출물**:
- Task 목표 명확화
- 성공 기준 정의
- Task 문서 완전 이해

**Checklist 작성법**:
```markdown
## Step 1: 목표 이해

### Task 목표
{Task 문서의 Section 4 입력/출력을 그대로 복사}

예시:
- **입력**: user_id: str
- **출력**: token: str (JWT 액세스 토큰, 1시간 유효)

### 성공 기준
{Task 문서의 Section 6 완성 기준을 그대로 복사}

예시:
- [ ] create_token(user_id) 함수 완전 작동
- [ ] pytest 테스트 3개 통과 (성공/만료/잘못된 시크릿)
- [ ] ruff 0, mypy 0, coverage 95%+
```

**도구**: Task 문서

---

### Step 2: 테스트 작성

**질문**: "어떻게 동작을 검증할 것인가?"

**산출물**:
- Given-When-Then 테스트 케이스
- 성공/실패/엣지 케이스 포함
- pytest 파일 생성

**Checklist 작성법**:
````markdown
## Step 2: 테스트 작성

### 테스트 케이스

**성공 케이스**:

```python
def test_create_token_success():
    # Given: 유효한 사용자 ID
    user_id = "user123"

    # When: 토큰 생성
    token = create_token(user_id)

    # Then: 유효한 JWT 토큰 반환
    assert isinstance(token, str)
    decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    assert decoded["user_id"] == user_id
```

**실패 케이스**:

```python
def test_create_token_expired():
    # Given: 만료된 토큰
    token = create_expired_token("user123")

    # When: 토큰 검증
    # Then: ExpiredSignatureError 발생
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
```

**엣지 케이스**:

```python
def test_create_token_invalid_secret():
    # Given: 잘못된 시크릿
    token = create_token("user123")

    # When: 잘못된 시크릿으로 검증
    # Then: InvalidSignatureError 발생
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(token, "wrong_secret", algorithms=["HS256"])
```
### 파일 생성

- `tests/test_jwt_token.py` 생성
- 위 테스트 케이스 3개 작성
````

**도구**: pytest, Task 문서 Section 6 (완성 기준)

---

### Step 3: 구현

**질문**: "핵심 로직을 어떻게 구현할 것인가?"

**산출물**:

- 실제 구현 코드 (스켈레톤 수준)
- Type hints 포함
- 프로젝트 표준 인라인 복사

**Checklist 작성법**:

````markdown
## Step 3: 구현

### 3.1 이 Task의 프로젝트 표준 (인라인 복사!)

{Task 문서 Section 6의 프로젝트 표준을 그대로 복사}

예시:

#### 로깅 (PROJECT_STANDARDS_01_로깅.md Line 12-25)
- `logger.info("event_name", key=value)` 형식 사용
- `print()` 절대 금지
- 모든 주요 작업 (생성, 수정, 삭제) 로깅 필수
- 에러는 `logger.error()` 또는 `logger.exception()` 사용

#### 설정 (PROJECT_STANDARDS_02_설정.md Line 30-45)
- 모든 SECRET은 `config.get_secret("KEY_NAME")` 사용
- 하드코딩 절대 금지
- `.env` 파일에서 환경변수 관리
- Pydantic Settings 클래스 사용

#### 에러 처리 (PROJECT_STANDARDS_03_에러.md Line 50-68)
- 프로젝트 CustomError 클래스 상속
- 모든 예외 structlog로 로깅
- 사용자에게 명확한 에러 메시지 전달

### 3.2 함수 시그니처

{Task 문서 Section 7의 함수 시그니처}

```python
def create_token(user_id: str) -> str:
    """JWT 액세스 토큰 생성.

    Args:
        user_id: 사용자 고유 ID

    Returns:
        JWT 토큰 문자열 (1시간 유효)

    Raises:
        ValueError: user_id가 빈 문자열인 경우
    """
```

### 3.3 구현 힌트 (스켈레톤!)

{Task 문서 Section 7의 구현 힌트를 Level 3 스켈레톤으로}

**핵심**: 전체 코드 아니고 40 lines 스켈레톤만!

```python
from datetime import datetime, timedelta
import jwt
from src.config import settings

def create_token(user_id: str) -> str:
    """JWT 액세스 토큰 생성."""
    # 1. Payload 구성
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    # 2. SECRET_KEY 가져오기
    secret_key = config.get_secret("JWT_SECRET_KEY")

    # 3. 토큰 생성
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    # 4. 로깅
    logger.info("token_generated", user_id=user_id)

    return token
```

**Agent가 추가해야 할 것**:
- user_id validation (빈 문자열 체크)
- 에러 처리 (try-except)
- 추가 payload 필드 (iat, jti 등)

### 3.4 자주 하는 실수 (이 Task 특화)

{Task 문서 Section 8의 실수 패턴을 ❌/✅ 형식으로}

**실수 1: exp를 초 단위로 제공**
```python
❌ payload["exp"] = 3600  # 1970년 1월 1일 1시간 후로 해석됨!
✅ payload["exp"] = datetime.utcnow() + timedelta(hours=1)
```

**실수 2: SECRET_KEY 하드코딩**
```python
❌ SECRET_KEY = "my-secret-key-123"
✅ secret_key = config.get_secret("JWT_SECRET_KEY")
```

**실수 3: print() 사용**
```python
❌ print(f"Token generated for {user_id}")
✅ logger.info("token_generated", user_id=user_id)
```

**실수 4: algorithm 파라미터 누락**
```python
❌ jwt.encode(payload, secret_key)  # 알고리즘 기본값 변경될 수 있음
✅ jwt.encode(payload, secret_key, algorithm="HS256")
```

### 3.5 구현 위치

{Task 문서 Section 7의 구현 위치}

- **파일**: `src/auth/jwt.py`
- **함수**: `create_token(user_id: str) -> str`
- **테스트**: `tests/auth/test_jwt_token.py`
````

**도구**: Task 문서 Section 6, 7, 8

---

### Step 4: 정적 검증

**질문**: "코드 품질이 표준을 만족하는가?"

**산출물**:
- ruff 0 violations
- mypy 0 errors
- import-linter 0 violations

**Checklist 작성법**:

````markdown
## Step 4: 정적 검증

### 검증 명령어

```bash
# 1. Ruff 검사 (코드 스타일)
ruff check src/auth/jwt.py tests/test_jwt_token.py
# 기대: All checks passed!

# 2. MyPy 검사 (타입 안전성)
mypy src/auth/jwt.py tests/test_jwt_token.py
# 기대: Success: no issues found

# 3. Import Linter 검사 (아키텍처 규칙)
import-linter
# 기대: All contracts passed!
```

### 위반 발견 시 조치

**Ruff 위반**:

```bash
ruff check --fix src/auth/jwt.py
```

**MyPy 에러**:

- Type hints 추가 또는 수정
- `# type: ignore` 사용 금지

**Import Linter 위반**:

- 계층 위반 수정 (domain → infrastructure 금지)
````

**도구**: ruff, mypy, import-linter

---

### Step 5: 테스트 실행

**질문**: "테스트가 통과하고 커버리지가 충분한가?"

**산출물**:
- 모든 테스트 통과
- 95%+ test coverage
- pytest 리포트

**Checklist 작성법**:

````markdown
## Step 5: 테스트 실행

### 테스트 실행 명령어

```bash
# 전체 테스트 실행 + 커버리지
pytest tests/test_jwt_token.py \
    --cov=src/auth/jwt \
    --cov-report=term-missing \
    --cov-fail-under=95
```

### 기대 결과

```
tests/test_jwt_token.py::test_create_token_success PASSED
tests/test_jwt_token.py::test_create_token_expired PASSED
tests/test_jwt_token.py::test_create_token_invalid_secret PASSED

---------- coverage: platform darwin, python 3.11 ----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
src/auth/jwt.py        12      0   100%
-------------------------------------------------
TOTAL                  12      0   100%
```

### 커버리지 부족 시 조치

- Missing 라인 확인
- 추가 테스트 케이스 작성
- 95% 이상 달성할 때까지 반복
````

**도구**: pytest, pytest-cov

---

### Step 6: 리팩토링

**질문**: "코드를 더 명확하고 유지보수 가능하게 개선할 수 있는가?"

**산출물**:
- 개선된 코드 구조
- 중복 제거
- 명확한 변수명

**Checklist 작성법**:

````markdown
## Step 6: 리팩토링

### 리팩토링 체크리스트

**코드 구조**:
- [ ] 함수 길이 50줄 이하
- [ ] 중첩 depth 3 이하
- [ ] 하나의 함수는 하나의 책임만

**가독성**:
- [ ] 변수명이 명확한가? (`t` → `token`, `u` → `user_id`)
- [ ] 매직 넘버 제거 (3600 → `HOUR_IN_SECONDS`)
- [ ] 복잡한 조건문 함수로 추출

**중복 제거**:
- [ ] 반복되는 코드 함수로 추출
- [ ] 공통 상수 별도 정의

### 리팩토링 예시

**Before**:
```python
def create_token(user_id: str) -> str:
    p = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1)}
    return jwt.encode(p, settings.jwt_secret, algorithm="HS256")
```

**After**:

```python
TOKEN_EXPIRY_HOURS = 1
JWT_ALGORITHM = "HS256"

def create_token(user_id: str) -> str:
    """JWT 액세스 토큰 생성."""
    payload = _create_payload(user_id)
    return jwt.encode(payload, settings.jwt_secret, algorithm=JWT_ALGORITHM)

def _create_payload(user_id: str) -> dict:
    """JWT payload 생성."""
    return {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
    }
```
````

**도구**: ruff (자동 리팩토링), IDE refactoring tools

---

### Step 7: 재테스트

**질문**: "리팩토링 후에도 모든 테스트가 통과하는가?"

**산출물**:
- 리팩토링 후 테스트 통과 확인
- 회귀 버그 없음 검증

**Checklist 작성법**:

```markdown
## Step 7: 재테스트

### 전체 검증 재실행

```bash
# 1. 정적 검증
ruff check src/auth/jwt.py tests/test_jwt_token.py
mypy src/auth/jwt.py tests/test_jwt_token.py
import-linter

# 2. 테스트 + 커버리지
pytest tests/test_jwt_token.py \
    --cov=src/auth/jwt \
    --cov-report=term-missing \
    --cov-fail-under=95

### 최종 확인

- [ ] ruff 0 violations
- [ ] mypy 0 errors
- [ ] import-linter 0 violations
- [ ] pytest 모든 테스트 통과
- [ ] coverage 95%+ 달성

### 실패 시 조치

- Step 6 리팩토링 재검토
- 깨진 테스트 수정
- 모든 검증 통과할 때까지 Step 6-7 반복
```

**도구**: ruff, mypy, import-linter, pytest

---

### Step 8: 문서화

**질문**: "다른 개발자가 이 코드를 쉽게 사용할 수 있는가?"

**산출물**:
- Google 스타일 docstring
- 사용 예시 코드
- 필요 시 README 업데이트

**Checklist 작성법**:

````markdown
## Step 8: 문서화

### Docstring 작성 (Google 스타일)

```python
def create_token(user_id: str) -> str:
    """JWT 액세스 토큰을 생성합니다.

    Args:
        user_id: 사용자 고유 ID (UUID 또는 문자열)

    Returns:
        JWT 토큰 문자열. 1시간 후 만료됩니다.

    Raises:
        ValueError: user_id가 빈 문자열인 경우

    Example:
        >>> token = create_token("user123")
        >>> print(token)
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

        >>> # 토큰 검증
        >>> decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        >>> print(decoded["user_id"])
        'user123'
    """
    if not user_id:
        raise ValueError("user_id cannot be empty")

    payload = _create_payload(user_id)
    return jwt.encode(payload, settings.jwt_secret, algorithm=JWT_ALGORITHM)
```

### 사용 예시 (README.md 또는 별도 파일)

## JWT 토큰 생성 사용법

### 기본 사용

```python
from src.auth.jwt import create_token

# 토큰 생성
token = create_token("user123")

# API 응답에 포함
response = {
    "access_token": token,
    "token_type": "Bearer",
    "expires_in": 3600,
}
```

### 주의사항
- 토큰은 1시간 후 자동 만료됩니다
- settings.jwt_secret은 환경변수로 설정해야 합니다
- Production에서는 반드시 HTTPS 사용
````

**도구**: Task 문서 Section 4 (입력/출력)

---

### Step 9: 커밋

**질문**: "변경사항을 Git에 안전하게 기록할 준비가 되었는가?"

**산출물**:
- Git commit with conventional commit message
- Pre-commit hooks 통과

**Checklist 작성법**:

````markdown
## Step 9: 커밋

### 커밋 전 최종 확인

```bash
# 변경된 파일 확인
git status

# 예상 결과:
# modified:   src/auth/jwt.py
# new file:   tests/test_jwt_token.py
```

### Git 커밋

```bash
# 파일 추가
git add src/auth/jwt.py tests/test_jwt_token.py

# Conventional Commit 메시지로 커밋
git commit -m "feat(auth): Add JWT token generation module

- Implement create_token() function with HS256 algorithm
- Add 3 test cases (success/expired/invalid secret)
- Achieve 100% test coverage
- Add comprehensive docstring with usage examples

Closes T2.1.1"
```

### Pre-commit Hook 검증

Pre-commit hooks가 자동 실행됩니다:

- ✅ ruff check
- ✅ mypy
- ✅ import-linter
- ✅ pytest --cov-fail-under=95

**모든 hook 통과 시**: 커밋 성공
**Hook 실패 시**: Step 4-7 재실행

### Conventional Commit 형식

- `feat`: 새 기능
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `test`: 테스트 추가
- `docs`: 문서화
````

**도구**: git, pre-commit hooks

---

## 4. Checklist 템플릿

아래 템플릿을 복사해서 각 Task마다 Checklist를 작성하세요.

````markdown
# Checklist: {Task ID} - {Task 이름}

> **Task 문서**: `docs/tasks/{Task_ID}.md`
> **생성일**: YYYY-MM-DD
> **예상 소요**: {Task 문서 Section 8 참조}

---

## Step 1: 목표 이해

### Task 목표
{Task 문서 Section 4: 입력/출력}

### 성공 기준
{Task 문서 Section 6: 완성 기준}

---

## Step 2: 테스트 작성

### 테스트 케이스

**성공 케이스**:

```python
def test_{function_name}_success():
    # Given:

    # When:

    # Then:
```

**실패 케이스**:

```python
def test_{function_name}_failure():
    # Given:

    # When:

    # Then:
```

**엣지 케이스**:

```python
def test_{function_name}_edge():
    # Given:

    # When:

    # Then:
```

### 파일 생성

- `tests/test_{module}.py` 생성

---

## Step 3: 구현

### 구현 위치

{Task 문서 Section 7: 구현 힌트}

### 구현 코드

```python
{실제 구현 코드}
```

### 프로젝트 표준 준수

{Task 문서 Section 2: 프로젝트 표준 참조}

---

## Step 4: 정적 검증

### 검증 명령어

```bash
ruff check {파일 경로}
mypy {파일 경로}
import-linter
```

### 기대 결과

- [ ] ruff 0 violations
- [ ] mypy 0 errors
- [ ] import-linter 0 violations

---

## Step 5: 테스트 실행

### 테스트 실행 명령어

```bash
pytest {테스트 파일} \
    --cov={모듈 경로} \
    --cov-report=term-missing \
    --cov-fail-under=95
```

### 기대 결과

- [ ] 모든 테스트 통과
- [ ] Coverage 95%+ 달성

---

## Step 6: 리팩토링

### 리팩토링 체크리스트

- [ ] 함수 길이 50줄 이하
- [ ] 중첩 depth 3 이하
- [ ] 변수명 명확
- [ ] 매직 넘버 제거
- [ ] 중복 코드 제거

---

## Step 7: 재테스트

### 전체 검증 재실행

```bash
ruff check {파일들}
mypy {파일들}
import-linter
pytest {테스트 파일} --cov={모듈} --cov-fail-under=95
```

### 최종 확인

- [ ] ruff 0 violations
- [ ] mypy 0 errors
- [ ] import-linter 0 violations
- [ ] pytest 모든 테스트 통과
- [ ] coverage 95%+ 달성

---

## Step 8: 문서화

### Docstring (Google 스타일)

```python
def {function_name}({args}):
    """{한 줄 요약}.

    Args:
        {arg}: {설명}

    Returns:
        {반환값 설명}

    Raises:
        {예외}: {발생 조건}

    Example:
        >>> {사용 예시}
    """
```

### 사용 예시

```python
{실제 사용 예시 코드}
```

---

## Step 9: 커밋

### Git 커밋

```bash
git add {파일들}

git commit -m "feat({scope}): {요약}

- {변경사항 1}
- {변경사항 2}

Closes {Task ID}"
```

### Pre-commit Hook 검증

- [ ] ruff check 통과
- [ ] mypy 통과
- [ ] import-linter 통과
- [ ] pytest 통과

---

## 완료 확인

- [ ] 9 Steps 모두 완료
- [ ] 모든 품질 기준 만족
- [ ] Git commit 성공
````

---

## 5. 실전 예시: Task T2.1.1 → Checklist

Task 문서에서 Checklist로 변환하는 과정을 보여드립니다.

### Task 문서 (요약)

```
# Task T2.1.1: JWT 토큰 생성 모듈

## 1. 📘 청사진 참조
Blueprint Line 145-178

## 2. 📋 프로젝트 표준 참조
PROJECT_STANDARDS.md Line 12-25 (structlog)
PROJECT_STANDARDS.md Line 45-58 (Pydantic Settings)

## 3. 🔧 사용 도구
- PyJWT

## 4. 📦 입력/출력
**입력**: user_id: str
**출력**: token: str - JWT 액세스 토큰

## 5. 🔗 조립 정보
**이 블럭을 사용하는 Task**: T2.2.1, T2.2.3
**이 블럭이 사용하는 Task**: 없음

## 6. 🎯 완성 기준
- [ ] create_token(user_id) 함수 완전 작동
- [ ] pytest 테스트 3개 통과
- [ ] ruff 0, mypy 0, coverage 95%+

## 7. 💡 구현 힌트
```python
def create_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

## 8. ⏱️ 예상 작업 시간

2-3 hours
```

### Checklist (완성본)

````markdown
# Checklist: T2.1.1 - JWT 토큰 생성 모듈

> **Task 문서**: `docs/tasks/T2.1.1_JWT_Token_Generation.md`
> **생성일**: 2025-01-09
> **예상 소요**: 2-3 hours

---

## Step 1: 목표 이해

### Task 목표
- **입력**: `user_id: str` - 사용자 고유 ID
- **출력**: `token: str` - JWT 액세스 토큰 (1시간 유효)

### 성공 기준
- [ ] `create_token(user_id)` 함수 완전 작동
- [ ] pytest 테스트 3개 통과 (성공/만료/잘못된 시크릿)
- [ ] ruff 0, mypy 0, coverage 95%+

---

## Step 2: 테스트 작성

### 테스트 케이스

**성공 케이스**:
```python
def test_create_token_success():
    # Given: 유효한 사용자 ID
    user_id = "user123"

    # When: 토큰 생성
    token = create_token(user_id)

    # Then: 유효한 JWT 토큰 반환
    assert isinstance(token, str)
    decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    assert decoded["user_id"] == user_id
    assert "exp" in decoded
```
**실패 케이스**:

```python
def test_create_token_expired():
    # Given: 만료된 토큰
    with freeze_time("2025-01-01 12:00:00"):
        token = create_token("user123")

    # When: 1시간 후 검증
    with freeze_time("2025-01-01 13:00:01"):
        # Then: ExpiredSignatureError 발생
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
```

**엣지 케이스**:

```python
def test_create_token_invalid_secret():
    # Given: 유효한 토큰
    token = create_token("user123")

    # When: 잘못된 시크릿으로 검증
    # Then: InvalidSignatureError 발생
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(token, "wrong_secret", algorithms=["HS256"])
```

### 파일 생성

- `tests/auth/test_jwt_token.py` 생성
- 위 테스트 케이스 3개 작성

---

## Step 3: 구현

### 구현 위치

- **파일**: `src/auth/jwt.py`
- **함수**: `create_token(user_id: str) -> str`

### 구현 코드

```python
"""JWT 토큰 생성 및 검증 모듈."""
from datetime import datetime, timedelta
import jwt
from src.config import settings

# 상수 정의
TOKEN_EXPIRY_HOURS = 1
JWT_ALGORITHM = "HS256"


def create_token(user_id: str) -> str:
    """JWT 액세스 토큰을 생성합니다.

    Args:
        user_id: 사용자 고유 ID

    Returns:
        JWT 토큰 문자열 (1시간 유효)

    Raises:
        ValueError: user_id가 빈 문자열인 경우
    """
    if not user_id:
        raise ValueError("user_id cannot be empty")

    payload = _create_payload(user_id)
    return jwt.encode(payload, settings.jwt_secret, algorithm=JWT_ALGORITHM)


def _create_payload(user_id: str) -> dict:
    """JWT payload를 생성합니다.

    Args:
        user_id: 사용자 고유 ID

    Returns:
        JWT payload 딕셔너리
    """
    return {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
    }
```

### 프로젝트 표준 준수

**참조**: Task 문서 Section 2

- ✅ **structlog**: 에러 발생 시 structlog 사용 (이 모듈은 에러 로깅 불필요)
- ✅ **Pydantic Settings**: `settings.jwt_secret` 사용
- ✅ **Type hints**: 100% 타입 힌트 적용

---

## Step 4: 정적 검증

### 검증 명령어

```bash
# 1. Ruff 검사
ruff check src/auth/jwt.py tests/auth/test_jwt_token.py

# 2. MyPy 검사
mypy src/auth/jwt.py tests/auth/test_jwt_token.py

# 3. Import Linter 검사
import-linter
```

### 기대 결과

- [ ] ruff 0 violations
- [ ] mypy 0 errors
- [ ] import-linter 0 violations (auth 모듈은 domain 계층 의존성 없음)

### 위반 발견 시 조치

**Ruff 위반 예시**:

```bash
# 자동 수정
ruff check --fix src/auth/jwt.py
```

**MyPy 에러 예시**:

```python
# ❌ Before
def create_token(user_id):
    return jwt.encode(...)

# ✅ After
def create_token(user_id: str) -> str:
    return jwt.encode(...)
```

---

## Step 5: 테스트 실행

### 테스트 실행 명령어

```bash
pytest tests/auth/test_jwt_token.py \
    --cov=src/auth/jwt \
    --cov-report=term-missing \
    --cov-fail-under=95 \
    -v
```

### 기대 결과

```
tests/auth/test_jwt_token.py::test_create_token_success PASSED         [ 33%]
tests/auth/test_jwt_token.py::test_create_token_expired PASSED         [ 66%]
tests/auth/test_jwt_token.py::test_create_token_invalid_secret PASSED  [100%]

---------- coverage: platform darwin, python 3.11 ----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
src/auth/jwt.py        15      0   100%
-------------------------------------------------
TOTAL                  15      0   100%

Required test coverage of 95% reached. Total coverage: 100.00%
```

### 체크리스트

- [ ] 모든 테스트 통과 (3/3)
- [ ] Coverage 95%+ 달성 (100%)
- [ ] Missing 라인 없음

---

## Step 6: 리팩토링

### 리팩토링 체크리스트

**코드 구조**:

- [x] 함수 길이 50줄 이하 (create_token: 10줄, _create_payload: 5줄)
- [x] 중첩 depth 3 이하 (최대 depth: 1)
- [x] 하나의 함수는 하나의 책임만

**가독성**:

- [x] 변수명이 명확한가? (payload, user_id 모두 명확)
- [x] 매직 넘버 제거 (TOKEN_EXPIRY_HOURS, JWT_ALGORITHM 상수화)
- [x] 복잡한 조건문 함수로 추출 (해당 없음)

**중복 제거**:

- [x] 반복되는 코드 함수로 추출 (_create_payload 분리)
- [x] 공통 상수 별도 정의 (모듈 최상단에 정의)

### 개선 사항

**개선 전** (Task 문서 구현 힌트):

```python
def create_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
```

**개선 후** (Step 3 구현):

- ✅ 상수 분리 (`TOKEN_EXPIRY_HOURS`, `JWT_ALGORITHM`)
- ✅ Payload 생성 함수 분리 (`_create_payload`)
- ✅ Validation 추가 (`user_id` 빈 문자열 체크)
- ✅ Docstring 추가 (Google 스타일)

---

## Step 7: 재테스트

### 전체 검증 재실행

```bash
# 1. 정적 검증
ruff check src/auth/jwt.py tests/auth/test_jwt_token.py
mypy src/auth/jwt.py tests/auth/test_jwt_token.py
import-linter

# 2. 테스트 + 커버리지
pytest tests/auth/test_jwt_token.py \
    --cov=src/auth/jwt \
    --cov-report=term-missing \
    --cov-fail-under=95
```

### 최종 확인

- [ ] ruff 0 violations ✅
- [ ] mypy 0 errors ✅
- [ ] import-linter 0 violations ✅
- [ ] pytest 모든 테스트 통과 (3/3) ✅
- [ ] coverage 100% 달성 ✅

### 회귀 테스트

리팩토링으로 인한 동작 변경 없음 확인:

- [ ] `create_token("user123")` 여전히 유효한 토큰 반환
- [ ] 만료 시간 여전히 1시간
- [ ] 알고리즘 여전히 HS256

---

## Step 8: 문서화

### Docstring (Google 스타일)

**이미 Step 3에서 작성 완료**:

```python
def create_token(user_id: str) -> str:
    """JWT 액세스 토큰을 생성합니다.

    Args:
        user_id: 사용자 고유 ID

    Returns:
        JWT 토큰 문자열 (1시간 유효)

    Raises:
        ValueError: user_id가 빈 문자열인 경우
    """
```

### 사용 예시 추가 (Docstring에 Example 섹션)

```python
def create_token(user_id: str) -> str:
    """JWT 액세스 토큰을 생성합니다.

    Args:
        user_id: 사용자 고유 ID

    Returns:
        JWT 토큰 문자열 (1시간 유효)

    Raises:
        ValueError: user_id가 빈 문자열인 경우

    Example:
        >>> from src.auth.jwt import create_token
        >>> token = create_token("user123")
        >>> print(token[:20])  # 토큰 앞부분 출력
        'eyJhbGciOiJIUzI1NiI...'

        >>> # 토큰 검증 예시
        >>> import jwt
        >>> from src.config import settings
        >>> decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        >>> print(decoded["user_id"])
        'user123'
    """
```

### README 업데이트 (필요 시)

`docs/auth/JWT_USAGE.md` 생성:

```markdown
# JWT 토큰 사용 가이드

## 개요
이 모듈은 HS256 알고리즘을 사용하여 JWT 액세스 토큰을 생성합니다.

## 기본 사용법

### 토큰 생성
\```python
from src.auth.jwt import create_token

token = create_token("user123")
print(f"Generated token: {token}")
\```

### 토큰 검증
\```python
import jwt
from src.config import settings

try:
    decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    user_id = decoded["user_id"]
    print(f"Valid token for user: {user_id}")
except jwt.ExpiredSignatureError:
    print("Token expired")
except jwt.InvalidSignatureError:
    print("Invalid token")
\```

## 설정

### 환경 변수
\```bash
# .env 파일
JWT_SECRET=your-secret-key-here
\```

### Settings 클래스
\```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str

settings = Settings()
\```

## 주의사항
- ⚠️ `JWT_SECRET`은 최소 32자 이상 강력한 암호를 사용하세요
- ⚠️ Production 환경에서는 반드시 HTTPS를 사용하세요
- ⚠️ 토큰은 1시간 후 자동 만료됩니다 (Refresh token 구현 권장)

## 관련 Task
- **T2.2.1**: JWT 토큰 검증 모듈
- **T2.2.3**: Login 엔드포인트 (이 모듈 사용)
```

---

## Step 9: 커밋

### 커밋 전 최종 확인

```bash
# 변경된 파일 확인
git status

# 예상 결과:
# new file:   src/auth/jwt.py
# new file:   tests/auth/test_jwt_token.py
# new file:   docs/auth/JWT_USAGE.md
```

### Git 커밋

```bash
# 파일 추가
git add src/auth/jwt.py tests/auth/test_jwt_token.py docs/auth/JWT_USAGE.md

# Conventional Commit 메시지로 커밋
git commit -m "feat(auth): Add JWT token generation module

- Implement create_token() function with HS256 algorithm
- Add TOKEN_EXPIRY_HOURS and JWT_ALGORITHM constants
- Extract _create_payload() for better testability
- Add 3 test cases: success, expired, invalid secret
- Achieve 100% test coverage
- Add comprehensive docstring with usage examples
- Create JWT usage guide documentation

Standards compliance:
- ruff 0 violations
- mypy 0 errors
- import-linter 0 violations
- pytest coverage 100%

Closes T2.1.1"
```

### Pre-commit Hook 검증

Pre-commit hooks 자동 실행:

```
[ruff] ................................................ Passed
[mypy] ................................................ Passed
[import-linter] ....................................... Passed
[pytest] .............................................. Passed
  - All tests passed (3/3)
  - Coverage: 100%
[commit-msg] .......................................... Passed
```

### 커밋 성공 확인

```bash
git log -1 --oneline
# f8a9c21 feat(auth): Add JWT token generation module

git show --stat
# 파일 변경 내역 확인
```

---

## 완료 확인

- [x] Step 1: 목표 이해 완료
- [x] Step 2: 테스트 3개 작성 완료
- [x] Step 3: 구현 완료 (create_token, _create_payload)
- [x] Step 4: 정적 검증 통과 (ruff 0, mypy 0, import-linter 0)
- [x] Step 5: 테스트 실행 통과 (100% coverage)
- [x] Step 6: 리팩토링 완료 (상수 분리, 함수 분리)
- [x] Step 7: 재테스트 통과 (모든 검증 재확인)
- [x] Step 8: 문서화 완료 (docstring + README)
- [x] Step 9: Git 커밋 성공

### 최종 산출물

✅ `src/auth/jwt.py` - JWT 토큰 생성 모듈 (100% coverage)
✅ `tests/auth/test_jwt_token.py` - 테스트 3개 (모두 통과)
✅ `docs/auth/JWT_USAGE.md` - 사용 가이드
✅ Git commit `f8a9c21` - Task T2.1.1 완료

**Task T2.1.1 완료! 다음 Task로 진행 가능.**
````

---

## 6. Checklist 작성 완료 검증

```markdown
### 완성도 체크리스트

**기본 요구사항**:

- [ ] 9-Step 모두 포함
- [ ] 각 Step마다 질문, 산출물, 도구 명시
- [ ] Task 문서와 명확히 연결 (Section 참조)

**실행 가능성**:

- [ ] AI가 이 Checklist만으로 작업 가능
- [ ] 모든 명령어가 실행 가능 (복사-붙여넣기 가능)
- [ ] 검증 기준이 명확 (✅/❌ 판단 가능)

**Task 문서 연결**:

- [ ] Section 1 (청사진) → Step 1 목표 이해
- [ ] Section 2 (표준) → Step 3, 4 준수 확인
- [ ] Section 3 (도구) → Step 2-5 사용
- [ ] Section 4 (입출력) → Step 1 목표, Step 8 문서화
- [ ] Section 5 (조립) → Step 1 이해 (의존성 파악)
- [ ] Section 6 (완성 기준) → Step 1, 7 검증
- [ ] Section 7 (구현 힌트) → Step 3 구현
- [ ] Section 8 (예상 시간) → Checklist 메타정보

**품질 검증**:

- [ ] Step 4: ruff, mypy, import-linter 명령어 정확
- [ ] Step 5: pytest coverage 명령어 정확
- [ ] Step 6-7: 리팩토링 후 재검증 포함
- [ ] Step 9: Conventional commit 형식 준수

### 흔한 실수 체크

**❌ 피해야 할 패턴**:

- Step 2에서 테스트 작성 없이 "테스트 작성 예정" 표시
- Step 3 구현이 너무 추상적 (실제 코드 없음)
- Step 4-7 검증 명령어 누락
- Step 8 docstring 없이 "문서화 완료" 표시
- Step 9 커밋 메시지가 Conventional Commit 형식 위반

**✅ 올바른 패턴**:

- 모든 Step에 실제 코드 또는 명령어 포함
- 검증 기준이 숫자로 명확 (ruff 0, coverage 95%+)
- Task 문서 내용을 직접 복사-참조
- 예시 코드가 실행 가능
```

## 7. Checklist와 Task 문서의 관계

### 정보 흐름

```markdown
Blueprint (5000 lines, 전체 설계)
    ↓
Task 문서 (100 lines, 이 작업만)
    ├─ Section 1: 청사진 참조 → "Blueprint Line 145-178만 읽어"
    ├─ Section 2: 표준 참조 → "PROJECT_STANDARDS.md Line 12-25만 읽어"
    ├─ Section 3: 도구 → "PyJWT 사용해"
    ├─ Section 4: 입출력 → "user_id 받아서 token 반환해"
    ├─ Section 5: 조립 → "T2.2.1, T2.2.3이 이걸 사용해"
    ├─ Section 6: 완성 기준 → "함수 작동 + 테스트 3개 + 0 위반"
    ├─ Section 7: 구현 힌트 → "이렇게 만들어"
    └─ Section 8: 예상 시간 → "2-3시간"
    ↓
Checklist (실행 지시서)
    ├─ Step 1: Task 문서 이해
    ├─ Step 2: 테스트 작성 (Given-When-Then)
    ├─ Step 3: 구현 (Section 7 힌트 사용)
    ├─ Step 4: 정적 검증 (ruff, mypy, import-linter)
    ├─ Step 5: 테스트 실행 (pytest coverage)
    ├─ Step 6: 리팩토링
    ├─ Step 7: 재테스트
    ├─ Step 8: 문서화
    └─ Step 9: 커밋
    ↓
완성된 코드 + 테스트 + 문서
```
### Necessary Information Only 원칙

**Blueprint (5000 lines)**:
- AI가 읽을 필요 없음 (너무 많음)
- Task 문서가 필요한 부분만 추출함

**Task 문서 (100 lines)**:
- AI가 읽어야 함
- "무엇을" 만들지 정의

**Checklist (실행 단계)**:
- AI가 따라야 함
- "어떻게" 만들지 단계별 지시

**핵심**: AI는 Blueprint를 직접 읽지 않고, Task 문서와 Checklist만으로 작업 완수 가능

---

## 8. 추가 참고 자료

### 관련 문서
- **CORE_METHODOLOGY.md Section 3**: 9-Step Checklist 상세 설명
- **TASK_BREAKDOWN_GUIDE.md**: Task 문서 작성 방법
- **PROJECT_STANDARDS.md**: 프로젝트 표준 (structlog, Pydantic, 아키텍처 규칙)

### 도구 문서
- **pytest**: https://docs.pytest.org/
- **ruff**: https://docs.astral.sh/ruff/
- **mypy**: https://mypy.readthedocs.io/
- **import-linter**: https://import-linter.readthedocs.io/

### Conventional Commit

```
<type>(<scope>): <subject>

<body>

<footer>
```
**Type**:

- `feat`: 새 기능
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `test`: 테스트 추가
- `docs`: 문서화

**Scope**: 변경된 모듈 (auth, payment, user 등)

**Footer**: `Closes T2.1.1` 형식으로 Task 참조

---

## 마무리

이 가이드를 사용하여:
1. **Task 문서 읽기** (TASK_BREAKDOWN_GUIDE 참조)
2. **Checklist 템플릿 복사** (Section 4)
3. **9-Step 순서대로 작성** (Section 3 참조)
4. **실전 예시 참고** (Section 5)
5. **검증 체크리스트 확인** (Section 6)

**핵심 원칙**:
- ✅ **실행 가능**: 모든 명령어가 복사-붙여넣기 가능
- ✅ **자급자족**: Task 문서 + Checklist만으로 완수 가능
- ✅ **검증 가능**: 0 violations, 95%+ coverage 명확히 확인

Happy coding! 🚀
