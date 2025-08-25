# /spark-fix - SPARK Troubleshooting Command

**Purpose**: Problem investigation, debugging, and root cause analysis with SPARK intelligence

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-fix COMMAND:**

```python
1. IMMEDIATELY CALL:
   Task("troubleshooter-spark", user_request)

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - output.files.modified is not empty
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Report fix complete to user
   ❌ ANY CONDITION FAILED → Task("troubleshooter-spark", "Complete the fix: {issues}")
```

The troubleshooter-spark specialist will:
- Systematically investigate the reported issue
- Analyze error patterns, logs, and stack traces
- Apply scientific debugging methods to isolate root causes
- Develop targeted fixes with minimal side effects
- Verify solutions thoroughly to prevent regressions

## Usage Examples

```bash
/spark-fix "API endpoints returning 500 errors intermittently"
/spark-fix "memory leak in the data processing pipeline"
/spark-fix "tests failing after dependency update" 
/spark-fix "performance degradation in search functionality"
/spark-fix "authentication system not working in production"
```

## Troubleshooting Capabilities

- **Error Investigation**: Systematic analysis of logs, stack traces, and error patterns
- **Performance Debugging**: Profiling, bottleneck identification, optimization
- **Integration Issues**: API failures, database connectivity, service communication
- **Environment Problems**: Configuration, deployment, dependency conflicts
- **Code Logic Bugs**: Logic errors, edge cases, race conditions

## Debugging Process

SPARK troubleshooting follows systematic approach:
1. **Problem Reproduction**: Isolate and reproduce the issue consistently
2. **Root Cause Analysis**: Trace the issue to its underlying cause
3. **Solution Development**: Create targeted fix with minimal side effects
4. **Verification**: Test fix thoroughly and ensure no regressions
5. **Prevention**: Suggest improvements to prevent similar issues

## SPARK Intelligence Integration

- 🎭 **Debugger Persona**: Activates systematic problem-solving patterns
- 🔍 **Evidence-Based**: All conclusions backed by logs, metrics, and testing
- 🧪 **Hypothesis Testing**: Scientific approach to isolating issues
- 🚀 **Optimized Token Usage**: Focused debugging without information overload