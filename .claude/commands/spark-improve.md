# /spark-improve - SPARK Code Improvement Command

**Purpose**: Systematic code improvement workflow with multi-dimensional enhancement through specialized personas and quality validation

## 🚀 Multi-Dimensional Improvement Workflow

This command orchestrates comprehensive code improvement across quality, performance, and security dimensions with intelligent persona activation based on code analysis.

### Workflow Architecture
```
┌──────────────────┐
│ Analyzer-Spark   │ ←────┐
└────────┬─────────┘      │
         ↓                │ (Analysis retry)
    Analysis Complete ────┘
         ↓ (Issues identified)
┌──────────────────┐
│ Improver-Spark   │ ←────┐
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
    ✅ Improvement Report
```

## 📝 Claude CODE Action Protocol

### **UPON RECEIVING /spark-improve COMMAND:**
```python
# Claude CODE's IMPROVEMENT ORCHESTRATION PROTOCOL (4-phase execution)
1. Task("analyzer-spark", improvement_target)  # ANALYZE FIRST
2. Wait for SubagentStop hook signal
3. Claude CODE reviews current_task.json:
   - Check `analysis` section for identified issues
   - Review complexity score and improvement areas
   - Examine technical debt and performance bottlenecks
   - Identify security vulnerabilities
4. DECISION:
   ✅ If issues found → Task("improver-spark", analysis_context)
   ❌ If no improvements needed → Report to user

5. Wait for improver SubagentStop hook signal  
6. Claude CODE reviews current_task.json:
   - Check `improvement` section
   - Review quality_metrics (linting, type checking)
   - Verify refactoring outcomes
   - Review performance optimizations
7. DECISION:
   ✅ If satisfied → Task("tester-spark", improvement_context)
   ❌ If issues found → Task("improver-spark", retry_with_feedback)

8. Wait for tester SubagentStop hook signal
9. Claude CODE reviews current_task.json:
   - Check `testing` section
   - Verify test coverage maintained/improved
   - Confirm all tests passing
   - Review regression test results
10. DECISION:
    ✅ If satisfied → Task("documenter-spark", context)
    ❌ If issues found → Task("tester-spark", retry_with_feedback)

11. Wait for documenter SubagentStop hook signal
12. FINAL REVIEW:
    - Check `documentation` section
    - Verify improvement documentation
    - Confirm changelog updates
    - Review API documentation changes
13. FINAL DECISION:
    ✅ All phases complete → Report success to user
    ❌ Issues found → Task("documenter-spark", retry_with_feedback)
```

⚡ **Core Principle**: Analyzer identifies improvement opportunities, Improver implements changes, Tester validates, Documenter records

## 📝 Improvement Process

### Phase 1: Analysis & Planning
Claude CODE will delegate to analyzer-spark specialist:

1. **Multi-Dimensional Analysis**: Analyze target code for:
   - Code quality issues (technical debt, complexity)
   - Performance bottlenecks (CPU, memory, I/O)
   - Security vulnerabilities (OWASP, dependency issues)
   - Architecture problems (coupling, cohesion)
   
2. **Complexity Assessment**: Determines improvement scope:
   - **0.0-0.3**: Simple refactoring (local improvements)
   - **0.4-0.6**: Moderate improvements (module-level changes)
   - **0.7-1.0**: Wave mode (system-wide improvements with multiple personas)

3. **Persona Activation**: Based on analysis keywords:
   - **Refactorer**: Code quality, technical debt, complexity reduction
   - **Performance**: Optimization, scalability, resource usage
   - **Security**: Vulnerabilities, hardening, compliance
   - **Architect**: Structure, patterns, maintainability

**Analysis Review Checklist:**
- ✅ Technical debt identified and prioritized
- ✅ Performance bottlenecks analyzed
- ✅ Security vulnerabilities scanned
- ✅ Architecture issues documented
- ✅ Improvement plan with priorities created

### Phase 2: Systematic Improvement
After Claude CODE approves analysis, call improver-spark specialist:

1. **Improvement Implementation**: Execute systematic improvements:
   - Code quality: Extract methods, apply patterns, reduce complexity
   - Performance: Algorithm optimization, caching, query improvement
   - Security: Input validation, encryption, authentication hardening
   - Architecture: Dependency injection, decoupling, modularization

2. **Quality Gates**: Automatic validation during improvement:
   - Syntax correctness (0 errors)
   - Type checking (MyPy 0 errors)
   - Linting compliance (Ruff 0 violations)
   - Security scanning (0 new issues)
   - Performance benchmarking (no regression)

3. **Wave Mode Coordination**: For complex improvements (≥0.7):
   - Multiple personas work in coordinated phases
   - Sequential MCP for systematic planning
   - Context7 for improvement patterns and best practices
   - Playwright for performance measurement

**Improvement Quality Standards:**
- ✅ Code complexity reduced (Cyclomatic, Halstead metrics)
- ✅ Performance improved or maintained
- ✅ Security posture enhanced
- ✅ Maintainability increased
- ✅ No breaking changes introduced

### Phase 3: Validation & Testing
After Claude CODE approves improvements, call tester-spark specialist:

1. **Regression Testing**: Ensure improvements don't break existing functionality
2. **Performance Testing**: Validate performance improvements with benchmarks
3. **Security Testing**: Verify security enhancements are effective
4. **Coverage Maintenance**: Ensure test coverage remains ≥95%

**Testing Validation:**
- ✅ All existing tests pass (0 failures)
- ✅ Performance benchmarks improved or maintained
- ✅ Security tests validate improvements
- ✅ Coverage ≥ 95% maintained

### Phase 4: Documentation
After Claude CODE approves testing, call documenter-spark specialist:

1. **Improvement Documentation**: Document changes and rationale:
   - Improvement summary with before/after metrics
   - Performance benchmark results
   - Security enhancement details
   - Code quality metrics improvement
   
2. **Update Documentation**: Ensure all docs reflect improvements:
   - README updates if public APIs changed
   - Architecture documentation updates
   - Performance characteristics documentation
   - Security considerations updates

**Documentation Completion Criteria:**
- Improvement changelog with metrics
- Performance benchmark documentation
- Security enhancement summary  
- Architecture updates (if applicable)
- API documentation updates (if needed)

## 💡 Improvement Categories

### Code Quality Improvements
- **Technical Debt Reduction**: Simplify complex methods, extract classes
- **Pattern Application**: Apply design patterns, SOLID principles
- **Code Duplication**: Extract common functionality, create utilities
- **Naming & Structure**: Improve readability, consistent conventions

### Performance Improvements  
- **Algorithm Optimization**: Reduce time complexity, optimize data structures
- **Resource Management**: Memory optimization, connection pooling
- **Caching Strategy**: Add strategic caching layers
- **Database Optimization**: Query optimization, indexing, N+1 prevention

### Security Improvements
- **Input Validation**: Strengthen data validation and sanitization
- **Authentication**: Enhance auth mechanisms, session management
- **Encryption**: Implement proper data encryption
- **Dependency Security**: Update vulnerable dependencies

### Architecture Improvements
- **Separation of Concerns**: Better layer separation
- **Dependency Management**: Reduce coupling, improve testability
- **Modularity**: Break down monolithic components
- **Scalability**: Design for horizontal scaling

## 🚀 Usage Examples

```bash
/spark-improve "legacy authentication module with performance issues"
/spark-improve "database layer with N+1 queries and security vulnerabilities" 
/spark-improve "monolithic service with high complexity and technical debt"
/spark-improve "frontend components with poor performance and accessibility"
```

## 📊 SPARK Efficiency

- **Token Usage**: Lazy-loading architecture (only load required agents)
- **Quality Assurance**: 8 quality gates + retry system (max 3 attempts)  
- **Multi-Dimensional**: Code quality + performance + security simultaneously
- **Wave Mode**: Complex improvements with coordinated persona execution
- **JSON Communication**: Unified current_task.json for all phases

## 🎯 Improvement Metrics

### Before/After Tracking
- **Cyclomatic Complexity**: Target reduction of 20-40%
- **Performance Metrics**: Response time, memory usage, CPU utilization
- **Security Score**: Vulnerability count, security rating improvement
- **Code Quality**: Maintainability index, technical debt reduction
- **Test Coverage**: Maintain/improve coverage during improvements

### Success Criteria
- ✅ All quality gates pass (0 syntax/type/lint/security errors)
- ✅ Performance maintained or improved (benchmarks)
- ✅ Security posture enhanced (vulnerability reduction)
- ✅ Code quality metrics improved (complexity, maintainability)
- ✅ Test coverage ≥95% maintained
- ✅ No breaking changes to public APIs