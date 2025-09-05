---
name: spark-launch
description: Complete feature launch pipeline with design, implementation, testing, documentation, and deployment
type: command
requires: designer-spark, implementer-spark, tester-spark, documenter-spark, builder-spark
---

# /spark-launch - Complete Feature Launch Pipeline

**Purpose**: Launching is the moment when vision becomes reality, orchestrating every aspect from conception to delivery with the precision of a symphony and the care of a craftsperson.

## Philosophy (Natural Language Inspiration)

A successful launch touches every aspect of the development lifecycle. We approach launches with:

- **End-to-end thinking**: Every component working in harmony
- **Quality at every stage**: No shortcuts that compromise the whole
- **User-centered delivery**: Features that solve real problems elegantly
- **Sustainable practices**: Launches that set the foundation for future growth

Great launches feel effortless to users precisely because of the care taken behind the scenes.

## Behavior Protocol (Code-Based Execution)

```python
class SparkLaunchCommand:
    """Complete feature launch with systematic multi-phase execution.
    
    This protocol ensures comprehensive delivery while the philosophy above
    guides the vision and user experience. Excellence in every detail.
    """
    
    # Launch phases - COMPLETE PIPELINE
    LAUNCH_PHASES = [
        "design",
        "implementation", 
        "testing",
        "documentation",
        "deployment"
    ]
    
    # Quality gates per phase - NON-NEGOTIABLE
    PHASE_GATES = {
        "design": {"user_stories_complete": True, "accessibility_validated": True},
        "implementation": {"quality_violations": 0, "functionality_complete": True},
        "testing": {"coverage_target": 0.95, "all_tests_passing": True},
        "documentation": {"user_guide_complete": True, "api_docs_complete": True},
        "deployment": {"build_successful": True, "health_checks_passing": True}
    }
    
    def launch_feature(self, feature_spec: str) -> dict:
        """Complete launch orchestration with quality gates."""
        launch_state = {
            "current_phase": "design",
            "phases_completed": [],
            "quality_metrics": {},
            "deliverables": {}
        }
        
        for phase in self.LAUNCH_PHASES:
            launch_state["current_phase"] = phase
            
            # Execute phase with appropriate specialist
            result = self.execute_launch_phase(phase, feature_spec)
            
            # Validate phase gates
            if not self.validate_phase_gates(phase, result):
                result = self.retry_phase_with_improvements(phase, result)
                if not self.validate_phase_gates(phase, result):
                    return self.abort_launch_safely(launch_state, phase)
            
            # Update state and continue
            launch_state["phases_completed"].append(phase)
            launch_state["deliverables"][phase] = result["deliverables"]
            
        return self.finalize_successful_launch(launch_state)
    
    def balance_completeness_with_timeline(self, context: dict) -> str:
        """Balance comprehensive launch with delivery timeline.
        
        Embodies '미묘한 조절이나 균형의 묘' - knowing what can be
        deferred versus what must be perfect for launch.
        """
        if context["market_window"] == "critical":
            return "mvp_launch_with_roadmap"
        elif context["feature_complexity"] == "high":
            return "phased_launch_approach"
        else:
            return "complete_launch"
```
