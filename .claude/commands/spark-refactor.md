# /spark-refactor - SPARK Multi-Agent Refactoring Pipeline

**Purpose**: Complete code refactoring with analysis, improvement, testing, and documentation

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-refactor COMMAND:**

```python
# PHASE 1: Analysis
1. IMMEDIATELY CALL:
   Task("analyzer-spark", user_request)

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 2
   ❌ ANY CONDITION FAILED → Task("analyzer-spark", "Retry analysis with focus on: {issues}")

# PHASE 2: Improvement
5. CALL:
   Task("improver-spark", "Refactor based on analysis findings")

6. WAIT for agent completion

7. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - output.files.modified is not empty
   - state.status == "completed"

8. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 3
   ❌ ANY CONDITION FAILED → Task("improver-spark", "Fix quality issues: {violations}")

# PHASE 3: Testing
9. CALL:
   Task("tester-spark", "Test refactored code thoroughly")

10. WAIT for agent completion

11. CHECK ~/.claude/workflows/current_task.json:
    REQUIRED CONDITIONS:
    - quality.step_6_testing.coverage >= 95
    - quality.can_proceed == true
    - state.status == "completed"

12. FINAL DECISION:
    ✅ ALL CONDITIONS MET → Report: "Refactoring complete with {coverage}% test coverage"
    ❌ ANY CONDITION FAILED → Task("tester-spark", "Improve test coverage to 95%")
```


## Usage Examples

```bash
/spark-refactor "refactor authentication module for better maintainability"
/spark-refactor "modernize legacy API endpoints to follow REST standards"
/spark-refactor "optimize database queries and improve performance"
/spark-refactor "restructure component hierarchy for better reusability"
