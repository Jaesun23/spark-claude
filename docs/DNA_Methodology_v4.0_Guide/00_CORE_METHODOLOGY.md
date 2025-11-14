# 핵심 개발 방법론 (DNA v3.6 Essence)

> **SPARK의 기반이 되는 핵심 원칙과 구조**

---

## 🎯 방법론의 본질

**"방법론 = WHAT TO CHOICE + HOW TO DESIGN + WHY"**

- **WHAT TO CHOICE**: 검증된 도구 중 최적 선택
- **HOW TO DESIGN**: 선택한 방안을 어떻게 설계/구조화
- **WHY**: 왜 이런 선택과 설계를 해야 하는가

---

## 1. 표준 도구 우선 원칙 (바퀴 재발명 금지)

### 바퀴 재발명의 대가
```python
# ❌ 실패 사례: 타입 시스템 직접 구현
- 89개 커스텀 타입 클래스 (1,679줄)
- MyPy 312개 오류
→ 결과: 프로젝트 중단

# ✅ 표준 도구 사용
from pydantic import BaseModel
from structlog import get_logger
# 3줄로 해결
```

### 도구 선택 3단계 검증

1. **필요성**: 이미 표준 도구가 있는가?
2. **성숙도**: GitHub 10k+ stars, 활발한 유지보수, Python 3.12+ 지원
3. **생태계**: MyPy/IDE 호환, 다른 도구와 연동

### 표준 도구 스택 (2025년 기준)

| 시스템 | 표준 도구 | 금지 사항 |
|--------|----------|----------|
| 타입/검증 | Pydantic v2 | 커스텀 검증 시스템 |
| 로깅 | structlog | print(), 커스텀 로거 |
| 테스트 | pytest | unittest, 수동 mocking |
| 설정 | pydantic-settings | 수동 환경변수 파싱 |
| API | FastAPI | 수동 타입 검증 |
| 데이터 | polars | pandas + 수동 검증 |

---

## 2. 작업의 계층적 분해

```
Project (전체 건물)
└── Stage (층) - 7단계 진화
    └── Phase (방) - 기능 영역
        └── Task (레고블럭) ← 핵심! 최소 기능 단위
            └── Step (조립단계) - 9-Step 체크리스트
                └── Action (구체적 행동)
```

### Task의 정의 (가장 중요!)

**Task = 완성된 레고블럭 (Complete Lego Block)**

> "Task는 라인 수나 테스트 개수로 정하는 게 아니에요. 이 Task가 완료되었을 때 결과물은 하나의 '레고블럭'이에요." - Jason

#### ✅ 올바른 Task (완성된 레고블럭)
- **독립적으로 테스트 가능**: 다른 Task 없이도 테스트 작동
- **TODO 없는 완전한 구현**: 이 블럭 안에서는 완성
- **표준 도구 활용**: 일관성 유지
- **ruff, MyPy 0 오류**: 품질 기준 충족
- **혼자서도 작동 가능**: 다른 블럭 없이도 의미 있음
- **다른 블럭과 조립 가능**: 레고처럼 결합 가능

**중요**: 라인 수나 테스트 개수는 기준이 **아님**! 기능의 완성도가 기준!

#### 예시: 인증 시스템의 Task 분해

```markdown
# ✅ 올바른 Task 분해

Task T1.1.1: JWT 토큰 생성 기능
- create_token(user_id) → JWT 문자열 반환
- 완전한 기능 (TODO 없음)
- pytest 테스트 3개 (성공, 만료, 잘못된 페이로드)
→ 완성된 레고블럭!

Task T2.1.1: POST /auth/login 엔드포인트
- 로그인 엔드포인트만 구현 (로그아웃 없어도 OK!)
- 비밀번호 검증, JWT 생성, Redis 저장
- 완전한 기능 (TODO 없음)
- pytest 테스트 5개
→ 완성된 레고블럭!

Task T2.2.1: POST /auth/logout 엔드포인트
- 로그아웃 엔드포인트만 구현
- 토큰 블랙리스트, Redis 삭제
- 완전한 기능 (TODO 없음)
→ 완성된 레고블럭!
```

```markdown
# ❌ 잘못된 Task 분해

Task: 인증 시스템 구현
- 로그인, 로그아웃, JWT, Redis 전부
- 너무 큼, 레고블럭이 아님!

Task: 로그인 함수 뼈대
- def login(): # TODO: 구현
- 미완성, 레고블럭이 아님!
```

### Task 분할의 두 가지 방식 (가장 중요!)

> "이렇게 작업을 나누는 부분이 진짜 중요한 거에요." - Jason

#### Case 1: 모듈화 분할 (수평 분할)

**전략**: 독립적인 모듈을 먼저 만들고, 나중에 조립

```python
# Task 1: JWT 토큰 생성 모듈 (독립 블럭)
def create_token(user_id: str) -> str:
    """JWT 액세스 토큰 생성"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    # ✅ 완전히 작동
    # ✅ 단독 테스트 가능
    # ✅ 의존성 없음
    # → 완성된 레고블럭!

# Task 2: JWT 토큰 검증 모듈 (독립 블럭)
def validate_token(token: str) -> dict | None:
    """JWT 토큰 검증 및 페이로드 반환"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    # ✅ 완전히 작동
    # ✅ 단독 테스트 가능
    # ✅ Task 1과 일관된 패턴
    # → 완성된 레고블럭!

# Task 3: Login 엔드포인트 (Task 1, 2 조립)
@app.post("/auth/login")
def login(request: LoginRequest) -> LoginResponse:
    """사용자 로그인"""
    user = authenticate_user(request.email, request.password)
    if not user:
        raise InvalidCredentialsError()

    # Task 1의 블럭 사용
    access_token = create_token(user.id)

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=3600
    )
    # ✅ Task 1, 2를 조립
    # ✅ 완전히 작동
    # → 완성된 레고블럭!
```

**특징**:
- ✅ 각 모듈이 완전히 독립적
- ✅ 재사용 가능 (다른 엔드포인트에서도 사용)
- ✅ 테스트 용이 (각 모듈 단독 테스트)
- ✅ 명확한 조립 순서 (Task 1, 2 → Task 3)

#### Case 2: 단계별 구현 (수직 분할)

**전략**: 한 기능을 완전히 구현하고, 다음 기능으로 확장

```python
# Task 1: Login 기능만 (완전 구현)
@app.post("/auth/login")
def login(request: LoginRequest) -> LoginResponse:
    """사용자 로그인 - 완전 구현"""
    # 사용자 검증
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise InvalidCredentialsError()

    # JWT 토큰 생성 (인라인)
    payload = {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=1)}
    access_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    # Redis 저장
    redis.setex(f"token:{user.id}", 3600, access_token)

    # 로깅
    logger.info("user_logged_in", user_id=user.id, email=user.email)

    return LoginResponse(access_token=access_token, token_type="bearer")
    # ✅ Login 기능 완전 작동
    # ✅ 토큰 생성, 저장, 로깅 모두 포함
    # ✅ Logout, Refresh는 미구현이지만 OK!
    # → "Login 레고블럭" 완성!

# Task 2: Logout 기능 (완전 구현, Task 1과 일관성)
@app.post("/auth/logout")
def logout(token: str = Depends(oauth2_scheme)) -> dict:
    """사용자 로그아웃 - 완전 구현"""
    # 토큰 검증 (Task 1과 같은 방식)
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    user_id = payload["user_id"]

    # Redis 삭제 (Task 1과 같은 Redis)
    redis.delete(f"token:{user_id}")

    # 블랙리스트 추가
    redis.sadd("blacklist", token)

    # 로깅 (Task 1과 같은 structlog)
    logger.info("user_logged_out", user_id=user_id)

    return {"message": "Successfully logged out"}
    # ✅ Logout 기능 완전 작동
    # ✅ Task 1과 일관된 패턴 (jwt, redis, structlog)
    # → "Logout 레고블럭" 완성!

# Task 3: Token Refresh (완전 구현, Task 1, 2와 일관성)
@app.post("/auth/refresh")
def refresh_token(refresh_token: str) -> LoginResponse:
    """토큰 갱신 - 완전 구현"""
    # 토큰 검증 (Task 1, 2와 같은 방식)
    payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

    # 새 토큰 생성 (Task 1과 같은 방식)
    new_payload = {"user_id": payload["user_id"], "exp": datetime.utcnow() + timedelta(hours=1)}
    new_token = jwt.encode(new_payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    # Redis 업데이트 (Task 1, 2와 같은 Redis)
    redis.setex(f"token:{payload['user_id']}", 3600, new_token)

    # 로깅 (Task 1, 2와 같은 structlog)
    logger.info("token_refreshed", user_id=payload["user_id"])

    return LoginResponse(access_token=new_token, token_type="bearer")
    # ✅ Refresh 기능 완전 작동
    # ✅ Task 1, 2와 완전히 일관된 패턴
    # → "Refresh 레고블럭" 완성!
```

**특징**:
- ✅ 각 기능이 완전히 독립적으로 작동
- ✅ 부분 배포 가능 (Login만 먼저 배포 OK)
- ✅ 일관된 패턴 유지 (jwt, redis, structlog 반복)
- ✅ 점진적 확장 (Task 1 → Task 2 → Task 3)

### 두 가지 방식의 선택 기준

#### Case 1 (모듈화)을 선택할 때:

```
✅ 재사용이 많을 때
   - create_token()을 여러 엔드포인트에서 사용
   - validate_token()을 미들웨어에서도 사용

✅ 복잡도가 높을 때
   - JWT 로직이 복잡해서 분리 필요
   - 각 모듈을 독립적으로 테스트해야 함

✅ 팀 협업이 필요할 때
   - A팀: JWT 모듈 개발
   - B팀: API 엔드포인트 개발
   - 병렬 작업 가능
```

#### Case 2 (단계별)를 선택할 때:

```
✅ 빠른 배포가 필요할 때
   - Login만 먼저 배포
   - Logout은 다음 스프린트에

✅ 기능이 단순할 때
   - JWT 로직이 간단
   - 재사용이 적음

✅ 학습 곡선이 있을 때
   - Login 구현하며 패턴 확립
   - 같은 패턴을 Logout, Refresh에 적용
```

### 레고블럭 조립의 핵심

#### 조립 가능한 블럭의 조건

```python
# ✅ 조립 가능한 블럭
def create_token(user_id: str) -> str:
    """명확한 입력과 출력"""
    # 입력: user_id (str)
    # 출력: token (str)
    # 의존성: settings.JWT_SECRET_KEY (환경 설정)
    # 부작용: 없음 (순수 함수)
    pass

# ✅ 이 블럭은 어디서든 조립 가능
login() → create_token(user.id)
refresh() → create_token(user.id)
api_key_gen() → create_token(service_id)
```

```python
# ❌ 조립 불가능한 블럭
def messy_function():
    """불명확한 인터페이스"""
    # 전역 변수 사용
    # 부작용 많음
    # 입출력 불명확
    pass

# ❌ 이 블럭은 조립 어려움
```

### 두 가지 필수 조건

**1️⃣ 일관성 (Consistency)**

```python
# ✅ 일관된 패턴

# Task 1: Login
from core.logging import get_logger
from core.types import LoginRequest, LoginResponse
from core.errors import InvalidCredentialsError

logger = get_logger()

@app.post("/auth/login")
def login(request: LoginRequest) -> LoginResponse:
    logger.info("login_attempt", email=request.email)
    # ...

# Task 2: Logout (Task 1과 똑같은 패턴!)
from core.logging import get_logger  # ✅ 같은 로깅
from core.types import LogoutResponse  # ✅ 같은 타입
from core.errors import InvalidTokenError  # ✅ 같은 에러

logger = get_logger()

@app.post("/auth/logout")
def logout(token: str) -> LogoutResponse:
    logger.info("logout_attempt", token=token)  # ✅ 같은 로깅 패턴
    # ...

→ 같은 스타일, 같은 도구, 같은 구조!
→ DNA 시스템이 이 일관성을 강제!
```

**2️⃣ 누락없음 (No Omissions)**

```markdown
# ✅ 청사진에서 계획한 모든 Task 완료

청사진 (Blueprint):
├── Task 1.1: JWT 토큰 생성 ✓ (완료)
├── Task 1.2: JWT 토큰 검증 ✓ (완료)
├── Task 2.1: Login 엔드포인트 ✓ (완료)
├── Task 2.2: Logout 엔드포인트 ✓ (완료)
├── Task 2.3: Refresh 엔드포인트 ✓ (완료)
├── Task 3.1: Rate Limiting ✓ (완료)
└── Task 3.2: Password Hashing ✓ (완료)

→ 모든 Task가 완료됨!
→ 하나도 빠뜨리지 않음!
→ Task Breakdown이 이 누락을 방지!
```

```markdown
# ❌ 누락 발생

청사진 (Blueprint):
├── Task 1.1: JWT 토큰 생성 ✓
├── Task 1.2: JWT 토큰 검증 ✓
├── Task 2.1: Login 엔드포인트 ✓
├── Task 2.2: Logout 엔드포인트 ❌ (누락!)
├── Task 2.3: Refresh 엔드포인트 ✓
├── Task 3.1: Rate Limiting ❌ (누락!)
└── Task 3.2: Password Hashing ✓

→ Logout과 Rate Limiting이 누락됨!
→ 나중에 발견하면 큰 문제!
```

### Task 나누기 실전 가이드

> "이렇게 작업을 나누는 부분이 진짜 중요한 거에요." - Jason

#### 4가지 핵심 질문

**Q1: 200K 컨텍스트로 가능한가?**

```
인증 시스템 전체 = 청사진 5000줄
→ 200K 컨텍스트 초과!
→ 나눠야 함!

어떻게 나눌까?
→ Case 1: 모듈화 (JWT 모듈, Login 모듈, Logout 모듈)
→ Case 2: 단계별 (Login 완성 → Logout 완성 → Refresh 완성)

JWT 토큰 생성 함수 = 청사진 50줄
→ 200K 충분히 가능!
→ 한 Task로 OK!
```

**Q2: 이 Task만으로 의미있는 기능인가?**

```python
# ✅ 의미있는 Task
Task: JWT 토큰 생성 함수
- create_token(user_id) → JWT 반환
- 단독으로도 의미 있음 (토큰 만드는 기능)
- 완전히 작동
→ 레고블럭 ✓

# ✅ 의미있는 Task
Task: Login 엔드포인트
- POST /auth/login 작동
- 사용자 로그인 완전 구현
- Logout 없어도 의미 있음
→ 레고블럭 ✓

# ❌ 의미없는 Task
Task: JWT 토큰 생성 준비
- 변수 선언만
- 함수 뼈대만
- # TODO: 로직 구현
→ 의미 없음, 레고블럭 아님!
```

**Q3: 다른 Task와 일관성이 있나?**

```python
# ✅ 일관성 있음

# Task 1: Login
from core.logging import get_logger  # structlog
from core.types import LoginRequest   # Pydantic
logger = get_logger()

# Task 2: Logout (Task 1과 같은 패턴!)
from core.logging import get_logger  # ✅ 같은 structlog
from core.types import LogoutRequest  # ✅ 같은 Pydantic
logger = get_logger()

→ 일관성 유지! DNA 시스템이 강제!

# ❌ 일관성 없음

# Task 1: Login
import logging  # logging
logger = logging.getLogger()

# Task 2: Logout
from structlog import get_logger  # structlog
logger = get_logger()

→ 다른 로깅 사용! 일관성 깨짐!
```

**Q4: 청사진에서 누락된 Task는 없나?**

```markdown
# ✅ 누락 없음

청사진에 명시된 Task:
├── Task 1.1: JWT 생성 ✓
├── Task 1.2: JWT 검증 ✓
├── Task 2.1: Login ✓
├── Task 2.2: Logout ✓
└── Task 2.3: Refresh ✓

작업분해 문서:
├── Task 1.1 작업 지시서 ✓
├── Task 1.2 작업 지시서 ✓
├── Task 2.1 작업 지시서 ✓
├── Task 2.2 작업 지시서 ✓
└── Task 2.3 작업 지시서 ✓

→ 청사진의 모든 Task가 작업분해에 포함됨!

# ❌ 누락 발생

청사진에 명시된 Task:
├── Task 1.1: JWT 생성 ✓
├── Task 1.2: JWT 검증 ✓
├── Task 2.1: Login ✓
├── Task 2.2: Logout ✓
└── Task 2.3: Refresh ✓

작업분해 문서:
├── Task 1.1 작업 지시서 ✓
├── Task 2.1 작업 지시서 ✓
└── Task 2.3 작업 지시서 ✓

→ Task 1.2, 2.2가 누락됨!
→ 나중에 "어? JWT 검증이 없네?" 발견!
```

#### 실전 판단 예시

**예시 1: 인증 시스템을 어떻게 나눌까?**

```
상황:
- 청사진 5000줄
- 200K 컨텍스트 초과
- 재사용이 많음 (JWT를 여러 곳에서 사용)
- 팀 협업 필요

결정: Case 1 (모듈화 분할) 선택!

Task 분해:
├── Task 1: JWT 생성 모듈 (독립 블럭)
│   - 100줄, 재사용 가능
│   - A팀 담당
├── Task 2: JWT 검증 모듈 (독립 블럭)
│   - 80줄, 재사용 가능
│   - A팀 담당
├── Task 3: Login 엔드포인트 (조립 블럭)
│   - 150줄, Task 1, 2 사용
│   - B팀 담당
├── Task 4: Logout 엔드포인트 (조립 블럭)
│   - 120줄, Task 2 사용
│   - B팀 담당
└── Task 5: Refresh 엔드포인트 (조립 블럭)
    - 100줄, Task 1, 2 사용
    - B팀 담당

→ A팀과 B팀 병렬 작업 가능!
→ JWT 모듈은 다른 곳에서도 재사용!
```

**예시 2: 간단한 CRUD API를 어떻게 나눌까?**

```
상황:
- 청사진 800줄
- 200K 충분히 가능
- 재사용 적음
- 빠른 배포 필요

결정: Case 2 (단계별 구현) 선택!

Task 분해:
├── Task 1: Create 엔드포인트 (완전 구현)
│   - POST /items
│   - 200줄, 완전 작동
│   - 먼저 배포 가능!
├── Task 2: Read 엔드포인트 (완전 구현)
│   - GET /items, GET /items/{id}
│   - 150줄, Task 1과 일관성
│   - 다음 스프린트 배포
├── Task 3: Update 엔드포인트 (완전 구현)
│   - PUT /items/{id}
│   - 180줄, Task 1, 2와 일관성
└── Task 4: Delete 엔드포인트 (완전 구현)
    - DELETE /items/{id}
    - 120줄, Task 1, 2, 3과 일관성

→ 점진적 배포 가능!
→ 각 단계에서 패턴 확립!
```

#### 흔한 실수와 해결

**실수 1: Task가 너무 큼**

```python
# ❌ 나쁜 Task
Task: 전체 인증 시스템 구현
- JWT, Login, Logout, Refresh, Rate Limiting 전부
- 2000줄
- 200K 컨텍스트 초과
→ 너무 큼!

# ✅ 해결: 모듈화 또는 단계별로 나누기
Task 1: JWT 생성 모듈 (100줄)
Task 2: JWT 검증 모듈 (80줄)
Task 3: Login 엔드포인트 (150줄)
...
→ 적절한 크기!
```

**실수 2: Task가 너무 작음**

```python
# ❌ 나쁜 Task
Task 1: 변수 선언
Task 2: 함수 시그니처 정의
Task 3: 로직 구현
Task 4: 테스트 작성
→ 의미 없는 조각!

# ✅ 해결: 의미있는 단위로 묶기
Task: JWT 토큰 생성 함수 (완전 구현)
- 변수 선언 ✓
- 함수 구현 ✓
- 로직 완성 ✓
- 테스트 완료 ✓
→ 완성된 레고블럭!
```

**실수 3: 일관성 깨짐**

```python
# ❌ 나쁜 일관성
Task 1: Login (logging 사용)
Task 2: Logout (structlog 사용)
Task 3: Refresh (print 사용)
→ 세 가지 다른 로깅!

# ✅ 해결: DNA 시스템으로 강제
DNA 시스템에서 core/logging/ 구축
→ 모든 Task가 get_logger() 사용
→ pre-commit hook이 print() 차단
→ 일관성 강제!
```

**실수 4: 누락 발생**

```markdown
# ❌ 나쁜 작업분해
청사진: Task 1.1, 1.2, 2.1, 2.2, 2.3 (5개)
작업분해: Task 1.1, 2.1, 2.3 (3개만)
→ 1.2, 2.2 누락!

# ✅ 해결: 체크리스트 사용
청사진 Task 목록:
[ ] Task 1.1 → 작업분해 ✓
[ ] Task 1.2 → 작업분해 ✓
[ ] Task 2.1 → 작업분해 ✓
[ ] Task 2.2 → 작업분해 ✓
[ ] Task 2.3 → 작업분해 ✓
→ 모든 Task 작업분해 완료!
```

---

### 청사진 (Blueprint)의 역할

**Blueprint = 모든 레고블럭의 완전한 명세서**

#### 왜 초상세해야 하나?

```
청사진 목적:
1. 모든 레고블럭(Task) 명시 → 누락 방지
2. 각 블럭의 완성 기준 정의 → 일관성 보장
3. 블럭 간 관계 명확화 → 조립 가능
4. 미래 모든 시나리오 포함 → 완성된 그림
```

#### 청사진 예시: 인증 시스템 (5000줄 중 일부)

```markdown
# 인증 시스템 청사진

## 1. JWT 토큰 관리 모듈

### 1.1 토큰 생성 (Token Generation)

#### Task T1.1.1: JWT 토큰 생성 함수
**목적**: 사용자 ID로부터 JWT 액세스 토큰 생성
**구현**:
- 함수: create_access_token(user_id: int) -> str
- 페이로드: {user_id, exp, iat, jti}
- 알고리즘: HS256
- 만료: 1시간
- 비밀키: settings.JWT_SECRET_KEY
**표준 도구**: PyJWT 라이브러리
**테스트**: 3개 (성공, 만료, 잘못된 페이로드)
**라인**: 약 20줄

#### Task T1.1.2: JWT 리프레시 토큰 생성 함수
...

### 1.2 토큰 검증 (Token Validation)
...

## 2. 로그인/로그아웃 모듈

### 2.1 로그인

#### Task T2.1.1: POST /auth/login 엔드포인트
**목적**: 사용자 인증 후 JWT 토큰 발급
**구현**:
- 엔드포인트: POST /auth/login
- Request: LoginRequest(email: str, password: str)
- Response: LoginResponse(access_token, refresh_token, expires_in)
- 로직:
  1. 이메일로 사용자 조회 (UserRepository)
  2. 비밀번호 검증 (bcrypt)
  3. 실패 횟수 확인 (Redis: "login_fail:{email}")
  4. 5회 실패 시 → 30분 계정 잠금
  5. 성공 시 JWT 생성 (Task T1.1.1)
  6. Redis에 토큰 저장 (TTL 1시간)
  7. structlog 모든 시도 기록
**표준 도구**: FastAPI, Pydantic, bcrypt, Redis
**테스트**: 5개 (성공, 실패, 잠금, Redis 저장, 로깅)
**라인**: 약 50줄

#### Task T2.1.2: 로그인 실패 추적 로직
...

### 2.2 로그아웃
...
```

**핵심**:
- 모든 Task가 명시됨 (T1.1.1, T1.1.2, ..., T2.1.1, T2.1.2, ...)
- 각 Task의 완성 기준이 상세함
- 일관성 기준 (표준 도구, 구조)
- 5000줄 = 모든 레고블럭의 완전한 설명서

#### 청사진의 실무적 활용

**문제: 5000줄 청사진은 AI 에이전트가 한 번에 못 읽음**

**해결: Task Breakdown (작업분해) - 필수 단계!**

```markdown
Task T2.1.1 작업 지시서:

읽어야 할 Blueprint 라인:
- Blueprint Line 145-189 (POST /auth/login 상세)
- Blueprint Line 23-35 (JWT 생성 함수 참조)
- Blueprint Line 67-82 (Redis 저장 패턴)

→ 5000줄 중 필요한 62줄만 정확히 읽기!
→ AI 컨텍스트 200K 절약!
```

**작업분해가 필수인 이유:**
1. **압축**: 5000줄 → 100줄 (필요한 부분만)
2. **집중**: Transformer attention 보존
3. **정확성**: 정확한 라인 참조
4. **완성도**: 모든 Task 분해 → 누락 방지

---

## 3. DNA 시스템 철학

### DNA 시스템 없이 시작한 프로젝트의 교훈

**"알고 있어도 안 하면 붕괴한다"**

```python
DNA 시스템_없이_시작한_사례 = {
    "결과": "1,362개 아키텍처 위반으로 프로젝트 붕괴",
    "원인": "DNA 시스템 없이 바로 도메인 구현 시작",
    "교훈": "기초가 부실하면 나중에 고칠 수 없다"
}
```

### DNA 시스템의 본질

**DNA 시스템 = "환경 만들기" = "강제 시스템 준비"**

> "본격적인 작업(도메인 구현) 전에 일관성과 품질을 강제할 환경을 구축하는 단계"

### 왜 DNA 시스템이 필요한가?

#### ❌ DNA 시스템 없이 바로 작업 시작
```python
Task 1: 개발자 A
- print("User logged in")  # print() 사용

Task 2: 개발자 B
- logging.info("Order created")  # logging 사용

Task 3: 개발자 C
- logger.log({"event": "payment"})  # structlog 사용

→ 3가지 다른 로깅 방식 혼재!
→ 일관성 붕괴!
```

#### ✅ DNA 시스템 완료 후 작업 시작
```python
# DNA 시스템에서 core/logging/ 구축
# Pre-commit hook: print() 감지 시 차단

Task 1: 개발자 A
- from core.logging import get_logger
- logger = get_logger()
- logger.info("user_logged_in", user_id=123)  # ✅

Task 2: 개발자 B
- from core.logging import get_logger  # ✅ 같은 방식

Task 3: 개발자 C
- from core.logging import get_logger  # ✅ 같은 방식

→ 시스템이 일관성을 강제!
```

### DNA 시스템에서 준비하는 4가지

#### 1️⃣ DNA의 8개 시스템 (생물학적 은유)

```
🏗️ 골격계 (Architecture)
- Import Linter 설정
- Layer 구조 (domain/application/infrastructure)
- 의존성 방향 강제 (domain은 infrastructure 모름)

🧠 신경계 (Logging)
- structlog 설치 및 설정
- JSON 구조화 로깅
- 중앙 로거 (get_logger 패턴)

🛡️ 면역계 (Testing)
- pytest 설치 및 설정
- Given-When-Then 템플릿
- 첫 테스트 작성 및 통과

🩸 순환계 (API)
- FastAPI 설치 및 설정
- Pydantic 모델 정의
- 첫 엔드포인트 작동 (GET /health)

🔔 내분비계 (Configuration)
- pydantic-settings 설정
- .env.example 생성
- 환경별 설정 분리

🍽️ 소화계 (Data Processing)
- polars 설치 (pandas 금지)
- 데이터 처리 패턴

🚽 배설계 (Cleanup)
- 로그 관리 정책
- 캐시 정리 전략

🫁 호흡계 (External Integration)
- HTTP 클라이언트 설정
- 외부 API 연동 패턴
```

#### 2️⃣ Layer 구조 (아키텍처 골격)

```
src/
├── domain/           # 비즈니스 로직 (순수, 의존성 없음)
│   ├── entities/
│   ├── value_objects/
│   └── interfaces/
├── application/      # 유스케이스 (domain 사용)
│   ├── services/
│   └── dtos/
└── infrastructure/   # 기술 구현 (application 구현)
    ├── api/
    ├── database/
    └── external/

# Import Linter로 강제:
# domain → application ❌
# domain → infrastructure ❌
# application → infrastructure ✅
```

#### 3️⃣ 표준 도구 스택 (도구 선택 및 설정)

**원칙: "선택하고 설정" (만들지 않음!)**

| 시스템 | 표준 도구 | 금지 사항 | 설정 위치 |
|--------|----------|----------|----------|
| 타입/검증 | Pydantic v2 | 커스텀 검증 시스템 | core/types/ |
| 로깅 | structlog | print(), 커스텀 로거 | core/logging/ |
| 테스트 | pytest | unittest, 수동 mocking | tests/ |
| 설정 | pydantic-settings | 수동 환경변수 파싱 | core/config/ |
| API | FastAPI | 수동 타입 검증 | infrastructure/api/ |
| 데이터 | polars | pandas + 수동 검증 | - |

#### 4️⃣ 프로젝트별 표준 모듈 (7가지 공통 컴포넌트)

```
core/
├── logging/          # 중앙 로깅 시스템
│   ├── __init__.py   # get_logger() 제공
│   ├── formatters.py # JSON 포맷터
│   └── handlers.py   # 로그 핸들러
├── types/            # Pydantic 모델들
│   ├── requests.py   # API Request 모델
│   ├── responses.py  # API Response 모델
│   └── entities.py   # 도메인 엔티티
├── errors/           # 표준 예외 클래스
│   ├── base.py       # BaseError
│   ├── http.py       # HTTPError
│   └── domain.py     # DomainError
├── api/              # API 기본 구조
│   ├── router.py     # 라우터 설정
│   ├── middleware.py # 미들웨어
│   └── responses.py  # 표준 응답 포맷
├── config/           # 설정 관리
│   ├── settings.py   # pydantic-settings
│   └── environments/ # 환경별 설정
├── db/               # 데이터베이스
│   ├── models.py     # DB 모델
│   ├── session.py    # DB 세션
│   └── repositories/ # Repository 패턴
└── security/         # 보안
    ├── auth.py       # 인증
    ├── crypto.py     # 암호화
    └── validators.py # 검증
```

### DNA 시스템 실행 순서

```yaml
1단계: 땅 고르기 (Architecture Foundation)
  - src/ 디렉토리 구조 생성
  - Import Linter 설정 (.importlinter)
  - pyproject.toml 의존성 방향 규칙

2단계: 기반 시설 설치 (Standard Tools)
  - uv add pydantic pydantic-settings
  - uv add structlog
  - uv add pytest pytest-cov
  - uv add fastapi uvicorn
  - uv add polars

3단계: 표준 모듈 구축 (Common Modules)
  - core/logging/ 구현 (get_logger)
  - core/types/ 기본 모델
  - core/errors/ 예외 클래스
  - core/config/ 설정 관리
  - core/api/ 라우터 기본 구조

4단계: 연결과 통합 (Integration)
  - 도구 간 설정 연동
  - .env.example 생성
  - 첫 Hello World 작동 (GET /health)

5단계: 품질 검증 (DNA 시스템 Gate)
  - MyPy 0 오류 확인
  - pytest 첫 테스트 통과
  - Import Linter 0 violations
  - ruff check 0 violations
```

### DNA 시스템 성공 vs 실패

#### ❌ 실패: 직접 만들기
```python
Day 1: "타입 시스템부터 직접 만들자"
Day 2-14: 89개 타입 클래스 생성 (1,679줄)
Day 15: MyPy 312개 오류 발견
Day 16: 개발 중단

→ 공장 기계를 직접 만들려다 실패
```

#### ✅ 성공: 표준 도구 사용
```python
Day 1 09:00: 표준 도구 설치 (1시간)
Day 1 10:00: core/ 모듈 구축 (2시간)
Day 1 12:00: 첫 API 엔드포인트 작동!
Day 1 14:00: DNA 시스템 Gate 통과!
Day 1 15:00: Domain별 구현 시작

→ 검증된 기계를 설치하고 바로 생산 시작
```

### 공장 건설의 비유

> "10만평 공장을 지을 건데, 1평짜리 콘크리트 방에서 공장 구현하라고 하면 가능한가?"

```
DNA 시스템 = 땅 고르기 + 기계 설치 + 전력 연결 + 첫 가동

1. 땅 고르기: Layer 구조, Import Linter
2. 기계 설치: Pydantic, structlog, pytest, FastAPI
3. 전력 연결: core/ 모듈, 설정 통합
4. 첫 가동: GET /health 작동, DNA 시스템 Gate 통과

제품 생산(도메인 구현)은 그 다음!
```

### DNA 시스템 vs 청사진

| | DNA 시스템 (Stage 2-3) | 청사진 (Stage 4) |
|---|---|---|
| 목적 | **환경 구축** (일관성 강제 준비) | **완성 그림** (모든 레고블럭 명세) |
| 범위 | 공통 인프라 (모든 Task 공유) | 도메인 로직 (프로젝트 고유) |
| 시점 | **Blueprint 작성 전** (필수 선행!) | **DNA 시스템 구현 완료 후** |
| 작성 | Stage 2: 계획 문서 → Stage 3: 구현 | DNA 시스템 환경 기반으로 작성 |
| 내용 | 도구, 구조, 표준 모듈 | 비즈니스 로직, API, 시나리오 |
| 예시 | "core/logging 구현" | "`from core.logging import get_logger` 사용" |
| 완성 기준 | DNA 시스템 Gate 통과 | 모든 레고블럭 명세 완료 |

**핵심 차이**:
- **DNA 시스템**: "어떻게 만들 것인가" (How) - 도구와 방법
- **청사진**: "무엇을 만들 것인가" (What) - 기능과 로직

**중요: 왜 DNA 시스템이 먼저 구현되어야 하나?**

```markdown
# ❌ DNA 시스템 구현 전에 청사진 작성
Task T2.1.1: Login 엔드포인트
- 로깅은... 뭘 쓰지? (아직 모름)
- 타입은... 뭘 쓰지? (아직 모름)
→ 추상적인 청사진!

# ✅ DNA 시스템 구현 후에 청사진 작성
Task T2.1.1: Login 엔드포인트
- `from core.logging import get_logger` ← 구체적!
- `from core.types import LoginRequest` ← 구체적!
- `logger.info("login_attempt", email=request.email)` ← 예시 코드!
→ 구체적인 청사진!
```

**DNA 시스템 = 공장, Blueprint = 제품 설계도**
- 공장이 먼저 있어야 제품 설계도를 구체적으로 그릴 수 있어요!

---

## 4. 8-Stage 진화 구조

### 전체 흐름

```
[Human-Driven: 결정과 설계가 필요한 단계]

Stage 1: 프로젝트 계획
  - 무엇을 만들 것인가?
  - 아키텍처 결정 (ADR)
  - 표준 도구 선택 결정
  → Jason + 1호/2호 대화

Stage 2: DNA 시스템 계획 문서
  - DNA 8개 시스템 설계
  - Layer 구조 정의
  - 표준 도구 스택 결정
  - core/ 표준 모듈 설계
  - DNA 시스템 Gate 기준 정의
  → "어떤 환경을 구축할지" 문서화

Stage 3: DNA 시스템 구현 ⭐ (핵심!)
  - DNA 8개 시스템 구축
  - Layer 구조 설정
  - 표준 도구 설치 및 설정
  - core/ 표준 모듈 구현
  - DNA 시스템 Gate 통과 (필수!)
  → "강제할 환경" 구현 완료!
  → 이제 core/ 모듈 다 있음!

Stage 4: 도메인별 청사진 (완성 그림)
  ⚠️ DNA 시스템 구현 (Stage 3) 완료 후에만 가능!
  - DNA 시스템 환경 기반으로 작성
  - 모든 레고블럭(Task) 명세
  - 구체적인 예시 코드 포함
    예: `from core.logging import get_logger`
  - 각 블럭의 완성 기준 정의
  - 5000줄+ 초상세 계획
  → DNA 시스템 환경에서 구체적으로 작성 가능!

──────────────────────────────────────
⬇️ SPARK 시작 가능 지점 ⬇️
──────────────────────────────────────

[SPARK-Enabled: 체계적 강제화가 가능한 단계]

Stage 5: 작업분해 (Task Breakdown)
  - 청사진 → Task 단위 분해
  - 각 Task마다 필요한 Blueprint 라인 지정
  - 필요한 Standards 섹션 지정
  - 5000줄 → 100줄로 압축
  → SPARK가 자동화 가능

Stage 6: 체크리스트 작성 (Checklist)
  - Task별 9-Step 체크리스트
  - 읽어야 할 문서 라인 명시
  - 완성 기준 체크리스트
  - 품질 기준 명시
  → SPARK가 자동화 가능

Stage 7: 도메인 구현 (Domain Implementation)
  - 체크리스트 기반 실행
  - DNA 시스템 환경이 일관성 강제
  - Quality Gates 검증
  - 레고블럭 조립
  → SPARK 에이전트 실행, 시스템 강제

Stage 8: 시스템 최적화 (Optimization)
  - 성능 개선
  - 품질 개선
  - 기술 부채 정리
  → SPARK 에이전트 실행
```

### Stage별 상세 설명

#### Stage 1: 프로젝트 계획 (Project Planning)
**Who**: Jason + 1호/2호 대화
**Output**:
- ADR (Architecture Decision Records)
- 프로젝트 목표 및 범위
- 표준 도구 선택 결정 (FastAPI? Flask? / Pydantic? dataclass?)

#### Stage 2: DNA 시스템 계획 문서 (DNA 시스템 Planning)
**Who**: Jason + 1호/2호 대화
**What**: 어떤 환경을 구축할지 문서화
**Output**:
- DNA 8개 시스템 설계
- Layer 구조 정의 (domain/application/infrastructure)
- 표준 도구 스택 결정 (Pydantic, structlog, pytest, FastAPI)
- core/ 표준 모듈 설계
  - core/logging: 어떤 구조?
  - core/types: 어떤 Base 모델?
  - core/errors: 어떤 예외들?
- DNA 시스템 Gate 기준 정의

**예시 문서**:
```markdown
# DNA 시스템 계획

## core/logging
- get_logger() 함수 제공
- JSON 구조화 로깅
- structlog 사용

## core/types
- BaseModel: Pydantic v2 기반
- 모든 Request/Response 모델의 부모 클래스

## core/errors
- BaseError
- HTTPError (4xx, 5xx)
- DomainError (비즈니스 로직 에러)
```

#### Stage 3: DNA 시스템 구현 ⭐ (DNA 시스템 Implementation)
**Who**: Jason + 1호/2호 대화 또는 SPARK designer-spark
**What**: 일관성 강제 환경 실제 구축
**Why 중요**: Blueprint 작성 전에 필수!

**실제 구현**:

```python
# Day 1 09:00-10:00: 표준 도구 설치
uv add pydantic pydantic-settings
uv add structlog
uv add pytest pytest-cov
uv add fastapi uvicorn

# Day 1 10:00-12:00: core/ 모듈 구현
# core/logging/__init__.py
import structlog

def get_logger():
    return structlog.get_logger()

# core/types/__init__.py
from pydantic import BaseModel
class BaseRequest(BaseModel): pass
class BaseResponse(BaseModel): pass

# core/errors/__init__.py
class BaseError(Exception): pass
class HTTPError(BaseError): pass

# Day 1 12:00: 첫 API 엔드포인트 작동!
@app.get("/health")
def health():
    return {"status": "ok"}

# Day 1 14:00: DNA 시스템 Gate 통과!
```

**DNA 시스템 Gate**:
```bash
✓ Import Linter 0 violations
✓ 중앙 로거 작동 (get_logger)
✓ pytest 첫 테스트 통과
✓ 첫 API 엔드포인트 작동 (GET /health)
✓ MyPy 0 오류
✓ ruff check 0 violations
```

**결과**: 이제 core/ 모듈 다 있음! → Blueprint 구체적으로 쓸 수 있음!

#### Stage 4: 도메인별 청사진 (Blueprint)
**Who**: Jason + 1호/2호 대화
**When**: ⚠️ DNA 시스템 구현 (Stage 3) 완료 후!
**What**: DNA 시스템 환경 기반으로 모든 레고블럭 명세
**Why Stage 3 후**: core/ 모듈이 있어야 구체적 예시 작성 가능

**Output**:
- 5000줄+ 초상세 청사진
- 모든 Task 명시 (T1.1.1, T1.1.2, ...)
- **구체적인 예시 코드** 포함
- 각 Task의 완성 기준
- 일관성 기준 (표준 도구, 패턴)

**예시**: 인증 시스템 청사진

```markdown
# 인증 시스템 청사진 (5000줄)

## Task T2.1.1: POST /auth/login 엔드포인트

### 구현 명세
```python
# ✅ DNA 시스템 구현 완료했으니 구체적으로 쓸 수 있어요!
from core.logging import get_logger  # ← 이미 있음!
from core.types import BaseRequest, BaseResponse  # ← 이미 있음!
from core.errors import InvalidCredentialsError  # ← 이미 있음!

logger = get_logger()

class LoginRequest(BaseRequest):
    email: str
    password: str

class LoginResponse(BaseResponse):
    access_token: str
    token_type: str = "bearer"

@app.post("/auth/login")
def login(request: LoginRequest) -> LoginResponse:
    logger.info("login_attempt", email=request.email)
    # ... 구체적인 로직
```

### 테스트
```python
# ✅ pytest도 DNA 시스템에서 설정했으니 구체적으로 쓸 수 있어요!
def test_login_success():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
```
```

**핵심**: DNA 시스템 없었으면 이렇게 구체적으로 못 써요!

#### Stage 5: 작업분해 (Task Breakdown)
**Who**: SPARK 자동화 가능
**What**: 청사진을 Task 단위로 분해
**Why 필수**: 5000줄 청사진을 100줄 작업 지시서로 압축

**작업분해 문서의 구조**:

```markdown
# Task T1.1.1: JWT 토큰 생성 모듈

## 📘 청사진 참조 (Blueprint References)
- **Blueprint Line 145-178**: JWT 알고리즘 명세
  - HS256 알고리즘 사용
  - Payload 구조: {user_id, exp, iat, jti}
  - Secret Key: 환경 변수에서 로드
- **Blueprint Line 179-195**: Payload 구조 상세
- **Blueprint Line 196-210**: 에러 처리 시나리오
  - InvalidUserError: 사용자 ID 없음
  - TokenGenerationError: 생성 실패

→ 총 66줄만 읽으면 됨! (청사진 5000줄 중)

## 📋 프로젝트 표준 참조 (Standards References)
- **PROJECT_STANDARDS.md Line 12-25**: structlog 로깅 패턴
  ```python
  from core.logging import get_logger
  logger = get_logger()
  logger.info("event_name", key=value)
```
- **PROJECT_STANDARDS.md Line 56-71**: Pydantic 검증 패턴
  ```python
  from core.types import BaseModel
  class TokenPayload(BaseModel):
      user_id: str
      exp: datetime
  ```
- **ARCHITECTURE.md Line 23-45**: core/ 모듈 사용 규칙

→ 총 40줄만 읽으면 됨! (표준 문서 중)

## 🔧 사용 도구 (Tools)
- **PyJWT**: 표준 JWT 라이브러리 (직접 구현 금지!)
- **Pydantic**: TokenPayload 모델 정의
- **structlog**: 토큰 생성 로깅
- **pytest**: 단독 테스트 작성

## 📦 입력/출력 (Interface)
**입력**:
- user_id: str (사용자 고유 ID)

**출력**:
- token: str (JWT 토큰 문자열)

**의존성**:
- settings.JWT_SECRET_KEY (환경 설정)
- 부작용: 없음 (순수 함수)

## 🔗 조립 정보 (Assembly)
**이 블럭을 사용하는 Task**:
- Task T2.1.1: Login 엔드포인트
- Task T2.3.1: Refresh 엔드포인트
- Task T4.1.1: API Key 생성

**이 블럭이 사용하는 Task**:
- 없음 (독립 블럭)

## 🎯 완성 기준 (Completion Criteria)
- [ ] create_token(user_id) 함수 완전 작동
- [ ] 올바른 JWT 생성 확인 (HS256, 페이로드 정확)
- [ ] 만료 시간 정확히 설정 (1시간)
- [ ] InvalidUserError 에러 처리
- [ ] TokenGenerationError 에러 처리
- [ ] structlog 로깅 (token_created 이벤트)
- [ ] pytest 테스트 3개 통과:
  - 성공: 유효한 user_id → JWT 반환
  - 실패: 빈 user_id → InvalidUserError
  - 검증: JWT decode로 페이로드 확인
- [ ] ruff check 0 violations
- [ ] mypy 0 errors
- [ ] 단독 실행 가능 (다른 Task 없이)

## 💡 구현 힌트 (Implementation Hints)
```python
# ✅ 올바른 구현 패턴
from datetime import datetime, timedelta
import jwt
from core.logging import get_logger
from core.config import settings
from core.errors import InvalidUserError, TokenGenerationError

logger = get_logger()

def create_token(user_id: str) -> str:
    if not user_id:
        raise InvalidUserError("user_id is required")

    try:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
            "jti": str(uuid.uuid4())
        }
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
        logger.info("token_created", user_id=user_id, expires_in=3600)
        return token
    except Exception as e:
        logger.error("token_generation_failed", user_id=user_id, error=str(e))
        raise TokenGenerationError(f"Failed to create token: {e}")
```

## ⏱️ 예상 작업 시간
- 구현: 30분
- 테스트: 20분
- 품질 검증: 10분
- **총 예상**: 1시간

---

# Task T2.1.1: POST /auth/login 엔드포인트

## 📘 청사진 참조 (Blueprint References)
- **Blueprint Line 345-412**: Login API 명세
- **Blueprint Line 413-448**: 성공/실패 시나리오
- **Blueprint Line 23-35**: JWT 생성 함수 참조 (Task T1.1.1)
- **Blueprint Line 67-82**: Redis 저장 패턴

→ 총 98줄만 읽으면 됨!

## 📋 프로젝트 표준 참조
- **PROJECT_STANDARDS.md Line 45-78**: API 엔드포인트 표준
- **PROJECT_STANDARDS.md Line 92-115**: 에러 처리 표준
- **PROJECT_STANDARDS.md Line 156-178**: Redis 사용 패턴

## 🔧 사용 도구
- **FastAPI**: API 엔드포인트
- **Pydantic**: LoginRequest, LoginResponse 모델
- **bcrypt**: 비밀번호 검증
- **Redis**: 실패 횟수 추적, 토큰 저장
- **structlog**: 모든 시도 로깅

## 📦 입력/출력
**입력**:
- LoginRequest(email: str, password: str)

**출력**:
- LoginResponse(access_token: str, refresh_token: str, expires_in: int)

**의존성**:
- Task T1.1.1: create_token() 함수 사용
- Task T3.2.1: verify_password() 함수 사용
- Redis: 실패 횟수, 토큰 저장
- DB: 사용자 조회

## 🔗 조립 정보
**이 블럭을 사용하는 Task**:
- 없음 (최종 엔드포인트)

**이 블럭이 사용하는 Task**:
- Task T1.1.1: JWT 토큰 생성
- Task T3.2.1: 비밀번호 검증

**조립 순서**:
1. Task T1.1.1 완료 (JWT 생성) ✓
2. Task T3.2.1 완료 (비밀번호 검증) ✓
3. Task T2.1.1 시작 (이 Task)

## 🎯 완성 기준
- [ ] POST /auth/login 엔드포인트 작동
- [ ] LoginRequest, LoginResponse Pydantic 모델
- [ ] 사용자 조회 (DB)
- [ ] 비밀번호 검증 (Task T3.2.1 사용)
- [ ] JWT 토큰 생성 (Task T1.1.1 사용)
- [ ] 실패 횟수 추적 (Redis)
- [ ] 5회 실패 → 30분 계정 잠금
- [ ] Redis 토큰 저장 (TTL 1시간)
- [ ] structlog 모든 시도 로깅
- [ ] pytest 테스트 5개 통과:
  - 성공: 유효한 credential → 200 + 토큰
  - 실패: 잘못된 password → 401
  - 실패: 존재하지 않는 email → 401
  - 잠금: 5회 실패 → 429
  - 검증: Redis 저장 확인
- [ ] ruff check 0 violations
- [ ] mypy 0 errors

## 💡 구현 힌트
```python
@app.post("/auth/login")
def login(request: LoginRequest) -> LoginResponse:
    # 1. 실패 횟수 체크
    fail_count = redis.get(f"login_fail:{request.email}")
    if fail_count and int(fail_count) >= 5:
        raise AccountLockedError("Account locked for 30 minutes")

    # 2. 사용자 조회
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # 실패 횟수 증가
        redis.incr(f"login_fail:{request.email}")
        redis.expire(f"login_fail:{request.email}", 1800)
        logger.warning("login_failed", email=request.email, reason="user_not_found")
        raise InvalidCredentialsError()

    # 3. 비밀번호 검증 (Task T3.2.1 사용)
    if not verify_password(request.password, user.hashed_password):
        # 실패 횟수 증가
        redis.incr(f"login_fail:{request.email}")
        logger.warning("login_failed", email=request.email, reason="invalid_password")
        raise InvalidCredentialsError()

    # 4. JWT 생성 (Task T1.1.1 사용)
    access_token = create_token(user.id)

    # 5. Redis 저장
    redis.setex(f"token:{user.id}", 3600, access_token)

    # 6. 실패 횟수 초기화
    redis.delete(f"login_fail:{request.email}")

    # 7. 로깅
    logger.info("login_success", user_id=user.id, email=user.email)

    return LoginResponse(access_token=access_token, token_type="bearer", expires_in=3600)
```

## ⏱️ 예상 작업 시간
- 구현: 1시간
- 테스트: 40분
- 품질 검증: 20분
- **총 예상**: 2시간
```

**작업분해가 필수인 이유**:

1. **압축**: 청사진 5000줄 → Task별 100줄
2. **정확성**: Line 145-178처럼 정확한 참조
3. **집중**: 이 Task에만 필요한 정보만
4. **조립**: 의존성과 조립 순서 명확
5. **완성도**: 구체적인 완성 기준
6. **효율**: 예상 시간으로 계획 가능

#### Stage 6: 체크리스트 작성 (Checklist)
**Who**: SPARK 자동화 가능
**What**: Task별 실행 체크리스트
**Output**:
- 9-Step 체크리스트
- 각 단계별 완성 기준
- 품질 기준 명시

**9-Step 체크리스트 상세 구조**:

```python
nine_step_checklist = {
    "1_목표_이해": {
        "질문": "이 Task로 무엇을 만들 것인가?",
        "산출물": "Task 목표 명확화 + 성공 기준 정의",
        "예시": "Task-Immune-01: PCI DSS 규정을 만족하는 결제 처리 보안 구현"
    },

    "2_테스트_작성": {
        "질문": "어떻게 동작을 검증할 것인가?",
        "산출물": "Given-When-Then 테스트 케이스",
        "예시": """
        def test_secure_payment_processing():
            # Given: 신용카드 정보가 주어졌을 때
            card_data = CardData(number="4111-1111-1111-1111")

            # When: 보안 결제 처리를 실행하면
            result = secure_payment_service.process(card_data)

            # Then: PCI DSS 규정을 만족하며 처리된다
            assert result.is_pci_compliant == True
            assert result.card_data_is_encrypted == True
        """
    },

    "3_구현": {
        "질문": "테스트를 통과하는 최소한의 코드는?",
        "산출물": "동작하는 구현 코드",
        "원칙": "테스트 먼저, 구현은 최소한으로"
    },

    "4_검증": {
        "질문": "코드 품질이 기준을 만족하는가?",
        "산출물": "Code Laundry 패턴 적용 완료",
        "도구": "mypy, black, isort, import-linter"
    },

    "5_테스트_실행": {
        "질문": "모든 테스트가 통과하는가?",
        "산출물": "pytest 실행 결과 all pass",
        "기준": "신규 테스트 + 기존 테스트 모두 통과"
    },

    "6_리팩토링": {
        "질문": "코드를 더 깔끔하게 만들 수 있는가?",
        "산출물": "개선된 코드 구조",
        "원칙": "기능 변경 없이 구조 개선"
    },

    "7_재테스트": {
        "질문": "리팩토링 후에도 모든 것이 동작하는가?",
        "산출물": "95%+ 커버리지 달성",
        "기준": "pytest --cov=. tests/ 통과"
    },

    "8_문서화": {
        "질문": "다른 사람이 이 코드를 이해할 수 있는가?",
        "산출물": "코드 문서 + API 문서",
        "원칙": "코드는 스스로 설명되어야 함"
    },

    "9_커밋": {
        "질문": "이 변경사항을 영구 보존할 준비가 되었는가?",
        "산출물": "Git commit with proper message",
        "절대금지": "--no-verify 사용 금지"
    }
}
```

**간단한 예시**:
```markdown
Task T2.1.1 체크리스트:

[ ] Step 1: 목표 이해
    - Blueprint Line 145-189 읽기 완료
    - Standards 읽기 완료
    - Task 목표: POST /auth/login 엔드포인트 구현

[ ] Step 2: 테스트 작성
    - Given-When-Then 패턴 적용
    - 성공 케이스: 200 + JWT 토큰
    - 실패 케이스: 401
    - 잠금 케이스: 429

[ ] Step 3: 구현
    - LoginRequest, LoginResponse Pydantic 모델
    - 비밀번호 검증 로직
    - Redis 실패 횟수 추적

[ ] Step 4: 검증
    - mypy 0 errors
    - ruff check 0 violations
    - import-linter 0 violations

[ ] Step 5: 테스트 실행
    - pytest 5개 모두 통과
    - Redis 저장 확인
    - structlog 확인

[ ] Step 6: 리팩토링
    - 중복 코드 제거
    - 함수 분리 (단일 책임)

[ ] Step 7: 재테스트
    - pytest --cov=. tests/ 통과
    - coverage ≥ 95%

[ ] Step 8: 문서화
    - Docstring 작성
    - API 문서 업데이트

[ ] Step 9: 커밋
    - git add, git commit (--no-verify 금지!)
    - 커밋 메시지 작성
```

#### Stage 7: 도메인 구현 (Domain Implementation)
**Who**: SPARK 에이전트 (implementer-spark, tester-spark)
**What**: 체크리스트 기반 구현, 시스템 강제
**How**:
- DNA 시스템 환경이 일관성 강제
- Pre-commit hook이 위반 차단
- Quality Gates가 품질 검증
- 레고블럭 완성 및 조립

**강제 시스템 작동**:
```python
# Layer 3: 실시간 검증
if "print(" in code:
    BLOCK "❌ print() 금지. structlog 사용"

if domain_imports_infrastructure:
    BLOCK "❌ 의존성 방향 위반"

# Layer 4: 완료 검증
if violations_total != 0:
    BLOCK "❌ Quality Gates 미통과"
```

#### Stage 8: 시스템 최적화 (Optimization)
**Who**: SPARK 에이전트 (improver-spark, qc-spark)
**What**: 성능 및 품질 개선
**Output**:
- 성능 병목 해결
- 코드 품질 개선
- 기술 부채 정리
- 아키텍처 개선

### SPARK의 역할 명확화

```
Stage 1-4: Jason + 1호/2호 대화
- Stage 1: 프로젝트 계획 (ADR, 도구 선택)
- Stage 2: DNA 시스템 계획 (환경 설계)
- Stage 3: DNA 시스템 구현 (환경 구축) ⭐
- Stage 4: Blueprint 작성 (도메인 설계)
→ 결정, 맥락, 전체 그림 필요
→ SPARK 역할 없음 (인간 판단 영역)

Stage 5-8: SPARK 자동화 + 강제화
- Stage 5: 작업분해 (Blueprint → Task)
- Stage 6: 체크리스트 (Task → 9-Step)
- Stage 7: 도메인 구현 (Checklist → Code)
- Stage 8: 최적화 (Quality → Better)
→ SPARK 핵심 역할 (시스템 강제 영역)
```

---

## 5. AI 협업의 핵심 교훈

### AI 협업 실패 사례

```
초기: Blueprint 381줄 + 체크리스트 600줄 ✓
구현: TODO 남발, --no-verify 우회
결과: 1,362개 아키텍처 위반 → 프로젝트 붕괴
```

**원인**: "알고 있다 ≠ 하고 있다"

### 해결책: 3가지 균형

#### 1️⃣ 매우 구체화된 계획 (Blueprint)
```
❌ "사용자 인증 만들어"
✅ "JWT 기반 /auth/login 엔드포인트
    - Request: {email, password}
    - 5회 실패 → 30분 잠금
    - Redis TTL 1시간
    - structlog 모든 시도 기록"
```

#### 2️⃣ 정확하고 상세한 지시 (Checklist)
```
❌ "테스트 작성해"
✅ "체크리스트:
    [ ] 성공: 올바른 credential → 200
    [ ] 실패: 잘못된 password → 401
    [ ] 엣지: 5회 실패 → 429
    [ ] Redis 저장 확인
    [ ] 로깅 확인"
```

#### 3️⃣ 한 번에 다 주면 안 됨 (Lego Block)
```
❌ 5000줄 Blueprint 전체 덤프
✅ "Task T3.2만:
    - Blueprint Line 62-94만
    - Standards Line 12-25, 45-58만
    - 이 Task에 필요한 것만"
```

### 적절한 자율성의 균형

**❌ 너무 옭아매면**:
```python
# Line 1: 정확히 이 코드
import logging
# Line 2: 클래스명은 반드시 UserService
```
→ 창의성 제로

**❌ 너무 풀어주면**:
```python
"사용자 서비스 구현하세요"
def user_service():
    # TODO: 구현 필요
```
→ TODO 남발

**✅ 균형**:
```python
# WHY: V3처럼 에러 못 찾는 일 방지
# 기준: JSON 형식, trace_id 필수, structlog 사용
# 자유: 구체적 구현 방식 선택
```
→ WHY 이해 + 기준 준수 + 창의적 구현

---

## 6. DNA 시스템 Gate (통과 필수!)

### 철학
> "살아있지 않으면 진화할 수 없다"

### 필수 체크포인트

#### 🏗️ 골격계
```yaml
✓ Import Linter 0 violations
✓ 레이어 구조 확립 (domain/application/infrastructure)
✓ 순환 참조 방지 규칙
```

#### 🧠 신경계
```yaml
✓ 중앙 로거 (get_logger 패턴)
✓ JSON 구조화 로깅
✓ structlog 설정 완료
```

#### 🛡️ 면역계
```yaml
✓ pytest 설정
✓ Given-When-Then 템플릿
✓ 첫 테스트 통과
```

#### 🩸 순환계
```yaml
✓ 첫 API 엔드포인트 작동
✓ Pydantic 모델 정의
✓ 기본 에러 응답 구조
```

#### 🔔 내분비계
```yaml
✓ pydantic-settings 설정
✓ .env.example 존재
✓ 설정 검증 로직
```

### DNA 시스템 Gate 자동 검증

```bash
#!/bin/bash
# DNA 시스템-gate.sh

# Import Linter 체크
if [ $(import-linter | grep "violations: 0" | wc -l) -eq 0 ]; then
    echo "❌ Import Linter 위반"
    exit 1
fi

# 중앙 로거 체크
if ! grep -r "get_logger" src/ > /dev/null; then
    echo "❌ 중앙 로거 미사용"
    exit 1
fi

# MyPy 체크
if ! mypy . --strict; then
    echo "❌ Type errors exist"
    exit 1
fi

echo "✅ DNA 시스템 Gate 통과!"
```

**원칙**: 통과할 때까지 Stage 4 (청사진 작성) 진행 불가

### 구체적인 설정 파일 예시

#### 골격계: Import Linter 설정

```toml
# .import-linter.toml
[tool.importlinter]
root_package = "src"

[[tool.importlinter.contracts]]
name = "Domain layer cannot import from outer layers"
type = "forbidden"
source_modules = ["src.domain"]
forbidden_modules = ["src.infrastructure", "src.interfaces"]

[[tool.importlinter.contracts]]
name = "Application layer can only import from domain"
type = "layers"
layers = [
    "src.interfaces",
    "src.application",
    "src.domain"
]

[[tool.importlinter.contracts]]
name = "No circular dependencies"
type = "independence"
modules = [
    "src.domain",
    "src.application",
    "src.infrastructure"
]
```

#### 신경계: Logging 설정

```python
# src/core/logging/config.py
import structlog

def configure_logging():
    """중앙 로깅 설정"""
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

def get_logger(name: str):
    """표준 로거 획득 패턴"""
    return structlog.get_logger(name)
```

#### 면역계: Pytest 설정

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Coverage 설정
addopts =
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=95
    --strict-markers
    -v

# 마커 정의
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
```

#### 내분비계: Settings 설정

```python
# src/core/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """환경 설정 (pydantic-settings)"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # 앱 기본 설정
    app_name: str = "MyApp"
    debug: bool = False

    # 로깅 설정
    log_level: str = "INFO"

    # DB 설정 (예시)
    database_url: str = "sqlite:///./app.db"

    @property
    def is_development(self) -> bool:
        return self.debug

settings = Settings()
```

```bash
# .env.example
# 앱 설정
APP_NAME=MyApp
DEBUG=false

# 로깅
LOG_LEVEL=INFO

# 데이터베이스
DATABASE_URL=sqlite:///./app.db
```

---

## 7. 시스템 강제화 (가장 중요!)

### 지침 vs 시스템

**지침 (❌ 약함)**:
```markdown
"Blueprint를 읽으세요"
"표준 도구를 쓰세요"
"print()를 쓰지 마세요"
```
→ AI가 무시하거나 잊음

**시스템 (✅ 강함)**:
```python
# Pre-commit hook
if "print(" in code:
    BLOCK "❌ print() 금지. structlog 사용하세요."

# Import Linter
if domain_imports_infrastructure:
    BLOCK "❌ 의존성 방향 위반"

# DNA 시스템 Gate
if not exists("BLUEPRINT.md"):
    STOP "❌ Blueprint 없음"

# Quality Gates
if mypy_errors > 0:
    BLOCK "❌ Type errors must be 0"
```

### 4-Layer 강제 시스템

```
Layer 1: 환경 강제 (작업 전)
├─ Blueprint 존재 확인
├─ 표준 문서 존재 확인
├─ 표준 도구 설치 확인
└─ DNA 시스템 Gate 통과 확인
→ BLOCKING validation

Layer 2: 단위 작업 집중 (작업 중)
├─ 지정된 Blueprint 라인만 읽기
├─ 지정된 Standards 섹션만 읽기
├─ 선언된 도구만 사용
└─ Task 체크리스트만 따르기
→ 정보 최소화

Layer 3: 실시간 검증 (작업 중)
├─ 파일 저장 시 즉시 ruff/mypy
├─ print() 감지 → 즉시 차단
├─ 타입 힌트 누락 → 즉시 차단
└─ 비표준 모듈 → 즉시 차단
→ 실시간 차단

Layer 4: 완료 검증 (작업 후)
├─ Quality Gates (Phase 5A/5B)
├─ Pre-commit hooks
├─ All violations = 0
└─ No --no-verify
→ 최종 방어선
```

---

## 8. 핵심 원칙 요약

### Jason의 3가지 핵심 질문과 답

> "이렇게 작업을 하기 위해서는 준비해야 할 것은 무엇인가?"
> "준비된 것을 어떻게 효율적이고 짜임새 있게 나눠서 목표를 달성할 것인가?"
> "목표 달성을 위한 일관성은 어떻게 프로젝트 종료까지 유지할 것인가?"

#### Q1: 이렇게 작업을 하기 위해서는 준비해야 할 것은 무엇인가?

**A1: DNA 시스템 (환경 구축)**

```
문제:
- 각자 다른 로깅 (print, logging, structlog 혼재)
- 각자 다른 타입 (dict, custom class, Pydantic 혼재)
- 각자 다른 에러 처리
→ 일관성 붕괴!

해결: DNA 시스템
1. DNA 8개 시스템 구축 (골격계, 신경계, 면역계, ...)
2. Layer 구조 설정 (domain/application/infrastructure)
3. 표준 도구 설치 (Pydantic, structlog, pytest, FastAPI)
4. core/ 표준 모듈 (logging, types, errors, api, config, db, security)
5. DNA 시스템 Gate 통과 (모든 violations = 0)

→ 일관성을 "시스템"이 강제!
→ 작업자는 정해진 도구만 사용 가능!
```

#### Q2: 준비된 것을 어떻게 효율적이고 짜임새 있게 나눠서 목표를 달성할 것인가?

**A2: Task Breakdown (작업분해) + 2가지 분할 방식**

```
문제:
- 청사진 5000줄 → 200K 컨텍스트 초과
- 어디서부터 시작? 어떻게 나눔?
- 누락 발생 위험

해결 1: 작업분해 (Task Breakdown)
청사진 5000줄 → Task별 작업 지시서 (100줄)
├── 📘 청사진 참조: Line 145-178 (66줄)
├── 📋 표준 참조: Line 12-25 (40줄)
├── 🔧 사용 도구: PyJWT, Pydantic, structlog
├── 📦 입력/출력: user_id → token
├── 🔗 조립 정보: 의존성, 조립 순서
└── 🎯 완성 기준: 구체적 체크리스트

→ 5000줄 압축 → 100줄 집중!
→ 정확한 라인 참조로 누락 방지!

해결 2: 2가지 분할 방식 선택

Case 1 (모듈화 분할):
- Task 1: JWT 생성 모듈 (독립 블럭)
- Task 2: JWT 검증 모듈 (독립 블럭)
- Task 3: Login 엔드포인트 (Task 1, 2 조립)
→ 재사용 많을 때, 팀 협업 시

Case 2 (단계별 구현):
- Task 1: Login 완전 구현 (Logout 없어도 OK)
- Task 2: Logout 완전 구현 (일관성 유지)
- Task 3: Refresh 완전 구현 (일관성 유지)
→ 빠른 배포, 점진적 확장 시

4가지 판단 질문:
Q1: 200K 컨텍스트로 가능? → 나눠야 하나?
Q2: 이 Task만으로 의미있나? → 레고블럭인가?
Q3: 다른 Task와 일관성? → 같은 패턴인가?
Q4: 청사진에서 누락? → 모든 Task 포함?

→ 체계적 분할로 효율 극대화!
→ 누락 없이 목표 달성!
```

#### Q3: 목표 달성을 위한 일관성은 어떻게 프로젝트 종료까지 유지할 것인가?

**A3: 4-Layer 강제 시스템**

```
문제:
- "Blueprint 읽으세요" → AI가 무시
- "표준 도구 쓰세요" → AI가 잊음
- "print() 쓰지 마세요" → AI가 사용
→ 가이드라인은 약함!

해결: 시스템 강제화 (4-Layer)

Layer 1: 환경 강제 (작업 전)
├─ Blueprint 존재 확인 → 없으면 차단
├─ DNA 시스템 Gate 통과 확인 → 미통과 시 차단
├─ 표준 모듈 존재 확인 → 없으면 차단
└─ 표준 도구 설치 확인 → 없으면 차단
→ 작업 시작 불가 조건 차단!

Layer 2: 단위 작업 집중 (작업 중)
├─ 지정된 Blueprint 라인만 읽기 (5000줄 → 100줄)
├─ 지정된 Standards 섹션만 읽기
├─ 이 Task 체크리스트만 따르기
└─ 선언된 도구만 사용
→ 정보 최소화로 집중 강제!

Layer 3: 실시간 검증 (작업 중)
├─ print() 감지 → 즉시 차단
├─ 타입 힌트 누락 → 즉시 차단
├─ 비표준 모듈 import → 즉시 차단
└─ 의존성 위반 → 즉시 차단
→ 위반 발생 즉시 차단!

Layer 4: 완료 검증 (작업 후)
├─ ruff check 0 violations
├─ mypy 0 errors
├─ pytest all pass
├─ coverage ≥ 95%
└─ Import Linter 0 violations
→ 완성 기준 미달 시 차단!

→ 가이드라인이 아닌 "차단"으로 강제!
→ 프로젝트 종료까지 일관성 유지!
```

### 3가지 질문의 연결

```
Q1: 준비? → DNA 시스템 (환경 구축)
      ↓
   일관성 강제 환경 완성
      ↓
Q2: 나누기? → Task Breakdown (작업분해)
      ↓
   효율적 분할 + 누락 방지
      ↓
Q3: 유지? → 4-Layer System (시스템 강제)
      ↓
   프로젝트 종료까지 일관성 유지
      ↓
   성공!
```

---

### 방법론의 공식

```
매우 구체화된 계획 (Blueprint - 5000줄 초상세)
+ 정확하고 상세한 지시 (Checklist - 9-Step)
+ 필요한 정보만 제공 (Lego Block - 100줄만)
+ 시스템으로 강제화 (Enforcement - 4-Layer)
────────────────────────────────────────────
= 성공적인 AI 협업
```

### 핵심 개념 한눈에

#### Task (단위작업)
```
완성된 레고블럭
- 독립적으로 테스트 가능
- TODO 없는 완전한 구현
- 혼자서도 작동
- 다른 블럭과 조립 가능
- 라인 수/테스트 개수는 기준 아님!
```

#### Blueprint (청사진)
```
모든 레고블럭의 완전한 명세서
- 5000줄+ 초상세
- 모든 Task 명시 (누락 방지)
- 각 블럭의 완성 기준 (일관성 보장)
- 블럭 간 관계 명확화
```

#### Task Breakdown (작업분해)
```
필수 압축 레이어
- 5000줄 → 100줄 압축
- 정확한 라인 참조
- AI 컨텍스트 절약
- 누락 방지
```

#### DNA 시스템 (환경 구축)
```
강제 시스템 준비
- DNA 8개 시스템
- Layer 구조
- 표준 도구 설치
- core/ 표준 모듈
- DNA 시스템 Gate 통과 필수
→ 일관성을 "시스템"이 강제
```

### 두 가지 완성 조건

**1️⃣ 일관성 (Consistency)**
```
모든 Task가:
- 같은 패턴 사용 (structlog, Pydantic, pytest)
- 같은 도구 사용 (표준 도구만)
- 같은 구조 사용 (domain/application/infrastructure)
→ DNA 시스템이 강제
```

**2️⃣ 누락없음 (No Omissions)**
```
청사진의 모든 Task가:
- 결국 완료되어야 함
- Login만 먼저 OK, 하지만 Logout도 언젠가 완료
- Task Breakdown이 모든 Task 추출
→ Blueprint + Task Breakdown이 보장
```

### SPARK의 역할

```
[Human-Driven: Stage 1-4]
Stage 1: 아키텍처 결정 → ADR
     ↓
Stage 2: DNA 시스템 계획 → 환경 설계 문서
     ↓
Stage 3: DNA 시스템 구현 → 환경 구축 (일관성 강제 준비) ⭐
     ↓ 이제 core/ 모듈 다 있음!
Stage 4: Blueprint 작성 → 모든 레고블럭 명세 (5000줄)
     ↓ DNA 시스템 환경 기반으로 구체적 작성 가능!
──────────────────────────────────
     ↓ SPARK 시작
──────────────────────────────────

[SPARK-Enabled: Stage 5-8]
Stage 5: 작업분해 → Blueprint → Tasks (100줄)
     ↓ 자동화
Stage 6: 체크리스트 → Task → 9-Step
     ↓ 자동화
Stage 7: 도메인 구현 → Checklist 기반
     ↓ 강제화 (DNA 시스템 환경 + Quality Gates)
Stage 8: 최적화 → violations_total = 0
     ↓ 강제화
완성 → 레고블럭 조립
```

**SPARK = 시스템 강제화 레이어 (Stage 5-8)**

### 4-Layer 강제 시스템

```
Layer 1: 환경 강제 (작업 전)
├─ Blueprint 존재 확인
├─ DNA 시스템 Gate 통과 확인
├─ 표준 모듈 존재 확인
└─ 표준 도구 설치 확인
→ 환경 준비 검증

Layer 2: 단위 작업 집중 (작업 중)
├─ 지정된 Blueprint 라인만 읽기 (5000줄 → 100줄)
├─ 지정된 Standards 섹션만 읽기
├─ 이 Task 체크리스트만 따르기
└─ 선언된 도구만 사용
→ 정보 최소화

Layer 3: 실시간 검증 (작업 중)
├─ print() 감지 → 즉시 차단
├─ 타입 힌트 누락 → 즉시 차단
├─ 비표준 모듈 → 즉시 차단
└─ 의존성 위반 → 즉시 차단
→ 실시간 차단

Layer 4: 완료 검증 (작업 후)
├─ ruff check 0 violations
├─ mypy 0 errors
├─ pytest all pass
├─ coverage ≥ 95%
└─ Import Linter 0 violations
→ 최종 방어선 (Quality Gates)
```

### 절대 잊으면 안 되는 것

1. **바퀴 재발명 금지**: 표준 도구 선택하고 설정 (만들지 않음!)
2. **DNA 시스템 Gate**: 통과 없이 Stage 4 (청사진 작성) 진행 불가 (강제 환경 준비)
3. **Task = 레고블럭**: 라인 수가 아닌 기능 완성도로 판단
4. **Blueprint 초상세**: 모든 레고블럭 명세 (누락 방지)
5. **Task Breakdown 필수**: 5000줄 → 100줄 압축 (AI 컨텍스트 절약)
6. **일관성 + 누락없음**: 두 가지 완성 조건
7. **시스템 강제 > 가이드라인**: 차단으로 강제 (4-Layer)
8. **"알고 있다 ≠ 하고 있다"**: 시스템이 강제해야 함

### 성공 공식

```
표준 도구 우선 (바퀴 재발명 금지)
     ↓
DNA 시스템 (환경 구축, Gate 통과)
     ↓
Blueprint (모든 레고블럭 명세, 5000줄)
     ↓
Task Breakdown (100줄 압축, 라인 참조)
     ↓
Checklist (9-Step, 완성 기준)
     ↓
Implementation (시스템 강제)
     ↓
Quality Gates (violations = 0)
     ↓
성공!
```

---

**Version**: DNA v3.6 Essence
**Created**: 2025-11-09
**For**: SPARK v4.3 Foundation
