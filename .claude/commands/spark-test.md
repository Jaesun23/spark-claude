---
name: spark-test
description: Intelligent test generation and validation with coverage-driven quality assurance
type: command
requires: tester-spark
---

# /spark-test - Intelligent Testing Command

**Purpose**: Testing is an art of healthy skepticism combined with systematic validation, where tests are not just safety nets but living documentation that teaches, validates, and inspires confidence.

## Philosophy (Natural Language Inspiration)

We test not to find bugs (though we will), but to prove our promises and document our intentions through executable examples. Testing philosophy shapes our approach:

- **Paranoid**: Assume everything will break
- **Pragmatic**: Test what matters most  
- **Comprehensive**: Leave no stone unturned

Every test should prevent a real bug or document intent. Test names should tell the story of the feature.

## Behavior Protocol (Code-Based Execution)

```python
class SparkTestCommand:
    """Intelligent test generation with systematic validation.
    
    This protocol enforces testing discipline while the philosophy above
    inspires thoughtful test design. Together they achieve balance.
    """
    
    # Test distribution pyramid
    TEST_PYRAMID = {
        "unit": {"proportion": 0.70, "speed": "< 100ms"},
        "integration": {"proportion": 0.20, "speed": "< 1s"},
        "e2e": {"proportion": 0.10, "speed": "< 10s"}
    }
    
    # Coverage requirements - NON-NEGOTIABLE
    COVERAGE_TARGETS = {
        "line": 0.95,
        "branch": 0.90,
        "function": 1.00,
        "critical_paths": 1.00
    }
    
    def generate_test_suite(self, analysis: dict, philosophy: str) -> dict:
        """Generate tests based on analysis and chosen philosophy."""
        test_suite = {
            "unit_tests": [],
            "integration_tests": [],
            "e2e_tests": []
        }
        
        # Philosophy shapes approach
        if philosophy == "paranoid":
            focus = ["error_paths", "edge_cases", "security", "concurrency"]
        elif philosophy == "pragmatic":
            focus = ["critical_paths", "complex_logic", "integrations"]
        else:  # comprehensive
            focus = ["all"]
        
        return self.generate_targeted_tests(analysis, focus, test_suite)
    
    def validate_test_quality(self, test: dict) -> bool:
        """Ensure test quality, not just coverage."""
        return (
            self.has_descriptive_name(test) and
            not self.is_trivial_test(test) and
            self.tests_behavior_not_implementation(test)
        )
    
    def balance_coverage_with_meaning(self, context: dict) -> str:
        """Balance between coverage metrics and meaningful tests.
        
        Sometimes 95% coverage with the right tests is better than
        100% with trivial tests - '미묘한 조절이나 균형의 묘'.
        """
        if context["code_criticality"] == "high":
            return "exhaustive_testing"
        elif context["time_constraint"] == "tight":
            return "risk_based_testing"
        else:
            return "balanced_testing"
```

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