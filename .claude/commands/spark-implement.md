---
name: spark-implement
description: Quality-driven implementation workflow orchestrating multiple specialists through phases with strict quality gates
type: command
requires: implementer-spark, tester-spark, documenter-spark
---

# /spark-implement - Quality-Driven Implementation Command

**Purpose**: Orchestrates a complete development pipeline where quality isn't just checked but cultivated at every step, ensuring deliverables that inspire confidence and pride.

## Philosophy (Natural Language Inspiration)

This command embodies a philosophy of comprehensive, thoughtful implementation that values:
- **Elegance in simplicity**, not cleverness
- **Thoughtful error handling** that anticipates real-world usage  
- **Documentation that teaches**, not just describes
- **Tests that validate intent**, not just coverage
- **Code that reads like well-written prose**

The command strives to nurture quality through iterative refinement, ensuring each phase builds upon excellence rather than merely meeting requirements.

## Behavior Protocol (Code-Based Execution)

```python
class SparkImplementCommand:
    """Quality-driven implementation workflow with intelligent orchestration.
    
    This protocol ensures unambiguous execution while the philosophy above
    provides nuanced inspiration. Together they maintain '미묘한 조절이나 균형의 묘'.
    """
    
    # Workflow phases - IMMUTABLE ORDER
    PHASES = ["implementation", "testing", "documentation"]
    
    # Quality requirements - ZERO TOLERANCE
    QUALITY_GATES = {
        "syntax_errors": 0,
        "type_errors": 0,
        "linting_violations": 0,
        "security_issues": 0,
        "test_coverage": 0.95,
        "documentation_completeness": 1.0
    }
    
    # Retry logic with learning
    MAX_RETRIES = 3
    RETRY_WITH_CONTEXT = True
    
    def orchestrate(self, user_request: str) -> Dict:
        """Main orchestration flow - no phase skipping allowed."""
        workflow_state = {
            "phases_completed": [],
            "current_phase": "implementation",
            "quality_achieved": None
        }
        
        # Execute phases in strict sequence
        for phase in self.PHASES:
            result = self.execute_phase(phase, user_request)
            
            if not result["success"]:
                # Retry with feedback from failure
                result = self.retry_with_learning(phase, result["feedback"])
                if not result["success"]:
                    return self.graceful_failure(workflow_state, result)
            
            workflow_state["phases_completed"].append(phase)
        
        return self.success_report(workflow_state)
    
    def validate_phase_transition(self, current: str, next: str) -> bool:
        """Ensure no phase skipping or backward movement."""
        phase_order = {phase: i for i, phase in enumerate(self.PHASES)}
        return phase_order[next] == phase_order[current] + 1
    
    def balance_quality_with_velocity(self, context: dict) -> str:
        """Balance between perfection and delivery.
        
        This embodies '미묘한 조절이나 균형의 묘' - maintaining quality
        standards while being pragmatic about time and resources.
        """
        if context["deadline_pressure"] == "high":
            # Still maintain quality gates, but focus on essentials
            return "essential_quality"
        elif context["complexity"] == "high":
            # Take more time for thorough validation
            return "comprehensive_quality"
        else:
            return "balanced_quality"
```

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

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-implement COMMAND:**

```python
# PHASE 1: Implementation
1. IMMEDIATELY CALL:
   Task("implementer-spark", user_request)

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - output.files.created is not empty
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 2
   ❌ ANY CONDITION FAILED → Task("implementer-spark", """
      Previous attempt failed quality checks:
      - Violations found: {specific violations}
      Please fix these issues and retry.
      """)

# PHASE 2: Testing
5. CALL:
   Task("tester-spark", "Create comprehensive tests for the implementation")

6. WAIT for agent completion

7. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.step_6_testing.coverage >= 95
   - output.tests.unit > 0
   - quality.can_proceed == true
   - state.status == "completed"

8. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 3
   ❌ ANY CONDITION FAILED → Task("tester-spark", """
      Testing requirements not met:
      - Current coverage: {coverage}%
      - Target: 95%
      Please improve test coverage.
      """)

# PHASE 3: Documentation
9. CALL:
   Task("documenter-spark", "Document the feature comprehensively")

10. WAIT for agent completion

11. CHECK ~/.claude/workflows/current_task.json:
    REQUIRED CONDITIONS:
    - output.docs.readme == true
    - output.docs.api == true
    - quality.can_proceed == true
    - state.status == "completed"

12. FINAL DECISION:
    ✅ ALL CONDITIONS MET → Report to user: "Implementation complete with tests and documentation"
    ❌ ANY CONDITION FAILED → Task("documenter-spark", """
       Documentation incomplete:
       - README: {status}
       - API docs: {status}
       Please complete all documentation.
       """)
```

⚡ **Core Principle**: Claude CODE reviews JSON results at each phase and decides next agent invocation

## 📝 Orchestration Process

### Phase 1: Implementation
Claude CODE will delegate to implementer-spark specialist:

1. **Task Assignment**: Request the implementer-spark specialist to implement the feature
2. **Quality Validation**: The SPARK quality gates hook automatically validates:
   - Syntax correctness (0 errors)
   - Type checking (MyPy 0 errors)
   - Linting compliance (Ruff 0 violations)
   - Security scanning (0 issues)
   - Documentation presence (docstrings required)
3. **Auto-Retry**: If quality gates fail, the specialist automatically retries (max 3 attempts)

**Quality Review Checklist:**
- ✅ Syntax validation (0 errors)
- ✅ Type checking (MyPy 0 errors)  
- ✅ Linting (Ruff 0 violations)
- ✅ Security scan (0 issues)
- ✅ Documentation (Docstrings required)

**Phase 1 → Phase 2 Decision by Claude CODE:**
- Review `implementation` section in current_task.json
- Check quality_metrics in the JSON
- If satisfied → Call tester-spark
- If issues found → Call implementer-spark again with feedback

### Phase 2: Testing
After Claude CODE approves implementation, call tester-spark specialist:

1. **Test Development**: Request comprehensive test creation with 95%+ coverage target
2. **Test Validation**: The test runner hook automatically verifies:
   - All tests passing (0 failures)
   - Coverage ≥ 95% (target achievement)
   - Edge cases covered (boundary testing)
   - Integration tests exist (system testing)
3. **Coverage Retry**: If coverage is below 95%, the specialist enhances tests (max 2 attempts)

**Test Quality Review:**
- ✅ All tests passing (0 failures)
- ✅ Coverage ≥ 95% (target achieved)
- ✅ Edge cases covered (boundary testing)
- ✅ Integration tests exist (system testing)

**Phase 2 → Phase 3 Decision by Claude CODE:**
- Review `testing` section in current_task.json
- Check test coverage (target: 95%+)
- If satisfied → Call documenter-spark
- If issues found → Call tester-spark again with feedback

### Phase 3: Documentation
After Claude CODE approves testing, call documenter-spark specialist:

1. **Documentation Creation**: Request comprehensive documentation including:
   - README updates with new features
   - API documentation for new endpoints
   - Usage examples and code samples
   - Inline docstrings for all functions
2. **Final Report**: Generate completion report with all deliverables

**Phase 3 Completion Criteria:**
- README.md updated
- API documentation complete (if applicable)
- Usage examples added
- All functions/classes have docstrings
- Final implementation report generated

## 💡 Quality Standards

### Implementation Quality (Phase 1)
- **필수 통과 항목**: Syntax (0), MyPy (0), Ruff (0), Security (0), Docstrings (0)

### Testing Quality (Phase 2) 
- **필수 달성**: Coverage ≥95%, Test failures (0), Edge cases covered

### Documentation Quality (Phase 3)
- **필수 포함**: README updates, API docs, Usage examples, Inline docstrings

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