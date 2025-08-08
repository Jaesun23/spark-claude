# /implement - SPARK Implementation Command

**Purpose**: Quality-driven implementation workflow with 2호's intelligent orchestration and 88.4% token efficiency

## 🚀 Quality-Driven Multi-Agent Workflow

This command orchestrates a complete development pipeline with quality gates ensuring all deliverables meet SPARK standards before progressing.

### Workflow Architecture
```
┌──────────────────┐
│ Implementer-Spark│ ←────┐
└────────┬─────────┘      │
         ↓                │ (Quality retry)
    Quality Gates ────────┘
         ↓ (Passed)
┌──────────────────┐
│  Tester-Spark    │ ←────┐
└────────┬─────────┘      │
         ↓                │ (Coverage retry)
    Test Validation ──────┘
         ↓ (95%+ achieved)
┌──────────────────┐
│ Documenter-Spark │
└────────┬─────────┘
         ↓
    ✅ Completion Report
```

## 📝 Automatic Orchestration Process

⚡ **핵심 원칙**: 수동 확인 절차 없음 - 모든 단계는 조건 충족 시 자동 진행

## 📝 Orchestration Process

### Phase 1: Implementation (자동 실행)
I will immediately delegate to implementer-spark specialist:

1. **Task Assignment**: Request the implementer-spark specialist to implement the feature
2. **Quality Validation**: The SPARK quality gates hook automatically validates:
   - Syntax correctness (0 errors)
   - Type checking (MyPy 0 errors)
   - Linting compliance (Ruff 0 violations)
   - Security scanning (0 issues)
   - Documentation presence (docstrings required)
3. **Auto-Retry**: If quality gates fail, the specialist automatically retries (max 3 attempts)

**Quality Review Checklist:**
- ✅ Syntax validation (구문 오류 0개)
- ✅ Type checking (MyPy 오류 0개)  
- ✅ Linting (Ruff 위반 0개)
- ✅ Security scan (보안 이슈 0개)
- ✅ Documentation (Docstring 존재)

**Phase 1 → Phase 2 자동 진행:**
- ✅ 모든 품질 게이트 통과 (5/5) → 자동으로 Phase 2 시작
- ✅ 구현 완료 감지 → 즉시 테스트 단계로 전환
- ✅ SubagentStop hook 성공 → 대기 없이 다음 단계 실행

### Phase 2: Testing (자동 실행)
Once quality gates pass, I will immediately engage tester-spark specialist:

1. **Test Development**: Request comprehensive test creation with 95%+ coverage target
2. **Test Validation**: The test runner hook automatically verifies:
   - All tests passing (0 failures)
   - Coverage ≥ 95% (target achievement)
   - Edge cases covered (boundary testing)
   - Integration tests exist (system testing)
3. **Coverage Retry**: If coverage is below 95%, the specialist enhances tests (max 2 attempts)

**Test Quality Review:**
- ✅ All tests passing (실패 0개)
- ✅ Coverage ≥ 95% (목표 달성)
- ✅ Edge cases covered (경계값 테스트)
- ✅ Integration tests exist (통합 테스트)

**Phase 2 → Phase 3 자동 진행:**
- ✅ 모든 테스트 통과 (0 failures) → 자동으로 Phase 3 시작
- ✅ 커버리지 95% 달성 → 즉시 문서화 단계로 전환
- ✅ 테스트 품질 검증 완료 → 대기 없이 다음 단계 실행
- ✅ Hook 검증 통과 → 자동 진행 신호

### Phase 3: Documentation (자동 실행)
Once 95%+ coverage is achieved, I will immediately activate documenter-spark specialist:

1. **Documentation Creation**: Request comprehensive documentation including:
   - README updates with new features
   - API documentation for new endpoints
   - Usage examples and code samples
   - Inline docstrings for all functions
2. **Final Report**: Generate completion report with all deliverables

**Phase 3 완료 조건:**
- README.md 업데이트 완료
- API 문서화 완료 (해당되는 경우)
- 사용 예제 추가
- 모든 함수/클래스에 docstring 존재
- 최종 구현 보고서 작성

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