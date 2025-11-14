# Stage 4: DNA 시스템 계획 가이드

> **목적**: 11개 DNA 시스템 구축을 위한 청사진, 작업 분해, 체크리스트 작성
> **버전**: v1.0 (2025-11-13)
> **소요 시간**: 2-4시간

---

## 🎯 이 Stage의 목표

**DNA 시스템 구축을 위한 완전한 계획 수립**

- DNA 청사진: 11개 시스템의 파일 구조와 인터페이스
- DNA 작업 분해: 구체적인 하위 작업 목록
- DNA 체크리스트: 통합 체크리스트 1개

---

## 🧬 DNA 시스템이란?

**DNA 시스템 = 모든 소프트웨어의 기본 설계도**

생명의 DNA가 모든 생물의 기초이듯, 11개 DNA 시스템은 모든 소프트웨어 프로젝트의 기초입니다.

### 특징
- ✅ 언어, 프레임워크, 도메인 무관
- ✅ 11개 모두 필수 (선택 없음)
- ✅ 자동 강제 (지키지 않으면 빌드/실행 실패)
- ✅ 일관성 필수 (한 곳만 다르면 전체 혼란)

### 왜 필요한가?
```
❌ 문서로 알려주기 → AI가 안 읽음/잊어버림
❌ 체크리스트 작성 → AI가 안 지킴
❌ 지시/설명 반복 → 매 세션마다 반복

✅ 해결: "환경"을 만들어서 잘못할 수 없게!
```

### 11개 DNA 시스템 목록

**기반 DNA (1-6)** - 코드 작성 전 필수:
1. Type System (타입 체커)
2. Observability System (로깅/메트릭/추적)
3. Testing System (테스트 프레임워크)
4. Code Quality System (포맷터/린터)
5. Architecture Enforcement (Layer 경계)
6. Configuration System (환경 변수 + 의존성)

**도메인 DNA (7-11)** - 기능 구현과 함께:
7. Error Handling System (Result/Either)
8. Performance System (벤치마크/프로파일링)
9. API System (인터페이스)
10. Data System (저장/조회)
11. Security System (인증/암호화)

---

## 📥 입력 문서 (Stage 3에서 받은 것)

### 필수
- **`03A-001~011_*.md`** (DNA 시스템 ADR 11개)
  - 각 DNA 시스템별 기술 선택 결정
  - 예: 03A-001_type_system.md (mypy vs TypeScript strict)
  - 예: 03A-002_observability.md (structlog vs winston)

### 참조
- **`DNA_Systems_11_Complete_Guide.md`**
  - 11개 DNA 시스템 상세 설명
  - Kent Beck 검증 사례
  - 체크리스트 템플릿

---

## 📋 작업 단계

### Step 1: DNA 청사진 작성 (1-2시간)

#### 1.1 디렉토리 구조 설계

**목표**: src/core/ 디렉토리 구조 결정

**작업**:
```markdown
# 04D-01_dna_blueprint.md 예시

## 디렉토리 구조

```
src/
├── core/                  # DNA 시스템 공통 모듈
│   ├── __init__.py
│   ├── logger.py         # Observability (DNA 2)
│   ├── error.py          # Error Handling (DNA 7)
│   ├── config.py         # Configuration (DNA 6)
│   └── types.py          # Type definitions (DNA 1)
├── api/                  # API System (DNA 9)
│   ├── __init__.py
│   └── routes.py
├── database/             # Data System (DNA 10)
│   ├── __init__.py
│   └── models.py
└── security/             # Security System (DNA 11)
    ├── __init__.py
    └── auth.py

tests/
├── core/                 # DNA 시스템 테스트
│   ├── test_logger.py
│   ├── test_error.py
│   └── test_config.py
└── integration/

benchmarks/               # Performance (DNA 8)
├── benchmark_core.py
└── profiles/

pyproject.toml            # Configuration + Type + Testing + Quality (DNA 1,3,4,6)
.pre-commit-config.yaml   # Code Quality (DNA 4)
mypy.ini                  # Type System (DNA 1)
ruff.toml                 # Code Quality (DNA 4)
```
```

#### 1.2 각 DNA 시스템별 파일 목록

**목표**: 11개 DNA 각각 어떤 파일을 만들지 명시

**작업**:
```markdown
### DNA 1: Type System
- [ ] pyproject.toml에 mypy 설정
- [ ] mypy.ini 파일 생성
- [ ] src/core/types.py (공통 타입 정의)

### DNA 2: Observability System
- [ ] src/core/logger.py
  - get_logger() 함수
  - trace_id 전파 로직
  - 구조화된 로깅 설정
- [ ] tests/core/test_logger.py

### DNA 3: Testing System
- [ ] pyproject.toml에 pytest 설정
- [ ] tests/conftest.py (공통 fixture)
- [ ] tests/core/ 구조

... (11개 모두 명시)
```

#### 1.3 인터페이스 설계

**목표**: 각 DNA 시스템의 공개 API 정의

**작업**:
```markdown
## DNA 시스템 공개 인터페이스

### Observability (logger.py)
```python
from src.core.logger import get_logger

logger = get_logger(__name__)
logger.info("message", extra={"user_id": 123})
```

### Error Handling (error.py)
```python
from src.core.error import AppError, Result

def process() -> Result[Data, AppError]:
    return Ok(data) or Err(error)
```

### Configuration (config.py)
```python
from src.core.config import config

db_url = config.DATABASE_URL
api_key = config.API_KEY
```

... (11개 모두 명시)
```

---

### Step 2: DNA 작업 분해 (30분-1시간)

#### 2.1 11개 DNA → 하위 작업 분해

**목표**: 각 DNA 시스템을 구체적인 작업으로 분해

**작업**:
```markdown
# 04T-01_dna_tasks.md 예시

## DNA 작업 분해

### DNA 1: Type System (3개 하위 작업)
1. pyproject.toml에 mypy 의존성 추가
2. mypy.ini 설정 파일 작성 (strict mode)
3. src/core/types.py 공통 타입 정의

### DNA 2: Observability System (5개 하위 작업)
1. structlog 의존성 추가
2. src/core/logger.py 기본 구조 작성
3. get_logger() 함수 구현
4. trace_id 전파 로직 구현
5. tests/core/test_logger.py 작성

... (11개 DNA → 총 30-50개 하위 작업)
```

#### 2.2 우선순위 결정

**목표**: 기반 DNA 6개 → 도메인 DNA 5개 순서 확정

**작업**:
```markdown
## 우선순위

### Phase 1: 기반 DNA (1-6) - 먼저 구축
- DNA 1: Type System
- DNA 2: Observability System
- DNA 3: Testing System
- DNA 4: Code Quality System
- DNA 5: Architecture Enforcement
- DNA 6: Configuration System

→ 이 6개가 완성되면 개발 환경 완성!

### Phase 2: 도메인 DNA (7-11) - 기능과 함께
- DNA 7: Error Handling System
- DNA 8: Performance System
- DNA 9: API System
- DNA 10: Data System
- DNA 11: Security System
```

#### 2.3 의존성 파악

**목표**: 작업 간 의존 관계 명시

**작업**:
```markdown
## 의존성

- Testing (DNA 3) → Type (DNA 1) 필요
  - 이유: 테스트에서 타입 체크 필요

- Observability (DNA 2) → Configuration (DNA 6) 필요
  - 이유: 로그 레벨 설정 필요

- Error Handling (DNA 7) → Type (DNA 1) 필요
  - 이유: Result<T, E> 타입 정의
```

---

### Step 3: DNA 체크리스트 작성 (30분)

#### 3.1 통합 체크리스트 작성

**목표**: 1개 파일로 11개 DNA 전체 관리

**작업**:
```markdown
# 04L-01_dna_checklist.md

## DNA 시스템 11개 구축 체크리스트

### [ ] DNA 1: Type System
  - [ ] pyproject.toml에 mypy 추가
    ```bash
    uv add --dev mypy
    ```
  - [ ] mypy.ini 작성 (strict mode)
    ```ini
    [mypy]
    strict = True
    warn_return_any = True
    ```
  - [ ] src/core/types.py 작성
  - [ ] mypy 실행 확인
    ```bash
    mypy src/
    ```

### [ ] DNA 2: Observability System
  - [ ] structlog 추가
    ```bash
    uv add structlog
    ```
  - [ ] src/core/logger.py 작성
  - [ ] get_logger() 구현
  - [ ] trace_id 전파 구현
  - [ ] tests/core/test_logger.py 작성
  - [ ] 테스트 실행
    ```bash
    pytest tests/core/test_logger.py
    ```

... (11개 DNA 모두)

### [ ] 전체 검증
  - [ ] 모든 DNA 시스템 동작 확인
  - [ ] 테스트 커버리지 95%+ 확인
  - [ ] ruff/mypy 0 violations 확인
```

**핵심**:
- ✅ 1개 파일로 전체 진행 상황 확인
- ✅ 11개 섹션 (DNA별)
- ✅ 하위 작업은 체크박스로
- ✅ 실행 명령어 포함 (복붙 가능)

---

## 📤 출력 문서 (이 Stage에서 생성해야 할 문서)

### 1. **`04D-01_dna_blueprint.md`** (DNA 청사진)

**내용**:
- 전체 디렉토리 구조
- 각 DNA 시스템별 파일 목록
- 공개 인터페이스 (사용 예시 포함)
- 설정 파일 구조

**예시 구조**:
```markdown
# DNA 시스템 청사진

## 1. 디렉토리 구조
[전체 tree 구조]

## 2. DNA 시스템별 파일
### DNA 1: Type System
[파일 목록]

### DNA 2: Observability System
[파일 목록]

... (11개)

## 3. 공개 인터페이스
### Observability
[코드 예시]

### Error Handling
[코드 예시]

... (11개)

## 4. 설정 파일
### pyproject.toml
[내용]

### mypy.ini
[내용]
```

---

### 2. **`04T-01_dna_tasks.md`** (DNA 작업 분해)

**내용**:
- 11개 DNA → 30-50개 하위 작업
- 우선순위 (Phase 1/2)
- 의존성

**예시 구조**:
```markdown
# DNA 작업 분해

## 전체 작업 개요
- 총 작업 수: 42개
- Phase 1 (기반 DNA): 24개
- Phase 2 (도메인 DNA): 18개

## Phase 1: 기반 DNA (1-6)

### DNA 1: Type System
1. [작업 1]
2. [작업 2]
...

### DNA 2: Observability System
...

## Phase 2: 도메인 DNA (7-11)
...

## 의존성 그래프
[의존 관계 명시]
```

---

### 3. **`04L-01_dna_checklist.md`** (DNA 체크리스트)

**내용**:
- 통합 체크리스트 1개
- 11개 섹션 (DNA별)
- 실행 가능한 명령어 포함

**예시 구조**:
```markdown
# DNA 시스템 구축 체크리스트

## 진행 상황
- [ ] Phase 1: 기반 DNA (0/6)
- [ ] Phase 2: 도메인 DNA (0/5)
- [ ] 전체 검증 (0/3)

## DNA 시스템 구축

### [ ] DNA 1: Type System
  - [ ] [하위 작업 1]
    ```bash
    [실행 명령어]
    ```
  - [ ] [하위 작업 2]
  ...

### [ ] DNA 2: Observability System
...

## 전체 검증
- [ ] 모든 DNA 동작 확인
- [ ] 테스트 커버리지 95%+
- [ ] 품질 검사 0 violations
```

---

## 🔄 다음 Stage로 전달되는 것

**Stage 4 → Stage 5**:
- ✅ DNA 청사진 (04D-01) → 파일 구조와 인터페이스 설계
- ✅ DNA 작업 분해 (04T-01) → 구체적인 작업 목록
- ✅ DNA 체크리스트 (04L-01) → 실행 가능한 체크리스트

**Stage 5에서 사용**:
- 체크리스트 따라 실제 구현
- 청사진의 인터페이스 준수
- 작업 분해 순서대로 진행

---

## ⚠️ 주의사항

### 1. 언어별 차이 반영
- Python: pyproject.toml + uv
- TypeScript: package.json + pnpm
- Rust: Cargo.toml
- Go: go.mod

→ ADR에서 결정된 언어에 맞게 작성!

### 2. 체크리스트는 1개!
- ❌ DNA별로 11개 파일 만들지 말 것
- ✅ 1개 파일에 11개 섹션

### 3. 실행 가능한 명령어 필수
- 체크리스트에 복붙 가능한 명령어 포함
- 예: `uv add --dev mypy`, `pytest tests/`

### 4. Kent Beck 검증 목표
- 11개 중 10개 이상 달성 목표
- Observability는 최소화 가능 (라이브러리 특성상)

---

## 📚 참고 자료

### 필수
- `DNA_Systems_11_Complete_Guide.md` - 11개 DNA 상세 설명
- `03A-001~011_*.md` - DNA 시스템 ADR

### 참고
- Kent Beck BPlusTree 프로젝트 구조
- 다른 Stage 가이드 (입출력 형식 참조)

---

## ✅ 완료 기준

이 Stage는 다음 조건을 모두 만족하면 완료:

- [ ] **04D-01_dna_blueprint.md** 작성 완료
  - [ ] 디렉토리 구조 명시
  - [ ] 11개 DNA 파일 목록
  - [ ] 공개 인터페이스 정의

- [ ] **04T-01_dna_tasks.md** 작성 완료
  - [ ] 30-50개 하위 작업 분해
  - [ ] 우선순위 (Phase 1/2)
  - [ ] 의존성 명시

- [ ] **04L-01_dna_checklist.md** 작성 완료
  - [ ] 통합 체크리스트 1개
  - [ ] 11개 섹션
  - [ ] 실행 명령어 포함

- [ ] **검증**
  - [ ] 3개 문서 간 일관성 확인
  - [ ] ADR과 청사진 일치 확인
  - [ ] 파일명 규칙 준수 (04D-01, 04T-01, 04L-01)

---

**마지막 업데이트**: 2025-11-13
**다음 검토**: Stage 5 가이드 작성 시 연계성 확인
