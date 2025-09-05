---
name: spark-refactor
description: Code refactoring pipeline with analysis, improvement, and testing phases for better maintainability
type: command
requires: analyzer-spark, improver-spark, tester-spark
---

# /spark-refactor - Intelligent Refactoring Command

**Purpose**: Refactoring is the art of improving code's internal structure while preserving its external behavior, making tomorrow's changes easier without changing today's functionality.

## Philosophy (Natural Language Inspiration)

Refactoring is like renovating a house while people still live in it - careful, respectful, and focused on making life better. We approach refactoring with:

- **Behavior preservation**: External behavior remains exactly the same
- **Internal improvement**: Structure becomes clearer, more maintainable
- **Incremental progress**: Small steps that compound into significant improvement
- **Test-driven confidence**: Every change validated by comprehensive tests

The best refactoring makes code feel like it was always meant to be that way.

## Behavior Protocol (Code-Based Execution)

```python
class SparkRefactorCommand:
    """Intelligent refactoring with behavior-preserving transformation.
    
    This protocol ensures safe structural changes while the philosophy above
    guides what to preserve versus what to improve. Better structure, same behavior.
    """
    
    # Refactoring phases - SAFE TRANSFORMATION
    REFACTORING_PHASES = [
        "analysis",     # Understand current structure
        "improvement",  # Apply refactoring patterns
        "testing"       # Validate behavior preservation
    ]
    
    # Safety requirements - BEHAVIOR PRESERVATION
    SAFETY_CHECKS = {
        "all_tests_passing": True,
        "external_behavior_unchanged": True,
        "performance_not_degraded": True,
        "api_contracts_preserved": True
    }
    
    def refactor_codebase(self, refactor_scope: str) -> dict:
        """Main refactoring orchestration with safety validation."""
        refactor_state = {
            "baseline_behavior": self.capture_current_behavior(),
            "structure_improvements": [],
            "safety_validations": {},
            "refactoring_results": {}
        }
        
        for phase in self.REFACTORING_PHASES:
            result = self.execute_refactoring_phase(
                phase, refactor_scope, refactor_state
            )
            
            # Validate safety checks after each phase
            safety_check = self.validate_behavior_preservation(
                refactor_state["baseline_behavior"]
            )
            
            if not safety_check["behavior_preserved"]:
                return self.abort_refactoring_safely(
                    refactor_state, safety_check["violations"]
                )
            
            refactor_state[f"{phase}_result"] = result
        
        return self.complete_refactoring_successfully(refactor_state)
    
    def balance_improvement_with_stability(self, context: dict) -> str:
        """Balance structural improvements with system stability.
        
        Embodies '미묘한 조절이나 균형의 묘' - knowing when to refactor
        aggressively versus when to make conservative changes.
        """
        if context["system_maturity"] == "production_critical":
            return "conservative_refactoring"
        elif context["technical_debt"] == "severe":
            return "comprehensive_refactoring"
        else:
            return "balanced_refactoring"
```
