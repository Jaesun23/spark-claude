---
name: spark-improve
description: Code quality enhancement and performance optimization with refactoring expertise
type: command
requires: improver-spark
---

# /spark-improve - Intelligent Code Improvement Command

**Purpose**: Improvement is the art of making good code great, enhancing what exists while preserving what works, guided by evidence and measured by impact.

## Philosophy (Natural Language Inspiration)

Code improvement requires both vision and restraint - seeing potential while respecting current functionality. We approach enhancement with:

- **Evidence-based changes**: Every improvement backed by metrics
- **Incremental evolution**: Small steps toward large improvements
- **Quality without disruption**: Better code that still works perfectly
- **Performance with purpose**: Optimize what matters most

The best improvements feel inevitable in retrospect - obvious solutions that somehow weren't obvious before.

## Behavior Protocol (Code-Based Execution)

```python
class SparkImproveCommand:
    """Intelligent improvement with systematic quality enhancement.
    
    This protocol ensures measurable improvements while the philosophy above
    guides what to change versus what to preserve. Progress with stability.
    """
    
    # Improvement dimensions - HOLISTIC ENHANCEMENT
    IMPROVEMENT_AREAS = {
        "performance": ["algorithmic", "memory", "io", "caching"],
        "maintainability": ["readability", "modularity", "documentation"],
        "reliability": ["error_handling", "edge_cases", "testing"],
        "security": ["vulnerabilities", "best_practices", "hardening"]
    }
    
    # Quality metrics - MEASURABLE PROGRESS
    IMPROVEMENT_METRICS = {
        "performance_gain": "> 20%",
        "complexity_reduction": "> 15%", 
        "test_coverage_increase": "> 10%",
        "maintainability_score": "> 0.8"
    }
    
    def improve_codebase(self, focus_area: str) -> dict:
        """Main improvement orchestration with metrics validation."""
        baseline = self.establish_baseline_metrics()
        
        improvement_plan = self.analyze_improvement_opportunities(
            focus_area, baseline
        )
        
        # Apply improvements incrementally with validation
        results = []
        for improvement in improvement_plan["prioritized_changes"]:
            result = self.apply_improvement_safely(improvement)
            
            # Measure impact
            new_metrics = self.measure_improvement_impact(baseline)
            if not self.meets_improvement_thresholds(new_metrics):
                self.revert_change(improvement)
                continue
                
            results.append(result)
            baseline = new_metrics  # New baseline for next improvement
        
        return self.generate_improvement_report(baseline, results)
    
    def balance_optimization_with_readability(self, context: dict) -> str:
        """Balance performance gains with code clarity.
        
        Embodies '미묘한 조절이나 균형의 묘' - sometimes slower,
        clearer code is better than fast, cryptic code.
        """
        if context["team_experience"] == "junior":
            return "readability_first"
        elif context["performance_critical"] == True:
            return "optimization_focused"
        else:
            return "balanced_improvement"
```
