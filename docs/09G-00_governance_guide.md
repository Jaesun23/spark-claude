# 09G-00: Governance 구현 가이드 (Automated Governance Implementation Guide)

**문서 버전**: 1.0
**작성일**: 2025-11-17
**대상**: DNA Methodology v4.0 Stage 9
**목적**: Project Standards를 자동화된 Governance로 구현하는 방법 제공

---

## 📋 목차

- [Part 1: Governance란 무엇인가](#part-1-governance란-무엇인가)
- [Part 2: 3-Phase 구현 로드맵](#part-2-3-phase-구현-로드맵)
- [Part 3: Phase 1 - Static Analysis](#part-3-phase-1---static-analysis)
- [Part 4: Phase 2 - Architecture Tests](#part-4-phase-2---architecture-tests)
- [Part 5: Phase 3 - Runtime Validation](#part-5-phase-3---runtime-validation)
- [Part 6: CI/CD 통합](#part-6-cicd-통합)
- [Part 7: 실전 예시](#part-7-실전-예시)
- [Appendix: Troubleshooting](#appendix-troubleshooting)

---

## Part 1: Governance란 무엇인가

### 1.1 Governance의 정의

**Governance**는 Project Standards (06D-01)를 **자동으로 강제**하는 시스템입니다.

**4대 구성요소의 마지막 단계**:

```
1. 성문화된 결정 (ADR)
  "Structlog를 사용한다"
      ↓
2. 재사용 가능한 컴포넌트 (DNA Systems)
  src/core/logging/logger.py
      ↓
3. 의무적 규칙 집합 (Standards)
  "✅ DO: from structlog import get_logger"
  "❌ DON'T: print('message')"
      ↓
4. 자동화된 거버넌스 (Governance) ← 여기!
  Pre-commit: print() 감지 → 커밋 실패
  ArchUnit: import logging 감지 → 빌드 실패
  Fitness: 로그 포맷 검증 → 배포 차단
```

**Governance = Standards + Automation + Enforcement**

### 1.2 왜 Governance가 필요한가?

**문제**: Standards만으로는 불충분

```markdown
# 06D-01: Project Standards
## 표준 01: 로깅
❌ DON'T: print("message")
```

**이 Standards만으로는:**
- ❌ 개발자가 실수로 print() 사용 가능
- ❌ Code Review에서 놓칠 수 있음
- ❌ 누적되면 일관성 깨짐

**해결책**: Automated Governance

```yaml
# .pre-commit-config.yaml
- id: disallow-print
  entry: "print\\("
  language: pygrep
```

**결과**:
- ✅ 개발자가 print() 작성 → 커밋 시 **자동 차단** (< 1초)
- ✅ Code Review 부담 감소
- ✅ 100% 일관성 보장

### 1.3 DNA v4.0의 혁신

**엔터프라이즈 vs DNA v4.0**:

| 항목 | 엔터프라이즈 | DNA v4.0 |
|------|-------------|----------|
| **강제 수단** | Code Review (인간) | Automation (AI) |
| **검증 시점** | PR 머지 전 | 커밋 전 + CI/CD + 배포 전 |
| **일관성** | 주관적 (리뷰어마다 다름) | 객관적 (100% 자동) |
| **비용** | 높음 (인건비) | 낮음 (초기 설정만) |
| **AI 협업** | 불가능 (암묵적) | 가능 (명시적) |

**DNA의 차별화**:
- **3-Phase**: Static → Arch → Runtime (단계적 강화)
- **Fast Feedback**: 커밋 전 (< 1초) 피드백
- **Zero-Tolerance**: 위반 시 무조건 차단

### 1.4 3-Phase Governance 개요

```
┌─────────────────────────────────────────────────────┐
│ Phase 1: Static Analysis (Day 1)                    │
│ - Pre-commit hooks                                  │
│ - Linters (Ruff, ESLint, mypy)                     │
│ - 시점: git commit 전                               │
│ - 피드백: < 1초                                     │
│ - 목적: 명백한 위반 차단                            │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ Phase 2: Architecture Tests (Week 2)                │
│ - ArchUnit, import-linter                          │
│ - pytest tests/architecture/                       │
│ - 시점: CI/CD (PR 머지 전)                         │
│ - 피드백: 2-5분                                     │
│ - 목적: 아키텍처 규칙 강제                          │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ Phase 3: Runtime Validation (Month 1+)              │
│ - Fitness Functions                                │
│ - Policy-as-Code (Terraform, OPA)                  │
│ - 시점: 통합 테스트, 배포 전                        │
│ - 피드백: 10-30분                                   │
│ - 목적: NFR 및 인프라 제약 검증                     │
└─────────────────────────────────────────────────────┘
```

---

## Part 2: 3-Phase 구현 로드맵

### 2.1 구현 순서 및 우선순위

**Why 3-Phase?**
- **비용 효율성**: 낮은 비용부터 → 높은 비용
- **피드백 속도**: 빠른 피드백부터 → 느린 피드백
- **영향 범위**: 개인 → 팀 → 전사

**우선순위 매트릭스**:

| Phase | 비용 | 효과 | 피드백 속도 | 우선순위 |
|-------|------|------|------------|---------|
| Phase 1: Static | 낮음 | 높음 | 매우 빠름 (< 1초) | ⭐⭐⭐ |
| Phase 2: Arch | 중간 | 높음 | 빠름 (2-5분) | ⭐⭐ |
| Phase 3: Runtime | 높음 | 중간 | 느림 (10-30분) | ⭐ |

### 2.2 각 Phase별 적용 대상

**Phase 1: Static Analysis**
- ✅ 코드 포맷팅 (Black, Prettier)
- ✅ 명백한 규칙 위반 (print(), import logging)
- ✅ 타입 힌트 (mypy, pyright)
- ❌ 복잡한 로직 (실행해야 알 수 있음)

**Phase 2: Architecture Tests**
- ✅ Layer 의존성 (Domain → Infrastructure 금지)
- ✅ 순환 의존성
- ✅ 패키지 구조
- ❌ 런타임 동작

**Phase 3: Runtime Validation**
- ✅ NFR (성능, 보안, 가용성)
- ✅ 외부 제약 (AWS Region, IAM Policy)
- ✅ 통합 동작
- ❌ 빠른 피드백 (느림)

### 2.3 구현 타임라인

```
Day 1:
  ✅ Pre-commit hooks 설치
  ✅ Ruff, Black 설정
  ✅ 표준 01 (로깅) 강제화

Week 1:
  ✅ 표준 02-05 강제화
  ✅ Custom pre-commit hooks

Week 2:
  ✅ Architecture tests (pytest)
  ✅ import-linter 설정

Week 3:
  ✅ CI/CD 통합 (GitHub Actions)
  ✅ PR 머지 게이트

Month 1:
  ✅ Fitness Functions (NFR 검증)

Month 2:
  ✅ Policy-as-Code (Terraform Sentinel)
```

---

## Part 3: Phase 1 - Static Analysis

### 3.1 Pre-commit 설치 및 설정

**Step 1: Pre-commit 설치**

```bash
# 1. pre-commit 설치
pip install pre-commit

# 2. 프로젝트에 추가
pip freeze | grep pre-commit >> requirements-dev.txt
```

**Step 2: .pre-commit-config.yaml 작성**

```yaml
# .pre-commit-config.yaml
repos:
  # 기본 hooks (파일 정리)
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-added-large-files
        args: ['--maxkb=500']

  # Ruff: Python Linter & Formatter (매우 빠름!)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # MyPy: 타입 체크 (선택적)
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
          - types-PyYAML
```

**Step 3: Git hooks 등록**

```bash
# Git hooks 등록 (한 번만 실행)
pre-commit install

# 확인
git status
# → .git/hooks/pre-commit 파일 생성됨
```

**Step 4: 전체 파일 실행 (최초)**

```bash
# 모든 파일에 pre-commit 실행
pre-commit run --all-files

# 실패 시 자동 수정 후 다시 실행
git add .
pre-commit run --all-files
```

### 3.2 DNA Standards 강제화 (Custom Hooks)

**표준 01: 로깅 (print() 금지, import logging 금지)**

```yaml
# .pre-commit-config.yaml에 추가
repos:
  - repo: local
    hooks:
      # print() 사용 금지
      - id: disallow-print
        name: "표준 01: print() 금지"
        entry: "print\\("
        language: pygrep
        types: [python]
        files: ^src/
        exclude: ^tests/
        description: |
          ❌ print() is prohibited in src/
          ✅ Use: from src.core.logging import get_logger

      # import logging 금지
      - id: disallow-stdlib-logging
        name: "표준 01: import logging 금지"
        entry: "^import logging|^from logging import"
        language: pygrep
        types: [python]
        files: ^src/
        exclude: ^src/core/logging/
        description: |
          ❌ stdlib logging is prohibited
          ✅ Use: structlog from DNA System 01
```

**표준 02: 에러 핸들링 (Generic Exception 금지)**

```yaml
      # Generic Exception raise 금지
      - id: no-generic-exception
        name: "표준 02: raise Exception() 금지"
        entry: "raise Exception\\("
        language: pygrep
        types: [python]
        files: ^src/
        description: |
          ❌ raise Exception("msg") is prohibited
          ✅ Use: class MyError(BaseProjectException)
```

**표준 06: API 설계 (동사 사용 금지)**

```yaml
      # RESTful API: 동사 사용 금지
      - id: no-verbs-in-api-routes
        name: "표준 06: API route에 동사 금지"
        entry: "@(app|router)\\.(get|post|put|delete)\\(['\"].*/(create|update|delete|get)"
        language: pygrep
        types: [python]
        files: ^src/api/
        description: |
          ❌ POST /createUser
          ✅ POST /users
```

### 3.3 실행 및 검증

**테스트 1: print() 사용 시도**

```python
# src/api/test.py
def hello():
    print("Hello")  # 이 줄이 차단되어야 함
```

```bash
# git commit 시도
git add src/api/test.py
git commit -m "test"

# 결과:
# 표준 01: print() 금지.................................................Failed
# - hook id: disallow-print
# - exit code: 1
#
# src/api/test.py:2:    print("Hello")
```

**테스트 2: 정상 코드**

```python
# src/api/test.py
from src.core.logging import get_logger

logger = get_logger(__name__)

def hello():
    logger.info("hello")  # ✅ 통과
```

```bash
git commit -m "test"
# ✅ 모든 hooks 통과!
```

### 3.4 개발자 경험 최적화

**Tip 1: 자동 수정 활성화**

```yaml
# Ruff가 자동으로 수정 가능한 것은 수정
- id: ruff
  args: [--fix]
```

**Tip 2: 실패 시 명확한 메시지**

```yaml
- id: disallow-print
  description: |
    ❌ print() is prohibited in src/
    ✅ Use: from src.core.logging import get_logger
    📚 See: docs/06D-01_standards.md#표준-01-로깅
```

**Tip 3: 특정 파일 제외**

```yaml
- id: disallow-print
  exclude: |
    (?x)^(
      tests/.*|
      scripts/.*|
      src/core/logging/.*
    )$
```

**Tip 4: 특정 hook만 실행**

```bash
# 특정 hook만 실행
pre-commit run disallow-print --all-files

# hook 건너뛰기 (긴급 시만!)
SKIP=disallow-print git commit -m "urgent fix"
```

---

## Part 4: Phase 2 - Architecture Tests

### 4.1 Architecture Tests란?

**목적**: 아키텍처 규칙을 코드로 검증

**검증 대상**:
- ✅ Layer 의존성 (Domain → Infrastructure 금지)
- ✅ 순환 의존성
- ✅ 패키지 구조
- ✅ DNA Systems 사용 강제

**도구**:
- **Python**: pytest + AST + import-linter
- **Java**: ArchUnit
- **TypeScript**: dependency-cruiser

### 4.2 Python: pytest + AST

**tests/architecture/test_layers.py**

```python
"""
Layer 의존성 검증

Layered Architecture:
- api → domain → infrastructure
- domain은 infrastructure 의존 금지!
"""
import pytest
from pathlib import Path


def test_domain_does_not_import_infrastructure():
    """Domain 레이어는 Infrastructure 레이어 임포트 금지"""
    domain_files = list(Path("src/domain").rglob("*.py"))
    violations = []

    for file in domain_files:
        content = file.read_text()

        # Infrastructure import 찾기
        if "from src.infrastructure" in content:
            violations.append(f"{file}: from src.infrastructure")
        elif "import src.infrastructure" in content:
            violations.append(f"{file}: import src.infrastructure")

    assert not violations, (
        f"\n❌ Domain imports Infrastructure:\n"
        + "\n".join(violations)
        + "\n\n✅ Fix: Remove infrastructure imports from domain"
    )


def test_api_does_not_import_infrastructure_directly():
    """API는 Infrastructure를 직접 임포트 금지 (Domain을 통해야 함)"""
    api_files = list(Path("src/api").rglob("*.py"))
    violations = []

    for file in api_files:
        content = file.read_text()

        # Direct infrastructure import 찾기
        if "from src.infrastructure" in content:
            violations.append(str(file))

    assert not violations, (
        f"\n❌ API directly imports Infrastructure:\n"
        + "\n".join(violations)
        + "\n\n✅ Fix: Use dependency injection through Domain"
    )
```

**tests/architecture/test_dna_systems.py**

```python
"""
DNA Systems 사용 강제 검증
"""
import ast
import pytest
from pathlib import Path


def test_all_logging_uses_dna_system_01():
    """모든 로깅은 DNA System 01 (Structlog) 사용"""
    src_files = list(Path("src").rglob("*.py"))
    violations = []

    for file in src_files:
        # src/core/logging/ 자체는 제외
        if "src/core/logging" in str(file):
            continue

        content = file.read_text()

        # logger 사용하는 파일만 검증
        if "logger." in content or "logging." in content:
            # DNA System 01 import 확인
            has_dna_import = (
                "from src.core.logging import" in content
            )

            if not has_dna_import:
                violations.append(str(file))

    assert not violations, (
        f"\n❌ These files use logging without DNA System 01:\n"
        + "\n".join(violations)
        + "\n\n✅ Fix: from src.core.logging import get_logger"
    )


def test_no_generic_exception_raises():
    """Generic Exception raise 금지"""
    src_files = list(Path("src/domain").rglob("*.py"))
    violations = []

    for file in src_files:
        tree = ast.parse(file.read_text(), filename=str(file))

        for node in ast.walk(tree):
            if isinstance(node, ast.Raise):
                if isinstance(node.exc, ast.Call):
                    if isinstance(node.exc.func, ast.Name):
                        if node.exc.func.id == "Exception":
                            violations.append(
                                f"{file}:{node.lineno}"
                            )

    assert not violations, (
        f"\n❌ Generic Exception raises found:\n"
        + "\n".join(violations[:10])  # 처음 10개만
        + "\n\n✅ Fix: Use BaseProjectException subclasses"
    )
```

### 4.3 Python: import-linter

**설치**:

```bash
pip install import-linter
```

**.importlinter**:

```toml
[importlinter]
root_package = src

# Contract 1: Layered Architecture
[importlinter:contract:layers]
name = Layered Architecture
type = layers
layers =
    api
    domain
    infrastructure

# Contract 2: DNA Systems 사용 강제
[importlinter:contract:no-stdlib-logging]
name = No stdlib logging in src/
type = forbidden
source_modules =
    src
forbidden_modules =
    logging
ignore_imports =
    src.core.logging -> logging

# Contract 3: 순환 의존성 금지
[importlinter:contract:no-cycles]
name = No circular dependencies
type = independence
modules =
    src.domain
    src.infrastructure
    src.api
```

**실행**:

```bash
# import-linter 실행
import-linter

# 결과:
# ✅ Layered Architecture: PASSED
# ✅ No stdlib logging in src/: PASSED
# ✅ No circular dependencies: PASSED
```

### 4.4 Java: ArchUnit

**build.gradle**:

```groovy
dependencies {
    testImplementation 'com.tngtech.archunit:archunit-junit5:1.3.0'
}
```

**ArchitectureTest.java**:

```java
package com.myproject.architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
import static com.tngtech.archunit.library.Architectures.layeredArchitecture;
import static com.tngtech.archunit.library.GeneralCodingRules.*;

class ArchitectureTest {

    private final JavaClasses classes = new ClassFileImporter()
        .importPackages("com.myproject");

    @Test
    void layered_architecture_is_respected() {
        ArchRule rule = layeredArchitecture()
            .consideringAllDependencies()
            .layer("API").definedBy("..api..")
            .layer("Domain").definedBy("..domain..")
            .layer("Infrastructure").definedBy("..infrastructure..")

            .whereLayer("API").mayNotBeAccessedByAnyLayer()
            .whereLayer("Domain").mayOnlyBeAccessedByLayers("API")
            .whereLayer("Infrastructure").mayOnlyBeAccessedByLayers("API", "Domain");

        rule.check(classes);
    }

    @Test
    void no_cycles_in_packages() {
        ArchRule rule = NO_CLASSES_SHOULD_HAVE_CYCLES;
        rule.check(classes);
    }

    @Test
    void domain_should_not_depend_on_infrastructure() {
        ArchRule rule = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAPackage("..infrastructure..");

        rule.check(classes);
    }
}
```

---

## Part 5: Phase 3 - Runtime Validation

### 5.1 Fitness Functions (NFR 검증)

**tests/fitness/test_performance.py**:

```python
"""
NFR 성능 요구사항 검증

ADR-201: 검색 성능 vs 일관성 트레이드오프
- NFR P-01: API 응답 시간 < 1초 (P95)
"""
import pytest
import requests
import time
import statistics


@pytest.mark.fitness
@pytest.mark.slow
def test_api_p95_response_time_under_1_second():
    """NFR P-01: API P95 응답 시간 < 1초"""
    # 100회 요청
    response_times = []
    failures = 0

    for i in range(100):
        start = time.time()
        try:
            response = requests.get(
                "http://localhost:8000/api/search?q=test",
                timeout=2
            )
            elapsed = time.time() - start

            if response.status_code == 200:
                response_times.append(elapsed)
            else:
                failures += 1

        except requests.RequestException as e:
            failures += 1

    # 실패율 검증
    assert failures < 5, f"Too many failures: {failures}/100"

    # P95 계산
    p95 = statistics.quantiles(response_times, n=20)[18]
    mean = statistics.mean(response_times)
    p50 = statistics.median(response_times)

    # 검증
    assert p95 < 1.0, (
        f"\n❌ NFR P-01 Failed:"
        f"\n  P95: {p95:.3f}s (> 1.0s)"
        f"\n  P50: {p50:.3f}s"
        f"\n  Mean: {mean:.3f}s"
    )


@pytest.mark.fitness
def test_database_query_performance():
    """NFR P-02: 복잡한 쿼리 < 500ms"""
    from src.infrastructure.database import db

    # 복잡한 쿼리 (JOIN 포함)
    query = """
        SELECT u.*, COUNT(o.id) as order_count
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.active = true
        GROUP BY u.id
        LIMIT 1000
    """

    start = time.time()
    results = db.execute(query)
    elapsed = time.time() - start

    assert elapsed < 0.5, f"Query took {elapsed:.3f}s (> 500ms)"
    assert len(results) > 0
```

**tests/fitness/test_security.py**:

```python
"""
보안 NFR 검증
"""
import pytest
import requests


@pytest.mark.fitness
def test_api_requires_authentication():
    """모든 API는 인증 필수 (public 제외)"""
    protected_endpoints = [
        "/api/users/me",
        "/api/orders",
        "/api/admin/settings"
    ]

    for endpoint in protected_endpoints:
        # 인증 없이 요청
        response = requests.get(f"http://localhost:8000{endpoint}")

        # 401 Unauthorized 반환해야 함
        assert response.status_code == 401, (
            f"{endpoint} allows unauthenticated access!"
        )


@pytest.mark.fitness
def test_sensitive_data_not_in_logs():
    """로그에 민감 정보 (비밀번호, API 키) 없음"""
    from pathlib import Path
    import re

    log_files = list(Path("logs").rglob("*.log"))

    # 민감 정보 패턴
    sensitive_patterns = [
        r"password['\"]?\s*[:=]\s*['\"]?[\w]+",  # password: "xxx"
        r"api[_-]?key['\"]?\s*[:=]\s*['\"]?[\w]+",  # api_key: "xxx"
        r"\d{16}",  # 카드 번호 (16자리)
    ]

    violations = []

    for log_file in log_files:
        content = log_file.read_text()

        for pattern in sensitive_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                violations.append(f"{log_file}: {matches[0]}")

    assert not violations, (
        f"\n❌ Sensitive data found in logs:\n"
        + "\n".join(violations)
    )
```

### 5.2 Policy-as-Code (Terraform)

**policies/aws-region-restriction.sentinel**:

```hcl
# Sentinel Policy: AWS Seoul Region만 허용

import "tfplan/v2" as tfplan

# 모든 AWS 리소스 검사
all_aws_resources = filter tfplan.resource_changes as _, rc {
    rc.provider_name is "registry.terraform.io/hashicorp/aws"
}

# Region 검증 함수
validate_region = func(resource) {
    # region 속성이 있는 경우만 검증
    if "region" in resource.change.after {
        return resource.change.after.region is "ap-northeast-2"
    }

    # region이 없으면 provider default 사용 (별도 검증)
    return true
}

# Main rule
main = rule {
    all all_aws_resources as _, resource {
        validate_region(resource)
    }
}
```

**Terraform 실행**:

```bash
# Policy 검증 포함 실행
terraform plan

# Sentinel Policy 실행
sentinel apply policies/aws-region-restriction.sentinel

# 결과:
# ✅ Pass: All AWS resources use ap-northeast-2
# 또는
# ❌ Fail: Resource 'aws_s3_bucket.data' uses us-east-1
```

### 5.3 OPA (Open Policy Agent)

**policies/kubernetes-security.rego**:

```rego
# OPA Policy: Kubernetes Security

package kubernetes.security

# 모든 컨테이너는 root로 실행 금지
deny[msg] {
    input.kind == "Deployment"
    container := input.spec.template.spec.containers[_]
    not container.securityContext.runAsNonRoot

    msg := sprintf(
        "Container '%s' must set runAsNonRoot: true",
        [container.name]
    )
}

# 모든 이미지는 latest 태그 금지
deny[msg] {
    input.kind == "Deployment"
    container := input.spec.template.spec.containers[_]
    endswith(container.image, ":latest")

    msg := sprintf(
        "Container '%s' uses :latest tag (prohibited)",
        [container.name]
    )
}

# 민감 정보는 Secret 사용 강제
deny[msg] {
    input.kind == "Deployment"
    container := input.spec.template.spec.containers[_]
    env := container.env[_]

    # PASSWORD, API_KEY 등은 valueFrom.secretKeyRef 사용해야 함
    regex.match("(PASSWORD|API_KEY|SECRET)", env.name)
    not env.valueFrom.secretKeyRef

    msg := sprintf(
        "Env '%s' contains sensitive data but doesn't use Secret",
        [env.name]
    )
}
```

**OPA 실행**:

```bash
# Kubernetes manifest 검증
opa eval -d policies/ -i deployment.yaml "data.kubernetes.security.deny"

# 결과:
# [
#   "Container 'app' must set runAsNonRoot: true",
#   "Env 'API_KEY' contains sensitive data but doesn't use Secret"
# ]
```

---

## Part 6: CI/CD 통합

### 6.1 GitHub Actions

**.github/workflows/quality-gates.yml**:

```yaml
name: Quality Gates

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  # Phase 1: Static Analysis
  static-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run pre-commit hooks
        run: |
          pre-commit run --all-files --show-diff-on-failure

      - name: Type checking (mypy)
        run: |
          mypy src/

  # Phase 2: Architecture Tests
  architecture-tests:
    runs-on: ubuntu-latest
    needs: static-analysis
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install import-linter

      - name: Run architecture tests
        run: |
          pytest tests/architecture/ -v --tb=short

      - name: Run import-linter
        run: |
          import-linter --verbose

  # Unit & Integration Tests
  tests:
    runs-on: ubuntu-latest
    needs: static-analysis
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Run unit tests
        run: |
          pytest tests/unit/ -v --cov=src --cov-report=xml

      - name: Run integration tests
        run: |
          pytest tests/integration/ -v

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

  # Phase 3: Fitness Functions (배포 전에만)
  fitness-functions:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    needs: [architecture-tests, tests]
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Start test server
        run: |
          uvicorn src.main:app --host 0.0.0.0 --port 8000 &
          sleep 5

      - name: Run fitness functions
        run: |
          pytest tests/fitness/ -v -m fitness

  # 모든 게이트 통과 확인
  quality-gates-passed:
    runs-on: ubuntu-latest
    needs: [static-analysis, architecture-tests, tests]
    steps:
      - name: All gates passed
        run: |
          echo "✅ All quality gates passed!"
```

### 6.2 GitLab CI

**.gitlab-ci.yml**:

```yaml
stages:
  - static
  - architecture
  - test
  - fitness

# Phase 1: Static Analysis
static-analysis:
  stage: static
  image: python:3.11
  script:
    - pip install -e ".[dev]"
    - pre-commit run --all-files
    - mypy src/
  cache:
    paths:
      - .cache/pip

# Phase 2: Architecture Tests
architecture-tests:
  stage: architecture
  image: python:3.11
  script:
    - pip install -e ".[dev]" import-linter
    - pytest tests/architecture/ -v
    - import-linter

# Unit Tests
unit-tests:
  stage: test
  image: python:3.11
  script:
    - pip install -e ".[dev]"
    - pytest tests/unit/ --cov=src --cov-report=term --cov-report=xml
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

# Phase 3: Fitness Functions (main 브랜치만)
fitness-functions:
  stage: fitness
  image: python:3.11
  only:
    - main
  script:
    - pip install -e ".[dev]"
    - uvicorn src.main:app --host 0.0.0.0 --port 8000 &
    - sleep 5
    - pytest tests/fitness/ -v -m fitness
```

### 6.3 PR 머지 게이트 설정

**GitHub Branch Protection Rules**:

```
Settings → Branches → Branch protection rules

Rule for: main

✅ Require status checks to pass before merging
  ✅ static-analysis
  ✅ architecture-tests
  ✅ tests
  ✅ quality-gates-passed

✅ Require branches to be up to date before merging

✅ Include administrators (선택)
```

**결과**:
- ❌ Quality gate 실패 → PR 머지 불가능
- ✅ 모든 gate 통과 → PR 머지 가능

---

## Part 7: 실전 예시

### 7.1 Stock Trading Platform Governance

**프로젝트 구조**:

```
stock-trading/
├── .pre-commit-config.yaml    # Phase 1
├── .importlinter                # Phase 2
├── tests/
│   ├── architecture/           # Phase 2
│   │   ├── test_layers.py
│   │   ├── test_dna_systems.py
│   │   └── test_kis_api.py
│   ├── fitness/                # Phase 3
│   │   ├── test_performance.py
│   │   └── test_kis_rate_limit.py
│   └── ...
├── .github/workflows/
│   └── quality-gates.yml       # CI/CD
└── ...
```

**Phase 1: Pre-commit (.pre-commit-config.yaml)**:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: local
    hooks:
      # 표준 01: 로깅
      - id: disallow-print
        name: "표준 01: print() 금지"
        entry: "print\\("
        language: pygrep
        types: [python]
        files: ^src/

      # 표준 07: KIS API 직접 호출 금지
      - id: no-direct-kis-api
        name: "표준 07: KIS API 직접 호출 금지"
        entry: "openapi\\.koreainvestment\\.com"
        language: pygrep
        types: [python]
        files: ^src/domain/
        description: |
          ❌ Direct KIS API call in domain layer
          ✅ Use: KISClient from src.infrastructure.kis
```

**Phase 2: Architecture Tests**:

```python
# tests/architecture/test_kis_api_usage.py
def test_domain_uses_kis_client_only():
    """표준 07: Domain은 KISClient만 사용"""
    domain_files = list(Path("src/domain").rglob("*.py"))

    for file in domain_files:
        content = file.read_text()

        # 직접 requests 사용 금지
        if "requests.get" in content or "requests.post" in content:
            # KIS API URL이 있으면 위반
            if "openapi.koreainvestment.com" in content:
                pytest.fail(
                    f"{file} calls KIS API directly. "
                    "Use KISClient from infrastructure"
                )
```

**Phase 3: Fitness Functions**:

```python
# tests/fitness/test_kis_rate_limit.py
@pytest.mark.fitness
def test_kis_rate_limit_respected():
    """NFR: KIS API Rate Limit 준수 (초당 20건)"""
    from src.infrastructure.kis import KISClient

    client = KISClient()
    start = time.time()
    call_count = 0

    # 1초 동안 호출
    while time.time() - start < 1.0:
        try:
            client.get_current_price("005930")
            call_count += 1
        except RateLimitError:
            break

    # 초당 20건 이하 확인
    assert call_count <= 20, (
        f"Rate limit violated: {call_count} calls/sec (> 20)"
    )
```

### 7.2 실행 결과 예시

**성공 케이스**:

```bash
$ git commit -m "feat: add user api"

표준 01: print() 금지.................................................Passed
표준 01: import logging 금지...........................................Passed
표준 02: raise Exception() 금지........................................Passed
표준 07: KIS API 직접 호출 금지........................................Passed
Ruff.................................................................Passed
Ruff format..........................................................Passed

[main 2ab2697] feat: add user api
 1 file changed, 50 insertions(+)
```

**실패 케이스**:

```bash
$ git commit -m "feat: add debug logging"

표준 01: print() 금지.................................................Failed
- hook id: disallow-print
- exit code: 1

src/api/users.py:42:    print(f"Debug: {user}")

❌ print() is prohibited in src/
✅ Use: from src.core.logging import get_logger
📚 See: docs/06D-01_standards.md#표준-01-로깅
```

**수정 후**:

```python
# src/api/users.py
from src.core.logging import get_logger

logger = get_logger(__name__)

def create_user(user_data):
    logger.debug("create_user", user_data=user_data)  # ✅
    # ...
```

```bash
$ git commit -m "feat: add user api with proper logging"
✅ 모든 hooks 통과!
```

---

## Appendix: Troubleshooting

### A.1 Pre-commit 문제 해결

**문제 1: hook이 실행 안 됨**

```bash
# 원인: git hooks 미등록
# 해결:
pre-commit install

# 확인:
ls .git/hooks/pre-commit
```

**문제 2: hook이 너무 느림**

```bash
# 원인: 모든 파일 검사
# 해결: 변경된 파일만 검사
pre-commit run  # git staged 파일만

# 특정 파일만:
pre-commit run --files src/api/test.py
```

**문제 3: 긴급 커밋 (hook 건너뛰기)**

```bash
# ⚠️ 긴급 시에만 사용!
git commit --no-verify -m "hotfix"

# 또는 특정 hook만 건너뛰기:
SKIP=disallow-print git commit -m "temporary debug"
```

### A.2 Architecture Tests 문제 해결

**문제 1: Import 경로 문제**

```python
# 원인: src/ 가 PYTHONPATH에 없음
# 해결:
# Option 1: pytest.ini
[pytest]
pythonpath = .

# Option 2: 환경 변수
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

**문제 2: False positive**

```python
# 원인: 테스트 코드도 검증됨
# 해결: 테스트 제외
def test_domain_does_not_import_infrastructure():
    domain_files = list(Path("src/domain").rglob("*.py"))
    # tests/ 제외!

    for file in domain_files:
        if "test" in str(file):  # 테스트 파일 제외
            continue
        # ...
```

### A.3 CI/CD 문제 해결

**문제 1: GitHub Actions 느림**

```yaml
# 해결: Cache 사용
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
```

**문제 2: Fitness Functions 실패 (서버 미실행)**

```yaml
# 해결: Health check 추가
- name: Start test server
  run: |
    uvicorn src.main:app &
    sleep 5

    # Health check
    curl --retry 5 --retry-delay 2 http://localhost:8000/health

- name: Run fitness functions
  run: pytest tests/fitness/ -v
```

---

## 🎯 최종 체크리스트

### Phase 1 Setup (Day 1)

- [ ] pre-commit 설치
- [ ] .pre-commit-config.yaml 작성
- [ ] Git hooks 등록 (`pre-commit install`)
- [ ] 전체 파일 실행 (`pre-commit run --all-files`)
- [ ] 표준 01-05 강제화 hooks 추가
- [ ] 팀원 교육 (pre-commit 사용법)

### Phase 2 Setup (Week 2)

- [ ] tests/architecture/ 폴더 생성
- [ ] test_layers.py 작성
- [ ] test_dna_systems.py 작성
- [ ] import-linter 설치 및 설정
- [ ] CI/CD에 architecture tests 추가

### Phase 3 Setup (Month 1+)

- [ ] tests/fitness/ 폴더 생성
- [ ] Performance NFR tests 작성
- [ ] Security NFR tests 작성
- [ ] Policy-as-Code 설정 (선택)
- [ ] CI/CD에 fitness tests 추가 (main 브랜치만)

### CI/CD Setup

- [ ] .github/workflows/quality-gates.yml 작성
- [ ] Branch protection rules 설정
- [ ] PR 템플릿에 checklist 추가
- [ ] README에 배지 추가

---

**작성일**: 2025-11-17
**작성자**: 2호 (with Jason)
**관련 문서**:
- `docs/03G-00_adr_guide.md` - ADR 작성 가이드
- `docs/06G-00_standards_guide.md` - Standards 작성 가이드
- `docs/research/20251117_Gemini_미싱링크_분석결과.md` - 분석 결과

---

## 🎉 축하합니다!

DNA Methodology v4.0 **Stage 3-6-9 완성**! 🚀

이제 다음 단계로:
1. **Stage 7: Blueprint** - 구체적 설계
2. **Stage 8: Implementation** - 실제 구현
3. **Celebrate!** - 미싱 링크 해결 완료! 🎊
