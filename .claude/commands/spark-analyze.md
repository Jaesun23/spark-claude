# /spark-analyze - SPARK Analysis Command

**Purpose**: Multi-dimensional code and system analysis with evidence-based investigation

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-analyze COMMAND:**

```python
1. IMMEDIATELY CALL:
   Task("analyzer-spark", user_request)

2. WAIT for agent completion

3. CHECK ~/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"

4. DECISION:
   ✅ ALL CONDITIONS MET → Report analysis results to user
   ❌ ANY CONDITION FAILED → Task("analyzer-spark", """
      Previous analysis incomplete or failed quality checks.
      Please complete the analysis and fix issues: {violations}
      """)
```

The analyzer-spark specialist will:
- Conduct comprehensive multi-perspective analysis
- Examine code from performance, security, and quality angles
- Provide evidence-based insights with specific metrics
- Generate actionable recommendations for improvements

## Usage Examples

```bash
/spark-analyze "performance bottlenecks in the authentication system"
/spark-analyze "security vulnerabilities in API endpoints"
/spark-analyze "code complexity and maintainability metrics"
/spark-analyze "dependency relationships and potential issues"
/spark-analyze "memory usage patterns in the data processing pipeline"
```

## Analysis Capabilities

- **Performance Analysis**: Bottlenecks, memory usage, optimization opportunities
- **Security Analysis**: Vulnerabilities, attack vectors, compliance issues  
- **Code Quality**: Complexity metrics, maintainability scores, technical debt
- **Architecture**: Structure analysis, coupling patterns, design issues
- **Dependencies**: Vulnerability scanning, usage optimization, conflict detection

## SPARK Intelligence Integration

- 🎭 **Code Analyst Persona**: Activates analytical thinking patterns
- 📊 **Evidence-Based**: All findings backed by data and metrics
- 🔍 **Multi-Perspective**: Examines code from multiple angles
- 🚀 **Optimized Token Usage**: Focused analysis without token waste