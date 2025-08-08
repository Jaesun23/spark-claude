---
description: SPARK-enhanced implementation with 2호's intelligent quality review and orchestration
---

# SPARK Implementation Command - Quality-Driven Workflow

## 🚀 Intelligent Quality-Driven Orchestration

This command implements a complete development workflow where **2호 acts as the quality gatekeeper**, ensuring all code meets SPARK standards before progressing.

## 📊 Quality-Driven Workflow

```
┌──────────────────┐
│ Implementer-Spark│ ←────┐
└────────┬─────────┘      │
         ↓                │ (품질 실패 시 재구현)
    🧑‍💼 2호 품질 검토 ────┘
         ↓ (품질 통과)
┌──────────────────┐
│  Tester-Spark    │ ←────┐
└────────┬─────────┘      │
         ↓                │ (95% 미달 시 재작성)
    🧑‍💼 2호 테스트 검토 ───┘
         ↓ (95%+ 달성)
┌──────────────────┐
│ Documenter-Spark │
└────────┬─────────┘
         ↓
    ✅ 완료 보고서
```

## 🎯 2호의 품질 관리 역할

### 핵심: 2호가 각 단계의 품질을 검증하고 다음 단계 결정

2호는 각 서브에이전트 완료 후:
1. **품질 메트릭 확인**: Hook 결과 및 실행 결과 검토
2. **기준 충족 판단**: 정해진 품질 기준과 비교
3. **라우팅 결정**: 재작업 또는 다음 단계 진행

## 📝 상세 워크플로우

### Phase 1: 구현 (Implementer-Spark)
```python
# 2호가 실행
Task(
    description="SPARK Implementation - $ARGUMENTS",
    prompt="""Implement the requested feature using appropriate personas.
    Quality gates will be automatically checked after completion.""",
    subagent_type="implementer-spark"
)
```

**2호의 품질 검토 체크리스트:**
- ✅ Syntax validation passed (구문 오류 0개)
- ✅ Type checking passed (MyPy 오류 0개)
- ✅ Linting passed (Ruff 위반 0개)
- ✅ Security scan passed (보안 이슈 0개)
- ✅ Documentation exists (Docstring 존재)

**품질 기준:**
- 모든 항목 통과 시 → Phase 2로 진행
- 1개 이상 실패 시 → Phase 1 재실행 (최대 3회)

### Phase 2: 테스트 (Tester-Spark)
```python
# 품질 통과 후 2호가 실행
Task(
    description="Comprehensive Testing - $ARGUMENTS",
    prompt="""Write comprehensive tests with 95%+ coverage.
    All tests must pass and coverage target must be met.""",
    subagent_type="tester-super"
)
```

**2호의 테스트 품질 검토:**
- ✅ All tests passing (실패 0개)
- ✅ Coverage ≥ 95% (목표 달성)
- ✅ Edge cases covered (경계값 테스트)
- ✅ Integration tests exist (통합 테스트)
- ✅ Test quality validated (테스트 코드 품질)

**테스트 기준:**
- 95%+ 커버리지 달성 시 → Phase 3로 진행
- 95% 미달 또는 실패 시 → Phase 2 재실행 (최대 2회)

### Phase 3: 문서화 (Documenter-Spark)
```python
# 테스트 통과 후 2호가 실행
Task(
    description="Documentation Generation - $ARGUMENTS",
    prompt="""Create comprehensive documentation including:
    - README updates
    - API documentation
    - Code docstrings
    - Usage examples""",
    subagent_type="documenter-super"
)
```

**2호의 문서 품질 확인:**
- ✅ README updated (프로젝트 문서)
- ✅ API documented (API 레퍼런스)
- ✅ Examples provided (사용 예제)
- ✅ Docstrings complete (코드 문서)

### Phase 4: 최종 보고서
2호가 직접 생성하는 종합 보고서:

```markdown
## ✅ SPARK Implementation Complete

### 📊 Quality Metrics
- **구현 품질**: 10/10 gates passed
- **테스트 커버리지**: 97.5%
- **문서화 완성도**: 100%

### 📁 Deliverables
- Implementation: [files created/modified]
- Tests: [test files created]
- Documentation: [docs updated]

### ⏱️ Performance
- Total duration: X minutes
- Retry count: X times
- Token usage: ~8,000 (82% saved)
```

## 🔧 2호의 실제 실행 코드

```python
# 2호가 실제로 실행할 오케스트레이션
def execute_sparkclaude_workflow(task_description):
    """2호의 품질 기반 워크플로우 실행"""
    
    # Phase 1: Implementation
    max_impl_retries = 3
    impl_attempt = 0
    
    while impl_attempt < max_impl_retries:
        # Run implementer-spark
        result = Task(
            description=f"Implementation - {task_description}",
            subagent_type="implementer-spark"
        )
        
        # Check quality gates (automatically done by hook)
        quality_passed = check_implementation_quality()
        
        if quality_passed:
            print("✅ 구현 품질 검증 통과")
            break
        else:
            impl_attempt += 1
            if impl_attempt < max_impl_retries:
                print(f"⚠️ 품질 기준 미달, 재구현 시도 {impl_attempt}/{max_impl_retries}")
            else:
                print("❌ 최대 재시도 횟수 초과")
                return False
    
    # Phase 2: Testing
    max_test_retries = 2
    test_attempt = 0
    
    while test_attempt < max_test_retries:
        result = Task(
            description=f"Testing - {task_description}",
            subagent_type="tester-super"
        )
        
        # Check test coverage and quality
        coverage = get_test_coverage()
        tests_passing = check_test_results()
        
        if coverage >= 95 and tests_passing:
            print(f"✅ 테스트 품질 검증 통과 (Coverage: {coverage}%)")
            break
        else:
            test_attempt += 1
            if test_attempt < max_test_retries:
                print(f"⚠️ 테스트 기준 미달 (Coverage: {coverage}%), 재작성 시도 {test_attempt}/{max_test_retries}")
            else:
                print("❌ 테스트 최대 재시도 횟수 초과")
                return False
    
    # Phase 3: Documentation
    result = Task(
        description=f"Documentation - {task_description}",
        subagent_type="documenter-super"
    )
    
    print("✅ 문서화 완료")
    
    # Generate final report
    generate_completion_report(task_description)
    return True
```

## 💡 품질 기준 상세

### 구현 품질 기준 (Phase 1)
- **필수 통과 항목:**
  - Syntax errors: 0
  - Type errors (MyPy): 0
  - Linting violations (Ruff): 0
  - Security issues: 0
  - Missing docstrings: 0

### 테스트 품질 기준 (Phase 2)
- **필수 달성 목표:**
  - Test coverage: ≥95%
  - Test failures: 0
  - Edge cases: Covered
  - Integration tests: Present

### 문서 품질 기준 (Phase 3)
- **필수 포함 항목:**
  - README updates
  - API documentation
  - Usage examples
  - Inline docstrings

## 🚀 사용 예시

```bash
/implement-super "Create secure user authentication with JWT tokens"
```

**실행 과정:**
1. **Implementer-Spark**: Security + Backend 페르소나로 구현
2. **2호 품질 검토**: 10개 품질 게이트 확인
3. **Tester-Spark**: 95%+ 커버리지 테스트 작성
4. **2호 테스트 검토**: 커버리지 및 테스트 통과 확인
5. **Documenter-Spark**: 완전한 문서 생성
6. **완료**: 최종 보고서 제공

## 📈 기대 효과

- **품질 보증**: 모든 코드가 SPARK 품질 기준 충족
- **자동 재작업**: 품질 미달 시 자동으로 재구현/재테스트
- **완전한 문서화**: 모든 기능이 문서화됨
- **82% 토큰 절약**: 효율적인 페르소나 활용
- **95%+ 테스트 커버리지**: 안정적인 코드 보장