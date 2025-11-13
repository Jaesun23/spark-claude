# Stage 3 Manual: ADR → Standards 변환 프로세스

> **목적**: ADR을 Standards 문서로 변환하는 상세 프로세스
> **버전**: v3.0 (2025-11-13, Stage 3 분리)
> **소요 시간**: 참고용 (Guide로 기본 작성 가능, Manual로 품질 향상)

---

## 📚 이 문서에 대해

**관계**:
- **Guide** (`03G-00_adr_guide.md`): ADR 기본 작성 방법
- **Manual 1** (`03M-01_adr_types_manual.md`): 5가지 유형 상세 설명
- **이 Manual**: ADR→Standards 변환 프로세스
- **Cases** (`03E-01_adr_examples_cases.md`): 실전 프로젝트 사례

**이 문서의 역할**:
- Guide의 섹션 5를 상세히 설명
- ADR → Standards 변환 절차
- Standards 파일 구조
- 상세 예시 (structlog, API, Testing)

---

## 5. ADR → Standards 변환 프로세스

### 5-1. 변환의 핵심 원칙

**ADR vs Standards 차이**:

| 측면 | ADR | Standards |
|------|-----|-----------|
| 목적 | 결정 기록 | 실행 가이드 |
| 내용 | What + Why | How + Enforcement |
| 형식 | Decision + Context | Rules + Examples |
| 독자 | 의사결정자 | 개발자 (Agent) |
| 변경 | 불변 (Superseded) | 업데이트 가능 |

**변환 원칙**:
1. ADR Decision → Standard Rules
2. ADR Compliance → Standard Enforcement
3. ADR Consequences (harder) → Standard Common Mistakes
4. ADR 예시 코드 → Standard Good/Bad Examples

### 5-2. 변환 Step-by-Step (예시: structlog)

#### Step 1: ADR Decision → Standard Sections

**ADR-015 Decision**:
```markdown
## Decision
모든 로깅은 structlog 사용, print()와 logging 모듈 금지.

패턴:
```python
from structlog import get_logger
logger = get_logger()
logger.info("event_name", key=value)
```

금지:
- print()
- import logging
```

**→ Standards/01_logging.md Section 1, 2**:
```markdown
# 01. Logging Standards

## 1. Import and Setup (Line 1-30)

**Mandatory Import**:
```python
from structlog import get_logger
logger = get_logger()
```

**Forbidden**:
❌ `import logging`
❌ `print()` for debugging

**Enforcement**: pre-commit hook, ruff T201

## 2. Event Format (Line 31-60)

**Pattern**: `logger.info("event_name", key=value)`

**Good Examples**:
✅ `logger.info("user_login", user_id=user.id, ip=request.ip)`

**Bad Examples**:
❌ `logger.info(f"User {user.id} logged in")` - No structure
```

#### Step 2: ADR Compliance → Standard Enforcement

**ADR-015 Compliance**:
```markdown
## Compliance
1. Automated: pre-commit hook (print 차단)
2. Automated: ruff T201
3. Semi-automated: PR 체크리스트
```

**→ Standards/01_logging.md Section 5**:
```markdown
## 5. Enforcement (Line 121-150)

**Pre-commit Hook**:
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: no-print
      entry: python scripts/check_no_print.py
```

**Ruff Configuration**:
```toml
[tool.ruff]
select = ["T201"]  # Detect print()
```

**Quality Gates** (Phase 5B):
```python
ruff_result = subprocess.run(["ruff", "check", "."])
if ruff_result.returncode != 0:
    BLOCK
```

**PR Checklist**:
- [ ] print() 없음
- [ ] logger.info("event", key=value) 형식
```

#### Step 3: ADR Consequences → Standard Common Mistakes

**ADR-015 Consequences (Harder)**:
```markdown
❌ Harder:
- 초기 설정 복잡도
- 팀 교육 필요
- Migration 작업
```

**→ Standards/01_logging.md Section 4**:
```markdown
## 4. Common Mistakes (Line 91-120)

**Mistake 1: 문자열 포맷 사용**
❌ Before: `logger.info(f"Processing {count} items")`
✅ After: `logger.info("processing_items", count=count)`

**Why**: ELK stack은 key-value 필요

**Mistake 2: 민감 정보 로깅**
❌ `logger.info("auth", password=password)`
✅ `logger.info("auth", user_id=user.id)`

**Why**: 보안 이슈, GDPR 위반
```

#### Step 4: 완성된 Standard 파일

**Standards/01_logging.md** (150 lines):
```markdown
# 01. Logging Standards

> **출처**: ADR-015 (structlog 사용)
> **업데이트**: 2025-01-15

## 1. Import and Setup (Line 1-30)

**Mandatory Import**:
```python
from structlog import get_logger
logger = get_logger()
```

**Configuration** (프로덕션):
```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)
```

**Configuration** (개발):
```python
structlog.configure(
    processors=[
        structlog.dev.ConsoleRenderer(),
    ],
)
```

**Forbidden**:
❌ `import logging` - 표준 logging 모듈 금지
❌ `print()` - 디버깅용 print 금지

**Enforcement**: pre-commit hook, ruff T201

---

## 2. Event Format (Line 31-60)

**Pattern**: `logger.info("event_name", key=value)`

**Event Naming**:
- snake_case 사용
- 동사_명사 형태 (`user_login`, `token_generated`)
- 과거형 아님 (`user_logged_in` ❌)

**Good Examples**:
```python
✅ logger.info("user_login", user_id=user.id, ip=request.ip)
✅ logger.error("token_expired", token_id=token.jti, user_id=user.id)
✅ logger.warning("rate_limit_exceeded", user_id=user.id, limit=100)
```

**Bad Examples**:
```python
❌ logger.info(f"User {user.id} logged in")  # 문자열 포맷
❌ logger.info("login")                       # Context 없음
❌ logger.info("User Login")                  # CamelCase
```

---

## 3. Context Binding (Line 61-90)

**Request ID Auto-binding**:
```python
from structlog import get_logger, BoundLogger

# FastAPI middleware
@app.middleware("http")
async def bind_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    logger = get_logger().bind(request_id=request_id)
    # ... call_next
```

**User Context Binding**:
```python
logger = get_logger().bind(user_id=current_user.id)
logger.info("order_created", order_id=order.id)
# Output: {"event": "order_created", "order_id": 123, "user_id": 456, ...}
```

---

## 4. Common Mistakes (Line 91-120)

**Mistake 1: 문자열 포맷 사용**
```python
❌ Before: logger.info(f"Processing {count} items")
✅ After:  logger.info("processing_items", count=count)
```
**Why**: ELK stack은 key-value 필요, 문자열 파싱 불가

**Mistake 2: 민감 정보 로깅**
```python
❌ logger.info("auth", password=password)
✅ logger.info("auth", user_id=user.id)
```
**Why**: 보안 이슈, GDPR 위반

**Mistake 3: Exception 로깅 시 context 누락**
```python
❌ logger.error("Error occurred")
✅ logger.error("token_generation_failed", user_id=user.id, exc_info=True)
```
**Why**: 디버깅을 위한 context 필요

---

## 5. Enforcement (Line 121-150)

**Pre-commit Hook**:
```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: no-print
      name: Detect print()
      entry: python scripts/check_no_print.py
      language: python
      types: [python]
```

**Ruff Configuration**:
```toml
[tool.ruff]
select = ["T201"]  # Detect print()
```

**Quality Gates** (Phase 5B):
```python
# ~/.claude/hooks/spark_quality_gates.py
ruff_result = subprocess.run(["ruff", "check", "."])
if ruff_result.returncode != 0:
    return "🚫 Quality gates FAILED"
```

**PR Checklist**:
- [ ] print() 없음
- [ ] logger.info("event", key=value) 형식
- [ ] 민감 정보(password, token) 로깅 없음
- [ ] Exception 로깅 시 exc_info=True 포함

**Manual Review** (주 1회):
- 민감 정보 로깅 여부
- Event naming convention 준수 여부
```

### 5-3. 변환 예시 2: FastAPI (부분 변환)

**ADR-025: FastAPI with OpenAPI** → **Standards/07_api.md**

#### ADR Decision (일부):
```markdown
## Decision
FastAPI로 RESTful JSON API 구축.

Endpoint 네이밍:
- Collection: GET /api/v1/users
- Item: GET /api/v1/users/{user_id}
```

#### Standards 변환:
```markdown
# 07. API Standards

> **출처**: ADR-025 (FastAPI with OpenAPI)

## 1. Endpoint Naming (Line 1-40)

**Pattern**: `/api/v1/{resource}`

**Collection endpoints**:
```python
@app.get("/api/v1/users")
async def list_users() -> List[UserResponse]:
    ...

@app.post("/api/v1/users")
async def create_user(user: UserCreateRequest) -> UserResponse:
    ...
```

**Item endpoints**:
```python
@app.get("/api/v1/users/{user_id}")
async def get_user(user_id: int) -> UserResponse:
    ...

@app.patch("/api/v1/users/{user_id}")
async def update_user(user_id: int, update: UserUpdateRequest) -> UserResponse:
    ...
```

**Action endpoints** (non-CRUD):
```python
@app.post("/api/v1/users/{user_id}/activate")
async def activate_user(user_id: int) -> UserResponse:
    ...
```

**Forbidden**:
❌ `/users` - API prefix 누락
❌ `/api/user` - 단수형 (복수형 사용!)
❌ `/api/v1/users/activate/{user_id}` - Action이 앞에 (뒤에!)
```

### 5-4. 변환 예시 3: Test Coverage (부분 업데이트)

**ADR-010: 95% Coverage** → **Standards/05_testing.md Section 4**

#### ADR Decision:
```markdown
## Decision
모든 Python 코드는 95% 이상 테스트 커버리지 필수.
- Unit test: 95% 이상
- Integration test: 85% 이상
```

#### Standards 변환 (기존 파일에 Section 추가):
```markdown
# 05. Testing Standards

> **출처**: ADR-005 (pytest), ADR-010 (95% coverage)

## 1. Test Framework (Line 1-40)
[기존 내용]

## 2. Test Structure (Line 41-80)
[기존 내용]

## 3. Fixtures (Line 81-120)
[기존 내용]

## 4. Coverage Requirements (Line 121-160) ← NEW!

> **출처**: ADR-010

**Mandatory Coverage**:
- Unit tests: **95% 이상**
- Integration tests: **85% 이상**

**Configuration**:
```ini
# pytest.ini
[pytest]
addopts = --cov=src --cov-fail-under=95 --cov-report=html
```

**CI Enforcement**:
```yaml
# .github/workflows/ci.yml
- name: Test with Coverage
  run: pytest --cov=src --cov-fail-under=95
```

**예외**:
- `__main__.py` (entry point)
- `*.pyi` (type stubs)
- Migration scripts (일회성)

**Coverage 측정**:
```bash
pytest --cov=src --cov-report=term-missing
```

**Enforcement**:
1. CI 실패 시 merge 불가
2. Quality Gates (Phase 5B) blocking
3. PR 체크리스트
```

---

