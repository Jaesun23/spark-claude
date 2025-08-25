# /spark-test - SPARK Testing Command

**Purpose**: Intelligent test generation, execution, and coverage analysis with SPARK enhancement

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-test COMMAND:**

```python
1. IMMEDIATELY CALL:
   Task("tester-spark", user_request)

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.step_6_testing.coverage >= 95
   - quality.can_proceed == true
   - output.tests.unit > 0
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Report test results to user
   ❌ ANY CONDITION FAILED → Task("tester-spark", "Improve coverage to 95%: {current_coverage}%")
```

The tester-spark specialist will:
- Generate comprehensive test suites based on the codebase
- Execute tests and analyze results
- Optimize for 95%+ code coverage
- Ensure all quality standards are met
- Provide detailed coverage reports and recommendations

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