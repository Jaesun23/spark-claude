# /implement - SPARK Implementation Command

**Purpose**: Quality-driven implementation workflow with 2호's intelligent orchestration and 88.4% token efficiency

## 🚀 Quality-Driven Multi-Agent Workflow

This command implements a complete development pipeline where **2호 acts as the quality gatekeeper**, ensuring all deliverables meet SPARK standards before progressing.

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

## 📝 2호의 오케스트레이션 실행 코드

### Phase 1: Implementation (Implementer-Spark)
```python
# 2호가 실행
max_impl_retries = 3
impl_attempt = 0

while impl_attempt < max_impl_retries:
    result = Task(
        description="SPARK Implementation",
        prompt=f"Implement: {user_request}. Quality gates will validate automatically.",
        subagent_type="implementer-spark"
    )
    
    # Hook이 자동으로 품질 검증 (current_task.json 확인)
    if all_quality_gates_passed():
        print("✅ 구현 품질 검증 통과 - Phase 2로 진행")
        break
    else:
        impl_attempt += 1
        if impl_attempt < max_impl_retries:
            print(f"⚠️ 품질 기준 미달, 재구현 시도 {impl_attempt}/{max_impl_retries}")
```

**2호의 품질 검토 체크리스트:**
- ✅ Syntax validation (구문 오류 0개)
- ✅ Type checking (MyPy 오류 0개)  
- ✅ Linting (Ruff 위반 0개)
- ✅ Security scan (보안 이슈 0개)
- ✅ Documentation (Docstring 존재)

### Phase 2: Testing (Tester-Spark)
```python
# 품질 통과 후 2호가 실행
max_test_retries = 2
test_attempt = 0

while test_attempt < max_test_retries:
    result = Task(
        description="Comprehensive Testing",
        prompt="Write comprehensive tests with 95%+ coverage. All tests must pass.",
        subagent_type="tester-spark"
    )
    
    # Hook이 테스트 결과 검증
    coverage = get_test_coverage()
    if coverage >= 95 and all_tests_passing():
        print(f"✅ 테스트 검증 통과 (Coverage: {coverage}%) - Phase 3로 진행")
        break
    else:
        test_attempt += 1
```

**2호의 테스트 품질 검토:**
- ✅ All tests passing (실패 0개)
- ✅ Coverage ≥ 95% (목표 달성)
- ✅ Edge cases covered (경계값 테스트)
- ✅ Integration tests exist (통합 테스트)

### Phase 3: Documentation (Documenter-Spark)
```python
# 테스트 통과 후 2호가 실행
result = Task(
    description="Documentation Generation",
    prompt="""Create comprehensive documentation:
    - README updates, API docs, Usage examples, Code docstrings""",
    subagent_type="documenter-spark"
)

print("✅ 문서화 완료 - 최종 보고서 생성")
```

## 💡 품질 기준

### Implementation Quality (Phase 1)
- **필수 통과 항목**: Syntax (0), MyPy (0), Ruff (0), Security (0), Docstrings (0)

### Testing Quality (Phase 2) 
- **필수 달성**: Coverage ≥95%, Test failures (0), Edge cases covered

### Documentation Quality (Phase 3)
- **필수 포함**: README updates, API docs, Usage examples, Inline docstrings

## 🚀 사용 예시

```bash
/implement "Create secure user authentication with JWT tokens"
/implement "Build responsive dashboard with real-time data"
/implement "Implement data validation pipeline with error handling"
```

## 📊 SPARK 효율성

- **SuperClaude**: 44,000 tokens (all agents loaded)
- **SPARK**: 5,100 tokens average (88.4% reduction)
- **Cost Savings**: $0.78 per request
- **Quality Assurance**: 10 quality gates + automatic retry system