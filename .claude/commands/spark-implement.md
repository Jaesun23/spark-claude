---
name: spark-implement
description: Quality-driven implementation workflow orchestrating multiple specialists through phases with strict quality gates
type: command
requires: implementer-spark, tester-spark, documenter-spark
---

# /spark-implement - Quality-Driven Implementation Command

**Purpose**: Orchestrates a complete development pipeline where quality isn't just checked but cultivated at every step, ensuring deliverables that inspire confidence and pride.

## Decision Framework (2호의 판단 기준)

2호가 이 명령어를 실행할 때 다음 기준으로 판단하고 행동합니다:

### Quality vs Velocity Balance (미묘한 조절이나 균형의 묘)

**상황별 의사결정:**
- **긴급한 요청**: 품질 게이트는 유지하되, 핵심 기능에 집중
- **복잡한 요청**: 시간을 더 투자해서 thorough 검증
- **일반적 요청**: 균형잡힌 접근으로 품질과 속도 모두 확보

**구체적 행동 지침:**
- 모든 품질 게이트는 반드시 통과 (violations_total = 0)
- 단, 시간 압박이 있을 때는 documentation을 간소화 가능
- 복잡도가 높을 때는 추가 validation 단계 포함

### Implementation Philosophy

**코드 품질 원칙:**
1. **Elegance over Cleverness**: 복잡한 로직보다는 읽기 쉬운 코드
2. **Proactive Error Handling**: 실제 사용 시나리오를 고려한 예외 처리
3. **Teaching Documentation**: 단순 설명이 아닌 이해를 돕는 문서
4. **Intent-Based Testing**: Coverage 숫자가 아닌 의도 검증 중심
5. **Prose-Like Code**: 코드 자체가 문서가 되도록 작성

## Design Principles (설계 지침)

**Phase 진행 원칙:**
- **Sequential Execution**: implementation → testing → documentation 순서 엄수
- **Quality Gates**: 각 단계마다 품질 검증 필수
- **Context-Aware Retry**: 실패 시 맥락을 고려한 재시도 (최대 3회)
- **Evidence-Based Decision**: JSON 결과를 바탕으로 다음 단계 결정

**품질 기준 (Zero Tolerance):**
- Syntax Errors: 0
- Type Errors: 0  
- Linting Violations: 0
- Security Issues: 0
- Test Coverage: ≥ 95%
- Documentation: 완전성 100%

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

## 📝 2호 Execution Protocol (정확한 실행 지침)

### **WHEN RECEIVING /spark-implement COMMAND:**

**PHASE 1: Implementation**
```bash
1. Task("implementer-spark", user_request)
2. Wait for completion
3. Check JSON: ~/.claude/workflows/current_task.json
   ✅ PASS CONDITIONS:
   - state.status == "completed"
   - quality.violations_total == 0  
   - quality.can_proceed == true
   - len(output.files.created) > 0 OR len(output.files.modified) > 0
   
   ❌ FAIL → Retry: Task("implementer-spark", "Fix violations: [list specific quality issues]")
   Maximum 3 retries, then abort with error report.
```

**PHASE 2: Testing**
```bash
4. Task("tester-spark", "Create comprehensive tests for the implemented features")
5. Wait for completion  
6. Check JSON: ~/.claude/workflows/current_task.json
   ✅ PASS CONDITIONS:
   - state.status == "completed"
   - quality.step_6_testing.coverage >= 95
   - output.tests.unit > 0
   - quality.can_proceed == true
   
   ❌ FAIL → Retry: Task("tester-spark", "Improve coverage to 95%+ and add missing tests")
   Maximum 2 retries, then abort with coverage report.
```

**PHASE 3: Documentation**
```bash
7. Task("documenter-spark", "Create comprehensive documentation for the feature")
8. Wait for completion
9. Check JSON: ~/.claude/workflows/current_task.json
   ✅ PASS CONDITIONS:
   - state.status == "completed"
   - output.docs.readme == true
   - output.docs.api == true (if API endpoints were created)
   - quality.step_7_documentation.docstrings == 0 (violations)
   
   ❌ FAIL → Retry: Task("documenter-spark", "Complete missing documentation")
   Maximum 2 retries, then abort with documentation status.
```

**SUCCESS REPORT:**
```
✅ Implementation Complete:
- Files: [list created/modified files]
- Tests: [coverage]% coverage, [count] test files
- Docs: README updated, API docs generated
- Quality: All gates passed (0 violations)
```

⚡ **Core Principle**: 2호는 각 단계마다 JSON 결과를 검토하고 다음 에이전트 호출을 결정합니다

## 💡 Quality Standards Summary

**Implementation**: Syntax(0), Types(0), Linting(0), Security(0), Docstrings(0)  
**Testing**: Coverage ≥95%, All tests pass, Edge cases covered  
**Documentation**: README updated, API docs complete, Examples provided

## 🚀 Usage Examples

```bash
/implement "Create secure user authentication with JWT tokens"
/implement "Build responsive dashboard with real-time data"
/implement "Implement data validation pipeline with error handling"
```

## 📊 SPARK Efficiency

- **Token Usage**: Lazy-loading architecture (only load required agents)
- **Quality Assurance**: 8 quality gates + retry system (max 3 attempts)
- **JSON Communication**: Unified current_task.json for all phases