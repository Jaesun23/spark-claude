---
name: spark-audit
description: Complete project audit orchestrating analysis, troubleshooting, and documentation phases with security and performance focus
type: command
requires: analyzer-spark, troubleshooter-spark, documenter-spark
---

# /spark-audit - Comprehensive System Audit Pipeline

**Purpose**: Systematic investigation that reveals not just what is wrong, but what is right, providing a complete picture of system health with actionable insights for improvement.

## Philosophy (Natural Language Inspiration)

Audit is more than finding flaws - it's understanding the complete story of a system. We approach auditing with:

- **Thoroughness without paralysis**: Be comprehensive but focused on impact
- **Evidence-based conclusions**: Every finding backed by data and examples
- **Balanced perspective**: Acknowledge what works well alongside areas for improvement
- **Actionable outcomes**: Every problem comes with a path to resolution

The best audit reveals opportunities, not just obstacles.

## Behavior Protocol (Code-Based Execution)

```python
class SparkAuditCommand:
    """Comprehensive system audit with systematic investigation.
    
    This protocol ensures thorough coverage while the philosophy above
    guides interpretation and reporting. Together they create valuable insights.
    """
    
    # Audit phases - SEQUENTIAL EXECUTION
    PHASES = ["analysis", "troubleshooting", "documentation"]
    
    # Audit scope - COMPREHENSIVE
    AUDIT_AREAS = {
        "security": ["vulnerabilities", "access_control", "data_protection"],
        "performance": ["bottlenecks", "scalability", "resource_usage"],
        "quality": ["maintainability", "testability", "documentation"],
        "compliance": ["standards", "best_practices", "regulations"]
    }
    
    # Quality gates for audit completion
    COMPLETION_CRITERIA = {
        "critical_issues_addressed": True,
        "findings_documented": True,
        "recommendations_actionable": True,
        "evidence_provided": True
    }
    
    def conduct_audit(self, scope: str) -> dict:
        """Main audit orchestration with systematic phases."""
        audit_results = {
            "findings": {},
            "fixes_applied": [],
            "report_generated": False
        }
        
        # Execute phases in order
        for phase in self.PHASES:
            result = self.execute_audit_phase(phase, scope)
            
            if not self.validate_phase_completion(phase, result):
                # Retry with enhanced context
                result = self.retry_phase_with_context(phase, result)
            
            audit_results = self.merge_phase_results(audit_results, result)
        
        return self.finalize_audit(audit_results)
    
    def balance_depth_with_practicality(self, context: dict) -> str:
        """Balance thorough investigation with practical outcomes.
        
        Embodies '미묘한 조절이나 균형의 묘' - knowing when findings
        are sufficient versus when deeper investigation is needed.
        """
        if context["risk_level"] == "high":
            return "exhaustive_audit"
        elif context["time_constraint"] == "tight":
            return "focused_audit"
        else:
            return "comprehensive_audit"
```

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
