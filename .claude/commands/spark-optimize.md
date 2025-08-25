# /spark-optimize - SPARK Performance Optimization Pipeline

**Purpose**: Comprehensive performance optimization with analysis, implementation, and validation

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-optimize COMMAND:**

```python
# PHASE 1: Analysis
1. IMMEDIATELY CALL:
   Task("analyzer-spark", user_request + " - performance analysis")

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 2
   ❌ ANY CONDITION FAILED → Task("analyzer-spark", "Complete performance analysis")

# PHASE 2: Optimization
5. CALL:
   Task("improver-spark", "Optimize based on analysis")

6. WAIT for agent completion

7. CHECK current_task.json:
   - output.files.modified is not empty

8. DECISION:
   ✅ ALL CONDITIONS MET → Proceed to Phase 3
   ❌ ANY CONDITION FAILED → Task("improver-spark", "Complete optimization")

# PHASE 3: Testing
9. CALL:
   Task("tester-spark", "Test optimized code")

10. WAIT for agent completion

11. CHECK current_task.json:
    - quality.step_6_testing.coverage >= 95

12. FINAL DECISION:
    ✅ ALL CONDITIONS MET → Report: "Optimization complete"
    ❌ ANY CONDITION FAILED → Task("tester-spark", "Improve test coverage")
```


## Usage Examples

```bash
/spark-optimize "optimize API response times and database query performance"
/spark-optimize "improve frontend loading speed and bundle size optimization"
/spark-optimize "optimize memory usage and garbage collection in data processing"  
/spark-optimize "enhance search functionality performance with indexing strategies"
/spark-optimize "optimize image processing pipeline for faster throughput"
