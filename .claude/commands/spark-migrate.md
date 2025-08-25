# /spark-migrate - SPARK Legacy Migration & Modernization Pipeline  

**Purpose**: Comprehensive legacy system migration with risk assessment and modern implementation

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-migrate COMMAND:**

```python
# PHASE 1: Analysis
1. IMMEDIATELY CALL:
   Task("analyzer-spark", user_request + " - migration analysis")

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 2
   ❌ ANY CONDITION FAILED → Task("analyzer-spark", "Complete migration analysis")

# PHASE 2: Design
5. CALL:
   Task("designer-spark", "Design new architecture for migration")

6. WAIT for agent completion

7. CHECK current_task.json

8. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 3
   ❌ ANY CONDITION FAILED → Task("designer-spark", "Complete design")

# PHASE 3: Implementation
9. CALL:
   Task("implementer-spark", "Implement migration")

10. WAIT for agent completion

11. CHECK current_task.json

12. DECISION:
    ✅ ALL CONDITIONS MET → Proceed to Phase 4
    ❌ ANY CONDITION FAILED → Task("implementer-spark", "Fix issues: {violations}")

# PHASE 4: Testing
13. CALL:
    Task("tester-spark", "Test migrated system")

14. WAIT for agent completion

15. CHECK current_task.json:
    - quality.step_6_testing.coverage >= 95

16. FINAL DECISION:
    ✅ ALL CONDITIONS MET → Report: "Migration complete"
    ❌ ANY CONDITION FAILED → Task("tester-spark", "Improve coverage")
```


## Usage Examples

```bash
/spark-migrate "migrate PHP legacy system to modern Node.js architecture"
/spark-migrate "modernize jQuery frontend to React with TypeScript"
/spark-migrate "move from monolithic Rails app to microservices"
/spark-migrate "migrate SQL Server database to PostgreSQL with optimization"
/spark-migrate "convert legacy REST API to GraphQL with better performance"
