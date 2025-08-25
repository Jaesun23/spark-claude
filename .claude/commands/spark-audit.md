# /spark-audit - SPARK Security & Performance Audit Pipeline

**Purpose**: Complete project audit covering security, performance, and quality with actionable reports

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-audit COMMAND:**

```python
# PHASE 1: Analysis
1. IMMEDIATELY CALL:
   Task("analyzer-spark", user_request + " - comprehensive audit")

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 2
   ❌ ANY CONDITION FAILED → Task("analyzer-spark", "Complete audit analysis")

# PHASE 2: Troubleshooting
5. CALL:
   Task("troubleshooter-spark", "Fix critical issues found in audit")

6. WAIT for agent completion

7. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - output.files.modified is not empty
   - state.status == "completed"

8. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 3
   ❌ ANY CONDITION FAILED → Task("troubleshooter-spark", "Address remaining issues: {issues}")

# PHASE 3: Documentation
9. CALL:
   Task("documenter-spark", "Create comprehensive audit report")

10. WAIT for agent completion

11. CHECK ~/.claude/workflows/current_task.json:
    REQUIRED CONDITIONS:
    - output.docs.readme == true
    - quality.can_proceed == true
    - state.status == "completed"

12. FINAL DECISION:
    ✅ ALL CONDITIONS MET → Report: "Audit complete with report generated"
    ❌ ANY CONDITION FAILED → Task("documenter-spark", "Complete audit documentation")
```


## Usage Examples

```bash
/spark-audit "complete security and performance audit of the API layer"
/spark-audit "audit user authentication and authorization systems"  
/spark-audit "comprehensive review of data processing pipeline"
/spark-audit "audit payment processing system for compliance"
