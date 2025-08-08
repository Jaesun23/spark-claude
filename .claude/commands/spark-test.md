# /spark-test - SPARK Testing Command

**Purpose**: Intelligent test generation, execution, and coverage analysis with SPARK enhancement

## Execution Instructions

When this command is called, use the Task tool to launch the tester-spark agent:

```
Use the Task tool with subagent_type "tester-spark" to perform comprehensive testing.
Pass the user's specific testing request as the prompt parameter.
The tester-spark agent will generate, execute, and analyze tests with quality assurance.
```

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
- 🚀 **88.4% Token Efficiency**: Efficient test creation and execution