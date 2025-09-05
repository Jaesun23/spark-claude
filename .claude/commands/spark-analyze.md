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