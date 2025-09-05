---
name: spark-fix
description: Systematic troubleshooting and issue resolution with root cause analysis
type: command
requires: troubleshooter-spark
---

# /spark-fix - Intelligent Troubleshooting Command

**Purpose**: Troubleshooting is detective work where every clue matters, systematically uncovering root causes and crafting solutions that prevent recurrence.

## Philosophy (Natural Language Inspiration)

Great troubleshooting goes beyond fixing symptoms to understand why problems occur. We approach issues with:

- **Systematic investigation**: Follow evidence, not assumptions
- **Root cause focus**: Fix the source, not just the symptom  
- **Prevention mindset**: Solutions that prevent future occurrences
- **Clear documentation**: Share knowledge to help others

Every bug is a teacher - listen to what it's trying to tell you about the system.

## Behavior Protocol (Code-Based Execution)

```python
class SparkFixCommand:
    """Systematic troubleshooting with evidence-based resolution.
    
    This protocol ensures thorough investigation while the philosophy above
    guides interpretation and solution design. Together they solve problems.
    """
    
    # Investigation phases - SYSTEMATIC APPROACH
    INVESTIGATION_PHASES = [
        "symptom_analysis",
        "reproduction",
        "root_cause_analysis", 
        "solution_design",
        "validation"
    ]
    
    # Evidence requirements - DATA-DRIVEN
    EVIDENCE_STANDARDS = {
        "reproduction_steps": True,
        "error_logs_captured": True,
        "environment_documented": True,
        "fix_tested": True
    }
    
    def troubleshoot_issue(self, problem_description: str) -> dict:
        """Main troubleshooting flow with systematic investigation."""
        investigation = {
            "symptoms": self.analyze_symptoms(problem_description),
            "reproduction": self.reproduce_issue(problem_description),
            "root_cause": None,
            "solution": None
        }
        
        # Follow evidence trail to root cause
        investigation["root_cause"] = self.find_root_cause(
            investigation["symptoms"],
            investigation["reproduction"]
        )
        
        # Design targeted solution
        investigation["solution"] = self.design_solution(
            investigation["root_cause"]
        )
        
        # Validate fix works and doesn't break anything else
        validation = self.validate_solution(investigation["solution"])
        
        return self.document_resolution(investigation, validation)
    
    def balance_speed_with_thoroughness(self, context: dict) -> str:
        """Balance quick fixes with comprehensive solutions.
        
        Embodies '미묘한 조절이나 균형의 묘' - knowing when to patch
        quickly versus when to investigate thoroughly.
        """
        if context["severity"] == "critical":
            return "rapid_mitigation_then_thorough_fix"
        elif context["recurring_issue"] == True:
            return "deep_root_cause_analysis"
        else:
            return "balanced_investigation"
```
