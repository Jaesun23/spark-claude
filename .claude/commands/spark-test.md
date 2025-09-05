---
name: spark-test
description: Intelligent test generation and validation with coverage-driven quality assurance
type: command
requires: tester-spark
---

# /spark-test - Intelligent Testing Command

**Purpose**: Testing is an art of healthy skepticism combined with systematic validation, where tests are not just safety nets but living documentation that teaches, validates, and inspires confidence.

## Decision Framework (2호의 테스트 전략 판단)

2호가 테스트 명령을 실행할 때 상황에 따른 판단 기준:

### Testing Strategy Balance (미묘한 조절이나 균형의 묘)

**상황별 테스트 접근:**
- **Critical Code**: 철저한 테스트 (모든 edge case 포함)
- **Time Pressure**: 위험 기반 테스트 (핵심 경로 우선)
- **Normal Cases**: 균형잡힌 테스트 (95% 커버리지 + 의미있는 테스트)

**구체적 판단 기준:**
- Coverage 95% 달성이 목표이지만, 무의미한 테스트로 채우지 않음
- 테스트 이름은 기능을 설명하는 문서 역할
- 버그 예방과 의도 증명에 집중

### Testing Philosophy

**테스트 작성 원칙:**
1. **Paranoid Assumption**: 모든 것이 실패할 수 있다고 가정
2. **Pragmatic Focus**: 가장 중요한 부분을 우선적으로 테스트
3. **Comprehensive Coverage**: 빠뜨린 부분이 없도록 체계적 접근
4. **Living Documentation**: 테스트 자체가 기능 설명서

## Design Principles (테스트 설계 지침)

**Test Pyramid Distribution:**
- Unit Tests: 70% (< 100ms 실행)
- Integration Tests: 20% (< 1s 실행)  
- E2E Tests: 10% (< 10s 실행)

**Quality Standards:**
- Line Coverage: ≥ 95%
- Branch Coverage: ≥ 90%
- Function Coverage: 100%
- Critical Paths: 100%

## 📝 2호 Execution Protocol (테스트 orchestration)

### **WHEN RECEIVING /spark-test COMMAND:**

**Single Phase: Testing**
```bash
1. Task("tester-spark", user_request)
2. Wait for completion
3. Check JSON: ~/.claude/workflows/current_task.json
   ✅ PASS CONDITIONS:
   - state.status == "completed"
   - quality.step_6_testing.coverage >= 95
   - output.tests.unit > 0
   - quality.can_proceed == true
   
   ❌ FAIL → Retry: Task("tester-spark", "Coverage insufficient: {current}%. Target: 95%+")
   Maximum 2 retries, then abort with coverage report.
```

**SUCCESS REPORT:**
```
✅ Testing Complete:
- Coverage: [line]% line, [branch]% branch, [function]% function
- Tests: [unit_count] unit, [integration_count] integration, [e2e_count] e2e  
- Quality: All tests passing, coverage target achieved
```

⚡ **Core Principle**: 2호는 tester-spark에게 위임하고 결과를 검증합니다

## Usage Examples

```bash
/spark-test "generate comprehensive unit tests for the authentication module"
/spark-test "run all tests and fix any failures" 
/spark-test "achieve 95% test coverage for the API endpoints"
/spark-test "create integration tests for the payment processing flow"
/spark-test "performance test the database query optimizations"
```

## Testing Capabilities

- **Unit Tests**: Function/method level testing with proper mocks and fixtures
- **Integration Tests**: Component interaction testing with realistic data
- **End-to-End Tests**: Full workflow testing using Playwright when available
- **Performance Tests**: Load testing and benchmarking for critical paths
- **Coverage Analysis**: Detailed coverage reporting with gap identification

## Quality Standards

All SPARK tests must meet:
- ✅ **95%+ Code Coverage**: Comprehensive coverage of critical functionality
- ✅ **Fast Execution**: Unit tests complete in < 10s, integration tests < 30s
- ✅ **Clear Naming**: Descriptive test names following AAA pattern
- ✅ **Proper Isolation**: Tests are independent and can run in any order
- ✅ **Realistic Scenarios**: Tests cover edge cases and error conditions

## SPARK Intelligence Integration

- 🎭 **QA Engineer Persona**: Activates testing-focused thinking patterns
- 🧪 **Smart Test Generation**: AI-powered test case creation
- 📊 **Coverage Optimization**: Identifies gaps and suggests additional tests
- 🚀 **Optimized Token Usage**: Efficient test creation and execution