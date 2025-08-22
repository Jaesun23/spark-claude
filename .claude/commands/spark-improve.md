# /spark-improve - SPARK Code Improvement Command

**Purpose**: Systematic code improvement and technical debt reduction with SPARK intelligence

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-improve COMMAND:**

```python
1. IMMEDIATELY CALL:
   Task("improver-spark", user_request)

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - output.files.modified is not empty
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Report improvement complete to user
   ❌ ANY CONDITION FAILED → Task("improver-spark", "Fix quality issues: {violations}")
```

The improver-spark specialist will:
- Analyze code quality, performance, security, and architecture comprehensively
- Create systematic improvement plans using 5-Phase methodology
- Execute refactoring, optimization, and enhancement implementations
- Validate all changes through rigorous testing and quality gates
- Generate detailed improvement reports with before/after metrics

## 🚀 Usage Examples

```bash
/spark-improve "legacy authentication module with performance issues"
/spark-improve "database layer with N+1 queries and security vulnerabilities" 
/spark-improve "monolithic service with high complexity and technical debt"
/spark-improve "frontend components with poor performance and accessibility"
```

## 📊 Quality Standards

### Jason's 8-Step Quality Gates (Must Pass All)
1. **Syntax Validation** (0 errors)
2. **Type Checking** - MyPy --strict (0 errors)  
3. **Linting** - Ruff --strict (0 violations)
4. **Security Analysis** - OWASP + secrets scan
5. **Test Coverage** - Unit 95%, Integration 85%
6. **Performance Check** - No regression
7. **Documentation Validation** - Docstrings required
8. **Integration Testing** - E2E scenarios pass

### Success Criteria
- ✅ All 8 quality gates pass
- ✅ Code quality metrics improved measurably
- ✅ No breaking changes to public APIs
- ✅ Comprehensive improvement documentation generated

## 🎯 SPARK Efficiency

- **Direct Delegation**: Single agent handles complete lifecycle
- **5-Phase Methodology**: Built-in systematic approach
- **Auto-Retry**: Max 3 attempts on quality gate failures
- **Token Efficient**: No multi-agent coordination overhead
- **Self-Contained**: improver-spark includes analysis, implementation, testing, documentation