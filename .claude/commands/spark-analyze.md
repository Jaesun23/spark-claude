---
name: spark-analyze  
description: Multi-dimensional system analysis with evidence-based investigation across performance, security, quality, architecture, and dependencies
type: command
requires: analyzer-spark
---

# /spark-analyze - Multi-Dimensional Analysis Command

**Purpose**: Analysis is an art of systematic investigation where multiple perspectives converge to reveal truth, understanding systems through every lens to discover where they excel, struggle, and how to improve.

## Philosophy (Natural Language Inspiration)

Understanding comes not from a single viewpoint, but from examining systems through multiple lenses. Each analysis tells a story:

- **Where the system excels** and should be preserved
- **Where it struggles** and needs attention
- **What paths lead to improvement** with actionable steps

Every finding must be backed by evidence, every recommendation grounded in data. We analyze not to criticize, but to understand and improve.

## Behavior Protocol (Code-Based Execution)

```python
class SparkAnalyzeCommand:
    """Multi-dimensional analysis with evidence-based investigation.
    
    This protocol ensures systematic analysis while the philosophy above
    provides the wisdom to interpret findings. Together they reveal truth.
    """
    
    # Analysis perspectives - COMPREHENSIVE
    PERSPECTIVES = [
        "performance",     # Execution efficiency
        "security",       # Vulnerabilities and risks
        "quality",        # Maintainability and debt
        "architecture",   # Structural integrity
        "dependencies"    # External risks
    ]
    
    # Evidence requirements - NO CLAIMS WITHOUT DATA
    EVIDENCE_REQUIRED = True
    METRICS_BASED = True
    ACTIONABLE_ONLY = True
    
    def analyze_system(self, codebase: dict) -> dict:
        """Systematic investigation from multiple angles."""
        findings = {}
        
        # Examine from each perspective
        for perspective in self.PERSPECTIVES:
            findings[perspective] = self.measure_perspective(
                codebase, 
                perspective
            )
        
        # Cross-reference findings for patterns
        patterns = self.identify_cross_perspective_issues(findings)
        
        # Generate prioritized recommendations
        return self.synthesize_insights(findings, patterns)
    
    def validate_finding(self, claim: str, evidence: dict) -> bool:
        """Never make claims without data."""
        return (
            evidence.get("metrics") is not None and
            evidence.get("examples") != [] and
            evidence.get("impact") is not None
        )
    
    def balance_depth_with_breadth(self, context: dict) -> str:
        """Balance between deep investigation and broad coverage.
        
        This embodies '미묘한 조절이나 균형의 묘' - knowing when
        to dig deep versus when to survey broadly.
        """
        if context["scope"] == "focused":
            return "deep_dive_analysis"
        elif context["time_available"] == "limited":
            return "rapid_assessment"
        else:
            return "balanced_analysis"
```

## 📝 2호(Claude Code) MUST FOLLOW THIS EXACT PROTOCOL

### **WHEN RECEIVING /spark-analyze COMMAND:**

```python
1. INITIAL ASSESSMENT:
   # Check if multi-session state exists
   state_file = ".claude/workflows/analyze_state.yaml"
   
   if exists(state_file):
      state = load_yaml(state_file)
      print(f"📂 이전 분석 발견 (진행률: {state['progress']['overall_percentage']}%)")
      print(f"🎯 다음 우선순위: {state['next_session']['focus']}")
      
      # Provide context to agent
      Task("analyzer-spark", f"""
         {user_request}
         
         PREVIOUS STATE EXISTS:
         - Sessions completed: {state['sessions_completed']}
         - Progress: {state['progress']['overall_percentage']}%
         Continue from saved state.
      """)
   else:
      # New analysis
      Task("analyzer-spark", user_request)

2. WAIT for agent completion

3. CHECK PROJECT/.claude/workflows/current_task.json:
   REQUIRED CONDITIONS:
   - quality.violations_total == 0
   - quality.can_proceed == true
   - state.status == "completed"

4. CHECK FOR MULTI-SESSION:
   if exists(state_file):
      state = load_yaml(state_file)
      
      if state['progress']['overall_percentage'] < 100:
         print(f"""
         📊 분석 진행 상황: {state['progress']['overall_percentage']}%
         🎯 다음 세션 포커스: {state['next_session']['focus']}
         
         대규모 코드베이스 분석이 진행 중입니다.
         계속하려면: /spark-analyze --continue
         
         또는 자동으로 계속 진행하시겠습니까? (Y/n)
         """)
         
         if user_confirms or "--auto" in request:
            # Continue automatically
            goto step 1 with "--continue" flag
         else:
            # Wait for user to resume
            return
      else:
         print("✅ 멀티세션 분석 완료!")

5. FINAL DECISION:
   ✅ ALL CONDITIONS MET → Report complete analysis results
   ❌ ANY CONDITION FAILED → Task("analyzer-spark", """
      Previous analysis incomplete or failed quality checks.
      Please complete the analysis and fix issues: {violations}
      """)
```

### **Multi-Session Orchestration Protocol:**

When analyzer-spark creates a state file, 2호 must:

1. **Recognize Multi-Session Need**: Large codebases require progressive analysis
2. **Monitor Progress**: Check state file for completion percentage
3. **Intelligent Continuation**: 
   - Offer to continue automatically
   - Show progress and next focus area
   - Allow user to review intermediate results
4. **Session Management**:
   ```python
   # Maximum 10 sessions for any analysis
   if state['sessions_completed'] >= 10:
      print("⚠️ 분석이 10세션을 초과했습니다. 범위를 재조정하세요.")
   
   # Intelligent resumption
   if time_since_last_session > 24_hours:
      print("💡 이전 분석이 24시간 전입니다. 컨텍스트 요약:")
      print(state['last_session_summary'])
   ```

The analyzer-spark specialist will:
- Conduct comprehensive multi-perspective analysis
- **Automatically plan multi-session strategy for large codebases**
- **Save progress state between sessions**
- **Resume from previous state intelligently**
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