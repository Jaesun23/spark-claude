---
name: spark-optimize
description: Performance optimization pipeline with analysis, improvement, and testing phases
type: command
requires: analyzer-spark, improver-spark, tester-spark
---

# /spark-optimize - Intelligent Optimization Command

**Purpose**: Optimization is the art of doing more with less, finding efficiency without sacrificing clarity, speed without compromising reliability.

## Philosophy (Natural Language Inspiration)

True optimization improves the experience for everyone - developers, users, and systems alike. We approach optimization with:

- **Measurement-driven decisions**: Optimize what matters, measure what improves
- **Holistic thinking**: Consider performance, maintainability, and user experience together
- **Sustainable improvements**: Changes that compound over time
- **Evidence-based validation**: Every optimization proves its worth

The best optimizations make systems feel more responsive and code more elegant simultaneously.

## Behavior Protocol (Code-Based Execution)

```python
class SparkOptimizeCommand:
    """Intelligent optimization with evidence-based improvement.
    
    This protocol ensures measurable gains while the philosophy above
    guides sustainable decisions. Performance with purpose.
    """
    
    # Optimization phases - SYSTEMATIC IMPROVEMENT
    OPTIMIZATION_PHASES = [
        "analysis",     # Identify bottlenecks
        "improvement",  # Apply optimizations
        "testing"       # Validate improvements
    ]
    
    # Performance targets - MEASURABLE GAINS
    PERFORMANCE_TARGETS = {
        "response_time_improvement": "> 25%",
        "memory_usage_reduction": "> 15%",
        "throughput_increase": "> 20%",
        "code_quality_maintained": True
    }
    
    def optimize_system(self, focus_area: str) -> dict:
        """Main optimization orchestration with validation."""
        optimization_state = {
            "baseline_metrics": self.establish_performance_baseline(),
            "improvements_applied": [],
            "final_metrics": {},
            "validation_results": {}
        }
        
        for phase in self.OPTIMIZATION_PHASES:
            result = self.execute_optimization_phase(
                phase, focus_area, optimization_state
            )
            
            # Validate improvements meet targets
            if phase == "improvement":
                if not self.meets_performance_targets(result["metrics"]):
                    result = self.refine_optimizations(result)
            
            optimization_state[f"{phase}_result"] = result
        
        return self.finalize_optimization_report(optimization_state)
    
    def balance_speed_with_maintainability(self, context: dict) -> str:
        """Balance performance gains with code clarity.
        
        Embodies '미묘한 조절이나 균형의 묘' - fast code that's
        impossible to maintain is ultimately slower.
        """
        if context["performance_critical"] == "extreme":
            return "performance_first_with_documentation"
        elif context["team_size"] == "large":
            return "maintainability_focused_optimization"
        else:
            return "balanced_optimization"
```
