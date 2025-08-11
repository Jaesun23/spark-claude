# /implement - SPARK Implementation Command

**Purpose**: Quality-driven implementation workflow with 2호's intelligent orchestration and optimized token efficiency

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

## 📝 Claude CODE Action Protocol

### **UPON RECEIVING /implement COMMAND:**
```python
# Claude CODE's ORCHESTRATION PROTOCOL (systematic 3-phase execution)
1. Task("implementer-spark", user_request)  # CALL IMMEDIATELY
2. Wait for SubagentStop hook signal
3. Claude CODE reviews current_task.json:
   - Check `implementation` section
   - Review quality_metrics (linting, type checking)
   - Verify files_created and files_modified
   - Review next_steps and known_issues
4. DECISION:
   ✅ If satisfied → Task("tester-spark", implementation_context)
   ❌ If issues found → Task("implementer-spark", retry_with_feedback)

5. Wait for tester SubagentStop hook signal  
6. Claude CODE reviews current_task.json:
   - Check `testing` section
   - Verify test coverage (target: 95%+)
   - Confirm all tests passing
   - Review test quality metrics
7. DECISION:
   ✅ If satisfied → Task("documenter-spark", context)
   ❌ If issues found → Task("tester-spark", retry_with_feedback)

8. Wait for documenter SubagentStop hook signal
9. Claude CODE reviews current_task.json:
   - Check `documentation` section
   - Verify README updates
   - Confirm API documentation
   - Review usage examples
10. FINAL DECISION:
    ✅ All phases complete → Report success to user
    ❌ Issues found → Task("documenter-spark", retry_with_feedback)
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